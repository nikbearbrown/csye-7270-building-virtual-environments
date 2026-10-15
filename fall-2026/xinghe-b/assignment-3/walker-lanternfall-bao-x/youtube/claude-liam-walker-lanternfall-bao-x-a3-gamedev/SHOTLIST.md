# SHOTLIST

Film `claude-liam-walker-lanternfall-bao-x-a3-gamedev` · "Lanternfall in 3D, Taken Apart" · game source revision c0dba4c. Times are seconds into each beat, or the narration phrase a reveal is timed to. Sources: CAPTURE.md (takes and Blender stills), FACTCHECK.md (claims).

## B00 · ASK · 15.62 s · ClaudeComposerAsk

COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's CHANGE-BRIEF A3-R0 (not a recorded prompt). Liam introduces himself.

- `0.02` — composer card on cream; greeting 'Hej, Liam'
- `0.25` — the reconstructed Walker prompt types in
- `0.62` — send arms; running line names the brief and the first two MCP calls
- `0.75` — three result lines: props and calls, source revision, checks and Bao's part

## B01 · BLUF · 14.42 s · BrutalistHesitantWriter

EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('an AI generated the 3D models') is corrected to what the film shows ('Claude scripted them from primitives').

- `0.0` — cream page; 'AI generated the props' types
- `0.3` — 'generated' struck in terracotta, 'scripted' typed in
- `0.6` — 'from basic shapes' and 'Bao judges the look' type in

## B02 · BRIEF · 21.18 s · media/B02.mp4 (tools/build_media.py)

Film item: the game, the three assets and why the game needs each. Values verbatim from CHANGE-BRIEF.md A3-R0; images are the MCP look renders of the finished props (evidence/a3/mcp/).

- `0.0` — CHANGE-BRIEF A3-R0 header: three props, frozen before the rebuild (commit 8a8c778)
- `Lantern Gate` — column 1: Lantern Gate · 1.20 × 0.80 × 2.85 m · 6 shapes · ≤ 160 triangles · MCP look image
- `Supply Stack` — column 2: Supply Stack · 1.20 × 0.80 × 1.10 m · 3 shapes · ≤ 180
- `Lamp-oil` — column 3: Lamp-oil Shrine · 0.80 × 0.80 × 1.45 m · 3 shapes · ≤ 120
- `origin` — footer: origin = centre of the underside, on the floor; Blender +Z → Godot +Y

## B03 · ROUTE · 20.93 s · media/B03.mp4 (tools/build_media.py)

The MCP route and its safety settings. Window capture 2026-10-14 12:47 EDT; log verbatim.

- `0.0` — Bao's Blender 5.2.2 window, captured through the MCP with Blender's own screenshot operator: MCP panel 'Connected on port 9876', every library and generator unchecked
- `first status call` — get_addon_status result, verbatim excerpt from evidence/a3/setup/04-mcp-connect.log (2026-10-13 16:30 EDT)
- `background scripts` — note: the earlier script route is kept in tools/blender/script_route/

## B04 · PLAN · 17.24 s · media/B04.mp4 (tools/build_media.py)

Film item: at least one prompt to Claude and what it built. Session excerpt verbatim; the English gloss is labelled as a translation.

- `0.0` — excerpt of this Claude Code session, 2026-10-14 11:59 EDT: Claude's eight-step plan, verbatim in Chinese, with an English gloss
- `Bao's reply` — Bao's two answers, verbatim: 批准，开始建 Stack · 和旧版一样

## B05 · BLENDER CODE · 15.21 s · media/B05.mp4 (tools/build_media.py)

Blender Python, not Godot: shown as a plain code panel with path and lines (the godot-gamedev ledger covers godot/ only).

- `0.0` — tools/blender/build_supply_stack.py lines 50–60, verbatim: the body of MCP call 2 of 7
- `quarter of a metre` — line 54 highlights: location (0, 0, 0.25)
- `dimensions` — line 57 highlights: dimensions (1.20, 0.80, 0.50)
- `scale behind` — note: a default cube is 2 m, so scale becomes (0.6, 0.4, 0.25)

## B06 · BLENDER RESULT · 16.77 s · media/B06.mp4 (tools/build_media.py)

Result of B05. Real Blender window of a film re-run (scratch file outside the repository); the shipped stack was built at 12:00 EDT by the same calls.

- `0.0` — Blender window after call 2 (Blender's own screenshot through the MCP), labelled film re-run, 12:49 EDT
- `scale point six` — callout on the Properties editor: Scale 0.600 / 0.400 / 0.250
- `non-uniform` — callout on the status bar: 'Active object has non-uniform scale'

## B07 · BLENDER CODE · 10.71 s · media/B07.mp4 (tools/build_media.py)

Blender Python shown as a plain code panel with path and lines.

- `0.0` — tools/blender/build_supply_stack.py lines 87–100, verbatim: MCP call 5 of 7
- `applies rotation and scale` — line 96 highlights: transform_apply(location=False, rotation=True, scale=True)

## B08 · BLENDER RESULT · 17.58 s · media/B08.mp4 (tools/build_media.py)

Result of B07, then the look renders of the shipped builds (evidence/a3/mcp/*-look.png).

- `0.0` — Blender window after call 5, sidebar Item tab: Scale 1.000 ×3, Dimensions 1.2 / 0.8 / 0.5 m (film re-run)
- `look tool` — the three MCP look renders (front · back · three-quarter · below), 2026-10-14 11:56–12:04
- `show through` — callout on the stack's below tile: coplanar faces (z-fighting)

## B09 · HAND EDIT · 19.01 s · media/B09.mp4 (tools/build_media.py)

Film item: Bao's own hand edit. Not recorded live (labelled); before/after captures and the measured check.

- `0.0` — before: MCP look render of the shrine, 12:04 EDT
- `twenty degrees` — after: Blender window, OilGem selected, Rotation 0° after Apply, 12:47 EDT
- `His note` — Bao's note from BLENDER-NOTES.md, quoted
- `vertex check` — measured: MCP export's gem rotated 20.0° about Z matches the re-export within 1.84e-8 m

## B10 · CODE · 19.09 s · GodotDevWorkbench

Code beat (code-then-result-v1): godot/tests/test_a3_assets.gd lines 58-64 at c0dba4c, read verbatim; the next beat shows the result.

- `0.0` — Godot editor reconstruction opens on tests/test_a3_assets.gd, lines 58-64
- `Line sixty-one` — line 61 highlights — AABB size vs brief ≤ 0.011 m; base y ≤ 0.011 m
- `Line sixty-two` — line 62 highlights — every MeshInstance3D scale = (1, 1, 1)
- `line sixty-three` — line 63 highlights — parts ≤ budget · triangles ≤ budget
- `notes` — source-notes panel (not Inspector values) lists the related lines

## B11 · RESULT · 16.73 s · media/B11.mp4 (tools/build_media.py)

Result of B10. Recorded tool output (capture/test-run-film-build-raw.txt), not drawn.

- `0.0` — HEADLESS — recorded terminal output of test_a3_assets.gd on a fresh git archive of the film build
- `Brief, Blender` — table: brief · Blender (MCP measure, sidebar) · Godot AABB, per prop
- `cannot show` — limit line: a passing check is not a look
- result media (hashed in gamedev-evidence.json): `media/B11.mp4`

## B12 · CODE · 14.70 s · GodotDevWorkbench

Code beat (code-then-result-v1): godot/a3/lantern_gate.gd lines 1-11 at c0dba4c, read verbatim; the next beat shows the result.

- `0.0` — Godot editor reconstruction opens on a3/lantern_gate.gd, lines 1-11
- `convcolonly` — line 3 highlights — Blender names: BaseCollider-convcolonly · PostCollider-convcolonly
- `physics layer three` — line 10 highlights — layer 3 = bit 4, 'market_prop'
- `no mask` — line 11 highlights — mask 0: the stand-in's mask does the detecting
- `notes` — source-notes panel (not Inspector values) lists the related lines

## B13 · RESULT · 14.78 s · media/B13.mp4 (tools/build_media.py)

Result of B12. Real Movie Maker capture of an isolated copy of the film build.

- `0.0` — real 4K capture, take 'block', collision shapes on; label: real engine capture · scripted input
- `stops at the base` — stand-in stops; logged z = 0.667 m
- `F4` — note: F4 from the 2D game opens res://a3/lantern_gate_room.tscn
- result media (hashed in gamedev-evidence.json): `media/B13.mp4`

## B14 · CODE · 17.56 s · GodotDevWorkbench

Code beat (code-then-result-v1): godot/a3/lantern_gate_room.gd lines 44-54 at c0dba4c, read verbatim; the next beat shows the result.

- `0.0` — Godot editor reconstruction opens on a3/lantern_gate_room.gd, lines 44-54
- `adds an orbit` — line 46 highlights — pitch clamped −50° … +80°
- `Line fifty-one` — line 51 highlights — position on a sphere around (0, 1.15, 0)
- `Line fifty-four` — line 54 highlights — floor mesh hidden below y = 0
- `notes` — source-notes panel (not Inspector values) lists the related lines

## B15 · RESULT · 15.42 s · media/B15.mp4 (tools/build_media.py)

Result of B14 (film item: the three assets in the running Godot scene). Real Movie Maker capture.

- `0.0` — real 4K capture, take 'orbit': start view
- `Around to the back` — E held: half orbit, behind
- `below the floor` — F held: −50°, floor mesh hidden
- `closer` — Z held: zoom in
- `nine checks` — HEADLESS: test_a3_camera.gd 9 checks, 0 failures (recorded)
- result media (hashed in gamedev-evidence.json): `media/B15.mp4`

## B16 · LIMITS · 26.45 s · media/B16.mp4 (tools/build_media.py)

Film item: Bao's human check, what remains uncertain, what Claude got wrong, one next step. Bao's words verbatim; the English is labelled as Claude's translation.

- `0.0` — Bao's words after his look at the F4 room, 2026-10-15, verbatim in Chinese, with Claude's English translation
- `What else` — panel: what Claude got wrong — one prop (A3-R0), MCP call 12 of 13 AssertionError, the fixed camera (A3-R3)
- `Next` — panel: next — barrel 0.60 m tall, centred at z 0.80; still uncertain: one viewer only

## B17 · ROLES · 19.09 s · media/B17.mp4 (tools/build_media.py)

Film item: human and AI contributions, and the source revision shown. From FRICTIONAL.md, SOURCES.md and the session logs.

- `0.0` — two columns: Bao · Claude
- `source revision` — source revision c0dba4c · Godot 4.7.2 · Blender 5.2.2 · mcp-for-blender 2.1.9

## B18 · VERDICT · 16.41 s · ClaudeVerdictArtifact

ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source revision.

- `0.0` — artifact card 'Verdict', heading with the source revision
- `0.2` — implemented line
- `0.45` — collision line
- `0.65` — limits line
- `0.85` — human-judgment line

## B19 · HANDOFF · 19.29 s · ClaudeComposerAsk

HANDOFF LAW — Your Turn: one bounded change plus a prediction and a test. Liam reads the prompt and signs off.

- `0.02` — composer card; greeting 'Your turn.'
- `0.1` — the paste-ready prompt types in
- `0.7` — three output lines: prediction first, run, put it back

## B20 · OUTRO · 13.68 s · ClaudeTitleOutro

OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.

- `0.0` — title 'Lanternfall in 3D, Taken Apart'
- `0.25` — @NikBearBrown
- `0.45` — slug-seeded mascot

Total: 21 beats, 361.9 s.
