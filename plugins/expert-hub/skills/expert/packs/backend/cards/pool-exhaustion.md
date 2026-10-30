# DB 연결 풀 고갈: 임시조치와 영구수정

ID: `backend:pool-exhaustion` | both | reference-only

풀 대기·가용 연결·트랜잭션·예외 경로로 고갈을 확인한다. 임시 복구와 연결 생명주기 수정을 분리한다.

## conditions

풀 상한·사용/대기 수, acquire timeout, 오래 열린 트랜잭션과 최근 배포를 확인한다.

## procedure

비필수 작업과 유입 동시성을 기존 절차 내에서 제한한다. 재시작이 필요하면 소유 대상·진행 중 작업·관측/복원 범위를 확인한다. 영구수정은 성공·예외·취소 경로의 연결 반환, 드라이버의 불량 연결 폐기, 트랜잭션 종료를 검증한다.

## limits

무조건 풀이나 앱 수를 늘리면 DB를 더 포화시킬 수 있다. 재시작 성공은 원인 제거 증거가 아니다.

## verification

실패 경로를 다시 주입하고 일반 업무가 정상 처리되는지, 연결이 회수되는지 확인한다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
- [2026-10-29 합성 HTTP/SQLite 첫 실험](../../../evidence/backend-lab/lab-20261029/verification-summary.json) · measured-synthetic · 확인 2026-10-29
