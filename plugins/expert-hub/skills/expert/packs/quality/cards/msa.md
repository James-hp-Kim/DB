# MSA / Gauge R&R: 측정 오차부터 분리

ID: `quality:msa` | both | reference-only

공정 차이로 보이는 현상이 측정기·작업자·측정 조건 차이인지 먼저 확인한다.

## conditions

반복성, 재현성, 편향, 선형성, 안정성, 분해능을 구분한다. 부품·측정자·반복 측정 구조와 실제 공정 범위를 반영해 설계한다.
동일 부품을 모든 측정자가 반복 측정할 수 있는지에 따라 crossed/nested 설계가 달라진다. 파괴시험은 동일 개체 반복을 가정할 수 없다.

## interpretation

%GRR의 분모가 전체 연구 변동인지 공차인지 명시한다. 보고서마다 분모가 다르면 수치만 직접 비교하지 않는다.
통용 임계값을 사내/고객의 일률 합격 기준으로 단정하지 않는다. 해당 측정 목적과 의사결정 위험에 맞는 기준을 확인한다.

## limits

자료가 없으면 MSA를 완료했다고 쓰지 않는다. 현재 분석의 측정 불확실성으로 남기고 시험 계획을 제시한다.

## 출처

- [NIST: Gauge R&R studies](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm) · primary · 확인 2026-10-29
- [RBraga01/Quality-Engineering-Skills: skills/measurement/msa-gauge-rr/SKILL.md](https://github.com/RBraga01/Quality-Engineering-Skills/blob/b338d802a0aa7c6ced8d062dd94e98b5f16030df/skills/measurement/msa-gauge-rr/SKILL.md) · community-source · 확인 2026-10-29
