# CUSUM: 누적 편차로 평균 이동 추적

ID: `quality:cusum` | deep | monitor

기준에서 벗어난 편차를 누적해 작은 변화를 찾는다. k와 h는 탐지할 이동량·오경보 요구에 맞춰 정한다.

## procedure

표준화 관측 u=(x-mu0)/sigma0. Cplus=max(0,Cplus+u-k), Cminus=max(0,Cminus-u-k); 어느 누적량이 h를 넘으면 후보 신호.

## limits

도구 기본 k=0.5, h=5는 예시 설정이다. 이 값만으로 공정별 ARL이나 탐지 성능이 보장되지 않는다.
EWMA·WECO와 함께 모두 실행한 결과를 독립된 증거 3개로 세지 않는다.

## conditions

기준 평균/표준편차는 검증된 정상 상태에서 제공한다. 안정성을 확인하지 않았으면 실행을 보류한다.

## interpretation

신호 뒤 조치·기준 재설정은 사람이 관리하는 OCAP로 정한다. 스크립트는 자동 리셋하지 않아 지속 신호가 여러 행에 나타날 수 있다.

## 출처

- [NIST: CUSUM control charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm) · primary · 확인 2026-10-29
