# walker-ninja-TiantongZhang

**CSYE 7270, Assignment 2 — Generate Art, Sound, and Music for Your Game.**
Tiantong Zhang · `zhang.tiant@northeastern.edu`

A 2D side-scrolling dungeon slice: a cyber-ninja with a double jump, an air
dash and a sword, against pop-up spike traps, patrolling slimes and flying
horses. It continues the Assignment 1 build rather than starting a new game.

| | |
|---|---|
| Repository | <https://github.com/TiantongZhang1/walker-ninja-TiantongZhang> |
| Engine | Godot **4.7.2.stable.official** `ed1daf0bf`, GL Compatibility |
| Resolution | 640 × 360 logical, 1280 × 720 windowed, `canvas_items` stretch |
| Physics | 60 Hz fixed |
| Automated checks | **113 — 0 failures** |

---

## Run it

Double-click **`run-game.bat`**.

There is no standalone `.exe` — this is a Godot project, so the editor binary
runs it from `godot/project.godot`. The `.bat` finds Godot relative to itself,
so moving the whole course folder is fine; separating this repository from the
Godot download is not, and if that happens the script says where it looked
instead of flashing a console and vanishing.

By hand, if you prefer:

```bash
"…/Godot_v4.7.2-stable_win64.exe" --path godot
```

From a fresh clone:

```bash
git clone https://github.com/TiantongZhang1/walker-ninja-TiantongZhang.git
```

The clone is **byte-identical** to what was committed, on Windows included.
That is not automatic — `.gitattributes` carries `* -text` for it, and the
comment in that file explains the Assignment 1 failure it exists to prevent.

### Controls

| | |
|---|---|
| `A` / `D` or arrows | move |
| `Space` | jump — once more in the air |
| `Shift` | air dash — **air only, once per airborne period, not invincible** |
| Left click | sword swing |
| **`0`** | **mute everything** |
| `R` | retry |
| `Esc` / `P` | pause |
| `Enter` | start · resume · play again |
| `M` | main menu, from pause or the results screen |

---

## What Assignment 2 added

| | state |
|---|---|
| **Music** — a 16-bar loop, on its own bus, surviving retries without restarting | **done**, generated (Suno `v6-mini`) |
| **A mute key**, on the Master bus, with a HUD indicator | **done** |
| **A dungeon setting** — stone wall, mortar courses, blind arches, wall torches, torchlit platform edges | **done**, original vector art |
| **A character with parts** — head, torso, two arms, two legs, directional rim light | **done**, original vector art |
| **A death pose** — prone, face down, the only pose wider than it is tall | **done**, original vector art |
| **Four sound effects** — jump, slash, trap warning, death | **wired; the audio is a placeholder, not generated** |
| **Generated art** | **done** — a reference plus eight poses, imported, checked and wired in. The blade is still drawn in code on purpose |
| **The film** | **done** — `NewWalkerArt_TiantongZhang.mp4`, 4:54, 3840×2160. Built in `youtube/claude-liam-walker-ninja-gamedev/`. Filename, size, hash and links are in [The film](#the-film) below |

`SOURCES.md` is the authoritative answer to *which of these did you actually
generate*. `godot/assets/README.md` is the one-table version.

---

## Verify it

```bash
GODOT="…/Godot_v4.7.2-stable_win64.exe"

"$GODOT" --headless --path godot --script res://tests/test_game.gd      # 99 checks
"$GODOT" --headless --path godot --script res://tests/test_keyboard.gd  # 14 checks
```

Both print one JSON object per check with **what it observed**, a final count,
and exit non-zero on any failure. Full results, including the numbers and the
three defects they caught, are in **`TEST-REPORT.md`**.

To regenerate the rendered evidence (these need a window — and note that
`--quit-after` counts *process* frames, not physics ticks, which is why the
number is large):

```bash
"$GODOT" --path godot --script res://tests/capture_game.gd      --quit-after 200000
"$GODOT" --path godot --script res://tests/capture_character.gd --quit-after 200000
"$GODOT" --path godot --script res://tests/capture_enemies.gd   --quit-after 200000
python scripts/check_trap_visibility.py     # spike drawn only while lethal
python scripts/check_enemy_visibility.py    # enemies drawn at their live positions
python scripts/build_char_sheet.py          # the 11-pose contact sheet
python scripts/synth_placeholder_sfx.py     # re-synthesise the placeholder effects

# once a pose has been generated -- see PROMPTS.md
python scripts/import_pose.py design/character/CHAR-P1.png --id p1-idle
```

Requires Python 3.12 with numpy, scipy and Pillow, plus `ffmpeg` on PATH.

---

## The film

The reel and all of its evidence live in
[youtube/claude-liam-walker-ninja-gamedev/](youtube/claude-liam-walker-ninja-gamedev/).
`./art godot-gamedev --check` **PASSes**: 18 source files inventoried, 5
components, 5 exact excerpts and 5 code-result pairs under the teaching
contract `code-then-result-v1`. Gate V samples 30 frames and reports 0 BLOCKER
and 0 MAJOR.

| | |
|---|---|
| Filename | `NewWalkerArt_TiantongZhang.mp4` |
| Size | 22,949,169 bytes (21.9 MB) |
| SHA-256 | `ae1668c0f5a44aa2c4bbdc689b51509bf2fd5e49ce3277198126f57ee2c9dff6` |
| Length | 294.40 s — 4:54 |
| Container | H.264 / AAC, 3840 × 2160, 30 fps, stereo 48 kHz |
| Game source demonstrated | `959f81b` — see below |
| URL | [northeastern-my.sharepoint.com/…/NewWalkerArt_TiantongZhang.mp4](https://northeastern-my.sharepoint.com/:v:/g/personal/zhang_tiant_northeastern_edu/IQDaPDnYendrTa9zgO53DBA0Ac_JPpgwzdAxPDHmO5Il5bY?e=Kfo2SC) |
| Also | [the submission folder](https://northeastern-my.sharepoint.com/:f:/g/personal/zhang_tiant_northeastern_edu/IgDg_vNibymFRo2cVCga_osiAVqFHeLr3Zj7NWzq7mmhysY?e=Hg0KSJ), which holds the film and a `CHECKSUM.txt` beside it |
| Access | Northeastern OneDrive. The links are **not public** — they require a Microsoft sign-in |

A **project archive** is submitted alongside: a `git archive` of the tagged
commit, named `walker-ninja-TiantongZhang-<short>.zip`. It holds exactly the
files that commit tracks — no `.godot/` cache, no `*.mp4`, no `*.wav`, no
credentials — and the film is not in it:

```bash
git archive --format=zip --prefix=walker-ninja-TiantongZhang/ -o walker-ninja-TiantongZhang-$(git rev-list -n1 --abbrev-commit a2-submitted).zip a2-submitted
```

`git rev-list -n1 --abbrev-commit`, not `git rev-parse --short` — the latter prints the annotated **tag object's** SHA, not the commit's.

The MP4 is deliberately **not** in this repository: it is over 25 MB and this
project keeps `*.mp4` out of git. It is reproducible from the tagged revision —
see
[BUILD-PROMPT.md](youtube/claude-liam-walker-ninja-gamedev/BUILD-PROMPT.md).

Verify the copy you were given is the one this README describes. **Download it
first** — a web preview is a re-encoded stream, the download is the original
bytes:

```bash
sha256sum NewWalkerArt_TiantongZhang.mp4
# ae1668c0f5a44aa2c4bbdc689b51509bf2fd5e49ce3277198126f57ee2c9dff6
```

### What game source the film shows

`959f81b`, stated precisely because the loose version of the claim is wrong.
`godot/game`, `godot/features`, `godot/levels` and `godot/ui` are
**byte-identical** between `959f81b` and the submitted tag:

```bash
git diff --name-only 959f81b a2-submitted -- godot/game godot/features godot/levels godot/ui
```

returns nothing. `godot/project.godot` *does* differ, by one line's **position**
only — Godot rewrote the file on save and moved
`textures/canvas_textures/default_texture_filter=0` above the renderer keys.
Same key, same value, same section. The commit that did that was `4b7dbff`, so
"`959f81b` is the last commit that touched the game" would not be true; "the
game source the film demonstrates is `959f81b`'s" is.

The capture driver `godot/tests/capture_gamedev.gd` was extended after the
first pass, inside `take_p()` only. `take_p` was re-recorded with the final
driver; `take_t`'s code path is untouched. All five of the ledger's
code-result pairs were re-verified against the files on disk at compile time.

### What the film does not prove

That the artwork is *right*. The footage shows the character moving and the
pose log shows which key was live; neither says the drawing is correct, and
`TEST-REPORT.md` section 6 says so first. Two of the film's fifteen beats also
render an empty code panel across the left ~45% of the frame — a limitation of
the shared component's `asset` layout, declared in that folder's `SHOTLIST.md`
rather than hidden.

---

## Read it

Written in this order, and the order is the point — each one is append-only, so
revisions are added and earlier text is never rewritten.

| file | what it is |
|---|---|
| **`CONCEPT.md`** | the game in one page, four design pillars, then revisions 1.1–1.4 as each decision landed: the music's feel, the art style, the dungeon, the character rebuild |
| **`CHARACTER-SHEET.md`** | the generation spec — palette with measured contrast ratios, 11 poses mapped to states the code can actually distinguish, and the acceptance order a generated frame has to survive |
| **`STORYBOARD.md`** | six panels on the level's own signage, with the method and per-panel coordinates, plus seven hand-drawn frames |
| **`CANVAS-NOTE.txt`** | the submission note as pasted into Canvas: every field the assignment asks for, the film's links and hash, and the declared gaps in one place |
| **`CHANGE-BRIEF.md`** | what changed in the code, revision by revision, each one naming its **predicted failure** and the check for it before the change was made |
| **`ASSET-LOG.md`** | one row per generation kept or seriously considered, including every rejection, with two corrections left standing above the text they correct |
| **`TEST-REPORT.md`** | 113 checks with their observed values, the three defects they caught, and **what was not checked** |
| **`SOURCES.md`** | provenance for every file, in four categories, with the one open rights question flagged |
| **`FRICTIONAL.md`** | the honest log. What was wanted, what was decided, what went wrong, and for each entry what was mine and what was Claude's |
| **`PROMPTS.md`** | everything still to be generated, in the order to generate it, as text to paste — derived from the two documents above it, never a decision of its own |

---

## Layout

```
CONCEPT.md  CHARACTER-SHEET.md  STORYBOARD.md  CHANGE-BRIEF.md
ASSET-LOG.md  TEST-REPORT.md  SOURCES.md  FRICTIONAL.md  PROMPTS.md
README.md  run-game.bat

godot/
  project.godot              640x360, nearest texture filter, dark clear colour
  game/session.gd            level, dungeon drawing, traps, enemies, audio, state
  game/main.tscn
  features/player/player.gd  movement, dash, sword, the body as a parts list
  features/player/tuning.gd  every gameplay number, in one Resource
  ui/hud.gd                  bands, cards, progress, mute indicator
  levels/first_steps.json    geometry, traps, enemies, labels — data, not code
  assets/                    music loop, four sound effects, two placeholders
  assets/README.md           which of these is generated: one table
  tests/test_game.gd         99 checks
  tests/test_keyboard.gd     14 checks, through the real InputMap
  tests/capture_*.gd         real rendered-viewport captures, each asserting its state
  tests/route_driver.gd      the input route that completes the level

design/
  storyboard/                the hand-drawn sheet and its seven crops
  rejected/                  the Suno library screenshot — eight tracks, with prompts

evidence/
  screens/                   21 rendered frames + the character contact sheet
  mechanics-*.json           every suite run, kept
  keyboard-*.json

scripts/
  import_pose.py             a generated pose -> a checked 32x32 sprite
  synth_placeholder_sfx.py   the four placeholder effects, deterministically
  check_trap_visibility.py   pixel check: the spike is drawn only while lethal
  check_enemy_visibility.py  pixel check: enemies are drawn where they really are
  build_char_sheet.py        the contact sheet, from real frames
  build_level_map.py         the level as one wide image
```

`scripts/` also holds the film pipeline — `build_coverage.py`,
`build_media_clips.py`, `build_source_snapshot.py`, `encode_captures.py`,
`render_takes.py`, `record-build.cjs`, `build_beat_sheet.py`,
`build_beat_bookends.py`, `build_gamedev_ledger.py`, `finalise_beat_timing.py`,
`fit_beat_panels.py`, `compose_b05_evidence.py`, `compose_b09_evidence.py` —
and the capture driver `godot/tests/capture_gamedev.gd`. All of it was used to
build this assignment's film; `youtube/claude-liam-walker-ninja-gamedev/BUILD-PROMPT.md`
is the order to run them in. `mix_death_laugh.py` and
`godot/tests/capture_walkthrough.gd` are carried over from Assignment 1 and
were **not** used here.

---

## Known state, stated plainly

- **The character is generated art; the dungeon is not.** Eight poses are
  imported and wired in (`godot/assets/poses/`). The dungeon, the HUD, the
  enemies and the traps are still original vector drawing in code. The
  character's **blade** is also still code-drawn, deliberately: it and the kill
  hitbox come from the same three numbers.
- **Two edits are applied to every generated pose** by
  `scripts/import_pose.py` — the directional rim, and restoring the visor
  through the downscale. Both are edits to generated assets rather than
  properties of the generation, and `ASSET-LOG.md` says so.
- **The art was generated on a tool that exposes no seed**, which breaks this
  project's own requirement. Deliberate, and the reasoning is in
  `ASSET-LOG.md` rather than silent.
- **The four sound effects are placeholders**, synthesised by arithmetic, and
  they do not satisfy the assignment's "generate sound" requirement. They exist
  so the masking check from `CONCEPT.md` revision 1.1 can be run at all, since
  it cannot be run against silence.
- **The film was watched end to end on 2026-10-06** by me, at playback speed,
  and accepted — the empty left panel on the two asset beats included, which
  was shown and named as a declared defect before being accepted. Gate V's own
  report says visual content review remains required; that is what closed it.
  `youtube/claude-liam-walker-ninja-gamedev/_qc/REPORT.md` records it as the
  one-sentence pass it was.
- **Four human checks were run on 2026-10-06** — the loop seam, the masking
  check, the retry behaviour and a muted playthrough. All four came back
  acceptable, in one sentence covering all four. `TEST-REPORT.md` section 6
  records it as exactly that: a pass with no detail is weaker evidence than a
  failure with detail would have been.
- **The music is non-commercial use only.** Suno owns it — the tracks were
  generated on the free tier, and the single-download pack bought afterwards
  purchased a download, not a licence upgrade. A graded submission and an
  unmonetised film are inside that grant; selling or monetising this slice
  would mean replacing the music first. `SOURCES.md` section 3 records what was
  checked and what was not.
- **One open rights question**: the licence terms of the art generator.
  `SOURCES.md` section 3.
- **The suite does not assert what the player character looks like.** Every one
  of the 113 checks is behavioural. Two real art defects passed all of them.
  `TEST-REPORT.md` section 6 explains why a pixel-diff of the player is not the
  answer.

---

## Credit

Built on **Nik Bear Brown's `walker-jumpman` "First Steps"** starter, by way of
my own Assignment 1 extension
[`walker-jumpman-TiantongZhang`](https://github.com/TiantongZhang1/walker-jumpman-TiantongZhang)
at commit `d1a52cd`. The starter's eight movement values are unchanged and the
code says so where they are declared.

Written with **Claude Code** as a pair. Attribution is per-commit in
`Co-Authored-By` trailers, and per-decision in `FRICTIONAL.md`, which records
for every entry which parts were mine and which were Claude's.
