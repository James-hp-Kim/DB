# 센서·throttle·refresh 연계

ID: `hbm:experiment-e06` | deep | reference-only; no production signoff or physics solver

제안: 센서가 hotspot을 놓치는 정도 및 제어 지연

## conditions

비균일 activity·센서 오차·sampling·hysteresis sweep

## procedure

센서가 hotspot을 놓치는 정도 및 제어 지연

## interpretation

overshoot, latency, false throttle, BW loss, ECC counters

## verification

제품 허용온도와 margin 입력 후 온도/성능 동시 검증

## limits

미수행 실험 제안. 개선량·합격값은 미확정이며 사전 baseline과 불확실성을 확인해야 함. 우선순위: 우선

## 출처

- [Thermal Improvement of HBM with Joint Thermal Resistance Reduction for Scaling 12 Stacks and Beyond](https://ieeexplore.ieee.org/abstract/document/10195397/) · 공식 초록 확인; 전문 미확보 · 확인 2026-10-29
- [Comparative Study of Thermal Dissipation in Increasing DRAM Layers of HBM Using 3D FEA Simulations](https://www.jsts.org/jsts/XmlViewer/f436715) · 공개 전문·조건·표 확인 · 확인 2026-10-29
- [VCS / Verdi](https://www.synopsys.com/verification/simulation/vcs.html) · source_entry · 확인 2026-10-29
