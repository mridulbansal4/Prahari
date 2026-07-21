"""The contract a drawing reader must return (CP-1).

A vision model is asked what a P&ID *means*, and answers in this shape. Everything here is
validated before a single node or edge reaches the graph: a field the model did not fill stays
empty, and an empty topology yields no edges rather than invented ones.

`source_note` on every item is the model's own justification — the text or symbol it read off
the drawing. It becomes the provenance span for the fact, so a drawing-derived edge is as
citable as a sentence from a PDF.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


def _clean_tag(v: str) -> str:
    """Canonical form for an equipment tag as drawn: upper-case, internal spaces removed.

    Deliberately conservative — it does NOT strip the hyphen, because `P-101B` and `P101B` are
    the same asset only after `resolution` says so. Normalising here would pre-empt the
    adjudication that entity resolution exists to perform.
    """
    return " ".join(str(v).split()).upper()


class DrawnComponent(BaseModel):
    tag: str = Field(description="Equipment tag exactly as printed, e.g. P-101B")
    kind: str = Field(default="", description="pump | vessel | valve | instrument | strainer | …")
    label: str = Field(default="", description="Descriptive name printed on the drawing")
    source_note: str = Field(default="", description="What was read off the drawing")

    _tag = field_validator("tag")(_clean_tag)


class DrawnConnection(BaseModel):
    """A directed process connection. `from_tag` feeds `to_tag`."""

    from_tag: str
    to_tag: str
    relation: str = Field(
        default="CONNECTED_TO",
        description="CONNECTED_TO for process flow; PART_OF for containment",
    )
    line_number: str = Field(default="", description="Line number if printed, e.g. 6\"-BFW-1042")
    source_note: str = Field(default="")

    _f = field_validator("from_tag")(_clean_tag)
    _t = field_validator("to_tag")(_clean_tag)


class DrawnAnnotation(BaseModel):
    """A rating, setpoint or note printed on the drawing."""

    subject_tag: str = Field(default="", description="Tag the annotation applies to, if any")
    text: str
    kind: str = Field(default="note", description="rating | setpoint | seal_plan | note")
    source_note: str = Field(default="")

    _s = field_validator("subject_tag")(_clean_tag)


class DrawingExtraction(BaseModel):
    """The whole of what a reader may assert about one drawing page."""

    drawing_title: str = Field(default="")
    drawing_number: str = Field(default="")
    components: list[DrawnComponent] = Field(default_factory=list)
    connections: list[DrawnConnection] = Field(default_factory=list)
    annotations: list[DrawnAnnotation] = Field(default_factory=list)
    confidence: float = Field(
        default=0.7, ge=0.0, le=1.0,
        description="Reader's own confidence; feeds the pipeline's confidence gate",
    )
    notes: str = Field(default="", description="Anything the reader could not resolve")

    def is_empty(self) -> bool:
        """True when the reader found nothing assertable — the caller must quarantine."""
        return not self.components and not self.connections

    def drop_dangling_connections(self) -> "DrawingExtraction":
        """Remove connections whose endpoints were not also reported as components.

        A model that names an edge but no node has not actually read the diagram; admitting
        the edge would create a phantom asset from a hallucinated tag.
        """
        known = {c.tag for c in self.components}
        self.connections = [
            c for c in self.connections if c.from_tag in known and c.to_tag in known
        ]
        return self
