# 홀드아웃·선택 편향·중첩 검증

ID: `sales:selection` | both | reference-only

반복 실험에서 가장 좋았던 개발 점수를 최종 일반화 성능으로 보고하지 않는다.

## conditions

독립 최종 평가의 기간 또는 outer folds를 사전에 지정한다.

## procedure

모델·변수·가중치 선택은 개발 구간에서 끝낸다. nested 방식이 필요하면 각 outer train 내부에서 튜닝을 반복한다. 최종 선택 파일과 데이터/설정 식별자를 기록한다.

## limits

동봉 구현은 개발 CV+단일 최종 홀드아웃이다. 파일 경로를 바꿔 재평가하는 것까지 차단하는 보안 장치는 없다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
