# 필요한 방법 하나만 읽기

기본 상태는 사용 안 함입니다. 도구를 조사하거나 설치한 것은 미래 사용 동의가 아닙니다.
선택 방법은 목적·범위·종료 조건을 짧게 설명하고 이번 작업의 동의를 받은 뒤 읽습니다.
동의가 없으면 일반 작업을 계속합니다. 같은 작업과 범위의 기존 동의는 재사용합니다.

심화 방법: sequential-thinking, gstack, superpowers, grilling, grill-me, wayfinder.
이 방법은 사용자가 문제를 복잡하다고 표현한 경우에만 제안합니다. 표현만으로 실행하지 않습니다.
일반 선택 방법: context7, ponytail, knowledge-work-plugins, caveman.

스킬 폴더 기준 명령:

```text
python -B -X utf8 scripts/optional_methods.py list
python -B -X utf8 scripts/optional_methods.py read NAME --context KEY --approved
```

KEY는 이 설치의 `expert_catalog`가 반환한 선택 키입니다.
심화 방법에는 `--complex`가 필요합니다. 두 플래그는 호출자의 선언입니다. 사용자 동의를 인증하는 장치는 아닙니다.
원시 JSON 전체를 읽어 동의 절차를 우회하지 않습니다.

반환되는 절차는 로컬 축약본입니다. 추가 패키지 없이 사용할 수 있습니다.
원본 스킬이나 MCP를 설치·호출한 것으로 보고하지 않습니다.
Grill Me는 Grilling의 별칭입니다. 한 번만 수행합니다.

## 외부 MCP가 실제로 필요한 경우

Context7은 해당 클라이언트의 [공식 설치 안내](https://context7.com/docs/resources/all-clients)를 확인합니다.
원격 서버 URL은 `https://mcp.context7.com/mcp`입니다. 인증 조건은 현재 안내를 따릅니다.
기본 사용 시 자동 호출 규칙을 추가하지 않습니다. 조회 전 동의를 받습니다.

Sequential Thinking 원본을 선택하면 [공식 README](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)를 확인합니다.
현재 검토 문서는 Node.js 24 이상을 요구합니다. Windows STDIO 명령은 아래와 같습니다.

```text
command: cmd
args: /c npx -y @modelcontextprotocol/server-sequential-thinking
env: DISABLE_THOUGHT_LOGGING=true
```

이 명령은 서버 시작 시 패키지를 내려받아 실행할 수 있습니다. 이번 설치에서는 실행하지 않습니다.
사용하려면 별도 설치 동의와 현재 패키지 검토를 먼저 받습니다. 모델의 비공개 사고 과정은 기록하지 않습니다.
외부 서버는 필요할 때만 연결합니다. 사용 후 앱에서 비활성화하면 다음 작업에 자동으로 제시되는 도구를 줄일 수 있습니다.

원본 Ponytail, Caveman, gstack, Superpowers 및 knowledge-work-plugins 전체 설치는 이 패키지에 포함하지 않습니다.
현재 연결된 다른 플러그인의 자동 동작을 전역으로 차단하는 도구도 아닙니다. 이 허브의 호출 정책 범위입니다.
