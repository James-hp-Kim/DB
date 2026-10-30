# HBM 입력자료 — 형상

ID: `hbm:input-02` | both | reference-only; no production signoff or physics solver

형상 자료 6개 필드. 단위·정의·계측/설계 출처를 함께 받는다.

## conditions

입력값은 사용자 원본과 적용 revision에서 확보. 모르면 미확인으로 남김.

## procedure

DF03 dram_die_count | 단위: 개 | 정의: 베이스 다이 제외 core die 수 | 확보: 도면/단면 | 이유: 12Hi의 포함 범위 통일
DF04 die_thickness_by_layer | 단위: µm | 정의: 층별 두께와 top/base 구분 | 확보: 계측/도면 | 이유: 열경로·휨 변동
DF05 bump_pitch / diameter / height | 단위: µm | 정의: signal/power/thermal bump 각각 | 확보: SEM/도면 | 이유: 전기·열·응력 연결
DF06 thermal_bump_fraction | 단위: 0~1 | 정의: 관심 영역 전체 면적 대비 금속 면적; 분모 기록 | 확보: layout | 이유: P01 비교 재현
DF07 TSV_geometry / keepout | 단위: µm | 정의: TSV 지름·pitch·liner·배치 | 확보: PDK/layout | 이유: 응력·SI·열경로
DF08 TIM_BLT / step_height | 단위: µm | 정의: 압착 후 TIM 두께와 GPU-HBM 높이차 | 확보: 단면/계측 | 이유: 접촉저항·공차 영향

## limits

수집 템플릿이며 내부 데이터·허용치가 채워져 있지 않음.

## 출처

- [HBM 수집·구조화·적용 범위 기록](../../../../../../../docs/HBM_DATA.md) · package-design · 확인 2026-10-30
