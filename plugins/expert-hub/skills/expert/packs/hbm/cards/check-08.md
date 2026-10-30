# HBM 검토 — RTL

ID: `hbm:check-08` | both | reference-only; no production signoff or physics solver

RTL 검토 3개 항목; 초기 상태는 모두 미확인.

## conditions

제품 범위·승인 규격과 책임자를 먼저 확인.

## verification

K14 sensor CDC/RDC·reset·timeout·fault 처리 | 필요 증거: assertion·CDC/RDC·오류주입 | 상태: 미확인
K15 throttle hysteresis·응답지연·성능 영향 | 필요 증거: 온도 overshoot·BW loss | 상태: 미확인
K16 전력상태 전환·UPF와 실제 전원순서 일치 | 필요 증거: power-aware regression | 상태: 미확인

## limits

실제 시험 완료/합격 판정이 아니며 사용자 증거 없이는 상태를 바꾸지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
