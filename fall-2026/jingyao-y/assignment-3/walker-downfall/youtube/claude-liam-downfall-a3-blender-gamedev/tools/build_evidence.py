"""Write gamedev-evidence.json (schema 1) against a pristine clone of the film's revision.

  python tools/build_evidence.py <snapshot-of-ceada15>

Every file in the snapshot (minus .git/.godot/*.uid) is either a hashed record tied
to a component the film explains, or an exclusion with a reason. Excerpts are read
from the snapshot and must equal the beat's displayed code; code/result pairs hash
the result media actually shown.
"""
import fnmatch, hashlib, json, sys
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
SNAP = Path(sys.argv[1]).resolve()
REV = "ceada15"
sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
beats = {b["beat_id"]: b for b in sheet["beats"]}

COMPONENTS = [
    ("terrace-dimensions",
     "The map generator's TIER, RAMP_RUN, RAMP_APRON and corridor half-width set every asset size; TerrainSurface "
     "already builds each ramp's slope and each cliff's face and collision, so the assets are dressing over it.",
     ["B03", "B04"],
     ["world/continuous_world_map.gd", "world/terrain_surface.gd"]),
    ("cliff-wall-asset",
     "cliff_wall_segment: three cube strata and one icosphere built by eight verbatim MCP calls; call 6 fixed the "
     "buried lip boulder found by look. 116 triangles, origin at the bottom of the face line.",
     ["B05", "B06"],
     ["tools/blender/build_cliff_wall_segment.py", "art/blender/cliff_wall_segment.blend", "art/models/cliff_wall_segment.glb*"]),
    ("rubble-asset",
     "cliff_rubble_pile: three flattened icospheres; call 5 sank the floating top stone found by look. 180 triangles.",
     ["B06"],
     ["tools/blender/build_cliff_rubble_pile.py", "art/blender/cliff_rubble_pile.blend", "art/models/cliff_rubble_pile.glb*"]),
    ("ramp-asset",
     "arched_ramp_segment: a plane edited into a cambered wedge by top_z, plus two kerbs; the author moved both kerbs "
     "0.1 m outward by hand, and a read-only MCP call verified it. 68 triangles, 18.7 degrees.",
     ["B07", "B08", "B09", "B10"],
     ["tools/blender/build_arched_ramp_segment.py", "art/blender/arched_ramp_segment.blend", "art/models/arched_ramp_segment.glb*"]),
    ("export-import",
     "export_glb.py exports each .blend headless as +Y-up glTF binary (Blender +Y becomes Godot -Z); .gdignore keeps "
     "Godot from importing .blend files and the write-up; *.blend1 backups are ignored.",
     ["B11", "B12"],
     ["tools/blender/export_glb.py", "art/blender/.gdignore", "a3/.gdignore", ".gitignore"]),
    ("preview-scene",
     "asset_preview.tscn: ground, sun, the game's camera and a 1.7 m capsule beside the three assets; its sun basis was "
     "first written by columns and lit the scene from below.",
     ["B12", "B15", "B16"],
     ["art/models/asset_preview.tscn"]),
    ("asset-checks",
     "test_a3_assets.gd reads the imported meshes back (bounds, node transforms, triangles, colours, ramp direction and "
     "slope); capture_a3_preview.gd renders the preview scene to PNG.",
     ["B13", "B14"],
     ["tests/test_a3_assets.gd", "tests/capture_a3_preview.gd"]),
]

EXCLUDE = [
    ("art/*", "Downfall's 2D art batches, shaders and helpers from earlier assignments; not part of the three Blender assets."),
    ("godot_assets/*", "Lappland sprite sheets and helpers from Assignment 2."),
    ("audio/*", "Generated audio from Assignment 2."),
    ("tests/*", "Other test and capture scripts for gameplay; not about the Blender assets."),
    ("game/*", "Gameplay systems outside an asset-pipeline film."),
    ("entities/*", "Enemies, loot and projectiles: runtime gameplay outside this film."),
    ("inventory/*", "Inventory data model: outside this film."),
    ("ui/*", "GUI screens: outside this film."),
    ("world/*", "Other map generation, dressing and base views not explained in this film."),
    ("*.md", "Design notes kept for the game; the A3 write-up lives in the course repo."),
    ("*", "Project configuration and remaining files outside the film's components."),
]


def inventory(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                  if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(root).parts) and p.suffix != ".uid")


files, exclusions, comp_files = [], [], {c[0]: [] for c in COMPONENTS}
for path in inventory(SNAP):
    ids = [cid for cid, _, _, pats in COMPONENTS if any(fnmatch.fnmatchcase(path, p) for p in pats)]
    if ids:
        sha = hashlib.sha256((SNAP / path).read_bytes()).hexdigest()
        role = "source" if path.endswith((".gd", ".py", ".tscn", ".gdignore", ".gitignore")) else "asset"
        files.append({"path": path, "sha256": sha, "role": role, "component_ids": ids})
        for cid in ids: comp_files[cid].append(path)
    else:
        reason = next(r for pat, r in EXCLUDE if fnmatch.fnmatchcase(path, pat))
        exclusions.append({"path": path, "reason": reason})

components = [{"id": cid, "explanation": expl, "beat_ids": bids, "files": comp_files[cid]} for cid, expl, bids, _ in COMPONENTS]
for c in components:
    assert c["files"], c["id"]

excerpts, pairs = [], []
order = list(beats)
for bid, b in beats.items():
    remotion = b.get("shot", {}).get("remotion", {})
    props = remotion.get("props", {})
    if remotion.get("pattern") == "GodotDevWorkbench" and props.get("code"):
        path = props["path"].removeprefix("res://")
        start = props["startLine"]
        text = props["code"]
        end = start + len(text.split("\n")) - 1
        excerpts.append({"beat_id": bid, "path": path, "start_line": start, "end_line": end, "text": text})
        result = order[order.index(bid) + 1]
        media = beats[result]["shot"]["evidence_media"]
        pairs.append({"code_beat": bid, "result_beat": result,
                      "observation": beats[result]["shot"]["show"][-1]["event"],
                      "media": {"path": media, "sha256": hashlib.sha256((REEL / media).read_bytes()).hexdigest()}})

data = {"schema_version": 1, "game_revision": REV, "snapshot": f"pristine git clone of {REV}",
        "teaching_contract": "code-then-result-v1", "files": files, "components": components,
        "excerpts": excerpts, "exclusions": exclusions, "code_result_pairs": pairs}
(REEL / "gamedev-evidence.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(files), "records,", len(exclusions), "exclusions,", len(excerpts), "excerpts,", len(pairs), "pairs")
