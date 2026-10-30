# 버그 최소 재현과 반증 가능한 원인 검사

ID: `backend:minimal-reproduction` | both | reference-only; no external tool installed

실제 증상을 구분하는 작은 입력과 기대값으로 원인을 좁히고 동일 재현·영향 범위의 회귀를 확인한다.

## conditions

보고된 실패와 실제 관찰 증상을 구분한다. 문제를 판별할 요청·입력·기대값과 현재 환경이 필요하다. 성능 문제는 기존 지연·성공률·정합성 지표와 함께 본다.

## procedure

문제를 재현하는 최소 사례를 구성한다. 한 번에 한 조건을 바꿔 원인 가설을 구분하고 실제 호출 경로의 책임 있는 부분만 수정한다. 재현할 수 없으면 원인을 확정하지 말고 확인한 범위와 필요한 관측을 제시한다. 여러 구성 요소가 있으면 증상을 구분할 최소 경계의 입력·출력부터 확인한다. 인증값과 전체 환경 출력은 수집하지 않는다.

## verification

수정 전 실패를 판별했던 같은 사례가 수정 후 기대값을 만족하는지 확인한다. 영향받은 기존 동작도 검사하고 재시작 같은 임시 회복과 원인 제거를 구분한다.

## limits

공개 준비 스킬의 일반 방법이며 모든 장애를 해결한다는 증거가 아니다. 개인 실행 기록·하네스 구성·광범위한 원본 로그 수집은 포함하지 않는다.

## 출처

- [cofa-debug — 공개 준비 지침의 일반 절차](https://github.com/arcturus0637-rgb/cofa-prelim-kit/blob/28479b0820c3933c7d2aa5aa9efb529577a7e593/skills/cofa-debug/SKILL.md) · public-preparation-guidance · 확인 2026-10-30
- [superpowers 선택 절차의 공개 근거](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
