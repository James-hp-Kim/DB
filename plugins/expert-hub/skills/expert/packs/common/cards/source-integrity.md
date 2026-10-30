# 원본·행 추적·중복 검토

ID: `common:source-integrity` | both | scan + convert_xlsx.py

원본을 보존하고 동일 행을 후보로 표시한다. 재검·반복측정인지 확인하기 전에 삭제하지 않는다.

## procedure

분석 입력의 SHA-256, 사용 열, 필터, 기간, 코드 버전, 분석 옵션을 결과와 보관한다.

## interpretation

CSV record는 헤더를 제외한 논리 레코드 번호다. 셀 안 줄바꿈 때문에 텍스트 파일 줄번호와 다를 수 있다.
XLSX 변환은 __source_excel_row로 원래 행을 보존한다. 숨김 행도 포함한다.
완전히 같은 행이 반복되어도 정상 반복측정·별도 이벤트일 수 있다. 업무키(LOT+장비+측정시각+측정회차 등)로 확인한다.

## limits

scan은 중복 후보를 표시하고 모든 원본 행을 유지한다. 삭제·병합은 별도 결정이다.

## 출처

- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
