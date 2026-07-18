"""Dispatch one Nodus run per trial (goal mode, async). Writes data/manifest.jsonl."""
import json, subprocess, sys, os

AGENT = "50616515-0480-4a67-a498-df56b265fc41"
RES = "https://huggingface.co/datasets/harborframework/terminal-bench-2-leaderboard/resolve/main"

GOAL = """Analyze one Terminal-Bench agent trajectory for wasted time.

Download these two public files (no auth):
- {res}/{trial}/agent/trajectory.json
- {res}/{trial}/result.json

Parse trajectory.json with python. Each step has an ISO `timestamp`; the gap between consecutive steps = command execution wait + generation time of the later step. Look for five kinds of wasted time:

- W1 repeat-slow: a command that took >30s, later re-run in near-identical form when a narrower/cheaper variant existed (full test suite vs one test, full rebuild vs incremental)
- W2 over-wait: tool_calls declaring a `duration` far larger than the command needs (e.g. 30s for ls/cat/echo) — the harness sleeps the full declared duration
- W3 under-wait churn: steps with empty keystrokes "" that only wait longer, each costing an extra model round-trip
- W4 same-error retry: a command re-run unchanged after failing with the same error
- W5 redundant env setup: repeated apt/pip installs, re-downloads, or full re-compiles

Print ONLY this JSON object as your final output (no markdown fence, no prose):
{{"trial": "{trial_short}", "reward": 0, "n_steps": 0, "total_s": 0.0,
 "w1": [], "w2": [], "w3": {{"count": 0, "wasted_s": 0.0}}, "w4": [], "w5": [],
 "wasted_s_total": 0.0, "waste_frac": 0.0, "time_death": false, "note": ""}}

where each item in w1/w2/w4/w5 is {{"cmd": "<=80 chars", "step_ids": [], "wasted_s": 0.0, "why_avoidable": "<=25 words"}}, reward comes from result.json (1 if solved else 0), waste_frac = wasted_s_total/total_s, and time_death = true if the trial failed and >40% of wall-clock went to W1-W5. Fill real values; keep empty lists if none. Be conservative: only claim waste defensible from the data.
"""

def dispatch(trial_path, submission):
    trial_short = trial_path.split("/")[-1]
    goal = GOAL.format(res=RES, trial=trial_path, trial_short=trial_short)
    r = subprocess.run(
        ["nodus", "run", "--agent", AGENT,
         "--instructions", "Complete the goal. Your final message must be only the JSON object.",
         "--goal", goal],
        capture_output=True, text=True, timeout=120)
    try:
        d = json.loads(r.stdout)
        run_id = d["id"] if "id" in d else d["run"]["id"]
    except Exception:
        return {"trial_path": trial_path, "submission": submission, "error": (r.stdout + r.stderr)[-300:]}
    return {"trial_path": trial_path, "submission": submission, "run_id": run_id}

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    trials = [json.loads(l) for l in open("data/trials.jsonl")]
    done = set()
    if os.path.exists("data/manifest.jsonl"):
        done = {json.loads(l)["trial_path"] for l in open("data/manifest.jsonl") if "run_id" in json.loads(l)}
    todo = [t for t in trials if t["trial_path"] not in done]
    if limit: todo = todo[:limit]
    with open("data/manifest.jsonl", "a") as mf:
        for i, t in enumerate(todo):
            rec = dispatch(t["trial_path"], t["submission"])
            mf.write(json.dumps(rec) + "\n")
            mf.flush()
            tag = rec.get("run_id", "ERROR")
            print(f"[{i+1}/{len(todo)}] {t['trial_path'].split('/')[-1]} -> {tag}", flush=True)
