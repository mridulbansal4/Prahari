"""M11 Admin & Ingestion Console — upload + ingestion status (Bible §7.3)."""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends, File, Form, UploadFile

from ..auth.abac import Principal
from ..auth.rbac import Access
from ..container import Container
from ..domain.errors import InvalidRequest
from ..domain.models import IngestionStatus
from .deps import container, require_module

router = APIRouter(tags=["ingestion"])


@router.post("/v1/documents", status_code=202)
async def upload_document(
    file: UploadFile | None = File(default=None),
    structured: str | None = Form(default=None),
    doc_type: str | None = Form(default=None),
    principal: Principal = Depends(require_module("M11", Access.CONTRIBUTE)),
    c: Container = Depends(container),
) -> dict:
    if structured:
        payload = json.loads(structured)
        content = json.dumps(payload).encode()
        job = c.ingestion.ingest(payload.get("filename", "structured.json"), content,
                                 principal.tenant, principal.subject, doc_type="structured",
                                 structured=payload)
    elif file is not None:
        content = await file.read()
        job = c.ingestion.ingest(file.filename or "upload", content, principal.tenant,
                                 principal.subject, doc_type=doc_type)
    else:
        raise InvalidRequest("Provide a file or a structured payload.")
    status = 409 if job.status == IngestionStatus.DUPLICATE else 202
    return {"doc_id": job.doc_id, "job_id": job.job_id, "status": job.status.value,
            "_http": status}


@router.get("/v1/documents/{doc_id}")
async def get_document(
    doc_id: str,
    principal: Principal = Depends(require_module("M11")),
    c: Container = Depends(container),
) -> dict:
    meta = c.stores.relational.get("document", doc_id, principal.tenant)
    return meta or {"doc_id": doc_id, "status": "unknown"}


@router.get("/v1/ingestion/{job_id}")
async def get_job(
    job_id: str,
    principal: Principal = Depends(require_module("M11")),
    c: Container = Depends(container),
) -> dict:
    job = c.ingestion.get_job(job_id, principal.tenant)
    if not job:
        raise InvalidRequest("Unknown job id.")
    return job.model_dump(mode="json")


@router.get("/v1/ingestion")
async def list_jobs(
    principal: Principal = Depends(require_module("M11")),
    c: Container = Depends(container),
) -> dict:
    return {"jobs": [j.model_dump(mode="json") for j in c.ingestion.list_jobs(principal.tenant)],
            "quarantined": [j.model_dump(mode="json") for j in c.ingestion.quarantined(principal.tenant)]}
