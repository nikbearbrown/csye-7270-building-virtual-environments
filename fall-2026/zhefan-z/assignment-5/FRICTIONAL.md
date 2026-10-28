# FRICTIONAL — Assignment 5

What I tried, what happened, what I checked and changed, and who did what. Organized by claude.ai (chat) from my session of 2026-10-22 to 2026-10-28; every entry is something that happened, checked by me. "Agent" means Claude Code (desktop app, Opus 5.5, manual permission mode).

## Entries

**1. Setup: pasted commands ran in the wrong folder (2026-10-22).** My first paste of the setup block lost its `cd` to a bracketed-paste control character, so every command ran in my home folder; git refused each one, and `mkdir` left empty folders and an empty tar file. I checked with `find` that nothing else was created and deleted them. After that I ran setup in short blocks joined by `&&`. Later pastes of long commit messages were cut off twice and left the shell waiting at `>`; shorter commands fixed it.

**2. Fresh import flagged 31 `.import` files as modified.** `git diff` showed nothing. I compared hashes: all 31 were byte-identical to the committed files (`31 SAME`); `core.autocrlf=true` caused the flag. I added `.gitattributes` rules so Godot text files stay LF (`220d61d`, `b764841`; suggested by claude.ai).

**3. Claude Code CLI failed twice before Step 1.** First `claude -p` run: "Not logged in", while the result event still said `"subtype":"success"`, so I now read `is_error` and `result`, not `subtype`. Second: CLI 2.1.220 too old for Opus 5.5 (`session-1-failed-run2.jsonl`). I ran Step 1 in the desktop app instead, with manual permissions (`1793c4f`).

**4. CLAUDE.md review.** The agent's draft cited a log that was not committed and is overwritten on every run, and described the blink as toggling every tick (it toggles every 0.1 s). I checked every file reference with `sed -n` (all line numbers in `player.gd` were right), fixed those two, and added Headless facts (`d893e68`). The draft also found that `rock.glb` has two materials, which my brief had missed; I decided only `Rock_Main` gets the shader (brief revision 2026-10-23).

**5. My first shader save was empty.** My headless probe printed `Parameter "shader" is null`. Moving the query after the main loop started still failed, then `CODE_LEN 0` showed the file was 0 bytes: Notepad had created it but my text was never saved. I re-saved and the probe listed both uniforms (`8936403`). The probe also taught me that `get_shader_uniform_list()` only works headless after the main loop starts, which I passed to the agent in prompt-2.

**6. R7 failed at 144 fps (inspect-and-revise cycle).** The agent's test measured the paused window by summing frame time: 1.0000 s at 30 fps, 0.9833 at 60, 0.9653 at 144, outside R4's tolerance. The agent stopped and offered to widen the tolerance or drop the clause. I rejected both: widening to two physics steps (0.0333 s) still would not cover 0.0347 s, so it would be fitting the tolerance to the data, and dropping a failing assertion is not allowed. I revised the brief first to measure in unpaused physics ticks (`b81bad4`); the test then counted 59 ticks at 144 fps while frame time still said 0.9653 s, so no ticks were missing (`9072f67`). The explanation (pause shifts which frames ticks land on) is still not confirmed.

**7. Mutations.** Deleting a semicolon gave `SHADER ERROR`, an empty uniform list and 1 failure. Renaming `intensity` in the shader only gave no error: 15 checks still passed because `set_shader_parameter` silently stored the old name; only the uniform-list and source-default checks failed (`9e5894d`). Removing `source_color` from the rock albedo sampler failed `test_materials` (`5ebfa15`).

**8. Use External would have broken an Assignment 3 test.** In its plan the agent found that `test_a3_assets.gd:106–107` expects the A3 `StandardMaterial3D` on `Rock_Main`, so Use External in `rock.glb.import` would fail an earlier suite I may not edit. It recommended letting the test fail and recording it. I rejected that and its alternative (an override in the A3 prop room) and revised the brief: both rocks in a new `material_compare.tscn` carry the material as a scene override, which a reimport does not touch (`47ce061`). The earlier suites stayed at 95 checks / 0 failures.

**9. Pure red could not test `hint_range`.** While writing the capture prompt, claude.ai noticed that with a pure red target every intensity of 1.0 or more gives (255, 0, 0), so a capture at 2.0 could not tell clamped from unclamped. I captured that case with a grey tint instead: (23, 25, 15) and (197, 191, 95), exactly the unclamped prediction, which also showed that a 2D `source_color` colour uniform is used as stored.

**10. Captures against my predictions.** All controlled values matched except the two channels that land on .5 (243.5 and 156.5), which the GPU wrote one step lower than my round-half-up; I had marked them ±1 in the brief. The hint quads matched all six values. The audit predicted the DXT1 roughness error (up to 13 of 255) might show 4×4 blocks at the frost edge; when I looked at the frost capture I saw a frost layer and no blocks.

**11. The editor rewrote `project.godot` on open.** It dropped two keys equal to their defaults (`audio/buses/default_bus_layout`, `window/stretch/aspect`). No behaviour changed; I restored the file after closing the editor. No `.import` file was rewritten, also after deleting `.godot`.

**12. Mistakes claude.ai made that I caught or it corrected.** It guessed a line number (`player.gd:52`, really 51) before checking; miscounted `prompt-1.txt` (32 lines, really 31); suggested "restart" as a retrigger rule before we saw it would need a game-logic change; and misread one of my answers about the frost edge. Each was corrected before it reached a committed file.

## Human and AI contributions

- **Mine:** every decision in CHANGE-BRIEF and its four revisions; the colour line and all uniform and sampler declarations; all hand computations (pixels, contrast, hint experiment); the three shaders, typed by me (for `rock_frost` and `hint_experiment`, claude.ai gave syntax examples and the idea of widening the frost threshold beyond 0–1; the formula, band 0.1, ice roughness 0.15 and endpoint check are mine); the language answers; every human check, capture key press, play test and the editor conversion of the generated shader.
- **Claude Code:** the CLAUDE.md draft, the driver, `test_hurt_tint.gd`, the hint PNG writer, the four materials, two scenes, the calibration and inspection scripts, the audit (`MATERIALS.md`, `test_materials.gd`) and the capture scenes. Accepted after review; changes I asked for: approve only step 1 then step 2, skip its optional CLAUDE.md edit, R7 in physics ticks, scene overrides instead of Use External, every uniform written explicitly.
- **claude.ai (chat):** planning, commands, checking my arithmetic and line references, compiling CHANGE-BRIEF and LANGUAGE-NOTES from my answers (translating my Chinese), reviewing CLAUDE.md and MATERIALS.md with me, and drafting this file and TEST-REPORT from what happened.

## Still open

- Why the .5 channels round down on the GPU, and why a pause shifts frame time by more than one physics step, are both untested explanations.
