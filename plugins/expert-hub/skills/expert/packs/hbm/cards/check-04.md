# HBM 검토 — 열

ID: `hbm:check-04` | both | reference-only; no production signoff or physics solver

열 검토 6개 항목; 초기 상태는 모두 미확인.

## conditions

제품 범위·승인 규격과 책임자를 먼저 확인.

## verification

K04 HBM/GPU 전력맵·workload·idle 포함 | 필요 증거: 전력 근거·coverage·실측 | 상태: 미확인
K05 stack·TIM·접촉·lid·냉각 geometry 확인 | 필요 증거: 도면·계측 | 상태: 미확인
K06 온도의존/방향성 물성과 계면저항 확인 | 필요 증거: 물성 curve·시험조건 | 상태: 미확인
K07 mesh·time step·에너지보존·수렴 검토 | 필요 증거: convergence study | 상태: 미확인
K08 calibration 외 독립 조건 검증 | 필요 증거: 검증 세트 온도 residual | 상태: 미확인
K09 다이별 hotspot·sensor offset·과도 peak 확인 | 필요 증거: T(x,y,z,t)와 불확도 | 상태: 미확인

## limits

실제 시험 완료/합격 판정이 아니며 사용자 증거 없이는 상태를 바꾸지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
