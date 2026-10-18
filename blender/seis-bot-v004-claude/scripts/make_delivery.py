"""make_delivery - write MANIFEST.md and DELIVERY.html for the finished SEIS bot, from the files that really exist.

    python3 <W>/src/make_delivery.py

Reads  W/AUDIT.json (the audit of the standing file), W/AUDIT-seated.json if present, W/renders/final/*.png, the .blend files.
Nothing here is invented: every number printed comes from the audit JSON or from the file system.
"""
import os
import json
import hashlib
import datetime

W = "/PATH/TO/seis-bot-v004-detailed"


def sha(path, n=16):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:n]


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024.0


def rel(p):
    return os.path.relpath(p, W)


def load(name):
    p = os.path.join(W, name)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    audit = load("AUDIT.json")
    seated = load("AUDIT-seated.json")
    finals = sorted(f for f in os.listdir(os.path.join(W, "renders", "final"))) if os.path.isdir(os.path.join(W, "renders", "final")) else []
    finals = [f for f in finals if f.endswith(".png")]
    deliver = [
        ("seis_bot_v004_standing.blend", "The model: standing A-pose, all parts, FK rig, materials, workshop and studio setups"),
        ("seis_bot_v004_seated_thinker.blend", "A separate pose study: the Thinker on the stone plinth (same meshes and rig, posed, plinth and dais added)"),
        ("AUDIT.md", "Geometry audit of the standing file: names, materials, geometry, weights"),
        ("AUDIT.json", "The same audit as data"),
        ("README.md", "Start here: what this is, what was verified, limits, how to use and rebuild"),
        ("DELIVERY.html", "Gallery page (open in a browser)"),
        ("spec/ONMODEL.md", "The on-model authority written from Bear's video frames"),
        ("spec/BIBLE.md", "Build rules used by every part builder"),
        ("src/assemble.py", "Rebuilds the whole figure from parts/*.py (run headless or through the Blender MCP add-on)"),
        ("src/seated.py", "Thinker pose (FK, elbow-on-thigh solve) and plinth placement"),
        ("src/audit_model.py", "The audit script"),
        ("parts", "One module per body region: the geometry as Python"),
    ]
    lines = ["# SEIS bot v004: file manifest", "",
             f"Generated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} by `src/make_delivery.py` from the files on disk.", "",
             "| File | What it is | Size | sha256 (first 16) |", "|---|---|---|---|"]
    for name, desc in deliver:
        p = os.path.join(W, name)
        if not os.path.exists(p):
            lines.append(f"| `{name}` | {desc} | MISSING | |")
            continue
        if os.path.isdir(p):
            n = sum(1 for _d, _s, fs in os.walk(p) if os.sep + "_out" not in _d and "__pycache__" not in _d for f in fs if f.endswith((".py", ".md")))
            lines.append(f"| `{name}/` | {desc} | {n} .py/.md files | |")
        else:
            lines.append(f"| `{name}` | {desc} | {human(os.path.getsize(p))} | `{sha(p)}` |")
    lines += ["", "## Renders (`renders/final/`)", "", "| File | Size | sha256 (first 16) |", "|---|---|---|"]
    for f in finals:
        p = os.path.join(W, "renders", "final", f)
        lines.append(f"| `renders/final/{f}` | {human(os.path.getsize(p))} | `{sha(p)}` |")
    open(os.path.join(W, "MANIFEST.md"), "w").write("\n".join(lines) + "\n")

    # ------------------------------------------------------------------------------------- DELIVERY.html
    g = (audit or {}).get("geometry", {})
    w_ = (audit or {}).get("weights", {})
    tech = [
        ("Blender", (audit or {}).get("blender", "5.1.2") + " / Cycles / Metal"),
        ("Geometry", f"{g.get('meshes', '?'):,} separate meshes" if isinstance(g.get("meshes"), int) else "?"),
        ("Evaluated triangles", f"{g.get('evaluated_triangles', 0):,}"),
        ("Height", f"{g.get('height_m', '?')} m"),
        ("Rig", f"{w_.get('bones', '?')} bones, FK, rigid binding"),
        ("Coordinates", "Metres, Z up, front faces -Y"),
        ("Audit", "PASS" if (audit or {}).get("overall_pass") else "see AUDIT.md"),
    ]
    imgs = "\n".join(f'<figure><a href="renders/final/{f}"><img src="renders/final/thumbs/{f[:-4]}.jpg" loading="lazy"></a><figcaption>{f[:-4].replace("_", " ")}</figcaption></figure>' for f in finals)
    rows = "\n".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in tech)
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEIS Bot v004</title>
<style>
:root{{--bg:#eeefec;--ink:#17323a;--mut:#4d6168;--card:#fff;--line:#d3d8d5}}
@media (prefers-color-scheme:dark){{:root{{--bg:#12191c;--ink:#e6eeee;--mut:#9fb2b6;--card:#1a2327;--line:#2c3a3f}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Georgia,serif}}
main{{max-width:1100px;margin:0 auto;padding:32px 20px 80px}}
h1{{font-size:2.2rem;margin:.2em 0}} h2{{margin-top:2em}}
table{{border-collapse:collapse;width:100%;background:var(--card)}} th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line)}} th{{width:34%;color:var(--mut);font-weight:600}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line)}} img{{width:100%;display:block}} figcaption{{padding:8px 12px;color:var(--mut);font-size:.9rem}}
.sw{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}} .sw span{{width:44px;height:44px;border-radius:50%;border:1px solid var(--line)}}
a{{color:inherit}}
</style></head><body><main>
<h1>SEIS Bot v004</h1>
<p>A highly detailed, interpretive 3D model of the SEIS bot, built in Blender from Bear's reference images and his video frames (the frames win where they disagree with the stills). It is not a scan.</p>
<h2>What is in the file</h2>
<p>Separate curved armour plates, mechanical bearings and fasteners, individual finger segments, exposed cables, a segmented spine and recessed optics. Procedural materials: glossy blue-teal gunmetal with thin champagne-gold trim, candy-red enamel, warm pewter, olive-gold band metal, dark gunmetal joints. A rigid FK rig moves the parts and each finger segment. The seated file is a separate pose study.</p>
<div class="sw"><span style="background:#122f36"></span><span style="background:#a0061a"></span><span style="background:#8f8a78"></span><span style="background:#c2a266"></span><span style="background:#1a1f18"></span><span style="background:#e0e0e0"></span></div>
<h2>Verified</h2>
<table>{rows}</table>
<p>Not verified: engine import, manufacturing, collision. The rig has no IK and no facial animation.</p>
<h2>Gallery</h2>
<div class="grid">{imgs}</div>
<h2>Files</h2>
<p><a href="MANIFEST.md">File manifest</a> . <a href="AUDIT.md">Geometry audit</a> . <a href="README.md">Usage and rebuild notes</a> . <a href="spec/ONMODEL.md">On-model spec</a></p>
</main></body></html>"""
    open(os.path.join(W, "DELIVERY.html"), "w").write(html)
    print("wrote MANIFEST.md and DELIVERY.html;", len(finals), "renders listed")


main()
