# 반도체 AI 통합 인수인계 — 2026-10-30

공유 파일 쓰기 중단 요청을 받은 후 공유 등록부/DB 재빌드는 중단했습니다. 요청 전 변경분:
- persona semiconductor-ai (default chip-review; allowed chip-review/chip-rtl/chip-memory/chip-analog/common/quality/rtl/nand/semiconductor)
- chip-review 17, chip-rtl 51, chip-memory 14, chip-analog 20: 102개 정본.
- sources.json의 chip- 접두사 출처 및 기존 동일 URL 출처 재사용.
- input_reference.py에 semiconductor-ai 라우팅, .sp/.spice/.cir 지원, selected_pack 추가. 기존 rtl/nand 분기 보존.
- SKILL.md 전용 안내 링크 한 단락, README 전용 안내 링크.
- references/semiconductor-ai.md, references/chip-evidence/*.json, docs/SEMICONDUCTOR_AI.md, docs/semiconductor-import.json
- third_party/semiconductor-evidence-20261029.zip 원본 보존.

공유 폴더의 DB는 최종 통합자가 다시 빌드하고 RELEASE_INVENTORY 및 manifest를 갱신해야 합니다. 이번 작업에서는 별도 workspace outputs/semiconductor-ai-hub-release-20261030 복사본에서 빌드/검증합니다. 원본 전체 통합본을 덮어쓰지 마세요. 자체 테스트는 tests/test_semiconductor_ai.py를 공유 폴더에 추가할 예정입니다.

## 완료된 반도체 고유 변경

tests/test_semiconductor_ai.py, tests/test_semiconductor_ai_sdk.py, tests/benchmark_semiconductor_ai.py를 추가했습니다. 검증 결과는 docs/SEMICONDUCTOR_AI_VALIDATION.md, 측정치는 docs/SEMICONDUCTOR_AI_BENCHMARK.json입니다.

공유 재빌드는 하지 않았습니다. HBM 분기가 합쳐지는 도중 patterns 사전에 chip-review가 없어 KeyError가 발생하는 것을 발견했고, input_reference.py의 해당 한 줄에 'chip-review': PATTERNS를 추가하여 RTL/NAND/HBM 분기와 함께 보존했습니다. 이 수정으로 고유 테스트 7개와 RTL 기존 테스트 7개가 통과했습니다. 이 한 줄을 유지해 주세요.

최종 THIRD_PARTY_NOTICES.md에 docs/SEMICONDUCTOR_AI_NOTICES.md 링크를 추가하고, 보존 ZIP의 mixed upstream licenses를 root MIT 부여에서 제외해야 합니다. 전체 파일을 덮어쓰지 않도록 이 고유 안내로 전달합니다.
