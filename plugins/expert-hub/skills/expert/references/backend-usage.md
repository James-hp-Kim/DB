# Backend retrieval with supplied evidence

The user can say: "너는 백엔드 전문가야. 제공한 자료를 로컬에서 요약하고 필요한 근거만 조회해줘."

First search `backend-expert` or `백엔드` with expert_catalog(limit=1). Reuse the exact returned context. Backend defaults and permissions are backend+common. Do not load other personas' knowledge.

Extract only useful fields from the provided files locally: runtime/DB/version, service, time window/timezone, request/error/correctness counts, traffic, p95/p99, pool saturation, relevant stack trace or query, and recent changes. Preserve filename/row/time evidence; do not dump all rows. Unknown file formats need inspection, not guessed parsing. A question does not authorize permanent ingestion or production changes.

1. lookup: short symptom keywords, limit=2, max_chars=1800.
2. read: one selected id, at most three necessary sections, max_chars=3000. Check conditions and limits before applying procedure. Follow next_offset only for a needed truncated section.
3. source: selected IDs only, max_chars=2000. Cite actual records/URLs and reviewed status; do not substitute a whole source catalog.
4. Reuse context and unchanged returned evidence. Give observed facts, hypotheses, immediate mitigation, permanent fix and verification as appropriate. Do not force all fields into simple questions.

Example CLI from this skill directory:

```powershell
$backendChoice = python -B -X utf8 scripts/expert.py catalog '백엔드' --limit 1 | ConvertFrom-Json
$backendContext = $backendChoice.personas[0].context
python -B -X utf8 scripts/expert.py lookup 'DB 연결 풀 고갈' --context $backendContext --limit 2 --max-chars 1800
python -B -X utf8 scripts/expert.py read 'backend:pool-exhaustion' --context $backendContext --sections conditions procedure limits --max-chars 3000
```

`scripts/compare_backend_runs.py` accepts two normalized run JSON files, not arbitrary logs. Read the input contract in [performance](backend/performance.md) only when using the comparator; its historical compare_runs.py name maps to compare_backend_runs.py here. Write full comparison output outside the public repository and quote only material changes. Do not apply the quality `scan` command's defective/inspected semantics to HTTP traffic without checking the event definition.

This pack retains both the successful first synthetic lab and the later7/320 pool timeouts. These are short local SQLite experiments, not enterprise capacity evidence. The knowledge MCP itself has no production connectivity, persistent monitoring or autonomous repair. Character limits are retrieval payload limits, not total model-token budgets.

## Existing effects after a write incident

When retries, duplicate writes or inconsistent reads may already have affected business state, separate prevention of new errors from reconciliation of existing effects. Propose a bounded, read-only comparison of authoritative records and request/payment/fulfillment logs using stable business-operation identifiers, amounts or quantities, statuses and time windows. Preserve evidence, distinguish legitimate repeated operations and unknown matches, and report candidates rather than inventing a confirmed loss. Missing records or schemas stay unknown. Cancellation, refunds, stock correction or deletion require their own evidence and authorization; fixing the read/retry path does not undo earlier effects.
