# 선택 기능의 동의와 조회량 제한

ID: `common:optional-method-consent` | both | reference-only; optional procedures require user consent

기본 경로는 작은 범위의 근거만 읽는다. 선택 기능은 사용 전에 동의를 받고 심화 기능은 사용자가 복잡한 문제라고 표현한 경우에만 제안한다.

## conditions

사용자 요청을 해결하는 데 일반 경로보다 추가 방법이 실제로 필요할 때 적용한다. 스킬 이름을 조사해 달라는 요청은 실행 동의가 아니다.

## procedure

목적·선택 항목 하나·범위·종료 조건을 짧게 알리고 사용 여부를 묻는다. 동의가 없으면 기본 경로를 계속한다. 심화 기능은 복잡한 문제라는 사용자 표현도 필요하다. 같은 작업과 범위에 이미 받은 동의는 재사용한다.

## verification

방법 본문은 scripts/optional_methods.py read NAME --context KEY --approved로 읽는다. 심화 기능은 --complex도 필요하다. 이 플래그는 호출자의 선언이며 사용자 동의의 독립적인 증명이 아니다.

## limits

문자 수 상한은 토큰 절감률이 아니다. 전체 스킬·모든 페르소나·반복 검사를 자동으로 불러오지 않는다. 원본 패키지는 설치하지 않는다.

## 출처

- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
- [context7 선택 절차의 공개 근거](https://github.com/upstash/context7/blob/c964733a3d87e89acd177cc4b24ebef4a7662f06/README.md) · upstream-technical-guidance · 확인 2026-10-30
- [grill-me 선택 절차의 공개 근거](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grill-me/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
