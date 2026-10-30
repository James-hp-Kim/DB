# Commands

Set `$expert` to this skill's `scripts/expert.py` path. Python 3.11+ with SQLite FTS5 is required; base operation needs no pip packages or API key.

```powershell
$choices = python -B -X utf8 $expert catalog '품질보증' --limit 1 | ConvertFrom-Json
$choices.personas # inspect before selecting; no result means change the query
$context = $choices.personas[0].context
python -B -X utf8 $expert status
python -B -X utf8 $expert lookup '불량률 분모' --context $context --limit 3
python -B -X utf8 $expert read common:data-contract --context $context --sections conditions procedure limits --max-chars 3000
python -B -X utf8 $expert source nist-wilson --context $context
```

Every lookup/read/source requires a context issued by persona search. Reuse for 24h;
catalog changes or a different installation require a new search. To switch roles,
search that role and choose its returned key. `--packs common quality` explicitly
expands only within that role's allowed packs. No direct files/SQL fallback for
ordinary knowledge questions. Contexts are local workflow receipts, not credentials.


`lookup` defaults: three summaries and the selected short role, at most 3,500 serialized JSON characters. `read` defaults: conditions/procedure/limits, at most 6,000 characters for all returned entries. A non-null next_offset marks omitted text; continue with exactly one id/section and `--offset`. No perfect semantic retrieval or total-token ceiling is claimed.

Data diagnostics:

Chip review: first `catalog 'chip-design-verification' --limit 1`, then use its context with `reference-input 'C:/chip-work/timing.rpt' --context <key> --max-chars 2500`. Optional `--query 'STA WNS setup hold'` narrows the question. Inputs must be explicit UTF-8 files <=2 MiB. It returns keyword hints and scoped references, not file contents or a verification verdict. See [chip-review](chip-review.md) when needed.

```powershell
python -B -X utf8 $expert scan 'C:/data/quality.csv' --groups product machine --numerator defective --denominator inspected --out 'C:/QA-runs/quick-01'
python -B -X utf8 $expert scan 'C:/data/measurements.csv' --values thickness --out 'C:/QA-runs/quick-02'
python -B -X utf8 $expert monitor 'C:/data/stream.csv' --value thickness --mean 10 --sigma 0.1 --order timestamp --baseline-validated --out 'C:/QA-runs/deep-01'
python -B -X utf8 $expert anomalies 'C:/data/comparable.csv' --values thickness pressure temperature --top 10 --out 'C:/QA-runs/deep-02'
```

The baseline values are examples, not operational limits. Confirm comparable independent individual observations, measurement suitability, stable reference mean/sigma and consistent time order. Baseline confirmation is an explicit attestation, not an automatic statistical test. Monitor rejects gaps and does not stop equipment. WECO uses eight same-side points; many simultaneous rules increase false alarms.

`scan --numerator-type units` requires nonnegative integer defective units <= inspected units. `events` allows multiple defects per unit and does not calculate a binomial interval. Category Pareto counts rows, not quantities. Exact duplicate rows are preserved and marked for review. Rates and intervals remain provisional when sampling/duplicates are unresolved. No correction of measurement units is inferred.

CSV/TSV limit: 100 MiB/200,000 records. Inputs beyond it fail without silent sampling. UTF-8 BOM is supported; use `--encoding cp949` explicitly for old Korean CSV. Full evidence is in `result.json` and `findings.csv`; stdout previews are bounded. Use a new output directory when the input/options/version changes.

For XLSX, run the colocated `convert_xlsx.py input.xlsx --sheet '검사' --out output.csv` with a Python that has openpyxl. It retains Excel row numbers and hidden rows; uncached formulas fail, existing caches may still be stale. For `anomalies`, use a Python with PyOD. It requires 20+ complete numeric rows; top-N ranks are review priorities, not defect counts or causes.

Explicit private text import:

```powershell
python -B -X utf8 $expert ingest-note 'C:/data/검토기록.md' --title '검토 기록' --store 'C:/QA-private'
$env:EXPERT_PRIVATE_DIR = 'C:/QA-private'
python -B -X utf8 $expert lookup '검토 기록' --context $context --include-private
```

Private lookup needs both the environment variable and explicit include_private/--include-private. Store outside the public repository. Inputs are UTF-8 TXT/MD <=2 MiB. Raw hash and line ranges are preserved. Existing MCP processes need restart after environment changes. Imports do not alter base packs and are not exposed as MCP tools.
