# 반도체 AI 조회 통합 검증

검증일: 2026-10-30. 별도 고정 복사본 semiconductor-ai-hub-release-20261030에서 수행했다. 공유 원본 폴더는 다른 분야 작업이 계속되어 배포본과 달라질 수 있다.

## 실제 통과한 검증

- test_semiconductor_ai.py: 7개. 한국어 페르소나 선택, 추가 102개 항목의 조건·한계·출처, 대표 검색, RTL/SDC/메모리/SPICE 라우팅, 한글·공백 경로, 원문 비노출·불변, 범위 제한, 문자 상한, 보존 ZIP 해시.
- 기존 test_hub.py 16개, test_persona_gate.py 8개, test_rtl_reference.py 7개 통과. 총 38개 단위 검사. 회로 정확도 검사가 아니다.
- official MCP Python SDK 2.3.0: catalog → lookup → read → source → reference_input 실제 stdio 왕복, 잘못된 팩 거부 통과. 프로토콜 2025-11-25.
- test_windows_install.py: 격리 CODEX_HOME에서 환경/Skill 복사와 MCP 등록/덮어쓰기 거부/MCP 목록/Plugin 설치/활성 목록/PowerShell 역할 검색/조회/context 누락 거부 9개 확인. 사용자 실제 전역 설정은 변경하지 않았다. 데스크톱 새 대화의 자동 발견까지 확인한 것은 아니다.
- build_knowledge.py 재생성 및 status: 13팩/760항목/9페르소나/305출처, DB integrity ok. 이 수치는 동결 시점의 전체 허브 합계이며 이번 반도체 추가분은 4팩/102항목이다.

## 참고 텍스트량 측정

[측정 원자료](SEMICONDUCTOR_AI_BENCHMARK.json): 고정 질문 4개에서 해당 팩 전체 Markdown을 읽는 방식과 요약 2개 + 적용 조건/한계 + 출처를 읽는 방식을 비교했다. 양쪽 모두 진입 Skill/라우팅 안내를 포함했다. o200k_base 기준 57.64~86.80% 감소. 선택 조회의 참고 텍스트는 2,594~2,873 tokens였다.

이 측정은 시스템 메시지·도구 스키마·추론·재시도·최종 답변을 제외한다. 실제 Codex 청구량 절감률이나 답변 품질이 동일하다는 증거가 아니다. 특정 자료에 필요한 조건과 한계는 생략하지 않는다.

## 검증하지 않은 것

새 환경의 실제 Codex 대화에서 자동 활성화, 모든 반도체 전문가 수준 진단, 실제 칩 signoff/실리콘 성능, 최신 웹 원문의 전수 정확성은 이번 통합에서 검증하지 않았다. 기존 공개 PicoRV32 실험은 알려진 변이·한정 입력에서 수행했으며 일반 정확도로 확대하지 않는다. 다른 분야 코드 전체에 대한 이번 턴의 전수 검증도 아니다.
