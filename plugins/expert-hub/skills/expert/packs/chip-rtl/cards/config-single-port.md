# PicoRV32 설정 single_port

ID: `chip-rtl:config-single-port` | both | reference-only

총 153807 cycles; baseline 대비 사이클 감소 -1.082%; generic 셀 6903 (-27.367%).

## conditions

동일 18개 프로그램 × 메모리 대기0/3의 36실행 합. 기준 baseline과 동일 조건.

## interpretation

{"name": "single_port", "passed": 36, "total": 36, "generic_cells": 6903, "cycle_sums": {"all": 153807, "shift": 72162, "mixed": 68671, "arithmetic_control": 3511, "directed": 9463}, "cycle_reduction_percent": {"all": -1.082, "shift": -1.705, "mixed": -0.586, "arithmetic_control": 0.0, "directed": -0.382}, "cell_change_percent": -27.367}

## verification

정상 동작 36/36 통과. 원본 로그와 배포 코드 재실행의 status/cycles/cell count가 동일.

## limits

generic cell count는 실제 면적이 아니다. 주파수/전력/공정/PVT 실측 없음. 사이클 개선은 해당 부하에 한정.

## 출처

- [PicoRV32 controlled Windows experiments, 2026-10-29](../../../references/chip-evidence/summary.json) · local-measured-experiment · 확인 2026-10-29 executed; 2026-10-30 imported hash checked
