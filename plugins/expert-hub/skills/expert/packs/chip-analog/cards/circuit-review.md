# 아날로그·소자·열 검토

ID: `chip-analog:circuit-review` | both | reference-only

소자/공정 모델과 바이어스·부하·PVT·분석 종류를 맞춘 후 후보를 비교한다.

## conditions

netlist·모델·바이어스·입력·부하 및 DC/AC/transient/noise 등의 목적을 확인한다.

## procedure

동작점과 단위·gain 정의부터 확인하고 필요한 sweep/응답/안정성·잡음 분석을 구분한다. 축약 모델은 원본과 오차를 대조하고 대안은 같은 조건으로 재검증한다.

## limits

회로별 실제 실행은 이번 DB 통합에서 수행하지 않았다. 공정 모델 없이 실제 칩 수치를 보장하지 않는다.

## 출처

- [ngspice 47 User's Manual](https://ngspice.sourceforge.io/docs/ngspice-47-manual.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [TI SLOA020A: Stability Analysis of VFB Op Amps](https://www.ti.com/lit/an/sloa020a/sloa020a.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [ADI MT-033: Voltage Feedback Op Amp Gain and Bandwidth](https://www.analog.com/media/en/training-seminars/tutorials/MT-033.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [ADI MT-048: Op Amp Noise Relationships](https://www.analog.com/media/en/training-seminars/tutorials/MT-048.pdf) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [devsim/devsim](https://github.com/devsim/devsim/tree/e3a25f08c7f17cc6932624c12bf9f0f10d7f7cfd) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [uvahotspot/HotSpot](https://github.com/uvahotspot/HotSpot/tree/f18831e48cef5d62580585cca0d7fab6c71bc3cc) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
