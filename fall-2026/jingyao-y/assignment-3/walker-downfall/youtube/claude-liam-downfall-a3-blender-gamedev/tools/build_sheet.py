"""Write beat_sheet.json for the Downfall Assignment 3 (Blender assets) gamedev film.

Run from the reel folder:  python tools/build_sheet.py <snapshot-of-ceada15>
Code excerpts are read verbatim from the snapshot clone, so displayed code
always equals the hashed source the evidence ledger records.
"""
import json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
SNAP = Path(sys.argv[1])
REV = "ceada15"
TITLE = "Downfall: First Blender Assets for the Terraces"
SLUG = "claude-liam-downfall-a3-blender-gamedev"
TOPIC = "GODOT GAMEDEV · DOWNFALL · BLENDER MCP"


def lines(path, a, b):
    text = (SNAP / path).read_text(encoding="utf-8").splitlines()
    return "\n".join(text[a - 1:b])


EXCERPTS = {
    "B03": ("world/continuous_world_map.gd", 61, 66),
    "B05": ("tools/blender/build_cliff_wall_segment.py", 95, 107),
    "B07": ("tools/blender/build_arched_ramp_segment.py", 47, 51),
    "B09": ("tools/blender/build_arched_ramp_segment.py", 192, 196),
    "B11": ("tools/blender/export_glb.py", 24, 33),
    "B13": ("tests/test_a3_assets.gd", 114, 121),
    "B15": ("art/models/asset_preview.tscn", 33, 35),
}


def say(bid, act, text, shot, **extra):
    beat = {"beat_id": bid, "act": act, "narration_text": text, "voice": "am_onyx", "engine": "kokoro",
            "estimated_duration_s": max(6, round(len(text.split()) / 2.5)), "shot": shot}
    beat.update(extra)
    return beat


def workbench(bid, title, notes, cues, note_label="Source notes — not Inspector values"):
    path, a, b = EXCERPTS[bid]
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": "code-highlight",
            "label": "Godot editor reconstruction",
            "show": [{"at": "0.0", "event": f"Godot editor reconstruction: {path} lines {a}-{b}, revision {REV}"}],
            "remotion": {"pattern": "GodotDevWorkbench", "props": {
                "mode": "code", "title": title, "project": "downfall-godot",
                "path": f"res://{path}", "source": f"Godot editor reconstruction · {path}:{a}-{b} · commit {REV}",
                "code": lines(path, a, b), "startLine": a, "codeFontSize": 27 if b - a < 8 else 24,
                "inspectorLabel": note_label, "notes": notes, "cues": cues}}}


def media(bid, label, events, source="image"):
    return {"type": "GAMEPLAY" if source == "capture" else "GRAPHIC", "class": "SHOW", "source": source,
            "label": label, "evidence_media": f"media/{bid}.mp4",
            "show": [{"at": str(t), "event": e} for t, e in events]}


def graphic(pattern, props, events, motion="type-on"):
    return {"type": "GRAPHIC", "class": "SHOW", "source": "remotion", "motion": motion,
            "show": [{"at": str(t), "event": e} for t, e in events],
            "remotion": {"pattern": pattern, "props": props}}


LABEL_BOX = [{"label": "burned-label", "box": [0.065, 0.91, 0.35, 0.945]}]
QC_ENGINE = {"full_bleed": True,
             "full_bleed_reason": "Real engine output (Godot render or Blender look view) shown edge to edge.",
             "contrast_regions": LABEL_BOX,
             "contrast_reason": "The engine image is a dark scene by design; the only overlay text is the burned provenance label, sampled here."}

beats = [
    say("B00", "ASK",
        "Hola. Liam, in for Bear. This is a reconstructed ask, not a transcript. A student wanted Walker to take the design "
        "for Downfall's new terraced field maps and turn it into the game's first three Blender assets, built through "
        "Blender MCP and checked inside Godot.",
        graphic("ClaudeComposerAsk", {
            "greeting": "Hola, Liam", "topic": TOPIC, "segment": "Please Use Walker",
            "command": "Please use Walker to convert my game design document about Downfall's terraced field maps into "
                       "three Blender assets: a cliff wall segment, an arched ramp segment and a cliff rubble pile, "
                       "built through Blender MCP and checked in Godot.",
            "runningText": "reading continuous_world_map.gd…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
            "effortLabel": "High",
            "output": ["Reconstructed prompt - illustrative, not a transcript.",
                       "Blender 5.4 Alpha + mcp-for-blender.",
                       "No asset libraries, no 3D generators."]},
            [(0.02, "composer card fades in"), (0.28, "the Walker ask types"), (0.78, "result lines land")])),
    say("B01", "BLUF",
        "Here's the honest version. Claude built all three assets by sending Python to Blender through MCP, one call per "
        "part, and every call is kept in the repo. The author made the design calls, learned the viewport, moved two kerbs "
        "by hand, and gave the final look. One difference up front: this was Blender five point four alpha, not the "
        "course's five point one.",
        graphic("BrutalistHesitantWriter", {
            "text": "Built in the course Blender.\nThree assets, through MCP.\nOne edit by hand.\nChecked in Godot.",
            "triggerWords": "course", "replacementWords": "5.4 Alpha",
            "fontSize": 128, "lineSpacing": 2.1, "align": "center", "seed": "2026", "charMs": 8, "mistakeRate": 2,
            "hesitateWithin": 0, "hesitateBetween": 1, "durationSeconds": 22},
            [(0.15, "'Built in the course Blender' types and pauses"), (0.4, "'course' struck through, corrected to '5.4 Alpha'")],
            motion="type-on-correct"), lead_silence_s=0.8),
    say("B02", "SETUP",
        "The assignment: three game assets, each in its own Blender file. At most six primitives and under five hundred "
        "triangles each, flat colours only, no sculpting, textures, rigging or animation, modelled around the origin with "
        "the bottom on the ground. Downfall's field maps had just become terraces, so these three dress them: a cliff wall, "
        "a ramp, and the rubble at a cliff's foot.",
        media("B02", "Assignment limits + real Godot capture (map seed 1729, isolated clone)",
              [(0.0, "assignment limits beside the terraced mine floor")]),
        qc=QC_ENGINE),
    say("B03", "MECHANISM",
        "Every size starts in the game's map generator. A terrace level is two point two metres. A ramp needs at least "
        "six point five metres of run per level, which is under nineteen degrees, plus two flat metres at each end. And "
        "a corridor's half-width is rolled between three point four and five point six, so the narrowest corridor is six "
        "point eight wide.",
        workbench("B03", "The terraces set every size",
                  [{"label": "Line 175", "value": "_corridor_width(): half-width 3.4–5.6"},
                   {"label": "Slope", "value": "atan(2.2 / 6.5) = 18.7°"}],
                  [{"at": 0.5, "line": 61, "label": "one level: 2.2 m"}, {"at": 5.0, "line": 65, "label": "run per level"},
                   {"at": 11.0, "line": 66, "label": "flat apron"}])),
    say("B04", "RESULT",
        "Here is that in the running game. On the mine floor with map seed seventeen twenty-nine, she stands at a ramp's "
        "foot. On seed thirteen thirty-three, she stands below a cliff between two terraces. The terrain mesh already gives "
        "every ramp and cliff its shape and its collision, which is how Grim Dawn's editor works too. So these assets are "
        "dressing, laid on top.",
        media("B04", "Real Godot capture · teleported into place (test shortcut) · isolated clone of ceada15",
              [(0.0, "ramp foot, game camera (seed 1729)"), (0.5, "below a cliff between terraces (seed 1333)")], source="capture"),
        qc=QC_ENGINE),
    say("B05", "MECHANISM",
        "The cliff segment is three stacked boxes and one icosphere: one terrace tall, plus a tenth of a metre above and "
        "below, and only point three in front of the face. This is the sixth call. After the first look, the boulder on "
        "top was mostly buried and read as a flat disc. This call makes it half a metre tall and moves it onto the front "
        "lip, still peaking at two point four.",
        workbench("B05", "A fix after looking",
                  [{"label": "Before", "value": "0.35 tall, centred on the top stratum: 0.2 buried"},
                   {"label": "Cliff", "value": "116 triangles · 4 primitives"}],
                  [{"at": 0.5, "line": 96, "label": "why: read as a disc"}, {"at": 9.0, "line": 102, "label": "0.5 tall"},
                   {"at": 15.0, "line": 107, "label": "front lip, peak 2.4"}])),
    say("B06", "RESULT",
        "Claude's look views, before and after: front, right, top, and three-quarter. Before, a thin disc on the top "
        "stratum. After, the boulder bulges out of the face. The rubble pile had the same kind of miss. Its top stone "
        "floated, and the next call sank it into the stone below.",
        media("B06", "Blender look views · captured by Claude through MCP",
              [(0.0, "cliff before and after"), (0.6, "rubble before and after")]),
        qc=QC_ENGINE),
    say("B07", "MECHANISM",
        "The ramp is one plane, edited into a solid wedge, plus two kerbs. Its top follows this function: the slope, two "
        "point two over six point five, plus two centimetres so it never fights the terrain, plus a ten-centimetre crown on "
        "the centre line. The crown fades to nothing over the first and last half metre, so neither end has a lip.",
        workbench("B07", "The crown is one function",
                  [{"label": "Ramp", "value": "68 triangles · 3 primitives"},
                   {"label": "Clearance", "value": "+0.02 above the slope plane"}],
                  [{"at": 0.5, "line": 47, "label": "rise, run, crown"}, {"at": 7.0, "line": 50, "label": "fade over 0.5 m"},
                   {"at": 12.0, "line": 51, "label": "slope + 0.02 + crown"}])),
    say("B08", "RESULT",
        "The result: an edge slope of eighteen point seven degrees, and a crown of exactly point one, half a metre in. One "
        "honest observation: in Blender's solid shading the crown is barely visible, and from the game's camera it isn't "
        "visible at all.",
        media("B08", "Blender look views · captured by Claude through MCP",
              [(0.0, "ramp: front, right, three-quarter, low front")]),
        qc=QC_ENGINE),
    say("B09", "MECHANISM",
        "One change was made by hand. The author opened the ramp in Blender and moved each kerb a tenth of a metre outward. "
        "The reason: the corridor's rock bank starts at three point four, so a kerb that ends exactly there leaves a seam. "
        "This comment records the steps Claude gave. The author's own report was just: all done.",
        workbench("B09", "The author's edit, by hand",
                  [{"label": "By", "value": "the author, mouse and keyboard in Blender"},
                   {"label": "Steps Claude gave", "value": "Tab · Alt+A · L · G X 0.1 · Ctrl+S (author reported: all done)"}],
                  [{"at": 0.5, "line": 192, "label": "not code"}, {"at": 5.0, "line": 194, "label": "0.1 m outward"},
                   {"at": 12.0, "line": 195, "label": "6.8 → 7.0"}])),
    say("B10", "RESULT",
        "Claude then read the file back without changing it. The left kerb now spans minus three point five to minus three "
        "point two, the road is unchanged, and the right kerb mirrors it. The overall width is seven metres. The file was "
        "saved, and Blender wrote a backup file, which git now ignores.",
        media("B10", "Recorded MCP output · get_scene_info and a read-only check",
              [(0.0, "recorded output lines")])),
    say("B11", "MECHANISM",
        "Export is headless: one script run per file, glTF binary, Y up, the mesh only. Blender's plus Y becomes Godot's "
        "minus Z. So the ramp should climb away from its origin towards minus Z, and the cliff's face should look towards "
        "plus Z.",
        workbench("B11", "Blender +Y becomes Godot −Z",
                  [{"label": "Run", "value": "blender -b <asset>.blend --python export_glb.py"},
                   {"label": "Out", "value": "art/models/<asset>.glb"}],
                  [{"at": 0.5, "line": 26, "label": "glTF binary"}, {"at": 4.0, "line": 28, "label": "Y up"},
                   {"at": 8.0, "line": 30, "label": "mesh only"}])),
    say("B12", "RESULT",
        "And in Godot: a moment through the game's own camera, then one full orbit, front, side and behind. The blue capsule "
        "is one point seven metres, for scale. Note that the game camera looks from minus Z, so by default the cliff's "
        "face points away from it. Placing cliffs on the map will need a rotation per cliff line.",
        media("B12", "Real Godot render · Movie Maker · isolated clone of ceada15",
              [(0.0, "game camera"), (0.15, "orbit begins at the cliff's face"), (0.9, "orbit completes")], source="capture"),
        qc=QC_ENGINE),
    say("B13", "MECHANISM",
        "The headless check reads the imported meshes back. This part finds the ramp's highest vertices and requires them "
        "past minus six on Z. Other checks compare each bounding box with the brief to two centimetres, plus every node's "
        "transform, the triangle counts and the colours.",
        workbench("B13", "Reading the import back",
                  [{"label": "Suite", "value": "test_a3_assets.gd · 25 checks"},
                   {"label": "Tolerance", "value": "±0.02 m"}],
                  [{"at": 0.5, "line": 114, "label": "F1 and F4"}, {"at": 5.0, "line": 117, "label": "highest vertices"},
                   {"at": 9.0, "line": 120, "label": "past −6 on Z"}])),
    say("B14", "RESULT",
        "On a fresh copy of the commit, all twenty-five checks pass. That proves Blender, the glTF file and Godot agree. It "
        "does not prove the assets look right, or that they fit the generated terrain. Nor does it prove the normals face "
        "out: the exporter marked the materials double-sided, so Godot never hides a back face.",
        media("B14", "Recorded test output · fresh copy of ceada15",
              [(0.0, "recorded PASS lines and RESULT")])),
    say("B15", "MECHANISM",
        "One bug was in Claude's preview scene, not in the assets. In a Godot scene file, a transform's basis is written "
        "row by row. Claude wrote the sun's basis column by column. This is the corrected line.",
        workbench("B15", "Rows, not columns",
                  [{"label": "First written", "value": "columns → light pointed upward"},
                   {"label": "Corrected", "value": "transposed (ceada15)"}],
                  [{"at": 0.5, "line": 33, "label": "the sun"}, {"at": 3.0, "line": 34, "label": "basis by rows"}])),
    say("B16", "RESULT",
        "Re-rendered with the basis as first written, the light points up. The stone tops go black and their sides glow, "
        "and it looks like flipped normals. Claude counted inward faces in Blender first, found none, and then found the "
        "transpose. With the corrected line, the tops catch the light and the shadows fall on the ground.",
        media("B16", "Real Godot render · re-rendered with the first sun basis, then the corrected one",
              [(0.0, "lit from below"), (0.5, "corrected")], source="capture"),
        qc=QC_ENGINE),
    say("B17", "HUMAN",
        "The human parts. The author learned the viewport and took this screenshot, with scene statistics on after a "
        "second try. The author also moved the kerbs, and at the end checked the assets in the Godot editor. The whole "
        "report was: everything is correct. That is recorded as given, with nothing added.",
        media("B17", "Screenshot taken by the author · Blender 5.4 Alpha, Chinese UI",
              [(0.0, "the author's screenshot"), (0.7, "the author's report")]),
        qc=QC_ENGINE),
    say("B18", "VERDICT",
        "Verdict. Working: three assets at a hundred and sixteen, sixty-eight and a hundred and eighty triangles, sized from "
        "the game's own numbers, with twenty-five checks passing. Found and fixed: a buried boulder, a floating stone, Godot "
        "trying to import the Blender files, and an upside-down sun. Still open: none of this is placed on a real map yet, "
        "the cliff faces away from the game camera, and the human check was one line.",
        graphic("ClaudeVerdictArtifact", {
            "artifactTitle": "Verdict", "artifactHeading": f"downfall-godot · {REV}", "brandLabel": "@NikBearBrown",
            "artifactLines": [
                "Working: cliff 116 · ramp 68 · rubble 180 triangles; sized from TIER, RAMP_RUN, half-width; 25/25 checks.",
                "Fixed: buried boulder · floating stone · .blend auto-import (.gdignore) · sun basis rows vs columns.",
                "Open: not placed by the map generator · cliff face points away from the game camera · ramp crown unreadable.",
                "Human: author's kerb edit verified; human check reported in one line, recorded as given."]},
            [(0.2, "line 1"), (0.4, "line 2"), (0.6, "line 3"), (0.8, "line 4")], motion="artifact-reveal")),
    say("B19", "HANDOFF",
        "Your turn. Paste this into Claude: 'Open one of my Blender files through MCP, change one dimension that my game's "
        "code depends on, export it, and add one Godot check that fails if the change breaks that number.' Before you run "
        "it, write down which check you expect to fail. Liam, in for Bear.",
        graphic("ClaudeComposerAsk", {
            "greeting": "Your turn.", "topic": TOPIC, "segment": "Break One Number",
            "command": "Open one of my Blender files through MCP, change one dimension that my game's code depends on, "
                       "export it, and add one Godot check that fails if the change breaks that number.",
            "runningText": "reading the game's constants…", "folderLabel": "@NikBearBrown", "modelLabel": "Claude",
            "effortLabel": "High", "output": ["Predict the failing check first.", "Then compare."], "animateTyping": True},
            [(0.02, "composer fades in"), (0.12, "prompt types"), (0.78, "running text")])),
    {"beat_id": "B20", "act": "OUTRO", "narration_text": "Liam, in for Bear.", "voice": "am_onyx", "engine": "kokoro",
     "estimated_duration_s": 7, "audio_policy": "silence",
     "shot": graphic("ClaudeTitleOutro", {"title": TITLE, "slug": SLUG}, [(0.0, "title card"), (0.45, "mascot"), (0.7, "jingle")], motion="mascot-title")},
]

sheet = {"metadata": {
    "title": TITLE, "slug": SLUG, "topic": TOPIC, "kind": "godot-gamedev", "mode": "walker",
    "playlist": "NikBearBrown", "brand": "claude-liam", "audience": "CSYE 7270 reviewers and Godot students",
    "register": "Teardown", "engine": "kokoro", "voice": "am_onyx", "voice_kokoro": "am_onyx",
    "palette": "claude", "style_preset": "claude", "ground": "#FAF9F5", "aspect_ratio": "16:9", "fit": "crop",
    "captions": False, "channel_title": "@NikBearBrown", "channel": "@NikBearBrown", "folderLabel": "@NikBearBrown",
    "greeting": "Hola, Liam", "persona": "Liam (in for Bear)", "presenter": "Liam (in for Bear)", "in_for_bear": True,
    "game": {"name": "downfall-godot", "engine_version": "Godot 4.7.2.stable.official.ed1daf0bf",
             "revision": REV, "repo": "https://github.com/coldfish432/GodotGame"},
    "note": "godot-gamedev, walker mode, Assignment 3. Engine media are native 3840x2160 Godot Movie Maker captures from an "
            "isolated clone of ceada15 (window override + MJPEG quality only); Blender views are Claude's MCP look images; "
            "B17 is the author's own screenshot. See CAPTURE.md.",
    "tags": ["Godot 4", "Blender", "Blender MCP", "godot-gamedev", "3D assets", "Kokoro", "Remotion", "Claude", "course assignment"]},
    "beats": beats}
(REEL / "beat_sheet.json").write_text(json.dumps(sheet, ensure_ascii=False, indent=1), encoding="utf-8")
print("beats", len(beats))
