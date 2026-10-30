# DOE: 상호작용을 포함한 개선 실험

ID: `common:doe` | deep | reference-only

후보 인자를 선별하고, 상호작용·곡률을 확인하며, 확인 실험으로 개선을 검증한다.

## conditions

목표 Y, 인자와 수준, 허용 공정 범위, 실험 단위를 정의한다. 측정계·공정 안정성·실험 순서를 검토한다.

## procedure

인자가 많으면 screening/fractional factorial 등으로 좁히고, 별칭/교락 구조를 명시한다. 블록·무작위화·반복으로 시간/LOT 영향을 다룬다.
곡률과 최적화가 목적이면 response surface 등 후속 설계를 선택한다. 한 번에 한 인자만 바꾸면 상호작용을 놓칠 수 있다.

## verification

모형 적합 후 잔차·적합 부족·외삽을 확인한다. 최적점은 새 조건의 확인 실험으로 평가한다.

## limits

도구는 계획과 코드 초안을 지원한다. 실제 설비 설정 변경·재료 투입·생산 조건 변경에는 사용자 권한과 현장 절차가 필요하다.

## 출처

- [NIST: Process improvement / DOE](https://www.itl.nist.gov/div898/handbook/pri/pri.htm) · primary · 확인 2026-10-29
