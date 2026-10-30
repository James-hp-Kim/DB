# DRAM·HBM 칩 설계·검증 DB 사용법

Windows의 Codex에서 이 저장소 폴더를 열고 아래 문장을 그대로 사용한다. GitHub에서 새 PC로 가져올 때는 **Download ZIP → 압축 해제 → Codex에서 폴더 열기** 순서다. GitHub에 파일을 올리는 것만으로 MCP가 실행되지는 않는다.

## Codex에 입력할 문장

```text
이 저장소의 plugins/expert-hub/skills/expert/SKILL.md를 읽고 DB를 사용해줘.
chip-design-verification 페르소나를 검색해 선택하고 rtl 팩만 먼저 조회해줘.
검토 파일: C:/chip-work/reports/timing_excerpt.rpt
질문: setup 위반의 원인 후보와 확인할 제약 조건을 찾아줘.
reference-input으로 관련 주제를 추린 뒤 상위 3개 요약에서 필요한 항목만 골라줘.
적용 조건과 한계를 확인하고 필요한 절·출처만 읽어줘.
확인된 사실, 가설, 누락 증거를 구분하고 다음 검증 방법을 짧게 제시해줘.
파일 전체를 출력하거나 DB에 자동 저장하지 마.
```

파일 경로와 질문만 바꾸면 된다. **파일이 없으면 질문만으로 lookup을 사용**한다. Skill 설치 후에는 `$expert 칩 설계·검증 관점으로 …`라고 요청할 수 있다. 이름이 비슷한 다른 역할이 검색되면 `chip-design-verification`을 명시한다.

## 필요한 설치

| 목적 | 필요 |
|---|---|
| 폴더 안에서 질문·DB 조회 | Windows Codex + Python 3.11 이상, SQLite FTS5 |
| 다른 작업 폴더에서도 Skill 사용 | 저장소의 Install.ps1, 기존 설치가 있으면 덮어쓰지 않음 |
| MCP 도구로 조회 | 선택 사항: Codex MCP 등록, 서버는 로컬 Python 표준 라이브러리 사용 |
| Skill+MCP Plugin | 선택 사항: 저장소의 Plugin 설치 방식, 지원 Codex CLI |
| 실제 RTL 시뮬레이션·STA·합성 | 별도 EDA 도구·모델·library·라이선스·프로젝트 환경 |

별도 벡터 DB·임베딩 서비스·API 키·Docker·WSL은 **DB 조회에 필요 없다**. Python/Skill/MCP 설치 세부 명령은 [시작 안내](../START_HERE_KO.md)를 따른다. 기존 expert Skill이 있으면 이 저장소의 새 버전이 자동 반영되지 않으므로 차이를 확인한 뒤 업데이트해야 한다.

## 설치 없이 실제 조회 확인

저장소 루트의 PowerShell에서 실행한다. 아래 파일은 제공된 **합성 예제**이며 실측 STA 결과가 아니다.

```powershell
$choice = powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 catalog 'chip-design-verification' --limit 1 | ConvertFrom-Json
$choice.personas
$chipContext = $choice.personas[0].context
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 reference-input '.\examples\chip-timing-synthetic.rpt' --context $chipContext --max-chars 2500
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\expert.ps1 read rtl:c22 --context $chipContext --sections conditions verification limits --max-chars 3000
# source에는 위 조회가 반환한 sources ID만 전달한다.
```

MCP 도구는 `expert_catalog → expert_reference_input 또는 expert_lookup → expert_read → expert_source`다. context는 해당 경로/등록부와 연결되어 24시간 유지되며, 팩 변경·이동·만료 시 다시 검색한다.

## 어떤 자료를 주는가

UTF-8 RTL(.sv/.v/.svh), 타이밍·CDC·검증 로그(.rpt/.log/.txt), 제약(.sdc/.upf), CSV 헤더·일부 구간, JSON/Markdown을 파일당 2 MiB 이하로 제공한다. 전체 칩 프로젝트나 대용량 파형을 넣지 말고 해당 모듈/경로/실패 구간을 지정한다. 추출 전 원본은 보존한다.

블록 역할·세대/제품·규격 revision·clock/reset·mode/corner·실패 증상·기대 동작을 함께 주면 적용 조건을 좁힐 수 있다. CSV라면 단위·chip/board ID·측정기간·반복 측정·baseline을 명시한다. 자세한 [입력 계약](../plugins/expert-hub/skills/expert/references/chip-review.md)은 필요할 때만 읽는다.

입력 내용은 자동으로 DB에 쌓이지 않는다. 파일에서 주제를 찾고 기존 근거를 연결한다. 수치 계산이나 실제 RTL/형식/STA 검증은 별도 실행이 필요하다. 업무 파일은 공개 저장소 밖에 둔다.

## 작은 조회를 유지하는 구조

- 역할 등록부는 검색 메타데이터만 읽고 선택된 역할만 반환한다. chip-design-verification의 기본 범위는 rtl 한 팩이다.
- 141개 자료를 ID/요약/검색 태그/절/출처 ID로 나눴다. 전문을 한 문서로 프롬프트에 넣지 않는다.
- SQLite FTS5·별칭 색인으로 상위 3개 요약을 찾는다. source 정보는 공유 DB에서 필요할 때만 읽는다.
- reference-input 기본 응답은 최대 3,500자, 상세 조회는 보통 2,500~3,500자로 요청한다. 다음 절이 필요할 때만 추가 호출한다.
- 같은 결과를 대화 안에서 재사용한다. 표현이 달라 검색되지 않으면 짧은 약어·동의어로 재검색하며 전체 DB 로딩으로 대체하지 않는다.

페르소나는 검토 관점을 지정한다. **토큰 절감은 선택 범위·분할 조회·응답 상한에서 생기며, 페르소나를 붙이는 것만으로 보장되지 않는다.** 문자 수는 모델 토큰 수와 다르며 모델 추론·사용자 파일·답변은 별도다. 실측 참고 수치는 [RTL 조회 벤치마크](RTL_TOKEN_BENCHMARK.json)와 [검증 기록](RTL_VALIDATION.md)에 기록한다.

## 데이터 범위와 배포

기존 공개 자료 54건(논문 13편 포함)과 검토/실험/데이터셋 설명을 141개 레코드로 이관했다. 2026-10-29 수집 당시 확인 수준을 보존했으며 이관 시 새 웹 검토를 수행하지 않았다. 출처 목록과 ID·해시 대응은 [이관 기록](RTL_IMPORT_PROVENANCE.json)에 있다.

유료 표준 전문, 회사 RTL·PDK·비공개 규격, 원시 CSV와 논문 PDF는 경량 DB에 포함하지 않는다. 데이터셋 항목에서 원본 URL·해시·스키마·한계를 찾아 필요한 파일만 별도로 확보한다. 이 DB는 학습 모델 가중치나 전체 과거 대화의 복사본이 아니다.

GitHub에는 저장소 루트의 내용과 숨김 폴더를 함께 올린다. 현재 작업에서는 업로드·전역 설치를 수행하지 않는다. [GitHub 인수인계](GITHUB_HANDOFF.md)를 참조한다.


설치 구조 확인(2026-10-30): [공식 Skill 지연 로딩](https://learn.chatgpt.com/docs/customization/overview), [로컬 MCP stdio 설정](https://learn.chatgpt.com/docs/extend/mcp), [Plugin 패키징](https://developers.openai.com/plugins/build/plugins). 이 문서 대조는 현재 앱에 설치·활성화했다는 의미가 아닙니다.
