# Final Project Pitch — Rhodes Daily

- **Author:** Jingyao Y (CSYE 7270, Fall 2026)
- **Working title:** Rhodes Daily (repository name: Downfall / `downfall-godot`)
- **Target role:** gameplay programmer / technical designer
- **Runtime:** Godot 4.7.2, GDScript, Forward+ on D3D12, Windows desktop export
- **Film:** `rhodes-daily-final-pitch.mp4`, 3:20 (199.6 s), 3840×2160, 30 fps
  - SHA-256 `2857982f73bf474c19d4cfd8099ee8753cc3ea4bd81025816f72b4dbb8e79745`
  - Link: https://youtu.be/waHo7Zp4W48 (the .mp4 is 129 MB and is not in GitHub)

## What is in this folder

| File | What it is |
|---|---|
| `PROJECT-BRIEF.md` | The seven questions in text, plus *exists today* / *will exist* lists |
| `beat_sheet.json` | Narration and visual plan, with the build stamp from the final compile |
| `BUILD-PROMPT.md` | The commands that rebuild the film |
| `SOURCES.md` | What was used, made, and contributed by Claude |
| `FRICTIONAL.md` | Dated log of the work |
| `capture/` | How the gameplay was recorded: `CAPTURE.md`, the choreography script, input logs, raw-capture hashes |
| `gate-reports/` | Brutalist gate V report and contact sheet, the verified-output record, FACTCHECK, SHOTLIST, PROMPTS, media provenance |
| `film-tools/make_media.py` | Builds every beat clip from the raw captures and draws the labelled diagram boards |

## How to rebuild the film

See `BUILD-PROMPT.md`.

Gameplay is filmed from commit `1fbc309a`. Narration is local Kokoro. Assembly and gates use the Brutalist toolkit's `compile.py`, and nothing is paid or uploaded.
