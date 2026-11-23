# PROMPTS — what was asked, and of whom

Written by Claude Code, 2026-11-22.

| # | Prompt | Who wrote it | Given to | Result |
|---|---|---|---|---|
| 1 | `prompt-1-pitch.txt` (in this folder): branch, brief commit, fact check, art renaming, the film's beat order, its labels and rules, the records | the author | Claude Code (Claude Opus 5.5), one session | this film and its records |
| 2 | One question from Claude Code: two files in `art/` were the same 2×2 expression sheet (a green 2048×2048 one and a transparent 1199×1312 cut-out); which becomes `witch_expressions.png`? | Claude Code | the author | "Green → expressions; drop cut-out": the cut-out stays untracked and is not in the film |
| 3 | The Gemini image prompts | the author, with claude.ai drafting some | Gemini 4 in the Gemini app | the concept art; recorded word for word in `ART-PROMPTS.md` |

No other model was prompted for this film: no paid generation, no API key, no upload. The narration is Kokoro `am_onyx` run locally by the toolkit (`generate_audio_kokoro.py --speed 1.05`), reading the script in `scripts/sheet.py`. Every picture is a real capture, the author's concept art, a figure from committed logs, or a drawing made by `scripts/cards.py` (Pillow).

No Claude response is shown on screen, so no reconstructed or historical chat appears in the film. The toolkit's `walker` modifier would open on a Claude composer prompt (B00 `ClaudeComposerAsk`); the author's beat order has no such beat, and a reconstructed chat would have to be labelled as one, so it was left out (BUILD-PROMPT.md, "Deviations from the toolkit").

## Added 2026-11-22 — the rebuild from the GDD

| # | Prompt | Who wrote it | Given to | Result |
|---|---|---|---|---|
| 4 | `prompt-2-gdd.txt` (in this folder): check GDD.md and the revised brief, commit them, rebuild the film in the updated spec's order, update the records | the author | Claude Code (Claude Opus 5.5), same session | Step 1 stopped at a wrong Built claim (next row) |
| 5 | Claude Code's report: GDD §4's Jump row said "only from the ground", but 840b501 allows a 0.08 s coyote time and a 0.10 s jump buffer; three smaller wording points (staff "orb" vs the character sheet's "red crystal", incomplete key lists, the heal key "A key") and the unverified Assignment 4 GDD | Claude Code | the author | the author fixed GDD.md: coyote time, buffer and no double jump; arrows, W and Up; heal key "still to be chosen"; red crystal; 5 hearts with tint, blink and 1.0 s invulnerability; the A4 GDD cited as a Canvas PDF of 2026-10-15 |
| 6 | The author's note that the A4 PDF was copied to `pitch/A4-GDD.pdf`; the file was not there | the author | Claude Code | Claude Code found two byte-identical copies in the author's Downloads (`The-Little-Flame-Witch-GDD.pdf`, file date 2026-10-15 17:09, PDF title "The Little Flame Witch — Game Design Document", created 2026-10-15 21:09 UTC, SHA-256 `c7b4f5fd…a769a9f`) and copied the 2026-10-15 one to `pitch/A4-GDD.pdf` unchanged; its text could not be extracted here (no PDF tool installed), so its contents were not read |

As in the first cut, no Claude response is shown on screen and no other model was prompted: the narration is Kokoro `am_onyx` run locally at `--speed 1.05`; the music and effects in G11 are the game's own Assignment 2 files.
