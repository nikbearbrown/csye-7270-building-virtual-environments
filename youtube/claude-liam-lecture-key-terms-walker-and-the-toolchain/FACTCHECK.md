# FACTCHECK - Key Terms: Walker and the Toolchain

Status: 2026-11-13, checked by Claude. Figures: every spoken figure machine-checked against the words on the slide at that step. Explanations: an independent second pass compared every beat with its slide and the chapter and reworded 2 beat(s). No human sign-off.

The film teaches from the deck; the deck's numbers are computed in the page or labelled illustrative or simulated on the slide itself (the badge at top right). This file checks that the narration says only what the slide and the chapter support.

| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |
|---|---|---|---|---|---|
| 1 | BOPEN | Playlist name, film title, what the film covers | PASS | Playlist name follows the Computational Skepticism one (course name, Exam Prep); summary restates the deck's map slide | none |
| 2 | BDEFS | What each tag and badge means: In the book text, In the glossary, Computed, Illustrative data, Conceptual | PASS | Deck slide 1 speaker note (tags); the badges are the deck's own evidence labels; seeded = the deck's `rng(seed)` | none |
| 3 | B0101 | Figures spoken: `26`, `four groups` | PASS | Each figure is printed on slide 2 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 4 | B0101 | Explanation of: GROUP; TERMS; WHAT IT IS ABOUT; The four tools | PASS | Second-pass check against slide 2 step 1 and 00-the-toolchain.md | none |
| 5 | B0102 | Explanation of: Running without a window; How a script runs and judges the game | PASS | Second-pass check against slide 2 step 2 and 00-the-toolchain.md | none |
| 6 | B0103 | Explanation of: Telling the agent; What the agent knows and what it may touch | PASS | Second-pass check against slide 2 step 3 and 00-the-toolchain.md | none |
| 7 | B0104 | Explanation of: Proving it; How you know a change is real | PASS | Second-pass check against slide 2 step 4 and 00-the-toolchain.md | none |
| 8 | B0201 | Explanation of: Walker; in the book text; TELL THESE APART; Commit | PASS | Second-pass check against slide 3 step 1 and 00-the-toolchain.md | none |
| 9 | B0202 | Explanation of: Repository; in the book text; A project folder with its full version history.; in the book text | PASS | Second-pass check against slide 3 step 2 and 00-the-toolchain.md | none |
| 10 | B0203 | Figures spoken: `33 lines changed across 3 commits` | PASS | Each figure is printed on slide 3 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 11 | B0203 | Explanation of: in the book text; The exact lines that changed between two versions.; Diff; WHAT EACH COMMIT CHANGED | PASS | Second-pass check against slide 3 step 3 and 00-the-toolchain.md | none |
| 12 | B0301 | Explanation of: CLI and shell; in the book text; TELL THESE APART; Flag | PASS | Second-pass check against slide 4 step 1 and 00-the-toolchain.md | none |
| 13 | B0302 | Explanation of: in the book text; An option on a command, such as --headless.; Flag; flags: --headless and --quit | PASS | Second-pass check against slide 4 step 2 and 00-the-toolchain.md | none |
| 14 | B0303 | Figures spoken: `25 checks, 0 failures` | PASS | Each figure is printed on slide 4 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 15 | B0303 | Explanation of: in the book text; Running with no window or display.; Headless; WINDOW VERSUS NO WINDOW | PASS | Second-pass check against slide 4 step 3 and 00-the-toolchain.md | none |
| 16 | B0401 | Figures spoken: `30 S TIMEOUT`, `exit code 0` | PASS | Each figure is printed on slide 5 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 17 | B0401 | Explanation of: Exit code; in the book text; A number a program returns; 0 means success.; TELL THESE APART | PASS | Second-pass check against slide 5 step 1 and 00-the-toolchain.md | none |
| 18 | B0402 | Figures spoken: `exit code 1` | PASS | Each figure is printed on slide 5 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 19 | B0402 | Explanation of: in the book text; A run that never finishes.; Hang; run B | PASS | Second-pass check against slide 5 step 2 and 00-the-toolchain.md | none |
| 20 | B0403 | Figures spoken: `timeout 30 s`, `stopped at 30 s` | PASS | Each figure is printed on slide 5 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 21 | B0403 | Explanation of: Timeout; in the book text; A limit after which a run is stopped.; timeout 30 s | PASS | Second-pass check against slide 5 step 3 and 00-the-toolchain.md | none |
| 22 | B0501 | Figures spoken: `source v1`, `made from v1` | PASS | Each figure is printed on slide 6 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 23 | B0501 | Explanation of: Import; in the book text; Convert a source file into the form the engine uses.; TELL THESE APART | PASS | Second-pass check against slide 6 step 1 and 00-the-toolchain.md | none |
| 24 | B0502 | Figures spoken: `source v2`, `made from v1` | PASS | Each figure is printed on slide 6 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 25 | B0502 | Explanation of: in the book text; Cache; source v2; STALE: the engine still shows v1 | PASS | Second-pass check against slide 6 step 2 and 00-the-toolchain.md | none |
| 26 | B0503 | Figures spoken: `made from v2` | PASS | Each figure is printed on slide 6 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 27 | B0503 | Explanation of: made from v2; fresh again; Re-import: the copy matches again. | PASS | Second-pass check against slide 6 step 3 and 00-the-toolchain.md | none |
| 28 | B0601 | Figures spoken: `6 of 6` | PASS | Each figure is printed on slide 7 at step 1 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 29 | B0601 | Explanation of: Permission prompt; in the book text; A question asking you to approve an action.; TELL THESE APART | PASS | Second-pass check against slide 7 step 1 and 00-the-toolchain.md | none |
| 30 | B0602 | Figures spoken: `3 of 6` | PASS | Each figure is printed on slide 7 at step 2 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 31 | B0602 | Explanation of: in the book text; A saved permission letting a command run without asking.; Allow rule; WITH AN ALLOW RULE FOR THE TEST | PASS | Second-pass check against slide 7 step 2 and 00-the-toolchain.md | none |
| 32 | B0603 | Figures spoken: `1 of 6` | PASS | Each figure is printed on slide 7 at step 3 (machine check, check_narration.py). Badge: Illustrative data. | none |
| 33 | B0603 | Explanation of: in the book text; Sandbox; WITH A SANDBOX AROUND THE PROJECT; blocked | PASS | Second-pass check against slide 7 step 3 and 00-the-toolchain.md | none |
| 34 | B0701 | Explanation of: Instruction file; in the book text; TELL THESE APART; Checkable | PASS | Second-pass check against slide 8 step 1 and 00-the-toolchain.md | none |
| 35 | B0702 | Figures spoken: `160.0`, `192.0`, `2 of 25` | PASS | Each figure is printed on slide 8 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 36 | B0702 | Explanation of: Spec; in the glossary; A written description of what must be built.; Checkable instruction | PASS | Second-pass check against slide 8 step 2 and 00-the-toolchain.md | none |
| 37 | B0801 | Figures spoken: `100 PX/S`, `30 frames a second`, `144 frames a second`, `100 px` | PASS | Each figure is printed on slide 9 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 38 | B0801 | Explanation of: Game time; in the glossary; The simulation's clock, as opposed to the wall clock.; TELL THESE APART | PASS | Second-pass check against slide 9 step 1 and 00-the-toolchain.md | none |
| 39 | B0802 | Figures spoken: `25-CHECK`, `22.4 s`, `--fixed-fps 60`, `0.34 s`, `66 times faster` | PASS | Each figure is printed on slide 9 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 40 | B0802 | Explanation of: Fixed frame rate; in the book text; Pinned time step; in the book text | CORRECTED | Second-pass check against the slide and the chapter: 'Locks a run to a set number of frames a second' implies wall-clock frames (yet the run went about 66 times faster than real time) and echoes the slide's 'rendering' wording; Chapter 0 says --fixed-fps makes each frame exactly 1/fps of game time and disables real-time sync, and nothing is drawn headless (Chapter 1: steps without waiting for the wall clock). | Reworded. Was: "The same twenty-five check test, timed two ways. Real time, twenty-two point four seconds. With the fixed f p s flag at sixty, zero point three four seconds, ab" |
| 41 | B0901 | Figures spoken: `Rung 1` | PASS | Each figure is printed on slide 10 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 42 | B0901 | Explanation of: Claim versus evidence; in the book text; A claim says what happened; evidence is proof that it did.; TELL THESE APART | PASS | Second-pass check against slide 10 step 1 and 00-the-toolchain.md | none |
| 43 | B0902 | Figures spoken: `Rung 2` | PASS | Each figure is printed on slide 10 at step 2 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 44 | B0902 | Explanation of: 2. a git diff; Rung 2 proves: which lines changed; It does not prove: that it works | PASS | Second-pass check against slide 10 step 2 and 00-the-toolchain.md | none |
| 45 | B0903 | Figures spoken: `Rung 3` | PASS | Each figure is printed on slide 10 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 46 | B0903 | Explanation of: 3. clean --import and --check-only; Rung 3 proves: scripts parse; It does not prove: behaviour is right | PASS | Second-pass check against slide 10 step 3 and 00-the-toolchain.md | none |
| 47 | B0904 | Figures spoken: `Rung 4` | PASS | Each figure is printed on slide 10 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 48 | B0904 | Explanation of: Deterministic; in the book text; The same inputs always give the same result.; Flaky | PASS | Second-pass check against slide 10 step 4 and 00-the-toolchain.md | none |
| 49 | B0905 | Figures spoken: `Rung 5` | PASS | Each figure is printed on slide 10 at step 5 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 50 | B0905 | Explanation of: 5. you played it; Rung 5 proves: what one person feels; It does not prove: other people, other machines | PASS | Second-pass check against slide 10 step 5 and 00-the-toolchain.md | none |
| 51 | B0906 | Figures spoken: `Rung 6` | PASS | Each figure is printed on slide 10 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 52 | B0906 | Explanation of: 6. exported build runs on the target; Rung 6 proves: it survives packaging; It does not prove: that anyone wants it | PASS | Second-pass check against slide 10 step 6 and 00-the-toolchain.md | none |
| 53 | B1001 | Figures spoken: `160`, `192` | PASS | Each figure is printed on slide 11 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 54 | B1001 | Explanation of: Text versus binary scene; in the book text; Readable scene files diff cleanly; opaque ones do not.; TELL THESE APART | PASS | Second-pass check against slide 11 step 1 and 00-the-toolchain.md | none |
| 55 | B1002 | Explanation of: Regression test; in the book text; A test that guards a behaviour that worked before.; A regression test then protects the behaviour you changed. | PASS | Second-pass check against slide 11 step 2 and 00-the-toolchain.md | none |
| 56 | B1101 | Figures spoken: `exit 0, 25/25` | PASS | Each figure is printed on slide 12 at step 1 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 57 | B1101 | Explanation of: PAIR 1 · LEFT; Claim; Someone says it works.; “done” | PASS | Second-pass check against slide 12 step 1 and 00-the-toolchain.md | none |
| 58 | B1102 | Explanation of: PAIR 2 · LEFT; Commit; Saves a snapshot on your machine.; stays on this machine | PASS | Second-pass check against slide 12 step 2 and 00-the-toolchain.md | none |
| 59 | B1103 | Figures spoken: `60 s`, `exit 1` | PASS | Each figure is printed on slide 12 at step 3 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 60 | B1103 | Explanation of: PAIR 3 · LEFT; Hang; Never finishes.; still running at 60 s | PASS | Second-pass check against slide 12 step 3 and 00-the-toolchain.md | none |
| 61 | B1104 | Figures spoken: `8 of 8` | PASS | Each figure is printed on slide 12 at step 4 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 62 | B1104 | Explanation of: PAIR 4 · LEFT; Deterministic; Same inputs, same result.; 8 of 8 the same | PASS | Second-pass check against slide 12 step 4 and 00-the-toolchain.md | none |
| 63 | B1201 | Figures spoken: `--fixed-fps 60`, `exit code 0`, `25 of 25` | PASS | Each figure is printed on slide 13 at step 1 (machine check, check_narration.py). Badge: Computed. | none |
| 64 | B1201 | Explanation of: “check it works”; WHAT THE INSTRUCTION DOES; agent says done; exit code 0, 25 of 25 | PASS | Second-pass check against slide 13 step 1 and 00-the-toolchain.md | none |
| 65 | B1202 | Figures spoken: `30 seconds`, `22 s`, `30 s` | PASS | Each figure is printed on slide 13 at step 2 (machine check, check_narration.py). Badge: Computed. | none |
| 66 | B1202 | Explanation of: “make sure it doesn't hang”; a run that ends at 22 s: passes; a hang: stopped at 30 s, fails; the timeout turns waiting into an answer | PASS | Second-pass check against slide 13 step 2 and 00-the-toolchain.md | none |
| 67 | B1203 | Figures spoken: `3 allowed, 2 blocked` | PASS | Each figure is printed on slide 13 at step 3 (machine check, check_narration.py). Badge: Computed. | none |
| 68 | B1203 | Explanation of: “keep the agent away from my files”; read; allowed; edit | PASS | Second-pass check against slide 13 step 3 and 00-the-toolchain.md | none |
| 69 | B1204 | Figures spoken: `22.4 s`, `0.34 s`, `66 times faster` | PASS | Each figure is printed on slide 13 at step 4 (machine check, check_narration.py). Badge: Computed. | none |
| 70 | B1204 | Explanation of: “the test is too slow”; → Pin the time step: 22.4 s real-time becomes 0.34 s; real-time: 22.4 s; pinned: 0.34 s | PASS | Second-pass check against slide 13 step 4 and 00-the-toolchain.md | none |
| 71 | B1205 | Figures spoken: `160.0`, `192.0`, `25 checks`, `2 of 25` | PASS | Each figure is printed on slide 13 at step 5 (machine check, check_narration.py). Badge: Computed. | none |
| 72 | B1205 | Explanation of: “make the player faster”; 2 of 25 checks fail after the change; a one-number change can break two checks | PASS | Second-pass check against slide 13 step 5 and 00-the-toolchain.md | none |
| 73 | B1301 | Explanation of: Was it headless, with the time step pinned?; Did I import first, so the cache is not stale?; Is the command allowed, and is everything else blocked?; Is the instruction checkable, with a number and a test? | PASS | Second-pass check against slide 14 step 1 and 00-the-toolchain.md | none |
| 74 | B1302 | Explanation of: Before you trust an agent’s change | CORRECTED | Second-pass check against the slide and the chapter: Nothing in the references says running in a window makes a run unrepeatable; Chapter 0 puts the cause on real-time steps (no --fixed-fps), so the window clause states a false cause. | Reworded. Was: "Second, was it headless, with the time step pinned? A run in a window, or with real-time steps, may not repeat the same way twice." |
| 75 | B1303 | Explanation of: Before you trust an agent’s change | PASS | Second-pass check against slide 14 step 3 and 00-the-toolchain.md | none |
| 76 | B1304 | Explanation of: Before you trust an agent’s change | PASS | Second-pass check against slide 14 step 4 and 00-the-toolchain.md | none |
| 77 | B1305 | Explanation of: Before you trust an agent’s change | PASS | Second-pass check against slide 14 step 5 and 00-the-toolchain.md | none |
| 78 | B1306 | Figures spoken: `exit code 0`, `--fixed-fps 60` | PASS | Each figure is printed on slide 14 at step 6 (machine check, check_narration.py). Badge: Conceptual illustration. | none |
| 79 | B1306 | Explanation of: Before you trust an agent’s change | PASS | Second-pass check against slide 14 step 6 and 00-the-toolchain.md | none |
| 80 | BVDT | Six recap lines | PASS | Each restates a body beat; nothing new | none |
| 81 | BHTF | Practice prompt | EXEMPT | A viewer exercise composed from the film's terms; not presented as a run | none |

## Things noticed on the deck itself (not changed; for Bear)

- Slide 2 step 3: the middle commit is labelled '1 lines changed'; it should read '1 line changed'.
- Slide 4 carries the badge Computed, but its own note says the run lengths are illustrative and the 30 s limit is an example. The badge should be Illustrative data. The narration calls the run lengths made-up.
- Slide 6 step 2 is headed 'WITH AN ALLOW RULE FOR THE TEST' and the caption says the allow rule lets 'the one command you trust run unasked', but 'read a script' also flips from 'asks you' to 'runs' (renderPerm marks rows 0, 2 and 4 as ok). The drop from 6 to 3 prompts depends on that unexplained change. The six actions also list 'run the headless test' twice.
- Slide 12 step 3: the instruction says 'Allow only the test command', but the chart shows read, edit and run test all allowed ('3 allowed, 2 blocked'). On slide 6, even inside the sandbox, the edit still 'asks you'.
- Slide 7 step 2 pairs the vague 'make the ball faster' (the Pong ball) with the Chapter 1 change 'change speed 160.0 to 192.0', which is the walker-jumpman player's run speed in tuning.gd, not a ball. Slide 12 step 5 says 'make the player faster' correctly. The checkable version also says 'and pass the mechanics test' while its own result is 2 fails, and Chapter 1's prompt told the agent not to try to make a failing check pass; slide 12's wording 'then run the mechanics test' is the accurate one.
- Slide 10 step 1 shows the run-speed change as a line 'speed = 160.0' inside a .tscn scene beside position and visible. In walker-jumpman the speed lives in tuning.gd, a resource created in code, not in a scene file. As a conceptual picture it may mislead.
- Slide 10 step 2: the caption 'A regression test then protects the behaviour you changed' conflicts with the definition on the same slide, 'guards a behaviour that worked before'. Regression test is also introduced twice with the same definition, on slide 9 step 4 and slide 10 step 2.
- Slide 8 step 2 and slide 12 step 4 use the walker-jumpman timings (22.4 s real-time, 0.34 s pinned), and slide 8's caption says that with the step pinned the test 'then runs the same way every time'. Chapter 1 says walker-jumpman is immune to the time trap and gave identical results with and without the flag, so the pin bought speed, not repeatability, for this test. The Pong test in Chapter 0 is the case where pinning fixed flakiness.
- Slide 3 step 3: the headless output mixes Pong lines ('ball hits wall', 'score = 1') with '25 checks, 0 failures', the walker-jumpman mechanics-test count; Chapter 0's Pong test has ten checks.
- Slide 8: 'Fixed frame rate' is defined as 'Rendering locked to a set number of frames a second', but Chapter 0 says --fixed-fps forces each frame to be exactly 1/fps of game time and disables real-time sync; in a headless run nothing is rendered. The definition matches the course glossary, so the glossary row may want the same fix.
- Slide 12 step 4: the line '22.4 s real-time becomes 0.34 s' wraps so the unit 's' sits alone on its own line.
- Title slide speaker note says 'Deck 2 of the topic order' while the file and film are deck 04.

## Open after the second pass

- slide 10 step 1: the slide draws the run-speed change as a line inside a .tscn scene, but in walker-jumpman the speed lives in tuning.gd (a resource made in code, Chapter 1); the narration only describes the conceptual picture and makes no Walker claim, so it is left, but the slide may mislead.
- slide 8 step 2 and slide 12 step 4: the slides pair the walker-jumpman timings with 'the test then runs the same way every time'; Chapter 1 says walker-jumpman gave identical results with and without the flag (pinning bought speed only). The narration says 'identical results' and claims no repeatability gain for walker-jumpman, and attributes the flaky-to-deterministic fix to the Pong test (slide 9 step 4), matching Chapter 0; nothing to change, flagged for the deck.
