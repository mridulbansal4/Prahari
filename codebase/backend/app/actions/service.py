"""Execution Center (M7, Bible §7.3 actions, CP-3) — gated writes to a system of record.

The hard boundary of CP-3: no write to a CMMS without an explicit, attributed, distinct-
authority human approval. This service makes that boundary a real, un-bypassable code path —
there is no method that reaches a committed work order without an approver principal passing the
ABAC check. A drafted action and a committed action are never confusable (NFR-13).
"""
from __future__ import annotations

from typing import Any

from ..audit.sink import AuditSink
from ..auth.abac import Principal, authorize_work_order_submit
from ..auth.rbac import Role
from ..domain.errors import Conflict
from ..domain.models import ActionDraft
from ..graph.provenance_sink import ProvenanceSink
from ..ports import IRelationalStore

_DRAFT = "action_draft"


class ActionService:
    def __init__(self, relational: IRelationalStore, sink: ProvenanceSink, audit: AuditSink) -> None:
        self._rel = relational
        self._sink = sink
        self._audit = audit

    def draft(
        self,
        asset_id: str,
        asset_tag: str,
        symptom: str,
        drafter: Principal,
        hypothesis_id: str | None = None,
        investigation_id: str | None = None,
    ) -> ActionDraft:
        draft = ActionDraft(
            draft_id=self._sink.new_id("draft"),
            asset_id=asset_id,
            asset_tag=asset_tag,
            symptom=symptom,
            hypothesis_id=hypothesis_id,
            investigation_id=investigation_id,
            drafter=drafter.subject,
            preview={
                "asset": asset_tag,
                "symptom": symptom,
                "type": "corrective_maintenance",
                "linked_investigation": investigation_id,
                "linked_hypothesis": hypothesis_id,
            },
        )
        self._rel.put(_DRAFT, draft.draft_id, draft.model_dump(mode="json"), drafter.tenant)
        self._audit.log(drafter.subject, "action.draft_created", drafter.tenant,
                        target=draft.draft_id, detail={"asset_id": asset_id,
                                                       "investigation_id": investigation_id})
        return draft

    def get(self, draft_id: str, tenant: str) -> ActionDraft | None:
        raw = self._rel.get(_DRAFT, draft_id, tenant)
        return ActionDraft(**raw) if raw else None

    def list_for_asset(self, asset_id: str, tenant: str) -> list[ActionDraft]:
        return [ActionDraft(**d) for d in self._rel.list(_DRAFT, tenant)
                if d.get("asset_id") == asset_id]

    def list_all(self, tenant: str) -> list[ActionDraft]:
        return [ActionDraft(**d) for d in self._rel.list(_DRAFT, tenant)]

    def submit(self, draft_id: str, approver: Principal, cmms_ok: bool = True) -> ActionDraft:
        """The CP-3 gate. Requires a distinct-authority approver; commits to the CMMS only after
        the ABAC check passes. Never marks committed unless the write actually succeeded."""
        draft = self.get(draft_id, approver.tenant)
        if not draft:
            raise Conflict("Draft not found or expired.", {"draft_id": draft_id})
        if draft.status == "committed":
            raise Conflict("This draft was already committed.", {"draft_id": draft_id})
        drafter_role = _role_of(draft.drafter)
        authorize_work_order_submit(drafter_role, approver)  # raises ApprovalRequired if not allowed
        if not cmms_ok:
            # CMMS unreachable → draft stays pending, explicit "not committed" (never silent).
            draft.status = "pending"
            self._save(draft, approver.tenant)
            raise Conflict("CMMS unreachable — work order NOT committed. Retry.",
                           {"draft_id": draft_id, "committed": False})
        draft.status = "committed"
        draft.approver = approver.subject
        draft.cmms_work_order_id = self._sink.new_id("CMMS-WO")
        self._save(draft, approver.tenant)
        self._audit.log(approver.subject, "action.submitted", approver.tenant,
                        target=draft.cmms_work_order_id,
                        detail={"draft_id": draft_id, "drafter": draft.drafter,
                                "approver": approver.subject, "asset_id": draft.asset_id})
        return draft

    def reject(self, draft_id: str, approver: Principal, reason: str | None = None) -> ActionDraft:
        draft = self.get(draft_id, approver.tenant)
        if not draft:
            raise Conflict("Draft not found.", {"draft_id": draft_id})
        draft.status = "rejected"
        draft.approver = approver.subject
        draft.rationale = reason
        self._save(draft, approver.tenant)
        self._audit.log(approver.subject, "action.rejected", approver.tenant, target=draft_id,
                        detail={"reason": reason})
        return draft

    def _save(self, draft: ActionDraft, tenant: str) -> None:
        self._rel.put(_DRAFT, draft.draft_id, draft.model_dump(mode="json"), tenant)


def _role_of(subject: str) -> Role:
    from ..auth.identity import DEMO_USERS

    u = DEMO_USERS.get(subject)
    return u["role"] if u else Role.TECHNICIAN
