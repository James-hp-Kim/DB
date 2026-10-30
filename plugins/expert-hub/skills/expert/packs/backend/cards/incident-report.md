# 장애 기록과 영구수정 인수인계

ID: `backend:incident-report` | both | reference-only

영향·시간대·근거·실행 조치·검증 결과와 남은 작업을 구분해 기록한다.

## conditions

사건 시작/탐지/조치/복구 시각, 업무 영향과 실패 분모, 변경 이력·관측 위치가 필요하다.

## procedure

안정화 조치와 원인 수정의 상태를 분리한다. 관찰→가설→검증된 원인→수정→재발 관측을 연결하고 다음 담당/검증 기준을 남긴다.

## limits

진행 중 조치를 완료라고 쓰지 않는다. green health 하나로 업무 정상화나 영구해결을 선언하지 않는다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
- [Incident runbook/postmortem skills](https://github.com/wshobson/agents/tree/main/plugins/incident-response/skills) · reviewed-entrypoint · 확인 2026-10-29
