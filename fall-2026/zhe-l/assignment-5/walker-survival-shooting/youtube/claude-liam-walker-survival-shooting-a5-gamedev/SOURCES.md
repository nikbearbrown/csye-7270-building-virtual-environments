# Sources — claude-liam-walker-survival-shooting-a5-gamedev

- **Game:** walker-survival-shooting, course repository `fall-2026/zhe-l/assignment-5/walker-survival-shooting/godot/`, files read at a84cfa23; game source last changed in 2d558bba. Every code excerpt was read from these files at build time (`scripts/author_sheet.py`), never retyped; `./art godot-gamedev --check` binds them by hash.
- **Documents the narration relies on:** `LANGUAGE-NOTES.md` (the four questions), `CHANGE-BRIEF.md`, `TEST-REPORT.md` sections 1–9, `godot/MATERIALS.md`, `FRICTIONAL.md`, `SOURCES.md`, `logs/`. See `FACTCHECK.md`.
- **Engine captures:** see `CAPTURE.md`. Godot v4.7.2.stable.official.ed1daf0bf, Forward+, D3D12.
- **Textures shown on the crates:** Metal041C by ambientCG (Lennart Demes), CC0 1.0 (`godot/assets/shader/metal041c/ATTRIBUTION.md`).
- **Narration:** local Kokoro (`kokoro-onnx`), voice `am_onyx`, presented as "Liam, narrating for Jonathan" (chosen by the user). No voice cloning, no paid service.
- **Toolkit:** brutalist.art `godot-gamedev` skill, walker mode. Remotion scenes used: `ClaudeComposerAsk`, `BrutalistHesitantWriter`, `GodotDevWorkbench`, `GodotDesignFigure`, `ClaudeVerdictArtifact`, `ClaudeTitleOutro`; no new component. Two local changes to `runtime/scripts/remotion_scenes.py` for speed (render concurrency 4 instead of 1; an optional 1080p preview tier that is re-rendered at 4K automatically before the final); output pixels unchanged (150 frames compared, identical).
- `./art doctor` stops on a guard that finds a paid-TTS vendor name in the toolkit's own example reels; each dependency it checks was run separately and is ready.
