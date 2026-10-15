# SCRIPT — Lanternfall in 3D, Taken Apart

The narration, beat by beat, as spoken (Kokoro `am_onyx`, Liam in for Bear), with measured durations and what is on screen.

## B00 · ASK · 0:00.0 · 15.6 s

Hej — this is Liam, in for Bear. Bao Xing's third assignment: build three simple 3D props for his game by directing Claude through the Blender MCP, change one of them by hand, export them, and show all three together in a Godot scene. Here is the ask, rebuilt from his brief.

On screen: composer card on cream; greeting 'Hej, Liam'; the reconstructed Walker prompt types in; send arms; running line names the brief and the first two MCP calls; three result lines: props and calls, source revision, checks and Bao's part

## B01 · BLUF · 0:15.6 · 14.4 s

The short version. No model generated these props. Claude scripted them from Blender's basic shapes, one call per part, and every call is kept. The checks measure size, orientation and scale. Whether the props look right in the game is Bao's call, and he made it.

On screen: cream page; 'AI generated the props' types; 'generated' struck in terracotta, 'scripted' typed in; 'from basic shapes' and 'Bao judges the look' type in

## B02 · BRIEF · 0:30.0 · 21.2 s

Lanternfall is a two-dimensional survivors game set in a fog-bound night market. Bao picked three props from that market and froze their numbers before the build. A Lantern Gate for the entrance, two point eight five metres tall, which also blocks the player. A Supply Stack beside a stall. And a Lamp-oil Shrine near the upgrade area. Each has a size, an origin at the centre of its base, and a triangle budget.

On screen: CHANGE-BRIEF A3-R0 header: three props, frozen before the rebuild (commit 8a8c778); column 1: Lantern Gate · 1.20 × 0.80 × 2.85 m · 6 shapes · ≤ 160 triangles · MCP look image; column 2: Supply Stack · 1.20 × 0.80 × 1.10 m · 3 shapes · ≤ 180; column 3: Lamp-oil Shrine · 0.80 × 0.80 × 1.45 m · 3 shapes · ≤ 120; footer: origin = centre of the underside, on the floor; Blender +Z → Godot +Y

## B03 · ROUTE · 0:51.2 · 20.9 s

The route. A community add-on, MCP for Blender, version two point one point nine, links Claude Code to Bao's running Blender through a socket on his own machine. The first status call answered straight away: add-on one point eight, telemetry off, and every model library and generator switched off. Earlier that day, a different coding session had no MCP tools at all, so the first builds were background scripts.

On screen: Bao's Blender 5.2.2 window, captured through the MCP with Blender's own screenshot operator: MCP panel 'Connected on port 9876', every library and generator unchecked; get_addon_status result, verbatim excerpt from evidence/a3/setup/04-mcp-connect.log (2026-10-13 16:30 EDT); note: the earlier script route is kept in tools/blender/script_route/

## B04 · PLAN · 1:12.2 · 17.2 s

Every prop began as a plan that Bao approved before anything was built. For the Supply Stack: clear the scene through Blender's data, make two crates and a barrel with one call each, apply rotation and scale, look from four sides, then export. Bao's reply: approved, build the Stack. And keep the barrel as the old version had it.

On screen: excerpt of this Claude Code session, 2026-10-14 11:59 EDT: Claude's eight-step plan, verbatim in Chinese, with an English gloss; Bao's two answers, verbatim: 批准，开始建 Stack · 和旧版一样

## B05 · BLENDER CODE · 1:29.4 · 15.2 s

This is call two, copied verbatim into the build script. A cube is added a quarter of a metre up, so its base sits on the floor. Then its dimensions are set to one point two by point eight by half a metre. On Blender's two-metre cube, that leaves a scale behind, on purpose, for now.

On screen: tools/blender/build_supply_stack.py lines 50–60, verbatim: the body of MCP call 2 of 7; line 54 highlights: location (0, 0, 0.25); line 57 highlights: dimensions (1.20, 0.80, 0.50); note: a default cube is 2 m, so scale becomes (0.6, 0.4, 0.25)

## B06 · BLENDER RESULT · 1:44.6 · 16.8 s

Here is Blender's own window, captured during a film re-run of the same calls in a scratch file. The crate sits on the floor. The Properties editor shows scale point six, point four, point two five, and the status bar warns about non-uniform scale. Exported like this, Godot would receive a scaled node.

On screen: Blender window after call 2 (Blender's own screenshot through the MCP), labelled film re-run, 12:49 EDT; callout on the Properties editor: Scale 0.600 / 0.400 / 0.250; callout on the status bar: 'Active object has non-uniform scale'

## B07 · BLENDER CODE · 2:01.4 · 10.7 s

Call five selects every mesh and applies rotation and scale, the same as Control-A in the window. Nothing moves on screen. The size stays, and the numbers move into the mesh itself.

On screen: tools/blender/build_supply_stack.py lines 87–100, verbatim: MCP call 5 of 7; line 96 highlights: transform_apply(location=False, rotation=True, scale=True)

## B08 · BLENDER RESULT · 2:12.1 · 17.6 s

After call five, the sidebar reads scale one, one, one, and the dimensions still read one point two, point eight and point five metres. Then the look tool rendered each finished prop from the front, the back, three-quarters and below. From below, the barrel's base shares a plane with the crate's underside, and the two faces show through each other.

On screen: Blender window after call 5, sidebar Item tab: Scale 1.000 ×3, Dimensions 1.2 / 0.8 / 0.5 m (film re-run); the three MCP look renders (front · back · three-quarter · below), 2026-10-14 11:56–12:04; callout on the stack's below tile: coplanar faces (z-fighting)

## B09 · HAND EDIT · 2:29.7 · 19.0 s

Then Bao's own edit, with the mouse. He selected the oil gem in the Outliner, turned it twenty degrees around Z, and applied the rotation. His note: the panel showed twenty, then zero, but the gem kept its new angle, because applying writes the turn into the mesh. It wasn't recorded live. These are captures from before and after, and a vertex check confirms twenty degrees.

On screen: before: MCP look render of the shrine, 12:04 EDT; after: Blender window, OilGem selected, Rotation 0° after Apply, 12:47 EDT; Bao's note from BLENDER-NOTES.md, quoted; measured: MCP export's gem rotated 20.0° about Z matches the re-export within 1.84e-8 m

## B10 · CODE · 2:48.7 · 19.1 s

In Godot, one headless script loads each exported file and measures it. Line sixty-one takes the merged bounding box of every mesh, compares it with the brief within eleven millimetres, and requires the base at height zero. Line sixty-two requires every mesh node's scale to be one, and line sixty-three counts the parts and triangles against the budget.

On screen: Godot editor reconstruction opens on tests/test_a3_assets.gd, lines 58-64; line 61 highlights — AABB size vs brief ≤ 0.011 m; base y ≤ 0.011 m; line 62 highlights — every MeshInstance3D scale = (1, 1, 1); line 63 highlights — parts ≤ budget · triangles ≤ budget; source-notes panel (not Inspector values) lists the related lines

## B11 · RESULT · 3:07.8 · 16.7 s

Recorded output, headless, on a fresh copy of the film build: seventeen checks, no failures. Brief, Blender and Godot agree on all three props, with height on Godot's Y axis, and a deliberate scale-two mutation is caught. This shows size, orientation, scale and names. It cannot show whether they look right.

On screen: HEADLESS — recorded terminal output of test_a3_assets.gd on a fresh git archive of the film build; table: brief · Blender (MCP measure, sidebar) · Godot AABB, per prop; limit line: a passing check is not a look

## B12 · CODE · 3:24.5 · 14.7 s

The gate also blocks. In Blender, two plain boxes carry the suffix convcolonly, so Godot imports them as collision with no picture. This script puts both bodies on physics layer three, the market-prop layer, and gives them no mask of their own.

On screen: Godot editor reconstruction opens on a3/lantern_gate.gd, lines 1-11; line 3 highlights — Blender names: BaseCollider-convcolonly · PostCollider-convcolonly; line 10 highlights — layer 3 = bit 4, 'market_prop'; line 11 highlights — mask 0: the stand-in's mask does the detecting; source-notes panel (not Inspector values) lists the related lines

## B13 · RESULT · 3:39.2 · 14.8 s

In the running room, with collision shapes drawn, the stand-in drives forward and stops at the base, about two thirds of a metre from the gate's centre: the base's front edge plus the stand-in's radius. There is no collider under the lantern arm. In the game, F4 opens this room.

On screen: real 4K capture, take 'block', collision shapes on; label: real engine capture · scripted input; stand-in stops; logged z = 0.667 m; note: F4 from the 2D game opens res://a3/lantern_gate_room.tscn

## B14 · CODE · 3:54.0 · 17.6 s

One thing Claude got wrong: the brief promised a camera that could move behind and below the props, but the room shipped with a fixed one. Revision A3-R3 adds an orbit. Line fifty-one places the camera on a sphere around the props. Line fifty-four hides only the floor's picture once the camera drops below it; its collider stays.

On screen: Godot editor reconstruction opens on a3/lantern_gate_room.gd, lines 44-54; line 46 highlights — pitch clamped −50° … +80°; line 51 highlights — position on a sphere around (0, 1.15, 0); line 54 highlights — floor mesh hidden below y = 0; source-notes panel (not Inspector values) lists the related lines

## B15 · RESULT · 4:11.5 · 15.4 s

Here are the three props in the running Godot scene, driven through the room's real input actions. From the front. Around to the back. Then down below the floor, where the undersides show. Then back to the front, and closer. A new headless suite checks the same limits: nine checks, all passing.

On screen: real 4K capture, take 'orbit': start view; E held: half orbit, behind; F held: −50°, floor mesh hidden; Z held: zoom in; HEADLESS: test_a3_camera.gd 9 checks, 0 failures (recorded)

## B16 · LIMITS · 4:26.9 · 26.4 s

Bao's own look at the final room. The front and back look normal. The lanterns and the gem draw yellower and the stack redder than in Blender, but the colours hang together, and he accepts that. From below he sees the overlapping circle under the stack, but only at very low angles, almost never from the game's view. The stand-in stops in front of the base and post and passes under the lantern arm. What else Claude got wrong: it first read the assignment as one prop, and one export call failed on its own check. Next: sit the barrel on the crate.

On screen: Bao's words after his look at the F4 room, 2026-10-15, verbatim in Chinese, with Claude's English translation; panel: what Claude got wrong — one prop (A3-R0), MCP call 12 of 13 AssertionError, the fixed camera (A3-R3); panel: next — barrel 0.60 m tall, centred at z 0.80; still uncertain: one viewer only

## B17 · ROLES · 4:53.4 · 19.1 s

Who did what. Bao chose the three props and the MCP route, approved every build plan, made the hand edit, took the interface screenshot, wrote the interface notes, and judged the room himself. Claude wrote and sent the twenty-seven build calls, wrote the Godot room and tests, and drafted the documents. This film shows source revision c zero d b a four c.

On screen: two columns: Bao · Claude; source revision c0dba4c · Godot 4.7.2 · Blender 5.2.2 · mcp-for-blender 2.1.9

## B18 · VERDICT · 5:12.5 · 16.4 s

The verdict. Implemented: three props built through the MCP from basic shapes, with every call kept, and their size, origin and scale confirmed in Godot. The gate blocks only where it should. The limits are a colour shift, overlapping faces under the barrel, and one hand edit. How they look is Bao's judgment.

On screen: artifact card 'Verdict', heading with the source revision; implemented line; collision line; limits line; human-judgment line

## B19 · HANDOFF · 5:28.9 · 19.3 s

Your turn. Paste this: Please use Walker and the Blender MCP on my Supply Stack. Before changing anything, predict what the Godot size check will report if the upper crate moves seven centimetres along plus Y. Then move it by hand, export, run the check and compare. Here's the catch: that crate's edge already sits one centimetre inside the footprint. Liam, in for Bear.

On screen: composer card; greeting 'Your turn.'; the paste-ready prompt types in; three output lines: prediction first, run, put it back

## B20 · OUTRO · 5:48.2 · 13.7 s

*(no narration: stock outro jingle)*

On screen: title 'Lanternfall in 3D, Taken Apart'; @NikBearBrown; slug-seeded mascot

Total 361.9 s.
