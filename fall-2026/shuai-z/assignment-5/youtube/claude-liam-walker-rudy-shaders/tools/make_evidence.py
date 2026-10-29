#!/usr/bin/env python3
"""Write the film's two source ledgers (schema 1, teaching_contract
code-then-result-v1), one per Godot project. Run after build_reel.py,
because the result media are hashed as built.

The course checker takes one folder holding project.godot (--game), and this
assignment has two: game/ (the 2D game) and godot/ (the 3D props scene). So
each project gets a check folder, checks/game/ and checks/godot/, holding:
- gamedev-evidence.json, for that project's files only;
- beat_sheet.json, the film's sheet without the other project's code beats
  (their result beats stay, as ordinary narrated beats), so every remaining
  code beat is still followed by its own result;
- stills/ and media/, hard links to the reel's result media (not in git), so
  the checker can hash them inside the folder it is given.

    python3 tools/make_evidence.py
    tools/check.sh            # runs the unmodified checker on both
"""
import hashlib, json, os
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
A5 = REEL.parents[1]

COMPONENTS = {
 "game": {
  "tint-shader": ("shaders/invulnerable_tint.gdshader, written by shuai-z: canvas_item, three uniforms (tint_amount driven by the game; tint_color "
                  "and tint_strength set by the material only) and the colour line at line 8, which moves only COLOR.rgb toward the waystone's glow. "
                  "project.godot names GL Compatibility, the renderer it runs in.",
                  lambda p: p in ("shaders/invulnerable_tint.gdshader", "project.godot")),
  "tint-driver": ("The hearts and what drives them: ui/hud.gd's _tint_hearts() sets tint_amount every frame to Rudy's _invulnerable_left / "
                  "invulnerable_time; ui/hearts_tint.tres is the ShaderMaterial, local to the scene, on Hud/Hearts (ui/hud.tscn); ui/hearts.gd draws "
                  "the heart art in ui/art/. content/rudy/rudy.gd owns the window and is unchanged byte for byte.",
                  lambda p: p.startswith("ui/") or p == "content/rudy/rudy.gd"),
  "tint-tests": ("tests/invulnerable_tint_checks.gd/.tscn: 15 headless checks through real input at 30, 60 and 144 fps (uniforms, defaults, "
                 "where the material is, begin, fade, end, duration, retrigger, time scale, pause, reload). tests/capture_tint.gd/.tscn: the windowed "
                 "capture at controlled values, with the driver stopped.",
                 lambda p: p.startswith("tests/") and ("invulnerable_tint" in p or "capture_tint" in p)),
 },
 "godot": {
  "stone-shader": ("shaders/weathered_stone.gdshader, written by shuai-z: three samplers with their hints (source_color for colour, hint_normal "
                   "and none for data), four grouped uniforms with ranges, and fragment() writing ALBEDO, NORMAL_MAP, NORMAL_MAP_DEPTH and ROUGHNESS. "
                   "scenes/props_room.tscn carries the two surface overrides, set by tools/add_stone_overrides.gd; project.godot names Forward Plus.",
                   lambda p: p in ("shaders/weathered_stone.gdshader", "scenes/props_room.tscn", "tools/add_stone_overrides.gd", "project.godot")),
  "stone-materials": ("materials/waystone_stone.tres and materials/circle_darkstone.tres: one shader, the same three textures, different values "
                      "(albedo_tint, normal_strength, roughness_offset). They override surface 0 of the waystone's mesh and surface 1 of the circle's, "
                      "in the Assignment 3 props in assets/props/, whose .glb and .import files are unchanged.",
                      lambda p: p in ("materials/waystone_stone.tres", "materials/circle_darkstone.tres") or p.startswith("assets/props/")),
  "stone-textures": ("Rock 01 from Poly Haven (Rob Tuytel, CC0) in assets/textures/rock_01/, with ATTRIBUTION.md and explicit import settings; "
                     "tests/normal_map_check.gd (the assignment's curl check, unchanged) and tests/calibrate_normal_map_check.gd (its calibration on "
                     "the GL/DX pair and the 0.5 threshold).",
                     lambda p: p.startswith("assets/textures/rock_01/") or p in ("tests/normal_map_check.gd", "tests/calibrate_normal_map_check.gd")),
  "hint-experiment": ("shaders/hint_experiment.gdshader (written by shuai-z), its two materials, scenes/hint_experiment.tscn, the grey strip and the "
                      "tools that write them, and the windowed captures tests/capture_hint.gd and tests/capture_hint_vs_os.gd.",
                      lambda p: "hint" in p or "grey_strip" in p),
  "generated-shader": ("shaders/standard_generated.gdshader: what Godot 4.7.2 generated from a StandardMaterial3D with Rock 01's textures, "
                       "annotated by shuai-z; nothing uses it.",
                       lambda p: p == "shaders/standard_generated.gdshader"),
  "stone-tests": ("tests/test_materials.gd (125 headless checks) and MATERIALS.md, the audit's report; tests/capture_sweep.gd, the windowed sweep and "
                  "two-materials capture; tests/check_props.gd, Assignment 3's 44 checks, unchanged and still passing.",
                  lambda p: p in ("tests/test_materials.gd", "MATERIALS.md", "tests/capture_sweep.gd", "tests/check_props.gd")),
 },
}
A2_REASON = ("Assignment 2's game, copied unchanged from tag a3 (84658acf) and not changed by Assignment 5; this film covers the layer Assignment 5 "
             "added. The 141 existing checks in tests/checks.gd guard it, and pass.")
EXCLUDE = {
 "godot": {"tests/capture_props.gd": "Assignment 3's screenshot tool, unchanged; not used by Assignment 5 or this film.",
           "tools/build_props_room.gd": "Assignment 3's scene builder, unchanged; deliberately not re-run, since it would write the scene without the overrides."},
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inventory(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*")
                  if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(root).parts) and p.suffix != ".uid")


def link(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        dst.unlink()
    os.link(src, dst)


def ledger(project, sheet):
    game = A5 / project
    out = REEL / "checks" / project
    comps = COMPONENTS[project]
    beats = [b for b in sheet["beats"] if not (b.get("excerpt") and b["excerpt"]["project"] != project)]
    narrated = {b["beat_id"] for b in beats if (b.get("narration_text") or "").strip()}
    files, comp_files, exclusions = [], {c: [] for c in comps}, []
    for path in inventory(game):
        ids = [c for c, (_, match) in comps.items() if match(path)]
        if not ids:
            reason = EXCLUDE.get(project, {}).get(path) or (A2_REASON if project == "game" else None)
            if not reason:
                raise SystemExit(f"unassigned file: {project}/{path}")
            exclusions.append({"path": path, "reason": reason})
            continue
        files.append({"path": path, "sha256": sha(game / path),
                      "role": "import settings" if path.endswith(".import") else path.rsplit(".", 1)[-1], "component_ids": ids})
        for c in ids:
            comp_files[c].append(path)
    comp_beats = {c: [b["beat_id"] for b in beats if b["beat_id"] in narrated and c in b.get("components", [])] for c in comps}
    components = [{"id": c, "explanation": e, "beat_ids": comp_beats[c], "files": comp_files[c]} for c, (e, _) in comps.items()]
    excerpts, pairs = [], []
    for i, b in enumerate(beats):
        ex = b.get("excerpt")
        if not ex:
            continue
        excerpts.append({"beat_id": b["beat_id"], "path": ex["path"], "start_line": ex["start_line"], "end_line": ex["end_line"],
                         "text": b["shot"]["remotion"]["props"]["code"]})
        r = beats[i + 1]
        media = r["shot"]["evidence_media"]
        link(REEL / media, out / media)
        pairs.append({"code_beat": b["beat_id"], "result_beat": r["beat_id"], "observation": r["shot"]["observation"],
                      "media": {"path": media, "sha256": sha(REEL / media)}})
    meta = sheet["metadata"]
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "game": {"name": f"walker-rudy assignment-5/{project}", "revision": meta["game"]["revision"], "folder": f"assignment-5/{project}"},
            "files": files, "components": components, "excerpts": excerpts, "exclusions": exclusions, "code_result_pairs": pairs}
    out.mkdir(parents=True, exist_ok=True)
    (out / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    (out / "beat_sheet.json").write_text(json.dumps({"metadata": {**meta, "check_note":
        f"Derived by tools/make_evidence.py from ../../beat_sheet.json for the {project}/ check: the other project's code beats are left out."},
        "beats": beats}, indent=1, ensure_ascii=False) + "\n")
    print(f"{project}: {len(files)} files, {len(exclusions)} exclusions, {len(components)} components, {len(excerpts)} excerpts, {len(pairs)} pairs")


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    for project in COMPONENTS:
        ledger(project, sheet)


if __name__ == "__main__":
    main()
