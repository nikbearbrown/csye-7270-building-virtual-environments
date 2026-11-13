"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1) for the A6 film.

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
    "base.tscn": ("saved subway-base scene: player, ceiling lights, wall switch, LandingDust and LightDust instances",
                  ["scene", "effect-a-trigger", "effect-b-condition"]),
    "project.godot": ("project settings: Forward+, Jolt, window 2048x1152, input map (Space, F, WASD)", ["scene"]),
    "effects/landing_dust.tscn": ("Effect A: Node3D + Dust and GroundRing GPUParticles3D", ["effect-a"]),
    "effects/landing_dust_trigger.gd": ("Effect A trigger: landed -> move to the feet, restart() both emitters",
                                        ["effect-a-trigger"]),
    "effects/light_dust.tscn": ("Effect B: one GPUParticles3D, box emission, turbulence, ramp, ADD, lit", ["effect-b"]),
    "effects/light_dust_listener.gd": ("Effect B listener: lights_changed / visibility -> show, restart, hide",
                                       ["effect-b-condition"]),
    "characters/human/humanoid/humanoid.gd": ("humanoid body: the notify-only landed signal", ["effect-a-trigger"]),
    "characters/human/humanoid/humanoid.tscn": ("humanoid body scene (capsule 1.6 m)", ["effect-a-trigger"]),
    "characters/human/player/player.tscn": ("player = humanoid + PlayerController brain + PlayerCamera",
                                            ["effect-a-trigger"]),
    "characters/human/player/player_controller.gd": ("player brain: keys -> intent (jump, move, interact)",
                                                     ["effect-a-trigger"]),
    "characters/human/player/screen_tablet.gd": ("on-screen tablet copy (start point; not explained here)", ["scene"]),
    "characters/character_intent.gd": ("intent passed from brain to body", ["effect-a-trigger"]),
    "world/lights/ceiling_lights.gd": ("CeilingLights keeper: lights_changed, is_lights_on()", ["effect-b-condition"]),
    "world/light_switch/light_switch.gd": ("wall switch: F inside InteractArea toggles CeilingLights",
                                           ["effect-b-condition"]),
    "world/light_switch/light_switch.tscn": ("wall switch scene with InteractArea", ["effect-b-condition"]),
    "previews/landing_dust_preview.tscn": ("Effect A preview scene (fixture) for the frame strips", ["strips"]),
    "previews/landing_dust_preview.gd": ("Effect A preview timeline: trigger at frame 10, retrigger at 25", ["strips"]),
    "previews/light_dust_preview.tscn": ("Effect B preview scene (fixture) for the frame strips", ["strips"]),
    "previews/light_dust_preview.gd": ("Effect B preview timeline: on 10, pause 45-55, hide 60-65, off 70",
                                       ["strips"]),
    "shaders/particles_generated.gdshader": ("process shader generated from Effect B's ParticleProcessMaterial",
                                             ["process-shader"]),
    "tests/test_landing_dust_config.gd": ("Effect A read-back test (ClassDB names + values), 157 checks", ["tests"]),
    "tests/test_landing_dust_events.gd": ("Effect A state test: real Space/D keys, retrigger, 27 checks", ["tests"]),
    "tests/test_light_dust_config.gd": ("Effect B read-back test, 110 checks", ["tests"]),
    "tests/test_light_dust_state.gd": ("Effect B state test: real S/F keys, pause, hide, 41 checks", ["tests"]),
    "tests/cost_effects.gd": ("headless CPU price with empty-scene and 10,000-CPU-particle controls", ["price"]),
    "debug/gpu_price.gd": ("windowed GPU-time helper: Effect B shown/hidden, Effect A bursting", ["price"]),
    "debug/vsync_toggle.gd": ("debug key V: vsync on/off for the FPS comparison", ["price"]),
}

EXCLUDE = {
    ".editorconfig": "Editor formatting defaults from the Godot project template; no runtime effect.",
    ".gitattributes": "Git line-ending rules from the project template; no runtime effect.",
    ".gitignore": "Git ignore rules; no runtime effect.",
    "icon.svg": "Default Godot project icon.",
    "icon.svg.import": "Import settings of the default icon.",
    "MATERIALS.md": "Assignment 5 material audit; not part of the particle work.",
    "tests/a3_asset_check.gd": "Assignment 3 baseline test; counts in TEST-REPORT, not explained here.",
    "tests/screen_glow_check.gd": "Assignment 5 baseline test; counts in TEST-REPORT, not explained here.",
    "tests/normal_map_check.gd": "Assignment 5 baseline test; counts in TEST-REPORT, not explained here.",
    "tests/test_materials.gd": "Assignment 5 baseline test (168 passed, 1 known failure); not explained here.",
    "debug/screen_glow_capture.gd": "Assignment 5 capture tool.",
    "debug/screen_glow_capture.tscn": "Assignment 5 capture scene.",
    "items/tablet/tablet_device.gd": "Assignment 5 tablet script; not part of the particle work.",
    "items/tablet/tablet_device.tscn": "Assignment 5 tablet prefab; not part of the particle work.",
    "tools/make_hint_greys.gd": "Assignment 5 hint-experiment tool.",
    "shaders/crate_wear.gdshader": "Assignment 5 crate shader; visible in the base, not explained here.",
    "shaders/hint_experiment.gdshader": "Assignment 5 hint experiment shader.",
    "shaders/pad_base_light.gdshader": "Assignment 5 tablet screen shader.",
    "shaders/standard_generated.gdshader": "Assignment 5 generated StandardMaterial3D shader.",
    "assets/props/tablet.glb": "Assignment 3 tablet model; not part of the particle work.",
    "assets/props/tablet.glb.import": "Import settings of the tablet model.",
    "assets/shader/metal041c/ATTRIBUTION.md": "Assignment 5 texture credits (crates); the particles use no outside texture.",
}
for _p in ["experiments/hint/hint_experiment.tscn", "experiments/hint/hint_greys_3x1.png",
           "experiments/hint/hint_greys_3x1.png.import", "experiments/hint/hint_raw.tres",
           "experiments/hint/hint_source_color.tres"]:
    EXCLUDE[_p] = "Assignment 5 hint experiment; not part of the particle work."
for _p in ["chair", "computer_desk", "computer_desk_l", "crate_cube", "crate_long", "test_chair"]:
    EXCLUDE[f"assets/furniture/{_p}.glb"] = "Assignment 3 furniture model; background in the captures only."
    EXCLUDE[f"assets/furniture/{_p}.glb.import"] = "Import settings of Assignment 3 furniture."
for _p in ["crate_cube_wear", "crate_long_wear"]:
    EXCLUDE[f"assets/furniture/materials/{_p}.tres"] = "Assignment 5 crate material; background only."
for _k in ("Color", "Displacement", "Roughness", "NormalGL", "NormalDX"):
    _p = f"assets/shader/metal041c/Metal041C_1K-PNG_{_k}.png"
    EXCLUDE[_p] = "Assignment 5 crate texture (ambientCG, CC0); not used by the particles."
    EXCLUDE[_p + ".import"] = "Import settings of an Assignment 5 crate texture."

COMPONENTS = {
    "scene": ("The saved base scene holds the player, the three ceiling lights, the wall switch and one instance of "
              "each effect; project.godot maps Space, WASD and F.", ["B02", "B08", "B16"]),
    "effect-a": ("Landing dust: Dust (24 one-shot billboard puffs, ring spawn, damping, scale curve, opacity ramp, "
                 "0.32 m quads) and GroundRing (one flat ring quad that grows and fades).",
                 ["B03", "B04", "B05", "B06"]),
    "effect-a-trigger": ("humanoid.gd emits landed once per landing (not on load); the trigger moves to the feet and "
                         "restart()s both emitters, so a second landing clears the first burst.",
                         ["B07", "B08", "B09", "B10"]),
    "effect-b": ("Light dust: 1300 specks in a 14 x 2.6 x 9 m box via emission_shape_offset, turbulence, a "
                 "multi-peak opacity ramp, additive lit quads 0.003-0.03 m, 6 s preprocess.",
                 ["B11", "B12", "B13", "B14"]),
    "effect-b-condition": ("The listener follows CeilingLights.lights_changed (queried once at start): on = show and "
                           "one restart(); off = hidden, no births; hide/show handled via visibility_changed.",
                           ["B15", "B16"]),
    "strips": ("Preview scenes replay each effect on a fixed timeline for the Movie Maker fixture strips.",
               ["B05", "B06", "B10", "B13", "B14", "B18", "B20"]),
    "process-shader": ("Godot's generated particles shader for Effect B: lines 261/263 emission box and offset; "
                       "line 253 colour ramp; lines 397/410 gravity.", ["B17", "B18", "B19", "B20"]),
    "tests": ("Read-back tests check ClassDB names then every brief value; state tests drive real keys and check "
              "landing count, retrigger, lights on/off, pause and hide.", ["B21", "B22", "B23"]),
    "price": ("Headless cost script with controls; windowed GPU-time helper and vsync key for the GPU price.",
              ["B24", "B25", "B26"]),
}

OBSERVATIONS = {
    "B04": "Fixture strip r0: the ring is clear at frames 15-20; the dust is a few small warm dots, gone by frame 30.",
    "B07": "Native 4K scripted capture: six landings logged (ticks 118, 268, 398, 458, 518, 578); dust and ring at "
           "the feet each time; rapid landings replace the previous burst.",
    "B09": "Fixture retrigger strip: old dust gone at frame 25, new ring at the new spot at 27, old cloud never returns.",
    "B12": "Fixture strips r0 and r1 under light 1: specks of 1-2 px; difference tiles show where they are; r1 sparser.",
    "B15": "Native 4K capture with a film camera: lights off -> dust gone that frame; on -> spread at once; paused "
           "frames identical; hidden -> none; shown -> full at once.",
    "B17": "Fixture strip redesign-2: the computed difference spans the whole frame, i.e. the 14 x 9 m box.",
    "B19": "Fixture strip redesign-2: f11 and f40 differ in which specks are lit; f46 = f54 (paused).",
    "B21": "Recorded output: 157 / 27 / 110 / 41 passed, 0 failed at 60 fps headless.",
    "B24": "Recorded output: empty 0.0041 ms, base 0.3110, A 0.3167, B 0.3356, CPU control 1.8764 ms per frame.",
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
