"""Request/response DTOs — mirror Bible §7 exactly. JSON fields snake_case (§12.2)."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel


# ---- auth / shell ----
class LoginRequest(BaseModel):
    username: str  # demo persona: ravi | meera | deepak | anil | auditor | compliance


class LoginResponse(BaseModel):
    token: str
    name: str
    role: str
    tenant: str


class MeResponse(BaseModel):
    subject: str
    name: str
    role: str
    tenant: str
    site: str
    modules: list[str]


# ---- investigations (Bible §7.3) ----
class InvestigationRequest(BaseModel):
    question: str
    as_of: date | None = None
    context: dict[str, str] | None = None  # {asset_id?}
    parent_investigation_id: str | None = None


class InvestigationAccepted(BaseModel):
    investigation_id: str


# ---- resolution (§7.3) ----
class AdjudicateRequest(BaseModel):
    decision: str  # merge | separate
    approver: str
    note: str | None = None
    corrected: bool = False
    corrected_target_asset_id: str | None = None
    version: int | None = None  # optimistic concurrency (Bible §7.6)


# ---- actions (§7.3) ----
class WorkOrderDraftRequest(BaseModel):
    asset_id: str
    symptom: str
    hypothesis_id: str | None = None
    investigation_id: str | None = None


class WorkOrderSubmitRequest(BaseModel):
    draft_id: str
    approver: str
    cmms_ok: bool = True  # demo hook to exercise the "CMMS unreachable" failure path


class WorkOrderRejectRequest(BaseModel):
    draft_id: str
    reason: str | None = None


# ---- corrections (§7.3) ----
class CorrectionRequest(BaseModel):
    target_kind: str
    target_ref: str
    new_value: str
    rationale: str
    author: str
    prior_value: str | None = None


# ---- org memory ----
class ExpertiseUpsert(BaseModel):
    person_id: str
    name: str
    role: str
    tenure_years: int
    retirement_risk: bool = False


class KnowsUpsert(BaseModel):
    person_id: str
    target_ref: str
    expertise: str
