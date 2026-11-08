# Blind check (2026-11-08)

**Set-up.** Five cases (1, 4, 7, 11, 13: the two-clocks, layer/mask, sRGB, state-machine and benchmark flaws), student pages only (no rubric, no key). Sub-agents wrote answers in a persona; I scored them against the rubric as a TA would. Because language models cannot easily imitate a weak student, two rounds were needed.

| Run | Persona (what the prompt asked) | What came back | Scores per case (1 / 4 / 7 / 11 / 13) | Total |
|---|---|---|---|---:|
| A | strong, exact terms | strong | 10 / 10 / 10 / 10 / 10 | 50 |
| B | "typical", second-language | indistinguishable from strong (persona did not hold) | 10 / 10 / 10 / 9 / 9 | 48 |
| C | "fluent but wrong", round 1 | also strong (persona did not hold) | not scored | n/a |
| D | vague, plain words, gets the gist in about half | caught 3 of 5 in plain words | 1 / 6 / 0 / 5 / 6 | 18 |
| E | fluent but shallow, forbidden to find the flaw | confident jargon, wrong target | 3 / 5 / 0 / 2 / 3 | 13 |

**Does the rubric separate good from weak?** Yes. Strong answers land at 9 to 10, plain-but-partly-right answers at 5 to 6 (or 0 to 1 where they missed the flaw), and fluent-wrong answers at 0 to 5. In cases 4, 11 and 13 the plain student who saw the problem without the exact term out-scored the jargon-heavy student (6, 5, 6 against 5, 2, 3), which is the intent. The cap rule held: no missed-flaw answer scored over 3.

**Weaknesses found, and what I changed**
1. Case 4: the fluent answer noticed the hand-emitted signal but diagnosed a race condition, and scored 5. Added a "partial catch" line to the key (Catches 2, Term 1 at most; call_deferred earns no Term).
2. Case 13: the fluent answer asked for several runs on the phone and scored 3 from the evidence and fix rows alone while agreeing the 3x looked real. Added a rule that repeat-runs alone is Evidence 1, and that agreeing with the claim means the flaw is missed.
3. Case 11: "log the blend value" or "lengthen the cross-fade" were scoring too generously. Key now says Evidence 1 and Fix 0.
4. Case 1: a "clamp delta" answer is explicitly worthless; the double-scaling remark is accepted as a side point only. Case 7: "the lights" excuse is explicitly Catches 0.

**Not tested.** Real student writing (no real second-language students were available; the model personas were still too articulate), the other ten cases, and TA-to-TA agreement (I was the only scorer). Run the README calibration step with real TAs on the three sample answers before using any case. The three-scored sample answers in each file were written by me, not drawn from the blind runs.
