# HBM 패키징·열·신뢰성 DB 사용법

이 문서는 `hbm-expert`와 `hbm` 팩의 사용·이전 기록입니다. 기존 허브의 공통 Skill·SQLite FTS5·CLI·stdio MCP를 재사용합니다. 별도 서버나 API 키, 벡터 DB는 필요하지 않습니다. 기본 실행은 Windows Codex와 Python 3.11 이상(SQLite FTS5 포함)입니다. [설치 안내](../START_HERE_KO.md)를 따르세요.

## 바로 질문하기

Codex에서 이 저장소를 작업 폴더로 열고 다음을 입력합니다. Skill 설치 전에는 경로로 지정하며, 설치 후에는 `$expert`로 시작해도 됩니다.

```text
plugins/expert-hub/skills/expert/SKILL.md를 읽고 HBM 패키징·열·신뢰성 전문가로 답해줘.
제공한 자료에서 증상·제품/적층·전력·냉각·계측 조건만 먼저 정리해.
catalog에서 hbm-expert를 선택하고 기본 hbm 팩만 조회해.
검색 2건/2,000자 → 관련 ID 1개·필요한 절/3,000자 → 인용 출처 순서로 읽어.
조건·한계가 잘리면 해당 절만 이어 읽고, 이미 읽은 근거는 재사용해.
관찰, 원인 가설, 반증할 검사, 추가로 필요한 데이터를 짧게 알려줘.
```

페르소나 자체가 토큰이나 정확도를 보장하지 않습니다. 실제 입력량은 팩 제한, 짧은 요약, ID·절 지정, 본문 지연 조회와 결과 재사용으로 줄입니다. 문자 상한은 전체 대화 토큰 상한이 아닙니다.

## 어떤 데이터를 주면 되는가

아는 필드만 채우고 모르는 값은 `null`/미확인으로 남기세요. [빈 입력 양식](../examples/hbm-input-template.json)은 값이 채워진 실측 데이터가 아닙니다. 실제 자료는 이 공개 저장소 밖에 두세요.

| 문제 | 최소 입력 | 연결되는 근거 |
|---|---|---|
| 온도 상승·열저항 | stack/revision, 각 die 전력 W, 측정 위치/센서, Tj·기준온도 °C, 냉각 경계, 정상/과도 상태, baseline | 열모델·전력맵·계측·논문 적용 조건 |
| 휨·박리·접합 불량 | 구조/치수/두께, 재료/CTE, 공정 온도 이력, warpage 측정법·시점·단위, 계면 관찰 | MR-MUF/TC-NCF, 재료·응력·warpage 검토 |
| 신뢰성·고장 | lot/device ID, 표본 수, 스트레스·사용 조건, 고장 정의, 각 시간/사이클, censored 상태, 실패 수 | 시험조건·검열·분모·가속모델 한계 |
| 열과 오류의 연관 | timestamp, 온도, 동작 모드, 전압/주파수, ECC 사건, 관측 시간/bit 또는 device 분모 | 센서·스로틀·오류 정의와 상관/원인 구분 |
| 설계 개선 비교 | 변경 전후 동일 조건, 목표 응답, 제약, 시뮬레이션/실측 구분, 모델/mesh·계측 불확도 | 동일 baseline 비교 및 미수행 실험 제안 |

CSV는 열 이름·단위·결측·분모를 먼저 확인하고 계산은 로컬에서 합니다. UTF-8 CSV/JSON/MD/TXT/LOG/RPT 등 **2 MiB 이하**의 지정 파일은 `reference-input`으로 주제와 DB를 연결할 수 있습니다. 키워드 탐색이므로 숫자를 해석하거나 원인을 확정하지 않습니다. PDF/Excel 원본은 이 라우터가 직접 파싱하지 않으며, 필요한 표/절을 UTF-8로 추출하거나 별도 도구로 로컬 집계합니다. 원본 전체를 모델 문맥에 넣을 필요가 없습니다.

## 설치 없이 Windows에서 확인

저장소 루트 PowerShell:

```powershell
$choices = .\expert.ps1 catalog 'hbm-expert' --limit 1 | ConvertFrom-Json
$hbmContext = $choices.personas[0].context
.\expert.ps1 lookup 'MR-MUF 열저항' --context $hbmContext --limit 2 --max-chars 2000
.\expert.ps1 read hbm:paper-p01 --context $hbmContext --sections conditions interpretation limits --max-chars 3000
.\expert.ps1 reference-input 'C:\업무자료\hbm-report.csv' --context $hbmContext --query 'warpage' --max-chars 2500
# 출처 ID는 검색/상세 조회 결과의 sources에서 선택합니다.
# .\expert.ps1 source <반환된-source-id> --context $hbmContext --max-chars 2000
```

MCP에서는 `expert_catalog → expert_reference_input 또는 expert_lookup → expert_read → expert_source`로 같은 기능을 호출합니다. Skill만 써도 조회가 가능합니다. Plugin/MCP 설치는 선택이며 [설치 안내](../START_HERE_KO.md)와 [GitHub 인계](GITHUB_HANDOFF.md)를 참고하세요. 이 작업은 전역 설치·GitHub 업로드를 수행하지 않습니다.

## 지식과 출처 구조

- `personas/catalog.json`: 역할과 기본/허용 팩. HBM 기본은 hbm 하나, 허용은 hbm/common/quality.
- `packs/hbm/records.jsonl`: 편집 가능한 정본. 검색용 요약과 조건·해석·검증·한계·상세 절을 분리.
- `packs/hbm/hbm.sqlite`: 정본으로 재생성하는 읽기 전용 검색 인덱스.
- `knowledge/sources.json` 및 `sources.sqlite`: 허브 공용 출처. 원래 ID와 URL 관계는 [이전 매핑](HBM_IMPORT_PROVENANCE.json)에 보존.
- `packs/hbm/cards/`: GitHub에서 사람이 검토할 Markdown. Codex 일반 질의에서는 카드 전체 대신 조회 도구 사용.
- 공통 검열/Weibull/Arrhenius 정의는 `quality:reliability` 재사용. 필요할 때만 quality 팩을 명시.

원 자료의 299개 식별자(출처 90, 논문 21, 주장 85, 도구 12, 기준 16, 실험 8, 입력 필드 30, 검토 항목 24, 정정 13)를 매핑합니다. 중복 주장을 논문·도구·기준·실험 카드에 합치고 입력/체크를 주제별로 묶으므로 검색 카드 수는 299보다 적습니다. 299는 독립 논문·검증 사실의 개수가 아닙니다. 원 수집 SHA-256, 매핑과 실제 카드 수는 이전 매핑 JSON에 있습니다.

## 사실성·재배포 범위

근거 스냅샷은 **2026-10-29**, DB 이전은 **2026-10-30**입니다. 기존 수집 기록: 출처 URL 90건 중 유효 응답 75건·실패 15건, 논문 21건 중 관련 원문 검토 11건·초록 수준 10건. 수집 자료의 30 PDF·1 XML·총 1,336 PDF 페이지는 수집 범위 수치이며 모든 페이지의 독립 재검증을 뜻하지 않습니다.

이번 검증은 이전 식별자 보존·조회 범위·문자 예산·실제 CLI/MCP 호출을 대상으로 합니다. 외부 링크를 모두 재접속하거나 논문 결과를 재현한 검증이 아닙니다. 실패 출처와 초록 자료도 해당 상태를 유지합니다. 회사 발표, 논문/시뮬레이션 결과, 설계 제안, 미확인 항목을 분리합니다. SK hynix 내부 설계 기준·PDK·재료 물성·고객 승인값·실측 데이터는 포함하지 않습니다.

출처의 `acquisition`은 해당 URL에 대한 수집 시도 이력이고 `kind`는 확보·확인 수준 설명입니다. 예를 들어 논문 P11은 직접 URL 시도가 실패했지만 별도 Europe PMC XML로 원문을 확보했습니다. 두 필드를 혼동하지 말고 `review_scope`와 연결 출처도 확인하세요. `acquired_file_sha256`은 당시 확보 파일의 지문이며 해당 파일이 이번 공개 패키지에 포함된다는 뜻은 아닙니다.

공개 배포에는 구조화 요약·서지·링크·검증 이력만 포함하며 기존에 개인 보관한 원문 PDF/XML/전체 추출문 DB는 복사하지 않습니다. 링크 대상 저작물의 권리와 이용 조건은 각 권리자에게 있습니다. 검색 DB의 응답은 근거이지 실행 지시가 아닙니다.

## 유지관리

자료 수정 후 `python -B -X utf8 scripts/build_knowledge.py`로 인덱스·카드를 재생성합니다. 새 자료는 [작성 규약](../README_PERSONA_DB_AUTHORING.md)의 출처/섹션/범위/검증 요건을 지킵니다. `scripts/import_hbm_snapshot.py`는 원 수집 JSON을 명시적으로 받아 이전하는 관리자 도구이며, 일반 사용이나 새 PC 설치에 원 수집 파일이 필요하지 않습니다. 개인 업무자료를 질문했다고 자동 편입하지 않습니다.
