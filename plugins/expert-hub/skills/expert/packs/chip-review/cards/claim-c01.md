# C01 검토: 해당 구성으로 대부분의 반도체를 구조 분석부터 개선 검증까지 처리한다

ID: `chip-review:claim-c01` | both | reference-only

근거 부족: 진단 보조 범위는 넓지만 범용 전문가 성능·커버리지 검증이 없다. 과제 입력·도메인·실행 환경별로 평가해야 한다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

진단 보조 범위는 넓지만 범용 전문가 성능·커버리지 검증이 없다. 과제 입력·도메인·실행 환경별로 평가해야 한다.

## verification

이 자료 구성에 대한 판단; 칩별 실증 없음
2026-10-29 후속 공개 실험: chip-rtl:public-benchmark. 비블라인드 주입 결함의 탐지 결과이며 일반 진단 정확도가 아님.

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님
광범위한 텍스트 지침; hold slack 및 Pegasus 표기 교정 필요. 실제 반도체 진단 성능은 미검증
모델 지원과 실제 제품 정확도는 별개. DRAM cell 회로·수율·실측을 대체하지 않음
SRAM compiler; DRAM/HBM 또는 NAND 소자 분석 도구 아님
실제 공정 calibration과 물성·경계조건 필요; 자동 역설계 아님
floorplan·power·thermal model 필요; 패키지 전체 SI/PI·기계 신뢰성 도구 아님

## detail

검토한 주장: 해당 구성으로 대부분의 반도체를 구조 분석부터 개선 검증까지 처리한다
판정: 근거 부족

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [K-Dense-AI/scientific-agents](https://github.com/K-Dense-AI/scientific-agents/tree/98c7fae46648724e1a43a1f2b207b0c82fcc462e) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [CMU-SAFARI/ramulator2](https://github.com/CMU-SAFARI/ramulator2/tree/c6c7a5de0cef35935d6fad7369e6271406798865) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [VLSIDA/OpenRAM](https://github.com/VLSIDA/OpenRAM/tree/2f7b3866418ac1ce17ad959207a1489033d8c577) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [devsim/devsim](https://github.com/devsim/devsim/tree/e3a25f08c7f17cc6932624c12bf9f0f10d7f7cfd) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [uvahotspot/HotSpot](https://github.com/uvahotspot/HotSpot/tree/f18831e48cef5d62580585cca0d7fab6c71bc3cc) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
