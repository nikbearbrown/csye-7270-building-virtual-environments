# Film sources

Game: Downfall (walker-downfall), Godot 4.7.2-stable, Forward+ / D3D12, RTX 4060 Laptop GPU. Filmed from git commit `299ef97305ac5347081044695b17507457b31af3`; game source unchanged since `45cf5845` (TEST-REPORT.md). The ledger hashes the working tree (gamedev-evidence.json source_revision).

## Code shown
Exact excerpts listed in gamedev-evidence.json (path, lines, text). Editor views are Godot editor reconstructions (GodotDevWorkbench), not screen recordings.

## Existing engine evidence (same build, hashed in the ledger)
- The user's FIXTURE capture: captures/wave_release/r0/ frames 27, 29, 36, 37, 40, 41, 49, 50 (previews/wave_release_preview.tscn, Movie Maker, 30 fps, run by the user).
- Logs: logs/*.log, logs/a7_mutations/, logs/baseline-*/summary.txt.
- Images: art/characters/npc/npc_closure_idle.png and animations/lappland_rig/*.png (the actual files, enlarged nearest-neighbour).

## New captures for this film (capture/; commands, logs and source hashes beside the frames)
All windowed Godot 4.7.2 Movie Maker, `--fixed-fps 30`, 1280×720, run by tools/run_captures.sh. No game code, test or A7 document was edited.
- capture/wave_dodges (B20; log lines on B12): previews/film_wave_dodges.tscn, a film fixture written for this film — SCRIPTED-INPUT capture, not human play: real main.tscn and loop, a real click on a still stand-in enemy and real "dash" action events timed by reading the player's state; between takes a real ground click walks her back, and the fixture refills the charge and resets cooldowns and stamina (labelled). The first two runs were discarded: a parse error, then a take where the target lock let her auto-attack into a second release before take 2.
- capture/npc_in_game (B04, B06, B10): previews/npc_idle_in_game.tscn (an A7 review fixture) — the player is placed for framing; frames 40–370 base store, 400–760 the field squad. Cell changes measured by frame differencing every 10 capture frames (capture/npc_ranges.json).
- capture/rig_turntable (B16): previews/wave_rig_turntable.tscn — the rig alone on a grey plane, advanced 1/30 s per frame from capture frame 10.
Enlargements use nearest neighbour and are labelled with their factor. Takes shorter than their beat are replayed and labelled REPLAY. Nothing is retimed.

## Sheet and rig art
Fan art generated with gpt sol 6.1 (the user's statement); terms, date checked and prompts were not supplied (animations/ATTRIBUTION.md).

## Toolkit, voice, music
Brutalist toolkit (local brutalist.art): godot-gamedev skill, walker modifier; ai-explainer chassis; riff. Voice: local Kokoro am_onyx (Liam, in for Bear), not a clone. Outro: locked ClaudeTitleOutro with the toolkit's stock jingle (outro-audio.json). No paid calls, no Higgsfield, no captions.
