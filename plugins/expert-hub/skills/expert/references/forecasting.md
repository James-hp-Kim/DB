# 매출·시계열 백테스트 절차

이 문서는 설계 기준이며 실제 구현 범위는 아래에 별도로 적는다.

## 1. 예측 계약 고정

target, series 단위, 주기, forecast origin, horizon, 정보 지연, 학습창, 주지표,
제품 가중치, 실패 처리, 비교 기준, 시간 예산을 결과를 보기 전에 정한다.
월별 다음 분기 예측이면 horizon=3의 업무 의미로 평가한다. 예시 기본값 horizon=6은 사용자의 사업 계획을 뜻하지 않는다.
같은 회사라도 현황 설명, 원인 추정, 수요 예측, 매출 예측은 성공 기준이 다르다.

## 2. 최종 평가 구간 예약

마지막 기간을 최종 홀드아웃으로 떼어 두고 특징·모델·튜닝·앙상블 선택에서 제외한다.
기본 실행기는 마지막 `horizon`개 관측을 예약하며 `holdout_periods=horizon`이어야 한다.
`gap>0`이면 홀드아웃 앞 gap도 튜닝 자료에서 제외한다.
파일 해시는 전체 입력을 식별하지만 모델 적합·목적함수는 홀드아웃 y를 사용하지 않는다.

## 3. 개발 구간 rolling-origin 분할

여러 과거 예측 시점에서 train을 만들고 이후 horizon을 평가한다.
expanding은 누적 train, rolling은 `train_window`로 최근 길이를 제한한다.
모든 series는 같은 날짜 cutoff를 따른다. 표를 행 번호만으로 나눠 다른 제품의 미래가 train에 섞이지 않게 한다.
출하와 매출 확정 시점이 다르거나 지표 공표 지연이 있으면 as-of/release 시각을 적용한다.
gap은 모든 누수를 자동 해결하지 않는다. target이 겹치는 구간 집계면 label span 기준 purge가 추가로 필요할 수 있다.

## 4. fold마다 재학습

각 train에서 결측 대체·스케일링·변수 선택을 fit한다. held-out 자료로 변환을 학습하지 않는다.
lag/rolling 특징은 series별로 shift하며 미래 실측을 넣지 않는다.
재귀 예측은 다음 단계 입력에 자신의 예측을 넣는다. 알려진 미래 계획 변수와 미래 실제값을 구분한다.

## 5. 같은 표본의 기준모델 비교

기본 기준은 naive·seasonal naive·mean·drift. 후보는 정확히 같은 `(unique_id,origin,lead)`를 예측한다.
후보가 일부 제품을 실패했다면 해당 행을 조용히 삭제하지 않는다. 실패·누락 수와 공통 표본을 공개한다.
step<horizon이면 동일 실제 날짜가 여러 origin에 등장한다. n은 예측 의사결정 수이며 독립 표본 수가 아니다.
기본 실행기는 `n`, `series_count`, `origin_count`, `unique_targets`를 기록한다.

## 6. 지표

`e=prediction-actual`. MAE=mean(|e|), RMSE=sqrt(mean(e²)).
본 패키지 WAPE=100×Σ|e|/Σ|actual|. 분모=0은 null. 음수 순매출에서도 abs 분모라는 정의를 명시한다.
편향은 mean(e), 정규화 편향은 100×Σe/Σ|actual|. 양수는 과대예측이다.
MASE 분모는 해당 train의 계절 naive 절대차 평균이다. 0/불충분이면 해당 scaled error는 undefined이며
`mase_defined_n`을 전체 n과 함께 보고한다. 서로 다른 계절 길이를 사용한 MASE는 정의를 확인하고 비교한다.
총오차 외에 series별·lead별·origin별 성능을 보고한다. 제품별 WAPE 단순 평균과 전체 WAPE를 혼용하지 않는다.

## 7. 튜닝과 구조 실험

inner 개발 CV만 Optuna objective로 사용한다. 각 후보에 같은 folds를 적용한다.
학습기간·특징·모델·손실/앙상블 가중치 변경을 기록한다. 결과가 좋아 보일 때까지 최종 평가 구간을 다시 쓰지 않는다.
기본 예제는 per-series Ridge의 alpha와 lag 길이를 탐색한다. 기준모델보다 나쁘면 기준모델을 유지한다.
더 엄격한 nested CV가 필요하면 outer train 안에서 튜닝을 매번 다시 수행한다. 기본 코드는 nested CV를 구현하지 않는다.

## 8. 고정 선택과 최종 평가

`selection.json`에 선택 모델, 데이터·설정 해시, 엔진 버전을 저장한다.
코드 파일 무결성은 배포물의 `MANIFEST.sha256`으로 별도 확인한다.
`--evaluate-holdout --selection ...`으로만 최종 평가한다. 선택 모델과 사전에 정한 reference를 비교한다.
최종 구간을 읽은 후 튜닝을 바꾸면 새 미사용 기간이 필요하다. 프로그램은 다른 폴더로의 반복 평가까지 차단하지 못한다.
회사 차원의 holdout 사용 이력은 별도 관리한다. 이 실행 예제는 자동 출시/승인을 수행하지 않는다.

## 9. 판단과 인수인계

기준 대비 변화, 절대 오차, 큰 제품의 악화 여부, 기간별 안정성, 학습·추론 비용,
데이터의 실제 이용 가능성, 미검증 범위를 보고한다. 자동으로 '대기업급 검증 완료'라고 판정하지 않는다.
성능 기준과 허용 편향은 업무 담당자가 정한다. 유리한 결과를 보고 기준을 변경하지 않는다.
통계적 개선 주장을 하려면 의존성·다중 비교에 맞는 방법과 충분한 표본이 필요하다.

## 10. 예측구간·집계 확장

명목 구간 대비 실제 포함률·폭과 적절한 quantile 지표를 별도 평가한다.
월별 점예측 합은 연간 점예측이 되지만 월별 quantile 합은 연간 quantile이 아니다.
연간 구간은 공동 샘플 경로 등 기간 간 의존성을 반영한다.
계층 reconciliation, 간헐 수요, cold-start, 구간 추정은 확장 구현과 별도 검증이 필요하다.

## 동봉 실행 예제

README의 명령은 개발 비교 → 선택 ML 튜닝 → 고정 후 홀드아웃 평가 순이다.
`predictions.csv`에는 origin·lead·실제·예측·MASE scale이 남는다.
`report.json`에는 config·입력 hash·평가 범위·분모·진단이 남는다.
합성 데이터 결과는 실제 매출 성능 증거가 아니다.

참고: [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html),
[Forecasting: Principles and Practice](https://otexts.com/fpp3/toolbox.html).
도구 사용 절차와 사업 계약·홀드아웃 관리 규칙은 이 패키지의 설계다.
