"""Write gamedev-evidence.json (schema 1, code-then-result-v1) from the real files.

Hashes every authored file in the exported godot/ folder (minus .godot/ and .uid), reads excerpt text
straight from the files and checks it against the beat sheet, and hashes the result media actually shown.
Run: python -I scripts/make_evidence.py
"""
import hashlib
import json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "godot"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
beats = {b["beat_id"]: b for b in sheet["beats"]}
F = "assets/furniture/"

components = [
    {"id": "scene-placement", "files": ["base.tscn"], "beat_ids": ["B10", "B11", "B17"],
     "explanation": "The saved subway-base scene. Each asset is one instance of its imported .glb with an identity "
                    "basis (scale 1) at y = 0.25, the top of the 0.5 m floor slab; the tablet carries a tilt and sits "
                    "at y 0.664 as a display placement. Two cameras (preview_camera, a3_asset_camera) and three "
                    "omni lights; no scripts."},
    {"id": "asset-chair", "files": [F + "chair.glb", F + "chair.glb.import"], "beat_ids": ["B06", "B11", "B13"],
     "explanation": "ENV-SEAT-02: the start-menu chair, 6 shapes, 72 triangles, 0.44 x 0.42 x 0.90 m, origin at the "
                    "bottom centre. Rebuilt headless (script route) from the 9-box v1; imported with default settings."},
    {"id": "asset-tablet", "files": ["assets/props/tablet.glb", "assets/props/tablet.glb.import"],
     "beat_ids": ["B04", "B05", "B13", "B18"],
     "explanation": "PROP-TABLET-02: the rugged military tablet, 21 bevelled boxes (over the course limit of 6 by the "
                    "designer's decision), 388 triangles, origin kept at the geometric centre (lowest y -0.081)."},
    {"id": "asset-crates", "files": [F + "crate_long.glb", F + "crate_long.glb.import",
                                     F + "crate_cube.glb", F + "crate_cube.glb.import"],
     "beat_ids": ["B07", "B09", "B14", "B15"],
     "explanation": "CRATE-LONG-03 and CRATE-CUBE-02: weapon crates on the 0.1 m grid (1.0 x 0.5 x 0.4 m and a 0.5 m "
                    "cube), 88 triangles each, lid origin on the back hinge, open / close animations (0 to -100 deg, "
                    "15 frames at 24 fps). The small crate carries the designer's hand edit (latches on the seam, "
                    "handles higher)."},
    {"id": "asset-desks", "files": [F + "computer_desk.glb", F + "computer_desk.glb.import",
                                    F + "computer_desk_l.glb", F + "computer_desk_l.glb.import"],
     "beat_ids": ["B11", "B17"],
     "explanation": "Extra project assets beyond the three: a 1.5 x 0.5 m computer desk and a 1.5 x 1.0 m L-shaped "
                    "desk, 6 shapes and 72 triangles each, on the 0.1 m grid."},
    {"id": "headless-check", "files": ["tests/a3_asset_check.gd"],
     "beat_ids": ["B12", "B13", "B14", "B15", "B16", "B17"],
     "explanation": "SceneTree script written by Claude: Part 1 loads each .glb and compares size, lowest point, node "
                    "scales and triangles with the brief, and plays the crate animations to their last frame; Part 2 "
                    "instantiates base.tscn and checks floor contact, the 0.1 m grid and pairwise overlaps. 55 PASS, "
                    "exit 0. It cannot judge appearance."},
]
roles = {"base.tscn": "saved scene (subway base with placed assets)",
         "tests/a3_asset_check.gd": "headless check script"}
for c in components:
    for f in c["files"]:
        roles.setdefault(f, "import settings sidecar" if f.endswith(".import") else "imported 3D asset (.glb)")

exclusions = {
    ".editorconfig": "Editor formatting defaults from the Godot project template; no runtime effect.",
    ".gitattributes": "Git line-ending rules from the project template; no runtime effect.",
    ".gitignore": "Git ignore rules from the project template; no runtime effect.",
    "icon.svg": "Default Godot project icon; not used by base.tscn.",
    "icon.svg.import": "Import sidecar for the default icon; default settings.",
    "project.godot": "Engine configuration (Forward Plus, Jolt Physics, D3D12, main scene base.tscn); named in the "
                     "film only as the engine setup, not explained as a component.",
    F + "test_chair.glb": "ENV-SEAT-TEST-01, the 2026-10-07 test chair export; no longer referenced by base.tscn "
                          "(replaced there by chair.glb). Shown only through its v1 viewport capture in B06.",
    F + "test_chair.glb.import": "Import sidecar of the unreferenced test chair.",
}

inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*")
             if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts)
             and p.suffix != ".uid")
files = []
for path in inv:
    if path in exclusions:
        continue
    ids = [c["id"] for c in components if path in c["files"]]
    files.append({"path": path, "sha256": sha(GAME / path), "role": roles[path], "component_ids": ids})

excerpts = []
for bid in ("B10", "B12", "B14", "B16"):
    props = beats[bid]["shot"]["remotion"]["props"]
    path = props["path"].split("  ")[0]
    start = props["startLine"]
    n = len(props["code"].split("\n"))
    text = "\n".join((GAME / path).read_text(encoding="utf-8").splitlines()[start - 1:start - 1 + n])
    assert text == props["code"], bid
    excerpts.append({"beat_id": bid, "path": path, "start_line": start, "end_line": start + n - 1, "text": text})


def media(path):
    return {"path": path, "sha256": sha(REEL / path)}


pairs = [
    {"code_beat": "B10", "result_beat": "B11",
     "observation": "Native 4K render through the scene's own a3_asset_camera (cropped to the figure frame): the chair, the "
                    "tablet floating tilted beside the large crate, and the small crate stand on the floor against "
                    "the back wall at the transforms in lines 137-147; nothing is scaled or sunk into the floor.",
     "media": media("figures/godot_asset_cam.png")},
    {"code_beat": "B12", "result_beat": "B13",
     "observation": "Recorded Part 1 output of the fresh headless run, beside the brief: chair (0.44, 0.9, 0.42), "
                    "tablet (0.242, 0.162, 0.028) lowest y -0.081, crate_long (1.0, 0.4, 0.5), crate_cube "
                    "(0.5, 0.5, 0.500006); triangles 72 / 388 / 88 / 88; all within the 0.002 m tolerance.",
     "media": media("figures/brief_vs_headless.png")},
    {"code_beat": "B14", "result_beat": "B15",
     "observation": "596-frame native 4K take at --fixed-fps 30: both lids swing open about the back hinge from frame "
                    "60, close from frame 210, and open again from frame 420, using each crate's own imported "
                    "animation; the headless log for the same animations reads -100.00 deg after open and 0 after close.",
     "media": media("media/B15.mp4")},
    {"code_beat": "B16", "result_beat": "B17",
     "observation": "Recorded Part 2 output: floor top 0.250 from room/floor; every floor item's bottom at 0.250; "
                    "crate and desk footprints 1.000 x 0.500, 0.500 x 0.500, 1.500 x 0.500, 1.500 x 1.000 on the grid; "
                    "tablet bottom 0.603; 15 overlap pairs pass; final line ALL PASS, 0 failures.",
     "media": media("figures/log_part2.png")},
]

ledger = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
          "game": {"name": "walker-survival-shooting", "source_revision": "b370626",
                   "engine": "Godot 4.7.2.stable.official.ed1daf0bf"},
          "files": files, "components": components, "excerpts": excerpts,
          "exclusions": [{"path": p, "reason": r} for p, r in exclusions.items()],
          "code_result_pairs": pairs}
(REEL / "gamedev-evidence.json").write_text(json.dumps(ledger, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
print("gamedev-evidence.json:", len(files), "files,", len(exclusions), "exclusions,", len(pairs), "pairs")
