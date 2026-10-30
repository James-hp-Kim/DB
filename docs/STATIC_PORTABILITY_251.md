# 새 Windows PC 사용 가능성 정적 점검

검토 대상: `[검토 당시 로컬 원본 저장소]`

**읽은 실행 코드·설정·설치 진입점에서 작성자 PC의 고정 절대경로로 인해 새 PC 실행을 막는 결함은 발견하지 못했다. 기본 런타임의 명백한 누락 의존성도 발견하지 못했다.** 검토 중 발견한 문서 버전 불일치는 작성자가 수정한 파일을 다시 읽어 해소를 확인했다. 다만 실제 새 PC 설치 성공을 검증한 결과는 아니며, 미확인 범위를 아래에 남긴다.

이번 점검은 파일 나열·파일 읽기·정적 문자열 검색만 수행했다. Python 프로그램, PowerShell 설치 스크립트, 테스트, 서비스, DB 조회, 패키지 설치, 해시 계산, Codex 등록을 실행하지 않았다. 대상 저장소는 수정하지 않았으며 이 보고서만 별도 채팅 출력 폴더에 작성했다.

## 1. 실행 경로 점검

| 대상 | 읽은 근거 | 정적 판정 |
|---|---|---|
| 설치 래퍼 | `Setup-NewPC.cmd:2`의 `%~dp0Setup-NewPC.ps1` | 래퍼 위치 기준. 작성자 폴더 고정 아님 |
| 설치·CLI 진입점 | `Setup-NewPC.ps1:4,7,13`, `Install.ps1:9-12`, `expert.ps1:4-6`, `Test-Environment.ps1:4-7` | `$PSScriptRoot` 기준으로 동봉 파일을 찾음 |
| Python 탐색 | `scripts/Resolve-Python.ps1:4-19` | 사용자 지정 실행 파일, PATH의 python, py -3 순으로 탐색. 원래 PC의 Python 경로를 저장하지 않음 |
| Skill 설치 위치 | `Install.ps1:30-39` | 현재 사용자 UserProfile에서 `.agents/skills/expert`를 구성하거나 명시한 목적지 사용 |
| MCP 등록 명령 | `Install.ps1:48`, `Setup-NewPC.ps1:19-22` | 설치 대상 PC에서 찾은 Python과 복사된 서버의 절대경로를 계산. 새 PC에서 계산하는 절대경로는 이식성 결함이 아님 |
| Plugin 설정 | `plugins/expert-hub/mcp.json:6-11` 및 `.mcp.json:6-11` | PATH의 python과 `${PLUGIN_ROOT}` 사용. Plugin 모드는 PATH의 Python이 필요하다고 `Install.ps1:18-21`에 명시·검사 |
| 로컬 Marketplace | `.agents/plugins/marketplace.json:9-11` | `./plugins/expert-hub` 상대 경로 사용 |
| DB 루트 | `plugins/expert-hub/skills/expert/scripts/knowledge.py:17,129,247,328` | `__file__`로 Skill 루트를 잡고 동봉 DB 경로 구성 |
| context 저장 | 같은 `knowledge.py:76-77` | `EXPERT_CONTEXT_DIR` 또는 현재 PC의 LOCALAPPDATA/home 사용 |
| 사실성 지침 | `scripts/grounding.py:8-15` (expert Skill 내부) | 현재 PC의 CODEX_HOME/home를 찾고 없으면 동봉 `references/fact-grounding.md` 사용 |

실행·설정 파일의 Windows 드라이브 경로, USER·OneDrive·AppData 경로, `/Users/`·`/home/` 표현을 정적으로 검색했다. 발견된 URL의 `https://`나 출력 문구의 `ID:`를 파일 경로로 오인하지 않았다. 현재 경로를 출력하거나 설치 때 경로를 계산하는 코드도 고정 경로와 구분했다.

## 2. 새 PC 의존성

- **필수 Python:** `scripts/probe_python.py:6-10`은 Python 3.11 이상과 SQLite FTS5를 전제로 한다. `README.md:76`, 최종 `INSTALL_NEW_PC_KO.md:11,15-16`의 요구사항과 일치한다. Python 런타임 자체를 동봉했다고 주장하지 않는다.
- **기본 MCP·CLI:** `mcp_server.py:2-7`, `expert.py:2-11`, `knowledge.py:4-15`의 기본 import는 표준 라이브러리와 동봉 모듈이다. 기본 실행에서 MCP SDK, openpyxl, PyOD, Optuna를 반드시 import하는 의존은 관찰되지 않았다. 각 동봉 모듈 파일은 목록과 내용에서 확인했다.
- **DB 파일:** 팩별 SQLite 13개와 출처 SQLite 1개 파일이 경로 목록에 존재한다. 내용을 열거나 무결성·최신성을 검증하지 않았다. 파일 존재를 DB 정상 동작으로 확대하지 않는다.
- **선택 분석:** `convert_xlsx.py:12`의 openpyxl, `analysis.py:186-188`의 NumPy·PyOD, `backtest.py:103-105`의 scikit-learn은 해당 기능에 진입할 때 import한다. `tune.py:10`의 Optuna는 별도 튜닝 프로그램의 의존성이다. `requirements-excel.txt`, `requirements-anomaly.txt`, `requirements-forecast.txt` 및 `README.md:78`, `START_HERE_KO.md:111-127`에서 별도 설치를 안내한다. 선택 기능 의존성을 기본 설치 누락으로 판정하지 않았다.
- **유지보수 의존성:** `requirements-validation.txt`는 PyYAML/MCP SDK/tiktoken을 유지보수 검사 전용으로 명시한다. 기본 사용자 실행에서 요구되는 것으로 읽히지 않는다.
- **Codex CLI:** 기본 Skill 복사에는 필수가 아니다. MCP 자동 등록 및 Plugin 설치 모드는 CLI가 필요하며 `Install.ps1:17,43`에서 구분한다. CLI가 없는 경우 `Setup-NewPC.ps1:18-23`은 수동 MCP 설정값을 안내한다.
- **별도 fact-grounding Skill:** `grounding.py`의 동봉 사본 fallback이 있어 별도 설치가 없다는 이유만으로 차단되지 않는 구조다. 해당 사본 경로를 파일 목록에서 확인했다.

선택 패키지의 고정 버전이 현재 패키지 저장소에 존재하는지, 새 PC의 Python 버전별 wheel을 제공하는지는 이번 허용 범위에서 확인하지 않았다. 따라서 모든 Python 3.11+ 환경에서 선택 패키지가 설치된다고 보증하지 않는다.

## 3. 문서와 설치 흐름에서 남은 항목

### 문서 버전 불일치: 최종 읽기에서 해소

처음 읽은 `INSTALL_NEW_PC_KO.md`는 2.5.0 ZIP을 안내했지만, 작성자가 수정한 최종 파일의 1·20행은 2.5.1로 바뀌었다. `README.md:5`, `plugins/expert-hub/plugin.json:4`와 일치한다. 평가자가 저장소를 수정한 것은 아니며 수정 후 파일을 읽어 확인했다.

최종 설치 문서 3행은 정적 보완본·최종 동작 미검증·검증 금지 시 설치기 실행 금지를 명시한다. 45행은 MCP 설정 UI가 앱마다 다르며 지원 CLI로 대체할 수 있음을 구분하고, 122행은 `-ManualMcp`도 MCP 실행 검사를 수행한다는 점을 명시한다. 143행은 기본 설치기가 expert만 복사하고 exam-setup은 별도 경로라는 점을 명시한다. 최종 `Setup-NewPC.ps1:19,23-24`의 출력도 UI가 존재한다고 단정하지 않는 내용으로 바뀌었다. 정적 코드와 안내의 해당 모순은 남아 있지 않다.

### 체크섬 최신성은 확인하지 않음

`Setup-NewPC.ps1:7-8`은 `scripts/verify_release.py`를 호출하고 실패 시 설치를 중단한다. 해당 Python 코드의 9-16행은 MANIFEST에 기재된 각 파일의 실제 해시를 비교한다. 따라서 배포 준비 중 기재 파일을 수정하면 MANIFEST도 최종 파일에 맞춰야 한다. 이번에는 MANIFEST의 파일명과 검사 코드만 읽었으며, 해시를 계산하거나 검사기를 실행하지 않았으므로 현재 일치 또는 불일치를 판정하지 않는다.

또한 검사기는 MANIFEST에 없는 추가 파일을 거부하거나 포함 여부를 보장하지 않는다. 새 exam-setup Skill·안내서를 배포 묶음에 포함하려면 최종 파일 목록에서 그 포함을 확인해야 한다. 이는 새 파일이 현재 정상 설치된다는 검증 결과가 아니다.

### 설치기는 실행 검사를 포함함

`Setup-NewPC.ps1:16`의 `verify_install.py`는 실제 MCP 하위 프로세스를 띄우고 페르소나별 조회를 하는 검사다(`verify_install.py:16-21,53-70`). 이번 사용자 지시는 추가 동작 검증 금지이므로 이 설치기나 검사기를 실행하지 않았다. 설치 스크립트를 읽은 사실을 설치·MCP 활성화 완료로 표현하지 않는다. 최종 문서 `INSTALL_NEW_PC_KO.md:65,78-80`는 서버 검사와 앱 재연결·모델 정확도를 구별하므로 이 부분의 명백한 모순은 없다.

## 4. 고정 경로로 분류하지 않은 자료

- `docs/UPDATE_242.json:3`의 `C:\\Users\\USER\\...\\expert_hub_before_242_...`는 과거 백업 위치 기록이다. 현재 설치·실행 코드가 이 경로를 입력으로 사용하는 것은 관찰되지 않았다.
- `docs/validation-evidence.json:22`, `docs/RTL_TEST_RESULTS.json:64`의 OneDrive 언급은 과거 검증 한계다. 런타임 파일 경로가 아니다.
- URL·스키마 URL·외부 출처 주소는 로컬 PC 경로가 아니다.
- 최종 `INSTALL_NEW_PC_KO.md:119`의 `C:\실제 Python 폴더\python.exe`는 116행에서 새 PC 실제 경로로 바꾸라고 명시한 예시다.
- 설치 시 계산되는 Python·서버·사용자 폴더의 절대경로와 context에 기록되는 설치 루트는 현재 환경을 가리키기 위한 값이다. 패키지를 다시 옮긴 후에는 context 재발급이 필요한 설계와 구분한다.

## 5. 검토 시점과 한계

검토 도중 추가된 `plugins/expert-hub/skills/exam-setup/SKILL.md`, `references/task-template.md`, `docs/EXAM_SETUP_KO.md` 및 갱신된 루트 `AGENTS.md`를 이후 실제로 읽었다. 최초 목록에서 아직 없었던 상태를 최종 누락 결함으로 판정하지 않았다.

새 Skill의 8·14·17행은 검증 금지 시 probe·설치기·MCP·테스트를 실행하지 않도록 하고, `-ManualMcp`가 검사 생략 옵션이 아님을 명시한다. 12·15행의 `../expert`는 형제 Skill 기준이며 작성자 PC 경로가 아니다. 작업 템플릿 12행도 금지 시 새로운 계산·검증을 수행하지 않도록 일치한다.

`docs/EXAM_SETUP_KO.md:21-36`은 저장소 경로 직접 지정, Skill 추가 복사, Plugin 구성을 구분한다. 기본 설치기는 expert만 설치한다는 현재 코드와 일치하며, exam-setup의 별도 복사 예시는 배포 폴더 현재 위치와 대상 PC UserProfile로 경로를 만든다. `Test-Path`로 원본 Skill 존재와 목적지 미존재를 확인하고 기존 설치를 덮어쓰지 않는다. 형제 expert가 필요하고 custom destination의 자동 발견은 별도라는 점도 명시돼 있다. 이 복사 예시는 실행하지 않았다.

같은 문서 40-55행은 런타임·Python 라이브러리·OCR/렌더러·EDA 등이 동봉되지 않았음을 구분하고, 신규 앱 발견·활성화·새 PC 동작이 미검증임을 명시한다. 명백한 고정경로·의존성 누락 은폐·설치 완료 주장과의 모순은 발견하지 못했다. `AGENTS.md:3-6`은 시험환경 준비 요청의 읽기 진입점일 뿐 자동 설치가 아님을 명시한다.

이 보고서는 정적 소스·문서 점검이다. 새 Windows PC 설치, Codex 명령의 현행 지원, 앱 UI, Plugin 발견, MCP 연결, 파이썬 패키지 설치, SQLite FTS5 실행, 파일 체크섬 및 OneDrive 동기화는 검증하지 않았다. 따라서 표현은 “정적 점검에서 작성자 PC 경로 의존 및 명백한 필수 의존 누락을 발견하지 못함”으로 제한한다.
