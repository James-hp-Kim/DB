# Incident stabilization and permanent resolution

## Triage

Record current time with time zone, symptom/onset, affected business flow and scope, data-integrity risk, recent changes and evidence sources. Use existing severity/ownership procedures. When unknown, ask only what changes the immediate decision. Preserve relevant evidence with bounded collection; do not reset counters or clear caches/logs as a diagnostic shortcut.

Inspect the critical path: edge/LB -> app/runtime -> pool/cache/queue -> DB/external dependency. Look at traffic, errors, latency and saturation together. Distinguish offered load from successful throughput, and downstream failure from local overload. Form and test a narrow hypothesis rather than executing a catalog of commands.

## Select an authorized mitigation

Before a state-changing action, record: exact target, supporting evidence, expected effect, existing authorization, blast radius, execution bounds, observation window, stop condition and recovery path. Reuse standing/user authorization when it covers the specific action; request only unresolved authority or materially different scope. Read-only access alone permits diagnosis and preparation, not mutation. Do not convert an emergency into unlimited authority.

| Evidence | Candidate mitigation | Preconditions and permanent follow-up |
|---|---|---|
| Regression begins with a deployment | Roll back the affected deployment or disable the implicated feature | Confirm schema/protocol compatibility, release and target. Then reproduce the defect, fix it, test and stage rollout |
| DB pool exhaustion / DB saturation | Reduce noncritical producers or request concurrency, apply existing admission limits; examine connection leak/blocker evidence | App replicas can multiply pools. Compute peak downstream demand including workers and rollout overlap. Fix pool lifecycle, transactions or retry amplification |
| App CPU saturation with healthy downstream capacity | Bounded increase in replicas/resources or reduced noncritical work | Confirm LB/DB/cache quotas and new total demand, then verify the application bottleneck and capacity model |
| One query/transaction blocks critical work | Consider cancellation of the identified query, then session termination only if justified | Identify owner, transaction age/state, business operation and rollback cost; target a specific session after authorization. Do not terminate all sessions matching an arbitrary age |
| Cache failure or miss storm | Protect the DB using existing rate/concurrency controls; restore or warm cache in bounded batches when appropriate | Respect freshness/consistency requirements. Avoid full flush. Fix synchronized expiry, hot-key behavior or invalidation |
| External dependency slow or failing | Apply existing circuit breaking, bounded retries/backoff or reduced optional calls | Preserve business semantics, idempotency and deadline propagation. Fix retry storms and dependency budgets |
| Disk pressure / replica lag | Bound producers, inspect retention and storage growth; expand storage if authorized and feasible | Do not delete WAL/data or launch VACUUM FULL blindly. Verify backups/retention/topology and correct the cause |

These are choices, not commands to run in order. Load shedding reduces accepted work intentionally; report rejected work and business impact. It is stabilization, not evidence of increased capacity.

For automatic or supervised execution, take one bounded action at a time, remeasure, and stop on worsening error rate, latency, data-integrity signals or replication health against the agreed limits. Preserve manual interventions. On ambiguous failure, inspect actual state before retrying. Escalate when the authorized action does not restore service or required evidence is unavailable.

## Recovery and permanent fix

Verify affected business operations, errors, successful throughput, tail latency, queues and DB consistency/replication across the agreed observation window. State what remains degraded and how to restore any temporary limit or disabled feature. Do not close the incident solely because a process is running.

Build a timeline and distinguish root cause from contributing factors. Deliver the smallest fix with a reproduction/meaningful regression test, representative load test, monitoring improvement and owner. Identify any remaining capacity, data repair or recovery work explicitly. Infrastructure and schema changes need their own validation and rollback/forward-recovery plan.

If failover or restore is required, verify source/replica roles, write fencing, replication positions and tolerated data loss. Avoid simultaneous writable primaries. Backups must be restore-tested against the required recovery objectives; configuration presence is insufficient.

An exercise should use an explicitly identified isolated environment, narrow fault scope, known stop/recovery path and bounded resources. Do not inject faults into production merely to validate this skill.
