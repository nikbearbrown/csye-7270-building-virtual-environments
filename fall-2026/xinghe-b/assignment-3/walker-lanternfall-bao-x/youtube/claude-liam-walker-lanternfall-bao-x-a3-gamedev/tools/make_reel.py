#!/usr/bin/env python3
"""Write beat_sheet.json for the Assignment 3 godot-gamedev (walker) film of Lanternfall.

Godot code excerpts are read from godot/ at run time by line range, so the film shows the file's text; the
evidence ledger re-checks them against the film source revision. Run it again after narration is measured:
measured durations are kept and every Remotion beat's durationSeconds and highlight times follow them.

    python3 tools/make_reel.py
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
GAME = REPO / "godot"
FILM_SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()
SHORT = FILM_SHA[:7]
SLUG = "claude-liam-walker-lanternfall-bao-x-a3-gamedev"
TITLE = "Lanternfall in 3D, Taken Apart"
PROJECT = "walker-lanternfall-bao-x"
HANDLE = "@NikBearBrown"


def excerpt(path: str, a: int, b: int) -> str:
    return "\n".join((GAME / path).read_text().splitlines()[a - 1:b])


def at(text: str, phrase: str, dur: float, lead: float = 0.25) -> float:
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"cue phrase not in narration: {phrase!r}")
    return round(max(0.0, dur * i / max(1, len(text)) - lead), 2)


def code_beat(bid, act, path, a, b, title, narration, cues, notes, output, est, font=None):
    return {"beat_id": bid, "act": act, "kind": "code",
            "role_note": f"Code beat (code-then-result-v1): godot/{path} lines {a}-{b} at {SHORT}, read verbatim; the next beat shows the result.",
            "narration_text": narration, "estimated_duration_s": est, "_cues": cues,
            "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "line-highlight",
                     "show": [{"at": "0.0", "event": f"Godot editor reconstruction opens on {path}, lines {a}-{b}"}] +
                             [{"at": c[0], "event": f"line {c[1]} highlights — {c[2]}"} for c in cues] +
                             [{"at": "notes", "event": "source-notes panel (not Inspector values) lists the related lines"}],
                     "remotion": {"pattern": "GodotDevWorkbench", "props": {
                         "mode": "code", "title": title, "project": PROJECT, "path": f"res://{path}",
                         "source": f"godot/{path} · lines {a}–{b} · source revision {SHORT} · Godot editor reconstruction",
                         "code": excerpt(path, a, b), "startLine": a, "codeFontSize": font or 25,
                         "inspectorLabel": "Source notes — not Inspector values",
                         "notes": [{"label": k, "value": v} for k, v in notes], "output": output,
                         "cues": [], "durationSeconds": est}}}}


OBSERVED = {
    "B11": "Recorded headless output on a fresh copy of the film build: test_a3_assets.gd 17 checks, 0 failures; the three merged AABBs match the brief with height on +Y, every mesh node has scale (1, 1, 1), and the scale-(2, 1, 1) mutation is caught and restored.",
    "B13": "With collision shapes drawn, the stand-in driven by W stops in front of the gate base at z = 0.667 m (base front face 0.40 m + capsule radius 0.25 m); nothing stops it under the lantern arm.",
    "B15": "Real 4K capture driven through the room's input actions: the camera orbits from the front to behind, tilts below the floor (floor mesh hidden, undersides visible), returns to the front and zooms in.",
}


def media_beat(bid, act, narration, show, est, role, result=False):
    b = {"beat_id": bid, "act": act, "kind": "result" if result else "evidence",
         "role_note": role, "narration_text": narration, "estimated_duration_s": est,
         "shot": {"type": "VIDEO", "class": "SHOW", "source": "own", "motion": "real-footage",
                  "show": [{"at": s[0], "event": s[1]} for s in show], "treatment": "none"}}
    if result:
        b["shot"]["evidence_media"] = f"media/{bid}.mp4"
        b["observation"] = OBSERVED[bid]
    return b


ASK = ("Please use Walker to convert my game design document about Lanternfall's fog-bound night market into three "
       "simple Blender props: a Lantern Gate, a Supply Stack and a Lamp-oil Shrine. Build them through the Blender MCP "
       "from basic shapes only, one call per part, at the sizes in my CHANGE-BRIEF, then export GLBs and show all three "
       "in a Godot 3D room.")

BEATS = [
    {"beat_id": "B00", "act": "ASK",
     "role_note": "COLD OPEN LAW — Claude composer; reconstructed Walker prompt from Bao's CHANGE-BRIEF A3-R0 (not a recorded prompt). Liam introduces himself.",
     "narration_text": ("Hej — this is Liam, in for Bear. Bao Xing's third assignment: build three simple 3D props for his "
                        "game by directing Claude through the Blender MCP, change one of them by hand, export them, and show "
                        "all three together in a Godot scene. Here is the ask, rebuilt from his brief."),
     "estimated_duration_s": 18,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card on cream; greeting 'Hej, Liam'"},
                       {"at": "0.25", "event": "the reconstructed Walker prompt types in"},
                       {"at": "0.62", "event": "send arms; running line names the brief and the first two MCP calls"},
                       {"at": "0.75", "event": "three result lines: props and calls, source revision, checks and Bao's part"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Hej, Liam", "topic": "WALKER · GODOT GAMEDEV", "segment": "Lanternfall in 3D",
                  "command": ASK,
                  "runningText": "reading CHANGE-BRIEF.md (A3-R0) · get_addon_status · get_scene_info…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["3 props · 27 build calls through the MCP · code kept in tools/blender/",
                             f"Godot 3D room at source revision {SHORT}",
                             "17 + 14 + 9 headless checks · Bao's hand edit and his own look"]}}}},
    {"beat_id": "B01", "act": "BLUF",
     "role_note": "EXECUTIVE-SUMMARY LAW — hesitant writer. The framing a viewer arrives with ('an AI generated the 3D models') is corrected to what the film shows ('Claude scripted them from primitives').",
     "narration_text": ("The short version. No model generated these props. Claude scripted them from Blender's basic "
                        "shapes, one call per part, and every call is kept. The checks measure size, orientation and scale. "
                        "Whether the props look right in the game is Bao's call, and he made it."),
     "estimated_duration_s": 15, "lead_silence_s": 0.8,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on-correct",
              "show": [{"at": "0.0", "event": "cream page; 'AI generated the props' types"},
                       {"at": "0.3", "event": "'generated' struck in terracotta, 'scripted' typed in"},
                       {"at": "0.6", "event": "'from basic shapes' and 'Bao judges the look' type in"}],
              "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
                  "text": "AI generated the props\nfrom basic shapes\nBao judges the look",
                  "triggerWords": "generated", "replacementWords": "scripted", "fontSize": 185, "lineSpacing": 1.5,
                  "align": "center", "seed": str(sum(map(ord, SLUG))), "mistakeRate": 2, "hesitateWithin": 0,
                  "hesitateBetween": 1, "ink": "#3D3929", "accent": "#D97757", "bg": "#FAF9F5"}}}},
    media_beat("B02", "BRIEF",
               ("Lanternfall is a two-dimensional survivors game set in a fog-bound night market. Bao picked three props "
                "from that market and froze their numbers before the build. A Lantern Gate for the entrance, two point "
                "eight five metres tall, which also blocks the player. A Supply Stack beside a stall. And a Lamp-oil "
                "Shrine near the upgrade area. Each has a size, an origin at the centre of its base, and a triangle budget."),
               [("0.0", "CHANGE-BRIEF A3-R0 header: three props, frozen before the rebuild (commit 8a8c778)"),
                ("Lantern Gate", "column 1: Lantern Gate · 1.20 × 0.80 × 2.85 m · 6 shapes · ≤ 160 triangles · MCP look image"),
                ("Supply Stack", "column 2: Supply Stack · 1.20 × 0.80 × 1.10 m · 3 shapes · ≤ 180"),
                ("Lamp-oil", "column 3: Lamp-oil Shrine · 0.80 × 0.80 × 1.45 m · 3 shapes · ≤ 120"),
                ("origin", "footer: origin = centre of the underside, on the floor; Blender +Z → Godot +Y")], 26,
               "Film item: the game, the three assets and why the game needs each. Values verbatim from CHANGE-BRIEF.md A3-R0; images are the MCP look renders of the finished props (evidence/a3/mcp/)."),
    media_beat("B03", "ROUTE",
               ("The route. A community add-on, MCP for Blender, version two point one point nine, links Claude Code to "
                "Bao's running Blender through a socket on his own machine. The first status call answered straight away: "
                "add-on one point eight, telemetry off, and every model library and generator switched off. Earlier that "
                "day, a different coding session had no MCP tools at all, so the first builds were background scripts."),
               [("0.0", "Bao's Blender 5.2.2 window, captured through the MCP with Blender's own screenshot operator: MCP panel 'Connected on port 9876', every library and generator unchecked"),
                ("first status call", "get_addon_status result, verbatim excerpt from evidence/a3/setup/04-mcp-connect.log (2026-10-13 16:30 EDT)"),
                ("background scripts", "note: the earlier script route is kept in tools/blender/script_route/")], 24,
               "The MCP route and its safety settings. Window capture 2026-10-14 12:47 EDT; log verbatim."),
    media_beat("B04", "PLAN",
               ("Every prop began as a plan that Bao approved before anything was built. For the Supply Stack: clear the "
                "scene through Blender's data, make two crates and a barrel with one call each, apply rotation and scale, "
                "look from four sides, then export. Bao's reply: approved, build the Stack. And keep the barrel as the old "
                "version had it."),
               [("0.0", "excerpt of this Claude Code session, 2026-10-14 11:59 EDT: Claude's eight-step plan, verbatim in Chinese, with an English gloss"),
                ("Bao's reply", "Bao's two answers, verbatim: 批准，开始建 Stack · 和旧版一样")], 20,
               "Film item: at least one prompt to Claude and what it built. Session excerpt verbatim; the English gloss is labelled as a translation."),
    media_beat("B05", "BLENDER CODE",
               ("This is call two, copied verbatim into the build script. A cube is added a quarter of a metre up, so its "
                "base sits on the floor. Then its dimensions are set to one point two by point eight by half a metre. On "
                "Blender's two-metre cube, that leaves a scale behind, on purpose, for now."),
               [("0.0", "tools/blender/build_supply_stack.py lines 50–60, verbatim: the body of MCP call 2 of 7"),
                ("quarter of a metre", "line 54 highlights: location (0, 0, 0.25)"),
                ("dimensions", "line 57 highlights: dimensions (1.20, 0.80, 0.50)"),
                ("scale behind", "note: a default cube is 2 m, so scale becomes (0.6, 0.4, 0.25)")], 18,
               "Blender Python, not Godot: shown as a plain code panel with path and lines (the godot-gamedev ledger covers godot/ only)."),
    media_beat("B06", "BLENDER RESULT",
               ("Here is Blender's own window, captured during a film re-run of the same calls in a scratch file. The "
                "crate sits on the floor. The Properties editor shows scale point six, point four, point two five, and the "
                "status bar warns about non-uniform scale. Exported like this, Godot would receive a scaled node."),
               [("0.0", "Blender window after call 2 (Blender's own screenshot through the MCP), labelled film re-run, 12:49 EDT"),
                ("scale point six", "callout on the Properties editor: Scale 0.600 / 0.400 / 0.250"),
                ("non-uniform", "callout on the status bar: 'Active object has non-uniform scale'")], 18,
               "Result of B05. Real Blender window of a film re-run (scratch file outside the repository); the shipped stack was built at 12:00 EDT by the same calls."),
    media_beat("B07", "BLENDER CODE",
               ("Call five selects every mesh and applies rotation and scale, the same as Control-A in the window. Nothing "
                "moves on screen. The size stays, and the numbers move into the mesh itself."),
               [("0.0", "tools/blender/build_supply_stack.py lines 87–100, verbatim: MCP call 5 of 7"),
                ("applies rotation and scale", "line 96 highlights: transform_apply(location=False, rotation=True, scale=True)")], 14,
               "Blender Python shown as a plain code panel with path and lines."),
    media_beat("B08", "BLENDER RESULT",
               ("After call five, the sidebar reads scale one, one, one, and the dimensions still read one point two, point "
                "eight and point five metres. Then the look tool rendered each finished prop from the front, the back, "
                "three-quarters and below. From below, the barrel's base shares a plane with the crate's underside, and "
                "the two faces show through each other."),
               [("0.0", "Blender window after call 5, sidebar Item tab: Scale 1.000 ×3, Dimensions 1.2 / 0.8 / 0.5 m (film re-run)"),
                ("look tool", "the three MCP look renders (front · back · three-quarter · below), 2026-10-14 11:56–12:04"),
                ("show through", "callout on the stack's below tile: coplanar faces (z-fighting)")], 22,
               "Result of B07, then the look renders of the shipped builds (evidence/a3/mcp/*-look.png)."),
    media_beat("B09", "HAND EDIT",
               ("Then Bao's own edit, with the mouse. He selected the oil gem in the Outliner, turned it twenty degrees "
                "around Z, and applied the rotation. His note: the panel showed twenty, then zero, but the gem kept its new "
                "angle, because applying writes the turn into the mesh. It wasn't recorded live. These are captures from "
                "before and after, and a vertex check confirms twenty degrees."),
               [("0.0", "before: MCP look render of the shrine, 12:04 EDT"),
                ("twenty degrees", "after: Blender window, OilGem selected, Rotation 0° after Apply, 12:47 EDT"),
                ("His note", "Bao's note from BLENDER-NOTES.md, quoted"),
                ("vertex check", "measured: MCP export's gem rotated 20.0° about Z matches the re-export within 1.84e-8 m")], 24,
               "Film item: Bao's own hand edit. Not recorded live (labelled); before/after captures and the measured check."),
    code_beat("B10", "CODE", "tests/test_a3_assets.gd", 58, 64, "Measuring the props in Godot.",
              ("In Godot, one headless script loads each exported file and measures it. Line sixty-one takes the merged "
               "bounding box of every mesh, compares it with the brief within eleven millimetres, and requires the base at "
               "height zero. Line sixty-two requires every mesh node's scale to be one, and line sixty-three counts the "
               "parts and triangles against the budget."),
              [("Line sixty-one", 61, "AABB size vs brief ≤ 0.011 m; base y ≤ 0.011 m"),
               ("Line sixty-two", 62, "every MeshInstance3D scale = (1, 1, 1)"),
               ("line sixty-three", 63, "parts ≤ budget · triangles ≤ budget")],
              [("ASSETS (lines 3–19)", "brief sizes, height on Y"),
               ("_measure (lines 26–47)", "merged AABB, triangles, materials"),
               ("Lines 83–89", "scale (2, 1, 1) caught")],
              ["godot --headless --path godot --script res://tests/test_a3_assets.gd --fixed-fps 60"], 20, font=21),
    media_beat("B11", "RESULT",
               ("Recorded output, headless, on a fresh copy of the film build: seventeen checks, no failures. Brief, Blender "
                "and Godot agree on all three props, with height on Godot's Y axis, and a deliberate scale-two mutation is "
                "caught. This shows size, orientation, scale and names. It cannot show whether they look right."),
               [("0.0", "HEADLESS — recorded terminal output of test_a3_assets.gd on a fresh git archive of the film build"),
                ("Brief, Blender", "table: brief · Blender (MCP measure, sidebar) · Godot AABB, per prop"),
                ("cannot show", "limit line: a passing check is not a look")], 20,
               "Result of B10. Recorded tool output (capture/test-run-film-build-raw.txt), not drawn.", result=True),
    code_beat("B12", "CODE", "a3/lantern_gate.gd", 1, 11, "Two boxes that only collide.",
              ("The gate also blocks. In Blender, two plain boxes carry the suffix convcolonly, so Godot imports them as "
               "collision with no picture. This script puts both bodies on physics layer three, the market-prop layer, and "
               "gives them no mask of their own."),
              [("convcolonly", 3, "Blender names: BaseCollider-convcolonly · PostCollider-convcolonly"),
               ("physics layer three", 10, "layer 3 = bit 4, 'market_prop'"),
               ("no mask", 11, "mask 0: the stand-in's mask does the detecting")],
              [("Colliders", "base 0.80 × 0.80 × 0.32 m · post 0.42 × 0.42 × 2.55 m"),
               ("Cross-arm, lanterns", "no collider"), ("test_lantern_gate.gd", "14 checks")],
              ["lantern_gate.glb.import keeps nodes/use_node_type_suffixes=true (generated by Godot, not hand-written)"], 16),
    media_beat("B13", "RESULT",
               ("In the running room, with collision shapes drawn, the stand-in drives forward and stops at the base, about "
                "two thirds of a metre from the gate's centre: the base's front edge plus the stand-in's radius. There is no "
                "collider under the lantern arm. In the game, F4 opens this room."),
               [("0.0", "real 4K capture, take 'block', collision shapes on; label: real engine capture · scripted input"),
                ("stops at the base", "stand-in stops; logged z = 0.667 m"),
                ("F4", "note: F4 from the 2D game opens res://a3/lantern_gate_room.tscn")], 17,
               "Result of B12. Real Movie Maker capture of an isolated copy of the film build.", result=True),
    code_beat("B14", "CODE", "a3/lantern_gate_room.gd", 44, 54, "The camera Claude forgot.",
              ("One thing Claude got wrong: the brief promised a camera that could move behind and below the props, but the "
               "room shipped with a fixed one. Revision A3-R3 adds an orbit. Line fifty-one places the camera on a sphere "
               "around the props. Line fifty-four hides only the floor's picture once the camera drops below it; its "
               "collider stays."),
              [("adds an orbit", 46, "pitch clamped −50° … +80°"),
               ("Line fifty-one", 51, "position on a sphere around (0, 1.15, 0)"),
               ("Line fifty-four", 54, "floor mesh hidden below y = 0")],
              [("Keys (lines 78–83)", "Q/E orbit · R/F tilt · Z/X zoom"),
               ("_ready (lines 23–30)", "same opening view"),
               ("test_a3_camera.gd", "9 checks, one mutation")],
              ["CHANGE-BRIEF A3-R3, committed 2505638 before the code (c0dba4c)"], 20, font=22),
    media_beat("B15", "RESULT",
               ("Here are the three props in the running Godot scene, driven through the room's real input actions. From the "
                "front. Around to the back. Then down below the floor, where the undersides show. Then back to the front, and "
                "closer. A new headless suite checks the same limits: nine checks, all passing."),
               [("0.0", "real 4K capture, take 'orbit': start view"), ("Around to the back", "E held: half orbit, behind"),
                ("below the floor", "F held: −50°, floor mesh hidden"), ("closer", "Z held: zoom in"),
                ("nine checks", "HEADLESS: test_a3_camera.gd 9 checks, 0 failures (recorded)")], 18,
               "Result of B14 (film item: the three assets in the running Godot scene). Real Movie Maker capture.", result=True),
    media_beat("B16", "LIMITS",
               ("Bao's own look at the final room. The front and back look normal. The lanterns and the gem draw "
                "yellower and the stack redder than in Blender, but the colours hang together, and he accepts that. From "
                "below he sees the overlapping circle under the stack, but only at very low angles, almost never from the "
                "game's view. The stand-in stops in front of the base and post and passes under the lantern arm. What else "
                "Claude got wrong: it first read the assignment as one prop, and one export call failed on its own check. "
                "Next: sit the barrel on the crate."),
               [("0.0", "Bao's words after his look at the F4 room, 2026-10-15, verbatim in Chinese, with Claude's English translation"),
                ("What else", "panel: what Claude got wrong — one prop (A3-R0), MCP call 12 of 13 AssertionError, the fixed camera (A3-R3)"),
                ("Next", "panel: next — barrel 0.60 m tall, centred at z 0.80; still uncertain: one viewer only")], 30,
               "Film item: Bao's human check, what remains uncertain, what Claude got wrong, one next step. Bao's words verbatim; the English is labelled as Claude's translation."),
    media_beat("B17", "ROLES",
               ("Who did what. Bao chose the three props and the MCP route, approved every build plan, made the hand edit, "
                "took the interface screenshot, wrote the interface notes, and judged the room himself. Claude wrote and sent "
                "the twenty-seven build calls, wrote the Godot room and tests, and drafted the documents. This film shows "
                "source revision c zero d b a four c."),
               [("0.0", "two columns: Bao · Claude"), ("source revision", f"source revision {SHORT} · Godot 4.7.2 · Blender 5.2.2 · mcp-for-blender 2.1.9")], 22,
               "Film item: human and AI contributions, and the source revision shown. From FRICTIONAL.md, SOURCES.md and the session logs."),
    {"beat_id": "B18", "act": "VERDICT",
     "role_note": "ClaudeVerdictArtifact — implemented work, limitations, human judgment; shows the source revision.",
     "narration_text": ("The verdict. Implemented: three props built through the MCP from basic shapes, with every call kept, "
                        "and their size, origin and scale confirmed in Godot. The gate blocks only where it should. The limits "
                        "are a colour shift, overlapping faces under the barrel, and one hand edit. How they look is Bao's judgment."),
     "estimated_duration_s": 20,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "artifact-reveal",
              "show": [{"at": "0.0", "event": "artifact card 'Verdict', heading with the source revision"},
                       {"at": "0.2", "event": "implemented line"}, {"at": "0.45", "event": "collision line"},
                       {"at": "0.65", "event": "limits line"}, {"at": "0.85", "event": "human-judgment line"}],
              "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
                  "artifactTitle": "Verdict", "artifactHeading": f"Lanternfall in 3D · source revision {SHORT}",
                  "brandLabel": HANDLE,
                  "artifactLines": ["Implemented: 3 primitive-built props via the MCP, all 27 calls kept, sizes confirmed in Godot.",
                                    "Collision: the gate blocks at its base and post only.",
                                    "Limits: emission colour shift, z-fighting under the barrel, one hand edit.",
                                    "Human judgment: the hand edit and the look at the room — Bao's."]}}}},
    {"beat_id": "B19", "act": "HANDOFF",
     "role_note": "HANDOFF LAW — Your Turn: one bounded change plus a prediction and a test. Liam reads the prompt and signs off.",
     "narration_text": ("Your turn. Paste this: Please use Walker and the Blender MCP on my Supply Stack. Before changing "
                        "anything, predict what the Godot size check will report if the upper crate moves seven centimetres "
                        "along plus Y. Then move it by hand, export, run the check and compare. Here's the catch: that crate's "
                        "edge already sits one centimetre inside the footprint. Liam, in for Bear."),
     "estimated_duration_s": 24,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "type-on",
              "show": [{"at": "0.02", "event": "composer card; greeting 'Your turn.'"},
                       {"at": "0.1", "event": "the paste-ready prompt types in"},
                       {"at": "0.7", "event": "three output lines: prediction first, run, put it back"}],
              "remotion": {"pattern": "ClaudeComposerAsk", "props": {
                  "greeting": "Your turn.", "topic": "WALKER · GODOT GAMEDEV", "segment": "Lanternfall in 3D",
                  "command": ("Please use Walker and the Blender MCP on my Supply Stack. Before changing anything, predict "
                              "what tests/test_a3_assets.gd will report if UpperCrate moves 0.07 m along +Y. Then move it by "
                              "hand in Blender, export the GLB, run the test and compare."),
                  "runningText": "paste this into Claude…",
                  "folderLabel": HANDLE, "modelLabel": "Claude", "effortLabel": "High",
                  "output": ["Prediction written before the move.", "Size check run: compare with your number.",
                             "Then put the crate back."], "animateTyping": True}}}},
    {"beat_id": "B20", "act": "OUTRO",
     "role_note": "OUTRO LAW — ClaudeTitleOutro: exact title, @NikBearBrown, slug-seeded mascot, stock jingle only, no narration.",
     "narration_text": "", "estimated_duration_s": 10.0,
     "shot": {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "mascot-title",
              "show": [{"at": "0.0", "event": f"title '{TITLE}'"}, {"at": "0.25", "event": "@NikBearBrown"},
                       {"at": "0.45", "event": "slug-seeded mascot"}],
              "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "durationSeconds": 10.0}}}},
]


def main() -> None:
    path = REEL / "beat_sheet.json"
    old = {b["beat_id"]: b for b in json.loads(path.read_text())["beats"]} if path.exists() else {}
    beats = []
    for b in BEATS:
        b = json.loads(json.dumps(b))
        prev = old.get(b["beat_id"], {})
        for k in ("actual_duration_s", "audio_file", "render_duration_s", "audio_levelled", "audio_note"):
            if k in prev and k not in b and prev.get("narration_text") == b.get("narration_text"):
                b[k] = prev[k]
        if b["beat_id"] == "B20" and "actual_duration_s" in prev:
            b["actual_duration_s"] = prev["actual_duration_s"]
            b["estimated_duration_s"] = prev["actual_duration_s"]
        dur = b.get("actual_duration_s") or b.get("estimated_duration_s")
        cues = b.pop("_cues", None)
        rem = b["shot"].get("remotion")
        if rem and "durationSeconds" in rem["props"]:
            rem["props"]["durationSeconds"] = round(float(dur), 2)
        if cues:
            rem["props"]["cues"] = [{"at": at(b["narration_text"], p, dur), "line": ln, "label": lab} for p, ln, lab in cues]
        b.setdefault("voice", "am_onyx")
        b.setdefault("engine", "kokoro")
        beats.append(b)
    sheet = {"metadata": {
        "title": TITLE, "slug": SLUG, "topic": "WALKER · GODOT GAMEDEV", "kind": "godot-gamedev", "modifier": "walker",
        "playlist": "CSYE 7270", "brand": "claude-liam", "audience": "CSYE 7270 classmates and instructors",
        "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
        "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "contain",
        "captions": False, "channel_title": "", "channel": HANDLE, "folderLabel": HANDLE,
        "channel_title_note": "empty on purpose: B00's composer already shows @NikBearBrown (OUTRO-LOCK: one handle per beat)",
        "greeting": "Hej, Liam",
        "greeting_note": "hello lexicon: Hej (Swedish), not used by the Assignment 2 film (Merhaba). Liam never takes Wagwan.",
        "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
        "game": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x", "project_dir": "godot",
                 "source_revision": FILM_SHA, "godot": "4.7.2.stable.official.ed1daf0bf",
                 "blender": "5.2.2 LTS", "mcp": "mcp-for-blender 2.1.9 (add-on 1.8)"},
        "teaching_contract": "code-then-result-v1",
        "note": ("godot-gamedev + walker teardown of Bao Xing's CSYE 7270 Assignment 3. Godot code panels are verbatim "
                 f"excerpts of godot/ at {FILM_SHA}; Blender code panels are verbatim from tools/blender/; the Godot shots "
                 "are real Movie Maker captures of an isolated copy of that revision, driven through the room's input "
                 "actions; the Blender stills are Blender's own window screenshots (through the MCP) and the MCP look "
                 "renders. No paid call, no upload."),
        "links": {"repo": "https://github.com/yanxlh/walker-lanternfall-bao-x"},
        "tags": ["Godot 4", "Blender", "Blender MCP", "godot-gamedev", "Walker", "glTF", "CSYE 7270",
                 "Teardown register", "Kokoro"]},
        "beats": beats}
    path.write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    words = sum(len(b["narration_text"].split()) for b in beats)
    est = sum(float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in beats)
    print(f"{path}: {len(beats)} beats, {words} words, ~{est:.0f}s")


if __name__ == "__main__":
    main()
