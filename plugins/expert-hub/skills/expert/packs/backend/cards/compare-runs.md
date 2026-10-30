# 부하 결과 JSON 비교 도구

ID: `backend:compare-runs` | both | scripts/compare_backend_runs.py; stdlib

정규화된 두 실행 JSON을 비교한다. exit0은 비교 생성,1은 기준/정확성 실패,2는 입력 오류/비교 불가다.

## conditions

schema_version=1, run_id/revision/evidence_ref, context와 metrics가 필요하다. 요청 실패는 union이며 정확성 실패는 그 부분집합이다. 스키마는 backend-comparison 안내를 읽는다.

## procedure

scripts/compare_backend_runs.py baseline.json candidate.json [--limits limits.json]를 로컬 실행한다. 원시 결과에서 값을 추출하고 없는 카운터를 추정하지 않는다. 전체 결과는 저장소 밖 파일로 보존하고 핵심 변경만 대화로 가져온다.

## limits

부하 생성기나 임의 k6 importer가 아니다. 조건 라벨 일치만으로 실제 환경이 같음을 증명하지 않는다. 기준 미지정은 SLO통과가 아니다.

## verification

부하 다름 거부와 빠른 오답 거부를 포함한 동봉 회귀 검사를 실행한다.

## 출처

- [성능 비교·검증 지침](../../../references/backend/performance.md) · authored-workflow · 확인 2026-10-29
- [정규화 실행 비교 코드](../../../scripts/compare_backend_runs.py) · tested-local-code · 확인 2026-10-29
