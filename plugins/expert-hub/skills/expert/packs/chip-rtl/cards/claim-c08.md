# C08 검토: 일반 .ys 합성 스크립트는 yosys -c synth.ys

ID: `chip-rtl:claim-c08` | both | reference-only

교정: native Yosys 명령 스크립트는 -s를 사용. -c는 Tcl 언어로 작성된 파일일 때 사용.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

native Yosys 명령 스크립트는 -s를 사용. -c는 Tcl 언어로 작성된 파일일 때 사용.

## verification

hdl-tools synthesis SKILL.reference.txt:94
2026-10-29 후속 공개 실험: chip-rtl:public-benchmark. 비블라인드 주입 결함의 탐지 결과이며 일반 진단 정확도가 아님.

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님
확장자만으로 언어가 강제되는 것은 아니며 파일 내용과 옵션을 맞춤

## detail

검토한 주장: 일반 .ys 합성 스크립트는 yosys -c synth.ys
판정: 교정

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [Yosys 0.70 Command line reference](https://yosyshq.readthedocs.io/projects/yosys/en/v0.70/cmd_ref.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
