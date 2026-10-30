# 데이터 프로파일과 최소 조회 경로

ID: `analytics:profile` | both | scripts/profile_data.py; CLI profile

원시 행을 대화에 올리기 전에 지정 열의 결측·수치·기간을 로컬 요약하고 질문에 맞는 팩만 조회한다.

## conditions

읽을 파일과 분석 목적이 정해져 있어야 한다. profile은 CSV만 지원하며 업무 의미를 자동 확정하지 않는다.

## procedure

expert.py profile FILE --columns 필요한열 --task forecast|sales|quality|general 실행. 기본 앞 100000행을 검사하며 complete_scan=false면 전체 통계로 말하지 않는다. suggested_lookups의 query/packs를 이미 검색한 data-analyst context와 함께 lookup에 전달하고 관련 id의 조건·절차·한계만 읽는다.

## limits

최대 30열, 기본 12열; 긴 결과는 열 요약을 생략하고 개수를 표시한다. 카디널리티는 256개 이후 하한이다. 키 중복·시계열 연속성·정렬은 별도 검사한다. Excel은 먼저 선택 시트만 로컬 변환한다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
