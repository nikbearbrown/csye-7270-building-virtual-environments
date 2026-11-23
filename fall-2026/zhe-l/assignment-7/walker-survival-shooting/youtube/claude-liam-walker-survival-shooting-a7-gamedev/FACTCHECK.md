# Fact check

Every claim in the narration, with its source in the game package at commit 42d6cc0d (or a capture made for this film).

| Claim | Source | Status |
|---|---|---|
| Pixel head = Sprite2D + AnimationPlayer frame track, loops | CHANGE-BRIEF routes table; pixel_head.tscn lines 7-20 (`loop_mode = 1`, `tracks/0/path = NodePath("Sprite2D:frame")`) | verified |
| Raise = imported 3D rig keyed in Blender, exported .glb, committing action | CHANGE-BRIEF routes table; FRICTIONAL entry 2026-11-21 to 11-22 | verified |
| B04 fixture strip labelled by movie frame; logged cell numbers appear to lead the picture by one (unverified, same logging order as r0/r1) | logs/pixel_head_r0.log vs frames | open |
| Sheet 448 x 56, hframes 8, vframes 1, 56 x 56 cells | TEST-REPORT read-back row; pixel_head.tscn line 38; sheet file opened at its real size | verified |
| Keys frame 0-7 every 0.25 s, discrete, LOOP_LINEAR, 2.0 s, no duplicate across the seam | pixel_head.tscn lines 7-20; CHANGE-BRIEF seam rule; TEST-REPORT read-back | verified |
| Sheet generated with Codex / OpenAI image tool; Claude drew the blink; OpenAI Terms of Use | CHANGE-BRIEF image source row; pixel_head/ATTRIBUTION.md | verified (source row); licence wording per the user's brief |
| Read-back passes 37 (head) / 25 (raise) | TEST-REPORT Read-back | verified |
| Phase table startup 0-6, active 7-15, recovery 16-20; 30 fps; overshoot 8 mm on 18 | CHANGE-BRIEF phase table | verified |
| Tablet bone keyed on 0, 7, 16, 20 | TEST-REPORT read-back row for test_tablet_raise_clip.gd | verified |
| Frame 19 dark, frame 20 lit and clickable; no walking during the raise | CHANGE-BRIEF keyed gameplay fact; TEST-REPORT Edges | verified |
| r2 strip: clip 0/5/7/10/14/16/18 = movie 33/38/40/43/47/49/51, lit on movie 54 | TUNING r2 capture | verified |
| AnimationTree is the one authority; tablet on BoneAttachment3D bone `tablet` | humanoid.tscn lines 94-106; humanoid.gd line 63; CHANGE-BRIEF state machine section | verified |
| Four states, ten transitions (Start -> hip plus nine), others 0.2 s cross-fades | humanoid.tscn line 78 (10 transitions); CHANGE-BRIEF transition table; TEST-REPORT State machine (26 PASS) | verified |
| Two-handed pose is a placeholder | CHANGE-BRIEF state table (`hold_2h`) | verified |
| Two clocks: process clip read on physics clock, 1 frame later; 2 before r1 | TEST-REPORT Two clocks; TUNING r1 | verified |
| r1: raise starts on the press frame; lit movie 55 -> 54 | TUNING r1; humanoid.gd lines 203-207 | verified |
| r2: tablet re-posed upright in Blender from play; grip 0.376 -> 0.293 m; kept | TUNING r2 | verified |
| Edge tests interrupt one frame before/on/after each boundary, short and long | TEST-REPORT Edges (126 PASS) | verified |
| Mutations that fail: subname frme, LOOP_NONE, last key 8, import loop_mode 0 -> 1 | TEST-REPORT Mutations | verified |
| Baseline 56/25 -> 55/24 (summary line counted) | TEST-REPORT Baseline correction | verified |
| Head property check too weak, exposed by rename mutation | TEST-REPORT Read-back finding | verified |
| Preview logged before the AnimationTree updated; r0/r1 labels one frame early | TUNING r1 fixture error; TEST-REPORT Frame strips | verified |
| Overshoot flattened accepted; back view not a fault | TUNING r0 "Where we differ" | verified |
| Cross-fade hand/tablet separation not measured | user's brief for this film; no test measures it | stated as open |
| 11 test suites pass with the same counts after r2 | TEST-REPORT After TUNING r2 | verified |
| Human vs Claude contributions | FRICTIONAL.md entries; TUNING verdicts | summarised |
| Next: walking while raising; put-back, two-hand raise, jump animations | TEST-REPORT Human checks (walking while raising); user's brief for this film (other animations) | planned, not built |

## Capture-specific facts (this film's scripted-input capture)

| Claim on screen | Evidence | Status |
|---|---|---|
| Startup interrupt at clip ~frame 3 | capture-log: INPUT frame=156 TAB_UP clip_pos=0.1000 | verified |
| Active interrupt at clip ~frame 9 | capture-log: INPUT frame=222 TAB_UP clip_pos=0.3000 | verified |
| Recovery interrupt at clip ~frame 18, screen still dark | capture-log: INPUT frame=291 TAB_UP clip_pos=0.6000 lit=false | verified |
| Long press in active at clip ~frame 12 -> hold_2h | capture-log: frame=355 clip_pos=0.4000, CHANGE frame=356 state=hold_2h | verified |
| Back view after the first two-hand hold | frames after 14.1 s (the body turns to the camera direction in two-hand mode) | observed |

## Narration wording vs the capture

The capture narration (B11) says a long press "blends to two hands"; in the capture the two-hand state also switches the game to its own first-person view, which the on-screen label states. The capture is 26.37 s and B11 narration is 30.33 s, so the last frame is held and labelled HELD FRAME; no footage was retimed.
