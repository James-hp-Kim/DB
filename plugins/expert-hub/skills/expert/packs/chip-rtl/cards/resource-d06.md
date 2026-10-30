# SBY file format reference

ID: `chip-rtl:resource-d06` | both | reference-only

bmc·prove·live·cover 모드와 depth의 의미 구분 — bounded PASS를 unbounded 증명으로 표현하지 않음

## conditions

bmc·prove·live·cover 모드와 depth의 의미 구분

## procedure

주장별 근거 또는 학습 자료

## limits

bounded PASS를 unbounded 증명으로 표현하지 않음

## verification

관련 본문 확인; 전체 문헌의 모든 문장 독립 검증 아님. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C10: bounded response는 실무 요구사항일 수 있지만 unbounded liveness와 다른 명세다. SBY는 live 모드를 별도로 지원한다.
C15: assumption·parameter·reset·모드·bound·proof status가 허용한 모델 범위의 결과다.
C16: lint 범위와 실행한 자극의 결과를 보고한다. 보편 증명으로 확대하지 않는다.

## 출처

- [SBY file format reference](https://yosyshq.readthedocs.io/projects/sby/en/stable/reference.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
