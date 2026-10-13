#!/usr/bin/env python3
"""make_lanes_act5.py — writes ../../lanes/act5.json (Act V part 1, beats B45–B58).

The Claude Code beats (B48, B49, B50, B51, B54) are Remotion `CCSession` scenes whose blocks are REAL events from
examples/03-blender-mcp-to-godot/transcripts/run1-claude.jsonl (line numbers in SESSION-act5.md). Block cues are frames at 30 fps
(Remotion runs at 30 fps, not Manim's 24), computed from the measured audio in beat_sheet.json by the same character-share rule the
Manim scenes use (`until`): time of a phrase = duration * index(phrase) / len(narration). Entries are then nudged so that NO block
enters or types inside the 45-55% window GATE T / Gate V sample (a block's spring needs ~24 frames, so its interval [cue, cue+24]
must not overlap the window).

Run:  python3 evidence/act5/make_lanes_act5.py        (re-run after any re-voicing; it reads ../../beat_sheet.json)
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REEL = HERE.parent.parent
SHEET = {b["beat_id"]: b for b in json.loads((REEL / "beat_sheet.json").read_text())["beats"]}
FPS = 30
TITLE = "walker-3d-platformer-asset"          # the real session's working directory (transcript init event)


def dur(bid):
    return float(SHEET[bid]["actual_duration_s"])


def window(bid):
    t = dur(bid)
    return 0.45 * t * FPS, 0.55 * t * FPS


def cue(bid, seconds, span=26):
    """seconds -> frame, nudged so [frame, frame+span] stays out of the 45-55% window."""
    f = int(round(seconds * FPS))
    lo, hi = window(bid)
    if f + span > lo and f < hi:                      # overlaps the sampled window
        f = int(hi + 2) if (f + span / 2.0) > (lo + hi) / 2.0 else int(lo - span - 2)
    return max(0, f)


def check_text(rows, limit=44):
    for r in rows:
        assert len(r) <= limit, (len(r), r)


def tool(name, arg, state="done", cue_s=0):
    return {"type": "tool", "name": name, "arg": arg, "state": state}


def text(s):
    check_text([s])
    return {"type": "text", "text": s}


def session(bid, blocks_with_times, mode="accept-edits", mascot="off"):
    blocks, cues = [], []
    for blk, t in blocks_with_times:
        if blk["type"] == "prompt":
            blk = dict(blk)
            blk["cue"] = cue(bid, t, span=blk["typeDuration"] + 6)
            blocks.append(blk); cues.append(blk["cue"])
        else:
            blocks.append(blk); cues.append(cue(bid, t))
    # block heights (kit's estimateBlockHeight) must fit the 836 px body
    h = 0
    for b in blocks:
        h += {"text": 68, "prompt": 88, "status": 80}.get(b["type"], 0)
        if b["type"] == "tool":
            h += 68 + 60 * len(b.get("children") or [])
        if b["type"] == "diff":
            h += 56 + 48 + 56 * len(b["lines"])
    assert h <= 820, (bid, h)
    return {"title": TITLE, "mode": mode, "blocks": blocks, "cues": cues, "mascot": mascot, "durationSeconds": "__AUDIO__"}, h


L = {}

# ───────────────────────────────────────────────── B45 ─────────────────────────────────────────────────
L["B45"] = {
    "lane": "manim", "class": "B45_TheJob",
    "visual_intent": "The act title, then the REAL Blender render of the post (Blender 5.1.2 Workbench, re-rendered at 2x from the first agent's own script) on a ghost floor tile. Dimension marks are placed on the real pixels through the camera projection of the script's 3-D points: 0.6 m on both front base edges, a leader to the base's 0.1 m edge, a top-down octagon on a leader to the pole ('8 sides'), and a 1.8 m arrow from floor to pole top.",
    "motion_claim": "Each number is drawn on the post at the word that names it: 0.6 m, 0.1 m, eight sides, 1.8 m.",
    "show": [{"at": 0.15, "event": "post fades in on the floor tile"}, {"at": 0.32, "event": "0.6 m arrows on both base edges"},
             {"at": 0.45, "event": "0.1 m leader to the base edge"}, {"at": 0.65, "event": "octagon + leader: 8 sides"}, {"at": 0.82, "event": "1.8 m arrow"}],
    "runner_up": "Real Blender window screenshot (pantry/blender_window.png) with its Outliner",
    "why": "The job is a SIZE specification: marks on the real render show which edge each number measures; the window screenshot shows the object list, not the measurements.",
    "sparse": True}

L["B46"] = {
    "lane": "manim", "class": "B46_PennantMaterialsCollider",
    "visual_intent": "Same render, same camera. The base/pole marks leave; 0.4 m and 0.25 m arrows appear on the pennant; a terracotta dot marks where it hangs; two swatch tags (PostMetal, FlagCloth) are led to pole and pennant; then the run-1 collision BOX (real render, ghosted, with its 12 edges) appears as a SEPARATE object beside the post, labelled 'collider' and 'base + pole'.",
    "motion_claim": "Pennant dimensions draw, the two material tags land on the names, and the collider arrives as its own object, apart from the post.",
    "show": [{"at": 0.08, "event": "0.4 m arrow under the pennant"}, {"at": 0.21, "event": "0.25 m arrow"}, {"at": 0.31, "event": "dot where it hangs"},
             {"at": 0.51, "event": "PostMetal tag"}, {"at": 0.58, "event": "FlagCloth tag"}, {"at": 0.66, "event": "collider box"}],
    "runner_up": "Blender window screenshot: the Outliner lists Base, Pennant, Pole and Collision-convcolonly as separate objects",
    "why": "The request is four measurable features plus a separate collider; drawing the collider apart from the post says 'separate' without showing the box overlapping the pennant, which is the later finding.",
    "sparse": True}

L["B47A"] = {
    "lane": "manim", "class": "B47A_ThreePredictions",
    "visual_intent": "A 2x2 prediction board that fills as each question is asked. Cell 1: the real post thumbnail with '1.8 m' and an X/Y/Z triad with '?'. Cell 2: three outlined X/Y/Z cells holding '?' under 'Y up off'. Cell 3: a luggage-style scale tag reading 'scale ? ? ?' under 'never applied'.",
    "motion_claim": "Each question's own drawing appears as it is asked: axes for the axis question, three empty cells for the bounding box, a tag for the scale.",
    "show": [{"at": 0.17, "event": "cell 1 draws: post, 1.8 m, axes, ?"}, {"at": 0.41, "event": "cell 2 draws: X Y Z cells"}, {"at": 0.69, "event": "cell 3 draws: scale tag"}],
    "runner_up": "ShowTellCard 'stack' (options fanned, one chosen)",
    "why": "Predict-before-reveal needs a place for the answers to go later; the board holds the questions without answering them, and each cue is a drawing, not a sentence.",
    "sparse": True}

L["B47B"] = {
    "lane": "manim", "class": "B47B_FourthPrediction",
    "visual_intent": "The first three cells stand as left by B47A; cell 4 draws: a page icon ('import'), an arrow, the ghosted collider box and its name '-convcolonly' in Menlo, and '?'.",
    "motion_claim": "The fourth question lands on the same board: copy this import file, what happens to a collider with this name?",
    "show": [{"at": 0.08, "event": "cell 4 frame + import page"}, {"at": 0.41, "event": "collider named -convcolonly"}, {"at": 0.85, "event": "arrow + ?"}],
    "runner_up": "FormBCard with four icons",
    "why": "Continuity: the fourth question belongs to the board the viewer has just watched fill; a new card would hide that all four are made before anything runs.",
    "sparse": True}

# ───────────────────────────────────────────────── B48 ─────────────────────────────────────────────────
b48, h48 = session("B48", [
    ({"type": "prompt", "text": "Task: build one small low-poly prop in Blender", "typeDuration": 48}, 0.3),
    (text("… One bounded change: do not edit any"), 2.0),
    (text("existing script, the player, …"), 2.4),
    (text("… Run it only in background mode (-b"), 3.7),
    (text("--factory-startup --python <script>)."), 4.2),
    (text("Never open its window."), 4.9),
    (text("… export godot/props/checkpoint_post.glb"), 7.2),
    (text("(binary glTF, +Y up, apply modifiers)."), 7.7),
    (text("… 4. Place one instance of the imported"), 8.8),
    (text("scene in game.tscn, standing on the floor"), 9.3),
    (text("5. Write godot/tests/test_checkpoint_post.gd"), 9.9),
])
L["B48"] = {
    "lane": "remotion", "pattern": "CCSession", "props": b48,
    "visual_intent": "Claude Code's own window (library skin, 'accept edits on' footer = the real --permission-mode acceptEdits): the first line of the real Prompt 1 types into the input band, then excerpt rows of the same prompt land in prompt order, each ellipsis marking what is skipped: the one-bounded-change sentence, the background-only / never-open-the-window rule, and the export, place and test steps.",
    "motion_claim": "The prompt types in and its rows land in order; the rule 'never open its window' arrives with the voice.",
    "show": [{"at": 0.02, "event": "'Task: build one small low-poly prop in Blender' types"}, {"at": 0.16, "event": "'One bounded change' rows"},
             {"at": 0.29, "event": "'Run it only in background mode … Never open its window.'"}, {"at": 0.56, "event": "export / place / write-the-test rows"}],
    "runner_up": "ClaudeComposerAsk (the claude.ai composer) holding the prompt",
    "why": "The prompt was given to Claude Code on the command line, so the tool is Claude Code, not the chat composer (SHOW-THE-THING rung 2: the library's faithful skin; text is the real prompt, excerpted with marked ellipses).",
    "sparse": False}

# ───────────────────────────────────────────────── B49 ─────────────────────────────────────────────────
b49, h49 = session("B49", [
    (tool("Read", "AGENTS.md"), 0.4),
    (tool("Read", "godot/enemy/enemy.glb.import"), 3.3),
    (text("Now write the pre-configured import file so"), 4.1),
    (text("Godot uses use_name_suffixes=true:"), 4.5),
    (tool("Write", "godot/props/checkpoint_post.glb.import"), 5.0),
    ({"type": "diff", "file": "godot/props/checkpoint_post.glb.import", "addCount": 44, "delCount": 0, "lines": [
        {"gutter": "22", "text": "nodes/use_name_suffixes=true", "kind": "add"},
        {"gutter": "23", "text": "nodes/use_node_type_suffixes=false", "kind": "add"}]}, 5.4),
    (tool("Bash", "godot --headless --path godot --import …"), 9.6),
])
L["B49"] = {
    "lane": "remotion", "pattern": "CCSession", "props": b49,
    "visual_intent": "Claude Code's window replaying the first agent's real first moves: Read AGENTS.md, Read godot/enemy/enemy.glb.import, its own sentence about the pre-configured import file, Write godot/props/checkpoint_post.glb.import, the lines it wrote (use_name_suffixes=true, use_node_type_suffixes=false), then the first Godot import.",
    "motion_claim": "The two import-setting lines land in the written file; the second one is the one that turns the collider off.",
    "show": [{"at": 0.03, "event": "Read AGENTS.md"}, {"at": 0.24, "event": "Read the enemy's import file"}, {"at": 0.37, "event": "Write the new import file"},
             {"at": 0.40, "event": "the two suffix lines"}, {"at": 0.62, "event": "first Godot import"}],
    "runner_up": "Manim side-by-side of the enemy's import file and the agent's",
    "why": "It is a recorded tool call with real arguments and real file content; the skin shows the order the agent did things in, which the side-by-side would reorder.",
    "sparse": False}

# ───────────────────────────────────────────────── B50 ─────────────────────────────────────────────────
b50, h50 = session("B50", [
    (text("ValueError: faces.new(...):"), 0.5),
    (text("face already exists"), 0.9),
    ({"type": "diff", "file": "tools/blender/build_checkpoint_post.py", "addCount": 1, "delCount": 2, "lines": [
        {"gutter": "-", "text": "bm.faces.new(pv[::-1])     # back  face (normal −Y)", "kind": "del"},
        {"gutter": "+", "text": "bm.faces.new(pv)           # single face; …", "kind": "add"}]}, 3.1),
    (tool("Read", "tools/blender/build_checkpoint_post.log"), 6.9),
    (text("Base … scale=(1.000, 1.000, 1.000) …"), 7.9),
    (text("Pole … scale=(1.000, 1.000, 1.000) …"), 8.4),
    (text("Pennant … scale=(1.000, 1.000, 1.000) …"), 8.9),
    (text("Collision-convcolonly"), 9.4),
    (text("… scale=(1.000, 1.000, 1.000) …"), 9.7),
])
L["B50"] = {
    "lane": "remotion", "pattern": "CCSession", "props": b50,
    "visual_intent": "Claude Code's window: Blender's real traceback line (ValueError: faces.new(...): face already exists), the Edit that removes the second faces.new on the same four vertices, then Read of the Blender log with the scale of all four objects (each log line excerpted with marked ellipses; every scale 1.000).",
    "motion_claim": "The duplicate-face line is struck out in the diff; then four 'scale=(1.000, 1.000, 1.000)' rows land one per object.",
    "show": [{"at": 0.04, "event": "ValueError rows"}, {"at": 0.25, "event": "diff: the back-face line removed"}, {"at": 0.56, "event": "Read the log"},
             {"at": 0.65, "event": "four scale rows land"}],
    "runner_up": "CCPlainShell replaying the Blender log",
    "why": "Each Blender log line is ~110 characters; the plain shell would cut the scale off at 66 columns, so the session skin with marked excerpts keeps the number the voice names.",
    "sparse": False}

# ───────────────────────────────────────────────── B51 ─────────────────────────────────────────────────
b51, h51 = session("B51", [
    (tool("Bash", "godot --headless --path godot --script …"), 0.4),
    (text("FAIL at least one StaticBody3D present …"), 1.6),
    (tool("Bash", "godot --headless --path godot --script …"), 3.4),
    (text("MeshInstance3D [Collision-convcolonly]"), 4.6),
    (text("The GLB node name is correct"), 8.2),
    (text("(Collision-convcolonly), but Godot 4.7"), 8.6),
    (text("seems to check the mesh name too."), 9.0),
    (tool("Edit", "tools/blender/build_checkpoint_post.py"), 10.6),
    (tool("Bash", "/Applications/Blender.app/…/Blender -b …"), 11.2),
    (tool("Bash", "godot --headless --path godot --import …"), 12.0),
    (text("MeshInstance3D [Collision-convcolonly]"), 13.1),
])
L["B51"] = {
    "lane": "remotion", "pattern": "CCSession", "props": b51,
    "visual_intent": "Claude Code's window: the test's real 'FAIL at least one StaticBody3D present' line, the debug script's printed tree showing the collider as MeshInstance3D [Collision-convcolonly], the agent's own sentence ('...Godot 4.7 seems to check the mesh name too'), then Edit, rebuild, reimport, and the SAME tree line again.",
    "motion_claim": "The same MeshInstance3D line appears before and after the rename: nothing changed.",
    "show": [{"at": 0.03, "event": "test run"}, {"at": 0.11, "event": "FAIL line"}, {"at": 0.32, "event": "tree: MeshInstance3D"}, {"at": 0.56, "event": "the agent's sentence"},
             {"at": 0.73, "event": "Edit, rebuild, reimport"}, {"at": 0.9, "event": "the same tree line again"}],
    "runner_up": "Manim before/after trees",
    "why": "The point is a guess in the agent's own words, followed by a rerun that returned the identical line; the transcript order IS the argument, so the skin plays it back in order.",
    "sparse": False}

# ───────────────────────────────────────────────── B52 / B53 ─────────────────────────────────────────────────
L["B52"] = {
    "lane": "manim", "class": "B52_TurnLimit",
    "visual_intent": "The real debug script's three lines (6, 8 and 14 of debug_options.gd), the real Godot error under them, 'never reached' beside quit(0), a ring for the still-running Godot; then a timeline bar (61 turns, 21 min) with the turn-limit marker and nine terracotta dots for the nine refused commands.",
    "motion_claim": "The error line lands under the failing call; the bar grows to 61 turns and stops at the limit; nine dots land one by one.",
    "show": [{"at": 0.05, "event": "script lines 6 and 8"}, {"at": 0.13, "event": "dot at line 8 + the real SCRIPT ERROR"}, {"at": 0.23, "event": "quit(0), never reached"},
             {"at": 0.52, "event": "bar: 61 turns, 21 min"}, {"at": 0.73, "event": "turn limit"}, {"at": 0.78, "event": "nine refused"}],
    "runner_up": "Claude Code session skin with a running Bash tool",
    "why": "'61 turns, 21 minutes, nine refused' are totals from the result event, not things the session screen ever printed in a -p run; a drawn timeline can carry them honestly, the session skin cannot.",
    "sparse": True}

L["B53"] = {
    "lane": "manim", "class": "B53_Resumed",
    "visual_intent": "The same timeline continues: a 'hung' gap while the debug process ran, the real task_notification ('Background command \"Print available import options\" completed (exit code 0)') arrives at its end, and a second bar of 24 turns (12 min) follows.",
    "motion_claim": "The notification arrives at the end of the gap and the timeline starts again.",
    "show": [{"at": 0.18, "event": "hung gap"}, {"at": 0.43, "event": "task_notification text + arrow"}, {"at": 0.61, "event": "second bar grows"}, {"at": 0.85, "event": "24 turns"}],
    "runner_up": "Claude Code session skin: notification row + Read of the task output",
    "why": "Same figure as B52 (ONE CAST PER ACT) so 21 + 8 + 12 minutes read as one session; the gap length is computed from the recorded start/stop times.",
    "sparse": True}

# ───────────────────────────────────────────────── B54 ─────────────────────────────────────────────────
b54, h54 = session("B54", [
    ({"type": "diff", "file": "godot/props/checkpoint_post.glb.import", "addCount": 1, "delCount": 1, "lines": [
        {"gutter": "25", "text": "nodes/use_node_type_suffixes=false", "kind": "del"},
        {"gutter": "25", "text": "nodes/use_node_type_suffixes=true", "kind": "add"}]}, 1.5),
    ({"type": "diff", "file": "godot/props/checkpoint_post.glb.import", "addCount": 7, "delCount": 1, "lines": [
        {"gutter": "42", "text": "_subresources={}", "kind": "del"},
        {"gutter": "42", "text": '"nodes/Collision-convcolonly": {', "kind": "add"},
        {"gutter": "43", "text": '"generate/physics": true,', "kind": "add"}]}, 3.4),
    (tool("Bash", "godot --headless --path godot --script …"), 6.7),
    (text("StaticBody3D [Collision]"), 7.4),
    (text("CollisionShape3D [CollisionShape3D]"), 7.9),
    (text("shape=ConvexPolygonShape3D"), 8.4),
])
L["B54"] = {
    "lane": "remotion", "pattern": "CCSession", "props": b54,
    "visual_intent": "Claude Code's window: two Edits to the same import file, one flipping use_node_type_suffixes from false to true, one replacing _subresources={} with a block that asks Godot to generate physics for Collision-convcolonly; then the debug tree finally printing StaticBody3D [Collision] and a CollisionShape3D with ConvexPolygonShape3D.",
    "motion_claim": "Two diffs land back to back; the collider appears only after both are in.",
    "show": [{"at": 0.13, "event": "diff 1: node type suffixes true"}, {"at": 0.29, "event": "diff 2: the physics block"}, {"at": 0.57, "event": "tree run"}, {"at": 0.63, "event": "StaticBody3D appears"}],
    "runner_up": "Manim two-change ledger",
    "why": "'Two changes at once' is visible as two consecutive Update diffs in the session itself; the skin's own diff block shows exactly what a reader of the session would have seen.",
    "sparse": False}

# ───────────────────────────────────────────────── B55 ─────────────────────────────────────────────────
L["B55"] = {
    "lane": "manim", "class": "B55_Compacted",
    "visual_intent": "A context gauge falls from 172390 to 10266 tokens (the compact_boundary numbers); the working 'godot --headless … --import' command is struck from memory; seven identical rows '/Applications/Godot.app/…/Godot' each get an X; the agent's final plea 'Please approve the Godot command'; test_checkpoint_post.gd never ran.",
    "motion_claim": "The gauge empties, then the same refused path lands seven times, then the test is left unrun.",
    "show": [{"at": 0.07, "event": "gauge shrinks 172390 to 10266"}, {"at": 0.2, "event": "the command that used to work"}, {"at": 0.47, "event": "seven refused path rows"},
             {"at": 0.68, "event": "please approve"}, {"at": 0.86, "event": "test never ran"}],
    "runner_up": "Claude Code session skin: seven stacked Bash rows",
    "why": "Compaction is a quantity falling (172390 to 10266) and the failure is a count of identical refusals; the skin has no state for 'refused', so a drawn tally is more honest than seven green ticks.",
    "sparse": True}

# ───────────────────────────────────────────────── B56–B58 ─────────────────────────────────────────────────
L["B56"] = {
    "lane": "manim", "class": "B56_OurOwnRun",
    "visual_intent": "A grid of 15 ticks (one per PASS line of the finished test's real log) and the log's own 'Failures: 0'; then the collider box alone, 'fresh import', the two real default settings (nodes/use_name_suffixes=true, nodes/use_node_type_suffixes=true) and leaders to StaticBody3D and ConvexPolygonShape3D.",
    "motion_claim": "Ticks fill the grid; the two defaults land; the box is named as a body with a convex shape.",
    "show": [{"at": 0.1, "event": "ticks fill"}, {"at": 0.26, "event": "grid leaves"}, {"at": 0.44, "event": "box + 'fresh import'"}, {"at": 0.67, "event": "two defaults"}, {"at": 0.81, "event": "StaticBody3D"}, {"at": 0.94, "event": "ConvexPolygonShape3D"}],
    "runner_up": "CCPlainShell with the log and the probe output",
    "why": "Fifteen PASS lines do not fit a 14-line shell and the probe's lines are 87 characters; ticks carry the count and Menlo carries the two settings and the two class names verbatim.",
    "sparse": True}

L["B57"] = {
    "lane": "manim", "class": "B57_SuffixAlone",
    "visual_intent": "A toggle for use_node_type_suffixes flips off; a reimport arrow; the ghosted collider is replaced by the REAL Blender render of what stands there when the collider stays a mesh (an opaque grey box around the post, pennant poking out) with a no-entry sign and 'no collision'; a ring round the toggle row ('enough') and a crossed-off '_subresources' ('redundant').",
    "motion_claim": "One toggle flips and the invisible collider becomes a visible, solid-looking box that nothing can hit.",
    "show": [{"at": 0.0, "event": "toggle flips off"}, {"at": 0.19, "event": "reimport arrow"}, {"at": 0.38, "event": "ghost becomes opaque box"}, {"at": 0.51, "event": "no collision sign"},
             {"at": 0.62, "event": "ring: enough"}, {"at": 0.79, "event": "_subresources"}, {"at": 0.94, "event": "crossed off"}],
    "runner_up": "ShowTellCard 'tabs' (before/after panels)",
    "why": "A setting flipping and a box changing from ghost to solid IS the claim; the opaque render is the same geometry from the same camera, so the box is visibly where the post was.",
    "sparse": True}

L["B58"] = {
    "lane": "manim", "class": "B58_RayThroughNothing",
    "visual_intent": "The real post render floats 15.8 cm above a ghost floor (the gap measured with the render's own camera), a ray is drawn down the pole's axis through the missing collider to a terracotta hit dot on the floor, the real log pieces 'ray hit at y=-4.0000' and 'post base y=-3.8419' are led to the dot and the base, and the post sinks onto the floor with its label changing to 'post base y=-4.0'.",
    "motion_claim": "The ray passes through the post and lands on the floor; the post is then lowered by the size of the gap.",
    "show": [{"at": 0.18, "event": "post appears floating"}, {"at": 0.34, "event": "16 cm gap"}, {"at": 0.5, "event": "ray down the axis"}, {"at": 0.6, "event": "no collider"},
             {"at": 0.79, "event": "log pieces"}, {"at": 0.87, "event": "post moves down"}],
    "runner_up": "Manim side view of two rays (finished-test ray included)",
    "why": "The first run's ray is the only ray in this beat's narration; the finished test's ray is drawn in the next beat on this same layout (B58_X0 / B58_YF / B58_S in scenes_act5.py).",
    "sparse": True}

(REEL / "lanes" / "act5.json").write_text(json.dumps(L, indent=1, ensure_ascii=False) + "\n")
print("wrote lanes/act5.json:", ", ".join(L))
for k, h in (("B48", h48), ("B49", h49), ("B50", h50), ("B51", h51), ("B54", h54)):
    print(f"  {k}: session block stack {h}px of 836")
