# 예측 시점에 알려진 정보와 gap

ID: `sales:availability` | both | reference-only

미래 계획 변수와 나중에 확정된 실제값을 구분하고 정보가 실제로 공개된 시점을 맞춘다.

## conditions

회계 마감·출하 확정·경제지표 공개 지연을 파악한다.

## procedure

as-of 시점 기준으로 스냅샷을 결합한다. lag는 series별 shift로 만들고 재귀 예측은 미래 실측 대신 이전 예측값을 사용한다. gap의 길이와 실제 예측 lead를 함께 기록한다.

## limits

gap만으로 모든 누수가 해결되지 않는다. 겹치는 기간 라벨이면 별도의 purge 설계가 필요하다. 동봉 실행기는 외생변수를 학습하지 않는다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
