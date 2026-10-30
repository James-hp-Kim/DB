# 지연 실행과 필요 열·행만 읽기

ID: `analytics:lazy` | both | reference-only

파일에서 시작하는 lazy 쿼리는 최적화가 실제 읽기량을 줄일 기회를 준다.

## conditions

Polars를 선택 설치하고 입력 스키마와 지원 연산을 확인한 경우에 사용한다.

## procedure

scan_csv/scan_parquet로 시작해 필요한 열 선택·기간 필터를 먼저 표현하고 실행 계획을 확인한다. 최종 집계나 선택 결과만 수집한다.

## limits

이미 전체 자료를 메모리에 읽은 뒤 lazy로 바꾸면 앞선 읽기 비용은 없어지지 않는다. 모든 연산의 메모리 사용이 자동으로 작아지는 것은 아니다.

## 출처

- [Polars: Lazy API Usage](https://docs.pola.rs/user-guide/lazy/using/) · primary-method-reference · 확인 2026-10-30
- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
