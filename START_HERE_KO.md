> 2026-10-31 지침 연결 수정 사본: 먼저 [AUTO_START_KO.md](AUTO_START_KO.md)를 확인하세요. 기존의 수동 START 문구 안내보다 이 연결 절차를 우선합니다.

# 처음 사용하기

이 폴더가 저장소 루트입니다. 배포 파일 생성과 PC의 Skill/MCP 설치는 별개입니다. 현재 설치 상태는 해당 PC에서 확인하며, 이 안내서만으로 설치·활성화를 판단하지 않습니다.

## 역할을 불러올 때

```text
$expert [백엔드/데이터 분석/품질 등] 전문가 관점으로 [자료]의 [목적]을 해결해줘.
DB는 필요한 근거만 참고하고, 내 자료·코드·실험 및 필요하면 공식 문서도 활용해.
DB에 없다는 이유로 멈추지 말고, 확인한 사실과 가설을 구분해 개선·검증까지 진행해줘.
```

기존 대화가 옛 Skill을 이미 읽었다면 새 대화에서 다시 불러오거나 갱신된 SKILL.md를 읽도록 요청하세요.

## 이 폴더에서 바로 사용

1. **Codex에서 이 폴더를 작업 폴더로 엽니다.**
2. 다음 문장을 입력합니다.

```text
이 폴더의 전문가 지식 DB를 사용해줘.
plugins/expert-hub/skills/expert/SKILL.md를 읽고,
품질보증 관점으로 “불량률의 분모가 다른 설비 비교”에 필요한 근거만 찾아줘.
```

이 폴더의 AGENTS.md에도 진입 경로를 적었습니다. 전역 Skill 설치 전에는 `$expert`가 Skill 선택 목록에 표시된다고 보장하지 않으므로, 위처럼 위치를 지정하면 됩니다.

## 매출·시계열 분석으로 바로 시작

```text
이 폴더의 plugins/expert-hub/skills/expert/SKILL.md를 읽어줘.
빅데이터·데이터 분석 전문가 관점으로 [파일 경로]의 [분석 목적]을 검토해줘.
원시 행은 로컬에서 요약하고, data-analyst의 context로 필요한 팩·절만 조회해.
예측은 개발 백테스트와 최종 홀드아웃을 분리하고 핵심 결과와 근거 ID만 알려줘.
```

[지원 데이터·실행 명령·선택 라이브러리](docs/DATA_ANALYSIS.md).

## 백엔드 자료 조회

```text
이 폴더의 plugins/expert-hub/skills/expert/SKILL.md를 읽어줘.
너는 백엔드 전문가야. 첨부 자료의 환경·기간·부하·오류율·p95만 먼저 요약해.
backend-expert를 선택하고 요약 2건/1800자, 필요한 본문 1건/3000자로 조회해.
확인한 사실과 가설을 구분하고, 임시조치·영구수정·검증·롤백 조건을 제시해.
자료가 부족하면 필요한 증거만 알려줘. 원시 로그 전체를 대화에 출력하지 마.
```

[백엔드 상세 안내](docs/BACKEND.md). 설치 전에도 위 경로 지정 방식으로 사용할 수 있습니다.

## NAND 자료 조회

```text
이 폴더의 expert SKILL.md를 읽고 NAND 전문가로 답해줘.
첨부 자료에서 증상·블록·제품 조건만 먼저 추려 DB를 검색해.
상위 3건과 필요한 조건·한계·검증 절만 읽고 근거 ID와 미확보 정보를 알려줘.
```

[어떤 자료를 주고 어떻게 질문할지](docs/NAND_DATA.md)에 입력 양식과 실제 조회 예가 있습니다.

## 다른 작업 폴더에서도 쓰기: Skill 설치 권장

Windows용 Codex와 Python 3.11 이상이 필요합니다. Python 설치 후 `python --version`이 실행되도록 PATH를 설정하고 PowerShell/Codex를 다시 여세요.

이 폴더에서 PowerShell을 열고:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Test-Environment.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install.ps1
```

사용자 폴더의 `.agents\skills\expert`에 복사됩니다. 같은 이름의 폴더가 있으면 덮어쓰지 않습니다. `ExecutionPolicy Bypass`는 해당 실행 프로세스에만 적용하며 PC의 영구 정책을 바꾸지 않습니다. Python 경로가 특수하면 `Install.ps1 -PythonExe '실제 Python 실행 파일 경로'`를 사용하고 Codex에도 같은 경로를 알려주세요.

새 Codex 대화에서:

```text
$expert 품질보증 관점으로 첨부 검사자료를 빠르게 분석해줘.
문제·근거 행과 수치·개선안·검증 방법만 먼저 알려줘.
```

```text
$expert 데이터 분석 관점으로 이 비교가 타당한지 확인해줘.
분모·제품 구성·기간·표본 구조를 확인하고 필요한 지식만 조회해줘.
```

```text
$expert 공정개선 관점으로 반복 불량을 심층 검토해줘.
발생 원인과 유출 원인을 구분하고, 확인할 수 있는 최소 실험부터 제안해줘.
```

## 설치 없이 검색 동작 확인

패키지 폴더에서 다음 명령은 실제 검색 결과를 짧게 출력합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 status
# 검색 결과를 먼저 확인하고 적합한 페르소나의 context를 선택합니다.
$choices = powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 catalog '품질보증' --limit 1 | ConvertFrom-Json
$choices.personas
$context = $choices.personas[0].context
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 lookup '불량률 분모' --context $context
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 read common:data-contract --context $context --sections conditions procedure limits
```

Skill 단독도 같은 검색 도구를 실행하므로 MCP가 필수는 아닙니다. 선택 키 없이 조회하면 거부됩니다. 새 역할·DB를 만들기 전에는 [필수 README](README_PERSONA_DB_AUTHORING.md)를 먼저 읽으세요.

## 선택 기능

DRAM·HBM RTL 파일/검증 로그로 시작하려면 [칩 설계·검증 사용법](docs/DRAM_HBM_START.md)을 읽으세요. `chip-design-verification`을 선택한 뒤 `reference-input`으로 근거를 연결합니다.

| 필요 | 추가 설치 |
|---|---|
| Excel XLSX → CSV | openpyxl |
| 여러 변수의 이상 후보 순위 | PyOD 및 의존 패키지 |
| 전용 MCP 도구로 DB 조회 | Codex CLI를 이용한 MCP 등록, 추가 Python 패키지는 불필요 |
| Skill+MCP를 Plugin으로 설치 | Codex CLI plugin 지원 + PATH의 Python |

선택 라이브러리는 실제 데이터를 분석할 PC에서 설치합니다. Python 환경은 GitHub에 올리지 않습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-excel.txt
# 다변량 탐지가 필요할 때만:
.\.venv\Scripts\python.exe -m pip install -r requirements-anomaly.txt
```

Codex에 분석에는 `.venv\Scripts\python.exe`의 **실제 전체 경로**를 사용하라고 알려주세요. 이미 실행 중인 MCP의 Python과 선택 분석용 Python이 다를 수 있습니다. MCP 검색에는 선택 라이브러리가 필요 없습니다.

## MCP 또는 Plugin

아래 방식 중 하나만 선택합니다. 설치하지 않은 상태에서:

```powershell
# Skill과 MCP를 함께 등록:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install.ps1 -EnableMcp
# 또는 Plugin으로 묶어서 등록:
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Install.ps1 -Mode Plugin
```

이미 Skill을 설치했다면 `-EnableMcp`로 재설치하지 말고 아래처럼 기존 Skill의 서버를 등록합니다. `codex mcp list --json`에서 같은 이름의 항목이 없는지 먼저 확인합니다.

```powershell
codex mcp list --json
$expertUser = [Environment]::GetFolderPath('UserProfile')
$expertServer = Join-Path $expertUser '.agents/skills/expert/scripts/mcp_server.py'
$expertPython = (Get-Command python).Source
codex mcp add expert-knowledge -- $expertPython -B -X utf8 $expertServer
```

등록 후 새 대화를 시작합니다. Plugin 설치 이름은 `expert-hub@expert-local`, 화면 표시명은 **전문가 지식 허브**입니다. 도구는 expert_catalog/lookup/read/source/reference_input 다섯 개입니다.

정확한 CLI 설치 방법은 [공식 안내](https://developers.openai.com/codex/cli/), Skill 발견 경로와 지연 로딩은 [공식 문서](https://learn.chatgpt.com/docs/customization/overview), Plugin 명령은 [공식 명령 안내](https://learn.chatgpt.com/docs/developer-commands)를 따릅니다.

## 반도체 기초 자료 조회

반도체기초전문가를 지정하면 기본 semiconductor 팩만 조회합니다. [입력 예시와 복사할 프롬프트](docs/SEMICONDUCTOR_DATA.md)를 사용하세요. 파일의 주제·행 위치만 읽어 근거를 찾는 전용 CLI도 포함합니다.

매출·시계열·ML: [데이터 분석 안내](docs/DATA_ANALYSIS.md).

HBM 패키징·열·신뢰성: [HBM 안내](docs/HBM_DATA.md) — hbm-expert, 149개 항목.

## 2.5.2 설치 방식별 스킬 이름

직접 Skill 설치: `$expert`, `$exam-setup`. Plugin 설치: `$expert-hub:expert`, `$expert-hub:exam-setup`. 실제 Codex 스킬 목록의 이름을 선택하세요. [격리 검증 범위](docs/ISOLATED_VALIDATION_252.md).
