# 집단 비교: 효과크기·불확실성·가정

ID: `common:group-comparison` | deep | reference-only

독립/대응 구조와 결과변수 유형에 맞는 검정을 고르고, p값과 실제 개선 크기를 함께 본다.

## conditions

같은 부품 전후 측정이면 대응 구조, 독립 집단이면 별도 비교가 필요하다. 연속값·이항·건수·생존시간은 다른 모형이다.
평균 비교에서는 분포·분산·독립성, 반복 관측과 LOT 클러스터를 확인한다. 비정규라는 이유만으로 모든 문제를 같은 비모수 검정으로 바꾸지 않는다.

## interpretation

여러 설비/항목 비교는 검정 가족과 다중 비교 보정을 정한다. 통계적 유의성만으로 실무 중요성을 결정하지 않는다.

## verification

차이 추정값·신뢰구간·표본수·비교 기간·중요한 교란 요인을 보고한다. 원인 확정은 별도 증거가 필요하다.

## procedure

실행 시 scipy/statsmodels의 해당 버전 API를 사용하고 재현 가능한 코드/옵션을 남긴다. 이 패키지의 기본 scan은 검정까지 자동 수행하지 않는다.

## 출처

- [NIST: Product and process comparisons](https://www.itl.nist.gov/div898/handbook/prc/prc.htm) · primary · 확인 2026-10-29
- [statsmodels: multipletests](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html) · primary · 확인 2026-10-29
