# ML 평가 분할과 최종 검증

ID: `analytics:validation` | both | reference-only

배포 때 만날 미관측 단위를 기준으로 시간·고객·설비 그룹을 분리한다.

## conditions

예측 대상, 동일 개체 반복 여부, 시간 의존, 실패 비용을 먼저 정한다.

## procedure

시간 문제는 과거→미래, 신규 고객 일반화는 고객 그룹 분할을 검토한다. 반복 튜닝에 쓴 개발 점수와 최종 미사용 구간 점수를 구분하고 동일 평가 행으로 후보를 비교한다.

## limits

무작위 행 분할은 시간/개체 누수를 만들 수 있다. 한 번 본 최종 평가를 재튜닝 기준으로 쓰면 더 이상 독립 검증이 아니다.

## 출처

- [scikit-learn: Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
