#!/usr/bin/env python3
"""_gen_capture_plan.py: writes CAPTURE-PLAN.md from captures.py (the table cannot drift from the recorder)."""
import importlib.util
from pathlib import Path
R = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("captures", R / "captures.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

MARKS = {  # id: (what is visible at the 50 % mark, at the 85 % mark, verified result to reproduce)
    "C01": ("waves rolling, buoy and crate on crests, foam net, white shore edge", "same, a different phase", "16,641 vertices; the smoke run (tools/smoke.gd) shows the same picture"),
    "C02": ("pale plane just before the shader lands (55 %)", "solid blue plane with the sun's glare", "shader assigned at 55 %"),
    "C03": ("teal-green water (set at 35 %, held to 62 %)", "default blue again (set at 82 %)", "typed 0.10, 0.45, 0.70 reads 25, 115, 178 (E1)"),
    "C04": ("glare about half its first width", "tight bright oval", "roughness 0.9 to 0.03 linear"),
    "C05": ("opacity easing from 1.0 (the swap came at 40 %): floor starting to show", "sand, rock and buoy underside clearly under the water", "swap at 40 %"),
    "C06": ("opacity held at 0.3 (42 to 56 %)", "opacity 0.7 settled", "holds at 1.0, 0.3, 0.7"),
    "C07a": ("a still", "a still", "probes (x across, y 0.5): 0.06 (184, 157, 110), 0.30 (108, 129, 162), 0.56 (128, 153, 186), 0.85 (217, 213, 202)"),
    "C07b": ("a still", "a still", "probes: 0.30 (71, 128, 158), 0.56 (81, 145, 186)"),
    "C08": ("grid with a dot in each square, dots circling", "same", "no black or white fields: pale squares, deep-blue dots"),
    "C09": ("cones: pale at points, deepening away", "same", "mean nearest distance 0.429 (E7)"),
    "C10": ("pale net on deep cells", "same", "mean second-minus-nearest 0.261"),
    "C11": ("foam bands widening (edge_width about 0.06 to 0.08)", "edge_width 0.1 settled: 12.8 % foam", "foam coverage 6.6 / 12.8 / 24.4 / 34.9 % at 0.05 / 0.1 / 0.2 / 0.3"),
    "C12": ("foam_roughness near 0.15 to 0.3: glare fans on the foam", "foam_roughness 0.9: flat white foam", "glare fans fade as roughness rises"),
    "C13": ("cell_speed rising", "density rising toward 18", "net breathes faster, then cells shrink"),
    "C14": ("soft blobs at mid power", "tiny glitter dots at power near 10", "clamped: 0 black pixels"),
    "C15": ("unclamped: black specks (clamp lands at 55 %)", "clamped: no specks", "462 black pixels in the unclamped frame (4 specks: 258, 167, 22, 15); ring on the 258-px speck at (221, 545) of 1080 x 1080"),
    "C16": ("left crisp net, right net with a smudge in the middle", "same", "texture min 0.000 with fractal None"),
    "C17": ("glare breaking into glints", "dense glints (strength 1.4)", "ripple_strength 0 to 1.5"),
    "C18": ("(images)", "(images)", "normal_a.png mean lean 3.4 deg, max 12.8 deg; seam jump 0.353 against 0.0067 (53 times) not seamless, 0.0063 seamless"),
    "C19": ("streaks across the water (swap at 55 %)", "fine ripples", "swap at 55 %"),
    "C20": ("glints drifting", "same", "one layer"),
    "C21": ("one steady drift (swap at 50 %)", "crossing shimmer", "swap at 50 %"),
    "C22": ("flat plane edge-on, glints moving", "same, edges straight", "near edge row 487 in every column at 1280 x 720 (spread 0)"),
    "C23": ("warp about 0.2: net bending", "warp near 0.34: net sloshing", "warp 0 to 0.4"),
    "C24": ("two scenes in step", "same", "median red 132 (Forward+) against 100 (Compatibility)"),
    "C25": ("left plane tilting, right plane rolling", "same", "4 and 16,641 vertices"),
    "C26": ("lumpy rolling surface", "same", "wave() with TIME"),
    "C27": ("rolling waves, shoreline wobbling", "same", "TIME from the capture start"),
    "C28": ("one flat glare (swap at 55 %)", "glints on the crests", "swap at 55 %"),
    "C29": ("rolling near edge", "same", "near edge rows 440 to 535 (95 px) in the stills; re-measured on the clip: logs/edge-spread.txt"),
    "C30": ("buoy and crate riding the waves", "same", "water_driver.gd: floaters at WaveMath.height"),
    "C31": ("waves at default (the sweeps start at 56 %)", "wave_speed rising", "the driver owns the numbers"),
    "C32": ("white along the beach edge, rocks and floaters", "same", "gap map"),
    "C33": ("floor held at 0.2 m, lowering (the lowering runs 30 to 55 %)", "floor rising back to 0.5 m", "gap 0.200, 0.500, 0.902 m (E8b)"),
    "C34": ("a ragged white band, wide", "wider band", "shore_width 0.05 to 1.0"),
    "C35": ("Compatibility: foam only at the shore", "Compatibility: the whole surface foam (swap at 66 %)", "gap 0.494 m with the branch, 0.000 m without (E8)"),
    "C36": ("three looks side by side", "same", "same file in all three"),
    "C37": ("red plane drawn over the water (swap at 78 %)", "red plane gone", "E16: 56,099 pixels differ by more than 8 levels"),
}
rows = []
for c in C.CAPTURES:
    kind = c.get("kind", "clip")
    m = MARKS[c["id"]]
    envs = c.get("env") or (c["parts"][0].get("env") if c.get("parts") else {})
    sh = envs.get("W_SHADER", "")
    if c.get("parts"):
        sh = " | ".join(p["env"].get("W_SHADER", p.get("label", "")) for p in c["parts"] if p.get("env"))
    L = max(C.beat_seconds(b) for b in c["beats"]) if kind != "export" else 0
    extras = ", ".join(f"{k}={v}" for k, v in envs.items() if k not in ("W_SHADER",))
    rows.append(f"| {c['id']} | {c['name']} | {', '.join(c['beats'])} | `{sh}` | {kind} · {c.get('size', '')} · {c.get('renderer') or ('Forward+ and Compatibility' if c.get('renderers') else 'Forward+')} | {extras} {' '.join(c.get('args') or []) if kind in ('clip', 'still') else ''} | {L:.1f} s | {m[0]} | {m[1]} | {m[2]} |")
head = """# Capture plan: Making Water in Godot

**What this is.** Every Godot capture of the film: its id, the beats it serves, the shader, how the scene is configured (environment variables read by `capture-scenes/water_scene.gd`), what must be visible at 50 and 85 percent of the beat, and the verified result to reproduce.
**Why.** The build session records again after the audio exists, so each clip is as long as its beat's measured audio and every scripted event lands on its words. This table is generated from `captures.py` (`_gen_capture_plan.py`), so it cannot drift from the recorder.
**Found.** 38 rows, C01 to C37 (C07 is two stills): single clips, side-by-side composites (C16, C24 and C25 are pairs, C36 is a triple), two stills and one image export. All were recorded in the Cowork stage at 1080p at ESTIMATED durations into `captures/` and looked at (contact sheets). Nothing needs a human; nothing needs the Godot editor except B48 (done by the series editor driver; frames in `captures/editor/`).

## How to record (all from `books/`)

```bash
python3 csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/captures.py --list
python3 csye-7270-building-virtual-environments/youtube/claude-liam-lecture-making-water-in-godot/captures.py [--only C05 C11 ...] [--size-scale 2]
```

Every capture is OFFLINE at a fixed tick rate (the Lab harness, `--fixed-fps 30`): it says nothing about real-time frame rate. TIME in a clip advances exactly one frame step per frame (after a constant 0.026 s start offset measured in E2; no beat depends on it: the wave clock is the script's own). The renderer is Forward+ unless the row says Compatibility. One Lab lock per run (`capture_shader.sh` takes it): never loop over frames yourself. **C22 and C29 carry measured pixel rows (487 and 95) at 1280 x 720: record them with `--size-scale 1` only, or restate the numbers.** The scenes: `water_scene.gd` (THE COVE), `gap_scene.gd` (the depth test), `evidence/planning-checks/scripts/e3_alpha_scene.gd` (the blend test). `W_FOLLOW=1` drives `wave_clock` and the floaters from the capture clock (`water_driver.gd`).

| id | file (making-water/<name>.mp4) | beats | shader | kind, size, renderer | settings | seconds (estimate; measured audio when it exists) | at 50 % | at 85 % | verified result to reproduce |
|---|---|---|---|---|---|---|---|---|---|
"""
tail = """
## Editor frames (B48)

Recorded by the series editor driver (`../_godot-shaders-series/editor-capture/`) in a scratch copy of `water-project/` (never in the project itself): `captures/editor/W1-...` to `W5-...` and `captures/editor-inspector.png`, with every exact label in `evidence/planning-checks/EDITOR-LABELS.md`. State scripts: `capture-scenes/editor-states/`. Label the clip 'scripted editor session'. Nobody records a screen by hand.

## The two renderer-labelled comparisons

C07a and C07b (the blend test) and C24 (the ripple shader) are the only captures made in both renderers on purpose; C35 is Compatibility only. Every other capture is Forward+.
"""
(R / "CAPTURE-PLAN.md").write_text(head + "\n".join(rows) + "\n" + tail)
print(len(rows))
