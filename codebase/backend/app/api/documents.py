"""M11 Admin & Ingestion Console — upload + ingestion status + content view (Bible §7.3)."""
from __future__ import annotations

import json
import pathlib
import re

from fastapi import APIRouter, Depends, File, Form, UploadFile

from ..auth.abac import Principal
from ..auth.rbac import Access
from ..container import Container
from ..domain.errors import InvalidRequest
from ..domain.models import IngestionStatus
from .deps import container, require_module

router = APIRouter(tags=["ingestion"])

# The demo corpus on disk — clean originals for documents ingested from it.
_CORPUS_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "corpus"
_LAST_INT = re.compile(r"(\d+)")


def _format_for(filename: str) -> str:
    low = filename.lower()
    if low.endswith((".md", ".markdown")):
        return "markdown"
    if low.endswith((".csv", ".tsv")):
        return "csv"
    if low.endswith(".json"):
        return "json"
    return "text"


def _span_order(span_id: str) -> tuple[int, ...]:
    """Natural order from the span id suffix (s0 < s1 < s10, row0 < row1)."""
    return tuple(int(n) for n in _LAST_INT.findall(span_id)) or (0,)


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


@router.get("/v1/documents/{doc_id}/content")
async def get_document_content(
    doc_id: str,
    principal: Principal = Depends(require_module("M11")),
    c: Container = Depends(container),
) -> dict:
    """The readable content of an ingested document.

    Prefers the clean original from the demo corpus (so markdown tables and structure survive);
    falls back to the parsed passages the system actually holds — each of which is a citable
    unit — for documents with no on-disk original (e.g. an uploaded file). Never invents text.
    """
    meta = c.stores.relational.get("document", doc_id, principal.tenant) or {}
    filename = str(meta.get("filename") or doc_id)

    # Passages: what the system extracted and can cite, ordered naturally.
    spans = c.stores.graph.spans_for_document(doc_id, principal.tenant)
    spans.sort(key=lambda s: ((s.page or 0), _span_order(s.span_id)))
    passages = [{"span_id": s.span_id, "page": s.page, "text": s.text} for s in spans]

    # Clean original, if this document came from the demo corpus (basename only — no traversal).
    source = "parsed"
    text = "\n\n".join(s.text for s in spans)
    safe = pathlib.Path(filename).name
    for candidate in (_CORPUS_DIR / safe, _CORPUS_DIR / "drawings" / safe):
        if candidate.is_file() and candidate.suffix.lower() in (
            ".md", ".markdown", ".txt", ".csv", ".tsv", ".json"
        ):
            try:
                text = candidate.read_text(encoding="utf-8")
                source = "original"
            except Exception:
                pass
            break

    return {
        "doc_id": doc_id,
        "filename": filename,
        "type": meta.get("type"),
        "format": _format_for(filename),
        "source": source,
        "page_count": len({s.page for s in spans if s.page is not None}) or 1,
        "passage_count": len(passages),
        "text": text,
        "passages": passages,
    }


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
