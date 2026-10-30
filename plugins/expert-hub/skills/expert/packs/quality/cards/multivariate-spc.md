# 다변량 SPC: 개별 정상값의 비정상 조합

ID: `quality:multivariate-spc` | deep | reference-only

서로 상관된 변수의 조합 이상을 평가한다. 정상 기준의 공분산 구조와 추정 불확실성이 중요하다.

## interpretation

개별 값은 범위 안이어도 변수 간 관계가 달라질 수 있다. Hotelling T²는 공분산을 고려한 거리로 이런 상태를 탐색한다.
Phase I/II, 추정에 사용한 데이터와 감시 데이터가 다른지에 따라 관리한계가 달라진다. T² 값을 임의의 3 sigma에 비교하지 않는다.

## conditions

변수 수에 비해 정상 표본이 적거나 공선성이 크면 공분산 역행렬이 불안정하다. 차원 축소/정규화와 기준 구간 검증을 검토한다.

## limits

PCA 잔차 지표는 선택한 부분공간 밖 변화를 추가로 볼 때 검토한다. 모델의 설명 변수 기여는 원인 입증이 아니다.
이 카드의 방법은 참조 지침이다. 번들 anomalies는 T² 구현이 아니라 ECOD/Isolation Forest 기반 탐색이다.

## 출처

- [NIST: Hotelling control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc341.htm) · primary · 확인 2026-10-29
- [scikit-learn: Novelty and outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html) · primary · 확인 2026-10-29
