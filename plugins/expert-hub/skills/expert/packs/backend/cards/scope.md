# 백엔드 전문가 페르소나의 기능과 권한

ID: `backend:scope` | both | reference-only

페르소나는 판단 관점이며 DB접속·변경 권한·자격 인증이 아니다. MCP는 선택한 지식을 조회한다.

## conditions

운영 분석에는 실제 코드·자료·관측 도구와 요청 범위가 필요하다.

## procedure

backend-expert 검색으로 얻은 context를 재사용하고 backend+common만 조회한다. 업무 원본은 로컬 계산에 사용하고 명시적 수집 요청 때만 공개 저장소 밖 private로 가져온다.

## limits

운영 DB접속, 지속 감시, 장애 자동 복구, SK하이닉스 내부 자료·채택을 제공/확인한 것이 아니다. 페르소나만 부여해서 토큰 절감이나 전문성이 보장되지 않는다.

## 출처

- [백엔드 진단 통합 지침](../../../references/backend/diagnostics.md) · authored-workflow · 확인 2026-10-29
