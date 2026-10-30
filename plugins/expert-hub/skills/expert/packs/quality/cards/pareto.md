# Pareto: 불량 집중과 개선 우선순위

ID: `quality:pareto` | quick | scan --category

동일 집계 기준의 불량 유형을 정렬한다. 빈도, 비용, 심각도는 서로 다른 우선순위다.

## conditions

사용: 어떤 불량 유형·공급사·설비부터 살펴볼지 빠르게 좁힐 때.

## procedure

분석 범위와 분모를 고정하고 유형별 건수와 누적 비중을 계산한다. 생산량이 다르면 불량 건수와 불량률을 함께 비교한다.

## limits

scan --category는 행 개수를 센다. 이미 집계된 불량수 열의 합계가 아니므로 집계 파일이면 별도 합산이 필요하다.
여러 불량명이 한 행에 중복 태깅된 경우 누적 비율의 분모를 재정의한다.

## interpretation

빈도가 낮아도 안전·핵심 기능에 큰 영향을 주는 항목은 별도 우선순위로 제시한다. 80/20 비율을 맞추려고 항목을 꾸미지 않는다.

## 출처

- [RBraga01/Quality-Engineering-Skills: skills/problem-solving/dmaic/SKILL.md](https://github.com/RBraga01/Quality-Engineering-Skills/blob/b338d802a0aa7c6ced8d062dd94e98b5f16030df/skills/problem-solving/dmaic/SKILL.md) · community-source · 확인 2026-10-29
- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
