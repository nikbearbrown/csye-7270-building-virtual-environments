# SOURCES — Assignment 7

Earlier assets and their sources are in `walker-magic-zhefan/SOURCES.md` (Assignments 2–3) and my Assignment 5 and 6 `SOURCES.md` files, unchanged.

## Starting point

`walker-magic-zhefan` copied unchanged from my Assignment 6 submission, `zhefan-z/assignment-6` at `7672d5a` (tree ID checked, `027a0ab`).

## New in this assignment

| What | Source | Terms |
|---|---|---|
| `assets/sprites/mage/mage_run_cycle_sheet.png` (run cycle, 4 frames) | generated in the Gemini app (free access through my Google account; model shown as "4 Hydrogen", 2026-11-12) from prompt v3 with my A2 contact sprite as the only reference; raw output unchanged in `design/a7/mage_run_cycle_gemini_raw.jpg`; cleaned by `tools/clean_run_cycle.py` onto my A2 palette; credits in `assets/sprites/mage/ATTRIBUTION.md` | Google Terms of Service and Generative AI Additional Terms of Service; under Assignment 2's rules for generated sprites (no named living artist, brand or copyrighted character); prompts in `design/IMAGE-PROMPTS-from-chat.md` (v1–v3; v1 and v2 rejected) |
| `assets/sprites/mage/mage_run_sheet.png` (r0 sheet) | packed by `tools/pack_run_sheet.gd` from my A2 `mage_run_contact.png` and `mage_run_passing.png` | my own A2 sprites |
| Wolf rig parts | `region_rect` on my A2 `wolf_lunge.png`, unchanged | my own A2 sprite |
| Motion reference | Eadweard Muybridge, *Animal Locomotion* (1887), plate 707 (dog galloping) and plate 60 (man running), from Wikimedia Commons, downloaded unchanged; SHA-1 matches Commons; `design/a7/reference/SOURCES.md` | public domain |
| Cave lights, embers | Godot nodes configured in scene files; embers reuse my A6 `spark.png` (code-generated) | — |

## Tools and models

- **Godot Engine 4.7.2-stable** (`ed1daf0bf`), Forward+.
- **Claude Code** desktop app, model **Opus 5.5**, through my Northeastern Claude Enterprise seat, manual permissions. Prompts: `prompt-1.txt` to `prompt-5.txt` and the messages recorded in `FRICTIONAL.md`. It made the commits I asked for, each labelled with who wrote the content.
- **claude.ai** (chat, Opus 5.5): planning, commands, the brief and the Gemini prompts, these documents.
- **Gemini app** ("4 Hydrogen"): the run-cycle images.

## Collaborators

None. Individual assignment.
