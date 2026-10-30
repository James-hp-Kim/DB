# PicoRV32 설정 barrel

ID: `chip-rtl:config-barrel` | both | reference-only

총 145999 cycles; baseline 대비 사이클 감소 4.05%; generic 셀 9583 (+0.831%).

## conditions

동일 18개 프로그램 × 메모리 대기0/3의 36실행 합. 기준 baseline과 동일 조건.

## interpretation

{"name": "barrel", "passed": 36, "total": 36, "generic_cells": 9583, "cycle_sums": {"all": 145999, "shift": 66616, "mixed": 66616, "arithmetic_control": 3511, "directed": 9256}, "cycle_reduction_percent": {"all": 4.05, "shift": 6.111, "mixed": 2.424, "arithmetic_control": 0.0, "directed": 1.814}, "cell_change_percent": 0.831}

## verification

정상 동작 36/36 통과. 원본 로그와 배포 코드 재실행의 status/cycles/cell count가 동일.

## limits

generic cell count는 실제 면적이 아니다. 주파수/전력/공정/PVT 실측 없음. 사이클 개선은 해당 부하에 한정.

## 출처

- [PicoRV32 controlled Windows experiments, 2026-10-29](../../../references/chip-evidence/summary.json) · local-measured-experiment · 확인 2026-10-29 executed; 2026-10-30 imported hash checked
