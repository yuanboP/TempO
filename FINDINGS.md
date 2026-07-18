# Phase 1 Findings — TB 2.0 Trajectory Waste Analysis (2026-07-18)

500 trials dispatched (10 submissions x 50, one Nodus goal-mode agent per trial),
499 harvested, 436 parseable analyses. Taxonomy: W1 repeat-slow, W2 over-wait,
W3 under-wait churn, W4 same-error retry, W5 redundant env setup.

## Headline numbers

- Overall waste_frac: median 3.7%, **p90 34%** — waste is a long-tail phenomenon.
- **18 TIME-DEATH trials** (failed at/near budget with >40% wall-clock in W1-W5) = 4.1% of all trials, ~8% of failures.
- Failed trials waste more than solved ones (median 4.3% vs 2.7%).

## Harness effect (the key natural experiment)

Same model, different harness — GLM-4.7:
- Terminus2 (blind `duration` guessing): waste median **7.2%**
- ClaudeCode (native tool calling): waste median **0.1%**

Terminus2's declared-duration mechanic mechanically produces W2/W3 (29.8% and
22.5% of all trials have them — the top two waste types). Native tool-calling
harnesses (ClaudeCode, Gemini_CLI) have ~0% *median* waste but violent tails:
Gemini_CLI 3.1-Pro p90 = **60.4%**, 5 TIME-DEATHs across the two Gemini_CLI
groups. Semantic waste (W1/W4/W5) is harness-independent.

## Model effect (within Terminus2)

Strong models fail on hard problems; weaker models fail on time management:
failed-trial waste median is 2.2% (GPT-5.3-Codex) / 5.6% (Opus-4.6) vs
**15.7% (Kimi-k2.5) / 13.9% (GLM-5)**; GLM-5 alone has 5 TIME-DEATHs.

## Top exhibits (Phase 2 adversarial-verification candidates)

| wasted | total | frac | reward | agent | trial |
|-------:|------:|-----:|:------:|-------|-------|
| 2856s | 3599s | 79% | fail | Terminus2/GLM-5 | circuit-fibsqrt__57LJYpt |
| 2109s | 3206s | 66% | pass | Terminus2/Opus-4.6 | fix-ocaml-gc__FGn4nuF |
| 2009s | 9338s | 22% | fail | Terminus2 | build-pov-ray__BZSVpnZ |
| 1190s | 1779s | 67% | fail | Terminus2 | feal-linear-cryptanalysis__AduqbuG |
| 1131s | 3551s | 32% | fail | Terminus2 | distribution-search__C4HedXz |
| 1010s | 1437s | 70% | fail | Gemini_CLI | extract-moves-from-video__7ZFER7w |
|  930s | 3570s | 26% | fail | Terminus2 | fix-ocaml-gc__RG57kDm |
|  906s | 2352s | 39% | fail | Gemini_CLI | compile-compcert__Tp3YxuU |
|  892s | 1339s | 67% | pass | Gemini_CLI | custom-memory-heap-crash__T4hAaNP |
|  768s | 1797s | 43% | fail | Terminus2 | feal-differential-cryptanalysis__Uoi5S58 |

`fix-ocaml-gc` and `build-pov-ray` recur across independent trials — some tasks
systematically induce time black holes.

## Caveats (write these into the paper)

- W2/W3 only exist mechanically in Terminus2-style harnesses; cross-harness
  comparisons must use W1/W4/W5 only.
- Each per-trial verdict is a single LLM judgment (kindle-alpha-api via Nodus);
  numbers above are unverified findings until Phase 2 adversarial verification.
- waste_frac conservatively capped at 1.0; per-agent overlap dedup conventions
  vary (see each record's `note`).

Reproduce: `scripts/enumerate_trials.py` -> `dispatch.py` -> `harvest.py` -> `aggregate.py`.
Raw verdicts in `data/results.jsonl` (gitignored, 499 records; regenerate via harvest).
