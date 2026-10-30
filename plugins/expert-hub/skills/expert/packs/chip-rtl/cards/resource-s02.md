# K-Dense-AI/scientific-agents

ID: `chip-rtl:resource-s02` | both | reference-only

vlsi-chip-design-engineer: 설계 진단과 PPA·signoff 검토 범위 — 광범위한 텍스트 지침; hold slack 및 Pegasus 표기 교정 필요. 실제 반도체 진단 성능은 미검증

## conditions

vlsi-chip-design-engineer: 설계 진단과 PPA·signoff 검토 범위

## procedure

보조 체크리스트

## limits

광범위한 텍스트 지침; hold slack 및 Pegasus 표기 교정 필요. 실제 반도체 진단 성능은 미검증

## verification

저장소·원문 확인; 이 환경에서 실행/성능 검증 안 함. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C01: 진단 보조 범위는 넓지만 범용 전문가 성능·커버리지 검증이 없다. 과제 입력·도메인·실행 환경별로 평가해야 한다.
C06: 일반적인 setup/recovery는 required−arrival, hold/removal은 arrival−required.
C07: Pegasus Verification System은 Cadence 제품. IC Validator와 공급사를 혼동하지 않는다.

## 출처

- [K-Dense-AI/scientific-agents](https://github.com/K-Dense-AI/scientific-agents/tree/98c7fae46648724e1a43a1f2b207b0c82fcc462e) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
