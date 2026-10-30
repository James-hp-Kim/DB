# 백업 복원과 장애조치 조건

ID: `backend:restore` | both | reference-only

백업 존재와 복원 성공을 구분하고 쓰기 차단·복제 위치·허용 손실을 확인한다.

## conditions

토폴로지, primary/replica 역할, RPO/RTO, 백업 무결성·암호키, 복원 대상과 권한이 필요하다.

## procedure

격리된 대상에서 복원을 검증하고 업무 정합성과 복원 시간을 확인한다. 장애조치에는 원래 주 서버의 쓰기 차단과 새 주 서버 승격 조건을 명시한다.

## limits

동시 writable primary를 만들지 않는다. 이번 합성 SQLite 실험은 HA/DR 또는 실제 복원 검증이 아니다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
