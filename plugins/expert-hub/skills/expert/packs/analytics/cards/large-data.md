# 대용량 분석: 열·행 축소와 메모리 예산

ID: `analytics:large-data` | both | reference-only

필요 열과 기간을 먼저 제한하고 로컬 집계 결과만 전달한다. 데이터 크기와 연산의 메모리 특성을 함께 본다.

## conditions

파일 크기, 사용 가능 메모리, 조인/정렬/그룹 수, 중간 결과와 디스크 공간을 확인한다.

## procedure

기본 profile은 행을 순차 처리한다. 대규모 집계는 DuckDB 또는 Polars lazy를 검토하고 SQL/쿼리 계획과 실제 peak memory를 확인한다. 원본 대신 목적에 맞춘 집계·Parquet 분할을 사용한다.

## limits

SQLite 지식 DB는 회사 원시 빅데이터용 분산 처리 엔진이 아니다. 조인·정렬·고카디널리티 집계는 스트리밍에서도 병목이 될 수 있다. DuckDB/Polars는 선택 도구이며 동봉 실행기 성능 보장이 아니다.

## 출처

- [DuckDB: Tuning Workloads](https://duckdb.org/docs/2.0/guides/performance/how_to_tune_workloads) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
