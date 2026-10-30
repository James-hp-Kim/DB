# DRAM·HBM 통합 검증 기록

2026-10-30 / Expert Hub 2.3.0 배포 사본. 작업 폴더가 여러 대화에서 동시에 갱신되므로 아래 결과는 시점을 고정한 사본에 대한 것이다. 전체 공유 저장소의 최종 통합·배포는 별도 조율 작업에서 맡는다.

## 확인한 결과

- DRAM·HBM `rtl` 141개, 공유 허브 전체 611개/12팩/8역할을 SQLite로 빌드했다. 본 사본 출처는 220개(배포 보정 기록 1개 포함)다.
- 핵심 회귀 31개: 허브 16, 페르소나 경계 8, DRAM·HBM 파일 참조 7 통과. 상위 3개 검색, 필요한 절 조회, 출처 연결, 문자 상한, 잘못된 context와 다른 역할 범위 거부, 원본 미변경을 검사했다.
- 기존 팩 회귀: NAND 8, backend 8, 데이터 분석 9, 반도체 기초 8, forecasting 12 통과. forecasting의 선택 ML 실행 1개는 라이브러리 미설치로 건너뛰었다.
- Windows 설치 시험 1개 통과: 임시 한글·공백 경로로 Skill 복사, 덮어쓰기 거부, 이동 후 파일 참조, PowerShell wrapper, 다른 설치 context와 키 누락 거부. 사용자 전역 설정은 변경하지 않았다.
- 공식 MCP Python SDK 1.30.0으로 stdio 초기화, 도구 5개, 페르소나→조회→절→출처 및 파일 참조를 확인했다.
- 기존 공통·품질 42개 정본의 레코드별 해시를 비교해 보존을 확인했다. 동시에 작업 중인 다른 팩의 변경은 원본 불변 주장에 포함하지 않는다.

기록: [기계 판독 검증 내역](RTL_TEST_RESULTS.json), [배포 보정](RTL_RELEASE_REPAIRS.md), [이관 메타데이터](RTL_IMPORT_PROVENANCE.json).

## 참고 토큰 측정

| 전달 구성 | o200k_base 참고 토큰 |
|---|---:|
| 진입 Skill + RTL 141개 전체 카드 | 41,204 |
| 진입 Skill + 역할 검색 + 상위 요약 + 필요한 3절 + 출처 | 1,952–2,338 |
| MCP 도구 정의 5개 (별도) | 972 |

FIFO·STA·refresh·전력 데이터의 **고정 4개 질문** 비교이며 모두 기대 ID가 상위 3개에 있었다. 위 선택 조회에서는 절 이어읽기와 출처 생략이 없었다. 매 사례에 페르소나 검색 응답을 포함했고, 실제 대화에서는 context를 재사용할 수 있다.

측정은 tiktoken 0.14.0의 o200k_base 기준이다. Codex의 실제 모델 토크나이저·전체 과금이 아니며 사용자 입력, 모델 추론·최종 답변, 대화 이력과 프로토콜을 제외한다. 무작위 context의 토큰화 때문에 재실행 값은 소폭 달라진다. [측정 JSON](RTL_TOKEN_BENCHMARK.json).

## 재현

```powershell
python -B -X utf8 scripts/build_knowledge.py
python -B -X utf8 tests/test_hub.py
python -B -X utf8 tests/test_persona_gate.py
python -B -X utf8 tests/test_rtl_reference.py
python -B -X utf8 tests/test_rtl_windows.py
# 검증 전용 가상환경에서 requirements-validation.txt 설치 후:
python -B -X utf8 tests/test_mcp_sdk.py
python -B -X utf8 tests/benchmark_rtl_retrieval.py
python -B -X utf8 tests/audit_distribution.py
```

## 미확인 범위

공개 문헌의 모든 사실 재검증, 사용자 회사 RTL·PDK·JEDEC 원문, 실칩 결함 탐지율, EDA 실행, PPA 개선, 제품 signoff는 검증하지 않았다. 새 물리 PC와 Codex 앱의 자동 Skill 선택/Plugin 활성화도 미확인이다. 설치용 파일 생성·SDK 시험과 실제 앱 활성화를 구분한다. 선택 Excel/PyOD/ML 실행 환경은 이번 작업에서 추가 설치하지 않았다.
