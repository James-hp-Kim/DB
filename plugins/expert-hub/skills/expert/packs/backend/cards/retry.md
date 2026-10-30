# 의존성 지연과 재시도 증폭

ID: `backend:retry` | both | reference-only

계층별 재시도의 곱셈 증폭, 전체 요청 deadline, 중복 쓰기 위험을 확인한다.

## conditions

상위/하위 timeout·재시도 횟수·backoff, 멱등성 키, 의존 서비스 오류가 필요하다.

## procedure

총 시간 예산 안에서 재시도 횟수를 제한하고 지연/jitter·회로 차단·선택 기능 축소를 기존 정책에 맞춘다. 쓰기 재시도는 중복 처리 방지를 검증한다.

## limits

업무 유실·중복을 숨겨 속도 개선으로 보고하지 않는다. 의존 서비스 문제인지 로컬 포화인지 구분한다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
