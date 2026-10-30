# Data-analysis commands

Resolve paths from this skill folder. Search role with scripts/expert.py catalog "빅데이터" and reuse its context. Profile FILE --columns names --task forecast|sales|quality|general; use --date-column name only for YYYY-MM-DD and --max-rows 0 only for explicit full scans. Default 100000 prefix rows, 12 columns; explicit maximum 30 columns. JSON default max_chars=3500. Omitted columns and incomplete scans are explicit.

Lookup queries: analytics "전처리" / "대용량 메모리" / "Optuna pruning" / "딥러닝 GPU"; sales "백테스트" / "WAPE 분모" / "매출 통화". Pass --packs with the same context to lookup/read/source. Do not read knowledge files directly for ordinary questions.

Baseline: python -B -X utf8 scripts/backtest.py --input examples/synthetic-monthly.csv --config examples/backtest-config.json --out PATH_OUTSIDE_REPOSITORY
Optional ML: python -B -X utf8 scripts/tune.py --input INPUT --config CONFIG --out NEW_OUTPUT --trials 20 --seconds 120. Requires Optuna/scikit-learn/NumPy; repository requirements-forecast.txt records tested direct versions. Installed skill alone: consult source metadata and current official package requirements before installing.
Final evaluation only after selection: scripts/backtest.py --input INPUT --config CONFIG --selection OUTPUT/selection.json --evaluate-holdout --out NEW_FINAL_OUTPUT.

Read [forecasting](forecasting.md) for input restrictions and holdout protocol. Training results are local computation, not knowledge ingestion. No automatic production deployment.
