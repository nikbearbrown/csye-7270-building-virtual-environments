#!/usr/bin/env python3
"""Write the film's source ledger (schema 1, teaching_contract
code-then-result-v1) for game/, the one Godot project of Assignment 6. Run
after build_reel.py, because the result media are hashed as built.

The course checker takes one folder holding project.godot (--game) and the
reel folder. As in Assignment 5, the ledger goes in a check folder,
checks/game/, holding:
- gamedev-evidence.json;
- beat_sheet.json, a copy of the film's sheet (this film has one project, so
  no beat is left out);
- stills/ and media/, hard links to the reel's result media (not in git), so
  the checker can hash them inside the folder it is given.

    python3 tools/make_evidence.py
    tools/check.sh            # runs the unmodified checker
"""
import hashlib, json, os
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]
A6 = REEL.parents[1]
PROJECT = "game"

COMPONENTS = {
  "slash-sparks": ("Effect A, SlashSparks: effects/slash_sparks.tscn, a Node2D root with two GPUParticles2D emitters, Flash (1 particle, "
                   "0.12 s) and Sparks (28 streaks, 0.45 s, one shot, explosiveness 1.0), each with a ParticleProcessMaterial and a "
                   "GradientTexture2D with a dark rim; local_coords off. previews/slash_sparks_preview.gd/.tscn is the fixture the strips "
                   "were captured from: Level 1 frozen, a still Rudy, seeded bursts on frames 10 and 20.",
                   lambda p: p.startswith("effects/slash_sparks") or p.startswith("previews/slash_sparks_preview")),
  "run-dust": ("Effect B, RunDust: effects/run_dust.tscn, one GPUParticles2D (40 puffs, 0.5 s, a steady stream) with a box emission shape, "
               "velocity 80–160 px/s up, and damping 120–180 px/s², the feature Effect A does not use; local_coords off makes the trail, "
               "trail_enabled stays false because the Compatibility renderer does not draw it. previews/run_dust_preview.gd/.tscn is the "
               "strip fixture: the emitter and Rudy's sprite move at 560 px/s from frame 10 and stop at frame 40.",
               lambda p: p.startswith("effects/run_dust") or p.startswith("previews/run_dust_preview")),
  "effects-driver": ("effects/effects_driver.gd, after Rudy in app/main.tscn: each physics tick it starts a new SlashSparks burst on the "
                     "true → false edge of Rudy's SwordHitbox/Shape.disabled, placed on the hitbox and mirrored with facing, and switches "
                     "RunDust's emitting with the run condition (mode PLAY, on the floor, |velocity.x| > 1, visible in the tree), keeping it "
                     "at his soles. content/rudy/rudy.gd owns the event and the condition and is unchanged; project.godot names GL Compatibility.",
                     lambda p: p in ("effects/effects_driver.gd", "app/main.tscn", "content/rudy/rudy.gd", "project.godot")),
  "process-shader": ("shaders/particles_generated.gdshader: the particles shader Godot 4.7.2's editor generated from a copy of Sparks' "
                     "ParticleProcessMaterial, saved by shuai-z; nothing uses it. Line 139 picks each speed between the velocity uniforms, "
                     "line 311 starts the force from gravity.",
                     lambda p: p == "shaders/particles_generated.gdshader"),
  "effects-tests": ("The new headless tests: tests/test_slash_sparks_config.gd (108 checks) and tests/test_run_dust_config.gd (61) compare "
                    "every setting with the brief and scan for Godot 3 names; tests/test_slash_sparks_state.gd/.tscn and "
                    "tests/test_run_dust_state.gd/.tscn (14 each) run the real Main through input actions; tests/cost_effects.gd measures "
                    "the headless CPU price against an empty-scene control.",
                    lambda p: p.startswith("tests/") and (p.startswith("tests/test_slash_sparks") or p.startswith("tests/test_run_dust")
                                                          or p == "tests/cost_effects.gd")),
  "vsync-debug": ("app/vsync_debug.gd, the VsyncDebug node last in Main: F9 turns vsync off and on again, for the FPS fallback when the "
                  "Visual Profiler reports no GPU time.",
                  lambda p: p == "app/vsync_debug.gd"),
}
BASE_REASON = ("The 2D game as Assignment 5 left it (tag a5, 9bd96c5a), copied unchanged into assignment-6/game; Assignment 6 changed none of "
               "it, and this film covers the layer Assignment 6 added. The existing 141 checks in tests/checks.gd and the 15 in "
               "tests/invulnerable_tint_checks guard it, and pass.")


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


def main():
    sheet = json.loads((REEL / "beat_sheet.json").read_text())
    game = A6 / PROJECT
    out = REEL / "checks" / PROJECT
    beats = sheet["beats"]
    narrated = {b["beat_id"] for b in beats if (b.get("narration_text") or "").strip()}
    files, comp_files, exclusions = [], {c: [] for c in COMPONENTS}, []
    for path in inventory(game):
        ids = [c for c, (_, match) in COMPONENTS.items() if match(path)]
        if not ids:
            exclusions.append({"path": path, "reason": BASE_REASON})
            continue
        files.append({"path": path, "sha256": sha(game / path),
                      "role": "import settings" if path.endswith(".import") else path.rsplit(".", 1)[-1], "component_ids": ids})
        for c in ids:
            comp_files[c].append(path)
    comp_beats = {c: [b["beat_id"] for b in beats if b["beat_id"] in narrated and c in b.get("components", [])] for c in COMPONENTS}
    components = [{"id": c, "explanation": e, "beat_ids": comp_beats[c], "files": comp_files[c]} for c, (e, _) in COMPONENTS.items()]
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
            "game": {"name": "walker-rudy assignment-6/game", "revision": meta["game"]["revision"], "folder": "assignment-6/game"},
            "files": files, "components": components, "excerpts": excerpts, "exclusions": exclusions, "code_result_pairs": pairs}
    out.mkdir(parents=True, exist_ok=True)
    (out / "gamedev-evidence.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    (out / "beat_sheet.json").write_text(json.dumps({"metadata": {**meta, "check_note":
        "Copied by tools/make_evidence.py from ../../beat_sheet.json for the game/ check."}, "beats": beats}, indent=1, ensure_ascii=False) + "\n")
    print(f"{PROJECT}: {len(files)} files, {len(exclusions)} exclusions, {len(components)} components, {len(excerpts)} excerpts, {len(pairs)} pairs")


if __name__ == "__main__":
    main()
