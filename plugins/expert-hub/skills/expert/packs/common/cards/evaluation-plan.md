# 새 환경 수용 검증과 실무 평가

ID: `common:evaluation-plan` | both | reference-only

설치·검색·수식 동작과 현장 분석 성능을 별도 검증한다.

## verification

패키지 검증: 파일 해시, Python/SQLite FTS, 스킬 YAML, 링크, 한·영 검색, DB 출처, MCP lifecycle/tools, CLI 입력 경계와 계산값, 이동 경로 동작.
합성 데이터: 알려진 중복/0분모/극단값/평균 이동이 의도대로 표시되는지 확인. 실제 불량 검증이라는 표현을 쓰지 않는다.
실무 평가: 과거 사건과 정상 기간을 분리해 탐지·누락·오경보·분석 소요·조치 유용성을 평가한다. 같은 문제를 quick/deep으로 비교하되 정답과 영향 위험도도 본다.
새 컴퓨터에서 문서의 스모크테스트를 실행한 뒤 Codex 새 대화에서 실제 도구 호출을 확인한다. 실제 출력·종료 상태를 확인하고 통과·실패·미실행으로 보고한다. 빌드·정적 검사만으로 전체 입력→출력 경로가 검증되었다고 하지 않는다. 관련 코드·데이터·설정이 바뀌면 영향받은 기존 증거를 재검증한다.

## limits

토큰 평가: 스킬/검색/선택 카드의 텍스트량과 실제 작업의 전체 토큰을 구별한다. 파일 크기나 추정 토큰 감소만으로 비용 절감을 보장하지 않는다.

## conditions

검증 대상 버전·입력·환경과 성공 기준을 먼저 정한다. 설치 여부, 실제 기능, 현업 성능은 서로 다른 검증 대상이다.

## 출처

- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
- [cofa-verify — 공개 준비 지침의 일반 절차](https://github.com/arcturus0637-rgb/cofa-prelim-kit/blob/28479b0820c3933c7d2aa5aa9efb529577a7e593/skills/cofa-verify/SKILL.md) · public-preparation-guidance · 확인 2026-10-30
