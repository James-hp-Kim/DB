# 캐시 장애와 동시 만료 폭증

ID: `backend:cache-storm` | both | reference-only

미스 폭증이 DB 부하로 전파되는지 확인하고 동시성을 보호하며 제한적으로 워밍한다.

## conditions

캐시 적중률, hot key, TTL 분포, 연결·타임아웃, DB 요청 증폭을 확인한다.

## procedure

기존 유입 제한·요청 합치기·제한된 워밍을 검토하고 신선도/일관성 요구를 지킨다. Redis 연결과 관측 지침을 실제 드라이버에 맞춰 확인한다.

## limits

전체 캐시 flush를 기본 진단으로 사용하지 않는다. 캐시 복구가 원본 DB 정상화와 같은 의미는 아니다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
- [Redis agent skills](https://github.com/redis/agent-skills) · reviewed-entrypoint · 확인 2026-10-29
