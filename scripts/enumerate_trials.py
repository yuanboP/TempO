"""Enumerate TB 2.0 leaderboard trials that have agent/trajectory.json, spread across submissions."""
import json, urllib.request, urllib.parse, sys

REPO = "harborframework/terminal-bench-2-leaderboard"
SUBMISSIONS = [
    "Terminus2__Claude-Opus-4.6",
    "Terminus2__GPT-5.3-Codex",
    "Terminus2__GLM-4.7",
    "Terminus2__GLM-5",
    "Terminus2__DeepSeek-V3.2",
    "Terminus2__Kimi-k2.5",
    "Terminus2__Minimax-m2.5",
    "ClaudeCode__GLM-4.7",
    "Gemini_CLI__Gemini-3.1-Pro-Preview",
    "Gemini_CLI__Gemini-3-Flash-Preview",
]
PER_SUBMISSION = 50  # 10 x 50 = 500

def tree(path):
    url = f"https://huggingface.co/api/datasets/{REPO}/tree/main/{urllib.parse.quote(path)}"
    return json.load(urllib.request.urlopen(url))

out = []
for sub in SUBMISSIONS:
    base = f"submissions/terminal-bench/2.0/{sub}"
    jobs = [x["path"] for x in tree(base) if x["type"] == "directory"]
    trials = []
    for job in jobs:
        trials += [x["path"] for x in tree(job) if x["type"] == "directory"]
    # one trial per task first (task name = dirname before __), then fill up
    seen_tasks, picked, rest = set(), [], []
    for t in sorted(trials):
        task = t.split("/")[-1].rsplit("__", 1)[0]
        (picked if task not in seen_tasks else rest).append(t)
        seen_tasks.add(task)
    picked = (picked + rest)[:PER_SUBMISSION]
    for t in picked:
        out.append({"submission": sub, "trial_path": t})
    print(f"{sub}: {len(trials)} trials found, picked {len(picked)}", file=sys.stderr)

with open("data/trials.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r) + "\n")
print(f"total: {len(out)}", file=sys.stderr)
