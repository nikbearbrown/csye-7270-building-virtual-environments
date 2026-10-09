# FRICTIONAL — Assignment 3

## 2026-10-09 — Copying the Assignment 2 project into assignment-3

**What happened**
- The project `walker-magic-zhefan` was copied into `walker-magic-zhefan/` here from branch `zhefan-z/assignment-2` at `946f1f1`, using `git archive` written to a temporary tar file outside the repository and then extracted with `tar -xf` (commit `249647b`). The copy was checked before committing: 227 files and 30,015,318 bytes, the same as the tracked project on that branch; nothing over 25 MB; no `.godot/`, caches, media or Blender backups; and `git write-tree` for the new folder gave tree ID `aab78206197db6c0b3149b95d313ff1cc84d0d40`, the same as the Assignment 2 folder, so the copy is byte-for-byte identical.
- The Assignment 2 submission docs (`README.md`, `SUBMISSION.md`, `TODO.md`, `HANDOFF.md`, `FRICTIONAL.md`, `TEST-REPORT.md`, `CHANGE-BRIEF.md` and `youtube/`) were moved into `walker-magic-zhefan/docs/a2/` with `git mv`. Every move is an exact rename (content unchanged), and the `youtube/` tree ID is the same before and after. Also added: `docs/.gdignore`, so Godot skips `docs/`; a dated block in the project `.gitignore` for the moved film folders; and `docs/README.md`, a note explaining the copies.
- Nothing on branch `zhefan-z/assignment-2` or under `fall-2026/zhefan-z/assignment-2/` was changed; that branch still points to `946f1f1` locally and on origin.

**Claude Code's mistake**
- Claude Code wrote the new note to `docs/a2/README.md` and so overwrote the Assignment 2 README it had just moved to that same path, because it did not check the target path first. It found this before committing, restored the original from git (blob `fc1c4fe`) and confirmed the staged file matched that blob, so nothing was lost. The note went to `docs/README.md` instead.

**My own decisions**
- Create the assignment-3 folder ourselves, because the instructor's folder was not present.
- Keep the Assignment 2 branch, PR and folder read-only.
- My standing rule that committed docs only get dated additions, never rewrites.

**Suggested by Claude (claude.ai chat), approved by me**
- Keep `ASSIGNMENT-3.txt` and my untracked Assignment 2 film working files out of git through `.git/info/exclude`.
- Copy the project with `git archive` into the new path only, instead of `git checkout zhefan-z/assignment-2 -- <path>`, which would have duplicated the Assignment 2 files in this PR.
- Write the archive to a temporary file instead of piping it into `tar`, because a PowerShell pipeline can corrupt binary data.
- Sort the docs into game docs that stay and Assignment 2 submission docs that move to `docs/a2/`.
- Applying my rule here: leave the stale mentions in `CONCEPT.md` and `SOURCES.md` unedited.

**Proposed by Claude Code, approved by me**
- Place the note at `docs/README.md` and keep its line about `design/…` paths (Claude Code's proposal; Claude in my claude.ai chat recommended accepting it).
- Copy everything exactly; put `CHANGE-BRIEF.md` with the moved docs; add `docs/.gdignore`, the `.gitignore` entries and the note. The per-file sorting of the two groups was also Claude Code's proposal.

**Claude Code's work**
- Ran the git commands and every check listed above.
- Searched the project for references to the moved paths and reported what would break. The Assignment 2 reel scripts find the project by their own position (`scripts/common.py`), so they would look in the wrong folder after the move (left unchanged, not meant to run). The project `.gitignore` film entries only matched a top-level `youtube/` (fixed with the dated block). The `../FRICTIONAL.md` link in the old stub no longer reaches the Assignment 2 log (explained in the note). It also found that `youtube/.gdignore` moves with the folder, so Godot still ignores it.
- Proposed `CHANGE-BRIEF.md` for the moved group, and drafted the note's wording, including the line about `design/…` paths.
