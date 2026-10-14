# FRICTIONAL — Assignment 3

## Entries

<!-- One entry per work session, newest last. Copy the block below. -->

### YYYY-MM-DD — <what I was working on>

- **Date and what I was working on:**
- **I tried / expected:**
- **What happened:**
- **What I did:**
- **What Claude or another person contributed:**
- **What I understand now / still do not understand:**
- **Evidence and next step:**

### 2026-10-08 — reading the assignment and choosing the three assets

- **Date and what I was working on:** 2026-10-08. I read Assignment 3 and chose what to build.
- **I tried / expected:** My professor suggested giving the assignment to Claude to see what it returns. I first asked Claude in chat; it said it needed my game, three assets, and a size reference.
- **What happened:**
  - In Claude Code, Claude found my Assignment 2 game in the repo (Extinguisho, a 2D game), so I did not have to describe it again.
  - Claude checked my Mac: Godot is installed, **Blender is not**.
  - Claude suggested four asset options from my game; it also found that the rescue bag already exists in my game, drawn in code (`player.gd`), 9 px wide next to a 64 px character.
- **What I did:**
  - Chose the first three: **fire hydrant, rescue bag, rooftop ledge**.
  - Told Claude to only edit files under `fall-2026/sreeja-p/`.
- **What Claude or another person contributed:** Claude suggested the asset options and their basic shapes, worked out the bag's pixel size from the code, and set up this folder and the CHANGE-BRIEF skeleton. The size scale and all predictions are left for me.
- **What I understand now / still do not understand:** Because my game is 2D, I still need a small 3D scene (floor, one light, camera). I still need to choose a pixel-to-metre scale.
- **Evidence and next step:** Install Blender, write BLENDER-NOTES.md, then fill in CHANGE-BRIEF.md before building.

### 2026-10-14 — learning the Blender window

- **Date and what I was working on:** 2026-10-14, 9:30–9:55. My "learn the window" session in Blender 5.2.2, before any prompting.
- **I tried / expected:** Orbit, pan, zoom, the axis gizmo, selecting in the Outliner, the Move tool, the sidebar (N), and Object vs Edit Mode.
- **What happened:**
  - Spotlight couldn't find Blender (it is installed in Applications), so Claude opened it.
  - Clicking Z on the gizmo gave the top view, so Z is up.
  - I grabbed the Move tool's white circle instead of the red arrow, and the cube went below the floor (Location Z -2.39). I found the axis lock myself; G then Z moves only up/down. Option+G put the cube back at 0.
  - I couldn't find "Confirm/Cancel": they are hints in the status bar, not buttons.
  - Sidebar: the default cube is 2 m on each side (Dimensions), even though Scale is 1.
  - In Edit Mode a corner was at Z = -1 m, so the default cube's origin is in its middle.
- **What I did:** Took my own screenshots (`walker-ninja-firefighter-joe-3d/evidence/blender-session.png`, `blender-edit-mode.png`).
- **What Claude or another person contributed:** I did the Blender session and answered the questions; Claude Code guided the steps and helped write the notes up from my answers and screenshots.
- **What I understand now / still do not understand:** Blender is Z-up and Godot is Y-up; a new object's origin is in its middle, so it sinks halfway into the floor unless the origin goes to the base.
- **Evidence and next step:** BLENDER-NOTES.md; next, my CHANGE-BRIEF before building.

## MCP connection attempts

<!-- Log every attempt and every error, verbatim. If it is not connected after ~2 hours of honest effort, switch to the script route and say so here. -->

| Date / time | Step tried | Exact error or result | What I changed next |
|---|---|---|---|

## GitHub pushes

| Date | Commit subject |
|---|---|
| 2026-10-14 | A3: log the push of my brief and Blender notes before building |
