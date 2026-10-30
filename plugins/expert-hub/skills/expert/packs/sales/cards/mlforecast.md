# MLForecast·트리 모델 확장

ID: `sales:mlforecast` | both | reference-only

lag·달력·허용된 외부 변수를 모델 입력으로 구성하고 동일 folds에서 비교한다.

## conditions

동봉 Ridge보다 복잡한 후보가 필요한 경우와 추가 설치가 가능한 경우에 검토한다.

## procedure

MLForecast의 특징 생성과 모델 연결을 검토한다. 어댑터는 기존 fold의 train만 받아 동일 평가 키를 반환하도록 만들고 타깃 변환의 복원 단위를 검증한다.

## limits

라이브러리 자동 연결은 아직 구현하지 않았다. 미래 외부 변수의 실제값을 미리 넣지 않는다. 공식 제공 기능과 업무 성능은 별도 검증이다.

## 출처

- [Nixtla MLForecast repository](https://github.com/Nixtla/mlforecast) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
