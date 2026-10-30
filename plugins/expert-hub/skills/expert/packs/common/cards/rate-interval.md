# 불량률과 Wilson 신뢰구간

ID: `common:rate-interval` | both | scan --numerator --denominator

불량품 수와 검사품 수를 함께 제시한다. 작은 표본의 높은 비율을 곧바로 최악 공정으로 판단하지 않는다.

## conditions

독립적인 이항 관측에서 불량품 k/검사품 n의 95% Wilson 구간을 계산한다. 표본수·모집단·검사 조건을 표시한다.
한 단위에서 여러 결함 이벤트가 발생하는 자료는 이항 비율이 아니다. 결함/단위 또는 노출량 모델을 사용한다.

## interpretation

합산은 sum(k)/sum(n). 0건 관측이어도 모집단 불량 확률이 0이라고 결론내리지 않는다.

## limits

LOT 안 반복 관측·클러스터·표본선정 편향이 있으면 단순 Wilson 구간이 불확실성을 과소평가할 수 있다.

## verification

두 그룹의 구간 겹침 여부만으로 유의성 검정을 대체하지 않는다. 원인 판단에는 교란 통제와 확인 실험이 필요하다.

## 출처

- [NIST: Proportion confidence intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) · primary · 확인 2026-10-29
- [NIST: Attributes control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc33.htm) · primary · 확인 2026-10-29
