# BUILD-PROMPT — rebuild the pitch film

All tools are local and free. Paths are from the author's machine. `ROOT` is the folder that contains `downfall-godot/`, `brutalist.art/` and the Godot 4.7.2 executable.

## 1. Gameplay captures (about 45 min of offline rendering)

Clone commit `1fbc309a` into a scratch folder. In the clone, edit `project.godot` as listed in `capture/CAPTURE.md`:

- 4K window override
- `movie_writer/mjpeg_quality=0.95`
- `config/name="downfall-pitch-capture"`, so the clone gets its own `user://`

Then copy `capture/capture_pitch_film.gd` into the clone's `tests/` and run:

```bash
godot --headless --path <clone> --import
for spec in title:2026:1500 mine:2026:3000 regions:2026:1800 bridge:2026:900 route:2026:900 camp:2026:1200 base:2026:1200; do
  IFS=: read clip seed cap <<< "$spec"
  godot --path <clone> --script res://tests/capture_pitch_film.gd \
    --write-movie ROOT/build/pitch-raw/$clip.avi --fixed-fps 30 --quit-after $cap -- $clip $seed
done
```

Check each clip against `capture/raw-avi-sha256.json`. Movie Maker output is deterministic per seed, but it can differ across drivers, so a hash mismatch means the clip needs to be inspected, not that the build failed.

## 2. Reel folder and narration

```bash
REEL=ROOT/downfall-godot/youtube/rhodes-daily-final-pitch
mkdir -p $REEL/{media,audio,tools,mp3}
cp pitch/beat_sheet.json $REEL/
cp pitch/film-tools/make_media.py $REEL/tools/
cd ROOT/brutalist.art
PYTHONUTF8=1 python3 runtime/scripts/generate_audio_kokoro.py $REEL
```

- Voice: `am_onyx`.
- B14 is intentional silence: `audio/end-silence.wav`, 5 s, made with `ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 5`.
- After Kokoro, pad the narration of the capture beats with trailing silence so the footage is not rushed: `ffmpeg -i in.mp3 -af apad=pad_dur=<s> out.mp3`.
- The pad lengths are in each beat's `audio_pad_s`: B00 4, B02 7, B03 3.5, B04 7, B05 6, B06 6, B09 3.
- Write the padded duration back to `actual_duration_s`.

## 3. Beat clips

```bash
cd $REEL && python3 tools/make_media.py
```

- Capture beats are windows cut from the AVIs, never retimed, each with a label strip.
- Graphic beats are Pillow boards labelled CONSTRUCTED.
- B06 uses the raw Movie Maker frames of A6 `capture/a_play` and A7 `capture/wave_dodges`.

## 4. Compile and gates

```bash
cd ROOT/brutalist.art
PYTHONUTF8=1 python3 runtime/scripts/compile.py $REEL --height 2160 --fps 30 --out $REEL/exports/landscape
```

`compile.py` refuses to write the film unless these pass:

- Gate F: FACTCHECK, SHOTLIST and PROMPTS are present.
- Gate V: frame-level visual QC.

Capture beats declare `qc.full_bleed` and a `contrast_regions` box on their label strip, each with a written reason in the beat sheet.

The final run gave **BLOCKER 0, MAJOR 0** (`gate-reports/gate-v-REPORT.md`). The SHA-256 of the output is in `gate-reports/rhodes-daily-final-pitch.verified.json`.

## The prompts

The prompts given to Claude Code are in `gate-reports/PROMPTS.md`.
