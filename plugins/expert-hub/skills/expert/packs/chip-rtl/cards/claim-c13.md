# C13 검토: hold violation은 클록 주파수를 낮추면 해결된다

ID: `chip-rtl:claim-c13` | both | reference-only

조건부: 일반적인 같은 edge hold 문제의 보편적 해결책이 아니다. 실제 edge 관계와 arrival/required·skew를 확인한다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

일반적인 같은 edge hold 문제의 보편적 해결책이 아니다. 실제 edge 관계와 arrival/required·skew를 확인한다.

## verification

Requirement 항목: 보통 setup 1 period, hold 0ns; 서로 다른 clock/phase는 별도

## limits

positive slack은 해당 path requirement 충족 의미; 전체 칩 보증 아님

## detail

검토한 주장: hold violation은 클록 주파수를 낮추면 해결된다
판정: 조건부

## 출처

- [AMD UG906: Timing Path Summary](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Timing-Path-Summary-Header-Information) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
