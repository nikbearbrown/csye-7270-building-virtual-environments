# CLAUDE.md — nik-bear-brown/ (Professor Bear's example folder)

This folder is the instructor's public example work for CSYE 7270, Fall 2026. It keeps the same process record students keep. **Each assignment lives in its own subfolder (`assignment-1/`, `assignment-2/`, …) with its own `FRICTIONAL.md`.** Every substantive change is logged in the log of the assignment it belongs to, and every push adds a line to that log. The top-level `FRICTIONAL.md` is only for changes to the folder itself (setup, layout, rules). The repo-root `AGENTS.md` still governs everything else.

## Rule 1 — log every substantive change in the right FRICTIONAL.md

Before you report a task in this folder as done, update the matching log in the same change set: `assignment-N/FRICTIONAL.md` for work on that assignment, the top-level `FRICTIONAL.md` for changes to the folder itself. Create an assignment's subfolder and its log when work on that assignment starts, not before; no empty placeholder folders.

**Substantive** means a new or deleted file or folder, a change to what a result says, a bug found or fixed, or a decision, a reversal, or something that went wrong. Typo and formatting fixes that don't change meaning are not substantive.

**How to log it:** a new day or new piece of work gets a new entry under `## Entries`, newest last, headed `### YYYY-MM-DD — <what it was>`, with the course's seven fields in order:

- Date and what I was working on
- I tried / expected
- What happened
- What I did
- What Claude or another person contributed
- What I understand now / still do not understand
- Evidence and next step

Write what happened, not what was hoped. Never invent a prediction, a result, an approval, or an understanding the human didn't state. Say what Claude Code did and what Professor Bear decided.

## Rule 2 — one line per GitHub push

Every push adds a row to the `## GitHub pushes` table of each log it touches (the assignment's log, or the top-level log for folder changes), in the same commit being pushed:

```
| YYYY-MM-DD | <commit subject, exactly as committed> |
```

No commit ID in the row: a commit can't contain its own ID.

## Pushing from this folder

- **Standing approval (granted by Professor Bear, 2026-09-25):** after any substantive change to this folder, commit and push it to `main` without asking again, once the log is updated. This covers **only** `fall-2026/nik-bear-brown/` (and `fall-2026/README.md` when its roster changes). Anything else in this repo, or any other repo, still needs his word for each push.
- Stage **only** `fall-2026/nik-bear-brown/` (and `fall-2026/README.md` when its roster changes). The repo often has other uncommitted instructor edits; never sweep them in.
- Git on this machine is already authenticated. Never ask for, accept, or write down a GitHub token.

## Privacy

This repo is public. The person here is "Professor Bear." No contact details, other people's names, or absolute local paths (`/Users/…`) in anything committed. JSON files are indented (2 spaces), never minified.
