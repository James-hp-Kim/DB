# hdl-tools/digital-chip-design-agents

ID: `chip-rtl:resource-s01` | both | reference-only

RTL·STA·합성·물리설계·Formal·검증·메모리 IP 분야별 지침 — 일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님

## conditions

RTL·STA·합성·물리설계·Formal·검증·메모리 IP 분야별 지침

## procedure

교정 지침과 함께 필요한 분야만 참고

## limits

일부 기술 규칙에 오류/과도한 일반화. Codex 경로는 docs/INSTALL.md의 프로젝트 AGENTS 방식도 포함; Claude 플러그인과 동일 기능 보장 아님

## verification

저장소·원문 확인; 이 환경에서 실행/성능 검증 안 함. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C01: 진단 보조 범위는 넓지만 범용 전문가 성능·커버리지 검증이 없다. 과제 입력·도메인·실행 환경별로 평가해야 한다.
C04: 스킬은 작업 지침·관련 자원이다. 도구 설치, 연결, 모델, 라이선스는 별도 확인 대상이다.
C05: 동일 waveform에서 원래 hold 관계를 복원하는 일반 패턴은 setup N / hold N−1. 다른 clock·위상·edge·의도는 별도 확인.
C08: native Yosys 명령 스크립트는 -s를 사용. -c는 Tcl 언어로 작성된 파일일 때 사용.
C09: 보편적 기준이 아니다. 속성이 가정 없이도 참일 수 있다. antecedent/witness reachability와 과도한 제약을 확인한다.
C10: bounded response는 실무 요구사항일 수 있지만 unbounded liveness와 다른 명세다. SBY는 live 모드를 별도로 지원한다.
C36: 문헌상 지원·작성자 테스트 주장·이 환경에서 재현한 실행 결과를 구분한다.

## 출처

- [hdl-tools/digital-chip-design-agents](https://github.com/hdl-tools/digital-chip-design-agents/tree/441cad1ffb4a6c980b82a55374a4d7222a237192) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
