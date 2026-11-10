# Gate V — visual QC report

Frames sampled: 64  ·  BLOCKER: 0  ·  MAJOR: 0

Clean — no BLOCKER/MAJOR defects. ✓
## Manual frame review (Claude Code, 2026-11-06)

96 frames read from the master `exports/landscape/claude-liam-walker-magic-particles-gamedev.mp4` (SHA-256 `ac6fb7bf9505d96fee604199e93993430528b7f5bb1ab086b841fe249cdff3bb`, 608.7 s), three per beat (15 / 50 / 85 % of each span), plus every card PNG and every Remotion render at full size before compiling. Audio: narration peak −2.9 dB (mean −27.2 dB); the outro's last 6 s at −91 dB (silent, as designed).

Corrected before this master:
- Cards under-filled (type 44–58 px, half-empty panels) on B02, B05, B06, B09–B28: layouts now pick the largest type and whole zoom that pass their own overflow checks (`media.py` `fit`). The copied `crops_and_table` caption claimed "outlined squares are the sampled pixels" with nothing outlined: replaced by new grid layouts.
- B14 line numbers touching the text at large sizes: the text column now scales with the font.
- GodotDevWorkbench does not scroll: B03 (pilot) showed lines 39–48 of an excerpt to 63 while the cue read "Line 63". Excerpts narrowed (B03 43–49, B08 25–36, B15 25–38 at the component's minimum 23 px); the rest in labelled source notes. B11, B15 and B17 notes clipped at the column bottom: shortened.
- B01's correction never fired: the writer swaps single words, and the trigger was "a picture". Now "picture" → "program"; narration regenerated. Gate V then found B01 under-filled at its midpoint (MAJOR, 35 %): typing sped up (30 ms per character) and enlarged, so the whole overview is up before the middle.
- Gate V BLOCKER edge-bleed on B04, B13, B19: the 640×360 canvas at ×5 ended at y 2100, past the title-safe bottom (2052). Canvas moved to y 250 (bottom 2050); the header note moved under the title after it collided with a long heading.

Remaining, accepted: the strip crops on B16 and B18 are small (×4) because the trail strips are 4:1 slivers; B02 and B05 leave some space at the bottom; the cards carry the source line in the footer but no @NikBearBrown corner bug (as in the Assignment 3 and 5 films); the code views, composer beats and verdict carry it. Gameplay is scripted input, not a human playtest; how the effects read in play is the author's judgement.
