# COMPONENTS.md — what this teardown explains, and why these five

`godot-gamedev walker` over `walker-ninja-TiantongZhang`.

The game is a 2D side-scrolling dungeon slice: a cyber-ninja with a double
jump, an air dash and a sword, against pop-up spike traps, patrolling slimes
and flying horses. It continues the Assignment 1 build. **Assignment 2 is about
generated art, sound and music**, so this film is about the five places where
generated assets meet the code that was already there — and about the checks
that make each claim true rather than asserted.

Every number below is from the current source or a recorded run. The film does
not round them and does not borrow a tutorial's values.

---

## Teaching contract

`code-then-result-v1`. Each code excerpt is immediately followed by a beat that
shows what those lines do in this game, bound by hash to the media shown. Five
pairs, ten beats, inside the `walker` bookends.

---

## C1 — `pose_key()`: a string, so the mapping can be tested

| | |
|---|---|
| Files | `features/player/player.gd` |
| Code | `pose_key()`, ~10 lines |
| Result | the state → pose table from a real run, and the sprite on screen |

**The mechanism.** Eight generated sprites, one per state the engine can
already distinguish. `pose_key()` returns a **string**; `_draw()` looks the
texture up from it.

**Why a string and not a branch that picks a texture.** Because a string can be
asserted without a renderer. The check
`pose-key-matches-the-state-it-claims` drives the game through all eight states
and reads the key back:

```
{"dash":"dash","death":"death","fall":"fall","idle":"idle",
 "live":"live","rise":"rise","run":"run","windup":"windup"}
```

**The trade-off.** One extra dictionary lookup per frame, and the pose names
now exist in two places — the key strings and `POSE_FILES`. A mismatch there is
a missing texture rather than a wrong texture, which is the cheaper failure.

**The ordering detail worth the screen time.** `death` is tested first. On death
the body is disabled and `is_on_floor()` keeps whatever it last returned, so a
pose derived from movement would differ depending on *how* the player died.
`death-pose-is-the-same-whatever-killed-you` checks all three causes.

---

## C2 — `import_pose.py`: two edits, both measured, both declared

| | |
|---|---|
| Files | `scripts/import_pose.py` (outside `godot/`, recorded in SOURCES) |
| Code | the rim pass and the visor restoration |
| Result | the measured before/after, and the preview strip the script writes |

**The mechanism.** The importer finds the figure, scales it to the collider's
height, places it on the (20, 30) anchor in a 32 × 32 cell, and snaps every
pixel to the eight-colour palette. Then it does two things the model did not.

**The rim.** The reference came back with a near-black outline. Snapped, that is
`shade` — **1.14:1** against the dungeon wall `#1b1620`, which is to say
nothing. The importer adds 1 px of `steel_edge` toward the back and up, because
the dungeon's light is a torch above and behind.

| | without | with |
|---|---|---|
| figure reading at 3:1+ against the wall | **6.3 %** | **24.2 %** |
| `steel_edge` pixels | 20 | 94 (74 added) |

The code-drawn character measures 9.1 % on the same test.

**The visor.** The slit is 1–2 px tall at a 28 px figure height. An area
resample averages it into the navy helm and the result snaps to `plate`:
**0 visor pixels in seven of the first eight imports.** The mask is taken from
the source before scaling, resampled by area coverage and thresholded low.
6–9 px restored per pose.

**Both are edits to generated assets, not properties of the generation**, and
`ASSET-LOG.md` says so. What the model produced is a slit in a 1254 px image;
what the importer does is keep it alive at 28.

**The trade-off, and a failure worth showing.** The first visor guard was
"only the top 45 % of the figure", to stop steel boot highlights being restored
as cyan specks. It **silently zeroed the prone pose**: lying down, the head is
at the *right*, not the top. Largest connected component instead.

---

## C3 — the trap warning fires on the trigger, not the damage

| | |
|---|---|
| Files | `game/session.gd`, `levels/first_steps.json` |
| Code | `advance_traps()` — the `trap_risen[i] == 0` branch |
| Result | `sfx_log` from a real run, and the trap section played |

**The mechanism.** A trap arms when the player crosses `trigger_x` and the
spike rises over `TRAP_RISE_TICKS = 15`. The sound fires on **the tick
`trap_risen` leaves 0** — the arming, not the contact.

**Why that is the whole fairness argument.** Hung off the damage it is a death
sound arriving after the information is useless, and it would **still pass** a
check that only asked whether a sound played when the trap killed you. So the
check reads `session.sfx_log`, which records `{id, tick}`:

| | |
|---|---|
| warning at tick | **24**, player at x **1064.6** (trigger_x = 1064) |
| death at tick | **59** |
| **lead** | **35 ticks ≈ 0.58 s** |
| rise it has to beat | 15 ticks |

**The design behind the sound itself.** `CONCEPT.md` revision 1.1 predicted on
2026-10-01 that a 124 bpm bed with pulsing bass would mask this, and specified
the answer before the sound existed: **a moving pitch, which percussion does
not have**, so it is told apart by motion rather than by level. Hence a rising
sweep, 420 → 2100 Hz, partials at inharmonic ratios, amplitude rising rather
than decaying, 0.260 s — 15.6 frames, the length of the warning.

**The limit, stated on screen.** That sound is **synthesised, not generated**.
It is a placeholder, and the film says so where it plays it.

---

## C4 — one `if` that stops the music restarting

| | |
|---|---|
| Files | `game/session.gd` |
| Code | the music guard in `restart_attempt()` |
| Result | playback position across a retry, from a real run |

**The mechanism.** `restart_attempt()` runs on **every** death. A naive
`music.play()` there restarts a 16-bar loop at bar 1 every 0.55 s, which is
worse than silence. The guard resumes instead.

**And the guard was still wrong.** `AudioStreamPlayer.playing` reports **false**
while `stream_paused` is true, so `if not music.playing` was right for an
ordinary death and wrong for *pause → R*: the track jumped back to the top.

That was found by **printing what the engine reports in each state before
writing the assertions**, not by reading the code — the code reads correctly.
It is a named regression check now, and the film shows the position going
forward across a retry:

```
a-retry-does-not-restart-the-track   before 0.467 s   after 0.557 s
```

---

## C5 — the blade stays in code, and that is the point

| | |
|---|---|
| Files | `features/player/player.gd`, `features/player/tuning.gd` |
| Code | `_draw_swing()` and `ATTACK_PIVOT` / `attack_angle()` / `attack_reach` |
| Result | the hitbox endpoint error, and a swing in motion |

**The mechanism.** The sprites carry the body, the scarf, the rim and the
visor. The blade does not. It is drawn from the same three numbers the kill
hitbox is built from, and `_draw_swing()` is shared by the sprite path and the
code-drawn fallback so those two cannot disagree either.

**Why it was kept out of the art.** The poses were prompted *"empty hand, NO
weapon"*. A blade baked into a sprite would stop tracking the hitbox the moment
anyone touched the tuning — and **nothing would report it**. The two
`attack-hitbox-on-the-blade-*` checks would still pass, because they measure the
hitbox against the numbers rather than against the picture.

| | |
|---|---|
| active ticks sampled | 9, each facing |
| worst endpoint error | **3.8 × 10⁻⁶ px** right, **3.9 × 10⁻⁶ px** left |

**The trade-off.** The character's most characteristic object is not generated
art, in a film about generated art. That is the honest cost of keeping what you
see and what kills you derived from one source.

---

## The 15 `.import` sidecars are INCLUDED, and they are inert

Worth a note because I got this wrong first and the correction is the
interesting part. I had written them into the exclusions on the grounds that
they were untracked editor artefacts, and that hashing them would break an
anonymous clone — the Assignment 1 failure. **They are tracked, all 15 of
them**, so a clone has them and hashing them is safe. The evidence reference
says to include `.import` sidecars because they *can* hold authored import
settings, so they are in the ledger.

What they actually contain is more useful than their presence. Two things:

1. **Every parameter is a Godot default.** No authored override — not
   `compress/mode`, not `mipmaps/generate`, nothing.
2. **There is no texture-filter setting in them at all.** Godot 4 moved canvas
   texture filtering off the import step and onto the CanvasItem, defaulting to
   the project setting. So `rendering/textures/canvas_textures/default_texture_filter=0`
   in `project.godot` is where "nearest" lives, and the sidecars have no say.

And the game never reads them. Every asset load goes through
`ProjectSettings.globalize_path("res://assets/…")` into `Image.load_from_file`
or `AudioStreamOggVorbis.load_from_file` — an absolute OS path, bypassing
`res://` import entirely. That is deliberate: a `--headless --script` run does
not rescan the filesystem, so `load()` on an unimported asset fails in exactly
the situation the assignment asks to verify, a fresh checkout.

So the ledger carries 15 files that the running game does not consult, the
`.godot/imported/*.ctex` they point at are not in the repository, and the film
says that rather than implying a normal import workflow the project does not
use.

## Excluded, and counted

| | reason |
|---|---|
| `tests/capture_walkthrough.gd` | Assignment 1's film capture driver, carried over and unused by this assignment. |
| `.gitignore`, `game/main.tscn` | 8 and 168 bytes; no mechanism to teach. `main.tscn` instantiates `session.gd` and nothing else. |

---

## What this film does not explain

- The dungeon's drawing code, the HUD, the enemies and the traps' geometry.
  All original vector art, all explained in Assignment 1's film, and reusing
  that ground here would crowd out the five components above.
- The level data format. Unchanged from Assignment 1.
- The three optional poses and the environment asset. **Not generated** — named
  in the verdict rather than taught.
