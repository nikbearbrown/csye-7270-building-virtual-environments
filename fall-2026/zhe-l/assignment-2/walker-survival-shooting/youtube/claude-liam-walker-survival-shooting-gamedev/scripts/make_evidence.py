"""Write gamedev-evidence.json (schema 1, code-then-result-v1) from the real files.

Hashes every authored file in the exported godot/ folder (minus .godot/ and
.uid), reads excerpt text straight from the files and from the beat sheet,
and hashes the result media actually shown. Run: python -I scripts/make_evidence.py
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

components = [
    {"id": "greybox-room", "files": ["base.tscn"], "beat_ids": ["B10", "B14"],
     "explanation": "ENV-BASE-01: one saved scene of CSG boxes (16 x 10 m room, 3 m interior) combined with "
                    "use_collision, a test chair instance and a preview camera. No scripts, no player, no audio nodes."},
    {"id": "stair-ramp", "files": ["base.tscn"], "beat_ids": ["B11", "B12"],
     "explanation": "Six CSG steps (0.2 m rise, 0.3 m run) plus an invisible StaticBody3D box tilted 33.7 deg so a "
                    "future character body can walk up; shown with --debug-collisions and a raycast check."},
    {"id": "lighting", "files": ["base.tscn"], "beat_ids": ["B13", "B14"],
     "explanation": "Two pale-blue OmniLight3D nodes (energy 1.5, range 8 m) and a near-black Environment with weak "
                    "blue-grey ambient light, implementing the concept's dark, cool art direction."},
    {"id": "project-config", "files": ["project.godot"], "beat_ids": ["B10"],
     "explanation": "Forward Plus, Jolt Physics, D3D12, canvas_items stretch. No input map and no main scene, which is "
                    "why nothing can trigger a sound and F5 asks for a scene."},
    {"id": "test-seat", "files": ["assets/furniture/test_chair.glb", "assets/furniture/test_chair.glb.import"],
     "beat_ids": ["B10", "B14"],
     "explanation": "ENV-SEAT-TEST-01: a low-poly chair Claude built in Blender from basic shapes and exported as GLB, "
                    "imported with default settings and instanced against the back wall."},
]
roles = {"base.tscn": "saved scene (greybox)", "project.godot": "project configuration",
         "assets/furniture/test_chair.glb": "imported 3D asset",
         "assets/furniture/test_chair.glb.import": "import settings sidecar"}
exclusions = {
    ".editorconfig": "Editor formatting defaults from the Godot project template; no runtime effect.",
    ".gitattributes": "Git line-ending rules from the project template; no runtime effect.",
    ".gitignore": "Git ignore rules from the project template; no runtime effect.",
    "icon.svg": "Default Godot project icon; not used by base.tscn.",
    "icon.svg.import": "Import sidecar for the default icon; default settings.",
}

files = []
inv = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*")
             if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts)
             and p.suffix != ".uid")
for path in inv:
    if path in exclusions:
        continue
    ids = [c["id"] for c in components if path in c["files"]]
    files.append({"path": path, "sha256": sha(GAME / path), "role": roles[path], "component_ids": ids})

excerpts = []
for bid in ("B11", "B13"):
    props = beats[bid]["shot"]["remotion"]["props"]
    start = props["startLine"]
    n = len(props["code"].split("\n"))
    text = "\n".join((GAME / "base.tscn").read_text(encoding="utf-8").splitlines()[start - 1:start - 1 + n])
    assert text == props["code"], bid
    excerpts.append({"beat_id": bid, "path": "base.tscn", "start_line": start, "end_line": start + n - 1, "text": text})

pairs = [
    {"code_beat": "B11", "result_beat": "B12",
     "observation": "Normal render shows only steps; the same orthographic frame with --debug-collisions shows the "
                    "ramp box lying across all six step edges. Raycast: step noses 1-5 hit stairs_ramp at +0.7 mm, "
                    "nose 6 hits the CSG landing edge at 0.0 mm (evidence/ramp-check.log).",
     "media": {"path": "figures/stairs_compare.png", "sha256": sha(REEL / "figures/stairs_compare.png")}},
    {"code_beat": "B13", "result_beat": "B14",
     "observation": "Native 4K render pan (614 frames): starts on the test chair at the back wall, passes the "
                    "bright light pools on the ceiling at x = +3.5 and x = -3.5, ends on the stairs; walls and floor read "
                    "blue-grey. Only the camera added by the capture script moves; the scene is static.",
     "media": {"path": "media/B14.mp4", "sha256": sha(REEL / "media/B14.mp4")}},
]

ledger = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
          "game": {"name": "walker-survival-shooting", "source_revision": "f848d84",
                   "engine": "Godot 4.7.2.stable.official.ed1daf0bf"},
          "files": files, "components": components,
          "excerpts": excerpts, "exclusions": [{"path": p, "reason": r} for p, r in exclusions.items()],
          "code_result_pairs": pairs}
(REEL / "gamedev-evidence.json").write_text(json.dumps(ledger, indent=1, ensure_ascii=True) + "\n", encoding="ascii")
print("gamedev-evidence.json:", len(files), "files,", len(exclusions), "exclusions,", len(pairs), "pairs")
