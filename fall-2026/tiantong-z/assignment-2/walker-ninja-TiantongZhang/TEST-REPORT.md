# TEST-REPORT.md — what was checked, what it said, and what was not checked

| | |
|---|---|
| Commit | `11fcc29a170536e783c6a2d84ccc192992c61e88` |
| Date | 2026-10-05 |
| Engine | Godot 4.7.2.stable.official.`ed1daf0bf`, GL Compatibility |
> **Correction, 2026-10-06.** This report said **110 checks — 96 in
> `test_game.gd`** until today. Both numbers were stale: three checks were added
> with the sprite wiring and the count here was never re-read off a run. The
> suite reports `WALKER TESTS: 99 checks / 0 failures`, and `test_keyboard.gd`
> reports 14, so the total is **113**. Caught because the film's FACTCHECK table
> cites section 1 of this report as the source for 113 and the two disagreed.
> The numbers below are re-read from a run of
> `Godot_v4.7.2-stable_win64.exe --headless --path godot --script
> res://tests/test_game.gd` on 2026-10-06, not edited to match the film.

| **Automated checks** | **113 — 99 in `test_game.gd`, 14 in `test_keyboard.gd`** |
| **Failures** | **0** |
| Pixel checks | 2, both PASS |
| Rendered evidence | 21 frames + 1 contact sheet |
| **Human checks** | **4 — all four run on 2026-10-06, all four acceptable** |

---

## 1. How to re-run all of it

```
GODOT="…/Godot_v4.7.2-stable_win64.exe"

# the suites (headless, no window, no audio device needed)
"$GODOT" --headless --path godot --script res://tests/test_game.gd
"$GODOT" --headless --path godot --script res://tests/test_keyboard.gd

# the captures (these need a window; --quit-after counts PROCESS frames, see §7)
"$GODOT" --path godot --script res://tests/capture_game.gd      --quit-after 200000
"$GODOT" --path godot --script res://tests/capture_character.gd --quit-after 200000
"$GODOT" --path godot --script res://tests/capture_enemies.gd   --quit-after 200000

# the pixel checks and the contact sheet, over those captures
python scripts/check_trap_visibility.py
python scripts/check_enemy_visibility.py
python scripts/build_char_sheet.py
```

Each suite prints one JSON object per check and a final count, exits non-zero
on any failure, and writes the whole run to
`evidence/mechanics-<unix>.json` / `evidence/keyboard-<unix>.json`.

**Every check records what it observed, not just pass/fail.** That is the point
of the format: a passing check with its numbers printed can be re-read later
and disagreed with. Several of the numbers quoted below are how the mistakes in
`FRICTIONAL.md` were found.

---

## 2. `test_game.gd` — 99 checks, 0 failures

### Movement, inherited and unchanged (checks 1–14, 41–44)

The starter's eight tuning values are not touched by this project, and these
checks are what says so rather than a comment.

| check | observed |
|---|---|
| `speed-cap`, `neutral-stop`, `simultaneous-directions`, `left-wall` | PASS |
| `fixed-jump-height`, `held-jump-no-bounce` | PASS — jump height does not depend on how long the key is held |
| `air-jump-exactly-two` | PASS |
| `air-jump-raises-apex` | single jump rises **56.07 px**, double **104.61 px** |
| `coyote-5` / `-6` / `-7` | PASS — the window is 6 ticks and the 7th tick is refused |
| `buffer-5` / `-6` / `-7` | PASS — same, for the jump buffer |
| `coyote-plus-air-caps-at-two` | PASS — a coyote jump spends the *first* jump, so the air jump is still in hand |
| `low-ceiling` | PASS |

### The dash (15–21)

| check | observed |
|---|---|
| `dash-refused-on-floor` | PASS — air only |
| `dash-refuses-second-in-air` | PASS — one per airborne period |
| `dash-displacement` | **66.667 px** measured against **66.7 px** analytic (400 px/s × 10 ticks ÷ 60) |
| `dash-air-locks-velocity` | `dy` exactly **0.0** |
| `jump-cancels-dash` | PASS |
| `dash-allowed-inside-coyote-window` | PASS |
| **`dash-not-invincible`** | PASS — this was a design requirement, not an accident |

### The sword (22–32)

| check | observed |
|---|---|
| `attack-phase-sequence` | PASS — 4 windup / 9 active / 3 recovery, summing to 16 |
| `attack-hitbox-live-only-in-active` | PASS — the hitbox is off during windup and recovery |
| **`attack-hitbox-on-the-blade-right`** | 9 active ticks sampled, **worst endpoint error 3.8 × 10⁻⁶ px** |
| **`attack-hitbox-on-the-blade-left`** | 9 ticks, **3.9 × 10⁻⁶ px** |
| `attack-hitbox-layers` | PASS — layer 6 (PlayerAttack) masking layer 3 (Enemy) only |
| `attack-ignores-press-mid-swing`, `attack-does-not-change-movement`, `attack-works-airborne`, `attack-grants-no-resources`, `attack-locks-facing-until-it-ends`, `attack-not-invincible` | PASS |

The two endpoint-error checks are the ones that matter: **what you see and what
kills are derived from the same three numbers** (`ATTACK_PIVOT`,
`attack_angle()`, `attack_reach`), and these measure the agreement rather than
asserting it. That invariant is why `CHARACTER-SHEET.md` section 2 forbids
baking the blade into a generated sprite.

### The death reaction (33–40)

| check | observed |
|---|---|
| `death-fx-assets-loaded` | PASS |
| `death-fx-outlasts-respawn` | PASS — the overlay lives as long as the sound, which is longer than the 0.55 s retry, on purpose |
| `death-fx-frozen-while-paused` | PASS |
| `death-fx-restarts-on-each-death` | PASS |
| `death-cat-does-not-cover-the-death-panel` | PASS — the first build hid the death reason behind the overlay |
| `death-fx-cleared-on-menu` | PASS |

### Retry, failure and the full route (45–58)

| check | observed |
|---|---|
| `pause-freezes`, `focus-loss-pauses` | PASS |
| `actual-spike-collision`, `duplicate-death-ignored`, `respawn`, `manual-restart-not-death` | PASS |
| `twenty-retries` | 21 deaths, **worst retry 34 ticks** |
| `fall-boundary`, `death-before-finish` | PASS |
| **`complete-real-route`** | reaches the finish in **1219 ticks with 0 deaths**, using 15 jump marks, ending at (3028.7, 319.9) |
| `replay-idempotent` | PASS — the same inputs twice give the same result |
| `hud-progress-spans-the-new-level` | PASS — derived from the level, not the starter's hard-coded 852 |

`complete-real-route` drives the **real InputMap-equivalent** inputs, not a
teleport: the level is provably completable.

### The pop-up traps (59–66)

| check | observed |
|---|---|
| `traps-start-buried-at-the-surface` | all four at y 320, the ground surface |
| `trap-rises-in-15-ticks` | **15** ticks, first tick 1, 14 further frames |
| `trap-does-not-retract` | PASS |
| `trap-trigger-is-one-way` | PASS |
| `trap-kills-when-risen` | PASS |
| `trap-shares-the-original-death-path` | PASS — same `resolve_contacts()`, only the message is new |
| `traps-reset-on-retry` | PASS |
| **`trap-warning-window-exceeds-rise`** | **32 frames of run-up per trap** against a 15-tick rise, worst case 32 |

That last row is the fairness argument in numbers: the player always has at
least twice the rise time between crossing the trigger and reaching the spike.

### The fork and the planks (67–69)

| check | observed |
|---|---|
| `thin-plank-does-not-tunnel` | lands at y **223.97** on a plank top of 224, at a peak fall speed of 480 px/s — **8 px per frame** through an 8 px plank |
| **`high-road-needs-the-dash`** | double jump alone lands back at y 319.9; double jump **plus** dash reaches y 223.9 |
| `high-road-clears-the-traps` | PASS — 0 deaths past the last trap |

`high-road-needs-the-dash` is the one that proves the fork is a real choice and
not decoration.

### The enemies (70–79)

| check | observed |
|---|---|
| `enemies-load-from-level` | 6 slimes, 5 horses, 11 total |
| `enemy-layers-serve-both-directions` | enemy layer 4, mask 2, slash mask 4 |
| `every-slime-patrols-on-solid-ground` | all supported, including the one on the high plank |
| `horses-hold-altitude` | all five still at y 268 after 260 ticks |
| `enemies-stay-inside-their-bounds` | 11 enemies, 260 ticks checked |
| `slash-removes-an-enemy`, `a-dead-enemy-is-harmless` | PASS |
| `enemy-contact-kills-the-player` | PASS, with its own message |
| `enemy-death-reuses-the-reaction` | PASS — the same reaction and the same 0.55 s retry |
| `enemies-reset-on-retry` | PASS |

### Music (80–87) — new in Assignment 2

| check | observed |
|---|---|
| `music-loop-is-flagged-to-loop` | loaded, `loop = true`, length **30.9632 s** — which is the cut recorded in `ASSET-LOG.md` |
| `music-is-on-its-own-bus` | bus `Music`, index 1 |
| `music-plays-during-a-run` | PASS |
| **`a-retry-does-not-restart-the-track`** | position **0.467 s → 0.557 s** across a `restart_attempt()`. It went forward |
| `music-pauses-with-the-game` | PASS |
| **`retry-while-paused-resumes-rather-than-restarts`** | PASS — a regression check, see §5 |
| `mute-is-a-master-bus-mute` | toggles bus 0, both directions |
| `music-stops-at-the-finish` | PASS — not left looping under the results card |

### The death pose and the sound effects (88–97) — new in Assignment 2

| check | observed |
|---|---|
| **`death-pose-is-the-same-whatever-killed-you`** | PASS across **spike, fall and enemy** — all three reach DYING with the prone pose set |
| `death-pose-clears-on-respawn` | PASS |
| `sfx-all-four-are-loaded-at-their-synthesised-lengths` | 0.110 / 0.140 / 0.260 / 0.450 s |
| `sfx-is-on-its-own-bus` | bus `Sfx`, index 2, distinct from `Music` |
| `sfx-jump-fires-once-per-jump` | 1 jump, 1 sound, at tick 4 |
| `sfx-slash-fires-on-the-swing` | 1 attack, 1 sound |
| **`sfx-trap-fires-on-the-trigger-not-the-contact`** | **warning at tick 24** with the player at x **1064.6** (trigger_x 1064); **death at tick 59**; **lead 35 ticks ≈ 0.58 s** against a 15-tick rise |
| `sfx-death-fires-on-the-fatal-contact` | 1 death, 1 sound |
| **`master-bus-has-a-limiter-because-two-sources-at-0db-clip`** | `AudioEffectHardLimiter` present, ceiling **−0.5 dB**, music at **−3.0 dB**; unlimited worst-case sum **1.512** |

The trap row is the most useful check added this assignment. "A sound played
when the trap killed me" would have passed while being useless to the player;
this one says the warning arrived **35 ticks early** and would fail if it were
ever moved onto the damage.

Nine rows over a ten-check range: position 93 in the run is a record the suite
emits under the bare id `jump`, inside `sfx-jump-fires-once-per-jump`. It
counts toward the 99 the suite reports, so it counts here, but it has nothing
of its own to show and naming it `jump` was not a good idea.

### The generated sprites (98–99) — new in Assignment 2

| check | observed |
|---|---|
| `pose-textures-all-eight-loaded-at-32x32` | 8 textures, all `32 × 32` |
| **`pose-key-matches-the-state-it-claims`** | PASS for idle, run, rise, fall, dash, windup, live and death — the key the drawing code asks for is the key the physics state implies |

**These two are the whole automated guarantee about the generated art, and
neither of them looks at a pixel.** The first counts textures and measures
their dimensions. The second drives the player into each of eight states and
checks that `pose_key()` returns the matching string — which is testable
precisely because it returns a string rather than a `Texture2D`. A pose file
could contain the wrong drawing, or a blank cell, and both would pass. That is
the subject of section 6.

---

## 3. `test_keyboard.gd` — 14 checks, 0 failures

Driven through **real `InputEvent`s and the real `InputMap`**, not the test
input-injection path, so the bindings themselves are covered.

| | |
|---|---|
| `keyboard-move`, `keyboard-jump`, `keyboard-air-jump`, `keyboard-air-dash` | PASS |
| `keyboard-dash-refused-on-floor` | PASS |
| `mouse-left-slashes` | PASS — the swing is a mouse button, so it needs an `InputEventMouseButton` |
| **`menu-click-does-not-swing`** | PASS — left click drives the HUD start button *and* the sword; this is the check that keeps them from overlapping |
| `escape-pause`, `enter-resume`, `enter-start`, `enter-replay`, `r-retry`, `pause-main-menu`, `menu-start-again` | PASS |

---

## 4. Pixel checks over real rendered frames — 2, both PASS

These exist because a green behavioural suite said nothing about **what was
drawn**, and a playtest once found a hazard that was lethal while still painted
underground.

### `scripts/check_trap_visibility.py`

Two frames at a **fixed camera position** (x 1117.2), differing only by the
spike's state, counting pixels of the spike colour `#d24e42`:

| | |
|---|---|
| buried frame | **0** spike-coloured pixels |
| risen frame | **767** spike-coloured pixels |
| verdict | **PASS — hidden while buried, drawn while risen** |

The spike colour was deliberately **not changed** during the dungeon re-skin,
because this script hard-codes that RGB. It sits at 4.15:1 against the dungeon
wall, so there was no reason to change it and a concrete reason not to.

### `scripts/check_enemy_visibility.py`

Three frames, five enemies, comparing each enemy's drawn body pixels against
its **live simulated position** rather than its spawn:

| frame | enemy | drawn at | moved from spawn | body px in the live box |
|---|---|---|---|---|
| `07-slime-and-horse` | slime #1 | x 1675.0 | 45.0 | 954 |
| | horse #2 | x 1715.0 | 45.0 | 823 |
| `08-contested-landings` | slime #5 | x 2196.0 | 20.0 | 1052 |
| | horse #6 | x 2284.0 | 12.0 | 819 |
| `09-plank-slime` | slime #0 | x 1373.0 | 17.0 | 1064 |
| verdict | | | | **PASS** |

---

## 5. Three defects these checks caught, with the check that caught them

Listed because a report of only passes is not a test report.

| defect | how it would have shipped | what caught it |
|---|---|---|
| **The music restarted at bar 1 on `pause → R`.** `AudioStreamPlayer.playing` reports **false** while `stream_paused` is true, so a guard written against `playing` alone replayed the track from the top. | Only on the pause-then-retry path. An ordinary death was fine, so casual play would not find it. | Not a check — **probing the engine** for what it actually reports in each state *before* writing the assertions. It is now the named regression check `retry-while-paused-resumes-rather-than-restarts`. |
| **The music and `SFX-TRAP` clip when their peaks align.** Music peaks 0.702, trap 0.810 after trim; sum 1.512. | Inaudibly. A handful of clipped samples inside a 0.26 s sweep is not reliably audible, and **every audio check before this one asked *whether* and *when* a sound plays, never what the sum of them looks like.** | Building an offline mix of the trap over the music in order to run the masking check. The render clipped at 1.172. Now asserted. |
| **The air pose put the boot inside the floor.** `y` is negative upward, so a leg lift must subtract; it added. The boot went to y +0.8 and the shin's height computed as 0.6 px. | It rendered as a glitch — 2 px of a 28 px character, for the duration of a jump. | Looking at the character contact sheet. **No check in this suite would ever have caught it**; see §6. |

---

## 6. What was NOT checked, and will not be

### The suite does not assert what the player character looks like

**Every one of the 113 checks is about behaviour** — where the hitbox is,
whether the trap is drawn, whether an enemy is at its live position, which tick
a sound fired on. None of them describes the figure on screen.

Two real defects in the character rebuild passed all 113 checks while being
obviously wrong on screen: the air-pose sign error above, and a rim that left
1 px of armour inside a 3 px arm so the limbs rendered as grey pipework.

**This is not going to be fixed with a pixel-diff of the player.** Such a test
fails on every intentional art change and gets deleted within a week, which is
worse than not having it. The honest position is that
`godot/tests/capture_character.gd` plus `scripts/build_char_sheet.py` **are**
the check — they assert the *state* of each of the 11 captured frames, and a
human has to look at the frames. That is a weaker guarantee than the rest of
this report and nothing in the submission should imply otherwise.

### Four human checks — run on 2026-10-06

All four need ears or eyes, not a script. All four were run and all four came
back acceptable.

**What was reported, in full:** *"检查完了，没问题"* — the checks are done, no
problems. That is a single-sentence pass covering all four, and it is recorded
as exactly that rather than expanded into four paragraphs of detail nobody
gave. A pass with no detail is weaker evidence than a failure with detail would
have been, and this report says so instead of dressing it up.

**H3 was a decision, not a pass/fail**, and this resolves it: `[TZ DECIDE]` #3
has been open since `CONCEPT.md` revision 1.1 — *what should the music do
during the 0.55 s retry.* It is implemented as "keeps playing", that is what
was listened to, and that is now the accepted answer. Ducking was the leading
alternative and is not being built.

| # | check | written down in | why it cannot be automated |
|---|---|---|---|
| **H1** | **The loop seam.** Play `music-loop.ogg` three times back to back and listen at the wrap (0:31, 1:02). | `CHANGE-BRIEF.md` C4 | The seam measured at the **10th percentile** of the track's own frame-to-frame spectral change and the waveform discontinuity is 0.00247 against a largest ordinary step of 0.33545 — 136× smaller. Those are strong numbers and **a number is not an ear.** |
| **H2** | **The masking check.** Play the trap section with music at full level and listen for the warning specifically. | `CONCEPT.md` revision 1.1, predicted 2026-10-01 | Masking is perceptual. This is the reason the placeholder effects exist at all: the check cannot be run against silence. |
| **H3** | **The retry behaviour.** `[TZ DECIDE]` #3 — what the music should do during the 0.55 s retry. Implemented as "keeps playing". | `CONCEPT.md` revisions 1.1–1.4 | Ducking is a bus-level change and should be decided against something heard. |
| **H4** | **A muted playthrough.** Press `0` and complete the level. | `CHANGE-BRIEF.md` C6 | The assignment requires the slice to stay understandable with all sound muted. The trap is fair on visuals alone — 15 frames of visible rise, 96 px of run-up, both measured above — so a failure here would mean the dungeon re-skin broke the visual warning, which is worth knowing. |

### Also not done

- **No art has been generated**, so `CHANGE-BRIEF.md` C2 (the sprite swap) is
  untested and C1's predicted non-integer-scale shimmer is unverified — there
  is no texture in the build to shimmer.
- **No sound effect has been generated.** The four in the build are
  placeholders; see `SOURCES.md` section 4.
- **The Suno download-pack licence has not been read.** It is the one open
  rights question in the project and it is flagged in `SOURCES.md` section 3.

---

## 6b. The clone is byte-identical, and that was checked

Not a claim carried over from Assignment 1 — re-run against this repository
after the first push:

```bash
git -c core.autocrlf=true clone https://github.com/TiantongZhang1/walker-ninja-TiantongZhang.git
```

`core.autocrlf=true` is **the Windows default**, and it is what broke
Assignment 1: it rewrites every LF to CRLF on checkout, which changes every
text file's length and therefore every per-file hash. An anonymous clone there
recomputed a `build_id` of `e83b9a83…` against the `82696a5d…` recorded in the
film's own evidence, so a reviewer following the documented verification would
have concluded the film did not match the posted source. `player.gd` alone
differed by 354 bytes, all of them carriage returns.

| | |
|---|---|
| Commits cloned | 25 |
| File list | **identical**, 135 files |
| File contents | **byte-identical**, all 135, with `core.autocrlf=true` |

The committed `.gitattributes` (`* -text`) is what makes that true, and the
comment in it is the record of why.

## 7. One environment note that cost real time

**`--quit-after` counts process iterations, not physics ticks.** A windowed
capture run renders uncapped, so 6000 "frames" can elapse in nine seconds of
wall clock while only ~450 physics ticks have happened — and the capture script
exits cleanly, three frames into a six-frame run, looking exactly like a
regression in whatever was changed last.

It is not. The headless suite passing on the same code is what isolates it. The
capture commands in §1 use `--quit-after 200000` for this reason.

---

## 8. Verdict

| | |
|---|---|
| Automated | **113 checks, 0 failures.** Gameplay, input bindings, audio behaviour and audio *timing* are covered, and three of the checks measure an invariant rather than asserting it. |
| Rendered | 21 frames and a contact sheet, with 2 pixel checks over them, both PASS. |
| Human | **4 of 4 run, 2026-10-06, all acceptable** — including H2, the masking prediction the assignment's argument rests on. Reported as one sentence without per-check detail, which is recorded as such in section 6. |
| Rights | 1 open item — the Suno download-pack terms. |
| Distribution | pushed to <https://github.com/TiantongZhang1/walker-ninja-TiantongZhang>; an anonymous clone is byte-identical, verified. |
| Generation | music only. Art and sound effects are specified but not generated. |
