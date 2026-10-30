# DB · Expert Hub 2.5.2 반도체 근거 연결 보완

- 저장소: https://github.com/James-hp-Kim/DB
- 반도체 질문은 관련 팩 검색 → 본문·출처 확인 → 실제 근거 ID 인용 순서로 답한다.
- DB에 직접 근거가 없으면 그 범위를 밝히고 외부 근거·계산으로 보완한다. 무관한 ID를 붙이지 않는다.
- 한국어 혼입과 MOS C–V 용어 확인을 추가했다. 검증 범위와 제한은 [수정·검증 보고서](docs/EVIDENCE_FIX_252.md)를 확인한다.
- 새 PC에 Git, Python, Node, Codex 설치 및 로그인이 끝난 뒤 다음을 실행한다.

```powershell
git clone https://github.com/James-hp-Kim/DB.git
Set-Location DB
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Start-Exam.ps1
```

`gpt-6.1-sol`로 시작하며 루트 AGENTS.md가 START.md를 읽도록 연결한다. 다른 폴더에서도 전역 연결이 필요하면 [자동 시작 안내](AUTO_START_KO.md)를 따른다. MCP·Plugin 설치는 별도 선택이다. URL만 채팅에 입력하는 것은 전역 설치가 아니다.

---

> 2026-10-31 지침 연결 수정 사본: 먼저 [AUTO_START_KO.md](AUTO_START_KO.md)를 확인하세요. 기존의 수동 START 문구 안내보다 이 연결 절차를 우선합니다.

# Expert Knowledge Hub — Windows · Codex

**여러 전문가 역할이 공통 지식과 분야별 지식 DB를 공유하고, 필요한 근거만 읽는 패키지입니다.** 시작은 [START_HERE_KO.md](START_HERE_KO.md)를 읽으세요.

버전: **2.5.2**. 현재 포함: **페르소나 9개 · 지식팩 13개 · 지식 항목 768개 · 출처 레코드 323개**.

**2.5.2 검증:** 수정한 테스트 2개와 전체 회귀 117개 통과. 같은 Windows PC의 새 Python·격리 설정에서 설치, Codex 스킬 인식, MCP 실제 호출, 합성 자료 분석과 별도 Excel/PDF 처리를 확인했습니다. [범위·결과·남은 한계](docs/ISOLATED_VALIDATION_252.md). 새 운영체제 설치나 새 계정의 모델 추론을 검증한 것은 아닙니다. [이전 블라인드 평가](docs/PERSONA_BLIND_251.md)는 당시 기록으로 보존합니다.

| 페르소나 | 역할 | 기본 DB |
|---|---|---|
| quality-assurance | 품질보증 전문가 | common + quality |
| data-analyst | 빅데이터·데이터 분석 전문가 | common + analytics |
| process-improvement | 공정개선 전문가 | common + quality |
| nand-expert | NAND 제어·ECC RTL 전문가 | nand |
| chip-design-verification | 칩 설계·검증 전문가 | rtl |
| semiconductor-basics | 반도체기초전문가 | semiconductor |
| backend-expert | 백엔드 전문가 | backend + common |
| semiconductor-ai | 반도체 AI 스킬 전문가 | chip-review |
| hbm-expert | HBM 패키징·열·신뢰성 전문가 | hbm |

페르소나는 전문가의 판단 관점이며 별도 모델이나 자격 인증이 아닙니다. 새로운 분야는 역할뿐 아니라 검증할 지식팩도 추가해야 합니다. 각 역할의 기본·허용 팩 범위는 personas/catalog.json에 명시합니다.

## 페르소나는 문제 해결을 돕는 역할

DB는 보조 근거이며 유일한 정답이나 능력의 경계가 아닙니다. 사용자 자료·코드·로그·측정 결과와 Codex의 추론·계산·디버깅·허용된 실험을 함께 사용합니다. 필요한 경우 최신 공식 문서·1차 자료와 관련 도구로 보완합니다. 단순 계산·코드 수정은 불필요한 DB 조회 없이 처리합니다.

DB에서 못 찾거나 근거가 낡았으면 그 한계를 밝히고 가능한 분석·수정을 계속합니다. DB 요약보다 실제 측정과 적용 조건을 우선 검토하며 출처 간 충돌을 설명합니다. 다른 지식팩이 필요하면 허용 범위에서 명시적으로 선택하거나 다른 페르소나를 검색합니다. 이 DB의 범위 제한은 사용자 프로젝트·외부 근거의 활용을 금지하는 규칙이 아닙니다. 원시 DB 전체를 읽는 우회는 하지 않습니다.

답변은 자료 나열로 끝내지 않고 결론·근거·대안·검증 방법과 요청된 실행 결과를 제시합니다. 불확실한 원인·개선 효과·미실행 작업을 확정 사실로 말하지 않습니다.

## 사용 흐름

**백엔드 성능·장애 대응:** [입력 자료와 사용법](docs/BACKEND.md), [백엔드 검증](docs/BACKEND_VALIDATION.md). `backend-expert`는 backend/common에서 요약 최대 2건·1,800자, 필요한 본문 1건·3,000자로 시작합니다.

**이번 지침·페르소나 점검:** [2.4.1 점검 기록](docs/PERSONA_AUDIT_241.md).

**이전 통합 배포 확인:** [2.4.0 검증 기록](docs/INTEGRATED_VALIDATION.md). 이전 분야별 시험 기록과 구분합니다.

반도체 AI 스킬 전문가의 입력 연결·최소 조회·설치 범위는 [전용 안내](docs/SEMICONDUCTOR_AI.md)를 따릅니다.

**반도체 기초·누설·최소화:** [입력·최소 조회 안내](docs/SEMICONDUCTOR_DATA.md). `semiconductor-basics` 역할, 기초팩 151개와 공통 계산식 1개를 사용합니다. CSV/JSON/보고서에서 주제와 행 위치만 추려 DB 근거로 연결합니다. [전용 검증](docs/SEMICONDUCTOR_VALIDATION.md).

**DRAM·HBM 칩 설계·검증:** [전용 시작 안내](docs/DRAM_HBM_START.md). `chip-design-verification` 역할과 `rtl` 팩(141개 항목)을 사용합니다. RTL·보고서·CSV 파일을 주면 `reference-input`이 관련 주제와 DB 요약만 반환합니다. 실제 EDA 검증·결함 판정과 구분합니다.

질문·자료 → 페르소나 검색 → 결과의 선택 키(context) 확보 → 짧은 요약 검색 → 적용 조건/절차/한계 등 필요한 절만 조회 → 로컬 계산 → 근거·개선·검증 방법.

- **Quick**: 분모·비교 조건이 명확한 문제를 빠르게 진단합니다.
- **Deep**: 반복·원인 불명·교란·시간 의존·상호작용 등 해결되지 않은 쟁점만 심화합니다.
- 계산 전제와 반대 근거를 잘라내면서까지 출력을 줄이지 않습니다.

## 토큰을 줄이는 구조

- 검색에서 받은 선택 키를 24시간 재사용하며 lookup/read/source 모두 키를 요구합니다. 등록부 변경 시 재검색합니다.
- 일반 분석은 공통 expert Skill과 선택된 페르소나의 짧은 역할만 읽습니다. exam-setup은 명시적인 환경 준비 요청에만 읽습니다.
- 검색은 기본 3개 요약, 전체 JSON 최대 3,500자입니다. 본문 전체는 반환하지 않습니다.
- 상세 조회는 id와 절 이름으로 지정하며 전체 JSON 기본 최대 6,000자입니다. 잘린 부분은 next_offset으로 표시합니다.
- 출처 상세는 별도 조회합니다. 데이터 원시 행은 로컬에서 계산하고 전체 결과를 파일로 보존합니다.
- 같은 입력·옵션·도구 버전은 분석 결과를 재사용합니다.

위 수치는 API 기본값입니다. Skill의 첫 호출 권장은 검색 3건/2,500자·본문 1건/3,000자이며 백엔드는 검색 2건/1,800자입니다. 필요한 근거가 잘리면 해당 절만 이어 읽습니다.

문자 상한은 모델 전체 토큰 상한이 아닙니다. 페르소나·DB 분리만으로 비용 절감이 보장되는 것도 아닙니다. [검증 결과](docs/VALIDATION.md)에 실제 시험 범위를 기록합니다.

NAND 사용자는 [입력 자료·최소 조회 안내](docs/NAND_DATA.md)를 먼저 읽으세요. 공개 지식 126건과 출처를 연결했으며 실제 NAND 측정 로그나 사내 사양은 포함하지 않습니다.

## 바로가기

- [새 페르소나·DB 작성 필수 README](README_PERSONA_DB_AUTHORING.md)
- [설치·첫 호출](START_HERE_KO.md)
- [사람용 검토 색인 — Codex 일반 질의는 조회 도구 사용](KNOWLEDGE_INDEX.md)
- [구조·데이터 형식·확장](docs/ARCHITECTURE.md)
- [개인 자료 추가](docs/PRIVATE_DATA.md)
- [GitHub 업로드와 새 PC](docs/GITHUB_HANDOFF.md)
- [검증 기록](docs/VALIDATION.md)

## 설치 요구사항

기본은 **Codex + Python 3.11 이상(SQLite FTS5 포함)**입니다. 별도 API 키, 벡터 DB, MCP 호스팅 서버가 필요 없습니다. 기본 CSV 분석도 표준 라이브러리만 사용합니다.

Ridge/Optuna 탐색은 requirements-forecast.txt, Excel은 openpyxl, 다변량 이상 탐지는 PyOD를 선택 설치합니다. Plugin 또는 MCP 등록 명령은 지원 버전 Codex CLI를 사용합니다. Codex 자체 서비스 이용과 질문/결과 전송은 사용자의 Codex 환경을 따르며, 전체 작업이 오프라인이라는 뜻은 아닙니다.

## 조회 경계

이 로컬 DB를 사용하는 질의는 페르소나 검색 → 선택 키 → 범위 제한 조회로 진행합니다. 출처도 선택한 팩의 레코드에서 참조한 것만 반환합니다. 같은 사용자 권한으로 로컬 파일을 직접 읽는 것은 이 구조로 막을 수 없습니다. 공개 원본·카드는 사람의 검토용이며, 이 규칙은 파일 접근 보안이 아닌 Codex 조회 절차입니다.

## 범위

현재 지식은 여러 분야 작업에서 수집·검토한 공개 자료와 자체 설계 지침을 통합한 것입니다. 모델 학습 자료 전체, 다른 대화의 업무자료, SK하이닉스 내부 자료를 가져온 DB가 아닙니다. 회사 채택·인증·현장 탐지 성능은 확인하지 않았습니다.

실행 기능: 선택 열 CSV 프로파일·기준모델 백테스트·Ridge/Optuna 탐색·별도 홀드아웃 평가, CSV 진단·중복 후보·불량률/Wilson·MAD·WECO/EWMA/CUSUM·선택 PyOD/Excel. MSA/Gage R&R, DOE, 공정능력, 신뢰성, FMEA 등은 적용 지침이며 모든 수치 계산기가 구현된 것은 아닙니다.

위 실행 기능 목록은 동봉 도구의 범위입니다. Codex가 사용자 요청에 따라 다른 분석 코드를 작성하고 검증하는 능력을 제한하지 않습니다.

새로 작성한 코드·문서는 [MIT](LICENSE), 보존한 제3자 자료는 [각 원본 라이선스](THIRD_PARTY_NOTICES.md)를 따릅니다.

매출·시계열·ML: [데이터 분석 안내](docs/DATA_ANALYSIS.md).

HBM 패키징·열·신뢰성: [HBM 안내](docs/HBM_DATA.md) — hbm-expert, 149개 항목.

**2.5.0 업데이트:** [선별 보강과 fact-grounding 연결](docs/UPDATE_242.md). 모든 페르소나에 공통 정책을 안내하며 설치된 fact-grounding을 우선합니다.

새 PC 설치: [INSTALL_NEW_PC_KO.md](INSTALL_NEW_PC_KO.md). 선택 도구 비교: [docs/OPTIONAL_METHODS_250.md](docs/OPTIONAL_METHODS_250.md).
