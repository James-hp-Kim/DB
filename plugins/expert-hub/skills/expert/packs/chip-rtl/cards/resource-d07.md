# YosysHQ AppNote-011 Interpreting results

ID: `chip-rtl:resource-d07` | both | reference-only

assumption이 반례를 가릴 수 있으며 witness cover와 overconstraint 검토가 필요 — PREUNSAT 통과만으로 모든 overconstraint가 제거됐다고 할 수 없음

## conditions

assumption이 반례를 가릴 수 있으며 witness cover와 overconstraint 검토가 필요

## procedure

주장별 근거 또는 학습 자료

## limits

PREUNSAT 통과만으로 모든 overconstraint가 제거됐다고 할 수 없음

## verification

관련 본문 확인; 전체 문헌의 모든 문장 독립 검증 아님. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C09: 보편적 기준이 아니다. 속성이 가정 없이도 참일 수 있다. antecedent/witness reachability와 과도한 제약을 확인한다.
C10: bounded response는 실무 요구사항일 수 있지만 unbounded liveness와 다른 명세다. SBY는 live 모드를 별도로 지원한다.
C15: assumption·parameter·reset·모드·bound·proof status가 허용한 모델 범위의 결과다.

## 출처

- [YosysHQ AppNote-011 Interpreting results](https://yosyshq.readthedocs.io/projects/ap011/en/latest/interpret.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
