# 반도체 AI 스킬 전문가

먼저 [반도체 근거 연결](semiconductor-evidence.md)을 적용한다. 한국어·용어 확인도 이 절차를 따른다.

1. `expert_catalog(query="semiconductor-ai",limit=1)`로 context를 받는다. 같은 키를 후속 호출에 전달한다.
2. 명시적인 로컬 텍스트 파일이 있으면 `expert_reference_input(file,context,max_chars=2500)`으로 주제·행 위치·관련 요약만 가져온다. 입력은 저장하지 않는다. 키워드 라우팅이며 결함 탐지가 아니다.
3. 파일이 없으면 `expert_lookup(query,context,packs=[한 팩],limit=2,max_chars=2000)`을 쓴다. 웨이퍼 이미지 ML·학습/평가 분리이면 common에서 데이터 계약·평가를 검색하고, 칩 설계 검토 절차이면 chip-review, 소자 물리·pn 접합·MOS·C–V이면 semiconductor, HBM 열·패키징이면 hbm, 디지털 RTL/SDC/STA/PPA는 chip-rtl, 메모리 모델은 chip-memory, SPICE/아날로그는 chip-analog.
4. 필요한 ID 1개에 `expert_read(ids,sections=["conditions","limits"],context,packs=[같은 팩],max_chars=2400)`을 먼저 적용한다. 절차가 필요할 때만 procedure/verification을 추가한다. source는 read 결과의 sources 배열에 있는 출처 ID만 조회한다. 같은 context와 packs를 유지한다. 실제 설명이 detail에 있으면 detail도 읽는다. 최종 답변에 사용한 본문 ID와 출처 ID를 명시한다.
5. 더 깊은 DRAM 회로 검증은 rtl, HBM 열·패키징은 hbm, NAND ECC는 nand, 제조사 기초 사양은 semiconductor 팩을 명시적으로 선택할 수 있다. 한 번에 모든 팩을 조회하지 않는다.
6. 관측 근거 → 원인 후보 → 대안과 trade-off → 판별/재검증 → 미확인 조건 순으로 답한다. evidence_level과 출처 확인 날짜를 보존한다.

입력 지원: UTF-8 .v/.sv/.svh/.sdc/.upf/.rpt/.log/.csv/.json/.md/.txt/.sp/.spice/.cir, 최대 2 MiB. 이미지/PDF는 Codex에서 필요한 페이지·위치를 별도로 읽고 관련 키워드로 조회한다. GDS/OASIS/바이너리 파형을 직접 해석하지 않는다. 라우팅이 틀리면 명시적 packs 조회로 교정한다.

문자 상한은 응답 JSON 상한이며 모델의 전체 토큰/비용 상한이 아니다. 페르소나는 판단 관점이지 전문가 정확도의 인증이 아니다. 기존 실험은 공개 RTL의 제한된 테스트이며 실제 칩 signoff·실리콘 성능을 증명하지 않는다.
