# CHECKS-REPORT

## Source and teaching contract

`/Users/…/brutalist.art/art godot-gamedev --check . --game <repo>/godot` (2026-10-15 00:33 EDT):

```
"status": "PASS", "source_files": 17, "exclusions": 73, "components": 5,
"exact_excerpts": 3, "teaching_contract": "code-then-result-v1", "code_result_pairs": 3
```

It checks hashes, inventory, source lines and code→result adjacency; not whether the explanation is true or the
pictures good. The on-disk `godot/` inventory equals `git ls-tree c0dba4c godot` (no stray files).

## Final compile

`art final . --height 2160 --fps 30`: 21/21 beats filled. GATE F (FACTCHECK, SHOTLIST, PROMPTS present) first
refused the build until those files existed. The final frame check (42 frames, each beat at 50 % and 85 %) refused
two candidates: B01 under-filled the safe area (22 % / 44 %, then 32 % / 52 %; minimum 55 %). Fixed by shorter,
larger lines and one more sentence of narration; the third candidate passed with 0 blockers, 0 majors.

## Visual QC by Claude (frames read, not just probed)

| Beat | Found | Fixed |
|---|---|---|
| B01 | third line clipped at the left edge (150 px) | shorter lines at 185 px |
| B04 | "−0.22" drawn as a box: Hiragino Sans GB lacks U+2212 | Chinese set in STHeiti Light |
| B05 | line 51 touched the code panel's right edge | 45 px code |
| B09 | the after-screenshot overlapped the quoted note | smaller screenshot; callout moved onto the Rotation fields |
| B10, B12, B14 | the last source note cut off by the panel | shorter notes |
| B11 | terminal and table text too small for 4K | PASS lines only at 32 px; table at 46 px |
| B13, B15 | "held last frame" label covered the room's help line | label moved to the bottom right |
| B16 | Chinese wrapped only at spaces (ragged) | character wrapping for Chinese in `tools/compose.py` |

## Audio

Narration levelled to −16 LUFS per beat (single-pass loudnorm; measured −19.1 to −17.5 LUFS after); the master
measures −18.0 LUFS integrated, peak −1.9 dBFS; no silence longer than 2.5 s below −50 dB. The film has no
game-sound beats (the room has no audio). Bao still has to watch and listen to the whole film.
