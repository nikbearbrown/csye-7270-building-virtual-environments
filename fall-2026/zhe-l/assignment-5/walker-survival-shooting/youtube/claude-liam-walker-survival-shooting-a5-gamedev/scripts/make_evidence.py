"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) for the A5 film.

Files are hashed from the game copy (GAME in author_sheet.py); excerpts are taken from beat_sheet.json,
whose code text author_sheet.py read from the same files. Result media hashes are of the reel files shown.
Run after author_sheet.py and make_figures.py / prepare_media.py:  python -I scripts/make_evidence.py
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from author_sheet import GAME, REEL  # noqa: E402

ROLES = {
    "base.tscn": ("saved subway-base scene: crates, player, lights, environment", ["scene"]),
    "project.godot": ("project settings: Forward Plus, input map (tablet = Tab), viewport size", ["scene"]),
    "shaders/pad_base_light.gdshader": ("hand-written unshaded screen-glow shader", ["screen-shader"]),
    "items/tablet/tablet_device.tscn": ("tablet prefab: Model + Screen quad with the Local To Scene ShaderMaterial",
                                        ["screen-shader", "screen-driver"]),
    "items/tablet/tablet_device.gd": ("tablet script: set_screen_lit() writes pad_light_data", ["screen-driver"]),
    "assets/props/tablet.glb": ("tablet model (Assignment 3 asset) under the Screen quad", ["screen-shader"]),
    "characters/human/humanoid/humanoid.gd": ("humanoid body: tablet state machine and _update_tablet_screen()",
                                              ["screen-driver"]),
    "characters/human/humanoid/humanoid.tscn": ("humanoid body scene with the tablet slots", ["screen-driver"]),
    "characters/human/player/player.tscn": ("player = humanoid + PlayerController brain", ["screen-driver"]),
    "characters/human/player/player_controller.gd": ("player brain: reads Tab into a tablet press intent",
                                                     ["screen-driver"]),
    "characters/character_intent.gd": ("intent passed from brain to body", ["screen-driver"]),
    "tests/screen_glow_check.gd": ("headless driver test, real Tab events, 30/60/144 fps", ["screen-tests"]),
    "debug/screen_glow_capture.gd": ("F9 controlled-value capture tool", ["screen-tests"]),
    "debug/screen_glow_capture.tscn": ("scene that runs the capture tool", ["screen-tests"]),
    "shaders/crate_wear.gdshader": ("hand-written crate wear shader (box projection, mask, two textures)",
                                    ["crate-shader"]),
    "assets/furniture/materials/crate_long_wear.tres": ("ShaderMaterial: wear 0.2, roughness 0.95",
                                                        ["crate-materials"]),
    "assets/furniture/materials/crate_cube_wear.tres": ("ShaderMaterial: wear 0.1, roughness 0.85",
                                                        ["crate-materials"]),
    "assets/furniture/crate_long.glb": ("long crate model (Assignment 3 asset)", ["crate-materials"]),
    "assets/furniture/crate_long.glb.import": ("import settings: Use External -> crate_long_wear.tres",
                                               ["crate-materials"]),
    "assets/furniture/crate_cube.glb": ("small crate model (Assignment 3 asset)", ["crate-materials"]),
    "assets/furniture/crate_cube.glb.import": ("import settings: Use External -> crate_cube_wear.tres",
                                               ["crate-materials"]),
    "experiments/hint/hint_experiment.tscn": ("hint experiment scene: two unshaded quads", ["hint-experiment"]),
    "shaders/hint_experiment.gdshader": ("hand-written hint experiment shader", ["hint-experiment"]),
    "experiments/hint/hint_source_color.tres": ("material: use_source_color = true", ["hint-experiment"]),
    "experiments/hint/hint_raw.tres": ("material: use_source_color = false", ["hint-experiment"]),
    "experiments/hint/hint_greys_3x1.png": ("3x1 grey PNG: 64, 128, 192", ["hint-experiment"]),
    "experiments/hint/hint_greys_3x1.png.import": ("lossless, no mipmaps", ["hint-experiment"]),
    "tools/make_hint_greys.gd": ("script that wrote the grey PNG (Claude)", ["hint-experiment"]),
    "shaders/standard_generated.gdshader": ("shader generated from a StandardMaterial3D, with my comments",
                                            ["generated-shader"]),
    "tests/test_materials.gd": ("material audit test (169 checks)", ["material-tests"]),
    "tests/normal_map_check.gd": ("curl-ratio normal map check", ["material-tests", "textures"]),
    "MATERIALS.md": ("material audit table, reviewed", ["material-tests"]),
    "assets/shader/metal041c/ATTRIBUTION.md": ("texture credits: ambientCG Metal041C, CC0", ["textures"]),
}
for kind in ("Color", "Displacement", "Roughness", "NormalGL", "NormalDX"):
    p = f"assets/shader/metal041c/Metal041C_1K-PNG_{kind}.png"
    ROLES[p] = (f"Metal041C {kind} texture (ambientCG, CC0)", ["textures"])
    ROLES[p + ".import"] = (f"explicit import settings for the {kind} texture", ["textures"])

EXCLUDE = {
    ".editorconfig": "Editor formatting defaults from the Godot project template; no runtime effect.",
    ".gitattributes": "Git line-ending rules from the project template; no runtime effect.",
    ".gitignore": "Git ignore rules; no runtime effect.",
    "icon.svg": "Default Godot project icon.",
    "icon.svg.import": "Import settings of the default icon.",
    "assets/furniture/test_chair.glb": "Assignment 3 test asset, not used by base.tscn.",
    "assets/furniture/test_chair.glb.import": "Import settings of the unused test asset.",
    "assets/furniture/chair.glb": "Assignment 3 furniture visible in the base; no shader work in this film.",
    "assets/furniture/chair.glb.import": "Import settings of Assignment 3 furniture.",
    "assets/furniture/computer_desk.glb": "Assignment 3 furniture visible in the base; no shader work in this film.",
    "assets/furniture/computer_desk.glb.import": "Import settings of Assignment 3 furniture.",
    "assets/furniture/computer_desk_l.glb": "Assignment 3 furniture visible in the base; no shader work in this film.",
    "assets/furniture/computer_desk_l.glb.import": "Import settings of Assignment 3 furniture.",
    "assets/props/tablet.glb.import": "Import settings of the Assignment 3 tablet model; unchanged in A5.",
    "tests/a3_asset_check.gd": "Assignment 3 baseline test; its counts (55 PASS before and after) are in "
                               "TEST-REPORT, not explained in this film.",
}

COMPONENTS = {
    "scene": ("The saved base scene holds the two crates, the player and the ceiling lights the crates are judged "
              "under; project.godot maps Tab to the tablet action.", ["B02", "B10"]),
    "screen-shader": ("Seven-line unshaded spatial shader: pad_light_data mixes black to cold_white; the colour "
                      "line matches the specification.", ["B03", "B04"]),
    "screen-driver": ("The body lights the screen only when the tablet has arrived in the hand and darkens it at "
                      "once when put away; the tablet writes the uniform into its own Local To Scene material.",
                      ["B05", "B06", "B07"]),
    "screen-tests": ("Headless driver test with real Tab events at 30/60/144 fps, and the F9 capture tool used for "
                     "the controlled values.", ["B04", "B08"]),
    "crate-shader": ("Box-projected UVs in vertex(); fragment() compares the height mask with wear_amount; five "
                     "grouped uniforms.", ["B11", "B12", "B13", "B14", "B15", "B16"]),
    "crate-materials": ("Two ShaderMaterials share crate_wear.gdshader and differ in wear_amount and "
                        "paint_roughness; each crate's .glb import points at its material with Use External.",
                        ["B09", "B10"]),
    "textures": ("ambientCG Metal041C (CC0): Color as rust colour with source_color, Displacement as data mask; "
                 "normal maps only in the Step 4 material and the curl check.", ["B11", "B22", "B26"]),
    "hint-experiment": ("One grey PNG sampled with and without source_color on unshaded quads; predicted and "
                        "measured values match.", ["B17", "B18"]),
    "generated-shader": ("Shader written by Godot from a StandardMaterial3D, annotated by the user; lines 13 and 42 "
                         "set colour vs data sampling.", ["B19", "B21"]),
    "material-tests": ("The audit's material test reads hints, values, imports and wiring; the source_color "
                       "mutation fails it.", ["B23", "B24", "B25"]),
}

OBSERVATIONS = {
    "B03": "The user's in-engine captures at 0, 0.39, 1.0 and 2.0: the screen centre reads exactly the hand-computed "
           "values; 2.0 is pure white.",
    "B05": "Scripted Tab input in a native 4K render: dark while the tablet moves, lit on arrival in the hand, no "
           "dark frame when switching hands, dark on put-away, never lit when put away before arrival.",
    "B07": "Recorded test output at 30/60/144 fps: lit 0.3667/0.35/0.35 s after the change; the second body's "
           "screen stayed 0.0 on every frame.",
    "B09": "Native 4K render: the long crate (wear 0.2, roughness 0.95) shows more rust than the small one "
           "(0.1, 0.85); both use the same shader and textures.",
    "B11": "wear_amount 0, 0.1 and 1.0 at runtime: no rust, about a tenth, all rust; the pattern stays where the "
           "mask puts it.",
    "B13": "texture_scale 0.1, 2.0 and 10.0 at runtime: large blotches, default patches, fine speckle.",
    "B15": "Every uniform at minimum, default and maximum; roughness and softness shown from a highlight angle.",
    "B17": "Native 4K render: 64/128/192 with source_color, 137/188/225 without, equal to the predictions.",
    "B19": "Same camera, film-only copy with source_color removed from crate_wear.gdshader line 3: the small "
           "crate's rust turns paler and washed out.",
    "B21": "Recorded curl ratios: NormalGL 0.1991 under GL, 1.8009 under DX; NormalDX the reverse.",
    "B23": "Recorded output of the source_color mutation: the rust_albedo hint check fails, exit 1.",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text(encoding="utf-8"))
    beats = sheet["beats"]
    files, missing = [], []
    for p in sorted(x.relative_to(GAME).as_posix() for x in GAME.rglob("*")
                    if x.is_file() and ".godot" not in x.parts and x.suffix != ".uid"):
        if p in EXCLUDE:
            continue
        if p not in ROLES:
            missing.append(p)
            continue
        role, comps = ROLES[p]
        files.append({"path": p, "sha256": sha(GAME / p), "role": role, "component_ids": comps})
    if missing:
        sys.exit(f"files with no role or exclusion: {missing}")
    comps = [{"id": k, "explanation": v[0], "beat_ids": v[1],
              "files": [f["path"] for f in files if k in f["component_ids"]]} for k, v in COMPONENTS.items()]
    excerpts, pairs = [], []
    for i, b in enumerate(beats):
        rem = (b.get("shot") or {}).get("remotion") or {}
        if rem.get("pattern") != "GodotDevWorkbench":
            continue
        props = rem["props"]
        path, rng = props["path"].split("  ·  lines ")
        a, z = (int(x) for x in rng.split("–"))
        excerpts.append({"beat_id": b["beat_id"], "path": path, "start_line": a, "end_line": z, "text": props["code"]})
        res = beats[i + 1]
        media = res["shot"]["evidence_media"]
        pairs.append({"code_beat": b["beat_id"], "result_beat": res["beat_id"],
                      "observation": OBSERVATIONS[b["beat_id"]],
                      "media": {"path": media, "sha256": sha(REEL / media) if (REEL / media).exists() else "MISSING"}})
    ev = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
          "game": {"name": "walker-survival-shooting", "revision": sheet["metadata"]["game"]["source_revision"],
                   "engine": "Godot 4.7.2.stable.official.ed1daf0bf"},
          "files": files, "components": comps, "excerpts": excerpts,
          "exclusions": [{"path": k, "reason": v} for k, v in EXCLUDE.items()], "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(ev, indent=1) + "\n", encoding="utf-8")
    print(f"files {len(files)}, exclusions {len(EXCLUDE)}, excerpts {len(excerpts)}, pairs {len(pairs)}")


if __name__ == "__main__":
    main()
