# Case 13: "Three times faster" from one run

Chapter 13, Profiling and optimization. Seeded flaw: an optimisation claim based on one run of each version, a mean only, in a debug build including warm-up, with no measurement of where the time goes. Key terms: variance / noise, warm-up, percentile, release build, hot spot, profiler, claim vs evidence, premature optimisation.

---

# STUDENT PAGE

## Scenario
Greta is the producer of a bullet-hell game that stutters on a mid-range phone when a boss fires hundreds of bullets. She will approve a week of rewrite work if the agent can show a real speed-up. She asks the agent to optimise the bullet system and report how much faster it is.

## The instruction given to the agent
"The boss fight stutters. Make the bullet system faster and tell me how much faster it is."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Change: replaced 800 Bullet nodes with a MultiMeshInstance2D and a manual update loop.
Benchmark (debug build, editor, one run each, 10 s each):
  before: average frame time 18.4 ms  (54 FPS)
  after : average frame time  6.1 ms  (164 FPS)
Speed-up: 3.0x.
The nodes were the bottleneck, so removing them explains the gain.
Conclusion: bullet system is 3x faster. Recommend approving the rewrite.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's claim, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "3x faster" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Greta why she should not approve yet.

---

# TA RUBRIC PAGE (not for students)

## The fixed rubric
| Row | Pts | Awarded for |
|---|---|---|
| Catches the flaw | 3 | Q1 |
| Exact term | 2 | Q1 |
| Asks for evidence | 2 | Q2 |
| Fix or next step | 2 | Q3 |
| Scope and plain language | 1 | Q4 |

## The flaw in one sentence
The speed-up rests on one run per version, a mean only, in a debug build in the editor, with warm-up included and no profile of where the time goes, so the 3x cannot be separated from noise or from build overhead, and "nodes were the bottleneck" is an assertion, not a measurement.

## Terms
- **Full credit (2):** variance/noise (repeat runs); warm-up excluded; percentile (99th) or median rather than mean; release build on target hardware; hot spot / profiler; claim vs evidence.
- **Half credit (1):** "not enough runs", "not accurate", "debug mode", "should test on the phone" (any one, without the reason).
- **No credit:** "needs more bullets", "MultiMesh is wrong", "FPS is the wrong unit" alone.

## Acceptable evidence requests
1. "Run each version 10 times in a release build on the target phone, discard the first 2 seconds of each run, and report median and 99th-percentile frame time with the spread."
2. "Capture a profiler trace of the old version during the boss fight and show which function takes the most time before changing anything."

**Unacceptable:** "Run it one more time", "check FPS again", "compare the average over 60 seconds on the same debug build".

## Traps
- Students may accept the numbers and quibble only about the unit (FPS vs ms). The flaw is the missing repeats and the build.
- "Premature optimisation" is a fair term if the student notes no profile identified the hot spot.
- A student who says "the change could be wrong" without naming measurement problems has not caught it.

- Evidence scoring: "run it several times on the phone" alone is 1. For 2 the request needs at least two of: release build, warm-up dropped, median or percentile instead of mean, profile before changing.
- A student who agrees the 3x "looks real" and only adds more optimisations (pooling, culling) has missed the flaw, even if they also ask for more runs; do not let the evidence points alone lift them past the cap.
**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "It is one run each, so no variance is known; it is a debug build in the editor, warm-up is included, and only the mean is given. The 'nodes were the bottleneck' claim has no profiler evidence." Q2: "Run 10 times in a release build on the phone, drop warm-up, report median and 99th percentile." Q3: "Profile the old version first to find the hot spot. Then benchmark both versions as above and report spread." Q4: "We only saw one try of each, in a slow test mode, so the gap might be luck or the test, not the rewrite." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 does not say what to do instead.*

**Typical (6/10).** Q1: "One run is not enough and it is a debug build." Q2: "Run it a few more times on the phone." Q3: "Test it again properly and show the results." Q4: "The test was too small to trust." *Catches 3; Term 1 (debug build, one run; no variance or percentile); Evidence 1 (repeat runs, no release build or warm-up); Fix 0 ("properly" is not an instruction); Scope 1.* Total 6. *Reason: sees the weakness, gives no specific method.*

**Fluent but wrong (3/10).** Q1: "The agent should have used GPU instancing and frustum culling, and object pooling to avoid garbage collection hitches, which would deliver more than 3x." Q2: "Verify draw call counts with the monitors." Q3: "Add object pooling and frustum culling." Q4: "More optimisations are needed first." *Catches 0 (more optimisation, not better measurement); Term 0; Evidence 1 (draw calls are a real metric but not asked); Fix 1; Scope 1.* Total 3. *Reason: optimisation buzzwords, no question of the measurement.*
