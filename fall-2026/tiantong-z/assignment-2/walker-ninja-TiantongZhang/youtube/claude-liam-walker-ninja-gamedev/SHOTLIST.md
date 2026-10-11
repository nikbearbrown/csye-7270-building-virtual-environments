# SHOTLIST.md — what is on screen, beat by beat

`godot-gamedev walker` · 15 beats · **294.40 s — 4:54**, measured off the
master, not a target length.
Durations are the Kokoro `am_onyx` narration as generated; nothing is padded to
a round number.

Teaching contract **`code-then-result-v1`**: each code excerpt is followed
immediately by the result those lines produce, bound by hash in
`gamedev-evidence.json`.

| # | act | s | surface | on screen |
|---|---|---|---|---|
| B00 | ASK | 16.8 | `ClaudeComposerAsk` | The reconstructed Walker prompt, typing on, labelled **reconstruction — illustrative, not a transcript**. Three result lines: the generated inventory, the eight poses, and that the blade stays in code. |
| B01 | RESULT | 32.3 | `BrutalistHesitantWriter` | "Walker generated my game." — then **game** is struck and **character** written in its place. Three cards: generated, unchanged, NOT generated. |
| B02 | BUILD | 20.1 | `GodotDevWorkbench` code | `player.gd` 118–131, `pose_key()`. Four timed highlights: death first, the live window, the dash, the sign of vertical velocity. |
| B03 | RESULT | 10.6 | **take-p** 0.15–7.20 | 7.05 s of real play: idle, run, rise, fall, run, idle, rise, dash. Last frame held 3.51 s. |
| B04 | BUILD | 27.4 | `GodotDevWorkbench` code | `player.gd` 313–326, `_mrect_o` / `_mpoly_o`. Highlights: the one-way growth, *x is forward*, the polygon translation. |
| B05 | RESULT | 21.7 | `GodotDevWorkbench` asset | `media/B05-poses.png` — all eight sprites at 32 px, on the wall / as silhouettes / on the torchlit edge. |
| B06 | BUILD | 20.2 | `GodotDevWorkbench` code | `session.gd` 276–288, `advance_traps()`. Highlights: the trigger gate, `trap_risen[i] == 0`, the rise offset. |
| B07 | RESULT | 15.5 | **take-t** 0.20–8.88 | 8.68 s: the whole run out to trap 0, the arming, the death, the prone pose, the respawn. Held 6.77 s. |
| B08 | BUILD | 27.9 | `GodotDevWorkbench` code | `session.gd` 601–611, the music guard. Highlights: the guard, `playing or stream_paused`, the cold start. |
| B09 | RESULT | 17.4 | `GodotDevWorkbench` asset | `media/B09-suite-output.png` — the two retry checks and the suite total, rendered verbatim from the recorded run. |
| B10 | BUILD | 21.9 | `GodotDevWorkbench` code | `player.gd` 678–690, `_draw_swing()`. Highlights: `ATTACK_PIVOT`, `phase >= 2`, the blade bar. |
| B11 | RESULT | 6.9 | **take-p** 6.90–8.36 | 1.46 s: landing, windup, the live arc, recovery. Held 5.43 s — the action is 16 ticks and no window makes it longer. |
| B12 | VERDICT | 31.3 | `ClaudeVerdictArtifact` | Eight lines: what was generated, what was not, the missing seed, 113 checks, and the two art bugs that passed all of them. |
| B13 | TURN | 19.3 | `ClaudeComposerAsk` | One bounded change — generate the ninth pose — with the prediction first and the check that will *not* settle it. Liam signs off here. |
| B14 | OUTRO | 5.0 | `ClaudeTitleOutro` | Locked card. `NewWalkerArt_TiantongZhang`, `@NikBearBrown`, one mascot, no subline, no narration, stock jingle only. |

---

## The three held frames, disclosed

`hold_s` is derived, not chosen: measured narration minus clip length. Nothing
is retimed and no action is repeated.

| beat | clip | hold | why |
|---|---|---|---|
| B03 | 7.05 s | 3.51 s | Comfortable. The first cut of take-p was 4.33 s against a 10.56 s narration, so the take was re-rendered longer rather than the frame held for seven seconds. |
| B07 | 8.68 s | 6.77 s | The whole take. The hold lands on the respawn, which is a near-static frame anyway. |
| B11 | 1.46 s | 5.43 s | **The worst ratio in the film, and it is structural.** The swing is 16 ticks — 0.27 s — and the beat has to show wind-up, live and recovery. The narration was cut from 29 words to 20 to shorten the hold; the held frame is the recovery pose, which is legible. |

## A known limitation: the two asset beats waste their left panel

B05 and B09 use `GodotDevWorkbench` in `asset` mode, which lays out
`{code}{image}`. **Their `code` is empty**, because the teaching contract says a
result beat may not be a code excerpt — so the left panel renders as a dark box
with a single blank line number, about 45 % of the frame.

This was found by rendering the master and looking at it; Gate V does not catch
it, because its CANVAS-FILL check measures the content bounding box and the
panel chrome fills the safe area.

**What was tried.** The right panel's image area was *measured* off a rendered
master — **1529 × 987**, aspect 1.549 — and both evidence images were recomposed
to exactly that. They now fill it. Before that they did not: B05 was a
938 × 1484 grid, which fits by height and leaves **59 % of the panel's width**
unused, and B09 was a 1809 × 530 band, which fits by width and leaves 55 % of
its height. Guessing at "squarer and larger" made B05 worse, not better; the
measurement is what fixed it. B05's sprites now render at an integer 7×, and
B09's text at 42 px instead of an effective 29 px.

**Why the empty panel was not fixed.** The alternatives were to put a real
source excerpt in the left panel, which would make the beat a code excerpt and
break `code-then-result-v1`; to use `GodotDesignBoard`, whose `image` layout
gives the visual the larger column but requires an `excerpt` field that would
then hold something that is not an excerpt; or to extend the shared component.
The skill says to extend a shared component only for a real missing teaching
need, and doing that in a toolkit I do not own, the day before a deadline, is
the riskier call. So this is the aesthetic cost of reusing a component
correctly, recorded rather than hidden.

## What the film does not show

- The dungeon's drawing code, the HUD, the enemies, the traps' geometry, the
  level format. All Assignment 1 ground, all still original vector art.
- `capture_character.gd`, `capture_game.gd`, `capture_enemies.gd`,
  `route_driver.gd`, `test_keyboard.gd`. Named in the verdict or the exclusions,
  not taught.
- The three optional poses and any environment asset. **Not generated.**

## Capture provenance

Both takes are native `3840 × 2160 @ 60 fps` Godot Movie Maker output of the
640 × 360 logical canvas at an exact 6× integer scale, driven through real
`InputEvent`s by `godot/tests/capture_gamedev.gd`, which asserts its own
outcome — so a finished render is not the claim; the take's `CAPTURE OK` line
is.

| | ticks | s | frames |
|---|---|---|---|
| take-p | 501 | 8.35 | 502 |
| take-t | 533 | 8.88 | 534 |

No test-fixture teleporting, no `test_*` input injection, no silent retiming.
The engine audio is carried into the capture MP4s.
