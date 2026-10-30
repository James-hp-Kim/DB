# 합성 주문 50만 건의 실제 HTTP 검증

ID: `backend:lab-results` | both | reference-only

첫 실험: p95 145.92~185.87→23.51~25.89ms. 장애80/80실패→재시작80/80성공; 누수 수정 후 재주입 정상.

## conditions

Windows/Python3.14.7/SQLite3.50.4, 주문500,000건, 풀4개, 40요청/초×8초×3회. 공유 PC, OS캐시 미통제.

## procedure

전960건 중1실패, 후960건 중0실패. 예외 경로 finally 반환과 인덱스 추가. 오류4회 재주입 후 가용 연결4, 일반요청80/80성공. HTTP200 오답80/80감지, 부하 불일치 비교 거부.

## limits

가상 데이터·단일 공유 PC의 짧은 기능 검증이다. 이후 별도 재현에서는7/320 시간 초과가 발생했다. 운영 적합성이나 최대 처리 용량이 입증되지 않았다.

## verification

첫 실험 전체 행 논리 해시 보존, integrity_check=ok,7개 서버 종료·포트 닫힘 확인. backend:lab-limit도 함께 확인한다.

## 출처

- [2026-10-29 합성 HTTP/SQLite 첫 실험](../../../evidence/backend-lab/lab-20261029/verification-summary.json) · measured-synthetic · 확인 2026-10-29
