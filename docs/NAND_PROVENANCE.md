# NAND 지식팩 출처와 변환

이 작업에서 작성한 2026-10-29 NAND RTL 공개 연구 패키지를 2026-10-30에 기존 Expert Hub에 통합했습니다. 웹 원문을 이번 변환에서 모두 재열람한 것은 아닙니다. 개별 출처의 checked와 레코드 reviewed는 당시 확인일을 유지합니다.

기존 124개 항목을 ID로 추적하고, K03의 오류 원인 부분을 `nand:error-physics`로 나눴으며 `nand:input-contract`를 추가해 NAND 팩은 126개입니다. 이번 NAND 작업은 기존 공통·품질 지식 항목의 내용을 수정하지 않았습니다. 논문 15개와 공식 출처 26개의 메타데이터를 공유 출처 레지스트리에 연결하고 자체 설계 제안 출처를 분리했습니다. 같은 허브에서 다른 분야도 추가되고 있으므로 전체 허브 건수는 배포 시점의 status 결과를 확인하세요.

기존 ID는 레코드 legacy_id로 유지합니다. P01 → nand:p01, V14 → nand:v14, D_raw_bits_compared → nand:d-raw-bits-compared로 변환했습니다. 공통 통계 설명은 common 팩을 명시적으로 조회하며 역할마다 복사하지 않습니다. K06의 일반적인 0회 실패 신뢰구간 설명은 common:rate-interval/time-structure 참조로 대체했습니다.

## 근거 수준

|표시|뜻|
|---|---|
|fulltext_key_sections_reviewed|원래 조사에서 필요한 본문 절을 검토. 독립 재현 아님|
|abstract_or_index|초록·색인 수준. 본문 확인이나 수치 재현으로 표현하지 않음|
|program_only|학회 프로그램만 확인. 회로 논문 본문 아님|
|source_entry|공식 출처의 목록. 개별 limits에 접근 수준 보존|
|design_proposal / field_definition|자체 설계·검증 제안 또는 수집 필드. 실측·사내 승인 기준 아님|
|research_synthesis|출처를 연결한 종합 설명. 제품별 적용 조건 별도 확인|

출처 상세에는 URL, 당시 확인일, 접근 제한을 보존했습니다. 사내 PDK, 공정 signoff, H matrix, 원시 실칩 로그, 미공개 수율/불량 분포는 없습니다. 논문의 개선율은 원저자 보고값이며 대상 제품의 기대 개선율로 바꾸지 않습니다.

논문 PDF·전문·유료 표준 원문은 배포하지 않습니다. 자체 요약과 링크만 포함하며 원문 권리는 각 권리자에게 있습니다. `nand-design`은 이 변환과 입력/검토 절차의 자체 제안 출처이며 외부 과학적 검증을 의미하지 않습니다. [제3자 권리 안내](../THIRD_PARTY_NOTICES.md)를 따릅니다.
