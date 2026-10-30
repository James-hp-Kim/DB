# PicoRV32 공개 검증 결과와 편향

ID: `chip-rtl:public-benchmark` | both | historical-execution; rerun code in optional archive

372회: 정상 설정144/144, 주입 결함6/6 탐지, 복구12/12. 실제 미지 칩 정확도 아님.

## conditions

PicoRV32 ef203c2b0a3fb793280f5114941416c425c5b461; 18 programs × wait0/3, 4 configurations. Icarus14 devel, Yosys0.70+255 Windows.

## interpretation

원문 전체 정확함은 발견한 오류로 성립하지 않는다. 대부분의 반도체 전문가 수준이라는 주장은 입증되지 않았다.

## verification

{"total": 372, "normal": 144, "mutations": 6, "repairs": {"passed": 12, "total": 12}, "additional": {"native_script": {"minus_s_exit": 0, "minus_c_exit": 1, "verdict": "-c interprets Tcl; native .ys needs -s"}, "assumption_counterexample": [{"case": "with_assumption", "result": "PASS", "log": "logs/with_assumption.log"}, {"case": "without_assumption", "result": "PASS", "log": "logs/without_assumption.log"}], "limits": "Small combinational formal counterexample, not a CPU proof or a general vacuity checker.", "upstream_smoke": {"status": "PASS", "write_count": 45, "values": "0..44", "address": 1020, "check": "Original upstream bench; externally checked sequential counter writes. Limited smoke test."}}}

## limits

Author-generated non-blind tests and known injected mutations; NOT an independent diagnostic-accuracy benchmark or skill/no-skill A/B test. No silicon PPA. Same-author oracle and known patches; no blind root-cause accuracy.

## 출처

- [PicoRV32 controlled Windows experiments, 2026-10-29](../../../references/chip-evidence/summary.json) · local-measured-experiment · 확인 2026-10-29 executed; 2026-10-30 imported hash checked
- [Original semiconductor evidence kit archive](../../../../../../../third_party/semiconductor-evidence-20261029.zip) · preserved-local-archive · 확인 2026-10-30 SHA-256 checked
