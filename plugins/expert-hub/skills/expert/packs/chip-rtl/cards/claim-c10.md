# C10 검토: liveness는 언제나 유한 BOUND를 둬야 한다

ID: `chip-rtl:claim-c10` | both | reference-only

조건부: bounded response는 실무 요구사항일 수 있지만 unbounded liveness와 다른 명세다. SBY는 live 모드를 별도로 지원한다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

bounded response는 실무 요구사항일 수 있지만 unbounded liveness와 다른 명세다. SBY는 live 모드를 별도로 지원한다.

## verification

formal SKILL.reference.txt:74,84; SBY Options

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님
bounded PASS를 unbounded 증명으로 표현하지 않음
PREUNSAT 통과만으로 모든 overconstraint가 제거됐다고 할 수 없음

## detail

검토한 주장: liveness는 언제나 유한 BOUND를 둬야 한다
판정: 조건부

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [SBY file format reference](https://yosyshq.readthedocs.io/projects/sby/en/stable/reference.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [YosysHQ AppNote-011 Interpreting results](https://yosyshq.readthedocs.io/projects/ap011/en/latest/interpret.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
