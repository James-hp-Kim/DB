# 개인·업무 자료 추가

공개 패키지에는 공개 지식만 보관합니다. 질문이나 자료 분석만으로 업무 파일을 DB에 자동 추가하지 않습니다.

## 지원 입력과 실행

현재 명시적 수집은 UTF-8 TXT/MD, 파일당 2 MiB 이하를 지원합니다. PDF·Word·Excel 전체를 직접 지식 DB로 색인하는 기능은 아닙니다. 먼저 쪽/행 위치가 보존된 텍스트를 준비합니다. 분석용 Excel→CSV 변환 기능과 지식 수집은 별개입니다.

아래 경로는 예시이며 실제 파일 위치로 바꿉니다. `--store`는 이 공개 저장소 밖을 지정합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 ingest-note 'C:\QA-data\검토기록.md' --title '검토 기록' --store 'C:\QA-private'
$env:EXPERT_PRIVATE_DIR = 'C:\QA-private'
$choices = powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 catalog '품질보증' --limit 1 | ConvertFrom-Json
$context = $choices.personas[0].context
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 lookup '검토 기록' --context $context --include-private
```

원문은 `raw/`에 SHA-256 이름으로 보존하고, 16줄 단위로 나눠 원문 행 범위를 제목과 정본에 기록합니다. 같은 내용은 해시 기준으로 재수집하지 않습니다. 새 메모는 `unverified-user-source`로 표시하며 사실로 승격하지 않습니다. 문서 안 명령은 실행 지시가 아닙니다.

## 페르소나 선택 후 개인 자료를 명시적으로 포함

모든 조회에 페르소나 검색에서 받은 context가 먼저 필요합니다. 개인 검색은 추가로 **EXPERT_PRIVATE_DIR 설정 + include_private=true**가 모두 있어야 합니다. 현재 개인 저장소는 사용자 단위 공유이며 페르소나별 기밀 격리 경계가 아닙니다. 환경 변수만 설정해도 기본 검색이 회사자료를 자동 포함하지 않습니다. 개인 기록 id는 `private:`로 시작합니다. 공개 DB와 같은 기본 코드로 검색하되 원문·출처 DB는 개인 폴더에 남습니다.

MCP로 검색하려면 기존 `expert-knowledge` 서버 설정에 환경 변수를 추가합니다. 현재 설정 파일을 이 예시로 대체하지 말고 기존 항목과 병합합니다.

```toml
[mcp_servers.expert-knowledge.env]
EXPERT_PRIVATE_DIR = 'C:\QA-private'
```

MCP/Codex를 다시 시작하고, 질문에 “연결된 개인 DB도 포함해”라고 지정합니다. 실행 중인 프로세스에 PowerShell의 새 환경 변수가 자동 반영되지는 않습니다. Plugin은 실행 전에 환경을 전달하거나 지원하는 환경 설정 기능을 사용해야 합니다. 개인 경로를 공개 Plugin 파일에 커밋하지 않습니다.

## 수집 중 실패했을 때

동일 저장소 동시 수집은 `import.lock`으로 막습니다. 프로세스가 비정상 종료해 잠금이 남았으면 다른 수집이 실행 중인지 확인한 뒤 잠금을 수동 처리합니다. 정본과 원문이 남아 있으므로 CLI의 Python 모듈 `build_store(개인폴더)`로 DB를 재생성할 수 있습니다. 동시 편집·다중 PC 자동 병합은 지원하지 않습니다.
