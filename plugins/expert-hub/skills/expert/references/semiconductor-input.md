# Semiconductor input routing

Use `semiconductor-basics` / 반도체기초전문가 for physics, devices, memory, leakage, power/area and introductory process/package questions. Start with semiconductor only. Add common for statistical definitions; add nand for NAND controller/ECC depth only when needed.

Ask only for missing variables that change interpretation: structure/product revision, metric/unit, voltage, temperature, comparison baseline, population/denominator, measurement floor and constraints. Ioff, storage charge loss and chip standby current are different metrics. Unknown values stay unknown; below detection is not zero.

For an explicitly supplied UTF-8 CSV/JSON/text/report file, run relative to this skill:

```powershell
python -B -X utf8 scripts/semiconductor_reference.py '<user-file>' --context '<catalog-context>' --max-chars 2500
```

The file is read locally, at most 2 MiB. Only topic hints, up to 3 row locations per topic, file hash and short scoped DB results return. It does not validate numerical measurements, infer causality, compile RTL or ingest data. A comment/column name also matches. No topic: add an explicit `--query 'question keywords'`. Do not read a whole file into the conversation just because routing found no keyword. Inspect a bounded excerpt or compute a local summary when needed for analysis.

Select 1–2 relevant result IDs. Read conditions and limits, then only the procedure/verification needed to distinguish hypotheses; retrieve source metadata for citations. Keep numerical units, study generations, measured-vs-assumed status and counterevidence. Reuse evidence already read. Report observation, hypothesis, improvement tradeoff, falsifying check and missing evidence separately.

Knowledge provenance: public research snapshot dated 2026-10-29, migrated on 2026-10-30. Educational calculations, authored field definitions and job-learning schedules are not fab specifications. The 151 semiconductor records and common:zero-failure-upper preserve the prior 152 non-source records; source cards are deduplicated in the shared registry. No fab/EDA execution or new live source review occurred during migration.

For persona questions, apply [semiconductor evidence](semiconductor-evidence.md), including substantive sections, actual source IDs, claim-level attribution and the C–V terminology check.
