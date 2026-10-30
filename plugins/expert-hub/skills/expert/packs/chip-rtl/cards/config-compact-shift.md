# PicoRV32 설정 compact_shift

ID: `chip-rtl:config-compact-shift` | both | reference-only

총 169951 cycles; baseline 대비 사이클 감소 -11.692%; generic 셀 9365 (-1.463%).

## conditions

동일 18개 프로그램 × 메모리 대기0/3의 36실행 합. 기준 baseline과 동일 조건.

## interpretation

{"name": "compact_shift", "passed": 36, "total": 36, "generic_cells": 9365, "cycle_sums": {"all": 169951, "shift": 83608, "mixed": 72991, "arithmetic_control": 3511, "directed": 9841}, "cycle_reduction_percent": {"all": -11.692, "shift": -17.837, "mixed": -6.914, "arithmetic_control": 0.0, "directed": -4.392}, "cell_change_percent": -1.463}

## verification

정상 동작 36/36 통과. 원본 로그와 배포 코드 재실행의 status/cycles/cell count가 동일.

## limits

generic cell count는 실제 면적이 아니다. 주파수/전력/공정/PVT 실측 없음. 사이클 개선은 해당 부하에 한정.

## 출처

- [PicoRV32 controlled Windows experiments, 2026-10-29](../../../references/chip-evidence/summary.json) · local-measured-experiment · 확인 2026-10-29 executed; 2026-10-30 imported hash checked
