# C15 검토: formal PASS는 어떤 동작 조건에서도 옳다는 뜻이다

ID: `chip-rtl:claim-c15` | both | reference-only

조건부: assumption·parameter·reset·모드·bound·proof status가 허용한 모델 범위의 결과다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

assumption·parameter·reset·모드·bound·proof status가 허용한 모델 범위의 결과다.

## verification

Options / overconstraint

## limits

bounded PASS를 unbounded 증명으로 표현하지 않음
PREUNSAT 통과만으로 모든 overconstraint가 제거됐다고 할 수 없음

## detail

검토한 주장: formal PASS는 어떤 동작 조건에서도 옳다는 뜻이다
판정: 조건부

## 출처

- [SBY file format reference](https://yosyshq.readthedocs.io/projects/sby/en/stable/reference.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [YosysHQ AppNote-011 Interpreting results](https://yosyshq.readthedocs.io/projects/ap011/en/latest/interpret.html) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
