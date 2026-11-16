# RIFF — gameplay observations (capture/run-01)

Riffs are on what the capture shows, inspected frame by frame before writing. Scripted input, not a human playtest; how the effects read in play was judged by the author in the running game (TUNING.md, TEST-REPORT.md "Human checks").

| Artifact + frames | Visible observation | Interpretation and source | Narration (beat) | Next experiment |
|---|---|---|---|---|
| run-01 16–70 | the trail leaves the staff behind the fireball (frames 20–28); at 29 the flash and the sparks burst on the ground; the trail's last dots fade where they were over the next frames | the trail is released into Main, not freed with the fireball (`fireball.gd` 49, 61–63) | B04 | watch the same shot at the screen edge |
| run-01 86–92 | a shot left hits the left wall at x 1.3: the burst sits on the screen's edge, sparks spread into view | `visibility_rect` (−96, −96, 192, 192); the author checked both walls at the camera limits (TEST-REPORT.md) | B13 | the same at the right wall |
| run-01 120–281 | D held, Space at x ≥ 492: the mage walks and jumps the pit | normal input path; not an effect | B13 | — |
| run-01 282–364 | three shots at the wolf; impacts at 311 and 333 on the wolf, the wolf defeated at 333; the third lands on the ground | one impact per hit (A1); the impact is a child of Main, so it survives the wolf (A5) | B13 | — |
| run-01 384–496 | nine clicks 11 frames apart: each impact appears while the previous one is still visible | overlap (A4): a new instance per explode() | B13 | count alive instances on screen against the test's "at most 3" |
| run-01 623–700 | a shot right at staff height flies 2 s without a hit; the trail stops and fades where the fireball was | the timeout path calls the same release (`fireball.gd` 28) | B19 | — |
| run-01 706–745 | a shot left: the dots trail to the right of the fireball | `direction` (−1, 0) follows the fireball's rotation (probe e174c96, brief revision 7957614) | B19 | — |
| run-01 765–873 | Esc at 787: the pause screen darkens the frame and the trail stays still; Esc at 835: it moves again; released at 873 | pausable nodes and a pausable free timer; game time, not wall time (B2 + B3 in `test_fireball_trail.gd`) | B19 | measure on screen whether a hidden emitter keeps simulating (B4, open) |
