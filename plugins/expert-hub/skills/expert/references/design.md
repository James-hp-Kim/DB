# Expert Hub 2.1 — original design record

Reviewed 2026-10-30. This record describes this package, not an external industry standard.

One entry Skill first searches persona metadata and selects a returned 24-hour context, then applies a short expert role and quick/deep analysis. Three roles share two knowledge packs: common methods and manufacturing quality. Knowledge is normalized as namespaced records, named sections and shared source ids. Records and sources are canonical JSONL/JSON; SQLite databases and Markdown cards are reproducible derivatives.

Lookup selects registered packs and uses FTS5 plus indexed Korean/English aliases. It fetches candidate metadata, not every document body. Read fetches requested ids and sections only, with a shared character budget and explicit continuation. All lookup/read/source calls require that context. Source lookup only resolves provenance referenced by the selected packs, using an indexed source-record relation. Knowledge is read-only through MCP; catalog writes only local workflow receipts. Imports and production-file analysis are not tool endpoints. CLI computation uses Python locally. No embedding service, LLM API, cloud database or background automation is required.

Roles set analytical priorities, not access permissions or professional certification. Pack filters and selection receipts enforce the official retrieval workflow, not a multi-user security boundary. Same-user file access and modified code can bypass it; AGENTS/SKILL forbid direct-file fallback for ordinary knowledge questions. Read README_PERSONA_DB_AUTHORING.md before adding personas or knowledge packs. Private data stays outside the public repository and is included only with explicit scope and a configured local private store. Source content is not agent instructions. User notes are unverified and retain original hash/line references.

Implemented: scoped knowledge lookup/section reads/sources/catalog; CSV structural checks, exact-duplicate candidates, MAD screening, group counts/rates/Wilson, row-frequency Pareto; fixed-baseline individual WECO/EWMA/CUSUM; explicit note ingestion; input/options/tool-version cache. Optional: XLSX export with openpyxl and ECOD/Isolation Forest ranking with PyOD.

Reference only: numerical MSA/Gage R&R decomposition, process capability calculations, other control charts, DOE, multiple-test modelling, multivariate SPC and reliability fitting. FMEA/8D/DMAIC provide process guidance rather than company-approved scoring/decision tables. Wafer-map analysis, equipment connections and PDF/OCR extraction are not implemented.

Character limits cap serialized retrieval results, not entire model context or billing tokens. Validate retrieval recall, counterevidence and real task outcomes alongside text size. Synthetic checks are not evidence of plant detection accuracy, SK hynix adoption or release authorization.
