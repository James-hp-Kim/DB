# C17 검토: VCD/SAIF 기반 전력 분석은 실측 칩 전력이다

ID: `chip-rtl:claim-c17` | both | reference-only

교정: activity와 모델을 이용한 추정이다. 실제 측정 자료가 없으면 실측으로 표기하지 않는다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

activity와 모델을 이용한 추정이다. 실제 측정 자료가 없으면 실측으로 표기하지 않는다.

## verification

OpenSTA activity 입력; AMD power estimation 입력

## limits

입력·corner·constraint가 필요; signoff 전 영역을 증명하지 않음
simulation-based estimate를 silicon 측정값으로 표현하지 않음

## detail

검토한 주장: VCD/SAIF 기반 전력 분석은 실측 칩 전력이다
판정: 교정

## 출처

- [The-OpenROAD-Project/OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA/tree/384b539085c54eef46cbaa02e2e17d2b983247e5) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [AMD UG907 Supported Inputs](https://docs.amd.com/r/en-US/ug907-vivado-power-analysis-optimization/Supported-Inputs) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
