# Evidence-driven diagnostic branches

Use the branch matching the current evidence. Verify tool and engine versions; do not assume that every listed capability is installed or permitted. Profilers, dumps, traces and database diagnostics need bounded scope and can contain sensitive data.

| Layer | Discriminating evidence | Common misleading shortcut to avoid |
|---|---|---|
| Edge/network | Upstream vs total timing, DNS/TLS/connect errors, LB queues and route distribution | App/DB blame from end-to-end latency alone |
| Java/Spring | CPU sample, GC pause/allocation metrics, thread state and executor/pool waits, ORM query counts | Raising heap or threads without distinguishing CPU, GC and waiting |
| Python/FastAPI | Event-loop delay, blocking call stacks, worker CPU, async DB lifecycle and pool waits | Assuming `async def` makes blocking libraries nonblocking; adding workers without DB pool budgeting |
| Node/NestJS | Event-loop delay, CPU/heap samples, allocation growth, concurrency and outgoing connection counts | Increasing parallel promises or retry counts into a saturated dependency |
| ASP.NET Core | Thread-pool queue/starvation, allocation/GC, blocked async flows, EF SQL and tracking | Treating every slow request as a database issue or forcing a runtime upgrade |
| PostgreSQL | Active/waiting sessions, blocker chain, transaction state, statement totals/calls, relation sizes and vacuum, replica/WAL state | Calling every sequential scan bad, killing old sessions blindly, using EXPLAIN ANALYZE as a free read-only probe |
| MySQL/InnoDB | performance_schema statement digests/locks, Threads_running vs connections, plans, transaction/replication state | Raising max_connections regardless of memory/CPU; applying a provider-specific command to plain MySQL |
| Redis | Slowlog/latency, memory/evictions, hit/miss rates, command mix, client and network timing | KEYS/full scans, cache flush, unlimited pipelining, or ignoring hot keys |
| Queue/workers | Oldest-message age, arrival/completion/retry rates, consumer concurrency, poison messages and dependency limits | Scaling consumers until the database fails; equating an empty queue with successful processing |
| OS/VM/Kubernetes | Process vs host CPU, throttling, memory/OOM, I/O latency, disk/inodes, socket limits, rollout/autoscaler events | Restarting all replicas and losing evidence; interpreting readiness alone as full recovery |

## Cross-layer invariants

- Estimate peak app DB demand as sum(replicas × processes/workers per replica × pools per process × pool limit), plus jobs/admin/migration connections and rollout overlap. Adjust for the actual pool/proxy architecture; frontend proxy connections are not automatically backend DB connections. Use measured active demand and DB capacity as well as upper bounds.
- Separate intrinsic service time from time waiting in queues, pools and locks. Increasing queue capacity can hide saturation while tail latency grows.
- Count retries as additional dependency work. Check idempotency and deadline propagation before adding retries or moving work to a queue.
- Identify whether DB load is dominated by high per-call cost, high call frequency, lock waiting or poor cache locality. Use total workload contribution and user impact, not only the slowest single query.
- Online/concurrent index operations can still create resource pressure and blocking phases. Validate engine/version support, resource cost and recovery behavior first.
- Low/zero index scans over a short or reset observation interval does not establish that an index is disposable; check uniqueness/constraints, business-cycle workloads, replica access and dependencies.

## Corrections to reviewed public examples

- PostgreSQL `pg_stat_user_indexes` exposes `indexrelname`, not `indexname`. Verify columns against the actual server version before using copied diagnostic SQL.
- EXPLAIN ANALYZE actually executes its statement. A transaction rollback does not remove load/lock impact and may not undo all externally visible side effects. Prefer estimated plans or a suitable isolated reproduction until execution is justified.
- Framework snippets can contain incorrect imports/API usage and unsafe data handling. Compile/run relevant tests; verify DTO/password handling, version compatibility and existing project patterns before adopting them.
- Host-specific recovery commands, fixed replica counts, arbitrary session-count thresholds and provider recommendations in public runbooks are examples, not site policy.
