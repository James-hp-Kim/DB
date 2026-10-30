# 전처리 규칙과 누수 없는 파이프라인

ID: `analytics:preprocessing` | both | reference-only

결측·0·취소·이상치는 다른 의미다. 학습되는 변환은 분할한 학습 구간 안에서만 적합한다.

## conditions

데이터 계약과 학습/검증 경계가 정해져 있어야 한다.

## procedure

원본을 보존하고 처리 전후 건수를 기록한다. 결측 대체·스케일링·변수 선택을 Pipeline으로 묶고 각 fold train에서 fit, validation/test에는 transform만 적용한다.

## limits

자동 삭제나 전체 기간 보간으로 미래 정보를 섞지 않는다. Pipeline도 잘못 만든 미래 특징이나 잘못된 분할 자체를 해결하지 못한다.

## 출처

- [scikit-learn: Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
