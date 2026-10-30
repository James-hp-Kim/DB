# C12 검토: TT에서 positive slack이고 DRC 0이면 최종 signoff 완료

ID: `chip-rtl:claim-c12` | both | reference-only

근거 부족: 해당 분석 조건의 결과만 말한다. 다른 corner·mode·제약 누락·LVS·전원 등 요구 범위 확인이 남는다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

해당 분석 조건의 결과만 말한다. 다른 corner·mode·제약 누락·LVS·전원 등 요구 범위 확인이 남는다.

## verification

scope를 넘는 결론에 대한 교정; DRC0 자체를 부정하는 뜻 아님

## limits

positive slack은 해당 path requirement 충족 의미; 전체 칩 보증 아님
프로젝트 목표 runtime/PPA를 모든 설계의 성능 보증으로 해석하지 않음
패키지 포함 동적 전원 무결성 전체가 검증됐다는 뜻은 아님
SK하이닉스의 공정 PDK가 아님; 규칙·수치를 다른 공정에 이식하지 않음

## detail

검토한 주장: TT에서 positive slack이고 DRC 0이면 최종 signoff 완료
판정: 근거 부족

## 출처

- [AMD UG906: Timing Path Summary](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Timing-Path-Summary-Header-Information) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [OpenROAD documentation](https://openroad.readthedocs.io/en/latest/) · source_entry · 확인 2026-10-29
- [OpenROAD IR Drop Analysis](https://openroad.readthedocs.io/en/latest/main/src/psm/README.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [SkyWater SKY130 PDK documentation](https://skywater-pdk.readthedocs.io/en/main/) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
