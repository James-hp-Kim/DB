# NAND 오류 원인과 조건별 관측

ID: `nand:error-physics` | both | reference-only

P/E·retention·disturb·온도·층별 편차를 나눠 관측하고 retry/ECC profile과 연결한다.

## conditions

제품 revision·WL·page type과 P/E·시간·온도 조건을 구분한다.

## procedure

| 오류·편차 | 관측해야 할 값 | RTL/firmware 연결

 | P/E cycling 열화 | P/E 수, cycling 온도·dwell 이력, raw error 분포 | 블록 상태·retry/ECC profile 선택

 | retention·초기 retention loss | program 이후 시간, 온도 이력, 초기 수시간의 drift | age bucket·LUT update·refresh 정책 연결

 | read disturb | read 횟수, victim/neighbor 위치, aging | 관측 counter·이동/refresh 요청·시험 오류 주입

 | 층·page type·이웃 간 편차 | WL별 RBER·Vref sweep·조건부 분포 | 층별 보정·LLR LUT·검증 cross coverage

 | program/read 온도 차이 | 두 시점 온도를 각각 기록 | 온도 보정과 이력 만료, sensor 실패 fallback

원인별 효과를 분리하기 위해 같은 P/E count라도 retention·dwell·온도가 다르면 별도 그룹으로 분석한다. 단순 평균 RBER만 보지 않고 상위 오류 꼬리와 codeword별 분포를 확인한다. P02, P03, P15.

## limits

작성한 연구 요약·설계 제안. 원본 보고서의 PDF 확보 설명은 이전 개인 조사 묶음에 해당하며 이 패키지는 요약과 링크만 포함. 내부 사양·실측 데이터·공정 signoff 기준 없음.

## 출처

- [Improving 3D NAND Flash Memory Lifetime by Tolerating Early Retention Loss and Process Variation](https://arxiv.org/abs/1807.05140) · fulltext_key_sections_reviewed · 확인 2026-10-29
- [HeatWatch: Improving 3D NAND Flash Memory Device Reliability by Exploiting Self-Recovery and Temperature-Awareness](https://publications.systems.ethz.ch/publication/1303) · abstract_or_index · 확인 2026-10-29
- [Cycling Condition Impacts on 3D QLC NAND Reliability](https://research.ibm.com/publications/cycling-condition-impacts-on-3d-qlc-nand-reliability) · abstract_or_index · 확인 2026-10-29
