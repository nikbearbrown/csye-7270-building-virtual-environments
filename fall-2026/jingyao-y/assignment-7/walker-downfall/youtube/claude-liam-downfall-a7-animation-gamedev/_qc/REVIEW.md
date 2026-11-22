# Agent frame review (manual)

Master: exports/landscape/claude-liam-downfall-a7-animation-gamedev.mp4, SHA-256 fff554fd6910f4f7cfa4eff609870ee66307507fee587af67537d8fac18149fe, 3840×2160, 30 fps, 466.8 s, H.264 + AAC 48 kHz.
Gate V (art final): 52 frames sampled, 0 BLOCKER, 0 MAJOR (_qc/REPORT.md). Previous export refused once (B01 underfill), fixed.

Looked at by the agent: mid-beat frames of all 26 beats (_qc/mid-all.png, before the B01 fix), 15/85 % samples of B01, B04, B10, B16, B18, B20, B22, B24, B25 (_qc/final-sample.png, b01_b25.png); every code beat at reading size (_qc/media/codesheet.png, cB03.png).
- B01: the correction "movie" → "list of keys" now plays (fixed after the first master).
- Code beats readable; B11/B17/B19 are the smallest (21–22 px at 1080p-equivalent), still legible.
- Labels present: "Godot editor reconstruction" on code views; FIXTURE / SCRIPTED-INPUT on captures; REPLAY on replayed takes; held boards are boards.
- Outro: locked title card, mascot, stock jingle (outro-audio.json); no narration on it.
Not checked: the full audio by ear end to end (only the ffprobe stream check), every frame of the 39 contact pages.
