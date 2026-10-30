# 시간 의존·자기상관·변화점

ID: `common:time-structure` | deep | monitor subset

행 순서, 공정 변경, 정상 운전 상태를 보존한다. 시간 자료를 독립 표본으로 섞지 않는다.

## conditions

장비별·제품별·레시피별 시간 흐름을 분리한다. 장비 정비·센서 교정·LOT 전환·레시피 변경 이력을 같은 시간축에 놓는다.

## procedure

관리도 신호가 실제 변화인지, 자기상관/주기/운전 상태 변화의 결과인지 확인한다. 필요하면 모델 잔차를 감시한다.

## interpretation

변화점 탐색은 기준선이 바뀐 구간을 제안할 수 있지만 원인 사건을 확정하지 않는다. 여러 후보 구간을 같은 데이터로 선택·확정하는 편향을 고려한다.

## limits

본 monitor는 누락값과 불명확한 순서에 실패하도록 설계했다. 공백을 삭제하거나 자동 정렬해 조용히 처리하지 않는다.

## 출처

- [NIST: EWMA control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm) · primary · 확인 2026-10-29
- [NIST: CUSUM control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm) · primary · 확인 2026-10-29
- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
