#!/usr/bin/env python3
"""Write gamedev-evidence.json (schema 1, teaching_contract code-then-result-v1)
from the beat sheet and the game folder. Run after build_reel.py, because the
result media are hashed as built.

    python3 tools/make_evidence.py
"""
import hashlib, json
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
GAME = REEL.parents[1] / "game"

COMPONENTS = {
    "app-flow": ("Main (app/main.gd) runs Level 1's states TITLE → PLAYING → DYING → COMPLETE: Enter on the title, the kill line and the "
                 "fall, the respawn at a checkpoint or the start-over, the teleport circle and the end card. SystemKeys reads Esc, M and N "
                 "while paused. project.godot holds the input map, the autoloads and the physics layer names.",
                 lambda p: p in ("project.godot", "app/main.gd", "app/main.tscn", "app/system_keys.gd")),
    "rudy-controller": ("Rudy (CharacterBody2D): run, turn on the spot, jump with separate rise/fall gravity, stomp bounce, the sword swing "
                        "and its timed hitbox, take_hit (gear first, then hearts), invulnerability, knockback and modes.",
                        lambda p: p in ("content/rudy/rudy.gd", "content/rudy/rudy.tscn")),
    "rudy-art": ("Rudy's sixteen generated frames on one canvas, chosen by pose ID (rudy.gd _pick_pose → rudy_look.gd), with the matting "
                 "record in frames.json; the outline shader and its material that add the 4 px outer line to Rudy, goblins and spikes.",
                 lambda p: p.startswith("content/rudy/frames/") or p == "content/rudy/rudy_look.gd" or p.startswith("systems/art/")),
    "level": ("Level 1's layout scene and its painted layers: the far sky/castle layer at 0.0218 of the camera, the repeated fields at 0.4, "
              "the ground blocks that size their own collision and draw the tiles and cliff pieces (env.json).",
              lambda p: p in ("content/level_1/level_1.tscn", "content/level_1/backdrop.gd", "content/level_1/ground_segment.gd",
                              "content/level_1/art/env.json") or any(p.startswith("content/level_1/art/" + n) for n in
                              ("sky_castle", "fields", "ground_"))),
    "hazards-checkpoints": ("Spikes (a hurt box narrower and lower than the art), the waystone checkpoint (lights once, halo and ring drawn "
                            "by code) and the teleport circle (column of light drawn by code); props.json gives their art origins.",
                            lambda p: any(p.startswith("content/level_1/" + n) for n in ("spikes", "waystone", "portal"))
                            or any(p.startswith("content/level_1/art/" + n) for n in ("ENV-SPIKES", "ENV-WAYSTONE", "ENV-PORTAL", "props.json"))),
    "goblin": ("The goblin Area2D: patrol, a 40×118 box queried every tick, stomp versus hit decided by STOMP_MARGIN, reset after a death; "
               "two walk frames and a squashed frame.",
               lambda p: p.startswith("content/goblin/")),
    "sword-pickup": ("The sword-and-shield pickup (taken once, hidden, reset after a death) and FlyingGear, the picture thrown off when a hit "
                     "knocks the gear away.",
                     lambda p: p.startswith("content/sword_pickup/") or p.startswith("content/level_1/art/PROP-SWORDSHIELD")),
    "audio": ("Sfx, the one entry point for six sounds (one player each, counted per ID), and Music, the looping theme with named dips "
              "(deepest wins), ramps and the fade-out; the Music and SFX buses.",
              lambda p: p.startswith("systems/audio/") or p == "default_bus_layout.tres"),
    "hud": ("The HUD: title over the opening, hearts, the debug line (F1), the black fade, 'Paused' and the end card.",
            lambda p: p.startswith("ui/") or p.startswith("content/level_1/art/endcard")),
    "tests": ("141 headless checks (tests/checks.gd) and the project's own screenshot/mix capture tool (tests/capture.gd). Both use "
              "test-only teleports to set up cases; the film's footage comes from a separate input-only driver.",
              lambda p: p.startswith("tests/")),
}
EXCLUDE = {".DS_Store": "macOS Finder metadata, gitignored; not part of the game."}


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
    order = [b["beat_id"] for b in beats]
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
            "game": {"name": "walker-rudy", "revision": sheet["metadata"]["game"]["revision"], "folder": "game"},
            "files": files, "components": components, "excerpts": excerpts,
            "exclusions": [{"path": p, "reason": r} for p, r in EXCLUDE.items() if (GAME / p).exists()],
            "code_result_pairs": pairs}
    (REEL / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(files)} files, {len(components)} components, {len(excerpts)} excerpts, {len(pairs)} pairs")


if __name__ == "__main__":
    main()
