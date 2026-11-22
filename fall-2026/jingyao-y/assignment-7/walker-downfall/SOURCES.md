# SOURCES.md — Assignment 7

The A6 version of this file is at tag `a6`. This file replaces it.

## Starting point

Downfall, the game chosen in Assignment 2 (no change of game since), copied
from the game repository at `22651e36` into this folder (`3dc59cd2`). The A5
cargo textures (Poly Haven "Rusty Metal Sheet", CC0, credited at tag `a5`)
stay only because `test_materials` loads them.

## Sprite art used by the A7 clips

Both clips use the game's own Sol art; the full record is
`animations/ATTRIBUTION.md` (and CHANGE-BRIEF.md "The sheets", r2, r7).

- **Model:** gpt sol 6.1 (as the user stated it). Fan art of Arknights
  characters. **Terms of use, date checked and prompt log:** not supplied by
  the user, who asked to record the model name only.
- **Originals as delivered (committed):**
  `art/portraits/batch_P1_v3/source_paintings/portrait_closure_chibi.png`,
  `art/field/batch_F1C_v1/source_paintings/squad_field_lineup.png`,
  `godot_assets/lappland_combat_source.png`.
- **Sheets written by code (committed with the code):**
  `art/characters/npc/prepare_npc.py` (the NPC idle sheets),
  `godot_assets/prepare_combat_atlas.py` (the combat atlas),
  `tools/a7_cut_rig_parts.py` (the three rig parts, rectangles only, pixels
  unchanged).
- The course rule for generated sprites (a free or local model, no
  copyrighted character) and the user's choice are stated in
  ATTRIBUTION.md; the agent records them without judging.

## Code and documentation consulted

- The course chapter's read-back snippets (`track_problems`, the tolerance,
  `step`, loop-mode and update-mode checks), used as given in
  `tests/a7_readback.gd` and the read-back tests.
- The A6 suite `tests/test_hit_spark_state.gd` for the headless input path
  (`root.push_input`).
- Godot 4.7.2 itself (`tests/a7_probe_headless.gd`) for every class,
  property and constant name; Godot documentation for AnimationPlayer,
  Animation, SubViewport and Movie Maker.

## Assistance and contributions

- **Agent (Claude Code, Claude Opus 5.5):** CHANGE-BRIEF.md and revisions
  r1–r6 (r7 records the user's provenance), the phase table, cycle spec and
  predictions, the pins, the probe, every review, the previews, the
  mutation runner, TUNING.md (its strip readings, labelled as claims),
  TEST-REPORT.md, FRICTIONAL.md, this file, ATTRIBUTION.md, the README and
  every commit.
- **Delegated agent sessions** (`prompts/`, `sessions/`): the CLAUDE.md
  draft; the `npc_idle` scene and read-back; the rig scene, cut script and
  read-back; the Step 5 plan, the NPC wiring, the rig attach, the wave state
  machine, the structure test, the edge tests and the re-pin.
- **The user:** chose the location, the art source, the rig route and the
  attack-speed rule; approved or declined every brief revision and plan
  step; watched every preview and gave every verdict (human-checks.md,
  TUNING.md); ran the Movie Maker capture; kept r0 without a revision.
- No collaborators. No paid media generation.
