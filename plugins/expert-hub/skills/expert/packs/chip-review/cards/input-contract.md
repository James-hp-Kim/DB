# 입력 자료와 칩 분석 범위

ID: `chip-review:input-contract` | both | reference-only

파일 유형·요구 기능·성공 기준을 먼저 정하고 관련 팩만 조회한다.

## conditions

회로도/스크린샷, RTL/넷리스트/SDC, STA/PPA/DRC/LVS 보고서, DRAM/SSD trace, SPICE netlist 중 실제 제공 자료를 구분한다.

## procedure

텍스트 설계 자료는 reference-input으로 유형·근거 행·제한된 요약을 얻는다. 이미지/PDF는 해당 페이지를 직접 보고 가시 정보를 추출한다. RTL/STA는 chip-rtl, 메모리 시스템은 chip-memory, 회로/소자/열은 chip-analog를 명시 조회한다.

## limits

실제 설계·시뮬레이션·실측 수준을 혼동하지 않는다. 입력 검사기는 lint/정답 판정기가 아니며 PDF/OCR·GDS를 해석하지 않는다.

## 출처

- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) · primary · 확인 2026-10-29
- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
