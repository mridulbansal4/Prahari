# Architecture Diagrams

C4-style views of the as-built system (Bible §2). Diagrams are Mermaid so they are diffable.

## Containers (as built)

```mermaid
graph TB
  subgraph Client
    PWA["frontend/ — React + TS PWA<br/>(design.md tokens)"]
  end
  subgraph Core["codebase/backend/ — modular monolith (FastAPI)"]
    API["API — REST + WS<br/>+ thin gateway (authn/z, rate-limit)"]
    ORCH["Agent Orchestrator<br/>Planner→Retriever→Executor→Critic→Verifier"]
    RET["Retrieval Router<br/>graph + vector"]
    ING["Ingestion Pipeline"]
    RES["Entity Resolution"]
    RULE["Compliance Rule Engine"]
    AUDIT["Audit + Provenance sink (CP-1)"]
  end
  subgraph Ports["Ports / Adapters (Bible §2.4)"]
    G[(IGraphStore)]
    V[(IVectorStore)]
    R[(IRelationalStore)]
    M[[IModelProvider]]
  end
  subgraph Embedded["Embedded adapters (default — air-gap / CP-9)"]
    SG[NetworkX/SQLite graph]
    SV[local cosine index]
    SR[SQLite]
    ST[template-synth model]
  end
  subgraph Prod["Production adapters (docker-compose)"]
    NEO[(Neo4j)]
    QD[(Qdrant)]
    PG[(Postgres)]
    LLM[[Provider-abstracted LLM — CP-5]]
  end

  PWA --> API --> ORCH --> RET
  API --> ING & RES & RULE & AUDIT
  RET --> G & V
  ORCH --> M
  RES --> G
  RULE --> G
  AUDIT --> R
  G -.-> SG & NEO
  V -.-> SV & QD
  R -.-> SR & PG
  M -.-> ST & LLM
```

## Investigation sequence (M1)

```mermaid
sequenceDiagram
  participant U as Ravi (PWA)
  participant O as Orchestrator
  participant R as Retrieval Router
  participant M as Model
  U->>O: POST /v1/investigations (question)
  O->>R: classify + retrieve
  R-->>O: assembled context + citations (each span cited)
  O->>M: grounded prompt (Executor)
  M-->>O: draft claims
  O->>O: Critic + Verifier grounding check (CP-2)
  alt grounding >= threshold
    O-->>U: streamed answer + citations + graph path
  else
    O-->>U: abstain + who-to-ask (CP-4)
  end
```

## The CP-9 degradation ladder (Bible §2.8)

```mermaid
graph LR
  full["Full: graph+vector+model"] --> m["-model: structured, no prose"]
  m --> v["-vector: graph traversal only"]
  v --> g["-graph: cached + doc search"]
  g --> e["-everything: who to ask"]
```
