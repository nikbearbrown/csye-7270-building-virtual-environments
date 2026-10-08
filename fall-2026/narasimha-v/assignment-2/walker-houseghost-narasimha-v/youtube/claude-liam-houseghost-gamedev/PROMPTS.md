# Prompts used for this film

**Narration** — none. Every word Liam speaks is written by hand in
`beat_sheet.json` and synthesised locally by Kokoro (`am_onyx`). No text model
wrote the script.

**Game assets** — recorded per asset in the project's `SOURCES.md`, with the exact
prompt text, model, date and outcome for every generation kept or rejected. The
film shows one of them verbatim in B10.

**Scene components** — no prompts. Scenes are rendered from
`GodotDevWorkbench`, `ClaudeComposerAsk`, `ClaudeVerdictArtifact` and
`ClaudeTitleOutro`, driven by props in the beat sheet.

**Figures** — `_figures/*.png` are composed from the project's own files with
Pillow. No figure contains generated imagery that is not already an asset of the
game or a rejected take of one.
