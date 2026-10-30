# 실험 이력·재현·결과 재사용

ID: `analytics:experiments` | both | reference-only

데이터·설정·코드·환경이 같은 결과를 재사용하고 변경 시 새 실험으로 기록한다.

## conditions

데이터 스냅샷, feature availability, 주지표와 평가 기간이 명시되어야 한다.

## procedure

입력 SHA-256, 설정, 코드 버전/배포 manifest, seed, 라이브러리와 실행시간을 저장한다. 튜닝 중 전체 로그 대신 best/기준모델/실패수/남은 쟁점만 읽는다.

## limits

동봉 profile은 선두 일부를 읽으므로 전체 파일 해시나 캐시를 만들지 않는다. 튜닝의 sampler RNG 상태는 저장되지 않아 재개가 연속 실행과 동일하지 않을 수 있다.

## 출처

- [데이터·매출 확장 설계 및 구현 범위](../../../../../../../docs/DATA_ANALYSIS.md) · package-design · 확인 2026-10-30
