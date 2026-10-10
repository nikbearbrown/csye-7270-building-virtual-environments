# Fact check — every claim in the narration, against its source

Source revision for all game/doc claims: **f848d84** (course repository). "Draft" = `README.md` / `TEST-REPORT.md`,
which the designer wrote but had not committed when the film was made; the brief named TEST-REPORT as the source
of truth for tests. Corrections found while writing are listed at the end.

| Beat | Claim | Source | Status |
|---|---|---|---|
| B00 | The opening prompt is a reconstruction, not a saved session | this film (labelled on screen and in narration) | ✓ disclosed |
| B00 | Design and first assets exist; playable slice does not | README (draft) "Status: incomplete submission"; TEST-REPORT | ✓ |
| B01 | Three generated sounds, one empty subway room, full asset log | SOURCES asset log; `design/sfx_sound/` (3 files); `base.tscn` | ✓ ("empty" = no character/props except the test chair) |
| B02 | Subway under a ruined city, rugged military tablet, deploy / fight / loot / extract, lose what you carry on death | CONCEPT "The game in two sentences", "Core loop" | ✓ |
| B02 | Three pillars; world keeps going while tablet open; small but complex maps; best loot guarded | CONCEPT "Design pillars" table | ✓ |
| B03 | Panel 3 is the designer's hand sketch; short Tab = one hand + small window, long Tab = two hands; "short beep" | STORYBOARD panel 3, three-state table, revision 2026-10-07 (sketches are the designer's) | ✓ |
| B04 | ChatGPT drafts rejected for gloss, tucked coat, thigh holster, built-in armour; accepted turnaround: matte, coat outside, holster right waist, armour modular | CHANGE-BRIEF "Design changes already made" 1–5; SOURCES CHAR-REF-01/03, CHAR-TURN | ✓ |
| B04 | 10 pose images, silhouette test, collision overlay still missing | CHARACTER-SHEET sections 2, 6 status lines; README limitations | ✓ |
| B05 | No character, no sound wired to an event, no music, no mute | TEST-REPORT required-checks table; README Controls / limitations | ✓ |
| B06 | Concept audio direction added 2026-10-09: short dry electronic tones, light radio static, squelch, rugged field electronics | CONCEPT revision history 2026-10-09 | ✓ |
| B06 | Change brief names SFX-TERMINAL-POWER-ON, event = picking up the tablet from not looking to one/two hands | CHANGE-BRIEF revision 2026-10-09 event table | ✓ (quoted verbatim on screen) |
| B07 | V01 asked for two confirmation beeps + rising tone; rejected as too sharp and explosive, like an electronic transient | SOURCES V01 row; prompt A1 | ✓ |
| B07 | V02 = rerolls (seeds / lengths), none satisfied; then design changed to one beep + short radio static | SOURCES V02 row | ✓ (the brief said "V01, V02 too sharp"; SOURCES gives V02's reason as "none satisfied", so the film follows SOURCES) |
| B07 | Every run used CFG 1.0, so negative prompts had no effect | SOURCES "Negative prompts had no effect"; FRICTIONAL 2026-10-09 | ✓ |
| B08 | V03 prompt asks for one clear confirmation beep with a brief filtered radio static burst | SOURCES prompt A4 (opening lines quoted verbatim) | ✓ |
| B08 | seed 1145141919810, 12 steps, CFG 1.0, lcm, 2.3 s length | SOURCES V03 row; **re-read from the FLAC's embedded ComfyUI workflow while making the film** (KSampler seed 1145141919810, steps 12, cfg 1.0, lcm, simple; EmptyLatentAudio 2.3 s, batch 2) | ✓ |
| B08 | 00042 accepted with no edits; repo file byte-identical | SOURCES V03 row (MD5 check by Claude on 2026-10-09) | ✓ (not re-checked against the ComfyUI output folder for the film; that folder is not in the repo) |
| B09 | Played files are the three accepted files, unaltered, at original level; not in-engine | `listen/terminal-sfx-sequence.flac` built by plain concatenation with silence (see SOURCES.md) | ✓ (the compositor resamples the master to 48 kHz) |
| B10 | base.tscn has no audio player node; godot/ has no audio files | `base.tscn` (node list); file inventory in `gamedev-evidence.json` | ✓ |
| B10 | project.godot defines no input actions | `project.godot` has no `[input]` section | ✓ |
| B10 | Sounds are FLAC in the design folder, not yet Ogg | `design/sfx_sound/*.flac`; CHANGE-BRIEF "not yet converted to OGG" | ✓ |
| B11 | Designer built floor and side walls; Claude finished from basic shapes | FRICTIONAL 2026-10-08; SOURCES ENV-BASE-01 | ✓ |
| B11 | Steps rise 0.2 m, run 0.3 m | `base.tscn` step sizes 0.2…1.2 high, z spacing 0.3 | ✓ |
| B11 | Ramp has no mesh; matrix entries 0.5547 / 0.8321; 33.7°; equals rise over run | `base.tscn` line 80; atan(0.5547/0.8321) = 33.69°, atan(0.2/0.3) = 33.69° | ✓ (computed) |
| B12 | Normal render shows only steps; debug-collision render shows the ramp across every step edge | `capture/stairs_side*.png` (native renders) | ✓ (debug colour changed to orange, disclosed) |
| B12 | Ramp meets first five step edges within a millimetre, ends at the sixth | `evidence/ramp-check.log`: 0.0007 m for 1–5, 0.0000 m for 6 (hit = landing) | ✓ new film-time check |
| B12 | Changing step height alone would break the match | reasoning only | labelled **untested prediction** |
| B13 | Two omni lights at x = ±3.5 under the ceiling, pale blue, energy 1.5, range 8 m; near-black environment, weak blue-grey ambient | `base.tscn` lines 5–10, 86–98 | ✓ |
| B13 | Concept asks for dark, cool tones | CONCEPT art direction note 1 | ✓ |
| B14 | Native 4K Godot render; camera added by capture script; scene static | CAPTURE.md | ✓ |
| B14 | Two cool pools of light, test chair at back wall, stairs visible | `media/B14.mp4` frames (inspected) | ✓ (checked in QC) |
| B14 | Character readability against the walls untested | CHANGE-BRIEF predicted failure 2; CHARACTER-SHEET palette status | ✓ |
| B15 | Fresh export imports; base.tscn runs 120 frames with no errors or warnings | TEST-REPORT check 1; re-run → `evidence/fresh-*.log` | ✓ |
| B15 | Same prompt + seed → identical decoded audio | SOURCES reproducibility check | ✓ (not re-run for the film) |
| B15 | No human playtest | TEST-REPORT | ✓ |
| B16 | Model → asset mapping | SOURCES "Generative models", asset log | ✓ |
| B16 | Assignment text says code-drawn art does not meet the generative-model requirement; professor confirmed Claude's basic-shape 3D builds count | assignment text, line 19: "code-drawn or SVG art written by Claude is welcome in your game, and it does not satisfy the generative-model requirement"; professor's ruling: SOURCES Claude Code row, FRICTIONAL 2026-10-08, README draft | ✓ text verified; the ruling is as the designer reports it (not in a public document) |
| B17 | Error sound: tremolo / repeated tones, designer does not know how to fix | TEST-REPORT known limitations (quoted) ; FRICTIONAL 2026-10-09 | ✓ |
| B17 | Next step: OGG → audio player → fire on tablet state change, log one trigger | FRICTIONAL 2026-10-09 "Next"; CHANGE-BRIEF failure 3 | ✓ |
| B18 | Verdict lines | recap of the above | ✓ |
| B19 | Your Turn prompt | written for this film | suggestion, not a claim |

## Corrections and omissions decided while writing

- The brief summarised V01 and V02 as "too sharp". SOURCES gives that reason only for V01; V02 is "rerolls, none
  satisfied". The film uses SOURCES' wording.
- The 10-08 raycast command was not saved (TEST-REPORT), so the film's raycast is presented as a new check.
- The 10-09 3D side experiments are outside the assignment (designer's decision) and are not shown or mentioned.
- The error sound is not final and is not played.
- Kokoro reads "Hej" closer to "Hey"; accepted.
