# CMU-SAFARI/ramulator2

ID: `chip-memory:resource-t07` | both | reference-only

현재 고정 README는 Ramulator 2.1; cycle-level DRAM·controller 모델 — 모델 지원과 실제 제품 정확도는 별개. DRAM cell 회로·수율·실측을 대체하지 않음

## conditions

현재 고정 README는 Ramulator 2.1; cycle-level DRAM·controller 모델

## procedure

메모리 병목 분석 우선 후보

## limits

모델 지원과 실제 제품 정확도는 별개. DRAM cell 회로·수율·실측을 대체하지 않음

## verification

저장소·원문 확인; 이 환경에서 실행/성능 검증 안 함. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C01: 진단 보조 범위는 넓지만 범용 전문가 성능·커버리지 검증이 없다. 과제 입력·도메인·실행 환경별로 평가해야 한다.
C26: 이번 고정 commit의 README는 Ramulator 2.1 User Guide이다.
C27: 메모리 시스템 timing/controller 모델과 cell 물리·회로 검증은 범위가 다르다.

## 출처

- [CMU-SAFARI/ramulator2](https://github.com/CMU-SAFARI/ramulator2/tree/c6c7a5de0cef35935d6fad7369e6271406798865) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
