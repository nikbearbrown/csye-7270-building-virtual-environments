# Build prompt and steps — claude-liam-walker-survival-shooting-a5-gamedev

The user's request (translated from Chinese): make the required Brutalist Godot explainer for Assignment 5 with the course `godot-gamedev` skill in walker mode, landscape 4K; real engine output only; label reconstructions, scripted input and held frames; every claim traceable to the submitted files; preview at 1080p, re-render only changed beats, render 4K once.

Steps (run from `brutalist.art`; REEL = this folder; GAME = the course repository's `assignment-5/walker-survival-shooting/godot`):

```bash
python -I REEL/scripts/make_figures.py
python -I REEL/scripts/prepare_media.py
python -I REEL/scripts/author_sheet.py --tbd          # must list nothing before voicing
python -I REEL/scripts/author_sheet.py
python3 runtime/scripts/generate_audio_kokoro.py REEL
python -I REEL/scripts/author_sheet.py --sync
python -I REEL/scripts/make_evidence.py
python -I REEL/scripts/make_docs.py
./art godot-gamedev --check REEL --game GAME
ART_REMOTION_SCALE=1 python3 runtime/scripts/remotion_scenes.py REEL      # preview tier
python3 runtime/scripts/remotion_scenes.py REEL                           # 4K tier (re-renders previews)
./art final REEL --height 2160 --fps 30 --out REEL/exports/landscape
./art godot-gamedev --check REEL --game GAME
```

Note: `./art run` calls the Remotion step itself; run it with `ART_REMOTION_SCALE=1` for a preview, otherwise it renders the 4K tier.
