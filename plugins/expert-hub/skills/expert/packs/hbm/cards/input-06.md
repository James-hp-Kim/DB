# HBM 입력자료 — 발열

ID: `hbm:input-06` | both | reference-only; no production signoff or physics solver

발열 자료 2개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF16 die_power_by_region_and_time | 단위: W; s | 정의: base/core/PHY별 P(x,y,t) | 확보: 활동도 해석·실측 | 이유: 총전력 하나로 hotspot 숨김 방지
DF17 workload / V / data_rate | 단위: 문자열; V; Gbps/pin | 정의: idle/read/write/refresh 상태 | 확보: 검증·시스템 | 이유: power 조건 재현

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
