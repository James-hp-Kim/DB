# Cp·Cpk와 Pp·Ppk 해석

ID: `quality:capability` | deep | reference-only

관리 안정성·규격·분포·군구분을 확인한 뒤 공정능력을 해석한다. Cpk와 Ppk의 산포 추정법을 구별한다.

## procedure

Cp=(USL-LSL)/(6*sigma_within), Cpk=min((USL-mu)/(3*sigma_within),(mu-LSL)/(3*sigma_within)). Pp/Ppk는 전체 표준편차를 사용한다.

## interpretation

규격한계는 고객·설계 요구, 관리한계는 공정 변동의 통계 기준이다. 둘을 바꿔 쓰지 않는다.
1.33/1.67 등은 모든 산업·특성에 공통인 합격 기준이 아니다. 적용 규격/고객 요구/특성의 위험을 확인한다.

## limits

불안정 공정의 지수를 장래 보증 수치로 제시하지 않는다. 비정규·한쪽 규격·자기상관이면 적절한 방법과 신뢰구간을 정한다.

## verification

표본수·기간·MSA·군 내 sigma 추정법·전체 sigma·불확실성을 함께 남긴다. 이 패키지에는 자동 합격 판정 기능이 없다.

## 출처

- [NIST: Process capability](https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm) · primary · 확인 2026-10-29
- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
