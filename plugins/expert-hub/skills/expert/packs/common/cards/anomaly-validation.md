# 이상탐지 성능 검증과 라벨 부족

ID: `common:anomaly-validation` | deep | reference-only

탐지기끼리 동의한다는 사실만으로 정확도를 증명할 수 없다. 검증 사례와 업무 비용을 기준으로 평가한다.

## conditions

가능하면 알려진 사건과 정상 기간으로 시간 분리 검증을 구성한다. 같은 LOT/설비 이력이 학습과 검증에 새지 않게 한다.

## verification

검토 가능한 상위 k건에서 precision@k, 알려진 이상에 대한 recall, 오경보 수/단위 시간, 검출 지연을 함께 평가한다.

## interpretation

라벨이 없으면 전문가 표본 검토, 기준 변화 민감도, 재현성 등을 보고하되 정답 기반 정확도처럼 표현하지 않는다.

## limits

여러 탐지기의 합의·자체 분리도는 보조 진단이다. 동일한 편향으로 모두 틀릴 수 있다.
인공 이상 주입은 회귀 테스트에는 유용하지만 실제 생산 불량 검증을 대체하지 않는다.

## 출처

- [yzhao062/pyod: pyod/skills/od_expert/SKILL.md](https://github.com/yzhao062/pyod/blob/7e1330e10ac5c56ed402fbbaa41b225efb4bbc5c/pyod/skills/od_expert/SKILL.md) · community-source · 확인 2026-10-29
- [scikit-learn: Novelty and outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html) · primary · 확인 2026-10-29
