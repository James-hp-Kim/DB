# 요청 경로별 병목 진단

ID: `backend:request-path` | both | reference-only

트래픽·오류·지연·포화도를 요청 경로와 연결한다. CPU 증가 하나로 DB 원인을 확정하지 않는다.

## conditions

동일 시간대의 LB·애플리케이션·풀·DB/캐시·외부 API 지표가 필요하다.

## procedure

요청 ID로 LB→런타임→풀/큐→DB/의존성 대기를 분리한다. 가장 큰 대기와 최근 변경을 연결하고 경쟁 가설 하나를 구분할 관측만 추가한다.

## limits

관측 공백은 원인 부재의 증거가 아니다. 프로파일링 자체의 CPU·I/O 비용과 표본 편향을 고려한다.

## verification

업무 경로의 응답 정확성·오류 분모·의존 서비스 포화를 함께 확인한다.

## 출처

- [백엔드 진단 통합 지침](../../../references/backend/diagnostics.md) · authored-workflow · 확인 2026-10-29
