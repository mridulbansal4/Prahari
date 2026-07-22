"""OCR providers (IOcrProvider adapters, Bible §3.1 parse/ocr stage).

Strictly transcription: given rendered page images, return the text printed on them. This
module answers "what does this page say" and never "what does this diagram mean" — diagram
reasoning is ``drawings.py`` (IDrawingReader), which returns validated structure instead of
prose.

The load-bearing rule is that an unavailable provider must fail loudly. ``available()`` returns
False and ``read_pages`` raises rather than returning ``[""]``, so ingestion quarantines the
document with a stated reason instead of admitting an empty parse as if the page were blank
(CP-1 / BR-1). Nothing here ever fabricates text: a failed provider raises or returns empty and
the caller decides.

Every heavy dependency (paddleocr, PyMuPDF) is imported lazily inside the function that needs
it, so a fresh checkout boots with no GPU, no CUDA and no extra wheels — matching the ``none``
default in config.py.
"""
from __future__ import annotations

import base64
from typing import Any

import httpx

from ..config import Settings
from ..ports import IOcrProvider


# --------------------------------------------------------------------------- null (the default)
class NullOcr:
    """The default: no OCR configured. Declares itself unavailable so the pipeline quarantines
    scanned documents with a reason rather than indexing an empty parse."""

    id = "none"

    def available(self) -> bool:
        return False

    def read_pages(self, pages: list[bytes], mime: str = "image/png") -> list[str]:
        raise RuntimeError(
            "No OCR provider is configured (PRAHARI_OCR_PROVIDER=none). Scanned pages cannot "
            "be transcribed; the document must be quarantined rather than parsed as empty."
        )


# ------------------------------------------------------------------- Unlimited-OCR (server mode)
class UnlimitedOcrProvider:
    """Unlimited-OCR behind an OpenAI-compatible vision endpoint (local vLLM/SGLang).

    Server mode only. The in-process ``transformers``/CUDA path is deliberately NOT implemented
    here — writing a fake local branch would let a misconfigured air-gap install look healthy
    while transcribing nothing. When ``unlimited_ocr_local`` is set, ``available()`` therefore
    returns False so the failure is visible at ingestion time.
    """

    id = "unlimited-ocr"

    # A model-agnostic transcription instruction. Unlimited-OCR's own "<image>document
    # parsing." sentinel is model-specific; a plain instruction also works on a general hosted
    # vision model (NVIDIA, etc.), so the same adapter serves both a local and a hosted endpoint.
    _PROMPT = (
        "Transcribe every piece of text visible in this document image, exactly as printed, "
        "preserving line and paragraph breaks. Do not summarise, explain, or add anything. "
        "Output only the transcribed text."
    )

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._base = (settings.unlimited_ocr_base_url or "").rstrip("/")
        self._key = settings.unlimited_ocr_api_key

    def available(self) -> bool:
        if self._settings.unlimited_ocr_local:
            # In-process transformers/CUDA inference is not implemented; report unavailable.
            return False
        return bool(self._base)

    def read_pages(self, pages: list[bytes], mime: str = "image/png") -> list[str]:
        if not self._base:
            raise RuntimeError(
                "Unlimited-OCR selected but PRAHARI_UNLIMITED_OCR_BASE_URL is not set."
            )
        headers = {"content-type": "application/json"}
        if self._key:  # a hosted endpoint needs a Bearer token; a local one ignores it
            headers["Authorization"] = f"Bearer {self._key}"
        out: list[str] = []
        for page in pages:
            b64 = base64.b64encode(page).decode("ascii")
            body: dict[str, Any] = {
                "model": self._settings.unlimited_ocr_model,
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self._PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:{mime};base64,{b64}"},
                            },
                        ],
                    }
                ],
            }
            resp = httpx.post(
                f"{self._base}/chat/completions",
                headers=headers,
                json=body,
                timeout=120.0,  # page-level VLM transcription is slow; generous by design
            )
            resp.raise_for_status()
            data = resp.json()
            try:
                text = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError) as exc:  # malformed → fail, never guess
                raise RuntimeError(f"Unlimited-OCR returned an unexpected response: {exc}") from exc
            out.append(text if isinstance(text, str) else "")
        return out


# --------------------------------------------------------------------------- PaddleOCR (CPU)
class PaddleOcrProvider:
    """CPU fallback. ``paddleocr`` is an optional dependency — it is imported lazily so the
    package's absence is a capability signal (``available() is False``), not an import error."""

    id = "paddle"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def available(self) -> bool:
        try:
            import paddleocr  # noqa: F401
        except ImportError:
            return False
        return True

    def read_pages(self, pages: list[bytes], mime: str = "image/png") -> list[str]:
        try:
            from paddleocr import PaddleOCR
        except ImportError as exc:
            raise RuntimeError(
                "PaddleOCR selected but the 'paddleocr' package is not installed."
            ) from exc
        engine = PaddleOCR(use_angle_cls=True, lang=self._settings.paddle_ocr_lang)
        out: list[str] = []
        for page in pages:
            result = engine.ocr(page, cls=True)
            out.append("\n".join(_paddle_lines(result)))
        return out


def _paddle_lines(result: Any) -> list[str]:
    """Flatten PaddleOCR's nested ``[[ [box, (text, score)], ... ]]`` output to text lines.

    Defensive: shapes differ across paddleocr versions, and a shape we do not recognise yields
    no lines rather than an invented transcription.
    """
    lines: list[str] = []
    if not result:
        return lines
    for block in result:
        if not block:
            continue
        for item in block:
            try:
                payload = item[1]
                text = payload[0] if isinstance(payload, (list, tuple)) else payload
            except (IndexError, TypeError):
                continue
            if isinstance(text, str) and text.strip():
                lines.append(text.strip())
    return lines


# ------------------------------------------------------------------------------------ selector
def build_ocr(settings: Settings) -> IOcrProvider:
    """Pick the OCR adapter for the configured provider.

    An explicitly named provider is always constructed even when unavailable, so a
    misconfiguration surfaces as a quarantine with a reason instead of silently degrading to a
    different engine. Only ``auto`` is allowed to fall through the ladder.
    """
    choice = settings.ocr_provider
    if choice == "unlimited":
        return UnlimitedOcrProvider(settings)
    if choice == "paddle":
        return PaddleOcrProvider(settings)
    if choice == "auto":
        if settings.unlimited_ocr_base_url:
            return UnlimitedOcrProvider(settings)
        paddle = PaddleOcrProvider(settings)
        if paddle.available():
            return paddle
        return NullOcr()
    return NullOcr()


# ------------------------------------------------------------------------- page rendering / sniff
def render_pdf_pages(content: bytes, dpi: int, max_pages: int = 20) -> list[bytes]:
    """Raster PDF pages to PNG bytes at ``dpi``, capped at ``max_pages``.

    PyMuPDF is an optional dependency; when it is missing this returns ``[]`` and the caller
    quarantines the document rather than treating a scan as text-free.
    """
    try:
        import fitz
    except ImportError:
        return []
    out: list[bytes] = []
    zoom = dpi / 72.0
    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception:
        return []
    try:
        matrix = fitz.Matrix(zoom, zoom)
        for index, page in enumerate(doc):
            if index >= max_pages:
                break
            pix = page.get_pixmap(matrix=matrix)
            out.append(bytes(pix.tobytes("png")))
    except Exception:
        return out
    finally:
        doc.close()
    return out


_IMAGE_MAGIC: tuple[bytes, ...] = (
    b"\x89PNG",       # PNG
    b"\xff\xd8\xff",  # JPEG
    b"II*\x00",       # TIFF little-endian
    b"MM\x00*",       # TIFF big-endian
    b"BM",            # BMP
    b"GIF8",          # GIF
)


def looks_like_pdf(content: bytes) -> bool:
    """Magic-byte sniff for PDF. The pipeline otherwise classifies on file extension alone,
    which misses a scan uploaded as ``report.dat`` and mislabels a renamed file."""
    return content[:4] == b"%PDF"


def looks_like_image(content: bytes) -> bool:
    """Magic-byte sniff for the raster formats OCR can consume."""
    return any(content.startswith(magic) for magic in _IMAGE_MAGIC)
