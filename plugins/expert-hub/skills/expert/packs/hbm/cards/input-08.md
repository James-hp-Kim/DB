# HBM 입력자료 — 온도

ID: `hbm:input-08` | both | reference-only; no production signoff or physics solver

온도 자료 2개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF21 Tj_peak / sensor_T / timestamp | 단위: °C; s | 정의: 위치·샘플링률·calibration 함께 | 확보: 센서/IR/TSP | 이유: hotspot과 센서값 구분
DF22 measurement_uncertainty | 단위: °C 또는 % | 정의: 확장불확도·coverage factor/방법 | 확보: 계측 검교정 | 이유: 유의미한 개선 판단

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
