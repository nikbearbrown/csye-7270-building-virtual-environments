# /gdd p3

Phase: Scope · Aliases: `/gdd technical` · Gate required: world
Output: `design/sections/14-technical.md`

ENGINE / TOOLCHAIN (default Godot 4, typed GDScript, 2D greybox first; pin exact
version, renderer, and target platform as decisions to confirm).
TARGET PLATFORMS: min/rec spec, platform-specific constraints.
PERFORMANCE GOALS: FPS, load time, memory, latency — non-negotiable numbers.
THIRD-PARTY MIDDLEWARE: licensing + integration complexity.
ASSET PIPELINE: L0 Greybox → L1 Proxy → L2 Alpha → L3 Beta → L4 Ship-ready, with
acceptance criteria at L4 per asset category. Reference `/asset-gen`
for generated art.
Godot contract: scene responsibilities, collision layers, input action names,
save/reset ownership, resource paths.

## Contract

- Read `persona.md`, then the project's `design/` folder (brief, sections, decisions,
  DESIGN-STATUS.json) before writing. Preserve human edits in existing files.
- Interactive: if the gate above is unsigned, ask the gate question first and stop.
  Silent (`silent` flag): proceed, and record "gate world unsigned at time of
  writing" in the output header.
- Write the output file; in chat give what changed, the assumptions made, and the
  next command. Long content never goes to chat.
- Bump `revision` in `design/DESIGN-STATUS.json` when a section changes.
