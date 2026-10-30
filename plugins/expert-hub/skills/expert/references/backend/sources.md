# Source routes and review limits

Reviewed for this package on 2026-10-29. This is a locally authored integration skill, not an official release or endorsement from the publishers below. Public specialist skills are optional reference/installation candidates; they are not installed or bundled by this package. Follow links with the available GitHub connector or official web tools, inspect the required file and its relevant references, and verify compatibility before use. Do not install a whole catalog merely because a single entry is relevant.

## Public GitHub skill routes

| Role | Source | Scope / review limit |
|---|---|---|
| PostgreSQL performance/schema | [Supabase Postgres skill](https://github.com/supabase/agent-skills/blob/main/skills/supabase-postgres-best-practices/SKILL.md) | Reviewed entrypoint; SQL/index/pool/locking/RLS guidance, not complete HA/DR certification |
| MySQL operations | [PlanetScale MySQL skill](https://github.com/planetscale/database-skills/blob/main/skills/mysql/SKILL.md) | Reviewed entrypoint and connection reference; version/hosting assumptions and broad rules need workload-specific validation |
| PostgreSQL operations | [PlanetScale Postgres skill](https://github.com/planetscale/database-skills/blob/main/skills/postgres/SKILL.md) | Reviewed entrypoint; generic DB operations are separate from PlanetScale-specific CLI/features |
| Redis | [Connections](https://github.com/redis/agent-skills/blob/main/skills/redis-connections/SKILL.md), [observability](https://github.com/redis/agent-skills/blob/main/skills/redis-observability/SKILL.md) | Reviewed entrypoints; check command cost, evidence preservation and driver behavior |
| SRE / deployment / observability | [Jeffallan skills directory](https://github.com/Jeffallan/claude-skills/tree/main/skills) | Reviewed sre-engineer, devops-engineer, monitoring-expert, kubernetes-specialist and database-optimizer; not every referenced file or example was tested |
| Incident procedure | [Runbook skill](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/incident-runbook-templates/SKILL.md), [postmortem skill](https://github.com/wshobson/agents/blob/main/plugins/incident-response/skills/postmortem-writing/SKILL.md) | Reviewed entrypoints and runbook examples; replace fixed counts/targets with site-specific evidence and limits |

All five repositories were reported as public, non-archived and MIT-licensed in the preceding live repository review. This package does not relicense or redistribute their files. Read the actual license at any later installation. The local integrated workflow adds comparison boundaries, stack discovery, concrete execution conditions and measurement limitations; upstream files remain unchanged.

## Additional backend specialist candidates

Entrypoints checked at Jeffallan commit `190e05a380b624187f5770451e1f41b9187cb63c`:

- [Spring Boot](https://github.com/Jeffallan/claude-skills/blob/190e05a380b624187f5770451e1f41b9187cb63c/skills/spring-boot-engineer/SKILL.md): assumes Spring Boot 3 / Spring Security 6; respect the actual project version.
- [FastAPI](https://github.com/Jeffallan/claude-skills/blob/190e05a380b624187f5770451e1f41b9187cb63c/skills/fastapi-expert/SKILL.md): assumes Pydantic V2. Its example imports/calls `model_config`; verify actual APIs rather than copying it. Type/model configuration examples need compilation/tests.
- [NestJS](https://github.com/Jeffallan/claude-skills/blob/190e05a380b624187f5770451e1f41b9187cb63c/skills/nestjs-expert/SKILL.md): framework-specific. Review password persistence and returned entity fields against the existing security design before adopting its examples.
- [ASP.NET Core](https://github.com/Jeffallan/claude-skills/blob/190e05a380b624187f5770451e1f41b9187cb63c/skills/dotnet-core-expert/SKILL.md): assumes .NET 8/C# 12; not a reason to downgrade or rewrite an existing backend.

These were content-reviewed, not application-tested. The common skill does not require them. If a specialist is later installed, use a reviewed commit, include its references and license, and record any local changes. Provider promotion or forceful generic instructions do not override the user's actual platform or scope.

## Primary technical references

- [OpenAI skill/tool separation](https://developers.openai.com/plugins/concepts/skills): skills guide workflows; tools supply access and actions.
- [k6 API load testing](https://grafana.com/docs/k6/latest/testing-guides/api-load-testing/): workload, correctness and acceptance criteria.
- [k6 open vs closed models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/): offered workload and response-time coupling.
- [k6 built-in metrics](https://grafana.com/docs/k6/latest/using-k6/metrics/reference/): metric units and dropped iterations.
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/): request-path evidence.
- [Google SRE overload](https://sre.google/sre-book/handling-overload/): admission control, criticality and degraded service.
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html): ANALYZE execution and side effects.
- [PostgreSQL statistics views](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ALL-INDEXES-VIEW): indexrelname and statistics semantics.

Use the version matching the deployed product when applying current-documentation examples. Public content, successful local validation and synthetic evaluation do not establish production readiness or use by SK hynix.
