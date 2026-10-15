#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1)
from the beat sheet and the Godot project folder. Run after build_reel.py,
because the result media are hashed as built.

    python3 tools/make_evidence.py
"""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "godot"

COMPONENTS = {
    "props-glb": ("The three props as Godot imports them: waystone.glb, teleport_circle.glb and spikes.glb (binary glTF exported from Blender "
                  "with +Y Up by tools/blender/export_glb.py) and their .import settings. Each origin is the centre of its underside; sizes and "
                  "budgets come from CHANGE-BRIEF.md.",
                  lambda p: p.startswith("assets/props/")),
    "scene": ("The small 3D scene: project.godot (main scene, Forward Plus, window size), scenes/props_room.tscn (floor, one light, a camera, "
              "the three props at Y = 0 and a 1.2 m post for Rudy's height) and tools/build_props_room.gd, the headless script that builds it.",
              lambda p: p in ("project.godot", "scenes/props_room.tscn", "tools/build_props_room.gd")),
    "check": ("tests/check_props.gd: the headless check. Part 1 measures each .glb on its own (bounding box against the brief within 5 mm, "
              "height on Y, origin at the underside centre, node scale and rotation, triangles, colours); part 2 checks each prop's lowest point "
              "against the floor mesh's top in the scene.",
              lambda p: p == "tests/check_props.gd"),
    "screenshots": ("tests/capture_props.gd: renders the running scene in a window from five views for TEST-REPORT.md. Its first version read "
                    "the camera before the scene was in the tree, one of the three things Claude got wrong. The film's orbit uses a separate "
                    "film-only driver on an isolated copy (capture/orbit_driver.gd).",
                    lambda p: p == "tests/capture_props.gd"),
}
EXCLUDE = {}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    beats = sheet["beats"]
    narrated = {b["beat_id"] for b in beats if (b.get("narration_text") or "").strip()}
    inventory = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*")
                       if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts) and p.suffix != ".uid")
    files, comp_files = [], {c: [] for c in COMPONENTS}
    for path in inventory:
        if path in EXCLUDE:
            continue
        ids = [c for c, (_, match) in COMPONENTS.items() if match(path)]
        if not ids:
            raise SystemExit("unassigned file: " + path)
        files.append({"path": path, "sha256": sha(GAME / path),
                      "role": ("import settings" if path.endswith(".import") else path.rsplit(".", 1)[-1]),
                      "component_ids": ids})
        for c in ids:
            comp_files[c].append(path)
    comp_beats = {c: [] for c in COMPONENTS}
    for b in beats:
        if b["beat_id"] in narrated:
            for c in b.get("components", []):
                comp_beats[c].append(b["beat_id"])
    components = [{"id": c, "explanation": e, "beat_ids": comp_beats[c], "files": comp_files[c]} for c, (e, _) in COMPONENTS.items()]
    excerpts, pairs = [], []
    for i, b in enumerate(beats):
        ex = b.get("excerpt")
        if not ex:
            continue
        code = b["shot"]["remotion"]["props"]["code"]
        excerpts.append({"beat_id": b["beat_id"], "path": ex["path"], "start_line": ex["start_line"], "end_line": ex["end_line"], "text": code})
        r = beats[i + 1]
        media = r["shot"]["evidence_media"]
        pairs.append({"code_beat": b["beat_id"], "result_beat": r["beat_id"], "observation": r["shot"]["observation"],
                      "media": {"path": media, "sha256": sha(REEL / media)}})
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "game": {"name": sheet["metadata"]["game"]["name"], "revision": sheet["metadata"]["game"]["revision"],
                     "folder": sheet["metadata"]["game"]["folder"]},
            "files": files, "components": components, "excerpts": excerpts,
            "exclusions": [{"path": p, "reason": r} for p, r in EXCLUDE.items() if (GAME / p).exists()],
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(files)} files, {len(components)} components, {len(excerpts)} excerpts, {len(pairs)} pairs")


if __name__ == "__main__":
    main()
