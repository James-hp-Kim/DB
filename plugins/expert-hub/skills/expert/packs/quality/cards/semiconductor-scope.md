# 반도체 품질 분석에 적용할 때의 범위

ID: `quality:semiconductor-scope` | deep | reference-only

wafer·die·LOT·설비·chamber·시간의 계층을 보존한다. 대기업에서 쓰는 기법과 해당 패키지의 도입 실적은 다르다.

## conditions

반도체 자료는 한 LOT의 wafer, wafer 안 die, 장비/chamber, 레시피, 시간의 계층과 공간 패턴을 가질 수 있다. 모든 행을 독립 표본으로 취급하지 않는다.

## limits

wafer map 공간 분석·공정 센서 FDC·가상계측·고장물리별 신뢰성은 각 데이터와 전문 모형이 추가로 필요하다. 본 패키지는 웨이퍼 이미지 판독기나 장비 연결 시스템을 포함하지 않는다.
SK하이닉스 2021년 산업 AI 소개는 SPC와 가상계측 등의 관련성을 설명한다. 이 공개 스킬들의 회사 채택/검증 증거는 아니다.

## verification

실제 현장 적용 전에 측정계, 기준 구간, false alarm, known failure recall, 조사 시간, 개선 검증을 해당 데이터로 평가한다.

## 출처

- [SK hynix: Gauss Labs industrial AI (2021)](https://news.skhynix.com/en/aiming-for-the-top-in-industrial-ai-sks-first-ai-company-gauss-labs/) · primary · 확인 2026-10-29
- [NIST: Variables control charts / WECO](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) · primary · 확인 2026-10-29
- [NIST: Product reliability](https://www.itl.nist.gov/div898/handbook/apr/apr.htm) · primary · 확인 2026-10-29
