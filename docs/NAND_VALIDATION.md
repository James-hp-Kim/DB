# NAND 추가 검증 — 2026-10-30

Windows / Python 3.12.14에서 NAND 지식팩 126개를 기존 Expert Hub 조회 API에 연결했습니다. 기본 실행은 표준 라이브러리만 사용합니다. 회사 실칩 로그와 실제 RTL 시뮬레이션을 검증한 결과는 아닙니다.

## 현재 실행한 검사

- NAND 회귀 테스트 8개 통과: 역할 선택·팩 제한, 대표 검색, 출력 상한·절 선택·출처 연결, 근거 수준 보존, 무결과·MCP dispatch, CLI 조회, 파일 주제 연결과 원본 미반환, 미일치 시 전체 조회 방지.
- 고정 한영 질문 8개에서 기대 항목이 상위 3개에 포함. 다른 표현이나 실제 업무 질문 전체의 정확도는 측정하지 않음.
- NAND 정본 126개와 페르소나 등록부 JSON Schema 검사 통과.
- 검색 상한 2,400자, 선택 절 상한 2,400자 테스트. 본문 전체를 검색 결과에 넣지 않음.
- 원문 확인 수준과 2026-10-29 확인일 보존. 이번 변환에서 외부 문헌을 모두 재검증한 것은 아님.

기존 허브의 별도 검증 이력은 [VALIDATION.md](VALIDATION.md)에 있습니다. 다른 작업이 같은 저장소에 팩을 추가하는 동안 전체 건수와 DB 해시가 바뀔 수 있으므로, 배포본은 고정 시점의 사본에서 별도로 검증합니다. 이번 실행의 최종 범위는 함께 제공한 배포 확인 기록을 따르세요.

## 조회 텍스트 전달량

o200k_base(tiktoken 0.14.0) 기준의 **참고 텍스트 토큰**이며 실제 Codex 사용량·과금 수치가 아닙니다. 같은 진입 skill을 포함한 전체 NAND 카드 읽기와 선택 조회를 비교했습니다.

|범위|참고 토큰|
|---|---:|
|진입 skill + 전체 NAND 카드 126개|30,619|
|retry epoch: 역할 검색 + 요약 + 조건/한계 + 출처 1개|1,542|
|LLR 포화: 같은 조회 구성|1,569|
|ONFI 6.0: 같은 조회 구성|1,508|
|P01: 같은 조회 구성|1,681|

위 선택 조회 수치에도 진입 skill을 포함했습니다. 역할 선택 키는 보통 재사용하지만 각 예에는 검색 1회를 넣었습니다. 기대 ID를 미리 정한 고정 시험이며, procedure/verification/수치 해석 절을 추가로 읽으면 전달량이 늘어납니다. 질문·첨부·추론·답변·대화 이력·도구 정의·프로토콜은 제외했습니다. 따라서 전체 토큰 절감률을 이 표로 계산해 보장하지 않습니다. 무작위 선택 키와 skill 변경에 따라 재실행 수치는 소폭 달라질 수 있습니다.

원본: [nand-retrieval-benchmark.json](nand-retrieval-benchmark.json).

## 다시 실행

```powershell
python -B -X utf8 scripts/build_knowledge.py
python -B -X utf8 tests/test_nand.py
python -B -X utf8 tests/test_hub.py
python -B -X utf8 tests/test_persona_gate.py
python -B -X utf8 tests/benchmark_nand.py
python -B -X utf8 tests/audit_distribution.py
```

tiktoken이 없으면 benchmark는 문자 수만 보고합니다. 토큰 참고 측정용 선택 의존성이며 일반 조회에는 필요 없습니다. 현재 사용자 Codex 설치·활성화, OneDrive 원격 동기화, 실무 개선 효과는 이 검사로 확인하지 않았습니다.
