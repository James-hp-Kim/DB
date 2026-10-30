# 분석 전 데이터 계약: 기간·단위·분모

ID: `common:data-contract` | both | scan

불량률은 같은 기간·동일 모집단의 불량품 수/검사품 수로 계산하고, 불량 건수/검사 기회와 구분한다.

## conditions

확인할 항목: 행의 의미(개별 측정/LOT 집계/고장 이벤트), 시간대와 기간, 제품/설비/공정, 측정 단위, 규격판, 검사수와 불량품수, 재검·수리품 처리.
부적합품 수는 검사품 수를 넘을 수 없지만, 한 제품의 여러 불량 건수는 넘을 수 있다. 두 자료를 섞지 않는다.

## procedure

비율은 합계 분자/합계 분모로 계산한다. 분모가 다른 행의 백분율을 단순 평균하지 않는다. 이미 확인된 의미는 다시 묻지 않는다. 처리 결과를 바꾸는 단위·중복 식별 기준·결측 의미·제외 규칙만 추가 확인하고, 답이 없으면 영향을 받지 않는 계산부터 진행한다.

## interpretation

0/0은 0%가 아니라 계산 불가. 작은 표본과 0건도 표본수·구간을 같이 보여준다.

## limits

단위나 품목 정의가 불명확하면 확정 지표를 만들지 말고 검증 가능한 부분만 요약한다.

## 출처

- [NIST: Attributes control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc33.htm) · primary · 확인 2026-10-29
- [NIST: Proportion confidence intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) · primary · 확인 2026-10-29
- [probe-data-check — 공개 준비 지침의 일반 절차](https://github.com/PKJthecreator/probe-kit/blob/79f2f94917ad32a630fd7d13c728409d6ec3de8b/.agents/skills/probe-data-check/SKILL.md) · public-preparation-guidance · 확인 2026-10-30
