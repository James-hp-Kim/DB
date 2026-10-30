# 딥러닝 도입 판단과 확장 경계

ID: `analytics:deep-learning` | both | reference-only

자료량·시계열 관련성·계산 예산을 확인하고 같은 평가 조건에서 단순 모델과 비교한다.

## conditions

충분한 개발 자료와 GPU/CPU 예산, 시간 검증 계약이 있을 때 후보로 검토한다.

## procedure

NeuralForecast의 모델을 후보로 조사하고 input_size·학습률·hidden size·dropout·학습 종료 조건을 기록한다. 학습 가중치는 로컬 훈련으로 추정하고 최종 홀드아웃을 early stopping에 쓰지 않는다.

## limits

NeuralForecast와 GPU 학습은 이 패키지에서 실행 연결되지 않았다. 공식 저장소의 모델 제공은 특정 회사에서 성능이 향상된다는 증거가 아니다.

## 출처

- [Nixtla NeuralForecast repository](https://github.com/Nixtla/neuralforecast) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
