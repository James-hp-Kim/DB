# AMD UG906: Multi-Bit Synchronizer

ID: `chip-rtl:resource-d04` | both | reference-only

여러 비트의 register synchronizer만으로 bus CDC 안전이 보장되지 않음 — Gray 코드도 적절한 timing constraints와 사용 조건 필요

## conditions

여러 비트의 register synchronizer만으로 bus CDC 안전이 보장되지 않음

## procedure

주장별 근거 또는 학습 자료

## limits

Gray 코드도 적절한 timing constraints와 사용 조건 필요

## verification

관련 본문 확인; 전체 문헌의 모든 문장 독립 검증 아님. 최초 수집 당시 상태이며 후속 PicoRV32 실험은 chip-rtl:public-benchmark.

## detail

C14: bus coherence와 프로토콜을 검토해야 하며 Gray·handshake 등도 사용 조건과 timing constraints가 필요하다.

## 출처

- [AMD UG906: Multi-Bit Synchronizer](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Multi-Bit-Synchronizer) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
