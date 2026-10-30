# 신뢰성: Weibull·검열·가속 시험

ID: `quality:reliability` | deep | reference-only

고장한 표본뿐 아니라 아직 고장하지 않은 표본과 노출 시간을 포함한다.

## conditions

비수리 제품 수명과 수리 가능한 시스템의 사건 빈도를 구분한다. 시험 종료까지 고장하지 않은 표본은 검열 정보다.
Weibull·lognormal 등 분포 선택은 고장 물리와 적합성으로 판단한다. 고장 건수·시험 조건·검열 방식을 같이 보고한다.
가속 시험은 Arrhenius 등 물리적으로 설명되는 가속 모델과 동일 고장 메커니즘 전제가 필요하다. 높은 스트레스의 전혀 다른 고장을 사용조건으로 외삽하지 않는다.
검열에는 종료시간과 사유를 기록한다. Weibull β는 형상, η는 척도 모수이며 복수 고장 기구에 단일 분포를 강제하지 않는다. Arrhenius 가속인자는 활성화에너지와 절대온도에 의존하며 Ea를 임의로 정하거나 피로에 일괄 적용하지 않는다.

## limits

반도체 패키지/제품별 JEDEC·고객 규격은 실제 적용판을 확인한다. 이 DB에는 유료 규격 전문이나 합격 판정표가 없다.

## verification

고장률 감소·수명 개선 주장은 신뢰구간과 확인시험으로 뒷받침한다.

## 출처

- [NIST: Product reliability](https://www.itl.nist.gov/div898/handbook/apr/apr.htm) · primary · 확인 2026-10-29
- [NIST Censoring](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm) · 웹 응답 보존·본문 대조 필요 · 확인 2026-10-29
- [NIST Weibull distribution](https://www.itl.nist.gov/div898/handbook/apr/section1/apr162.htm) · 웹 응답 보존·본문 대조 필요 · 확인 2026-10-29
- [NIST Arrhenius model](https://www.itl.nist.gov/div898/handbook/apr/section1/apr151.htm) · 웹 응답 보존·본문 대조 필요 · 확인 2026-10-29
- [NIST Reliability projection at use conditions](https://www.itl.nist.gov/div898/handbook/apr/section4/apr43.htm) · 웹 응답 보존·본문 대조 필요 · 확인 2026-10-29
