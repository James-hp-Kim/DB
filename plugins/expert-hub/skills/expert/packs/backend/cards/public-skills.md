# 공개 백엔드 스킬 출처와 선택

ID: `backend:public-skills` | both | reference-only

DB·캐시·SRE 분야별로 검토한 공개 스킬을 선택한다. 전체 저장소 설치나 기업 채택을 전제하지 않는다.

## conditions

필요한 분야와 실제 제품/버전·사용 도구가 확인되어야 한다.

## procedure

PostgreSQL은 Supabase 또는 PlanetScale, MySQL은 PlanetScale, Redis는 연결·관측 스킬, SRE/배포/관측은 Jeffallan, 런북/사후분석은 wshobson 자료를 선택 검토한다.

## limits

진입 문서·일부 예제 검토 이력이며 원본 전체 런타임 검증이 아니다. 설치 시 검토 commit과 라이선스·참조 파일을 확인한다.

## 출처

- [Supabase PostgreSQL skill](https://github.com/supabase/agent-skills/blob/main/skills/supabase-postgres-best-practices/SKILL.md) · reviewed-entrypoint · 확인 2026-10-29
- [PlanetScale database skills](https://github.com/planetscale/database-skills) · reviewed-entrypoint · 확인 2026-10-29
- [Redis agent skills](https://github.com/redis/agent-skills) · reviewed-entrypoint · 확인 2026-10-29
- [Jeffallan backend specialist review](../../../references/backend/sources.md) · reviewed-entrypoints · 확인 2026-10-29
- [Incident runbook/postmortem skills](https://github.com/wshobson/agents/tree/main/plugins/incident-response/skills) · reviewed-entrypoint · 확인 2026-10-29
