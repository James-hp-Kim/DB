# 열모델-실측 상관

ID: `hbm:experiment-e01` | deep | reference-only; no production signoff or physics solver

제안: 현재 양산/개발 기준구조의 steady/transient 온도 보정

## conditions

power map·TIM BLT·contact R·냉각을 기록; 독립 조건에서 검증

## procedure

현재 양산/개발 기준구조의 steady/transient 온도 보정

## interpretation

Tj peak, sensor residual, Zth, energy balance

## verification

모델오차·센서오차·margin 목표는 사전 합의; baseline 없이는 개선율 채택 보류

## limits

미수행 실험 제안. 개선량·합격값은 미확정이며 사전 baseline과 불확실성을 확인해야 함. 우선순위: 최우선

## 출처

- [Advanced Packaging Technologies in Memory Applications for Future Generative AI Era](https://iedm23.mapyourshow.com/mys_shared/iedm23/handouts/15-6_Tue_14482.pdf) · 원문 PDF 확보·4쪽 및 표/그림 확인 · 확인 2026-10-29
- [Comparative Study of Thermal Dissipation in Increasing DRAM Layers of HBM Using 3D FEA Simulations](https://www.jsts.org/jsts/XmlViewer/f436715) · 공개 전문·조건·표 확인 · 확인 2026-10-29
- [Semiconductor and IC Package Thermal Metrics, SPRA953D](https://www.ti.com/lit/an/spra953d/spra953d.pdf) · 원문 PDF 확보·본문 확인 · 확인 2026-10-29
- [Icepak 3D-IC workflow](https://ansyshelp.ansys.com/public/Views/Secured/Electronics/v261/en/Subsystems/Icepak/Content/Icepak/3DIntegratedCircuitsinIcepak.htm) · 공식 기술 문서 · 확인 2026-10-29
- [Simcenter T3STER](https://www.siemens.com/en-gb/products/simcenter/physical-testing/t3ster/) · 공식 제품 설명 · 확인 2026-10-29
