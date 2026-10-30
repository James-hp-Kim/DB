# PyOD: ECOD·Isolation Forest로 검토 순위 생성

ID: `common:pyod-screen` | deep | anomalies (optional PyOD dependency)

선택한 수치 열을 두 탐지기로 평가해 검토 우선순위를 만든다. 상위 N건은 불량 N건이라는 뜻이 아니다.

## procedure

본 패키지 anomalies 명령은 PyOD classic API의 ECOD와 IForest를 사용하며 seed=42, CPU 1개로 시작한다.
탐지기별 점수는 서로 단위가 다르므로 순위를 결합한다. 동점은 평균 순위로 처리한다.

## conditions

표·수치 데이터에서만 사용한다. ID·범주 숫자·서로 다른 제품·시간 흐름을 무조건 한 행렬에 넣지 않는다. 결측은 자동 대체하지 않는다.

## interpretation

상위 10개 등 검토 예산을 지정해 후보를 반환한다. contamination 기본값이나 상위 비율을 실제 불량률로 보고하지 않는다.

## verification

알려진 이상/정상 사례와 시간 분리 검증으로 임계값·오경보·누락을 평가한 뒤 운영 기준을 정한다. 원본 od-expert의 잘못된 YAML은 활성화하지 않는다.

## 출처

- [yzhao062/pyod: pyod/skills/od_expert/SKILL.md](https://github.com/yzhao062/pyod/blob/7e1330e10ac5c56ed402fbbaa41b225efb4bbc5c/pyod/skills/od_expert/SKILL.md) · community-source · 확인 2026-10-29
- [scikit-learn: Novelty and outlier detection](https://scikit-learn.org/stable/modules/outlier_detection.html) · primary · 확인 2026-10-29
