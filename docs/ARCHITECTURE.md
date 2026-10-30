# 최종 구조와 확장

단일 저장소·단일 진입 Skill·단일 선택형 MCP가 여러 페르소나를 지원합니다. 페르소나와 DB는 1:1 관계가 아닙니다. 지식은 공통/분야별로 저장하고 역할은 필요한 팩을 선택합니다.

## 실제 배치

```text
plugins/expert-hub/skills/expert/
  SKILL.md
  personas/catalog.json          역할·검색 keywords·기본 팩·허용 팩
  scripts/                       검색 엔진·MCP·분석 CLI
  references/                    실행 명령·심층 지침·설계
  knowledge/sources.json         공유 출처 정본
  knowledge/sources.sqlite       공유 출처 DB
  packs/common/records.jsonl     공통 22개 항목 정본
  packs/common/common.sqlite     공통 DB
  packs/quality/records.jsonl    품질 21개 항목 정본
  packs/quality/quality.sqlite   품질 DB
  packs/*/cards/                 사람이 읽는 카드
```

Skill이 단독 설치되어도 스스로 실행할 수 있도록 런타임·역할·DB를 같은 Skill 폴더 안에 넣었습니다. 논리적 역할은 앞서 제안한 구조와 같으며, 설치 후 깨지는 상위 폴더 참조를 줄인 배치입니다.

## 지식 레코드

```json
{
  "id": "quality:example-method",
  "title": "방법 이름",
  "summary": "이 지식으로 해결하는 문제의 짧은 설명",
  "track": "both",
  "tags": ["한글 별칭", "English alias"],
  "source_ids": ["existing-source-id"],
  "evidence_level": "source-linked-summary",
  "reviewed": "2026-10-30",
  "implementation": "reference-only",
  "sections": {
    "conditions": "적용 전제",
    "procedure": "절차",
    "interpretation": "해석",
    "verification": "확인 방법",
    "limits": "제약과 반례"
  }
}
```

이는 형식 예시입니다. 새 항목은 실제 출처와 내용으로 작성합니다. 없는 절은 생략하며, 임의의 근거로 채우지 않습니다. `detail`은 원문 메모처럼 절별 분류가 적절하지 않은 자료에 사용합니다. `present=false`는 해당 절이 없다는 뜻이지 한계가 없다는 뜻이 아닙니다.

기존 QA 42개 항목의 본문은 행별 배치를 검토해 절로 분리했습니다. 새 운영 구조와 달라진 설치·검색 안내는 수정했고, 품질 기법의 원문 설명은 유지했습니다. `legacy_id`로 이전 항목을 추적합니다. `source_ids`는 공유 출처 레지스트리를 가리킵니다. 같은 통계 설명을 역할별로 복사하지 않습니다.

## 조회·길이 제한

| 도구 | 역할 | 기본 상한 |
|---|---|---|
| expert_catalog | 역할 검색·선택 context 발급 | 3개 페르소나 |
| expert_lookup | 선택한 역할과 관련 항목 요약 | 3개, 전체 JSON 3,500자 |
| expert_read | 선택한 id·절의 본문 | 기본 3종 절, 전체 JSON 6,000자 |
| expert_source | 출처 URL·확인일·한계 | 전체 JSON 5,000자 |
| expert_reference_input | 명시한 로컬 파일의 주제 → rtl 팩 근거 연결 | 입력 2 MiB, 응답 JSON 3,500자 |

조회 상한은 JSON 직렬화 이후 문자 수에 적용합니다. `lookup`은 길면 뒤쪽 후보를 줄이며 `more=true`로 표시합니다. `read`는 각 절의 `offset`, `next_offset`, `total_chars`를 반환합니다. 이어 읽기는 id 하나·절 하나에 적용합니다. 메타데이터만으로 예산을 넘으면 조용히 누락하지 않고 더 작은 요청을 요구합니다. 출처는 `omitted_ids`를 확인합니다.

현재 검색은 FTS5 관련도와 한글 복합어/영문 별칭의 인덱스 조회입니다. 후보 메타데이터만 읽고, 상세 본문은 별도 테이블에서 선택한 절만 가져옵니다. 의미 임베딩 모델은 없습니다. 다른 표현에서 놓치면 별칭을 보강하고 실제 질문의 검색 재현율을 측정합니다. 자동으로 전체 DB를 모델에 보내 보완하지 않습니다.

`max_chars`는 실제 토큰 제한이 아닙니다. MCP 도구 정의, 사용자 파일, 모델 추론, 답변과 대화 이력은 별도입니다. 같은 결과 파일의 캐시는 계산량을 줄이며, 다시 출력하면 전달 토큰은 발생합니다. 반복 검색 결과를 대화 안에서 재사용하는 것은 Skill 지침입니다.

모든 내용 조회는 페르소나 검색에서 발급한 context를 먼저 검증합니다. 출처는 `record_sources(source_id, record_id)` 색인으로 선택 팩 내 참조를 확인한 후 반환합니다. 키는 로컬 별도 폴더에 저장하며 지식 DB를 수정하지 않습니다.

## 페르소나 추가

먼저 [필수 작성 README](../README_PERSONA_DB_AUTHORING.md)를 읽습니다. 아래 개요보다 해당 계약을 우선합니다.

1. `personas/catalog.json`에 고유 ID, 짧은 `label`, 최대 900자의 `role`, 한영 검색용 `keywords`, `default_packs`, `allowed_packs`를 추가합니다.
2. 전문 지식이 기존 팩에 없으면 `packs/<이름>/records.jsonl`과 실제 출처를 추가합니다. 빈 역할만 만들고 해당 분야 전문가 DB가 완성됐다고 하지 않습니다.
3. `python -B -X utf8 scripts/build_knowledge.py`로 DB와 카드를 생성합니다.
4. 새 역할의 기본/확장 팩 범위, 기대 근거, 반례·한계를 테스트하고 패키지 버전을 올립니다.

현재 `tests/test_hub.py`는 배포 기준 168개/4역할/21+21+126개를 확인합니다. 지식을 늘릴 때 그 수용 기준도 새 정본에 맞춰 갱신합니다. 삭제한 카드의 오래된 Markdown은 확인 후 정리해야 합니다.

등록부 수정 후 기존 context는 무효가 되므로 다시 검색합니다. 일반 질의에서 파일을 직접 읽는 우회는 AGENTS/SKILL에 금지되어 있습니다. 역할별 팩 선택은 논리적 검색 범위이며 다중 사용자 보안 체계가 아닙니다. 다른 사용자 권한이 필요하면 계정·파일 권한·별도 프로세스나 저장소 경계로 분리해야 합니다.

## 재생성·동기화

정본은 JSONL/JSON, 실행 DB와 카드/색인은 파생물입니다. 운영자는 단일 수정 흐름으로 재생성하고 테스트한 버전을 배포합니다. OneDrive 폴더에서도 조회는 읽기 전용이며 DB를 WAL 모드로 열지 않습니다. 동시에 여러 PC에서 같은 정본/DB를 갱신하는 동기화 충돌을 처리하는 기능은 없습니다. 이번 검증은 로컬 파일 기준이며 OneDrive 원격 동기화 완료를 확인하는 검증이 아닙니다.
