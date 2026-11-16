#!/usr/bin/env python3
"""captures.py: every Godot capture of "Making Water in Godot" (CAPTURE-PLAN.md has the table). Run from anywhere:

  python3 captures.py --list                       # the table
  python3 captures.py [--only C01 C05 ...]         # record (default: all) into captures/ (or --dest DIR)
  python3 captures.py --stale                      # list the captures whose recorded length differs from their beat's CURRENT length by more than 0.5 s
  python3 captures.py --size-scale 2               # 4K: 3840x2160 clips and 2160 squares (the Cowork stage records 1920x1080)

Each clip is as long as its beat's MEASURED audio (actual_duration_s in beat_sheet.json) plus a 1.0 s tail; before the audio exists it uses the estimate
(0.34 s per word). EVERY scripted event inside a clip is a fraction of that length, so a clip lands on its words once recorded at the measured length.
Every capture is OFFLINE at a fixed tick rate (lab/capture_shader.sh): it says nothing about real-time frame rate. Renderer is Forward+ unless the
capture says Compatibility. One Lab lock per run (capture_shader.sh takes it); never loop over frames yourself.
Output files are named as the lanes expect (video: "making-water/<name>.mp4"): at build time copy captures/ to
brutalist.art/runtime/remotion/public/making-water/ (BUILD-PROMPT.md).
"""
import argparse, importlib.util, json, os, subprocess, sys
from pathlib import Path

R = Path(__file__).resolve().parent
S = R.parent / "_godot-shaders-series"
LAB = S / "lab"
SC = R / "capture-scenes"
SCENE = str(SC / "water_scene.gd")
GAP = str(SC / "gap_scene.gd")
BLEND = str(R / "evidence/planning-checks/scripts/e3_alpha_scene.gd")
EV = "../evidence/planning-checks/check-shaders/"          # shader paths are relative to lab-shaders/ for the scenes
ORG = R / "evidence" / "capture-logs"
FPS = 30

spec = importlib.util.spec_from_file_location("narration", R / "narration.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)
BODY = {b: t for b, _, t in N.BODY}


def beat_seconds(bid):
    """Measured audio if the beat sheet has it, else the estimate."""
    try:
        for b in json.loads((R / "beat_sheet.json").read_text())["beats"]:
            if b["beat_id"] == bid and b.get("actual_duration_s"):
                return float(b["actual_duration_s"])
    except Exception:
        pass
    return round(len(BODY[bid].split()) * 0.34, 2)


# id, file, beats, scene, env, harness args, size, renderer, kind
# kind: clip | still | pair (two parts side by side) | export | triple
def A(*xs):
    return list(xs)


CAPTURES = [
    dict(id="C01", name="hook", beats=["B01"], env=dict(W_SHADER="06-shore-foam.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0"), args=[], size="1920x1080",
         note="the finished water (stage 06) with the script clock driving waves and floaters"),
    dict(id="C02", name="blue-applied", beats=["B03"], env=dict(W_SHADER="01-blue.gdshader", W_LATE="1"), args=A("--call-at", "0.55f:apply_material"), size="1920x1080",
         note="a plain plane, then the first shader is assigned at 55 % of the beat"),
    dict(id="C03", name="blue-dial", beats=["B04"], env=dict(W_SHADER="01-blue.gdshader"),
         args=A("--set-at", "0.35f:water.water_color=0.12,0.66,0.52", "--set-at", "0.62f:water.water_color=0.45,0.30,0.65", "--set-at", "0.82f:water.water_color=0.10,0.45,0.70"),
         size="1920x1080", note="water_color changed three times: green-teal, violet, back to the default (typed numbers)"),
    dict(id="C04", name="roughness", beats=["B05"], env=dict(W_SHADER="01-blue.gdshader"), args=A("--animate", "water.roughness:0.9:0.03"), size="1920x1080",
         note="roughness 0.9 down to 0.03 (linear across the beat): the sun's reflection tightens"),
    dict(id="C05", name="alpha-switch", beats=["B06"], env=dict(W_SHADER="01-blue.gdshader", W_SHADER2="02-transparent.gdshader"),
         args=A("--call-at", "0.40f:swap_shader", "--animate", "water.opacity:0:1.0,0.40f:1.0,0.70f:0.7,1f:0.7"), size="1920x1080",
         note="stage 01 (solid) swapped for stage 02 at 40 %, opacity 1.0 easing to 0.7"),
    dict(id="C06", name="opacity", beats=["B07"], env=dict(W_SHADER="02-transparent.gdshader"), args=A("--animate", "water.opacity:0:1.0,0.2f:1.0,0.42f:0.3,0.56f:0.3,0.72f:0.7,1f:0.7"), size="1920x1080",
         note="opacity 1.0 to 0.3 (held 0.42 to 0.56) and up to 0.7"),
    dict(id="C07a", name="blend-fp", beats=["B08", "B09"], scene=BLEND, kind="still",
         args=A("--shader", str(R / "evidence/planning-checks/check-shaders/e3-alpha.gdshader"), "--set", "opacity=0.7",
                "--probe-at", "0:0.06,0.5", "--probe-at", "0:0.30,0.5", "--probe-at", "0:0.56,0.5", "--probe-at", "0:0.85,0.5"), size="1280x720", env={},
         note="E3: an unshaded plate (alpha 0.7) over a sand floor, Forward+; probes: floor alone, plate over floor, plate over background, background"),
    dict(id="C07b", name="blend-compat", beats=["B08", "B09"], scene=BLEND, kind="still", renderer="gl_compatibility",
         args=A("--shader", str(R / "evidence/planning-checks/check-shaders/e3-alpha.gdshader"), "--set", "opacity=0.7",
                "--probe-at", "0:0.06,0.5", "--probe-at", "0:0.30,0.5", "--probe-at", "0:0.56,0.5", "--probe-at", "0:0.85,0.5"), size="1280x720", env={},
         note="E3 again in the Compatibility renderer"),
    dict(id="C37", name="sorting", beats=["B11"], env=dict(W_SHADER="02-transparent.gdshader", W_SHADER2="02a-depth-draw-always.gdshader", W_EXTRA="sort"), args=A("--call-at", "0.78f:swap_shader"),
         size="1920x1080", note="a red see-through plane UNDER the water (its node nearer the camera) draws on top of it; at 78 % the water is made to write depth (depth_draw_always) and the red plane vanishes"),
    dict(id="C08", name="foam-points", beats=["B15"], env=dict(W_SHADER="03a-cells-debug.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8", W_SET="show=0;cell_density=8"), args=[],
         size="1080x1080", note="top view, the points of the squares (and the grid); the points circle"),
    dict(id="C09", name="foam-nearest", beats=["B17"], env=dict(W_SHADER="03a-cells-debug.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8", W_SET="show=1;cell_density=8"), args=[],
         size="1080x1080", note="the nearest distance as a grey field of cones"),
    dict(id="C10", name="foam-edge", beats=["B18"], env=dict(W_SHADER="03a-cells-debug.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8", W_SET="show=2;cell_density=8"), args=[],
         size="1080x1080", note="second nearest minus nearest: dark lines along the borders"),
    dict(id="C11", name="foam-width", beats=["B19"], env=dict(W_SHADER="03-noise-foam.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8"), args=A("--animate", "water.edge_width:0:0.02,0.75f:0.1,1f:0.1"),
         size="1080x1080", note="top view of the foam on water; edge_width 0.02 widening to the default 0.1"),
    dict(id="C12", name="foam-matte", beats=["B20"], env=dict(W_SHADER="03-noise-foam.gdshader"), args=A("--animate", "water.foam_roughness:0:0.15,0.15f:0.15,0.85f:0.9,1f:0.9"), size="1920x1080",
         note="foam_roughness 0.15 (glossy foam, the glare streaks along the lines) up to 0.9"),
    dict(id="C13", name="foam-move", beats=["B21"], env=dict(W_SHADER="03-noise-foam.gdshader"),
         args=A("--animate", "water.cell_speed:0:0.0,0.3f:0.0,0.6f:2.0,1f:2.0", "--animate", "water.cell_density:0:10,0.62f:10,1f:18"), size="1920x1080",
         note="cell_speed 0 to 2, then cell_density 10 to 18"),
    dict(id="C14", name="power-curve", beats=["B22"], env=dict(W_SHADER="03b-power-curve.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8", W_SET="clamped=1"),
         args=A("--animate", "water.sharpness:0:2,1f:10"), size="1080x1080", note="one minus nearest distance, to a power (sharpness 2 to 10), clamped"),
    dict(id="C15", name="power-specks", beats=["B23"], env=dict(W_SHADER="03b-power-curve.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8", W_SET="clamped=0;sharpness=5;cell_speed=0"),
         args=A("--set-at", "0.55f:water.clamped=1"), size="1080x1080", note="the same shader unclamped (black specks), clamped at 55 %"),
    dict(id="C16", name="foam-vs-texture", beats=["B24"], kind="pair", size="1080x1080",
         parts=[dict(env=dict(W_SHADER="03-noise-foam.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8"), args=[]),
                dict(env=dict(W_SHADER="03d-foam-from-texture.gdshader", W_BARE="1", W_VIEW="top", W_TOPSIZE="8"), args=[])],
         note="left: the function (stage 03); right: the baked cellular texture (03d). Both top views, same clock"),
    dict(id="C17", name="normal-strength", beats=["B25"], env=dict(W_SHADER="04a-normal-map.gdshader"), args=A("--animate", "water.ripple_strength:0:0,1f:1.5"), size="1920x1080",
         note="ripple_strength 0 to 1.5 on a single static normal map: one glare breaks into glints"),
    dict(id="C18", name="images", beats=["B26", "B27"], kind="export", note="normal_a.png, tiles-not-seamless.png, tiles-seamless.png, cell-texture.png (Godot's own noise textures)"),
    dict(id="C19", name="repeat-switch", beats=["B28"], env=dict(W_SHADER="04e-no-repeat.gdshader", W_SHADER2="04b-scrolling-normals.gdshader"), args=A("--call-at", "0.55f:swap_shader"),
         size="1920x1080", note="repeat_disable (streaks) swapped for repeat_enable at 55 %"),
    dict(id="C20", name="scroll", beats=["B29"], env=dict(W_SHADER="04b-scrolling-normals.gdshader"), args=[], size="1920x1080", note="one scrolling normal map"),
    dict(id="C21", name="two-layers", beats=["B30"], env=dict(W_SHADER="04b-scrolling-normals.gdshader", W_SHADER2="04c-two-layers.gdshader"), args=A("--call-at", "0.50f:swap_shader"),
         size="1920x1080", note="one layer, then two layers moving opposite ways at 50 %"),
    dict(id="C22", name="low-flat", beats=["B31"], env=dict(W_SHADER="04d-warped-foam.gdshader", W_BARE="1", W_VIEW="low"), args=[], size="1280x720", fixed=True,
         note="low camera, flat plane with normal maps: the near edge is one pixel row (487 at 1280 x 720) in every column"),
    dict(id="C23", name="warp", beats=["B32"], env=dict(W_SHADER="04d-warped-foam.gdshader"), args=A("--animate", "water.warp_strength:0:0,1f:0.4"), size="1920x1080",
         note="warp_strength 0 to 0.4"),
    dict(id="C24", name="renderers-ripples", beats=["B33"], kind="pair", size="1080x1080", renderers=["forward_plus", "gl_compatibility"],
         parts=[dict(env=dict(W_SHADER="04d-warped-foam.gdshader"), args=[]), dict(env=dict(W_SHADER="04d-warped-foam.gdshader"), args=[])],
         note="left Forward+, right Compatibility: the same shader, the same clock"),
    dict(id="C25", name="cuts-compare", beats=["B34"], kind="pair", size="1080x1080",
         parts=[dict(env=dict(W_SHADER="05-vertex-waves.gdshader", W_BARE="1", W_VIEW="low", W_CUTS="0"), args=[]),
                dict(env=dict(W_SHADER="05-vertex-waves.gdshader", W_BARE="1", W_VIEW="low", W_CUTS="127"), args=[])],
         note="left: the plane uncut (4 vertices), right: cut 127 x 127 (16,641 vertices): the same wave shader"),
    dict(id="C26", name="waves-low", beats=["B35"], env=dict(W_SHADER="05-vertex-waves.gdshader", W_BARE="1", W_VIEW="low", W_CUTS="127"), args=[], size="1920x1080",
         note="the wave function on the cut plane, low camera, shader TIME"),
    dict(id="C27", name="waves-iso", beats=["B36"], env=dict(W_SHADER="05-vertex-waves.gdshader", W_CUTS="127"), args=[], size="1920x1080", note="vertex waves in the cove (floaters still)"),
    dict(id="C28", name="normal-swap", beats=["B37"], env=dict(W_SHADER="05c-no-normal-update.gdshader", W_SHADER2="05b-synced-clock.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0",
                                                               W_SET="ripple_strength=0;edge_width=0.01;foam_roughness=0.15"), args=A("--call-at", "0.55f:swap_shader"), size="1920x1080",
         note="waves without the normal line (one flat glare), then with it (glints on the crests)"),
    dict(id="C29", name="low-waves", beats=["B38"], env=dict(W_SHADER="05b-synced-clock.gdshader", W_BARE="1", W_VIEW="low", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0"), args=[], size="1280x720", fixed=True,
         note="low camera, real waves: the near edge spans 95 rows in the stills (at 1280 x 720)"),
    dict(id="C30", name="floaters", beats=["B39"], env=dict(W_SHADER="05b-synced-clock.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0"), args=[], size="1920x1080",
         note="buoy and crate ride the waves: a script runs the same function"),
    dict(id="C31", name="wave-dials", beats=["B41"], env=dict(W_SHADER="05b-synced-clock.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0",
                                                             W_DRIVE="wave_height:0:0.12,0.56f:0.12,0.62f:0.25,0.66f:0.06,0.69f:0.12;wave_length:0:3.0,0.69f:3.0,0.78f:6.0,0.84f:3.0;wave_speed:0:0.8,0.84f:0.8,0.95f:2.5"),
         args=[], size="1920x1080", note="wave_height, then wave_length, then wave_speed swept (the driver owns the numbers)"),
    dict(id="C32", name="gap-view", beats=["B43"], env=dict(W_SHADER="06a-gap-view.gdshader", W_CUTS="0"), args=[], size="1920x1080",
         note="the gap (how far the solid scene is under the water) as white near contact lines"),
    dict(id="C33", name="gap-test", beats=["B44"], scene=GAP, env=dict(W_SHADER="06a-gap-view.gdshader", G_STEPS="0:-0.2,0.3f:-0.2,0.55f:-0.9,0.62f:-0.9,0.72f:-0.5,1f:-0.5"), args=[], size="1920x1080",
         note="top-down test: a floor under half the plate held at 0.2 m, lowered to 0.9 m, raised to 0.5 m; measured gap = floor depth (RESULTS.md)"),
    dict(id="C34", name="shore-width", beats=["B46"], env=dict(W_SHADER="06-shore-foam.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0"), args=A("--animate", "water.shore_width:0.05:1.0"),
         size="1920x1080", note="shore_width 0.05 to 1.0 in the finished water"),
    dict(id="C35", name="compat-branch", beats=["B47"], renderer="gl_compatibility",
         env=dict(W_SHADER="06-shore-foam.gdshader", W_SHADER2="06b-no-renderer-branch.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0"), args=A("--call-at", "0.66f:swap_shader"),
         size="1920x1080", note="Compatibility: the real stage 06 (foam only at the shore), swapped at 66 % for the version without the renderer branch (foam everywhere)"),
    dict(id="C36", name="restyle", beats=["B49"], kind="triple", size="1080x1080",
         parts=[dict(label="lagoon", env=dict(W_SHADER="06-shore-foam.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0",
                                              W_SET="water_color=0.05,0.58,0.62;opacity=0.55;edge_width=0.05;cell_density=14;wave_height=0.05;ripple_strength=0.6"), args=[]),
                dict(label="pond", env=dict(W_SHADER="06-shore-foam.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0",
                                            W_SET="water_color=0.10,0.28,0.18;opacity=0.92;edge_width=0.01;wave_height=0.03;ripple_strength=0.5;shore_width=0.15"), args=[]),
                dict(label="storm", env=dict(W_SHADER="06-shore-foam.gdshader", W_CUTS="127", W_FOLLOW="1", W_CLOCK0="1.0",
                                             W_SET="water_color=0.28,0.36,0.44;opacity=0.85;edge_width=0.15;cell_density=8;wave_height=0.20;wave_length=3.4;wave_speed=1.8;ripple_strength=1.2;roughness=0.3;shore_width=0.9"), args=[])],
         note="the same shader, three sets of numbers: Lagoon, Pond, Storm"),
]


def run_one(c, part_env, part_args, name, dest, size, renderer, still, length, scene=None):
    env = dict(os.environ)
    env.update(part_env or {})
    env["W_ID"] = c["id"]
    env["CLIP_L"] = f"{length:.2f}"
    cmd = [str(LAB / "capture_shader.sh"), "--scene", scene or c.get("scene") or SCENE, "--length", f"{length:.2f}", "--size", size, "--warmup", "60"]
    if not still:
        cmd += ["--tail", "1.0"]
    cmd += list(part_args or []) + ["--name", name, "--dest", str(dest)]
    if still:
        cmd += ["--png", "1"]
    if renderer:
        cmd += ["--renderer", renderer]
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    ORG.mkdir(parents=True, exist_ok=True)
    (ORG / f"{name}.log").write_text(" ".join(cmd) + "\n" + (" ".join(f"{k}={v}" for k, v in env.items() if k.startswith(('W_', 'G_', 'CLIP'))) + "\n") + r.stdout + r.stderr)
    res = [l for l in r.stdout.splitlines() if l.startswith("RESULT")]
    j = json.loads(res[0][7:]) if res else {}
    ok = bool(j.get("ok")) and "WROTE" in r.stdout and "SHADER_OR_SCRIPT_ERROR" not in r.stdout
    print(f"  {name}: {'ok' if ok else 'FAILED ' + (r.stdout + r.stderr)[-300:]}  {length:.2f}s {renderer or 'forward_plus'}", [(p['t'], p['at'], [round(v * 255) for v in p['rgba'][:3]]) for p in j.get('probes', [])] or "", flush=True)
    return ok, j


def scale_size(size, k):
    w, h = size.split("x")
    return f"{int(w) * k}x{int(h) * k}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--stale", action="store_true")
    ap.add_argument("--rebuild-manifest", action="store_true", help="rewrite MANIFEST.json from the files in --dest (length = file duration - 1.0 s tail)")
    ap.add_argument("--dest", default=str(R / "captures"))
    ap.add_argument("--size-scale", type=int, default=1)
    a = ap.parse_args()
    if a.list:
        for c in CAPTURES:
            L = max(beat_seconds(b) for b in c["beats"]) if c.get("kind") != "export" else 0
            print(f"{c['id']:5} {c['name']:18} beats {','.join(c['beats']):8} {L:5.1f}s {c.get('kind', 'clip'):7} {c.get('renderer', '')}  {c['note']}")
        return 0
    if a.rebuild_manifest:
        man = {}
        for c in CAPTURES:
            f = Path(a.dest) / (c["name"] + (".png" if c.get("kind") == "still" else ".mp4"))
            if c.get("kind") == "export" or not f.exists():
                continue
            if f.suffix == ".mp4":
                d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout)
                man[c["id"]] = dict(name=c["name"], ok=True, seconds=round(d - 1.0, 2))
            else:
                man[c["id"]] = dict(name=c["name"], ok=True, seconds=0.1)
        (Path(a.dest) / "MANIFEST.json").write_text(json.dumps(man, indent=2))
        print("rebuilt", len(man), "entries")
        return 0
    if a.stale:
        man = json.loads((Path(a.dest) / "MANIFEST.json").read_text()) if (Path(a.dest) / "MANIFEST.json").exists() else {}
        stale = []
        for c in CAPTURES:
            if c.get("kind") in ("export", "still"):
                continue
            now = max(beat_seconds(b) for b in c["beats"])
            was = (man.get(c["id"]) or {}).get("seconds")
            if was is None or abs(now - was) > 0.5:
                stale.append((c["id"], c["name"], was, round(now, 2)))
        for sid, nm, was, now in stale:
            print(f"{sid:5} {nm:18} recorded {was}  beat now {now}")
        print("python3 captures.py --only " + " ".join(x[0] for x in stale) if stale else "none stale")
        return 0
    dest = Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    tmp = Path("/private/tmp/claude-501/water-parts")
    tmp.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for c in CAPTURES:
        if a.only and c["id"] not in a.only and c["name"] not in a.only:
            continue
        kind = c.get("kind", "clip")
        print(c["id"], c["name"], flush=True)
        if kind == "export":
            r = subprocess.run(["godot", "--headless", "--path", str(R / "water-project"), "--script", str(SC / "export_images.gd"), "--", str(dest)], capture_output=True, text=True)
            print("  ", [l for l in r.stdout.splitlines() if l.startswith("EXPORT")])
            continue
        length = max(beat_seconds(b) for b in c["beats"])
        size = (c["size"] if c.get("fixed") else scale_size(c["size"], a.size_scale)) if c.get("size") else None
        if kind in ("clip", "still"):
            ok, j = run_one(c, c.get("env"), c.get("args"), c["name"], dest, size or "1280x720", c.get("renderer"), kind == "still", 0.1 if kind == "still" else length)
            manifest[c["id"]] = dict(name=c["name"], ok=ok, seconds=length, probes=j.get("probes"), renderer=j.get("renderer"))
        else:   # pair or triple: parts recorded separately, joined side by side with ffmpeg (a real composite of real renders)
            outs = []
            for i, p in enumerate(c["parts"]):
                rend = (c.get("renderers") or [None] * 9)[i] if c.get("renderers") else c.get("renderer")
                nm = f"{c['name']}__{i}"
                ok, j = run_one(c, p.get("env"), p.get("args"), nm, tmp, size, rend, False, length)
                outs.append(tmp / f"{nm}.mp4")
            cmd = ["ffmpeg", "-y", "-loglevel", "error"]
            for o in outs:
                cmd += ["-i", str(o)]
            cmd += ["-filter_complex", f"hstack=inputs={len(outs)}", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dest / f"{c['name']}.mp4")]
            subprocess.run(cmd, check=True)
            for o in outs:
                o.unlink(missing_ok=True)
            print("  joined ->", dest / f"{c['name']}.mp4", flush=True)
            manifest[c["id"]] = dict(name=c["name"], ok=True, seconds=length, parts=len(outs))
    mp = dest / "MANIFEST.json"
    old = json.loads(mp.read_text()) if mp.exists() else {}
    old.update(manifest)
    mp.write_text(json.dumps(old, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
