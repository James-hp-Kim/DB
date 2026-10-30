# 인덱스 통계와 삭제 판단

ID: `backend:index-statistics` | both | reference-only

pg_stat_user_indexes의 이름 열은 indexrelname이다. 사용 횟수 하나로 인덱스를 삭제하지 않는다.

## conditions

통계 초기화 시각·관찰 기간·주기 배치·제약조건·복제/업무 의존성을 확인한다.

## procedure

검토한 공개 예제의 indexname 사용을 실제 버전의 뷰 스키마와 대조한다. 드문 중요 쿼리와 제약조건을 확인한 뒤 후보를 검토한다.

## limits

카운터0은 영구적으로 불필요하다는 증거가 아니다. 원본 공개 스킬 전체가 검증됐다는 뜻도 아니다.

## 출처

- [PostgreSQL statistics views](https://www.postgresql.org/docs/current/monitoring-stats.html) · primary-reference · 확인 2026-10-29
- [Jeffallan backend specialist review](../../../references/backend/sources.md) · reviewed-entrypoints · 확인 2026-10-29
