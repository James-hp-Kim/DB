# DRAM·HBM·SRAM·SSD 분석 수준 선택

ID: `chip-memory:model-levels` | both | reference-only

메모리 시스템 성능 모델과 셀·PHY·공정 검증은 다른 수준의 자료가 필요하다.

## conditions

요구가 controller/trace/bandwidth/latency인지 셀 안정성·PHY·열·수율인지 먼저 구분한다.

## procedure

시스템 병목은 trace·타이밍 설정·queue·workload부터 확인한다. 전력 모델은 명령·메모리 사양을 확인한다. 셀/회로 문제는 소자 모델·netlist·corner 및 별도 검증 자료를 요구한다.

## limits

이 DB의 DRAM/SSD 도구 소개는 실제 제품 정확도 인증이 아니며 NAND ECC decoder나 HBM PHY 검증기를 구현한 것이 아니다.

## 출처

- [CMU-SAFARI/ramulator2](https://github.com/CMU-SAFARI/ramulator2/tree/c6c7a5de0cef35935d6fad7369e6271406798865) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [umd-memsys/DRAMsim3](https://github.com/umd-memsys/DRAMsim3/tree/29817593b3389f1337235d63cac515024ab8fd6e) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [tukl-msd/DRAMPower](https://github.com/tukl-msd/DRAMPower/tree/a2068bc58411ff36abb2f6aab74b1a5fbe98e93d) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [VLSIDA/OpenRAM](https://github.com/VLSIDA/OpenRAM/tree/2f7b3866418ac1ce17ad959207a1489033d8c577) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [CMU-SAFARI/MQSim](https://github.com/CMU-SAFARI/MQSim/tree/51f0f2d3fed92d88ef4a0fa61a38024b07bf9d16) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [MoatLab/FEMU](https://github.com/MoatLab/FEMU/tree/2d50161f24c4cb86d58185b0efd44457412eadce) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
