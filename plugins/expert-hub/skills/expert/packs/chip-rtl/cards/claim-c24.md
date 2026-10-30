# C24 검토: OpenSTA로 gate-level STA를 할 수 있다

ID: `chip-rtl:claim-c24` | both | reference-only

문헌 확인: Verilog/Liberty/SDC/SPEF 등 입력을 사용하는 기능이 문서화돼 있다. 제공된 실제 설계로 실행한 것은 아니다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

Verilog/Liberty/SDC/SPEF 등 입력을 사용하는 기능이 문서화돼 있다. 제공된 실제 설계로 실행한 것은 아니다.

## verification

README 지원 입력 목록

## limits

입력·corner·constraint가 필요; signoff 전 영역을 증명하지 않음
실제 실행 버전의 help와 모델·제약 조건을 함께 확인

## detail

검토한 주장: OpenSTA로 gate-level STA를 할 수 있다
판정: 문헌 확인

## 출처

- [The-OpenROAD-Project/OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA/tree/384b539085c54eef46cbaa02e2e17d2b983247e5) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [OpenSTA Documentation](https://opensta.readthedocs.io/en/latest/) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
