"""Compliance Rule Engine (M6, Bible §3.x, ADR-005) — rules as data, not code (CP-6).

Evaluates a versioned rule library (effective-date ranges, BR-5) against graph state and
produces evidence + gaps attributed to a clause — never a legal opinion (BR-3), and always
disclosing encoded-vs-total clause coverage (FM-6). The engine is regulation-agnostic; the same
engine serves OISD today and OSHA/ATEX later without a rewrite.
"""
from __future__ import annotations

from datetime import date

from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import ComplianceRow, CoverageReport, ObligationStatus
from ..ports import IGraphStore, IRelationalStore

_RULE = "compliance_rule"


class RuleEngine:
    def __init__(self, graph: IGraphStore, relational: IRelationalStore) -> None:
        self._g = graph
        self._rel = relational

    def load_rules(self, tenant: str) -> list[dict]:
        return self._rel.list(_RULE, tenant)

    def evaluate_asset(self, asset_id: str, tenant: str, as_of: date | None = None) -> list[ComplianceRow]:
        as_of = as_of or date.today()
        rows: list[ComplianceRow] = []
        asset = self._g.get_node(asset_id)
        if not asset:
            return rows
        asset_tag = str(asset.props.get("tag") or asset_id)
        # Obligations that GOVERN this asset (Bible §5.8 compliance Cypher, applied in-code).
        for ob in self._g.nodes_by_label(NodeLabel.OBLIGATION.value, tenant):
            governs = any(
                e.dst == asset_id for e in self._g.edges_from(ob.id, EdgeType.GOVERNS.value, tenant)
            )
            if not governs:
                continue
            # only rules effective as-of the evaluation date (BR-5)
            eff_from = ob.props.get("effective_from")
            if eff_from and date.fromisoformat(eff_from) > as_of:
                continue
            periodicity = int(ob.props.get("periodicity_months", 12))
            instrument, authority = self._instrument_of(ob.id, tenant)
            last_date, last_doc, last_span = self._last_evidence(asset_id, tenant)
            status = self._status(last_date, periodicity, as_of)
            rows.append(
                ComplianceRow(
                    clause=str(ob.props.get("clause", ob.id)),
                    instrument=instrument,
                    authority=authority,
                    asset_id=asset_id,
                    asset_tag=asset_tag,
                    periodicity_months=periodicity,
                    last_evidence_date=last_date,
                    last_evidence_doc=last_doc,
                    last_evidence_span=last_span,
                    status=status,
                )
            )
        return rows

    def _instrument_of(self, ob_id: str, tenant: str) -> tuple[str, str]:
        for e in self._g.edges_from(ob_id, EdgeType.DEFINED_IN.value, tenant):
            inst = self._g.get_node(e.dst)
            if inst:
                return str(inst.props.get("name", "?")), str(inst.props.get("authority", "?"))
        return "?", "?"

    def _last_evidence(self, asset_id: str, tenant: str) -> tuple[date | None, str | None, str | None]:
        latest: date | None = None
        doc: str | None = None
        span: str | None = None
        for etype in (EdgeType.HAS_INSPECTION.value, EdgeType.HAS_WORKORDER.value):
            for e in self._g.edges_from(asset_id, etype, tenant):
                n = self._g.get_node(e.dst)
                if not n:
                    continue
                raw = n.props.get("date") or n.props.get("opened")
                if not raw:
                    continue
                d = date.fromisoformat(str(raw)[:10])
                if latest is None or d > latest:
                    latest = d
                    spans = self._g.evidence_spans(n.id, tenant)
                    if spans:
                        doc, span = spans[0].doc_id, spans[0].span_id
        return latest, doc, span

    @staticmethod
    def _status(last: date | None, periodicity_months: int, as_of: date) -> ObligationStatus:
        if last is None:
            return ObligationStatus.OVERDUE  # no evidence at all is overdue, not "unknown"
        # crude month math is sufficient for the interval check
        months_elapsed = (as_of.year - last.year) * 12 + (as_of.month - last.month)
        if months_elapsed > periodicity_months:
            return ObligationStatus.OVERDUE
        if months_elapsed >= periodicity_months - 1:
            return ObligationStatus.DUE
        return ObligationStatus.SATISFIED

    def coverage(self, tenant: str) -> CoverageReport:
        rules = self.load_rules(tenant)
        by_instrument: dict[str, dict[str, int]] = {}
        for r in rules:
            inst = r.get("instrument", "?")
            slot = by_instrument.setdefault(inst, {"encoded": 0, "total": 0})
            slot["total"] += r.get("total_clauses_in_instrument", 1)
            slot["encoded"] += 1
        encoded = sum(v["encoded"] for v in by_instrument.values())
        total = sum(v["total"] for v in by_instrument.values())
        return CoverageReport(
            encoded_clauses=encoded,
            total_applicable_clauses=max(total, encoded),
            by_instrument=by_instrument,
            disclaimer=f"Encoded clauses: {encoded} of {max(total, encoded)}. "
            "This is not a completeness guarantee.",
        )
