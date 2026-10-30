# AMD UG907 Supported Inputs

ID: `chip-rtl:resource-d23` | both | reference-only

제약·SAIF activity·운영 조건·vectorless/default activity가 전력 추정 입력 — simulation-based estimate를 silicon 측정값으로 표현하지 않음

## conditions

제약·SAIF activity·운영 조건·vectorless/default activity가 전력 추정 입력

## procedure

주장별 근거 또는 학습 자료

## limits

simulation-based estimate를 silicon 측정값으로 표현하지 않음

## verification

관련 본문 확인; 전체 문헌의 모든 문장 독립 검증 아님. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C17: activity와 모델을 이용한 추정이다. 실제 측정 자료가 없으면 실측으로 표기하지 않는다.
C18: 조건을 고정하거나 차이를 통제한 실험이 필요하다. 단순 수치 차이를 변경의 인과 효과로 표현하지 않는다.

## 출처

- [AMD UG907 Supported Inputs](https://docs.amd.com/r/en-US/ug907-vivado-power-analysis-optimization/Supported-Inputs) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
