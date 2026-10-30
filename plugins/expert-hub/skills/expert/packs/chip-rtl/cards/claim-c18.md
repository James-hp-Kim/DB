# C18 검토: 다른 workload·전압·corner 결과의 PPA 차이를 설계 개선율로 바로 비교한다

ID: `chip-rtl:claim-c18` | both | reference-only

조건부: 조건을 고정하거나 차이를 통제한 실험이 필요하다. 단순 수치 차이를 변경의 인과 효과로 표현하지 않는다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

조건을 고정하거나 차이를 통제한 실험이 필요하다. 단순 수치 차이를 변경의 인과 효과로 표현하지 않는다.

## verification

본 패키지의 비교 실험 원칙; 특정 업체의 공식 채점 기준 아님

## limits

positive slack은 해당 path requirement 충족 의미; 전체 칩 보증 아님
저자 연구 결과; 이번 환경에서 재현 안 함. 실제 DRAM cell signoff가 아님
simulation-based estimate를 silicon 측정값으로 표현하지 않음

## detail

검토한 주장: 다른 workload·전압·corner 결과의 PPA 차이를 설계 개선율로 바로 비교한다
판정: 조건부

## 출처

- [AMD UG907 Supported Inputs](https://docs.amd.com/r/en-US/ug907-vivado-power-analysis-optimization/Supported-Inputs) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [AMD UG906: Timing Path Summary](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Timing-Path-Summary-Header-Information) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [Ramulator 2.1: A Composable Memory System Simulator for Modern DRAM Systems](https://arxiv.org/abs/2606.13844) · 논문 / 본문 §2–4 확인 · 확인 2026-10-29
