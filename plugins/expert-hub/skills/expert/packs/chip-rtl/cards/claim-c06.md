# C06 검토: Slack은 setup·hold 모두 required−arrival

ID: `chip-rtl:claim-c06` | both | reference-only

교정: 일반적인 setup/recovery는 required−arrival, hold/removal은 arrival−required.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

일반적인 setup/recovery는 required−arrival, hold/removal은 arrival−required.

## verification

K-Dense SKILL.reference.txt:32

## limits

광범위한 텍스트 지침; hold slack 및 Pegasus 표기 교정 필요. 실제 반도체 진단 성능은 미검증
positive slack은 해당 path requirement 충족 의미; 전체 칩 보증 아님

## detail

검토한 주장: Slack은 setup·hold 모두 required−arrival
판정: 교정

## 출처

- [K-Dense-AI/scientific-agents](https://github.com/K-Dense-AI/scientific-agents/tree/98c7fae46648724e1a43a1f2b207b0c82fcc462e) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [AMD UG906: Timing Path Summary](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Timing-Path-Summary-Header-Information) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
