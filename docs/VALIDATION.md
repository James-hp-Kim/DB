# 검증 기록 — 2026-10-30

Expert Hub 2.1.0을 Windows 11, Python 3.14.7, Windows PowerShell 5.1, Codex CLI 0.164.0에서 확인했습니다. Python 3.11 이상을 요구하지만 모든 버전 조합을 시험한 것은 아닙니다.

## 통과한 검사

| 대상 | 확인한 동작 |
|---|---|
| 기본 검사 16개 | 42개 항목·출처·DB 무결성, 한영 검색, 선택 팩 제한, 본문 미반환, JSON 문자 상한, 절 선택, 없는 절 표시, 잘못된 입력, 개인 DB 명시적 포함, 긴 본문 이어 읽기, 재생성·잘못된 정본 거절, MCP, 분석 계산, 캐시·원본 보존 |
| 선택 기능 검사 3개 — v2.0.0 이력, 해당 코드 변경 없음 | Excel 원본 행번호·숨김행 보존, 계산 캐시 없는 수식 거절, PyOD 합성 이상행 순위·반복 재현 |
| 페르소나 우회 검사 8개 | 키 누락·임의 키·ID 직접 전달·만료·등록부 변경·다른 설치 거부, 역할 검색·페이지, 새 역할, 출처 범위·private, CLI/MCP 동일 계약 |
| 공식 MCP SDK | 프로토콜 초기화, 도구 4개 목록, 페르소나 검색→요약→본문→출처 연결 |
| Skill | skill-creator 형식 검사 통과 |
| Windows 설치 | 한글·공백 경로의 Skill 복사, 기존 설치 덮어쓰기 거절, MCP 등록, Plugin installed/enabled, PowerShell 페르소나 검색·조회 및 키 누락 거부 — 총 9개 |

설치 시험은 별도 시험 폴더와 격리된 자식 프로세스 Codex 설정에서 수행했습니다. 실제 사용자 설정에는 자동 설치하지 않았습니다.

선택 기능 확인 버전: openpyxl 3.1.5, PyOD 3.6.7. 연결 검증은 MCP Python SDK 1.30.0, 형식 검증은 PyYAML 6.0.3을 사용했습니다. 기본 사용에는 이 검증 라이브러리가 필요 없습니다.

## 검색·전달량 측정

7개 고정 한영 질문에서 기대한 근거가 상위 3개에 포함되는 것을 회귀 검사로 확인했습니다. 일반적인 검색 정확도나 실제 업무 전체의 정답률은 아닙니다.

동일 진입 Skill을 기준으로 모든 카드와 선택 조회를 비교했습니다. tiktoken 0.14.0의 o200k_base로 센 **참고 텍스트 토큰**입니다.

| 전달 구성 | 참고 토큰 |
|---|---:|
| 진입 Skill만 | 730 |
| 진입 Skill + 전체 42개 카드 | 16,608 |
| 진입 Skill + 페르소나 검색 1회 + “불량률 분모” 검색 + 조건/절차/한계 | 1,571 |
| 네 개 예시의 선택 조회 범위 — 각각 페르소나 검색 포함 | 1,428~1,571 |
| MCP 도구 4개 정의 — 별도 | 772 |

선택 키는 보통 재사용하지만 이 측정에는 매 사례의 페르소나 검색 응답도 포함했습니다. 무작위 키의 토큰화로 재실행 시 소폭 차이가 납니다. 기대 항목을 사전에 지정한 비교이며, 추가 해석·검증 절이나 원문 출처 상세를 읽으면 전달량이 늘어납니다. 사용자 질문·자료, 모델 추론·답변, 프로토콜, 대화 이력은 제외했습니다. 따라서 전체 토큰/과금 절감률을 보장하지 않습니다. 기본 문자 상한 역시 모델 토큰 상한과 다릅니다.

측정 원본: [retrieval-benchmark.json](retrieval-benchmark.json), 환경: [validation-evidence.json](validation-evidence.json). 검색+부분 읽기 함수 실행시간은 프로세스 시작·Codex 응답·네트워크를 제외한 이 PC의 참고치입니다.

## 재현

```powershell
python -B -X utf8 .\tests\test_hub.py
python -B -X utf8 .\tests\test_persona_gate.py
# 선택 의존성을 설치한 환경에서:
.\.venv\Scripts\python.exe -B -X utf8 .\tests\test_optional.py
.\.venv\Scripts\python.exe -m pip install -r requirements-validation.txt
.\.venv\Scripts\python.exe -B -X utf8 .\tests\test_mcp_sdk.py
.\.venv\Scripts\python.exe -B -X utf8 .\tests\benchmark_retrieval.py
# 별도 새 폴더에만 설치 시험:
python -B -X utf8 .\tests\test_windows_install.py --out 'C:\QA-test\hub-install-01'
python -B -X utf8 .\tests\audit_distribution.py
```

## 실무 해석과 미검증 범위

단순 합성 예제는 M1 15/1500=1%, M2 16/200=8%이며 M2 중복 후보를 남깁니다. M3 0/0은 계산 불가입니다. M2 반복이 독립 관측인지 확인 전에는 잠정 집계입니다. 시간 변화 예제의 첫 신호는 54번째 관측입니다. PyOD에서는 강한 편차를 넣은 100번째 행이 1순위이며, Top-N의 개수를 실제 불량 개수로 해석하지 않습니다.

실제 공장 데이터의 오탐/미탐·개선 효과, 인증된 Codex 대화에서의 자동 역할 선택, 다른 새 PC 전체 환경, OneDrive 원격 동기화 완료는 검증하지 않았습니다. 이 결과는 SK하이닉스 등 특정 기업의 도입·승인 증거가 아닙니다.

로컬 파일/코드 접근 권한이 같은 사용자의 직접 열람은 차단하지 않습니다. 페르소나 검색 키는 인증 자격이 아니라 공식 조회 경로의 순서를 강제하는 영수증입니다.
