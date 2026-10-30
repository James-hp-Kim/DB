# 주입 결함 6종과 복구 확인

ID: `chip-rtl:mutation-results` | both | reference-only

알려진 변형의 탐지·복구 시험. 결함별 테스트 실패 수와 실제 진단 정확도는 구분한다.

## conditions

고의 변형 SUB/비교/AND/OR/shift/load. 각36시험, 복구 directed2조건씩.

## interpretation

[{"name": "M01_sub_as_add", "reason": "SUB subtraction incorrectly replaced by addition", "failed_tests": 20, "total_tests": 36, "detected": true}, {"name": "M02_signed_compare", "reason": "Signed less-than incorrectly uses unsigned comparison", "failed_tests": 18, "total_tests": 36, "detected": true}, {"name": "M03_and_as_or", "reason": "AND decoded datapath incorrectly computes OR", "failed_tests": 20, "total_tests": 36, "detected": true}, {"name": "M04_or_as_xor", "reason": "OR decoded datapath incorrectly computes XOR", "failed_tests": 20, "total_tests": 36, "detected": true}, {"name": "M05_shift_sign", "reason": "Iterative arithmetic right shift loses sign extension", "failed_tests": 34, "total_tests": 36, "detected": true}, {"name": "M06_load_sign", "reason": "Signed byte load incorrectly zero extends", "failed_tests": 2, "total_tests": 36, "detected": true}]

## verification

모두 최소1개 실패로 탐지. 복구는 알려진변경을 원문으로 되돌림; 12/12 통과.

## limits

실제 업스트림 버그·독립 진단 정확도 시험이 아님.

## 출처

- [PicoRV32 controlled Windows experiments, 2026-10-29](../../../references/chip-evidence/summary.json) · local-measured-experiment · 확인 2026-10-29 executed; 2026-10-30 imported hash checked
