# C14 검토: 버스 각 비트에 2-FF를 넣으면 CDC가 안전하다

ID: `chip-rtl:claim-c14` | both | reference-only

교정: bus coherence와 프로토콜을 검토해야 하며 Gray·handshake 등도 사용 조건과 timing constraints가 필요하다.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

bus coherence와 프로토콜을 검토해야 하며 Gray·handshake 등도 사용 조건과 timing constraints가 필요하다.

## verification

Multi-Bit Synchronizer 본문

## limits

Gray 코드도 적절한 timing constraints와 사용 조건 필요

## detail

검토한 주장: 버스 각 비트에 2-FF를 넣으면 CDC가 안전하다
판정: 교정

## 출처

- [AMD UG906: Multi-Bit Synchronizer](https://docs.amd.com/r/2024.2-English/ug906-vivado-design-analysis/Multi-Bit-Synchronizer) · primary-reference · 확인 2026-10-29; imported 2026-10-30, not re-crawled
