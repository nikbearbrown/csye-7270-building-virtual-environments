#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching contract code-then-result-v1) for the Lanternfall film.

Every authored file under godot/ (no .godot/, no .uid) is hashed and tied to a component or excluded with a reason;
excerpts are taken from the beat sheet's GodotDevWorkbench beats and re-read from disk; each code beat is paired with
the next beat's hashed result media.

    python3 tools/make_evidence.py
"""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "godot"
SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()

COMPONENTS = {
    "player": ("The Lamp-Head Courier: movement, facing (code flip), i-frames, pose choice and the draw call that cuts "
               "one 32 x 32 frame out of pc_sheet.png at SPRITE_ORIGIN (16, 23); blocking hooks into movement through "
               "blocker.push_out.", ["B07", "B08", "B09", "B10", "B21"],
               ["features/player/player.gd"]),
    "sprite-asset": ("ART-PC-01 from design to Godot: the generated, palette-locked 10-frame sheet, the palettes and "
                     "geometry manifests, and art.gd, which loads textures and lets the game run on placeholders.",
                     ["B04", "B05", "B06", "B07", "B08"],
                     ["assets/art/pc_sheet.png", "assets/art/pc_sheet.png.import", "assets/art/palettes.json",
                      "assets/art/manifest.json", "features/art.gd"]),
    "world-art": ("The other 13 generated art assets (enemies, map props, ground tile, weapon effects, gem), all FLUX.1-"
                  "schnell; shown in play throughout, with the moth's sprite box and the stall's solid box measured from "
                  "these files.", ["B17", "B22", "B29"],
                  [p for p in ["enemy_moth", "enemy_wraith", "env_crates", "env_ground_tile", "env_lantern_post",
                               "env_leaves", "env_noodle_cart", "env_puddle", "env_stall", "fx_beam", "fx_orbit_moth",
                               "fx_sunflare", "pickup_gem"] for p in (f"assets/art/{p}.png", f"assets/art/{p}.png.import")]),
    "audio": ("AudioBus listens to session signals and never writes game state: one RULES table throttles every SFX "
              "(pure SfxGate on the simulation clock), music follows state.changed (pause low-pass -10 dB, card duck "
              "-6 dB, fades and stingers), mute flips bus flags only. The seven WAV effects and two OGG loops it plays.",
              ["B11", "B12", "B13", "B14", "B23", "B24"],
              ["audio/audio_bus.gd", "audio/sfx_gate.gd", "assets/manifest.json"] +
              [p for n in ["sfx_01_kill", "sfx_02_pickup", "sfx_03_hurt", "sfx_04_levelup", "sfx_05_evolve",
                           "sfx_06a_lose", "sfx_06b_win"] for p in (f"assets/sfx/{n}.wav", f"assets/sfx/{n}.wav.import")] +
              [p for n in ["mus_01_night_market", "mus_02_sunflare_layer"] for p in (f"assets/music/{n}.ogg", f"assets/music/{n}.ogg.import")]),
    "session": ("The deterministic fixed-tick session and its state machine (MENU, PLAYING, LEVELUP, PAUSED, WON, LOST): "
                "weapons, damage, card offers, evolution, input actions (pause, restart, mute, cards; the input map is created "
                "in code by _ensure_inputs), project settings (640 x 360 canvas, stretch mode, main scene) and the "
                "one-node main scene.", ["B16", "B17", "B23", "B24"],
                ["game/session.gd", "game/game_state.gd", "game/main.tscn", "project.godot"]),
    "weapons": ("The Beam bolt and its effects, and the enemy hit tests: touches() / touches_segment() test the visible "
                "sprite box, the change that made bullets stop on what the player sees.", ["B16", "B17"],
                ["features/weapons/beam_shot.gd", "features/weapons/weapon_fx.gd", "features/enemies/enemy.gd"]),
    "progression": ("Levels, XP, branching cards, five-level passives and the evolution rule: when both weapons reach "
                    "level 3 the Sunflare card is offered first.", ["B18", "B19"],
                    ["features/progression/progression.gd"]),
    "world": ("The broken-up market (14 clusters, solid props with fixed boxes measured from the sprites, push_out) "
              "and the camera moves (Sunflare zoom-out, hit tilt, title push-in).", ["B19", "B21", "B22"],
              ["features/world/ground.gd", "features/world/camera_fx.gd"]),
    "pacing": ("Spawner phases, gems and the tuning table that the runs on screen are made of (dense waves, HP growth "
               "per minute, pickup radius). Shown in play and counted in the dense-wave beat; not read line by line.",
               ["B12"], ["features/enemies/spawner.gd", "features/pickups/gem.gd", "features/tuning.gd"]),
    "hud": ("The HUD text rebuilt from state each frame, including the MUSIC/SFX line read from the bus flags.",
            ["B23", "B24"], ["ui/hud.gd"]),
    "tests": ("Headless suites on a harness that fails a suite that stops early: logic 32, gameplay 65, audio 25 checks; "
              "the audio suite's independence check replays a seed with all sound removed. capture.gd rendered the "
              "in-game row of the character comparison.", ["B27", "B28", "B08"],
              ["tests/harness.gd", "tests/test_logic.gd", "tests/test_gameplay.gd", "tests/test_audio.gd", "tests/capture.gd"]),
}
EXCLUSIONS = {
    "tests/capture_map.gd": "Development tool that renders design/map-overview.png; the map overview is not shown in this film.",
    "tests/probe_balance.gd": "Development tool (scripted balance bots for evidence/balance-probe-*.txt); not part of the playable slice and not shown.",
    "tests/rasterize_storyboard.gd": "Development tool that rasterises the storyboard SVGs for the storyboard comparison, which this film does not show.",
}
ROLES = {".gd": "GDScript", ".tscn": "scene", ".godot": "project settings", ".png": "generated sprite (PNG)",
         ".wav": "generated sound effect (WAV)", ".ogg": "generated music loop (OGG Vorbis)", ".import": "import settings sidecar",
         ".json": "asset data"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    beats = sheet["beats"]
    order = [b["beat_id"] for b in beats]
    inventory = sorted(p.relative_to(GAME).as_posix() for p in GAME.rglob("*")
                       if p.is_file() and not any(x in (".godot", ".git") for x in p.relative_to(GAME).parts) and p.suffix != ".uid")
    owner = {}
    for cid, (_e, _b, files) in COMPONENTS.items():
        for f in files:
            owner.setdefault(f, []).append(cid)
    missing = [p for p in inventory if p not in owner and p not in EXCLUSIONS]
    extra = [p for p in owner if p not in inventory]
    if missing or extra:
        raise SystemExit(f"inventory mismatch: unassigned {missing}, unknown {extra}")
    files = [{"path": p, "sha256": sha(GAME / p), "role": ROLES.get(Path(p).suffix, "file"), "component_ids": owner[p]}
             for p in inventory if p in owner]
    comps = [{"id": cid, "explanation": e, "beat_ids": b, "files": f} for cid, (e, b, f) in COMPONENTS.items()]
    excerpts, pairs = [], []
    for i, b in enumerate(beats):
        rem = (b.get("shot") or {}).get("remotion") or {}
        if not rem.get("pattern", "").startswith("GodotDevWorkbench") or not rem.get("props", {}).get("code"):
            continue
        p = rem["props"]
        path = p["path"].replace("res://", "")
        n = len(p["code"].split("\n"))
        text = "\n".join((GAME / path).read_text().splitlines()[p["startLine"] - 1:p["startLine"] - 1 + n])
        if text != p["code"]:
            raise SystemExit(f"{b['beat_id']}: displayed code differs from {path}")
        excerpts.append({"beat_id": b["beat_id"], "path": path, "start_line": p["startLine"], "end_line": p["startLine"] + n - 1,
                         "text": text})
        nxt = beats[i + 1]
        media = nxt["shot"].get("evidence_media")
        if not media:
            raise SystemExit(f"{b['beat_id']}: next beat {nxt['beat_id']} has no evidence media")
        pairs.append({"code_beat": b["beat_id"], "result_beat": nxt["beat_id"],
                      "observation": nxt.get("observation") or nxt["role_note"],
                      "media": {"path": media, "sha256": sha(REEL / media)}})
    data = {"schema_version": 1, "teaching_contract": "code-then-result-v1",
            "game": {"project_dir": "godot", "source_revision": SHA, "engine": "Godot 4.7.2.stable.official.ed1daf0bf"},
            "files": files, "components": comps, "excerpts": excerpts,
            "exclusions": [{"path": p, "reason": r} for p, r in EXCLUSIONS.items()],
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"gamedev-evidence.json: {len(files)} files, {len(EXCLUSIONS)} exclusions, {len(comps)} components, "
          f"{len(excerpts)} excerpts, {len(pairs)} code/result pairs")


if __name__ == "__main__":
    main()
