# C11 검토: 1 fF 미만 C·1 Mohm 초과 R를 버린 후에도 원래 회로 검증과 같다

ID: `chip-analog:claim-c11` | both | reference-only

조건부: 탐색용 축약일 수 있으나 등가성·오차를 검증해야 한다. 고임피던스·누설·고주파·누적 기생 영향에 따라 결과가 달라진다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

탐색용 축약일 수 있으나 등가성·오차를 검증해야 한다. 고임피던스·누설·고주파·누적 기생 영향에 따라 결과가 달라진다.

## verification

analog-audit upstream lines149-153. 필터의 영향은 회로 의존이라는 공학적 판단

## limits

1 fF/1 Mohm 필터를 검증 보증으로 해석 금지. Spectre/API·관련 스킬 등 실행 의존성 확인 필요
매뉴얼 전체 기술 정확성을 독립적으로 검증한 것은 아님; 회로에 맞는 모델 필요

## detail

검토한 주장: 1 fF 미만 C·1 Mohm 초과 R를 버린 후에도 원래 회로 검증과 같다
판정: 조건부

## 출처

- [Arcadia-1/analog-agents](https://github.com/Arcadia-1/analog-agents/tree/4d6bd218ceff60624d7ee62887787aa83daecdb4) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [ngspice 47 User's Manual](https://ngspice.sourceforge.io/docs/ngspice-47-manual.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
