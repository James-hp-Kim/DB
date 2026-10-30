# EWMA: 작고 지속적인 변화 감지

ID: `quality:ewma` | deep | monitor

이전 관측을 가중해 작은 평균 이동을 감시한다. 정상 기준과 시간 순서가 필요하다.

## procedure

z_t=lambda*x_t+(1-lambda)*z_(t-1), z_0=기준 평균. 작은 lambda는 더 긴 기억을 가진다.

## conditions

고정 기준 평균/표준편차와 시간에 따른 관리한계로 비교한다. 기본 lambda=0.2, L=3은 이 도구의 예시 시작값이며 최적·사내 표준값이 아니다.
기준 구간은 측정계 적합성·안정성과 동일 모집단 조건을 확인해야 한다. 이상 구간으로 한계를 자동 재추정하지 않는다.

## limits

누락값을 삭제해 시간을 이어 붙이거나, 장비가 다른 자료를 한 시계열로 묶지 않는다.

## verification

자기상관·불균일 시간 간격·주기 변화는 잔차 모형 등 별도 접근이 필요하다. 알려진 변화로 민감도/오경보를 평가한다.

## 출처

- [NIST: EWMA control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm) · primary · 확인 2026-10-29
