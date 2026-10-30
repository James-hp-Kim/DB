# 기준모델부터 ML까지 비교

ID: `sales:baselines` | both | scripts/backtest.py; optional scripts/tune.py

naive·seasonal naive·mean·drift를 먼저 계산하고 복잡한 후보의 추가 가치를 평가한다.

## conditions

기준모델도 동일 train과 평가 행을 사용해야 한다.

## procedure

단순 기준 비교 후 Ridge lag/alpha를 개발 folds에서 탐색한다. 개선되지 않으면 기준모델을 유지한다. 학습시간·예측시간과 큰 제품의 악화도 검토한다.

## limits

이 순서는 비용을 줄이려는 시작점이며 모델 정확도 순위를 뜻하지 않는다. 계절 길이와 추세 변화에 따라 결과가 달라진다.

## 출처

- [Forecasting: Principles and Practice — toolbox](https://otexts.com/fpp3/toolbox.html) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
