"""Build the B09 (README key table) and B12 (test output) frames as HTML, then screenshot them with headless Edge.
The text in both pages is copied verbatim from the files; nothing is retyped by hand."""
import html, os, re, subprocess, sys

README = sys.argv[1]      # pitch/README.md (English)
LOGS = sys.argv[2]        # folder with b12-<test>.txt outputs
OUT = sys.argv[3]         # output folder
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
TESTS = ["a3_asset_check", "screen_glow_check", "test_landing_dust_config",
         "test_landing_dust_events", "test_light_dust_config", "test_light_dust_state"]

BASE_CSS = """
body{margin:0;width:1920px;height:1080px;overflow:hidden;font-family:'Segoe UI',Arial,sans-serif}
.tag{position:absolute;right:40px;bottom:28px;font:600 22px 'Segoe UI',Arial;letter-spacing:.06em;padding:8px 14px;border-radius:6px}
"""


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", s)


def readme_page():
    text = open(README, encoding="utf-8").read()
    sec = text.split("## Keys", 1)[1].split("\n## ", 1)[0]
    rows, before, after = [], [], []
    for ln in sec.strip().split("\n"):
        if ln.startswith("|") and not set(ln) <= set("|- "):
            rows.append([c.strip() for c in ln.strip("|").split("|")])
        elif ln.strip() and not ln.startswith("|"):
            (after if rows else before).append(ln.strip())
    head, body = rows[0], rows[1:]
    t = "<tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>"
    t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    css = BASE_CSS + """
body{background:#f4f2ec;color:#2b2a26}
.file{position:absolute;left:80px;top:36px;font:500 22px Consolas,monospace;color:#6b6860}
.doc{position:absolute;left:80px;top:84px;width:1760px;box-sizing:border-box;background:#fff;border:1px solid #d9d5cb;border-radius:10px;padding:30px 44px}
h2{margin:0 0 10px;font-size:34px;border-bottom:1px solid #e4e0d6;padding-bottom:8px}
p{font-size:21px;margin:8px 0 14px;line-height:1.35}
p.after{margin:16px 0 0}
table{border-collapse:collapse;width:100%;font-size:19.5px}
th,td{border:1px solid #dcd8ce;padding:7px 12px;text-align:left;vertical-align:top;line-height:1.3}
th{background:#f0ede5}
td:first-child{white-space:nowrap;font-weight:600;width:250px}
code{font-family:Consolas,monospace;background:#f0ede5;padding:1px 5px;border-radius:4px}
.tag{background:#2b2a26;color:#f4f2ec}
"""
    pb = "".join(f"<p>{inline(p)}</p>" for p in before)
    pa = "".join(f"<p class='after'>{inline(p)}</p>" for p in after)
    doc = (f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>"
           f"<div class='file'>assignment-8/pitch/README.md</div>"
           f"<div class='doc'><h2>Keys</h2>{pb}<table>{t}</table>{pa}</div>"
           f"<div class='tag'>DOCUMENT · pitch/README.md</div></body></html>")
    return doc


def tests_page():
    blocks = []
    for name in TESTS:
        lines = open(os.path.join(LOGS, f"b12-{name}.txt"), encoding="utf-8", errors="replace").read().rstrip().split("\n")
        passes = sum(1 for l in lines if l.strip().startswith("PASS"))
        tail = [l for l in lines if l.strip()][-3:]
        cmd = f"$ ./scripts/run-test.sh {name}.gd 60"
        blocks.append((cmd, tail, passes))
    out = []
    for cmd, tail, passes in blocks:
        out.append(f"<div class='blk'><div class='cmd'>{html.escape(cmd)}</div>"
                   + "".join(f"<div class='ln'>{html.escape(l)}</div>" for l in tail)
                   + f"<div class='cnt'>{passes} PASS lines (counted)</div></div>")
    css = BASE_CSS + """
body{background:#15171a;color:#d6d9dd}
.wrap{position:absolute;left:60px;top:120px;width:1800px;columns:2;column-gap:50px}
.blk{break-inside:avoid;margin-bottom:40px;font:24px Consolas,monospace;position:relative}
.cmd{color:#e8c27a}
.ln{white-space:pre;overflow:hidden;text-overflow:ellipsis;color:#b9c2cc}
.ln:nth-last-of-type(1){color:#9fe0a5}
.cnt{color:#7d8590;font-size:19px;margin-top:4px}
.tag{background:#d6d9dd;color:#15171a}
"""
    return (f"<html><head><meta charset='utf-8'><style>{css}</style></head><body><div class='wrap'>{''.join(out)}</div>"
            f"<div class='tag'>REAL OUTPUT · f13431bf · last lines of each test log</div></body></html>")


os.makedirs(OUT, exist_ok=True)
for name, page in (("b09-readme-keys", readme_page()), ("b12-tests", tests_page())):
    hp = os.path.join(OUT, name + ".html")
    open(hp, "w", encoding="utf-8").write(page)
    png = os.path.join(OUT, name + ".png")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--screenshot={png}", "--window-size=1920,1080", "file:///" + hp.replace("\\", "/")],
                   check=True, capture_output=True, timeout=120)
    print(name, os.path.getsize(png))
