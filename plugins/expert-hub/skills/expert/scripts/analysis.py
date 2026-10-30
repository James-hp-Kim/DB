"""Bounded CSV diagnostics and monitoring; alerts are leads, not confirmed defects/causes."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from qa_core import VERSION, digest, dump


def read_csv(path, encoding="utf-8-sig", max_rows=200000):
    path = Path(path).resolve()
    if path.suffix.lower() not in (".csv", ".tsv"):
        raise ValueError("Use CSV/TSV; convert XLSX with convert-xlsx first")
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValueError("Input exceeds 100 MiB; partition by comparable product/process/time before analysis")
    text = path.read_text(encoding=encoding)
    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter="\t" if path.suffix.lower() == ".tsv" else ",", strict=True)
    headers = reader.fieldnames
    if not headers or any(not h for h in headers) or len(headers) != len(set(headers)):
        raise ValueError("Headers must be nonempty and unique")
    rows = []
    for number, row in enumerate(reader, 1):
        if number > max_rows:
            raise ValueError(f"Input exceeds {max_rows} records; no partial analysis was returned")
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"Malformed CSV at record {number}")
        rows.append({"record": number, "line_end": reader.line_num, "data": row})
    if not rows:
        raise ValueError("No data records")
    return headers, rows


def numeric(text):
    if not isinstance(text, str) or text.strip().casefold() in ("", "na", "n/a", "null"):
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def require_columns(headers, columns):
    missing = sorted(set(columns) - set(headers))
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))


def wilson(k, n, z=1.959963984540054):
    if n <= 0:
        return None
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return [max(0.0, center - radius), min(1.0, center + radius)]


def scan(path, *, values=(), groups=(), numerator=None, denominator=None,
         numerator_type="units", category=None, encoding="utf-8-sig"):
    if bool(numerator) != bool(denominator):
        raise ValueError("Both numerator and denominator are required")
    if numerator_type not in ("units", "events"):
        raise ValueError("numerator_type must be units or events")
    headers, rows = read_csv(path, encoding)
    require_columns(headers, [*values, *groups, *filter(None, (numerator, denominator, category))])
    findings, warnings, profiles = [], [], {}
    seen = {}
    duplicate_count = 0
    missing = {name: sum(not row["data"][name].strip() for row in rows) for name in headers}
    for row in rows:
        # Exact row identity only; numeric equality and business-key duplication are separate questions.
        key = tuple(row["data"][name] for name in headers)
        if key in seen:
            duplicate_count += 1
            findings.append({"type": "duplicate_candidate", "record": row["record"], "first_record": seen[key], "detail": "Exact repeated record; retained. Confirm sampling/business keys before deduplication."})
        else:
            seen[key] = row["record"]
    for name in values:
        pairs = [(row["record"], numeric(row["data"][name])) for row in rows]
        valid = [(index, value) for index, value in pairs if value is not None]
        invalid = [index for index, value in pairs if value is None]
        for index in invalid:
            findings.append({"type": "missing_or_invalid_numeric", "record": index, "column": name})
        numbers = [value for _, value in valid]
        if not numbers:
            profiles[name] = {"valid": 0, "invalid_or_missing": len(invalid)}
            continue
        median = statistics.median(numbers)
        mad = statistics.median(abs(value - median) for value in numbers)
        profiles[name] = {"valid": len(numbers), "invalid_or_missing": len(invalid), "min": min(numbers), "max": max(numbers), "mean": statistics.mean(numbers), "median": median, "sample_sd": statistics.stdev(numbers) if len(numbers) > 1 else None, "mad": mad}
        if len(numbers) < 8 or mad == 0:
            warnings.append(f"{name}: MAD screen skipped (n<8 or MAD=0); this does not establish absence of anomalies")
        else:
            for index, value in valid:
                robust_z = 0.6744897501960817 * (value - median) / mad
                if abs(robust_z) > 3.5:
                    findings.append({"type": "robust_outlier_candidate", "record": index, "column": name, "value": value, "robust_z": robust_z})
    group_results = []
    if numerator:
        buckets = defaultdict(lambda: {"numerator": 0, "denominator": 0, "records": 0, "invalid_records": [], "zero_denominator_records": []})
        for row in rows:
            key = tuple(row["data"][name] for name in groups)
            bucket = buckets[key]
            bucket["records"] += 1
            k, n = numeric(row["data"][numerator]), numeric(row["data"][denominator])
            valid = k is not None and n is not None and k >= 0 and n >= 0 and k.is_integer() and n.is_integer()
            valid = valid and (k <= n if numerator_type == "units" else n > 0 or k == 0)
            if not valid:
                bucket["invalid_records"].append(row["record"])
                findings.append({"type": "invalid_counts", "record": row["record"], "detail": "Nonnegative integer counts required; units must not exceed inspected units. Group rate withheld."})
                continue
            bucket["numerator"] += int(k)
            bucket["denominator"] += int(n)
            if n == 0:
                bucket["zero_denominator_records"].append(row["record"])
                findings.append({"type": "zero_denominator", "record": row["record"], "detail": "No rate for this record"})
        for key, bucket in buckets.items():
            rate = bucket["numerator"] / bucket["denominator"] if bucket["denominator"] > 0 and not bucket["invalid_records"] else None
            group_results.append({"group": dict(zip(groups, key)) if groups else {"scope": "all supplied records"}, **bucket, "rate": rate, "rate_type": "fraction_nonconforming" if numerator_type == "units" else "defects_per_unit", "ppm": rate * 1000000 if rate is not None and numerator_type == "units" else None, "wilson_95": wilson(bucket["numerator"], bucket["denominator"]) if rate is not None and numerator_type == "units" else None})
        group_results.sort(key=lambda item: (item["rate"] is None, -(item["rate"] or 0)))
    pareto = []
    if category:
        counts = Counter(row["data"][category] or "(missing)" for row in rows)
        cumulative = 0
        for label, count in counts.most_common():
            cumulative += count
            pareto.append({"category": label, "record_count": count, "cumulative_fraction": cumulative / len(rows)})
        warnings.append("Pareto counts records, not summed defect quantities; mutually overlapping defect labels need a separate denominator")
    warnings.append("Screening only. Mixed products, autocorrelation, duplicate sampling and measurement error can generate misleading patterns. No cause is confirmed.")
    return {"analysis": "quick_scan", "records": len(rows), "columns": headers, "missing_cells": missing, "duplicate_candidates": duplicate_count, "numeric_profiles": profiles, "group_rates": group_results, "pareto": pareto, "findings": findings, "warnings": warnings, "evidence_index": "record is 1-based data record, excluding header; CSV physical lines can differ when cells contain newlines"}


def monitor(path, *, value, mean, sigma, order=None, baseline_validated=False,
            ewma_lambda=0.2, cusum_k=0.5, cusum_h=5.0, encoding="utf-8-sig"):
    if not baseline_validated:
        raise ValueError("Confirm baseline stability, measurement adequacy and appropriate independent observations with --baseline-validated")
    if not all(math.isfinite(v) for v in (mean, sigma, ewma_lambda, cusum_k, cusum_h)) or sigma <= 0 or not 0 < ewma_lambda <= 1 or cusum_k <= 0 or cusum_h <= 0:
        raise ValueError("Invalid baseline or monitoring parameters")
    headers, rows = read_csv(path, encoding)
    require_columns(headers, [value] + ([order] if order else []))
    series = [numeric(row["data"][value]) for row in rows]
    if any(item is None for item in series):
        raise ValueError("Monitoring refuses missing/nonfinite observations; resolve gaps without silently joining across them")
    if order:
        order_values = [row["data"][order] for row in rows]
        if any(not item.strip() for item in order_values) or order_values != sorted(order_values) or len(order_values) != len(set(order_values)):
            raise ValueError("Order must be unique ascending ISO-8601 text (consistent timezone/precision); split simultaneous or separate streams first")
    z_scores = [(item - mean) / sigma for item in series]
    findings, trace = [], []
    ewma, positive, negative = mean, 0.0, 0.0
    for index, (observed, z) in enumerate(zip(series, z_scores)):
        rules = []
        if abs(z) > 3:
            rules.append("WECO_1_beyond_3sigma")
        for width, threshold, needed, rule in ((3, 2, 2, "WECO_2_2of3_beyond_2sigma"), (5, 1, 4, "WECO_3_4of5_beyond_1sigma"), (8, 0, 8, "WECO_4_8_same_side")):
            if index + 1 >= width:
                window = z_scores[index + 1 - width:index + 1]
                if sum(v > threshold for v in window) >= needed or sum(v < -threshold for v in window) >= needed:
                    rules.append(rule)
        ewma = ewma_lambda * observed + (1 - ewma_lambda) * ewma
        spread = sigma * math.sqrt(ewma_lambda / (2 - ewma_lambda) * (1 - (1 - ewma_lambda) ** (2 * (index + 1))))
        if abs(ewma - mean) > 3 * spread:
            rules.append("EWMA_3sigma")
        positive = max(0.0, positive + z - cusum_k)
        negative = max(0.0, negative - z - cusum_k)
        if positive > cusum_h or negative > cusum_h:
            rules.append("CUSUM")
        point = {"record": index + 1, "value": observed, "z": z, "ewma": ewma, "ewma_lcl": mean - 3 * spread, "ewma_ucl": mean + 3 * spread, "cusum_positive": positive, "cusum_negative": negative, "rules": rules}
        trace.append(point)
        if rules:
            findings.append({"type": "process_signal", **point})
    return {"analysis": "deep_monitor", "records": len(rows), "baseline": {"mean": mean, "sigma": sigma, "validated": "user_confirmed", "kind": "individual-observation mean/sigma, not subgroup standard error"}, "parameters": {"ewma_lambda": ewma_lambda, "cusum_k": cusum_k, "cusum_h": cusum_h}, "findings": findings, "trace": trace, "warnings": ["Uses fixed baseline and supplied row order. Does not automatically reset limits or stop equipment.", "WECO four-rule family uses 8 same-side points, not Nelson's 9-point rule.", "Multiple monitoring rules increase false alarms. Calibrate the chosen rule family/ARL to the process; these are candidate signals.", "Requires comparable independent individual observations. Autocorrelation, subgroup means, counts and rates need a different model."]}


def anomalies(path, *, values, encoding="utf-8-sig", top=10):
    if not 1 <= top <= 100 or not values:
        raise ValueError("Specify numeric features and top between 1 and 100")
    try:
        import numpy as np
        from pyod.models.ecod import ECOD
        from pyod.models.iforest import IForest
    except ImportError as exc:
        raise ValueError("Optional anomaly dependencies missing: install requirements-anomaly.txt in a project venv") from exc
    headers, rows = read_csv(path, encoding)
    require_columns(headers, values)
    if len(rows) < 20:
        raise ValueError("This exploratory helper requires at least 20 records; use simple diagnostic plots for smaller datasets")
    matrix = [[numeric(row["data"][name]) for name in values] for row in rows]
    if any(v is None for row in matrix for v in row):
        raise ValueError("Resolve missing/nonfinite features explicitly; no silent imputation")
    x = np.asarray(matrix, dtype=float)
    if np.any(np.ptp(x, axis=0) == 0):
        raise ValueError("Remove constant features from the explicit feature list")
    detectors = {"ecod": ECOD(n_jobs=1), "iforest": IForest(n_estimators=100, max_samples=min(256, len(rows)), random_state=42, n_jobs=1)}
    ranked = {}
    for name, detector in detectors.items():
        detector.fit(x)
        scores = np.asarray(detector.decision_scores_, dtype=float)
        if not np.all(np.isfinite(scores)):
            raise ValueError("Detector returned nonfinite scores")
        # Average ranks preserve ties; no arbitrary contamination fraction is reported as defect rate.
        ordered = np.sort(scores)
        ranks = (np.searchsorted(ordered, scores, side="left") + np.searchsorted(ordered, scores, side="right") - 1) / 2
        ranked[name] = ranks / max(1, len(rows) - 1)
    consensus = np.mean(list(ranked.values()), axis=0)
    indices = np.argsort(-consensus, kind="stable")[:min(top, len(rows))]
    findings = [{"type": "review_priority_only", "record": int(index + 1), "rank_percentile": float(consensus[index]), "detector_percentiles": {name: float(scores[index]) for name, scores in ranked.items()}, "features": dict(zip(values, matrix[index]))} for index in indices]
    return {"analysis": "deep_multivariate_screen", "records": len(rows), "features": list(values), "detectors": list(detectors), "findings": findings, "warnings": ["Top-N review priorities always returned; they are not a validated anomaly count, defect rate or calibrated probability.", "Ranks are relative to this dataset. Use independent known cases and a time-separated holdout to choose an operational threshold.", "Treat time series, categorical ids and different product populations separately. These scores do not establish causes."]}


def save_result(result, path, options, out):
    out = Path(out).resolve()
    source = Path(path).resolve()
    fingerprint = hashlib.sha256((digest(source) + dump(options) + VERSION).encode("utf-8")).hexdigest()
    if out.exists():
        existing = out / "result.json"
        if existing.is_file():
            stored = json.loads(existing.read_text(encoding="utf-8"))
            if stored.get("fingerprint") == fingerprint:
                return {"cached": True, "result": stored, "output": str(out)}
        raise FileExistsError("Output directory already exists for other work; choose a new --out directory")
    result = {"version": VERSION, "fingerprint": fingerprint, "input": {"path": str(source), "sha256": digest(source)}, "options": options, **result}
    out.mkdir(parents=True)
    (out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (out / "findings.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["type", "source_data_record", "details_json"])
        for finding in result.get("findings", []):
            detail = dump(finding)
            writer.writerow([finding.get("type"), finding.get("record"), detail])
    return {"cached": False, "result": result, "output": str(out)}


def concise(saved):
    result = saved["result"]
    def preview(value):
        if isinstance(value, str):
            return value if len(value) <= 300 else value[:300] + ' [truncated]'
        if isinstance(value, list):
            items = [preview(item) for item in value[:10]]
            return items if len(value) <= 10 else items + [{"additional_items_in_file": len(value)-10}]
        if isinstance(value, dict):
            items = {key: preview(item) for key, item in list(value.items())[:12]}
            if len(value) > 12:
                items['additional_fields_in_file'] = len(value)-12
            return items
        return value
    return {"analysis": result["analysis"], "records": result["records"], "cached": saved["cached"], "output": saved["output"], "finding_count": len(result.get("findings", [])), "duplicate_candidates": result.get("duplicate_candidates"), "findings_preview": preview(result.get("findings", [])[:10]), "group_rates_preview": preview(result.get("group_rates", [])[:8]), "numeric_profiles_preview": preview(result.get("numeric_profiles", {})), "pareto_preview": preview(result.get("pareto", [])[:10]), "missing_cells_preview": preview({k:v for k,v in result.get("missing_cells", {}).items() if v}), "warnings": preview(result.get("warnings", [])), "more": "Complete evidence is in result.json and findings.csv; previews are bounded."}
