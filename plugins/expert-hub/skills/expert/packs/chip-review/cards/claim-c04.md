# C04 검토: 스킬을 설치하면 EDA 도구·PDK·상업 라이선스도 준비된다

ID: `chip-review:claim-c04` | both | reference-only

교정: 스킬은 작업 지침·관련 자원이다. 도구 설치, 연결, 모델, 라이선스는 별도 확인 대상이다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

스킬은 작업 지침·관련 자원이다. 도구 설치, 연결, 모델, 라이선스는 별도 확인 대상이다.

## verification

SKILL와 실행 환경의 역할 구분

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님
실제 Virtuoso 연결·실행 환경 필요; 범용 반도체 분석기가 아님. 포함된 파일은 선택된 참고 문서이며 전체 실행 패키지 아님
1 fF/1 Mohm 필터를 검증 보증으로 해석 금지. Spectre/API·관련 스킬 등 실행 의존성 확인 필요
스킬 설치 자체가 전문성·정확성의 보증이라는 내용은 아님

## detail

검토한 주장: 스킬을 설치하면 EDA 도구·PDK·상업 라이선스도 준비된다
판정: 교정

## 출처

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) · primary · 확인 2026-10-29
- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [Matthew-Laplace/custom-digital-in-analog-environment](https://github.com/Matthew-Laplace/custom-digital-in-analog-environment/tree/ed172b943c54e961d4aaefea95168d0e1297ca52) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [Arcadia-1/analog-agents](https://github.com/Arcadia-1/analog-agents/tree/4d6bd218ceff60624d7ee62887787aa83daecdb4) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
