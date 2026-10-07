# RIFF.md — commentary grounded in inspected output

- **Lappland's states.** The combat atlas has five drawn rows, and the narration says "the other three are mirrored". That comes from `COMBAT_ROWS` and the animator's flip logic, and the B04 capture shows her facing turns under real WASD events.
- **"Counted, but silent."** `FieldAudio.FILE_CUES` lists `hatch.wav` and `shelf.wav`, and neither file exists in `111bf6e`. In the B07 audio, the only warehouse cues are the light switches.
- **"Until she is killed."** In `death-inputs.jsonl` (map seed 2026), the run has settled (she is back in the base) by frame 349, about 11.6 s into the clip and about 9 s after the 继续 click at frame 80.
- **"The fail sting plays once."** `test_audio.gd` covers it ("two settles give one sting"), and the B10 capture shows a single sting.
- **"Forty-three percent isolated pixels."** This is Claude's independent measurement of R1 v1 (mean 43%, range 19–70%), recorded in the session and in `FRICTIONAL.md`.
- **"Five music files."** `git show --stat 111bf6e` lists `base_loop`, `mine_end`, `mine_loop`, `sting_extract` and `sting_fail` (each `.ogg` plus its `.import`).
