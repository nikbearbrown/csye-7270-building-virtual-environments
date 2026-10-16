#!/usr/bin/env python3
"""Build media/<BID>.mp4 for every non-Remotion beat of the Assignment 3 film from real material only: Blender's own
window screenshots (taken through the MCP), the MCP look renders, the 4K Movie Maker takes in capture/, files from the
repository (brief, logs, build scripts, notes) and recorded tool output. Durations are the measured narration.

    python3 tools/build_media.py [B02 B03 ...]
"""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
TOOLS = REEL / "tools"
WORK = REEL / "media" / "_work"
sys.path.insert(0, str(TOOLS))

W, H, FPS = 3840, 2160, 30
PAD, TITLE_Y, TOP, BOT = 211, 97, 346, 1901
INK, SOFT, GHOST, SPARK, PAGE, CARD, BORDER = "#3D3929", "#73705F", "#A9A491", "#D97757", "#FAF9F5", "#FFFFFF", "#E5E2D9"
CODE_BG, CODE_TXT, CODE_DIM, CODE_HI = "#1F232B", "#E8E6DF", "#7C8494", "#3A3324"
SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()[:7]
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
BL = "images/blender"
MCP = "../../evidence/a3/mcp"
BLEND_SCALE = 1.0          # Blender screenshots are 2940 x 1660


def dur(bid):
    return float(BEATS[bid]["actual_duration_s"])


def at(bid, phrase, lead=0.25):
    text = BEATS[bid]["narration_text"]
    i = text.find(phrase)
    if i < 0:
        raise SystemExit(f"{bid}: phrase not in narration: {phrase!r}")
    return round(max(0.0, dur(bid) * i / len(text) - lead), 2)


def text(t, x, y, size, color=INK, f="sans", w=0, align="left", t_in=0.0, t_out=None, fade=0.25, spacing=1.25):
    L = {"kind": "text", "text": t, "x": x, "y": y, "size": size, "color": color, "font": f, "w": w, "align": align,
         "spacing": spacing}
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = fade
    return L


def rect(x, y, w, h, fill=None, outline=None, width=0, radius=0, t_in=0.0, t_out=None, fade=0.3):
    L = {"kind": "rect", "x": x, "y": y, "w": w, "h": h, "fill": fill, "outline": outline, "width": width, "radius": radius}
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = fade
    return L


def image(src, x, y, w, h, t_in=0.0, t_out=None, fade=0.3, fit="contain"):
    L = {"kind": "image", "src": src, "x": x, "y": y, "w": w, "h": h, "fit": fit}
    if t_in or t_out is not None:
        L["t"] = [t_in, t_out if t_out is not None else 9999]
        L["fade"] = fade
    return L


def frame_chrome(title, source):
    return [text(title, PAD, TITLE_Y, 120, INK, "serif"),
            text(source, PAD, 2005, 44, SOFT, "sans", w=3000),
            text("@NikBearBrown", W - PAD - 420, 1996, 58, INK, "serif", w=420, align="right")]


def spec_write(bid, layers, duration):
    for L in layers:
        if "t" in L and L["t"][1] > duration:
            L["t"][1] = duration
    spec = {"out": f"media/{bid}.mp4", "duration": round(duration, 4), "fps": FPS, "bg": PAGE, "base": str(REEL),
            "audio": None, "layers": layers}
    WORK.mkdir(parents=True, exist_ok=True)
    p = WORK / f"{bid}.json"
    p.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    subprocess.run([sys.executable, str(TOOLS / "compose.py"), str(p)], check=True)


def crop_tile(src, tile, name):
    """One tile of a 2 x 2 MCP look render (768 x 768): 0 front, 1 back, 2 three-quarter, 3 below."""
    im = Image.open(REEL / src)
    s = im.width // 2
    x, y = (tile % 2) * s, (tile // 2) * s
    out = WORK / f"{name}.png"
    WORK.mkdir(parents=True, exist_ok=True)
    im.crop((x, y, x + s, y + s)).save(out)
    return f"media/_work/{name}.png"


def last_frame(take, name):
    out = WORK / f"{name}.png"
    WORK.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.05", "-i", str(REEL / take), "-frames:v", "1", str(out)], check=True)
    return f"media/_work/{name}.png"


def frame_at(take, n, name):
    out = WORK / f"{name}.png"
    WORK.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(REEL / take), "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
                    str(out)], check=True)
    return f"media/_work/{name}.png"


def frames(take):
    return int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                               "stream=nb_read_frames", "-of", "csv=p=0", str(REEL / take)],
                              capture_output=True, text=True, check=True).stdout.strip())


def code_panel(path, a, b, x, y, w, h, highlights, size=52):
    """Verbatim lines a..b of a repository file with line numbers; highlights = [(line, t_in)]."""
    lines = (REPO / path).read_text().splitlines()[a - 1:b]
    lh = int(size * 1.32)
    layers = [rect(x, y, w, h, fill=CODE_BG, radius=24)]
    for ln, t_in in highlights:
        layers.append(rect(x + 20, y + 40 + (ln - a) * lh - 6, w - 40, lh, fill=CODE_HI, radius=8, t_in=t_in))
        layers.append(rect(x + 20, y + 40 + (ln - a) * lh - 6, 10, lh, fill=SPARK, t_in=t_in))
    nums = "\n".join(str(n) for n in range(a, b + 1))
    layers.append(text(nums, x + 50, y + 40, size, CODE_DIM, "mono", spacing=1.32))
    layers.append(text("\n".join(lines), x + 50 + int(size * 2.6), y + 40, size, CODE_TXT, "mono", spacing=1.32))
    return layers


# ---------------------------------------------------------------- beats

def b02():
    bid, d = "B02", dur("B02")
    layers = frame_chrome("Three props, frozen first",
                          "CHANGE-BRIEF.md · A3-R0 (8a8c778, 2026-10-13) · images: MCP look renders of the MCP builds (shrine before Bao's hand edit), evidence/a3/mcp/")
    cols = [("Lantern Gate", "market entrance · static blocker", "1.20 × 0.80 × 2.85 m", "6 shapes · ≤ 160 triangles",
             "built: 6 · 88", "lantern_gate-look.png", "A Lantern Gate"),
            ("Supply Stack", "obstacle beside a market stall", "1.20 × 0.80 × 1.10 m", "3 shapes · ≤ 180 triangles",
             "built: 3 · 68", "supply_stack-look.png", "A Supply Stack"),
            ("Lamp-oil Shrine", "landmark near the upgrade area", "0.80 × 0.80 × 1.45 m", "3 shapes · ≤ 120 triangles",
             "built: 3 · 60", "oil_shrine-look.png", "And a Lamp-oil")]
    gap = 60
    cw = (W - 2 * PAD - 2 * gap) // 3
    for k, (name, role, size, budget, built, img, ph) in enumerate(cols):
        t_in = at(bid, ph)
        x = PAD + k * (cw + gap)
        layers.append(rect(x, TOP, cw, 1470, fill=CARD, outline=BORDER, width=3, radius=28, t_in=t_in))
        layers.append(image(crop_tile(f"{MCP}/{img}", 2, f"B02-{k}"), x + (cw - 760) // 2, TOP + 40, 760, 760, t_in=t_in))
        layers.append(text(name, x + 56, TOP + 830, 92, INK, "serif", t_in=t_in))
        layers.append(text(role, x + 56, TOP + 960, 52, SOFT, "sans", w=cw - 100, t_in=t_in))
        layers.append(text(size, x + 56, TOP + 1080, 66, INK, "sans-medium", t_in=t_in + 0.2))
        layers.append(text(budget, x + 56, TOP + 1190, 54, INK, "sans", t_in=t_in + 0.3))
        layers.append(text(built, x + 56, TOP + 1290, 50, GHOST, "sans", t_in=t_in + 0.4))
    layers.append(text("Origin: centre of the underside, on the floor · Blender +Z up → Godot +Y up · "
                       "frozen before the MCP rebuild", PAD, TOP + 1500, 46, SOFT, "sans", w=W - 2 * PAD,
                       t_in=at(bid, "origin")))
    spec_write(bid, layers, d)


def b03():
    bid, d = "B03", dur("B03")
    log = (REPO / "evidence/a3/setup/04-mcp-connect.log").read_text().splitlines()
    keep = [l for l in log if any(k in l for k in ('"up_to_date"', '"addon_version"', '"blender_version"',
                                                   '"libraries"', '"generators"', '"telemetry_consent"'))]
    layers = frame_chrome("The route: MCP for Blender 2.1.9",
                          "window: Blender's own screenshot through the MCP, 2026-10-14 12:47 EDT · log: evidence/a3/setup/04-mcp-connect.log, verbatim")
    w, h = 2300, round(2300 * 1660 / 2940)
    layers.append(image(f"{BL}/1247-shrine-after-hand-edit-mcp-panel.png", PAD, TOP, w, h))
    s = w / 2940
    t_lib = at(bid, "every model library")
    layers.append(rect(PAD + int(1881 * s), TOP + int(162 * s), int(475 * s), int(1000 * s), outline=SPARK, width=8,
                       radius=12, t_in=t_lib))
    layers.append(text("Bao's Blender 5.2.2 · MCP panel: Connected on port 9876 · every library and generator unchecked",
                       PAD, TOP + h + 30, 44, SOFT, "sans", w=w))
    x = PAD + w + 70
    t_log = at(bid, "The first status call")
    layers.append(rect(x, TOP, W - PAD - x, 1060, fill=CODE_BG, radius=24, t_in=t_log))
    layers.append(text("$ get_addon_status · 2026-10-13 16:30 EDT", x + 40, TOP + 40, 40, CODE_DIM, "mono", t_in=t_log))
    body = "\n".join(l.strip() for l in keep)
    layers.append(text(body, x + 40, TOP + 130, 36, CODE_TXT, "mono", w=W - PAD - x - 80, spacing=1.45, t_in=t_log + 0.2))
    t_bg = at(bid, "background scripts")
    layers.append(rect(x, TOP + 1110, W - PAD - x, 445, fill="#FBEFE9", outline=SPARK, width=4, radius=24, t_in=t_bg))
    layers.append(text("Earlier on 2026-10-13 another coding session had no MCP tools: the first builds were "
                       "background scripts, kept in tools/blender/script_route/.", x + 40, TOP + 1150, 46, INK, "sans",
                       w=W - PAD - x - 80, t_in=t_bg))
    spec_write(bid, layers, d)


PLAN_ZH = ("下面是 Supply Stack 的 MCP 计划，等你批准：\n"
           "1. 用 bpy.data 清空场景，建 MarketTimber 和 CrateBrass 两个材质。\n"
           "2. LowerCrate：1.20 × 0.80 × 0.50 m，中心在 (0, 0, 0.25)。\n"
           "3. UpperCrate：0.72 × 0.68 × 0.50 m，中心在 (−0.22, 0.05, 0.75)。\n"
           "4. OilBarrel：12 边圆柱，半径 0.22 m（见下面的问题）。\n"
           "5. 应用旋转和缩放，再用 get_scene_info 确认。\n"
           "6. 测量，另存为 blender/a3/supply_stack.blend，写 build JSON。\n"
           "7. 用 look 从正面、背面、斜上方和下方看。\n"
           "8. 导出 GLB，把代码合成 tools/blender/build_supply_stack.py。")
PLAN_EN = ("Plan for the Supply Stack, waiting for approval: 1 clear the scene through bpy.data, make MarketTimber and "
           "CrateBrass · 2 LowerCrate 1.20 × 0.80 × 0.50 m at (0, 0, 0.25) · 3 UpperCrate 0.72 × 0.68 × 0.50 m at "
           "(−0.22, 0.05, 0.75) · 4 OilBarrel, 12-sided, r 0.22 m · 5 apply rotation and scale, confirm with "
           "get_scene_info · 6 measure, save supply_stack.blend, write the build JSON · 7 look from front, back, "
           "three-quarter, below · 8 export the GLB, save the code as build_supply_stack.py")


def b04():
    bid, d = "B04", dur("B04")
    layers = frame_chrome("The plan, then Bao's approval",
                          "excerpt of this Claude Code session, 2026-10-14 11:59 EDT · Chinese verbatim · English gloss is Claude's translation")
    layers.append(rect(PAD, TOP, 2150, 1555, fill=CARD, outline=BORDER, width=3, radius=28))
    layers.append(text("Claude", PAD + 50, TOP + 40, 56, SOFT, "sans-medium"))
    layers.append(text(PLAN_ZH, PAD + 50, TOP + 140, 52, INK, "cjk", w=2050, spacing=1.5))
    x = PAD + 2210
    layers.append(text("English gloss (Claude's translation)", x, TOP + 10, 44, SOFT, "sans"))
    layers.append(text(PLAN_EN, x, TOP + 80, 42, INK, "sans", w=W - PAD - x, spacing=1.35))
    t = at(bid, "Bao's reply")
    layers.append(rect(x, TOP + 1000, W - PAD - x, 555, fill="#FBEFE9", outline=SPARK, width=4, radius=24, t_in=t))
    layers.append(text("Bao, verbatim", x + 40, TOP + 1030, 44, SOFT, "sans", t_in=t))
    layers.append(text("“批准，开始建 Stack”", x + 40, TOP + 1110, 70, INK, "cjk", t_in=t))
    layers.append(text("approved, build the Stack", x + 40, TOP + 1210, 42, SOFT, "sans", t_in=t))
    t2 = at(bid, "And keep the barrel")
    layers.append(text("“和旧版一样”  (barrel: same as the old version)", x + 40, TOP + 1330, 54, INK, "cjk",
                       w=W - PAD - x - 80, t_in=t2))
    spec_write(bid, layers, d)


def b05():
    bid, d = "B05", dur("B05")
    layers = frame_chrome("MCP call 2: the lower crate",
                          "tools/blender/build_supply_stack.py · lines 50–60 · verbatim body of execute_blender_code call 2 of 7 · sent 2026-10-14 11:59 EDT")
    layers += code_panel("tools/blender/build_supply_stack.py", 50, 60, PAD, TOP, 2500, 1555,
                         [(54, at(bid, "quarter of a metre")), (57, at(bid, "dimensions"))], size=45)
    x = PAD + 2560
    layers.append(text("Blender Python, not Godot", x, TOP + 10, 56, INK, "serif"))
    layers.append(text("Sent through the MCP in Bao's running Blender; saved verbatim in the build script.", x, TOP + 110,
                       44, SOFT, "sans", w=W - PAD - x))
    t = at(bid, "scale behind")
    layers.append(rect(x, TOP + 520, W - PAD - x, 700, fill="#FBEFE9", outline=SPARK, width=4, radius=24, t_in=t))
    layers.append(text("A default cube is 2 × 2 × 2 m, so these dimensions leave scale (0.6, 0.4, 0.25) on the object.",
                       x + 40, TOP + 560, 50, INK, "sans", w=W - PAD - x - 80, t_in=t))
    layers.append(text("get_scene_info after the call:\nat (0.0, 0.0, 0.25) · scale (0.6, 0.4, 0.25) · size 1.2x0.8x0.5",
                       x + 40, TOP + 900, 38, INK, "mono", w=W - PAD - x - 80, t_in=t + 0.3))
    spec_write(bid, layers, d)


def blender_shot(src, label):
    h = 1555
    w = round(h * 2940 / 1660)
    return [image(src, PAD, TOP, w, h), text(label, PAD, TOP + h + 18, 40, SOFT, "sans", w=w)], w / 2940


def b06():
    bid, d = "B06", dur("B06")
    layers = frame_chrome("After call 2: scale left on the object",
                          "Blender's own window screenshot through the MCP · film re-run of the same calls in a scratch file, 2026-10-14 12:49 EDT")
    shot, s = blender_shot(f"{BL}/1249-rerun-2-lower-crate.png", "")
    layers += shot[:1]
    w = round(1555 * 2940 / 1660)
    t1, t2 = at(bid, "scale point six"), at(bid, "non-uniform")
    layers.append(rect(PAD + int(2620 * s), TOP + int(905 * s), int(240 * s), int(150 * s), outline=SPARK, width=8, radius=10, t_in=t1))
    layers.append(rect(PAD + int(8 * s), TOP + int(1615 * s), int(445 * s), int(42 * s), outline=SPARK, width=8, radius=8, t_in=t2))
    x = PAD + w + 60
    layers.append(text("FILM RE-RUN", x, TOP, 56, SPARK, "sans-medium"))
    layers.append(text("Same calls as the shipped build (12:00), sent again into a scratch file outside the repository.",
                       x, TOP + 90, 40, SOFT, "sans", w=W - PAD - x))
    layers.append(text("Scale\n0.600\n0.400\n0.250", x, TOP + 520, 60, INK, "mono", t_in=t1))
    layers.append(text("“Active object has non-uniform scale”", x, TOP + 980, 44, INK, "sans", w=W - PAD - x, t_in=t2))
    spec_write(bid, layers, d)


def b07():
    bid, d = "B07", dur("B07")
    layers = frame_chrome("MCP call 5: apply rotation and scale",
                          "tools/blender/build_supply_stack.py · lines 87–100 · verbatim body of execute_blender_code call 5 of 7 · sent 2026-10-14 12:00 EDT")
    layers += code_panel("tools/blender/build_supply_stack.py", 87, 100, PAD, TOP, 3418, 1555,
                         [(96, at(bid, "applies rotation and scale"))], size=48)
    spec_write(bid, layers, d)


def b08():
    bid, d = "B08", dur("B08")
    t_look = at(bid, "look tool")
    layers = frame_chrome("Unit scale, and the look tool",
                          "window: film re-run after call 5, 12:50 EDT · look renders: the shipped builds, 2026-10-14 11:56–12:04 EDT (evidence/a3/mcp/)")
    w = round(1555 * 2940 / 1660)
    s = w / 2940
    layers.append(image(f"{BL}/1250-rerun-6-sidebar-dimensions.png", PAD, TOP, w, 1555, t_out=t_look))
    layers.append(rect(PAD + int(1880 * s), TOP + int(600 * s), int(470 * s), int(330 * s), outline=SPARK, width=8, radius=10, t_out=t_look))
    x = PAD + w + 60
    layers.append(text("Sidebar · Item\nScale 1.000 ×3\nDimensions\n1.2 m · 0.8 m · 0.5 m", x, TOP + 300, 56, INK, "sans",
                       w=W - PAD - x, spacing=1.4, t_out=t_look))
    names = [("lantern_gate-look.png", "Lantern Gate"), ("supply_stack-look.png", "Supply Stack"),
             ("oil_shrine-look.png", "Lamp-oil Shrine")]
    side = 1080
    gap = (W - 2 * PAD - 3 * side) // 2
    for k, (img, name) in enumerate(names):
        x = PAD + k * (side + gap)
        layers.append(image(f"{MCP}/{img}", x, TOP + 60, side, side, t_in=t_look))
        layers.append(text(name + " · front · back · three-quarter · below", x, TOP + 60 + side + 30, 40, SOFT, "sans",
                           w=side, t_in=t_look))
    t_z = at(bid, "show through")
    x1 = PAD + side + gap
    layers.append(rect(x1 + side // 2, TOP + 60 + side // 2, side // 2, side // 2, outline=SPARK, width=8, radius=10, t_in=t_z))
    layers.append(text("below: barrel base and crate underside share a plane (z-fighting)", PAD, TOP + 1360, 50, INK,
                       "sans", w=W - 2 * PAD, t_in=t_z))
    spec_write(bid, layers, d)


def b09():
    bid, d = "B09", dur("B09")
    notes = (REPO / "BLENDER-NOTES.md").read_text()
    seen = re.search(r"\*\*What I saw\.\*\* (.*?)\n\n", notes, re.S).group(1).replace("\n", " ").replace("`", "")
    layers = frame_chrome("Bao's hand edit: OilGem, 20° around Z",
                          "NOT RECORDED LIVE · before: MCP look render 12:04 · after: Blender window 12:47 · quote: BLENDER-NOTES.md · check: TEST-REPORT.md")
    layers.append(text("before · 12:04", PAD, TOP, 44, SOFT, "sans"))
    layers.append(image(crop_tile(f"{MCP}/oil_shrine-look.png", 0, "B09-before"), PAD, TOP + 70, 900, 900))
    t_after = at(bid, "twenty degrees")
    x = PAD + 960
    w = 1700
    layers.append(text("after · 12:47 · OilGem selected, Rotation 0° after Apply", x, TOP, 44, SOFT, "sans", t_in=t_after))
    layers.append(image(f"{BL}/1247-shrine-after-hand-edit-mcp-panel.png", x, TOP + 70, w, round(w * 1660 / 2940), t_in=t_after))
    s = w / 2940
    layers.append(rect(x + int(2500 * s), TOP + 70 + int(740 * s), int(400 * s), int(120 * s), outline=SPARK, width=6,
                       radius=8, t_in=t_after + 0.4))
    t_note = at(bid, "His note")
    layers.append(rect(PAD, TOP + 1100, 2460, 455, fill="#FBEFE9", outline=SPARK, width=4, radius=24, t_in=t_note))
    layers.append(text("Bao · BLENDER-NOTES.md", PAD + 40, TOP + 1125, 40, SOFT, "sans", t_in=t_note))
    layers.append(text("“" + seen + "”", PAD + 40, TOP + 1190, 44, INK, "serif-italic", w=2380, spacing=1.3, t_in=t_note))
    t_chk = at(bid, "vertex check")
    x2 = PAD + 2520
    layers.append(rect(x2, TOP + 1100, W - PAD - x2, 455, fill=CARD, outline=BORDER, width=3, radius=24, t_in=t_chk))
    layers.append(text("Measured\nMCP gem × 20.0° about Z\n= re-exported gem\nmax error 1.84e-8 m", x2 + 40, TOP + 1130, 46,
                       INK, "sans", spacing=1.35, t_in=t_chk))
    spec_write(bid, layers, d)


def b11():
    bid, d = "B11", dur("B11")
    raw = (REEL / "capture/test-run-film-build-raw.txt").read_text().splitlines()
    i = next(k for k, l in enumerate(raw) if "test_a3_assets.gd" in l)
    j = next(k for k in range(i, len(raw)) if raw[k].startswith("exit="))
    out = "\n".join(["$ godot --headless --script res://tests/test_a3_assets.gd"] +
                    [l.split(" {")[0] for l in raw[i + 1:j + 1]])
    layers = frame_chrome("HEADLESS · numbers beside the brief",
                          f"recorded output: capture/test-run-film-build-raw.txt · fresh git archive of {SHA} · not a rendered view")
    layers.append(rect(PAD, TOP, 1500, 1555, fill="#14121C", radius=24))
    layers.append(text("HEADLESS", PAD + 40, TOP + 30, 40, SPARK, "sans-medium"))
    layers.append(text(out, PAD + 40, TOP + 100, 32, "#E8E6DF", "mono", w=1440, spacing=1.3))
    t = at(bid, "Brief, Blender")
    x = PAD + 1560
    rows = ("              brief          Blender        Godot AABB\n"
            "Gate      1.20×0.80×2.85  1.20×0.80×2.85  (1.20, 2.85, 0.80)\n"
            "Stack     1.20×0.80×1.10  1.20×0.80×1.10  (1.20, 1.10, 0.80)\n"
            "Shrine    0.80×0.80×1.45  0.80×0.80×1.45  (0.80, 1.45, 0.80)")
    layers.append(rect(x, TOP, W - PAD - x, 900, fill=CARD, outline=BORDER, width=3, radius=24, t_in=t))
    layers.append(text("W × D × H in metres · Godot size is (x, y, z): height on +Y", x + 40, TOP + 40, 40, SOFT, "sans",
                       w=W - PAD - x - 80, t_in=t))
    layers.append(text(rows, x + 40, TOP + 160, 46, INK, "mono", spacing=1.6, t_in=t + 0.2))
    layers.append(text("every mesh node scale (1, 1, 1) · base at y = 0 · budgets met · material names exact",
                       x + 40, TOP + 620, 40, INK, "sans", w=W - PAD - x - 80, t_in=t + 0.4))
    t2 = at(bid, "cannot show")
    layers.append(rect(x, TOP + 960, W - PAD - x, 595, fill="#FBEFE9", outline=SPARK, width=4, radius=24, t_in=t2))
    layers.append(text("A passing check shows size, orientation, scale and names. It does not show that a prop looks "
                       "right under the game's light — that is the human check.", x + 40, TOP + 1000, 48, INK, "sans",
                       w=W - PAD - x - 80, t_in=t2))
    spec_write(bid, layers, d)


def take_beat(bid, take, title, source, side, held_note):
    d = dur(bid)
    n = frames(take)
    t_end = n / FPS
    vw, vh = 2764, 1555
    layers = frame_chrome(title, source)
    layers.append({"kind": "video", "src": take, "ss": 0.0, "x": PAD, "y": TOP, "w": vw, "h": vh, "t": [0.0, t_end]})
    if t_end < d:
        layers.append(image(last_frame(take, f"{bid}-last"), PAD, TOP, vw, vh, t_in=t_end, fade=0.0))
        layers.append(rect(PAD + vw - 590, TOP + vh - 120, 560, 90, fill="#14121C", radius=14, t_in=t_end, fade=0.0))
        layers.append(text(held_note, PAD + vw - 565, TOP + vh - 102, 46, "#FFFFFF", "sans-medium", t_in=t_end, fade=0.0))
    x = PAD + vw + 60
    for k, (phrase, line) in enumerate(side):
        layers.append(text(line, x, TOP + 20 + k * 330, 46, INK, "sans", w=W - PAD - x, t_in=at(bid, phrase) if phrase else 0.0))
    spec_write(bid, layers, d)


def b13():
    take_beat("B13", "capture/take-a3-block.avi", "The gate blocks at its base",
              f"real Movie Maker capture · isolated copy of {SHA} · take 'block', 210 frames · scripted input through the room's actions",
              [("", "Real engine capture\ncollision shapes on"), ("stops at the base", "stopped at\nz = 0.667 m (log)\n= 0.40 + 0.25 radius"),
               ("no collider under", "no collider under the lantern arm"), ("F4", "F4 in the game opens this room")],
              "held last frame")


def b15():
    take_beat("B15", "capture/take-a3-orbit.avi", "The three props in the running scene",
              f"real Movie Maker capture · isolated copy of {SHA} · take 'orbit', 450 frames · scripted input through the room's actions",
              [("", "Real engine capture\nstart view"), ("Around to the back", "E held:\nbehind the props"),
               ("below the floor", "F held: −50°\nfloor mesh hidden"), ("nine checks", "HEADLESS\ntest_a3_camera.gd\n9 checks · 0 failures")],
              "held last frame")


def board(bid, title, source, cols, extra=None):
    d = dur(bid)
    layers = frame_chrome(title, source)
    n = len(cols)
    gap = 50
    cw = (W - 2 * PAD - gap * (n - 1)) // n
    for k, (head, phrase, items, accent) in enumerate(cols):
        t_in = at(bid, phrase) if phrase else 0.0
        x = PAD + k * (cw + gap)
        layers.append(rect(x, TOP, cw, 1555, fill=CARD, outline=accent or BORDER, width=4 if accent else 3, radius=28, t_in=t_in))
        layers.append(text(head, x + 50, TOP + 46, 80, INK, "serif", w=cw - 90, t_in=t_in))
        layers.append(text("\n\n".join(items), x + 50, TOP + 220, 50, INK, "sans", w=cw - 100, spacing=1.3, t_in=t_in + 0.2))
    if extra:
        layers += extra(d)
    spec_write(bid, layers, d)


LOOK_ZH = ("正面和背面看起来都正常，灯和 OilGem 虽然偏黄、Stack 被照得偏红，但整体颜色统一，我觉得可以接受。"
           "从下方能看到 Stack 底部那块重叠的圆面，有一点 z-fighting，不过只在很低的角度明显，正常游戏视角基本看不到。"
           "替身撞 Gate 时会停在底座和立柱前面，位置感觉合理，灯臂下面可以通过，没有发现影响游玩的问题。")
LOOK_EN = ("The front and back both look normal. The lanterns and the OilGem are yellowish and the Stack is lit reddish, "
           "but the overall colour is consistent, and I think that is acceptable. From below I can see the overlapping "
           "round face under the Stack, a little z-fighting, but it is only obvious at very low angles; from a normal "
           "game view you basically cannot see it. When the stand-in hits the Gate it stops in front of the base and the "
           "post, the position feels reasonable, it can pass under the lantern arm, and I found no problem that affects play.")


def b16():
    bid, d = "B16", dur("B16")
    layers = frame_chrome("Bao's look · what Claude got wrong · next",
                          "Bao, 2026-10-15, after the F4 room (front, behind, below) · English is Claude's translation · TEST-REPORT.md · CHANGE-BRIEF A3-R0, A3-R3")
    lw = 2200
    layers.append(rect(PAD, TOP, lw, 1555, fill="#FBEFE9", outline=SPARK, width=4, radius=28))
    layers.append(text("HUMAN CHECK · Bao, verbatim", PAD + 50, TOP + 40, 48, SOFT, "sans-medium"))
    zh = text("“" + LOOK_ZH + "”", PAD + 50, TOP + 130, 54, INK, "cjk", w=lw - 100, spacing=1.55)
    zh["wrap"] = "char"
    layers.append(zh)
    layers.append(text("Claude's translation: " + LOOK_EN, PAD + 50, TOP + 880, 38, SOFT, "sans", w=lw - 100, spacing=1.35))
    x = PAD + lw + 60
    cw = W - PAD - x
    t1, t2 = at(bid, "What else"), at(bid, "Next:")
    layers.append(rect(x, TOP, cw, 900, fill=CARD, outline=BORDER, width=3, radius=28, t_in=t1))
    layers.append(text("Claude got wrong", x + 46, TOP + 36, 70, INK, "serif", t_in=t1))
    layers.append(text("· read the assignment as one prop (A3-R0)\n\n· MCP call 12 of 13 failed its own check "
                       "(AssertionError: [])\n\n· shipped a fixed camera against the brief (A3-R3)", x + 46, TOP + 170, 46,
                       INK, "sans", w=cw - 90, spacing=1.3, t_in=t1 + 0.2))
    layers.append(rect(x, TOP + 950, cw, 605, fill=CARD, outline=BORDER, width=3, radius=28, t_in=t2))
    layers.append(text("Next", x + 46, TOP + 980, 70, INK, "serif", t_in=t2))
    layers.append(text("· barrel 0.60 m tall at z = 0.80, so no faces overlap under the stack\n\n· still uncertain: "
                       "one viewer only", x + 46, TOP + 1110, 46, INK, "sans", w=cw - 90, spacing=1.3, t_in=t2 + 0.2))
    spec_write(bid, layers, d)


def b17():
    board("B17", "Who did what", f"FRICTIONAL.md · SOURCES.md · source revision {SHA} · Godot 4.7.2 · Blender 5.2.2 LTS · mcp-for-blender 2.1.9", [
        ("Bao Xing", "", ["chose the three props and the MCP route", "approved every build plan before it ran",
                          "hand edit: OilGem 20° about Z, applied, File > Export", "interface screenshot and interface notes",
                          "the look at the final room"], SPARK),
        ("Claude", "Claude wrote", ["wrote and sent the 27 build calls; kept them in tools/blender/",
                                    "Godot room, orbit camera, three headless suites", "measured, logged, drafted the documents",
                                    "this film: script, captures, narration (Kokoro am_onyx)"], None)])


BUILDERS = {"B02": b02, "B03": b03, "B04": b04, "B05": b05, "B06": b06, "B07": b07, "B08": b08, "B09": b09,
            "B11": b11, "B13": b13, "B15": b15, "B16": b16, "B17": b17}

if __name__ == "__main__":
    for bid in sys.argv[1:] or list(BUILDERS):
        print("[media]", bid, flush=True)
        BUILDERS[bid]()
