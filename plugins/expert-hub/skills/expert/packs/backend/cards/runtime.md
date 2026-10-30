# 언어·런타임과 서버 환경별 진단

ID: `backend:runtime` | both | reference-only

실제 언어·DB·호스팅·버전을 확인하고 해당 진단 경로만 선택한다.

## conditions

manifest·배포 설정·진행 중 요청·스레드/이벤트루프·GC·워커 수를 확인한다.

## procedure

런타임 대기와 DB/외부 의존성 대기를 분리한다. Kubernetes가 없으면 관련 명령을 전제하지 않는다. Oracle/SQL Server에 PostgreSQL 명령을 적용하지 않는다.

## limits

공개 스킬의 버전 가정으로 기존 프로젝트를 다운그레이드하거나 플랫폼을 바꾸지 않는다.

## 출처

- [백엔드 진단 통합 지침](../../../references/backend/diagnostics.md) · authored-workflow · 확인 2026-10-29
- [Jeffallan backend specialist review](../../../references/backend/sources.md) · reviewed-entrypoints · 확인 2026-10-29
