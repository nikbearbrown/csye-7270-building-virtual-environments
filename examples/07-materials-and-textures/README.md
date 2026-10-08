# Example 07 — Materials and textures: auditing the Dutch ship and giving the hull its AO

## Executive summary

**What this is.** The worked record behind Chapter 7:

- a Claude Code audit of the Poly Haven ship's three materials, nine textures and attribution in `walker-3d-graphics-settings`;
- a Claude Code change session that the account's session limit cut off;
- a Codex session that finished the same change;
- our human review and verification after each step.

**Why it exists.** The chapter's claims about what the agents found, got wrong and fixed must trace to real runs.

**What was found.**

- **The audit.** It correctly found that no material uses the AO in the ARM textures and that the sails' alpha scissor cannot work with a JPEG. It also named the wrong tonemapper, misdescribed what a Lossless "normal map" import stores, invented video-memory figures, and proposed a "fix" for dead code that would have mislabelled a menu.
- **The change.** Claude's partial change used a `_subresources` key that the importer ignores. Codex wired the external `ORMMaterial3D` correctly, but left `ao_enabled` off, so the AO that was the whole point stayed off, while its test passed 100 checks.
- **The fix.** One line (`ao_enabled = true`) and one assertion, checked from an empty import cache and by mutation.

No window was opened, so nothing here shows what the ship looks like.

## Contents

| Path | What it is |
|---|---|
| `prompts/` | `prompt-1-audit.txt`, `prompt-2-ao.txt` (given to Claude Code), `prompt-2b-ao-codex.txt` (the same task with a handoff paragraph, given to Codex) |
| `PROMPTS.md` | Prompts and command lines, with each session's outcome |
| `changes.diff` | `git diff` from the baseline (`31f00c4`) to the final state (`bf86ae3`) |
| `git-log.txt` | The scratch repository's commits, each labelled with who made it |
| `files/MATERIALS.agent-draft.md` / `MATERIALS.reviewed.md` | The audit as the agent wrote it, and after human review |
| `files/dutch_ship_medium_hull.claude-partial.tres`, `claude-partial-gltf-import.diff` | Claude's interrupted change |
| `files/dutch_ship_medium_hull.final.tres`, `final-gltf-import.diff` | The final material and import wiring |
| `tests/test_materials.session1.gd`, `tests/test_materials.final.gd` | The agent's first test, and the final one (Codex's version plus one human-added assertion) |
| `tests/test_settings.gd` | The Walker harness from `walker-3d-graphics-settings` (17 checks), needed when starting from the upstream demo |
| `probes/` | Headless probe scripts used to check the agents' claims (`probe_hull.gd`, `probe_pixels.gd`, `probe_alpha.gd`, `probe_enums.gd`, `probe_material.gd`) |
| `logs/` | Baseline, audit, mutation, partial, Codex and human-fix logs; probe outputs (ANSI codes stripped) |
| `transcripts/` | Claude Code sessions 1 and 2 (`stream-json`; the init event's lists of installed plugins, skills and commands replaced with counts) and the Codex session (`--json` events plus its final message) |

## Starting point

- `walker-3d-graphics-settings/godot`: identical to upstream `godot-demo-projects` `3d/graphics_settings` at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, except `config/name` and the added `test_settings.gd`. This was checked with a recursive diff against the local checkout of that commit.
- Students start from upstream; see Chapter 7, *Build It*.
- Godot generated `test_settings.gd.uid` on the first test run. It was committed separately (`e8d1e72`).

## Results (from `logs/`)

| Step | Check | Result |
|---|---|---|
| Baseline | import / `test_settings.gd` @60 | exit 0, no warnings / 17 checks, 0 failures |
| Audit (Claude) | `test_materials.gd` (95 checks) | 95 PASS; mutation (hull normal `compress/normal_map` 1→0) gives 1 FAIL |
| Change (Claude, cut off) | its own updated test | 4 FAIL: hull still the internal `StandardMaterial3D` (flat `_subresources` key ignored) |
| Change (Codex) | `test_materials.gd` | 100 PASS, but probe shows `ao_enabled=false` on the hull `ORMMaterial3D` |
| Human fix | clean reimport (`.godot` deleted) + `test_materials.gd` / `test_settings.gd` | 101 PASS / 17 PASS; probe: hull `ORMMaterial3D`, `ao_enabled=true`; rigging and sails unchanged; no texture `.import` changed |
| Mutation | `ao_enabled = false` | 1 FAIL (`hull ao_enabled = true …`) |

## Facts established from Godot 4.7.2 source

Used to check the agents; the source is at commit `ed1daf0bf`.

- `scene/resources/material.cpp`: the ORM path emits `AO = orm_tex.r` only when the AO feature is on, and sets `ROUGHNESS = orm_tex.g` and `METALLIC = orm_tex.b` without the scalars. `StandardMaterial3D` multiplies the texture by the scalar.
- `editor/import/3d/resource_importer_scene.cpp`: per-material settings are read from `_subresources["materials"][<name>]`.
- `editor/import/resource_importer_texture.cpp`: the enum values used in the chapter's table; detection is driven by renderer callbacks.
- `core/io/resource_uid.cpp`: the UID alphabet is `a`–`y` and `0`–`8`, and the decoder is lenient.

## Human checks not performed

These are the student's checks, listed in Chapter 7, *Use It*:

- AO on/off screenshots of the hull with SSAO off;
- the hull otherwise unchanged;
- the sail edges;
- `git diff` of `.import` files after the first editor session.

## Incident

The Claude Code account reached its session limit during the change session (`You've hit your session limit · resets 6:40pm (America/New_York)`); other agents were sharing the account. The unfinished work was committed unedited (`791a0e8`), and Codex was given the same task with a handoff paragraph.
