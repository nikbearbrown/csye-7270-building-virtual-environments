# PROMPTS

## B00 — the Walker ask (reconstructed, not a recorded prompt)

Rebuilt from CHANGE-BRIEF.md A3-R0 to open the film, as the walker modifier requires:

> Please use Walker to convert my game design document about Lanternfall's fog-bound night market into three simple
> Blender props: a Lantern Gate, a Supply Stack and a Lamp-oil Shrine. Build them through the Blender MCP from basic
> shapes only, one call per part, at the sizes in my CHANGE-BRIEF, then export GLBs and show all three in a Godot 3D
> room.

## The prompts that actually built the props (recorded)

The session followed the assignment's adapted prompt (read CHANGE-BRIEF, call `get_scene_info`, propose steps, wait
for approval, one `execute_blender_code` call per object with `get_scene_info` after each, apply rotation and scale,
show the result with `look`, never call `generate_3d` / `search_assets` / `import_asset`, say what could not be
verified). For each prop Claude proposed a numbered plan in the session and Bao answered before anything ran:

| Prop | Bao's answer (verbatim) | Time (EDT) |
|---|---|---|
| Lantern Gate | 批准，开始建 Gate | 2026-10-14 11:53 |
| Supply Stack | 批准，开始建 Stack · barrel: 和旧版一样 | 11:59 |
| Lamp-oil Shrine | 批准，开始建 Shrine | 12:02 |

B04 shows the Supply Stack plan verbatim with an English gloss. Every call body is in `tools/blender/build_<asset>.py`.
Each call also carried Bao's words as the MCP's `user_prompt` field.

## B19 — Your Turn (suggested to the viewer)

> Please use Walker and the Blender MCP on my Supply Stack. Before changing anything, predict what
> tests/test_a3_assets.gd will report if UpperCrate moves 0.07 m along +Y. Then move it by hand in Blender, export
> the GLB, run the test and compare.

Why it is worth running: the upper crate's edge already sits 0.01 m inside the 0.80 m footprint, so a hand edit
that looks harmless breaks the frozen depth (0.86 m > 0.80 + 0.011). It is the change an earlier draft suggested as
Bao's hand edit, which was caught before use (TEST-REPORT "What Claude got wrong").

## The requests that produced this film (Bao, verbatim)

- "做 把作业没完成的都做完" — finish what the assignment still needs.
- "根据作业要求 做到100分" — meet every requirement of the assignment.
- "你帮我录" — record the Blender session for him (CAPTURE.md: Blender's own window screenshots through the MCP,
  since the Claude app has no screen-recording permission).
- His human-check words, 2026-10-15, are quoted in B16 and TEST-REPORT.md.

No paid service, upload or publication was requested or used.
