"""
kit.py — the lecture's shared drawing + pacing kit. NOT imported: assemble_scenes.py pastes it at the top of
scenes.py (Gate A copies only scenes.py). It is show-tell's iso_kit (palette, Iso projection, pacing helpers
until/finish) plus the midpoint guard (ST/guard/done) from show-tell-context-is-a-budget, plus a few lecture helpers.
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)


# ─────────────── midpoint guard: GATE T and Gate V sample each clip at its MIDPOINT ───────────────
class ST:
    """No animation straddles the clip midpoint: one that would cross it is shortened to land before it, or
    starts just after it, so the midpoint frame is always a still. assemble_scenes.py attaches it to every
    beat class (the classes stay literal `(Scene)` for run.sh's scene discovery)."""
    def play(self, *anims, **kw):
        if not all(isinstance(a, Wait) for a in anims):
            kw["run_time"] = guard(self, float(kw.get("run_time", 1.0)))
        return Scene.play(self, *anims, **kw)


def guard(self, rt):
    """Returns the run time to use so an animation of length rt starting now does not straddle the midpoint.
    Call it BEFORE staging anything off-position."""
    tgt = _TARGET.get(type(self).__name__.split("_")[0], 0)
    if not tgt:
        return rt
    mid, t0 = tgt / 2.0, _elapsed(self)
    if t0 < mid + 0.06 and t0 + rt > mid - 0.06:
        room = mid - 0.08 - t0
        if room >= 0.6 * rt and room > 0.25:
            return room
        Scene.wait(self, max(0.02, mid + 0.08 - t0))
    return rt


def done(self):
    """finish() plus a pacing report (a clip must not outrun its audio: compile centre-cuts it)."""
    bid = type(self).__name__.split("_")[0]
    t = _elapsed(self)
    tgt = _TARGET.get(bid, 0)
    print(f"[pace] {bid} content={t:.2f}s target={tgt:.2f}s" + ("  OVER" if t > tgt - 0.1 else ""))
    if tgt:
        self.wait(max(0.05, tgt - t - 0.05))     # end 0.05 s under the audio (4K frame rounding)
    else:
        self.wait(2.0)


# ─────────────── lecture helpers ───────────────
MONO = "Menlo"


def M(s, size=32, color=INK):
    """Monospace text for real code/log lines (Menlo). Size floor 32 at this frame."""
    return Text(s, font=MONO, color=color, font_size=size)


def dim_arrow(a, b, color=INK, w=5, tip=0.16):
    """A dimension line with arrow tips at both ends (a, b are scene points)."""
    return DoubleArrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w,
                       tip_length=tip, max_tip_length_to_length_ratio=0.45)


# ══════════════════════════════ scenes_act1.py ══════════════════════════════
"""ACT I · What Godot Is  (B01–B05, all Manim)

One cast for the act: REAL captures shown as themselves in grey-framed windows on the cream stage: godotengine.org (home, licence,
download) and a real Godot game (Walker Pong, a recorded run, scripted input), plus real text from this Mac (the `godot --help`
copyright line, `du -sh`, the walker-claude player.gd lines). Drawings carry only ideas (a card pair, two bars, an indent guide)
and are labelled; the one Python block is labelled "illustrative". Nothing is mocked: every capture was taken 2026-10-09.

Frames of the Pong clip: pantry/a1_pong_001..105.jpg (15 fps, cropped to the playfield, 1152x720) from
_conducting-series-evidence/godot-captures/walker-pong/walker-pong-clip.mp4 (ffmpeg, see evidence/act1/README-evidence.md).
"""

A1P = "pantry/"
_A1_FR = {}


def a1_rgba(name):
    """A pantry frame as an RGBA array (cached) for the video updater."""
    if name not in _A1_FR:
        from PIL import Image
        _A1_FR[name] = np.array(Image.open(A1P + name).convert("RGBA"))
    return _A1_FR[name]


def a1_window(name, w, cx, cy):
    """A real capture shown as itself: the image, and a grey (DIM) frame just outside its edge."""
    im = ImageMobject(A1P + name)
    im.set_width(w)
    im.move_to([cx, cy, 0])
    fr = Rectangle(width=w + 0.1, height=im.height + 0.1, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    return im, fr


def a1_clip(prefix, n, fps, w, cx, cy):
    """A real recorded clip as a window: a pantry frame sequence stepped in time by an updater (starts when added)."""
    im = ImageMobject(A1P + f"{prefix}001.jpg")
    im.set_width(w)
    im.move_to([cx, cy, 0])
    im.a1c = dict(t=0.0, last=0)

    def tick(m, dt):
        a = m.a1c
        a["t"] += dt
        i = min(n - 1, int(a["t"] * fps))
        if i != a["last"]:
            a["last"] = i
            m.pixel_array = a1_rgba(f"{prefix}{i + 1:03d}.jpg")
    im.add_updater(tick)
    fr = Rectangle(width=w + 0.1, height=im.height + 0.1, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    return im, fr


def a1_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_left(mob, x_left, y):
    """Place a mob so its left edge is at x_left (explicit coordinate; width is the mob's own)."""
    mob.move_to([x_left + mob.width / 2.0, y, 0])
    return mob


def a1_no(x, y, r=0.3, sw=6):
    """A prohibition mark in grey (DIM): ring + bar. Sits beside text, never around it."""
    ring = Circle(radius=r, stroke_color=DIM, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=DIM, stroke_width=sw)
    return VGroup(ring, bar)


# ═════════════════════════════ B01 · what Godot is ═════════════════════════════
class B01_WhatGodotIs(Scene):
    def construct(self):
        title = T("What Godot Is", 40).to_corner(UL, buff=0.95)
        pimg, pfr = a1_clip("a1_pong_", 105, 15, 5.4, -3.1, 0.3)
        pl1 = a1_t("a game running in Godot", -3.1, -1.72)
        pl2 = a1_t("recorded run, scripted input", -3.1, -2.22)
        self.add(title, pimg)
        self.play(FadeIn(pfr), FadeIn(pl1), FadeIn(pl2), run_time=0.5)
        # the four things the engine runs, one word at a time on the spoken word (one Text so the baseline is shared)
        row = T("graphics         physics         input         sound", 36).move_to([0.3, -2.92, 0])
        spans = [(0, 8), (8, 15), (15, 20), (20, 25)]
        for (a, b), ph in zip(spans, ("graphics", "physics", "input", "sound")):
            wd = VGroup(*row[a:b])
            dot = Dot([wd.get_center()[0] - wd.width / 2.0 - 0.3, -2.92, 0], radius=0.09, color=INK)
            until(self, ph, lead=0.1)
            self.play(GrowFromCenter(dot), FadeIn(wd), run_time=0.35)
        # with an editor to build it in: a REAL Godot 4.7.2 editor window (it lands after the midpoint: its dark UI fails GATE T at the 50% sample)
        himg, hfr = a1_window("a1_editor.png", 6.0, 3.1, 0.3)
        hl1 = a1_t("the Godot editor", 3.1, -1.72)
        hl2 = a1_t("captured 9 Oct 2026", 3.1, -2.22)
        until(self, "with an editor", lead=0.2)
        self.play(FadeIn(himg), FadeIn(hfr), FadeIn(hl1), FadeIn(hl2), run_time=0.5)
        done(self)


# ═════════════════════════════ B02 · free, open source, MIT ═════════════════════════════
class B02_FreeOpenSource(Scene):
    def construct(self):
        wimg, wfr = a1_window("a1_license_crop.png", 7.0, -2.3, 0.2)
        wl1 = a1_t("godotengine.org/license", -2.3, -2.2)
        wl2 = a1_t("captured 9 Oct 2026", -2.3, -2.72)
        self.play(FadeIn(wimg), FadeIn(wfr), FadeIn(wl1), FadeIn(wl2), run_time=0.6)
        until(self, "under the M I T licence", lead=0.2)
        # the row of the page that says "MIT license" sits at y = +1.47 in the window; the dot marks that row outside the frame
        dot = Dot([1.75, 1.47, 0], radius=0.11, color=TERRA)
        mit = a1_left(T("MIT license", 40), 2.15, 1.47)
        self.play(GrowFromCenter(dot), FadeIn(mit), run_time=0.4)
        rows = []
        for i, (wd, ph) in enumerate((("No account", "No account"), ("No fee", "No fee"), ("No royalty", "No royalty"))):
            y = 0.5 - 0.95 * i
            mark = a1_no(1.75, y)
            lab = a1_left(T(wd, 40), 2.3, y)
            rows.append((mark, lab, ph))
        for mark, lab, ph in rows:
            until(self, ph, lead=0.15)
            self.play(Create(mark), FadeIn(lab), run_time=0.4)
        done(self)


# ═════════════════════════════ B03 · stewardship, not ownership ═════════════════════════════
class B03_LooksAfterNotOwns(Scene):
    def construct(self):
        cl = RoundedRectangle(width=5.2, height=3.2, corner_radius=0.2, stroke_color=DIM, stroke_width=4).move_to([-3.3, 0.95, 0])
        cr = RoundedRectangle(width=5.2, height=3.2, corner_radius=0.2, stroke_color=DIM, stroke_width=4).move_to([3.3, 0.95, 0])
        hl = a1_t("Godot Foundation", -3.3, 2.05, 36)
        hr = a1_t("Contributors", 3.3, 2.05, 36)
        sub = a1_t("a non-profit", -3.3, 1.55)
        self.play(Create(cl), Create(cr), FadeIn(hl), FadeIn(hr), FadeIn(sub), run_time=0.7)
        # its name: a tag
        tag = VGroup(Polygon([-0.32, 0.2, 0], [0.12, 0.2, 0], [0.36, 0, 0], [0.12, -0.2, 0], [-0.32, -0.2, 0],
                             stroke_color=INK, stroke_width=5, fill_opacity=0),
                     Dot([-0.14, 0, 0], radius=0.06, color=INK)).move_to([-5.2, 0.8, 0])
        name = a1_left(T("its name", 36), -4.75, 0.8)
        # its money: a coin
        coin = VGroup(Circle(radius=0.27, stroke_color=INK, stroke_width=5), Dot(radius=0.07, color=INK)).move_to([-5.2, 0.05, 0])
        money = a1_left(T("its money", 36), -4.75, 0.05)
        until(self, "its name", lead=0.2)
        self.play(GrowFromCenter(tag), FadeIn(name), run_time=0.4)
        until(self, "its money", lead=0.2)
        self.play(GrowFromCenter(coin), FadeIn(money), run_time=0.4)
        # it does not own the engine: an ownership arrow across the gap, struck out
        arr = Arrow([-0.62, 0.95, 0], [0.62, 0.95, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        own = a1_t("owns", 0, 1.5, 32)
        no = a1_no(0, 0.95, r=0.3, sw=6)
        until(self, "It does not own", lead=0.2)
        self.play(Create(arr), FadeIn(own), run_time=0.4)
        self.play(Create(no), run_time=0.3)
        # the code belongs to its contributors: the real copyright line printed by `godot --help`
        c1 = M("(c) 2014-present", 32)
        c2 = M("Godot Engine", 32)
        c3 = M("contributors.", 32)
        code = VGroup(c1, c2, c3).arrange(DOWN, buff=0.22).move_to([3.3, 0.55, 0])
        cap = a1_t("printed by godot --help", 3.3, -1.1)
        until(self, "The code belongs", lead=0.2)
        self.play(FadeIn(code), FadeIn(cap), run_time=0.5)
        # no company can buy it: Godot's own governance words, quoted (not captured)
        q = T("“Godot can't be sold or purchased by any company.”", 36).move_to([0, -2.0, 0])
        qa = a1_t("quoted, not captured: godotengine.org/governance", 0, -2.65)
        until(self, "no company can buy it", lead=0.3)
        self.play(FadeIn(q), FadeIn(qa), run_time=0.5)
        done(self)


# ═════════════════════════════ B04 · version and size ═════════════════════════════
class B04_VersionAndSize(Scene):
    def construct(self):
        # right: Godot's own Mac download page as itself (only the buttons are cropped in: the page's dark artwork fails GATE T)
        dimg, dfr = a1_window("a1_download_btn.jpg", 6.0, 3.1, 0.7)
        dl1 = a1_t("godotengine.org/download/macos", 3.1, -0.75)
        dl2 = a1_t("captured 9 Oct 2026", 3.1, -1.25)
        hero = T("4.7.2", 88).move_to([-3.0, 2.55, 0])
        self.add(hero)
        self.play(FadeIn(dimg), FadeIn(dfr), FadeIn(dl1), FadeIn(dl2), run_time=0.6)
        until(self, "released on", lead=0.2)
        dstamp = a1_t("stable, 18 August 2026", -3.0, 1.7, 36)
        self.play(FadeIn(dstamp), run_time=0.4)
        # sizes: bars in greys, in BYTES (1 MB = 1e6 B = 0.0143 scene units), left edge x = -5.9. GitHub says 170,622,178 B = 170.6 MB;
        # du -sh prints 337M, which is MiB (337 x 1,048,576 B = 353.4 MB), so the second bar is drawn 353.4 MB long, not 337.
        S = 0.0143
        l1 = a1_left(T("170.6 MB: GitHub release zip", 32), -5.9, 0.85)
        b1 = Rectangle(width=170.6 * S, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.9 + 170.6 * S / 2, 0.35, 0])
        l2 = a1_left(T("337M: du -sh on this Mac", 32), -5.9, -0.5)
        b2 = Rectangle(width=353.4 * S, height=0.4, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.9 + 353.4 * S / 2, -1.0, 0])
        until(self, "The Mac download", lead=0.2)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(GrowFromEdge(b1, LEFT), run_time=0.7)
        until(self, "Installed on this Mac", lead=0.2)
        self.play(FadeIn(l2), run_time=0.3)
        self.play(GrowFromEdge(b2, LEFT), run_time=0.9)
        # one application file: a tile and its name
        tile = VGroup(RoundedRectangle(width=0.8, height=0.8, corner_radius=0.14, stroke_color=INK, stroke_width=5),
                      Dot(radius=0.08, color=TERRA)).move_to([-5.5, -2.15, 0])
        tl = a1_left(T("one application file", 32), -4.85, -2.15)
        until(self, "One application file", lead=0.2)
        self.play(GrowFromCenter(tile), FadeIn(tl), run_time=0.5)
        done(self)


# ═════════════════════════════ B05 · GDScript ═════════════════════════════
class B05_GDScriptAndCSharp(Scene):
    def construct(self):
        XL = -6.0
        # GDScript: three real lines of walker-claude/godot/features/player/player.gd (lines 33-35), tab-indented in the file
        d1 = Dot([XL + 0.1, 2.95, 0], radius=0.09, color=TERRA)
        g_lab = a1_left(T("GDScript: real code from the Claude Walker project", 32), XL + 0.4, 2.95)
        g_h = a1_left(M("func reset_at(spawn: Vector2) -> void:", 32), XL, 2.2)
        g_1 = a1_left(M("position = spawn", 32), XL + 0.9, 1.65)
        g_2 = a1_left(M("velocity = Vector2.ZERO", 32), XL + 0.9, 1.1)
        self.play(FadeIn(g_lab), GrowFromCenter(d1), run_time=0.4)
        until(self, "Games are written", lead=0.1)
        self.play(FadeIn(g_h), FadeIn(g_1), FadeIn(g_2), run_time=0.5)
        # Python: the same idea, illustrative
        until(self, "built for Godot", lead=0.4)
        d2 = Dot([XL + 0.1, 0.35, 0], radius=0.09, color=TERRA)
        p_lab = a1_left(T("Python: the same idea, illustrative (not Godot code)", 32), XL + 0.4, 0.35)
        p_h = a1_left(M("def reset_at(spawn: Vector2) -> None:", 32), XL, -0.4)
        p_1 = a1_left(M("position = spawn", 32), XL + 0.9, -0.95)
        p_2 = a1_left(M("velocity = Vector2.ZERO", 32), XL + 0.9, -1.5)
        self.play(FadeIn(p_lab), GrowFromCenter(d2), FadeIn(p_h), FadeIn(p_1), FadeIn(p_2), run_time=0.6)
        # reads a lot like Python: the same indent guide down both blocks
        until(self, "reads a lot like Python", lead=0.2)
        gu1 = Line([XL + 0.4, 1.9, 0], [XL + 0.4, 0.85, 0], color=DIM, stroke_width=5)
        gu2 = Line([XL + 0.4, -0.65, 0], [XL + 0.4, -1.75, 0], color=DIM, stroke_width=5)
        self.play(Create(gu1), Create(gu2), run_time=0.5)
        # or in C sharp: the .NET build, as a chip; the example project: all scripts are .gd
        until(self, "or in C sharp", lead=0.2)
        chip = a1_left(T("C#: needs the .NET build", 32), 1.4, -2.55)
        cd = Dot([1.05, -2.55, 0], radius=0.09, color=INK)
        self.play(GrowFromCenter(cd), FadeIn(chip), run_time=0.4)
        until(self, "The example games", lead=0.2)
        ex = a1_left(T("Claude Walker: 11 scripts, all .gd", 32), XL + 0.4, -2.55)
        ed = Dot([XL + 0.1, -2.55, 0], radius=0.09, color=INK)
        self.play(GrowFromCenter(ed), FadeIn(ex), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · A Scene Is a Text File  (B06–B14, all Manim)

One cast for the act: THE REAL TEXT of the real runs, shown as recorded text in plain outlined windows on the cream stage
(never as a live screen, never mocked): the real pong.tscn (EVID/godot-evidence/part2/pong.tscn.before), the real `file` output
(evidence/act2/file-check.txt, run 2026-10-09 on this Mac), the real tool calls of the recorded run
(part2/04-tool-calls-and-results.txt), the real independent checks (part2/independent-checks.txt), the real diff (part2/pong.tscn.diff)
and Godot's own re-saved copy (part2/pong.resaved-by-godot.tscn). Real game: the Walker Pong capture (godot-captures/walker-pong,
scripted input, recorded 2026-10-09), frames in pantry/a2_pong_NN.png (8 fps, game area only: crop 1728x1080 of the 1920x1080 clip).
Every line is verbatim; where a line is shortened the cut is shown with a visible ellipsis (Menlo 32 is 0.25 units per character,
so a 69-character node line cannot fit beside anything else). Pacing: cues are the real spoken word times (faster-whisper,
evidence/act2/word_times.json) through a2_at().
GATE T: the dark Pong window is small and sits clear of text; the terracotta Dot is only ever a dot (never text, never a stroke).
"""
from PIL import Image as _A2Img

A2P = "pantry/"


def a2_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a2_l(s, x, y, size=34, color=INK):
    """Serif label whose LEFT edge is at x."""
    return T(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a2_c(s, x, y, size=34, color=INK):
    """Serif label centred on x."""
    return T(s, size, color).move_to([x, y, 0])


def a2_m(s, x, y, size=32, color=INK):
    """Menlo text whose first character CELL starts at x (0.25 units per character at size 32), on a common baseline
    (hidden bars at both ends give every row the same ascender/descender box)."""
    t = M("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x - 0.243 * size / 32 + t.width / 2, y, 0])


def a2_win(x0, x1, y0, y1, color=DIM, sw=4):
    """Outline-only window (no fill behind text)."""
    return RoundedRectangle(width=x1 - x0, height=y1 - y0, corner_radius=0.12, stroke_color=color, stroke_width=sw,
                            fill_opacity=0).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def a2_x(cx, cy, s=0.3, color=INK, sw=8):
    return VGroup(Line([cx - s, cy + s, 0], [cx + s, cy - s, 0], color=color, stroke_width=sw),
                  Line([cx - s, cy - s, 0], [cx + s, cy + s, 0], color=color, stroke_width=sw))


def a2_page(cx, cy, w=1.0, h=1.3):
    """A file page: card outline, three ghost text lines."""
    pg = RoundedRectangle(width=w, height=h, corner_radius=0.06, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                          stroke_width=4).move_to([cx, cy, 0])
    ls = VGroup(*[Line([cx - w * 0.3, cy + h * f, 0], [cx + w * 0.3, cy + h * f, 0], color=GHOST, stroke_width=6)
                  for f in (0.25, 0.05, -0.15)])
    return VGroup(pg, ls)


def a2_clip(prefix, n, fps, cx, cy, w):
    """The real capture as stepped frames (pantry/<prefix>NN.png), advancing in scene time through an updater
    (frames are read lazily; a missing file just leaves the first frame, so Gate A's pantry-less copy still builds)."""
    im = ImageMobject(f"{A2P}{prefix}01.png")
    im.set_width(w)
    im.move_to([cx, cy, 0])
    im.a2 = [0.0, {}]

    def upd(m, dt):
        m.a2[0] += dt
        i = int(m.a2[0] * fps) % n + 1
        try:
            if i not in m.a2[1]:
                m.a2[1][i] = np.array(_A2Img.open(f"{A2P}{prefix}{i:02d}.png").convert("RGBA"))
            m.pixel_array = m.a2[1][i]
        except Exception:
            pass
    im.add_updater(upd)
    return im


def a2_pong_clip(cx, cy, w):
    return a2_clip("a2_pong_", 64, 8.0, cx, cy, w)


# ── B06 · a scene is a text file: the real pong.tscn beside the real game ──────────────────────────────────────────────
class B06_RealScene(Scene):
    def construct(self):
        title = T("A Scene Is a Text File", 40).move_to([-6.1, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        a2_at(self, 3.0)                                        # "A Godot scene is a text file"
        win = a2_win(-6.1, 3.46, -2.7, 1.5)
        f_l = a2_l("pong.tscn: 103 lines, excerpt", -6.1, 1.95, 34)
        self.play(Create(win), FadeIn(f_l), run_time=0.45)
        rows = [('[node name="Left" type="Area2D"…', 1.08), ('modulate = Color(0, 1, 1, 1)', 0.62),
                ('position = Vector2(67.6285, 192.594)', 0.16), ('script = ExtResource("1")', -0.30),
                ('[node name="Ball" type="Area2D"…', -1.22), ('position = Vector2(320.5, 191.124)', -1.68),
                ('script = ExtResource("4")', -2.14)]
        R = [a2_m(s, -5.8, y) for s, y in rows]
        a2_at(self, 3.45)
        self.play(LaggedStart(*[FadeIn(r) for r in R[:4]], lag_ratio=0.35), run_time=1.0)
        a2_at(self, 5.0)                                        # "This is a real one, from a Pong game"
        pong = a2_pong_clip(5.0, -1.55, 2.3)
        p_l = a2_c("Pong game", 5.0, -2.65, 34)
        p_s = a2_c("scripted play", 5.0, -3.1, 32, DIM)
        self.play(FadeIn(pong), FadeIn(p_l), FadeIn(p_s), LaggedStart(*[FadeIn(r) for r in R[4:]], lag_ratio=0.3), run_time=0.7)
        # (midpoint: the real file excerpt, the running game, both labelled: a still)
        a2_at(self, 7.2)                                        # "Every object in the game is a few plain lines"
        b1 = Line([3.75, 1.3, 0], [3.75, 0.86, 0], color=DIM, stroke_width=6)
        b2 = Line([3.75, 0.5, 0], [3.75, -0.5, 0], color=DIM, stroke_width=6)
        self.play(Create(b1), Create(b2), run_time=0.5)
        a2_at(self, 9.55)                                       # "its name, its type"
        n_l = a2_l("name, type", 4.0, 1.08, 34)
        self.play(FadeIn(n_l), run_time=0.3)
        a2_at(self, 10.65)                                      # "its settings"
        s_l = a2_l("settings", 4.0, 0.0, 34)
        self.play(FadeIn(s_l), run_time=0.3)
        done(self)


# ── B07 · scripts, settings, scenes: all plain text, as the file command reports ─────────────────────────────────────────
class B07_FileCommand(Scene):
    def construct(self):
        xs = (-5.0, -2.6, -0.2)
        pg = [a2_page(x, 1.85) for x in xs]
        names = ["scripts", "settings", "scenes"]
        labs = [a2_c(n, x, 0.88, 34) for n, x in zip(names, xs)]
        ticks = [check(x, 1.78, s=0.2, color=INK, w=7) for x in xs]
        self.add(pg[0], labs[0])
        a2_at(self, 0.2)                                        # "The scripts are text"
        self.play(Create(ticks[0]), run_time=0.3)
        a2_at(self, 1.1)                                        # "the project's settings are text"
        self.play(FadeIn(pg[1]), FadeIn(labs[1]), run_time=0.3)
        self.play(Create(ticks[1]), run_time=0.25)
        a2_at(self, 2.0)                                        # "text"
        self.play(FadeIn(pg[2]), FadeIn(labs[2]), run_time=0.3)
        self.play(Create(ticks[2]), run_time=0.25)
        a2_at(self, 2.6)                                        # "On this Mac, the file command"
        win = a2_win(-6.1, 6.1, -2.7, 0.3)
        rec = a2_c("recorded on this Mac, 2026-10-09", 0.0, -3.0, 32, DIM)
        self.play(Create(win), FadeIn(rec), run_time=0.4)
        cmd = a2_m("$ file game/main.tscn ui/hud.gd project.godot", -5.8, -0.2)
        self.play(FadeIn(cmd), run_time=0.25)
        out = [a2_m("game/main.tscn: ASCII text", -5.8, -0.8), a2_m("ui/hud.gd:      ASCII text", -5.8, -1.4),
               a2_m("project.godot:  ASCII text", -5.8, -2.0)]
        self.play(LaggedStart(*[FadeIn(o) for o in out], lag_ratio=0.5), run_time=0.7)
        # (midpoint: the three file kinds ticked, the command and its three real lines: a still)
        a2_at(self, 4.95)                                       # "every script and scene file"
        hero = T("13 of 13", 72).move_to([4.1, 2.1, 0])
        c1, c2 = a2_c("script and scene files", 4.1, 1.4, 32), a2_c("read as ASCII text", 4.1, 0.9, 32)
        cks = [check(1.3, y, s=0.18, color=INK, w=7) for y in (-0.8, -1.4, -2.0)]
        self.play(FadeIn(hero), FadeIn(c1), FadeIn(c2), LaggedStart(*[Create(c) for c in cks], lag_ratio=0.3), run_time=0.8)
        done(self)


# ── B08 · no bridge: the agent reads a file, edits a file, and the diff shows what changed ─────────────────────────────
class B08_NoBridge(Scene):
    def construct(self):
        ai_box = RoundedRectangle(width=2.8, height=1.3, corner_radius=0.14, stroke_color=INK, stroke_width=5,
                                  fill_opacity=0).move_to([-4.6, 1.3, 0])
        ai_t = T("A. I.", 44).move_to([-4.6, 1.3, 0])
        page = a2_page(0.6, 1.3, 1.8, 2.4)
        pg_l = a2_c("pong.tscn", 0.6, 2.85, 36)
        self.add(ai_box, ai_t, page, pg_l)
        a2_at(self, 1.0)                                        # "no special bridge"
        br = DashedVMobject(RoundedRectangle(width=1.9, height=1.1, corner_radius=0.1).move_to([-1.75, 1.3, 0]),
                            num_dashes=24).set_stroke(DIM, 5)
        ring = Circle(radius=0.78, stroke_color=INK, stroke_width=7).move_to([-1.75, 1.3, 0])
        bar = Line([-2.30, 1.85, 0], [-1.20, 0.75, 0], color=INK, stroke_width=7)
        b_l = a2_c("bridge", -1.75, 2.55, 36)
        self.play(Create(br), Create(ring), Create(bar), FadeIn(b_l), run_time=0.6)
        a2_at(self, 2.85)                                       # "to read your game": the bridge goes
        self.play(FadeOut(br), FadeOut(ring), FadeOut(bar), FadeOut(b_l), run_time=0.3)
        a2_at(self, 3.2)                                        # "It reads a file"
        rd = Arrow([-0.5, 1.7, 0], [-3.0, 1.7, 0], buff=0, color=INK, stroke_width=7, tip_length=0.28)
        rd_l = a2_c("read", -1.75, 2.3, 40)
        self.play(GrowArrow(rd), FadeIn(rd_l), run_time=0.4)
        a2_at(self, 4.6)                                        # "It edits a file"
        ed = Arrow([-3.0, 0.9, 0], [-0.5, 0.9, 0], buff=0, color=INK, stroke_width=7, tip_length=0.28)
        ed_l = a2_c("edit", -1.75, 0.3, 40)
        self.play(GrowArrow(ed), FadeIn(ed_l), run_time=0.3)
        # (midpoint: the agent and the file with its read and edit arrows: a still)
        a2_at(self, 6.95)                                       # "And your version history"
        dn = Arrow([0.6, 0.05, 0], [0.6, -0.7, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        dn_l = a2_l("version history", 0.95, -0.3, 34)
        win = a2_win(-6.1, 4.5, -3.1, -0.9)
        dif_l = a2_l("diff", 4.8, -2.0, 34)
        self.play(GrowArrow(dn), FadeIn(dn_l), Create(win), FadeIn(dif_l), run_time=0.5)
        rows = [("@@ -95,6 +95,9 @@", -1.3, DIM), (" offset = Vector2(320, 200)", -1.75, DIM),
                ('+[node name="HelloLabel" type="Label"…', -2.2, INK), ('+text = "Hello from a text file"', -2.65, INK)]
        R = [a2_m(s, -5.5, y, 32, c) for s, y, c in rows]
        a2_at(self, 7.5)
        self.play(LaggedStart(*[FadeIn(r) for r in R], lag_ratio=0.3), run_time=1.0)
        a2_at(self, 8.9)                                        # "exactly what changed"
        d1 = Dot([-5.9, -2.2, 0], radius=0.09, color=TERRA)
        d2 = Dot([-5.9, -2.65, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(d1), FadeIn(d2), run_time=0.3)
        done(self)


# ── B09 · the recorded run: one job, four tools, nothing else ──────────────────────────────────────────────────────────
class B09_TheJob(Scene):
    def construct(self):
        hdr = a2_l("recorded run: a Claude Code subagent", -6.1, 2.9, 34)
        self.add(hdr)
        a2_at(self, 1.2)                                        # "A fresh Claude Code agent"
        win = a2_win(-6.1, 3.1, -2.4, 1.9)
        w_l = a2_l("the job, from the real prompt (excerpt)", -6.1, 2.3, 34)
        self.play(Create(win), FadeIn(w_l), run_time=0.45)
        a2_at(self, 2.85)                                       # "a small Pong project"
        pong = a2_pong_clip(4.95, 1.55, 2.3)
        p_l = a2_c("Pong", 4.95, 2.75, 34)
        p_s = a2_c("scripted play", 4.95, 0.45, 32, DIM)
        self.play(FadeIn(pong), FadeIn(p_l), FadeIn(p_s), run_time=0.4)
        rows = [("Task: add a new Label node named", 1.35), ("HelloLabel as a child of the root", 0.7),
                ("node in …/pong.tscn, with its text", 0.05), ('set to "Hello from a text file", by', -0.6),
                ("editing the .tscn text directly.", -1.25)]
        R = [a2_m(s, -5.8, y) for s, y in rows]
        a2_at(self, 4.5)                                        # "one job"
        self.play(FadeIn(R[0]), run_time=0.3)
        a2_at(self, 5.2)
        self.play(FadeIn(R[1]), run_time=0.25)
        a2_at(self, 5.55)
        self.play(FadeIn(R[2]), run_time=0.25)
        # (midpoint: the card with its first three prompt lines and the running Pong: a still)
        a2_at(self, 6.2)
        self.play(FadeIn(R[3]), run_time=0.3)
        a2_at(self, 6.7)
        self.play(FadeIn(R[4]), run_time=0.3)
        a2_at(self, 7.7)                                        # "It could read, edit, write a file, and run Godot"
        names = [("Read", -0.3), ("Edit", -1.1), ("Write", -1.9), ("godot", -2.7)]
        chips = []
        cues = [7.95, 8.5, 8.85, 9.65]
        for (n, y), c in zip(names, cues):
            pill_ = RoundedRectangle(width=2.4, height=0.7, corner_radius=0.35, stroke_color=INK, stroke_width=4,
                                     fill_opacity=0).move_to([4.95, y, 0])
            txt = a2_m(n, 4.95 - len(n) * 0.249 / 2, y)
            dot = Dot([3.9, y, 0], radius=0.09, color=TERRA)
            chips.append((pill_, txt, dot))
        for (pill_, txt, dot), c in zip(chips, cues):
            a2_at(self, c)
            self.play(Create(pill_), FadeIn(txt), FadeIn(dot), run_time=0.25)
        done(self)


# ── B10 · the four real tool calls on a time axis: 23.4 seconds from request to report ───────────────────────────────────
class B10_Timeline(Scene):
    def construct(self):
        hdr = a2_l("recorded run", -6.1, 2.9, 34)
        K = 10.8 / 23.4
        X = lambda s: -5.4 + s * K
        axis = Line([-5.4, -0.4, 0], [5.4, -0.4, 0], color=DIM, stroke_width=5)
        cap = a2_c("seconds since the request, to scale", 0.0, -2.75, 34, DIM)
        d0 = Dot([X(0), -0.4, 0], radius=0.12, color=INK)
        r_l = a2_c("request", -5.0, -0.95, 34)
        self.add(hdr, axis, d0, r_l, cap)
        tool = Dot([X(0), -0.4, 0], radius=0.14, color=TERRA)
        self.add(tool)
        ev = [("Read", 1.7, 0.15, "the scene", 0.75), ("Edit", 4.4, -0.95, "+3 lines", -1.55),
              ("Write", 7.1, 0.15, "check script", 0.75), ("godot", 10.5, -0.95, "no window", -1.55)]
        cues = [0.12, 0.95, 2.3, 3.75]
        for (n, s, y, sub, sy), c in zip(ev, cues):
            a2_at(self, c)
            x = X(s)
            dt = Dot([x, -0.4, 0], radius=0.12, color=INK)
            nm = a2_m(n, x - len(n) * 0.249 / 2, y)
            sb = a2_c(sub, x, sy, 34, DIM)
            self.play(tool.animate.move_to([x, -0.4, 0]), FadeIn(dt), FadeIn(nm), FadeIn(sb), run_time=0.35)
        # (midpoint: four ticks placed, the clock dot at the godot call: a still)
        a2_at(self, 5.9)                                        # "Twenty-three seconds"
        x_end = X(23.4)
        end_d = Dot([x_end, -0.4, 0], radius=0.12, color=INK)
        e_l = a2_c("report", x_end - 0.2, 0.15, 34)
        hero = T("23.4 s", 80).move_to([3.4, 1.9, 0])
        self.play(tool.animate.move_to([x_end, -0.4, 0]), FadeIn(end_d), FadeIn(e_l), FadeIn(hero), run_time=0.9)
        done(self)


# ── B11 · two checks: the agent's own (little), and one written outside the project ────────────────────────────────────
class B11_TwoChecks(Scene):
    def construct(self):
        a_l = a2_l("its own check: the agent wrote it", -6.1, 2.65, 34)
        winA = a2_win(-6.1, 4.3, 1.0, 2.25)
        a1 = a2_m("HelloLabel text: Hello from a text file", -5.8, 1.85)
        a2 = a2_m("PASS", -5.8, 1.35)
        self.add(a_l, winA, a1, a2)
        a2_at(self, 0.75)                                       # "printed pass"
        ckA = check(5.2, 1.7, s=0.2, color=DIM, w=7)
        self.play(Create(ckA), run_time=0.3)
        a2_at(self, 3.7)                                        # "So a second check"
        b_l = a2_l("a second check, written outside the project", -6.1, 0.55, 34)
        winB = a2_win(-6.1, 4.3, -2.95, 0.15)
        self.play(FadeIn(b_l), Create(winB), run_time=0.4)
        rows = [("Original nodes present: 21/21", -0.25), ("Label found: path=HelloLabel…", -0.85),
                ("script on Left: res://logic/paddle.gd", -1.45), ("INDEPENDENT RESULT: PASS", -2.05)]
        R = [a2_m(s, -5.4, y) for s, y in rows]
        a2_at(self, 4.7)
        self.play(LaggedStart(*[FadeIn(r) for r in R], lag_ratio=0.3), run_time=1.0)
        # (midpoint: the agent's own PASS above, the second check's four real lines below: a still)
        a2_at(self, 6.7)                                        # "All twenty-one original nodes still there"
        dot = Dot([-5.75, -0.25, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(dot), run_time=0.2)
        a2_at(self, 8.8)                                        # "Scripts still attached"
        self.play(dot.animate.move_to([-5.75, -1.45, 0]), run_time=0.3)
        a2_at(self, 10.25)                                      # "exactly one new label"
        self.play(dot.animate.move_to([-5.75, -0.85, 0]), run_time=0.3)
        a2_at(self, 11.2)
        ckB = check(5.2, -2.05, s=0.2, color=INK, w=7)
        self.play(Create(ckB), run_time=0.3)
        done(self)


# ── B12 · the control: the same check on the scene before the edit fails ───────────────────────────────────────────────
class B12_Control(Scene):
    def construct(self):
        a_l = a2_l("the same check, on the edited scene", -6.1, 2.65, 34)
        winA = a2_win(-6.1, 3.6, 1.0, 2.25)
        a1 = a2_m("INDEPENDENT RESULT: PASS", -5.8, 1.85)
        a2 = a2_m("exit=0", -5.8, 1.35)
        ckA = check(5.0, 1.65, s=0.2, color=INK, w=7)
        self.add(a_l, winA, a1, a2, ckA)
        a2_at(self, 0.15)                                       # "a control"
        b_l = a2_l("the same check, on the scene before the edit", -6.1, 0.4, 34)
        winB = a2_win(-6.1, 3.6, -2.35, 0.0)
        self.play(FadeIn(b_l), Create(winB), run_time=0.4)
        rows = [("Original nodes present: 21/21", -0.4), ("Expected exactly 1 Label, found 0", -0.95),
                ("INDEPENDENT RESULT: FAIL (1)", -1.5), ("exit=1", -2.0)]
        R = [a2_m(s, -5.8, y) for s, y in rows]
        a2_at(self, 1.4)
        self.play(LaggedStart(*[FadeIn(r) for r in R[:2]], lag_ratio=0.4), run_time=0.7)
        a2_at(self, 2.55)                                       # "fails"
        self.play(FadeIn(R[2]), FadeIn(R[3]), run_time=0.25)
        # (midpoint: the PASS above, the control's lines and its FAIL below: a still)
        cx = a2_x(5.0, -1.15, s=0.3)
        a2_at(self, 3.4)
        self.play(Create(cx), run_time=0.3)
        a2_at(self, 4.0)                                        # "A check that cannot fail proves nothing"
        cap = T("a check that cannot fail proves nothing", 40).move_to([0.0, -2.9, 0])
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ── B13 · the one difference: the unique_id the agent left out, and Godot's own save adds ──────────────────────────────
class B13_UniqueId(Scene):
    def construct(self):
        hdr = a2_l("the end of a node's first line, from the real scene files", -6.1, 2.85, 34)
        X0 = -2.3
        o_l = a2_l("another node", -6.1, 1.6, 34)
        o_t = a2_m('…parent="." unique_id=957432765]', X0, 1.6)
        self.add(hdr, o_l, o_t)
        a2_at(self, 0.8)                                        # "the agent left out an identifier"
        g_l = a2_l("the agent's node", -6.1, 0.2, 34)
        g_t = a2_m('…parent="."]', X0, 0.2)
        miss = DashedVMobject(RoundedRectangle(width=4.5, height=0.7, corner_radius=0.08).move_to([3.45, 0.2, 0]),
                              num_dashes=34).set_stroke(DIM, 5)
        m_l = a2_c("missing", 3.45, 0.2, 34, DIM)
        self.play(FadeIn(g_l), FadeIn(g_t), run_time=0.4)
        self.play(Create(miss), FadeIn(m_l), run_time=0.5)
        a2_at(self, 4.8)                                        # "Godot loaded the file anyway"
        ok_l = a2_l("Godot loads it: no warning", X0, -0.55, 34)
        self.play(FadeIn(ok_l), run_time=0.4)
        # (midpoint: another node with its id, the agent's node with the id missing, the loads-it note: a still)
        a2_at(self, 7.0)                                        # "When Godot saved the scene itself"
        s_l = a2_l("re-saved by Godot", -6.1, -1.4, 34)
        s_t = a2_m('…parent="." unique_id=1828201969]', X0, -1.4)
        self.play(FadeIn(s_l), FadeIn(s_t), run_time=0.5)
        s_n = a2_l("a Godot script saved a copy", X0, -2.0, 34, DIM)
        self.play(FadeIn(s_n), run_time=0.3)
        a2_at(self, 8.7)                                        # "it added one"
        d = Dot([3.9, -0.98, 0], radius=0.1, color=TERRA)
        self.play(FadeOut(miss), FadeOut(m_l), FadeIn(d), run_time=0.4)
        a2_at(self, 9.8)                                        # "So the text was valid, but not what the editor would have written"
        cap = T("valid text, not what Godot saves", 40).move_to([0.0, -2.85, 0])
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ── B14 · the limits of one run, four rows ────────────────────────────────────────────────────────────────────────────
class B14_Limits(Scene):
    def construct(self):
        hdr = T("The limits", 40).move_to([-6.1, 2.95, 0], aligned_edge=LEFT)
        self.add(hdr)
        ys = [1.7, 0.45, -0.8, -2.05]

        def ring(y):
            return DashedVMobject(Circle(radius=0.2).move_to([-5.85, y, 0]), num_dashes=10).set_stroke(DIM, 6)

        a2_at(self, 0.7)                                        # "One run"
        r1, t1 = ring(ys[0]), a2_l("one run", -5.3, ys[0], 38)
        self.play(Create(r1), FadeIn(t1), run_time=0.35)
        a2_at(self, 1.35)                                       # "A tiny change"
        r2, t2 = ring(ys[1]), a2_l("a tiny change", -5.3, ys[1], 38)
        self.play(Create(r2), FadeIn(t2), run_time=0.35)
        a2_at(self, 2.3)                                        # "one node, no resources, no signals"
        s2 = a2_l("one node, no resources, no signals", -5.3, ys[1] - 0.55, 34, DIM)
        self.play(FadeIn(s2), run_time=0.4)
        a2_at(self, 4.7)                                        # "Nothing was drawn on screen"
        r3, t3 = ring(ys[2]), a2_l("nothing drawn on screen", -5.3, ys[2], 38)
        self.play(Create(r3), FadeIn(t3), run_time=0.35)
        a2_at(self, 5.9)                                        # "so this does not show it looks right"
        s3 = a2_l("so it does not show that it looks right", -5.3, ys[2] - 0.55, 34, DIM)
        self.play(FadeIn(s3), run_time=0.3)
        # (midpoint: three limits so far, each with its open ring: a still)
        a2_at(self, 8.3)                                        # "the agent's tool limits were written in its prompt"
        r4, t4 = ring(ys[3]), a2_l("tool limits only in the prompt", -5.3, ys[3], 38)
        self.play(Create(r4), FadeIn(t4), run_time=0.35)
        a2_at(self, 10.5)                                       # "not enforced"
        s4 = a2_m("Not logged in · Please run /login", -5.3, ys[3] - 0.6, 32, DIM)
        self.play(FadeIn(s4), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · A Complete Command Line  (B15-B18, all Manim)

HONESTY RULE for the act: every option name, command and output line on screen is verbatim from the real runs of 2026-10-09 on one Mac
(Godot 4.7.2.stable.official.ed1daf0bf): _conducting-series-evidence/godot-evidence/part1/godot-help-full.txt (the option names),
part1/walker-claude-copy-import-quit.txt (B16, B18), part2/independent-checks.txt section 4 (B17). Scratch paths are shown as <copy> /
<project> (the real paths are private scratch folders); line-broken or trimmed text carries a visible label. The game frames in B17 are
frames of a SEPARATE windowed recording (Movie Maker, scripted input), not of the headless run, and are labelled so: a headless run draws
no window. The 60 tick marks in B17 are an idea drawing of the sixty iterations the command asked for.
Menlo 32 is 0.25 scene units per character (measured 0.2497), so rows are placed by column from an explicit left edge.
"""

A3_CW = 0.25                  # Menlo 32: width of one character in scene units
A3P = "pantry/"

# the long option names of `godot --headless --help` (4.7.2), in the help's own order (the "--, ++" separator row omitted)
A3_FLAGS = ["--help", "--version", "--verbose", "--quiet", "--no-header", "--editor", "--project-manager", "--recovery-mode",
            "--debug-server", "--dap-port", "--lsp-port", "--quit", "--quit-after", "--language", "--path", "--scene", "--main-pack",
            "--render-thread", "--remote-fs", "--remote-fs-password", "--audio-driver", "--display-driver", "--audio-output-latency",
            "--rendering-method", "--rendering-driver", "--gpu-index", "--text-driver", "--tablet-driver", "--headless", "--log-file",
            "--write-movie", "--fullscreen", "--maximized", "--windowed", "--always-on-top", "--resolution", "--position", "--screen",
            "--single-window", "--xr-mode", "--wid", "--accessibility", "--accessibility-driver", "--debug", "--breakpoints",
            "--ignore-error-breaks", "--profiling", "--gpu-profile", "--gpu-validation", "--gpu-abort", "--generate-spirv-debug-info",
            "--extra-gpu-memory-tracking", "--accurate-breadcrumbs", "--remote-debug", "--single-threaded-scene", "--debug-collisions",
            "--debug-paths", "--debug-navigation", "--debug-avoidance", "--debug-stringnames", "--debug-canvas-item-redraw",
            "--max-fps", "--frame-delay", "--time-scale", "--disable-vsync", "--disable-render-loop", "--disable-crash-handler",
            "--fixed-fps", "--delta-smoothing", "--print-fps", "--editor-pseudolocalization", "--script", "--main-loop", "--check-only",
            "--import", "--export-release", "--export-debug", "--export-pack", "--export-patch", "--patches",
            "--install-android-build-template", "--convert-3to4", "--validate-conversion-3to4", "--doctool", "--no-docbase",
            "--gdextension-docs", "--gdscript-docs", "--build-solutions", "--dump-gdextension-interface",
            "--dump-gdextension-interface-json", "--dump-extension-api", "--dump-extension-api-with-docs", "--validate-extension-api",
            "--benchmark", "--benchmark-file"]


def a3_m(s, size=32, color=INK):
    """Menlo text with ligatures off, so '--' stays two hyphens (the real text), not one long dash."""
    return Text(s, font=MONO, color=color, font_size=size, disable_ligatures=True)


def a3_row(s, x_left, y, size=32, color=INK):
    """One Menlo row whose first character starts at x_left (explicit coordinates; no get_left()). No leading spaces."""
    cw = A3_CW * size / 32.0
    return a3_m(s, size, color).move_to([x_left + len(s) * cw / 2.0, y, 0])


def a3_tok(s, x_left, col, y, size=32, color=INK):
    """One Menlo token at a column of a row (used where a double space must survive)."""
    cw = A3_CW * size / 32.0
    return a3_m(s, size, color).move_to([x_left + (col + len(s) / 2.0) * cw, y, 0])


def a3_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    return t.move_to([x, y, 0], aligned_edge=LEFT) if left else t.move_to([x, y, 0])


def a3_window(cx, cy, w=1.5, h=1.05, color=DIM):
    """A plain app window drawn as an outline: frame + title bar line (Polygon/Line, not Rectangle)."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    frame = Polygon([x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0], color=color, stroke_width=6)
    bar = Line([x0, y1 - 0.28, 0], [x1, y1 - 0.28, 0], color=color, stroke_width=5)
    dots = VGroup(*[Dot([x0 + 0.17 + 0.17 * i, y1 - 0.14, 0], radius=0.045, color=color) for i in range(3)])
    return VGroup(frame, bar, dots)


def a3_no(x, y, r=0.95, sw=7):
    """A prohibition mark (ring + bar) in INK, drawn around an object (never touching text)."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a3_plus(x, y, s=0.22, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x + s, y, 0], color=color, stroke_width=w),
                  Line([x, y - s, 0], [x, y + s, 0], color=color, stroke_width=w))


# ── B15 · the second property: a complete command line (ACT TITLE) ──────────────────────────────────────────────────
class B15_CompleteCommandLine(Scene):
    def construct(self):
        title = T("A  Complete  Command  Line", 40).move_to([-2.7, 3.0, 0])
        cmd_a = a3_tok("godot", -3.6, 0, 1.6, 36)
        self.play(FadeIn(title), FadeIn(cmd_a), run_time=0.5)
        until(self, "You can run it with no window", lead=0.15)
        win = a3_window(-5.0, 1.6, 1.3, 0.9)
        no = a3_no(-5.0, 1.6, 0.98)
        cmd_b = a3_tok("--headless", -3.6, 6, 1.6, 36)
        self.play(Create(win), run_time=0.4)
        self.play(Create(no), FadeIn(cmd_b), run_time=0.4)
        wl = a3_lab("no window", 3.6, 1.6, 34)
        self.play(FadeIn(wl), run_time=0.25)
        rows = [("import a project", "--import", 0.15, "tell it to import a project"),
                ("run a script", "--script", -0.7, "run a script"),
                ("check a script for errors", "--check-only", -1.55, "check a script for errors"),
                ("export a build", "--export-release", -2.4, "or export a build")]
        for lab, opt, y, ph in rows:
            until(self, ph, lead=0.2)
            l = a3_lab(lab, -5.5, y, 34, left=True)
            d = Dot([-0.9, y, 0], radius=0.09, color=TERRA)
            o = a3_row(opt, -0.55, y)
            self.play(FadeIn(l), GrowFromCenter(d), FadeIn(o), run_time=0.4)
        cap = a3_lab("option names from the help text, version 4.7.2", 0.0, -3.05, 32, DIM)
        self.play(FadeIn(cap), run_time=0.3)
        done(self)


# ── B16 · the help's options scroll past; then a real import and a real run-and-quit, timed ───────────────────────────
class B16_ImportAndQuit(Scene):
    def construct(self):
        hc = a3_row("godot --headless --help", -6.0, 3.0)
        flags = VGroup(*[a3_row(f, -2.2, 0.0) for f in A3_FLAGS])
        off = ValueTracker(0.0)

        def place(g):
            o = off.get_value()
            for i, m in enumerate(g):
                m.move_to(np.array([-2.2 + (len(A3_FLAGS[i]) * A3_CW / 2.0), o - 2.4 - 0.5 * i, 0.0]))
                y = m.get_center()[1]
                m.set_opacity(0.0 if (y > 2.45 or y < -2.65) else 1.0)
        flags.add_updater(place)
        place(flags)
        self.add(flags)
        self.play(FadeIn(hc), run_time=0.3)
        self.play(off.animate.set_value(48.4), run_time=1.7, rate_func=linear)
        flags.remove_updater(place)
        self.play(FadeOut(flags), FadeOut(hc), run_time=0.3)
        until(self, "Here is a real project", lead=0.1)
        X0 = -6.0
        c1 = a3_row("$ godot --headless --path <copy> --import", X0, 2.9)
        p1 = a3_row("[ DONE ] loading_editor_layout", X0, 2.3)
        self.play(FadeIn(c1), run_time=0.3)
        self.play(FadeIn(p1), run_time=0.25)
        until(self, "exit code zero, in three", lead=0.25)
        e1 = VGroup(a3_tok("exit=0", X0, 0, 1.7), a3_tok("wall=3.03s", X0, 8, 1.7))
        k1 = check(-1.2, 1.7, 0.22)
        bar1 = Line([X0, 1.1, 0], [X0 + 3.03 * 1.4, 1.1, 0], color=BAR1, stroke_width=14)
        self.play(FadeIn(e1), Create(k1), run_time=0.35)
        self.play(Create(bar1), run_time=0.6, rate_func=linear)
        self.play(GrowFromCenter(Dot([X0 + 3.03 * 1.4 + 0.3, 1.1, 0], radius=0.11, color=TERRA)), run_time=0.2)
        until(self, "Then run and quit", lead=0.2)
        c2 = a3_row("$ godot --headless --path <copy> --quit", X0, 0.3)
        self.play(FadeIn(c2), run_time=0.3)
        until(self, "exit code zero, in a quarter", lead=0.25)
        e2 = VGroup(a3_tok("exit=0", X0, 0, -0.3), a3_tok("wall=0.25s", X0, 8, -0.3))
        k2 = check(-1.2, -0.3, 0.22)
        bar2 = Line([X0, -0.9, 0], [X0 + 0.25 * 1.4, -0.9, 0], color=BAR1, stroke_width=14)
        self.play(FadeIn(e2), Create(k2), run_time=0.3)
        self.play(Create(bar2), run_time=0.2, rate_func=linear)
        self.play(GrowFromCenter(Dot([X0 + 0.25 * 1.4 + 0.3, -0.9, 0], radius=0.11, color=TERRA)), run_time=0.2)
        cap = a3_lab("recorded run, on a copy of a real project (27 files)", 0.0, -2.2, 34)
        cap2 = a3_lab("bars drawn to scale: 3.03 s and 0.25 s", 0.0, -2.85, 32, DIM)
        self.play(FadeIn(cap), FadeIn(cap2), run_time=0.3)
        done(self)


# ── B17 · sixty frames with no window: exit code and output; the same game in a window, recorded separately ────────────
class B17_SixtyFrames(Scene):
    def construct(self):
        X0 = -6.0
        c1 = a3_row("$ godot --headless --path <project> \\", X0, 2.9)
        c2 = a3_row("--quit-after 60", X0 + 1.0, 2.35)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        until(self, "for sixty frames", lead=0.2)
        n0 = 60
        x0, x1 = -6.0, -0.4
        ticks = VGroup(*[Line([x0 + (x1 - x0) * i / (n0 - 1), -0.55, 0], [x0 + (x1 - x0) * i / (n0 - 1), -0.15, 0], color=DIM,
                              stroke_width=4) for i in range(n0)])
        tl = a3_lab("60 frames", -3.2, -1.15, 34)
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.02), run_time=1.2, rate_func=linear)
        self.play(FadeIn(tl), run_time=0.25)
        until(self, "without a window", lead=0.2)
        o1 = a3_row("Godot Engine v4.7.2.stable.official.ed1daf0bf", X0, 1.5)
        e1 = VGroup(a3_tok("exit=0", X0, 0, 0.95), a3_tok("wall=0.56s", X0, 8, 0.95))
        k1 = check(-1.2, 0.95, 0.22)
        self.play(FadeIn(o1), run_time=0.3)
        self.play(FadeIn(e1), Create(k1), run_time=0.3)
        cap = a3_lab("recorded run, line broken", -3.2, -2.35, 32, DIM)
        self.play(FadeIn(cap), run_time=0.25)
        until(self, "tell you whether it ran", lead=0.1)
        imgs = [ImageMobject(f"{A3P}a3_pong_{i}.png").set_width(5.4).move_to([3.1, -1.75, 0]) for i in range(1, 6)]
        fl = a3_lab("the same game, in a window", 3.1, 0.2, 34)
        self.add(imgs[0])
        self.play(FadeIn(fl), run_time=0.25)
        for i in range(1, 5):
            self.wait(0.38)
            self.remove(imgs[i - 1])
            self.add(imgs[i])
        until(self, "You can run the same command", lead=0.2)
        d = Dot([-0.85, 2.35, 0], radius=0.1, color=TERRA)
        yl = a3_lab("run it yourself", 1.2, 2.35, 36)
        self.play(GrowFromCenter(d), FadeIn(yl), run_time=0.35)
        done(self)


# ── B18 · the import quietly created one file: the folder before and after, then the two commands that show it ─────────
class B18_QuietNewFile(Scene):
    def construct(self):
        XL, XR = -6.0, 0.5
        hl = a3_lab("before the import", XL + 2.3, 3.0, 34)
        hr = a3_lab("after the import", XR + 2.3, 3.0, 34)
        arr = Arrow([-1.9, 3.0, 0], [0.0, 3.0, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.4)
        Y = [2.3 - 0.52 * i for i in range(7)]
        names_b = ["route_driver.gd.uid", "test_clawd.gd", "test_game.gd", "test_game.gd.uid"]
        lb = [a3_row("tests/ (excerpt)", XL, Y[0])] + [a3_row(n, XL + 0.5, Y[1 + i]) for i, n in enumerate(names_b)]
        lb.append(a3_row("...", XL + 0.5, Y[5]))
        self.play(FadeIn(hl), *[FadeIn(r) for r in lb], run_time=0.5)
        until(self, "That import quietly created one new file", lead=0.25)
        la = [a3_row("tests/ (excerpt)", XR, Y[0]), a3_row("route_driver.gd.uid", XR + 0.5, Y[1]), a3_row("test_clawd.gd", XR + 0.5, Y[2])]
        self.play(FadeIn(hr), Create(arr), *[FadeIn(r) for r in la], run_time=0.45)
        newr = a3_row("test_clawd.gd.uid", XR + 0.5, Y[3])
        pl = a3_plus(XR + 0.22, Y[3], 0.14, INK, 6)
        dot = Dot([XR - 0.25, Y[3], 0], radius=0.11, color=TERRA)
        self.play(FadeIn(newr), Create(pl), GrowFromCenter(dot), run_time=0.45)
        rest = [a3_row("test_game.gd", XR + 0.5, Y[4]), a3_row("test_game.gd.uid", XR + 0.5, Y[5]), a3_row("...", XR + 0.5, Y[6])]
        self.play(*[FadeIn(r) for r in rest], run_time=0.3)
        until(self, "a missing sidecar", lead=0.25)
        uid = a3_row("inside it, this run: uid://ci27qal208t75", XL, -1.45)
        self.play(FadeIn(uid), run_time=0.4)
        until(self, "Even a command that sounds read-only", lead=0.2)
        self.play(Indicate(VGroup(newr, dot), color=INK, scale_factor=1.04), run_time=0.5)
        until(self, "Check the diff", lead=0.35)
        g1 = a3_row("git diff", XL + 0.5, -2.3)
        g2 = a3_row("git status", XL + 0.5, -2.9)
        gl = a3_lab("check what changed", -2.1, -2.6, 34, left=True)
        gd = Dot([XL + 0.15, -2.6, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(gl), GrowFromCenter(gd), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · The Other Two Engines  (B19–B24, all Manim)

HONESTY RULE for the act (LANE-PLAN.md): Godot has NO official MCP; Unity (public 2026-03-03, open beta) and Unreal 5.8 (Experimental) DO. Nothing here
draws Godot "ahead on MCP" or Unity / Unreal as "raw": their own labels are shown. Unity scenes are text by default; only Unreal's are binary.
Everything on screen is real or labelled:
  * REAL captures (pantry/a4_*.png, cropped from EVID/web-captures by evidence/act4/make_crops_act4.py, never altered): Unity's docs page and
    changelog, the two GitHub repo headers, the Godot Foundation's policy post, and 15 real gameplay frames of the walker-claude capture.
  * unity.com blog and Epic docs returned HTTP 403 to the capture: they are shown ONLY as short quotes (<= 15 words), attributed, labelled
    "quoted, not captured". The capture PNGs of those pages are error pages and are NOT used.
  * The YAML lines are verbatim from Unity's own Manual page (docs.unity3d.com/Manual/FormatDescription.html), trimmed.
  * Star counts: GitHub API 2026-10-09 (Coding-Solo/godot-mcp 5,987; CoplayDev/unity-mcp 14,793); the pages' own buttons read 6k and 14.8k.
One cast for the act (ACTS.md): an engine = a kraft box with its name; an official MCP server = the kit's dark MCP block on top of it; "none" = the
empty outlined slot where it would sit. Pacing lands on real spoken times (evidence/act4/word_times.py, faster-whisper).
"""

A4P = "pantry/"
A4_CABLE = "#9C8462"
A4_PX = {"a4_unity_docs.png": (1680, 540), "a4_unity_changelog.png": (1680, 378), "a4_godot_mcp_banner.png": (1035, 138),
         "a4_unity_mcp_banner.png": (855, 138), "a4_policy_title.png": (2040, 264)}


def a4_at(self, t, lead=0.0):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus an optional lead)."""
    gap = t - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


A4_W = {
    ('14.8k', 40, False): 1.115,
    ('30 Jun 2026, same page', 32, False): 3.94,
    ('6.0k', 40, False): 0.89,
    ('Epic, Unreal MCP docs', 32, False): 4.063,
    ('Experimental', 36, False): 2.492,
    ('GitHub stars, 9 Oct 2026', 32, False): 4.383,
    ('Godot', 40, False): 1.445,
    ('Godot Foundation', 32, False): 3.104,
    ('June 2026', 32, False): 1.734,
    ('No.', 48, True): 0.98,
    ('The Other Two Engines', 40, False): 4.997,
    ('Unity', 40, False): 1.233,
    ('Unity', 48, False): 1.479,
    ('Unity Manual, trimmed', 32, False): 4.213,
    ('Unity blog, 11 May 2026', 32, False): 4.192,
    ('Unreal Engine 5.8', 44, False): 4.104,
    ('YAML', 40, False): 1.519,
    ('a different thing', 40, False): 3.324,
    ('be human authored.”', 34, False): 3.921,
    ('beta', 34, False): 0.78,
    ('better MCP story?', 40, False): 3.864,
    ('binary', 40, False): 1.387,
    ('command line', 34, False): 2.556,
    ('community server', 32, False): 3.031,
    ('contributing TO Godot', 38, False): 4.893,
    ('cross-references', 36, False): 2.878,
    ('experimental', 34, False): 2.34,
    ('has it', 32, False): 0.928,
    ('incomplete or', 36, False): 2.603,
    ('lacks it', 32, False): 1.178,
    ('last push 16 Apr 2026', 32, False): 3.795,
    ('last push 8 Oct 2026', 32, False): 3.595,
    ('licence', 34, False): 1.213,
    ('making a game WITH Godot', 38, False): 5.999,
    ('missing.”', 36, False): 1.628,
    ('no', 34, False): 0.456,
    ('no official MCP', 32, False): 2.723,
    ('none', 34, False): 0.911,
    ('official MCP', 34, False): 2.332,
    ('open beta', 44, False): 2.222,
    ('or be discontinued', 36, False): 3.434,
    ("per Epic's UE 4.26 docs", 32, False): 4.021,
    ('public, March 2026', 34, False): 3.607,
    ('quoted, not captured', 32, False): 3.608,
    ('read as text', 36, False): 2.038,
    ('recorded 2026-10-09', 32, False): 3.243,
    ('scenes as text', 34, False): 2.381,
    ('scripted input,', 32, False): 2.468,
    ('text by default', 40, False): 2.9,
    ('use or vibe coding”', 34, False): 3.465,
    ('without notice”', 36, False): 2.937,
    ('yes', 34, False): 0.535,
    ('yes, YAML', 34, False): 2.069,
    ('“Many features are', 36, False): 3.462,
    ('“No autonomous AI agent', 34, False): 4.925,
    ('“We require all code to', 34, False): 4.148,
    ('“may change, be limited,', 36, False): 4.521,
}  # measured


def a4_w(s, size, bold=False):
    """Width of an EB Garamond string: the measured value when known, else about 0.0058 x size per character."""
    if _os.environ.get("A4_REC"):
        with open(_os.environ["A4_REC"], "a") as _f:
            _f.write(_json.dumps([s, size, bool(bold)]) + "\n")
    return A4_W.get((s, size, bool(bold)), len(s) * size * 0.0058)


def a4_tl(s, x, y, size=34, color=INK, bold=False):
    """Text whose LEFT edge sits at x."""
    return T(s, size, color, bold).move_to([x + a4_w(s, size, bold) / 2.0, y, 0])


def a4_nx(s, x, size, gap=0.3):
    """x just right of the string s whose left edge is at x."""
    return x + a4_w(s, size) + gap


def a4_tc(s, x, y, size=34, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def a4_ml(s, x, y, size=32):
    """Menlo text whose left edge sits at x (0.2459 units per character at size 32)."""
    return M(s, size).move_to([x + len(s) * 0.2459 * size / 32.0 / 2.0, y, 0])


def a4_img(name, cx, cy, w):
    """A real capture crop with a ghost offset shadow behind it. Returns (shadow, image, height)."""
    pw, ph = A4_PX[name]
    h = w * ph / pw
    shadow = Rectangle(width=w, height=h, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([cx + 0.07, cy - 0.07, 0])
    im = ImageMobject(A4P + name).set_width(w).move_to([cx, cy, 0])
    return shadow, im, h


def a4_page(cx, cy, w=1.0, h=1.3, lines=3):
    """A page icon: card body with a folded corner and ghost text lines (grey outline, no ink)."""
    f = 0.28
    pts = [[cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2 - f, 0], [cx + w / 2 - f, cy + h / 2, 0],
           [cx - w / 2, cy + h / 2, 0]]
    body = Polygon(*pts, fill_color=CARD, fill_opacity=1, stroke_color=DIM, stroke_width=4)
    fold = Polygon([cx + w / 2 - f, cy + h / 2, 0], [cx + w / 2 - f, cy + h / 2 - f, 0], [cx + w / 2, cy + h / 2 - f, 0],
                   fill_color=GHOST, fill_opacity=1, stroke_color=DIM, stroke_width=3)
    ls = [Line([cx - w / 2 + 0.18, cy + h / 2 - 0.5 - i * 0.24, 0], [cx + w / 2 - 0.18, cy + h / 2 - 0.5 - i * 0.24, 0], color=GHOST, stroke_width=4)
          for i in range(lines)]
    return VGroup(body, fold, *ls)


def a4_binfile(cx, cy, w=1.0, h=1.3):
    """A binary file: the page with a grid of small grey squares where text would be (an idea drawing: bytes, not real data)."""
    pg = a4_page(cx, cy, w, h, lines=0)
    shades = [BAR1, BAR3, BAR2, GHOST]
    sq = []
    for i in range(5):
        for j in range(4):
            c = shades[(i * 7 + j * 3 + i * j) % 4]
            sq.append(Rectangle(width=0.15, height=0.15, fill_color=c, fill_opacity=1, stroke_width=0).move_to(
                [cx - 0.3 + j * 0.2, cy + 0.12 - i * 0.2, 0]))
    return VGroup(pg, *sq)


def a4_no(x, y, r=0.3, sw=7):
    """A prohibition mark (ink ring + bar), standing alone."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a4_iso(cx, cy, s, W, D, H=0.0):
    """An Iso whose projected footprint W x D x H is centred on the scene point (cx, cy)."""
    ox = cx - (W - D) * C30 * s / 2
    oy = cy - ((W + D) / 2 + H) * s / 2
    return Iso(ox, oy, s)


def a4_engine(cx, cy, s=0.85, official=True):
    """An engine: kraft box + (the kit's dark MCP block on top | the empty outlined slot where it would sit)."""
    W = D = 1.5
    H = 0.8
    iso = a4_iso(cx, cy, s, W, D, H)
    d = {"iso": iso, "box": iso.box(0, 0, 0, W, D, H)}
    if official:
        d["mcp"] = iso.mcp(0.45, 0.45, H, 0.6, 0.6, 0.4)
    else:
        d["slot"] = Polygon(*[iso.p(x, y, H) for x, y in [(0.45, 0.45), (1.05, 0.45), (1.05, 1.05), (0.45, 1.05)]],
                            stroke_color=DIM, stroke_width=5, fill_opacity=0)
    d["top"] = iso.p(0.75, 0.75, H + 0.4)        # where a call starts (the block's top)
    d["face"] = iso.p(0.0, 0.75, H * 0.5)         # where it lands (the box's left face)
    return d


# ───────────────────────── B19 · three engines: official MCP | official MCP | none ─────────────────────────
class B19_ThreeEngines(Scene):
    """Act title first. Unity and Unreal each get a kraft box, then an official MCP block drops onto it; a terracotta call goes from the block into
    the editor; then Godot's box arrives with an EMPTY slot where the block would sit."""
    def construct(self):
        title = a4_tl("The Other Two Engines", -6.1, 3.05, 40)
        self.play(FadeIn(title), run_time=0.4)
        cols = {"Unity": -4.3, "Unreal Engine": 0.0, "Godot": 4.3}
        cy = -0.35
        a4_at(self, 1.55)                                          # "Unity"
        u = a4_engine(cols["Unity"], cy, 1.1)
        un = a4_tc("Unity", cols["Unity"], 2.15, 44)
        self.play(FadeIn(un), FadeIn(u["box"], shift=UP * 0.2), run_time=0.45)
        a4_at(self, 2.05)                                          # "Unreal"
        r = a4_engine(cols["Unreal Engine"], cy, 1.1)
        rn = a4_tc("Unreal Engine", cols["Unreal Engine"], 2.15, 44)
        self.play(FadeIn(rn), FadeIn(r["box"], shift=UP * 0.2), run_time=0.45)
        a4_at(self, 3.9)                                           # "official" ... "MCP"
        u["mcp"].shift(UP * 1.3)
        r["mcp"].shift(UP * 1.3)
        self.add(u["mcp"], r["mcp"])
        self.play(u["mcp"].animate.shift(DOWN * 1.3), r["mcp"].animate.shift(DOWN * 1.3), run_time=0.5)
        lu = a4_tc("official MCP", cols["Unity"], -2.2, 36)
        lr = a4_tc("official MCP", cols["Unreal Engine"], -2.2, 36)
        self.play(FadeIn(lu), FadeIn(lr), run_time=0.35)
        a4_at(self, 7.1)                                           # "that lets an AI call the editor's tools directly"
        du = Dot(u["top"], radius=0.12, color=TERRA)
        dr = Dot(r["top"], radius=0.12, color=TERRA)
        self.play(GrowFromCenter(du), GrowFromCenter(dr), run_time=0.25)
        self.play(du.animate.move_to(u["face"]), dr.animate.move_to(r["face"]), run_time=0.8)
        a4_at(self, 9.55)                                          # "Godot has none"
        g = a4_engine(cols["Godot"], cy, 1.1, official=False)
        gn = a4_tc("Godot", cols["Godot"], 2.15, 44)
        self.play(FadeIn(gn), FadeIn(g["box"], shift=UP * 0.2), run_time=0.4)
        lg = a4_tc("none", cols["Godot"], -2.2, 36)
        self.play(Create(g["slot"]), FadeIn(lg), run_time=0.45)
        done(self)


# ───────────────────────── B20 · Unity: public March 2026, open beta, text scenes full of references ─────────────────────────
class B20_UnityBeta(Scene):
    """Phase A: Unity's own docs page and the changelog entry dated 2026-03-03 that made MCP public (real captures). Phase B (before the midpoint):
    the blog's words, quoted not captured. Phase C: Unity's own YAML excerpt, with its fileID cross-references marked."""
    def construct(self):
        un = a4_tl("Unity", -6.1, 2.6, 48)
        sh1, im1, h1 = a4_img("a4_unity_docs.png", 2.1, 1.55, 8.2)
        self.play(FadeIn(un), FadeIn(sh1), FadeIn(im1), run_time=0.45)
        a4_at(self, 1.0)                                           # "went public in March 2026"
        sh2, im2, h2 = a4_img("a4_unity_changelog.png", 2.1, -1.0, 8.2)
        self.play(FadeIn(sh2), FadeIn(im2), run_time=0.45)
        d1 = Dot([-2.45, -1.0, 0], radius=0.11, color=TERRA)
        l1 = a4_tl("public, March 2026", -6.1, -1.0, 32)
        self.play(GrowFromCenter(d1), FadeIn(l1), run_time=0.3)
        a4_at(self, 2.6)                                           # "open beta"
        l2 = a4_tl("open beta", -6.1, 1.75, 44)
        self.play(FadeIn(l2), run_time=0.3)
        # phase B: the blog's words (before the clip midpoint)
        a4_at(self, 3.9)                                           # "Unity's own blog"
        self.play(FadeOut(sh1), FadeOut(im1), FadeOut(sh2), FadeOut(im2), FadeOut(d1), FadeOut(l1), run_time=0.3)
        pg = a4_page(-0.9, 0.9)
        q = [a4_tl("“may change, be limited,", 0.2, 1.4, 36), a4_tl("or be discontinued", 0.2, 0.85, 36), a4_tl("without notice”", 0.2, 0.3, 36)]
        src = a4_tl("Unity blog, 11 May 2026", 0.2, -0.6, 32)
        nt = a4_tl("quoted, not captured", 0.2, -1.1, 32)
        self.play(FadeIn(pg), run_time=0.3)
        self.play(*[FadeIn(x) for x in q], FadeIn(src), FadeIn(nt), run_time=0.5)
        # phase C (after the midpoint): Unity's own YAML, trimmed
        a4_at(self, 6.75)                                          # "Its scenes are text"
        self.play(FadeOut(pg), *[FadeOut(x) for x in q], FadeOut(src), FadeOut(nt), FadeOut(l2), run_time=0.3)
        hd = a4_tl("text by default", -1.6, 2.4, 40)
        lines = ["--- !u!4 &8", "Transform:", "  m_GameObject: {fileID: 6}", "  m_Father: {fileID: 0}"]
        ys = [1.55, 0.95, 0.35, -0.25]
        ml = [a4_ml(s, -1.6, y) for s, y in zip(lines, ys)]
        self.play(FadeIn(hd), FadeIn(ml[0]), FadeIn(ml[1]), run_time=0.4)
        a4_at(self, 8.0)                                           # "by default"
        self.play(FadeIn(ml[2]), FadeIn(ml[3]), run_time=0.4)
        sc = a4_tl("Unity Manual, trimmed", -1.6, -2.0, 32)
        self.play(FadeIn(sc), run_time=0.25)
        a4_at(self, 9.15)                                          # "YAML"
        ya = a4_tl("YAML", 3.6, 2.4, 40)
        self.play(FadeIn(ya), run_time=0.3)
        a4_at(self, 10.0)                                          # "packed with cross-references"
        k1 = Dot([-1.95, 0.35, 0], radius=0.1, color=TERRA)
        k2 = Dot([-1.95, -0.25, 0], radius=0.1, color=TERRA)
        cr = a4_tl("cross-references", -1.6, -1.1, 36)
        self.play(GrowFromCenter(k1), GrowFromCenter(k2), FadeIn(cr), run_time=0.35)
        done(self)


# ───────────────────────── B21 · Unreal 5.8: Experimental; Epic's words; binary files ─────────────────────────
class B21_UnrealExperimental(Scene):
    """Left: Unreal's kraft box, an MCP block dropping on, the word Experimental in a tag. Right (before the midpoint): Epic's docs, quoted not
    captured. Bottom: .umap and .uasset as binary files, with a prohibition mark on 'read as text'."""
    def construct(self):
        t1 = a4_tl("Unreal Engine 5.8", -6.1, 2.9, 44)
        self.play(FadeIn(t1), run_time=0.4)
        e = a4_engine(-3.7, 0.55, 0.8)
        a4_at(self, 1.1)                                           # "5.8"
        self.play(FadeIn(e["box"], shift=UP * 0.2), run_time=0.4)
        a4_at(self, 1.9)                                           # "an MCP plug-in"
        e["mcp"].shift(UP * 1.2)
        self.add(e["mcp"])
        self.play(e["mcp"].animate.shift(DOWN * 1.2), run_time=0.45)
        a4_at(self, 3.05)                                          # "in June 2026"
        mo = a4_tl("June 2026", -6.1, 2.3, 32)
        self.play(FadeIn(mo), run_time=0.3)
        a4_at(self, 4.3)                                           # "labelled Experimental"
        pill = RoundedRectangle(width=3.5, height=0.7, corner_radius=0.35, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-3.7, -0.95, 0])
        px = a4_tl("Experimental", -3.7 - 1.75 + 0.7, -0.95, 36)
        pd = Dot([-3.7 - 1.75 + 0.4, -0.95, 0], radius=0.1, color=TERRA)
        self.play(Create(pill), FadeIn(px), GrowFromCenter(pd), run_time=0.4)
        # Epic's own docs, quoted (before the midpoint)
        a4_at(self, 6.35)                                          # "Epic's own documentation"
        pg = a4_page(0.3, 1.3)
        src = a4_tl("Epic, Unreal MCP docs", 1.3, 0.1, 32)
        nt = a4_tl("quoted, not captured", 1.3, -0.4, 32)
        self.play(FadeIn(pg), FadeIn(src), FadeIn(nt), run_time=0.4)
        q = [a4_tl("“Many features are", 1.3, 1.9, 36), a4_tl("incomplete or", 1.3, 1.35, 36), a4_tl("missing.”", 1.3, 0.8, 36)]
        a4_at(self, 7.0)
        self.play(*[FadeIn(x) for x in q], run_time=0.4)
        # the files (after the midpoint)
        a4_at(self, 10.9)                                          # "levels"
        bl = a4_tl("binary", -6.1, -2.1, 40)
        f1 = a4_binfile(-3.2, -2.05, 1.0, 1.1)
        l1 = M(".umap", 32).move_to([-3.2, -3.0, 0])
        self.play(FadeIn(bl), FadeIn(f1), FadeIn(l1), run_time=0.4)
        a4_at(self, 11.35)                                         # "assets"
        f2 = a4_binfile(-1.3, -2.05, 1.0, 1.1)
        l2 = M(".uasset", 32).move_to([-1.3, -3.0, 0])
        self.play(FadeIn(f2), FadeIn(l2), run_time=0.4)
        a4_at(self, 12.85)                                         # "an AI cannot read"
        no = a4_no(0.9, -2.0)
        rt = a4_tl("read as text", 1.45, -2.0, 36)
        self.play(Create(no), FadeIn(rt), run_time=0.45)
        a4_at(self, 14.0)
        ep = a4_tl("per Epic's UE 4.26 docs", 1.45, -2.75, 32)
        self.play(FadeIn(ep), run_time=0.3)
        done(self)


# ───────────────────────── B22 · stars: the community Godot server vs Unity's (real repo-header buttons + a bar each) ─────────────────────────
class B22_StarCounts(Scene):
    """Top row: the best-known community Godot MCP server (the real Fork / Star buttons of its GitHub header, Star 6k) and its bar; its last push in
    April. Second row: Unity's biggest community server (real buttons, Star 14.8k) and its bar, with ticks at 1x and 2x of Godot's. Scale: 0.4 units
    per thousand stars. The repo names are set as labels beside the real buttons."""
    def construct(self):
        K = 0.4
        X0 = -5.6
        gl = a4_tl("Godot", -6.1, 3.05, 40)
        rg = Circle(radius=0.13, stroke_color=DIM, stroke_width=5).move_to([a4_nx("Godot", -6.1, 40, 0.5), 3.05, 0])
        c1 = a4_tl("no official MCP", a4_nx("Godot", -6.1, 40, 0.8), 3.05, 32)
        self.play(FadeIn(gl), Create(rg), FadeIn(c1), run_time=0.4)
        a4_at(self, 2.3)                                           # "several from the community"
        shG, imG, hG = a4_img("a4_godot_mcp_banner.png", 2.8, 2.15, 6.42)
        nG = a4_tl("Coding-Solo/godot-mcp", -6.0, 2.15, 32)
        self.play(FadeIn(nG), FadeIn(shG), FadeIn(imG), run_time=0.45)
        c2 = a4_tl("community server", 1.5, 3.05, 32)
        self.play(FadeIn(c2), run_time=0.25)
        a4_at(self, 4.9)                                           # "about six thousand stars"
        bG = Rectangle(width=6.0 * K, height=0.42, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([X0 + 6.0 * K / 2, 1.15, 0])
        self.play(GrowFromEdge(bG, LEFT), run_time=0.6)
        vG = a4_tl("6.0k", X0 + 6.0 * K + 0.3, 1.15, 40)
        ft = a4_tl("GitHub stars, 9 Oct 2026", -6.1, -3.0, 32)
        self.play(FadeIn(vG), FadeIn(ft), run_time=0.3)
        a4_at(self, 7.3)                                           # "has not been updated since April"
        dG = Dot([-1.5, 1.15, 0], radius=0.1, color=TERRA)
        pG = a4_tl("last push 16 Apr 2026", -1.2, 1.15, 32)
        self.play(GrowFromCenter(dG), FadeIn(pG), run_time=0.35)
        a4_at(self, 9.25)                                          # "Unity's biggest community server"
        ul = a4_tl("Unity", -6.1, 0.3, 40)
        shU, imU, hU = a4_img("a4_unity_mcp_banner.png", 3.35, -0.6, 5.30)
        nU = a4_tl("CoplayDev/unity-mcp", -6.0, -0.6, 32)
        self.play(FadeIn(ul), FadeIn(nU), FadeIn(shU), FadeIn(imU), run_time=0.45)
        c3 = a4_tl("community server", a4_nx("Unity", -6.1, 40, 0.8), 0.3, 32)
        bU = Rectangle(width=14.8 * K, height=0.42, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to(
            [X0 + 14.8 * K / 2, -1.55, 0])
        self.play(FadeIn(c3), GrowFromEdge(bU, LEFT), run_time=0.9)
        vU = a4_tl("14.8k", X0 + 14.8 * K + 0.3, -1.55, 40)
        dU = Dot([2.2, -1.55, 0], radius=0.1, color=TERRA)
        pU = a4_tl("last push 8 Oct 2026", 2.45, -1.55, 32)
        self.play(FadeIn(vU), GrowFromCenter(dU), FadeIn(pU), run_time=0.3)
        a4_at(self, 11.4)                                          # "more than twice that"
        t1 = Line([X0 + 6.0 * K, -1.23, 0], [X0 + 6.0 * K, -1.95, 0], color=DIM, stroke_width=5)
        t2 = Line([X0 + 12.0 * K, -1.23, 0], [X0 + 12.0 * K, -1.95, 0], color=DIM, stroke_width=5)
        n1 = a4_tc("1×", X0 + 6.0 * K, -2.35, 32)
        n2 = a4_tc("2×", X0 + 12.0 * K, -2.35, 32)
        self.play(Create(t1), Create(t2), FadeIn(n1), FadeIn(n2), run_time=0.4)
        done(self)


# ───────────────────────── B23 · "better MCP story?" No. The comparison, plainly ─────────────────────────
class B23_NoBetterStory(Scene):
    """A drawn table: rows official MCP / scenes as text / command line / licence, columns Godot / Unity / Unreal. Terracotta dot = has it, grey ring =
    lacks it. 'No.' lands with the MCP row (before the midpoint); 'no bridge needed' on 'basic work'; the text row on 'its files are plain text', the command-line row on 'its command line is complete', the licence row last."""
    def construct(self):
        CX = {"Godot": -1.7, "Unity": 1.3, "Unreal": 4.3}
        hd = a4_tl("better MCP story?", -6.1, 2.95, 40)
        self.play(FadeIn(hd), run_time=0.35)
        # legend + header + rules
        ld = Dot([1.75, 2.95, 0], radius=0.1, color=TERRA)
        lt = a4_tl("has it", 2.05, 2.95, 32)
        lr = Circle(radius=0.1, stroke_color=DIM, stroke_width=4).move_to([3.65, 2.95, 0])
        lt2 = a4_tl("lacks it", 3.95, 2.95, 32)
        heads = [a4_tc(k, x, 2.0, 36) for k, x in CX.items()]
        rules = [Line([-6.1, y, 0], [6.0, y, 0], color=GHOST, stroke_width=4) for y in (1.65, 0.75, -0.15, -1.05, -1.95)]
        self.play(FadeIn(ld), FadeIn(lt), Create(lr), FadeIn(lt2), *[FadeIn(h) for h in heads], Create(rules[0]), run_time=0.5)
        rows = [("official MCP", 1.2, [("none", 0), ("beta", 1), ("experimental", 1)]),
                ("scenes as text", 0.3, [("yes", 1), ("yes, YAML", 1), ("no", 0)]),
                ("command line", -0.6, [("yes", 1), ("yes", 1), ("yes", 1)]),
                ("licence", -1.5, [("MIT", None), ("proprietary", None), ("proprietary", None)])]

        def mkrow(r):
            name, y, cells = r
            grp = [a4_tl(name, -6.1, y, 34)]
            for (txt, has), x in zip(cells, CX.values()):
                grp.append(a4_tc(txt, x, y, 34))
                if has is not None:
                    px = x - a4_w(txt, 34) / 2.0 - 0.32
                    grp.append(Dot([px, y, 0], radius=0.1, color=TERRA) if has else Circle(radius=0.1, stroke_color=DIM, stroke_width=4).move_to([px, y, 0]))
            return grp
        a4_at(self, 1.75)                                          # "the better MCP story"
        r1 = mkrow(rows[0])
        self.play(Create(rules[1]), *[FadeIn(x) for x in r1], run_time=0.5)
        a4_at(self, 3.15)                                          # "it does not"
        no = a4_tl("No.", -1.7, 2.95, 48, INK, True)
        self.play(FadeIn(no), run_time=0.3)
        a4_at(self, 5.75)                                          # "for the basic work" (after the midpoint)
        nb = a4_tc("no bridge needed", CX["Godot"], -2.5, 36)
        self.play(FadeIn(nb), run_time=0.3)
        a4_at(self, 6.75)                                          # "its files are plain text"
        r2 = mkrow(rows[1])
        self.play(Create(rules[2]), *[FadeIn(x) for x in r2], run_time=0.45)
        a4_at(self, 8.15)                                          # "its command line is complete"
        r3 = mkrow(rows[2])
        self.play(Create(rules[3]), *[FadeIn(x) for x in r3], run_time=0.45)
        a4_at(self, 9.2)                                           # "complete" (the honest rest of the table)
        r4 = mkrow(rows[3])
        self.play(Create(rules[4]), *[FadeIn(x) for x in r4], run_time=0.4)
        done(self)


# ───────────────────────── B24 · two cards kept apart: contributing TO Godot / making a game WITH Godot ─────────────────────────
class B24_TwoThings(Scene):
    """A divider and two headings keep the two things apart. Left (before the midpoint): the Godot Foundation's real post header and two short
    quotes from the same page, with a prohibition mark by the agents line. Right (lands at 'Using an AI to make a game'): 1.4 s of REAL gameplay of
    the walker-claude capture, stepped at 10 fps, labelled 'scripted input, recorded 2026-10-09'."""
    def construct(self):
        dv = Line([0, 3.15, 0], [0, -3.15, 0], color=DIM, stroke_width=5)
        hl = a4_tl("contributing TO Godot", -6.1, 2.85, 36)
        hr = a4_tl("making a game WITH Godot", 0.4, 2.85, 36)
        self.play(Create(dv), FadeIn(hl), FadeIn(hr), run_time=0.5)
        a4_at(self, 1.75)                                          # "In June 2026"
        sh, im, h = a4_img("a4_policy_title.png", -3.1, 1.85, 6.0)
        self.play(FadeIn(sh), FadeIn(im), run_time=0.4)
        a4_at(self, 4.3)                                           # "engine code must be human-written"
        q1 = [a4_tl("“We require all code to", -5.3, 0.85, 34), a4_tl("be human authored.”", -5.3, 0.4, 34)]
        self.play(*[FadeIn(x) for x in q1], run_time=0.4)
        a4_at(self, 6.25)                                          # "and would ban autonomous agents"
        q2 = [a4_tl("“No autonomous AI agent", -5.3, -0.45, 34), a4_tl("use or vibe coding”", -5.3, -0.9, 34)]
        self.play(*[FadeIn(x) for x in q2], run_time=0.4)
        sr = a4_tl("Godot Foundation", -5.3, -1.7, 32)
        s2 = a4_tl("30 Jun 2026, same page", -5.3, -2.2, 32)
        self.play(FadeIn(sr), FadeIn(s2), run_time=0.3)
        a4_at(self, 7.85)                                          # "its repository" (after the midpoint)
        no = a4_no(-5.8, -0.68, 0.26, 6)
        self.play(Create(no), run_time=0.35)
        # the right card: a real game, after the midpoint
        a4_at(self, 11.35)                                         # "Using an AI to make a game with Godot"
        win = ImageMobject(A4P + "a4_game_00.png").set_width(5.4).move_to([3.2, 0.7, 0])
        gsh = Rectangle(width=5.4, height=5.4 * 720 / 1280, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([3.27, 0.63, 0])
        self.play(FadeIn(gsh), FadeIn(win), run_time=0.4)
        cap1 = a4_tl("scripted input,", 0.55, -1.3, 32)
        cap2 = a4_tl("recorded 2026-10-09", 0.55, -1.75, 32)
        arrs = []
        for i in range(15):
            arrs.append(getattr(ImageMobject(A4P + f"a4_game_{i:02d}.png"), "pixel_array", None))
        if arrs[0] is not None and hasattr(arrs[0], "shape"):
            def step(m, a):
                m.pixel_array = arrs[min(14, int(a * 15))].copy()
            self.play(UpdateFromAlphaFunc(win, step), FadeIn(cap1), FadeIn(cap2), run_time=1.4, rate_func=linear)
        else:                                                      # Gate A's stub carries no pixels
            self.play(win.animate.shift(UP * 0.01), FadeIn(cap1), FadeIn(cap2), run_time=1.4)
        a4_at(self, 13.8)                                          # "a different thing"
        dt = a4_tl("a different thing", 0.55, -2.6, 40)
        self.play(FadeIn(dt), run_time=0.3)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Why It Fits, and What This Proves  (B25-B27, all Manim)

One cast for the act: THE THREE EXHIBITS (B25) and THE TABLE (B26) and THE TWO EMPTY CELLS (B27) - one grid language: outline-only
cells in grey, real text in Menlo, labels in EB Garamond, a terracotta dot as the only accent.
B25 shows three REAL exhibits from the earlier acts: the real scene text (godot-evidence/part2/pong.tscn.after), the real command and its
real exit line (part2/independent-checks.txt section 4), and the real download button on godotengine.org (web-captures, cropped).
B26 is a dated table; every cell is traceable in factcheck/act5.md. B27 draws what is NOT shown, as empty cells.
"""

A5P = "pantry/"


def a5_at(self, t):
    """Wait until the clip clock reaches t seconds (word times measured from mp3/beat-<ID>.mp3 with faster-whisper base.en)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a5_lab(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a5_left(s, x, y, size=36, color=INK):
    """A label whose LEFT edge sits at x (explicit coordinates, never get_left)."""
    t = T(s, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


def a5_mleft(s, x, y, size=32, color=INK):
    t = M(s, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


def a5_slot(cx, cy, w, h, color=DIM, sw=4):
    """An empty slot: dashed outline, no fill."""
    return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=0.12).move_to([cx, cy, 0]),
                          num_dashes=44).set_stroke(color, sw)


def a5_cell(cx, cy, w, h, color=DIM, sw=3):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])


def a5_cross(x, y, s=0.17, color=INK, w=7):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w))


# ── B25 · three properties as three real exhibits: plain text / command line / no account ─────────────────────────────
class B25_WhyItFits(Scene):
    def construct(self):
        title = T("Why It Fits, and What This Proves", 40)
        title.move_to([-6.0 + title.width / 2, 2.95, 0])
        self.add(title)
        ys = [1.4, -0.5, -2.4]
        BX, BW, BH = -1.8, 8.6, 1.6                       # exhibit slots: x from -6.1 to 2.5
        slots = [a5_slot(BX, y, BW, BH) for y in ys]
        a5_at(self, 1.6)                                           # "not because it has the best A. I. features": three empty places
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.3), run_time=1.2)       # three empty places to fill
        ptr = Dot([2.8, ys[0], 0], radius=0.1, color=TERRA)
        # 1 - plain text: the real scene text of the Pong game, typed in
        a5_at(self, 4.45)                                          # "everything you need to inspect"
        l1 = a5_mleft('[node name="HelloLabel" …', -5.8, ys[0] + 0.33)
        l2 = a5_mleft('text = "Hello from a text file"', -5.8, ys[0] - 0.33)
        lab1 = a5_left("plain text", 3.1, ys[0], 40)
        self.play(FadeOut(slots[0]), FadeIn(ptr), run_time=0.25)
        box1 = a5_cell(BX, ys[0], BW, BH)
        self.play(Create(box1), AddTextLetterByLetter(l1, time_per_char=0.015), FadeIn(lab1), run_time=0.45)
        self.play(AddTextLetterByLetter(l2, time_per_char=0.015), run_time=0.45)
        # (midpoint: title, the scene text with its label, two empty slots waiting)
        # 2 - command line: the real command and its real exit line
        a5_at(self, 6.95)                                          # "everything you need to run"
        c1 = a5_mleft("$ godot --headless …", -5.8, ys[1] + 0.47)
        c1b = a5_mleft("… --quit-after 60", -5.8, ys[1])
        c2 = a5_mleft("exit=0  wall=0.56s", -5.8, ys[1] - 0.47)
        lab2 = a5_left("command line", 3.1, ys[1], 40)
        box2 = a5_cell(BX, ys[1], BW, BH)
        self.play(FadeOut(slots[1]), ptr.animate.move_to([2.8, ys[1], 0]), run_time=0.35)
        self.play(Create(box2), AddTextLetterByLetter(c1, time_per_char=0.03), run_time=0.6)
        self.play(AddTextLetterByLetter(c1b, time_per_char=0.03), run_time=0.5)
        self.play(AddTextLetterByLetter(c2, time_per_char=0.04), FadeIn(lab2), run_time=0.6)
        # 3 - no account: the real download button
        a5_at(self, 9.3)                                           # "nothing sits behind an account"
        btn = ImageMobject(A5P + "a5_download_button_r.png").set_width(4.4).move_to([BX, ys[2], 0])
        lab3 = a5_left("no account", 3.1, ys[2], 40)
        self.play(FadeOut(slots[2]), ptr.animate.move_to([2.8, ys[2], 0]), FadeIn(btn, scale=0.96), FadeIn(lab3), run_time=0.7)
        done(self)


# ── B26 · a dated snapshot: the table, 9 October 2026 ─────────────────────────────────────────────────────────────────
A5_COLX = [-1.775, 1.375, 4.525]                            # Godot, Unity, Unreal column centres (each 3.15 wide)
A5_ROWY = [0.5, -0.7, -1.9]                                 # scene files, official MCP, licence (each 1.2 tall)


class B26_Snapshot(Scene):
    def construct(self):
        # the grid draws while the voice says "Unity is close on text"
        heads = [a5_lab(n, x, 1.75, 38) for n, x in zip(["Godot", "Unity", "Unreal"], A5_COLX)]
        rows = [a5_left(n, -6.0, y, 34) for n, y in zip(["scene files", "official MCP", "licence"], A5_ROWY)]
        cells = [[a5_cell(x, y, 3.15, 1.2) for x in A5_COLX] for y in A5_ROWY]
        self.play(FadeIn(VGroup(*heads)), FadeIn(VGroup(*rows)),
                  LaggedStart(*[Create(c) for c in cells[0]], lag_ratio=0.2), run_time=0.9)
        # row 1: text / text (YAML) / binary
        g = a5_lab("text", A5_COLX[0] + 0.3, A5_ROWY[0], 32)
        u = a5_lab("text (YAML)", A5_COLX[1] + 0.3, A5_ROWY[0], 32)
        r = a5_lab("binary", A5_COLX[2] + 0.3, A5_ROWY[0], 32)
        a5_at(self, 0.9)                                           # "Unity is close on text"
        self.play(FadeIn(g), Create(check(A5_COLX[0] - 1.2, A5_ROWY[0], s=0.15, w=6)),
                  FadeIn(u), Create(check(A5_COLX[1] - 1.2, A5_ROWY[0], s=0.15, w=6)), run_time=0.7)
        a5_at(self, 1.7)                                           # "Unreal is furthest"
        self.play(FadeIn(r), Create(a5_cross(A5_COLX[2] - 1.2, A5_ROWY[0], s=0.13, w=6)), run_time=0.5)
        # row 2: the official MCP: none / open beta / Experimental (their own labels: features may change)
        a5_at(self, 2.85)                                          # "and both say their features may change"
        self.play(*[Create(c) for c in cells[1]], run_time=0.5)
        m_g = a5_lab("none", A5_COLX[0], A5_ROWY[1], 34)
        m_u = a5_lab("open beta", A5_COLX[1], A5_ROWY[1], 34)
        m_r = a5_lab("Experimental", A5_COLX[2], A5_ROWY[1], 34)
        self.play(FadeIn(m_g), FadeIn(m_u), FadeIn(m_r), run_time=0.5)
        # row 3: licence
        self.play(*[Create(c) for c in cells[2]], run_time=0.4)
        l_g = a5_lab("MIT", A5_COLX[0], A5_ROWY[2], 34)
        l_u = a5_lab("proprietary", A5_COLX[1], A5_ROWY[2], 34)
        l_r = a5_lab("proprietary", A5_COLX[2], A5_ROWY[2], 34)
        self.play(FadeIn(l_g), FadeIn(l_u), FadeIn(l_r), run_time=0.4)
        # (midpoint: the whole table, filled)
        # the date: stamped on "the ninth of October"
        a5_at(self, 6.05)                                          # "the ninth of October"
        stamp = RoundedRectangle(width=3.8, height=0.85, corner_radius=0.12, stroke_color=DIM, stroke_width=5, fill_opacity=0
                                 ).move_to([4.2, 2.95, 0])
        date = a5_lab("9 October 2026", 4.2, 2.95, 36)
        dot = Dot([2.05, 2.95, 0], radius=0.1, color=TERRA)
        self.play(Create(stamp), FadeIn(date, scale=1.15), GrowFromCenter(dot), run_time=0.6)
        # check again: a circular arrow draws round
        a5_at(self, 8.25)                                          # "Check it again"
        arc = Arc(radius=0.34, start_angle=0.5, angle=4.9, stroke_color=INK, stroke_width=6).move_to([-1.3, -2.95, 0])
        tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-2.2).move_to([-1.05, -2.74, 0])
        again = a5_left("check again before you rely on it", -0.7, -2.95, 34)
        self.play(Create(arc), FadeIn(tip), FadeIn(again), run_time=0.7)
        done(self)


# ── B27 · what this film does not show: two empty cells, yours to test ────────────────────────────────────────────────
class B27_NotShown(Scene):
    def construct(self):
        CX = [-3.1, 3.1]
        w1 = a5_lab("better games?", CX[0], 1.75, 38)
        w2 = a5_lab("large, complicated scenes?", CX[1], 1.75, 38)
        c1 = a5_slot(CX[0], -0.35, 5.6, 3.0)
        c2 = a5_slot(CX[1], -0.35, 5.6, 3.0)
        a5_at(self, 1.45)                                          # "that Godot makes better games"
        self.play(FadeIn(w1), Create(c1), run_time=0.7)
        a5_at(self, 3.15)                                          # "or that an agent handles large, complicated scenes"
        self.play(FadeIn(w2), Create(c2), run_time=0.7)
        # (midpoint: two labelled empty cells)
        a5_at(self, 6.95)                                          # "Those are for you to test"
        k1, k2 = cursor(CX[0] - 0.9, -0.15), cursor(CX[1] - 0.9, -0.15)
        d1, d2 = Dot([CX[0] + 0.45, -0.55, 0], radius=0.1, color=TERRA), Dot([CX[1] + 0.45, -0.55, 0], radius=0.1, color=TERRA)
        you = a5_lab("yours to test", 0.0, -2.75, 40)
        self.play(FadeIn(k1, shift=UP * 0.3), FadeIn(k2, shift=UP * 0.3), run_time=0.4)
        self.play(GrowFromCenter(d1), GrowFromCenter(d2), FadeIn(you), run_time=0.4)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
