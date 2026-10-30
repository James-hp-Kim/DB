# 합리적 군구분과 혼합 모집단

ID: `quality:rational-subgroups` | both | reference-only

비슷한 조건의 관측을 묶고, 제품·LOT·설비 간 차이와 시간 내 변동을 구분한다.

## conditions

동일 제품·동일 규격·공정 단계·측정법을 먼저 맞춘다. 군 안과 군 사이에 어떤 변동을 담을지 설계한다.

## interpretation

제품 A가 주로 장비 1에서 생산되고 제품 B가 장비 2에서 생산되면 장비 평균 차이가 제품 차이일 수 있다.

## limits

행을 무작위로 섞어 관리도를 그리지 않는다. 같은 LOT의 여러 die를 독립 LOT처럼 처리하지 않는다.

## procedure

간단 비교는 조건별 층화 표로 시작한다. 효과가 층별로 달라지거나 비교 가능한 자료가 없으면 deep으로 올린다.

## verification

군 크기·생산 시점·검사 선택 방식을 기록하고 합리적 군을 사후 유리한 결과에 맞춰 바꾸지 않는다.

## 출처

- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
- [NIST: Product and process comparisons](https://www.itl.nist.gov/div898/handbook/prc/prc.htm) · primary · 확인 2026-10-29
