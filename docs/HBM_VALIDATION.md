# HBM 이전·조회 검증 — 2026-10-30

HBM 패키징·열·신뢰성 자료를 기존 Expert Hub에 통합했습니다. 기본 범위는 `hbm` 하나이며 공통 통계가 필요할 때만 `quality` 또는 `common`을 명시합니다. 전체 허브의 최종 합본 검증은 별도 통합 기록을 참고하세요.

## 확인한 범위

- 원 식별자 299개를 149개 HBM 지식 항목·공유 출처·기존 공통 신뢰성 항목에 연결했습니다. [매핑](HBM_IMPORT_PROVENANCE.json).
- HBM 회귀 검사 **8개 통과**: 모든 매핑 대상 존재, 90개 원 출처 매핑, HBM 출처 해석, 범위 제한, 4개 검색 사례, 문자 상한, 14°C의 두 지표 구분, 파일 경계·원문 비노출·원본 불변.
- 공통 페르소나 gate 검사 **8개 통과**: 선택 키와 범위 제한 회귀. 기존 다른 팩 전체의 정확성을 보증하는 검사가 아닙니다.
- 공식 Python MCP SDK **1.30.0**, 실제 stdio 서버로 `catalog → reference_input → lookup → read → source` 호출 및 다른 팩 접근 거부 확인. 협상 프로토콜 `2025-11-25`.
- Windows PowerShell `expert.ps1`의 실제 catalog → reference-input 호출로 HBM 페르소나·warpage 근거 반환 확인. HBM 정본 149건은 JSON Schema 검사 통과.
- Windows Python **3.14.7** 및 한글·공백 경로에서 검증. 다른 Python 버전과 실제 빈 PC, Codex 앱의 Plugin 활성화는 이 검사에서 실행하지 않았습니다.
- 모델의 전문 자격·자율 판단 정확도, 실제 반도체 수율/성능, 내부 규격 적합성은 검증 대상이 아닙니다.

## 참고 토큰 측정

[측정 JSON](hbm-retrieval-benchmark.json), 재현 스크립트 `tests/benchmark_hbm.py`.

고정 질의 4개에서 전체 HBM 카드 149개를 읽는 기준과 선택 조회를 비교했습니다. 양쪽에 공통 Skill과 HBM 안내 전체를 포함했고, 선택 조회에는 페르소나 검색·요약·해당 조건/해석/한계(또는 절차)·인용된 모든 출처 메타데이터를 포함했습니다. 절의 `next_offset`이 없어 조건·한계가 완전히 반환되었는지 확인했습니다.

측정 tokenizer는 `o200k_base`입니다. 공유 Skill이 통합 과정에서 바뀔 수 있으므로 최종 수치는 JSON의 entry 크기 및 실행 시점에 따릅니다. 이 방식은 일반적인 전체 카드 적재 대비 참고 전달량 비교이며, **실제 청구 토큰 절감률이 아닙니다.** 사용자 입력·도구 정의·프로토콜·추론·최종 답변·대화 이력은 제외됩니다. 미리 선정한 4개 ID가 검색 2건 안에 드는지 확인한 시험이며 전체 검색 재현율 평가가 아닙니다.

## 근거의 한계

원 자료의 확인일은 2026-10-29로 유지했습니다. 이전·구조·검색 검사는 논문 전체의 사실 재검증이나 독립 실험 재현을 대신하지 않습니다. 초록 수준, 원문 관련 절 검토, 미확보, 회사 발표와 미수행 제안 상태를 보존합니다. 입력 양식과 합성 파일은 실제 제품 측정치가 아닙니다. 공개 배포에 PDF/XML 원문 및 개인 전체본문 DB를 넣지 않았습니다.

## 재현

저장소 루트에서:

```powershell
python -B -X utf8 -m unittest discover -s tests -p test_hbm.py -v
python -B -X utf8 -m unittest discover -s tests -p test_persona_gate.py -q
# 아래 두 개는 검증용 requirements-validation.txt 환경에서 실행
python -B -X utf8 tests/check_hbm_mcp.py
python -B -X utf8 tests/benchmark_hbm.py
```

기본 DB 조회에는 위의 MCP SDK/tiktoken 검증용 패키지가 필요하지 않습니다. 전역 Codex 설정 변경과 GitHub 업로드는 수행하지 않았습니다.
