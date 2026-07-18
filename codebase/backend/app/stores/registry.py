"""Build the store adapters for the active profile (ADR-P01)."""
from __future__ import annotations

from dataclasses import dataclass

from ..config import Settings, get_settings
from ..ports import IGraphStore, IRelationalStore, IVectorStore


@dataclass
class Stores:
    graph: IGraphStore
    vector: IVectorStore
    relational: IRelationalStore


_stores: Stores | None = None


def build_stores(settings: Settings | None = None) -> Stores:
    settings = settings or get_settings()
    if settings.profile == "production":
        return _build_production(settings)
    return _build_embedded(settings)


def _build_embedded(settings: Settings) -> Stores:
    from .embedded import EmbeddedStore

    db = EmbeddedStore(settings.state_path / "sentinel.db")
    return Stores(graph=db, vector=db, relational=db)  # one object, three ports


def _build_production(settings: Settings) -> Stores:
    # Production adapters implement the identical port contract (extraction seam, Bible §2.4).
    from .production import Neo4jGraphStore, PostgresRelationalStore, QdrantVectorStore

    return Stores(
        graph=Neo4jGraphStore(settings),
        vector=QdrantVectorStore(settings),
        relational=PostgresRelationalStore(settings),
    )


def get_stores() -> Stores:
    global _stores
    if _stores is None:
        _stores = build_stores()
    return _stores


def reset_stores() -> None:  # test hook
    global _stores
    _stores = None
