# C05 검토: hdl-tools의 multicycle은 언제나 setup N / hold 1

ID: `chip-rtl:claim-c05` | both | reference-only

교정: 동일 waveform에서 원래 hold 관계를 복원하는 일반 패턴은 setup N / hold N−1. 다른 clock·위상·edge·의도는 별도 확인.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

동일 waveform에서 원래 hold 관계를 복원하는 일반 패턴은 setup N / hold N−1. 다른 clock·위상·edge·의도는 별도 확인.

## verification

sources/hdl-tools/digital-chip-design-agents/plugins/sta/skills/sta/SKILL.reference.txt:147,243; synthesis:119

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님
N/N−1은 이 조건의 패턴; 다른 clock 관계에 무조건 적용 금지

## detail

검토한 주장: hdl-tools의 multicycle은 언제나 setup N / hold 1
판정: 교정

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [AMD UG903: Relaxing Setup While Maintaining Hold](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/Relaxing-Setup-While-Maintaining-Hold) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
