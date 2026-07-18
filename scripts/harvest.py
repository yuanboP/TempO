"""Poll dispatched runs; collect finalOutput JSON into data/results.jsonl."""
import json, subprocess, os

def get_run(run_id):
    r = subprocess.run(["nodus", "runs", "get", "--run", run_id],
                       capture_output=True, text=True, timeout=60)
    d = json.loads(r.stdout)
    return d.get("run", d)

if __name__ == "__main__":
    manifest = [json.loads(l) for l in open("data/manifest.jsonl") if "run_id" in json.loads(l)]
    harvested = set()
    if os.path.exists("data/results.jsonl"):
        harvested = {json.loads(l)["run_id"] for l in open("data/results.jsonl")}
    counts = {}
    with open("data/results.jsonl", "a") as rf:
        for m in manifest:
            if m["run_id"] in harvested:
                counts["harvested_before"] = counts.get("harvested_before", 0) + 1
                continue
            try:
                run = get_run(m["run_id"])
            except Exception:
                counts["fetch_error"] = counts.get("fetch_error", 0) + 1
                continue
            status = run.get("status")
            counts[status] = counts.get(status, 0) + 1
            if status not in ("completed", "failed", "cancelled"):
                continue
            rec = {"run_id": m["run_id"], "trial_path": m["trial_path"],
                   "submission": m["submission"], "status": status,
                   "usage": run.get("usage")}
            out = run.get("finalOutput") or ""
            try:
                start, end = out.find("{"), out.rfind("}")
                rec["analysis"] = json.loads(out[start:end + 1])
            except Exception:
                rec["raw_output"] = out[-2000:]
            rf.write(json.dumps(rec) + "\n")
    print(json.dumps(counts, indent=1))
