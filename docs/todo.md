# TODO

Post-hackathon / enterprise-ring items explicitly out of the current MVP (PRB §5.2 "Won't",
§5.3 Enterprise column). Recorded so scope discipline stays visible.

- [ ] Extract ingestion workers + model-inference workers to separate deployables (Bible
      ADR-007, `17_ROADMAP.md`).
- [ ] Real Neo4j read replicas + Qdrant per-tenant sharding at enterprise scale (NFR-8).
- [ ] Full OISD/PESO/DGMS/CPCB rule library with state parameterisation (PRB §5.3 enterprise).
- [ ] Customer estate connectors (CMMS/DMS/Historian) replacing the demo corpus.
- [ ] K8s + GPU + full observability stack (infra/ has compose only for the hackathon box).
- [ ] Custom `Datum Sans`/`Datum Mono` cut (Inter/JetBrains Mono substitutes ship now).
- [ ] gRPC internal service-to-service once the monolith is split (Bible §7.9, ADR-007).

## Won't (this cycle — do not build, PRB §5.2)
- Autonomous writes of any kind.
- Native mobile app (PWA only, ADR-013).
- Multi-plant network features.
