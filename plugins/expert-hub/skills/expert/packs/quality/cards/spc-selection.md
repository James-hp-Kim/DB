# SPC 관리도 선택

ID: `quality:spc-selection` | both | monitor subset; other charts reference-only

연속 측정치, 부적합품 비율, 결함 건수, 표본 크기에 따라 관리도를 고른다.

## procedure

연속값: 합리적 군이 있으면 Xbar-R 또는 Xbar-S, 개별 관측은 I-MR 등을 검토한다. 단순히 숫자로 표현된다는 이유로 계량형 관리도를 선택하지 않는다.
부적합품: p(검사 수 변동), np(고정 검사 수). 결함: c(일정 기회/면적), u(변동 노출량).

## limits

시계열 자기상관, 과산포, 불균일 기회, 드문 사건은 기본 가정을 깨므로 모델 조정이 필요하다.
이 패키지 monitor는 지정한 개별 관측 평균/표준편차에 대한 WECO/EWMA/CUSUM만 실행한다. 모든 관리도 생성기를 제공하지는 않는다.

## conditions

Phase I에서 기준 구간과 특수원인을 검토하고 Phase II에 고정 기준으로 감시한다. 규격선을 관리한계로 대신 쓰지 않는다.

## 출처

- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
- [NIST: Attributes control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc33.htm) · primary · 확인 2026-10-29
