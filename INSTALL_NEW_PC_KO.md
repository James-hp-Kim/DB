> 2026-10-31 지침 연결 수정 사본: 먼저 [AUTO_START_KO.md](AUTO_START_KO.md)를 확인하세요. 기존의 수동 START 문구 안내보다 이 연결 절차를 우선합니다.

# 새 PC에서 설치하기 — 2.5.2

**2.5.2는 격리된 Windows 설치·스킬 인식·MCP 호출·합성 분석을 확인했습니다.** [검증 범위](docs/ISOLATED_VALIDATION_252.md)를 확인하세요. 같은 PC의 기존 Python/Codex 실행 파일을 사용했으며 완전히 새 OS와 계정 로그인은 시험하지 않았습니다. 설치기는 실제 검사를 수행합니다.

이 안내는 Windows PC를 기준으로 합니다. 다른 Skill, MCP 서버, Plugin은 필요하지 않습니다.
Python과 MCP를 지원하는 앱은 필요합니다. DB 조회 서버에는 별도 API 키가 필요하지 않습니다.

## 1. 필요한 프로그램을 준비합니다

1. [Python 공식 설치 페이지](https://www.python.org/downloads/windows/)를 엽니다.
2. Python 3.11 이상을 설치합니다. 설치 화면에 PATH 추가 항목이 있으면 선택합니다.
3. [OpenAI 공식 시작 안내](https://developers.openai.com/codex/quickstart)에 따라 Codex를 준비합니다.
4. 앱에 로그인합니다.

기존 Python이 있으면 다시 설치할 필요가 없습니다. 설치기는 Python 버전과 SQLite FTS5 기능을 검사합니다.
Python 설치와 앱 로그인은 사용자가 수행합니다. 이 묶음에는 운영체제와 런타임이 들어 있지 않습니다.

## 2. 설치 묶음을 풉니다

1. ExpertHub 2.5.2 ZIP을 새 PC로 복사합니다.
2. ZIP의 압축을 모두 풉니다.
3. 압축을 푼 폴더를 엽니다.

압축 안에서 바로 실행하지 마세요. 원래 PC의 절대 경로를 새 PC에 붙여 넣지 마세요.

## 3. 설치기를 실행합니다

1. `Setup-NewPC.cmd`를 두 번 클릭합니다.
2. 설치 결과를 확인합니다.

설치기는 파일 체크섬을 확인합니다. 기본 설치 위치는 현재 사용자의 `.agents\skills\expert`입니다.
같은 폴더가 이미 있으면 덮어쓰지 않고 중단합니다. 기존 설치의 업데이트 도구가 아닙니다.

Codex CLI가 있으면 `expert-knowledge` MCP 등록도 수행합니다.
Codex CLI가 없으면 설치기가 새 PC에 맞는 실행 명령과 인수를 표시합니다.
Python을 찾지 못하면 공식 설치 링크를 표시하고 중단합니다.

`Setup-NewPC.cmd`는 이번 실행의 PowerShell 정책만 지정합니다. 컴퓨터의 영구 실행 정책은 바꾸지 않습니다.
조직에서 스크립트 실행을 금지한 경우에는 관리자 정책을 따르세요.

## 4. MCP 연결을 완료합니다

자동 등록이 끝났으면 5단계로 이동합니다.

앱별 화면이 다릅니다. 아래 화면은 공식 안내의 desktop/IDE 예시이며 모든 Codex 앱에서 동일한 메뉴가 있다고 확인한 것은 아닙니다. 해당 메뉴가 없으면 지원 Codex CLI의 `codex mcp add` 등록 경로를 사용합니다.

1. 사용 중인 앱이 제공하는 **Settings → MCP servers**를 엽니다.
2. **Add server**를 선택합니다.
3. 이름을 `expert-knowledge`로 입력합니다.
4. 연결 형식을 **STDIO**로 선택합니다.
5. 설치기가 표시한 Command와 Arguments를 입력합니다.
6. 저장합니다.

Arguments는 표시된 배열의 각 값을 개별 인수로 입력합니다.
Python과 `mcp_server.py`에는 새 PC의 절대 경로를 사용합니다.
다른 MCP 앱도 같은 STDIO 명령을 사용할 수 있습니다. 앱마다 입력 화면은 다릅니다.

## 5. 서버를 다시 연결합니다

1. MCP 서버 설정에서 **Restart**를 선택합니다.
2. 새 채팅을 엽니다.
3. 입력창에서 `/mcp`를 확인합니다.
4. `expert-knowledge` 연결 상태를 확인합니다.

CLI 등록과 앱 재연결은 별개입니다. 설치기의 서버 검사가 통과해도 기존 채팅이 새 서버로 바뀌었다고 판단하지 않습니다.
앱에서 Restart를 제공하지 않으면 앱을 정상 종료한 뒤 다시 엽니다.

## 6. 페르소나를 불러옵니다

새 채팅에서 다음과 같이 요청합니다.

```text
$expert 품질보증 관점으로 내 자료를 검토해줘.
fact-grounding 지침을 읽고, 확인된 사실과 미확인을 구분해줘.
선택 도구는 필요할 때 목적과 범위를 설명하고 먼저 물어봐.
```

설치기는 새 MCP 연결에서 9개 페르소나를 각각 조회합니다.
새 DB 항목, 기존 추가 항목, 출처, fact-grounding 파일의 해시를 확인합니다.
이는 지침이 전달되는지 확인하는 검사입니다. 모델의 모든 답변이 정확하다는 검사는 아닙니다.

## fact-grounding이 없는 PC

설치된 `fact-grounding/SKILL.md`가 있으면 그 파일을 우선합니다.
없으면 동봉된 `references/fact-grounding.md`를 읽도록 안내합니다.
별도 스킬이 없어도 지침을 사용할 수 있습니다. 동봉 사본을 썼다는 사실은 답변에 밝힙니다.

## 선택 기능을 사용하는 방법

일반 작업은 기본 절차로 처리합니다. 선택 방법 10개는 자동 실행하지 않습니다.
원본 플러그인 전체 대신 검토한 로컬 절차를 포함했습니다.

```text
이건 복잡한 문제야. 사용할 심화 방법 하나와 종료 조건을 먼저 제안해줘.
내 동의를 받은 뒤에만 적용해줘.
```

“복잡한 문제”라고 말해도 사용 동의가 되지는 않습니다.
Grill Me는 Grilling으로 연결합니다. 둘을 중복 실행하지 않습니다.
[도구별 기능·의존성·한계](docs/OPTIONAL_METHODS_250.md)를 참고하세요.

## 직접 검사하기

압축을 푼 폴더에서 PowerShell을 엽니다.

```powershell
python -B -X utf8 scripts/verify_release.py
python -B -X utf8 plugins/expert-hub/skills/expert/scripts/verify_install.py
```

`passed: true`는 이 검사 범위가 통과했다는 뜻입니다.
실제 새 PC의 앱 연결과 답변은 그 PC에서 확인해야 합니다.

## Python 경로를 직접 지정해야 할 때

다음의 예시 경로를 새 PC의 실제 Python 경로로 바꿉니다.

```powershell
.\Setup-NewPC.ps1 -PythonExe 'C:\실제 Python 폴더\python.exe'
```

자동 MCP 등록을 원하지 않으면 `-ManualMcp`를 추가합니다. 이 옵션도 설치 후 MCP 실행 검사를 수행하며 검사 생략 옵션이 아닙니다.
이 경우 설치만 완료되고 MCP는 4단계에서 직접 등록해야 합니다.

## 운영체제 범위

두 번 클릭하는 설치기는 Windows용입니다. macOS와 Linux의 설치 자동화는 검증하지 않았습니다.
Python 서버 자체는 표준 라이브러리로 작성했습니다. 다른 운영체제에서는 Python 3.11+와 SQLite FTS5를 준비하고 `scripts/mcp_server.py`를 STDIO 서버로 등록할 수 있습니다. 해당 환경의 실행 검증은 별도로 필요합니다.

## 설명 방식과 출처

한국어가 자연스럽도록 ASD-STE100의 명확성 원칙을 느슨하게 참고했습니다.
짧은 문장, 한 단계에 한 동작, 일관된 용어를 사용합니다. ‘80%’는 요청한 적용 강도이며 준수율을 측정한 값이 아닙니다.

- [ASD-STE100 공식 사이트](https://www.asd-ste100.org/)
- [OpenAI MCP 설정 안내](https://learn.chatgpt.com/docs/extend/mcp?surface=cli): STDIO 등록, 저장 후 Restart, 연결 확인.
- [Python Windows 배포](https://www.python.org/downloads/windows/)

원본 외부 설치 스크립트를 실행하지 않았습니다. 선택 MCP의 인증값과 개인 설정은 이 묶음에 포함하지 않습니다.

## 시험환경 시작 지침

기본 Skill 설치기는 expert만 복사합니다. 새 exam-setup 지침을 다른 폴더에서도 불러오려면 [별도 복사/Plugin 경로](docs/EXAM_SETUP_KO.md)를 따르세요. 별도 복사와 Plugin 경로 모두 격리 환경에서 스킬 발견을 확인했습니다. Plugin 설치에서는 `$expert-hub:expert`, `$expert-hub:exam-setup`처럼 표시되는 실제 이름을 사용하세요.
