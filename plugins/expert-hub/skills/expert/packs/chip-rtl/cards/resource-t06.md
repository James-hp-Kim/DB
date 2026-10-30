# cocotb/cocotb

ID: `chip-rtl:resource-t06` | both | reference-only

Python으로 HDL testbench 작성 — 시뮬레이터를 별도로 연결; 테스트 통과는 테스트 범위에 한정

## conditions

Python으로 HDL testbench 작성

## procedure

동작·경계조건 테스트 후보

## limits

시뮬레이터를 별도로 연결; 테스트 통과는 테스트 범위에 한정

## verification

저장소·원문 확인; 이 환경에서 실행/성능 검증 안 함. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C16: lint 범위와 실행한 자극의 결과를 보고한다. 보편 증명으로 확대하지 않는다.
C22: Verilator는 simulation/lint 도구, cocotb는 시뮬레이터와 연결하는 Python testbench 환경.

## 출처

- [cocotb/cocotb](https://github.com/cocotb/cocotb/tree/cf073c0494e6e4340a4c251679d1cf2cb22ad1d3) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
