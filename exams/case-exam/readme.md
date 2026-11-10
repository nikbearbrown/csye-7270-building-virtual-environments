> **Retired 2026-11-09.** The Fall 2026 exam is now entirely multiple-answer, with no case questions. These 16 cases are kept for reference only and are not used for practice or for the exam. See [../../fall-2026-exam/README.md](../../fall-2026-exam/README.md).

# CSYE 7270 case exam: audit an agent's report

One case per chapter, Chapters 0 to 14 (Chapter 15 is the final project and has no case). Drafted 2026-11-08 for Bear to review. Nothing here is wired into the exam yet.

## The format
A student gets a **scenario** (a designer or producer with a goal), the **instruction** a person gave a coding agent, and the **agent's output** (a plan, diff summary or report, 10 to 25 lines, sometimes with a few lines of GDScript). The output is confident and plausible and contains **one seeded flaw** on a concept from the chapter. All agent outputs are **author-written for illustration, not sampled runs**, and each says so.

Then four scripted probes, worth 10 points in total:

| Probe | Points | Asks |
|---|---:|---|
| Q1 | 5 | What is the flaw, and what is the exact term? |
| Q2 | 2 | What single check or instruction turns the agent's claim into evidence? |
| Q3 | 2 | Write the correction to the agent |
| Q4 | 1 | Explain it to the designer in two sentences, no jargon |

The exam is 30 points of multiple-answer jargon questions plus these cases at 10 points each. The test is whether the student uses the course vocabulary precisely enough to direct and audit an agent.

Each case file has a **STUDENT PAGE** (print only this) and a **TA RUBRIC PAGE** (never shown to students).

## The shared rubric (identical for every case)
| Row | Pts | Where scored | Full marks when the student... |
|---|---:|---|---|
| Catches the flaw | 3 | Q1 | identifies the case's flaw (the key states it in one sentence) |
| Exact term | 2 | Q1 | uses a full-credit term from the case key correctly; near-misses get 1 |
| Asks for evidence | 2 | Q2 | asks for a check that can pass or fail and targets the flaw (two acceptable examples and one unacceptable are in each key) |
| Fix or next step | 2 | Q3 | gives an instruction the agent could execute, aimed at the real cause; a correct but vague instruction gets 1 |
| Scope and plain language | 1 | Q4 | explains the problem to a non-expert in plain words, without over-claiming |

**CAP RULE.** If the student does not catch the flaw (Catches = 0), the case maximum is **5/10**, however good the rest sounds. This stops fluent jargon from buying points.

## TA grading guide
1. **Grade the substance, never the writing.** No credit for grammar, length, polish or confident tone. A short answer in rough English that names the right problem earns the same as a polished one. This protects second-language writers.
2. **Grade one case across all students**, then the next case. Do not grade a student's whole exam in one sitting; it stops one strong or weak answer from colouring the others.
3. **Calibrate first.** Before real grading, every TA scores the three sample answers on the case (strong about 9, typical about 6, fluent-but-wrong about 3) without looking at the totals, then compares. Scores must agree within 1 point on each. If not, discuss the key and try again.
4. **Double-score 10%** of papers (chosen at random) by a second TA. Differences over 1 point go to the instructor.
5. **One-line reason for any score under 4**, written on the paper, quoting the term or step missing.
6. **Time:** about 4 to 5 minutes per case once calibrated.
7. Use the key's lists of full-credit terms, half-credit near-misses and traps. When an answer is correct but uses wording the key does not list, award it and add the wording to the key for the next case in the batch.
8. Do not give credit for a correct idea written in a different case's terms (see each key's "Traps").

## Subject-expert check before first use
The keys for the physics and shader cases rest on engine behaviour that a TA who is not a game developer may not be able to verify. **A game developer must check the physics and shader keys before they are used:** Case 1 (the two clocks), Case 4 (layer/mask), Case 6 (alpha), Case 7 (sRGB decode) and Case 8 (golden images). Those files carry a note at the end of their traps.

## Index
| Ch | Case | Seeded flaw | Key terms |
|---:|---|---|---|
| 0 | [The test that "passed" after loosening](ch00-the-unpinned-test.md) | Failing test explained as "flaky" and tolerance widened; real cause was no pinned frame rate | fixed frame rate (`--fixed-fps`), loosening, false pass, deterministic |
| 1 | [Movement on the wrong clock](ch01-movement-on-the-wrong-clock.md) | Moving and colliding in `_process` instead of `_physics_process`; delta-scaling called a fix | `_process`, `_physics_process`, delta, fixed timestep, tunnelling |
| 2 | [The sprite that was "crisp"](ch02-crisp-pixel-art-claim.md) | Pixel art with linear filtering and a 3.5 scale, called crisp from the file size | nearest vs linear filtering, integer scaling, import settings |
| 3 | [The checkpoint post that was "2 metres"](ch03-the-unapplied-scale.md) | Scale 4 left on the object, hull unscaled; size confirmed from Blender "dimensions" | apply transforms, node scale vs mesh size, collision shape vs visual mesh |
| 4 | [The shield nobody can pick up](ch04-layer-and-mask-swapped.md) | Pickup layer and mask swapped; test fired the signal by hand | collision layer, collision mask, Area2D, detection vs response |
| 5 | [The checkpoint that "activates quickly"](ch05-the-unmeasurable-criterion.md) | Unmeasurable acceptance criterion; test teleports the player onto the pad | acceptance criterion, tolerance, given-when-then, direct state write |
| 6 | [The failure flash that draws a box](ch06-the-flash-that-boxes-the-sprite.md) | `mix` over RGBA overwrites alpha; "done" because it compiled | fragment shader, RGBA / alpha channel, compile vs looks right |
| 7 | [The hull that turned to plastic](ch07-the-gloss-from-a-data-map.md) | Roughness map imported as an sRGB colour texture; blamed the lights | data vs colour texture, sRGB-to-linear decode, import settings |
| 8 | [The golden image that agreed with itself](ch08-the-golden-image-regenerated.md) | Golden image regenerated from the new output, then PASS | test oracle, golden / reference image, false pass, pinned clock |
| 9 | [The death burst nobody sees](ch09-the-burst-that-dies-with-its-parent.md) | Burst parented to the creep that is freed the same frame | parenting, node lifetime, state vs visual intent |
| 10 | [The walk cycle with a hitch](ch10-the-walk-cycle-that-hitches.md) | Last key repeats the first pose, so the loop holds a pose twice | loop seam, keyframe, loop mode, frame index |
| 11 | [Walk and run as two states](ch11-the-state-machine-that-pops.md) | State machine with a speed threshold where a blend space was needed | blend space (blend tree), state machine, parameter, threshold |
| 12 | [The click that is twice as loud](ch12-the-signal-connected-twice.md) | Signal connected twice (editor and code); two voices sum and clip | signal connect, voice / polyphony, clipping |
| 13 | ["Three times faster" from one run](ch13-the-speedup-from-one-run.md) | Speed-up claimed from one debug-build run, mean only, with warm-up | variance, warm-up, percentile, release build, profiler, hot spot |
| 14 | [The guard that cannot decide](ch14-the-guard-that-flickers.md) | One sight-range threshold for chase and patrol | hysteresis, flicker, finite state machine, threshold |

Every flaw is distinct, no key depends on chapter wording, dates or API signatures, and terms match the [glossary](../GLOSSARY-jargon-midterm.md).

## Blind check
See [blind-check.md](blind-check.md).
