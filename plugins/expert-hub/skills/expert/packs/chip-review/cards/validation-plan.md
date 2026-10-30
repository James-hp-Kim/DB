# 독립 검증과 개선 효과 평가

ID: `chip-review:validation-plan` | both | reference-only

진단 정확도는 정답·모집단·오탐/미탐 정의가 있어야 평가할 수 있다.

## conditions

테스트 설계와 채점 기준을 먼저 정하고 진단 대상·결함 단위·정답·전문가 검토의 독립성을 확보한다.

## procedure

범위별 정상/결함 사례, 숨긴 정답, 동일 모델/예산, 스킬 유무 비교를 설계한다. 개선안은 동일 조건의 전후값과 기능 회귀를 확인한다. 이 패키지는 해당 독립 평가를 수행하지 않았다.

## limits

선택한 주입 결함 6/6 탐지는 전체 진단 정확도 100%가 아니다. expert persona는 자격 인증이 아니다.

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [K-Dense-AI/scientific-agents](https://github.com/K-Dense-AI/scientific-agents/tree/98c7fae46648724e1a43a1f2b207b0c82fcc462e) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
