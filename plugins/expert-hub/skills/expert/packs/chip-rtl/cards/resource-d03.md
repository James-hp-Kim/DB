# AMD UG906: Timing Path Summary

ID: `chip-rtl:resource-d03` | both | reference-only

setup/recovery slack=required−arrival; hold/removal slack=arrival−required — positive slack은 해당 path requirement 충족 의미; 전체 칩 보증 아님

## conditions

setup/recovery slack=required−arrival; hold/removal slack=arrival−required

## procedure

주장별 근거 또는 학습 자료

## limits

positive slack은 해당 path requirement 충족 의미; 전체 칩 보증 아님

## verification

관련 본문 확인; 전체 문헌의 모든 문장 독립 검증 아님. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C06: 일반적인 setup/recovery는 required−arrival, hold/removal은 arrival−required.
C12: 해당 분석 조건의 결과만 말한다. 다른 corner·mode·제약 누락·LVS·전원 등 요구 범위 확인이 남는다.
C13: 일반적인 같은 edge hold 문제의 보편적 해결책이 아니다. 실제 edge 관계와 arrival/required·skew를 확인한다.
C18: 조건을 고정하거나 차이를 통제한 실험이 필요하다. 단순 수치 차이를 변경의 인과 효과로 표현하지 않는다.

## 출처

- [AMD UG906: Timing Path Summary](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Timing-Path-Summary-Header-Information) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
