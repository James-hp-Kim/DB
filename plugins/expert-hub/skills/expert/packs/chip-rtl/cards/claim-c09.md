# C09 검토: 각 assume을 제거하면 property가 반드시 실패해야 vacuity 검사를 통과한다

ID: `chip-rtl:claim-c09` | both | reference-only

교정: 보편적 기준이 아니다. 속성이 가정 없이도 참일 수 있다. antecedent/witness reachability와 과도한 제약을 확인한다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

보편적 기준이 아니다. 속성이 가정 없이도 참일 수 있다. antecedent/witness reachability와 과도한 제약을 확인한다.

## verification

formal SKILL.reference.txt:131; verification:622. 가정과 무관한 항상 참인 속성이 반례가 됨
2026-10-29 후속 공개 실험: chip-rtl:public-benchmark. 비블라인드 주입 결함의 탐지 결과이며 일반 진단 정확도가 아님.

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님
PREUNSAT 통과만으로 모든 overconstraint가 제거됐다고 할 수 없음

## detail

검토한 주장: 각 assume을 제거하면 property가 반드시 실패해야 vacuity 검사를 통과한다
판정: 교정

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [YosysHQ AppNote-011 Interpreting results](https://yosyshq.readthedocs.io/projects/ap011/en/latest/interpret.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
