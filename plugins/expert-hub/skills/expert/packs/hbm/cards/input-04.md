# HBM 입력자료 — 계면

ID: `hbm:input-04` | both | reference-only; no production signoff or physics solver

계면 자료 2개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF13 contact_thermal_resistance | 단위: m²·K/W | 정의: 면적 정규화값인지 K/W인지 명시 | 확보: 열측정·보정 | 이유: bulk k와 계면 저항 분리
DF14 adhesion / fracture_parameters | 단위: J/m² 등 | 정의: 모드혼합·습도·온도 조건 기록 | 확보: DCB/계면시험 | 이유: 박리 예측

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
