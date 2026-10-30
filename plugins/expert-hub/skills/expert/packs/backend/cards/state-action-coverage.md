# 상태와 사용자 동작별 결과 검증

ID: `backend:state-action-coverage` | both | reference-only; optional procedures require user consent

상태 종류 × 사용자 동작별 기대 결과와 검사를 연결한다. 공통 코드 경로의 일부 검사만으로 다른 상태를 검증했다고 하지 않는다.

## conditions

상태 전이 또는 API 계약을 바꾸는 복잡한 변경에서 선택 검토를 승인받았을 때 적용한다.

## procedure

상태와 사용자 동작을 나열한다. 요구 의미에서 기대 데이터 결과를 정한다. 각 조합을 실제 검사와 연결하고 변경된 입력·출력·오류·페이지 처리 계약을 비교한다.

## verification

기대 결과와 실제 데이터를 확인한다. 상태 필드만 보거나 유사 종류의 검사로 대체하지 않는다. 없는 검사는 미검증으로 표시한다.

## limits

검사 부재는 결함 확정이 아니다. 원본 gstack 검사기·자동 리뷰·배포는 실행하지 않는다.

## 출처

- [gstack 선택 절차의 공개 근거](https://github.com/garrytan/gstack/blob/ce3a093a6421f84705ff6d58b1b2b022ca9e945d/review/specialists/api-contract.md) · upstream-technical-guidance · 확인 2026-10-30
- [gstack-state 선택 절차의 공개 근거](https://github.com/garrytan/gstack/blob/ce3a093a6421f84705ff6d58b1b2b022ca9e945d/review/specialists/state-machines.md) · upstream-technical-guidance · 확인 2026-10-30
