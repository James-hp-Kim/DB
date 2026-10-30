# Western Electric 4규칙과 Nelson 규칙 구분

ID: `quality:weco-rules` | both | monitor

WECO의 한쪽 연속점 조건은 8점이다. 다른 규칙 체계의 9점 조건과 이름·설정을 혼용하지 않는다.

## procedure

본 패키지에서 사용하는 WECO 4규칙:
1. 중심선 기준 ±3 sigma 밖 1점.
2. 연속 3점 중 같은 쪽 ±2 sigma 밖 2점 이상.
3. 연속 5점 중 같은 쪽 ±1 sigma 밖 4점 이상.
4. 중심선 같은 쪽으로 연속 8점. 정확히 중심선 위 점은 연속을 끊는다.

## conditions

규칙 계열·한계 추정법·관측 단위를 기록한다. sigma는 여기서는 개별 관측 표준편차다. 군평균 관리도라면 표준오차를 별도로 설계해야 한다.

## interpretation

RBraga 원본 스킬의 WECO 표에는 9점 조건이 있어 원전과 불일치한다. 원본은 보관하고 실행 규칙은 이 카드처럼 명시적으로 정정한다.

## limits

여러 규칙을 추가하면 오경보가 늘어난다. 모든 신호가 생산 중단·불량 확정을 뜻하지 않으며 공정 OCAP에 따라 조사한다.

## 출처

- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
- [RBraga01/Quality-Engineering-Skills: skills/measurement/spc-control-charts/SKILL.md](https://github.com/RBraga01/Quality-Engineering-Skills/blob/b338d802a0aa7c6ced8d062dd94e98b5f16030df/skills/measurement/spc-control-charts/SKILL.md) · community-source · 확인 2026-10-29
