# CHANGE-BRIEF — Assignment 7: animation

Written by me (decisions, phase table, cycle spec, predictions); Claude Code organised my decisions into this form and drafted the predictions and short answers, which I went through and confirmed one by one. My working draft is in Chinese; this is the English version.

## Shared facts

- Character: my main-character model `xz.blend`, commissioned for this project and used with permission. Animation is keyed in a working copy, `xz_anim.blend`, in Blender and exported to Godot as a `.glb` (the imported 3D route).
- Frame rate: 30 fps. Frames are numbered from 0; frame N is at N / 30 s.
- I describe or pose each motion; Claude keys it in Blender.
- Sprite clip: a small character head in the corner of the tablet OS taskbar (see "Clip: pixel head").
- Which clip loops: the sprite clip (pixel head) loops; the one-handed tablet raise is the committing action.
- Godot version: 4.7.2-stable. Godot 4 class and property names only.
- Clips are resources: the imported rig clips live in the `.glb` (owned by the character scene); the head clip lives in the head scene's `AnimationPlayer`. No clip is built in code at runtime.

## The two clips

| | Pixel head (taskbar) | One-handed tablet raise |
|---|---|---|
| What it communicates | The tablet OS is on and idle; every time the player takes the tablet out, they see their own character | The character is taking the tablet out, and when the tablet actually becomes usable |
| Why the player needs it | Two jobs (my decision): a moving head shows the tablet OS is running and not frozen (a status cue); and it shows whose tablet this is (every player has their own tablet; later, in co-op, one each) | Taking the tablet out costs time: while raising it you cannot walk or jump, and the screen only lights once the tablet is in hand (a gameplay trade-off) |
| Object it plays on | A `Sprite2D` in the tablet OS taskbar (head scene in `computer_system/tablet_os/system/pixel_head/`) | The player character (the xz model's `Skeleton3D` in `humanoid.tscn`); `TabletDevice` hangs on the `tablet` bone and follows it |
| Route | Sprite2D + an `AnimationPlayer` frame track (keys `frame`) | Imported 3D rig (keyed in Blender, exported as `.glb`) |
| Why this route | Only 8 cells and one loop: one integer track is the most direct, and the read-back can check that the track points at `Sprite2D:frame`, its update mode and its frame range | The character is already a commissioned 3D model with a full skeleton and IK controllers; the fingers and arm have to fit the tablet, which only the Blender controllers make precise |
| The one authority | The `AnimationPlayer` in the head scene, autoplaying and looping. It reads no game state | The character's `AnimationTree` (state machine). It reads `Humanoid.get_tablet_hold()` (`humanoid.gd`) and changes state when the hold state changes |
| Cycle or committing action | Cycle | Committing action (phase table below) |

## Clip: pixel head (sprite sheet, loops)

### Task

A looping character head in the corner of the tablet OS taskbar. Eight frames side by side in one sprite sheet; in Godot a `Sprite2D` (`hframes` = 8, `vframes` = 1) with an `AnimationPlayer` that keys `frame` in order, discrete updates, looping.

### Design (2026-11-22)

| Item | Content |
|---|---|
| Image source | Pixel art generated with Codex: `avatar-idle-front-sheet-4x2-56.png` (4 × 2, transparent, 15 colours; frames 1–3 are identical, frames 4–8 are the same image moved up 1 px). Claude drew half-closed and closed eyes and re-laid the frames out 8 × 1: `avatar-idle-front-blink-8x1-56.png`. This replaced the earlier plan to render the head from Blender |
| Framing | Head only (with a little neck), fully frontal (my decision) |
| Motion | Head: low on frames 1–3, 1 px higher on frames 4–8 (after frame 8 it drops back: the "sink"). Eyes: frame 1 open, 2 half-closed, 3 closed, 4 half-open (the same frame the head rises), 5–8 open. The blink overlaps the head's sink and rise instead of one motion finishing before the next starts (my decision: start closing the eyes on the 2nd–3rd frame after the head starts to sink) |
| Frame count | 8 frames, laid out 8 × 1 |
| Speed | 4 frames per second; one loop is 2 s |
| Cell size | 56 × 56 px pixel art, shown at its native size in the taskbar |
| Position | Far left of the taskbar, left of the window buttons |
| Seam | Frame 8 goes straight back to frame 1; the first frame is not repeated |

- It only displays; it decides no game state. When the tablet is put away the tablet OS canvas stops drawing, so the head is not drawn either.
- Its code lives in `computer_system/tablet_os/system/pixel_head/` (part of the system UI, not an app).

### The sheet: provenance and slicing

| Item | Content |
|---|---|
| Source | Generated asset, logged under Assignment 2's rules in SOURCES.md (AVATAR-SPRITE-02). Codex (OpenAI) generated one front-facing master head with its image tool, then in code reduced it to a 56 × 56 pixel grid, copied it into 8 cells and moved it 1 px; Claude drew the two blink eye states with Pillow |
| Author | Me (generated with Codex, edited by Claude at my request) |
| Licence | OpenAI Terms of Use (effective 2026-01-01, read on 2026-11-22): the user owns the Output, and OpenAI assigns its rights in the Output to the user; the user must review Output before using or sharing it and must not present it as human-made. OpenAI's Sharing & Publication Policy (2022-11-14) asks that AI-generated content shared on social media be clearly marked as AI-generated. So it can go in a public repository and a published film, and README, the film and `ATTRIBUTION.md` all say the head is AI-generated (Codex image tool) and edited by Claude |
| Date checked | 2026-11-22 |
| Original as downloaded | Codex's `avatar-idle-front-sheet-4x2-56.png` (4 × 2, 224 × 112), committed unchanged in `design/avatar-sprite/`. The image tool's first 1254 × 1254 output was not saved; Codex kept the reduced `avatar-idle-front-master-56.png` |
| Sheet used in the game | `avatar-idle-front-blink-8x1-56.png` (448 × 56), in `computer_system/tablet_os/system/pixel_head/` with the head scene and `ATTRIBUTION.md` |
| Cell size | 56 × 56 px, no padding between cells |
| Grid | `hframes` = 8, `vframes` = 1 |
| Frame order | Left to right, 0–7, matching frames 1–8 under "Motion" |
| Credits file | `ATTRIBUTION.md` next to the sheet: source, author, licence, date checked |
| Registration | In the original the head sits in only two positions in its cell, low and 1 px up; that is the intended bob, not drift. The frame strip checks for any other shift |

### Cycle spec

| Item | Content |
|---|---|
| Frame count and rate | 8 frames, 4 fps |
| Clip length | 2.0 s |
| `Animation.step` | 0.25 s (one frame at 4 fps) |
| Keys | At 0.00, 0.25, 0.50 … 1.75 s, `frame` = 0 to 7 in order |
| Loop mode | `Animation.LOOP_LINEAR` |
| Update mode | `Animation.UPDATE_DISCRETE` |
| Seam rule (frame track) | No duplicate across the wrap: the last key is `frame` = 7 and it wraps to `frame` = 0, which differ (head height and eyes); the gap from the last key (1.75 s) to the clip's length (2.0 s) is 0.25 s, equal to the key interval |
| Frame range | Only 0–7; never a cell past the 8th (the sheet has 8 cells) |

## Clip: one-handed tablet raise (`tablet_raise_one_hand`, committing action)

### Task

From standing, the character takes the tablet off her left hip with her left hand and raises it to chest height to look at the screen. I posed the end pose in Blender (`tablet_hold_one_hand`); Claude worked out the in-between frames from the hip start pose.

### Phase table

Frame rate 30 fps; `Animation.step` = 1/30 s (≈ 0.0333 s, one frame). Frames 0–20, 21 frames in all, 20 / 30 ≈ 0.667 s. Each phase includes its first frame and excludes its last; the last phase includes frame 20. Frame 0 is the physics frame on which a short press changes `Humanoid`'s hold state from put away to one-handed.

| Phase | Begins on | Frames | Time (s) | What the player may do | What the game reads | What the animation does |
|---|---|---|---|---|---|---|
| Startup | 0 | 0–6 | 0.000–0.233 | No walking, running, jumping, aiming or interacting; can interrupt with Tab (short press = put it back, long press = switch to two hands) | Hold state = one-handed; screen dark, not clickable | 0–5: the left hand reaches for the tablet on the hip, fingers opening slightly; 5–7: the hand grips the tablet's edge and the fingers close into the grip |
| Active | 7 | 7–15 | 0.233–0.533 | Same | Same | 7–10: the tablet is lifted straight up about 10 cm; 10–16: it moves forward while turning, screen towards the face; 8–16: the head slowly lowers |
| Recovery | 16 | 16–20 | 0.533–0.667 | Same | Frames 16–19: screen still dark, not clickable; frame 20: screen lights and becomes clickable | 16: reaches the end pose; 18: overshoots 8 mm along the motion; 20: back on the end pose, settled |
| (Afterwards: holding one-handed) | after 20 | — | — | Can walk; no running, jumping, aiming or interacting (the existing rule, unchanged) | Screen lit, clickable | Holds the end pose |

**Keyed gameplay fact: on frame 20 (0.667 s, the clip's last frame) the screen lights and becomes clickable.** On frame 19 and before it is dark and not clickable; only when the clip has finished, on frame 20, does it light (my decision: "light it after it has been picked up, once the animation has finished"). The bottom-right demo tablet still slides in on its own over 0.35 s, but its screen also waits for frame 20 before it lights and becomes clickable (my decision).

### What is already set up

- Start pose: left hand hanging at the side, tablet on the outside of the left hip. So that the hand can reach it, the hip position of the tablet was moved 7 cm forward and 5 cm up from the first draft (about (0.29, −0.07, 0.88) m in Blender's world space). The old position was 0.417 m from the shoulder; this arm is 0.379 m long.
- End pose: the tablet position, grip, elbow direction and head angle I posed; the fingers were posed by Claude (thumb on the left bezel of the screen, four fingers on the back, no back finger showing through the screen).
- The tablet follows a `tablet` bone in the rig; the left hand follows the tablet through a grip bone, `tablet_grip.l`.

### One authority

- In the game, the tablet (`TabletDevice`) hangs under a `BoneAttachment3D` that follows the `tablet` bone; only the animation decides where the tablet is.
- The code in `humanoid.gd` that slides the tablet between three slots over 0.35 s (`_update_tablet_visual()`), and the three slots `TabletHipSlot` / `TabletOneHandSlot` / `TabletTwoHandSlot`, are removed.
- The screen no longer lights when "the tablet has slid into place"; it lights when the clip reaches frame 20 (its last frame).

### Testable rules

- While raising (frames 0–20): no walking, running or jumping.
- Interrupts: if the player presses a key mid-raise to change state, the current clip is **cancelled and the character blends from its current pose into the next state's animation**. Example: a long press halfway through the one-handed raise (switch to two hands) immediately blends into the two-handed state from the current pose, without finishing the one-handed raise first.
  - The blend from the current pose takes 6 frames (0.2 s).
  - An interrupted one-handed raise never reaches frame 20, so the screen does not light (I confirmed this); if the interrupt goes to two hands, the two-handed rule decides when it lights.

### Import settings (where the loop mode lives)

- One `.glb` (character + skeleton + actions) exported from `xz_anim.blend` into `assets/characters/main_character/`, with an `ATTRIBUTION.md` beside it (commissioned for this project, used with permission). The reference tablet model in Blender is not exported; only the `tablet` bone's animation is.
- Each action's loop mode is set in the importer's per-animation settings (saved in the `.glb.import` file), not edited by hand in the imported scene: `tablet_raise_one_hand` = no loop (`Animation.LOOP_NONE`); the hold poses do not loop either.
- Proof that it survives: delete the `.godot/` import cache, run `--import` again, and run the read-back test that reads the loop mode.
- To handle on export: the character is scaled up 5.07× in Blender (otherwise the tablet hanging on the bone would be scaled up too); Blender and Godot use different axis conventions (the tablet may need a fixed rotation).

## State machine (the tablet-raise side)

(I agreed to this, 2026-11-22.) The tablet logic I already built in `humanoid.gd` (put away / one-handed / two-handed, what a short and a long press do) does not change. This state machine is a separate layer: an animation state machine that only decides which animation plays, following that logic. It is the character's `AnimationTree` with an `AnimationNodeStateMachine` as its root. It is the one authority over the skeleton; because the tablet follows the `tablet` bone, it is also the one authority over the tablet's position.

| State | Plays |
|---|---|
| `hip` (put away) | The put-away hold pose (tablet on the left hip; frame 0 of the raise) |
| `raise_1h` (raising one-handed) | `tablet_raise_one_hand`, frames 0–20, no loop |
| `hold_1h` (holding one-handed) | The one-handed hold pose (my end pose) |
| `hold_2h` (holding two-handed) | The two-handed hold pose. I have not posed it yet, so the one-handed hold pose stands in for it (my decision: finish the assignment minimum first, then add animation); it will be replaced in a dated revision |

The transitions follow the hold-state table in `humanoid.gd` (`_next_tablet_hold()`: put away + short press → one-handed, + long press → two-handed; one-handed + short → put away, + long → two-handed; two-handed + short → one-handed, + long → put away):

| From → to | Condition | Cross-fade | Switch |
|---|---|---|---|
| `hip` → `raise_1h` | Hold state becomes one-handed | 0 (same start pose) | Immediate |
| `raise_1h` → `hold_1h` | Clip finished (frame 20) | 0 | At end (`SWITCH_MODE_AT_END`) |
| `raise_1h` → `hip` | Hold state becomes put away (short press mid-raise) | 6 frames (0.2 s) | Immediate (interrupt) |
| `raise_1h` → `hold_2h` | Hold state becomes two-handed (long press mid-raise) | 0.2 s | Immediate (interrupt) |
| `hip` → `hold_2h` | Hold state becomes two-handed | 0.2 s | Immediate |
| `hold_1h` → `hold_2h` | Hold state becomes two-handed | 0.2 s | Immediate |
| `hold_2h` → `hold_1h` | Hold state becomes one-handed | 0.2 s | Immediate |
| `hold_1h` → `hip` | Hold state becomes put away | 0.2 s | Immediate |
| `hold_2h` → `hip` | Hold state becomes put away | 0.2 s | Immediate |

- Apart from the at-end transition, every transition uses `ADVANCE_MODE_AUTO` with an advance expression such as `get_tablet_hold() == 1`. The expression is evaluated against `advance_expression_base_node`, which is set to the character's root node `Humanoid` (`humanoid.gd`); without it the expression silently fails.
- The `AnimationTree` only reads the hold state; it writes no game state (presentation reads, never writes).
- Screen lighting: every physics frame `Humanoid` reads which state the state machine is in. The rule is always "light once in place" (my decision): it lights when the raise finishes and the machine enters `hold_1h`; for every other transition the screen is dark during the 6-frame blend and lights when the blend ends and the machine is in `hold_1h` / `hold_2h` (so switching between one and two hands now goes dark for 0.2 s, unlike the current game); on the frame the state becomes `hip` the screen goes dark (as now).

## The two clocks

| Node | `callback_mode_process` | Advances on |
|---|---|---|
| Character `AnimationTree` | `AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE` (default; my decision) | Process tick |
| Head `AnimationPlayer` | `AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE` (default) | Process tick |

- The project uses no `AnimatedSprite2D` (it can only advance on the process tick and has no such setting).
- The game reads one keyed gameplay fact: "the raise has finished → the screen lights and is clickable". `Humanoid` reads it on the physics tick (`apply_intent()` is called by the brain from `_physics_process()`).
- The character's `AnimationTree` advances on the process tick and the game reads on the physics tick, so the clocks differ. If the state machine enters `hold_1h` during a process frame, the game sees it on the next physics frame. Largest disagreement: the larger of one rendered frame and one physics frame (1/60 s ≈ 0.017 s). At 60 fps rendering about 0.017 s; if rendering drops to 30 fps, about 0.033 s (one rendered frame then advances the clip by 2 frames).
- Headless tests run with `--fixed-fps`, where a process frame and a physics frame are the same length, so the tests are deterministic; the real-game disagreement can only be judged in play.
- The head clip produces no gameplay fact, so its tick does not affect the game.
- No method track is used to make the clocks agree (method tracks are deferred).

## Boundaries

Unchanged: collision, movement speeds, input bindings, jumping, interaction, the hold-state table in `humanoid.gd`, my Assignment 5 shaders (the two hand-written files in `shaders/`), my Assignment 6 effects (both dusts), every other object in the base scene, and the rest of the tablet OS.

Changed by this brief (only these):

1. The tablet's position is driven by the animation: the 0.35 s slide in `_update_tablet_visual()` and the three slots (`TabletHipSlot` / `TabletOneHandSlot` / `TabletTwoHandSlot`) are removed, and `TabletDevice` hangs under a `BoneAttachment3D` on the `tablet` bone.
2. The screen-lighting rule: from "the tablet has slid into place" to "the one-handed raise has finished (frame 20)", plus the "light once in place" rule for the other transitions.
3. No walking, running or jumping while raising (frames 0–20). This is new; the one-handed rule after the raise is unchanged.
4. The character's capsule look is replaced by the xz model (under `Visual/human_model`; the collision capsule is unchanged).
5. Existing test expectations that depend on the 0.35 s slide change: the take-out, put-away and mid-way interrupt cases in `tests/screen_glow_check.gd`, and the "screen stays lit between one and two hands" case (Claude lists them one by one before writing the pins).
6. The bottom-right demo tablet (`screen_tablet.gd`, which slides in by code): its 0.35 s slide is unchanged; its screen now waits for frame 20 of the raise before it lights and becomes clickable (my decision).
7. The pixel head is added at the far left of the tablet OS taskbar.

Presentation (animation, the pixel head, the demo tablet) may read game state; it never writes it.

## The evidence split

| Rule | Checked by |
|---|---|
| The head track points at `Sprite2D:frame`, discrete updates, frames only 0–7, key times, `LOOP_LINEAR`, `step` = 0.25, no duplicate across the seam | Read-back test |
| Every rig-clip track resolves to a real bone; key times land on the phase table's frames; `step` = 1/30; `LOOP_NONE` | Read-back test |
| The loop mode survives an empty import cache | Delete `.godot/`, re-import, re-run the read-back |
| The state machine's states, transitions and the clip each state plays match the table above | State-machine structure test |
| Screen dark on frame 19 and lit on frame 20; no walking or jumping while raising; an interrupt in each phase switches immediately | Edge tests (every phase boundary, and one interrupt in each phase) |
| Behaviour outside this change is unchanged (landing dust, ambient dust, the switch, the assets, the other screen-glow cases) | Behaviour pins committed before the change and re-run after |
| The motion reads right: the tablet follows the hand, no bad clipping, the timing | Movie Maker frame strip + my own eyes in the running game |
| The head does not jump within its cell (registration) | Frame strip + my own eyes in the running game |

## The frame strip

- Background: a real stretch of the subway base (near the player spawn, with the walls and ceiling lights in frame).
- Cameras (my decision): the main strip uses **the player's game camera** (third person, what the player actually sees), and my verdict is based on it; a second strip from a **front camera** shows the hand, tablet and face in detail and also serves the film.
- Rendered with Movie Maker at 30 fps. Trigger frame = the frame on which a short Tab press changes the hold state to one-handed (clip frame 0).
- Frames to read and what each should show:

| Frame | Should show |
|---|---|
| 0 | Standing, left hand down, tablet on the left hip |
| 5 | Left hand at the tablet's upper back corner, fingers slightly open |
| 7 | Active begins: hand gripping, tablet still on the hip |
| 10 | Tablet lifted straight up about 10 cm |
| 14 | Tablet front-left of the body, turning |
| 16 | Recovery begins: end pose reached, head lowered |
| 18 | 8 mm overshoot (barely visible) |
| 20 | Settled; the screen lights |

## Predicted failures (drafted by Claude, confirmed by me one by one, 2026-11-22)

1. The one-handed raise is triggered by the hold-state change and plays once; it does not loop (my words), so its loop mode must be "no loop". If that setting is only edited in the imported scene and not written into the `.glb` import settings, a re-import wipes it → delete the `.godot/` cache, re-import, and have the read-back test read the loop mode.
2. Exporting only the deform bones changes the name or hierarchy of the `tablet` bone or the finger bones, so some tracks point at bones that do not exist; nothing moves and nothing errors → the read-back test checks, track by track, that each resolves to a real bone.
3. Once hung on the bone, the tablet is scaled up 5× or turned 90° → obvious in the frame strip; plus a behaviour test that checks `TabletDevice`'s global scale is 1.
4. The old `_update_tablet_visual()` is not fully removed, so code and animation both write the tablet and it jumps between the hand and a slot (two authorities) → frame strip + a test that the tablet's position always equals the bone's.
5. The head's frame track is left on continuous updates, or `step` is left at the default 1/30 → the read-back test checks the update mode and `step`.
6. The screen lights too early (e.g. on frame 16, when the tablet arrives) or too late (the animation on the process tick and the logic on the physics tick, read a frame or two late) → edge tests check that frame 19 is dark and frame 20 is lit.

## Short answers (drafted by Claude, confirmed and understood by me one by one, 2026-11-22)

1. **Which route does each clip use, and what does that route's read-back see that the other route's does not?** The head uses Sprite2D + an `AnimationPlayer` frame track: the read-back sees the track pointing at `Sprite2D:frame`, each key's integer value and the update mode; with `AnimatedSprite2D` the frame order lives in a `SpriteFrames` resource and there is no such track to read. The raise uses an imported 3D rig: the read-back sees the bone name of every bone track and the loop mode stored by the importer; a 2D cutout rig has no import-settings layer.
2. **If your frame track is left on continuous updates, what does the sprite show between two keys, and why?** Between two keys the engine interpolates between the two integers and sets `frame` to an in-between value (rounded, so the switch comes early or late), so the frames change at the wrong times and the rhythm is no longer one cell every 0.25 s.
3. **What will `Animation.step` be, and what happens to your key times if you leave it at its default?** 1/30 s for the raise and 0.25 s for the head. The editor snaps keys to `step`; if the head were left at the default 1/30, 0.25 is not a whole multiple of 1/30, so keys would snap to 0.2333 or 0.2667 s, off the cycle spec.
4. **Which node is the one authority over each animated node, and what else in your project could write to it?** Skeleton and tablet: the character's `AnimationTree`; the one thing that could fight it is the old `_update_tablet_visual()` (removed). The head `Sprite2D`'s `frame`: the head scene's `AnimationPlayer`; nothing else in the tablet OS writes it.
5. **Which tick does each clip advance on, and which tick does gameplay read the fact your committing action's active window depends on? If they differ, what is the largest disagreement in seconds?** The `AnimationTree` advances on the process tick; the game reads "the raise has finished" on the physics tick. The largest disagreement is the larger of one rendered frame and one physics frame: about 0.017 s at 60 fps, about 0.033 s at 30 fps. The head also advances on the process tick, but the game does not read it.
6. **For your cycle: what is the seam rule for its track type, and what would a duplicated frame at the wrap look like in play?** Frame track: no duplicate across the wrap, and the gap from the last key to the length equals the key interval. If frame 8 were the same as frame 1, the head would hold one extra beat there (0.25 s becoming 0.5 s), a hitch every loop.
7. **If your rig is imported: where does loop mode have to live so that a reimport keeps it, and how will you prove it survived an empty import cache?** In the importer's per-animation settings (`.glb.import`). Proof: delete the `.godot/` cache, re-import, and the read-back test still reads `LOOP_NONE`.

## Priorities (my decision, 2026-11-22)

1. **Finish the assignment minimum first**: one looping sprite-sheet clip plus one rig clip (the one-handed raise, the committing action).
2. Then, before the due date, add as many of the planned animations below as I can.
3. However many get done, the film shows the whole tablet animation set (the finished ones shown, the rest described as the plan).

## Every hold change has a motion: cross-fade to a hold pose

(I agreed to this, 2026-11-22.) With the tablet driven by animation, each of the 6 tablet transitions (between put away / one-handed / two-handed) needs a motion:

- Each hold has a **hold pose** (a one-frame clip): put away (tablet on the left hip), one-handed (my pose), two-handed (not posed yet; the one-handed pose stands in).
- In the `AnimationTree` state machine each hold is a state. Transitions between them use a **6-frame (0.2 s) cross-fade**: from the character's **current** pose (whatever frame the previous animation was on) to the target state.
- Put away → one-handed has its own clip, `tablet_raise_one_hand`; the other 5 transitions use "cross-fade to the target hold pose" for now. Each time a dedicated clip is made, it replaces the matching cross-fade.
- Interrupts (e.g. a long Tab press before the one-handed raise finishes) follow the same rule: an immediate 6-frame cross-fade from the current pose to two hands.
- Known limit: a cross-fade blends two skeleton poses, so during the 0.2 s the hand may drift slightly off the tablet's edge (to be measured once it is in Godot).

## Planned animations (as many as possible before the due date)

| Animation | Use | Status |
|---|---|---|
| One-handed raise | Put away → one-handed | Done in Blender |
| Two-handed hold pose | Two-handed state | Not posed yet (I pose it) |
| Two-handed raise | Put away → two-handed | Planned |
| One → two hands | Switch to two hands | Planned |
| Two → one hand | Switch to one hand | Planned |
| Put away from one hand | One-handed → put away | Planned |
| Put away from two hands | Two-handed → put away | Planned |
| Jump | Take-off, air, landing | Planned |
| Walk + one-handed hold | One-handed allows walking: legs walk, upper body holds the tablet; needs an animation layer (bone filter) | Later (no walk animation yet) |

## Revision history

### 2026-11-22 — three things the first version did not name (found in the CLAUDE.md review)

1. **First person keeps the tablet.** Today `set_visual_visible(false)` hides the whole `human_model` in two-handed first person. With the tablet now on a bone inside the model, that would hide the tablet too. Change: it hides only the model's `MeshInstance3D` nodes, not the skeleton, so the tablet stays visible. (Adds to Boundaries item 4.)
2. **The tablet's node path changes** from `Visual/TabletDevice` to `Visual/human_model/.../Skeleton3D/TabletBone/TabletMount/TabletDevice`. `TabletMount` carries a fixed offset measured in Godot (scale 1 / 5.0684, +90 degrees about X, the same on every key frame), so the tablet keeps its real size. `screen_glow_check.gd`'s screen path follows the move. (Adds to Boundaries items 1 and 5.)
3. **How the pieces talk** (no new rule, only the means): `Humanoid` reads the state machine's current state and whether a blend is still running from the `AnimationTree` playback (`get_current_node()`, `get_fading_from_node()`); the brain passes the held screen's lit state to the demo tablet every physics frame; "no walking, running or jumping while raising" is a query on the body, `Humanoid.is_raising_tablet()`, that the brain's input filter asks.

### 2026-11-22 — measured: the game reads "raise finished" 2 physics frames late (prediction 6 came true)

Wired up and traced frame by frame at 60 fps: the short press is read on physics frame N (clip frame 0). The state machine enters `raise_1h` in that frame's process step at position 0.0, and on the next process frame the position is still 0.0 (its first frame in the new state does not advance the clip). From then on the clip advances 1/60 s per frame, reaches its end and switches to `hold_1h` in the process step of frame N + 41, and `Humanoid` reads it on physics frame N + 42. So the screen lights 0.70 s after the press instead of 0.667 s: 1 frame from the state machine's first-frame stall, 1 frame from the two clocks (the clip on the process tick, the read on the physics tick). The brief's own estimate (at most one rendered frame, about 0.017 s) missed the stall. The tests pin what was measured (`screen_glow_check.gd`: 0.667 s + 2 frames). Whether to keep this 0.033 s or remove it is my decision, still open.
