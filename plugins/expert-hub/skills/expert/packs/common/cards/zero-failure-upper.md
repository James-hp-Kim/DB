# 실패 0건의 단측 이항 신뢰상한

ID: `common:zero-failure-upper` | both | reference-only; no fab/EDA execution

교육용 식 · 실패 0건의 단측 이항 신뢰상한 · 출력 probability · 실패 0건이며 독립·동일 실패확률인 시행에만 적용. 같은 die의 상관 bit를 독립 표본으로 세지 않음.

## conditions

실패 0건이며 독립·동일 실패확률인 시행에만 적용. 같은 die의 상관 bit를 독립 표본으로 세지 않음.

## procedure

1 - (1-confidence)**(1/trials)

## verification

가상 입력: {"confidence": 0.95, "trials": 1000}
출력 단위: probability; 실측이 아님.

## limits

공개 연구·교육용 근거이며 현행 공정 PDK·제품 규격·보정 모델·실측 검증을 대체하지 않는다. 이 팩은 계산식 참조를 제공하며 실행 계산기를 추가하지 않는다.

## 출처

- [NIST: Proportion confidence intervals](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) · primary · 확인 2026-10-29
