# HBM 입력자료 — 추적

ID: `hbm:input-01` | both | reference-only; no production signoff or physics solver

추적 자료 2개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF01 sample_id / wafer_id / lot_id | 단위: 문자열 | 정의: 시료·wafer·lot을 별도 식별 | 확보: MES/시험 기록 | 이유: lot 내부 상관을 무시한 독립표본 취급 방지
DF02 product / revision / process_split | 단위: 문자열 | 정의: HBM 세대·die revision·공정 split | 확보: 설계/공정 | 이유: 비교 대상의 동일성 판단

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
