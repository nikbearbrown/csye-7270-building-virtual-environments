# Film sources

Game: Downfall (walker-downfall), Godot 4.7.2-stable, Forward+ / D3D12, RTX 4060 Laptop GPU. Filmed from git commit `6f980233fe3c31f11b4957b50b30e020bae61fda`; the ledger hashes the working tree, which had no tracked-file modifications at filming (gamedev-evidence.json source_revision).

## Code shown
Exact excerpts listed in gamedev-evidence.json (path, lines, text). Editor views are Godot editor reconstructions (GodotDevWorkbench), not screen recordings.

## Existing engine evidence (same build, hashed in the ledger)
- FIXTURE captures: captures/hit_spark/r0, r0-snow, r1, r1-snow; captures/fire_pit_flames/r0, r0b, r1 (Movie Maker, 30 fps, preview scenes).
- USER SCREENSHOTS: evidence/a6/gpu/*.png (Visual Profiler), evidence/a6/user/fire_pit_preview_occluded_by_boulders.png.
- Mutation fixture frame: evidence/a6/mutations/m1_godot3_name_frame12_fixture.png. Logs: logs/*.log, evidence/a6/mutations/*.log.

## New captures for this film (capture/, gitignored; commands and logs beside the frames)
All windowed Godot 4.7.2 Movie Maker, `--fixed-fps 30`, 1280×720, run by tools/run_captures.sh from this folder. No game file was edited; the two helper scripts live in tools/ and are loaded with `--script`.
- capture/a_play (B03): tools/capture_play.gd — SCRIPTED-INPUT fixture: real main.tscn and loop, real left-mouse events (as tests/test_hit_spark_state.gd), fixture dummy enemies; city, seed 2026; hit_spark.tscn at r1 (Puff 1.0; sha256 in effect-hashes.txt). A first take (capture/a_play_take1_r0settings_occluded, Puff 0.5) was not used: a map prop hid the dummy.
- capture/b_loop (B05): previews/fire_pit_flames_preview.tscn -- --loop, 540 frames.
- capture/a_loop_city (B11): previews/hit_spark_preview.tscn -- --loop, 660 frames; captured after the r1 edit (Puff 1.0).
- capture/b_states (B21): tools/capture_fire_states.gd — fixture with an on-screen FIXTURE label: feed, tree pause, hide/show, burn to 24 s, burn to 0 via FirePit.feed()/burn().
Enlargements use nearest neighbour and are labelled with their factor. Takes shorter than their beat are replayed once and labelled REPLAY. Nothing is retimed.

## Textures
None sourced; the effects use GradientTexture2D/1D and CurveTexture written inside the scene files (SOURCES.md of the game).

## Toolkit, voice, music
Brutalist toolkit (local brutalist.art): godot-gamedev skill, walker modifier; ai-explainer chassis; riff. Voice: local Kokoro am_onyx (Liam, in for Bear), not a clone. Outro: locked ClaudeTitleOutro with the toolkit's stock jingle (outro-audio.json). No paid calls, no Higgsfield, no captions.
