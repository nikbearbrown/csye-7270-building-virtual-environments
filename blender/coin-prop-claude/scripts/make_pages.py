"""Write README.md, BUILD_NOTES.md and a self-contained index.html for one blender/<folder>/ from a single pages.json,
so the three pages cannot drift apart.

  python3 -I make_pages.py <model-folder>        (reads <model-folder>/pages.json; run it twice so Download sizes are filled in)

pages.json keys (all strings unless noted):
  folder, title, builder_name, tagline, stats, description
  files: [{"name": "x.blend", "purpose": "...", "note": "optional"}]      (must exist in the folder, except index/README)
  views: [{"file": "renders/web/front.jpg", "title": "Front", "text": "one sentence"}]
  compares: [{"file": "compare/x.jpg", "title": "...", "text": "..."}]    (may be empty; then compare_note explains why)
  compare_note: shown when compares is empty
  reference_label: e.g. "Reference" (used in the viewer grid)
  built_by: {"builder", "method", "tools", "date", "review"}
  limitations: [str]
  build_notes: markdown body for BUILD_NOTES.md
  glb_note: sentence about textures/flat colours (or "" if no glb)
"""
import base64
import io
import json
import sys
from html import escape
from pathlib import Path

from PIL import Image

root = Path(sys.argv[1]).resolve()
P = json.loads((root / "pages.json").read_text())
FOLDER = P["folder"]
REPO = "https://github.com/nikbearbrown/csye-7270-building-virtual-environments"
RAW = f"{REPO}/raw/main/blender/{FOLDER}"
PAGES = f"https://nikbearbrown.github.io/csye-7270-building-virtual-environments/blender/{FOLDER}/"
FALLBACK = f"https://htmlpreview.github.io/?{RAW}/index.html"
B = P["built_by"]


def size(rel):
    p = root / rel
    if not p.exists():
        return "this page"
    n = p.stat().st_size
    return f"{n / 1e6:.1f} MB" if n >= 1e6 else f"{max(1, round(n / 1e3))} KB"


for item in P["views"] + P.get("compares", []):
    assert (root / item["file"]).exists(), item["file"]
for f in P["files"]:
    assert f["name"] in ("index.html", "README.md", "BUILD_NOTES.md") or (root / f["name"]).exists(), f["name"]

built_by_md = (f"- **Builder:** {B['builder']}\n- **Method:** {B['method']}\n- **Tools:** {B['tools']}\n"
               f"- **Build date:** {B['date']}\n- **Human review:** {B['review']}")

# ---------------- README ----------------
L = [f"# {P['title']}", "", f"*{P['tagline']}*", "", f"`{P['stats']}`", "", P["description"], "", "## Views", ""]
for v in P["views"]:
    full = v.get("full", v["file"])
    L += [f"### {v['title']}", "", v["text"], "", f"<img src=\"{v['file']}\" width=\"720\" alt=\"{escape(v['title'])}\">", "",
          f"[Full-size file]({full})", ""]
L += ["## Compare with references", ""]
if P.get("compares"):
    for c in P["compares"]:
        L += [f"### {c['title']}", "", c["text"], "", f"<img src=\"{c['file']}\" width=\"720\" alt=\"{escape(c['title'])}\">", "",
              f"[Full-size file]({c.get('full', c['file'])})", ""]
else:
    L += [P.get("compare_note", "No reference comparison was made for this model."), ""]
L += ["## Film", "", "Companion film: coming soon", "", "<!-- FILM_URL -->", "", "## Download", "",
      "| File | Size | What it is | Download |", "|---|---|---|---|"]
for f in P["files"]:
    L.append(f"| `{f['name']}` | {size(f['name'])} | {f['purpose']} | [download]({RAW}/{f['name']}) |")
L += ["", P.get("glb_note", ""), "", "## How to import into Blender", "",
      "- **`.blend`:** open it in Blender 4.2 or later (File > Open). " + P.get("blend_note", ""),
      "- **`.glb`:** in Blender, File > Import > glTF 2.0 (.glb/.gltf), or drop it into a game engine or a web viewer.", "",
      "## Viewer", "", f"A self-contained interactive viewer is in [`index.html`](index.html) (images embedded, works offline once downloaded):", "",
      f"- GitHub Pages: {PAGES} (works once Pages is enabled for the repo)",
      f"- Fallback through htmlpreview: {FALLBACK}", "", "## Built by", "", built_by_md, "", "## Honest limitations", ""]
L += [f"- {x}" for x in P["limitations"]]
(root / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")

# ---------------- BUILD_NOTES ----------------
(root / "BUILD_NOTES.md").write_text(f"# Build notes: {P['title']}\n\n`{P['stats']}`\n\n{P['build_notes']}\n\n## Built by\n\n{built_by_md}\n\n"
                                     "## Known limitations\n\n" + "\n".join(f"- {x}" for x in P["limitations"]) + "\n", encoding="utf-8")


# ---------------- index.html ----------------
def embed(rel, maxw=1100, q=82):
    im = Image.open(root / rel).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


budget = 4.6e6
n_img = len(P["views"]) + len(P.get("compares", []))
maxw = 1100 if n_img <= 10 else 1000 if n_img <= 16 else 900
views = [{"t": v["title"], "c": v["text"], "src": embed(v["file"], maxw)} for v in P["views"]]
comps = [{"t": c["title"], "c": c["text"], "src": embed(c["file"], maxw)} for c in P.get("compares", [])]
while sum(len(v["src"]) + 0 for v in views + comps) > budget and maxw > 640:
    maxw -= 100
    views = [{"t": v["title"], "c": v["text"], "src": embed(v["file"], maxw)} for v in P["views"]]
    comps = [{"t": c["title"], "c": c["text"], "src": embed(c["file"], maxw)} for c in P.get("compares", [])]

data = json.dumps({"views": views, "comps": comps}).replace("</", "<\\/")
dl_rows = "".join(f"<tr><td><a href=\"{RAW}/{escape(f['name'])}\"><code>{escape(f['name'])}</code></a></td><td>{size(f['name'])}</td>"
                  f"<td>{escape(f['purpose'])}</td></tr>" for f in P["files"])
lim = "".join(f"<li>{escape(x)}</li>" for x in P["limitations"])
bb = "".join(f"<li><b>{k}:</b> {escape(v)}</li>" for k, v in
             (("Builder", B["builder"]), ("Method", B["method"]), ("Tools", B["tools"]), ("Build date", B["date"]), ("Human review", B["review"])))
cmp_html = ("<h2>Compare with references</h2><div id=\"grid\"></div>" if comps else
            f"<h2>Compare with references</h2><p>{escape(P.get('compare_note', 'No reference comparison was made for this model.'))}</p>")

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title><style>
:root{--bg:#fafaf7;--fg:#1d1d1b;--mu:#66655f;--bd:#d9d8d0;--ac:#b03a2e;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#17171a;--fg:#ececea;--mu:#9a9a95;--bd:#34343a;--ac:#e8836f;--card:#202025}}
:root[data-theme=dark]{--bg:#17171a;--fg:#ececea;--mu:#9a9a95;--bd:#34343a;--ac:#e8836f;--card:#202025}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,sans-serif}
main{max-width:1000px;margin:0 auto;padding:20px 16px 60px}h1{margin:.2em 0 .1em}h2{margin-top:1.8em;border-bottom:1px solid var(--bd);padding-bottom:.2em}
.stats{font:13px ui-monospace,Menlo,monospace;color:var(--mu)}a{color:var(--ac)}
#btns{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0}#btns button,.th{cursor:pointer}
#btns button{background:var(--card);color:var(--fg);border:1px solid var(--bd);border-radius:6px;padding:5px 10px;font:inherit;font-size:14px}
#btns button.on{background:var(--ac);color:#fff;border-color:var(--ac)}
#stage{width:100%;border:1px solid var(--bd);border-radius:8px;background:var(--card);display:block}
#cap{color:var(--mu);margin:.6em 0}#strip{display:flex;gap:6px;overflow-x:auto;padding:4px 0}
.th{height:64px;border:2px solid transparent;border-radius:4px}.th.on{border-color:var(--ac)}
.g{margin:18px 0}.g img{width:100%;border:1px solid var(--bd);border-radius:8px}.g p{color:var(--mu);margin:.3em 0}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--bd);padding:6px;text-align:left;vertical-align:top;font-size:14px}
#theme{float:right;background:var(--card);color:var(--fg);border:1px solid var(--bd);border-radius:6px;padding:4px 10px;cursor:pointer}
@media (max-width:600px){h1{font-size:1.4em}td,th{font-size:13px}}</style></head><body><main>
<button id="theme" onclick="tg()">Light/dark</button>
<h1>__TITLE__</h1><div class="stats">__STATS__</div><p>__DESC__</p>
<div id="btns"></div><img id="stage" alt=""><p id="cap"></p><div id="strip"></div>
__CMP__
<h2>Film</h2><p id="film">Companion film: coming soon.</p>
<h2>Download</h2><table><tr><th>File</th><th>Size</th><th>What it is</th></tr>__DL__</table><p>__GLB__</p>
<h2>How to import into Blender</h2><ul><li>Open the <code>.blend</code> in Blender 4.2 or later (File &gt; Open).</li>
<li>For the <code>.glb</code>: File &gt; Import &gt; glTF 2.0, or drop it into a game engine or web viewer.</li></ul>
<h2>Built by</h2><ul>__BB__</ul>
<h2>Honest limitations</h2><ul>__LIM__</ul>
<p class="stats">Folder: <a href="__REPO__/tree/main/blender/__FOLDER__">__FOLDER__</a></p>
</main><script>
const FILM_URL="";
const D=__DATA__;let i=0;
const $=s=>document.querySelector(s);
function tg(){const r=document.documentElement;const d=r.dataset.theme==="dark"||(r.dataset.theme!=="light"&&matchMedia("(prefers-color-scheme:dark)").matches);r.dataset.theme=d?"light":"dark"}
function show(n){i=(n+D.views.length)%D.views.length;const v=D.views[i];$("#stage").src=v.src;$("#stage").alt=v.t;$("#cap").textContent=v.t+": "+v.c;
document.querySelectorAll("#btns button").forEach((b,k)=>b.classList.toggle("on",k==i));document.querySelectorAll(".th").forEach((b,k)=>b.classList.toggle("on",k==i))}
D.views.forEach((v,k)=>{const b=document.createElement("button");b.textContent=v.t;b.onclick=()=>show(k);$("#btns").appendChild(b);
const t=document.createElement("img");t.src=v.src;t.className="th";t.onclick=()=>show(k);$("#strip").appendChild(t)});
const g=$("#grid");if(g)D.comps.forEach(c=>{const d=document.createElement("div");d.className="g";d.innerHTML="<h3></h3><img><p></p>";d.querySelector("h3").textContent=c.t;d.querySelector("img").src=c.src;d.querySelector("p").textContent=c.c;g.appendChild(d)});
if(FILM_URL){$("#film").innerHTML='<a href="'+FILM_URL+'">Watch the companion film</a>'}
addEventListener("keydown",e=>{if(e.key==="ArrowRight")show(i+1);if(e.key==="ArrowLeft")show(i-1)});show(0);
</script></body></html>"""
for k, v in {"__TITLE__": escape(P["title"]), "__STATS__": escape(P["stats"]), "__DESC__": escape(P["description"]), "__CMP__": cmp_html,
             "__DL__": dl_rows, "__GLB__": escape(P.get("glb_note", "")), "__BB__": bb, "__LIM__": lim, "__REPO__": REPO,
             "__FOLDER__": FOLDER}.items():
    HTML = HTML.replace(k, v)
HTML = HTML.replace("__DATA__", data)
(root / "index.html").write_text(HTML, encoding="utf-8")
print("wrote README.md BUILD_NOTES.md index.html", f"({(root / 'index.html').stat().st_size / 1e6:.2f} MB, img width {maxw})")
