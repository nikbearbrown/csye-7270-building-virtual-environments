"""make_terminals.py - draws act VI's two terminal windows (pantry/a6_term_check.png, pantry/a6_term_import.png) from the REAL logs
of run_godot_act6.sh, in the CC kit's plain-terminal colours (CCPlainShell: window #252422, ink #F2F0E9, violet "$ ", ghost #6B6760).
Every output row is a line of the log, character for character (ANSI colour codes stripped); "…" rows (ghost) mark lines left out;
the wrapper's own "[exit code N]" line is not drawn (a terminal would not print it). Menlo 40 px, so the Manim camera can push in.
Also writes evidence/act6/terminals.json: per image, its size, the x of column 0, the row baseline-centre y's, and Menlo's advance,
so a scene can put a mark beside any character. Run from the reel folder: python3 evidence/act6/make_terminals.py"""
import json, re
from PIL import Image, ImageDraw, ImageFont

ANSI = re.compile(r"\x1b\[[0-9;]*m")
MONO = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 40, index=0)
MONO_B = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 40, index=1)
UI = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 28, index=0)
PANEL, BAR, BORDER = "#252422", "#2C2B28", "#3A3835"
INK, INK2, INK3, VIOLET = "#F2F0E9", "#A8A398", "#6B6760", "#A78BFA"
ADV = MONO.getlength("M")                 # Menlo advance at 40 px
ROW, LEFT, TOP_BAR, TOP_PAD, BOT_PAD, RIGHT = 62, 44, 64, 34, 30, 44


def log_lines(path):
    out = []
    for raw in open(path, encoding="utf-8").read().split("\n"):
        s = ANSI.sub("", raw)
        if s.startswith("[exit code"):
            continue
        out.append(s)
    while out and out[-1] == "":
        out.pop()
    return out


def draw(rows, title, out_png, key, meta):
    width = int(LEFT + RIGHT + ADV * max(len(r) for r in rows))
    height = TOP_BAR + TOP_PAD + ROW * len(rows) + BOT_PAD
    im = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, width - 1, height - 1], radius=22, fill=PANEL, outline=BORDER, width=2)
    d.rounded_rectangle([1, 1, width - 2, TOP_BAR], radius=21, fill=BAR)
    d.rectangle([1, TOP_BAR - 22, width - 2, TOP_BAR], fill=BAR)
    d.line([1, TOP_BAR, width - 2, TOP_BAR], fill=BORDER, width=2)
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        cx = 34 + i * 30
        d.ellipse([cx - 9, TOP_BAR / 2 - 9, cx + 9, TOP_BAR / 2 + 9], fill=c)
    tw = d.textlength(title, font=UI)
    d.text(((width - tw) / 2, TOP_BAR / 2), title, font=UI, fill=INK2, anchor="lm")
    ys = []
    for i, r in enumerate(rows):
        y = TOP_BAR + TOP_PAD + ROW * i + ROW / 2
        ys.append(y)
        if r.startswith("$ "):
            d.text((LEFT, y), "$", font=MONO_B, fill=VIOLET, anchor="lm")
            d.text((LEFT + 2 * ADV, y), r[2:], font=MONO, fill=INK, anchor="lm")
        elif r == "…":
            d.text((LEFT, y), r, font=MONO, fill=INK3, anchor="lm")
        else:
            d.text((LEFT, y), r, font=MONO, fill=INK, anchor="lm")
    im.save(out_png)
    meta[key] = {"png": out_png, "w": width, "h": height, "x0": LEFT, "adv": ADV, "rows": rows, "y": ys}
    print(out_png, width, height, len(rows), "rows")


meta = {}
# B54: the check, every line of its output, verbatim
chk = log_lines("evidence/act6/a6_check.log")
assert chk[0].startswith("$ timeout 120 godot --headless --path godot --script res://tests/check_assets.gd --fixed-fps 60")
draw(chk, "zsh — recorded output · Godot 4.7.2", "pantry/a6_term_check.png", "check", meta)

# B53: ls + the import, with the per-file reimport lines; "…" marks the lines left out
ls = log_lines("evidence/act6/a6_ls_assets.log")
imp = log_lines("evidence/act6/a6_import.log")
imp = [s for s in imp if s.strip() != ""]
pick = [imp[0], imp[1]]
for want in ["[   0% ] reimport | coin.glb", "[  25% ] reimport | crate.glb", "[  50% ] reimport | lantern.glb", "[ DONE ] reimport"]:
    assert want in imp, want
    pick += ["…", want]
draw(ls + pick, "zsh — recorded output · lines left out: …", "pantry/a6_term_import.png", "import", meta)
json.dump(meta, open("evidence/act6/terminals.json", "w"), indent=1)
