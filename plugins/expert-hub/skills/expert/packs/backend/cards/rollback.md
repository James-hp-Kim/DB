# 배포 회귀와 롤백 호환성

ID: `backend:rollback` | both | reference-only

배포 시점과 회귀를 연결하고 스키마·프로토콜 호환성이 확인된 범위에서 되돌린다.

## conditions

배포 revision, 구/신 앱 호환성, DB마이그레이션·데이터변환, 영향 범위·소유자를 확인한다.

## procedure

관련 기능 비활성화 또는 특정 배포 롤백을 선택하고 관측창·중단조건을 정한다. 원인을 재현해 수정한 뒤 작은 범위에서 재배포한다.

## limits

코드 롤백이 이미 변경된 데이터·스키마를 복원하지 않는다. 호환되지 않으면 전진 복구가 필요할 수 있다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
