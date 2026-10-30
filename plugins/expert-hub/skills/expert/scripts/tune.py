"""Budgeted Optuna example: per-series Ridge with recursive lags, on development folds only."""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import math
import sys
import time
from pathlib import Path
import optuna
import backtest as bt

SEARCH_VERSION = "ridge-lags-v1"


def tune(input_path, config_path, output, trials=20, seconds=120, seed=42, resume=False):
    if trials < 1 or seconds <= 0: raise ValueError("Positive trials and seconds required")
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    calendar,panel = bt.load_panel(input_path,config["frequency"])
    bt.validate_config(config,len(calendar))
    folds,_ = bt.make_folds(len(calendar),config)
    min_length = min(f["train_end"]-f["train_start"] for f in folds)
    lag_choices = [x for x in (3,6,12,24) if x+3 <= min_length]
    if not lag_choices: raise ValueError("Insufficient training observations for this search space")
    signature = bt.provenance(input_path,config)
    versions = {name:importlib.metadata.version(name) for name in ("optuna","scikit-learn","numpy")}
    contract = {"provenance":signature,"seed":seed,"search_version":SEARCH_VERSION,"lag_choices":lag_choices,"versions":versions}
    if output.exists():
        if not resume: raise ValueError("Output exists. Use --resume only for the same input/config/search/version")
        previous=json.loads((output/"contract.json").read_text(encoding="utf-8"))
        if previous != contract: raise ValueError("Study contract changed; use a new output directory")
    else:
        if resume: raise ValueError("No study to resume")
        output.mkdir(parents=True)
        bt.write_json(output/"contract.json",contract)
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study=optuna.create_study(study_name="sales-ridge", storage="sqlite:///"+str((output/"study.sqlite").resolve()).replace("\\","/"),
        load_if_exists=resume,direction="minimize",sampler=optuna.samplers.TPESampler(seed=seed),
        pruner=optuna.pruners.MedianPruner(n_startup_trials=5,n_warmup_steps=1))
    def objective(trial):
        model={"name":"ridge","alpha":trial.suggest_float("alpha",1e-4,1e4,log=True),"lags":trial.suggest_categorical("lags",lag_choices)}
        rows=[]
        for i,fold in enumerate(folds):
            rows.extend(bt.evaluate(calendar,panel,[fold],model,config))
            value=bt.score_rows(rows)[config["metric"]]
            if value is None or not math.isfinite(value): raise ValueError("Undefined optimization objective")
            trial.report(value,i)
            if trial.should_prune(): raise optuna.TrialPruned()
        return value
    started=time.monotonic()
    study.optimize(objective,n_trials=trials,timeout=seconds,n_jobs=1)
    completed=[t for t in study.trials if t.state==optuna.trial.TrialState.COMPLETE]
    if not completed: raise ValueError("No completed trial; no model selected")
    candidate={"name":"ridge",**study.best_params}
    candidate_rows=bt.evaluate(calendar,panel,folds,candidate,config)
    candidate_metrics=bt.score_rows(candidate_rows)
    baseline,ranked,_=bt.baseline_selection(calendar,panel,config)
    baseline_score=ranked[0]["metrics"][config["metric"]]
    improved=study.best_value < baseline_score
    selected=candidate if improved else baseline
    bt.write_json(output/"selection.json",{"model":selected,"provenance":signature,"stage":"development_only","versions":versions})
    bt.write_rows(output/"candidate-predictions.csv",candidate_rows)
    trial_rows=[{"trial":t.number,"state":t.state.name,"value":t.value,"alpha":t.params.get("alpha"),"lags":t.params.get("lags")} for t in study.trials]
    bt.write_rows(output/"trials.csv",trial_rows)
    result={"stage":"development_only","holdout_evaluated":False,"best_ridge":candidate,"ridge_metrics":candidate_metrics,
            "baseline_ranking":ranked,"selected":selected,"ridge_beats_baseline_on_development":improved,
            "trial_count":len(study.trials),"completed_trials":len(completed),"elapsed_seconds":round(time.monotonic()-started,3),
            "budget_note":"Optuna timeout is checked between trials; a running trial and final diagnostics may exceed it. Not a hard process deadline.",
            "resume_note":"Trial history resumes. Sampler RNG state is not persisted, so a resumed run need not match an uninterrupted run.",
            "contract":contract}
    bt.write_json(output/"report.json",result)
    return {k:result[k] for k in ("stage","holdout_evaluated","selected","trial_count","elapsed_seconds")}


if __name__ == "__main__":
    if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True); p.add_argument("--config",type=Path,required=True); p.add_argument("--out",type=Path,required=True)
    p.add_argument("--trials",type=int,default=20);p.add_argument("--seconds",type=float,default=120);p.add_argument("--seed",type=int,default=42);p.add_argument("--resume",action="store_true")
    a=p.parse_args()
    try: print(json.dumps(tune(a.input,a.config,a.out,a.trials,a.seconds,a.seed,a.resume),ensure_ascii=False))
    except (ValueError,OSError,KeyError) as exc:
        print(str(exc),file=sys.stderr);raise SystemExit(2)
