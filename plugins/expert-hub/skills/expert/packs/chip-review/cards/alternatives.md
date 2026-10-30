# 문제 진단·개선 대안 비교

ID: `chip-review:alternatives` | both | reference-only

기능 오류와 개선 기회를 분리하고 동일 조건에서 효과와 비용을 비교한다.

## conditions

동일 workload·corner·전압·클록·입출력 조건 및 면적/전력 정의가 필요하다.

## procedure

근거 위치 → 현상 → 원인 가설 → 최소 변경/구조 변경 → 기능·지연·처리량·PPA 비용 → 검증 작업 → 채택 조건을 제시한다. 측정이 없으면 기대 효과는 정성으로 둔다.

## limits

파이프라이닝·retiming·자원 공유는 지연/인터페이스 계약을 바꿀 수 있다. 실제 측정 없는 개선율을 만들지 않는다.

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [AMD UG907 Supported Inputs](https://docs.amd.com/r/en-US/ug907-vivado-power-analysis-optimization/Supported-Inputs) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
