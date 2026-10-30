# devsim/devsim

ID: `chip-analog:resource-t13` | both | reference-only

유한체적법 기반 TCAD; PDE·mesh·material 모델 활용 — 실제 공정 calibration과 물성·경계조건 필요; 자동 역설계 아님

## conditions

유한체적법 기반 TCAD; PDE·mesh·material 모델 활용

## procedure

소자 문제가 명확할 때만 확장

## limits

실제 공정 calibration과 물성·경계조건 필요; 자동 역설계 아님

## verification

저장소·원문 확인; 이 환경에서 실행/성능 검증 안 함. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C01: 진단 보조 범위는 넓지만 범용 전문가 성능·커버리지 검증이 없다. 과제 입력·도메인·실행 환경별로 평가해야 한다.
C27: 메모리 시스템 timing/controller 모델과 cell 물리·회로 검증은 범위가 다르다.
C30: TCAD에 필요한 mesh·PDE·물성·경계조건과 calibration 자료가 필요하다.

## 출처

- [devsim/devsim](https://github.com/devsim/devsim/tree/e3a25f08c7f17cc6932624c12bf9f0f10d7f7cfd) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
