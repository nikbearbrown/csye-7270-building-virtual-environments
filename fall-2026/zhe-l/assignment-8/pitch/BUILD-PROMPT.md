# Rebuild the pitch film

The film was built with the Brutalist toolkit (local checkout at commit 22264a3; `show-tell` skill for the drawings), Godot 4.7.2 Movie Maker for the game footage, local Kokoro for the voice, and headless Microsoft Edge for two document frames. Everything is free and local; no keys, no paid generation, no upload.

Placeholders: `<brutalist.art>` = the toolkit checkout, `<film-work>` = my film work folder, `<course-repo>` = this repository, `<working-folder>` = my local working folder (its Chinese draft of the beat sheet is not in this repository).

## The prompts
The film session was driven from Claude Code (Claude Opus 5.5) by my requests, in Chinese, translated here:
1. "Let's discuss what our film needs to contain, what to stress, and what to ask the instructor." Then the seven answers, given one by one (recorded in PROJECT-BRIEF.md and FRICTIONAL.md).
2. "Go through them one by one": the 19 beats were reviewed one at a time; then "compress the narration first", "translate the narration first".
3. "You capture it": record the footage from the uploaded commit with scripted input.
4. "Narration only says landing dust."
5. "Start making the film", in the show-tell isometric style.

## The commands
```bash
# 1. the game copy (never the course repository itself)
git -C <course-repo> archive f13431bf fall-2026/zhe-l/assignment-8/walker-survival-shooting/godot | tar -x -C <film-work>/a8/game --strip-components=4
godot_console --headless --path <film-work>/a8/game/godot --import
# copy film-scripts/capture/*.gd, *.tscn into <film-work>/a8/game/godot/film_capture/

# 2. scripted-input captures (Movie Maker, 30 fps); A8_CAPTURE_LOG_DIR = where the capture logs go
godot_console --path <copy> res://film_capture/a8_capture.tscn    --write-movie <film-work>/a8/captures/b10/frame.png    --fixed-fps 30 --resolution 1920x1080 -- seq=b10
godot_console --path <copy> res://film_capture/a8_capture.tscn    --write-movie <film-work>/a8/captures/b11/frame.png    --fixed-fps 30 --resolution 1920x1080 -- seq=b11
godot_console --path <copy> res://film_capture/a8_capture_os.tscn --write-movie <film-work>/a8/captures/tablet/frame.png --fixed-fps 30 --resolution 1920x1080 -- seq=tablet
godot_console --path <copy> res://film_capture/a8_capture_os.tscn --write-movie <film-work>/a8/captures/mome1/frame.png  --fixed-fps 30 --resolution 1920x1080 -- seq=mome1
godot_console --path <copy> res://film_capture/a8_capture_os.tscn --write-movie <film-work>/a8/captures/mome2/frame.png  --fixed-fps 30 --resolution 1920x1080 -- seq=mome2

# 3. document frames: rerun the six tests in the copy, then screenshot the README Keys and the test logs
bash scripts/run-test.sh <test>.gd 60        # six tests, output kept as logs/b12-<test>.txt
python -I film-scripts/capture/make_doc_frames.py <course-repo>/.../pitch/README.md <film-work>/a8/logs <film-work>/a8/captures/docs

# 4. the reel (REEL = <film-work>/a8/reel/walker-survival-shooting-pitch)
python -I film-scripts/make_sheet.py                       # writes REEL/beat_sheet.json (the copy here is that output)
python3 <brutalist.art>/runtime/scripts/generate_audio_kokoro.py REEL
python -I film-scripts/finish_audio.py                     # pads the outro by 1.0 s, measures every beat
python -I film-scripts/prepare_media.py                    # media/<BID>.mp4 with burned-in labels and held frames
# scenes.py goes into REEL (it carries the show-tell iso kit inline)
cd <brutalist.art>
./art run REEL --height 1080                               # Gates L, A, W, B, then compile, then Gate V
python3 runtime/scripts/bookend_check.py REEL
python3 runtime/qc/factcheck_check.py REEL
./art final REEL --height 1080 --out REEL/exports/landscape   # Gate T, then the verified master
```

## Result
`walker-survival-shooting-pitch.mp4`, 1920 × 1080, 210.9 s, SHA-256 `4ab1cd281cbb0afe7f93d5a4129e047a2b6885d6ce32f2261ca65cb577edf980` (kept out of git; delivered as `walker-survival-shooting-pitch-1080p.mp4`). Gate reports: `gate-reports/`. Earlier rounds that failed a gate (Gate B: two labels outside the safe area; Gate V: low contrast in B02, edge bleed in B03 and B06) and one round I rejected myself (the CONSTRUCTED tag appeared a few seconds late) are recorded in FRICTIONAL.md.
