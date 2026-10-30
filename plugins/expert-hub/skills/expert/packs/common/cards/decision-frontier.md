# 선행 조건에 따른 결정 순서

ID: `common:decision-frontier` | both | reference-only; optional procedures require user consent

복잡한 문제의 결정만 작은 단위로 관리한다. 이미 해결된 선택을 반복하지 않고 선행 조건이 충족된 질문부터 확인한다.

## conditions

사용자가 복잡한 문제라고 표현했고 해당 심화 방법 사용에 동의한 경우에만 실행한다.

## procedure

목적과 중요한 미확정 선택을 구분한다. 직접 확인할 사실은 조사한다. 선행 조건이 해결된 질문을 최대 3개씩 묻는다. 작업이 길면 결정과 근거 링크를 한 곳에 두고 필요한 부분만 다시 읽는다.

## verification

각 결정의 근거와 남은 조건을 확인한다. 사용자의 답을 대신 만들지 않는다. grill-me는 grilling의 진입점이므로 두 방법으로 중복 집계하지 않는다.

## limits

전체 원본 워크플로 설치가 아닌 로컬 축약 방법이다. 자동 에이전트 생성·외부 이슈 작성·무한 인터뷰를 허용하지 않는다.

## 출처

- [grilling 선택 절차의 공개 근거](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grilling/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
- [grill-me 선택 절차의 공개 근거](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grill-me/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
- [wayfinder 선택 절차의 공개 근거](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/wayfinder/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
