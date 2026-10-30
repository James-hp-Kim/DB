# C22 검토: Verilator와 cocotb는 같은 종류의 시뮬레이터다

ID: `chip-rtl:claim-c22` | both | reference-only

교정: Verilator는 simulation/lint 도구, cocotb는 시뮬레이터와 연결하는 Python testbench 환경.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

Verilator는 simulation/lint 도구, cocotb는 시뮬레이터와 연결하는 Python testbench 환경.

## verification

각 프로젝트 README와 docs

## limits

경고만으로 기능 정답이나 CDC 안전을 보증하지 않음
시뮬레이터를 별도로 연결; 테스트 통과는 테스트 범위에 한정
실행 환경·버전·test stimulus는 사용자가 가진 설계에 맞춰야 함

## detail

검토한 주장: Verilator와 cocotb는 같은 종류의 시뮬레이터다
판정: 교정

## 출처

- [verilator/verilator](https://github.com/verilator/verilator/tree/5e119ba2ed3a1b4d43fe5ddc8fb24803f16e9607) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [cocotb/cocotb](https://github.com/cocotb/cocotb/tree/cf073c0494e6e4340a4c251679d1cf2cb22ad1d3) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [cocotb First Steps](https://docs.cocotb.org/en/stable/first_steps.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
