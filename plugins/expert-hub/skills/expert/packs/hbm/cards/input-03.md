# HBM 입력자료 — 물성

ID: `hbm:input-03` | both | reference-only; no production signoff or physics solver

물성 자료 4개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF09 k_x / k_y / k_z versus T | 단위: W/(m·K) | 정의: 온도별 방향성 열전도도 | 확보: 공급사+시험 | 이유: 등방성 가정의 오차
DF10 rho / Cp versus T | 단위: kg/m³; J/(kg·K) | 정의: 밀도·비열 | 확보: 공급사+시험 | 이유: 과도해석 열용량
DF11 E / nu / CTE versus T | 단위: Pa; 무차원; 1/K | 정의: 탄성·포아송·팽창계수; Tg 전후 | 확보: DMA/TMA | 이유: warpage/응력
DF12 Tg / cure_shrinkage / viscoelasticity | 단위: °C; %; 모델계수 | 정의: 경화이력·점탄성 모델 포함 | 확보: DSC/DMA/공정 | 이유: 상온 E만 쓰는 오류 방지

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
