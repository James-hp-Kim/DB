# RTL·넷리스트·제약·보고서 검토

ID: `chip-rtl:design-review` | both | reference-only

기능 계약, 클록/리셋, 부호/폭, CDC, 제약 및 분석 조건을 단계별로 검토한다.

## conditions

top·버전·목표·인터페이스와 실행 도구 및 모델이 있어야 해당 범위의 검증을 재현할 수 있다.

## procedure

계층/연결을 파악하고 lint·simulation·formal·STA 결과의 실패 근거를 좁힌다. 의심 코드의 파일/행, 반례 입력, 원인 가설과 추가 확인을 연결한다. 실제 실행 전에는 실행 결과로 표현하지 않는다.

## limits

lint/일부 테스트 통과는 모든 입력 증명이 아니다. 수집한 도구가 모두 설치되어 있지는 않다.

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [Verilator Errors and Warnings](https://verilator.org/guide/latest/warnings.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [AMD UG906: Multi-Bit Synchronizer](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Multi-Bit-Synchronizer) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
