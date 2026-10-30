# AMD UG903: Relaxing Setup While Maintaining Hold

ID: `chip-rtl:resource-d02` | both | reference-only

같은 waveform에서 setup을 늦춘 뒤 원래 hold edge 관계를 복원하는 예시: 2/1, 4/3 — N/N−1은 이 조건의 패턴; 다른 clock 관계에 무조건 적용 금지

## conditions

같은 waveform에서 setup을 늦춘 뒤 원래 hold edge 관계를 복원하는 예시: 2/1, 4/3

## procedure

주장별 근거 또는 학습 자료

## limits

N/N−1은 이 조건의 패턴; 다른 clock 관계에 무조건 적용 금지

## verification

관련 본문 확인; 전체 문헌의 모든 문장 독립 검증 아님. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C05: 동일 waveform에서 원래 hold 관계를 복원하는 일반 패턴은 setup N / hold N−1. 다른 clock·위상·edge·의도는 별도 확인.

## 출처

- [AMD UG903: Relaxing Setup While Maintaining Hold](https://docs.amd.com/r/en-US/ug903-vivado-using-constraints/Relaxing-Setup-While-Maintaining-Hold) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
