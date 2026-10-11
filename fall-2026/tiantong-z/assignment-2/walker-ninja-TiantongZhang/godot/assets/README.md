# godot/assets/

Everything here is a **placeholder** until Assignment 2's generated assets land.

| File | What it is | Replaces | To be replaced by |
|---|---|---|---|
| `death-laugh.ogg` | 3.42 s of **silence**, generated with `ffmpeg anullsrc` | Assignment 1's meme laugh, third-party with no documented permission | a generated sound effect |
| `death-laugh-cat.png` | a flat colour card reading PLACEHOLDER | Assignment 1's meme cat image, same rights problem | generated art, or the reaction is cut |

The duration is 3.42 s on purpose: `test_game.gd`'s
`enemy-death-reuses-the-reaction` asserts the reaction's remaining time, so a
placeholder of the same length keeps the suite green without weakening an
assertion. The assignment forbids deleting a failing assertion to get a green
report; this keeps it passing honestly instead, and says so here.

**Neither Assignment 1 asset was copied into this repository**, so no
undocumented-rights file exists anywhere in its history.


## Added 2026-10-05

| File | What it is | Generated? |
|---|---|---|
| `music-loop.ogg` | 16 bars cut from a purchased Suno download, 30.9632 s, 20 ms crossfade at the wrap | **yes** -- Suno `v6-mini`, see `ASSET-LOG.md` |
| `sfx-jump.ogg` | 0.110 s | **no** -- synthesised by `scripts/synth_placeholder_sfx.py` |
| `sfx-slash.ogg` | 0.140 s | **no** -- same |
| `sfx-trap.ogg` | 0.260 s rising inharmonic metallic sweep | **no** -- same |
| `sfx-death.ogg` | 0.450 s | **no** -- same |

The four effects are **placeholders in the same sense as the two files above
them**: they make the slice audible so that the masking check from `CONCEPT.md`
revision 1.1 can actually be run, and they are replaced file-for-file by
generated versions without any change to the wiring or the assertions.
