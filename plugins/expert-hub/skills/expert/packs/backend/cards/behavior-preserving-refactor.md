# 동작 보존을 기준으로 한 코드 단순화

ID: `backend:behavior-preserving-refactor` | both | reference-only; no external tool installed

공개 인터페이스·출력·오류 처리와 데이터 의미를 보존하면서 관련 코드만 정리한다.

## conditions

구조 정리와 기능 변경을 구분하고 보존해야 할 관찰 동작을 먼저 정한다. 기존 인터페이스·오류·권한·데이터 의미를 변경하지 않는 것이 목표다.

## procedure

변경 전 의미 있는 검사 결과를 확보한다. 최근 변경 또는 요청된 범위에서 중복·불필요한 분기·과도한 추상화를 줄인다. 줄 수 감소보다 명확성과 책임 경계를 우선한다. 기존 구현과 표준 기능을 우선 재사용한다. 필요한 호출부·검사까지 함께 고친다.

## verification

영향받은 동작·경계·실패 사례를 변경 전후 대조한다. 기존 검사로 증명할 수 없는 부분을 밝히고 확인하지 않은 성능 개선을 주장하지 않는다.

## limits

형식 검사나 코드 리뷰만으로 동작 보존을 증명할 수 없다. 운영 배포·삭제·인터페이스 변경 권한은 별도이며 원문 모델 지정·자동 활성화 지침은 제외했다.

## 출처

- [cofa-simplify — 공개 준비 지침의 일반 절차](https://github.com/arcturus0637-rgb/cofa-prelim-kit/blob/28479b0820c3933c7d2aa5aa9efb529577a7e593/skills/cofa-simplify/SKILL.md) · public-preparation-guidance · 확인 2026-10-30
- [ponytail 선택 절차의 공개 근거](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
