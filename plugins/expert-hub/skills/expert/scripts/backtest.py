"""Leakage-aware reference backtest: aligned daily/month-start CSV, baselines and optional Ridge."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ENGINE_VERSION = "1.0.0"


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def next_date(d, frequency):
    if frequency == "D": return d + timedelta(days=1)
    return date(d.year + (d.month == 12), d.month % 12 + 1, 1)


def load_panel(path: Path, frequency: str):
    if frequency not in {"D", "MS"}: raise ValueError("Only D and MS are supported by this reference runner")
    groups = defaultdict(dict)
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not {"unique_id", "ds", "y"} <= set(reader.fieldnames or []):
            raise ValueError("Required CSV columns: unique_id,ds,y")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Duplicate CSV column names")
        for line, row in enumerate(reader, 2):
            key = row["unique_id"]
            if not key or key != key.strip(): raise ValueError(f"Invalid series ID at row {line}")
            try:
                day = date.fromisoformat(row["ds"])
                value = float(row["y"])
            except (ValueError, TypeError) as exc:
                raise ValueError(f"Invalid date or missing/non-numeric y at row {line}") from exc
            if not math.isfinite(value): raise ValueError(f"Non-finite y at row {line}")
            if frequency == "MS" and day.day != 1: raise ValueError("MS dates must be first day of month")
            if day in groups[key]: raise ValueError(f"Duplicate key at row {line}: {key}/{day}")
            groups[key][day] = value
    if not groups: raise ValueError("Empty dataset")
    calendar = sorted(next(iter(groups.values())))
    for a, b in zip(calendar, calendar[1:]):
        if b != next_date(a, frequency): raise ValueError(f"Missing time period between {a} and {b}; resolve explicitly")
    result = {}
    for key, values in sorted(groups.items()):
        if sorted(values) != calendar: raise ValueError(f"Series {key} is not calendar-aligned; this runner does not silently fill/drop rows")
        result[key] = [values[d] for d in calendar]
    return calendar, result


def validate_config(config, n):
    allowed = {"frequency", "horizon", "gap", "season_length", "min_train", "n_windows", "step", "train_window", "holdout_periods", "metric", "reference_model", "scope", "unit"}
    if set(config) - allowed: raise ValueError("Unknown config keys: " + str(set(config) - allowed))
    for key in ("horizon", "season_length", "min_train", "n_windows", "step", "holdout_periods"):
        if type(config.get(key)) is not int or config[key] < 1: raise ValueError(f"{key} must be a positive integer")
    if type(config.get("gap")) is not int or config["gap"] < 0: raise ValueError("gap must be a nonnegative integer")
    if config["holdout_periods"] != config["horizon"]: raise ValueError("Reference runner requires one terminal holdout equal to horizon")
    if config["metric"] not in {"mae", "wape"}: raise ValueError("metric must be mae or wape")
    if config["reference_model"] not in {"naive", "seasonal_naive"}: raise ValueError("Unsupported reference_model")
    if not config.get("scope") or not config.get("unit"): raise ValueError("Specify scope and unit, e.g. synthetic / arbitrary units")
    window = config.get("train_window")
    if window is not None and (type(window) is not int or window < config["min_train"]): raise ValueError("train_window must be null or >= min_train")
    if config["min_train"] < max(2, config["season_length"]): raise ValueError("min_train must cover season_length and at least two points")
    make_folds(n, config)


def make_folds(n, c):
    # Nothing at or after final_train_end participates in tuning.
    final_train_end = n - c["holdout_periods"] - c["gap"]
    last_end = final_train_end - c["gap"] - c["horizon"]
    ends = [last_end - c["step"] * i for i in reversed(range(c["n_windows"]))]
    if not ends or ends[0] < c["min_train"]: raise ValueError("Insufficient history for configured backtests and untouched holdout")
    folds = []
    for index, end in enumerate(ends):
        start = max(0, end - c["train_window"]) if c.get("train_window") else 0
        folds.append({"fold": index, "train_start": start, "train_end": end,
                      "test_start": end + c["gap"], "test_end": end + c["gap"] + c["horizon"]})
    holdout = {"fold": "holdout", "train_start": max(0, final_train_end - c["train_window"]) if c.get("train_window") else 0,
               "train_end": final_train_end, "test_start": n - c["holdout_periods"], "test_end": n}
    return folds, holdout


def predict(train, steps, model):
    name = model["name"]
    if name == "naive": return [train[-1]] * steps
    if name == "seasonal_naive":
        season = model["season_length"]
        if len(train) < season: raise ValueError("Seasonal history unavailable")
        return [train[-season + i % season] for i in range(steps)]
    if name == "mean": return [sum(train) / len(train)] * steps
    if name == "drift":
        slope = (train[-1] - train[0]) / (len(train) - 1)
        return [train[-1] + slope * (i + 1) for i in range(steps)]
    if name == "ridge":
        from sklearn.linear_model import Ridge
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        lags = model["lags"]
        if len(train) <= lags + 2: raise ValueError("Not enough observations for Ridge lag features")
        x = [train[i-lags:i] for i in range(lags, len(train))]
        y = train[lags:]
        estimator = make_pipeline(StandardScaler(), Ridge(alpha=model["alpha"]))
        estimator.fit(x, y)
        history = list(train)
        result = []
        for _ in range(steps):
            value = float(estimator.predict([history[-lags:]])[0])
            history.append(value); result.append(value)
        return result
    raise ValueError(f"Unsupported model: {name}")


def score_rows(rows):
    if not rows: raise ValueError("No scored observations")
    n = len(rows)
    abs_error = sum(abs(r["prediction"] - r["actual"]) for r in rows)
    denom = sum(abs(r["actual"]) for r in rows)
    bias_sum = sum(r["prediction"] - r["actual"] for r in rows)
    scaled = [abs(r["prediction"] - r["actual"]) / r["mase_scale"] for r in rows if r["mase_scale"] is not None and r["mase_scale"] > 0]
    return {"mae": abs_error/n, "rmse": math.sqrt(sum((r["prediction"]-r["actual"])**2 for r in rows)/n),
            "wape": 100*abs_error/denom if denom else None, "bias": bias_sum/n,
            "bias_pct": 100*bias_sum/denom if denom else None,
            "mase": sum(scaled)/len(scaled) if scaled else None, "mase_defined_n": len(scaled),
            "n": n, "absolute_actual_sum": denom, "absolute_error_sum": abs_error,
            "series_count": len({r["unique_id"] for r in rows}), "origin_count": len({r["origin"] for r in rows}),
            "unique_targets": len({(r["unique_id"],r["ds"]) for r in rows})}


def evaluate(calendar, panel, folds, model, config):
    rows = []
    for fold in folds:
        for key, values in panel.items():
            train = values[fold["train_start"]:fold["train_end"]]
            steps = fold["test_end"] - fold["train_end"]
            predictions = predict(train, steps, model)
            season = config["season_length"]
            differences = [abs(a-b) for a,b in zip(train[season:], train[:-season])]
            scale = sum(differences)/len(differences) if differences else None
            for i in range(fold["test_start"], fold["test_end"]):
                prediction = predictions[i-fold["train_end"]]
                if not math.isfinite(prediction): raise ValueError("Model produced a non-finite forecast")
                rows.append({"unique_id":key,"ds":calendar[i].isoformat(),"fold":fold["fold"],
                    "origin":calendar[fold["train_end"]-1].isoformat(),"lead":i-fold["train_end"]+1,
                    "actual":values[i],"prediction":prediction,"model":model["name"],"mase_scale":scale})
    return rows


def diagnostics(rows):
    result = {"overall": score_rows(rows)}
    for field in ("unique_id", "lead", "origin"):
        groups = defaultdict(list)
        for row in rows: groups[str(row[field])].append(row)
        result["by_"+field] = {key:score_rows(value) for key,value in groups.items()}
    return result


def provenance(path, config):
    return {"input_sha256":hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            "config_sha256":canonical_hash(config), "engine_version":ENGINE_VERSION}


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def write_rows(path, rows):
    with Path(path).open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def baseline_selection(calendar, panel, config):
    folds, _ = make_folds(len(calendar), config)
    models = [{"name":"naive"},{"name":"seasonal_naive","season_length":config["season_length"]},{"name":"mean"},{"name":"drift"}]
    results = []
    all_rows = []
    for model in models:
        rows = evaluate(calendar, panel, folds, model, config)
        results.append({"model":model,"metrics":score_rows(rows)})
        all_rows.extend(rows)
    def objective(r):
        value = r["metrics"][config["metric"]]
        return math.inf if value is None else value
    results.sort(key=objective)
    if not math.isfinite(objective(results[0])): raise ValueError("Objective undefined; choose a suitable metric before tuning")
    return results[0]["model"], results, all_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--evaluate-holdout", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8-sig"))
    calendar, panel = load_panel(args.input, config["frequency"])
    validate_config(config, len(calendar))
    signature = provenance(args.input, config)
    if args.evaluate_holdout:
        if not args.selection: raise ValueError("Freeze a selection first, then explicitly evaluate the holdout")
        selected = json.loads(args.selection.read_text(encoding="utf-8"))
        if selected["provenance"] != signature: raise ValueError("Input/config/engine changed since model selection")
        _, holdout = make_folds(len(calendar), config)
        ref = {"name":config["reference_model"]}
        if ref["name"] == "seasonal_naive": ref["season_length"] = config["season_length"]
        models = [selected["model"]] + ([] if selected["model"] == ref else [ref])
        scored = [(m, evaluate(calendar,panel,[holdout],m,config)) for m in models]
        args.out.mkdir(parents=True, exist_ok=False)
        result = {"stage":"final_holdout_consumed", "provenance":signature, "config":config,
                  "results":[{"model":m,"diagnostics":diagnostics(rows)} for m,rows in scored],
                  "note":"Do not retune using these outcomes and call this period untouched again. This runner does not enforce a cross-directory holdout registry."}
        write_rows(args.out/"predictions.csv", [r for _,rows in scored for r in rows])
    else:
        if args.selection: raise ValueError("--selection is only valid with --evaluate-holdout")
        model, ranking, rows = baseline_selection(calendar,panel,config)
        args.out.mkdir(parents=True, exist_ok=False)
        write_json(args.out/"selection.json", {"model":model,"provenance":signature,"stage":"development_only"})
        write_rows(args.out/"predictions.csv",rows)
        result = {"stage":"development_only", "provenance":signature,"config":config,"ranking":ranking,
                  "folds":make_folds(len(calendar),config)[0], "holdout_evaluated":False,
                  "diagnostics":diagnostics([r for r in rows if r["model"] == model["name"]])}
    result["python_version"] = platform.python_version()
    result["evaluation_unit"] = "series x forecast-origin x lead; overlapping targets are repeated forecast decisions"
    result["negative_actual_count"] = sum(v < 0 for series in panel.values() for v in series)
    write_json(args.out/"report.json", result)
    print(json.dumps({"stage":result["stage"],"output":str(args.out),"holdout_evaluated":args.evaluate_holdout}, ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    try: main()
    except (ValueError,OSError,KeyError) as exc:
        print(str(exc),file=sys.stderr); raise SystemExit(2)
