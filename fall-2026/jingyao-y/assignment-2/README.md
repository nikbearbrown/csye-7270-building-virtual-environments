# assignment-2 — Downfall: generated art, sound and music

Assignment 2 for CSYE 7270, by Jingyao Y, with Claude Code assistance.

| What | Where |
|---|---|
| Film | https://youtu.be/n6yPUyUQEaM |
| The submission form | [downfall-godot/SUBMISSION.md](downfall-godot/SUBMISSION.md) |
| Design documents | [CONCEPT](downfall-godot/CONCEPT.md) · [STORYBOARD](downfall-godot/STORYBOARD.md) · [CHARACTER-SHEET](downfall-godot/CHARACTER-SHEET.md) · [CHANGE-BRIEF](downfall-godot/CHANGE-BRIEF.md) |
| Verification | [TEST-REPORT](downfall-godot/TEST-REPORT.md) |
| Sources and asset log | [SOURCES](downfall-godot/SOURCES.md) |
| Frictional log | [FRICTIONAL.md](FRICTIONAL.md) |
| Design images | `downfall-godot/design/`: storyboard frames, character captures, silhouette, collision overlay, pose sheet, thumbnails of raw and rejected generations |
| Generated audio | `downfall-godot/audio/`: Gemini music and stings (OGG), the two event WAVs, prompts, cut log, cutting scripts |
| Game | `downfall-godot/`: the Godot project (`project.godot`, `game/`, `entities/`, `world/`, `ui/`, `tests/`, `art/`, `godot_assets/`) |
| Film sources | `downfall-godot/youtube/claude-liam-downfall-gamedev/`: beat sheet, generator scripts, capture script and input logs, source ledger, fact check, QC report |

**The Godot project is in `downfall-godot/`**. It holds all code, tests and scenes, plus every asset the game loads (949 files); open `downfall-godot/project.godot` in Godot 4.7.2. Its game files are identical to https://github.com/coldfish432/GodotGame at `100dce3`. That repository also keeps the generation batch history (previews, revision rounds, originals), which is not copied here.

The film's MP4/MP3 files are excluded by this repository's media rule; the film's SHA-256 is in `SUBMISSION.md`. The two generated WAV cues are force-added, because the game loads them.
