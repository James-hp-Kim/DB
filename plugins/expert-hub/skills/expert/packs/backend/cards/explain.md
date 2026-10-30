# EXPLAIN ANALYZE는 문장을 실행한다

ID: `backend:explain` | both | reference-only

EXPLAIN ANALYZE의 실행 부하·변경 효과를 고려한다. 읽기 전용 SELECT도 비용이 있다.

## conditions

제품과 버전의 문서, 쿼리 유형, 실행 권한·허용 부하를 먼저 확인한다.

## procedure

실행이 허용되지 않거나 영향이 크면 일반 EXPLAIN으로 시작한다. 실행 측정은 타임아웃·기간·데이터 범위를 제한하고 영향 관측을 준비한다.

## limits

롤백이 모든 외부 효과를 되돌린다고 가정하지 않는다. 운영에서 예제를 그대로 실행하지 않는다.

## 출처

- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) · primary-reference · 확인 2026-10-29
