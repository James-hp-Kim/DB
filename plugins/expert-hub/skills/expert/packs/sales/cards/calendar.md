# 시계열 달력·결측·간헐 매출

ID: `sales:calendar` | both | scripts/backtest.py input validation

거래 없음, 관측 누락, 영업 종료를 구분하고 제품별 달력을 정렬한다.

## conditions

series 키, 일/월 주기, 휴일·영업일과 집계 범위가 정해져야 한다.

## procedure

series×date의 중복을 확인한 뒤 합계 또는 다른 집계 규칙을 적용한다. 누락 날짜를 표시하고 실제 0인지 확인한다. 전처리 후 학습용 unique_id,ds,y를 만든다.

## limits

동봉 backtest는 동일 달력을 가진 연속 D/MS만 지원한다. 자동 채움·간헐수요 전용모델·신제품 cold start는 구현하지 않았다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
