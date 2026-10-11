# SOURCES.md — this film's own materials

The game's provenance is `../../SOURCES.md`. This file covers what the **film**
is made of.

## Footage

Both takes are native `3840 × 2160 @ 60 fps` Godot Movie Maker output, driven
through real `InputEvent`s by `godot/tests/capture_gamedev.gd`.

| | source revision | ticks | frames | encoded |
|---|---|---|---|---|
| take-p | the repository tip at capture time | 501 | 502 | `capture/take-p.mp4` |
| take-t | same | 533 | 534 | `capture/take-t.mp4` |

Hashes are in `gamedev-evidence.json` → `code_result_pairs[].media`. The
lossless frame sequences are reproducible with
`python scripts/render_takes.py p t --out <dir> --driver res://tests/capture_gamedev.gd`
and are gitignored; 165 MB for 17 seconds of 4K.

**Movie Maker fixes its output size from the window at engine startup**, before
`--resolution` and before any script runs, so the size comes from a temporary
`godot/override.cfg` that `render_takes.py` writes and removes. Without it the
same command silently records 1280 × 720 — which is how Assignment 1's first
take was produced, and why the script verifies three PNG headers per take.

## Stills

| | what it is |
|---|---|
| `media/B05-poses.png` | Built from the eight committed sprites in `godot/assets/poses/` by `scripts/compose_b05_evidence.py`. Three bands, one per background: on the dungeon wall, as solid silhouettes, on the torchlit platform edge. Sprites are nearest-neighbour at an integer 7×, so the pixels stay pixels. |
| `media/B09-suite-output.png` | A monospace render of `media/B09-suite-output.txt` by `scripts/compose_b09_evidence.py`. Check names, values and their order are verbatim; **the two JSON payloads are wrapped one key per line**, because the recorded lines are 91 characters wide and a 91-character line in this panel renders at 29 px on a 3840-wide frame. The wrap buys 42 px. Nothing is reworded, reordered, rounded or dropped. That `.txt` is the recorded stdout of `godot --headless --script res://tests/test_game.gd`. |

Both are composed at **1529 × 987**, which is the workbench's right-hand image
area measured off a rendered master. An earlier pair was composed to no
particular aspect and rendered inside that area with up to 59 % of its width
unused.

Both are tracked, against this repository's usual rule of keeping media out of
git, because the ledger hashes them and a reviewer has to be able to recompute
those hashes.

## Narration

**Kokoro-82M**, local, Apache-2.0, voice `am_onyx`. No API, no account, no
cost. 14 of 15 beats; B14 is the locked outro card and carries no narration by
rule. `mp3/timings.json` holds the measured durations, which are ground truth
for every downstream timing in `beat_sheet.json`.

## Editor views

Every code panel is `GodotDevWorkbench`, a shared component of the toolkit,
reused rather than redrawn — `./art scenes` was run first and reported it as
the match. The views are labelled **"Godot editor reconstruction ·
source-backed teaching view"** on screen. They are teaching views, not
recordings of a live editing session, and every displayed line is extracted
from the hashed file by `scripts/build_gamedev_ledger.py`, which refuses to
build if the text, the beat's props and the file disagree.

No property is shown as an Inspector value. The right-hand column is labelled
**"Source notes — not Inspector values"**, because ordinary script variables are
not exported fields and this project has almost none.

## Outro

`ClaudeTitleOutro`, locked per `OUTRO-LOCK.md`: exact title, `@NikBearBrown`,
one slug-seeded mascot, no subline, existing stock jingle only, no narration
and no game audio.

## The master

| | |
|---|---|
| file | `exports/landscape/NewWalkerArt_TiantongZhang.mp4` |
| container | H.264 / AAC, 3840 × 2160, 30 fps, stereo 48 kHz |
| length | 294.40 s — 4:54 |
| size | 22,949,169 bytes |
| SHA-256 | `ae1668c0f5a44aa2c4bbdc689b51509bf2fd5e49ce3277198126f57ee2c9dff6` |

That hash also appears in the repository's own `README.md`, under **The film**,
and in `CHECKSUM.txt` uploaded beside the master — a grader expects it in the
README and a downloaded file should be able to describe itself. Three copies of
one number is a risk, so all three are written from the same `sha256sum` run and
the file is immutable once uploaded. `./art final` names its
output after the reel slug — `claude-liam-walker-ninja-gamedev.mp4` — and the
file is renamed to the locked title afterwards, so the toolkit's own
`build-state.json` records the pre-rename name and is gitignored for that
reason. The export itself is gitignored too, by the repository's rule that
media over 25 MB and all `*.mp4` stay out of git.

Gate V reports 30 frames sampled, 0 BLOCKER, 0 MAJOR, and says in its own words
that visual content review remains required. `_qc/REPORT.md` carries both
halves: the gate's, and the human inspection that followed it — which found two
things the gate does not check.

## Upstream material consulted

`skills/make/godot-gamedev/SKILL.md` and its `references/evidence.md`;
`RENDER-TARGETS.md`; `OUTRO-LOCK.md`; `docs/PIPELINE-SAFETY.md`. Assignment 1's
reel was read for the shapes of `ClaudeComposerAsk` and
`BrutalistHesitantWriter` props after `./art scenes --check` rejected two names
I had invented.

No secrets, no `.env` contents, and no absolute developer-machine paths are
embedded in any reusable skill or scene.
