# Gate V — visual QC report

Frames sampled: 62  ·  BLOCKER: 0  ·  MAJOR: 0

Clean — no BLOCKER/MAJOR defects. ✓
## Manual frame review (Claude Code, 2026-11-13)

93 frames read from the master `exports/landscape/claude-liam-walker-magic-animation-gamedev.mp4` (SHA-256 `ede03b7860729da965bc3b8f2ea71526c02e086abe19e1f2078f0eb413282ec5`, 375.3 s, 3840×2160, 30 fps, H.264 + AAC), three per beat (15 / 50 / 85 % of each span), plus every card PNG at full size and every Remotion render before compiling. Audio: narration peak −3.3 dB (mean −27.0 dB); the outro's last 6 s at −91 dB (silent, as designed).

Corrected before this master:
- First `art final` refused: Gate V MAJOR `underfill` on B01 at 50 % and 85 % (54 % of the safe area). The hesitant writer's type went from 190 to 235 px; the second export passed (0 BLOCKER, 0 MAJOR).
- GodotDevWorkbench does not scroll: the first renders of B10, B12, B15 and B23 cut the excerpt before the cued line (for example B10 ended at line 99 while the cue read "Line 100"). Excerpts narrowed (B10 93–101, B12 143–154, B15 152–163, B23 19–30) and type set so every line shows; the dropped lines moved into labelled source notes. The pilot (B07) showed the notes column clips a third note: every workbench now carries two.
- B18's second heading ran past the right margin at the largest type: the card layout now checks heading width, and the heading was shortened.
- B03 first included capture frame 441, which is empty (the scene had been freed between segments): real speed now ends at 439; the torch measurement stops at 440.
- B02 first showed both whole frames at ×2 with half the card empty: it now shows the same crop at ×3. B13 crops enlarged ×4 → ×5; B16's figure widened.

Remaining, accepted: the capture crops on B11 are small (×4 of a 50×84 px crop, 25 ticks on one card); the Muybridge plates on B06 and B09 are shown whole (the plate, not a crop) so each frame of the sequence is small; the cards carry their source in the footer but no @NikBearBrown corner bug (as in the Assignment 3, 5 and 6 films); the code views, composer beats and verdict carry it. The crosshair the game draws at the parked mouse position overlaps the top-right phase chip on gameplay beats by a few pixels; both stay legible. Gameplay is scripted input, not a human playtest; how the clips read in play is the author's judgement.
