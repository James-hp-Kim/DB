# 동일 평가 표본과 겹치는 예측기간

ID: `sales:comparison` | both | scripts/backtest.py diagnostics

series×origin×lead를 평가 단위로 맞추고 unique target 건수도 별도로 기록한다.

## conditions

모든 후보가 같은 제품과 시점을 예측해야 한다.

## procedure

누락·실패 후보를 조용히 빼지 말고 실패 건수를 보인다. step<horizon이면 동일 실제 날짜에 여러 예측이 존재하므로 n과 unique_targets를 구분한다.

## limits

중복 예측오차를 독립 표본처럼 다루면 검정이 과신될 수 있다. 동일 표본 비교만으로 통계적 유의성이 증명되지 않는다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
