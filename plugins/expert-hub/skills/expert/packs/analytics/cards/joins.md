# 조인·중복·집계의 행 수 검증

ID: `analytics:joins` | both | reference-only

키의 유일성과 일대다 관계를 확인하고 조인 전후 행 수·금액 합을 검증한다.

## conditions

행 식별자, 품목·고객·기간 키와 각 테이블의 집계 단위를 알아야 한다.

## procedure

미매칭 키, 중복 키, 조인 전후 행 수와 합계를 별도 집계한다. 예상 one-to-one/many-to-one 계약을 검증한 뒤 결합한다. 반복 거래를 임의 중복 제거하지 않는다.

## limits

중복 값과 중복 거래는 다르다. many-to-many 조인으로 매출이 증폭될 수 있으며 누락 키를 0 매출로 간주하면 안 된다.

## verification

공유 전 핵심 합계를 독립 재계산한다. 비교 기간의 완결성·모집단·분모가 같은지 확인한다. 분석 결과의 조건과 한계를 함께 표시한다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
- [knowledge-work-plugins 선택 절차의 공개 근거](https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/data/skills/validate-data/SKILL.md) · upstream-technical-guidance · 확인 2026-10-30
