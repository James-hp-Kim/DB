# NAND 입력 자료를 최소 근거 조회로 연결

ID: `nand:input-contract` | both | retrieval guidance; NAND log parser not bundled

질문 목적·제품 조건·증상·이미 확인한 근거만 추려 retry/LLR/CDC/규격/지표 항목을 검색한다. 대량 로그는 로컬 집계 후 요약만 전달한다.

## conditions

자료 유형: 질문/RTL 일부/검증 로그/CSV 요약/공개 논문. 대상 NAND revision, 관심 블록, 기준 조건과 원하는 판단을 적는다. 비공개 원본은 저장소 밖에 둔다.

## procedure

1. 증상과 업무 목적을 1~3개의 핵심어로 추린다. 2. catalog NAND의 context로 lookup 상위 3건만 확인한다. 3. conditions와 limits를 먼저 읽고 procedure/verification을 필요한 경우 추가한다. 4. 논문 수치 적용 전 interpretation과 출처 access를 확인한다. 5. 대량 행은 로컬에서 표본수·분모·단위·조건별 집계와 대표 오류 행만 추출한다. 필요한 통계 지침은 common 팩을 명시적으로 선택한다.

## verification

원본 위치/행, 입력 단위·분모·기간, baseline/후보의 동일 조건, 재현 명령, 근거 ID와 source URL을 남긴다. 검색에 없으면 필요한 사양/자료를 특정한다.

## limits

자동 ingestion·파형 해석·NAND 전용 계산기·상용 EDA 실행·사내 규격 판정은 제공하지 않는다. 파일 전달만으로 개인 DB에 저장하지 않는다.

## 출처

- [NAND 연구 변환·설계 제안 및 미확보 데이터](../../../../../../../docs/NAND_PROVENANCE.md) · authored-design-proposal · 확인 2026-10-30
