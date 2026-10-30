# 점진 적용·중단·복구 기준

ID: `backend:rollout` | both | reference-only

한정된 변경 하나를 적용하고 오류·지연·정합성·의존성 관측으로 확대 또는 복구를 판단한다.

## conditions

대상·권한·관측창·중단 조건·복구 경로와 실제 성공 기준을 정한다.

## procedure

작은 범위에서 배포하고 대표 업무를 확인한다. 악화 시 현재 상태를 확인한 뒤 승인 범위의 복구 경로를 사용한다. 임시 제한/기능 비활성화의 해제 조건도 기록한다.

## limits

확인되지 않은 실패에 맹목 재시도를 반복하지 않는다. 임의의 공통 임계치를 운영 SLO로 만들지 않는다.

## 출처

- [성능 비교·검증 지침](../../../references/backend/performance.md) · authored-workflow · 확인 2026-10-29
- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
