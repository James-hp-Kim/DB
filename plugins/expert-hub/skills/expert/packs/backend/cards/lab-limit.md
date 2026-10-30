# 추가 재현의7/320시간 초과와 실패 판정

ID: `backend:lab-limit` | both | reference-only

추가 재현의 인덱스 재적용 회차에서7/320건(2.1875%) 풀 시간 초과. 원인은 미확인이고 성능 판정은 실패다.

## conditions

첫 실험과 별도 생성·실행한 합성 재현 기록이다. 해당 회차320요청,40회/초,8초.

## procedure

SQL오류0, 종료 시 가용 연결4, p95 154.11ms를 관찰했다. 누수 재발이나 특정 OS원인으로 단정하지 않는다. 회귀 기능 통과와 성능 기준 실패를 따로 기록한다.

## limits

최초 판정 스크립트가 이 회차 실패를 반영하지 않아 보완했다. 보완 후 같은 실패 기록은 exit1이며 재시험 성공으로 덮지 않았다.

## verification

원본 요청/지표와 보완 판정 JSON을 보존한다. 7÷320×100=2.1875%.

## 출처

- [추가 합성 재현: 성능 실패 판정](../../../evidence/backend-lab/reproduction-02/reproduction-checks.json) · measured-synthetic · 확인 2026-10-29
