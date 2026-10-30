# 선택 도구 검토 — 2.5.0 / 2026-10-30

10개 이름을 검토했습니다. Grill Me는 Grilling의 진입점이므로 실행 절차는 9개입니다. 원본 전체를 설치하지 않았습니다. 검토한 절차를 허브에 맞게 줄여 넣었습니다.

기본 기능은 바로 사용합니다. 아래 선택 기능은 이번 작업의 동의를 받은 뒤 사용합니다. 심화 항목은 사용자가 복잡한 문제라고 표현해야 제안할 수 있습니다. 표현만으로 실행 동의가 되지는 않습니다.

|이름|종류|기능|심화 전용|
|---|---|---|---|
|context7|MCP / CLI+Skill|사용 중인 라이브러리 버전의 문서를 좁혀 조회한다.|아니요; 사용 동의는 필요|
|sequential-thinking|MCP|대안별 근거와 검증 결과를 짧게 정리하고 수정한다.|예|
|ponytail|Skill / Plugin|필요한 동작을 모두 보존하며 변경을 작게 유지한다.|아니요; 사용 동의는 필요|
|knowledge-work-plugins|Plugin collection / Skills|분석을 공유하기 전에 비교 기준과 계산을 검토한다.|아니요; 사용 동의는 필요|
|gstack|Skills / supporting tools|변경된 상태 전이와 API 계약의 누락을 점검한다.|예|
|superpowers|Skills / Plugin|반복되는 실패의 원인을 증거로 좁힌다.|예|
|caveman|Skill|기술적 의미를 보존하면서 설명을 줄인다.|아니요; 사용 동의는 필요|
|grilling|Skill|중요한 결정을 선행 조건 순으로 확인한다.|예|
|grill-me|Skill alias|Grilling을 명시적으로 시작하는 원본 진입점이다.|예|
|wayfinder|Skill|여러 작업에 걸친 결정을 작은 연결 목록으로 관리한다.|예|

## context7

사용 중인 라이브러리 버전의 문서를 좁혀 조회한다.

1. 먼저 로컬 의존성 파일에서 라이브러리와 버전을 확인한다.
2. 사용자에게 Context7 조회 목적과 범위를 알리고 동의를 받는다.
3. 연결되어 있으면 알려진 libraryId를 재사용한다. 모르면 resolve-library-id로 하나를 선택한다.
4. query-docs에 구체적인 질문 하나를 전달한다. 비밀값과 업무 원문을 보내지 않는다.
5. 반환 문서의 버전과 출처를 확인한다. 같은 근거는 재조회하지 않는다.

필요 조건: 선택: Context7 MCP 연결과 인터넷. 현재 도구 명세 및 인증 조건 확인. CLI 방식은 Node.js 22.13+. 연결이 없으면 공식 문서 링크로 대조할 수 있으나 Context7을 실행했다고 말하지 않는다.

한계: 조회 결과가 정확성을 보장하지 않는다. 자동 사용 규칙과 OAuth/API 키 발급은 이 패키지에서 실행하지 않는다. 원격 URL: https://mcp.context7.com/mcp. 설치: https://context7.com/docs/resources/all-clients

근거:
- [upstash/context7 / README.md](https://github.com/upstash/context7/blob/c964733a3d87e89acd177cc4b24ebef4a7662f06/README.md) · 검토 행 25–127 · Git blob `5d763258318ad99a8324faab59c6c6b2efd72350`

## sequential-thinking

대안별 근거와 검증 결과를 짧게 정리하고 수정한다.

1. 복잡한 문제라는 사용자 표현과 이번 작업의 사용 동의를 확인한다.
2. 대안 최대 3개와 다음 검증 한 개를 정한다.
3. 관찰·가정·대안·검증 결과의 요약만 기록한다. 비공개 내부 사고 과정이나 대화 로그는 저장하지 않는다.
4. 도구를 실제 연결했다면 현재 입력 명세를 확인한다. 판단이 바뀐 항목만 수정한다.
5. 결론을 구분할 근거가 확보되거나 합의한 검사 범위가 끝나면 멈춘다.

필요 조건: 로컬 축약 절차는 추가 설치 불필요. 실제 MCP 서버는 Node.js 24+ 또는 Docker와 MCP 클라이언트 필요. 원본 도구명 sequential_thinking. DISABLE_THOUGHT_LOGGING=true 사용.

한계: 로컬 절차는 Sequential Thinking 서버 실행이 아니다. 서버는 연결 중 상태를 유지한다. 별도 설치·연결·호출은 미실행.

근거:
- [modelcontextprotocol/servers / src/sequentialthinking/README.md](https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking/README.md) · 검토 행 1–145 · Git blob `390d09646d135548481e7bab983306895f802619`

## ponytail

필요한 동작을 모두 보존하며 변경을 작게 유지한다.

1. 변경이 닿는 호출부와 오류 처리부터 확인한다.
2. 기존 기능, 표준 기능, 설치된 의존성 순으로 재사용한다.
3. 요청을 완성하는 최소 변경을 한다. 영향받는 동작을 검증한다.

필요 조건: 로컬 축약 절차는 추가 설치 불필요. 원본 플러그인과 별개다.

한계: 자동 세션 활성화, 모델 지정, 운영 훅은 반영하지 않는다. 토큰 절감률은 측정하지 않았다.

근거:
- [DietrichGebert/ponytail / skills/ponytail/SKILL.md](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md) · 검토 행 1–55 · Git blob `d64edd32265ba21cbf5270158f04e97d96925f27`

## knowledge-work-plugins

분석을 공유하기 전에 비교 기준과 계산을 검토한다.

1. 기간·모집단·분모·지표 정의가 비교 가능한지 확인한다.
2. 조인 전후 행 수와 합계를 대조한다. 일부 기간을 완결 기간과 비교하지 않는다.
3. 핵심 수치를 독립적으로 재계산한다. 결론의 한계와 필요한 수정을 표시한다.

필요 조건: 사용자가 지정한 분석 또는 계산 결과. 원본 커넥터는 로컬 절차에 필요하지 않다.

한계: data/validate-data의 선택 항목만 반영했다. 전체 플러그인 묶음의 기능·설치·연결을 검증한 것은 아니다.

근거:
- [anthropics/knowledge-work-plugins / data/skills/validate-data/SKILL.md](https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/data/skills/validate-data/SKILL.md) · 검토 행 1–100 · Git blob `30a1bac41bf9679dc7d96b7ec59a116f03ec0575`

## gstack

변경된 상태 전이와 API 계약의 누락을 점검한다.

1. 복잡한 문제라는 사용자 표현과 사용 동의를 확인한다.
2. 바뀐 기능 하나의 입력·출력·오류 계약을 비교한다.
3. 상태 종류 × 사용자 동작별 기대 결과와 실제 검사를 연결한다.
4. 같은 코드 경로를 지나는 다른 상태의 검사를 대체 증거로 쓰지 않는다.
5. 영향받은 범위의 누락과 실패만 보고한다.

필요 조건: 변경 코드와 의미를 설명한 요구사항. 로컬 축약 절차는 브라우저·Bun·외부 계정이 필요하지 않다.

한계: 원본 gstack 실행·브라우저 자동화·다중 검토자·배포는 포함하지 않는다. 검사 부재만으로 실제 결함을 확정하지 않는다.

근거:
- [garrytan/gstack / review/specialists/api-contract.md](https://github.com/garrytan/gstack/blob/ce3a093a6421f84705ff6d58b1b2b022ca9e945d/review/specialists/api-contract.md) · 검토 행 1–55 · Git blob `01a649b1b0f47bb1af78e1614924b80cddbd48fa`
- [garrytan/gstack / review/specialists/state-machines.md](https://github.com/garrytan/gstack/blob/ce3a093a6421f84705ff6d58b1b2b022ca9e945d/review/specialists/state-machines.md) · 검토 행 1–66 · Git blob `9dc973fe7ff0b96367bc43e6588bcbcbe825a71b`

## superpowers

반복되는 실패의 원인을 증거로 좁힌다.

1. 복잡한 문제라는 사용자 표현과 사용 동의를 확인한다.
2. 실패 재현과 최근 변경을 확인한다. 증거를 얻을 수 있는 최소 경계를 고른다.
3. 가설을 구분하는 검사를 하나 수행한다. 결과에 맞춰 수정한다.
4. 같은 재현과 영향받은 동작을 재검사한다.

필요 조건: 문제 입력·실제 관찰 결과. 로컬 축약 절차에 원본 스킬 설치는 불필요하다.

한계: 모든 작업에 의무화하는 절차, 자동 하위 에이전트, 무조건적인 TDD는 반영하지 않는다. 인증값·전체 환경·원본 로그를 수집하지 않는다.

근거:
- [obra/superpowers / skills/systematic-debugging/SKILL.md](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md) · 검토 행 1–130 · Git blob `62fc752aaef59a8bbed5d305f4cadc60f8ae07ed`

## caveman

기술적 의미를 보존하면서 설명을 줄인다.

1. 결론을 먼저 쓴다. 한 문장에 한 가지 내용을 담는다.
2. 명령·경로·숫자·단위·부정어·불확실성은 보존한다.
3. 문장이 모호해지면 줄이지 않는다. 자연스러운 한국어를 사용한다.

필요 조건: 추가 설치 불필요. 기존 common:review-output과 같은 방법을 재사용한다.

한계: 원시인 말투, 세션 영구 모드, 압축 프록시, 운영 훅은 포함하지 않는다. 절감률을 주장하지 않는다.

근거:
- [JuliusBrussee/caveman / skills/caveman/SKILL.md](https://github.com/JuliusBrussee/caveman/blob/9b68f7ed12b05e7efaff18e65c5a3fc2849fd0a4/skills/caveman/SKILL.md) · 검토 행 1–95 · Git blob `9a94044529e5ee1576361c891b4a271504518e6f`

## grilling

중요한 결정을 선행 조건 순으로 확인한다.

1. 복잡한 문제라는 사용자 표현과 사용 동의를 확인한다.
2. 자료로 확인할 사실은 먼저 조사한다. 사용자 선택이 필요한 결정만 남긴다.
3. 선행 결정이 해결된 질문을 한 번에 최대 3개 묻는다.
4. 이미 답한 것은 다시 묻지 않는다. 독립 작업은 계속한다.
5. 결론을 바꿀 미확정 선택이 없어지면 끝낸다. 무한 인터뷰를 하지 않는다.

필요 조건: 사용자의 이번 작업 동의. 원본의 추가 Skill 도구나 하위 에이전트는 필요하지 않다.

한계: 원본의 전체 질문 동시 제시·자동 하위 에이전트·모든 실행 정지 요구를 적용하지 않는다.

근거:
- [mattpocock/skills / skills/productivity/grilling/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grilling/SKILL.md) · 검토 행 1–38 · Git blob `d2f09a18e6a6c65c55f1271ba08dfeaf06f0bed3`

## grill-me

Grilling을 명시적으로 시작하는 원본 진입점이다.

Grilling으로 연결합니다. 중복 실행하지 않습니다.

필요 조건: 

한계: 독립 방법으로 중복 실행하지 않는다. 로컬에서는 grilling으로 연결한다.

근거:
- [mattpocock/skills / skills/productivity/grill-me/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grill-me/SKILL.md) · 검토 행 1–7 · Git blob `3947ff9c4ad980d14fc07fccbf659d47c114e81d`

## wayfinder

여러 작업에 걸친 결정을 작은 연결 목록으로 관리한다.

1. 복잡한 문제라는 사용자 표현과 사용 동의를 확인한다.
2. 목적과 이번에 결정할 질문을 적는다. 외부 이슈를 자동 생성하지 않는다.
3. 각 결정의 선행 조건과 근거 위치를 연결한다. 지금 결정할 수 있는 한 항목부터 처리한다.
4. 원문을 반복하지 않고 결정과 근거 링크를 한 곳에 둔다.
5. 목적에 필요한 결정이 끝나면 계획을 종료한다. 구현 완료와 구분한다.

필요 조건: 로컬 결정 문서만으로 가능. 외부 이슈 추적기는 선택 사항이며 쓰기 권한이 별도로 필요하다.

한계: 원본의 연구·도메인 모델링·프로토타입 스킬 연쇄 호출과 하위 에이전트는 포함하지 않는다. 100K 토큰 세션 가정은 채택하지 않는다.

근거:
- [mattpocock/skills / skills/engineering/wayfinder/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/wayfinder/SKILL.md) · 검토 행 1–85 · Git blob `975d6bf9c0a49d18a651f3335e0b4dcf8650fe31`

## DB에 반영한 내용

신규 4개: common:optional-method-consent, common:versioned-doc-retrieval, common:decision-frontier, backend:state-action-coverage.

기존 4개 보완: analytics:joins, backend:minimal-reproduction, backend:behavior-preserving-refactor, common:review-output.

총 768개 지식 항목, 323개 출처 레코드입니다. 출처 레코드 수는 서로 독립적인 증거의 수를 뜻하지 않습니다.

## 적은 입력으로 사용하는 순서

1. 페르소나 하나를 고릅니다.
2. 요약 1~3개만 조회합니다.
3. 필요한 본문 절과 출처만 읽습니다.
4. 이미 읽은 근거를 재사용합니다.
5. 선택 기능은 동의 후 하나만 읽습니다.

문자 상한과 토큰 수는 다릅니다. 토큰 절감률은 측정하지 않았습니다. 사실·단위·부정어를 삭제해 길이를 줄이지 않습니다.

## 실제 설치 범위

설치 묶음에는 expert Skill, 읽기 전용 지식 MCP, fact-grounding 사본, 선택 절차 조회기가 들어 있습니다. Context7과 Sequential Thinking 서버는 별도 선택 설치입니다. 원본 플러그인들의 전체 자동화·훅·하위 에이전트·모델 설정은 수집하거나 이식하지 않았습니다.

등록된 다른 플러그인의 전역 자동 활성화를 차단하지는 않습니다. 이 정책은 expert 허브를 사용할 때 적용하는 지침입니다. 동의 플래그는 호출자의 선언이며 사람이 동의했음을 독립적으로 인증하지 않습니다.

[새 PC 설치 안내](../INSTALL_NEW_PC_KO.md) · [검토 출처 목록](OPTIONAL_SOURCES_250.json)
