# NAND 작업 인계 — 2026-10-30

공통 파일 통합 조율 요청을 받은 뒤 이 작업은 공유 등록부·README·manifest·DB 재빌드를 중지했습니다. 아래 NAND 자료와 코드는 이미 skhynix_ai에 반영되어 있습니다. 전체 허브 최종 배포는 통합 담당 작업의 재빌드와 검증을 따릅니다.

## 반영 내용

- `plugins/expert-hub/skills/expert/packs/nand/records.jsonl`: 126개. 기존 공개 조사 124개 + K03 오류물리 분리 1개 + 입력 계약 1개.
- 페르소나 `nand-expert`: 기본 nand, 허용 nand/common. 기존 역할을 대체하지 않음.
- 출처 `nand-p01`~`nand-p15`, `nand-s01`~`nand-s26`, `nand-design`: 42개 추가. 원문 확인일 2026-10-29 보존.
- `input_reference.py`: 기존 칩 입력 연결을 NAND에도 확장. NAND_RULES/NAND_PATTERNS 및 persona→pack 선택 추가. `expert_reference_input`/CLI `reference-input`으로 사용자 지정 UTF-8 최대 2 MiB 파일을 읽고 주제·행번호·짧은 DB 결과만 반환. 원문/자동 ingestion 없음.
- MCP 도구 description의 Chip-only를 Chip-or-NAND로 변경. 기존 5개 도구 수를 늘리지 않음.
- `tests/test_nand.py` 8개, `tests/test_nand_sdk.py`, `tests/benchmark_nand.py`.
- `docs/NAND_DATA.md`, `NAND_PROVENANCE.md`, `NAND_VALIDATION.md`, `nand-retrieval-benchmark.json` 및 `examples/nand-retry-synthetic.log`.

## 검증 및 통합 시 확인

격리된 배포 사본에서 hub 기본 16개, persona gate 8개, NAND 8개와 공식 MCP SDK 1.30.0의 NAND catalog→lookup→read→source→file-reference 흐름이 통과했습니다. 이는 현재 계속 변하는 공유 폴더 전체의 최종 검증 완료를 뜻하지 않습니다.

NAND 검색 별칭을 의도적으로 보강한 항목: V08/V09/V12/V14/V15. 다른 작업이 보관한 `RTL_IMPORT_PROVENANCE.json`의 NAND 항목 해시가 보강 전 값이면 `test_rtl_reference.py`의 보존 검사가 실패합니다. 이를 원본 손상으로 처리하지 말고 이번 의도된 태그 변경과 비교해 새 배포 기준을 기록하세요. 기타 기존 본문·출처 확인 수준은 유지했습니다.

공유 빌드를 막던 새 chip 팩 형식 오류 두 종류도 최소 수정했습니다: `chip-review:claim-c39`의 빈 source_ids를 기존 `chip-historical-archive`에 연결하고 미실행 한계를 명시; `chip-rtl:config-compact_shift`/`config-single_port` ID의 underscore를 hyphen으로 변경. 같은 ID를 참조한 정본 텍스트도 변경했습니다. 새로운 과학적 근거를 추가한 수정이 아닙니다.

## 남은 공통 통합 반영

1. SKILL.md의 NAND 문단에 `expert_reference_input(file, context, query)` 또는 CLI reference-input 사용을 추가하면 파일 입력 흐름을 자동 선택하기 쉬워집니다. 사용자 지정 파일만 읽고 필요한 절을 추가 조회하며 원문을 반환하지 않는다는 계약을 유지하세요.
2. source의 `nand-design` URL은 `docs/NAND_PROVENANCE.md`입니다. 저장소 상대 경로이며 단독 설치 skill에 루트 docs가 자동 복사되지는 않습니다. 필요한 경우 해당 문서를 skill references에도 포함하고 출처 경로 해석 정책을 적용하세요.
3. README의 전체 개수는 현재 등록부로 갱신하고, root/installed authoring README·plugin 버전·RELEASE_INVENTORY·MANIFEST·ZIP을 최종 통합 시 동기화합니다.
4. 모든 팩이 확정된 후 필수 회귀와 NAND SDK 검사를 다시 실행합니다. NAND 지식 수는 126개를 기대합니다.

NAND 원본은 같은 작업의 2026-10-29 공개 연구 catalog.json입니다. 실제 개인 장비의 절대 경로와 작업 중 설정·선택 키를 배포물에 넣지 않습니다. 이 인계 문서는 로컬 작업 상태를 설명하며 최종 배포 기록으로 대체할 수 있습니다.
