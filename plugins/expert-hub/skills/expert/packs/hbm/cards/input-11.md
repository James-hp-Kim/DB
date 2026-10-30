# HBM 입력자료 — 신뢰성

ID: `hbm:input-11` | both | reference-only; no production signoff or physics solver

신뢰성 자료 3개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF25 stress_profile | 단위: °C; RH%; V; s | 정의: ramp/dwell/주기/바이어스 포함 | 확보: 시험 recipe | 이유: 가속조건의 동등성
DF26 time_or_cycles_to_failure | 단위: h 또는 cycle | 정의: 미고장 시료도 종료시간과 censoring 기록 | 확보: 시험로그 | 이유: Weibull 생존분석
DF27 failure_mode / location / FA_id | 단위: 분류·링크 | 정의: open/short/delam/crack/retention 구분 | 확보: FA | 이유: 서로 다른 고장기구 혼합 방지

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
