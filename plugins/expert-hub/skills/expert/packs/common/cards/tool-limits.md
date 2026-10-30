# 실행 가능 기능과 참조 전용 기능

ID: `common:tool-limits` | both | reference-only

검색·CSV 진단·WECO/EWMA/CUSUM·선택 PyOD는 실행 가능. DOE·GRR·FMEA·수명 분석은 방법 지침과 Codex 작업으로 제공한다.

## procedure

표준 라이브러리: DB 검색/조회/출처, 페르소나 선택, CSV 품질·중복·MAD·집단 불량률/Wilson·행 빈도 Pareto, 고정 기준의 개별값 WECO/EWMA/CUSUM.
선택 의존성: openpyxl로 지정 XLSX 시트 변환, PyOD로 ECOD/IForest 검토 우선순위.

## limits

참조 전용: GRR 수치 분산분해, p/u/Xbar-R 등 미구현 관리도, Cp/Cpk 자동 판정, DOE 설계 생성, 생존/가속모형 적합, FMEA 정식 평가표, wafer map·FDC 특화 엔진.
참조 전용 기능은 Codex가 데이터·적용판·검증 조건을 확인해 필요한 분석을 작성할 수 있도록 지식을 제공하는 것이다. 이미 검증된 실행기로 오인하지 않는다.
실제 탐지율·전체 토큰·대기업 적합성은 고객 데이터로 평가해야 한다.

## 출처

- [Expert Hub 2.1 설계·구현 범위](../../../references/design.md) · package-design · 확인 2026-10-30
