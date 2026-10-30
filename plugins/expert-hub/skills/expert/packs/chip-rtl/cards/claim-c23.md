# C23 검토: OpenROAD 하나만 있으면 어떤 공정이든 RTL-to-GDS가 된다

ID: `chip-rtl:claim-c23` | both | reference-only

근거 부족: standalone application과 전체 flow가 다르고 PDK·library·flow 설정이 필요하다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

standalone application과 전체 flow가 다르고 PDK·library·flow 설정이 필요하다.

## verification

OpenROAD Documentation distinction

## limits

응용프로그램과 전체 RTL-to-GDS flow는 구분; 지원 PDK·도구 구성 필요
프로젝트 목표 runtime/PPA를 모든 설계의 성능 보증으로 해석하지 않음
SK하이닉스의 공정 PDK가 아님; 규칙·수치를 다른 공정에 이식하지 않음

## detail

검토한 주장: OpenROAD 하나만 있으면 어떤 공정이든 RTL-to-GDS가 된다
판정: 근거 부족

## 출처

- [OpenROAD documentation](https://openroad.readthedocs.io/en/latest/) · source_entry · 확인 2026-10-29
- [SkyWater SKY130 PDK documentation](https://skywater-pdk.readthedocs.io/en/main/) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [The-OpenROAD-Project/OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD/tree/82552e4e9180fd5dd0c9cda58273029c83efb146) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
