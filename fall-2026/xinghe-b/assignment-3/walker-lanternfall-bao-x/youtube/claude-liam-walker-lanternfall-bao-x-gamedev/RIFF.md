# RIFF — the judgments the narration makes, and what they rest on

Teardown register: describe the mechanism, then judge it. Every judgment below points at something the viewer can see in the same beat.

| Beat | Judgment | Evidence on screen |
|---|---|---|
| B01 | "AI made the assets — not the game." | the beats that follow show code written for the game and Bao's decisions; the models appear only as asset sources (B05, B29) |
| B02 | the design came first | tag `design-v1` date beside the first generation commit |
| B06 | the edit chain is reproducible | re-running the logged steps lands on the shipped frame, pixel for pixel |
| B08 | what held and what broke | the comparison image; the origin change and its test |
| B11–B12 | one throttle table is enough to stop machine-gunning | counters from the take: kills vs kill sounds |
| B13–B15 | music follows state, never the other way | the code path is one-way (`state.changed` in, mixer out); heard in B15 |
| B16–B17 | the hit-test change fixed what Bao actually saw | before/after frames from the build Bao played and the film build, with the old circle and the sprite box drawn from the engine's transform |
| B21–B22 | "what stops him is what you see" | the solid box drawn over the stall sprite |
| B23–B25 | mute is presentation only | HUD line flips, run continues; heard in B25 |
| B27–B28 | sound cannot decide the game | the independence record: identical summaries with and without sound |
| B30 | the limits are small and written down | TEST-REPORT open items on screen |
| B31 | "the strongest engineering choice is that sound can never decide the game" | B27–B28; it is the one design rule a test proves end to end |

What the film does **not** claim: that the game is balanced (only Bao's play and scripted bots), that the gamepad works (untested), or that the playtests saw the final review fixes (they predate them; tests cover the fixes).
