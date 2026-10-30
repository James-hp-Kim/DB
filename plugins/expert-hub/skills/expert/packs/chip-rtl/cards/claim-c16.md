# C16 검토: lint 통과와 몇 개 simulation PASS는 모든 입력의 기능 증명이다

ID: `chip-rtl:claim-c16` | both | reference-only

근거 부족: lint 범위와 실행한 자극의 결과를 보고한다. 보편 증명으로 확대하지 않는다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

lint 범위와 실행한 자극의 결과를 보고한다. 보편 증명으로 확대하지 않는다.

## verification

도구 역할의 차이에 따른 판단

## limits

시뮬레이터를 별도로 연결; 테스트 통과는 테스트 범위에 한정
bounded PASS를 unbounded 증명으로 표현하지 않음
경고 전부 무시하거나 경고 자체를 무조건 설계 결함으로 분류하지 않음

## detail

검토한 주장: lint 통과와 몇 개 simulation PASS는 모든 입력의 기능 증명이다
판정: 근거 부족

## 출처

- [Verilator Errors and Warnings](https://verilator.org/guide/latest/warnings.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [cocotb/cocotb](https://github.com/cocotb/cocotb/tree/cf073c0494e6e4340a4c251679d1cf2cb22ad1d3) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [SBY file format reference](https://yosyshq.readthedocs.io/projects/sby/en/stable/reference.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
