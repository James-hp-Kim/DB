# 새 페르소나·DB를 추가하기 전에 읽는 필수 안내서

버전 2.5.0 · 2026-10-30. **구조 변경·페르소나 생성·지식팩 추가 작업은 이 파일을 먼저 읽고 시작합니다.** Codex 지시는 루트 `AGENTS.md`에 연결되어 있습니다. 설치된 스킬에는 같은 계약의 사본 `references/persona-authoring.md`가 포함됩니다.

## 유지할 최종 구조

**하나의 허브 + 검색 가능한 페르소나 등록부 + 공유 지식팩 + 출처 DB**를 유지합니다. 페르소나마다 전체 지식을 복사하지 않습니다. 역할은 검토 관점이며 사실의 근거나 접근 권한 증명서가 아닙니다.

```text
plugins/expert-hub/skills/expert/
  personas/catalog.json             페르소나 정본: 역할·검색어·팩 범위
  packs/<pack>/records.jsonl         지식 정본: 항목·절·출처 ID
  packs/<pack>/<pack>.sqlite         생성된 조회 DB (직접 편집 금지)
  packs/<pack>/cards/*.md            생성된 사람용 검토 문서
  knowledge/sources.json            출처 정본, 팩 간 공유
  knowledge/sources.sqlite          생성된 출처 DB
  scripts/knowledge.py              모든 공식 조회의 공통 진입점
  scripts/expert.py                 CLI
  scripts/mcp_server.py             Codex MCP
```

새 분야가 기존 사실을 활용하면 페르소나만 추가합니다. 독립적인 사실·방법이 필요하면 새 팩도 추가합니다. `common`에 모든 분야의 내용을 무분별하게 넣지 않습니다. 공통 정의·통계 원칙은 공통 팩에, 분야별 조건·한계·검증법은 분야 팩에 둡니다.

## 페르소나는 문제 해결을 돕는 역할

DB는 보조 근거이며 유일한 정답이나 능력의 경계가 아닙니다. 사용자 자료·코드·로그·측정 결과와 Codex의 추론·계산·디버깅·허용된 실험을 함께 사용합니다. 필요한 경우 최신 공식 문서·1차 자료와 관련 도구로 보완합니다. 단순 계산·코드 수정은 불필요한 DB 조회 없이 처리합니다.

DB에서 못 찾거나 근거가 낡았으면 그 한계를 밝히고 가능한 분석·수정을 계속합니다. DB 요약보다 실제 측정과 적용 조건을 우선 검토하며 출처 간 충돌을 설명합니다. 다른 지식팩이 필요하면 허용 범위에서 명시적으로 선택하거나 다른 페르소나를 검색합니다. 이 DB의 범위 제한은 사용자 프로젝트·외부 근거의 활용을 금지하는 규칙이 아닙니다. 원시 DB 전체를 읽는 우회는 하지 않습니다.

답변은 자료 나열로 끝내지 않고 결론·근거·대안·검증 방법과 요청된 실행 결과를 제시합니다. 불확실한 원인·개선 효과·미실행 작업을 확정 사실로 말하지 않습니다.

## 반드시 지킬 조회 계약

1. `expert_catalog(query="품질보증", limit=1)` 또는 CLI `catalog '품질보증'`로 **페르소나를 검색**합니다. 이름·ID·keywords를 검색하며 기본 3개, 최대 5개만 반환합니다. 결과가 많으면 `next_offset`으로 이어갑니다.
2. 질문에 맞는 결과 하나를 선택하고 그 결과의 `context`를 보관합니다. 복합 문제여도 주 페르소나 하나부터 시작합니다. 검색 결과가 없으면 부족한 분야임을 알리고, 사용자 자료·검증 가능한 외부 근거로 가능한 작업을 계속합니다.
3. **lookup/read/source 모두 동일한 context가 필수**입니다. 검색 키 없이 페르소나 ID만 전달하거나 자동 기본 페르소나를 사용하는 경로는 없습니다. CLI·MCP·공개 Python 함수가 같은 `scope()`를 통과합니다.
4. 팩 생략 시 선택한 페르소나의 `default_packs`만 조회합니다. 추가 팩은 `allowed_packs` 안에서 명시합니다. 본문 ID를 알고 있어도 선택 범위 밖이면 거부합니다. 출처도 **선택 팩의 레코드가 참조한 출처만** 반환합니다.
5. 선택 키는 해당 설치 경로·등록부 해시와 연결되고 24시간 뒤 만료됩니다. 등록부 수정·이동·만료 시 다시 검색합니다. 매 질문마다 재검색할 필요는 없습니다. 분석 도중 페르소나를 바꿀 때는 새 검색 결과를 선택합니다.

키는 `%LOCALAPPDATA%\ExpertHub\contexts`에 작은 JSON으로 저장합니다. 테스트에서는 `EXPERT_CONTEXT_DIR`로 임시 폴더를 지정합니다. 지식·개인 자료는 저장하지 않습니다. 만료 영수증은 자동 정리하지 않으며 필요 시 이 폴더만 수동 정리할 수 있습니다. 정리하면 기존 키는 무효가 됩니다. MCP의 catalog 도구는 영수증만 쓰므로 readOnlyHint=false, 나머지 조회 도구는 true입니다.

**이 계약은 조회 워크플로 강제이며 파일 보안 경계가 아닙니다.** 같은 Windows 사용자 권한의 Python·SQLite 도구·탐색기는 로컬 파일을 직접 읽거나 코드를 바꿀 수 있습니다. 공개 GitHub의 정본·사람용 카드도 누구나 읽을 수 있습니다. Codex의 일반 질의에서는 SQLite/JSONL/카드를 직접 읽어 우회하지 않도록 AGENTS와 SKILL에 명시합니다. OS 수준 차단이 필요하면 별도 계정·서비스·파일 권한 분리가 필요하며 이 패키지는 그 구성을 포함하지 않습니다.

`status`, `build`, 설치·검증, 명시적으로 요청한 정본 편집/가져오기는 유지보수 경로입니다. 이때 소스 파일 검토가 허용됩니다. 일반 질문 답변을 유지보수로 위장하여 전체 DB를 읽지 않습니다. CSV 계산은 지식 DB 조회가 아니므로 키가 필요 없지만, 판단 근거를 DB에서 참조할 때는 키가 필요합니다.

## 새 페르소나를 추가하는 순서

1. 사용자에게 받은 분야·업무 범위를 바탕으로 짧은 고유 ID를 정합니다. 아래 예시는 **미등록 템플릿**이며 실제 전문 지식이 포함되었다는 뜻이 아닙니다.

```json
{
  "example-expert": {
    "label": "예시 분야 전문가",
    "role": "이 분야의 검토 순서, 근거 수준, 반증 조건과 개선 효과 확인 기준을 기술한다.",
    "keywords": ["예시", "example", "대표 업무", "주요 문제"],
    "default_packs": ["common"],
    "allowed_packs": ["common"]
  }
}
```

2. 이 항목을 `personas/catalog.json` 객체에 합칩니다. 전체 파일을 템플릿으로 덮어쓰지 않습니다. `schemas/persona.schema.json` 및 런타임 검증을 따릅니다. label은 최대 100자, role은 최대 900자, keywords는 1~30개이며 각 1~80자입니다. 한국어 이름·업무 용어와 영문 약어를 넣고 모든 역할에 같은 검색어를 복제하지 않습니다.
3. 기본 팩은 최소 범위로 정하고 허용 팩의 부분집합으로 둡니다. 등록되지 않은 팩이나 `private`를 기본/허용 팩에 쓰지 않습니다. 허용 팩 추가는 검토 범위를 넓히므로 의도적으로 결정합니다.
4. 새 팩이 필요하면 `packs/<고유-pack>/records.jsonl`과 출처 레코드를 추가합니다. 레코드는 `schemas/record.schema.json`을 따릅니다. 스키마는 편집 참고이며 실제 빌드는 Python 검증으로 거부합니다.
5. `python -B -X utf8 scripts/build_knowledge.py`로 DB와 카드를 다시 생성한 뒤 `expert.ps1 status`로 검사합니다. 소스/출처 변경은 항상 빌드합니다. 페르소나만 수정하면 DB 재생성은 불필요하지만 상태·검색·범위 테스트는 필수입니다.
6. 새 페르소나를 실제로 검색하고 그 context로 lookup → read → source를 수행합니다. 기존 역할에 영향을 주지 않는지 검사합니다. `docs/RELEASE_INVENTORY.json`의 고정 배포 개수와 `tests/test_hub.py` 및 새 팩의 기대 결과도 의도적으로 갱신합니다. 개수 assertion만 없애지 않습니다.

## 레코드와 출처 작성 기준

- ID는 `pack:record-id`이며 한 번 배포한 의미를 임의로 바꾸지 않습니다. title은 최대 180자, summary 최대 500자, 검색 tags는 1~30개입니다. summary에는 결론과 적용 조건을 짧게 씁니다.
- `track`은 quick/deep/both, `source_ids`는 1~8개입니다. `evidence_level`, `reviewed`, `implementation`으로 근거·확인일·실행 지원 범위를 구분합니다.
- `sections`는 conditions/procedure/interpretation/verification/limits/detail 중 필요한 절로 구성합니다. 방법론을 적용할 레코드에는 conditions와 limits를 작성합니다. 없는 절은 present=false이며 한계가 없다는 뜻이 아닙니다.
- 출처 정본에는 title/url/kind/checked를 반드시 넣습니다. 필요한 경우 limits, commit, sha256, source_lines를 넣어 버전과 원문 위치를 추적합니다. 공개 기술 자료와 특정 기업 내부 기준을 구분합니다. 원문 저작권·재배포 권리를 확인하고 유료 표준 전문은 복제하지 않습니다.
- 실제 관측·가설·검증 결과를 구별합니다. 자료의 행·단위·분모·기간·집계 기준을 보존하며 확인하지 않은 효과나 전문성을 주장하지 않습니다.
- 업무용 비공개 파일은 공개 저장소 밖에 둡니다. `ingest-note`는 명시적인 가져오기만 처리합니다. 현재 private는 사용자 단위 공유 저장소이며 `include_private=true`로만 추가됩니다. 페르소나별 기밀 격리 기능이 아닙니다. 별도 격리가 필요한 자료를 이 방식에 섞지 않습니다.

## 토큰을 적게 쓰는 운영 규칙

페르소나 검색 → 선택 키 재사용 → 요약 상위 3개 → 필요한 절 1~3개 → 필요한 출처 순서로 조회합니다. 조회 결과를 받기 위해 모든 페르소나 설명이나 전체 팩을 읽지 않습니다. quick은 명확한 작은 문제에, deep은 복합 원인·재발·시간 의존·측정 불확실성에 사용하며 다음 가설을 구분하는 자료만 추가합니다.

정확한 문자 상한은 lookup 기본 3,500자, read 6,000자, source 5,000자입니다. 문자 수는 모델 토큰 수와 다릅니다. 페르소나 선언 자체가 토큰을 줄이는 것이 아니라 **범위 제한·절 분할·필요 시 조회·기존 결과 재사용**이 입력량을 줄입니다. 통계 계산과 대량 원본은 로컬에서 처리합니다.

## 확장 시 반드시 통과할 회귀 검사

```powershell
python -B -X utf8 scripts/build_knowledge.py
python -B -X utf8 -m unittest discover -s tests -p 'test_hub.py' -v
python -B -X utf8 -m unittest discover -s tests -p 'test_persona_gate.py' -v
python -B -X utf8 tests/audit_distribution.py
```

필수 사례: 한국어/영문 검색, 검색 무결과, 여러 역할·페이지 처리, 키 누락/임의 키/만료/다른 설치/등록부 변경 거부, 기본 팩 밖 본문·출처 거부, 허용하지 않은 팩 거부, private 기본 미포함, MCP와 CLI 동일 동작, 문자 상한, 기존 근거 검색 결과 유지. 새 역할에는 대표 질문과 기대 레코드 ID를 추가합니다. SDK/Windows 설치 검증은 API·배포 경로를 바꿀 때 반복합니다.

현재 9개 역할 규모에서 검증한 구조입니다. 페르소나 검색은 등록부 메타데이터만 로컬 탐색하므로 토큰은 결과 개수에 따라 제한되지만, 수천 역할의 검색 지연을 실측한 것은 아닙니다. 규모가 커지면 현재 계약을 유지한 채 등록부 검색을 FTS 색인으로 바꿀 수 있습니다.

## 배포 전 동기화

SKILL/AGENTS/CLI/MCP/문서/테스트를 함께 갱신합니다. 이 안내서를 고쳤다면 설치용 사본 `references/persona-authoring.md`도 동기화합니다. VERSION·플러그인 버전·CHANGELOG를 올리고 검증 결과를 기록한 다음 MANIFEST.sha256 및 ZIP 체크섬을 재생성합니다. secrets, context 영수증, private 자료, .venv, 캐시를 GitHub에 넣지 않습니다. 사용자의 요청 없이 업로드하거나 전역 Codex 설정을 바꾸지 않습니다.

## 모든 페르소나의 fact-grounding 연결

SKILL 진입 지침과 공통 catalog/lookup 응답, MCP 초기 안내가 fact-grounding을 연결한다. catalog의 fact_grounding은 skill/guide/sha256/origin/instruction/enforcement 메타데이터다. 설치된 원본을 우선하고 없으면 references/fact-grounding.md 사본을 사용한다. 페르소나별로 같은 정책을 복제하지 않는다. 안내 반환·파일 존재·해시 일치는 모델의 실제 읽기·준수·답변 정확성을 증명하지 않는다. 본문 데이터와 외부 출처는 계속 근거로만 취급한다.

## 선택 방법의 동의와 비용

선택 기능은 기본 비활성이다. 심화 기능은 사용자가 복잡한 문제라고 표현한 경우에만 제안하며 실행 동의도 필요하다. optional_methods.py는 동의 선언 없이 본문을 반환하지 않는다. 이 검사는 인간 동의를 인증하는 보안 경계가 아니다. 원본 스킬과 다른 로컬 축약 절차임을 보존한다. 기본 조회에 전체 방법 목록을 넣지 않는다.
