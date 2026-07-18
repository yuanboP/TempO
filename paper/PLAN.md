# Road to ICLR (submission ~late Sept 2026)

Working backwards from the deadline. Paper claims that must be true by then:

1. Measurement study (Sec 3) — **data in hand**, needs Phase 2 adversarial
   verification of top exhibits + inter-judge agreement number. ~1 week.
2. Tempo (Sec 4) — build the harness layer on Harbor; 3 ablation variants.
   Target: working by mid-Aug.
3. Main experiment (Sec 6) — 2 harnesses x 3 models x {tempo, no-tempo} x 89
   tasks x 3 trials. Compute-heavy; start as soon as Tempo works.
4. RotBench (Sec 5) — mining can run concurrently (searcher/verifier agents);
   accept a small-but-verified v0 (5-10 tasks) for the paper.

## Timeline

- Jul W4: Phase 2 verification; write Related Work; freeze Sec 3 numbers.
- Aug W1-W2: Tempo implementation + smoke runs; RotBench mining starts.
- Aug W3-W4: main experiment runs; RotBench verifier pass.
- Sep W1-W2: full results in, figures (time-to-success CDF is the money plot).
- Sep W3: polish, internal red-team pass, submit.

## Open risks

- Tempo effect size could be small on TB (20-min tasks, no growth) → RotBench
  results carry the headline; hedge by reporting waste_frac reduction even
  where time-to-success shift is modest.
- kindle-alpha-api judge quality → Phase 2 survival rate decides whether we
  re-judge with a stronger model.
- ICLR style kit not yet released → prose in main.tex is style-agnostic.
