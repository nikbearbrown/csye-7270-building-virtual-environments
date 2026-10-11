# CHANGE-BRIEF.md — what Assignment 2 changes in the slice

Append-only, the same discipline `CONCEPT.md` and Assignment 1's brief use:
later revisions are added below, earlier ones are never rewritten.

---

# Revision 2.0.0 — 2026-10-03 — the plan, written before any art or sound exists

**Where this sits in the order.** `CHARACTER-SHEET.md` was written earlier
today and is the specification this brief implements. The music was generated
on 2026-10-01, *before* either document existed; the art and the sound effects
have not been generated at all yet, so for everything except the music this
brief comes first. That split is recorded as it happened in `FRICTIONAL.md`.

## 0. What is **not** changing

**Every gameplay number is frozen.** `tuning.gd` is untouched: speed 160,
jump −320, gravity 960, coyote 6, buffer 6, air jumps 1, air dashes 1, dash
speed 400, dash 10 ticks, attack 16 ticks (4 windup / 9 active / 3 recovery),
reach 30. Level geometry, enemy patrols and trap timings are untouched.

This is deliberate and it is the point of the exercise. The assignment compares
the slice before and after its assets. If the tuning moved at the same time, the
comparison would measure two things at once and prove neither. **If the new art
makes the game feel different, that is the art doing its job — not a number.**

Also unchanged: the collider (18 × 28 at (0, −14)), the collision layers, and
the swing hitbox geometry.

## 1. The changes

### C1 — Texture filter set to nearest

**What.** Add `rendering/textures/canvas_textures/default_texture_filter=0` to
`project.godot`. There is no `[rendering]` texture entry today
(`godot/project.godot`), so the project is on the linear default.

**Why.** `CONCEPT.md` revision 1.2 commits to pixel art, and the assignment
names this setting specifically. Without it every generated frame is blurred by
bilinear filtering and the 1 px outline of `CHARACTER-SHEET.md` section 3 turns
into a 3 px smear — which would destroy the one colour that carries the
character against the cream sky.

**Predicted failure.** The project renders 640 × 360 logical with
`canvas_items` stretch into a 1280 × 720 window — an exact 2×, which is safe.
The film renders at 3840 × 2160, an exact 6×, also safe. But any **non-integer**
scale (a resized window, a 1366 × 768 laptop) puts nearest-neighbour sampling on
fractional boundaries and some sprite rows become 2 px tall while their
neighbours stay 1 px. The character then visibly shimmers while walking.

**Check.** Screenshot the same idle frame at 1280 × 720 and at one deliberately
awkward window size, and compare the helm's pixel rows. If the awkward size
shimmers, that is recorded as a known limitation of windowed play rather than
fixed by turning filtering back on — the fix would cost the whole art direction.

### C2 — The player body becomes a texture; the sword stays code-drawn

**What.** `player.gd:_draw()` keeps its structure. The body-and-scarf block
(`player.gd:300-336`) is replaced by a single texture draw selected from the
state table in `CHARACTER-SHEET.md` section 5. The sheathed-blade block and the
swung-blade block are **left exactly as they are**.

**Why.** `CHARACTER-SHEET.md` section 2 has the argument in full: the swung
blade is built from `ATTACK_PIVOT`, `attack_angle()` and `tuning.attack_reach`,
and so is the kill hitbox. Baking the blade into a static frame would let the
picture and the hitbox drift apart silently the next time anyone touches the
tuning.

**Predicted failure, concrete.** `_mrect`/`_mpoly` mirror the character by
negating x (`player.gd:239-251`). `draw_texture_rect` has no flip argument, so a
naive port draws the sprite facing right while the sword still mirrors — a
character swinging backwards. The fix is `draw_set_transform(Vector2.ZERO, 0.0,
Vector2(facing, 1.0))` around the texture draw only, reset before the sword.

**Check.** Run left, swing, screenshot. The blade must leave from the shoulder
the character is facing. This is an eyes-on check because it is a visual
contradiction, not a numeric one.

**Second predicted failure.** The sprite's anchor is (20, 30) in a 32 × 32 cell.
Get that wrong and the character floats above the floor or sinks into it, while
every collision test still passes — because the collider has not moved. A green
suite would say nothing.

**Check.** Stand idle on a platform, zoom the screenshot, confirm the lowest
opaque sprite row is the platform's top row. Then flip through all eight poses
in place and confirm the feet do not move vertically
(`CHARACTER-SHEET.md` section 6, item 5).

### C3 — A death pose, which does not exist today

**What.** On `State.DYING`, draw pose P8 instead of whatever frame the player
was on.

**Why.** `session.gd:477-492` sets `player.enabled = false` on death and the
sprite simply freezes. For 0.55 s the player looks at a character mid-stride,
hanging in the air, with no acknowledgement that anything happened. Pillar 1 of
`CONCEPT.md` is "every failure teaches"; a frozen frame teaches nothing.

**Predicted failure.** The player is frozen but `_draw()` still runs, and
`is_on_floor()` on a disabled body is whatever it was last tick. Keying P8 off
movement state instead of off `session.state` would give an inconsistent pose
depending on *how* the player died. P8 must be keyed off the session state, and
it must take priority over every other row in the table.

**Check.** Die three ways — spikes, a fall, an enemy — and confirm the same pose
in all three. The existing `test_game.gd` already drives all three deaths.

### C4 — Music

**What.** One `AudioStreamPlayer` on a `Music` bus, looping, started when
`State.PLAYING` begins. The loop is cut from `MUS-B-01` or `MUS-B-02`
(`ASSET-LOG.md`), neither of which has been downloaded yet — 0 of 7 lifetime
downloads are spent.

**Why.** `CONCEPT.md` revision 1.1: driving, 124 bpm, the score supplies the
pressure.

**Predicted failure — the one already written down.** Revision 1.1 predicted it
in advance and it is restated here because this is the brief that has to check
it: *the trap's 15-frame warning is masked by the music, so the hazard reads as
unfair with sound on even though it is fair with sound off.* A 124 bpm bed with
pulsing bass and tight percussion competes for exactly the attention the warning
needs.

**Check.** A human playtest of the trap section at full music level, listening
for the warning specifically. Automated checks cannot test masking — it is
perceptual. If it fails, `SFX-TRAP` is redesigned as a rising sweep (pitch
motion, which percussion does not have) before the music is touched, because the
music direction is a decision and the trap sound is an implementation of it.

**Second predicted failure.** A loop cut anywhere but a bar boundary clicks
once per repetition. Heard once it sounds like a glitch; heard twenty times it
is the thing the player remembers.

**Check.** Play the exported OGG three times back to back and listen at the
seam before it goes anywhere near the project.

**Third predicted failure.** `session.gd:456-465` pauses `laugh` on focus loss
and on pause. A second stream added without the same handling keeps playing
after the window loses focus.

**Check.** Alt-tab mid-level. Silence, both streams.

### C5 — Sound effects

Four, matched to events that already exist in the code:

| ID | Event | Where it fires |
|---|---|---|
| `SFX-JUMP` | jump and air jump | `player.gd:221-233` — both branches |
| `SFX-SLASH` | swing starts | the tick `attack_phase()` goes 0 → 1 |
| `SFX-TRAP` | trap trigger, the 15-frame warning | the trap's rise, not its contact |
| `SFX-DEATH` | fatal contact | `session.gd:477` |

**Why these four and not more.** They are the four moments the player's hands
are already committed to. A sound on an event the player did not cause teaches
nothing.

**Predicted failure.** `SFX-TRAP` has to fire the tick the player crosses
`trigger_x`, which is where the 15-tick rise starts (`TRAP_RISE_TICKS = 15`,
`session.gd:29`). Hanging it off the damage contact instead would make it a
death sound, arriving after the information is useless — and it would *still
pass* a test that only asserted "a sound played when the trap killed me".

**Check.** An assertion on the tick index: the sound's start tick equals the
tick `trap_risen[i]` leaves 0, and is at least 15 ticks before any contact. The
geometry gives the player room for it — trap 0 triggers at x = 1064 and its
spike starts at x = 1160, so 96 px of run-up, 87 px to the player's leading edge
(`levels/first_steps.json:27`, and `test_game.gd:547` already computes exactly
that distance).

**Generator requirement.** `CHARACTER-SHEET.md` section 8 and `ASSET-LOG.md`
both say it: these go on a tool that records a seed, so the log can reproduce
the output and not only the request. That is a direct consequence of Suno being
unable to, which is logged there.

### C6 — Mute

**What.** A new `mute` action (key `M` is taken by `menu` in
`session.gd:105` — so `KEY_0` or `KEY_N`), toggling the master bus, with the
state shown on the HUD.

**Why.** The assignment requires the slice to stay understandable with all sound
muted, and that is not a claim to make without being able to test it in one
keypress.

**Predicted failure.** Muting by setting stream volumes individually leaves any
stream added later audible. It has to be the bus.

**Check.** Mute, then play a full run including a death and the trap. Nothing
audible, and the run is still completable — the trap is already fair on visuals
alone (15 frames of visible rise, 96 px of run-up, section C5), so a failure here would mean
the art changes broke the visual warning, which is worth knowing.

### C7 — The placeholder death assets are replaced

**What.** `godot/assets/death-laugh.ogg` (3.42 s of silence) and
`death-laugh-cat.png` (a flat PLACEHOLDER card) are replaced by generated
assets, or the reaction is cut.

**Why.** `godot/assets/README.md` records why they are placeholders: Assignment
1's meme cat and laugh had no documented permission and were deliberately not
copied into this repository.

**Predicted failure, and it is certain.** `test_game.gd`'s
`enemy-death-reuses-the-reaction` asserts the reaction's remaining time, and the
placeholder is 3.42 s **on purpose** to keep that assertion honest. Any
generated sound of a different length breaks it.

**The honest fix, stated in advance so it is not improvised later.** The
assertion is rewritten to read the stream's own length
(`laugh.stream.get_length()`, which `session.gd:97` already does) rather than a
literal 3.42. It is **not** deleted, and it is **not** loosened to a range. The
assignment forbids removing a failing assertion to get a green report, and the
README already commits to that in writing.

## 2. Order of work, and why

1. REF-01, then the eight required poses — everything else waits on them.
2. C1, then C2 — the filter has to be right before any pose can be judged in
   the game.
3. C3 — needs P8.
4. C4 and C6 together — the mute check is how the music gets judged.
5. C5, then C7 — the trap sound is the one with a real risk attached, and C7's
   test rewrite is cleanest once the real sound lengths are known.

## 3. The risks worth naming now

| Risk | Consequence | Where it is handled |
|---|---|---|
| A generated pose loses the scarf | The character is invisible on platforms (1.12:1) | `CHARACTER-SHEET.md` section 3; silhouette check first |
| The music masks the trap warning | A fair hazard reads as unfair | C4, human playtest |
| Download budget | 7 Suno downloads for the life of the account, 0 spent | one download, chosen after a browser audition |
| Time | 4 days to 2026-10-07 | the optional poses P9–P11 are the slack, and are dropped first |


---

# Revision 2.1.0 — 2026-10-04 — the dungeon is in the build

`CONCEPT.md` revision 1.3 changed the setting. This revision records what that
actually cost in code, what shipped today, and what it did to the plan above.
Revision 2.0.0 is unchanged.

## Done today

### C1 — texture filter: **done**

`rendering/textures/canvas_textures/default_texture_filter=0` is in
`project.godot`. The predicted non-integer-scale shimmer is still unverified
because no texture is in the build yet; the check moves to when the first pose
lands.

`environment/defaults/default_clear_color` also changed from the cream
`Color(0.965, 0.953, 0.925, 1)` to `Color(0.106, 0.086, 0.125, 1)` — the
dungeon wall. Without it the engine clears to cream outside the drawn backdrop.

### C8 — the dungeon backdrop (new)

`session.gd:_draw()`. Wall `#1b1620`; mortar courses with staggered vertical
joints `#2b2430`; blind arches `#241e2c` with a 2 px lighter masonry edge
`#352c40`; wall torches with a sixteen-disc warm pool; platform top edge teal
`#438e7d` → torchlit `#c89a5a`.

Two helpers added, `_draw_alcove()` and `_draw_torch()`.

**The arches stand at `level.hills`.** The level file is untouched — the same x
values, a different thing drawn at them. A cheaper option was to delete the
hills array; keeping it means the backdrop can be re-skinned again without
touching level data.

**The torches do not flicker, deliberately.** A time-driven flicker would make
two renders of the same frame differ, and the capture pipeline diffs frames
pixel-exactly (`scripts/check_trap_visibility.py` counts spike-coloured pixels
in fixed-camera frames). Atmosphere is not worth making the evidence
non-reproducible.

**A new ink/chalk split.** `ink` `#25354a` still draws platform bodies; `chalk`
`#9aa7bd` draws everything that has to read *against the wall* — the section
labels and the finish pole. Before this, `ink` did both jobs because the
backdrop was bright. At 1.43:1 against the wall it would have done neither.

### C9 — the character's rim (new, and a prerequisite not a polish)

`player.gd:_draw()` gains a rim pass before everything else: the body's four
rects and four polygons, grown 1 px, in `steel_edge` `#9aa7bd`. The body paints
over the middle and only the rim survives.

**This is load-bearing.** Without it the character is 1.60:1 against the wall
and the game is unplayable, not merely uglier. `CHARACTER-SHEET.md` section 3b
has the numbers.

The rim puts one pixel outside the 18 × 28 collider, at x −10..10. It carries
no hitbox, exactly like the scarf and the sword, and the collider contract
comment in `player.gd` says so now.

### C10 — the HUD bands (new)

`hud.gd`: the top (0–74) and bottom (335–360) bands go dark `#1b1620` with
light `#c6cedb` text; the progress track `#daddd6` → `#3a3344`; the death-cat
border `INK` → `CHALK`.

**The pop-up cards stay light.** Menu, pause, complete and death panels bring
their own background, and a light card on a dark world is the most readable
thing in the build. Only the bands changed — the ones that sit *on* the
dungeon.

## Verified, not asserted

| check | result |
|---|---|
| `tests/test_game.gd` | **79 checks / 0 failures** |
| `scripts/check_trap_visibility.py` | **PASS** — 0 spike pixels buried, 767 risen |
| `scripts/check_enemy_visibility.py` | **PASS** — all 5 captured enemies drawn at their live position |
| Rendered frames | `evidence/screens/01-menu` … `06-trap-risen`, re-captured on the dungeon |

The spike colour `#d24e42` was **not** changed, because
`check_trap_visibility.py` hard-codes that RGB. It is 4.15:1 against the wall,
which is fine, so there was no reason to change it and a concrete reason not
to.

## What the screenshots caught that the code did not

The first torch pool used four nested translucent discs. In the rendered frame
that is **visible ring banding**, which reads as a cheap effect; at sixteen
discs it is smooth. Nothing in the source suggested a problem. This is the
second time in this project that rendering and looking has caught something
arithmetic could not.

## What revision 2.0.0 said that is now wrong

Section 0 said every gameplay number is frozen and the comparison would isolate
the assets. **The gameplay numbers are still frozen** — tuning, geometry,
patrols and trigger distances are all untouched, and the 79 checks passing
unchanged is the evidence. But the before/after comparison is no longer
"same game, new assets": the setting changed too. The film has to say so
plainly rather than let a dungeon be mistaken for what generated art did.

## Still open from 2.0.0

C2 (sprite swap), C3 (death pose), C4 (music wiring — the loop file is in the
project but nothing plays it yet), C5 (sound effects), C6 (mute), C7 (replace
the placeholder death assets).


---

# Revision 2.2.0 — 2026-10-04 (later) — C4 and C6 are in the build

Revisions 2.0.0 and 2.1.0 are unchanged.

## C4 — music: **done**

`session.gd`. An `AudioStreamPlayer` on a **`Music` bus created at runtime**
(index 1), loaded the same no-import way the death laugh is, with
`stream.loop = true`. It starts on the first attempt of a session, stops at
the finish and at the main menu, and freezes with the game on pause and on
focus loss exactly as the death reaction does.

**The one line that matters.** `restart_attempt()` runs on *every* death, so a
naive `music.play()` there would restart the loop at bar 1 every 0.55 s —
worse than no music at all. The guard resumes instead of restarting.

**A bug the guard had anyway, found by probing rather than by reasoning.**
`AudioStreamPlayer.playing` reports **false** while `stream_paused` is true.
The first guard was `if not music.playing: music.play()`, which meant
**pause → R → the track jumped back to bar 1**. Rewritten to test
`playing or stream_paused`, and the case is now a named regression check.

## C6 — mute: **done**

New `mute` action on **`KEY_0`** (`M` is already `menu`), handled *before* the
state branches so it works on the menu and the results screen, not only
mid-run. It calls `AudioServer.set_bus_mute` on **Master**.

**Master, not per-stream** — the failure 2.0.0 predicted was that a per-stream
mute leaves anything added later audible, and the four sound effects of C5 do
not exist yet. A bus mute cannot be forgotten by a stream that was not written
when it was.

The HUD advertises the key in the control line and prints a warm `MUTED` in the
bottom band while it is on. Captured as `evidence/screens/10-muted.png`: the
assignment requires the slice to stay understandable with sound off, and that
claim is only checkable if the player can see which state they are in.

## Verified

**`tests/test_game.gd`: 87 checks / 0 failures** — eight new, all of them
behavioural rather than "the object exists":

| check | what it pins down |
|---|---|
| `music-loop-is-flagged-to-loop` | `loop` set and length 30.9632 s, matching the cut in `ASSET-LOG.md` |
| `music-is-on-its-own-bus` | bus is `Music`, index > 0 — not Master |
| `music-plays-during-a-run` | starts with the session |
| `a-retry-does-not-restart-the-track` | playback position does not go backwards across `restart_attempt()` |
| `music-pauses-with-the-game` | `stream_paused` on, then off, and still playing |
| `retry-while-paused-resumes-rather-than-restarts` | the `playing`/`stream_paused` bug above |
| `mute-is-a-master-bus-mute` | toggles bus 0, both directions |
| `music-stops-at-the-finish` | not left looping under the results card |

Trap and enemy visibility checks both still PASS; all screen captures redone.

## An operational note worth keeping

Re-running `capture_game.gd` produced only three of its six frames and exited
cleanly, which looked exactly like a regression from this change. It was not.
**`--quit-after` counts process iterations, not physics ticks**, and the
windowed run renders uncapped — so 6000 "frames" can elapse in nine seconds of
wall clock while only ~450 physics ticks have run. The same script passes
headless, which is what isolated it. The captures now run with
`--quit-after 200000`.

Recorded because the first instinct was to go looking for the bug in the music
code, and ten minutes went into a thing that was never broken.

## `[TZ DECIDE]` #3 is now answerable

v1 and revisions 1.1–1.3 left open *what the music does during the 0.55 s
retry*, on the grounds that it could not be judged until the loop was audible
in the game. **It is now implemented as "keeps playing"** — the simplest
behaviour, chosen because ducking is a bus-level change that should be made
against something heard rather than imagined.

It is now a listening decision, not a design one.

## Still open from 2.0.0

C2 (sprite swap), C3 (death pose), C5 (sound effects), C7 (replace the
placeholder death assets).


---

# Revision 2.3.0 — 2026-10-05 — C11: the character has parts now

Revisions 2.0.0–2.2.0 are unchanged. `CONCEPT.md` revision 1.4 carries the
design argument; this is what changed in the code.

## C11 — the body is a parts list

`player.gd`. The hand-ordered sequence of draw calls is replaced by
`_body_parts()`, which returns the figure back-to-front as data:

```
[0, colour, rim, x, y, w, h]   a rect
[1, colour, rim, points]       a polygon
```

**Both the rim pass and the paint pass walk the same array.** The old code
listed eight shapes twice — once in `_mrect_o`/`_mpoly_o` calls for the rim and
once in `_mrect`/`_mpoly` calls for the body — and nothing stopped the two
copies drifting apart. They cannot now.

New: a far arm and a near arm (upper / forearm / gauntlet each), legs split
into thigh / shin / boot, a 2 px neck, a jawline, and a recessed abdomen. The
`rim` flag marks the parts that form the outer silhouette; interior detail —
visor, glint, belt, abdomen, jawline, neck — is `false` and gets no halo.

## C12 — the rim is directional

`_mrect_o` grows **1 px back and 1 px up**, not 1 px on four sides.
`_mpoly_o` **translates** by (−1, −1) instead of expanding from the centroid,
so a thin wedge keeps its thickness.

**Why, in numbers.** An all-sides rim costs a part 2 px of width. The limbs
here are 3 px (arms) and 4 px (legs), so they would keep 1 px and 2 px of
armour respectively, and the three-value separation scheme would have nowhere
to happen. Rendered, the figure was grey pipework. A directional rim costs
**0 px** of width.

## C13 — the air pose is a bent knee

Rising lifts the far leg's shin and boot by 2.6 px and the near leg's by 0.9;
falling reaches 0.8 px. Shin and boot move **together at full height**.

**The bug this replaces.** `tuck` was *added* to y. y is negative upward, so
that pushed the boot to y +0.8 — below the feet line, into the floor — and
computed the shin's height as `3.2 - tuck` = 0.6 px. The jump frame rendered as
a glitch. Caught by looking at the contact sheet, not by a test: no assertion
in this project describes what the player looks like.

## Verified

| check | result |
|---|---|
| `tests/test_game.gd` | **87 checks / 0 failures**, unchanged |
| `attack-hitbox-on-the-blade-right` / `-left` | PASS, worst endpoint error 3.8e-6 px |
| `scripts/check_trap_visibility.py` | PASS |
| `scripts/check_enemy_visibility.py` | PASS |
| `tests/capture_character.gd` | 11 frames, every state assertion passed |
| `scripts/build_char_sheet.py` | `evidence/screens/char-contact-sheet.png` rebuilt |

## The gap this exposes in the test suite

Every check above is about **behaviour**: where the hitbox is, whether the trap
is drawn, whether an enemy is at its live position. **Nothing asserts what the
player character looks like**, which is why both of the bugs in this revision
were found by eye and not by the suite — and why both of them passed 87 checks
while being obviously wrong on screen.

That is a real limitation and not a thing to fix by writing a pixel-diff test
of the player, which would fail on every intentional art change and get
deleted. The honest answer is that `capture_character.gd` plus the contact
sheet **is** the check, and it requires a human to look. It is recorded here so
the film does not claim more than the suite delivers.

## Still open from 2.0.0

C2 (sprite swap), C3 (death pose), C5 (sound effects), C7 (replace the
placeholder death assets).


---

# Revision 2.4.0 — 2026-10-05 (later) — C3 and C5 are in the build

Revisions 2.0.0–2.3.0 are unchanged.

## C3 — the death pose: **done**

`player.death_pose`, set by the session on a fatal contact and cleared on
respawn. `_body_parts()` early-returns `_prone_parts()` when it is set, and
`_draw()` swaps the standing scarf and the sheathed sword for a scarf settled
over the legs and a blade that has skidded on past the body.

The pose is the storyboard's: `design/storyboard/panel-06-death.jpg` — flat,
face down, head pointing the way the character was travelling, limbs
collapsed. **It is the only pose in the game wider than it is tall** — roughly
26 × 9 against the standing figure's 18 × 28 — which is the whole reason it
works at this size. Nothing else can be mistaken for it without reading a
single pixel of detail.

**One inversion does the work.** The visor is a band along the **bottom** edge
of the helm. That single move is what says "face down" rather than "asleep on
its side".

**Keyed off `session.state`, not off movement**, which revision 2.0.0's C3
predicted and this confirms: on death the body is disabled and `is_on_floor()`
keeps whatever it last returned, so a movement-derived pose would differ
depending on *how* the player died. Asserted across all three causes.

The collider is not consulted. The body is disabled for the 0.55 s this is on
screen, so the drawing lies outside the 18 × 28 box exactly as the scarf and
the sword already do.

## C5 — four sound effects: **wired, with placeholder audio**

**The audio is not generated and does not satisfy the assignment's "generate
sound" requirement.** It is synthesised by arithmetic in
`scripts/synth_placeholder_sfx.py`. `ASSET-LOG.md` says so in a block quote at
the top of its sound-effects section, and `godot/assets/README.md` lists each
file with a "Generated?" column that reads **no**.

**Why wire against placeholders instead of waiting.** `CONCEPT.md` revision 1.1
predicted that a 124 bpm bed would mask the trap warning, and C4 turned that
into the one check in this project that cannot be automated. **It cannot be run
against silence either.** With placeholders in, it can be run today and re-run
against the generated versions, which makes the two comparable rather than
sequential. The wiring, the triggers and the assertions do not change when the
files are replaced.

A dedicated `Sfx` bus (index 2) with per-sound trim: jump −7 dB, slash −5 dB,
**trap 0 dB**, death −2 dB. The trap is loudest deliberately — it is the only
one of the four the player is supposed to *act* on.

### Where each one fires, and why there

| | trigger | why not somewhere else |
|---|---|---|
| jump | `player.jumps` increments | read off the player's own counter rather than fired from inside `player.gd`, so the player stays pure gameplay and the test can check against the same number |
| slash | `player.attacks` increments | same |
| **trap** | the tick `trap_risen[i]` leaves 0 | **the trigger crossing, not the damage.** Hung off the contact it is a death sound arriving after the information is useless — and it would still pass a check that only asked whether a sound played when the trap killed you |
| death | the fatal contact in `resolve_contacts()` | the same single path spikes, falls and enemies already share |

### The timing is measured, not asserted in prose

`session.sfx_log` records `{id, tick}` for every effect and is cleared per
attempt, so it is bounded and a test can read it without subtracting a previous
life's events. The trap check walks the player from x 1020 into trap 0 and
reads the log:

| | |
|---|---|
| warning fires at tick | **24**, with the player at x **1064.6** (trigger_x = 1064) |
| death at tick | **59** |
| **warning lead** | **35 ticks ≈ 0.58 s** |
| rise the warning has to beat | 15 ticks |

That is the fairness argument of the whole slice, as a number, in the suite.

## Verified

| check | result |
|---|---|
| `tests/test_game.gd` | **95 checks / 0 failures** — eight new |
| `death-pose-is-the-same-whatever-killed-you` | PASS across spike, fall and enemy |
| `sfx-trap-fires-on-the-trigger-not-the-contact` | PASS, lead 35 ticks |
| `scripts/check_trap_visibility.py` | PASS |
| `scripts/check_enemy_visibility.py` | PASS |
| captures | game 7 frames, character 11 frames, enemies 3 frames, contact sheet rebuilt |

## Still open from 2.0.0

- **C2** — the generated sprite swap. Blocked on art generation.
- **C7** — the placeholder death reaction assets, and now also the four
  placeholder effects. All of it is a file-for-file replacement.
- The **human listen**: the seam, the retry behaviour, and the masking check
  that C5 exists to make runnable.


---

# Revision 2.4.1 — 2026-10-05 (later still) — C14: two sources at 0 dB clip

Found within the hour of shipping 2.4.0, by building an offline mix of
`SFX-TRAP` over the music loop in order to run the masking check. **The render
clipped at 1.172.**

## The arithmetic

| | peak |
|---|---|
| `music-loop.ogg` | 0.702 |
| `sfx-trap.ogg` after its 0 dB trim | 0.810 |
| sum, if those peaks land on the same sample | **1.512** |

**Turning the music down does not fix it.** Even at −9 dB the bound is 1.059,
and a −9 dB bed is not the "the score supplies the pressure" of `CONCEPT.md`
revision 1.1. The trade on offer was *a quiet score* against *rare clipping*,
and both answers are bad.

## The fix

An `AudioEffectHardLimiter` on **Master**, ceiling −0.5 dB, plus **−3 dB** on
the music player for ordinary headroom. The limiter is a safety net for the
rare alignment, not something squashing the mix:

> On a 14-second test with `SFX-TRAP` fired three times over the loop at the
> game's own levels, the limiter would touch **9 samples out of 672 000 —
> 0.0013 %**.

## Why this needed a limiter rather than a louder ear

**Playing the game would not have shown it.** A handful of clipped samples
inside a 0.26 s sweep is not something an ear reliably catches, and nothing in
the suite was listening to the mix — every audio check until now was about
*whether* and *when* a sound plays, never about what the sum of them looks
like.

So it is asserted now:
`master-bus-has-a-limiter-because-two-sources-at-0db-clip` checks the effect is
present, its ceiling is at or below 0 dB, and the music is at −3 dB. **96
checks / 0 failures.**

## The pattern worth naming

This is the third thing in two days that was found by **rendering an artefact
and measuring it** rather than by reading code or playing the game: the torch
banding, the grey-pipework limbs, and now the clipping. In each case the source
was correct and the output was wrong, and in each case the thing that caught it
was building the output in order to check something else.


---

# Revision 2.5.0 — 2026-10-05 (later still) — C2: the generated sprites are in

Revisions 2.0.0–2.4.1 are unchanged. **This is the change the whole assignment
was for**: the character the player sees is now generated art rather than
geometry written in GDScript.

## C2 — the sprite swap: **done**

`player.gd` loads the eight PNGs from `godot/assets/poses/` in `_ready()` and
`_draw()` picks one per tick. Where they are read from and how is the same
no-import trick `session.gd` uses for audio — straight off disk with
`Image.load_from_file`, because a `--headless --script` run does not rescan the
filesystem and `load()` on an unimported asset fails in exactly the situation
the assignment asks to verify: a fresh checkout.

### The mapping is a value, not a branch

`pose_key()` returns a **string**, and `_draw()` looks the texture up from it.
That is deliberate: it means the mapping from state to pose can be asserted
without a renderer, and `pose-key-matches-the-state-it-claims` drives the game
through all eight states and reads it back.

Priority order, and `death` is first for the reason revision 2.0.0 predicted:
on death the body is disabled and `is_on_floor()` keeps whatever it last
returned, so anything derived from movement would differ by cause of death.

### The blade stayed in code, and that is the point

The sprites carry the body, the scarf, the rim and the visor. **The blade does
not.** It is still drawn from `ATTACK_PIVOT`, `attack_angle()` and
`tuning.attack_reach` — the same three numbers the kill hitbox is built from.

`CHARACTER-SHEET.md` section 2 argued for this before any art existed, and the
poses were prompted with *"empty hand, NO weapon"* to keep it true. A blade
baked into a sprite would stop tracking the hitbox the moment anyone touched
the tuning, and **nothing would say so** — the two
`attack-hitbox-on-the-blade-*` checks would still pass, because they measure
the hitbox against the numbers, not against the picture.

The swing routine was also extracted to `_draw_swing()` and is now shared by
the sprite path and the code-drawn fallback, so those two cannot disagree about
the blade either.

### The code-drawn body is kept as a fallback

If `godot/assets/poses/` is absent, `_draw()` falls through to `_body_parts()`
exactly as before. The project still runs from a checkout without the art, and
the parts list, the directional rim and the prone layout all stay live and
tested.

### One thing that had to be re-aimed

The sheathed blade's endpoints are **not** the code-drawn body's. That
silhouette was 18 px wide with a flat-topped helm and the blade was tuned to be
occluded by it; the generated sprite has a taller hood and a narrower waist, so
the same line left **the grip floating in the air above the head**. Pulled from
`(-9, -32) → (11, -4)` to `(-7.5, -27) → (10, -5)`, so it emerges from behind
the shoulder.

Found by rendering it and looking. The fourth time in three days.

## Verified

| check | result |
|---|---|
| `tests/test_game.gd` | **99 checks / 0 failures** — three new |
| `pose-textures-all-eight-loaded-at-32x32` | 8 loaded, none missing, none the wrong size |
| `pose-key-matches-the-state-it-claims` | all eight states return their own key, driven through real movement |
| `sprites-did-not-take-over-the-blade` | the shared swing routine is still there |
| `tests/test_keyboard.gd` | 14 / 14 |
| `check_trap_visibility.py` / `check_enemy_visibility.py` | PASS |
| captures | game 7, character 11, enemies 3, contact sheet rebuilt |

**The feet were measured, not eyeballed.** The lit platform edge begins at
logical y 320 and the player's `position.y` is 319.93; the sprite's anchor at
cell row 30 puts its lowest opaque row exactly there.

## What this does NOT change

- **No gameplay number.** 99 checks pass, including both blade-hitbox
  assertions at sub-micron endpoint error.
- **The collider.** 18 × 28 at (0, −14). The sprite cell is 32 × 32 and the
  overhang is decoration, exactly as the scarf and the blade already were.
- **The dungeon, the HUD, the enemies, the traps.** All still code-drawn.

## Still open from 2.0.0

- **C7** — the placeholder death reaction (`death-laugh.ogg`,
  `death-laugh-cat.png`) and the four placeholder sound effects.
- The four human checks of `TEST-REPORT.md` section 6.
