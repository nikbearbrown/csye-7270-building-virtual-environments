# FRICTIONAL.md — Downfall (Assignment 2, retrospective)

> **All entries are reconstructed on 2026-10-07 from existing files.**
>
> Sources:
> - file timestamps;
> - C2PA metadata;
> - prompt, brief and revision docs;
> - Claude's session memory notes.
>
> They are not a diary kept at the time. The "Decided" lines quote recorded user
> decisions only. Where nothing was recorded, the line says so. The author should add
> their own reasoning; it has not been invented here.

**Contribution key, applying to all entries:**

| Who | Did what |
|---|---|
| **gpt-image** (via Codex `image_gen`, "Sol") | Produced every raw image. |
| **Claude Code** | Wrote briefs, revision notes, processing scripts, game code and tests. Reviewed batches with pixel statistics. |
| **The author** | Relayed briefs to Sol, chose what to accept or reject, and set the design rules. |

## 2026-09-22 — Lappland walk sheet

- **Wanted:** a chibi pixel Lappland walking in 8 directions.
- **Asked:** gpt-image; **the prompt was not saved.** Concepts `lappland_chibi_pixel*.png` came first.
- **Got:** a 1774×887 sheet (C2PA 20:14Z). The SE row faced the wrong way.
- **Decided:** accepted the sheet; SE is mirrored from SW at runtime. No reason was recorded for picking this one over the 5 chibi concepts.
- **Unresolved:** no reproducible prompt. → asset log row CHAR-WALK

## 2026-09-24 — Master GDD written

- `策划案_v1_0.md` already existed in `../evidence/downfall-before-v1-20260924-235931.zip`.
- **Design followed the first generation, rather than preceding it.**

## 2026-09-25 — First field art with PRTS references

- **Asked:** `art/field/prompts.md`. A 3×3 grid of 512 px cells; PRTS avatars and map previews as references; Lappland as style reference.
- **Got:** `enemies_v1`, `props_v1`, `ground_v1`.
- **Decided:** props_v1 became the style anchor for everything later. The enemies were replaced by the 8-direction boards. → ENEMY-V1, ENV-PROPS-V1

## 2026-09-29 — Backgrounds v1 → scene v2

- **Wanted:** regions that read as different places while keeping the red warnings readable.
- **Got:** seamless background v1 (`background_prompts_v1.md`).
- **Decided:** replaced it the same day by low-contrast surfaces plus prop groups (`场景美术重构_v2.md`). Before/after captures: `design/evidence/background-{before,after}-*.png`. → ENV-BG-V1 (rejected), ENV-SURF-*

## 2026-09-29/30 — Lappland combat atlas

- **Asked:** the prompt in `godot_assets/拉普兰德战斗素材.md`, with the walk sheet as the reference image.
- **Got:** the combat source sheet.
- **Decided:** the first uniform-grid slice was rejected because it shrank the sprite 80% and clipped the swords. It was replaced by per-cell foot-line alignment (`prepare_combat_atlas.py`).
- **Unresolved:** SW ≈ S row; N frames too similar. → CHAR-COMBAT

## 2026-09-30 — Enemy attack poses

- **Decided (user):** deleted the variant with an engine-drawn floating weapon because it "看起来像蓄力条" (looked like a charge bar). **No thumbnail survives.**
- The first 8-direction board prompt was rejected for duplicate directions. → ENEMY-ATK, ENEMY-DIR

## 2026-09-30 → 10-02 — Rhodes base

- Batch1 source v1 was rejected.
- **Decided (user):** approved drawing the walls and doors directly on the pixel grid after the model failed the geometry (`art/rhodes/batch1_v4/README.md`).
- **Recorded preferences** (Claude memory notes):
  - "罗德岛标志最重要" (the Rhodes logo matters most);
  - objects must face the camera head-on.
- H3 v1 was returned because its icons were code-drawn. → ENV-RHODES

## 2026-10-0x — Equipment icons E1–E4

- v1 was rejected because it was drawn by code, not painted (`E_revision_brief_v2.md`).
- The following rounds were judged on:
  - speckle;
  - camouflage blotches;
  - misuse of the originium-orange ramp;
  - glyph-like shapes.
- **Decided (user):** for raw originium, picked the "mode" reduction over the box reduction (`raw_originium_downscale_tests.png`). → ITEM-E1..E4

## 2026-10-07 — Relic icons R1–R4

- **Claude flagged:** 43% isolated pixels and off-palette colours in R1.
- **Decided (user):** "挺好的" ("it's fine"). R1 was accepted, and that pipeline became the standard for R2–R4. → RELIC-R1..R4

## 2026-10-07 — Assignment 2 decision

- Claude pointed out four problems with submitting Downfall:
  - it uses the Arknights IP;
  - the design came after generation;
  - it has no generated audio;
  - it has no music.
- **Decided (user):** submit Downfall as it is, and summarize the existing work rather than build anything new.
- **Unresolved:** every gap listed in [TEST-REPORT.md](downfall-godot/TEST-REPORT.md) §limitations.


## 2026-10-07 (live, not reconstructed) — fresh clone and the film

- **Wanted:** prove the slice runs from a fresh copy of the commit, then record the Brutalist film from that copy.
- **Did:** cloned the repo into an empty folder and ran `run_all.ps1 -Visual`.
- **Got: two real defects.**
  1. Every suite writes to `../evidence`, which a clone does not have, so the first suite crashed. Fixed in `f770e26`; `run_all.ps1` now creates the folder.
  2. A trial film capture of a camp start was silent: no music, no sting. Claude's first hypothesis (the camp screen pauses the scene tree) was wrong; there is no tree pause. A debug print showed no music streams loaded. The cause was Claude's own `.gitignore` rule `music/`, which also excluded `audio/music/`. Fixed in `111bf6e`.
- **Decided (author):**
  - keep the existing GodotGame repository, not a new `walker-` one;
  - generate no new assets for this submission;
  - make the film.
- **Decided (Claude, film staging, disclosed in the film):**
  - the death and extraction clips start from a camp unlocked in memory, which stands in for walking 10 or 30 floors;
  - the death happens on floor 31 because on floor 1 Lappland out-heals the damage and never dies.
- **Human / Claude / model:**
  - Claude wrote the capture choreography, found and fixed both defects, and wrote this entry;
  - no model generated anything new;
  - the author chose the scope.
- **Still unresolved:** the human playtest with sound on and muted has not been recorded.



## 2026-10-07 (live) — human playtest

- **Wanted:** check, by playing, that the slice works and stays readable with sound on and with sound muted.
- **Did:** the author played the game with normal controls, once with sound on and once muted.
- **Got:** it passed both times, by the author's own report.
- **Human / Claude / model:**
  - the author played and judged the result;
  - Claude only recorded the report.

---

## GitHub pushes

| Date | Commit note |
|---|---|
| 2026-10-07 | `coldfish432/GodotGame` `main` → `100dce3`: game code and assets only (game-only rebuild of the history whose film revision is `111bf6e`; game files identical). |
| 2026-10-07 | This branch (`Jingyao_Y`): assignment documents, design images, generated audio and film sources for Assignment 2. |
| 2026-10-07 | Added the Godot project (code and used assets) to this branch, then the film link https://youtu.be/n6yPUyUQEaM. |
| 2026-10-07 | Recorded the author's playtest (sound on and muted: passed). |
