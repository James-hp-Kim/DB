# 트래픽 급증과 과부하 대응

ID: `backend:overload` | both | reference-only

유입률·처리율·거부율·포화를 구분한다. 하위 시스템 여유 없이 앱 증설만 하지 않는다.

## conditions

업무 우선순위와 기존 유입 제한, 큐 상한, 서비스/DB 병목, 유실 허용 여부가 필요하다.

## procedure

원인에 따라 비필수 생산자 감속, 기존 유입/동시성 제한, 기능 축소 또는 근거 있는 증설을 한정 적용한다. open arrival 시험에서 증가→지속→회복을 구분하고 생성기 한계를 기록한다.

## limits

거부한 업무를 빼고 성공 처리량 증가라고 주장하지 않는다. 무한 큐·재시도는 회복을 늦출 수 있다.

## verification

거부/오류 건수와 분모, backlog, 업무 지연, 하위 시스템 포화·회복 시간을 확인한다.

## 출처

- [장애 안정화·영구수정 지침](../../../references/backend/incident-response.md) · authored-workflow · 확인 2026-10-29
- [Google SRE handling overload](https://sre.google/sre-book/handling-overload/) · primary-reference · 확인 2026-10-29
