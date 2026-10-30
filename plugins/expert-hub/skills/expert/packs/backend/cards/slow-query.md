# 느린 쿼리와 인덱스 검증

ID: `backend:slow-query` | both | reference-only

계획과 실제 호출 분포로 스캔·정렬·추정 행 수를 검토하고, 인덱스 쓰기/저장/잠금 비용도 확인한다.

## conditions

DB종류·버전, 쿼리와 파라미터 분포, 데이터량, 통계 시각, 기존 인덱스가 필요하다.

## procedure

범위를 제한한 실행계획부터 본다. 조건·조인·정렬과 인덱스 순서를 연결한다. 작은 변경 하나를 적용해 같은 데이터·부하에서 재측정하고 원복 또는 전진 복구 경로를 기록한다.

## limits

읽기 속도만으로 인덱스를 승인하지 않는다. 쓰기 증폭·생성 중 잠금·복제·디스크 비용은 별도 검증해야 한다.

## verification

결과 행/총액 정확성, 계획 변화, 지연과 실패율, 쓰기 경로를 확인한다.

## 출처

- [성능 비교·검증 지침](../../../references/backend/performance.md) · authored-workflow · 확인 2026-10-29
- [2026-10-29 합성 HTTP/SQLite 첫 실험](../../../evidence/backend-lab/lab-20261029/verification-summary.json) · measured-synthetic · 확인 2026-10-29
