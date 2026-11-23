# FRICTIONAL — Assignment 7

My Assignment 6 log is in `../assignment-6/FRICTIONAL.md`.

## Entries

### 2026-11-21 to 11-22 — The one-handed tablet raise in Blender: the rig, my end pose, the in-betweens, the fingers

- **Date and what I was working on:** 2026-11-21 to 11-22. A7's rig clip: the main character raises the tablet from her left hip with one hand. The animation is keyed in Blender and played in Godot. It uses the commissioned main-character model (xz), in a copy of its Blender file (`xz_anim.blend`); the original file is untouched.
- **I tried / expected:**
  - First I had Claude make a raise directly, and played it in Blender to look at it.
  - I found it "not very natural", so we changed the method: I pose the end frame of holding the tablet in one hand myself, and Claude works out the in-between frames from the start pose on the hip.
  - I wanted the hand to be "tied" to the tablet, with the palm's position and rotation adjustable on their own, and no backwards-bending joints.
- **What happened:**
  - Claude added a `tablet` bone to the rig and hung the tablet model on it, plus a grip point `tablet_grip.l` (a small dark-red box) that the left-hand IK controller follows through a constraint.
  - My first try at posing put the hand completely wrong: the palm could not be adjusted on its own, and moving the left hand moved the right hand too. Pose X-mirror was on. Claude turned it off and made the grip point a box I can move and rotate freely.
  - I dragged the gold ring at the elbow (`c_stretch_arm.l`) and the upper arm stretched by 21%. Claude reset, hid and locked all the stretch controllers; the elbow direction is now set only with the pole controller.
  - Claude posed the fingers: the thumb on the left bezel of the screen, four fingers on the back. A mesh check found no back finger showing through the screen.
  - I asked for the eyes to look at the tablet, and Claude built eye bones that track it; I then decided to leave the eyes alone for now, and they were restored.
  - In-betweens: frames 0–5 reach, 5–7 grip, 7–16 lift and turn, 16 arrive, 18 an 8 mm overshoot, 20 settle. The original hip position was 0.417 m from the shoulder for an arm 0.379 m long, so Claude moved it forward and up to make it reachable.
  - Some clipping into the coat is fine with me.
- **What I did:** Judged the first version unnatural; posed the end pose myself (tablet position, grip, elbow direction, head angle); decided to leave the eyes alone; accepted the phase-table numbers Claude proposed ("use your current numbers in the phase table"); decided the screen lights on frame 20, after the clip has finished; decided that an interrupt cancels the clip and blends from the current pose to the next state.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5), through Blender MCP, added the `tablet` bone, the grip point and the constraints, fixed the mirror and stretch problems, posed the fingers, derived the in-betweens from my end pose, and proposed the phase-table numbers. I rejected its first version (thumbnail in `design/rejected/`).
- **What I understand now / still do not understand:**
- **Evidence and next step:** `xz_anim.blend` is not in this repo (it is the commissioned model's source file); the exported `walker-survival-shooting/godot/assets/characters/main_character/main_character.glb`; `walker-survival-shooting/tools/blender/export_main_character.py`; the phase table in CHANGE-BRIEF. Next: the sprite clip.

---

### 2026-11-22 — A front-facing pixel head breathing sprite sheet for the taskbar

(This entry was written by Codex in its own session; translated, otherwise unchanged.)

- **Date and what I was working on:** 2026-11-22. Making a head-only, front-facing pixel-art head for the taskbar, output as an 8-frame transparent PNG sprite sheet.
- **I tried / expected:** Keep the dark navy short bob, the straight fringe, the blue-grey eyes and the X-shaped hair clip on the right of the image; 56 × 56 per frame, 4 columns × 2 rows; the only change between frames is 1 pixel up or down.
- **What happened:** The Blender breathing reference image named in the request did not exist at its path, so the uploaded front image and character-three-quarter.png were used. A 1-pixel amplitude gives only two heights on an integer grid; the user confirmed repeated frames are allowed. One base head was generated, then its grid, colours and transparency were normalised, and it was copied into the frames, to avoid the facial changes that separate generations would cause. Result: 224 × 112, 15 colours, alpha only 0 and 255; with the offsets undone, the 8 frames are pixel-identical, and frame 8 differs from frame 1.
- **What I did:** The user gave the character references, the pixel style, the framing, the layout and the motion, and confirmed the 1-pixel amplitude and that repeated frames are allowed.
- **What Codex or another person contributed:** Codex used its image tool to generate a single head, then did a local nearest-neighbour downscale, fixed-palette quantisation, alpha binarisation, a one-pixel outer outline and the repeated layout; filled in one missing pixel of the X clip; and wrote a verification record.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `design/avatar/avatar-idle-front-sheet-4x2-56.png`, `avatar-idle-front-sheet-4x2-8x.png`, `avatar-idle-front-verification.json`; in SOURCES, CHAR-AVATAR-IDLE-FRONT-20261122-01. Offset sequence 0,0,0,-1,-1,-1,-1,-1. This request (4 × 2, head only) takes precedence over the existing CHANGE-BRIEF's 8 × 1 with a little neck; no game nodes or earlier design text were changed. Whether it is adopted: to be confirmed.

The user then added a front modelling-reference image of the character with facial features (in my working folder's `design/character/`, not in this repo); it was checked to be the same character's front modelling reference (not a breathing sheet) and used to review the finished look, not as input to the image tool.

Later changes (added by Claude): the sheet was adopted, with a blink added (next entry). In this repo these files are now in `walker-survival-shooting/design/avatar-sprite/`; Codex's SOURCES record was merged into AVATAR-SPRITE-02.

---

### 2026-11-22 — A blink for the pixel head, the head in the taskbar, and going through the brief item by item

- **Date and what I was working on:** 2026-11-22. A7's sprite clip (the cycle): the main character's pixel head at the far left of the tablet OS taskbar. Also going through CHANGE-BRIEF with Claude one item at a time.
- **I tried / expected:**
  - The first plan was to render a bust of the character in Blender. I changed it to having an AI draw a pixel-art head: head only, fully frontal, with the prompt written in the chat window, so my computer does not fill up with extra files.
  - I was very happy with the style Codex produced, but not sure whether the frames actually differed.
- **What happened:**
  - Claude found only two distinct images among the 8 frames: frames 1–3 are identical, frames 4–8 are the same image 1 pixel higher.
  - I asked for one blink, overlapping the head's sinking, "not one movement finished before the next starts": the eyes start closing on the 2nd–3rd frame of the sinking.
  - Claude drew half-closed and closed eyes on the low image and re-laid the frames out 8 × 1: frame 1 open (low), 2 half-closed (low), 3 closed (low), 4 half-open (high), 5–8 open (high). The original is unchanged.
  - The folder was first called `taskbar_avatar`; I found that too hard to understand, and it became `pixel_head`.
  - OpenAI's Terms of Use were checked: the output is mine, but it must be marked as AI-generated. README, the film and `ATTRIBUTION.md` say so.
- **What I did:** Chose the head in the taskbar (option A); decided head only, fully frontal; generated it with Codex; asked for the blink and set its timing; answered the brief item by item: the head's two jobs (shows the OS is running, shows whose tablet it is), the AnimationTree on the IDLE tick, "light only once in place" for every switch, the demo tablet keeping its 0.35 s slide, frame strips from the player camera plus a front camera; confirmed the 6 predictions and 7 short answers one by one (prediction 1 with my addition: "the one-handed raise is triggered by a signal anyway, not looped").
- **What Claude or another person contributed:** Codex (OpenAI) generated the head and laid it out 4 × 2 (previous entry). Claude Code (Claude Opus 5.5) checked how the frames differ, drew the blink eyes with Pillow and re-laid the frames, checked the terms, merged Codex's record into SOURCES, and assembled my answers into the brief and translated it into English.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/design/avatar-sprite/` (Codex's original sheet, master, generation prompt, verification JSON, the sheet with the blink); `walker-survival-shooting/godot/computer_system/tablet_os/system/pixel_head/`; SOURCES AVATAR-SPRITE-02 and the Avatar prompt appendix; CHANGE-BRIEF (a399a863). Next: the assignment's steps, through at least step 10.

---

### 2026-11-22 — Assignment steps 1–10: start point, test wrapper, CLAUDE.md, pins, the two clips, wiring, edge tests, mutations, empty cache

- **Date and what I was working on:** 2026-11-22. Doing A7 in the assignment's order, in this repo's A7 folder (the English copy). My instruction: "First do the assignment's minimum, through at least step 10; then, if we still have time, add more animations."
- **I tried / expected:** The start point is my working folder's current project (after A6, with the tablet OS and the new tablet model), comments translated into English. I expected the earlier tests to give the same results under the new wrapper.
- **What happened:**
  - Start point (8d1c8a73) and the A7 test wrapper (e466c00d; one more rule than A6: "Failed loading resource" in the log also fails). Baseline 55 / 24 / 157 / 27 / 110 / 41 PASS. The commit message said 56 / 25 because the summary line was counted too; corrected in the review commit and TEST-REPORT.
  - Step 1: CLAUDE.md was revised by a subagent (Claude Opus 5.5) started from my main session with prompt-1.txt, committed unedited (eccdb597), then the review (a36cb0ce) and the Headless facts addendum (f37486ee). In the review every class and property name was checked against Godot 4.7.2's ClassDB; all exist.
  - Behaviour pins (38) committed before the animation change (ac082671); later switched to `Input.parse_input_event` input with the same expectations.
  - Both clips with read-back tests (e227a915): pixel head 37, raise 25. Godot's importer drops repeated keys, so the tablet bone keeps only frames 0, 7–17 and 20, and the "every frame keyed" check became an information line. The head's playback check first sampled exactly on key times; it now reads between two keys.
  - Wiring (0f7de1f0): only the character's AnimationTree decides where the tablet is (a BoneAttachment3D follows the `tablet` bone); the three old slots and the 0.35 s slide are gone; state-machine structure test 26.
  - Measured: the screen lights 2 physics frames after frame 20 (0.70 s instead of 0.667 s), recorded in a brief revision (740003ed). The brief's prediction 6 said only 1 frame.
  - Edge tests (126): one frame before, on and after each phase boundary, each with a short and a long press. A 0.4 s long press does not fit inside the 7-frame startup, so the test lowers the long-press time to 0.095 s.
  - Mutations (f1987ba3), each in its own sparse git worktree, removed afterwards. The track-property mutation showed the head's property check was too weak (it passed as long as a property named `frame` existed); it now checks the property the track itself names (6342b5de).
  - `.godot/` deleted and re-imported from an empty cache: all 11 tests pass and the loop modes survive (4c92784d).
- **What I did:** Chose the start point; decided the shader keeps its Chinese comments (an exception for this assignment); "minimum first"; looked at the baseline and each step's results.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5) wrote the wrapper, every test, the export script, the wiring code, the mutation script and the frame-strip tools, translated the start project's comments, and ran all headless tests; Step 1's CLAUDE.md draft came from a subagent it started.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/scripts/run-test.sh`, `scripts/mutate.sh`, `godot/tests/`, `logs/`, `TEST-REPORT.md`, `prompt-1.txt`, `session-1.jsonl`. Next: frame strips and TUNING.

---

### 2026-11-22 — Frame strips, TUNING r1 and r2, human checks

- **Date and what I was working on:** 2026-11-22. Movie Maker frame strips of the raise and the head, revisions driven by what I saw, then playing the game myself to check.
- **I tried / expected:** I run the Movie Maker commands myself; Claude picks frames from the log and builds the strips. My verdict comes first, Claude's reading after it.
- **What happened:**
  - r0: from the player camera, behind her, the body hides the tablet for the whole raise. I said to turn the camera "in the game", not to move the original camera, so the front strip turns the player's own camera 180 degrees in game. My verdict: I had already looked at the animation in Blender; no problem.
  - PowerShell mis-decoded the `×` in Godot's log into garbage; Claude fixed it and amended the unpushed commit. Since then the console is set to UTF-8 before each capture.
  - r1: the screen lit late because on the frame the state machine entered the raise, the clip stayed at 0. Turning `reset` off removes that frame, but a second raise after an interrupt would then start mid-clip, so it was not used; instead code starts the raise on the press frame. Prediction and result agree: the screen lights on movie frame 54 instead of 55, with the same poses. While comparing, we found the preview logged before the AnimationTree updated, so r0 and r1 labels were one clip frame early; the preview now runs last, and later strips are labelled correctly. My verdict: keep.
  - r2 (a problem I saw in the game): where and how the tablet sits on the hip did not match my idea, and the hand had to twist to a strange place to take it. I posed a new stowed pose in Blender: the tablet hangs upright, turned 90 degrees, more like how we normally hold a tablet. I saved with Ctrl+S, but when Claude read the file it was back as before: Blender MCP's viewing tool re-evaluated the animation and wiped my unkeyed pose, and my I key had not landed. That was the tool, not my operation. Claude read my live pose and keyed it on frames 0 and 7 in code. Observation and prediction were written first, then the change: Claude re-derived the reach, lift and turn keys and re-exported; all 11 tests kept their counts. The first r2 capture saved no frames because the command was missing the step that creates the folder (Movie Maker does not create it and gives no error). After re-capturing, the result matched the prediction. My verdict: keep.
  - Human checks: all four fine. I noticed the character stands still while raising and can only walk once the clip is over; that is the brief's rule. I decided to keep it for this assignment and later change it to walking while raising.
  - Where we differ: the 8 mm overshoot is dropped in the game, which I accept, no change; not seeing the whole tablet from behind is not a fault, because the camera orbits freely around the character and the animation is made for every angle.
  - I noticed putting the tablet back on the hip looks natural, though we never made that animation. Claude explained it is the state machine's 0.2 s cross-fade, not a keyed clip.
- **What I did:** Ran every Movie Maker capture (r0, r0-front, r1-front, r2-front, pixel head r0); wrote each verdict; chose r1 as a revision; posed r2's new stowed pose in Blender; did the four human checks; answered both differences.
- **What Claude or another person contributed:** Claude Code (Claude Opus 5.5) wrote the preview scenes and the frame-picking script, read the logs and built the strips, found the cause of the late screen and made the r1 change, keyed my pose in Blender and re-derived r2's in-betweens, and drafted and translated TUNING and TEST-REPORT.
- **What I understand now / still do not understand:**
- **Evidence and next step:** `walker-survival-shooting/captures/tablet_raise/` (r0, r0-front, r1-front, r2-front), `captures/pixel_head/r0/`, `logs/tablet_raise_*.log`, `TUNING.md`, `TEST-REPORT.md`. Next: README, SUBMISSION, the film, push, tag `zhe-l-a7`.

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-11-22 | First A7 upload: the whole A7 history in work order (start point, wrapper and baseline, brief, CLAUDE.md draft and review, pins, both clips with read-backs, wiring, edges, mutations, fresh cache, strips r0/r1/r2 with TUNING and my verdicts, human checks, FRICTIONAL, README), plus the film records and the README film section. |
