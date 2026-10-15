#!/usr/bin/env python3
"""Author beat_sheet.json for the walker-rudy Assignment 3 godot-gamedev film.

Every Godot code excerpt is cut from godot/ by line range here, so the text on
screen is the text in the file. Timing fields (durationSeconds, cue times) are
filled later by build_reel.py from the measured narration.

    python3 tools/make_sheet.py        # from the reel folder
"""
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "godot"
PUB = "reels/claude-liam-walker-rudy-3d-props"   # Remotion public/ subfolder for this reel's figures
TITLE = "Three Props for Walker Rudy."
SLUG = "claude-liam-walker-rudy-3d-props"
REV = "f6f8acf"
PROJECT = f"Walker Rudy Props 3D · godot/ @ {REV}"
TOPIC = "WALKER-RUDY · BLENDER MCP TO GODOT 4.7"


def lines(path, a, b):
    return "\n".join((GAME / path).read_text().splitlines()[a - 1:b])


def code(bid, act, path, a, b, title, narration, cues, notes, output, components, font=25):
    return {
        "beat_id": bid, "act": act, "narration_text": narration, "components": components,
        "shot": {"type": "REMOTION", "lane": "code", "remotion": {"pattern": "GodotDevWorkbench", "props": {
            "mode": "code", "title": title, "project": PROJECT, "path": "res://" + path,
            "source": f"Source: assignment-3/godot/{path}, lines {a}–{b} (verbatim). Godot editor reconstruction.",
            "code": lines(path, a, b), "startLine": a, "codeFontSize": font,
            "inspectorLabel": "Source notes — not Inspector values",
            "notes": [{"label": k, "value": v} for k, v in notes],
            "output": output}},
            "cue_phrases": [{"phrase": p, "line": ln, "label": lb} for p, ln, lb in cues]},
        "excerpt": {"path": path, "start_line": a, "end_line": b},
    }


def figure(bid, act, title, status, image, image_label, source, cards, cues, narration, components=(), excerpt=""):
    return {"beat_id": bid, "act": act, "narration_text": narration, "components": list(components),
            "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "GodotDesignFigure", "props": {
                "title": title, "status": status, "image": f"{PUB}/{image}", "imageLabel": image_label,
                "excerpt": excerpt, "source": source, "cards": [{"label": a, "text": b} for a, b in cards]}},
                "cue_cards": [[p, k] for p, k in cues]}}


def still(bid, act, image, observation, narration, components=()):
    return {"beat_id": bid, "act": act, "narration_text": narration, "components": list(components),
            "shot": {"type": "VIDEO", "lane": "evidence", "source": "own", "treatment": "none",
                     "evidence_media": f"stills/{image}", "still_plan": {"image": f"stills/{image}"},
                     "observation": observation},
            "qc": {"full_bleed": False}}


B = []

# ── walker bookends ─────────────────────────────────────────────────────────
B.append({"beat_id": "B00", "act": "cold open — the Walker ask", "components": [],
  "role_note": "walker modifier B00. Reconstructed prompt, said out loud; not a transcript.",
  "narration_text": "Jambo, this is Liam, in for Bear. That prompt is an illustrative reconstruction, not something anyone typed. "
                    "What is real is underneath it: walker-rudy, the game shuai-z started in Assignment 2, and three props now built "
                    "in Blender by directing Claude through the Blender MCP, then checked in Godot.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Jambo, Liam", "topic": TOPIC, "segment": TITLE,
    "command": "Please use Walker to convert my game design document about Walker Rudy — a chibi boy who crosses the Harvest Fields past "
               "spikes and a waystone checkpoint to a teleport circle — into three simple 3D props built in Blender through the Blender "
               "MCP, exported as .glb, and shown side by side at game scale in a small Godot 3D scene.",
    "runningText": "reconstructed prompt — illustrative, not a transcript…",
    "output": [f"Repo walker-rudy · assignment-3/ at {REV} · Blender 5.2.2 · MCP for Blender 2.1.9 · Godot 4.7.2.",
               "Built: waystone, teleport circle, spikes — basic shapes, flat colours, 82 to 280 triangles each.",
               "Brief, approvals and the hand edit: shuai-z · every Blender call and the Godot scripts: Claude Code."],
    "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})

B.append({"beat_id": "B01", "act": "BLUF — what was actually built", "components": [], "lead_silence_s": 0.8,
  "role_note": "EXECUTIVE-SUMMARY LAW. The correction is the misconception: nothing here was sculpted or generated.",
  "qc": {"sparse_by_design": True, "sparse_reason": "BrutalistHesitantWriter types the overview token by token; mid-beat frames are mostly cream by design."},
  "narration_text": "Three props for Walker Rudy, assembled from basic shapes. Nobody sculpted them, and no model generated a mesh. "
                    "Claude moved cubes, cones and cylinders in a running Blender, shuai-z made one edit by hand, and Godot measured the result.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "BrutalistHesitantWriter", "props": {
    "text": "Three props for Walker Rudy,\nsculpted from basic shapes,\nmeasured in Godot.",
    "triggerWords": "sculpted", "replacementWords": "assembled",
    "seed": "walker-rudy-3d-props-bluf-2026-10-13", "face": "serif", "fontSize": 112, "lineSpacing": 1.4,
    "align": "center", "charMs": 24, "jitter": 6, "mistakeRate": 3, "hesitateWithin": 1, "hesitateBetween": 4, "banner": ""}}}})

# ── the game, the brief ─────────────────────────────────────────────────────
B.append(still("B02", "the game and the three props", "game-card.png",
  "The game's own 2D files drawn at one scale on a common ground line: Rudy (160 px), the spikes, the lit waystone and the teleport circle, "
  "each labelled with its role in Level 1.",
  "Walker Rudy is a 2D side-scroller. Rudy crosses Level 1, the Harvest Fields, and these are the three props on his way: "
  "spikes, which cost him a heart; the waystone, where he gets back up; and the teleport circle that ends the level. "
  "Here they are from the game's own files, all at one scale. Rudy is a hundred and sixty pixels tall, so shuai-z set him at one point two metres, "
  "and every size in the brief comes from these pixels.", ["props-glb"]))

B.append(figure("B03", "the brief, before building", "The Brief, Committed Before Building",
  "CHANGE-BRIEF.md · revision 1, committed before any prop existed", "brief.png", "",
  "Source: CHANGE-BRIEF.md revisions 1–3 (the waystone's shapes and budget changed in revision 2; revision 1 is kept).",
  [("Size", "metres, from the 2D pixels"), ("Origin", "centre of the underside"), ("Budget", "100 to 300 triangles"), ("Predictions", "six, each with a check")],
  [["in metres", 0], ["origin", 1], ["triangle budget", 2], ["six failures", 3]],
  "Before anything was built, the brief was committed. Each prop in metres, its origin at the centre of its underside so it stands on the floor, "
  "its shapes and a triangle budget. And six failures, predicted with a way to catch each: lying on its side, because Blender is Z-up and Godot is Y-up, "
  "the wrong size by a factor, a floating origin, too many triangles, a colour lost in export, and more detail than asked.", ["props-glb"]))

# ── Blender: the real session ───────────────────────────────────────────────
B.append(figure("B04", "the real Blender session", "shuai-z's Own Blender Screenshots",
  "SCREENSHOTS BY SHUAI-Z — the real session, not reconstructions", "blender-own.png", "",
  "Source: assignment-3/evidence/blender-notes-cube-selected.png and evidence/mcp-panel-connected.png (taken by shuai-z, 2026-10-12 and 10-13).",
  [("Blender", "5.2.2 LTS, macOS"), ("Sidebar (N)", "location, size, dimensions"), ("MCP add-on", "1.8, port 9876"), ("Off", "every download and generator")],
  [["Blender", 0], ["sidebar", 1], ["port", 2], ["switched off", 3]],
  "Now the real Blender. These two are shuai-z's own screenshots. On the left, Blender five point two with the default cube selected and the sidebar "
  "open, the panel that shows an object's dimensions. On the right, the MCP for Blender tab, connected on port ninety eight seventy six, "
  "with every asset library and generator switched off, so no geometry could come from anywhere but these shapes."))

B.append(still("B05", "one prompt → the code Claude ran", "prompt-code.png",
  "shuai-z's Chinese prompt from the session (20:14 EDT), with Claude's translation, beside tools/blender/build_waystone.py lines 301–311: "
  "the 8-sided Rune_Ring cylinder Claude added in one execute_blender_code call.",
  "Here is one prompt and what it did. The waystone's rune had become a capital R, and shuai-z wrote: it does not look good now; no R, try a ring. "
  "Claude answered with code, run inside that Blender. An eight-sided cylinder, twenty-two centimetres across, two centimetres deep, turned to lie flat "
  "against the stone at the height shuai-z had chosen by hand. Every one of these calls is kept, in order, in the tools folder.", ["props-glb"]))

B.append(still("B06", "what it built", "prompt-result.png",
  "The MCP look image Claude captured at 20:15 EDT: the waystone from the front and three-quarter, the blue 8-sided ring with a stone-coloured centre.",
  "And this is what it built: Blender's own viewport, captured by Claude through the MCP's look tool, not a screenshot shuai-z took. "
  "A blue ring with a stone-coloured disc in its middle. A torus is not one of the course's basic shapes, so the ring is two cylinders.", ["props-glb"]))

B.append(still("B07", "the hand edit — before and after", "hand-edit.png",
  "Front views from the MCP look tool: before (19:58 EDT, as built, rune centre Z 0.42) and after (the saved hand-edited file, rune centre Z 0.4537); "
  "the guide lines mark the rune's top in each.",
  "Before any of that came the hand edit. Left, the rune as Claude built it. Right, the saved file after shuai-z moved it in Blender's window: "
  "G, then Z, then a drag. G starts a move and Z locks it to the vertical axis. Three point four centimetres up. These are comparison stills, not a recording; "
  "no recording of the edit was made. What it taught: Blender's keys are a sequence, not a chord.", ["props-glb"]))

B.append(figure("B08", "inspect and revise", "Inspect, Revise, Keep",
  "ONE REVISION CYCLE — every image from the MCP look tool", "revision-strip.png", "",
  "Source: blender-looks/ (MCP look captures, 2026-10-13 19:58–20:18 EDT); FRICTIONAL.md; CHANGE-BRIEF.md revision 2.",
  [("Built", "a plain rectangle"), ("Rejected", "the R, on sight"), ("Kept", "12 sides, a thinner band"), ("Budget", "60 → 130, with a reason")],
  [["rectangle", 0], ["rejected", 1], ["twelve sides", 2], ["sixty", 3]],
  "The whole cycle. A plain rectangle, moved by hand. An R, which went over budget and was rejected on sight. An eight-sided ring, then twelve sides "
  "and a thinner band, kept. That pushed the waystone from forty-two triangles to a hundred and eighteen, past the brief's sixty, so revision two raised the "
  "budget to a hundred and thirty and said why. Revision one stays as it was.", ["props-glb"]))

B.append(figure("B09", "the other two props", "The Teleport Circle and the Spikes",
  "BLENDER VIEWPORT — captured by Claude through the MCP look tool", "other-props.png", "",
  "Source: blender-looks/7-teleport-circle.png (21:02 EDT) and 8-spikes.png (21:18 EDT); sizes and counts read through the MCP (TEST-REPORT.md).",
  [("Circle", "three discs, three runes"), ("Undersides", "fixed in revision 3"), ("Spikes", "five 8-sided cones"), ("Budget", "280 / 300 · 82 / 100")],
  [["stacked discs", 0], ["undersides", 1], ["five", 2], ["eighty-two", 3]],
  "The other two, built the same way. The teleport circle is three stacked discs and three rune marks. While planning it, Claude found that all three "
  "undersides would share the floor plane and flicker from below, which the brief had missed, so revision three lifted two of them. The spikes are a wooden "
  "block and five eight-sided cones. Two hundred eighty triangles of three hundred, and eighty-two of a hundred.", ["props-glb"]))

# ── Godot: code → result ────────────────────────────────────────────────────
B.append(code("B10", "the scene — one line per prop", "tools/build_props_room.gd", 10, 18, "Placing Three Props on One Floor",
  "Each prop was exported as its own glb file, with Blender's plus Y up option, and loaded into a new Godot project. A script builds the scene. "
  "Look at the table: a name, a file and an X position, and no height at all. Every prop goes in at Y equals zero. That only works because each origin "
  "is the centre of the prop's underside. And a one point two metre post stands in for Rudy, so the sizes can be judged.",
  [("a name, a file", 13, "name, .glb file, X in metres"), ("no height", 11, "Y = 0 puts it on the floor"), ("one point two metre post", 18, "RUDY_HEIGHT = 1.2 m")],
  [("Floor", "8 × 5 m (line 38)"), ("Light, camera", "one sun with shadows; fov 50"),
   ("Export", "binary glTF, +Y Up")],
  ["Godot --headless --path godot --script res://tools/build_props_room.gd → scenes/props_room.tscn"], ["scene"], font=27))
B.append({"beat_id": "B11", "act": "result — the running scene", "components": ["scene", "props-glb"],
  "narration_text": "And here is the scene running in Godot, rendered at 4K. The camera starts where the scene puts it, then circles once. "
                    "From left to right: the post, the spikes up to below its middle, the waystone, and the teleport circle, almost twice as wide as he is tall. "
                    "From behind, the waystone is plain, as built. Each prop casts its shadow from its own base.",
  "shot": {"type": "VIDEO", "lane": "gameplay", "source": "own", "treatment": "none", "evidence_media": "media/B11.mp4",
           "capture_plan": {"capture": "orbit-01", "segments": [{"from": 0, "to": 691, "speed": 1.0, "label": ""}],
                            "chips": ["CAMERA ORBIT ADDED FOR THE FILM · props, light and floor untouched"], "silent_source": True},
           "observation": "The real main scene res://scenes/props_room.tscn in Godot 4.7.2 Forward+, Movie Maker at 3840×2160, 30 fps: 45 frames on the "
                          "scene's own camera, a 600-frame orbit at its radius (4.6 m) and height (2.2 m), 45 frames back home. All three props stand on the "
                          "floor with shadows from their bases; the waystone's back is plain."},
  "qc": {"full_bleed": True, "full_bleed_reason": "Engine capture: the 3D scene renders edge to edge at 3840x2160; the film's chips sit inside the title-safe inset. Only the edge-bleed check is waived."}})

B.append(code("B12", "the check — axis and origin", "tests/check_props.gd", 62, 71, "Numbers, Not Looks",
  "The check. It loads each glb on its own, with no window, and measures its bounding box. Width, depth and height must match the brief within "
  "five millimetres. Then the lines that catch two predicted failures. Which axis carries the height? Upright means only Y does, which catches the "
  "lying-on-its-side failure. And the centre of the underside must sit at the origin, or the prop would float or sink.",
  [("which axis", 62, "the brief's height, found on which axis?"), ("Upright means", 65, "within TOL on this axis?"),
   ("centre of the underside", 70, "origin check"), ("float or sink", 71, "underside centre within 5 mm of (0, 0, 0)")],
  [("Size, lines 55–60", "bounding box; width X, depth Z, height Y each within TOL = 0.005 m"),
   ("Also checked", "node scale and rotation, triangles, colours")],
  ["timeout 120 Godot --headless --path godot --script res://tests/check_props.gd --fixed-fps 60"], ["check"], font=25))
B.append(still("B13", "result — the headless numbers", "headless-numbers.png",
  "Recorded headless output on an isolated copy of godot/ at f6f8acf: the three bounding boxes match the brief to four decimals, heights on Y, "
  "origins at (0, 0, 0), 118/130, 280/300 and 82/100 triangles; 44 ok lines, PASS: 0 failed check(s), exit code 0.",
  "These are headless numbers, run again for this film. Brief, Blender and Godot agree: point seven by point four by point eight four for the waystone, "
  "to four decimal places. Every height is on Y, every origin is at zero, every count is inside its budget. Forty-four checks, zero failed. "
  "Read the last line, not the exit code: when the first version of this script would not even parse, Godot still exited with zero.", ["check"]))

B.append(code("B14", "the check — sitting on the floor", "tests/check_props.gd", 93, 104, "Does It Sit on the Floor?",
  "The second part loads the scene itself. It finds the floor's top from the floor mesh, not from the prop, and then asks, for each prop, how far its lowest "
  "point is above it. In Module 3, an agent's floor check measured the object against its own collider and proved nothing. So: can this one fail?",
  [("floor's top", 97, "from the Floor mesh's own box"), ("lowest point", 103, "gap = prop bottom − floor top"), ("can this one fail", 104, "within 5 mm, or FAIL")],
  [("Floor top", "Y = 0.0000 in the scene"), ("Scene", "res://scenes/props_room.tscn"), ("Not checked", "whether it looks right")],
  ["_expect prints ok or FAIL and counts failures"], ["check", "scene"], font=26))
B.append(still("B15", "result — yes, it can fail", "fail-diagnostic.png",
  "Recorded output: the scene as built passes (lowest point 0.0000 m); an isolated copy with the waystone's transform Y set to 0.3 reports "
  "'FAIL Waystone sits on the floor (lowest point 0.3000 m above the floor's top)', 'FAIL: 1 failed check(s)', exit code 1.",
  "Yes. On an isolated copy, the waystone was raised thirty centimetres in the scene file, and nothing else changed. The check reports it, fails, and exits "
  "with one. A test of the test, not the game; the project's scene was never touched.", ["check", "scene"]))

# ── verdict, your turn, outro ───────────────────────────────────────────────
B.append({"beat_id": "BVD1", "act": "verdict — checked, uncertain, wrong", "components": ["screenshots", "check"], "lead_silence_s": 0.4,
  "narration_text": "Verdict. Checked by machine: sizes, axis, origin, scale, triangles and colours, forty-four checks, and the check can fail. "
                    "Checked by a person: shuai-z walked the camera round, behind and below. The sizes suit the post, and the spikes look most like the 2D art; "
                    "the teleport circle least, with no rune pattern, no light and no glow. Uncertain: no one else has looked, it ran only on a Mac, "
                    "and the scene is not yet joined to the game. What Claude got wrong: the brief missed the undersides, the first check never ran, "
                    "and the first screenshot was taken from the wrong place.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Checked, uncertain, wrong",
    "artifactLines": [f"Machine: 44 headless checks pass on godot/ at {REV} (re-run for this film on an isolated copy); with the waystone raised 0.3 m, the floor check fails, exit code 1.",
                      "Human: shuai-z looked in the Godot editor, from behind and below: sizes suit the 1.2 m post; the gold is brighter in Godot than in Blender; spikes closest to the 2D art, the teleport circle furthest.",
                      "Uncertain: no second viewer; macOS only; Blender sizes read by code, not from the sidebar; the scene is separate from the 2D game.",
                      "Claude got wrong: the brief missed the circle's undersides (revision 3); the first check had parse errors yet exited 0; the first screenshot read the camera before the scene was in the tree."]}}}})
B.append({"beat_id": "BVD2", "act": "verdict — who made what, next step", "components": [],
  "narration_text": "Who made what. shuai-z chose the props, approved the brief and every build step, made the hand edit, rejected the R and chose the ring, "
                    "and did the human check. Claude drafted the brief, wrote and ran every Blender call through the MCP, the export, the Godot scene, "
                    "the check and this film. The source shown is f six f eight a c f. The next step is the teleport circle: its rune pattern, its column of light and its glow.",
  "shot": {"type": "REMOTION", "lane": "card", "remotion": {"pattern": "ClaudeVerdictArtifact", "props": {
    "artifactTitle": TITLE, "artifactHeading": "Who made what",
    "artifactLines": ["shuai-z: chose the three props; approved the brief and each build step; the hand edit (rune +0.034 m); rejected the R; chose the ring, 12 sides, the thinner band; the human check.",
                      "Claude Code (Opus 5.5): drafted CHANGE-BRIEF.md; wrote and ran every execute_blender_code call (tools/blender/); the glTF export; the Godot scene, check and screenshot scripts; this film.",
                      "Not used: asset libraries, downloaded models, generate_3d. Narration: Liam, local Kokoro am_onyx.",
                      f"Source shown: walker-rudy assignment-3/ at {REV}. Next step: the teleport circle's rune pattern, column of light and glow."]}}}})
B.append({"beat_id": "BHTF", "act": "your turn", "components": [],
  "narration_text": "Your turn. Here is the prompt, read it with me. Read my change brief and check props dot g d. Before you change anything, predict what the "
                    "check will print if the spikes are exported with their origin at the centre of the block instead of the underside. Then make that change "
                    "on a copy, re-export, and show me the check before and after. Write your prediction down first. Liam, in for Bear.",
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeComposerAsk", "props": {
    "greeting": "Your turn.", "topic": TOPIC, "segment": TITLE,
    "command": "Read my CHANGE-BRIEF.md and godot/tests/check_props.gd. Before you change anything, predict what the check will print if spikes.glb "
               "is exported with its origin at the centre of the wooden block instead of the centre of its underside. Then make that change on a copy, "
               "re-export, and show me the check's output before and after.",
    "runningText": "paste this into your own Claude session…", "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"}}}})
B.append({"beat_id": "BOUT", "act": "outro", "components": [], "kind": "outro_voice",
  "role_note": "OUTRO-LOCK: exact title, @NikBearBrown, slug-seeded mascot, no subline; spoken, never scored; 1.0 s tail.",
  "narration_text": f"{TITLE} At Nik Bear Brown.", "tail_s": 1.0,
  "shot": {"type": "REMOTION", "lane": "bookend", "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG}}}})

for b in B:
    b.setdefault("voice", "am_onyx")
    b.setdefault("engine", "kokoro")

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "register": "Teardown",
    "audience": "Claude", "brand": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "engine": "kokoro",
    "voice_kokoro": "am_onyx", "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "greeting": "Jambo, Liam",
    "folderLabel": "@NikBearBrown", "in_for_bear": True, "aspect_ratio": "16:9", "fps": 30,
    "skill": "godot-gamedev (walker modifier)", "student": "shuai-z",
    "game": {"name": "walker-rudy (assignment-3 props)", "revision": "f6f8acf09b1c8e737caa1de08db60f61e28c2a2e", "short_revision": REV,
             "engine": "4.7.2.stable.official.ed1daf0bf", "folder": "assignment-3/godot"}},
    "beats": B}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
print(f"wrote beat_sheet.json: {len(B)} beats")
