# C19 검토: 파이프라인을 추가하면 동일 동작이면서 성능만 좋아진다

ID: `chip-rtl:claim-c19` | both | reference-only

조건부: latency·throughput·handshake·feedback·reset 계약을 다시 검증해야 한다. 효과는 설계 의존.

## conditions

원문 주장 검토이며 모든 칩에 적용하는 규칙이 아니다. 아래 해석의 조건과 원본 도구/모델 범위를 확인한다.

## interpretation

latency·throughput·handshake·feedback·reset 계약을 다시 검증해야 한다. 효과는 설계 의존.

## verification

제공 인터페이스/구성별 동작 설명에 기반한 설계 검토 원칙

## limits

발췌 파일만 확보; 완전한 빌드 프로젝트 아님. 저자의 검증/tapeout 서술은 이번 실행 증거 아님
README에 active development 종료 명시. 발췌 TB는 추가 firmware/환경 의존; 바로 실행 가능한 전체 프로젝트 아님

## detail

검토한 주장: 파이프라인을 추가하면 동일 동작이면서 성능만 좋아진다
판정: 조건부

## 출처

- [lowRISC/ibex](https://github.com/lowRISC/ibex/tree/c0c07085791e4d16a0f2d9a753b2fb79d72e5ffa) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
- [YosysHQ/picorv32](https://github.com/YosysHQ/picorv32/tree/ef203c2b0a3fb793280f5114941416c425c5b461) · public-repository · 확인 2026-10-29; imported 2026-10-30, not re-crawled
