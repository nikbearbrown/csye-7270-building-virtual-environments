# ATTRIBUTION — Assignment 7 animation assets

Recorded by the agent from the user's statements (CHANGE-BRIEF.md "The
sheets", r2, r7). Nothing here was downloaded from a third party.

| Asset | Source | Original as delivered (committed) | Derived by (committed code) |
|---|---|---|---|
| NPC idle sheets `art/characters/npc/npc_*_idle.png` (256×64, 4 cells of 64×64) used by `animations/npc_idle.tscn` | The user's image-model output: fan art of Arknights characters generated with **gpt sol 6.1** | `art/portraits/batch_P1_v3/source_paintings/portrait_closure_chibi.png`, `art/field/batch_F1C_v1/source_paintings/squad_field_lineup.png` | `art/characters/npc/prepare_npc.py` |
| Lappland rig parts `animations/lappland_rig/{body,blade_front,blade_back}.png` | The same model's output (Lappland combat sheet) | `godot_assets/lappland_combat_source.png` | `godot_assets/prepare_combat_atlas.py` → `godot_assets/lappland_combat_64.png` (row `west`, column 10) → `tools/a7_cut_rig_parts.py` (rectangles only, pixels unchanged) |

- **Model:** gpt sol 6.1 (user, 2026-11-22). **Terms of use, date checked,
  prompt log:** not supplied by the user (they asked to record the model name
  only).
- **The user's position on rights (verbatim, translated from Chinese):**
  "ordinary fan derivative work, no violation."
- **The course rule, stated for the reviewer:** Assignment 2's rule for
  generated sprites asks for a free or local model and no copyrighted
  character. The characters are from Arknights; the user chose to use this
  art. The agent records that choice and does not judge it.
- Registration: the NPC sheets keep the feet 2 px above the cell bottom
  (`art/field_art.gd`); the rig parts sit by their pivots. The user saw no
  drift (evidence/a7/human-checks.md).
