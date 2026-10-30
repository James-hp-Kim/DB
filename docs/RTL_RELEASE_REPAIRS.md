# 배포 사본의 형식 보정

2026-10-30, 다른 작업이 동시에 수정하던 저장소를 시점 고정한 배포 사본에서 발견한 3개 레코드의 스키마 문제를 보정했다. 원래 작업 폴더의 해당 팩은 수정하지 않았다.

- `chip-review:claim-c39`: 출처 ID 목록과 limits가 비어 있었다. 이 항목은 “준비된 8개 시나리오가 진단 성능 검증 완료를 의미하지 않는다”는 기존 자체 검토 기록이다. 이 문서를 편집 이력 출처로 연결하고, 실제 EDA/모델 A/B 검증 증거가 없다는 기존 한계를 limits에 명시했다. 독립 연구나 새 실험 결과를 추가한 것이 아니다.
- `chip-rtl:config-compact_shift` → `chip-rtl:config-compact-shift`.
- `chip-rtl:config-single_port` → `chip-rtl:config-single-port`.

마지막 두 항목은 DB ID의 허용 문자에 맞춘 변경이며, 기존 ID는 legacy_id로 보존했다. 설정값·본문·실험 수치는 변경하지 않았다. 그 외 팩의 내용은 이 스냅샷에서 추가 사실 검증한 것으로 주장하지 않는다.

추가 시험 보정: `test_semiconductor.py`의 MCP 호출이 초기화 이전 빈 상태로 조회를 호출하고 있었다. 테스트에서 실제 initialize → notifications/initialized 순서를 수행한 뒤 결과를 비교하도록 수정했다. 서버의 초기화 거부 규칙은 변경하지 않았다.
