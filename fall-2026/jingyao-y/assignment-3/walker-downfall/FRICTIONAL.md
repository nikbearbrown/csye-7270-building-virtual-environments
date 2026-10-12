# FRICTIONAL.md — what actually went wrong (A3)

Only things that actually happened are listed, with who found them. Nothing here describes the author's feelings; none were reported. No third-party viewing feedback exists, so none is recorded.

## Setup (in the previous Claude session, found by the author and Claude together)

1. **The Claude desktop app's `claude` CLI was not on PATH.**
2. **The MSIX package redirects AppData.** The app's `%APPDATA%` resolves to `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming`, not the usual `Roaming` folder.
3. **The course's MCP command failed on Claude Code 2.1.295.** `claude mcp add -e DISABLE_TELEMETRY=true blender -- …` reported `Invalid environment variable format: blender`: `-e` swallowed the next argument. It worked with the name first: `claude mcp add -s user blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender`.
4. **`uvx mcp-for-blender install-addon` reported "Could not find a Blender user addons directory".** We created `%APPDATA%\Blender Foundation\Blender\5.4\scripts\addons` by hand and set `BLENDERMCP_ADDONS_DIR`; after that the add-on installed.

## This session (2026-10-12)

5. **Blender version.** The available build was 5.4.0 Alpha; the course uses 5.1.2. Everything was done in 5.4 Alpha and nothing was re-checked in 5.1.2.
6. **The UI language did not match the instructions.** Claude's first step list used English menu names. The author's Blender is in Chinese (物体模式, 变换, …), and Claude saw this only in the author's first screenshot. Later instructions gave the Chinese names.
7. **The author did not find Scene Statistics on the first try** (author's report: "没找到场景统计"). After a second set of directions it was on in the status bar.
8. **The screenshot was not at the requested path.** The author's screenshots went to Windows' default `Pictures\Screenshots`. Claude found them by modification time and copied them into `a3/screenshots/`.
9. **The cliff's lip boulder was mostly buried** and read as a disc (TEST-REPORT loop 1). This was Claude's placement error, caught by `look`.
10. **A rubble stone floated above the pile** (loop 1b). This was Claude's placement error, caught by `look`.
11. **One of Claude's own checks printed a wrong number.** The ramp script's last line filtered with `abs(x) < 3.1` and caught the kerbs' inner vertices (x = 3.0999…), so it reported 0.27 instead of the road's 0.02. It was re-measured correctly in the next call; the script header notes it.
12. **Godot tried to import the `.blend` files (predicted F5).** The first `--headless --import` failed with `Blender path is invalid or not set … Cannot configure blender path in headless mode.` Fixed with `.gdignore` (loop 2).
13. **The preview light pointed upward (loop 3).** Claude wrote the sun's `Transform3D` by columns, but `.tscn` stores the basis by rows. The render looked like inverted normals, and Claude first checked the normals (0 inward faces) before finding the real cause.
14. **The exporter made every material double-sided,** so Godot disabled back-face culling. This was not predicted. It means a flipped face would not have disappeared in Godot.
15. **The course repository had no `assignment-3` folder** for this student. Claude created `fall-2026/jingyao-y/assignment-3/walker-downfall/`; the `walker-` prefix was the author's choice.
16. **The HUMAN CHECK report was a single line,** "都是对的" ("everything is correct"). It is recorded as given, without detail.

## GitHub pushes

| Date | Repository / branch | Commit | What | Pushed? |
|---|---|---|---|---|
| 2026-10-12 | `nikbearbrown/csye-7270-building-virtual-environments` / `Jingyao_Y` | `ff43a88` | CHANGE-BRIEF.md (as approved) | Not yet; waiting for the author |
