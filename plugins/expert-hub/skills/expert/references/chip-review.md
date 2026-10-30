# 칩 설계·검증: 필요한 근거만 조회

이 문서는 자체 검토 방법이다. SK hynix 내부 설계 기준·PDK·JEDEC 전문·실제 회사 RTL은 포함하지 않는다. DRAM·HBM 팩은 2026-10-29에 수집한 공개 자료의 편집 요약을 2026-10-30에 이관했다. 이관일이 웹 재검증일은 아니다.

## 최소 조회 순서

1. `expert_catalog(query="chip-design-verification", limit=1)`의 context를 선택한다. 이 역할은 기본 `rtl` 팩만 조회한다. 통계·분모·편향 지침이 필요하면 `packs=["common"]`을 명시한다.
2. 파일이 있으면 `expert_reference_input(file=<사용자가 준 경로>, context, query=<구체적인 쟁점>)`를 실행한다. 파일이 없으면 `expert_lookup`으로 시작한다. 입력을 지식으로 자동 수집하지 않는다.
3. 상위 3개 요약에서 최대 1~2개 ID를 고른다. 먼저 conditions/limits를 읽고, 필요한 procedure/verification/interpretation만 추가한다. 읽기 상한은 보통 2,500~3,500자로 지정한다.
4. 결론에 사용하는 출처 ID만 `expert_source`로 읽는다. 논문은 장치·세대·실험 조건을 보존한다. 조건이 맞지 않으면 적용 후보로만 제시한다.
5. 같은 파일 해시·질문·버전의 조회 결과가 현재 대화에 있으면 재사용한다. 다음 가설을 구별하는 증거만 추가 요청한다. 실제 파일 전체를 프롬프트로 붙이지 않는다.

`expert_reference_input`은 로컬 파일의 주제를 찾아 DB와 연결하는 기능이다. 주석·문자열을 포함한 키워드 탐색이므로 버그 탐지·구문 분석·CDC/STA/형식 검증 결과가 아니다. 경로·본문을 반환하지 않고 SHA256·형식·크기·줄 수·주제별 최대 3개 줄 번호를 반환한다. 최대 3개 주제의 합성 질의를 사용하며 나머지 주제 이름은 좁혀 재조회할 단서로만 반환한다. 특정 질문을 주면 그 질문이 검색어가 된다. 결과가 없다는 이유로 전체 팩을 읽지 않는다.

## 입력 계약

| 검토 대상 | 필요한 최소 입력 | 추가될 때 도움이 되는 증거 |
|---|---|---|
| RTL 기능/CDC | 관련 모듈·interface·clock/reset·증상 | 실패 seed, assertion 위치, FIFO full/empty·reset 순서 |
| 타이밍 | WNS/TNS가 나온 관련 report 구간, mode/corner | SDC, start/end point, setup/hold 구분, 경로 예외 근거 |
| refresh·명령 | 세대·speed bin·mode, 명령 trace 일부 | 승인 spec revision, tRFC/tREFI, counter·debt 정책 |
| UVM/SVA | 실패 로그·assertion/coverage 관련 구간 | reference model 독립성, assumptions, vacuity, seed |
| 전력/PPA | baseline/variant 조건·지표·단위·집계 창 | PVT/RC, library, 활동률, workload, throughput/latency |
| 공개 CSV | 열 이름과 해당 분석 구간, 파일 식별자 | chip/board ID, 필터, 단위, 반복 측정·보정·요약 구분 |

지원: UTF-8의 `.sv .svh .v .sdc .upf .log .rpt .csv .json .md .txt`, 파일당 2 MiB 이하. 큰 파일은 로컬에서 관련 구간을 추출해 제공한다. JSON 문법/CSV 수치 분석은 이 도구의 기능이 아니다. PDF·XLSX·파형은 텍스트 report나 발췌로 변환해 연결하고, 원본 판독과 수치 검증은 별도 수행한다. CP949 등은 원본을 보존하고 UTF-8 사본을 만든다.

## 검토 결과 형식

먼저 결론과 상태를 쓴다: **확인된 결함 / 근거 있는 가설 / 개선 기회 / 증거 부족**. 이어 입력 증거 위치 → 관련 DB ID/출처 → 제안 변경 → 반증 검사 → 비교할 지표·조건을 짧게 제시한다. 파형·실행 로그·원문 규격이 없으면 통과, 원인 확정, 개선율을 만들어내지 않는다.

## 자료 구분

`rtl:s* / h* / t* / k* / d*`는 출처·도구·공개 자료 소개, `p*`는 논문 요약, `b*`는 기본 개념, `c*`는 미평가 검토 항목, `e*`는 미실행 실험안, `ds*`는 원본 CSV의 스키마·해시·범위, `i*`는 미확보 사내 입력, `g*`는 적용 한계다. 실제 검색에서는 ID를 추측하지 않고 반환된 ID를 사용한다.

141개 카드에 공개 출처 54건(논문 13편 포함), 개념 18개, 도구 조합 9개, 검토 항목 28개, 실험안 6개, 데이터셋 설명 10개, 미확보 입력 7개, 해석 가이드 9개를 담았다. 논문 전문·원시 CSV는 넣지 않는다. `source` 조회는 URL과 수집 시 확인 수준을 반환한다.

## 잘못 적용하기 쉬운 한계

- tRCD/tRFC·전압·MR bit는 승인된 제품별 규격 없이 확정하지 않는다.
- 호스트 controller 연구를 DRAM core/base die RTL의 직접 개선 효과로 바꾸지 않는다.
- `num_bitflips`는 해당 전력 데이터에서 자극 전환 수다. 메모리 고장 건수로 집계하지 않는다.
- 원시 행 수는 독립 chip 수가 아니다. 미확인 파일 간 chip ID를 임의 결합하지 않는다.
- positive slack·DRC=0·VCD 기반 전력 추정은 전체 signoff나 실리콘 실측 증거가 아니다.
- 도구 소개는 해당 버전의 Windows 지원·회사 승인·라이선스 확보를 보장하지 않는다. EDA 실행환경은 별도 준비 대상이다.
