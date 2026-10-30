# 디스크 압박과 복제 지연

ID: `backend:disk-lag` | both | reference-only

증가 원인·보존 정책·복제 상태를 확인하고 생산량·용량을 제한적으로 조정한다.

## conditions

디스크 종류별 잔여량, 데이터/로그 증가, 보존 정책, 복제 위치, 백업 상태를 확인한다.

## procedure

비필수 생산자 감속이나 승인된 용량 확장을 검토한다. 장기 트랜잭션·복제 슬롯·보존 설정 등 실제 원인을 좁혀 영구수정한다.

## limits

데이터/WAL 삭제나 무분별한 VACUUM FULL을 임시조치로 실행하지 않는다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
