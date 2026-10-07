# FILM-REVIEW — human-style QC of the master (Claude, 2026-10-04)

Master: `exports/landscape/claude-liam-walker-rudy-gamedev.mp4` · 3840×2160 · 30 fps · H.264 + AAC 48 kHz ·
595.67 s (9:56) · SHA-256 `cb2f01dbe7f0788b5a8c9196b8168e2f2151e4be09aee4febee018a1165528a0`
(matches `claude-liam-walker-rudy-gamedev.verified.json`, status `ready`).

This file is Claude's frame and sound review, not a human sign-off. **shuai-z has not yet watched the film.**

> **2026-10-07, human review:** shuai-z watched and listened to the whole final film (this master, same SHA-256) and
> reported "完整看过听过最终的影片了，没问题" [I have watched and listened to the whole final film; no problems].

## Gates (actual results)

| Gate | Result |
| --- | --- |
| `./art godot-gamedev --check` | PASS — 114 source files, 1 exclusion, 10 components, 15 exact excerpts, 15 code→result pairs (`code-then-result-v1`) |
| GATE T (`TYPECHECK.md`) | PASS |
| Gate V (`REPORT.md`, final-frame check, 86 samples) | 0 BLOCKER · 0 MAJOR |
| beat lint / shape | clean / n.a. |
| Retiming | none: no "slowed" or "center-cut" line in the compile; every gameplay clip was built at its beat's exact frame count |
| Loudness | whole film −24.4 LUFS integrated; B03 (game audio only) −23.8; narrated gameplay −23.8; outro voice −21.8; outro 1 s tail ≤ −50 dBFS (silence) |

## What I looked at

`tools/qc_frames.py` sampled every beat at 15/50/85 % (129 frames, `_qc/sheet-01…15.jpg`); I read every sheet.
Checked: code at reading size and fully inside its panel; the highlighted line matches the spoken phrase;
"Godot editor reconstruction" and source path/lines on every code beat; provenance, SOUND, REPLAY, HELD and
DIAGNOSTIC labels present and inside the title-safe area; the sound chips appear on the frame the log says;
the asset trace reads in order; verdict and Your Turn text; the outro card (exact title, @NikBearBrown, one
mascot, no subline).

## Defects found and fixed

| # | Found | Cause | Fix |
| --- | --- | --- | --- |
| 1 | Code panels cut off their last lines (B06 pilot) | 14+ wrapped rows in a ~13-row panel | every excerpt re-cut to fit (≤ 13 rows), five beats at the 23 px floor; B12's narration rewritten and re-voiced so it no longer points at lines moved out |
| 2 | ♪ rendered as a box on the sound chips | Inter has no ♪ glyph | chip text "SOUND SFX-X · Sfx.play(…)" |
| 3 | Long held frames (up to 6.6 s) in result beats | narration longer than the action | longer 1.0× ranges and labelled 0.25× replays; two lines re-voiced shorter; holds now ≤ 1.9 s, all labelled |
| 4 | GATE T min-size / accent-contrast FAIL on B16 | the matted sprite's hair and fine lines on the cream page read as small terracotta "text" | B16 became a code view; the frame moved to its own result beat B16R on a dark viewport backing, canvas and origin marked |
| 5 | GATE T §8.9 "truncated" on B00/BHTF | segment title ended in "In" without its period | the exact title, period included |
| 6 | Gate V low-contrast on all gameplay and B19 | whole-frame average measures the painted art | `qc.contrast_regions` on the provenance chip (gameplay) and on B19's headings/caption, each with a written reason |
| 7 | Gate V edge-bleed on B37, B19 | text/figures inside the 5 % margin | moved inside the safe area |
| 8 | Gate V underfill on BVD1/BVD2 | short verdict lines | fuller, more specific lines (no waiver) |
| 9 | **B01's correction never happened** — the writer kept "that AI generated." | the trigger phrase carried a period; the component strips punctuation before matching | trigger without punctuation; verified on frames: the wrong phrase is typed in terracotta, deleted, and "built from generated parts" typed |

Defect 9 passed every automated gate; it was caught only by reading frames.

## Declared waivers (reviewable in `beat_sheet.json`)

- `qc.full_bleed` on gameplay beats: the game draws edge to edge (hearts, debug line). Edge-bleed only.
- `qc.contrast_regions` + `contrast_reason` on gameplay beats and B19 (see 6).
- `qc.sparse_by_design` + `sparse_reason` on B01 (the hesitant writer types onto an empty page).

## Not verified / limits

- No person has watched or listened to the whole film; I sampled frames and measured audio. Watch it once
  end to end, with sound, before handing it in.
- The machine checks confirm hashes, line ranges and adjacency, not that every explanation is right.
- B03's level and the −14 dB game bed under narration were set by measurement, not by ear.
- The apex/rise/fall figures (B10) are the source comment's, not re-measured.
