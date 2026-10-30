# 매출 예측 MAE·WAPE·MASE·편향

ID: `sales:metrics` | both | scripts/backtest.py score_rows

오차율은 분모·건수와 함께 보고하며 분모 0은 정의되지 않음으로 유지한다.

## conditions

예측-실제 오차 부호와 통화·집계 단위 및 평가 행을 고정한다.

## procedure

MAE=mean(abs(e)), RMSE=sqrt(mean(e²)), 본 패키지 WAPE=100*sum(abs(e))/sum(abs(y)). bias=mean(e). MASE는 각 fold train의 계절 naive 절대 차이 평균으로 나눈다. 전체와 제품·lead별 지표를 함께 확인한다.

## limits

순매출 음수 때문에 WAPE에 abs(y) 분모를 쓰는 정의를 명시한다. 분모 0은 null이다. MASE undefined 항목과 유효 건수를 표시한다. 품목별 비율의 단순 평균과 전체 WAPE는 다르다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
