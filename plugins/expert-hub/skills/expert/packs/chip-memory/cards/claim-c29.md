# C29 검토: MQSim·FEMU는 NAND cell 전기적 검증을 완성한다

ID: `chip-memory:claim-c29` | both | reference-only

근거 부족: SSD/스토리지 시스템 시뮬레이션·에뮬레이션 자료다. cell 물리 모델을 대신하지 않는다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

SSD/스토리지 시스템 시뮬레이션·에뮬레이션 자료다. cell 물리 모델을 대신하지 않는다.

## verification

README scope

## limits

특정 검증 조건의 논문 결과를 모든 SSD 정확도로 일반화 금지; NAND cell 전기적 모델 아님
운영체제/가상화 환경 의존; 칩 회로·NAND 제조 물리 검증 도구 아님
4개 SSD에서 저자가 검증한 오차를 모든 SSD에 일반화하지 않음

## detail

검토한 주장: MQSim·FEMU는 NAND cell 전기적 검증을 완성한다
판정: 근거 부족

## 출처

- [CMU-SAFARI/MQSim](https://github.com/CMU-SAFARI/MQSim/tree/51f0f2d3fed92d88ef4a0fa61a38024b07bf9d16) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [MoatLab/FEMU](https://github.com/MoatLab/FEMU/tree/2d50161f24c4cb86d58185b0efd44457412eadce) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [MQSim FAST 2018 paper](https://people.inf.ethz.ch/omutlu/pub/MQSim-SSD-simulation-framework_fast18.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
