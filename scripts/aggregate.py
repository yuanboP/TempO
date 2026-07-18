"""Aggregate data/results.jsonl into per-model waste statistics."""
import json
from collections import defaultdict

def pct(xs, p):
    if not xs: return 0.0
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))]

rows = []
bad = 0
for l in open("data/results.jsonl"):
    r = json.loads(l)
    a = r.get("analysis")
    if not a or r["status"] != "completed" or not isinstance(a, dict):
        bad += 1
        continue
    try:
        # recompute waste conservatively: cap waste_frac at 1, coerce numbers
        total = float(a.get("total_s") or 0)
        wasted = float(a.get("wasted_s_total") or 0)
        if total <= 0: bad += 1; continue
        rows.append({
            "submission": r["submission"], "trial": a.get("trial", ""),
            "reward": int(a.get("reward") or 0), "total_s": total,
            "wasted_s": min(wasted, total), "waste_frac": min(wasted / total, 1.0),
            "w1": len(a.get("w1") or []), "w2": len(a.get("w2") or []),
            "w3": int((a.get("w3") or {}).get("count") or 0),
            "w4": len(a.get("w4") or []), "w5": len(a.get("w5") or []),
            "time_death": bool(a.get("time_death")),
        })
    except (TypeError, ValueError):
        bad += 1

print(f"parsed {len(rows)} trials ({bad} unparseable/failed)\n")

def summarize(name, rs):
    if not rs: return
    wf = [r["waste_frac"] for r in rs]
    solved = [r for r in rs if r["reward"] == 1]
    failed = [r for r in rs if r["reward"] == 0]
    td = sum(r["time_death"] for r in rs)
    print(f"{name:42s} n={len(rs):3d} pass={len(solved)/len(rs):5.0%} "
          f"waste med={pct(wf,.5):5.1%} p90={pct(wf,.9):5.1%} "
          f"failed-trial waste med={pct([r['waste_frac'] for r in failed],.5) if failed else 0:5.1%} "
          f"time_death={td}")

summarize("ALL", rows)
print()
for sub in sorted({r["submission"] for r in rows}):
    summarize(sub, [r for r in rows if r["submission"] == sub])

print("\nwaste-type prevalence (share of trials with >=1 finding):")
for w in ["w1", "w2", "w3", "w4", "w5"]:
    n = sum(1 for r in rows if r[w] > 0)
    print(f"  {w}: {n/len(rows):5.1%}  ({n}/{len(rows)})")

print("\nsolved vs failed:")
for tag, rs in [("solved", [r for r in rows if r["reward"] == 1]),
                ("failed", [r for r in rows if r["reward"] == 0])]:
    if rs:
        wf = [r["waste_frac"] for r in rs]
        print(f"  {tag}: n={len(rs)} waste med={pct(wf,.5):5.1%} p90={pct(wf,.9):5.1%}")

# top exhibits for phase 2
rows.sort(key=lambda r: r["wasted_s"], reverse=True)
print("\ntop 10 by absolute wasted seconds:")
for r in rows[:10]:
    print(f"  {r['wasted_s']:7.0f}s wasted / {r['total_s']:7.0f}s total  reward={r['reward']}  {r['submission'].split('__')[0]:12s} {r['trial'][:40]}")
