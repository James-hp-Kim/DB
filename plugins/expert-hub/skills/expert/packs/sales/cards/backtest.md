# 매출·시계열 롤링 백테스트

ID: `sales:backtest` | both | scripts/backtest.py + references/forecasting.md

예측 시점을 과거로 이동하며 실제 업무 horizon을 평가하고 최종 구간은 모델 선택에서 제외한다.

## conditions

horizon·gap·min_train·step·학습창·주지표·기준모델을 결과 보기 전에 고정한다.

## procedure

마지막 horizon을 홀드아웃으로 예약한다. 나머지 구간의 여러 origin에서 학습→미래 horizon 예측을 반복한다. 각 train에서 전처리를 다시 fit한다. 같은 series/origin/lead의 기준모델과 비교한 뒤 선택을 고정하고 별도 명령으로 최종 평가한다.

## limits

기본 구현은 nested CV가 아니다. 실제값 수정·자료 지연·계층·외생변수는 추가 설계가 필요하다. 최종 평가를 본 뒤 재튜닝하면 새 미사용 구간이 필요하다.

## 출처

- [Forecasting: Principles and Practice — toolbox](https://otexts.com/fpp3/toolbox.html) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
