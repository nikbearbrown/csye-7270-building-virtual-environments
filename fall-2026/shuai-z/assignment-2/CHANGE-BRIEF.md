# CHANGE-BRIEF — walker-rudy

> Draft v3, 2026-10-01. This is the plan and the predictions for the Assignment 2 asset slice: Level 1 as one Godot 4.7.2 scene at 1920×1080. The deadline is the evening of 2026-10-04, so every asset has a priority, and a cut order follows the list.

## Rules this plan assumes

These rules come from CONCEPT.md and the decisions logged in FRICTIONAL.md:

- Rudy starts in the default form with 3 hearts.
- Any hit (an enemy, a spore, spikes) knocks the gear away if he carries it; otherwise it costs one heart.
- There is short invulnerability after every hit.
- On a hit, the camera shakes briefly (panel 4).
- On the "Level complete" card, Enter plays Level 1 again from the opening.
- Falling below a cliff is instant death.
- Zero hearts or a fall sends Rudy back to the last waystone with 3 hearts.
- After a death Rudy respawns without gear, and the sword-and-shield pickup reappears where it was.
- Level 1 has one waystone near the middle, one sword-and-shield pickup, no health pack, and ends at the teleport circle.

## Asset list

Priorities: **must** means it is in the slice; **should** means it is planned for the slice and cut only if time runs out; **could** is stretch work. "Generated" means made by an image or audio model and logged in the asset log.

| ID | Asset | Panels | Source | Priority |
|---|---|---|---|---|
| CHAR-REF | Rudy's turnaround reference | sheet | generated | must |
| CHAR-IDLE | idle | 1 | generated, edited from CHAR-REF | must |
| CHAR-RUN-A / CHAR-RUN-B | run, contact and passing | 2 | generated, edited from CHAR-REF | must |
| CHAR-RISE / CHAR-FALL | rising, falling (also the stomp) | 2, 5 | generated, edited from CHAR-REF | must |
| CHAR-HURT | hurt | 4 | generated, edited from CHAR-REF | must |
| CHAR-SWORD-IDLE | sword-and-shield idle | 3 | generated, edited from CHAR-REF | must |
| CHAR-SWORD-RUN-A / -RUN-B / -RISE / -FALL | sword-form movement (default poses plus the props) | 3, 4 | generated, edited from the default poses | must |
| CHAR-SWORD-SLASH | slash | — | generated | must |
| CHAR-SWORD-BLOCK | block | 4 | generated | should |
| CHAR-RESPAWN / CHAR-DEFEAT / CHAR-CELEBRATE | respawn, defeat, celebrate | 5, 6 | generated | could; idle plus flashing stands in |
| ENV-SKY-CASTLE | far parallax layer: sky, hills, distant castle | 1, 6 | generated | must |
| ENV-FIELDS | middle layer: wheat meeting meadow | 1, 2, 6 | generated | must |
| ENV-GROUND | ground strip and cliff edges | 2, 5 | generated | must |
| ENV-SPIKES | spikes | 2 | generated | must |
| ENV-WAYSTONE | checkpoint, dark and lit | 5 | generated | must |
| ENV-PORTAL | teleport circle | 6 | generated | must |
| PROP-SWORDSHIELD | sword-and-shield pickup | 3 | generated | must |
| ENEMY-GOBLIN | goblin: two walk frames and a squashed frame | 2, 4 | generated | must |
| ENEMY-MUSHROOM | mushroom monster: idle, attack, squashed | 4 | generated | should |
| FX-SPORE | spore projectile | 4 | generated | should |
| UI-HEART | full and empty heart | 4, 5 | generated | must |
| UI-TITLE | the title over the opening of play, and the "Level complete" text | 1, 7 | text | could |
| ENV-ENDCARD | end card: a high view of the road to the castle | 7 | generated | could |
| SFX-JUMP | jump (the **action** event) | 2 | generated | must |
| SFX-STOMP | stomp defeats an enemy (**success**) | 2 | generated | must |
| SFX-PICKUP | gear picked up (**success**) | 3 | generated | must |
| SFX-HURT | Rudy takes a hit (**failure**) | 4 | generated | must |
| SFX-PORTAL | teleport circle reached (**completion**) | 6 | generated | must |
| SFX-SLASH | sword slash | — | generated | must |
| SFX-SPORE / SFX-BLOCK | mushroom fires; shield stops a spore | 4 | generated | should |
| SFX-FALL / SFX-CHECKPOINT | fall death; waystone lights | 5 | generated | could |
| MUS-LOOP | the Level 1 theme, looping | 1–6 | generated | must |

**Cut order** if the schedule slips:
1. UI-TITLE and ENV-ENDCARD; the slice then opens straight into play and ends on a plain "Level complete" text.
2. The respawn, defeat and celebrate poses.
3. SFX-FALL and SFX-CHECKPOINT.
4. The mushroom (ENEMY-MUSHROOM, FX-SPORE, SFX-SPORE, SFX-BLOCK, CHAR-SWORD-BLOCK). Panel 4's failure would then come from touching a goblin.

Any panel the slice does not cover is named in TEST-REPORT.md.

## Event-to-sound map

All sounds go through one entry point, `Sfx.play(id)`, called right after the code that already represents the event has changed the game state. Sound never decides game state: nothing reads a sound back, and a missing or muted sound changes nothing. The entry point also counts plays per ID for the automated check.

| Sound | Exact trigger | Guard against double triggers |
|---|---|---|
| SFX-JUMP | the physics frame in which the jump velocity is applied | needs a fresh press (`is_action_just_pressed`) and ground under Rudy, so holding the key cannot fire it again |
| SFX-STOMP | an enemy's `defeat()` because Rudy landed on it from above | the enemy sets `dead = true` and disables its collision before playing; a dead enemy ignores further hits |
| SFX-PICKUP | the pickup's first `body_entered` from Rudy | the pickup disables monitoring, then frees itself |
| SFX-HURT | `take_hit()` when it actually costs gear or a heart | invulnerability: hits during the window are ignored, so a spore and a goblin at once still make one sound |
| SFX-PORTAL | the level state changes to `COMPLETE` | the state can enter `COMPLETE` once; input stops |
| SFX-SLASH | a slash starts | no new slash until the current swing ends, so holding or mashing the key gives one sound per swing |
| SFX-SPORE | the mushroom spawns a spore | one call per spawn, inside the spawn function |
| SFX-BLOCK | the shield's block zone destroys a spore | the spore stops monitoring and frees itself on first contact, so it cannot also hurt Rudy |
| SFX-FALL | Rudy crosses the kill line below a cliff | the death state is set first; the kill line ignores Rudy while he is dead or respawning |
| SFX-CHECKPOINT | a waystone activates | an `activated` flag; lighting happens once per waystone |

## Music behavior

| Moment | What the music does |
|---|---|
| Title | MUS-LOOP starts under the title and keeps playing when Enter starts play; it does not restart |
| Normal play | MUS-LOOP plays continuously on the Music bus |
| Pause | the Music bus drops 12 dB until play resumes; the loop keeps its place |
| Hurt (failure) | dips 6 dB for about 0.6 s under SFX-HURT, then returns |
| Death and respawn | dips 9 dB through the fade and respawn, then returns; it never restarts from the top |
| Stomp, pickup (success) | no change; the sound effect carries the moment |
| Teleport circle (end of the slice) | fades out over about 1.5 s under SFX-PORTAL; the "Level complete" card is silent |

**Mute:** M toggles the Music bus and N toggles the SFX bus. These are bus mutes that the game never checks.

## Predicted failure cases and how they will be checked

1. **Generated poses drift from the reference** (head size, robe length, cowlick, eye color).
   - Check: overlay every frame on CHAR-REF at 160 px with the height bar and the capsule.
   - A frame more than about 5% off in height, or breaking a consistency rule, is rejected and logged.
2. **Rudy disappears against the wheat**, because both are yellow (planned contrast 1.21; see the character sheet).
   - Check: repeat the silhouette and palette test on the generated ENV-FIELDS, using an in-engine screenshot (with the outer outline on) and a grayscale copy, and re-measure the contrast.
3. **A sound fires twice on one event**, for example a held jump, a mashed slash, two goblins stomped at once, or a spore hitting the shield and the body.
   - Check: the automated test plays a scripted input sequence and compares the `Sfx.play` counts per ID with the events that actually happened.
4. **The music loop clicks or leaves a gap at the seam.**
   - Check: cut the loop at a bar boundary on a zero crossing, import the OGG into Godot with Loop on, and listen to at least three repetitions.
5. **Art and collision disagree**: feet float or sink, or the hair and shield look as if they should be hit.
   - Check: in-engine screenshots of every state with Debug → Visible Collision Shapes turned on.
6. **The slice is unreadable with sound muted.**
   - Check: a full muted playtest, confirming each sound has a visual twin (squash, flash, flying gear, waystone light, portal light).

## Build order

Each step is approved before it is implemented, then run and checked.

1. Greybox: Rudy's controller, the level layout, spikes, a cliff, a goblin, the waystone and the portal, all as code-drawn placeholders. This can start as soon as `design-v1` is committed, alongside generation.
2. Swap in the generated art: Rudy's states and facing, the parallax layers, ground, props and enemies. A canvas shader adds the 4 px outer outline to characters, enemies and hazards.
3. Audio: buses, `Sfx.play`, the four required sounds first, then the rest; MUS-LOOP with its pause, dip and fade behavior; the mute keys.
4. The mushroom, the spores and blocking (should).
5. Automated checks, then my own playtest with sound on and with sound muted.

## Revisions after design-v1

The sections above are design v1 (tag `design-v1`, commit `5649d5b`) and stay as written. Where they differ, these revisions win.

- **2026-10-01, greybox step 1c:** after a death, every monster is back where it started, the defeated ones too, alongside the sword-and-shield pickup. Decided in the greybox plan; see FRICTIONAL.md.
- **2026-10-02, after the step 1c playtests:**
  - a fall below a cliff is no longer instant death with full hearts. It costs one heart, plays SFX-FALL only, and sends Rudy back to the last checkpoint with the hearts he has left; as after any death, every monster is back there too;
  - whenever his last heart goes, by a hit or a fall, the level starts over from the opening, as if the game had just begun: Rudy is at the start with three hearts, the waystone is dark again, and every monster is back;
  - this replaces "Falling below a cliff is instant death" and "Zero hearts or a fall sends Rudy back to the last waystone with 3 hearts" above, and panel 5's "reappears at the last waystone with 3 hearts" in STORYBOARD.md. The waystone now matters only after a fall that leaves him hearts.
- **2026-10-02, greybox step 1d:** the pickup does not free itself after its first `body_entered`, as the event-to-sound map says: it stops monitoring and hides, so it can be back where it was after a death. The guard against a second SFX-PICKUP is the same.
- **2026-10-02, cutting the sound list to six:** the slice has six sound effects: SFX-JUMP, SFX-STOMP, SFX-HURT and SFX-PORTAL (the four the assignment requires), plus SFX-SLASH and SFX-PICKUP.
  - SFX-FALL is cut. A fall costs a heart, so it plays SFX-HURT, once, at the same moment SFX-FALL would have played (Rudy crosses the kill line); the kill line's guard is unchanged. This replaces "plays SFX-FALL only" above and panel 5's "the fall sound (SFX-FALL)" in STORYBOARD.md.
  - SFX-CHECKPOINT is cut. The waystone lighting up is the cue, with no sound.
  - SFX-SPORE and SFX-BLOCK are cut with the mushroom (cut-order step 4). If the mushroom is built after all, SFX-SPORE comes back, since P2 gives every enemy shot its attack sound.
  - The asset list and the event-to-sound map above keep their rows for the record; the cut rows are not generated.
- **2026-10-04, the music loop:** MUS-LOOP is 24 bars (54.87 s at about 105 BPM), because the generated song repeats every 24 bars, not 16 or 32. Predicted failure 4's check changes accordingly: the loop is cut at bar lines, and instead of a cut on a zero crossing, the beat after the end is crossfaded into the first beat, so the end runs straight into the start; the file is mono. Details in ASSET-LOG.md.
- **2026-10-04, build step 3 (the audio):**
  - the pause: the game had no pause. Esc pauses play and resumes it, only in play (not on the title, through a death and the respawn, or from the teleport circle on). The game stops, "Paused" shows over a dimmed screen, the sound effects pause, and the music plays on 12 dB down, keeping its place. This is what the music behavior's "Pause" row means;
  - the dips act on the music's player, not on the Music bus, so they never touch the M mute. Where two are in force the music plays at the deeper one, so they never add up: a hit that takes the last heart dips 9 dB, not 15. Every change ramps over 0.15 s;
  - the hurt dip follows a hit; a fall plays SFX-HURT and gets the death dip only;
  - the music starts under the title and plays on across a start-over from the opening; only playing again from the end card starts it from the top;
  - the starting mix: the Music bus at −6 dB, the SFX bus at 0 dB, and every sound at its file's level, to be set by ear in the playtest.
- **2026-10-04, build step 4 cut:** the mushroom is cut, as cut-order step 4 says: ENEMY-MUSHROOM, FX-SPORE, SFX-SPORE, SFX-BLOCK and CHAR-SWORD-BLOCK in play (its frame is generated and loaded, but nothing shows it). Panel 4's failure comes from a goblin or the spikes: the hit knocks the gear away, as before. The build order's step 4 is skipped, and TEST-REPORT.md names what of panel 4 the slice does not cover.
