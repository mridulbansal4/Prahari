"""Audit + provenance sink (Bible §8.5, FR-10). Append-only log of every read/answer/write.

Every answer additionally logs {question, context span ids, prompt manifest hash, model id,
verdict} for reproducibility (CP-7) and forensic trail.
"""
from __future__ import annotations

import uuid
from typing import Any

from ..domain.models import AuditEntry
from ..ports import IRelationalStore


class AuditSink:
    def __init__(self, relational: IRelationalStore) -> None:
        self._rel = relational

    def log(
        self,
        actor: str,
        action: str,
        tenant: str,
        target: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> AuditEntry:
        entry = AuditEntry(
            entry_id=f"aud-{uuid.uuid4().hex[:12]}",
            actor=actor,
            action=action,
            target=target,
            detail=detail or {},
            tenant=tenant,
        )
        self._rel.append_audit(entry)
        return entry

    def query(self, tenant: str, **kw: Any) -> list[AuditEntry]:
        return self._rel.query_audit(tenant, **kw)
