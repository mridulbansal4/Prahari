"""Entity Resolution Service (M2, Bible §3.2, §5.6) — the moat, mechanically.

- Blocking → candidate generation.
- Scoring → calibrated probability (scoring.py).
- Decision → high (auto-merge) / medium (queue for human) / low (keep separate).
- Adjudication → human confirms/corrects; writes an attributed RESOLVED_AS edge + a labelled
  training example (CP-10).
- Reversibility → every merge is a recorded event; unmerge restores prior state (BR-4). This is
  why FM-1 (wrong-asset merge) is survivable: versioned + reversible.

Human adjudication is the trust anchor — a wrongly-merged node yields a perfectly-cited answer
about the wrong pump, undetectable by model-side QC (§3.2, PRB §2.3).
"""
from __future__ import annotations

from datetime import date
from typing import Any

from ..audit.sink import AuditSink
from ..config import Settings
from ..domain.errors import Conflict
from ..domain.graph_types import EdgeType, NodeLabel
from ..domain.models import Adjudication, Edge, Node, ResolutionProposal, now_utc
from ..graph.provenance_sink import ProvenanceSink
from ..ports import IGraphStore, IRelationalStore
from .scoring import score_pair

_PROPOSAL = "resolution_proposal"
_MERGE_EVENT = "merge_event"


class ResolutionService:
    def __init__(
        self,
        graph: IGraphStore,
        relational: IRelationalStore,
        sink: ProvenanceSink,
        audit: AuditSink,
        settings: Settings,
    ) -> None:
        self._g = graph
        self._rel = relational
        self._sink = sink
        self._audit = audit
        self._s = settings

    # ------------------------------------------------------------ candidate generation
    def generate_proposals(self, tenant: str) -> list[ResolutionProposal]:
        """Blocking + scoring over unresolved identifiers, grouping by candidate asset."""
        identifiers = self._g.nodes_by_label(NodeLabel.IDENTIFIER.value, tenant)
        assets = {a.id: a for a in self._g.nodes_by_label(NodeLabel.ASSET.value, tenant)}
        # Group identifiers by their (possibly hinted) canonical asset.
        groups: dict[str, list[Node]] = {}
        for ident in identifiers:
            hint = ident.props.get("candidate_asset")
            if hint and hint in assets:
                groups.setdefault(hint, []).append(ident)
        proposals: list[ResolutionProposal] = []
        for asset_id, idents in groups.items():
            if len(idents) < 2:
                continue
            asset = assets[asset_id]
            # already fully resolved?
            resolved = {
                e.src
                for i in idents
                for e in self._g.all_edges(tenant)
                if e.type == EdgeType.RESOLVED_AS and e.dst == asset_id and e.src == i.id
            }
            pending = [i for i in idents if i.id not in resolved]
            if len(pending) < 2:
                continue
            base = pending[0]
            scores = []
            feats: dict[str, float] = {}
            for other in pending[1:]:
                sc, fe = score_pair(
                    str(base.props.get("value")), str(other.props.get("value")),
                    asset.props.get("iso14224_class"), asset.props.get("iso14224_class"),
                    str(base.props.get("context", "")), str(other.props.get("context", "")),
                    shared_wo=True,
                )
                scores.append(sc)
                feats = fe
            score = round(sum(scores) / len(scores), 4)
            proposal = ResolutionProposal(
                proposal_id=self._sink.new_id("prop"),
                canonical_asset_id=asset_id,
                canonical_tag=str(asset.props.get("tag") or asset_id),
                identifier_ids=[i.id for i in pending],
                identifiers=[
                    {"id": i.id, "value": i.props.get("value"),
                     "source_system": i.props.get("source_system"),
                     "vocabulary": i.props.get("vocabulary")}
                    for i in pending
                ],
                score=score,
                method="rules+embedding",
                features=feats,
                tenant=tenant,
            )
            # Decision: high → auto-merge (transparently); medium → queue; low → separate.
            if score >= self._s.confidence_auto_write:
                self._commit_merge(proposal, approver="system:auto", auto=True)
            elif score >= self._s.confidence_provisional:
                self._rel.put(_PROPOSAL, proposal.proposal_id, proposal.model_dump(mode="json"), tenant)
                proposals.append(proposal)
            # low → keep separate; ambiguous identifiers never auto-merge (FR-2.1)
        return proposals

    def queue(self, tenant: str) -> list[ResolutionProposal]:
        return [ResolutionProposal(**p) for p in self._rel.list(_PROPOSAL, tenant)]

    def get_proposal(self, proposal_id: str, tenant: str) -> ResolutionProposal | None:
        raw = self._rel.get(_PROPOSAL, proposal_id, tenant)
        return ResolutionProposal(**raw) if raw else None

    # ------------------------------------------------------------------- adjudication
    def adjudicate(
        self, proposal_id: str, adj: Adjudication, tenant: str
    ) -> dict[str, Any]:
        prop = self.get_proposal(proposal_id, tenant)
        if not prop:
            raise Conflict("Already resolved or not found.", {"proposal_id": proposal_id})
        target_asset = adj.corrected_target_asset_id or prop.canonical_asset_id
        if adj.decision == "merge":
            merge_id = self._commit_merge(prop, adj.approver, auto=False,
                                          target_asset_id=target_asset, corrected=adj.corrected)
            self._rel.delete(_PROPOSAL, proposal_id, tenant)
            self._audit.log(adj.approver, "resolution.adjudicated", tenant, target=target_asset,
                            detail={"decision": "merge", "corrected": adj.corrected,
                                    "proposal_id": proposal_id, "merge_id": merge_id})
            return {"resulting_asset_id": target_asset, "reversible_id": merge_id}
        else:
            self._rel.delete(_PROPOSAL, proposal_id, tenant)
            self._audit.log(adj.approver, "resolution.adjudicated", tenant,
                            detail={"decision": "separate", "note": adj.note,
                                    "proposal_id": proposal_id})
            return {"resulting_asset_id": None, "reversible_id": None}

    def _commit_merge(
        self,
        prop: ResolutionProposal,
        approver: str,
        auto: bool,
        target_asset_id: str | None = None,
        corrected: bool = False,
    ) -> str:
        target = target_asset_id or prop.canonical_asset_id
        merge_id = self._sink.new_id("merge")
        prior: list[dict[str, str]] = []  # for reversibility (BR-4)
        for ident_id in prop.identifier_ids:
            # Record any existing RESOLVED_AS for exact restoration on unmerge.
            for e in self._g.edges_from(ident_id, EdgeType.RESOLVED_AS.value, prop.tenant):
                prior.append({"ident": ident_id, "asset": e.dst, "edge_id": e.id})
            edge = Edge(
                id=f"res-{ident_id}-{target}",
                type=EdgeType.RESOLVED_AS,
                src=ident_id,
                dst=target,
                tenant=prop.tenant,
                props={
                    "confidence": prop.score,
                    "method": "auto" if auto else "human",
                    "adjudicated_by": approver,
                    "adjudicated_at": now_utc().isoformat(),
                    "merge_id": merge_id,
                    "corrected": corrected,
                },
                effective_from=date.today(),
            )
            self._g.upsert_edge(edge)  # RESOLVED_AS is not fact-bearing-requiring-span; it IS provenance of identity
        event = {
            "merge_id": merge_id,
            "proposal_id": prop.proposal_id,
            "target_asset_id": target,
            "identifier_ids": prop.identifier_ids,
            "prior_mapping": prior,
            "approver": approver,
            "auto": auto,
            "corrected": corrected,
            "created_at": now_utc().isoformat(),
            "reversed": False,
        }
        self._rel.put(_MERGE_EVENT, merge_id, event, prop.tenant)
        # CP-10: a human adjudication is a labelled training example for the Learning agent.
        if not auto:
            self._rel.put(
                "eval_label",
                merge_id,
                {"kind": "resolution", "target_asset_id": target,
                 "identifier_ids": prop.identifier_ids, "label": "merge", "author": approver},
                prop.tenant,
            )
        return merge_id

    # --------------------------------------------------------------------- reversibility
    def unmerge(self, merge_id: str, tenant: str, approver: str) -> dict[str, Any]:
        event = self._rel.get(_MERGE_EVENT, merge_id, tenant)
        if not event or event.get("reversed"):
            raise Conflict("Merge not found or already reversed.", {"merge_id": merge_id})
        # Remove the RESOLVED_AS edges this merge created.
        for ident_id in event["identifier_ids"]:
            self._g.delete_edge(f"res-{ident_id}-{event['target_asset_id']}")
        # Restore any prior mapping exactly (BR-4).
        for prior in event.get("prior_mapping", []):
            self._g.upsert_edge(
                Edge(id=prior["edge_id"], type=EdgeType.RESOLVED_AS, src=prior["ident"],
                     dst=prior["asset"], tenant=tenant,
                     props={"restored_from": merge_id}, effective_from=date.today())
            )
        event["reversed"] = True
        event["reversed_by"] = approver
        event["reversed_at"] = now_utc().isoformat()
        self._rel.put(_MERGE_EVENT, merge_id, event, tenant)
        self._audit.log(approver, "resolution.unmerged", tenant, target=event["target_asset_id"],
                        detail={"merge_id": merge_id})
        return {"restored": True, "merge_id": merge_id}

    def corpus_size(self, tenant: str) -> int:
        """The moat as a number (PRB §5.1 flywheel metric): count of human adjudications."""
        return sum(
            1 for e in self._rel.list(_MERGE_EVENT, tenant) if not e.get("auto")
        )

    def asset_history(self, asset_id: str, tenant: str) -> list[dict[str, Any]]:
        return [e for e in self._rel.list(_MERGE_EVENT, tenant) if e.get("target_asset_id") == asset_id]
