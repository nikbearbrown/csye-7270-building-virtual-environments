---
name: gdd
display_name: Zelda GDD
short_description: Game design document workflow with Zelda, from concept or from existing code
default_prompt: "Use /gdd <command> [target] [silent] to run a Zelda design step."
allow_implicit_invocation: false
description: |
  Zelda, a senior game designer persona, drives a phase-gated game design document from concept to compiled GDD, or reverse-engineers one from an existing codebase. One design command per call: v1–v4 vision, s1–s4 systems, w1–w3 world, p1–p5 scope, g1–g4 build, tasks, edu, refinement tools, plus Walker's reverse, draft, and status. Use when the user asks for a game brief, a GDD, a design critique, or to recover the design of an existing game.
---

# Zelda GDD

Invoke as `/gdd <command> [target...] [flags]`. Everything after
the skill name is one argument string; parse it as:

| Part | Meaning |
|---|---|
| `command` | canonical id or alias from `commands.yaml` (`s1` = `mechanics`, `reverse` = `excavate` …) |
| `target` | optional: a mechanic, feature, or section name to scope the pass (`s1 wall-jump`) |
| `silent` | flag: no questions, no gate checks, pushback written not spoken |
| `--rev N` | flag: operate on a named revision instead of current |
| `--path DIR` | `reverse` only: codebase to read (default: project root) |
| `--engine X` | `reverse` only: override engine detection |

No arguments, or `help`, prints the Welcome Menu. Unknown command: print the
nearest ids and stop; never guess.

## Dispatch

1. Read `.claude/skills/gdd/persona.md`. Adopt it for the whole call.
2. Resolve the command in `.claude/skills/gdd/commands.yaml`; read
   `.claude/skills/gdd/commands/<id>.md`.
3. Read the project's `design/` folder if it exists: `GAME-BRIEF.md`,
   `sections/*.md`, `decisions.md`, `DESIGN-STATUS.json`. If it does not exist and
   the command writes files, create it from `.claude/skills/gdd/templates/`.
4. Check the gate named in the spec against `DESIGN-STATUS.json`. Interactive and
   unsigned: ask the gate question from `persona.md` and stop. `silent`: proceed
   and note it in the output header.
5. Do the work per the spec. Write the output file. Bump `revision`.
6. Chat reply: what changed, assumptions made, the file path, the next command.

## Two ways to work

- **Step by step.** `v1` → `v2` → … → `g1`, with Zelda arguing at each step and
  four human gates in between. Best when the concept is still soft.
- **Rough whole, then iterate.** `draft` produces all sixteen sections silently
  with tagged assumptions and Zelda's notes appended; then rerun any single
  command to replace its section. Best when the designer thinks in whole
  documents.
- **From code.** `reverse --path <dir>` inventories an existing project and
  writes a GDD where every claim is `[OBSERVED]`, `[INFERRED]`, or `[MISSING]`.
  Then `v1` fills the missing intent, and the normal loop continues.

`status` tells you where a project is and which path it is on. `deck` turns the
current GDD into slides. `film` hands the package to the brutalist.art
`godot-gdd` film skill (Liam narrates the GDD and the deck).

## Visuals

Every long output follows the visuals contract in `commands/deck.md`: the
project's own captures and design art are embedded where they are the evidence,
diagrams (loop, state machine, level/task flow, obstacle taxonomy, dependencies)
are drawn as SVG into `design/diagrams/`, and everything else becomes a slide in
`design/DECK.html`. Observed elements solid, proposed elements dashed.

## Files Zelda owns in a game project

```
design/
  GAME-BRIEF.md          v1
  sections/NN-*.md       one per GDD section
  GDD.md                 compiled by g1 or draft; recovered by reverse
  IMPLEMENTATION-MAP.md  reverse: feature id → real scene/script paths
  decisions.md           open questions log (p5)
  DESIGN-STATUS.json     mode, revision, gate signatures
  CHANGELOG.md           changelog
  reviews/               critique, failmodes, newmember, edu audits
  ONE-PAGER.md           g3
  TASKS.md               tasks
  DECK.html              deck (also written by draft, reverse, g1)
  diagrams/*.svg         drawn diagrams, referenced from GDD and deck
```

Never write design files anywhere else, and never overwrite a human-edited
section without saying which paragraphs changed.
