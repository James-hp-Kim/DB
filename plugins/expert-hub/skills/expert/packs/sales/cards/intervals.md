# 예측구간과 연간 합계

ID: `sales:intervals` | both | reference-only

점예측과 구간의 포함률·폭을 별도로 평가하고 기간 간 의존성을 보존한다.

## conditions

예측 분포 또는 샘플 경로를 만들 수 있는 모델이 필요하다.

## procedure

동일 평가기간에서 명목 포함률·실제 포함률·구간 폭과 quantile loss를 비교한다. 연간 합계 구간은 월별 공동 샘플 경로 등을 합해 계산한다.

## limits

월별 quantile을 합한 값은 일반적으로 연간 quantile이 아니다. 동봉 실행기는 점예측만 제공한다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
