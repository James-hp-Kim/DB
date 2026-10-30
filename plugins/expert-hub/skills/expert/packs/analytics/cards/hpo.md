# 적은 호출로 하이퍼파라미터 탐색

ID: `analytics:hpo` | both | scripts/tune.py: Ridge lag/alpha only

실험 반복은 로컬 루프에 맡기고 예산·목적함수·시드·선택 결과만 Codex에 반환한다.

## conditions

동일 개발 folds와 주지표, 최대 trial 수, 시간 예산을 정한다.

## procedure

Optuna sampler로 후보를 제안하고 trial.report/should_prune으로 중간 성과를 평가한다. 먼저 작은 탐색으로 방향을 고른 뒤 선택 후보만 확대한다. study·설정·버전·실패 원인을 저장한다.

## limits

Pruning 기준과 timeout의 의미를 확인한다. 동봉 예제 timeout은 진행 trial을 강제 중단하지 않는다. 적은 토큰은 적은 연산시간과 동일하지 않다.

## 출처

- [Optuna: Efficient Optimization Algorithms](https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/003_efficient_optimization_algorithms.html) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
