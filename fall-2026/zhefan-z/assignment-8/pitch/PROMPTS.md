# PROMPTS — what was asked, and of whom

Written by Claude Code, 2026-11-22.

| # | Prompt | Who wrote it | Given to | Result |
|---|---|---|---|---|
| 1 | `prompt-1-pitch.txt` (in this folder): branch, brief commit, fact check, art renaming, the film's beat order, its labels and rules, the records | the author | Claude Code (Claude Opus 5.5), one session | this film and its records |
| 2 | One question from Claude Code: two files in `art/` were the same 2×2 expression sheet (a green 2048×2048 one and a transparent 1199×1312 cut-out); which becomes `witch_expressions.png`? | Claude Code | the author | "Green → expressions; drop cut-out": the cut-out stays untracked and is not in the film |
| 3 | The Gemini image prompts | the author, with claude.ai drafting some | Gemini 4 in the Gemini app | the concept art; recorded word for word in `ART-PROMPTS.md` |

No other model was prompted for this film: no paid generation, no API key, no upload. The narration is Kokoro `am_onyx` run locally by the toolkit (`generate_audio_kokoro.py --speed 1.05`), reading the script in `scripts/sheet.py`. Every picture is a real capture, the author's concept art, a figure from committed logs, or a drawing made by `scripts/cards.py` (Pillow).

No Claude response is shown on screen, so no reconstructed or historical chat appears in the film. The toolkit's `walker` modifier would open on a Claude composer prompt (B00 `ClaudeComposerAsk`); the author's beat order has no such beat, and a reconstructed chat would have to be labelled as one, so it was left out (BUILD-PROMPT.md, "Deviations from the toolkit").
