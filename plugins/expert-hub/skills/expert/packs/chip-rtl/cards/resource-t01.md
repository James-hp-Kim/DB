# The-OpenROAD-Project/OpenSTA

ID: `chip-rtl:resource-t01` | both | reference-only

Verilog·Liberty·SDC·SPEF 등을 이용한 gate-level timing — 입력·corner·constraint가 필요; signoff 전 영역을 증명하지 않음

## conditions

Verilog·Liberty·SDC·SPEF 등을 이용한 gate-level timing

## procedure

타이밍 과제 우선

## limits

입력·corner·constraint가 필요; signoff 전 영역을 증명하지 않음

## verification

저장소·원문 확인; 이 환경에서 실행/성능 검증 안 함. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C17: activity와 모델을 이용한 추정이다. 실제 측정 자료가 없으면 실측으로 표기하지 않는다.
C20: 그림에 보이는 연결/표시만 관찰로 삼고 추가 데이터가 필요한 판단을 분리한다.
C24: Verilog/Liberty/SDC/SPEF 등 입력을 사용하는 기능이 문서화돼 있다. 제공된 실제 설계로 실행한 것은 아니다.

## 출처

- [The-OpenROAD-Project/OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA/tree/384b539085c54eef46cbaa02e2e17d2b983247e5) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
