# Build prompt and steps — claude-liam-walker-survival-shooting-a6-gamedev

The request (from the user's main Claude Code session, which started this film session): make the required Brutalist Godot explainer for Assignment 6 (particle effects) with the course `godot-gamedev` skill in walker mode, landscape 4K; real engine output only (fixture strips or captures of the running game), with fixtures, scripted input, film cameras, code-set states and held frames labelled; never a reconstruction presented as a screenshot; every claim traceable to the submitted files; capture on a copy, never change the course repository; show the user the film before anything is committed.

Steps (run from `<brutalist.art>`; REEL = this folder; GAME = `git archive` of the course repository's `assignment-6/walker-survival-shooting/godot` at 1828bb6b):

```bash
godot_console --path <copy> --headless --import
godot_console --path <copy> --rendering-driver d3d12 --fixed-fps 30 --script res://film_capture/play_capture.gd -- shot=landing out=<film-work>/a6/captures/landing-run-02
godot_console --path <copy> --rendering-driver d3d12 --fixed-fps 30 --script res://film_capture/play_capture.gd -- shot=lights cam=film out=<film-work>/a6/captures/lights-film-01
python -I REEL/scripts/make_figures.py
python -I REEL/scripts/author_sheet.py --tbd          # must list nothing before voicing
python -I REEL/scripts/author_sheet.py
python3 runtime/scripts/generate_audio_kokoro.py REEL
python -I REEL/scripts/author_sheet.py --rebuild      # keeps measured audio, re-syncs cues
python -I REEL/scripts/prepare_media.py --hold-b 3    # PLAY_A, PLAY_B (B16 narration 15.66 s > clip 13.03 s)
python -I REEL/scripts/make_evidence.py
python -I REEL/scripts/make_docs.py
./art godot-gamedev --check REEL --game GAME
ART_REMOTION_SCALE=1 python3 runtime/scripts/remotion_scenes.py REEL      # 1080p preview tier
ART_REMOTION_SCALE=1 ./art run REEL --height 1080                        # preview film
python3 runtime/scripts/remotion_scenes.py REEL                           # 4K tier
./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape
./art godot-gamedev --check REEL --game GAME
```
