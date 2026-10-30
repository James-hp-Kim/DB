"""Compare normalized, matched performance runs offline (Python standard library)."""

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

CONTEXT_TEXT = (
    "environment", "dataset", "workload", "load_model", "offered_load",
    "resources", "tool_version", "cache_state", "latency_scope",
)
COUNTERS = ("requests", "failures", "correctness_failures", "dropped_iterations")
LATENCIES = ("p50_ms", "p95_ms", "p99_ms")
LIMITS = {
    "max_p95_ms": ("p95_ms", "max"),
    "max_p99_ms": ("p99_ms", "max"),
    "max_error_rate": ("error_rate", "max"),
    "min_success_rps": ("success_rps", "min"),
    "max_dropped_iterations": ("dropped_iterations", "max"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonnegative_number(value, label):
    require(type(value) in (int, float), f"{label}: expected a number, not null/bool/text")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    require(finite and value >= 0, f"{label}: expected a finite nonnegative number")
    return value


def validate_run(run):
    require(isinstance(run, dict), "run must be an object")
    require(type(run.get("schema_version")) is int and run["schema_version"] == 1,
            "schema_version must be 1")
    for field in ("run_id", "revision", "evidence_ref"):
        require(isinstance(run.get(field), str) and run[field].strip(), f"{field}: required text")
    context = run.get("context")
    require(isinstance(context, dict), "context must be an object")
    expected = set(CONTEXT_TEXT) | {"warmup_seconds", "duration_seconds"}
    require(set(context) == expected, "context fields must match the documented schema")
    for field in CONTEXT_TEXT:
        value = context[field]
        require(isinstance(value, str) and value.strip(), f"context.{field}: required text")
        require(value.strip().lower() not in {"unknown", "unset", "tbd", "n/a"},
                f"context.{field}: unresolved context cannot establish comparability")
    require(context["load_model"] in {"open", "closed"}, "load_model must be open or closed")
    nonnegative_number(context["warmup_seconds"], "warmup_seconds")
    require(nonnegative_number(context["duration_seconds"], "duration_seconds") > 0,
            "duration_seconds must be positive")
    metrics = run.get("metrics")
    require(isinstance(metrics, dict), "metrics must be an object")
    require(set(metrics) == set(COUNTERS) | set(LATENCIES),
            "metrics fields must match the documented schema")
    for field in COUNTERS:
        require(type(metrics[field]) is int and metrics[field] >= 0,
                f"metrics.{field}: expected a nonnegative integer")
        nonnegative_number(metrics[field], field)
    require(metrics["requests"] > 0, "requests must be positive; no zero-denominator rate")
    require(metrics["correctness_failures"] <= metrics["failures"] <= metrics["requests"],
            "correctness_failures <= failures <= requests must hold")
    for field in LATENCIES:
        nonnegative_number(metrics[field], field)
    require(metrics["p50_ms"] <= metrics["p95_ms"] <= metrics["p99_ms"],
            "latency percentiles must be nondecreasing")
    return run


def summarize(run):
    metrics = run["metrics"]
    successes = metrics["requests"] - metrics["failures"]
    success_rps = successes / run["context"]["duration_seconds"]
    nonnegative_number(success_rps, "derived success_rps")
    return {
        **metrics,
        "successful_requests": successes,
        "error_rate": metrics["failures"] / metrics["requests"],
        "success_rps": success_rps,
    }


def evaluate_limits(summary, limits):
    if limits is None:
        return {"status": "not_evaluated", "checks": []}
    require(isinstance(limits, dict) and limits, "limits must be a nonempty object")
    require(set(limits) <= set(LIMITS), "unsupported limit name")
    checks = []
    for name, target in limits.items():
        nonnegative_number(target, name)
        if name == "max_error_rate":
            require(target <= 1, "max_error_rate must be a fraction between 0 and 1")
        if name == "max_dropped_iterations":
            require(type(target) is int, "max_dropped_iterations must be an integer")
        metric, direction = LIMITS[name]
        actual = summary[metric]
        passed = actual <= target if direction == "max" else actual >= target
        checks.append({"limit": name, "target": target, "actual": actual, "passed": passed})
    return {
        "status": "passed_for_supplied_limits" if all(c["passed"] for c in checks) else "failed",
        "checks": checks,
    }


def compare(baseline, candidate, limits=None):
    validate_run(baseline)
    validate_run(candidate)
    require(baseline["run_id"] != candidate["run_id"], "run_id must distinguish the two runs")
    before, after = summarize(baseline), summarize(candidate)
    mismatches = [key for key in baseline["context"]
                  if baseline["context"][key] != candidate["context"][key]]
    result = {
        "comparison_status": "not_comparable" if mismatches else "matched_context",
        "context_mismatches": mismatches,
        "baseline": before,
        "candidate": after,
        "candidate_limits": evaluate_limits(after, limits),
        "candidate_correctness": "failed" if after["correctness_failures"] else "no_failures_reported",
        "changes": {},
        "adverse_directions": [],
        "limitations": [
            "User-supplied summaries; labels do not verify raw evidence or resource equality.",
            "One pair of runs does not establish significance, complete SLO compliance, or production readiness.",
            "No automatic overall improvement verdict or deployment authorization.",
        ],
    }
    if mismatches:
        return result
    for metric in (*LATENCIES, "error_rate", "success_rps", "dropped_iterations"):
        delta = after[metric] - before[metric]
        percent = None if before[metric] == 0 else delta / before[metric] * 100
        if percent is not None and not math.isfinite(percent):
            percent = None
        result["changes"][metric] = {
            "before": before[metric], "after": after[metric], "delta": delta,
            "percent_change": percent,
        }
        if (metric == "success_rps" and delta < 0) or (metric != "success_rps" and delta > 0):
            result["adverse_directions"].append(metric)
    return result


def read_json(path):
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8-sig")), hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--limits", type=Path)
    args = parser.parse_args()
    try:
        baseline, baseline_hash = read_json(args.baseline)
        candidate, candidate_hash = read_json(args.candidate)
        limits, limits_hash = read_json(args.limits) if args.limits else (None, None)
        result = compare(baseline, candidate, limits)
        result["input_sha256"] = {"baseline": baseline_hash, "candidate": candidate_hash,
                                  "limits": limits_hash}
    except (ValueError, OSError, UnicodeError, OverflowError) as error:
        print(json.dumps({"comparison_status": "invalid_input", "error": str(error)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    if result["comparison_status"] == "not_comparable":
        return 2
    return int(result["candidate_limits"]["status"] == "failed"
               or result["candidate_correctness"] == "failed")


if __name__ == "__main__":
    sys.exit(main())
