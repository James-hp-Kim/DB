# HBM 입력자료 — 냉각

ID: `hbm:input-07` | both | reference-only; no production signoff or physics solver

냉각 자료 3개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF18 inlet_T / ambient_T / case_T | 단위: °C | 정의: 각 온도의 정의·센서 위치 | 확보: 시험환경 | 이유: Rth 기준온도 혼동 방지
DF19 flow / pressure_drop / pump_power | 단위: L/min; Pa; W | 정의: 냉각수·유량·압력 센서 교정 | 확보: 냉각장비 | 이유: 냉각 성능/비용 비교
DF20 h / contact_pressure / clamp | 단위: W/(m²·K); Pa | 정의: 공간 분포·구속조건 | 확보: CFD/시험 | 이유: thermal/structural boundary

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
