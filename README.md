# TempO — Temporal Observability for Coding Agents

Phase 1: mine Terminal-Bench 2.0 leaderboard trajectories for wasted tool-call time
(W1 repeat-slow, W2 over-wait, W3 under-wait churn, W4 same-error retry, W5 redundant env setup).

- `scripts/enumerate_trials.py` — pick 500 trials (10 submissions x 50) from the HF leaderboard dataset
- `scripts/dispatch.py` — one Nodus goal-mode run per trial (30 concurrent)
- `scripts/harvest.py` — poll runs, collect per-trial waste JSON into `data/results.jsonl`

Data source: `harborframework/terminal-bench-2-leaderboard` on Hugging Face (public).
