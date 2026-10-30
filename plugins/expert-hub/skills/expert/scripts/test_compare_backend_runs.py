"""Synthetic checks for the offline comparison contract; no network or load generation."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from compare_backend_runs import compare


def fixture():
    return {
        "schema_version": 1, "run_id": "baseline-fixture", "revision": "fixture-a",
        "evidence_ref": "synthetic-unittest-only",
        "context": {
            "environment": "fixture", "dataset": "fixture-v1", "workload": "fixture-GET",
            "load_model": "open", "offered_load": "100 iterations/s",
            "resources": "fixture-app2-db4", "tool_version": "fixture1",
            "cache_state": "warm", "latency_scope": "all-finalized-attempts",
            "warmup_seconds": 30, "duration_seconds": 60,
        },
        "metrics": {"requests": 6000, "failures": 60, "correctness_failures": 0,
                    "dropped_iterations": 0, "p50_ms": 50, "p95_ms": 200, "p99_ms": 400},
    }


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.before = fixture()
        self.after = copy.deepcopy(self.before)
        self.after.update(run_id="candidate-fixture", revision="fixture-b")

    def test_success_denominator_and_units(self):
        result = compare(self.before, self.after)
        self.assertEqual(result["candidate"]["successful_requests"], 5940)
        self.assertEqual(result["candidate"]["success_rps"], 99)
        self.assertEqual(result["candidate"]["error_rate"], 0.01)
        self.assertEqual(result["candidate_limits"]["status"], "not_evaluated")

    def test_faster_errors_are_not_silently_improvement(self):
        self.after["metrics"].update(failures=1200, p95_ms=100, p99_ms=200)
        result = compare(self.before, self.after)
        self.assertIn("error_rate", result["adverse_directions"])
        self.assertIn("success_rps", result["adverse_directions"])

    def test_changed_context_suppresses_relative_comparison(self):
        for field, value in (("offered_load", "50 iterations/s"), ("resources", "more-cpus"),
                             ("dataset", "other"), ("duration_seconds", 30),
                             ("latency_scope", "success-only"), ("load_model", "closed")):
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.after)
                candidate["context"][field] = value
                result = compare(self.before, candidate)
                self.assertEqual(result["comparison_status"], "not_comparable")
                self.assertEqual(result["changes"], {})

    def test_zero_baseline_has_no_percentage(self):
        self.before["metrics"]["failures"] = 0
        result = compare(self.before, self.after)
        self.assertIsNone(result["changes"]["error_rate"]["percent_change"])

    def test_limits_are_specific_and_do_not_hide_correctness(self):
        self.after["metrics"]["correctness_failures"] = 2
        result = compare(self.before, self.after, {"max_p95_ms": 250})
        self.assertEqual(result["candidate_limits"]["status"], "passed_for_supplied_limits")
        self.assertEqual(result["candidate_correctness"], "failed")

    def test_dropped_iterations_not_added_to_requests(self):
        self.after["metrics"]["dropped_iterations"] = 50
        result = compare(self.before, self.after, {"max_dropped_iterations": 0})
        self.assertEqual(result["candidate"]["error_rate"], 0.01)
        self.assertEqual(result["candidate_limits"]["status"], "failed")
        self.assertIn("dropped_iterations", result["adverse_directions"])

    def test_invalid_counters(self):
        for field, value in (("requests", 0), ("requests", True), ("failures", -1),
                             ("failures", 6001), ("correctness_failures", 61),
                             ("dropped_iterations", 0.5)):
            with self.subTest(field=field, value=value):
                candidate = copy.deepcopy(self.after)
                candidate["metrics"][field] = value
                with self.assertRaises(ValueError):
                    compare(self.before, candidate)

    def test_bad_percentiles(self):
        for value in (float("nan"), float("inf"), None, -1, True, 500):
            with self.subTest(value=value):
                self.after["metrics"]["p95_ms"] = value
                with self.assertRaises(ValueError):
                    compare(self.before, self.after)

    def test_incomplete_or_unknown_context(self):
        for value in (None, "", "unknown"):
            self.after["context"]["dataset"] = value
            with self.assertRaises(ValueError):
                compare(self.before, self.after)

    def test_invalid_limits(self):
        for limits in ({}, {"max_error_rate": 2}, {"bogus": 1}, {"max_p95_ms": True},
                       {"max_dropped_iterations": 1.5}):
            with self.subTest(limits=limits), self.assertRaises(ValueError):
                compare(self.before, self.after, limits)

    def test_duplicate_run_rejected(self):
        with self.assertRaises(ValueError):
            compare(self.before, self.before)

    def test_nonfinite_derived_throughput_rejected(self):
        self.before["context"]["duration_seconds"] = 1e-320
        with self.assertRaises(ValueError):
            compare(self.before, self.after)

    def test_cli_files_hashes_exit_codes_and_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before, after, limits = (root / name for name in ("before.json", "after.json", "limits.json"))
            before.write_text(json.dumps(self.before), encoding="utf-8")
            after.write_text(json.dumps(self.after), encoding="utf-8")
            command = [sys.executable, str(Path(__file__).with_name("compare_backend_runs.py")), str(before), str(after)]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["candidate_limits"]["status"], "not_evaluated")
            self.assertEqual(len(output["input_sha256"]["baseline"]), 64)
            limits.write_text(json.dumps({"max_p95_ms": 100}), encoding="utf-8")
            failed = subprocess.run(command + ["--limits", str(limits)], capture_output=True, text=True, check=False)
            self.assertEqual(failed.returncode, 1, failed.stderr)
            after.write_text("{bad-json", encoding="utf-8")
            invalid = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(invalid.returncode, 2, invalid.stderr)
            self.assertEqual(json.loads(invalid.stdout)["comparison_status"], "invalid_input")


if __name__ == "__main__":
    unittest.main()
