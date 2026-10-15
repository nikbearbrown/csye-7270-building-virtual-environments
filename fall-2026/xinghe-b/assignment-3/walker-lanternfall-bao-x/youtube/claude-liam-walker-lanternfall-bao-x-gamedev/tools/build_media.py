#!/usr/bin/env python3
"""Build media/<BID>.mp4 for every non-Remotion beat of the Lanternfall film from real material only: the 4K engine
takes in capture/, files from the repository (sprites, raw model outputs, logs, design images) and recorded tool
output. Event times come from each take's own capture log; courier positions come from the identical dry run's
per-frame track (capture/*-dryrun-track.jsonl). Durations are the measured narration (beat_sheet.json).

    gen/.venv-audio/bin/python youtube/<reel>/tools/build_media.py [B03 B04 ...]
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REEL = Path(__file__).resolve().parents[1]
REPO = REEL.parents[1]
TOOLS = REEL / "tools"
WORK = REEL / "media" / "_work"
sys.path.insert(0, str(TOOLS))
from compose import FONT_FILES  # noqa: E402

W, H, FPS = 3840, 2160, 30
PAD, TITLE_Y, TOP, BOT = 211, 97, 346, 1901
INK, SOFT, GHOST, SPARK, PAGE, CARD, BORDER = "#3D3929", "#73705F", "#A9A491", "#D97757", "#FAF9F5", "#FFFFFF", "#E5E2D9"
DARK, DARK2, PANEL_TXT = "#202531", "#2b3240", "#edf1f7"
SHA = (REEL / "FILM-SOURCE-REVISION.txt").read_text().strip()[:7]
SHEET = json.loads((REEL / "beat_sheet.json").read_text())
BEATS = {b["beat_id"]: b for b in SHEET["beats"]}
SFX = {"kill": ("SFX-01", "kill"), "pickup": ("SFX-02", "pickup"), "hurt": ("SFX-03", "hurt"),
       "levelup": ("SFX-04", "level-up"), "evolve": ("SFX-05", "evolve"), "lose": ("SFX-06a", "lose"),
       "win": ("SFX-06b", "win")}
TAKES = {
    "main": ("capture/take-main-seed11.avi", "capture/take-main-seed11-inputs.jsonl", "capture/take-main-seed11-dryrun-track.jsonl"),
    "lose": ("capture/clean/take-lose-seed3.mov", "capture/take-lose-seed3-inputs.jsonl", "capture/take-lose-seed3-dryrun-track.jsonl"),
    "props": ("capture/take-props-seed11.avi", "capture/take-props-seed11-inputs.jsonl", "capture/take-props-seed11-dryrun-track.jsonl"),
    "before": ("capture/take-before-40102ab-seed14.avi", "capture/take-before-40102ab-seed14-inputs.jsonl", "capture/take-before-40102ab-seed14-dryrun-track.jsonl"),
}
TAKE_NOTE = {"main": "main take · seed 11", "lose": "lose take · seed 3", "props": "props take · seed 11",
             "before": "build 40102ab · seed 14"}


def font(name, size):
    return ImageFont.truetype(str(FONT_FILES[name]), size)


class Take:
    def __init__(self, key):
        src, log, track = TAKES[key]
        self.key, self.src = key, src
        self.events = [json.loads(l) for l in (REEL / log).read_text().splitlines()]
        mf = next(e for e in self.events if e["event"] == "movie_frames")
        self.stale = sorted(mf["stale"])
        tr = [json.loads(l) for l in (REEL / track).read_text().splitlines()]
        self.track = next(e for e in tr if e["event"] == "track")["frames"]
        self.dry = tr                       # identical dry run: also has every kill and gem (LF_LOG_EVENTS=1)
        self.start = next(self.frame(e) for e in self.events if e["event"] == "start_run")

    def frame(self, e):
        """Clean movie frame of a logged event (stale frames removed by tools/clean_take.py)."""
        pf = e["pf"]
        return pf - sum(1 for s in self.stale if s < pf)

    def find(self, event, **kw):
        return [e for e in self.events if e["event"] == event and all(e.get(k) == v for k, v in kw.items())]

    def pos4k(self, frame):
        x, y, zoom, _rot = self.track[min(frame, len(self.track) - 1)]
        return x * 6, y * 6, zoom

    def tick_at(self, frame):
        """Run tick shown in a frame, from the nearest logged event (2 ticks per frame while playing)."""
        ev = min((e for e in self.events if "tick" in e and e["event"] == "sfx"), key=lambda e: abs(self.frame(e) - frame))
        return ev["tick"] + 2 * (frame - self.frame(ev))

    def clock(self, frame):
        s = max(0, self.tick_at(frame)) / 60
        return f"{int(s // 60)}:{int(s % 60):02d}"

    def run_clock(self, frame, tick=None):
        if tick is None:
            return "title" if frame < self.start else ""
        return f"{int(tick // 60 // 60)}:{tick / 60 % 60:04.1f}"


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


def frame_chrome(title, source, extra_source=""):
    return [text(title, PAD, TITLE_Y, 120, INK, "serif"),
            text(source + (f" · {extra_source}" if extra_source else ""), PAD, 2005, 44, SOFT, "sans", w=3000),
            text("@NikBearBrown", W - PAD - 420, 1996, 58, INK, "serif", w=420, align="right")]


def spec_write(bid, layers, duration, audio=None):
    for L in layers:
        if "t" in L and L["t"][1] > duration:
            L["t"][1] = duration
    spec = {"out": f"media/{bid}.mp4", "duration": round(duration, 4), "fps": FPS, "bg": PAGE, "base": str(REEL),
            "audio": audio, "layers": layers}
    WORK.mkdir(parents=True, exist_ok=True)
    p = WORK / f"{bid}.json"
    p.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    subprocess.run([sys.executable, str(TOOLS / "compose.py"), str(p)], check=True)


def video(take, start_frame, x, y, w, h, t_in=0.0, t_out=None, crop=None, nearest=False):
    L = {"kind": "video", "src": TAKES[take][0], "ss": start_frame / FPS, "x": x, "y": y, "w": w, "h": h,
         "t": [t_in, t_out if t_out is not None else 9999]}
    if crop:
        L["crop"] = [int(round(c)) for c in crop]
    if nearest:
        L["resample"] = "nearest"
    return L


def crop_around(cx, cy, cw, ch):
    x0 = min(max(0, cx - cw / 2), W - cw)
    y0 = min(max(0, cy - ch / 2), H - ch)
    return [x0, y0, cw, ch]


PADX = 700


def crop_centred(cx, cy, cw, ch):
    """Crop rectangle in the padded source (PADX of dark margin on every side): always centred on (cx, cy)."""
    x0 = min(max(0, cx - cw / 2 + PADX), W + 2 * PADX - cw)
    y0 = min(max(0, cy - ch / 2 + PADX), H + 2 * PADX - ch)
    return [x0, y0, cw, ch]


def video_follow(take, start_frame, x, y, w, h, cx, cy, cw, ch, t_in=0.0, t_out=None):
    L = video(take, start_frame, x, y, w, h, t_in, t_out, crop=crop_centred(cx, cy, cw, ch))
    L["pad"] = PADX
    return L


# ---------------------------------------------------------------- side panels rendered frame by frame (RGBA video)

def render_panel(name, width, height, duration, draw):
    """draw(img, t) paints one panel frame; frames are piped to ffmpeg as RGBA and stored with alpha (png in mov)."""
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.mov"
    n = round(duration * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{width}x{height}",
                          "-r", str(FPS), "-i", "-", "-c:v", "png", "-pix_fmt", "rgba", str(out)], stdin=subprocess.PIPE)
    last, last_bytes = None, None
    for i in range(n):
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        key = draw(img, i / FPS)
        if key is not None and key == last:
            p.stdin.write(last_bytes)
            continue
        b = img.tobytes()
        last, last_bytes = key, b
        p.stdin.write(b)
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit("panel encode failed: " + name)
    return str(out.relative_to(REEL))


def event_rows(take, f0, f1, extra=()):
    """(t, chip, label, colour) for SFX plays between frames f0 and f1 of a take, plus extra rows."""
    rows = []
    for e in take.events:
        if e["event"] == "sfx":
            fr = take.frame(e)
            if f0 <= fr < f1:
                chip, name = SFX[e["id"]]
                clock = take.run_clock(fr, e["tick"])
                rows.append(((fr - f0) / FPS, chip, f"{name}  ·  run {clock}", SPARK))
    rows += list(extra)
    return sorted(rows, key=lambda r: r[0])


def log_panel(name, title, sub, rows, duration, width=614, height=1555, max_rows=15):
    f_title, f_sub, f_chip, f_row = font("serif", 72), font("sans", 38), font("sans-medium", 40), font("sans", 36)

    def draw(img, t):
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, width - 1, height - 1), 28, fill=CARD, outline=BORDER, width=3)
        d.text((40, 36), title, font=f_title, fill=INK)
        y = 130
        for line in sub.split("\n"):
            d.text((42, y), line, font=f_sub, fill=SOFT)
            y += 48
        d.line((40, y + 18, width - 40, y + 18), fill=BORDER, width=3)
        shown = [r for r in rows if r[0] <= t][-max_rows:]
        y0 = y + 50
        for k, (rt, chip, label, colour) in enumerate(shown):
            yy = y0 + k * 86
            age = t - rt
            alpha = 255 if age > 0.25 else int(255 * age / 0.25)
            fill = (217, 119, 87, alpha) if colour == SPARK else (115, 112, 95, alpha)
            tw = d.textlength(chip, font=f_chip)
            d.rounded_rectangle((40, yy, 40 + tw + 32, yy + 60), 16, fill=fill)
            d.text((56, yy + 8), chip, font=f_chip, fill=(255, 255, 255, alpha))
            room, size = width - (40 + tw + 52) - 24, 36
            while size > 24 and d.textlength(label, font=font("sans", size)) > room:
                size -= 2
            d.text((40 + tw + 52, yy + 12 + (36 - size) // 2), label, font=font("sans", size), fill=(61, 57, 41, alpha))
        return (len(shown), round(min(1.0, (t - shown[-1][0]) / 0.25), 2) if shown else 0)
    return render_panel(name, width, height, duration, draw)


def listen_beat(bid, take_key, f0, f1, title, sub, extra=(), note=""):
    take = Take(take_key)
    duration = (f1 - f0) / FPS
    rows = event_rows(take, f0, f1, extra)
    panel = log_panel(bid + "-log", "Game sound", sub, rows, duration)
    layers = frame_chrome(title, f"Real engine capture, {TAKE_NOTE[take_key]} · source revision {SHA if take_key != 'before' else '40102ab'}",
                          note or "labels from the take's own AudioBus play log")
    layers += [video(take_key, f0, PAD, TOP, 2764, 1555),
               {"kind": "video", "src": panel, "ss": 0, "x": 3015, "y": TOP, "w": 614, "h": 1555, "t": [0, duration]}]
    spec_write(bid, layers, duration, audio="video")
    BEATS[bid]["_media"] = {"take": take_key, "frames": [f0, f1]}


# ---------------------------------------------------------------- beats

def b03():
    t = Take("main")
    lv = t.frame(t.find("sfx", id="levelup")[0])
    pick = t.frame(t.find("action", action="card_2")[0])
    extra = [((t.start - 0) / FPS, "MUS-01", "music starts", INK),
             (lv / FPS + 0.01, "−6 dB", "cards up: duck", INK),
             (pick / FPS, "0 dB", "card taken", INK)]
    listen_beat("B03", "main", 0, 480, "Listen: the first sixteen seconds",
                "no narration\nthe title screen is silent", extra)


def b15():
    t = Take("main")
    lv = [t.frame(e) for e in t.find("sfx", id="levelup")][3]
    pick = t.frame([e for e in t.find("action") if e["action"].startswith("card_")][3])
    p0, p1 = [t.frame(e) for e in t.find("action", action="pause")]
    f0 = lv - 25
    extra = [((lv - f0) / FPS + 0.01, "−6 dB", "cards up: duck", INK),
             ((pick - f0) / FPS, "0 dB", "card taken", INK),
             ((p0 - f0) / FPS, "Esc", "paused · muffled", INK),
             ((p1 - f0) / FPS, "Esc", "resumed", INK)]
    listen_beat("B15", "main", f0, p1 + 60, "Listen: a card screen, then a pause", "no narration", extra)


def b20():
    t = Take("main")
    hurt = t.frame(t.find("sfx", id="hurt")[0])
    evo = t.frame(t.find("sfx", id="evolve")[0])
    f0 = hurt - 35
    extra = [((evo - f0) / FPS + 0.01, "MUS-02", "layer fades in", INK)]
    listen_beat("B20", "main", f0, evo + 160, "Listen: a hit, two level-ups, the evolution", "no narration", extra)


def b25():
    t = Take("props")
    keys = [(t.frame(e), e["action"]) for e in t.find("action") if e["action"].startswith("mute")]
    f0 = keys[0][0] - 45
    names = {"mute_all": ("M", "all audio"), "mute_music": ("9", "music"), "mute_sfx": ("0", "effects")}
    extra, state = [], {"mute_all": False, "mute_music": False, "mute_sfx": False}
    for fr, a in keys:
        state[a] = not state[a]
        k, what = names[a]
        extra.append(((fr - f0) / FPS, k, f"{what}: {'off' if state[a] else 'on'}", INK))
    listen_beat("B25", "props", f0, len(t.track) - 1, "Listen: M, then 9, then 0", "no narration\neach key pressed twice", extra)


def b26():
    t = Take("lose")
    lost = t.frame(t.find("ended")[0])
    restart = t.frame(t.find("action", action="restart")[0])
    first_hurt = t.frame(t.find("sfx", id="hurt")[0])
    f0 = first_hurt - 40
    extra = [((lost - f0) / FPS + 0.01, "fade", "music fades out", INK),
             ((restart - f0) / FPS, "R", "retry: music restarts", INK)]
    listen_beat("B26", "lose", f0, min(len(t.track) - 1, restart + 95), "Listen: losing, then one key to retry",
                "no narration", extra, note="stale frames removed (tools/clean_take.py)")


def b04():
    bid, d = "B04", dur("B04")
    img = "../../design/character/blockout-poses-x8.png"
    rules = [("32 × 32 px frame, binary alpha", "thirty-two pixel frame"),
             ("lamp 11–13 px tall", "eleven to"),
             ("feet on row 31", "feet on the bottom row"),
             ("authored facing right; code flips", "facing right"),
             ("5 colours only, 1-px ink outline", "five locked")]
    layers = frame_chrome("Trace 1 · Design comes first", "CHARACTER-SHEET.md at design-v1 (46d2fe2) · blockout drawn by design/character/make_blockout.py")
    layers.append({"kind": "rect", "x": PAD, "y": TOP, "w": 2190, "h": 1555, "fill": CARD, "outline": BORDER, "width": 3, "radius": 28})
    layers.append({"kind": "image", "src": img, "x": PAD + 30, "y": TOP + 230, "w": 2130, "h": 1290})
    layers.append(text("Pre-generation blockout · 12 poses · x8", PAD + 50, TOP + 40, 56, SOFT, "sans"))
    layers.append(text("committed 2026-09-28, before any model ran", PAD + 50, TOP + 120, 46, GHOST, "sans"))
    x = PAD + 2250
    layers.append(text("Rules every frame must meet", x, TOP + 10, 64, INK, "serif"))
    for k, (r, ph) in enumerate(rules):
        layers.append(text("· " + r, x, TOP + 140 + k * 120, 54, INK, "sans", w=1150, t_in=at(bid, ph)))
    t_pal = at(bid, "five locked")
    sw = [("#F2B84B", "lamp gold"), ("#FFF1C9", "glow cream"), ("#2E3A59", "coat navy"), ("#8A5A3C", "satchel brown"), ("#14121C", "outline ink")]
    for k, (hexc, name) in enumerate(sw):
        yy = TOP + 790 + k * 140
        layers.append({"kind": "rect", "x": x, "y": yy, "w": 110, "h": 110, "fill": hexc, "outline": BORDER, "width": 3,
                       "radius": 14, "t": [t_pal, 9999], "fade": 0.25})
        layers.append(text(f"{hexc}  {name}", x + 150, yy + 26, 50, INK, "mono", t_in=t_pal + 0.1 * k))
    spec_write(bid, layers, d)


def b05():
    bid, d = "B05", dur("B05")
    log = json.loads((REPO / "gen/log/ART-PC-01/ART-PC-01-20260929T210117Z-s11-walk_contact.json").read_text())
    first = json.loads((REPO / "gen/log/ART-PC-01/ART-PC-01-20260929T202956Z-s11.json").read_text())
    st = log["settings"]
    layers = frame_chrome("Trace 2 · The prompt, rejected and rewritten", "gen/log/ART-PC-01/*.json · prompts verbatim from the run logs")
    layers.append({"kind": "rect", "x": PAD, "y": TOP, "w": 1500, "h": 1555, "fill": CARD, "outline": BORDER, "width": 3, "radius": 28})
    layers.append(text("First batch · seed 11 · 1536 × 1024", PAD + 50, TOP + 40, 50, SOFT, "sans"))
    layers.append({"kind": "image", "src": "../../" + first["raw_outputs"][0], "x": PAD + 50, "y": TOP + 120, "w": 1400, "h": 934})
    t_rej = at(bid, "Bao rejected")
    layers.append({"kind": "rect", "x": PAD + 50, "y": TOP + 1090, "w": 1400, "h": 420, "fill": "#FBEFE9", "outline": SPARK,
                   "width": 5, "radius": 20, "t": [t_rej, 9999], "fade": 0.25})
    layers.append(text("REJECTED by Bao", PAD + 90, TOP + 1120, 60, SPARK, "sans-medium", t_in=t_rej))
    layers.append(text("“不用3d就是2d像素游戏，然后不用太多动作”", PAD + 90, TOP + 1215, 62, INK, "cjk", t_in=t_rej + 0.2))
    layers.append(text("no 3D: it is a 2D pixel game, and it needs few poses", PAD + 90, TOP + 1320, 46, SOFT, "sans", w=1320, t_in=t_rej + 0.2))
    x0, t_new = PAD + 1560, at(bid, "rewritten")
    layers.append({"kind": "rect", "x": x0, "y": TOP, "w": W - PAD - x0, "h": 1555, "fill": DARK, "radius": 28,
                   "t": [t_new, 9999], "fade": 0.3})
    layers.append(text("walk_contact · the rewritten prompt (verbatim)", x0 + 50, TOP + 40, 48, "#8bc7f3", "sans", t_in=t_new))
    layers.append(text(log["prompt"], x0 + 50, TOP + 140, 50, PANEL_TXT, "mono", w=W - PAD - x0 - 100, spacing=1.32, t_in=t_new + 0.2))
    t_neg = at(bid, "negative prompt")
    layers.append(text(f"FLUX.1-schnell @ 741f7c3 · {log['model_version']} · seed {st['seed']} · {st['width']} × {st['height']} · "
                       f"{st['steps']} steps · {st['seconds']:.0f} s on the laptop", x0 + 50, TOP + 1250, 40, "#bec8d7", "sans",
                       w=W - PAD - x0 - 100, t_in=t_new + 0.4))
    layers.append(text("No negative prompt: the model is guidance-distilled, so every exclusion is written into the prompt itself.",
                       x0 + 50, TOP + 1380, 40, "#ece0a1", "sans", w=W - PAD - x0 - 100, t_in=t_neg))
    spec_write(bid, layers, d)


def checker(name, w, h, cell=24):
    p = WORK / f"{name}.png"
    im = Image.new("RGB", (w, h), "#E9E6DC")
    dr = ImageDraw.Draw(im)
    for yy in range(0, h, cell):
        for xx in range(0, w, cell):
            if (xx // cell + yy // cell) % 2:
                dr.rectangle((xx, yy, xx + cell - 1, yy + cell - 1), fill="#D7D3C6")
    WORK.mkdir(parents=True, exist_ok=True)
    im.save(p)
    return str(p.relative_to(REEL))


def b06():
    bid, d = "B06", dur("B06")
    tr = "images/trace/"
    stages = [("raw output · 512 × 512", tr + "walk_contact-1-raw.png", "Here is the raw", "lanczos"),
              ("1 · background + shadow keyed", tr + "walk_contact-2-keyed.png", "key out", "lanczos"),
              ("2 · mirrored to face right", tr + "walk_contact-3-mirrored.png", "mirror", "lanczos"),
              ("3 · lamp = 12 px (fitted at 4×)", tr + "walk_contact-4-fitted-128.png", "twelve", "nearest"),
              ("4 · palette-locked 32 × 32", tr + "walk_contact-5-locked-32.png", "lock every pixel", "nearest")]
    layers = frame_chrome("Trace 3 · Raw output, then the logged edits",
                          "gen/accepted/ART-PC-01/…-s11-walk_contact.png · stages re-run with gen/art_process.py (tools/asset_trace_stages.py)")
    cw, gap, y = 640, 48, TOP + 120
    for k, (label, src, ph, rs) in enumerate(stages):
        x = PAD + k * (cw + gap)
        t_in = at(bid, ph)
        if k:   # keyed stages sit on the game's own ground colour, as they do in play
            layers.append({"kind": "rect", "x": x, "y": y, "w": cw, "h": cw, "fill": "#1F2540", "radius": 12, "t": [t_in, 9999], "fade": 0.3})
            layers.append({"kind": "image", "src": src, "x": x, "y": y, "w": cw, "h": cw, "resample": rs, "t": [t_in, 9999], "fade": 0.3})
        else:
            layers.append({"kind": "image", "src": src, "x": x, "y": y, "w": cw, "h": cw, "t": [t_in, 9999], "fade": 0.3})
        layers.append(text(label, x, y + cw + 30, 44, INK, "sans", w=cw, t_in=t_in))
    t_ok = at(bid, "Re-running")
    layers.append({"kind": "rect", "x": PAD, "y": TOP + 1050, "w": W - 2 * PAD, "h": 380, "fill": CARD, "outline": BORDER,
                   "width": 3, "radius": 24, "t": [t_ok, 9999], "fade": 0.3})
    layers.append({"kind": "image", "src": "../../godot/assets/art/pc_sheet.png", "x": PAD + 60, "y": TOP + 1110, "w": 2560,
                   "h": 256, "resample": "nearest", "t": [t_ok, 9999], "fade": 0.3})
    layers.append({"kind": "rect", "x": PAD + 60 + 512, "y": TOP + 1106, "w": 256, "h": 264, "outline": SPARK, "width": 8,
                   "t": [t_ok + 0.3, 9999], "fade": 0.2})
    layers.append(text("godot/assets/art/pc_sheet.png, frame 3 of 10:\nre-running the logged steps gives the same 1024 pixels",
                       PAD + 2700, TOP + 1120, 46, INK, "sans", w=760, t_in=t_ok + 0.3))
    spec_write(bid, layers, d)


def b08():
    bid, d = "B08", dur("B08")
    t = Take("main")
    f0 = 105                               # 3.5 s: the run has just started, the courier walks to the first gems
    t_cmp = at(bid, "The comparison image")
    layers = frame_chrome("Trace 4 · In Godot: the frame in the running game",
                          f"Real engine capture, main take · source revision {SHA}", "comparison: design/character/sheet-vs-game.png")
    cx, cy, _ = t.pos4k(f0 + 60)
    layers.append({"kind": "rect", "x": PAD, "y": TOP, "w": 2430, "h": 1370, "fill": DARK, "radius": 24, "t": [0, t_cmp]})
    layers.append(video_follow("main", f0, PAD + 15, TOP + 15, 2400, 1340, cx, cy - 40, 960, 536, t_out=t_cmp))
    layers.append(text("live capture, cropped around the courier (2.5×)", PAD, TOP + 1400, 44, SOFT, "sans", t_out=t_cmp))
    x = PAD + 2500
    sheet = "../../godot/assets/art/pc_sheet.png"
    for k, (name, idx) in enumerate([("walk_contact", 2), ("walk_passing", 3)]):
        WORK.mkdir(parents=True, exist_ok=True)
        fr = Image.open(REPO / "godot/assets/art/pc_sheet.png").crop((idx * 32, 0, idx * 32 + 32, 32))
        p = WORK / f"pc-{name}.png"
        fr.save(p)
        yy = TOP + k * 560
        layers.append({"kind": "rect", "x": x, "y": yy, "w": 480, "h": 480, "fill": "#1F2540", "radius": 20, "t": [0, t_cmp]})
        layers.append({"kind": "image", "src": str(p.relative_to(REEL)), "x": x + 48, "y": yy + 48, "w": 384, "h": 384,
                       "resample": "nearest", "t": [0, t_cmp]})
        layers.append(text(f"{name}\npc_sheet.png frame {idx + 1}", x + 510, yy + 150, 44, INK, "sans", w=W - PAD - x - 510, t_out=t_cmp))
    layers.append(text("drawn facing right; draw_set_transform mirrors it when he faces left",
                       x, TOP + 1150, 46, INK, "sans", w=W - PAD - x, t_out=t_cmp))
    layers.append({"kind": "image", "src": "../../design/character/sheet-vs-game.png", "x": PAD, "y": TOP, "w": W - 2 * PAD,
                   "h": 1180, "t": [t_cmp, 9999], "fade": 0.35})
    t_held, t_broke = at(bid, "What held"), at(bid, "What broke")
    layers.append(text("Held: 32 × 32 · 5 colours · 1-px outline · feet on row 31 · lamp 12 px", PAD, TOP + 1250, 56, INK, "sans",
                       w=W - 2 * PAD, t_in=t_held))
    layers.append(text("Broke: the generated courier is shorter (19–23 px), so the torso sat 1.7–3.6 px below the hurtbox → "
                       "SPRITE_ORIGIN (16, 20) → (16, 23); test hurtbox-centred-on-torso RED → GREEN", PAD, TOP + 1380, 56, SPARK,
                       "sans", w=W - 2 * PAD, t_in=t_broke))
    spec_write(bid, layers, d)


def pose_frame(idx):
    WORK.mkdir(parents=True, exist_ok=True)
    p = WORK / f"pose-{idx}.png"
    Image.open(REPO / "godot/assets/art/pc_sheet.png").crop((idx * 32, 0, idx * 32 + 32, 32)).save(p)
    return str(p.relative_to(REEL))


def b10():
    bid, d = "B10", dur("B10")
    main, props, lose = Take("main"), Take("props"), Take("lose")
    hurt = main.frame(main.find("sfx", id="hurt")[0])
    evo = main.frame(main.find("sfx", id="evolve")[0])
    won = main.frame(main.find("ended")[0])
    lost = lose.frame(lose.find("ended")[0])
    lv = main.frame(main.find("sfx", id="levelup")[0])
    stand = props.frame(props.find("action", action="mute_all")[0])
    # (phrase, take, start frame, label, sheet index, crop centre override)
    segs = [("Walking", "main", 120, "walk_contact ↔ walk_passing", 2, None),
            ("Casting", "props", stand + 30, "cast, 8 ticks after each shot (idle between)", 4, None),
            ("The hurt flinch", "main", hurt - 6, "hurt + red flash (i-frames)", 5, None),
            ("The level-up pose", "main", lv + 10, "levelup: the card-screen portrait", 6, (360, 1905)),
            ("The Sunflare pose", "main", evo - 6, "sunflare, then the brighter coat", 7, None),
            ("defeat", "lose", lost - 8, "defeat: the result-panel portrait", 8, (1920, 1000)),
            ("victory", "main", won + 4, "victory at 3:00: the result-panel portrait", 9, (1920, 1000))]
    layers = frame_chrome("Seven states the code chooses", "Real engine captures · main, props and lose takes",
                          f"source revision {SHA} · crops follow the courier (engine canvas transform)")
    starts = [at(bid, s[0]) for s in segs] + [d]
    starts[0] = 0.0
    takes = {"main": main, "props": props, "lose": lose}
    for k, (ph, tk, f, label, idx, centre) in enumerate(segs):
        a, b = starts[k], starts[k + 1]
        tko = takes[tk]
        if centre:
            cx, cy = centre
            cw, ch = (900, 506) if ph == "The level-up pose" else (1800, 1012)
        else:
            cx, cy, zoom = tko.pos4k(f + int((b - a) * FPS / 2))
            cw, ch = 1320 / max(zoom, 0.5) * 0.7, 742 / max(zoom, 0.5) * 0.7
            cy -= 40 * zoom
        if tk == "lose" and ph == "defeat":
            hold_at = (lost + 3 - f) / FPS
            span = b - a
            run = min(span, hold_at)
            layers.append(video(tk, f, PAD, TOP, 2400, 1350, t_in=a, t_out=a + run, crop=crop_around(cx, cy, cw, ch)))
            still = extract_still(tk, lost + 3, crop_around(cx, cy, cw, ch), (2400, 1350), f"held-defeat")
            layers.append({"kind": "image", "src": still, "x": PAD, "y": TOP, "w": 2400, "h": 1350, "t": [a + run, b]})
            layers.append(text("held frame", PAD + 40, TOP + 30, 52, "#FFF1C9", "sans-medium", t_in=a + run, t_out=b, fade=0.1))
        elif centre:
            layers.append(video(tk, f, PAD, TOP, 2400, 1350, t_in=a, t_out=b, crop=crop_around(cx, cy, cw, ch)))
        else:
            layers.append(video_follow(tk, f, PAD, TOP, 2400, 1350, cx, cy, cw, ch, t_in=a, t_out=b))
        x = PAD + 2480
        layers.append({"kind": "rect", "x": x, "y": TOP, "w": 660, "h": 660, "fill": "#1F2540", "radius": 22, "t": [a, b]})
        layers.append({"kind": "image", "src": pose_frame(idx), "x": x + 34, "y": TOP + 34, "w": 592, "h": 592,
                       "resample": "nearest", "t": [a, b]})
        layers.append(text(label, x, TOP + 700, 54, INK, "sans-medium", w=W - PAD - x, t_in=a, t_out=b, fade=0.1))
        layers.append(text(f"pc_sheet.png frame {idx + 1} of 10", x, TOP + 860, 44, SOFT, "sans", t_in=a, t_out=b, fade=0.1))
        layers.append(text(f"{k + 1} / 7", x, TOP + 1250, 64, GHOST, "serif", t_in=a, t_out=b, fade=0.1))
    layers.append(text("crops follow the courier; the dark margin is outside the game screen", PAD, TOP + 1380, 44, SOFT, "sans"))
    spec_write(bid, layers, d)


def extract_still(take_key, frame, crop, size, name):
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK / f"{name}.png"
    x, y, w, h = [int(round(c)) for c in crop]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{frame / FPS:.4f}", "-i", str(REEL / TAKES[take_key][0]),
                    "-frames:v", "1", "-vf", f"crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:flags=neighbor",
                    "-update", "1", str(out)], check=True)
    return str(out.relative_to(REEL))


def counter_panel(name, take, f0, n_frames, title):
    kills = sorted(e["pf"] for e in take.dry if e["event"] == "killed")   # main take: no stale frames, pf = frame
    sounds = sorted(take.frame(e) for e in take.events if e["event"] == "sfx" and e["id"] == "kill")
    f_big, f_lab, f_t, f_s = font("serif", 190), font("sans", 44), font("serif", 72), font("sans", 38)

    def draw(img, t):
        fr = f0 + int(round(t * FPS))
        k = sum(1 for x in kills if f0 <= x <= fr)
        s = sum(1 for x in sounds if f0 <= x <= fr)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, 613, 1554), 28, fill=CARD, outline=BORDER, width=3)
        d.text((40, 36), title, font=f_t, fill=INK)
        d.text((42, 130), "counted in this clip", font=f_s, fill=SOFT)
        d.text((40, 260), "monsters killed", font=f_lab, fill=SOFT)
        d.text((40, 310), str(k), font=f_big, fill=INK)
        d.text((40, 620), "kill sounds played", font=f_lab, fill=SOFT)
        d.text((40, 670), str(s), font=f_big, fill=SPARK)
        d.text((40, 980), "SFX-01 · 60 ms cooldown\nat most 3 voices", font=f_lab, fill=SOFT, spacing=14)
        return (k, s)
    return render_panel(name, 614, 1555, n_frames / FPS, draw), kills, sounds


def b12():
    bid, d = "B12", dur("B12")
    t = Take("main")
    f0 = int(189.0 * FPS)
    n = round(d * FPS)
    panel, kills, sounds = counter_panel("B12-count", t, f0, n, "The throttle")
    t_q = at(bid, "nothing ran together")
    layers = frame_chrome("A dense wave, counted", f"Real engine capture, main take, run {t.clock(f0)}–{t.clock(f0 + n)} · source revision {SHA}",
                          "counts from the take's play log and kill signal")
    layers += [video("main", f0, PAD, TOP, 2764, 1555),
               {"kind": "video", "src": panel, "ss": 0, "x": 3015, "y": TOP, "w": 614, "h": 1555, "t": [0, d]}]
    layers.append({"kind": "rect", "x": PAD + 80, "y": TOP + 1170, "w": 2600, "h": 300, "fill": "#FAF9F5F0", "radius": 24,
                   "t": [t_q, 9999], "fade": 0.3})
    layers.append(text("Bao, Run A (sound on): “不会连起来”", PAD + 140, TOP + 1210, 72, INK, "cjk", t_in=t_q))
    layers.append(text("“they don’t run together” · evidence/playtest/2026-10-01-runs-A-B.md", PAD + 140, TOP + 1330, 46, SOFT, "sans", t_in=t_q))
    spec_write(bid, layers, d)


def key_cap(label, x, y, t_in, t_out, size=120):
    w = max(size * 1.4, size * 0.6 * len(label) + size * 0.8)
    return [{"kind": "rect", "x": x, "y": y, "w": int(w), "h": int(size * 1.25), "fill": CARD, "outline": INK, "width": 8,
             "radius": 24, "t": [t_in, t_out], "fade": 0.08},
            text(label, x, y + int(size * 0.18), size * 0.72, INK, "sans-medium", w=int(w), align="center", t_in=t_in,
                 t_out=t_out, fade=0.08)]


def b14():
    bid, d = "B14", dur("B14")
    t = Take("main")
    p0, p1 = [t.frame(e) for e in t.find("action", action="pause")]
    f0 = p0 - 45
    a, b = (p0 - f0) / FPS, (p1 - f0) / FPS
    layers = frame_chrome("Pause: the field freezes, the music muffles", f"Real engine capture, main take, run 0:40 · source revision {SHA}",
                          "Esc sent through the input map")
    layers.append(video("main", f0, PAD, TOP, 2764, 1555))
    x = 3015
    layers.append({"kind": "rect", "x": x, "y": TOP, "w": 614, "h": 1555, "fill": CARD, "outline": BORDER, "width": 3, "radius": 28})
    layers += key_cap("Esc", x + 60, TOP + 60, a, a + 0.9)
    layers.append(text("PAUSED\nlow-pass 900 Hz\nmusic −10 dB", x + 50, TOP + 300, 54, SPARK, "sans-medium", w=540, t_in=a, t_out=b))
    layers += key_cap("Esc", x + 60, TOP + 700, b, b + 0.9)
    layers.append(text("PLAYING\nfilter off, 0 dB", x + 50, TOP + 940, 54, INK, "sans-medium", w=520, t_in=b))
    layers.append(text("timer before and after: 0:40", x + 50, TOP + 1250, 46, SOFT, "sans", w=520, t_in=at(bid, "timer reads")))
    spec_write(bid, layers, d)


def b19():
    bid, d = "B19", dur("B19")
    t = Take("main")
    lv = [t.frame(e) for e in t.find("sfx", id="levelup")][5]
    evo = t.frame(t.find("sfx", id="evolve")[0])
    f0 = lv - 35
    a, b = (lv - f0) / FPS, (evo - f0) / FPS
    layers = frame_chrome("The evolution in the run", f"Real engine capture, main take, run 0:58 · source revision {SHA}")
    layers.append(video("main", f0, PAD, TOP, 2764, 1555))
    x = 3015
    layers.append({"kind": "rect", "x": x, "y": TOP, "w": 614, "h": 1555, "fill": CARD, "outline": BORDER, "width": 3, "radius": 28})
    layers.append(text("card screen", x + 50, TOP + 60, 50, SOFT, "sans", t_in=a))
    layers.append(text("Sunflare Lighthouse offered first\n(beam 3/3, moths 3/3)", x + 50, TOP + 130, 50, INK, "sans-medium", w=540, t_in=a))
    layers.append(text("card taken", x + 50, TOP + 560, 50, SOFT, "sans", t_in=b))
    layers.append(text("SFX-05 evolve\nbanner\nzoom-out to 0.72\nsunflare pose\nbrighter coat\nMUS-02 fades in", x + 50, TOP + 630, 50,
                       SPARK, "sans-medium", w=540, t_in=b, spacing=1.4))
    spec_write(bid, layers, d)


def b22():
    bid, d = "B22", dur("B22")
    t = Take("props")
    f0 = t.start + 90                          # run 0:03, still walking to the stall (pushing starts at tick 360)
    layers = frame_chrome("Blocked, then sliding", f"Real engine capture, props take · source revision {SHA}",
                          "scripted input through the real input map")
    cx, cy, zoom = t.pos4k(t.start + 200)
    layers.append({"kind": "rect", "x": PAD, "y": TOP, "w": 2420, "h": 1365, "fill": DARK, "radius": 24})
    layers.append(video("props", f0, PAD + 10, TOP + 10, 2400, 1345, crop=crop_around(cx + 120, cy - 40, 1600, 896)))
    x = PAD + 2500
    a_right = (t.start + 180 - f0) / FPS
    a_diag = (t.start + 240 - f0) / FPS
    layers.append(text("walking to the nearest stall", x, TOP, 54, INK, "sans-medium", w=W - PAD - x, t_out=a_right))
    layers.append(text("holding → : stopped at the stall's edge", x, TOP + 160, 54, INK, "sans-medium", w=W - PAD - x, t_in=a_right))
    layers.append(text("holding ↘ : slides along the edge", x, TOP + 330, 54, SPARK, "sans-medium", w=W - PAD - x, t_in=a_diag))
    t_box = at(bid, "The box")
    WORK.mkdir(parents=True, exist_ok=True)
    stall = Image.open(REPO / "godot/assets/art/env_stall.png").convert("RGBA")
    k = 10
    big = Image.new("RGBA", (stall.width * k, stall.height * k), "#1F2540")
    big.alpha_composite(stall.resize((stall.width * k, stall.height * k), Image.NEAREST))
    dr = ImageDraw.Draw(big)
    # SOLID_BOX stall Rect2(-19, -18, 39, 39) relative to the sprite centre (32, 24)
    x0, y0 = (32 - 19) * k, (24 - 18) * k
    dr.rectangle((x0, y0, x0 + 39 * k, y0 + 39 * k), outline="#D97757", width=6)
    p = WORK / "stall-box.png"
    big.save(p)
    layers.append({"kind": "image", "src": str(p.relative_to(REEL)), "x": x, "y": TOP + 560, "w": 900, "h": 675, "t": [t_box, 9999], "fade": 0.3})
    layers.append(text("diagnostic overlay: SOLID_BOX stall (−19, −18, 39 × 39) on env_stall.png ×10", x, TOP + 1260, 40, SOFT, "sans",
                       w=900, t_in=t_box))
    spec_write(bid, layers, d)


def b24():
    bid, d = "B24", dur("B24")
    t = Take("props")
    keys = [(t.frame(e), e["action"]) for e in t.find("action") if e["action"].startswith("mute")]
    n = round(d * FPS)
    f0 = len(t.track) - 1 - n
    layers = frame_chrome("Mute changes the mixer, not the game", f"Real engine capture, props take · source revision {SHA}",
                          "M / 9 / 0 sent through the input map")
    layers.append(video("props", f0, PAD, TOP, 2764, 1555))
    layers.append({"kind": "rect", "x": PAD + 1380, "y": TOP + 1240, "w": 1360, "h": 272, "fill": DARK, "radius": 20})
    layers.append(video("props", f0, PAD + 1400, TOP + 1260, 1320, 232, crop=[3100, 20, 740, 130]))
    layers.append(text("HUD corner, enlarged", PAD + 1400, TOP + 1140, 40, "#FFF1C9", "sans"))
    x = 3015
    layers.append({"kind": "rect", "x": x, "y": TOP, "w": 614, "h": 1555, "fill": CARD, "outline": BORDER, "width": 3, "radius": 28})
    names = {"mute_all": "M", "mute_music": "9", "mute_sfx": "0"}
    for k, (fr, act) in enumerate(keys):
        ta = (fr - f0) / FPS
        tb = (keys[k + 1][0] - f0) / FPS if k + 1 < len(keys) else d
        layers += key_cap(names[act], x + 200, TOP + 120, ta, tb - 0.05, size=150)
        what = {"mute_all": "all audio", "mute_music": "music", "mute_sfx": "effects"}[act]
        layers.append(text(f"{what}: {'off' if k % 2 == 0 else 'on'}", x + 50, TOP + 400, 56, SPARK if k % 2 == 0 else INK,
                           "sans-medium", w=520, t_in=ta, t_out=tb - 0.05, fade=0.08))
    layers.append(text("the run never pauses", x + 50, TOP + 1300, 46, SOFT, "sans", w=520))
    spec_write(bid, layers, d)


def overlay_frame(take_key, frame, centre, cw, ch, size, name, view, kind, note):
    """A held frame with labelled diagnostic overlays: the old hit circle (r = 10) and the visible sprite box."""
    crop = crop_around(centre[0], centre[1], cw, ch)
    src = REEL / extract_still(take_key, frame, crop, size, name)
    im = Image.open(src).convert("RGBA")
    s = size[0] / cw                    # display px per 4K px
    dr = ImageDraw.Draw(im)
    mx, my = view["monster"][0] * 6, view["monster"][1] * 6
    px, py = (mx - crop[0]) * s, (my - crop[1]) * s
    r = 10 * 6 * s
    for a in range(0, 360, 12):         # dashed circle
        dr.arc((px - r, py - r, px + r, py + r), a, a + 6, fill="#7FE3FF", width=7)
    hx, hy = (11 + 1) * 6 * s, (7 + 1) * 6 * s if kind == "moth" else (19 + 1) * 6 * s
    if kind != "moth":
        hx = (13 + 1) * 6 * s
    dr.rectangle((px - hx, py - hy, px + hx, py + hy), outline="#FFB347", width=7)
    f = font("sans-medium", 40)
    dr.rectangle((0, size[1] - 70, size[0], size[1]), fill=(20, 18, 28, 200))
    dr.text((24, size[1] - 60), note, font=f, fill="#FFF1C9")
    im.save(src)
    return str(src.relative_to(REEL))


def b17():
    bid, d = "B17", dur("B17")
    before = Take("before")
    main = Take("main")
    # read-only diagnostic records (capture driver) with screen positions from the identical dry runs
    btr = [json.loads(l) for l in (REEL / TAKES["before"][2]).read_text().splitlines()]
    mtr = [json.loads(l) for l in (REEL / TAKES["main"][2]).read_text().splitlines()]
    pt = next(e for e in btr if e["event"] == "pass_through" and e["first"] == 4015)
    eh = next(e for e in mtr if e["event"] == "edge_hit" and e["first"] == 433)
    fb = (pt["first"] - 1) // 2 - 1          # movie frame drawn with the state the record saw (see capture_driver.gd)
    fa = (eh["first"] - 1) // 2 - 1
    cw, ch, size = 400, 300, (1560, 1170)
    cb = (pt["view_first"]["monster"][0] * 6 + 30, pt["view_first"]["monster"][1] * 6 - 40)   # moth and the bolt's path
    ca = (eh["view_first"]["monster"][0] * 6 + 55, eh["view_first"]["monster"][1] * 6)
    t_right, t_tests = at(bid, "On the right"), at(bid, "Two tests")
    layers = frame_chrome("Before and after the hit-test change",
                          "Real engine captures, same capture driver: build 40102ab (seed 14) and the film build (seed 11)",
                          "held frames and overlays labelled")
    xl, xr, y = PAD, PAD + 1660, TOP + 110
    layers.append(text("Before · build 40102ab, the one Bao first played", xl, TOP, 52, INK, "sans-medium"))
    layers.append(text(f"After · film build {SHA}", xr, TOP, 52, INK, "sans-medium", t_in=t_right))
    seq_b = [(fb, "held · bolt touches the sprite box, not the old circle → no hit"), (fb + 1, "next frame · still flying"),
             (fb + 2, "next frame · the moth is untouched")]
    seq_a = [(fa, "held · bolt at the wing tip, outside the old circle"), (fa + 1, "next frame · hit: the moth drops a gem, bolt gone")]
    tb = [0.3, 3.2, 4.6, t_right]
    for k, (fr, note) in enumerate(seq_b):
        src = overlay_frame("before", fr, cb, cw, ch, size, f"b17-before-{k}", pt["view_first"], "moth", note) if k == 0 else \
            extract_note("before", fr, cb, cw, ch, size, f"b17-before-{k}", note)
        layers.append({"kind": "image", "src": src, "x": xl, "y": y, "w": size[0], "h": size[1], "t": [tb[k], tb[k + 1] if k < 2 else d]})
    ta = [t_right + 0.2, t_right + 3.2, d]
    for k, (fr, note) in enumerate(seq_a):
        src = overlay_frame("main", fr, ca, cw, ch, size, f"b17-after-{k}", eh["view_first"], "moth", note) if k == 0 else \
            extract_note("main", fr, ca, cw, ch, size, f"b17-after-{k}", note)
        layers.append({"kind": "image", "src": src, "x": xr, "y": y, "w": size[0], "h": size[1], "t": [ta[k], ta[k + 1]]})
    layers.append(text("dashed: the old test (centre within 10 px) · box: the visible sprite (moth 11 × 7 half-size, +1)", xl,
                       y + size[1] + 30, 42, SOFT, "sans", w=W - 2 * PAD))
    layers.append(text("beam-stops-on-moth-wing  RED → GREEN   ·   beam-stops-on-wraith-hood  RED → GREEN   ·   control: beam-misses-when-clear-of-sprite",
                       xl, y + size[1] + 110, 44, INK, "mono", w=W - 2 * PAD, t_in=t_tests))
    layers.append(text("Bao, next playtest: “子弹对的” — the bullets are right", xl, y + size[1] + 210, 56, SPARK, "cjk",
                       w=W - 2 * PAD, t_in=t_tests + 1.0))
    spec_write(bid, layers, d)


def extract_note(take_key, frame, centre, cw, ch, size, name, note):
    crop = crop_around(centre[0], centre[1], cw, ch)
    src = REEL / extract_still(take_key, frame, crop, size, name)
    im = Image.open(src).convert("RGBA")
    dr = ImageDraw.Draw(im)
    dr.rectangle((0, size[1] - 70, size[0], size[1]), fill=(20, 18, 28, 200))
    dr.text((24, size[1] - 60), note, font=font("sans-medium", 40), fill="#FFF1C9")
    im.save(src)
    return str(src.relative_to(REEL))


def b28():
    bid, d = "B28", dur("B28")
    out = (REEL / "capture/test-run-film-build.txt").read_text().rstrip("\n")
    rec = json.loads((REEL / "capture/test-run-independence.json").read_text())
    t_ind, t_play = at(bid, "The independence check"), at(bid, "Bao played it twice")
    layers = frame_chrome("Recorded output, film build", f"godot --headless --script res://tests/test_*.gd on an isolated copy of {SHA}",
                          "output verbatim")
    layers.append({"kind": "rect", "x": PAD, "y": TOP, "w": 1900, "h": 1555, "fill": "#14121C", "radius": 24})
    layers.append(text(out, PAD + 50, TOP + 40, 40, "#E8E6DF", "mono", w=1800, spacing=1.3))
    x = PAD + 1980
    layers.append({"kind": "rect", "x": x, "y": TOP, "w": W - PAD - x, "h": 860, "fill": CARD, "outline": BORDER, "width": 3,
                   "radius": 24, "t": [t_ind, 9999], "fade": 0.3})
    layers.append(text("independence (test_audio.gd)", x + 50, TOP + 40, 54, INK, "sans-medium", t_in=t_ind))
    keys = ["state", "tick", "kills", "level", "hp", "x", "y"]
    rows = "\n".join(f"{k:<7}{str(rec['with_sound'][k]):>12}{str(rec['silent'][k]):>12}" for k in keys)
    layers.append(text(f"{'':<7}{'sound':>12}{'silent':>12}\n" + rows, x + 50, TOP + 150, 48, INK, "mono", spacing=1.35, t_in=t_ind + 0.2))
    layers.append({"kind": "rect", "x": x, "y": TOP + 920, "w": W - PAD - x, "h": 635, "fill": "#FBEFE9", "outline": SPARK, "width": 4,
                   "radius": 24, "t": [t_play, 9999], "fade": 0.3})
    layers.append(text("Bao's playtests, 2026-10-01", x + 50, TOP + 960, 52, INK, "sans-medium", t_in=t_play))
    layers.append(text("Run A, sound on: “只响一次，不会连起来，不会，没有空白”", x + 50, TOP + 1060, 48, INK, "cjk", w=W - PAD - x - 100, t_in=t_play + 0.2))
    layers.append(text("Run B, muted: “第二局都能”", x + 50, TOP + 1230, 48, INK, "cjk", w=W - PAD - x - 100, t_in=t_play + 0.5))
    layers.append(text("build 1b24721, before the review fixes", x + 50, TOP + 1400, 40, SOFT, "sans", t_in=t_play + 0.5))
    spec_write(bid, layers, d)


def board_columns(bid, title, source, cols, extra=None):
    d = dur(bid)
    layers = frame_chrome(title, source)
    n = len(cols)
    gap = 60
    cw = (W - 2 * PAD - gap * (n - 1)) // n
    for k, (head, phrase, items, accent) in enumerate(cols):
        t_in = at(bid, phrase) if phrase else 0.0
        x = PAD + k * (cw + gap)
        layers.append({"kind": "rect", "x": x, "y": TOP, "w": cw, "h": 1555, "fill": CARD, "outline": accent or BORDER,
                       "width": 4 if accent else 3, "radius": 28, "t": [t_in, 9999], "fade": 0.3})
        layers.append(text(head, x + 56, TOP + 50, 92, INK, "serif", w=cw - 100, t_in=t_in))
        layers.append(text("\n\n".join(items), x + 56, TOP + 240, 60, INK, "sans", w=cw - 110, spacing=1.32,
                           t_in=t_in + 0.2))
    if extra:
        layers += extra(d)
    spec_write(bid, layers, d)


def b29():
    board_columns("B29", "Who did what · which model made what", "FRICTIONAL.md (header) · SOURCES.md · gen/log/*/ sidecars", [
        ("Bao Xing", "", ["genre, theme, scope, local-only models", "every accept / reject call (94 of 99 runs)",
                          "listened to every sound-effect candidate", "playtests: sound on and muted", "every change request"], SPARK),
        ("Claude", "Claude wrote", ["Godot code and the 122 checks", "generation and processing scripts",
                                    "ran the models; measured candidates", "suggested picks; drafted the documents"], None),
        ("Local models", "FLUX made", ["FLUX.1-schnell @ 741f7c3: all 14 art assets (ART-PC-01, EN-01/02, ENV-01…07, FX-01…03, PK-01)",
                                       "Stable Audio Open 1.0 @ f21265c: SFX-01…05, 06a, 06b",
                                       "MusicGen-medium @ d3bd7b0: MUS-01, MUS-02",
                                       "MusicGen-melody @ 68d653a: one MUS-02 batch, all rejected"], None)],
        extra=lambda d: [text("5 MUS-02 rejects came from an automated layer check that Bao did not listen to; they are logged that way.",
                              PAD, 1924, 40, SOFT, "sans", w=W - 2 * PAD, t_in=at("B29", "MusicGen both"))])


def b30():
    board_columns("B30", "Tested · uncertain · next", "TEST-REPORT.md §3, §12, §16 · CONCEPT.md (semester goal)", [
        ("Tested", "", ["122 automated checks pass (logic 32, gameplay 65, audio 25)", "loop seams, palettes, tile seam, repo audit",
                        "Bao: Run A sound on, Run B muted", "fresh local clone runs"], None),
        ("Still uncertain", "What's still uncertain", ["fog-wraith contrast lowest (0.03)", "hurtbox (r = 10) reaches the lower lamp",
                                                     "gamepad untested", "balance: Bao + scripted bots only",
                                                     "playtests predate the review fixes (tests cover them)"], SPARK),
        ("Next", "Next:", ["more weapons and evolutions", "a boss at the end of the fog", "between-run progression, saving",
                           "more than one market map"], None)])


BUILDERS = {"B03": b03, "B04": b04, "B05": b05, "B06": b06, "B08": b08, "B10": b10, "B12": b12, "B14": b14, "B15": b15,
            "B17": b17, "B19": b19, "B20": b20, "B22": b22, "B24": b24, "B25": b25, "B26": b26, "B28": b28, "B29": b29,
            "B30": b30}

if __name__ == "__main__":
    todo = sys.argv[1:] or list(BUILDERS)
    for bid in todo:
        print("[media]", bid, flush=True)
        BUILDERS[bid]()
