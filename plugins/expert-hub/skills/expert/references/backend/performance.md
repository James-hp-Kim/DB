# Performance evaluation and verification

## Define a representative comparison

Reuse existing tests where suitable. Confirm the business flow, endpoints/mix, request sizes, tenant/key distribution, data snapshot/scale, expected correctness, offered load, retries, timeouts, connection reuse, and caches. Include hot-key or expensive-query cases when relevant. A synthetic fixture demonstrates tooling behavior only.

Choose an open arrival-rate model when the question is how the service handles externally arriving traffic; a closed concurrency model is useful for fixed concurrent-user behavior but may reduce offered throughput as responses slow. Record the model and actual delivered load. Include dropped iterations and check load-generator CPU/network capacity. Do not silently switch models or add generators to manufacture comparability.

Record application revision/configuration, runtime/tool versions, resources, replica count, background work, warm-up, measurement window, and cache state. Compare baseline and candidate under matched conditions. When resource size changes, report capacity/cost tradeoffs separately rather than attributing all gains to the code. Repeat enough representative runs to assess variability; one pair does not prove statistical significance or an SLA.

Measure:
- Total finalized request attempts, failures/timeouts, response-correctness failures, successful requests/second, and dropped workload iterations.
- Latency distribution including p50/p95/p99 and its population (all finalized attempts vs successful requests). State timeout censoring and do not silently discard slow failures.
- App CPU/memory/GC or event-loop/thread waits; DB query/pool/lock/I/O metrics; cache, queue and dependency effects appropriate to the bottleneck.

Warm-up and measurement boundaries must match. Do not average per-node percentiles or per-run percentiles to construct a fleet percentile. Use merged compatible histograms/raw observations, or show runs independently.

## Attribute and change

Start with the critical request path and a ranked hypothesis supported by measurements. A CPU spike alone does not establish its cause. Test the smallest discriminating observation. Consider downstream saturation and amplification from retries/concurrency.

Change one cause at a time where possible. Preserve result correctness, authentication/authorization, write semantics and durability. Include index write amplification/storage and replication effects. Verify the exact runtime/DB version against official documentation before applying tuning or migration examples.

For rollout, use the existing delivery process with a defined scope, observation window and recovery path. Validate the business flow and relevant dependency metrics. A green health endpoint or lower latency with more dropped requests is insufficient.

## Offline comparison helper

`scripts/compare_runs.py` reads normalized JSON files without contacting any service. It is not a load generator or raw k6 importer. Extract values from real test evidence and preserve source references; do not estimate missing counters. `checks_failed` is a count of checks, not necessarily failed requests. `dropped_iterations` counts iterations, not HTTP requests; never combine them into a request denominator.

Each run requires:

```json
{
  "schema_version": 1,
  "run_id": "synthetic-example-only",
  "revision": "example-revision",
  "evidence_ref": "synthetic fixture; replace with actual evidence for a real run",
  "context": {
    "environment": "fixture",
    "dataset": "fixture-v1",
    "workload": "fixture-one-get-per-iteration",
    "load_model": "open",
    "offered_load": "100 iterations/s",
    "resources": "fixture-app-2cpu-4gb-db-4cpu-8gb",
    "tool_version": "fixture-v1",
    "cache_state": "warm",
    "latency_scope": "all-finalized-attempts",
    "warmup_seconds": 30,
    "duration_seconds": 60
  },
  "metrics": {
    "requests": 6000,
    "failures": 30,
    "correctness_failures": 0,
    "dropped_iterations": 0,
    "p50_ms": 70,
    "p95_ms": 200,
    "p99_ms": 350
  }
}
```

`failures` is the union of failed attempts, including incorrect responses, counted once per request. `correctness_failures` is a subset. All started attempts in the measurement cohort must be finalized (including timeout/abort outcomes); record their latency consistently. If the tool cannot supply these semantics, report the gap instead of coercing unrelated counters into this format. `resources` must describe or identify the full unchanged resource configuration, including replica/worker counts. Labels cannot prove underlying sameness: audit raw evidence too.

Run from the skill's root directory with the available Python executable (or use absolute paths):

```text
python scripts/compare_runs.py baseline.json candidate.json
python scripts/compare_runs.py baseline.json candidate.json --limits agreed-limits.json
```

Optional limits support `max_p95_ms`, `max_p99_ms`, `max_error_rate` (fraction 0..1), `min_success_rps`, and `max_dropped_iterations`. Supply only agreed values. The helper reports passing **supplied** limits, not complete SLO compliance. Correctness failures are always reported separately. It never declares a deployment safe or an optimization proven.

Different context values produce `not_comparable` and no relative changes. With matched context, raw changes and any adverse directions are reported; these are observations, not a significance test. A zero baseline or an unrepresentable percentage yields null instead of a percentage change. Missing/invalid data is rejected.

Exit status: 0 = comparison produced (not an improvement verdict), 1 = supplied limit failure or candidate correctness failure, 2 = invalid input or unmatched comparison. No limits means `not_evaluated`, not a pass.
