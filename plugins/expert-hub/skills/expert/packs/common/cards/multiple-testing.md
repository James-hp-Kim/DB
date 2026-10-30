# FDR와 다중 비교: 많은 항목의 오경보 관리

ID: `common:multiple-testing` | deep | reference-only

수백 항목을 각각 0.05로 검사하면 우연한 신호가 늘어난다. 탐색 범위와 보정 방법을 정한다.

## procedure

탐색의 검정 가족을 먼저 정의한다. 많은 변수/그룹의 검정 결과를 취합한 뒤 적절한 FDR 또는 가족오류율 방법을 적용한다.

## conditions

Benjamini-Hochberg 등 방법의 독립성/의존성 가정을 확인한다. 보정된 p값은 결함일 확률이나 원인일 확률이 아니다.

## verification

효과크기·표본수·재현 여부를 함께 검토한다. 탐색 데이터에서 고른 항목은 별도 기간·새 LOT·확인 실험으로 재검증한다.

## limits

순차 감시의 오경보 문제는 단순 일회성 다중검정과 같지 않다. SPC에서는 ARL/검출지연과 규칙 선택도 함께 설계한다.

## 출처

- [statsmodels: multipletests](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html) · primary · 확인 2026-10-29
- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
