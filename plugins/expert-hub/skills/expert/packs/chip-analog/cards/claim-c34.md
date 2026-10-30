# C34 검토: 증폭기 gain·noise 개선은 숫자 한 개로 판정할 수 있다

ID: `chip-analog:claim-c34` | both | reference-only

조건부: gain 종류, 주파수·부하, noise 적분대역과 시험 조건을 맞춰야 한다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

gain 종류, 주파수·부하, noise 적분대역과 시험 조건을 맞춰야 한다.

## verification

각 문헌의 정의와 범위

## limits

오래된 application note의 일반 원리; 임의 IC/PDK 수치의 직접 근거로 사용 금지
VFB op amp 설명; 모든 증폭기 topology에 그대로 적용하지 않음
적분 대역·noise gain·소스 조건 없이 noise 우열 비교 금지

## detail

검토한 주장: 증폭기 gain·noise 개선은 숫자 한 개로 판정할 수 있다
판정: 조건부

## 출처

- [TI SLOA020A: Stability Analysis of VFB Op Amps](https://www.ti.com/lit/an/sloa020a/sloa020a.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [ADI MT-033: Voltage Feedback Op Amp Gain and Bandwidth](https://www.analog.com/media/en/training-seminars/tutorials/MT-033.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [ADI MT-048: Op Amp Noise Relationships](https://www.analog.com/media/en/training-seminars/tutorials/MT-048.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
