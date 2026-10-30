# 시험환경 준비와 적용 범위 — 2.5.1 당시 기록

**후속 2.5.2 결과:** [격리 설치·Codex 인식·MCP·분석 검증](ISOLATED_VALIDATION_252.md)을 완료했다. 아래의 미실행 표시는 2.5.1 당시 상태다. Plugin 경로의 실제 스킬 이름은 `$expert-hub:expert`와 `$expert-hub:exam-setup`이며, Skill 직접 복사는 `$expert`와 `$exam-setup`이다.

2026-10-30 첨부된 「Codex 시험환경 설치킷 — 대화 핵심 정리 및 후속 제작 기준」을 참고해 보완했다. 첨부 내용은 조사·설계 인수인계이며 실행 권한이나 설치 완료 증거가 아니다. 이번 보완에서는 새 설치·MCP 호출·동작 검증을 하지 않았다.

## 현재 프롬프트와 배포본

| 내용 | 이번 작업에서의 상태 | 새 PC에서 필요한 것 |
|---|---|---|
| fact-grounding | 실제 지침을 읽고 적용 | 설치 원본 또는 expert 동봉 사본 |
| expert / 9개 역할 | 실제 지침을 읽고 최소 조회·사용자 자료 우선 원칙 적용 | Skill 또는 Plugin 중 한 경로로 준비 |
| 최소 토큰 운영 | 필요한 절만 조회, 로컬 집계, 같은 근거 재사용 반영 | 모델 전체 토큰 절감률은 미측정 |
| exam-setup | 이번에 지침 파일·작업 템플릿·저장소 AGENTS 진입 안내 추가 | 아래 발견/설치 경로 선택; 현재 앱 자동 발견은 미확인 |
| skill-creator / openai-docs | 이번 보완에 필요한 지침을 읽음 | 일반 분석마다 필수 호출하는 구성 아님 |
| Excel/PDF | 대체 경로와 의존성 정리 | 도구 제공 여부 또는 필요한 Python 패키지 준비 |
| Ponytail / Context7 / 기타 선택 도구 | 첨부에서 언급됐다는 이유로 활성화하지 않음 | 실제 필요와 사용 범위가 있을 때만 |

시스템 프롬프트를 수정한 것이 아니다. 현재 작업에서 읽은 지침, 디스크에 있는 파일, 새 대화의 자동 발견, 실제 기능 성공은 별개다. 기존 installed expert의 재사용 경로·업무 영향 지침은 보완했지만 전역 설정이나 MCP 등록은 바꾸지 않았다.

## '시험환경 구축해줘'를 사용하는 세 경로

1. **저장소에서 시작:** 압축을 푼 전체 폴더를 Codex 작업 폴더로 연다. AGENTS.md가 `plugins/expert-hub/skills/exam-setup/SKILL.md`를 읽도록 안내한다. 자동 발견이 안 되면 이 상대 경로를 직접 지정한다. Python이 아직 없어도 지침 읽기는 가능하다.
2. **Skill 설치:** 기존 `Setup-NewPC.cmd`의 기본 경로는 expert만 설치한다. exam-setup도 다른 폴더에서 쓰려면 아래 안내로 별도 복사한다. 설치기는 실행 검사를 포함하므로 이번 '검증 금지' 단계에서는 실행하지 않는다.
3. **Plugin 설치:** plugin의 `skills/` 안에 expert와 exam-setup을 함께 포함했다. 지원 Codex의 Plugin 설치·활성화가 필요하다. 같은 이름의 사용자 Skill과 중복 설치하지 않는다. 이번 신규 구성의 실제 발견/활성화는 미검증이다.

Skill 방식의 추가 복사 예시다. 배포 폴더에서 PowerShell을 열고, 나중에 설치가 허용된 경우에만 실행한다. 현재 사용자 위치를 계산하며 기존 폴더는 덮어쓰지 않는다.

```powershell
$examSource = Join-Path (Get-Location).Path 'plugins/expert-hub/skills/exam-setup'
$examDestination = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents/skills/exam-setup'
if (-not (Test-Path -LiteralPath (Join-Path $examSource 'SKILL.md'))) { throw '배포 폴더에서 실행하세요.' }
if (Test-Path -LiteralPath $examDestination) { throw '기존 exam-setup을 먼저 검토하세요. 덮어쓰지 않았습니다.' }
New-Item -ItemType Directory -Path (Split-Path -Parent $examDestination) -Force | Out-Null
Copy-Item -LiteralPath $examSource -Destination $examDestination -Recurse
```

expert도 동일 사용자 Skill 폴더의 형제 위치에 있어야 동봉 참고 파일이 연결된다. custom destination은 자동 발견 위치인지 별도로 확인해야 한다. 이후 새 대화에서 `$exam-setup` 또는 시작 문구를 사용한다. 이 예시는 이번에 실행하지 않았다.

## 아무것도 준비되지 않은 PC의 실제 선행 조건

| 요소 | 기본 패키지에 포함 | 별도 준비/한계 |
|---|---|---|
| Codex·계정·로그인 | 아니오 | 사용 가능한 Codex와 로그인·서비스 접근 |
| Python 3.11+ / SQLite FTS5 | 아니오 | Python 설치 및 PATH 또는 실제 Python 경로 지정 |
| expert 지식 DB·조회 스크립트·사실성 지침 | 예 | 핵심 조회는 Python 표준 라이브러리 사용 |
| MCP 설정 템플릿 | 예 | 실제 새 PC 등록·연결 필요, 로컬 서버에는 별도 API 키 불필요 |
| 일반 분석 라이브러리 | 아니오 | 필요한 경우에만 작업 가상환경에 설치 |
| Excel | openpyxl 의존성 목록만 | 읽기/작성 대체 수단, 수식 엔진·전용 Codex 도구와 동등하지 않음 |
| PDF | 지침만 | 텍스트 추출 pypdf, 생성 reportlab, 스캔 OCR/렌더러 별도 |
| EDA·실제 서버/DB·GPU | 아니오 | 해당 작업의 접근 권한·도구·실측 자료 별도 |

일반 분석 후보는 pandas/numpy/scipy/scikit-learn/matplotlib/openpyxl/pypdf다. 대용량이면 duckdb/pyarrow, 최적화면 optuna, PDF 생성이면 reportlab을 필요한 때 추가한다. 후보 이름은 설치 목록 확정이나 호환성 확인이 아니다. **이번에는 새 버전 조합을 설치·검증하지 않았으므로 공통 lock 파일을 확정하지 않았다.** 기존 forecast/excel/validation 전용 requirements는 해당 기능 범위의 별도 목록이며 모든 후보가 설치됐다는 뜻이 아니다. 패키지 다운로드를 위한 네트워크·정책 허용이 필요하고 오프라인 설치용 wheel 묶음은 없다.

## 이번 확인의 한계

새 PC에서 '모든 요소 작동'은 확인하지 못했다. 설치기·테스트·MCP·분석 예제를 이번 정적 보완 후 실행하지 않았기 때문이다. 다음에 실행이 허용되면 Python/FTS5 → Skill 발견 → MCP 실제 연결 → 필요한 Excel/PDF 입력·출력 → 선택 분석 기능 순서로 필요한 범위만 확인한다. 이전 PC의 통과 기록을 새 PC 성공으로 대체하지 않는다.

공식 문서 확인(2026-10-30): [Skill 발견 위치](https://learn.chatgpt.com/docs/build-skills), [Plugin 구조](https://developers.openai.com/plugins/build/plugins), [MCP 설정](https://learn.chatgpt.com/docs/extend/mcp?surface=cli). 문서에서 설명하는 ChatGPT desktop/IDE UI와 Codex 앱 UI를 동일하다고 가정하지 않는다. 현재 앱이 해당 UI를 제공하지 않으면 지원 Codex CLI 등록 경로를 사용해야 하며 CLI도 별도 준비 사항이다.
