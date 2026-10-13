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
"""ACT I · Three Simple Assets  (B01–B13 Manim; B14 is a Remotion BrowserCapture, see lanes/act1.json)

One cast for the act: the three REAL assets (crate, lantern, coin) as real Blender 5.1.2 renders (pantry/ev_*_34.png,
cropped to pantry/a1_crate|lantern|coin.png). Everything else that is a real thing is shown as itself: Blender by its real
icon and its real window (Blender's own screenshot), Godot by its real icon and the real Godot screenshot, Claude Code by
the library's Claude Code skin with nothing typed, the add-on by its README's own words.
Act I renders (evidence/act1/render_act1.py, crop_act1.py): the five default basic shapes, the lantern and the crate built
shape by shape (same camera as the real renders, so the pictures stack), and four example assets (platform, tree, rock, gem).
Numbers on screen are the real counts from evidence/primitives/tris.log and evidence/act1/render_act1.log.
Pacing: until() leads were set from faster-whisper word times (evidence/act1/word_times.json), not from the character share.
"""

A1P = "pantry/"


def a1_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A1P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a1_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_no(x, y, r=0.32, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE or over a picture, never over type."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a1_toggle(x, y):
    """A generic OFF switch (outline pill, grey knob on the left)."""
    pill = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK,
                            stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x - 0.2, y, 0])
    return VGroup(pill, knob)


def a1_cloud(x, y, s=1.0):
    parts = [Circle(radius=0.62 * s).move_to([x - 0.55 * s, y - 0.1 * s, 0]),
             Circle(radius=0.8 * s).move_to([x + 0.15 * s, y + 0.25 * s, 0]),
             Circle(radius=0.6 * s).move_to([x + 0.85 * s, y - 0.12 * s, 0]),
             RoundedRectangle(width=2.6 * s, height=0.75 * s, corner_radius=0.37 * s).move_to([x + 0.12 * s, y - 0.35 * s, 0])]
    for p in parts:
        p.set_fill(BAR2, 1).set_stroke(width=0)
    rim = VGroup(*[p.copy().set_fill(opacity=0).set_stroke(INK, 4) for p in parts[:3]])
    rim.set_z_index(0)
    fill = VGroup(*parts).set_z_index(1)
    return VGroup(rim, fill)


# ── B01 · the job: three simple assets, then into the game engine ────────────────────────────────────────────────
class B01_ThreeAssets(Scene):
    def construct(self):
        title = T("Three  Simple  Assets", 40).move_to([-3.75, 2.95, 0])
        self.add(title)
        xs = [-4.4, -1.4, 1.5]
        until(self, "three simple", lead=0.25)
        slots = VGroup(*[Ellipse(width=1.9, height=0.42, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x, -1.25, 0])
                         for x in xs])
        self.play(LaggedStart(*[GrowFromCenter(s) for s in slots], lag_ratio=0.25), run_time=0.7)
        crate = a1_img("a1_crate.png", h=2.35, at=(xs[0], -0.05))
        lantern = a1_img("a1_lantern.png", h=2.35, at=(xs[1], -0.05))
        coin = a1_img("a1_coin.png", w=2.3, at=(xs[2], -0.55))
        labs = [a1_lab("crate", xs[0], -1.95, 36), a1_lab("lantern", xs[1], -1.95, 36), a1_lab("coin", xs[2], -1.95, 36)]
        for img, lab, ph, ld in [(crate, labs[0], "a crate", 0.34), (lantern, labs[1], "a lantern", 0.32), (coin, labs[2], "a coin", 0.23)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.25), FadeIn(lab), run_time=0.4)
        until(self, "Then show", lead=0.07)
        arrow = Arrow([3.05, -0.05, 0], [3.95, -0.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.24)
        godot = a1_img("ev_icon_godot.png", h=2.0, at=(5.05, -0.05))
        g_l = a1_lab("Godot", 5.05, -1.95, 36)
        self.play(GrowArrow(arrow), FadeIn(godot), FadeIn(g_l), run_time=0.6)
        # small copies of the three assets ride the arrow into the engine
        trio = Group(a1_img("a1_crate.png", h=0.55, at=(2.35, 0.6)), a1_img("a1_lantern.png", h=0.55, at=(2.85, 0.6)),
                     a1_img("a1_coin.png", w=0.6, at=(3.4, 0.45)))
        self.play(FadeIn(trio), run_time=0.3)
        self.play(trio.animate.scale(0.5).move_to([5.05, -0.05, 0]), run_time=0.8)
        self.play(FadeOut(trio), run_time=0.2)
        until(self, "the way you meant", lead=0.62)
        ok = check(5.0, 1.55, s=0.28, color=INK, w=8)
        spark = Dot([5.65, 1.7, 0], radius=0.1, color=TERRA)
        self.play(Create(ok), FadeIn(spark), run_time=0.5)
        done(self)


# ── B02 · Claude drives Blender through MCP; you stay in the loop ────────────────────────────────────────────────
class B02_ClaudeDrives(Scene):
    def construct(self):
        cc = a1_img("a1_cc_shell.png", w=3.5, at=(-4.35, 1.05))
        cc_l = a1_lab("Claude Code", -4.35, -0.35, 36)
        bl = a1_img("ev_icon_blender.png", h=1.85, at=(4.35, 1.05))
        bl_l = a1_lab("Blender", 4.35, -0.35, 36)
        self.add(cc, cc_l, bl, bl_l)
        until(self, "Claude drives", lead=0.37)
        long = Arrow([-2.4, 1.05, 0], [3.2, 1.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.26)
        self.play(GrowArrow(long), run_time=0.7)
        until(self, "the free", lead=0.46)
        free = a1_lab("free", 4.35, -0.9, 32)
        self.play(FadeIn(free), run_time=0.35)
        until(self, "through a standard", lead=0.85)
        iso = Iso(-0.65, 0.42, 1.0)
        block = iso.mcp(0, 0, 0, w=1.3, d=1.3, h=0.7)
        m_l = a1_lab("MCP", 0.0, -0.35, 36)
        a1 = Arrow([-2.4, 1.05, 0], [-1.35, 1.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.24)
        a2 = Arrow([1.35, 1.05, 0], [3.2, 1.05, 0], buff=0, color=INK, stroke_width=6, tip_length=0.26)
        self.play(FadeOut(long), FadeIn(a1), FadeIn(a2), FadeIn(block, shift=DOWN * 0.3), FadeIn(m_l), run_time=0.6)
        until(self, "And you stay", lead=0.05)
        you = cursor(4.7, -1.75, s=0.6)
        you_l = a1_lab("you", 3.85, -2.05, 36)
        self.play(FadeIn(you, shift=UP * 0.2), FadeIn(you_l), run_time=0.45)
        until(self, "at least one edit", lead=0.75)
        loop = CurvedArrow([5.25, -2.0, 0], [5.55, 0.35, 0], angle=PI / 2.2, color=INK, stroke_width=6, tip_length=0.24)
        e_l = a1_lab("one edit by hand", 3.85, -2.8, 34)
        self.play(Create(loop), FadeIn(e_l), run_time=0.7)
        until(self, "made by hand", lead=1.07)
        spark = Dot([5.75, -0.1, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(spark, scale=0.5), run_time=0.35)
        done(self)


# ── B03 · three kinds of asset, each named thing appears on its word ────────────────────────────────────────────
class B03_ThreeKinds(Scene):
    def construct(self):
        cols = [-4.3, 0.0, 4.3]
        divs = VGroup(*[Line([x, 2.35, 0], [x, -2.4, 0], color=GHOST, stroke_width=4) for x in (-2.15, 2.15)])
        self.play(Create(divs), run_time=0.4)
        heads = [a1_lab("prop", cols[0], 2.8, 38), a1_lab("environment", cols[1], 2.8, 38), a1_lab("collectible", cols[2], 2.8, 38)]
        pointer = Dot([cols[0] - 0.85, 2.8, 0], radius=0.1, color=TERRA)
        crate = a1_img("a1_crate.png", h=1.75, at=(cols[0], 1.0))
        lantern = a1_img("a1_lantern.png", h=1.75, at=(cols[0], -1.35))
        platform = a1_img("a1_ex_platform.png", w=2.7, at=(cols[1], 1.15))
        tree = a1_img("a1_ex_tree.png", h=1.8, at=(cols[1] - 0.85, -1.3))
        rock = a1_img("a1_ex_rock.png", w=1.45, at=(cols[1] + 0.9, -1.75))
        coin = a1_img("a1_coin.png", w=2.2, at=(cols[2], 0.95))
        gem = a1_img("a1_ex_gem.png", h=1.15, at=(cols[2], -1.45))
        until(self, "A prop", lead=0.68)
        self.play(FadeIn(heads[0]), FadeIn(pointer, scale=0.5), run_time=0.35)
        for img, ph, ld in [(crate, "a crate", 0.81), (lantern, "a lantern", 0.79)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.35)
        until(self, "A piece of the environment", lead=0.53)
        self.play(FadeIn(heads[1]), pointer.animate.move_to([cols[1] - 1.55, 2.8, 0]), run_time=0.45)
        for img, ph, ld in [(platform, "a platform", 0.77), (tree, "a tree", 0.76), (rock, "a rock", 0.65)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.35)
        until(self, "something the player collects", lead=0.55)
        self.play(FadeIn(heads[2]), pointer.animate.move_to([cols[2] - 1.4, 2.8, 0]), run_time=0.45)
        for img, ph, ld in [(coin, "a coin", 1.17), (gem, "a gem", 0.97)]:
            until(self, ph, lead=ld)
            self.play(FadeIn(img, shift=DOWN * 0.2), run_time=0.35)
        done(self)


# ── B04 · simple = Blender's basic shapes, moved, scaled, combined, one flat colour; four things ruled out ─────────────
A1_K = 1.85 / 1116.0                              # scene units per pixel: the five primitives share one camera, so sizes compare
A1_PRIMS = [("cube", 1109, 1116, -4.30), ("cylinder", 807, 999, -1.96), ("cone", 744, 903, 0.08),
            ("sphere", 774, 774, 2.08), ("plane", 1064, 426, 4.35)]


class B04_BasicShapes(Scene):
    def construct(self):
        icon = a1_img("ev_icon_blender.png", h=0.72, at=(-5.65, 2.8))
        head = a1_lab("basic shapes", -4.0, 2.8, 38)
        until(self, "basic shapes", lead=0.58)
        self.play(FadeIn(icon), FadeIn(head), run_time=0.4)
        prims, labs = [], []
        base = Line([-5.4, -0.32, 0], [5.4, -0.32, 0], color=GHOST, stroke_width=4)
        self.play(Create(base), run_time=0.3)
        for (name, pw, ph, x), ld in zip(A1_PRIMS, (0.46, 0.48, 0.59, 0.41, 0.57)):
            h = ph * A1_K
            im = a1_img(f"a1_clay_{name}.png", h=h, at=(x, -0.3 + h / 2))
            lb = a1_lab(name, x, -0.9, 34)
            prims.append(im); labs.append(lb)
            until(self, name, lead=ld)
            self.play(FadeIn(im, shift=DOWN * 0.2), FadeIn(lb), run_time=0.28)
        until(self, "Move them", lead=-0.4)                # just after the midpoint: the row of shapes is the still GATE T reads
        # the clay lantern's five parts arrive spread out and oversized: move, scale, combine
        LH, LX, LY = 4.3, -3.2, -0.25
        cum = [a1_img(f"a1_clay_lancum_{i}.png", h=LH, at=(LX, LY)) for i in range(1, 6)]
        parts = [a1_img(f"a1_clay_lanpart_{i}.png", h=LH, at=(LX, LY)) for i in range(1, 6)]
        offs = [(-0.9, -0.55), (0.0, -0.1), (0.9, 0.3), (-0.6, 0.7), (0.7, 1.0)]
        for p, (dx, dy) in zip(parts, offs):
            p.scale(1.25).shift(np.array([dx, dy, 0.0]))
        self.play(*[FadeOut(m) for m in prims + labs + [base, head, icon]], *[FadeIn(p) for p in parts], run_time=0.45)
        until(self, "combine them", lead=0.67)
        self.play(*[p.animate.shift(np.array([-dx, -dy, 0.0])).scale(1 / 1.25) for p, (dx, dy) in zip(parts, offs)],
                  run_time=0.7)
        self.add(cum[4]); self.remove(*parts)           # the running total, so the parts overlap exactly as Blender drew them
        until(self, "give them a flat colour", lead=0.85)
        colour = a1_img("a1_lantern_colour.png", h=LH, at=(LX, LY))
        l_l = a1_lab("5 shapes, flat colours", LX, 2.6, 34)
        self.play(FadeIn(colour), FadeIn(l_l), run_time=0.5)
        self.remove(cum[4])
        rows = [("sculpting", 1.45, "No sculpting", 0.91), ("painted textures", 0.45, "no painted textures", 0.87),
                ("rigging", -0.55, "no rigging", 0.83), ("animation", -1.55, "no animation", 0.91)]
        for word, y, ph, ld in rows:
            until(self, ph, lead=ld)
            mark = a1_no(0.95, y, r=0.3)
            lab = T(word, 36).move_to([1.6, y, 0], aligned_edge=LEFT)
            self.play(Create(mark), FadeIn(lab), run_time=0.35)
        done(self)


# ── B05 · the budget: six shapes, 500 triangles; what a triangle is ─────────────────────────────────────────────────
def a1_cube_pt(x, y, z):
    """An oblique (not isometric) view, so the hidden back corner does not land on a front corner."""
    return np.array([3.2 + 2.0 * x - 1.1 * y, -1.9 + 0.6 * x + 0.8 * y + 2.0 * z, 0.0])


class B05_Budget(Scene):
    def construct(self):
        until(self, "no more than six", lead=0.73)
        six = T("6", 120).move_to([-4.85, 1.35, 0])
        six_l = a1_lab("basic shapes", -4.85, 0.0, 34)
        self.play(FadeIn(six, shift=UP * 0.2), FadeIn(six_l), run_time=0.45)
        until(self, "five hundred triangles", lead=0.95)
        five = T("500", 120).move_to([-1.95, 1.35, 0])
        five_l = a1_lab("triangles", -1.95, 0.0, 34)
        self.play(FadeIn(five, shift=UP * 0.2), FadeIn(five_l), run_time=0.45)
        until(self, "A triangle is", lead=0.65)
        P = a1_cube_pt
        vis = [((0, 0, 0), (1, 0, 0)), ((1, 0, 0), (1, 0, 1)), ((1, 0, 1), (0, 0, 1)), ((0, 0, 1), (0, 0, 0)),
               ((0, 0, 0), (0, 1, 0)), ((0, 1, 0), (0, 1, 1)), ((0, 1, 1), (0, 0, 1)), ((0, 1, 1), (1, 1, 1)), ((1, 1, 1), (1, 0, 1))]
        hid = [((1, 1, 0), (1, 0, 0)), ((1, 1, 0), (0, 1, 0)), ((1, 1, 0), (1, 1, 1))]
        edges = VGroup(*[Line(P(*a), P(*b), color=INK, stroke_width=6) for a, b in vis])
        back = VGroup(*[DashedLine(P(*a), P(*b), color=DIM, stroke_width=4, dash_length=0.14) for a, b in hid])
        tri = Polygon(P(0, 0, 1), P(1, 0, 1), P(1, 1, 1), fill_color=TERRA, fill_opacity=1, stroke_width=0)
        tri.set_z_index(-1)
        t_l = a1_lab("a triangle", 4.35, 2.2, 34)
        self.play(Create(edges), Create(back), run_time=0.6)
        self.play(FadeIn(tri), FadeIn(t_l), run_time=0.4)
        until(self, "every surface is cut into", lead=0.64)
        diag_v = VGroup(Line(P(0, 0, 0), P(1, 0, 1), color=INK, stroke_width=5), Line(P(0, 0, 0), P(0, 1, 1), color=INK, stroke_width=5),
                        Line(P(0, 0, 1), P(1, 1, 1), color=INK, stroke_width=5))
        diag_h = VGroup(DashedLine(P(1, 0, 0), P(1, 1, 1), color=DIM, stroke_width=4, dash_length=0.14),
                        DashedLine(P(0, 1, 0), P(1, 1, 1), color=DIM, stroke_width=4, dash_length=0.14),
                        DashedLine(P(0, 0, 0), P(1, 1, 0), color=DIM, stroke_width=4, dash_length=0.14))
        self.play(Create(diag_v), Create(diag_h), run_time=0.8)
        c_l = a1_lab("cube: 12 triangles", 3.35, -2.6, 34)
        self.play(FadeIn(c_l), run_time=0.35)
        until(self, "Those limits", lead=0.10)
        brace = BraceBetweenPoints([-6.0, -0.55, 0], [-0.8, -0.55, 0], direction=DOWN, color=INK)
        k_l = a1_lab("course limits", -3.4, -1.45, 36)
        self.play(GrowFromCenter(brace), FadeIn(k_l), run_time=0.5)
        until(self, "They aren't", lead=0.29)
        n_l = a1_lab("not engine limits", -3.4, -2.1, 34)
        self.play(FadeIn(n_l), run_time=0.35)
        done(self)


# ── B06 · the trap: real triangle counts against the 500 budget ─────────────────────────────────────────────────────
A1_BASE = -2.25
A1_KT = 4.55 / 960.0
A1_BARS = [("cube", 12, -3.35), ("cylinder", 124, -1.45), ("cone", 62, 0.45), ("sphere", 960, 2.35)]


def a1_bar(n, x, fill):
    h = max(0.04, n * A1_KT)
    return Rectangle(width=1.2, height=h, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, A1_BASE + h / 2, 0])


class B06_Trap(Scene):
    def construct(self):
        cap = a1_lab("triangles, at Blender 5.1.2's defaults", -2.35, 2.95, 34)
        yb = A1_BASE + 500 * A1_KT
        budget = DashedLine([-5.6, yb, 0], [3.25, yb, 0], color=INK, stroke_width=5, dash_length=0.2)
        b_l = a1_lab("budget 500", -4.75, yb + 0.5, 34)
        self.add(cap, budget, b_l)
        base = Line([-4.15, A1_BASE, 0], [3.25, A1_BASE, 0], color=DIM, stroke_width=4)
        self.play(Create(base), run_time=0.4)
        bars, nums, names = {}, {}, {}
        for name, n, x in A1_BARS:
            bars[name] = a1_bar(n, x, BAR1 if name == "sphere" else BAR2)
            nums[name] = T(str(n), 40).move_to([x, A1_BASE + n * A1_KT + 0.38, 0])
            names[name] = a1_lab(name, x, A1_BASE - 0.5, 34)
        for name, ph, ld in [("cube", "A cube is", 0.31), ("cylinder", "A default cylinder", 0.25)]:
            until(self, ph, lead=ld)
            self.play(GrowFromEdge(bars[name], DOWN), FadeIn(names[name]), run_time=0.5)
            self.play(FadeIn(nums[name]), run_time=0.25)
        self.play(GrowFromEdge(bars["cone"], DOWN), FadeIn(names["cone"]), FadeIn(nums["cone"]), run_time=0.45)
        until(self, "A default sphere", lead=0.47)
        self.play(GrowFromEdge(bars["sphere"], DOWN), FadeIn(names["sphere"]), run_time=1.0)
        self.play(FadeIn(nums["sphere"]), run_time=0.3)
        until(self, "nearly twice", lead=0.80)
        over = dim_arrow([3.3, yb, 0], [3.3, A1_BASE + 960 * A1_KT, 0])
        o_l = a1_lab("1.92 × budget", 4.75, (yb + A1_BASE + 960 * A1_KT) / 2, 34)
        spark = Dot([2.35, A1_BASE + 960 * A1_KT - 0.25, 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(over), FadeIn(o_l), FadeIn(spark), run_time=0.6)
        done(self)


# ── B07 · the same sphere, 12 segments × 6 rings: 960 → 120 ─────────────────────────────────────────────────────────
class B07_LowerSegments(Scene):
    def construct(self):
        big = a1_img("a1_sphere_960.png", h=3.3, at=(-3.4, 0.55))
        b1 = a1_lab("32 segments × 16 rings", -3.4, -1.55, 34)
        b2 = a1_lab("960 triangles", -3.4, -2.2, 36)
        self.add(big, b1, b2)
        until(self, "lower the segment", lead=0.31)
        arrow = Arrow([-1.25, 0.55, 0], [1.25, 0.55, 0], buff=0, color=INK, stroke_width=6, tip_length=0.26)
        self.play(GrowArrow(arrow), run_time=0.6)
        until(self, "The same sphere", lead=0.16)
        small = a1_img("a1_sphere_120.png", h=3.3, at=(3.4, 0.55))
        self.play(FadeIn(small, shift=LEFT * 0.3), run_time=0.5)
        until(self, "twelve segments", lead=0.42)
        s1 = a1_lab("12 segments × 6 rings", 3.4, -1.55, 34)
        self.play(FadeIn(s1), run_time=0.35)
        until(self, "a hundred and twenty", lead=0.51)
        s2 = a1_lab("120 triangles", 3.4, -2.2, 36)
        spark = Dot([4.75, -2.2, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(s2), FadeIn(spark, scale=0.5), run_time=0.4)
        done(self)


# ── B08 · one game, one repository; each assignment a layer; this one is tagged a3 ──────────────────────────────────
A1_SLAB = 0.34


def a1_slab(i, ghost=False):
    iso = Iso(-0.55, -2.55, 1.0)
    z = i * A1_SLAB
    if ghost:
        return iso.box(0, 0, z, 2.4, 2.4, 0.27, top=CARD, left=BAR2, right=BAR1, sw=3)
    return iso.box(0, 0, z, 2.4, 2.4, 0.27)


def a1_slab_y(i):
    """Screen y of the middle of layer i's left face (Iso(-0.55,-2.55)): y0 + (x+y)/2 + z with x=0, y=1.2."""
    return -2.55 + 0.6 + i * A1_SLAB + 0.135


class B08_OneGame(Scene):
    def construct(self):
        floor = Iso(-0.55, -2.55, 1.0).quad([(-0.2, -0.2, 0), (2.6, -0.2, 0), (2.6, 2.6, 0), (-0.2, 2.6, 0)], GHOST, stroke=GHOST, sw=0)
        self.add(floor)
        until(self, "From the second", lead=0.13)
        s2 = a1_slab(0)
        l2 = M("a2", 34).move_to([-3.25, a1_slab_y(0), 0])
        self.play(FadeIn(s2, shift=DOWN * 0.4), FadeIn(l2), run_time=0.45)
        until(self, "one game in one repository", lead=0.96)
        g_l = a1_lab("one game,", -4.6, 1.75, 36)
        r_l = a1_lab("one repository", -4.6, 1.15, 36)
        self.play(FadeIn(g_l), FadeIn(r_l), run_time=0.45)
        until(self, "Each assignment adds", lead=0.45)
        s3 = a1_slab(1)
        self.play(FadeIn(s3, shift=DOWN * 0.4), run_time=0.4)
        ghosts = [a1_slab(i, ghost=True) for i in range(2, 9)]
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.3) for g in ghosts], lag_ratio=0.35), run_time=1.0)
        lg = M("a4 … a10", 32).move_to([-4.15, a1_slab_y(5), 0])
        self.play(FadeIn(lg), run_time=0.3)
        until(self, "git tag", lead=1.08)
        # the tag hangs from the a3 layer's right face (Iso(-0.55,-2.55): p(2.3, 0, 0.475) = (1.44, -0.925))
        tag = Polygon([2.75, -0.75, 0], [3.15, -0.4, 0], [4.55, -0.4, 0], [4.55, -1.1, 0], [3.15, -1.1, 0],
                      fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        hole = Circle(radius=0.09, stroke_color=INK, stroke_width=4).move_to([3.18, -0.75, 0])
        string = Line([1.44, -0.925, 0], [2.75, -0.75, 0], color=INK, stroke_width=4)
        t_l = M("git tag a3", 32).move_to([3.65, -1.7, 0])
        self.play(Create(string), FadeIn(tag), FadeIn(hole), run_time=0.5)
        self.play(FadeIn(t_l), run_time=0.3)
        until(self, "a three", lead=0.81)
        spark = Dot([3.18, -0.75, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(spark, scale=0.4), run_time=0.4)
        done(self)


# ── B09A / B09B / B10 · a 2-D game still gets three assets and a small 3-D scene; then the real scene ───────────────────
def a1_twod():
    frame = RoundedRectangle(width=4.3, height=2.7, corner_radius=0.12, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                             stroke_width=5).move_to([-3.85, 0.55, 0])
    ground = Rectangle(width=4.0, height=0.36, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-3.85, -0.55, 0])
    plat1 = Rectangle(width=1.1, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-4.85, 0.35, 0])
    plat2 = Rectangle(width=1.2, height=0.22, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-2.85, 0.95, 0])
    hero = Square(side_length=0.42, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.85, 0.67, 0])
    pick = Circle(radius=0.14, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-2.85, 1.3, 0])
    lab = a1_lab("2-D game", -3.85, -1.2, 36)
    return VGroup(frame, ground, plat1, plat2, hero, pick), lab


A1_FLOOR = Iso(2.75, -2.15, 1.12)


def a1_floor():
    return A1_FLOOR.quad([(0, 0, 0), (2.5, 0, 0), (2.5, 2.5, 0), (0, 2.5, 0)], BOX_TOP, stroke="#9C8462", sw=4)


def a1_stage_assets(h=1.25):
    """The three real renders standing on the stage (equal heights: before 'game scale')."""
    c = a1_img("a1_crate.png", h=h, at=(1.75, -0.25))
    l = a1_img("a1_lantern.png", h=h, at=(2.85, 0.05))
    k = a1_img("a1_coin.png", w=h * 1.0, at=(3.95, -0.45))
    return c, l, k


class B09A_TwoD(Scene):
    def construct(self):
        until(self, "If it's two-D", lead=0.32)
        game, g_l = a1_twod()
        self.play(FadeIn(game), FadeIn(g_l), run_time=0.5)
        until(self, "three assets", lead=0.71)
        c, l, k = a1_stage_assets()
        for im in (c, l, k):
            self.play(FadeIn(im, shift=DOWN * 0.2), run_time=0.25)
        until(self, "a small three-D scene", lead=0.86)
        floor = a1_floor()
        floor.set_z_index(-1)
        s_l = a1_lab("small 3-D scene", 2.75, -2.75, 36)
        self.play(GrowFromCenter(floor), FadeIn(s_l), run_time=0.6)
        done(self)


def a1_light():
    halo = Circle(radius=0.42, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([1.15, 2.3, 0])
    lamp = Dot([1.15, 2.3, 0], radius=0.2, color=TERRA)
    return halo, lamp


def a1_camera():
    body = RoundedRectangle(width=0.95, height=0.62, corner_radius=0.08, fill_color=BAR1, fill_opacity=1, stroke_color=INK,
                            stroke_width=4).move_to([5.3, 1.75, 0])
    lens = Circle(radius=0.2, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([4.75, 1.62, 0])
    view = Polygon([4.55, 1.55, 0], [3.2, 0.9, 0], [4.1, 0.25, 0], fill_color=GHOST, fill_opacity=0.9, stroke_width=0)
    view.set_z_index(-2)
    return view, body, lens


# "Game scale": the three renders shown in their TRUE relative sizes. All three were rendered with the same 50 mm lens, from
# camera distances 3.6 m (crate), 2.3 m (lantern), 1.0 m (coin) (evidence/renders/render_assets.py), so a picture's real size is
# proportional to its pixel size x its camera distance: crate 1116 px x 3.6, lantern 815 px x 2.3, coin 1046 px wide x 1.0.
A1_GS = 1.76 / (1116 * 3.6)
A1_GS_CRATE_H, A1_GS_LANTERN_H, A1_GS_COIN_W = 1116 * 3.6 * A1_GS, 815 * 2.3 * A1_GS, 1046 * 1.0 * A1_GS   # 1.76, 0.82, 0.46


def a1_game_scale(c, l, k):
    c.set_height(A1_GS_CRATE_H).move_to([1.65, -0.1, 0])
    l.set_height(A1_GS_LANTERN_H).move_to([2.95, -0.55, 0])
    k.set_width(A1_GS_COIN_W).move_to([3.7, -0.8, 0])


class B09B_SceneParts(Scene):
    def construct(self):
        game, g_l = a1_twod()
        floor = a1_floor(); floor.set_z_index(-1)
        c, l, k = a1_stage_assets()
        s_l = a1_lab("small 3-D scene", 2.75, -2.75, 36)
        self.add(game, g_l, floor, c, l, k, s_l)
        f_l = a1_lab("floor", 5.55, -1.45, 34)
        self.play(FadeIn(f_l), run_time=0.3)
        until(self, "one light", lead=0.16)
        halo, lamp = a1_light()
        lamp_l = a1_lab("light", 0.0, 2.3, 34)
        self.play(GrowFromCenter(halo), FadeIn(lamp), FadeIn(lamp_l), run_time=0.35)
        until(self, "a camera", lead=0.38)
        view, body, lens = a1_camera()
        cam_l = a1_lab("camera", 5.3, 2.5, 34)
        self.play(FadeIn(view), FadeIn(body), FadeIn(lens), FadeIn(cam_l), run_time=0.35)
        until(self, "game scale", lead=0.77)
        self.play(c.animate.set_height(A1_GS_CRATE_H).move_to([1.65, -0.1, 0]),
                  l.animate.set_height(A1_GS_LANTERN_H).move_to([2.95, -0.55, 0]),
                  k.animate.set_width(A1_GS_COIN_W).move_to([3.7, -0.8, 0]), run_time=0.6)
        sc_l = a1_lab("game scale", 4.55, -2.75, 34)
        self.play(s_l.animate.move_to([1.6, -2.75, 0]), run_time=0.25)
        self.play(FadeIn(sc_l), run_time=0.25)
        done(self)


class B10_ReuseScene(Scene):
    def construct(self):
        game, g_l = a1_twod()
        floor = a1_floor(); floor.set_z_index(-1)
        c, l, k = a1_stage_assets()
        a1_game_scale(c, l, k)
        halo, lamp = a1_light()
        view, body, lens = a1_camera()
        labs = [a1_lab("floor", 5.55, -1.45, 34), a1_lab("light", 0.0, 2.3, 34), a1_lab("camera", 5.3, 2.5, 34),
                a1_lab("game scale", 4.55, -2.75, 34)]
        s_l = a1_lab("small 3-D scene", 1.6, -2.75, 36)
        self.add(game, g_l, floor, c, l, k, halo, lamp, view, body, lens, s_l, *labs)
        self.play(*[FadeOut(m) for m in labs], run_time=0.35)
        until(self, "reuse that scene", lead=0.36)
        a4 = Arrow([4.1, -1.05, 0], [4.55, -2.2, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        a5 = Arrow([4.75, -0.8, 0], [5.6, -2.2, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        l4 = M("a4", 36).move_to([4.55, -2.65, 0])
        l5 = M("a5", 36).move_to([5.65, -2.65, 0])
        self.play(GrowArrow(a4), GrowArrow(a5), FadeIn(l4), FadeIn(l5), run_time=0.5)
        until(self, "connect it", lead=0.54)
        link = DashedLine([-1.55, -0.2, 0], [0.1, -0.7, 0], color=DIM, stroke_width=5, dash_length=0.16)
        n_l = a1_lab("not yet", -0.65, 0.35, 34)
        self.play(Create(link), FadeIn(n_l), run_time=0.5)
        done(self)


# ── B11 · the tools, each shown as itself; all free ─────────────────────────────────────────────────────────────────
class B11_Tools(Scene):
    def construct(self):
        until(self, "Claude Code", lead=0.38)
        cc = a1_img("a1_cc_shell.png", w=3.3, at=(-4.5, 1.25))
        cc_l = a1_lab("Claude Code", -4.5, -0.45, 36)
        self.play(FadeIn(cc, shift=UP * 0.2), FadeIn(cc_l), run_time=0.4)
        until(self, "university access", lead=0.70)
        cc_s = a1_lab("university access", -4.5, -1.0, 32)
        self.play(FadeIn(cc_s), run_time=0.3)
        until(self, "Blender, which", lead=0.34)
        bw = a1_img("a1_blender_view.png", h=2.6, at=(-0.6, 1.25))
        bw_l = a1_lab("Blender", -0.6, -0.45, 36)
        bw_s = a1_lab("free", -0.6, -1.0, 32)
        self.play(FadeIn(bw, shift=UP * 0.2), FadeIn(bw_l), run_time=0.4)
        self.play(FadeIn(bw_s), run_time=0.25)
        until(self, "the Blender M C P add-on", lead=0.56)
        card = RoundedRectangle(width=3.9, height=2.5, corner_radius=0.14, fill_opacity=0, stroke_color=INK,
                                stroke_width=4).move_to([3.85, 1.25, 0])
        r1 = T("MCP for Blender", 36).move_to([3.85, 2.0, 0])
        r2 = T("Connect Blender", 32).move_to([3.85, 1.4, 0])
        r3 = T("to any LLM", 32).move_to([3.85, 0.95, 0])
        r4 = M("License: MIT", 32).move_to([3.85, 0.45, 0])
        ad_l = a1_lab("MCP add-on", 3.85, -0.45, 36)
        self.play(Create(card), FadeIn(r1), FadeIn(r2), FadeIn(r3), FadeIn(r4), FadeIn(ad_l), run_time=0.45)
        src = a1_lab("README 2.1.9, 6 Oct 2026", 3.85, -1.55, 32)
        self.play(FadeIn(src), run_time=0.25)
        until(self, "also free", lead=0.58)
        ad_s = a1_lab("free", 3.85, -1.0, 32)
        self.play(FadeIn(ad_s), run_time=0.3)
        until(self, "Nothing paid is needed", lead=0.13)
        mark = a1_no(-2.3, -2.35, r=0.34)
        n_l = a1_lab("nothing paid", -0.2, -2.35, 38)
        self.play(Create(mark), FadeIn(n_l), run_time=0.45)
        until(self, "earns credit", lead=0.73)
        n2 = a1_lab("no credit for paid tools", -0.2, -2.9, 32)
        self.play(FadeIn(n2), run_time=0.3)
        done(self)


# ── B12 · provenance: you build the geometry; downloaded or AI-generated meshes do not count ───────────────────────────
class B12_Provenance(Scene):
    def construct(self):
        # crate at the same size as B01 (2.35): at 3.3 its top band read as a low-contrast "text" blob under the real 4K GATE T
        CH, CX, CY = 2.35, -3.6, 0.6
        cum = [a1_img(f"a1_ccum_{i}.png", h=CH, at=(CX, CY)) for i in range(1, 6)]
        self.add(cum[0])
        offs = [None, (0.0, -0.8), (0.0, 0.7), (-1.0, 0.0), (1.0, 0.15)]
        until(self, "You build", lead=0.19)
        shown = cum[0]
        for i in range(1, 5):
            part = a1_img(f"a1_cpart_{i + 1}.png", h=CH, at=(CX, CY)).shift(np.array([offs[i][0], offs[i][1], 0.0]))
            self.play(FadeIn(part), run_time=0.15)
            self.play(part.animate.shift(np.array([-offs[i][0], -offs[i][1], 0.0])), run_time=0.4)
            self.add(cum[i]); self.remove(part, shown)
            shown = cum[i]
        joined = a1_img("a1_crate_colour.png", h=CH, at=(CX, CY))    # the finished asset: five shapes joined into one object
        self.add(joined); self.remove(shown)                           # same picture, one outline: an invisible swap
        until(self, "with Claude", lead=0.86)
        y_l = a1_lab("you build it", CX, -1.3, 36)
        y_s = a1_lab("from basic shapes", CX, -1.9, 32)      # true of THIS crate (script route); the rule itself is spoken
        ok = check(-1.95, 1.55, s=0.3, color=INK, w=8)
        self.play(FadeIn(y_l), FadeIn(y_s), Create(ok), run_time=0.45)
        until(self, "A downloaded", lead=0.59)
        tray = VGroup(Line([0.85, 0.8, 0], [0.85, 0.45, 0], color=INK, stroke_width=7),
                      Line([0.85, 0.45, 0], [1.95, 0.45, 0], color=INK, stroke_width=7),
                      Line([1.95, 0.45, 0], [1.95, 0.8, 0], color=INK, stroke_width=7))
        down = Arrow([1.4, 1.9, 0], [1.4, 0.65, 0], buff=0, color=INK, stroke_width=8, tip_length=0.3)
        d_l = VGroup(a1_lab("downloaded", 4.0, 1.45, 36), a1_lab("3D model", 4.0, 0.9, 36))
        self.play(Create(tray), GrowArrow(down), FadeIn(d_l), run_time=0.45)
        until(self, "generated mesh", lead=0.74)
        star = Star(n=4, outer_radius=0.5, inner_radius=0.17, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK,
                    stroke_width=5).move_to([1.3, -1.1, 0])
        star2 = Star(n=4, outer_radius=0.24, inner_radius=0.09, fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK,
                     stroke_width=4).move_to([1.85, -0.55, 0])
        a_l = a1_lab("AI-generated mesh", 4.3, -1.0, 36)
        self.play(GrowFromCenter(star), GrowFromCenter(star2), FadeIn(a_l), run_time=0.45)
        until(self, "doesn't count", lead=0.66)
        n1 = a1_no(1.4, 1.2, r=0.8, sw=9)
        n2 = a1_no(1.45, -0.95, r=0.8, sw=9)
        self.play(Create(n1), Create(n2), run_time=0.5)
        done(self)


# ── B13 · the add-on's model fetchers and generators: leave every one off ─────────────────────────────────────────────
A1_SERV = [("Poly Haven", 1.75), ("Sketchfab", 1.15), ("Poly Pizza", 0.55), ("Hyper3D Rodin", -1.1), ("Hunyuan3D", -1.7), ("Tripo", -2.3)]


class B13_ServicesOff(Scene):
    def construct(self):
        until(self, "fetch three-D models", lead=0.42)
        h1 = T("fetch 3D models", 36).move_to([-5.6, 2.6, 0], aligned_edge=LEFT)
        rows, toggles = [], []
        for name, y in A1_SERV:
            rows.append(T(name, 34).move_to([-5.6, y, 0], aligned_edge=LEFT))
            toggles.append(a1_toggle(-0.65, y))
        self.play(FadeIn(h1), *[FadeIn(r) for r in rows[:3]], *[FadeIn(t) for t in toggles[:3]], run_time=0.5)
        until(self, "ask A. I. services", lead=1.03)
        h2 = T("generate 3D models", 36).move_to([-5.6, -0.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(h2), *[FadeIn(r) for r in rows[3:]], *[FadeIn(t) for t in toggles[3:]], run_time=0.5)
        until(self, "Leave every one", lead=0.22)
        ring = RoundedRectangle(width=1.35, height=4.85, corner_radius=0.25, fill_opacity=0, stroke_color=INK,
                                stroke_width=5).move_to([-0.65, -0.27, 0])
        off_l = a1_lab("all off", -0.65, 2.6, 36)
        self.play(Create(ring), FadeIn(off_l), run_time=0.45)
        until(self, "They call remote", lead=0.51)
        cloud = a1_cloud(3.6, 0.55, 1.15)
        c_l = a1_lab("remote services", 3.75, -1.15, 36)
        links = VGroup(*[DashedLine([0.05, y, 0], [2.05, 0.35, 0], color=DIM, stroke_width=4, dash_length=0.14) for _, y in A1_SERV])
        self.play(FadeIn(cloud), Create(links), FadeIn(c_l), run_time=0.6)
        until(self, "cost money", lead=0.94)
        m_l = a1_lab("some may cost money", 3.75, -1.85, 34)
        spark = Dot([1.6, -1.85, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(m_l), FadeIn(spark, scale=0.5), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Learn the Window First  (B15–B20, all Manim)

One cast for the act: ONE real Blender 5.1.2 window with the lantern selected (Blender's own screenshot operator, run by a
script: pantry/ev_bl_object_mode.png and the Act II captures pantry/a2_bl_*, all the same 3456 x 2006 layout; part boxes from
evidence/gui/NOTES.md), seen through a fixed viewer frame on the cream stage (x -2.95..6.3, y -3.5..3.5). The sidebar is
closed until B18, where "Press N" opens it (two real windows, before and after). The camera moves INSIDE the frame: four cream
masks hide the rest of the capture, so the screenshot is cropped and zoomed, never shrunk (s = 4K pixels per screenshot
pixel; every held view is s >= 1.25, which puts Blender's 33-px capitals at >= 41 px, the GATE T floor). One terracotta ring
marks the part the sentence names; labels sit on the cream column to the left; six step dots count the six parts. Nothing is
drawn on a Blender screen except that ring and a spark. Camera numbers were chosen so every MIDPOINT frame passes GATE T
(see evidence/act2/qa/check_midpoints.sh: Blender's small dark UI shapes are read as text runs at some zooms). Cue times are
faster-whisper word times of the measured audio (evidence/act2/word_times.json), rescaled if a beat is re-voiced.
"""

# ── viewer frame (scene units) and the screenshot grid ──────────────────────────────────────────────────────────────
A2_WX0, A2_WY0, A2_WX1, A2_WY1 = -2.95, -3.5, 6.3, 3.5
A2_WCX, A2_WCY = (A2_WX0 + A2_WX1) / 2.0, (A2_WY0 + A2_WY1) / 2.0
A2_WW, A2_WH = A2_WX1 - A2_WX0, A2_WY1 - A2_WY0
A2_IW, A2_IH = 3456.0, 2006.0                      # every Blender window capture used here
A2_PX = 270.0                                       # 4K pixels per scene unit (3840 / 14.222)
A2_LX = -6.2                                        # left edge of the label column

# the captures (real windows; see evidence/gui/NOTES.md and evidence/act2/)
A2_IMG = {
    "object": "pantry/ev_bl_object_mode.png",        # the finished lantern, selected, sidebar open
    "closed": "pantry/a2_bl_sidebar_closed.png",     # the same window with the sidebar hidden (Act II capture)
    "orbit1": "pantry/a2_bl_orbit1_closed.png",      # front view, sidebar closed (= ev_bl_orbit_1.png minus the sidebar)
    "orbit3": "pantry/a2_bl_orbit3_closed.png",      # top view, sidebar closed
    "orbit4": "pantry/a2_bl_orbit4_closed.png",      # three-quarter, zoomed in, sidebar closed
    "parts_c": "pantry/a2_bl_parts_closed.png",      # the five-object lantern, sidebar closed (Act II capture)
    "ledit":   "pantry/a2_bl_lantern_edit_closed.png",  # the lantern in EDIT Mode, roof selected, sidebar closed (Act II capture)
}

# camera states: (cx, cy) = screenshot pixel at the frame centre, s = 4K px per screenshot px
A2_CAM = {
    "V":     (999.0, 956.0, 1.25),      # the free viewport + toolbar (B16, B17)
    "O":     (2675.0, 640.0, 1.6),      # the Outliner
    "O2":    (2900.0, 560.0, 2.0),      # the Outliner, closer (the tree)
    "P":     (2624.0, 1376.0, 1.5),     # the Properties editor
    "S":     (2026.5, 760.0, 1.6),      # the sidebar (N): Transform, Location, Rotation (the navigation gizmo just out of view)
    "S4":    (2026.5, 1415.0, 1.6),     # the sidebar, lower: Scale, Dimensions
    "M":     (960.0, 797.0, 1.3),       # the header + the lantern (mode selector)
}

# part boxes in screenshot pixels (x0, y0, x1, y1), from evidence/gui/NOTES.md (rings sit just inside or round them)
A2_BOX = {
    "viewport":   (244, 228, 1940, 1690),     # the 3D viewport's free area (sidebar closed), as far as the frame shows it
    "toolbar":    (22, 236, 250, 1568),       # the toolbar's icon strip
    "outliner":   (2462, 122, 3430, 924),
    "properties": (2462, 962, 3430, 1896),
    "sidebar":    (1316, 240, 2440, 1100),    # the sidebar's top: tab strip + Transform, Location, Rotation (the part camera S frames)
    "location":   (1366, 352, 2312, 684),
    "rotation":   (1366, 690, 2312, 1104),
    "scale":      (1366, 1096, 2312, 1418),
    "dimensions": (1366, 1430, 2312, 1756),
    "header":     (24, 112, 1900, 206),
    "selector":   (178, 110, 628, 206),
    "roof":       (486, 538, 1006, 860),      # the lantern's roof: 12 selected faces and their points (Edit Mode)
    "lantern":    (492, 538, 1038, 1430),
}

# measured audio length when the cue times were taken (cues are rescaled if a beat is re-voiced)
A2_DUR = {"B15": 8.81, "B16": 7.04, "B17": 7.91, "B18": 10.11, "B19": 9.32, "B20": 6.44}


def a2_at(self, t):
    """Wait until t seconds into the beat (a faster-whisper word time, rescaled to the current audio)."""
    bid = type(self).__name__.split("_")[0]
    tgt = _TARGET.get(bid, 0)
    if not tgt:
        return
    gap = t * tgt / A2_DUR.get(bid, tgt) - _elapsed(self)
    if gap > 0.02:
        self.wait(gap)


def a2_view(cam):
    """Clamp a camera so the frame never shows past the screenshot's edges. Returns (cx, cy, u) with u = scene units per px."""
    cx, cy, s = cam
    u = s / A2_PX
    vw, vh = A2_WW / u, A2_WH / u
    cx = min(max(cx, vw / 2.0), A2_IW - vw / 2.0)
    cy = min(max(cy, vh / 2.0), A2_IH - vh / 2.0)
    return cx, cy, u


def a2_pt(cam, x, y):
    """A screenshot pixel -> its scene point under camera cam."""
    cx, cy, u = a2_view(cam)
    return np.array([A2_WCX + (x - cx) * u, A2_WCY - (y - cy) * u, 0.0])


def a2_place(cam):
    """(height, centre offset from the frame centre) of a full screenshot under camera cam."""
    cx, cy, u = a2_view(cam)
    return A2_IH * u, np.array([(A2_IW / 2.0 - cx) * u, -(A2_IH / 2.0 - cy) * u, 0.0])


def a2_img(key, cam):
    """A real capture under camera cam (positioned by a shift from the frame centre)."""
    h, off = a2_place(cam)
    im = ImageMobject(A2_IMG[key]).set_height(h)
    im.move_to([A2_WCX, A2_WCY, 0])
    im.shift(off)
    im.set_z_index(0)
    return im


def a2_cam_anims(imgs, cam):
    """Camera move: every capture layer goes to camera cam (same similarity transform for all)."""
    h, off = a2_place(cam)
    c = np.array([A2_WCX, A2_WCY, 0.0]) + off
    return [im.animate.set_height(h).move_to(c) for im in imgs]


def a2_ring(cam, part, sw=8):
    """The one terracotta ring: a closed rounded rectangle round a part, thick stroke, no fill."""
    x0, y0, x1, y1 = A2_BOX[part]
    cx, cy, u = a2_view(cam)
    r = RoundedRectangle(width=(x1 - x0) * u, height=(y1 - y0) * u, corner_radius=0.16, stroke_color=TERRA,
                         stroke_width=sw, fill_opacity=0)
    r.move_to(a2_pt(cam, (x0 + x1) / 2.0, (y0 + y1) / 2.0))
    r.set_z_index(2)
    return r


def a2_stage(self):
    """Four cream masks round the viewer frame (they crop the capture) and its ink outline."""
    m_l = Rectangle(width=A2_WX0 + 7.111 + 0.02, height=8.2, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(LEFT, buff=0)
    m_r = Rectangle(width=7.111 - A2_WX1 + 0.02, height=8.2, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(RIGHT, buff=0)
    m_t = Rectangle(width=14.4, height=4.0 - A2_WY1 + 0.02, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(UP, buff=0)
    m_b = Rectangle(width=14.4, height=4.0 + A2_WY0 + 0.02, fill_color=STAGE, fill_opacity=1, stroke_width=0).to_edge(DOWN, buff=0)
    masks = VGroup(m_l, m_r, m_t, m_b).set_z_index(5)
    frame = Rectangle(width=A2_WW, height=A2_WH, stroke_color=INK, stroke_width=4, fill_opacity=0)
    frame.move_to([A2_WCX, A2_WCY, 0]).set_z_index(6)
    self.add(masks, frame)
    return masks, frame


def a2_lab(s, y, size=40, x=A2_LX):
    """A label on the cream column, left-aligned at x."""
    return T(s, size).move_to([x, y, 0], aligned_edge=LEFT).set_z_index(7)


def a2_rlab(s, y, size=36, x=-3.45):
    """A label right-aligned at x (beside the frame's left edge, level with what it names)."""
    return T(s, size).move_to([x, y, 0], aligned_edge=RIGHT).set_z_index(7)


A2_TY = -3.0                                       # the six step dots
A2_TX = [-6.05 + 0.42 * i for i in range(6)]


def a2_dots():
    return VGroup(*[Circle(radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, A2_TY, 0])
                    for x in A2_TX]).set_z_index(7)


def a2_fill(i):
    return Dot([A2_TX[i], A2_TY, 0], radius=0.12, color=INK).set_z_index(8)


def a2_tracker(self, n):
    """Six step dots with the first n already filled (continuity from the previous beat)."""
    d = a2_dots()
    f = [a2_fill(i) for i in range(n)]
    self.add(d, *f)
    return d, f


A2_PARTY = -2.3                                    # the part-name label sits just above the dots


# ── B15 marks: orbit, pan, zoom (drawn ideas of the three gestures, ink, beside their words) ──────────────────────────
def a2_orbit_mark(x, y):
    a = Arc(radius=0.27, start_angle=PI * 0.8, angle=-PI * 1.55, stroke_color=INK, stroke_width=6).move_arc_center_to([x, y, 0])
    a.add_tip(tip_length=0.16, tip_width=0.16)
    return VGroup(a, Dot([x, y, 0], radius=0.06, color=INK)).set_z_index(7)


def a2_pan_mark(x, y):
    arms = VGroup(*[Arrow([x, y, 0], [x + 0.32 * dx, y + 0.32 * dy, 0], buff=0, stroke_width=6, color=INK, tip_length=0.13,
                          max_tip_length_to_length_ratio=0.5) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))])
    return arms.set_z_index(7)


def a2_zoom_mark(x, y):
    lens = Circle(radius=0.2, stroke_color=INK, stroke_width=6).move_to([x - 0.06, y + 0.06, 0])
    handle = Line([x + 0.09, y - 0.09, 0], [x + 0.3, y - 0.3, 0], color=INK, stroke_width=8)
    plus = VGroup(Line([x - 0.15, y + 0.06, 0], [x + 0.03, y + 0.06, 0], color=INK, stroke_width=5),
                  Line([x - 0.06, y - 0.03, 0], [x - 0.06, y + 0.15, 0], color=INK, stroke_width=5))
    return VGroup(lens, handle, plus).set_z_index(7)


# ── B15 · open Blender and just look: orbit, pan, zoom (carries the act title) ────────────────────────────────────────
class B15_LookFirst(Scene):
    def construct(self):
        a2_stage(self)
        cam = A2_CAM["V"]
        t1 = a2_lab("Learn the", 2.85)
        t2 = a2_lab("Window First", 2.25)
        icon = ImageMobject("pantry/ev_icon_blender.png").set_height(1.9).move_to([A2_WCX, A2_WCY, 0]).set_z_index(1)
        self.add(t1, t2, icon)
        a2_at(self, 1.55)                                            # "open Blender"
        img = a2_img("orbit1", cam)
        self.play(FadeOut(icon), FadeIn(img), run_time=0.5)
        a2_at(self, 3.45)                                            # "Orbit": a real second viewpoint
        img2 = a2_img("closed", cam)
        m1, l1 = a2_orbit_mark(-5.85, 0.95), a2_lab("orbit", 0.95, 36, -5.15)
        self.play(FadeIn(img2), Create(m1), FadeIn(l1), run_time=0.45)
        self.remove(img)
        a2_at(self, 3.9)                                             # "pan"
        m2, l2 = a2_pan_mark(-5.85, -0.15), a2_lab("pan", -0.15, 36, -5.15)
        self.play(Create(m2), FadeIn(l2), run_time=0.35)
        a2_at(self, 4.5)                                             # "and zoom" (just after the clip's midpoint)
        img3 = a2_img("orbit4", cam)
        m3, l3 = a2_zoom_mark(-5.85, -1.25), a2_lab("zoom", -1.25, 36, -5.15)
        self.play(FadeIn(img3), Create(m3), FadeIn(l3), run_time=0.45)
        self.remove(img2)
        a2_at(self, 5.75)                                            # "spend a short session"
        img4 = a2_img("orbit3", cam)
        self.play(FadeIn(img4), run_time=0.5)
        self.remove(img3)
        a2_at(self, 6.95)                                            # "with no prompting at all"
        img5 = a2_img("closed", cam)
        self.play(FadeIn(img5), run_time=0.5)
        self.remove(img4)
        done(self)


# ── B16 · six parts; the first: the 3D viewport ───────────────────────────────────────────────────────────────────────
class B16_Viewport(Scene):
    def construct(self):
        a2_stage(self)
        img = a2_img("closed", A2_CAM["V"])
        self.add(img)
        a2_at(self, 0.95)                                            # "name six parts"
        dots = a2_dots()
        six = a2_lab("six parts", A2_PARTY)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), FadeIn(six), run_time=0.8)
        a2_at(self, 2.7)                                             # "First, the 3D viewport"
        name = a2_lab("3D viewport", A2_PARTY)
        self.play(FadeOut(six), FadeIn(name), GrowFromCenter(a2_fill(0)), run_time=0.45)
        a2_at(self, 3.62)                                            # ring on "viewport" (after the midpoint: a ring round
        ring = a2_ring(A2_CAM["V"], "viewport")                      # viewport pixels must not be in GATE T's frame)
        self.play(Create(ring), run_time=0.5)
        a2_at(self, 4.9)                                             # "where your three-D model lives"
        self.play(Transform(ring, a2_ring(A2_CAM["V"], "lantern")), run_time=0.6)
        done(self)


# ── B17 · the toolbar (move, rotate, scale); the Outliner (every object, as a tree) ────────────────────────────────────
class B17_ToolbarOutliner(Scene):
    def construct(self):
        a2_stage(self)
        img = a2_img("closed", A2_CAM["V"])
        ring = a2_ring(A2_CAM["V"], "lantern")
        name = a2_lab("3D viewport", A2_PARTY)
        self.add(img, ring, name)
        dots, fills = a2_tracker(self, 1)
        # "The toolbar"
        n2 = a2_lab("toolbar", A2_PARTY)
        self.play(Transform(ring, a2_ring(A2_CAM["V"], "toolbar")), FadeOut(name), FadeIn(n2), GrowFromCenter(a2_fill(1)),
                  run_time=0.45)
        tools = []
        for word, t, ys in (("move", 1.65, 612), ("rotate", 2.15, 750), ("scale", 2.8, 891)):
            a2_at(self, t)
            lab = a2_rlab(word, a2_pt(A2_CAM["V"], 0, ys)[1])
            tools.append(lab)
            self.play(FadeIn(lab, shift=RIGHT * 0.15), run_time=0.3)
        a2_at(self, 4.15)                                            # "The Outliner"
        n3 = a2_lab("Outliner", A2_PARTY)
        self.play(*a2_cam_anims([img], A2_CAM["O"]), Transform(ring, a2_ring(A2_CAM["O"], "outliner")),
                  FadeOut(VGroup(*tools)), FadeOut(n2), FadeIn(n3), GrowFromCenter(a2_fill(2)), run_time=0.7)
        a2_at(self, 5.0)                                             # "lists every object": the same scene before its parts were joined
        img3 = a2_img("parts_c", A2_CAM["O"])
        self.play(FadeIn(img3), run_time=0.5)
        self.remove(img)
        a2_at(self, 6.3)                                             # "in the scene, as a tree"
        self.play(*a2_cam_anims([img3], A2_CAM["O2"]), Transform(ring, a2_ring(A2_CAM["O2"], "outliner")), run_time=0.6)
        done(self)


# ── B18 · the Properties editor; press N, the sidebar opens: location, rotation, scale, dimensions ─────────────────────
def a2_key(x, y, s=0.9):
    """A keyboard key with its letter (the N key): an ink-outlined cap on a grey base."""
    base = RoundedRectangle(width=s, height=s, corner_radius=0.14, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y - 0.1, 0])
    cap = RoundedRectangle(width=s, height=s, corner_radius=0.14, fill_color=CARD, fill_opacity=1, stroke_color=INK,
                           stroke_width=5).move_to([x, y, 0])
    letter = T("N", 44).move_to([x, y, 0])
    return base.set_z_index(7), VGroup(cap, letter).set_z_index(8)


class B18_PropertiesSidebar(Scene):
    def construct(self):
        a2_stage(self)
        img = a2_img("closed", A2_CAM["P"])
        self.add(img)
        dots, fills = a2_tracker(self, 3)
        # "The Properties editor"
        ring = a2_ring(A2_CAM["P"], "properties")
        n1 = VGroup(a2_lab("Properties", A2_PARTY + 0.55), a2_lab("editor", A2_PARTY))
        self.play(Create(ring), FadeIn(n1), GrowFromCenter(a2_fill(3)), run_time=0.45)
        a2_at(self, 3.15)                                            # "Press N"
        base, key = a2_key(-4.75, 0.6)
        self.play(FadeIn(base), FadeIn(key), FadeOut(ring), run_time=0.2)
        self.play(key.animate.shift(DOWN * 0.1), run_time=0.12)      # the key goes down on "N"
        self.play(key.animate.shift(UP * 0.1), run_time=0.12)
        self.play(*a2_cam_anims([img], A2_CAM["S"]), run_time=0.4)   # to where the sidebar opens
        a2_at(self, 3.95)                                            # "and the sidebar opens"
        img2 = a2_img("object", A2_CAM["S"])
        self.play(FadeIn(img2), run_time=0.4)
        self.remove(img)
        ring = a2_ring(A2_CAM["S"], "sidebar")
        n2 = a2_lab("sidebar", A2_PARTY)
        self.play(Create(ring), FadeOut(n1), FadeIn(n2), GrowFromCenter(a2_fill(4)), run_time=0.45)
        a2_at(self, 6.25)                                            # "location"
        self.play(Transform(ring, a2_ring(A2_CAM["S"], "location")), run_time=0.3)
        a2_at(self, 7.35)                                            # "rotation"
        self.play(Transform(ring, a2_ring(A2_CAM["S"], "rotation")), run_time=0.3)
        a2_at(self, 8.1)                                             # "scale": the camera follows down the panel
        self.play(*a2_cam_anims([img2], A2_CAM["S4"]), Transform(ring, a2_ring(A2_CAM["S4"], "scale")), run_time=0.35)
        a2_at(self, 8.65)                                            # "and dimensions"
        self.play(Transform(ring, a2_ring(A2_CAM["S4"], "dimensions")), run_time=0.3)
        done(self)


# ── B19 · the mode selector: Object Mode (whole objects) and Edit Mode (points and faces) ─────────────────────────────
class B19_ModeSelector(Scene):
    def construct(self):
        a2_stage(self)
        cam = A2_CAM["M"]
        img = a2_img("closed", cam)
        self.add(img)
        dots, fills = a2_tracker(self, 5)
        a2_at(self, 0.2)                                             # "in the viewport's header"
        ring = a2_ring(cam, "header")
        self.play(Create(ring), run_time=0.45)
        a2_at(self, 1.1)                                             # "the mode selector"
        name = a2_lab("mode selector", A2_PARTY)
        self.play(Transform(ring, a2_ring(cam, "selector")), FadeIn(name), GrowFromCenter(a2_fill(5)), run_time=0.45)
        a2_at(self, 3.7)                                             # "where you work on whole objects"
        spark = Dot(a2_pt(cam, 1095, 985), radius=0.13, color=TERRA).set_z_index(3)
        self.play(FadeOut(ring), GrowFromCenter(spark), run_time=0.45)
        a2_at(self, 5.2)                                             # "and Edit Mode"
        img2 = a2_img("ledit", cam)
        ring = a2_ring(cam, "selector")
        self.play(FadeIn(img2), FadeOut(spark), Create(ring), run_time=0.5)
        self.remove(img)
        a2_at(self, 6.95)                                            # "the points and faces of one"
        self.play(Transform(ring, a2_ring(cam, "roof")), run_time=0.5)
        done(self)


# ── B20 · one screenshot of your own session, object selected, into a notes file (a TEMPLATE, nothing typed) ───────
A2_HEADS = [("3D viewport", 0), ("Toolbar", 0), ("Outliner", 0), ("Properties editor", 1), ("Sidebar (N)", 1), ("Mode selector", 1)]
A2_SLOT = (2.75, -2.35, 3.2)                       # the notes file's screenshot slot: centre x, y, width


class B20_NotesFile(Scene):
    def construct(self):
        masks, frame = a2_stage(self)
        cam = A2_CAM["V"]
        img = a2_img("closed", cam)                                  # the act's window, the lantern selected
        self.add(img)
        dots, fills = a2_tracker(self, 6)
        lab = a2_lab("screenshot", A2_PARTY)
        self.add(lab)
        flash = Rectangle(width=A2_WW, height=A2_WH, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([A2_WCX, A2_WCY, 0]).set_z_index(3)
        a2_at(self, 0.2)                                             # "one screenshot": a shutter flash on the window
        self.add(flash)
        self.play(FadeOut(flash), run_time=0.5)
        a2_at(self, 1.95)                                            # "with an object selected": a spark beside the selected lantern
        spark = Dot(a2_pt(cam, 1095, 985), radius=0.13, color=TERRA).set_z_index(3)
        self.play(GrowFromCenter(spark), run_time=0.4)
        # the notes file (a template: six headings = the six parts; nothing typed in a session)
        card = Rectangle(width=A2_WW, height=A2_WH, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([A2_WCX, A2_WCY, 0]).set_z_index(3)
        fname = M("BLENDER-NOTES.md", 32).move_to([A2_WX0 + 0.35, 3.0, 0], aligned_edge=LEFT).set_z_index(7)
        tag = T("template", 32).move_to([A2_WX1 - 0.35, 3.0, 0], aligned_edge=RIGHT).set_z_index(7)
        rule = Line([A2_WX0 + 0.3, 2.55, 0], [A2_WX1 - 0.3, 2.55, 0], color=GHOST, stroke_width=4).set_z_index(4)
        heads, ghosts = VGroup(), VGroup()
        for i, (h, col) in enumerate(A2_HEADS):
            hx = A2_WX0 + 0.35 + col * 3.8
            hy = 1.85 - (i % 3) * 1.1
            heads.add(T(h, 32, bold=True).move_to([hx, hy, 0], aligned_edge=LEFT))
            ghosts.add(Line([hx, hy - 0.45, 0], [hx + 2.6, hy - 0.45, 0], color=GHOST, stroke_width=10))
        heads.set_z_index(7); ghosts.set_z_index(4)
        shot_h = T("Screenshot", 32, bold=True).move_to([A2_WX0 + 0.35, -1.55, 0], aligned_edge=LEFT).set_z_index(7)
        sx, sy, sw = A2_SLOT
        thumb = ImageMobject("pantry/a2_b20_screenshot.png").set_width(A2_WW).move_to([A2_WCX, A2_WCY, 0]).set_z_index(4)
        a2_at(self, 3.32)                                            # "to a notes file" (just after the midpoint)
        self.play(FadeIn(card), FadeIn(thumb), FadeOut(spark), FadeOut(lab), run_time=0.3)   # the window becomes one screenshot
        self.remove(img)
        tedge = Rectangle(width=sw, height=sw * A2_IH / A2_IW, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([sx, sy, 0]).set_z_index(5)
        self.play(thumb.animate.set_width(sw).move_to([sx, sy, 0]), FadeIn(fname), FadeIn(tag), FadeIn(rule), FadeIn(heads),
                  FadeIn(ghosts), FadeIn(shot_h), run_time=0.6)                       # ...and is filed in the notes
        self.play(Create(tedge), FadeIn(a2_lab("notes file", A2_PARTY)), run_time=0.3)
        a2_at(self, 4.6)                                             # "That's your evidence that you looked"
        ok = check(sx + sw / 2 + 0.55, sy + 0.1, 0.22).set_z_index(7)
        self.play(Create(ok), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · Write the Brief Before You Build  (B21–B28, all Manim)

One cast for the act: THE CRATE (the real crate, 0.8 x 0.8 x 0.8 m, built by evidence/assets/build_crate.py) and its ORIGIN as a
terracotta dot. Where the crate is the real thing it is the real render (pantry/a3_crate_34.png, a crop of ev_crate_34.png) or the real
Blender window (pantry/a3_bl_crate_origin.png); where the beat is about an IDEA (where the origin sits, what the floor does with it) it
is a side-view drawing of the same crate: a 0.8 m square with its bottom and top bands and its centre strap, like the render.
Every number on screen is from a real run: build_crate.log / build_lantern.log (Blender 5.1.2), evidence/godot/*.log (Godot 4.7.2).
Illustrative values (the example player, the example brief entries) say "example" on screen.
"""

A3_FRAME_W = 14.222                              # Manim frame width (units) at 16:9
A3_WOOD, A3_BAND = "#B5804D", "#7E5530"          # the crate's two materials: wood browns toward the real render (CrateWood/CrateBand);
                                                 # the pale kraft tones failed Gate V contrast (B25A 0.29 < 0.30, 4K review cut 2026-10-06)
A3_S = 3.0                                       # side views of the origin story: scene units per metre
A3_F = -0.2                                      # ... and the floor's y
A3_XL, A3_XR = -3.4, 3.0                         # ... and the two crates' centres

# real crate render crop (pantry/a3_crate_34.png = ev_crate_34.png cropped at 600,150 -> 1180 x 1160 px); corners projected from
# the render camera (evidence/act3/make_crops.log): x- y- z0, x+ y- z0 (nearest), x+ y+ z0, x+ y+ z0.8, x+ y- z0.8
A3_CRATE_PX = (1180, 1160)
A3_C_LB, A3_C_FB, A3_C_RB = (92.5, 896.4), (701.3, 1122.5), (1083.5, 814.9)
A3_C_RT, A3_C_FT = (1124.4, 141.3), (711.6, 340.7)

# the crate render's silhouette ON its edge (alpha > 10, not dilated; evidence/act3/make_crops.py). B22 draws it in ink over the render's own
# dark Workbench outline: GATE T read those edge pixels (they fall inside its MUTE tolerance after encoding) as text-like blobs (4K cut, 2026-10-06)
A3_CRATE_OUTLINE = [[702.0, 1122.5], [90.5, 895.0], [85.5, 814.0], [110.5, 800.0], [109.5, 772.0], [80.5, 298.0], [51.5, 287.0], [45.5, 205.0],
                    [48.0, 190.5], [514.0, 36.5], [1124.5, 140.0], [1119.5, 232.0], [1095.0, 244.5], [1092.5, 254.0], [1065.5, 722.0],
                    [1066.0, 728.5], [1088.5, 736.0], [1084.5, 815.0]]

# real lantern render crop (pantry/a3_lantern_34.png = ev_lantern_34.png cropped at 970,295 -> 461 x 825 px) and its silhouette
# (alpha > 10, dilated 14 px, simplified; evidence/act3/make_crops.py)
A3_LANTERN_PX = (461, 825)
A3_LANTERN_OUTLINE = [[236.0, 819.5], [191.0, 819.5], [91.0, 801.5], [20.5, 759.0], [6.5, 707.0], [5.5, 630.0], [48.0, 584.5],
                      [73.5, 575.0], [69.5, 334.0], [99.0, 306.5], [131.5, 297.0], [87.0, 287.5], [24.0, 260.5], [9.5, 225.0],
                      [9.5, 194.0], [184.0, 77.5], [184.5, 16.0], [208.0, 5.5], [273.0, 12.5], [274.5, 77.0], [427.0, 171.5],
                      [451.5, 206.0], [451.5, 236.0], [419.0, 270.5], [327.5, 296.0], [372.0, 314.5], [389.5, 342.0], [386.5, 577.0],
                      [429.0, 597.5], [454.5, 645.0], [453.5, 726.0], [416.0, 777.5], [337.0, 810.5]]


def a3_px(cx, cy, k, size, px, py):
    """Scene point of pixel (px, py) of an image of `size` (w, h) px shown at scale k units/px, centred on (cx, cy)."""
    return np.array([cx + (px - size[0] / 2) * k, cy - (py - size[1] / 2) * k, 0.0])


def a3_crate_side(cx, base_y, s=A3_S):
    """The crate in side view: a 0.8 m square, bottom and top bands 0.1 m, a 0.1 m centre strap (the real crate's pattern)."""
    w = 0.8 * s
    body = Rectangle(width=w, height=w, fill_color=A3_WOOD, fill_opacity=1, stroke_width=0).move_to([cx, base_y + w / 2, 0])
    bot = Rectangle(width=w, height=0.1 * s, fill_color=A3_BAND, fill_opacity=1, stroke_width=0).move_to([cx, base_y + 0.05 * s, 0])
    top = Rectangle(width=w, height=0.1 * s, fill_color=A3_BAND, fill_opacity=1, stroke_width=0).move_to([cx, base_y + 0.75 * s, 0])
    strap = Rectangle(width=0.1 * s, height=w, fill_color=A3_BAND, fill_opacity=1, stroke_width=0).move_to([cx, base_y + w / 2, 0])
    edge = Rectangle(width=w, height=w, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([cx, base_y + w / 2, 0])
    return VGroup(body, bot, top, strap, edge)


def a3_dot(x, y, r=0.13):
    return Dot([x, y, 0], radius=r, color=TERRA).set_z_index(6)


def a3_floor(x0=-6.1, x1=6.1, y=A3_F):
    return Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=8).set_z_index(4)


def a3_page(x, y, w=1.6, h=1.9, fill=CARD, stroke=INK):
    """A document: a sheet with a folded top-right corner (no lines on it)."""
    f = 0.42
    sheet = Polygon([x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2 - f, 0], [x + w / 2 - f, y + h / 2, 0],
                    [x - w / 2, y + h / 2, 0], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=4)
    fold = Polygon([x + w / 2 - f, y + h / 2, 0], [x + w / 2 - f, y + h / 2 - f, 0], [x + w / 2, y + h / 2 - f, 0],
                   fill_color=GHOST, fill_opacity=1, stroke_color=stroke, stroke_width=3)
    return VGroup(sheet, fold)


def a3_no(x, y, r=0.42):
    """A 'not this' mark: an ink ring with a bar."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=8).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=8)
    return VGroup(ring, bar)


def a3_left(mob, x, y):
    """Place a text so its LEFT edge sits at x (explicit numbers: Gate A's stub cannot measure text)."""
    return mob.move_to([x + mob.width / 2, y, 0])


# ── B21 · the brief, committed before anything is built; revisions added, the original kept ─────────────────────────────
class B21_BriefFirst(Scene):
    def construct(self):
        title = T("Write the Brief Before You Build", 40).move_to([-2.6, 3.0, 0])
        line = Line([-5.7, -1.45, 0], [5.7, -1.45, 0], color=DIM, stroke_width=6)
        self.add(title, line)
        until(self, "Before you ask Claude", lead=0.1)
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(2.1).move_to([0.0, -0.05, 0])
        crate.set_opacity(0.3)
        c2 = Dot([0.0, -1.45, 0], radius=0.14, color=GHOST).set_z_index(3)
        l2 = T("build", 36).move_to([0.0, -2.05, 0])
        self.play(FadeIn(crate), FadeIn(c2), FadeIn(l2), run_time=0.5)
        until(self, "commit a file", lead=0.2)
        p1 = a3_page(-3.8, 0.1)
        p1.shift(UP * 1.2)
        c1 = Dot([-3.8, -1.45, 0], radius=0.14, color=INK).set_z_index(3)
        self.play(p1.animate.shift(DOWN * 1.2), FadeIn(c1), rate_func=ease_in, run_time=0.55)
        l1 = M("CHANGE-BRIEF.md", 32).move_to([-3.8, -2.05, 0])
        self.play(FadeIn(l1), run_time=0.3)
        until(self, "Keep the original", lead=0.15)
        orig = T("original", 36).move_to([-3.8, 1.55, 0])
        tick = check(-2.55, 1.6, s=0.2)
        self.play(FadeIn(orig), Create(tick), run_time=0.4)
        until(self, "Add revisions", lead=0.25)
        p2 = a3_page(3.8, 0.1)
        p2.shift(UP * 1.2)
        c3 = Dot([3.8, -1.45, 0], radius=0.14, color=INK).set_z_index(3)
        self.play(p2.animate.shift(DOWN * 1.2), FadeIn(c3), rate_func=ease_in, run_time=0.5)
        l3 = T("revision", 36).move_to([3.8, -2.05, 0])
        self.play(FadeIn(l3), run_time=0.25)
        until(self, "rewrite it", lead=0.3)
        back = CurvedArrow(np.array([2.85, 0.75, 0]), np.array([-2.75, 0.75, 0]), angle=TAU / 5, color=INK, stroke_width=5, tip_length=0.24)
        self.play(Create(back), run_time=0.6)
        until(self, "every prediction", lead=0.2)
        no = a3_no(0.0, 1.62)
        self.play(GrowFromCenter(no), run_time=0.4)
        done(self)


# ── B22 · name, what it is, where it appears (an example brief entry for the real crate) ─────────────────────────────────
class B22_NameRoleWhere(Scene):
    def construct(self):
        ch, ccx, ccy = 4.0, -3.45, -0.25
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(ch).move_to([ccx, ccy, 0])
        kc = ch / A3_CRATE_PX[1]
        edge = Polygon(*[a3_px(ccx, ccy, kc, A3_CRATE_PX, x, y) for x, y in A3_CRATE_OUTLINE], stroke_color=INK, stroke_width=6, fill_opacity=0)
        self.add(crate, edge)
        head = a3_left(M("CHANGE-BRIEF.md", 32), 0.3, 2.35)
        ex = a3_left(T("example", 32), 4.55, 2.35)
        self.play(FadeIn(head), FadeIn(ex), run_time=0.3)        # text only: the dot below is the first NEW shape (Gate A)
        # (key, key centre-above-baseline, value, value centre-above-baseline, baseline): offsets measured in Manim so the rows share a baseline
        base = [("name", 0.094, "Crate", 0.188, 1.0), ("what it is", 0.162, "a prop", 0.048, -0.1), ("where", 0.162, "the dock", 0.198, -1.2)]
        rows = [(k, v, yb + 0.12) for k, ko, v, vo, yb in base]                     # the dot sits at x-height
        keys = [a3_left(T(k, 32), 0.3, yb + ko) for k, ko, v, vo, yb in base]          # ink: DIM type risks GATE T's contrast floor
        vals = [a3_left(T(v, 40), 2.6, yb + vo) for k, ko, v, vo, yb in base]
        cue = ["its name", "what it is in your game", "where it appears"]
        mark = None
        for i in range(3):
            until(self, cue[i], lead=0.3)
            if mark is None:
                mark = a3_dot(-0.05, rows[i][2], r=0.11)
                self.play(FadeIn(keys[i]), FadeIn(vals[i]), GrowFromCenter(mark), run_time=0.3)
            else:
                self.play(FadeIn(keys[i]), FadeIn(vals[i]), mark.animate.move_to([-0.05, rows[i][2], 0]), run_time=0.3)
        done(self)


# ── B23 · size in metres, against something in the game ──────────────────────────────────────────────────────────────────
class B23_SizeInMetres(Scene):
    def construct(self):
        k, cx, cy = 0.00262, -3.0, -1.079
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(A3_CRATE_PX[1] * k).move_to([cx, cy, 0])
        self.add(crate)
        P = lambda q: a3_px(cx, cy, k, A3_CRATE_PX, *q)
        lb, fb, rb, rt = P(A3_C_LB), P(A3_C_FB), P(A3_C_RB), P(A3_C_RT)
        until(self, "width", lead=0.25)
        w_a = dim_arrow(lb + np.array([-0.12, -0.33, 0]), fb + np.array([-0.12, -0.33, 0]))
        w_l = T("0.8 m wide", 36).move_to([-4.55, -3.0, 0])
        self.play(Create(w_a), FadeIn(w_l), run_time=0.4)
        until(self, "depth", lead=0.25)
        d_a = dim_arrow(fb + np.array([0.22, -0.27, 0]), rb + np.array([0.22, -0.27, 0]))
        d_l = T("0.8 m deep", 36).move_to([-0.55, -2.8, 0])
        self.play(Create(d_a), FadeIn(d_l), run_time=0.4)
        until(self, "height.", lead=0.25)
        h_a = dim_arrow(rb + np.array([0.4, 0, 0]), rt + np.array([0.4, 0, 0]))
        h_l = T("0.8 m tall", 36).move_to([0.05, -0.8, 0])
        self.play(Create(h_a), FadeIn(h_l), run_time=0.4)
        until(self, "the player's height", lead=0.45)
        u = (P(A3_C_FB)[1] - P(A3_C_FT)[1]) / -0.8           # units per metre at the crate's nearest corner (0.8 m edge)
        feet, tall = -2.5, 1.8 * u
        body = RoundedRectangle(width=1.0, height=tall - 0.72, corner_radius=0.45, fill_color=BAR2, fill_opacity=1,
                                stroke_color=INK, stroke_width=4).move_to([2.2, feet + (tall - 0.72) / 2, 0])
        head = Circle(radius=0.33, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([2.2, feet + tall - 0.33, 0])
        self.play(FadeIn(VGroup(body, head), shift=LEFT * 0.3), run_time=0.45)
        p_a = dim_arrow([3.3, feet, 0], [3.3, feet + tall, 0])
        p_l = T("player 1.8 m", 36).move_to([4.75, 0.15, 0])
        p_x = T("example", 32).move_to([4.75, -0.5, 0])
        self.play(Create(p_a), FadeIn(p_l), FadeIn(p_x), run_time=0.4)
        done(self)


# ── B24 · Blender and Godot both count in metres: the crate's 0.8 stays 0.8 ────────────────────────────────────────────────
class B24_SameUnits(Scene):
    def construct(self):
        k = 2.0 / A3_CRATE_PX[1]
        sx = (-3.4, 3.4)
        bl = ImageMobject("pantry/ev_icon_blender.png").set_height(1.0).move_to([sx[0] - 1.15, 2.45, 0])
        bl_n = T("Blender", 40).move_to([sx[0] + 0.55, 2.45, 0])
        crate = ImageMobject("pantry/a3_crate_34.png").set_height(2.0).move_to([sx[0] - 0.3, -0.45, 0])
        self.add(bl, bl_n, crate)
        fb_y = a3_px(sx[0] - 0.3, -0.45, k, A3_CRATE_PX, *A3_C_FB)[1]
        u = (A3_C_FB[1] - A3_C_FT[1]) * k / 0.8                       # units per metre at the crate's nearest corner

        def ruler(x):
            return VGroup(Line([x, fb_y, 0], [x, fb_y + u, 0], color=INK, stroke_width=6),
                          Line([x - 0.16, fb_y, 0], [x + 0.16, fb_y, 0], color=INK, stroke_width=6),
                          Line([x - 0.16, fb_y + u, 0], [x + 0.16, fb_y + u, 0], color=INK, stroke_width=6))
        until(self, "one unit is one metre", lead=0.25)
        r1 = ruler(sx[0] + 1.6)
        u1 = T("1 unit = 1 m", 36).move_to([sx[0], 1.2, 0])
        self.play(Create(r1), FadeIn(u1), run_time=0.5)
        until(self, "And Godot's", lead=0.25)
        gd = ImageMobject("pantry/ev_icon_godot.png").set_height(1.0).move_to([sx[1] - 1.15, 2.45, 0])
        gd_n = T("Godot", 40).move_to([sx[1] + 0.45, 2.45, 0])
        self.play(FadeIn(gd), FadeIn(gd_n), run_time=0.35)
        until(self, "units are metres too", lead=0.25)
        r2 = ruler(sx[1] + 1.6)
        u2 = T("1 unit = 1 m", 36).move_to([sx[1], 1.2, 0])
        self.play(Create(r2), FadeIn(u2), run_time=0.5)
        until(self, "So if you keep it", lead=0.2)
        o1 = M("0.800 x 0.800 x 0.800", 32).move_to([sx[0], -2.35, 0])
        self.play(FadeIn(o1), run_time=0.3)
        go = Arrow([-1.0, -0.45, 0], [1.0, -0.45, 0], buff=0, color=INK, stroke_width=6, tip_length=0.24)
        self.play(Create(go), run_time=0.3)
        until(self, "nothing needs converting", lead=0.75)
        copy = crate.copy()
        self.play(copy.animate.move_to([sx[1] - 0.3, -0.45, 0]), run_time=0.7)
        o2 = M("(0.8, 0.8, 0.8) m", 32).move_to([sx[1], -2.35, 0])
        self.play(FadeIn(o2), run_time=0.3)
        done(self)


# ── B25A · the origin: the point the model is placed and rotated from; on the floor, the centre of the underside ────────────
class B25A_Origin(Scene):
    def construct(self):
        s, x0, x1, y_air, y_floor = 3.5, -2.9, -0.3, 0.0, -1.0           # centred: the crate settles just left of centre, labels to its right
        crate = a3_crate_side(x0, y_air, s)
        self.add(crate)
        until(self, "origin:", lead=0.2)
        dot = a3_dot(x0, y_air)
        lab = T("origin", 36).move_to([x0, y_air - 0.55, 0])
        self.play(GrowFromCenter(dot), FadeIn(lab), run_time=0.35)
        until(self, "placed", lead=0.55)        # leads from the whisper word times of the re-voiced mp3 (placed 2.20 s)
        self.play(VGroup(crate, dot, lab).animate.shift(RIGHT * (x1 - x0)), run_time=0.55)
        until(self, "rotated", lead=0.6)         # rotated 2.78 s
        piv = np.array([x1, y_air, 0.0])
        self.play(Rotate(VGroup(crate, dot), angle=-0.4, about_point=piv), run_time=0.4)
        self.play(Rotate(VGroup(crate, dot), angle=0.4, about_point=piv), run_time=0.4)
        until(self, "For a prop", lead=0.3)
        floor = a3_floor(-5.1, 4.5, y_floor)
        fl = T("floor", 36).move_to([3.65, y_floor + 0.38, 0])
        self.play(Create(floor), FadeIn(fl), run_time=0.35)
        self.play(VGroup(crate, dot, lab).animate.shift(DOWN * (y_air - y_floor)), rate_func=ease_in, run_time=0.45)
        until(self, "the centre of the underside", lead=0.6)    # centre 6.02 s
        w = 0.4 * s
        a_l = dim_arrow([x1 - w, -2.2, 0], [x1, -2.2, 0], tip=0.22)          # tips >= GATE T size floor
        a_r = dim_arrow([x1, -2.2, 0], [x1 + w, -2.2, 0], tip=0.22)
        h_l = T("0.4 m", 38).move_to([x1 - w / 2, -2.78, 0])
        h_r = T("0.4 m", 38).move_to([x1 + w / 2, -2.78, 0])
        cl = T("centre of the underside", 36).move_to([3.55, -2.2, 0])
        self.play(GrowFromCenter(a_l), GrowFromCenter(a_r), FadeIn(h_l), FadeIn(h_r), FadeIn(cl), run_time=0.5)
        done(self)


# ── B25B · Blender's world origin: three axes meet at a point on the floor; the crate is built with its base there ───────────
# (isometric drawing; the real-window version failed GATE T: Blender's dark viewport sits inside its INK tolerance, so any crop of it reads as text)
def a3_crate_iso(iso, w=0.8, alpha=0.62):
    """The crate in isometric, centred on (0, 0), base at z = 0: wood faces, band-coloured lid, bottom bands and a centre strap per face.
    Fills are see-through (like Blender's X-ray) so the axes and the origin show inside; edges are ink."""
    h = w
    x0, y0, x1, y1 = -w / 2, -w / 2, w / 2, w / 2
    b, t = 0.1, 0.05
    Q = lambda pts, c: iso.quad(pts, c, stroke=c, sw=0).set_fill(c, opacity=alpha)
    left = [(x0, y0, 0), (x0, y1, 0), (x0, y1, h), (x0, y0, h)]           # the x = x0 face
    right = [(x0, y0, 0), (x1, y0, 0), (x1, y0, h), (x0, y0, h)]          # the y = y0 face
    top = [(x0, y0, h), (x1, y0, h), (x1, y1, h), (x0, y1, h)]
    fills = VGroup(Q(left, A3_WOOD), Q(right, "#A06F42"), Q(top, A3_BAND),
                   Q([(x0, y0, 0), (x0, y1, 0), (x0, y1, b), (x0, y0, b)], A3_BAND),
                   Q([(x0, y0, 0), (x1, y0, 0), (x1, y0, b), (x0, y0, b)], A3_BAND),
                   Q([(x0, -t, 0), (x0, t, 0), (x0, t, h), (x0, -t, h)], A3_BAND),
                   Q([(-t, y0, 0), (t, y0, 0), (t, y0, h), (-t, y0, h)], A3_BAND))
    edges = VGroup(*[Polygon(*[iso.p(*q) for q in f], fill_opacity=0, stroke_color=INK, stroke_width=4) for f in (left, right, top)])
    fills.set_z_index(1); edges.set_z_index(3)
    return VGroup(fills, edges)


class B25B_WorldOrigin(Scene):
    def construct(self):
        iso = Iso(-1.3, -0.1, 1.6)
        L = 1.6                                                              # axis half-length, metres
        ax_x = Line(iso.p(-L, 0, 0), iso.p(L, 0, 0), color=DIM, stroke_width=6)
        ax_y = Line(iso.p(0, -L, 0), iso.p(0, L, 0), color=DIM, stroke_width=6)
        ax_z = Line(iso.p(0, 0, 0), iso.p(0, 0, L), color=DIM, stroke_width=6)
        VGroup(ax_x, ax_y, ax_z).set_z_index(2)                             # axes show through the see-through crate
        lx, ly, lz = T("X", 36).move_to(iso.p(L + 0.25, 0, 0)), T("Y", 36).move_to(iso.p(0, L + 0.25, 0)), T("Z", 36).move_to(iso.p(0, 0, L + 0.25))
        floor = Polygon(*[iso.p(x, y, 0) for x, y in ((-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0))], fill_opacity=0, stroke_color=DIM, stroke_width=3)
        self.add(floor)
        until(self, "world origin", lead=0.4)
        self.play(Create(ax_x), Create(ax_y), Create(ax_z), FadeIn(lx), FadeIn(ly), FadeIn(lz), run_time=0.7)
        until(self, "the point where", lead=0.3)
        o = iso.p(0, 0, 0)
        start = iso.p(-1.2, 0, 0)
        dot = a3_dot(start[0], start[1], r=0.14)
        key = a3_dot(2.25, 1.25, r=0.13)
        kl = a3_left(T("world origin", 36), 2.6, 1.25)
        self.play(GrowFromCenter(dot), GrowFromCenter(key), FadeIn(kl), run_time=0.3)
        self.play(MoveAlongPath(dot, Line(np.array(start), np.array(o))), run_time=0.55)
        until(self, "with the base on the floor", lead=0.3)
        crate = a3_crate_iso(iso)
        crate.shift(UP * 1.6)
        self.play(FadeIn(crate), run_time=0.15)
        self.play(crate.animate.shift(DOWN * 1.6), rate_func=ease_in, run_time=0.45)
        l1 = a3_left(M("origin at world (0.000, 0.000, 0.000)", 32), -5.6, -2.35)
        l2 = a3_left(M("lowest point z = 0.0000 m", 32), -5.6, -2.95)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(FadeIn(l2), run_time=0.3)
        done(self)


# ── B26A · origin in the middle: at floor level it sinks (-0.4 m); lifted by a guess it floats (+0.1 m) ─────────────────────
class B26A_SinkFloat(Scene):
    def construct(self):
        s = A3_S
        floor = a3_floor()
        fl = T("floor", 36).move_to([-0.2, A3_F + 0.38, 0])
        c1 = a3_crate_side(A3_XL, A3_F)
        d1 = a3_dot(A3_XL, A3_F)
        self.add(c1, floor, fl, d1)
        until(self, "in the middle", lead=0.2)
        self.play(d1.animate.move_to([A3_XL, A3_F + 0.4 * s, 0]), run_time=0.5)
        until(self, "won't sit on the floor", lead=0.95)    # whisper: "won't" 2.28 s
        self.play(VGroup(c1, d1).animate.shift(DOWN * 0.4 * s), rate_func=ease_in, run_time=0.55)
        sk = T("sinks", 36).move_to([A3_XL, -1.95, 0])
        self.play(FadeIn(sk), run_time=0.25)
        until(self, "it sinks half", lead=0.8)    # sinks 4.92 s
        g1 = M("gap to floor = -0.4 m", 32).move_to([A3_XL, -2.6, 0])
        self.play(FadeIn(g1), run_time=0.3)
        until(self, "Lift it by a guess", lead=0.75)    # lift 6.34 s
        c2 = a3_crate_side(A3_XR, A3_F - 0.4 * s)
        d2 = a3_dot(A3_XR, A3_F)
        self.play(FadeIn(c2), FadeIn(d2), run_time=0.3)
        up = Arrow([A3_XR + 1.6, A3_F, 0], [A3_XR + 1.6, A3_F + 0.5 * s, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        ul = T("+0.5 m", 34).move_to([A3_XR + 2.55, A3_F + 0.25 * s, 0])
        self.play(VGroup(c2, d2).animate.shift(UP * 0.5 * s), GrowArrow(up), FadeIn(ul), run_time=0.6)
        ft = T("floats", 36).move_to([A3_XR, -1.95, 0])
        g2 = M("gap to floor = 0.1 m", 32).move_to([A3_XR, -2.6, 0])
        self.play(FadeIn(ft), FadeIn(g2), run_time=0.3)
        done(self)


# ── B26B · lifted by exactly 0.4 m it sits and the gap check PASSES; the origin check FAILS it ─────────────────────────────
class B26B_OriginCheck(Scene):
    def construct(self):
        s = A3_S
        floor = a3_floor()
        fl = T("floor", 36).move_to([-0.2, A3_F + 0.38, 0])
        c1 = a3_crate_side(A3_XL, A3_F - 0.4 * s)
        d1 = a3_dot(A3_XL, A3_F)
        sk = T("sinks", 36).move_to([A3_XL, -1.95, 0])
        g1 = M("gap to floor = -0.4 m", 32).move_to([A3_XL, -2.6, 0])
        c2 = a3_crate_side(A3_XR, A3_F + 0.1 * s)
        d2 = a3_dot(A3_XR, A3_F + 0.5 * s)
        up = Arrow([A3_XR + 1.6, A3_F, 0], [A3_XR + 1.6, A3_F + 0.5 * s, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        ul = T("+0.5 m", 34).move_to([A3_XR + 2.55, A3_F + 0.25 * s, 0])
        ft = T("floats", 36).move_to([A3_XR, -1.95, 0])
        g2 = M("gap to floor = 0.1 m", 32).move_to([A3_XR, -2.6, 0])
        self.add(c1, c2, floor, fl, d1, d2, sk, g1, up, ul, ft, g2)
        self.play(FadeOut(VGroup(c2, d2, up, ul, ft, g2, sk, g1)), fl.animate.move_to([5.35, A3_F + 0.38, 0]), run_time=0.35)
        lift = Arrow([A3_XL + 1.6, A3_F, 0], [A3_XL + 1.6, A3_F + 0.4 * s, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        ll = T("moved 0.4 m", 34).move_to([A3_XL + 3.15, A3_F + 0.2 * s, 0])
        self.play(VGroup(c1, d1).animate.shift(UP * 0.4 * s), GrowArrow(lift), FadeIn(ll), run_time=0.7)
        until(self, "and it sits", lead=0.15)
        p1 = a3_left(M("gap to floor = 0.0 m", 32), 1.0, 2.05)
        p2 = a3_left(M("PASS", 32), 1.0, 1.35)
        pt = check(2.45, 1.4, s=0.2)
        self.play(FadeIn(p1), FadeIn(p2), Create(pt), run_time=0.4)
        until(self, "only because you moved it", lead=0.2)
        self.play(Indicate(VGroup(lift, ll), color=INK, scale_factor=1.12), run_time=0.7)
        until(self, "look at the origin", lead=0.35)
        ring = Circle(radius=0.34, stroke_color=INK, stroke_width=7).move_to([A3_XL, A3_F + 0.4 * s, 0]).set_z_index(5)
        self.play(GrowFromCenter(ring), run_time=0.35)
        f = [M("FAIL crate_origin_centre.glb:", 32), M("the origin is 0.4 m above the base:", 32),
             M("it sits on the floor only because", 32), M("the node was moved", 32)]
        for i, m in enumerate(f):
            a3_left(m, -5.75, -1.0 - 0.6 * i)
        self.play(FadeIn(VGroup(*f)), run_time=0.45)
        until(self, "not just the gap", lead=0.2)
        self.play(VGroup(p1, p2, pt).animate.set_opacity(0.3), run_time=0.45)
        done(self)


# ── B27 · look and budget: the real lantern, its real materials, its real 202 triangles ────────────────────────────────────
class B27_LookBudget(Scene):
    def construct(self):
        h, cx, cy = 5.4, -3.6, 0.0
        k = h / A3_LANTERN_PX[1]
        lan = ImageMobject("pantry/a3_lantern_34.png").set_height(h).move_to([cx, cy, 0])
        self.add(lan)
        P = lambda x, y: a3_px(cx, cy, k, A3_LANTERN_PX, x, y)
        until(self, "the shape that makes it", lead=0.25)
        outline = Polygon(*[P(x, y) for x, y in A3_LANTERN_OUTLINE], stroke_color=INK, stroke_width=5, fill_opacity=0)
        self.play(Create(outline), run_time=0.9)
        until(self, "material colours", lead=0.3)
        mats = [("DarkIron", P(400, 215), 1.29), ("Flame", P(262, 323), 0.59), ("WarmGlass", P(370, 455), -0.28)]
        leads, labs = [], []
        for name, at, y in mats:
            leads.append(Line(np.array([at[0], y, 0]), np.array([-1.45, y, 0]), color=INK, stroke_width=4))
            labs.append(a3_left(T(name, 36), -1.15, y))
        self.play(*[Create(l) for l in leads], *[FadeIn(l) for l in labs], run_time=0.5)
        until(self, "Its budget", lead=0.0)                          # starts just after the midpoint: no empty bar in the sampled frame
        x0, x5, by = 1.5, 5.9, -0.3
        bar = Rectangle(width=x5 - x0, height=0.6, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([(x0 + x5) / 2, by, 0])
        fill = Rectangle(width=0.02, height=0.6, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x0 + 0.01, by, 0])
        self.play(Create(bar), run_time=0.25)
        self.add(fill)
        wf = 202 / 500 * (x5 - x0)
        self.play(fill.animate.stretch_to_fit_width(wf).move_to([x0 + wf / 2, by, 0]), run_time=0.75)
        n = a3_left(T("202", 96), x0, 1.3)
        nl = a3_left(T("triangles", 36), x0 + 1.89 + 0.3, 1.1)        # "202" at size 96 is 1.89 wide (measured; Gate A's stub cannot measure)
        spark = a3_dot(x0 + wf, by + 0.55, r=0.11)
        self.play(FadeIn(n), FadeIn(nl), GrowFromCenter(spark), run_time=0.35)
        until(self, "at or under five hundred", lead=0.2)
        cap = T("500", 36).move_to([x5 - 0.3, by - 0.7, 0])
        sh = a3_left(T("5 shapes", 36), x0, -1.95)
        self.play(FadeIn(cap), bar.animate.set_stroke(INK, 5), run_time=0.35)
        self.play(FadeIn(sh), run_time=0.3)
        done(self)


# ── B28 · four predicted failures, each with the check that catches it (three are real runs; the server one is not run) ────
class B28_FourFailures(Scene):
    def construct(self):
        W, H = 5.9, 2.85
        cen = [(-3.05, 1.6), (3.05, 1.6), (-3.05, -1.6), (3.05, -1.6)]
        panels = [RoundedRectangle(width=W, height=H, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
                  for x, y in cen]
        # an empty slot holds only its number (ink: numerals are ink) until its failure is named; the check mark lands LAST
        nums = [a3_left(T(str(i + 1), 36), x - W / 2 + 0.35, y + H / 2 - 0.5) for i, (x, y) in enumerate(cen)]
        for i, cue in enumerate(["at least", "three", "predicted", "failures"]):
            until(self, cue, lead=0.15)
            self.play(Create(panels[i]), FadeIn(nums[i]), run_time=0.3)

        def label(i, s):                       # top-left of the panel: the predicted failure (takes the number's place)
            x, y = cen[i]
            return a3_left(T(s, 36), x - W / 2 + 0.35, y + H / 2 - 0.5)

        def line(i, mob):                      # bottom row: what the check reports
            x, y = cen[i]
            return a3_left(mob, x - W / 2 + 1.0, y - H / 2 + 0.5)

        def tick(i):                           # the check mark, beside the check's report
            x, y = cen[i]
            return check(x - W / 2 + 0.55, y - H / 2 + 0.55, s=0.19)
        # pictures sit in the upper right of each panel, on a base line 0.2 below the panel's centre

        # 1 · lying on its side (Godot 4.7.2, +Y Up off: longest axis Z) - the real lantern render topples about its corner
        until(self, "It arrives", lead=0.25)
        x, y = cen[0]
        lh = 1.45
        lw = lh * A3_LANTERN_PX[0] / A3_LANTERN_PX[1]
        lan1 = ImageMobject("pantry/a3_lantern_34.png").set_height(lh).move_to([x + 0.75, y - 0.2 + lh / 2, 0])
        self.play(FadeOut(nums[0]), FadeIn(label(0, "lying on its side")), FadeIn(lan1), FadeIn(line(0, M("longest axis Z", 32))), run_time=0.3)
        self.play(Rotate(lan1, angle=-PI / 2, about_point=np.array([x + 0.75 + lw / 2, y - 0.2, 0.0])), run_time=0.5)
        self.play(Create(tick(0)), run_time=0.2)
        # 2 · ten times too big (every axis x10: the real run printed (3.0, 5.0, 3.0) m against the brief's (0.3, 0.5, 0.3))
        until(self, "wrong by a factor", lead=0.35)
        x, y = cen[1]
        lan2 = ImageMobject("pantry/a3_lantern_34.png").set_height(0.42).move_to([x + 1.65, y - 0.2 + 0.21, 0])
        self.play(FadeOut(nums[1]), FadeIn(label(1, "ten times too big")), FadeIn(lan2), run_time=0.3)
        self.play(lan2.animate.scale(1.45 / 0.42, about_edge=DOWN), run_time=0.6)
        self.play(FadeIn(line(1, M("(3.0, 5.0, 3.0) m", 32))), run_time=0.3)
        self.play(Create(tick(1)), run_time=0.2)
        # 3 · the server won't connect (predicted; the MCP route was not run, so no output is shown)
        until(self, "The server", lead=0.3)
        x, y = cen[2]
        py = y + 0.25
        sock = RoundedRectangle(width=0.75, height=1.1, corner_radius=0.12, fill_color=BAR1, fill_opacity=1, stroke_color=INK,
                                stroke_width=4).move_to([x + 2.3, py, 0])
        holes = VGroup(*[Circle(radius=0.08, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x + 2.15, py + d, 0]) for d in (0.22, -0.22)])
        plug = VGroup(RoundedRectangle(width=0.7, height=0.8, corner_radius=0.12, fill_color=A3_WOOD, fill_opacity=1, stroke_color=INK,
                                       stroke_width=4).move_to([x + 0.3, py, 0]),
                      *[Line([x + 0.65, py + d, 0], [x + 0.97, py + d, 0], color=DIM, stroke_width=9) for d in (0.22, -0.22)],
                      Line([x - 0.05, py, 0], [x - 0.75, py, 0], color=A3_BAND, stroke_width=9))
        self.play(FadeOut(nums[2]), FadeIn(label(2, "won't connect")), FadeIn(sock), FadeIn(holes), FadeIn(plug), run_time=0.3)
        self.play(plug.animate.shift(RIGHT * 0.6), run_time=0.45)
        nr = a3_left(T("not run", 32), x - W / 2 + 3.4, y + H / 2 - 0.5)
        self.play(FadeIn(line(2, T("MCP for Blender tab", 36))), FadeIn(nr), run_time=0.3)     # 36: at 32 Pango splits "Blen der"
        self.play(Create(tick(2)), run_time=0.2)
        # 4 · a colour does not survive the export (Godot reads albedo #E7E7E7 for both of the crate's materials)
        until(self, "A colour", lead=0.3)
        x, y = cen[3]
        cr = a3_crate_side(x + 1.65, y - 0.2, s=1.8)
        self.play(FadeOut(nums[3]), FadeIn(label(3, "colour lost")), FadeIn(cr), run_time=0.3)
        self.play(*[cr[i].animate.set_fill("#E7E7E7") for i in range(4)], run_time=0.7)
        self.play(FadeIn(line(3, M("albedo #E7E7E7", 32))), run_time=0.3)
        self.play(Create(tick(3)), run_time=0.2)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · Connect Claude to Blender  (B29, B30, B34–B40 Manim; B31 BrowserCapture, B32–B33 CCPlainShell: see lanes/act4.json)

HONESTY RULE for the whole act: the course has NEVER run the MCP route. No beat shows an MCP session, a tool call's output, or the
add-on's panel. The route is drawn as an idea (the act's cast) and labelled "documented, not run"; the three typed commands are shown
without output; README text is the project's own words (<= 15 words per quote, version and date on screen). The script route WAS run:
B39A/B39B replay its real output (evidence/assets/build_lantern.log, evidence/exitcode/*.log).

One cast for the act (ACTS.md): three blocks, Claude Code (kraft block), the server (the kit's dark server stack) and Blender (kraft
block + Blender's REAL icon) with its add-on (the kit's dark MCP block) sitting on it; the socket (a ring with a terracotta dot) on
the add-on's face is where the line from the server ends. `a4_cast` builds it at any scale so every beat shows the same objects.
"""

A4_CABLE = "#9C8462"                           # deep kraft for connectors (ink-edged pipes fuse blocks into one text blob)
A4_ICON = "pantry/ev_icon_blender.png"         # the REAL Blender app icon
A4_TAG = "documented, not run"
A4_XL = -6.25                                  # left edge of a Menlo 32 command block (0.25 units per character)
A4_DX = -6.05                                  # x of the terracotta 'you are here' dot beside indented flag rows


# ═════════════════════════════ cast helpers ═════════════════════════════
def a4_iso(cx, cy, s, W, D, H=0.0):
    """An Iso whose projected footprint W x D x H is centred on the scene point (cx, cy)."""
    ox = cx - (W - D) * C30 * s / 2
    oy = cy - ((W + D) / 2 + H) * s / 2
    return Iso(ox, oy, s)


def a4_socket(x, y, r=0.22, open_=True):
    """The add-on's socket: a ring; a terracotta dot inside while it is open (listening)."""
    ring = Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    dot = Dot([x, y, 0], radius=r * 0.38, color=TERRA if open_ else GHOST)
    return VGroup(ring, dot)


def a4_cable(p, q, w=8):
    return Line(np.array([p[0], p[1], 0.0]), np.array([q[0], q[1], 0.0]), color=A4_CABLE, stroke_width=w)


def a4_page(cx, cy, s=1.0):
    """A script / file page (kit page: white slab, ghost lines, terracotta dot), centred on (cx, cy)."""
    return a4_iso(cx, cy, s, 1.1, 1.4, 0.06).page(0, 0, 0, 1.1, 1.4)


def a4_cast(x0=0.0, y0=0.0, k=1.0):
    """The act's cast, designed at k=1 for B29, scaled by k about the origin and shifted by (x0, y0). Returns a dict."""
    def P(x, y):
        return (x0 + x * k, y0 + y * k)
    c = {}
    c["cc"] = a4_iso(*P(-4.7, -0.55), k, 1.3, 1.3, 0.8).box(0, 0, 0, 1.3, 1.3, 0.8)
    stack, lights = a4_iso(*P(-0.9, -0.45), k, 1.2, 1.2, 1.16).server(0, 0, 0, 1.2, 1.2, 0.36, 3)
    c["server"], c["lights"] = stack, lights
    bi = a4_iso(*P(3.9, -0.65), k, 1.5, 1.5, 0.9)
    c["blender"] = bi.box(0, 0, 0, 1.5, 1.5, 0.9)
    c["addon"] = bi.mcp(0.1, 0.75, 0.9, 0.6, 0.6, 0.45)
    c["icon"] = ImageMobject(A4_ICON).set_height(1.15 * k).move_to([*P(4.35, 1.35), 0])
    sx, sy = P(3.08, -0.15)
    c["sock"] = np.array([sx, sy, 0.0])
    c["socket"] = a4_socket(sx, sy, 0.22 * max(k, 0.75))
    c["cc_r"] = np.array([*P(-3.5, -0.5), 0.0])           # Claude Code's right face
    c["srv_l"] = np.array([*P(-1.95, -0.5), 0.0])         # server, left face
    c["srv_r"] = np.array([*P(0.2, -0.45), 0.0])          # server, right face
    c["sock_l"] = np.array([*P(3.08 - 0.24, -0.17), 0.0])  # where the server's line meets the socket ring
    c["land"] = np.array([*P(4.35, -0.3), 0.0])           # where a call lands, on Blender's top face
    c["c1"] = a4_cable(c["cc_r"], c["srv_l"], 8 if k >= 0.7 else 6)
    c["c2"] = a4_cable(c["srv_r"], c["sock_l"], 8 if k >= 0.7 else 6)
    c["c1"].set_z_index(-1); c["c2"].set_z_index(-1)
    return c


def a4_doc(cx, cy, w, h, lines, src, size=34, src_size=32, gap=0.56):
    """README words, shown as the project's own words: an outline page (DIM, no fill behind text) holding the quote lines
    (serif ink, centred) and, last, the source line (version and date). Returns (outline, [line texts], source text)."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    n = len(lines) + 1
    y0 = cy + gap * (n - 1) / 2
    txt = [T(s, size).move_to([cx, y0 - i * gap, 0]) for i, s in enumerate(lines)]
    srct = T(src, src_size).move_to([cx, y0 - (n - 1) * gap, 0])
    return box, txt, srct


def a4_mline(s, y, indent=0, color=INK):
    """One Menlo 32 line, left edge at A4_XL + indent characters."""
    return M(s, 32, color).move_to([A4_XL + (indent + len(s) / 2.0) * 0.25, y, 0])


def a4_switch(x, y, on=False):
    """A plain on/off switch (an idea of a setting, not the add-on's panel): outline pill + knob (left = off)."""
    pill = RoundedRectangle(width=0.8, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x + (0.19 if on else -0.19), y, 0])
    return pill, knob


def a4_strike(cx, cy, w, h, color=INK, sw=8):
    return VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=color, stroke_width=sw),
                  Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=color, stroke_width=sw))


# ── B29 · the MCP route: add-on, socket, server, Claude Code (ACT TITLE) ─────────────────────────────────────────
class B29_MCPRoute(Scene):
    def construct(self):
        c = a4_cast()
        title = T("Connect  Claude to Blender", 40).move_to([-3.05, 3.05, 0])   # double space: Pango fuses the single one
        tag = T(A4_TAG, 32).move_to([0.0, -3.05, 0])
        self.add(title, tag)
        until(self, "An add-on inside", lead=0.35)
        bl = T("Blender", 34).move_to([4.35, -2.3, 0])
        self.play(FadeIn(c["blender"]), FadeIn(c["icon"]), FadeIn(bl), run_time=0.5)
        al = T("add-on", 34).move_to([3.0, 0.98, 0])
        self.play(FadeIn(c["addon"], shift=DOWN * 0.25), FadeIn(al), run_time=0.45)
        until(self, "opens a local socket", lead=0.25)
        sl = T("socket", 34).move_to([1.95, 0.3, 0])
        self.play(GrowFromCenter(c["socket"]), FadeIn(sl), run_time=0.5)
        until(self, "a small server", lead=0.3)
        srl = T("server", 34).move_to([-0.9, -2.2, 0])
        self.play(FadeIn(c["server"]), FadeIn(c["lights"]), FadeIn(srl), run_time=0.45)
        self.play(Create(c["c2"]), run_time=0.35)
        until(self, "launched by Claude Code", lead=0.2)
        ccl = T("Claude Code", 34).move_to([-4.7, -2.2, 0])
        self.play(FadeIn(c["cc"]), FadeIn(ccl), Create(c["c1"]), run_time=0.55)
        until(self, "relays", lead=0.25)
        path = VMobject().set_points_as_corners([c["cc_r"], c["srv_l"], c["srv_r"], c["sock"], c["land"]])
        dots = [Dot(c["cc_r"], radius=0.13, color=TERRA) for _ in range(3)]
        self.add(*dots)
        self.play(c["lights"].animate.set_color(TERRA), run_time=0.25)
        self.play(LaggedStart(*[MoveAlongPath(d, path, rate_func=linear) for d in dots], lag_ratio=0.4), run_time=2.2)
        self.play(*[FadeOut(d) for d in dots], run_time=0.2)
        until(self, "That's the M C P route", lead=0.15)
        br = VGroup(Line([-5.6, 1.5, 0], [-5.6, 1.75, 0]), Line([-5.6, 1.75, 0], [3.2, 1.75, 0]),
                    Line([3.2, 1.75, 0], [3.2, 1.5, 0])).set_stroke(DIM, 4)
        ml = T("the MCP route", 36).move_to([-1.2, 2.2, 0])
        self.play(Create(br), FadeIn(ml), run_time=0.45)
        done(self)


# ── B30 · what is known: not run by the course; the README's steps as recorded 27 Sept; 7 releases in 9 days ───────
A4_T0, A4_T1 = -5.6, 5.6                     # the release strip: 27 Sept 2026 .. 6 Oct 2026 (9 days)


def a4_day(d):
    return A4_T0 + d * (A4_T1 - A4_T0) / 9.0


class B30_KnownAndNot(Scene):
    def construct(self):
        c = a4_cast(-2.6, 2.4, 0.5)
        self.add(c["cc"], c["server"], c["lights"], c["blender"], c["addon"], c["icon"], c["socket"], c["c1"], c["c2"])
        until(self, "hasn't run", lead=0.3)
        g1 = DashedLine(c["cc_r"], c["srv_l"], dash_length=0.12, color=GHOST, stroke_width=6)
        g2 = DashedLine(c["srv_r"], c["sock_l"], dash_length=0.12, color=GHOST, stroke_width=6)
        tag = T(A4_TAG, 36).move_to([3.4, 2.4, 0])
        self.play(FadeOut(c["c1"]), FadeOut(c["c2"]), Create(g1), Create(g2), c["socket"][1].animate.set_color(GHOST),
                  FadeIn(tag), run_time=0.6)
        until(self, "These steps come from", lead=0.2)
        box, _, head = a4_doc(-2.2, -0.05, 7.6, 2.55, [], "README, version 2.1.1 · 27 Sept 2026")
        head.move_to([-2.2, 0.82, 0])
        steps = ["1. Install uv", "2. Add the MCP server to your client", "3. Install the Blender addon"]
        widths = [2.08, 6.89, 5.08]                      # measured EB Garamond 36 widths (Text(...).width)
        rows = [T(s, 36).move_to([-5.55 + w / 2, 0.22 - i * 0.6, 0]) for i, (s, w) in enumerate(zip(steps, widths))]
        self.play(Create(box), FadeIn(head), run_time=0.45)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.25)
        until(self, "as recorded on", lead=0.15)
        axis = Line([A4_T0 - 0.2, -2.55, 0], [A4_T1 + 0.2, -2.55, 0], color=DIM, stroke_width=4)
        d0 = Dot([A4_T0, -2.25, 0], radius=0.12, color=TERRA)
        l0 = T("2.1.1", 32).move_to([A4_T0 + 0.68, -2.22, 0])
        day0 = T("27 Sept", 32).move_to([A4_T0 + 0.05, -3.02, 0])
        self.play(Create(axis), FadeIn(d0), FadeIn(l0), FadeIn(day0), run_time=0.5)
        until(self, "And the project changes fast", lead=0.6)
        rel = [(3, 0), (3, 1), (8, 0), (8, 1), (8, 2), (8, 3), (9, 0)]    # 2.1.2, 2.1.3 (30 Sept); 2.1.5-2.1.8 (5 Oct); 2.1.9 (6 Oct)
        for d, j in rel:
            self.play(GrowFromCenter(Dot([a4_day(d), -2.25 + 0.32 * j, 0], radius=0.11, color=INK)), run_time=0.09)
        l9 = T("2.1.9", 32).move_to([A4_T1, -1.82, 0])
        day9 = T("6 Oct", 32).move_to([A4_T1 - 0.1, -3.02, 0])
        cnt = T("7 releases in 9 days", 34).move_to([1.15, -1.75, 0])
        self.play(FadeIn(l9), FadeIn(day9), FadeIn(cnt), run_time=0.35)
        done(self)


# ── B34 · step three: the add-on; Edit > Preferences > Add-ons (REAL captures); the README's words for the row ────────
class B34_AddOn(Scene):
    """The real dark Blender captures land AFTER the clip midpoint (GATE T reads a dark capture's interior as stacked text blobs);
    before it, the shell and Blender's real icon carry "in Blender"."""
    def construct(self):
        shell = ImageMobject("pantry/a4_shell_install_addon.png").set_width(12.2).move_to([0.0, 2.45, 0])
        self.add(shell)                                   # the toolkit's plain shell: the command, no output, "documented, not run"
        until(self, "Then, in Blender", lead=0.2)
        ic = ImageMobject(A4_ICON).set_height(0.95).move_to([-5.55, -0.1, 0])
        il = T("Blender", 32).move_to([-5.55, -1.0, 0])
        cap = T("real Blender 5.1.2 windows", 32).move_to([-2.0, -2.45, 0])
        self.play(FadeIn(ic), FadeIn(il), run_time=0.45)
        until(self, "Preferences", lead=0.0)              # lands just after the midpoint, on the word
        edit = ImageMobject("pantry/a4_edit_menu_prefs.png").set_width(3.0).move_to([-3.25, -0.1, 0])     # REAL Blender Edit menu
        el = T("Edit menu", 32).move_to([-3.25, -1.0, 0])
        d1 = Dot([-1.6, -0.36, 0], radius=0.1, color=TERRA)                                              # beside "Preferences..."
        self.play(FadeIn(edit), FadeIn(el), FadeIn(d1), FadeIn(cap), run_time=0.35)
        until(self, "Add-ons, and", lead=0.35)
        a1 = Arrow([-1.47, -0.36, 0], [-1.1, -0.2, 0], buff=0, color=INK, stroke_width=5, tip_length=0.14)
        prefs = ImageMobject("pantry/a4_prefs_addons_tab.png").set_height(1.65).move_to([0.45, -0.1, 0])  # REAL Preferences, Add-ons tab
        pl = T("Preferences", 32).move_to([0.45, -1.35, 0])
        d2 = Dot([2.08, -0.2, 0], radius=0.1, color=TERRA)                                               # beside "Add-ons"
        self.play(Create(a1), FadeIn(prefs), FadeIn(pl), FadeIn(d2), run_time=0.4)
        until(self, "and enable", lead=0.1)
        a2 = Arrow([2.21, -0.2, 0], [2.6, -0.2, 0], buff=0, color=INK, stroke_width=5, tip_length=0.14)
        box, txt, src = a4_doc(4.45, -0.15, 3.9, 2.6, ["\u201cenable Interface:", "MCP for Blender\u201d", "README 2.1.1"],
                               "27 Sept 2026", size=34, gap=0.52)
        self.play(Create(a2), Create(box), run_time=0.3)
        self.play(FadeIn(txt[0]), FadeIn(txt[1]), run_time=0.4)
        self.play(FadeIn(txt[2]), FadeIn(src), run_time=0.3)
        done(self)


# ── B35 · the server starts when Blender opens; press N, the tab; services off; a fresh Claude Code session ────────────
class B35_Checks(Scene):
    def construct(self):
        c = a4_cast(0.2, 1.75, 0.7)
        self.add(c["blender"], c["addon"])
        until(self, "starts its server", lead=0.25)
        self.play(FadeIn(c["icon"]), GrowFromCenter(c["socket"]), run_time=0.5)
        # README words (2.1.9): one sentence, then the tab instruction as two verbatim fragments (its arrow glyph is left out)
        box = RoundedRectangle(width=12.0, height=1.9, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0.0, -2.4, 0])
        q1 = T("\u201cThe addon starts its server when Blender opens.\u201d", 32).move_to([0.0, -2.1, 0])
        src = T("README 2.1.9 \u00b7 6 Oct 2026", 32).move_to([0.0, -2.9, 0])
        self.play(Create(box), FadeIn(q1), FadeIn(src), run_time=0.45)
        until(self, "To check, press N", lead=0.2)
        key = RoundedRectangle(width=0.95, height=0.95, corner_radius=0.16, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([-5.0, -0.55, 0])
        kn = T("N", 44).move_to([-5.0, -0.55, 0])
        q2a = T("\u201cTo check, press N in the 3D viewport\u201d", 32).move_to([0.0, -1.85, 0])
        q2b = T("\u201copen the MCP for Blender tab\u201d", 32).move_to([0.0, -2.37, 0])
        self.play(Create(key), FadeIn(kn), FadeOut(q1), run_time=0.4)
        self.play(FadeIn(q2a), FadeIn(q2b), run_time=0.35)
        until(self, "Every service", lead=-0.3)          # the row starts just after the clip midpoint
        sw = []
        for i in range(6):
            pill, knob = a4_switch(1.0 + i * 0.9, -0.4)
            sw += [pill, knob]
        sl = T("services and downloads: off", 34).move_to([3.25, -1.0, 0])
        for i in range(6):
            self.play(Create(sw[2 * i]), FadeIn(sw[2 * i + 1]), run_time=0.14)
        self.play(FadeIn(sl), run_time=0.3)
        until(self, "start a fresh Claude Code session", lead=0.25)
        nl = T("new session", 34).move_to([-3.09, 0.25, 0])
        self.play(FadeIn(c["cc"]), FadeIn(nl), FadeIn(c["server"]), FadeIn(c["lights"]), Create(c["c1"]), Create(c["c2"]), run_time=0.55)
        until(self, "so it sees the server", lead=0.15)
        d = Dot(c["cc_r"], radius=0.11, color=TERRA)
        self.add(d)
        self.play(d.animate.move_to(c["srv_l"]), c["lights"].animate.set_color(TERRA), run_time=0.4, rate_func=linear)
        done(self)


# ── B36 · the safety note: Python that Claude writes runs with no guard; the socket has no authentication ──────────────
class B36_OpenPort(Scene):
    def construct(self):
        c = a4_cast(0.2, 0.5, 1.0)
        tag = T(A4_TAG, 32).move_to([-4.15, 3.05, 0])
        self.add(c["cc"], c["server"], c["lights"], c["blender"], c["addon"], c["icon"], c["socket"], c["c1"], c["c2"], tag)
        ccl = T("Claude Code", 32).move_to([-4.5, -1.6, 0])
        self.add(ccl)
        until(self, "runs Python that Claude writes", lead=0.4)
        pg = a4_page(-4.5, 1.15, 0.45)
        pyl = T("Python", 34).move_to([-4.5, 1.95, 0])
        rp = T("runs Python", 34).move_to([4.55, 2.85, 0])
        self.play(FadeIn(pg, shift=DOWN * 0.2), FadeIn(pyl), run_time=0.4)
        until(self, "inside your Blender", lead=0.5)
        self.play(pg.animate.move_to(c["srv_l"] + np.array([0.0, 0.55, 0])), FadeOut(pyl), run_time=0.45, rate_func=linear)
        self.play(pg.animate.move_to(c["sock"] + np.array([-0.55, 0.45, 0])), run_time=0.5, rate_func=linear)
        self.play(pg.animate.move_to(c["sock"]).scale(0.25), run_time=0.3)
        self.play(FadeOut(pg), FadeIn(rp), Indicate(c["socket"], color=TERRA, scale_factor=1.3), run_time=0.45)
        until(self, "with no guard", lead=0.35)
        posts = VGroup(Line([1.85, -0.35, 0], [1.85, 0.75, 0]), Line([2.35, -0.35, 0], [2.35, 0.75, 0])).set_stroke(INK, 8)
        ng = T("no guard", 34).move_to([1.6, -0.85, 0])
        self.play(Create(posts), FadeIn(ng), run_time=0.45)
        until(self, "The readme says", lead=0.2)
        box, txt, src = a4_doc(0.0, -2.6, 12.0, 1.3, ["“the addon’s socket server has no authentication or encryption”"],
                               "README 2.1.9 · 6 Oct 2026", size=32, gap=0.52)
        self.play(Create(box), FadeIn(txt[0]), FadeIn(src), run_time=0.5)
        until(self, "anyone who can reach", lead=0.3)
        xs = [-1.55, -0.35, 0.85]
        outs = VGroup(*[RoundedRectangle(width=0.8, height=0.6, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                         stroke_width=5).move_to([x, 2.55, 0]) for x in xs])
        anl = T("anyone", 34).move_to([2.35, 2.55, 0])
        paths = VGroup(*[DashedLine([x, 2.2, 0], c["sock"] + np.array([-0.12, 0.2, 0]), dash_length=0.12, color=DIM, stroke_width=4)
                         for x in xs])
        paths.set_z_index(-1)
        self.play(Create(outs), FadeIn(anl), Create(paths), run_time=0.45)
        until(self, "can run Python inside", lead=0.6)
        ps = [a4_page(x, 2.55, 0.3) for x in xs]
        for p in ps:
            self.add(p)
        self.play(*[p.animate.move_to(c["sock"]).scale(0.3) for p in ps], run_time=0.55, rate_func=linear)
        self.play(*[FadeOut(p) for p in ps], Indicate(c["socket"], color=TERRA, scale_factor=1.3), run_time=0.45)
        done(self)


# ── B37A · localhost; save first; the add-on off when not in use (the socket opens whenever Blender starts with it on) ──
class B37A_ThreeHabits(Scene):
    def construct(self):
        # 1 · localhost: a wall round this machine; a call from outside stops at it
        wall = RoundedRectangle(width=2.6, height=2.5, corner_radius=0.25, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-3.9, 0.45, 0])
        ic1 = ImageMobject(A4_ICON).set_height(0.85).move_to([-4.15, 0.95, 0])
        so1 = a4_socket(-4.45, -0.15, 0.22)
        self.add(ic1, so1)
        until(self, "keep the port on localhost", lead=0.3)
        out = Dot([-6.0, -0.15, 0], radius=0.13, color=TERRA)
        lh = M("localhost", 32).move_to([-3.9, -1.3, 0])
        self.play(Create(wall), FadeIn(out), FadeIn(lh), run_time=0.45)
        self.play(out.animate.move_to([-5.38, -0.15, 0]), run_time=0.4, rate_func=linear)
        # 2 · save your work first
        until(self, "Save your work first", lead=0.25)
        pg = a4_page(0.0, 0.5, 1.0)
        sv = T("save first", 34).move_to([0.0, -1.3, 0])
        self.play(FadeIn(pg, shift=DOWN * 0.2), FadeIn(sv), run_time=0.4)
        self.play(Create(check(0.65, 1.55, 0.3)), run_time=0.35)
        # 3 · the add-on off: the switch goes off and the socket closes
        pill, knob = a4_switch(4.1, 1.55, on=True)
        ic3 = ImageMobject(A4_ICON).set_height(0.85).move_to([3.55, 0.2, 0])
        so3 = a4_socket(4.65, 0.2, 0.25)
        self.play(FadeIn(pill), FadeIn(knob), FadeIn(ic3), FadeIn(so3), run_time=0.35)
        until(self, "turn the add-on off", lead=0.2)
        of = T("add-on off", 34).move_to([4.1, -1.3, 0])
        shut = Line([4.47, 0.2, 0], [4.83, 0.2, 0], color=INK, stroke_width=8)
        self.play(knob.animate.move_to([3.91, 1.55, 0]), so3[1].animate.set_color(GHOST), FadeIn(of), run_time=0.5)
        self.play(Create(shut), run_time=0.3)
        # the reason: on every start it would open; off, it stays shut
        until(self, "the socket opens whenever", lead=0.3)
        self.play(ic3.animate.set_opacity(0.15), run_time=0.4)                    # Blender closed ...
        until(self, "Blender starts", lead=0.3)
        self.play(ic3.animate.set_opacity(1.0), Indicate(VGroup(so3, shut), color=INK, scale_factor=1.12), run_time=0.6)   # ... starts: stays shut
        done(self)


# ── B37B · don't open files from people you don't trust while the server is running ────────────────────────────────────
class B37B_Untrusted(Scene):
    def construct(self):
        c = a4_cast(0.8, 0.2, 1.0)
        rl = T("server running", 34).move_to([4.7, -2.15, 0])
        self.add(c["blender"], c["addon"], c["icon"], c["socket"])
        pg = a4_page(-4.6, -0.1, 1.0)
        ul = T("a .blend from a stranger", 34).move_to([-4.0, -1.5, 0])
        self.add(pg, ul)
        until(self, "open Blender files", lead=0.3)
        self.play(pg.animate.shift(RIGHT * 2.9), ul.animate.shift(RIGHT * 1.2), run_time=0.75)
        until(self, "people you don't trust", lead=0.35)
        x = a4_strike(1.6, -0.1, 0.8, 0.8)
        dl = T("don't open", 34).move_to([1.6, 1.05, 0])
        self.play(Create(x), FadeIn(dl), run_time=0.4)
        until(self, "while the server is running", lead=0.2)
        self.play(FadeIn(rl), Indicate(c["socket"], color=TERRA, scale_factor=1.3), run_time=0.6)
        done(self)


# ── B38 · it won't connect: that's data. About two hours, every step logged; then the script route ────────────────────
class B38_TimeBox(Scene):
    """Spread across the full width (Gate V fill): the broken connection runs along the top, the clock ring left, the log
    card centre, and the script route lands on the right on its words."""
    def construct(self):
        # no connection: the server's line stops short of the socket
        srv, lts = a4_iso(-5.1, 2.7, 0.5, 1.2, 1.2, 1.16).server(0, 0, 0, 1.2, 1.2, 0.36, 3)
        so = a4_socket(-0.15, 2.7, 0.22, open_=False)
        ca = a4_cable((-4.45, 2.7), (-2.65, 2.7), 7)
        cb = a4_cable((-1.75, 2.7), (-0.42, 2.7), 7)
        self.add(srv, lts, so)
        until(self, "doesn't connect", lead=0.3)
        gap = a4_strike(-2.2, 2.7, 0.36, 0.36, sw=6)
        nc = T("no connection", 36).move_to([3.3, 2.7, 0])
        self.play(Create(ca), Create(cb), Create(gap), FadeIn(nc), run_time=0.5)
        until(self, "that's data", lead=0.2)
        log = RoundedRectangle(width=4.2, height=3.3, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-0.15, -0.3, 0])
        lh = M("FRICTIONAL.md", 32).move_to([-0.15, 0.85, 0])
        self.play(Create(log), FadeIn(lh), run_time=0.4)
        until(self, "about two hours", lead=0.25)
        ring = Circle(radius=1.5, stroke_color=GHOST, stroke_width=14).move_to([-4.55, -0.3, 0])
        hl = T("about 2 hours", 36).move_to([-4.55, -2.45, 0])
        self.play(Create(ring), FadeIn(hl), run_time=0.3)
        arc = Arc(radius=1.5, start_angle=PI / 2, angle=-TAU * 0.999, color=INK, stroke_width=14).move_to([-4.55, -0.3, 0])
        self.play(Create(arc), run_time=1.6, rate_func=linear)
        until(self, "each step", lead=0.3)
        rows = VGroup()
        for i in range(3):
            y = 0.1 - i * 0.65
            rows.add(VGroup(Dot([-1.85, y, 0], radius=0.1, color=TERRA), Line([-1.55, y, 0], [1.5 - 0.45 * (i % 2), y, 0], color=DIM, stroke_width=9)))
        el = T("each step, its exact error", 36).move_to([-0.15, -2.45, 0])
        for r in rows:
            self.play(FadeIn(r), run_time=0.22)
        self.play(FadeIn(el), run_time=0.3)
        until(self, "switch to the script route", lead=0.3)
        fork = Arrow([2.15, -0.3, 0], [2.85, -0.3, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        sr = T("script route", 36).move_to([4.5, 1.5, 0])
        self.play(Create(fork), FadeIn(sr), run_time=0.45)
        until(self, "Claude writes a Blender script", lead=0.2)
        sp = a4_page(3.6, -0.3, 0.85)
        spl = T("script", 34).move_to([3.6, 0.65, 0])
        self.play(FadeIn(sp), FadeIn(spl), run_time=0.4)
        until(self, "and you run Blender", lead=0.45)
        a2 = Arrow([4.35, -0.3, 0], [4.8, -0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.16)
        bi = ImageMobject(A4_ICON).set_height(1.0).move_to([5.45, -0.3, 0])
        nw = T("no window", 32).move_to([5.2, -1.45, 0])
        self.play(Create(a2), FadeIn(bi), FadeIn(nw), run_time=0.45)
        done(self)


# ── B39A · the command (REAL, as run for the lantern): -b, --factory-startup, --python; its real output ──────────────────
A4_RY = [3.0, 2.3, 1.6, 0.9, 0.2]            # the command block rows


def a4_cmd_rows(exit_flag_color=GHOST):
    return [a4_mline("/Applications/Blender.app/Contents/MacOS/Blender \\", A4_RY[0]),
            a4_mline("-b \\", A4_RY[1], 2), a4_mline("--factory-startup \\", A4_RY[2], 2),
            a4_mline("--python-exit-code 1 \\", A4_RY[3], 2, exit_flag_color),
            a4_mline("--python build_lantern.py", A4_RY[4], 2)]


class B39A_Command(Scene):
    def construct(self):
        rows = a4_cmd_rows()
        self.play(FadeIn(VGroup(*rows)), run_time=0.45)
        # what it printed lands with the command (recorded output, excerpt), so the frame is full while the flags are read
        until(self, "that command", lead=0.1)
        oh = T("recorded output, excerpt", 32).move_to([-3.2, -0.6, 0])
        out = [a4_mline("Blender 5.1.2 | metric, 1 unit = 1 m | Z up", -1.15),     # build_lantern.log line 1
               a4_mline("\u2026", -1.62),                                           # lines 2-10 omitted
               a4_mline("exported lantern.glb (16520 bytes), +Y Up on", -2.09),    # line 11
               a4_mline("\u2026", -2.56),                                           # lines 12-13 omitted
               a4_mline("Blender quit", -3.03)]                                     # line 14
        rule = Line([-6.2, -0.25, 0], [6.2, -0.25, 0], color=GHOST, stroke_width=4)
        self.play(Create(rule), FadeIn(oh), *[FadeIn(o) for o in out], run_time=0.4)
        dot = Dot([A4_DX, A4_RY[1], 0], radius=0.12, color=TERRA)
        until(self, "Dash b", lead=0.2)
        l1 = T("no window", 34).move_to([3.2, A4_RY[1], 0])
        self.play(FadeIn(dot), FadeIn(l1), run_time=0.4)
        until(self, "Factory startup", lead=0.15)
        l2 = T("your settings, skipped", 34).move_to([3.2, A4_RY[2], 0])
        self.play(dot.animate.move_to([A4_DX, A4_RY[2], 0]), run_time=0.25)
        self.play(FadeIn(l2), run_time=0.35)
        until(self, "Python runs the script", lead=0.5)
        l3 = T("runs the script", 34).move_to([3.2, A4_RY[4], 0])
        self.play(dot.animate.move_to([A4_DX, A4_RY[4], 0]), run_time=0.25)
        self.play(FadeIn(l3), run_time=0.3)
        done(self)


# ── B39B · --python-exit-code 1: the same error, exit 1 with it, exit 0 without it (REAL output) ──────────────────────
class B39B_ExitCode(Scene):
    def construct(self):
        flag = a4_mline("--python-exit-code 1", 2.95, 2)
        dot = Dot([A4_DX, 2.95, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(flag), FadeIn(dot), run_time=0.4)
        until(self, "makes a crashing script", lead=0.3)
        wl = T("with the flag", 34).move_to([2.6, 2.95, 0])
        e1 = a4_mline("ValueError: this script fails on purpose", 2.3)
        self.play(FadeIn(wl), FadeIn(e1), run_time=0.4)
        until(self, "fail loudly", lead=0.35)
        e2 = a4_mline("Error: script failed, file: 'bad.py', exiting.", 1.7)
        k1 = a4_mline("$ echo $?", 1.05)
        n1 = T("1", 88).move_to([-3.15, 1.0, 0])
        x1 = T("exit code", 32).move_to([-1.85, 1.0, 0])
        self.play(FadeIn(e2), FadeIn(k1), FadeIn(n1), FadeIn(x1), run_time=0.45)
        until(self, "Without it", lead=0.0)
        rule = Line([-6.2, 0.35, 0], [6.2, 0.35, 0], color=GHOST, stroke_width=4)
        wo = T("without the flag", 34).move_to([-4.7, -0.25, 0])
        e3 = a4_mline("ValueError: this script fails on purpose", -0.9)
        self.play(Create(rule), FadeIn(wo), FadeIn(e3), run_time=0.45)
        until(self, "exits with zero", lead=0.3)
        k0 = a4_mline("$ echo $?", -1.55)
        n0 = T("0", 88).move_to([-3.15, -1.6, 0])
        x0_ = T("exit code", 32).move_to([-1.85, -1.6, 0])
        self.play(FadeIn(k0), FadeIn(n0), FadeIn(x0_), run_time=0.4)
        until(self, "raises an error", lead=0.3)
        sp = Dot([4.1, -0.9, 0], radius=0.12, color=TERRA)
        rec = T("recorded output, excerpts", 32).move_to([2.6, -2.75, 0])
        self.play(FadeIn(sp), FadeIn(rec), run_time=0.35)
        done(self)


# ── B40 · an honest failed attempt + a working script fallback: up to 6 of the 8 MCP points, not all 8 ────────────────
class B40_SixOfEight(Scene):
    def construct(self):
        x0, cw, gp, y = -3.0, 0.95, 0.1, 0.3
        cells = [Rectangle(width=cw, height=0.9, fill_color=BAR1, fill_opacity=0, stroke_color=DIM, stroke_width=4)
                 .move_to([x0 + cw / 2 + i * (cw + gp), y, 0]) for i in range(8)]
        self.add(*cells)
        until(self, "honest, specific account", lead=0.3)
        h1 = T("honest account", 34).move_to([-4.75, 0.62, 0])
        self.play(FadeIn(h1), run_time=0.35)
        until(self, "working script fallback", lead=0.3)
        h2 = T("+ script fallback", 34).move_to([-4.75, -0.02, 0])
        self.play(FadeIn(h2), run_time=0.35)
        until(self, "earns up to six", lead=0.3)
        for i in range(6):
            self.play(cells[i].animate.set_fill(BAR1, 1), run_time=0.11)
        xe = x0 + 6 * cw + 5 * gp
        br = VGroup(Line([x0, -0.35, 0], [x0, -0.55, 0]), Line([x0, -0.55, 0], [xe, -0.55, 0]),
                    Line([xe, -0.55, 0], [xe, -0.35, 0])).set_stroke(INK, 5)
        u6 = T("up to 6", 36).move_to([(x0 + xe) / 2, -1.05, 0])
        self.play(Create(br), FadeIn(u6), run_time=0.4)
        until(self, "of the eight", lead=0.2)
        x8 = x0 + 8 * cw + 7 * gp
        top = VGroup(Line([x0, 0.95, 0], [x0, 1.15, 0]), Line([x0, 1.15, 0], [x8, 1.15, 0]),
                     Line([x8, 1.15, 0], [x8, 0.95, 0])).set_stroke(DIM, 4)
        e8 = T("8 MCP points", 36).move_to([(x0 + x8) / 2, 1.6, 0])
        self.play(Create(top), FadeIn(e8), run_time=0.4)
        until(self, "Not all eight", lead=0.15)
        s7 = a4_strike(x0 + cw / 2 + 6 * (cw + gp), y, 0.6, 0.6, sw=6)
        s8 = a4_strike(x0 + cw / 2 + 7 * (cw + gp), y, 0.6, 0.6, sw=6)
        na = T("not all 8", 36).move_to([x0 + 7 * (cw + gp), -1.05, 0])
        self.play(Create(s7), Create(s8), FadeIn(na), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Build the Assets  (B41-B47, B49 Manim; B48 is a Remotion ClaudeCodeBeat, see lanes/act5.json)

HONESTY. The course never ran the MCP route and no Claude session in Blender is shown. B41, B42 and B44 show the assignment's
plan-first prompt as a DOCUMENT (PROMPT-asset.txt, labelled "adapted prompt from the assignment, not run"): the text is verbatim
(evidence/act5/prompt.txt), only its line breaks are re-wrapped to fit Menlo at size 32. B43's five shapes are the REAL parts of
evidence/assets/build_lantern.py (names, radii and heights in metres, drawn to scale), shown as the loop's cast, never as tool output.
B45's tool names come from evidence/mcp/README-FACTS.md. B46/B47 crop the REAL Blender 5.1.2 window shots (evidence/act5/crop_a5.py;
the hand-edit pair is made by script and labelled "illustrative"). B49 replays the real `ls -1` (evidence/act5/ls_1.log) and the real
.gitignore lines of the scratch submission repo (evidence/act5/gitignore.log).

Cast for the act: the prompt document (B41, B42, B44); the lantern, shape by shape (B43, B46, B47); the loop strip
plan / approve / build / look / hand edit / save (B43, B46, B47, B49).
"""

# ── measured text metrics: (font, size, string) -> (centre_y - baseline, width, top - baseline, bottom - baseline) ──
# generated by evidence/act5/measure_a5_text.py with the real fonts (Menlo, EB Garamond); used so rows share baselines and
# rings/dots sit at exact distances from the glyphs. Missing keys fall back to an estimate.
A5_BL = {
    ('M', 32, "We are using Walker's Game brief → Build →"): (0.1249, 10.5033, 0.3422, -0.0924),
    ('M', 32, 'Playtest → Inspect → Revise → Export workflow.'): (0.1233, 11.368, 0.3391, -0.0924),
    ('M', 32, 'Use the Blender MCP tools in my open Blender'): (0.1233, 10.9688, 0.3391, -0.0924),
    ('M', 32, 'session. Read CHANGE-BRIEF.md first.'): (0.1657, 8.8645, 0.3377, -0.0063),
    ('M', 32, 'Task: build only this asset: <asset name>,'): (0.1296, 10.4035, 0.3453, -0.0861),
    ('M', 32, 'exactly as the brief specifies (size in'): (0.1364, 9.7014, 0.3621, -0.0893),
    ('M', 32, 'metres, origin, materials, triangle budget).'): (0.1317, 10.8871, 0.359, -0.0955),
    ('M', 32, 'Start from an empty scene with metric units;'): (0.1227, 10.8836, 0.3377, -0.0924),
    ('M', 32, 'Blender is Z-up.'): (0.1233, 3.8748, 0.3391, -0.0924),
    ('M', 32, 'First call get_scene_info and tell me what is'): (0.1218, 11.173, 0.3391, -0.0955),
    ('M', 32, 'in the scene, then propose the steps.'): (0.1289, 9.1092, 0.3439, -0.0861),
    ('M', 32, 'Do not build yet.'): (0.1233, 4.1311, 0.3391, -0.0924),
    ('M', 32, 'After I approve: one execute_blender_code call'): (0.1296, 11.4838, 0.3453, -0.0861),
    ('M', 32, 'per object. After each, call get_scene_info'): (0.128, 10.6967, 0.3453, -0.0893),
    ('M', 32, 'with the location, size, rotation and scale'): (0.1331, 10.7432, 0.3391, -0.0729),
    ('M', 32, 'fields and report them. Apply rotation and'): (0.1233, 10.4338, 0.3391, -0.0924),
    ('M', 32, 'scale before you finish. Then show me the'): (0.1233, 10.1969, 0.3391, -0.0924),
    ('M', 32, 'result with the look tool.'): (0.1664, 6.3322, 0.3391, -0.0063),
    ('M', 32, 'Do not use Poly Haven, Sketchfab, Poly Pizza,'): (0.1233, 11.134, 0.3391, -0.0924),
    ('M', 32, 'Hyper3D, Hunyuan3D or Tripo, and do not call'): (0.1233, 10.9621, 0.3391, -0.0924),
    ('M', 32, 'generate_3d, search_assets or import_asset.'): (0.1273, 10.634, 0.3439, -0.0893),
    ('M', 32, 'Do not export yet.'): (0.1158, 4.3811, 0.324, -0.0924),
    ('M', 32, 'Say what you could not verify.'): (0.1265, 7.3807, 0.3422, -0.0893),
    ('M', 32, "We are using Walker's Game brief"): (0.128, 7.9807, 0.3453, -0.0893),
    ('M', 32, 'Build'): (0.1664, 1.1902, 0.3391, -0.0063),
    ('M', 32, 'Playtest'): (0.1233, 1.9313, 0.3391, -0.0924),
    ('M', 32, 'Inspect'): (0.1189, 1.6805, 0.3271, -0.0893),
    ('M', 32, 'Revise'): (0.1683, 1.4621, 0.3396, -0.0031),
    ('M', 32, 'Export workflow.'): (0.1233, 3.868, 0.3391, -0.0924),
    ('M', 32, 'PROMPT-asset.txt'): (0.1618, 3.9313, 0.3299, -0.0063),
    ('M', 32, '…'): (0.0331, 0.2324, 0.0662, 0.0),
    ('M', 32, '1 of 5'): (0.1688, 1.4369, 0.3408, -0.0031),
    ('M', 32, '2 of 5'): (0.1688, 1.449, 0.3408, -0.0031),
    ('M', 32, '3 of 5'): (0.172, 1.4523, 0.3439, 0.0),
    ('M', 32, '4 of 5'): (0.1688, 1.46, 0.3408, -0.0031),
    ('M', 32, '5 of 5'): (0.172, 1.451, 0.3439, 0.0),
    ('M', 32, 'execute_blender_code'): (0.1367, 4.9664, 0.3453, -0.0719),
    ('M', 32, 'get_scene_info'): (0.1273, 3.4611, 0.3439, -0.0893),
    ('M', 32, 'look'): (0.1695, 0.9588, 0.3422, -0.0031),
    ('M', 32, 'get_object_info'): (0.1273, 3.7111, 0.3439, -0.0893),
    ('M', 32, 'get_viewport_screenshot'): (0.1211, 5.6973, 0.3377, -0.0955),
    ('M', 32, 'export_scene'): (0.1161, 2.9664, 0.3184, -0.0861),
    ('M', 32, '$ ls -1 *.blend *.blend1 *.glb'): (0.1218, 7.4502, 0.3391, -0.0955),
    ('M', 32, '.gitignore'): (0.1205, 2.4088, 0.3365, -0.0955),
    ('M', 32, '.godot/'): (0.1273, 1.6498, 0.3439, -0.0893),
    ('M', 32, '*.blend1'): (0.1664, 1.9744, 0.3391, -0.0063),
    ('M', 32, 'Lantern_Base'): (0.1229, 2.9465, 0.324, -0.0781),
    ('M', 32, 'Lantern_Glass'): (0.1336, 3.177, 0.3422, -0.075),
    ('M', 32, 'Lantern_Flame'): (0.1305, 3.1965, 0.3391, -0.0781),
    ('M', 32, 'Lantern_Roof'): (0.1298, 2.934, 0.3377, -0.0781),
    ('M', 32, 'Lantern_Finial'): (0.1305, 3.4451, 0.3391, -0.0781),
    ('M', 32, 'coin.blend'): (0.1695, 2.4338, 0.3422, -0.0031),
    ('M', 32, 'coin.blend1'): (0.1664, 2.6951, 0.3391, -0.0063),
    ('M', 32, 'coin.glb'): (0.1218, 1.949, 0.3391, -0.0955),
    ('M', 32, 'crate.blend'): (0.1727, 2.6838, 0.3453, 0.0),
    ('M', 32, 'crate.blend1'): (0.1695, 2.9451, 0.3422, -0.0031),
    ('M', 32, 'crate.glb'): (0.1249, 2.199, 0.3422, -0.0924),
    ('M', 32, 'lantern.blend'): (0.1664, 3.174, 0.3391, -0.0063),
    ('M', 32, 'lantern.blend1'): (0.1664, 3.4354, 0.3391, -0.0063),
    ('M', 32, 'lantern.glb'): (0.1218, 2.6893, 0.3391, -0.0955),
    ('T', 32, 'plan'): (0.0946, 0.716, 0.3146, -0.1254),
    ('T', 32, 'approve'): (0.0385, 1.3959, 0.1975, -0.1205),
    ('T', 32, 'build'): (0.1587, 0.917, 0.3195, -0.0021),
    ('T', 32, 'look'): (0.1573, 0.7045, 0.3171, -0.0024),
    ('T', 32, 'hand edit'): (0.1587, 1.5775, 0.3195, -0.0021),
    ('T', 32, 'save'): (0.0938, 0.6494, 0.1904, -0.0029),
    ('T', 32, 'move'): (0.0974, 0.9016, 0.1977, -0.0029),
    ('T', 32, 'colour'): (0.1587, 1.0307, 0.3195, -0.0021),
    ('T', 32, 'adapted prompt from the assignment, not run'): (0.0987, 7.958, 0.3201, -0.1227),
    ('T', 32, 'location'): (0.1596, 1.316, 0.3195, -0.0004),
    ('T', 32, 'size'): (0.138, 0.5494, 0.2784, -0.0024),
    ('T', 32, 'rotation'): (0.1402, 1.3615, 0.2805, 0.0),
    ('T', 32, 'scale'): (0.1596, 0.7494, 0.3195, -0.0004),
    ('T', 32, 'apply rotation + scale'): (0.0995, 3.6459, 0.3195, -0.1205),
    ('T', 32, 'recorded 27 Sep'): (0.0997, 2.5021, 0.3195, -0.1201),
    ('T', 32, '6 Oct'): (0.1505, 0.965, 0.3016, -0.0006),
    ('T', 32, 'removed'): (0.1584, 1.4111, 0.3195, -0.0027),
    ('T', 32, 'added'): (0.1606, 0.9576, 0.3213, 0.0),
    ('T', 32, 'check yours'): (0.0995, 2.0137, 0.3195, -0.1205),
    ('T', 32, 'Blender viewport'): (0.0995, 2.8275, 0.3195, -0.1205),
    ('T', 32, 'you'): (0.0361, 0.6277, 0.1917, -0.1194),
    ('T', 32, 'Claude'): (0.1591, 1.1918, 0.3199, -0.0018),
    ('T', 32, 'illustrative'): (0.1582, 1.8016, 0.3195, -0.0031),
    ('T', 32, 'before'): (0.1599, 1.0553, 0.3201, -0.0004),
    ('T', 32, 'after'): (0.1599, 0.7799, 0.3201, -0.0004),
    ('T', 32, 'notes'): (0.1085, 0.8686, 0.2174, -0.0004),
    ('T', 32, 'flame: up 0.02 m, now blue'): (0.0998, 4.6016, 0.3201, -0.1205),
    ('T', 32, 'learned:'): (0.1587, 1.2717, 0.3195, -0.0021),
    ('T', 32, 'source'): (0.0979, 1.0494, 0.1977, -0.002),
    ('T', 32, 'previous save'): (0.08, 2.2039, 0.2805, -0.1205),
    ('T', 32, 'not committed'): (0.1585, 2.5133, 0.3191, -0.0021),
    ('T', 40, 'Build the Assets'): (0.1983, 3.4012, 0.3994, -0.0027),
    ('T', 40, '2.1.1'): (0.1748, 1.0145, 0.3557, -0.0061),
    ('T', 40, '2.1.9'): (0.1762, 1.0395, 0.3617, -0.0094),
    ('T', 40, 'looks right?'): (0.117, 2.4623, 0.3934, -0.1594),
    ('T', 72, '?'): (0.3375, 0.241, 0.675, 0.0),
}

# x of each "→" glyph's centre from the row's left ink edge (same script). At Menlo 32 the arrow glyph is 17 px tall at 1080
# (34 at 4K), under GATE T's 1.9 % floor, so the glyph is hidden and the SAME arrow is drawn as a shape in its own cell.
A5_ARROWS = {"We are using Walker's Game brief → Build →": [8.3838, 10.3838], 'Playtest → Inspect → Revise → Export workflow.': [2.341, 4.841, 7.091]}
A5_PIECES = {"We are using Walker's Game brief → Build →": [("We are using Walker's Game brief", 0.0), ('Build', 8.7859)], 'Playtest → Inspect → Revise → Export workflow.': [('Playtest', 0.0), ('Inspect', 2.7508), ('Revise', 5.2383), ('Export workflow.', 7.5)]}

A5_P = 0.52                 # document row pitch
A5_TX = -5.5                # document text left edge
A5_TOPB = 1.38              # baseline of the first visible document row
A5_DOTX = -6.0              # the terracotta dot's column (left margin, outside every ring)
A5_DOC = [                  # (verbatim text of the prompt, re-wrapped; gap before the row in pitches)
    ("We are using Walker's Game brief → Build →", 0),          # 0  P1
    ("Playtest → Inspect → Revise → Export workflow.", 1),       # 1
    ("Use the Blender MCP tools in my open Blender", 1),        # 2
    ("session. Read CHANGE-BRIEF.md first.", 1),                # 3
    ("Task: build only this asset: <asset name>,", 2),          # 4  P2
    ("exactly as the brief specifies (size in", 1),             # 5
    ("metres, origin, materials, triangle budget).", 1),        # 6
    ("Start from an empty scene with metric units;", 1),        # 7
    ("Blender is Z-up.", 1),                                    # 8
    ("First call get_scene_info and tell me what is", 2),       # 9  P3
    ("in the scene, then propose the steps.", 1),               # 10
    ("Do not build yet.", 1),                                   # 11
    ("After I approve: one execute_blender_code call", 2),      # 12 P4
    ("per object. After each, call get_scene_info", 1),         # 13
    ("with the location, size, rotation and scale", 1),         # 14
    ("fields and report them. Apply rotation and", 1),          # 15
    ("scale before you finish. Then show me the", 1),           # 16
    ("result with the look tool.", 1),                          # 17
    ("Do not use Poly Haven, Sketchfab, Poly Pizza,", 2),       # 18 P5
    ("Hyper3D, Hunyuan3D or Tripo, and do not call", 1),        # 19
    ("generate_3d, search_assets or import_asset.", 1),         # 20
    ("Do not export yet.", 1.83),                               # 21 (extra space so the rings clear their neighbours)
    ("Say what you could not verify.", 1.83),                   # 22
]
def _a5_offsets():
    out, o = [], 0.0
    for _, g in A5_DOC:
        o += g * A5_P
        out.append(round(o, 4))
    return out


A5_OFF = _a5_offsets()
A5_SCROLL = {"B41": 0.0, "B42": A5_OFF[7], "B44": A5_OFF[18]}

A5_STEPS = ["plan", "approve", "build", "look", "hand edit", "save"]
A5_PARTS = [  # build_lantern.py: (object name, shape, radius m, depth m, z0 m); sphere: (name, "sphere", radius, None, centre z)
    ("Lantern_Base", "cylinder", 0.15, 0.04, 0.00),
    ("Lantern_Glass", "cylinder", 0.10, 0.23, 0.04),
    ("Lantern_Flame", "sphere", 0.06, None, 0.32),
    ("Lantern_Roof", "cone", 0.14, 0.10, 0.37),
    ("Lantern_Finial", "cylinder", 0.02, 0.03, 0.47),
]
A5_LS = ["coin.blend", "coin.blend1", "coin.glb", "crate.blend", "crate.blend1", "crate.glb",
         "lantern.blend", "lantern.blend1", "lantern.glb"]

A5_ALL = ([("M", 32, t) for t, _ in A5_DOC] +
          [("M", 32, w.strip()) for t, _ in A5_DOC if "→" in t for w in t.split("→") if w.strip()] +
          [("M", 32, s) for s in ["PROMPT-asset.txt", "…", "1 of 5", "2 of 5", "3 of 5", "4 of 5", "5 of 5", "execute_blender_code", "get_scene_info", "look", "get_object_info",
                                  "get_viewport_screenshot", "export_scene", "$ ls -1 *.blend *.blend1 *.glb", ".gitignore",
                                  ".godot/", "*.blend1"] + [p[0] for p in A5_PARTS] + A5_LS] +
          [("T", 32, s) for s in A5_STEPS + ["move", "colour", "adapted prompt from the assignment, not run", "location", "size", "rotation", "scale",
                                             "apply rotation + scale",
                                             "recorded 27 Sep", "6 Oct", "removed", "added", "check yours", "Blender viewport",
                                             "you", "Claude", "illustrative", "before", "after", "notes", "flame: up 0.02 m, now blue",
                                             "learned:", "source", "previous save", "not committed"]] +
          [("T", 40, s) for s in ["Build the Assets", "2.1.1", "2.1.9", "looks right?"]] +
          [("T", 72, "?")])


def a5_m(key):
    f, size, s = key
    if key in A5_BL:
        return A5_BL[key]
    w = len(s) * (0.2496 if f == "M" else 0.17) * size / 32.0
    return (0.06 * size / 32.0, w, 0.31 * size / 32.0, -0.11 * size / 32.0)


def a5_text(s, x, yb, size=32, mono=False, align="l", color=INK):
    """Text placed by its BASELINE yb. align 'l': x is the left edge; 'c': x is the centre."""
    key = ("M" if mono else "T", size, s)
    off = a5_m(key)[0]
    mob = M(s, size, color) if mono else T(s, size, color)
    if align == "l":
        mob.move_to([x, yb + off, 0], aligned_edge=LEFT)
    else:
        mob.move_to([x, yb + off, 0])
    return mob


def a5_w(s, size=32, mono=False):
    return a5_m(("M" if mono else "T", size, s))[1]


# ── the prompt document (B41, B42, B44) ──────────────────────────────────────────────────────────────────────
def a5_card():
    """A document window in the house code-card look: white card, title band with three dots and the file name."""
    card = RoundedRectangle(width=12.56, height=5.47, corner_radius=0.2, fill_color="#FFFFFF", fill_opacity=1,
                            stroke_color=DIM, stroke_width=3).move_to([0, 0.015, 0])
    sep = Line([-6.28, 2.12, 0], [6.28, 2.12, 0], color=DIM, stroke_width=2)
    dots = VGroup(*[Dot([x, 2.44, 0], radius=0.075, color=c) for x, c in ((-6.0, TERRA), (-5.7, GHOST), (-5.4, GHOST))])
    name = a5_text("PROMPT-asset.txt", -5.0, 2.33, mono=True)
    return VGroup(card, sep, dots, name)


def a5_label():
    return a5_text("adapted prompt from the assignment, not run", -6.3, -3.2)


def a5_yb(i, scroll):
    return A5_TOPB - (A5_OFF[i] - scroll)


def a5_visible(scroll):
    return [i for i in range(len(A5_DOC)) if -2.3 <= a5_yb(i, scroll) <= 1.4]


def a5_row(i, scroll):
    """One document row. A row with "→" is set as its words (each at its measured place) plus the arrows drawn as shapes in
    their own cells: the Menlo arrow glyph is 17 px tall at 1080 (34 at 4K), under GATE T's floor, and a shape inside a text
    box trips the layout audit."""
    s, yb = A5_DOC[i][0], a5_yb(i, scroll)
    if "→" not in s or s not in A5_PIECES:
        return a5_text(s, A5_TX, yb, mono=True)
    words = [a5_text(w, A5_TX + dx, yb, mono=True) for w, dx in A5_PIECES[s]]
    arrows = [Arrow([A5_TX + dx - 0.15, yb + 0.12, 0], [A5_TX + dx + 0.15, yb + 0.12, 0], buff=0, color=INK, stroke_width=4,
                    tip_length=0.2, max_tip_length_to_length_ratio=0.75) for dx in A5_ARROWS[s]]
    return VGroup(*words, *arrows)


def a5_rows(scroll):
    return {i: a5_row(i, scroll) for i in a5_visible(scroll)}


def a5_ring(a, b, scroll):
    """Outline round document rows a..b, 0.25 clear of every glyph. DIM, never ink: GATE T reads an ink outline round text
    as a text run that overlaps the text inside it (§8.6b); the same holds for every chip outline in this act."""
    top = a5_yb(a, scroll) + a5_m(("M", 32, A5_DOC[a][0]))[2] + 0.25
    bot = a5_yb(b, scroll) + a5_m(("M", 32, A5_DOC[b][0]))[3] - 0.25
    right = A5_TX + max(a5_w(A5_DOC[i][0], mono=True) for i in range(a, b + 1)) + 0.25
    left = A5_TX - 0.25
    return RoundedRectangle(width=right - left, height=top - bot, corner_radius=0.16, stroke_color=DIM, stroke_width=6,
                            fill_opacity=0).move_to([(left + right) / 2, (top + bot) / 2, 0])


def a5_dot_at(i, scroll):
    return np.array([A5_DOTX, a5_yb(i, scroll) + 0.1, 0.0])


def a5_scroll(self, rows, scroll_from, scroll_to):
    """Scroll the document: rows that leave fade upward, rows that stay slide up, new rows rise in. Returns the new row dict."""
    vis = a5_visible(scroll_to)
    leave = [i for i in rows if i not in vis]
    stay = [i for i in rows if i in vis]
    new = {i: a5_row(i, scroll_to) for i in vis if i not in rows}
    if leave:
        self.play(*[FadeOut(rows[i], shift=UP * 0.3) for i in leave], run_time=0.3)
    if stay:
        self.play(VGroup(*[rows[i] for i in stay]).animate.shift(UP * (scroll_to - scroll_from)), run_time=0.4)
    if new:
        self.play(LaggedStart(*[FadeIn(new[k], shift=UP * 0.3) for k in sorted(new)], lag_ratio=0.15), run_time=0.45)
    out = {i: rows[i] for i in stay}
    out.update(new)
    return out


# ── the loop strip (B43, B46, B47, B49) ──────────────────────────────────────────────────────────────────────
A5_SY = -2.9          # strip chip centre
A5_SGAP = 0.32


def a5_strip_x():
    ws = [a5_w(s) + 0.6 for s in A5_STEPS]
    total = sum(ws) + A5_SGAP * (len(ws) - 1)
    xs, x = [], -total / 2
    for w in ws:
        xs.append((x + w / 2, w))
        x += w + A5_SGAP
    return xs


def A5_CHIP_STATE(i, k):
    """(colour, width) of strip chip i when step k is active: done DIM 4, active DIM 8 (plus the dot), still to come GHOST 4."""
    return (DIM, 8) if i == k else ((DIM, 4) if i < k else (GHOST, 4))


def a5_strip(active):
    """Six outlined chips. Steps before `active` are done (ink), the active one is heavy ink with a terracotta dot above,
    the rest are dim outlines (labels stay ink)."""
    xs = a5_strip_x()
    k = A5_STEPS.index(active)
    chips = VGroup()
    for i, (s, (cx, w)) in enumerate(zip(A5_STEPS, xs)):
        col, sw = A5_CHIP_STATE(i, k)
        box = RoundedRectangle(width=w, height=0.95, corner_radius=0.3, stroke_color=col, stroke_width=sw,
                               fill_opacity=0).move_to([cx, A5_SY, 0])
        lab = a5_text(s, cx, A5_SY - 0.09, align="c")
        chips.add(VGroup(box, lab))
    dot = Dot([xs[k][0], A5_SY + 0.68, 0], radius=0.08, color=TERRA)
    return chips, dot


def a5_strip_to(chips, dot, step):
    """Animations that move the strip's active step to `step`."""
    xs = a5_strip_x()
    k = A5_STEPS.index(step)
    anims = [dot.animate.move_to([xs[k][0], A5_SY + 0.68, 0])]
    for i, ch in enumerate(chips):
        col, sw = A5_CHIP_STATE(i, k)
        anims.append(ch[0].animate.set_stroke(col, sw))
    return anims


# ── the lantern, drawn to scale from build_lantern.py (B43) ───────────────────────────────────────────────────
A5_LX, A5_LY, A5_LS_ = -4.4, -2.05, 8.0          # base centre x, floor y, scene units per metre


def a5_part(i):
    name, kind, r, d, z0 = A5_PARTS[i]
    fill = TERRA if name == "Lantern_Flame" else (BOX_R if name == "Lantern_Glass" else DIM)
    if kind == "cylinder":
        return Rectangle(width=2 * r * A5_LS_, height=d * A5_LS_, fill_color=fill, fill_opacity=1, stroke_color=INK,
                         stroke_width=4).move_to([A5_LX, A5_LY + (z0 + d / 2) * A5_LS_, 0])
    if kind == "cone":
        return Polygon([A5_LX - r * A5_LS_, A5_LY + z0 * A5_LS_, 0], [A5_LX + r * A5_LS_, A5_LY + z0 * A5_LS_, 0],
                       [A5_LX, A5_LY + (z0 + d) * A5_LS_, 0], fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return Circle(radius=r * A5_LS_, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([A5_LX, A5_LY + z0 * A5_LS_, 0])


def a5_chip(s, x_left, y, mono=False, h=0.95, col=DIM, sw=4):
    w = a5_w(s, mono=mono) + 0.6
    box = RoundedRectangle(width=w, height=h, corner_radius=0.25, stroke_color=col, stroke_width=sw,
                           fill_opacity=0).move_to([x_left + w / 2, y, 0])
    lab = a5_text(s, x_left + w / 2, y - 0.09, mono=mono, align="c")
    return VGroup(box, lab)


def a5_eye(x, y, s=1.0):
    """An eye: two arcs, an iris ring and a pupil, all ink."""
    top = ArcBetweenPoints([x - 0.75 * s, y, 0], [x + 0.75 * s, y, 0], angle=-1.4, color=INK, stroke_width=6)
    bot = ArcBetweenPoints([x - 0.75 * s, y, 0], [x + 0.75 * s, y, 0], angle=1.4, color=INK, stroke_width=6)
    iris = Circle(radius=0.27 * s, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    pupil = Dot([x, y, 0], radius=0.12 * s, color=INK)
    return VGroup(top, bot, iris, pupil)


def a5_at(self, t):
    """Wait until absolute clip time t (seconds): for cues taken from whisper word times of the beat's real audio."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


# B44 cue times (s) from faster-whisper word timestamps of mp3/beat-B44.mp3 (8.87 s, re-voiced 2026-10-06):
# "3D" 0.88, "AI" 2.52, "generation" 2.90, "forbids" 4.28, "say" 6.98, "verify." 7.66-8.08
A5_B44_T = {"three-D model downloads": 0.88, "generation tools": 2.90, "forbids": 4.28, "say what you could not verify": 6.98}


# ── B41 · plan first: the prompt (carries the act title) ───────────────────────────────────────────────────────
class B41_PlanPrompt(Scene):
    def construct(self):
        sc = A5_SCROLL["B41"]
        title = a5_text("Build the Assets", -6.3, 2.98, size=40)
        lab = a5_label()
        self.add(title, lab)
        card = a5_card()
        self.play(FadeIn(card, shift=UP * 0.2), run_time=0.5)
        rows = a5_rows(sc)
        until(self, "Ask Claude for a plan first", lead=0.1)
        self.play(LaggedStart(*[FadeIn(rows[i]) for i in range(0, 4)], lag_ratio=0.3), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(rows[i]) for i in range(4, 7)], lag_ratio=0.3), run_time=0.5)
        until(self, "names the workflow", lead=0.25)
        r1 = a5_ring(0, 3, sc)
        dot = Dot(a5_dot_at(0, sc), radius=0.09, color=TERRA)
        self.play(Create(r1), FadeIn(dot), run_time=0.5)
        until(self, "points at your brief", lead=0.15)
        self.play(dot.animate.move_to(a5_dot_at(3, sc)), run_time=0.35)
        until(self, "gives one task", lead=0.2)
        r2 = a5_ring(4, 6, sc)
        self.play(r1.animate.set_stroke(GHOST, 4), Create(r2), dot.animate.move_to(a5_dot_at(4, sc)), run_time=0.5)
        until(self, "exactly as the brief says", lead=0.15)
        self.play(dot.animate.move_to(a5_dot_at(5, sc)), run_time=0.35)
        done(self)


# ── B42 · get_scene_info first; propose; do not build yet ──────────────────────────────────────────────────────
class B42_SceneInfoFirst(Scene):
    def construct(self):
        s0, s1 = A5_SCROLL["B41"], A5_SCROLL["B42"]
        card = a5_card()
        lab = a5_label()
        rows = a5_rows(s0)
        self.add(card, lab, *rows.values())
        rows = a5_scroll(self, rows, s0, s1)
        until(self, "calling get scene info", lead=0.1)
        ring = a5_ring(9, 11, s1)
        dot = Dot(a5_dot_at(9, s1), radius=0.09, color=TERRA)
        self.play(Create(ring), FadeIn(dot), run_time=0.5)
        until(self, "proposes steps", lead=0.15)
        self.play(dot.animate.move_to(a5_dot_at(10, s1)), run_time=0.35)
        until(self, "doesn't build yet", lead=0.15)
        self.play(dot.animate.move_to(a5_dot_at(11, s1)), run_time=0.35)
        done(self)


# ── B43 · one execute_blender_code call per object; report; apply; look ──────────────────────────────────────────
class B43_OnePerObject(Scene):
    def construct(self):
        chips, sdot = a5_strip("approve")
        floor = Line([-6.1, A5_LY, 0], [-2.7, A5_LY, 0], color=DIM, stroke_width=3)
        self.add(chips, sdot, floor)
        X0 = -1.9
        YA, YB, YC, YD, YH = 1.75, 0.55, -0.25, -1.4, 2.62
        ex = a5_chip("execute_blender_code", X0, YA, mono=True)
        gsi = a5_text("get_scene_info", X0, YB, mono=True)
        fields, x = VGroup(), X0
        for f in ("location", "size", "rotation", "scale"):
            c = a5_chip(f, x, YC, h=0.9)
            fields.add(c)
            x += a5_w(f) + 0.6 + 0.15
        apply_ = a5_chip("apply rotation + scale", X0, YD)
        look = a5_chip("look", X0 + a5_w("apply rotation + scale") + 0.6 + 0.35, YD, mono=True)   # the prompt's look tool
        DX = -2.3                                           # the step dot's column
        step = Dot([DX, YA, 0], radius=0.09, color=TERRA)

        def head(i):
            return VGroup(a5_text(f"{i + 1} of 5", X0, YH, mono=True), a5_text(A5_PARTS[i][0], X0 + 1.95, YH, mono=True))

        parts = [a5_part(i) for i in range(5)]
        order = [0, 1, 2, 4, 3]                              # draw order: base, glass, flame, (finial), roof over the flame
        until(self, "one execute", lead=0.3)
        h = head(0)
        self.play(*a5_strip_to(chips, sdot, "build"), FadeIn(ex), FadeIn(step), FadeIn(h), GrowFromEdge(parts[0], DOWN),
                  run_time=0.6)
        cues = [("per object", 1), ("location, size", 2), ("rotation and scale. It", 3), ("It applies", 4)]
        for k, (cue, i) in enumerate(cues):
            if k == 1:
                until(self, "After each", lead=0.2)
                self.play(FadeIn(gsi), LaggedStart(*[FadeIn(c) for c in fields], lag_ratio=0.2),
                          step.animate.move_to([DX, YC, 0]), run_time=0.6)
            until(self, cue, lead=0.2)
            h2 = head(i)
            self.play(step.animate.move_to([DX, YA, 0]), FadeOut(h), FadeIn(h2), GrowFromEdge(parts[i], DOWN), run_time=0.45)
            h = h2
            if k >= 1:
                self.play(step.animate.move_to([DX, YC, 0]), run_time=0.3)
        until(self, "before finishing", lead=0.5)
        box = DashedVMobject(Rectangle(width=2.75, height=4.25, stroke_color=INK, stroke_width=4).move_to(
            [A5_LX, A5_LY + 2.0, 0]), num_dashes=40)
        self.play(FadeIn(apply_), Create(box), step.animate.move_to([DX, YD, 0]), run_time=0.6)
        until(self, "shows you the result", lead=0.2)
        lx = X0 + a5_w("apply rotation + scale") + 0.6 + 0.35
        self.play(FadeIn(look), step.animate.move_to([lx + a5_w("look", mono=True) + 0.6 + 0.35, YD, 0]), run_time=0.45)
        done(self)


# ── B44 · forbidden downloads and generators; "Say what you could not verify." ──────────────────────────────────
class B44_ForbidAndVerify(Scene):
    def construct(self):
        s0, s1 = A5_SCROLL["B42"], A5_SCROLL["B44"]
        card = a5_card()
        lab = a5_label()
        rows = a5_rows(s0)
        self.add(card, lab, *rows.values())
        rows = a5_scroll(self, rows, s0, s1)
        a5_at(self, A5_B44_T["three-D model downloads"] + 0.27)      # ring lands by "downloads"
        r1 = a5_ring(18, 20, s1)
        dot = Dot(a5_dot_at(18, s1), radius=0.09, color=TERRA)
        self.play(Create(r1), FadeIn(dot), run_time=0.5)
        a5_at(self, A5_B44_T["generation tools"] - 0.2)
        self.play(dot.animate.move_to(a5_dot_at(20, s1)), run_time=0.35)
        a5_at(self, A5_B44_T["say what you could not verify"] - 0.25)
        r2 = a5_ring(22, 22, s1)
        self.play(r1.animate.set_stroke(GHOST, 4), Create(r2), dot.animate.move_to(a5_dot_at(22, s1)), run_time=0.5)
        done(self)


# ── B45 · tool names drift: 2.1.1 vs 2.1.9 ────────────────────────────────────────────────────────────────────────
class B45_ToolNamesDrift(Scene):
    def construct(self):
        LX, RX = -6.0, 0.5
        ys = [1.55, 0.95, 0.35, -0.25, -0.85, -1.45]
        YE = -2.05                                          # "…": both lists go on (36 tools in the 27 Sept code, nine in the 2.1.9 README)
        hl = VGroup(a5_text("2.1.1", LX, 2.62, size=40), a5_text("recorded 27 Sep", LX + 1.3, 2.62))
        hr = VGroup(a5_text("2.1.9", RX, 2.62, size=40), a5_text("6 Oct", RX + 1.35, 2.62))
        rule = Line([-6.1, 2.2, 0], [6.1, 2.2, 0], color=DIM, stroke_width=3)
        shared = ["get_scene_info", "execute_blender_code"]
        left0 = VGroup(*[a5_text(s, LX, ys[i], mono=True) for i, s in enumerate(shared)])
        right0 = VGroup(*[a5_text(s, RX, ys[i], mono=True) for i, s in enumerate(shared)])
        more = VGroup(a5_text("…", LX, YE, mono=True), a5_text("…", RX, YE, mono=True))
        self.add(hl, hr)
        self.play(Create(rule), FadeIn(left0), FadeIn(right0), FadeIn(more), run_time=0.6)
        gone = ["get_object_info", "get_viewport_screenshot", "export_scene"]
        cues = ["get object info", "get viewport screenshot", "export scene"]
        lefts = []
        for i, (s, cue) in enumerate(zip(gone, cues)):
            until(self, cue, lead=0.2)
            t = a5_text(s, LX, ys[2 + i], mono=True)
            lefts.append(t)
            self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.35)
        until(self, "removed all three", lead=0.25)
        xs = VGroup()
        for i in range(3):
            y = ys[2 + i] + 0.1
            xs.add(VGroup(Line([0.8, y - 0.2, 0], [1.2, y + 0.2, 0], color=INK, stroke_width=7),
                          Line([0.8, y + 0.2, 0], [1.2, y - 0.2, 0], color=INK, stroke_width=7)))
        rem = a5_text("removed", 1.65, ys[3])
        self.play(LaggedStart(*[Create(m) for m in xs], lag_ratio=0.25), FadeIn(rem), run_time=0.7)
        until(self, "added a tool called look", lead=0.2)
        lk = a5_text("look", RX, ys[5], mono=True)
        ld = Dot([RX + a5_w("look", mono=True) + 0.35, ys[5] + 0.1, 0], radius=0.09, color=TERRA)
        add = a5_text("added", RX + a5_w("look", mono=True) + 0.75, ys[5])
        self.play(FadeIn(lk, shift=LEFT * 0.2), FadeIn(ld), FadeIn(add), run_time=0.45)
        until(self, "Use whatever your install has", lead=0.2)
        top = ys[0] + a5_m(("M", 32, "get_scene_info"))[2] + 0.25
        bot = YE + a5_m(("M", 32, "…"))[3] - 0.25
        right = RX + a5_w("execute_blender_code", mono=True) + 0.3
        ring = RoundedRectangle(width=right - (RX - 0.25), height=top - bot, corner_radius=0.18, stroke_color=DIM,
                                stroke_width=6, fill_opacity=0).move_to([(right + RX - 0.25) / 2, (top + bot) / 2, 0])
        chk = a5_text("check yours", right - a5_w("check yours"), -3.0)
        self.play(Create(ring), FadeIn(chk), run_time=0.55)
        done(self)


# ── B46 · look yourself, in the viewport ─────────────────────────────────────────────────────────────────────────
class B46_LookYourself(Scene):
    def construct(self):
        chips, sdot = a5_strip("look")
        vp = ImageMobject("pantry/a5_viewport_lantern.png").set_height(4.7).move_to([-3.3, 0.25, 0])
        cap = a5_text("Blender viewport", -5.0, 3.05)
        self.add(chips, sdot, vp, cap)
        q = a5_text("looks right?", 2.9, 2.6, size=40, align="c")
        until(self, "look at it yourself", lead=0.35)
        eye = a5_eye(1.25, 1.1)
        sight = DashedLine([0.3, 1.1, 0], [-1.5, 0.9, 0], color=DIM, stroke_width=4, dash_length=0.12)
        you = a5_text("you", 2.3, 1.0)
        self.play(FadeIn(q), Create(eye), Create(sight), FadeIn(you), run_time=0.6)
        until(self, "in the viewport", lead=0.15)
        frame = RoundedRectangle(width=4.7 * 680 / 930 + 0.24, height=4.7 + 0.24, corner_radius=0.08, stroke_color=DIM,
                                 stroke_width=6, fill_opacity=0).move_to([-3.3, 0.25, 0])
        self.play(Create(frame), run_time=0.45)
        until(self, "after every step", lead=0.2)
        ok = check(4.35, 1.15, s=0.3, color=INK, w=8)
        self.play(Create(ok), run_time=0.35)
        until(self, "Claude can't tell you", lead=0.2)
        cl = a5_text("Claude", 0.75, -0.75)
        qm = a5_text("?", 4.35, -0.85, size=72, align="c")
        self.play(FadeIn(cl), FadeIn(qm, scale=1.3), run_time=0.45)
        done(self)


# ── B47 · one hand edit (illustrative pair) ───────────────────────────────────────────────────────────────────────
class B47_HandEdit(Scene):
    def construct(self):
        chips, sdot = a5_strip("hand edit")
        # crop A: the flame (narrow on purpose: the roof is cut by both edges, so its dark shape is not read as a text run)
        AX, AY, AH = -4.6, 0.5, 4.3
        fa_b = ImageMobject("pantry/a5_hand_before_flame.png").set_height(AH).move_to([AX, AY, 0])
        fa_a = ImageMobject("pantry/a5_hand_after_flame.png").set_height(AH).move_to([AX, AY, 0])
        AW = AH * 310 / 490
        # crop B: the sidebar's Location panel, large enough that its own numbers read
        BX, BY, BW = 2.95, 1.45, 6.0
        BH = BW * 330 / 760
        lb_b = ImageMobject("pantry/a5_hand_before_location.png").set_width(BW).move_to([BX, BY, 0])
        lb_a = ImageMobject("pantry/a5_hand_after_location.png").set_width(BW).move_to([BX, BY, 0])
        ill = a5_text("illustrative", BX + BW / 2 - a5_w("illustrative"), 3.0)
        st_b = a5_text("before", AX - AW / 2, 3.0)
        self.add(chips, sdot, fa_b, lb_b, ill, st_b)
        until(self, "by hand", lead=0.3)
        cx, cy = AX + 0.55, AY - 1.05                       # a mouse pointer, tip just right of the flame
        cur = Polygon([cx, cy, 0], [cx, cy - 0.55, 0], [cx + 0.15, cy - 0.41, 0], [cx + 0.27, cy - 0.65, 0],
                      [cx + 0.37, cy - 0.6, 0], [cx + 0.25, cy - 0.36, 0], [cx + 0.45, cy - 0.36, 0], fill_color=CARD,
                      fill_opacity=1, stroke_color=INK, stroke_width=4).set_z_index(5)
        self.play(FadeIn(cur, shift=UP * 0.3 + LEFT * 0.3), run_time=0.4)
        # the three kinds of hand edit, as the voice lists them
        OX = -2.85
        opts = {}
        for name, cue, y in (("move", "move a part", 1.55), ("scale", "scale it", 0.5), ("colour", "change a colour", -0.55)):
            until(self, cue, lead=0.2)
            opts[name] = a5_chip(name, OX, y, h=0.9)
            self.play(FadeIn(opts[name], shift=RIGHT * 0.15), run_time=0.3)
        # the illustrative edit itself: the flame moved up 0.02 m and turned blue (after the clip's midpoint)
        until(self, "Write down what you changed", lead=0.35)
        st_a = a5_text("after", AX - AW / 2, 3.0)
        zdot = Dot([BX + BW / 2 + 0.2, BY + BH / 2 - 0.84 * BH, 0], radius=0.09, color=TERRA).set_z_index(5)
        ticks = VGroup(*[check(OX + a5_w(n) + 0.6 + 0.35, y + 0.05, s=0.24, color=INK, w=7)
                         for n, y in (("move", 1.55), ("colour", -0.55))])
        self.play(FadeOut(fa_b), FadeIn(fa_a), FadeOut(lb_b), FadeIn(lb_a), FadeOut(st_b), FadeIn(st_a),
                  cur.animate.shift(UP * 0.25), FadeIn(zdot), Create(ticks), run_time=0.6)
        until(self, "what you changed", lead=0.05)
        NX = BX - BW / 2 + 0.3
        note = RoundedRectangle(width=BW, height=1.95, corner_radius=0.15, fill_color="#FFFFFF", fill_opacity=1,
                                stroke_color=DIM, stroke_width=3).move_to([BX, -0.95, 0])
        nh = a5_text("notes", NX, -0.43)
        n1 = a5_text("flame: up 0.02 m, now blue", NX, -1.05)
        self.play(FadeIn(note), FadeIn(nh), FadeIn(n1), run_time=0.45)
        until(self, "what it taught you", lead=0.2)
        n2 = a5_text("learned:", NX, -1.65)
        blank = Line([NX + a5_w("learned:") + 0.35, -1.68, 0], [BX + BW / 2 - 0.3, -1.68, 0], color=DIM, stroke_width=3)
        self.play(FadeIn(n2), Create(blank), run_time=0.5)
        done(self)


# ── B49 · save the .blend; .blend1 is Blender's previous save; keep it out of git ─────────────────────────────────
class B49_BlendAndBackup(Scene):
    def construct(self):
        chips, sdot = a5_strip("save")
        LX = -6.0
        ys = [1.95 - 0.47 * i for i in range(9)]
        cmd = a5_text("$ ls -1 *.blend *.blend1 *.glb", LX, 2.62, mono=True)
        rows = VGroup(*[a5_text(s, LX, ys[i], mono=True) for i, s in enumerate(A5_LS)])
        self.add(chips, sdot, cmd, rows)
        TX = LX + a5_w("lantern.blend1", mono=True) + 0.45
        until(self, "dot blend source", lead=0.3)
        ticks = VGroup(*[check(TX + 0.2, ys[i] + 0.12, s=0.24, color=INK, w=7) for i in (0, 3, 6)])
        src = a5_text("source", TX + 0.8, ys[3])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), FadeIn(src), run_time=0.6)
        until(self, "previous saved version", lead=0.3)
        dots = VGroup(*[Dot([TX + 0.2, ys[i] + 0.1, 0], radius=0.09, color=TERRA) for i in (1, 4, 7)])
        prev = a5_text("previous save", TX + 0.8, ys[7])
        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.2), FadeIn(prev), run_time=0.55)
        until(self, "named dot blend one", lead=0.2)
        gx = 2.15
        gcard = RoundedRectangle(width=4.0, height=2.95, corner_radius=0.15, fill_color="#FFFFFF", fill_opacity=1,
                                 stroke_color=DIM, stroke_width=3).move_to([gx + 1.85, 0.3, 0])
        gsep = Line([gx - 0.15, 1.2, 0], [gx + 3.85, 1.2, 0], color=DIM, stroke_width=2)
        gname = a5_text(".gitignore", gx + 0.2, 1.38, mono=True)
        g1 = a5_text(".godot/", gx + 0.2, 0.5, mono=True)
        g2 = a5_text("*.blend1", gx + 0.2, -0.45, mono=True)
        self.play(FadeIn(gcard), Create(gsep), FadeIn(gname), FadeIn(g1), FadeIn(g2), run_time=0.5)
        until(self, "Don't commit that", lead=0.25)
        top = -0.45 + a5_m(("M", 32, "*.blend1"))[2] + 0.25
        bot = -0.45 + a5_m(("M", 32, "*.blend1"))[3] - 0.25
        right = gx + 0.2 + a5_w("*.blend1", mono=True) + 0.25
        ring = RoundedRectangle(width=right - (gx - 0.05), height=top - bot, corner_radius=0.14, stroke_color=DIM,
                                stroke_width=6, fill_opacity=0).move_to([(right + gx - 0.05) / 2, (top + bot) / 2, 0])
        nc = a5_text("not committed", gx + 1.85, -1.65, align="c")
        self.play(Create(ring), FadeIn(nc), run_time=0.45)
        done(self)


# ══════════════════════════════ scenes_act6.py ══════════════════════════════
"""ACT VI · Export, Import, Check  (B50–B60, all Manim)

The act's worked example, and nearly everything on screen is a real record:
  B50  Blender 5.1.2's own glTF export dialog (pantry/ev_bl_export_gltf.png), pushed into its options (pantry/a6_export_opts.png).
  B51  axes drawn as an idea; the lantern's numbers are real (Blender sidebar 0.3/0.3/0.5; Godot check, +Y Up on and off).
  B52  Blender's own File > Export submenu, captured for this act (evidence/act6/run_file_export.sh -> pantry/a6_bl_file_export.png,
       crops pantry/a6_file_menu.png, a6_export_submenu.png); the exporter call is build_lantern.py line 119, wrapped at its commas.
  B53  the real `ls` and `godot --headless --path godot --import` output (evidence/act6/a6_*.log, drawn by make_terminals.py), then the
       real Godot render of the scene (pantry/ev_godot_showcase_crop.png).
  B54  the real check output, every line (evidence/act6/a6_check.log -> pantry/a6_term_check.png); dots land on what is spoken.
Gate notes (pre-checked with type_check.py / final_frame_check.py functions on 1080p and 1620p renders): at the 50% and 85% samples
every capture sits INSIDE the title-safe box (no camera crop past the frame: Gate V edge-bleed), and a capture whose dark UI greys fall
inside GATE T's ink tolerance is shown only where it forms one large panel (B50) or is replaced at the midpoint by a tighter crop of
its own pixels (B52 submenu, B57 status bar); each midpoint carries at least one INK label on the cream.
  B55  a drawn table of real numbers (assets/ASSETS.md, the check's BRIEF, a6_check.log).
  B56  the real gap values and the origin check's real verdict (evidence/godot/demo_iii_*.log).
  B57  Blender's status bar with Scene Statistics (pantry/ev_bl_status_stats.png), then the three real triangle counts against 500.
  B58  a recorded case from the course's own example run (examples/03-blender-mcp-to-godot: logs/verify1-test_checkpoint_post.log,
       logs/verify1-independent.log), drawn to scale in a side view.
  B59  the real lantern renders (back, below) and the real Godot render.
  B60  the real x10 demonstration (evidence/godot/demo_iv_lantern_x10.log) against the good check, and the assignment's own example
       commit message, labelled as an example.
Cues use the measured audio: word start times from faster-whisper (evidence/act6/whisper_words.log), via a6_at().
Cast: the lantern is the act's recurring object (B50-B55, B57, B59, B60); the crate carries the origin demonstrations (B56, as in the
real runs); B58's post is a different, labelled, recorded case.
"""


def a6_at(self, t):
    """Wait until t seconds into the beat (t = a word's start in the measured audio, evidence/act6/whisper_words.log)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a6_place(w_px, h_px, width, center):
    """Pixel (origin top-left) -> scene point, for an image w_px x h_px drawn `width` units wide at `center` (its rest state)."""
    k = width / float(w_px)
    cx, cy = center
    return lambda px, py: np.array([cx + (px - w_px / 2.0) * k, cy - (py - h_px / 2.0) * k, 0.0])


def a6_img(path, width, center):
    return ImageMobject(path).set_width(width).move_to([center[0], center[1], 0])


def a6_mono(s, xl, y, size=32, color=INK):
    """Menlo line whose LEFT edge sits at xl (Menlo is about 0.25 units per character at size 32)."""
    return M(s, size, color).move_to([xl + 0.25 * (size / 32.0) * len(s) / 2.0, y, 0])


def a6_cell(x, y, letter, value, w=1.05, h=1.15, strong=False):
    """An outlined cell: axis letter on top, the number under it (no fill behind text)."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_opacity=0, stroke_color=INK if strong else DIM,
                           stroke_width=7 if strong else 4).move_to([x, y, 0])
    a = T(letter, 32, DIM).move_to([x, y + 0.3, 0])
    n = T(value, 42).move_to([x, y - 0.2, 0])
    return VGroup(box, a, n)


# ── B50 · export as a .glb; +Y Up on, by default (carries the act title) ───────────────────────────────────────────────────
class B50_ExportGLB(Scene):
    def construct(self):
        title = T("Export, Import, Check", 40).move_to([-3.75, 3.05, 0])
        W1, C1 = 9.6, (0.9, -0.5)
        pv1 = a6_place(3456, 2006, W1, C1)
        full = a6_img("pantry/ev_bl_export_gltf.png", W1, C1)
        self.add(full, title)
        # 'Export each asset as a G L B': the file the dialog will write, lantern.glb
        a6_at(self, 1.1)
        d_file = Dot(pv1(1290, 1921), radius=0.09, color=TERRA)
        self.play(FadeIn(d_file, scale=0.5), run_time=0.3)
        # 'binary glTF': the options column comes forward (the crop sits exactly on its own pixels, then moves)
        a6_at(self, 2.3)
        cw, ch = 916, 788                                                    # pantry/a6_export_opts.png = (2540, 292) .. (3456, 1080)
        opts = a6_img("pantry/a6_export_opts.png", cw * W1 / 3456.0, pv1(2540 + cw / 2.0, 292 + ch / 2.0)[:2])
        self.add(opts)
        W2, C2 = 6.5, (2.75, -0.3)
        pv2 = a6_place(cw, ch, W2, C2)
        self.play(FadeOut(full), FadeOut(d_file), opts.animate.set_width(W2).move_to([C2[0], C2[1], 0]), run_time=0.9)
        d_fmt = Dot(pv2(150, 51), radius=0.11, color=TERRA)                  # beside Format: glTF Binary (.glb)
        self.play(FadeIn(d_fmt, scale=0.5), run_time=0.3)
        # 'a format Godot reads directly'
        a6_at(self, 3.7)
        gd = ImageMobject("pantry/ev_icon_godot.png").set_height(1.45).move_to([-4.3, 1.3, 0])
        gl = T("Godot", 36).move_to([-4.3, 0.2, 0])
        arr = Arrow(pv2(0, 51) + np.array([-0.25, 0.0, 0]), [-3.35, 1.45, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(GrowArrow(arr), FadeIn(gd), FadeIn(gl), run_time=0.7)
        # 'the plus Y up option should be on'
        a6_at(self, 7.15)
        self.play(d_fmt.animate.move_to(pv2(330, 551)), run_time=0.5)      # beside the +Y Up checkbox, ticked
        # 'It is by default'
        a6_at(self, 9.05)
        lab = T("on by default", 36).move_to([-3.5, pv2(330, 551)[1], 0])
        self.play(FadeIn(lab), run_time=0.4)
        done(self)


# ── B51 · Blender is Z-up; glTF and Godot are Y-up; the exporter turns the world ────────────────────────────────────────────
def a6_gizmo(o, kind):
    """Three axes at o. kind 'blender': X right-front, Y into the screen (dim), Z up (returned separately).
    kind 'godot': X right-front, Z toward you (left-front), Y up (returned separately)."""
    o = np.array([o[0], o[1], 0.0], dtype=float)
    ax = Arrow(o, o + np.array([1.3, -0.55, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.18)
    lx = T("X", 34).move_to(o + np.array([1.62, -0.62, 0]))
    if kind == "blender":
        side = Arrow(o, o + np.array([0.95, 0.55, 0]), buff=0, color=DIM, stroke_width=5, tip_length=0.18)
        ls = T("Y", 34, DIM).move_to(o + np.array([1.22, 0.78, 0]))
        up_l = "Z"
    else:
        side = Arrow(o, o + np.array([-1.3, -0.55, 0]), buff=0, color=DIM, stroke_width=5, tip_length=0.18)
        ls = T("Z", 34, DIM).move_to(o + np.array([-1.62, -0.62, 0]))
        up_l = "Y"
    up = Arrow(o, o + np.array([0.0, 1.6, 0]), buff=0, color=INK, stroke_width=7, tip_length=0.24)
    lu = T(up_l + " up", 36).move_to(o + np.array([0.75, 1.55, 0]))
    return VGroup(ax, lx, side, ls), VGroup(up, lu)


class B51_YUp(Scene):
    def construct(self):
        O1, O2 = (-3.55, 0.35), (3.45, 0.35)
        hb = Group(ImageMobject("pantry/ev_icon_blender.png").set_height(0.75).move_to([-4.85, 2.85, 0]),
                   T("Blender", 36).move_to([-3.55, 2.85, 0]))
        base1, up1 = a6_gizmo(O1, "blender")
        self.add(hb, base1)
        # 'Blender's Z axis points up'
        a6_at(self, 0.85)
        self.play(GrowArrow(up1[0]), FadeIn(up1[1]), run_time=0.6)
        # its numbers: the sidebar's dimensions of the lantern, 0.3 / 0.3 / 0.5 m (height on Z)
        yb = -1.5
        c1 = VGroup(a6_cell(-4.75, yb, "x", "0.3"), a6_cell(-3.55, yb, "y", "0.3"), a6_cell(-2.35, yb, "z", "0.5", strong=True))
        self.play(FadeIn(c1), run_time=0.4)
        # 'and in glTF and Godot'
        a6_at(self, 2.5)
        hg = Group(ImageMobject("pantry/ev_icon_godot.png").set_height(0.75).move_to([1.9, 2.85, 0]),
                   T("glTF · Godot", 36).move_to([3.75, 2.85, 0]))
        base2, up2 = a6_gizmo(O2, "godot")
        self.play(FadeIn(hg), FadeIn(base2), run_time=0.5)
        a6_at(self, 3.1)
        self.play(GrowArrow(up2[0]), FadeIn(up2[1]), run_time=0.55)
        # 'The exporter turns the world on the way out': +Y Up, and the 0.5 moves from Z to Y
        a6_at(self, 5.1)
        turn = CurvedArrow(np.array([-1.15, 1.0, 0]), np.array([1.15, 1.0, 0]), angle=-PI / 2.2, color=INK, stroke_width=5, tip_length=0.2)
        tl = T("+Y Up", 38).move_to([0.0, 1.95, 0])
        self.play(Create(turn), FadeIn(tl), run_time=0.45)
        xs = [2.3, 3.5, 4.7]
        on_l = T("+Y Up on", 32).move_to([0.75, yb, 0])
        boxes = VGroup(*[RoundedRectangle(width=1.05, height=1.15, corner_radius=0.16, fill_opacity=0, stroke_color=INK if i == 1 else DIM,
                                          stroke_width=7 if i == 1 else 4).move_to([x, yb, 0]) for i, x in enumerate(xs)])
        letters = VGroup(*[T(a, 32, DIM).move_to([x, yb + 0.3, 0]) for a, x in zip("xyz", xs)])
        self.play(Create(boxes), FadeIn(letters), FadeIn(on_l), run_time=0.35)
        mv = [c1[0][2].copy(), c1[2][2].copy(), c1[1][2].copy()]        # x 0.3 -> X, z 0.5 -> Y, y 0.3 -> Z
        self.play(*[MoveAlongPath(m, ArcBetweenPoints(m.get_center(), np.array([x, yb - 0.2, 0]), angle=-PI / 4))
                    for m, x in zip(mv, xs)], run_time=0.75)
        # +Y Up off: the same lantern measures (0.3, 0.3, 0.5): its height lies on Z
        yo = -2.7
        off = VGroup(T("+Y Up off", 32).move_to([0.75, yo, 0]),
                     a6_cell(2.3, yo, "x", "0.3", h=1.0), a6_cell(3.5, yo, "y", "0.3", h=1.0), a6_cell(4.7, yo, "z", "0.5", h=1.0, strong=True))
        for c in off[1:]:
            c[1].shift(UP * -0.03); c[2].shift(UP * 0.05)
        self.play(FadeIn(off), run_time=0.35)
        done(self)


# ── B52 · no export tool: Blender's own File > Export > glTF 2.0, or the exporter as code, saved ──────────────────────────────
class B52_TwoRoutes(Scene):
    def construct(self):
        hdr = T("version 2.1.9", 34).move_to([-4.5, 2.85, 0])          # mcp-for-blender 2.1.9 (6 Oct)
        self.add(hdr)
        # 'The newer add-on has no export tool'
        a6_at(self, 0.45)
        slot = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.18, stroke_color=DIM, stroke_width=5,
                                fill_opacity=0).move_to([-4.5, 1.95, 0])              # an empty slot: no export tool
        none_l = T("no export tool", 34).move_to([-4.5, 1.05, 0])
        self.play(Create(slot), run_time=0.6)
        self.play(FadeIn(none_l), run_time=0.35)
        # 'So use Blender's own File, Export, glTF 2.0'  (Blender's own window, the submenu open; nothing is clicked in it)
        a6_at(self, 2.35)
        W, C = 9.0, (1.7, -0.25)
        pv = a6_place(1800, 1330, W, C)
        menu = a6_img("pantry/a6_file_menu.png", W, C)
        self.play(FadeIn(menu, shift=LEFT * 0.3), run_time=0.5)
        a6_at(self, 3.2)
        dot = Dot(pv(224, 52), radius=0.1, color=TERRA)                       # between File and Edit
        self.play(FadeIn(dot, scale=0.5), run_time=0.25)
        a6_at(self, 3.92)
        self.play(dot.animate.move_to(pv(388, 1268)), run_time=0.35)         # after "Export"
        # 'glTF 2.0': in to the submenu (a tighter crop of the same capture, laid on its own pixels, then enlarged)
        a6_at(self, 4.28)
        sw, sh = 916, 812                                                     # pantry/a6_export_submenu.png = (862, 500) .. (1778, 1312)
        sub = a6_img("pantry/a6_export_submenu.png", sw * W / 1800.0, pv(862 + sw / 2.0, 500 + sh / 2.0)[:2])
        self.add(sub)
        W2, C2 = 6.4, (2.75, -0.15)
        ps = a6_place(sw, sh, W2, C2)
        fe = T("File › Export", 34).move_to([-4.5, -0.6, 0])
        self.play(FadeOut(menu), FadeOut(dot), sub.animate.set_width(W2).move_to([C2[0], C2[1], 0]), FadeIn(fe), run_time=0.6)
        gdot = Dot(ps(530, 768), radius=0.11, color=TERRA)                   # after "glTF 2.0 (.glb/.gltf)"
        self.play(FadeIn(gdot, scale=0.5), run_time=0.25)
        # 'or have Claude run the exporter through execute Blender code'
        a6_at(self, 6.2)
        self.play(FadeOut(sub), FadeOut(gdot), FadeOut(fe), FadeOut(hdr), FadeOut(slot), FadeOut(none_l), run_time=0.35)
        cap = T("the exporter, in Python", 34).move_to([-3.1, 2.75, 0])
        code = ["bpy.ops.export_scene.gltf(", "    filepath=path,", "    export_format='GLB',", "    export_yup=True,",
                "    use_selection=True)"]
        rows = VGroup(*[a6_mono(s, -5.9, 1.9 - 0.55 * i) for i, s in enumerate(code)])
        self.play(FadeIn(cap), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.75)
        yup = Dot([-5.9 + 0.25 * 20 + 0.3, 1.9 - 0.55 * 3, 0], radius=0.09, color=TERRA)   # beside export_yup=True (B50's +Y Up)
        self.play(FadeIn(yup, scale=0.5), run_time=0.25)
        a6_at(self, 7.85)
        tool = a6_mono("execute_blender_code", 1.15, 0.85)
        tnote = T("documented, not run", 32).move_to([3.65, 0.2, 0])
        self.play(FadeIn(tool, shift=LEFT * 0.15), FadeIn(tnote), run_time=0.45)
        # 'and save that code too': it goes into the asset's build script
        a6_at(self, 9.0)
        page = VGroup(Polygon([-5.75, -1.25, 0], [-5.2, -1.25, 0], [-4.98, -1.47, 0], [-4.98, -2.3, 0], [-5.75, -2.3, 0],
                              fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                      Line([-5.2, -1.25, 0], [-5.2, -1.47, 0], color=INK, stroke_width=3),
                      Line([-5.2, -1.47, 0], [-4.98, -1.47, 0], color=INK, stroke_width=3))
        fname = a6_mono("build_lantern.py", -4.55, -1.78)
        ghost = rows.copy()
        self.play(FadeIn(page), FadeIn(fname), run_time=0.35)
        self.play(ghost.animate.scale(0.12).move_to([-5.37, -1.85, 0]).set_opacity(0), run_time=0.6)
        done(self)


# ── B53 · the three files into the project, import; the small scene, in Godot ──────────────────────────────────────────────
class B53_IntoGodot(Scene):
    def construct(self):
        WT, CT = 8.4, (-1.5, 0.15)
        pt = a6_place(1797, 996, WT, CT)
        row = lambda i: 129 + 62 * i                                         # pantry/a6_term_import.png row centres (terminals.json)
        term = a6_img("pantry/a6_term_import.png", WT, CT)
        self.add(term)
        # 'Put the three files inside your Godot project'
        a6_at(self, 0.3)
        d = Dot(pt(44 + 24.078 * 8 + 60, row(1)), radius=0.08, color=TERRA)  # after coin.glb
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        self.play(d.animate.move_to(pt(44 + 24.078 * 9 + 60, row(2))), run_time=0.3)
        self.play(d.animate.move_to(pt(44 + 24.078 * 11 + 60, row(3))), run_time=0.3)
        # 'and import'
        a6_at(self, 2.15)
        self.play(d.animate.move_to(pt(44 + 24.078 * 40 + 60, row(4))), run_time=0.35)
        ys = [pt(0, row(i))[1] for i in (7, 9, 11)]
        checks = VGroup(*[check(3.25, y + 0.05, s=0.17) for y in ys])
        imp = T("imported", 34).move_to([4.75, ys[1], 0])
        self.play(LaggedStart(*[Create(c) for c in checks], lag_ratio=0.3), FadeIn(imp), run_time=0.7)
        # 'Then build the small scene: a floor': the real Godot render of it
        a6_at(self, 4.93)
        W, C = 9.0, (1.3, -0.15)
        pg = a6_place(1600, 900, W, C)
        shot = a6_img("pantry/ev_godot_showcase_crop.png", W, C)
        gi = ImageMobject("pantry/ev_icon_godot.png").set_height(1.2).move_to([-4.75, 0.6, 0])
        gv = T("Godot 4.7.2", 32).move_to([-4.75, -0.4, 0])
        self.play(FadeOut(term), FadeOut(d), FadeOut(checks), FadeOut(imp), FadeIn(shot), FadeIn(gi), FadeIn(gv), run_time=0.4)
        fp = pg(150, 820)
        fl = T("floor", 34).move_to([fp[0], 2.82, 0])
        fld = Dot(fp, radius=0.09, color=TERRA)
        fll = Line([fp[0], 2.35, 0], fp + np.array([0, 0.14, 0]), color=INK, stroke_width=4)
        self.play(FadeIn(fl), Create(fll), FadeIn(fld), run_time=0.35)
        # 'a light': the shadows it casts
        a6_at(self, 5.62)
        lp = pg(1240, 632)
        ll = T("light", 34).move_to([lp[0], 2.82, 0])
        lld = Dot(lp, radius=0.09, color=TERRA)
        lll = Line([lp[0], 2.35, 0], lp + np.array([0, 0.14, 0]), color=INK, stroke_width=4)
        self.play(FadeIn(ll), Create(lll), FadeIn(lld), run_time=0.35)
        # 'a camera': this picture is its view
        a6_at(self, 6.0)
        x0, x1, y0, y1 = C[0] - W / 2 - 0.15, C[0] + W / 2 + 0.15, C[1] - W * 900 / 1600 / 2 - 0.15, C[1] + W * 900 / 1600 / 2 + 0.15
        L = 0.45
        brk = VGroup(*[VGroup(Line([x, y, 0], [x + sx * L, y, 0], color=INK, stroke_width=6), Line([x, y, 0], [x, y + sy * L, 0], color=INK, stroke_width=6))
                       for x, y, sx, sy in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]])
        cl = T("camera", 34).move_to([5.25, 2.82, 0])
        self.play(Create(brk), FadeIn(cl), run_time=0.4)
        # 'and the three assets side by side at game scale'
        a6_at(self, 6.6)
        names = [("crate", 585), ("lantern", 1060), ("coin", 1340)]
        labs = [T(n, 34).move_to([pg(px, 0)[0], -3.05, 0]) for n, px in names]
        for lb in labs:
            self.play(FadeIn(lb, shift=UP * 0.1), run_time=0.3)
        done(self)


# ── B54 · the headless check: the real command and every line it printed ───────────────────────────────────────────────────
class B54_CheckByNumber(Scene):
    def construct(self):
        W, C = 10.6, (0.0, -0.35)
        pv = a6_place(2375, 1368, W, C)
        col = lambda c: 44 + 24.078 * c                                     # pantry/a6_term_check.png (evidence/act6/terminals.json)
        row = lambda i: 129 + 62 * i
        term = a6_img("pantry/a6_term_check.png", W, C)
        self.add(term)
        # 'Ask Claude Code to write a short headless script'
        a6_at(self, 1.45)
        cap = T("headless check", 34).move_to([-3.95, 3.1, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.4)
        # 'one that runs with no window': --headless
        a6_at(self, 4.15)
        hd = Dot(pv(col(24.5), row(0) - 46), radius=0.08, color=TERRA)       # just above "--headless"
        self.play(FadeIn(hd, scale=0.5), run_time=0.3)
        # 'It loads each asset and prints its bounding box size'
        a6_at(self, 7.15)
        bb = [5, 10, 15]
        dots = VGroup(*[Dot(pv(col(0.8), row(i)), radius=0.08, color=TERRA) for i in bb])
        self.play(FadeOut(hd), FadeIn(dots, scale=0.5), run_time=0.3)
        # 'its node scale'
        a6_at(self, 8.6)
        self.play(*[d.animate.move_to(pv(col(0.8), row(i + 1))) for d, i in zip(dots, bb)], run_time=0.4)
        # 'and the axis it stands along': the end of each size line, 'longest axis ... | height (Y) ...'
        a6_at(self, 9.62)
        ends = [87 + 1.6, 83 + 1.6, 87 + 1.6]                                  # the three size lines are 87, 83, 87 characters
        self.play(*[d.animate.move_to(pv(col(c), row(i))) for d, i, c in zip(dots, bb, ends)], run_time=0.45)
        done(self)


# ── B55 · compare: brief, Blender's sidebar, Godot's box, node scale ─────────────────────────────────────────────────────────
A6_COLS = {"asset": -5.3, "brief": -3.1, "blender": 0.15, "godot": 3.15, "scale": 5.55}
A6_DX = {"blender": 0.85, "godot": 1.0, "scale": 0.4}
A6_ROWS = {"crate": 0.55, "lantern": -0.55, "coin": -1.65}
A6_VALS = {   # brief w x d x h (check_assets.gd BRIEF) | Blender sidebar x y z (assets/ASSETS.md) | Godot box x y z (a6_check.log)
    "crate":   ("0.8 × 0.8 × 0.8", ("0.8", "0.8", "0.8"), ("0.8", "0.8", "0.8")),
    "lantern": ("0.3 × 0.3 × 0.5", ("0.3", "0.3", "0.5"), ("0.3", "0.5", "0.3")),
    "coin":    ("0.3 × 0.3 × 0.04", ("0.3", "0.3", "0.04"), ("0.3", "0.04", "0.3")),
}


def a6_triple(vals, x, y, dx, size=34):
    return VGroup(*[T(v, size).move_to([x + (i - 1) * dx, y, 0]) for i, v in enumerate(vals)])


class B55_Compare(Scene):
    def construct(self):
        hy, sy = 2.15, 1.5
        C, D = A6_COLS, A6_DX
        H = {"brief": VGroup(T("brief", 34).move_to([C["brief"], hy, 0]), T("w × d × h, m", 32, DIM).move_to([C["brief"], sy, 0]))}
        for k, name in (("blender", "Blender"), ("godot", "Godot box"), ("scale", "scale")):
            H[k] = VGroup(T(name, 34).move_to([C[k], hy, 0]), *[T(c, 32, DIM).move_to([C[k] + (i - 1) * D[k], sy, 0]) for i, c in enumerate("xyz")])
        names = VGroup(*[T(n, 36).move_to([C["asset"], y, 0]) for n, y in A6_ROWS.items()])
        rules = VGroup(*[Line([-6.2, y, 0], [6.2, y, 0], color=GHOST, stroke_width=3) for y in (1.05, 0.0, -1.1)])
        cols = {"brief": VGroup(*[T(A6_VALS[n][0], 32).move_to([C["brief"], y, 0]) for n, y in A6_ROWS.items()]),
                "blender": VGroup(*[a6_triple(A6_VALS[n][1], C["blender"], y, D["blender"]) for n, y in A6_ROWS.items()]),
                "godot": VGroup(*[a6_triple(A6_VALS[n][2], C["godot"], y, D["godot"]) for n, y in A6_ROWS.items()])}
        self.add(names, H["godot"], cols["godot"])
        # 'Compare those numbers with your brief'
        a6_at(self, 0.25)
        self.play(Create(rules), run_time=0.5)
        a6_at(self, 1.05)
        self.play(FadeIn(H["brief"]), FadeIn(cols["brief"], shift=RIGHT * 0.15), run_time=0.45)
        # 'and with the dimensions in Blender's sidebar'
        a6_at(self, 2.0)
        self.play(FadeIn(H["blender"]), FadeIn(cols["blender"], shift=RIGHT * 0.15), run_time=0.45)
        # the lantern row, the one this act follows: Blender 0.3 0.3 0.5 = Godot 0.3 0.5 0.3 (the height moved from Z to Y)
        a6_at(self, 3.15)
        ld = Dot([-6.2, A6_ROWS["lantern"], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(ld, scale=0.5), run_time=0.3)
        # 'The node scale should be one, one, one'  (the check printed (1.0, 1.0, 1.0) for all three)
        a6_at(self, 4.25)
        sc = [VGroup(*[T("1", 34).move_to([C["scale"] + (i - 1) * D["scale"], y, 0]) for y in A6_ROWS.values()]) for i in range(3)]
        self.play(FadeIn(H["scale"]), run_time=0.3)
        for t, s_ in zip((5.2, 5.65, 6.0), sc):
            a6_at(self, t)
            self.play(FadeIn(s_, shift=DOWN * 0.1), run_time=0.25)
        # 'Each asset should stand upright': every height sits on Godot's Y
        a6_at(self, 6.6)
        ring = RoundedRectangle(width=1.04, height=2.95, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=7).move_to([C["godot"], -0.55, 0])
        upl = T("height on Y", 32).move_to([C["godot"], -2.55, 0])
        self.play(Create(ring), FadeIn(upl), run_time=0.5)
        done(self)


# ── B56 · sit, sink or float: the origin; moving the node hides it ────────────────────────────────────────────────────────────
A6_U = 1.5                                                                    # scene units per metre (the crate is 0.8 m = 1.2 units)


def a6_crate(cx, bottom):
    s = 0.8 * A6_U
    body = Square(side_length=s, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([cx, bottom + s / 2, 0])
    band_lo = Line([cx - s / 2, bottom + 0.15, 0], [cx + s / 2, bottom + 0.15, 0], color=BOX_FLOOR, stroke_width=6)
    band_hi = Line([cx - s / 2, bottom + s - 0.15, 0], [cx + s / 2, bottom + s - 0.15, 0], color=BOX_FLOOR, stroke_width=6)
    return VGroup(body, band_lo, band_hi)


class B56_SitSinkFloat(Scene):
    def construct(self):
        fy = 0.0
        floor = Line([-6.1, fy, 0], [6.1, fy, 0], color=DIM, stroke_width=8)
        self.add(floor)
        xs = [-4.0, 0.0, 4.0]
        # base origin (gap 0.0) | centre origin at floor level (gap -0.4) | centre origin, node lifted 0.5 by a guess (gap 0.1)
        bottoms = [fy, fy - 0.4 * A6_U, fy + 0.1 * A6_U]
        crates = [a6_crate(x, b) for x, b in zip(xs, bottoms)]
        origins = [Dot([xs[0], fy, 0], radius=0.11, color=TERRA), Dot([xs[1], fy, 0], radius=0.11, color=TERRA),
                   Dot([xs[2], fy + 0.5 * A6_U, 0], radius=0.11, color=TERRA)]
        # 'Place each asset on the floor without moving it'
        a6_at(self, 0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in crates], lag_ratio=0.25), run_time=1.0)
        a6_at(self, 1.5)
        self.play(*[FadeIn(o, scale=0.5) for o in origins], run_time=0.35)
        # 'Does it sit, sink or float?'  (gap to floor, from the real check runs)
        words = [("sits", "gap 0.0 m", 2.55), ("sinks", "gap -0.4 m", 3.0), ("floats", "gap 0.1 m", 3.45)]
        tops = []
        for x, (w, g, t) in zip(xs, words):
            a6_at(self, t)
            grp = VGroup(T(w, 38).move_to([x, 2.75, 0]), T(g, 34).move_to([x, 2.15, 0]))
            tops.append(grp)
            self.play(FadeIn(grp, shift=DOWN * 0.1), run_time=0.3)
        guess = T("node lifted 0.5", 32).move_to([xs[2], -0.6, 0])
        self.play(FadeIn(guess), run_time=0.25)
        # 'Move the node to compensate': lift the sinking crate by exactly 0.4 m
        a6_at(self, 5.5)
        self.play(VGroup(crates[1], origins[1]).animate.shift(UP * 0.4 * A6_U), run_time=0.7)
        new = VGroup(T("sits", 38).move_to([xs[1], 2.75, 0]), T("gap 0.0 m", 34).move_to([xs[1], 2.15, 0]))
        self.play(FadeOut(tops[1]), FadeIn(new), run_time=0.3)
        # 'and you've hidden the problem': the origin check's real verdict
        a6_at(self, 6.95)
        oc = T("origin check", 34).move_to([-4.7, -1.4, 0])
        v = ["FAIL crate_origin_centre.glb: the origin is", "0.4 m above the base: it sits on the floor", "only because the node was moved"]
        vr = VGroup(*[a6_mono(s, -5.4, -2.0 - 0.5 * i) for i, s in enumerate(v)])
        ring = Circle(radius=0.3, stroke_color=INK, stroke_width=6).move_to([xs[1], fy + 0.4 * A6_U, 0])        # round the moved origin
        self.play(FadeIn(oc), FadeIn(vr), Create(ring), run_time=0.5)
        done(self)


# ── B57 · triangle count: Blender's status bar, Scene Statistics; each asset against 500 ──────────────────────────────────────
class B57_Triangles(Scene):
    def construct(self):
        W, C = 11.0, (0.0, -0.3)
        pv = a6_place(3456, 2006, W, C)
        win = a6_img("pantry/ev_bl_status_stats.png", W, C)
        self.add(win)
        # 'Right-click Blender's status bar and enable Scene Statistics': the status bar's own pixels, lifted out and enlarged
        a6_at(self, 1.9)
        strip = a6_img("pantry/a6_statusbar.png", 1336 * W / 3456.0, pv(1830 + 668, 1915 + 44.5)[:2])
        self.add(strip)
        SW, SY = 12.2, 0.15
        self.play(FadeOut(win), strip.animate.set_width(SW).move_to([0, SY, 0]), run_time=1.0)
        lab = T("Scene Statistics", 36).move_to([0, 1.25, 0])
        self.play(FadeIn(lab), run_time=0.3)
        a6_at(self, 3.05)
        ks = SW / 1336.0
        td = Dot([(2808 - 2498) * ks, SY - 89 * ks / 2 - 0.32, 0], radius=0.11, color=TERRA)     # under "Tris:202"
        self.play(FadeIn(td, scale=0.5), run_time=0.3)
        # 'Is each asset within your budget?': the strip moves up; three counts against 500
        a6_at(self, 4.95)
        self.play(FadeOut(lab), FadeOut(td), strip.animate.set_width(10.4).move_to([0, 2.8, 0]), run_time=0.6)
        base_y, k = -2.55, 4.0 / 500.0
        axis = Line([-4.4, base_y, 0], [4.4, base_y, 0], color=DIM, stroke_width=5)
        lim = DashedLine([-4.4, base_y + 500 * k, 0], [4.4, base_y + 500 * k, 0], color=INK, stroke_width=5, dash_length=0.3)
        liml = T("500", 40).move_to([5.25, base_y + 500 * k + 0.05, 0])
        limn = T("budget", 32).move_to([5.25, base_y + 500 * k - 0.5, 0])
        self.play(Create(axis), Create(lim), FadeIn(liml), FadeIn(limn), run_time=0.4)
        data = [("crate", 60, -2.7, BAR2), ("lantern", 202, 0.0, BAR1), ("coin", 180, 2.7, BAR2)]
        bars = VGroup(*[Rectangle(width=1.3, height=n * k, fill_color=c, fill_opacity=1, stroke_width=0).move_to([x, base_y + n * k / 2, 0])
                        for _, n, x, c in data])
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=0.5)
        nums = VGroup(*[T(str(n), 40).move_to([x, base_y + n * k + 0.38, 0]) for _, n, x, _ in data])
        names = VGroup(*[T(nm, 34).move_to([x, base_y - 0.45, 0]) for nm, _, x, _ in data])
        ld = Dot([0.75, base_y + 202 * k + 0.38, 0], radius=0.1, color=TERRA)  # beside 202, the count the status bar shows
        self.play(FadeIn(nums), FadeIn(names), FadeIn(ld), run_time=0.35)
        done(self)


# ── B58 · a check can prove less than it claims: the ray stopped on the object's own collider (a recorded case) ──────────────
A6_RU = 1.3                                                                   # units per metre in the side view


def a6_ry(wy):
    """Scene y of world height wy (Godot Y, metres) in the recorded run: the ray starts at -0.2, the floor is at -4.0."""
    return 2.6 + (wy + 0.2) * A6_RU


class B58_RayStops(Scene):
    def construct(self):
        px = -1.2                                                             # the post's axis on screen
        fy = a6_ry(-4.0)
        floor = Line([-5.9, fy, 0], [2.9, fy, 0], color=DIM, stroke_width=8)
        fl = T("floor, y = -4.0", 34).move_to([4.6, fy, 0])
        u = A6_RU
        base = Rectangle(width=0.6 * u, height=0.1 * u, fill_color=BOX_R, fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([px, fy + 0.05 * u, 0])
        pole = Rectangle(width=0.16 * u, height=1.7 * u, fill_color=BOX_L, fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([px, fy + 0.95 * u, 0])
        pen = Rectangle(width=0.4 * u, height=0.25 * u, fill_color=BOX_TOP, fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([px + 0.28 * u, fy + 1.675 * u, 0])
        post = VGroup(pole, pen, base)
        self.add(floor, fl, post)
        # 'Read the check Claude wrote': its own collider, a 0.6 x 1.8 m box
        a6_at(self, 0.35)
        box = Rectangle(width=0.6 * u, height=1.8 * u, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([px, fy + 0.9 * u, 0])
        bl = T("its own collider", 34).move_to([-3.75, fy + 1.0 * u, 0])
        self.play(Create(box), FadeIn(bl), run_time=0.7)
        # 'A check can prove less than it claims': it printed PASS
        a6_at(self, 1.4)
        ck = VGroup(T("the check printed", 34).move_to([2.25, 1.55, 0]), M("PASS", 40).move_to([4.85, 1.55, 0]))
        self.play(FadeIn(ck), run_time=0.4)
        # 'In one recorded case'
        a6_at(self, 3.55)
        rc = T("a recorded case", 36).move_to([3.1, 2.8, 0])
        self.play(FadeIn(rc), run_time=0.4)
        # 'an agent's floor check stopped on the object's own collider'
        a6_at(self, 5.25)
        top = np.array([px, a6_ry(-0.2), 0])
        hit = np.array([px, a6_ry(-2.2), 0])
        ray = Line(top, hit + np.array([0, 0.1, 0]), color=INK, stroke_width=7)
        rl = T("ray", 34).move_to([px + 0.7, a6_ry(-0.2) - 0.3, 0])
        self.play(Create(ray), FadeIn(rl), run_time=0.6)
        hd = Dot(hit, radius=0.12, color=TERRA)
        hl = a6_mono("ray hit at y=-2.2000", 0.85, hit[1])
        self.play(FadeIn(hd, scale=0.5), FadeIn(hl), run_time=0.35)
        a6_at(self, 7.05)
        self.play(Indicate(VGroup(box, bl), color=INK, scale_factor=1.06), run_time=0.6)
        # 'and proved nothing about the floor': the floor under the post was never reached
        a6_at(self, 8.1)
        rest = DashedLine(hit + np.array([0, -0.15, 0]), [px, fy + 0.2, 0], color=DIM, stroke_width=6, dash_length=0.25)
        q = T("?", 64).move_to([px + 1.1, fy + 0.85, 0])
        self.play(Create(rest), run_time=0.5)
        self.play(FadeIn(q, scale=0.6), run_time=0.3)
        done(self)


# ── B59 · the part no number covers: walk the camera round, behind and below; at game size ───────────────────────────────────
class B59_LookYourself(Scene):
    def construct(self):
        H, C = 4.9, (1.4, -0.25)
        views = [ImageMobject(f"pantry/a6_lantern_{v}.png").set_height(H).move_to([C[0], C[1], 0]) for v in ("34", "back", "below")]
        views[1].set_opacity(0); views[2].set_opacity(0)
        orbit = Ellipse(width=5.6, height=1.5, stroke_color=DIM, stroke_width=6).move_to([C[0], C[1] - 2.05, 0])
        self.add(orbit, *views)
        cam = Dot(orbit.point_from_proportion(0.75), radius=0.13, color=TERRA)      # the bottom of the ellipse: in front
        cl = T("you", 34).move_to(orbit.point_from_proportion(0.75) + np.array([0.6, -0.05, 0]))
        # 'Walk the camera around each asset'
        a6_at(self, 1.6)
        self.play(FadeIn(cam, scale=0.5), FadeIn(cl), run_time=0.3)
        self.play(FadeOut(cl), run_time=0.2)
        arc = ArcBetweenPoints(orbit.point_from_proportion(0.75), orbit.point_from_proportion(0.25), angle=-PI * 0.75)
        a6_at(self, 2.2)
        self.play(MoveAlongPath(cam, arc), run_time=1.3)
        # 'including from behind'
        a6_at(self, 3.75)
        bl = T("behind", 36).move_to([-3.6, 1.2, 0])
        self.play(views[1].animate.set_opacity(1), views[0].animate.set_opacity(0), FadeIn(bl), run_time=0.45)
        # 'and from below'
        a6_at(self, 4.4)
        b2 = T("below", 36).move_to([-3.6, 0.3, 0])
        self.play(cam.animate.move_to([C[0], C[1] - 3.05, 0]), views[2].animate.set_opacity(1), views[1].animate.set_opacity(0), FadeIn(b2), run_time=0.5)
        # 'Do the shapes read as what they are at game size?': the lantern among the others, in the game's own render
        a6_at(self, 5.65)
        Wg, Cg = 8.6, (1.85, -0.2)
        pg = a6_place(1600, 900, Wg, Cg)
        shot = a6_img("pantry/ev_godot_showcase_crop.png", Wg, Cg)
        self.play(FadeOut(views[2]), FadeOut(orbit), FadeOut(cam), FadeOut(bl), FadeOut(b2), FadeIn(shot), run_time=0.5)
        gl = T("game size", 36).move_to([-4.4, 1.3, 0])
        self.play(FadeIn(gl), run_time=0.3)
        # 'Are faces missing, or colours wrong?'
        a6_at(self, 7.95)
        fd = Dot(pg(1058, 700), radius=0.1, color=TERRA)                     # the lantern's base
        f1 = T("faces?", 36).move_to([-4.4, 0.2, 0])
        self.play(FadeIn(fd, scale=0.5), FadeIn(f1), run_time=0.3)
        a6_at(self, 9.2)
        f2 = T("colours?", 36).move_to([-4.4, -0.9, 0])
        self.play(fd.animate.move_to(pg(1062, 515)), FadeIn(f2), run_time=0.35)     # the flame
        done(self)


# ── B60 · one revision from something you saw; write the cycle down; keep the failing check ──────────────────────────────────
class B60_Revise(Scene):
    def construct(self):
        # the real lantern render; x10 (the real demonstration: every axis 10x the brief) shrinking to the real 0.5 m
        lx, lb = -3.6, -1.6                                                   # the lantern's foot on screen
        k1 = 0.85 / 787.0                                                     # 787 px of render = the lantern's 0.5 m
        im = ImageMobject("pantry/a6_lantern_34.png").set_height(867 * k1 * 10).move_to([lx + (274 - 274) * k1 * 10, lb + (827 - 433.5) * k1 * 10, 0])
        big_a = Arrow([lx + 3.25, lb, 0], [lx + 3.25, 3.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
        big_l = T("5.0 m", 38).move_to([lx + 2.45, 1.0, 0])
        demo = T("demonstration runs", 32).move_to([3.0, -0.05, 0])
        fail = VGroup(M("FAIL", 32).move_to([0.95, 1.25, 0]), a6_mono("(3.0, 5.0, 3.0)", 1.8, 1.25))
        self.add(im, big_a, big_l)
        # 'from something you saw'
        a6_at(self, 1.1)
        self.play(FadeIn(fail, shift=LEFT * 0.15), FadeIn(demo), run_time=0.35)
        # 'a size you corrected'
        a6_at(self, 2.55)
        w1 = T("size", 36).move_to([1.4, 2.75, 0])
        w1d = Dot([0.75, 2.75, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(w1), FadeIn(w1d, scale=0.5), run_time=0.3)
        self.play(im.animate.scale(0.1, about_point=np.array([lx, lb, 0])), FadeOut(big_a), FadeOut(big_l), run_time=0.7)
        sm_a = dim_arrow([lx + 0.65, lb, 0], [lx + 0.65, lb + 0.85, 0], w=4, tip=0.12)
        sm_l = T("0.5 m", 38).move_to([lx + 1.55, lb + 0.43, 0])
        ok = VGroup(M("PASS", 32).move_to([0.95, 0.6, 0]), a6_mono("(0.3, 0.5, 0.3)", 1.8, 0.6))
        self.play(Create(sm_a), FadeIn(sm_l), FadeIn(ok, shift=LEFT * 0.15), run_time=0.4)
        # 'an origin you moved, a part you rebuilt'
        a6_at(self, 3.85)
        w2 = T("origin", 36).move_to([3.15, 2.75, 0])
        self.play(FadeIn(w2), run_time=0.3)
        a6_at(self, 4.95)
        w3 = T("part", 36).move_to([4.85, 2.75, 0])
        self.play(FadeIn(w3), run_time=0.25)
        # 'Write the cycle down'  (the assignment's own example message)
        a6_at(self, 6.2)
        ml = T("example commit message", 32).move_to([0.0, -2.35, 0])
        msg = a6_mono("Fix lantern height to 0.9 m; origin to base", -5.5, -2.95)
        node = Circle(radius=0.14, stroke_color=INK, stroke_width=5).move_to([-5.85, -2.95, 0])
        self.play(FadeIn(ml), FadeIn(msg), Create(node), run_time=0.45)
        # 'Don't delete a failing assertion to turn a report green': the FAIL stays on the record
        a6_at(self, 7.65)
        ring = RoundedRectangle(width=5.75, height=0.74, corner_radius=0.18, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([3.0, 1.25, 0])
        keep = T("keep it", 34).move_to([5.0, 1.95, 0])
        self.play(Create(ring), FadeIn(keep), run_time=0.45)
        done(self)


# ══════════════════════════════ scenes_act7.py ══════════════════════════════
"""ACT VII · Ship It, and How It's Graded  (B61A–B69; B63 and B64 are Remotion CCPlainShell beats, see lanes/act7.json)

The cast of the act: the FILM (a strip of four frames, B61A), the REAL Godot scene (B61A tile, B61B, B69), the REAL Blender
window (B61A, B62, B68), the REPOSITORY (the terminal in B63/B64), and the GRADE COLUMN 60 / 10 / 10 / 20 (B66, B67).
Every image is a crop of a real capture in pantry/ev_* made by evidence/act7/make_crops.py (no pixel drawn). Numbers on
screen come from evidence/godot/check_good.log, godot/project_src/tests/check_assets.gd (the brief the check compares with,
shown as "example") and the assignment's rubric. The hand-edit pair is made by script and is labelled illustrative.
"""

A7_TILE_W, A7_TILE_H = 2.85, 2.064                        # B61A film frames (crop aspect 1.381)
A7_PIC_W = A7_TILE_W - 0.2                                  # a capture sits 0.1 inside its frame: a cream mount (GATE T samples the ring round a blob)
A7_TILE_X = [-4.575, -1.525, 1.525, 4.575]
A7_TILE_Y = 0.3


def a7_img(path, x, y, w=None, h=None):
    im = ImageMobject(path)
    if w is not None:
        im.set_width(w)
    else:
        im.set_height(h)
    im.move_to([x, y, 0])
    return im


def a7_lbl(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a7_lbl_bl(s, x, y, size=34, color=INK):
    """A centred label on a common BASELINE: invisible bars at both ends give every label the same ascender/descender box."""
    t = T("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x, y, 0])


def a7_lbl_left(s, x, y, size=34, color=INK):
    """A label whose LEFT edge sits at x (computed from the text width, never from get_left())."""
    t = T(s, size, color)
    return t.move_to([x + t.width / 2, y, 0])


def a7_mono_left(s, x, y, size=32, color=INK):
    """Menlo text whose first visible character starts at x, on a common baseline (hidden bars at both ends)."""
    t = M("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x - 0.243 + t.width / 2, y, 0])


def a7_strip():
    """The film: two DIM bands with sprocket holes, separators between four empty frames (the frames are bare stage)."""
    bands = VGroup()
    for yc in (A7_TILE_Y + A7_TILE_H / 2 + 0.22, A7_TILE_Y - A7_TILE_H / 2 - 0.22):
        bands.add(Rectangle(width=12.3, height=0.44, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([0, yc, 0]))
    seps = VGroup(*[Rectangle(width=0.2, height=A7_TILE_H + 0.02, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x, A7_TILE_Y, 0])
                    for x in (-3.05, 0.0, 3.05)])
    caps = VGroup(*[Rectangle(width=0.15, height=A7_TILE_H + 0.02, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x, A7_TILE_Y, 0])
                    for x in (-6.075, 6.075)])
    holes = VGroup()
    for yc in (A7_TILE_Y + A7_TILE_H / 2 + 0.22, A7_TILE_Y - A7_TILE_H / 2 - 0.22):
        for i in range(27):
            holes.add(Rectangle(width=0.17, height=0.15, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([-5.85 + i * 0.45, yc, 0]))
    return VGroup(bands, seps, caps, holes)


# ── B61A · one film: four frames, each from the real evidence ─────────────────────────────────────────────────────────────
class B61A_OneFilm(Scene):
    def construct(self):
        title = T("Ship It, and How It's Graded", 40).move_to([-3.05, 3.05, 0])
        strip = a7_strip()
        self.add(title)
        self.play(FadeIn(strip, shift=LEFT * 0.4), run_time=0.6)
        head = Dot([A7_TILE_X[0], 2.2, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(head), run_time=0.3)
        # frame 1: the game and its three assets, in the running Godot scene
        until(self, "It names", lead=-0.1)
        g = a7_img("pantry/a7_godot_tile2.png", A7_TILE_X[0], A7_TILE_Y, w=A7_PIC_W)
        l1a, l1b = a7_lbl_bl("your game,", A7_TILE_X[0], -1.72), a7_lbl_bl("three assets", A7_TILE_X[0], -2.25)
        self.play(FadeIn(g), FadeIn(l1a), FadeIn(l1b), run_time=0.5)
        # frame 2: the real Blender session
        until(self, "and shows your real Blender", lead=-0.2)
        b = a7_img("pantry/a7_bl_session_tile.png", A7_TILE_X[1], A7_TILE_Y, w=A7_PIC_W)
        l2 = a7_lbl_bl("Blender session", A7_TILE_X[1], -1.72)
        self.play(head.animate.move_to([A7_TILE_X[1], 2.2, 0]), FadeIn(b), FadeIn(l2), run_time=0.5)
        # frame 3: a prompt (the assignment's own words, from its adapted prompt)
        until(self, "with at least one prompt", lead=0.0)
        p = VGroup(*[M(s, 32).move_to([A7_TILE_X[2], A7_TILE_Y + 0.5 - i * 0.5, 0]) for i, s in enumerate(["Do not", "build", "yet."])])
        l3 = a7_lbl_bl("a prompt", A7_TILE_X[2], -1.72)
        self.play(head.animate.move_to([A7_TILE_X[2], 2.2, 0]), FadeIn(p), FadeIn(l3), run_time=0.45)
        # frame 4: the hand edit, before -> after (made by script: illustrative)
        until(self, "and your own hand edit", lead=0.05)
        hb = a7_img("pantry/a7_hand_before_tile.png", A7_TILE_X[3], A7_TILE_Y, w=A7_PIC_W)
        ha = a7_img("pantry/a7_hand_after_tile.png", A7_TILE_X[3], A7_TILE_Y, w=A7_PIC_W)
        l4a, l4b = a7_lbl_bl("hand edit", A7_TILE_X[3], -1.72), a7_lbl_bl("(illustrative)", A7_TILE_X[3], -2.25)
        self.play(head.animate.move_to([A7_TILE_X[3], 2.2, 0]), FadeIn(hb), FadeIn(l4a), FadeIn(l4b), run_time=0.4)
        self.wait(0.15)
        self.play(FadeIn(ha), run_time=0.3)
        done(self)


# ── B61B · the real Godot scene, with the headless numbers beside the brief ─────────────────────────────────────────────────
A7_BRIEF = [("crate", "(0.8, 0.8, 0.8)"), ("lantern", "(0.3, 0.5, 0.3)"), ("coin", "(0.3, 0.04, 0.3)")]     # check_assets.gd BRIEF (Godot X, Y, Z)
A7_HEADLESS = ["(0.8, 0.8, 0.8)", "(0.3, 0.5, 0.3)", "(0.3, 0.04, 0.3)"]                                    # check_good.log, bounding box size


class B61B_GodotNumbers(Scene):
    def construct(self):
        img = a7_img("pantry/a7_godot_lookA_wide.png", A7_TILE_X[0], A7_TILE_Y, h=A7_TILE_H)
        self.add(img)
        self.play(img.animate.set_height(3.49).move_to([-1.2, 1.45, 0]), run_time=0.7)
        until(self, "running Godot scene", lead=0.3)
        g1, g2 = a7_lbl("running", 3.7, 2.35, 36), a7_lbl("Godot scene", 3.7, 1.8, 36)
        spark = Dot([2.55, 2.35, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(g1), FadeIn(g2), FadeIn(spark), run_time=0.4)
        hy = -0.85
        h1 = a7_lbl_bl("brief (example)", -1.5, hy, 34)
        h2 = a7_lbl_bl("headless", 3.15, hy, 34)
        h0 = a7_lbl_bl("in metres", -4.7, hy, 34)
        sep = Line([0.82, -0.55, 0], [0.82, -3.1, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(h0), FadeIn(h1), FadeIn(h2), Create(sep), run_time=0.35)
        rows_y = [-1.55, -2.2, -2.85]
        until(self, "with the headless numbers", lead=0.0)
        for (name, brief), hv, y in zip(A7_BRIEF, A7_HEADLESS, rows_y):
            n = a7_lbl_bl(name, -4.7, y, 36)
            bv = M(brief, 32).move_to([-1.5, y, 0])
            hvm = M(hv, 32).move_to([3.15, y, 0])
            self.play(FadeIn(n), FadeIn(bv), FadeIn(hvm), run_time=0.3)
        until(self, "beside your brief", lead=0.1)
        checks = VGroup(*[check(5.6, y + 0.05, 0.2) for y in rows_y])
        self.play(LaggedStart(*[Create(c) for c in checks], lag_ratio=0.3), run_time=0.6)
        done(self)


# ── B62 · the ledger: checked / uncertain / Claude got wrong / human and AI; then labelled evidence ─────────────────────────
def a7_person(x, y, s=1.0, color=INK):
    head = Circle(radius=0.17 * s, color=color, stroke_width=5).move_to([x, y + 0.2 * s, 0])
    body = Arc(radius=0.34 * s, start_angle=0, angle=PI, color=color, stroke_width=5).move_to([x, y - 0.22 * s, 0])
    return VGroup(head, body)


def a7_cross(x, y, s=0.26, color=INK):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=7),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=7))


def a7_lantern(cx, base_y, u=3.6):
    """The lantern redrawn from its own build numbers (evidence/assets/ASSETS.md), side view: a RECONSTRUCTION."""
    base = Rectangle(width=0.30 * u, height=0.04 * u, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    base.move_to([cx, base_y + 0.02 * u, 0])
    glass = Rectangle(width=0.20 * u, height=0.23 * u, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4)
    glass.move_to([cx, base_y + 0.155 * u, 0])
    flame = Circle(radius=0.06 * u, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([cx, base_y + 0.32 * u, 0])
    roof = Polygon([cx - 0.14 * u, base_y + 0.37 * u, 0], [cx + 0.14 * u, base_y + 0.37 * u, 0], [cx, base_y + 0.47 * u, 0],
                   fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4)
    fin = Rectangle(width=0.04 * u, height=0.03 * u, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=3)
    fin.move_to([cx, base_y + 0.485 * u, 0])
    return VGroup(base, glass, flame, roof, fin)


class B62_Ledger(Scene):
    def construct(self):
        xs = A7_TILE_X
        heads = ["checked", "uncertain", "Claude got wrong", "human / AI"]
        cues = ["It says what you checked", "what's uncertain", "what Claude got wrong", "and who did what"]
        leads = [-0.6, 0.0, 0.0, 0.1]
        for i, (x, hd, cue, ld) in enumerate(zip(xs, heads, cues, leads)):
            until(self, cue, lead=ld)
            cell = RoundedRectangle(width=2.85, height=2.1, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([x, 1.15, 0])
            h = a7_lbl_bl(hd, x, 2.72, 34)
            if i == 0:
                glyph = check(x - 0.05, 1.68, 0.3)
            elif i == 1:
                glyph = T("?", 64).move_to([x, 1.66, 0])
            elif i == 2:
                glyph = a7_cross(x, 1.66)
            else:
                glyph = VGroup(a7_person(x - 0.35, 1.66), Dot([x + 0.45, 1.6, 0], radius=0.15, color=TERRA))
            rows = VGroup(*[Line([x - 1.0, yy, 0], [x + 1.0, yy, 0], color=GHOST, stroke_width=6) for yy in (0.82, 0.45)])
            self.play(Create(cell), FadeIn(h), FadeIn(glyph), Create(rows), run_time=0.45)
        # evidence you made, labelled; a reconstruction, labelled a reconstruction
        until(self, "Use screenshots", lead=0.0)
        shot = a7_img("pantry/a7_bl_view_tile2.png", -3.2, -2.1, h=2.2)
        self.play(FadeIn(shot, shift=UP * 0.2), run_time=0.45)
        until(self, "labelled as such", lead=0.1)
        s_lbl = a7_lbl("screenshot", -3.2, -0.5, 34)
        s_dot = Dot([-4.55, -0.5, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(s_lbl), FadeIn(s_dot), run_time=0.35)
        until(self, "A reconstruction is labelled", lead=0.1)
        frame = RoundedRectangle(width=3.04, height=2.2, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.2, -2.1, 0])
        lan = a7_lantern(3.2, -2.97)
        self.play(Create(frame), LaggedStart(*[FadeIn(p) for p in lan], lag_ratio=0.25), run_time=0.7)
        until(self, "a reconstruction.", lead=0.15)
        r_lbl = a7_lbl("reconstruction", 3.2, -0.5, 34)
        self.play(FadeIn(r_lbl), run_time=0.35)
        done(self)


# ── B65 · the submission note: the assignment's own template, field by field ─────────────────────────────────────────────
A7_FORM = ["…",
           "The three assets and what each is for:",
           "MCP project and version, or \"script route\" …",
           "My hand edit in Blender:",
           "Checks run (command and result):",
           "Final film URL and filename:",
           "Final film SHA-256:",
           "…"]


class B65_SubmissionNote(Scene):
    def construct(self):
        iso = Iso(3.0, 2.3, 0.5)
        box = iso.box(0, 0, 0, 1.0, 1.0, 0.75)
        zl = a7_lbl_left("source zip", 3.95, 2.72, 34)
        self.play(FadeIn(box, shift=DOWN * 0.25), FadeIn(zl), run_time=0.45)
        until(self, "a submission note", lead=0.2)
        fname = a7_mono_left("SUBMISSION.md", -6.0, 2.75)
        tl = a7_lbl_left("the template", -2.45, 2.72, 34)
        page = RoundedRectangle(width=12.2, height=5.45, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0, -0.5, 0])
        ys = [1.72 - i * 0.62 for i in range(len(A7_FORM))]
        rows = [a7_mono_left(s, -5.25, y) for s, y in zip(A7_FORM, ys)]
        self.play(FadeIn(fname), FadeIn(tl), Create(page), FadeIn(rows[0]), FadeIn(rows[-1]), run_time=0.6)
        ptr = Dot([-5.65, ys[1], 0], radius=0.09, color=TERRA)
        # each field lands as it is named; the one terracotta dot points at it ("the film link with its checksum" is one item: both rows)
        steps = [("the three assets", [1], 1, 0.15), ("which route", [2], 2, 0.15), ("your hand edit", [3], 3, 0.15),
                 ("the checks you ran", [4], 4, 0.15), ("and the film link", [5, 6], 5, 0.15), ("checksum", [], 6, 0.3)]
        for k, (cue, new_rows, at, ld) in enumerate(steps):
            until(self, cue, lead=ld)
            anims = [FadeIn(rows[r], shift=RIGHT * 0.15) for r in new_rows]
            anims.append(FadeIn(ptr, scale=1.6) if k == 0 else ptr.animate.move_to([-5.65, ys[at], 0]))
            self.play(*anims, run_time=0.3)
        done(self)


# ── B66 · grading: 60 / 10 / 10 / 20, the 80 bracketed, the 20 ringed ────────────────────────────────────────────────────
A7_CX, A7_CW, A7_U = -1.2, 1.6, 0.06              # grade column: centre x, width, units per point
A7_NUMX, A7_LBLX = 0.45, 1.45


def a7_seg(y0, y1, fill, stroke=None):
    r = Rectangle(width=A7_CW, height=y1 - y0, fill_color=fill, fill_opacity=1,
                  stroke_color=stroke or fill, stroke_width=3 if stroke else 0)
    return r.move_to([A7_CX, (y0 + y1) / 2, 0])


A7_SEGS = [(-3.2, 0.4, BAR1, None, "60", "the work"),
           (0.48, 1.08, BAR2, None, "10", "honest log"),
           (1.16, 1.76, BAR2, None, "10", "GitHub = Canvas"),
           (1.84, 3.04, GHOST, DIM, "20", "relative")]


def a7_b66_parts():
    """Every B66 mobject at its final place (B66 builds them on cue; B67 opens on all of them, so the cut is seamless)."""
    top = a7_lbl_left("100 points", -6.0, 2.7, 40)
    segs = []
    for y0, y1, fill, stroke, num, lbl in A7_SEGS:
        segs.append((a7_seg(y0, y1, fill, stroke), T(num, 44).move_to([A7_NUMX, (y0 + y1) / 2, 0]),
                     a7_lbl_left(lbl, A7_LBLX, (y0 + y1) / 2, 34)))
    br = Brace(Line([-2.15, -3.2, 0], [-2.15, 1.76, 0]), direction=LEFT, color=INK, buff=0.1)
    e80 = T("80", 52).move_to([-3.4, -0.55, 0])
    ecl = a7_lbl("criteria met", -3.9, -1.3, 34)
    ring = Ellipse(width=1.25, height=0.95, color=TERRA, stroke_width=7).move_to([A7_NUMX, 2.44, 0])
    return dict(top=top, segs=segs, br=br, e80=e80, ecl=ecl, ring=ring)


class B66_Grading(Scene):
    def construct(self):
        P = a7_b66_parts()
        self.add(P["top"])
        for (seg, n, l), cue in zip(P["segs"], ["Sixty points", "ten for your honest log", "ten for matching", "and twenty relative"]):
            until(self, cue, lead=0.1)
            self.play(GrowFromEdge(seg, DOWN), FadeIn(n), FadeIn(l), run_time=0.5)
        until(self, "Meeting the criteria", lead=0.1)
        self.play(FadeIn(P["ecl"]), run_time=0.4)
        until(self, "the other eighty", lead=0.05)
        self.play(GrowFromCenter(P["br"]), FadeIn(P["e80"]), run_time=0.5)
        until(self, "the twenty", lead=0.0)
        self.play(Create(P["ring"]), run_time=0.48)
        done(self)


# ── B67 · the sixty, split: 10 / 14 / 18 / 10 / 8 ───────────────────────────────────────────────────────────────────────
A7_SPLIT = [("10", "brief"), ("14", "process"), ("18", "three assets"), ("10", "Godot checks"), ("8", "film")]


class B67_TheSixty(Scene):
    def construct(self):
        P = a7_b66_parts()
        everything = [P["top"], P["br"], P["e80"], P["ecl"], P["ring"]] + [m for part in P["segs"] for m in part]
        self.add(*everything)                                   # B66's last frame
        seg = P["segs"][0][0]
        tall = Rectangle(width=A7_CW, height=6.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([A7_CX, -0.1, 0])
        br = Brace(Line([-2.15, -3.2, 0], [-2.15, 3.0, 0]), direction=LEFT, color=INK, buff=0.1)
        b60 = T("60", 52).move_to([-3.4, -0.1, 0])
        self.play(Transform(seg, tall), *[FadeOut(m) for m in everything if m is not seg], run_time=0.45)
        self.play(GrowFromCenter(br), FadeIn(b60), run_time=0.25)
        gap, u = 0.07, (6.2 - 4 * 0.07) / 60
        top_y = 3.0
        cues = ["ten for the brief", "fourteen for the process", "eighteen for the three assets", "ten for the Godot checks", "and eight for the film"]
        for i, ((num, lbl), cue) in enumerate(zip(A7_SPLIT, cues)):
            h = int(num) * u
            ya, yb = top_y - h, top_y
            until(self, cue, lead=0.1)
            piece = a7_seg(ya, yb, BAR1 if i % 2 == 0 else BAR2)
            nn = T(num, 44).move_to([A7_NUMX, (ya + yb) / 2, 0])
            ll = a7_lbl_left(lbl, A7_LBLX, (ya + yb) / 2, 34)
            self.play(GrowFromEdge(piece, UP), FadeIn(nn), FadeIn(ll), run_time=0.4)
            top_y = ya - gap
        done(self)


# ── B68 · late work, and explaining it from the real Blender sidebar ─────────────────────────────────────────────────────
A7_PX = 1.45 / 270.0                              # scene units per crop pixel (crop shown at 1.45x its pixels on a 4K frame)
A7_LOC = ("pantry/a7_bl_location.png", 970, 345, 1.7, 1.55)      # path, w px, h px, centre x, centre y
A7_SD = ("pantry/a7_bl_scale_dims.png", 970, 669, 1.7, -1.45)


def a7_crop(spec):
    path, w, h, cx, cy = spec
    return a7_img(path, cx, cy, w=w * A7_PX)


def a7_ring(spec, box, color=TERRA):
    """A ring round a pixel box (x0, y0, x1, y1) of a crop placed by its spec."""
    _, w, h, cx, cy = spec
    x0, y0, x1, y1 = box
    left, top = cx - w * A7_PX / 2, cy + h * A7_PX / 2
    pa = np.array([left + x0 * A7_PX, top - y1 * A7_PX, 0])
    pb = np.array([left + x1 * A7_PX, top - y0 * A7_PX, 0])
    return RoundedRectangle(width=pb[0] - pa[0], height=pb[1] - pa[1], corner_radius=0.12, fill_opacity=0,
                            stroke_color=color, stroke_width=7).move_to((pa + pb) / 2)


class B68_LateAndExplain(Scene):
    def construct(self):
        late = a7_lbl_left("late work", -6.0, 2.95, 36)
        cells = VGroup(*[Rectangle(width=0.4, height=0.55, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([-5.8 + i * 0.45, 2.2, 0])
                         for i in range(10)])
        self.add(late, cells)
        until(self, "ten percent a day", lead=0.2)
        gone = DashedVMobject(Rectangle(width=0.4, height=0.55, color=DIM, stroke_width=4).move_to([-5.8 + 9 * 0.45, 2.2, 0]), num_dashes=10)
        self.play(FadeOut(cells[9], shift=DOWN * 0.6), Create(gone), run_time=0.55)
        m10 = T("−10%", 60).move_to([-3.85, 1.1, 0])
        pdy = a7_lbl("per day", -3.85, 0.35, 36)
        self.play(FadeIn(m10), FadeIn(pdy), run_time=0.35)
        until(self, "And you must be able", lead=0.0)
        ex = a7_lbl("explain it", -3.85, -2.3, 40)
        self.play(FadeIn(ex), run_time=0.35)
        until(self, "Be ready to open", lead=0.1)
        icon = a7_img("pantry/ev_icon_blender.png", -3.85, -1.05, h=1.1)
        arr = Arrow([-3.05, -1.05, 0], [-1.25, -1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        loc, sd = a7_crop(A7_LOC), a7_crop(A7_SD)
        self.play(FadeIn(icon), Create(arr), FadeIn(loc, shift=LEFT * 0.3), FadeIn(sd, shift=LEFT * 0.3), run_time=0.6)
        # rings: size (Dimensions), origin (Location: where the origin sits), applied transforms (Scale 1.000)
        until(self, "size, origin", lead=0.05)
        r_size = a7_ring(A7_SD, (14, 408, 948, 660))
        t_size = a7_lbl("size", 5.3, -2.35, 36)
        self.play(Create(r_size), FadeIn(t_size), run_time=0.4)
        until(self, "origin and applied", lead=0.05)
        r_org = a7_ring(A7_LOC, (14, 80, 815, 336))
        t_org = a7_lbl("origin", 5.3, 1.3, 36)
        self.play(Create(r_org), FadeIn(t_org), run_time=0.4)
        until(self, "applied transforms", lead=0.0)
        r_scl = a7_ring(A7_SD, (14, 78, 740, 330))
        t_scl = a7_lbl("scale 1", 5.3, -0.6, 36)
        self.play(Create(r_scl), FadeIn(t_scl), run_time=0.4)
        done(self)


# ── B69 · what a check shows, and what only you judge ─────────────────────────────────────────────────────────────────────
class B69_JudgmentIsYours(Scene):
    def construct(self):
        div = Line([0, 2.95, 0], [0, -3.05, 0], color=DIM, stroke_width=4)
        h1 = a7_lbl("a check shows", -3.3, 2.7, 40)
        h2 = a7_lbl("only you judge", 3.3, 2.7, 40)
        self.add(div)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.4)
        items = ["size", "orientation", "scale"]
        ys = [1.35, 0.25, -0.85]
        until(self, "A passing check", lead=0.0)
        labels = VGroup(*[a7_lbl_left(s, -4.25, y, 40) for s, y in zip(items, ys)])
        self.play(FadeIn(labels), run_time=0.4)
        for y, cue in zip(ys, ["the size", "orientation", "and scale"]):
            until(self, cue, lead=0.0)
            self.play(Create(check(-5.1, y + 0.03, 0.22)), run_time=0.3)
        until(self, "It doesn't show", lead=0.1)
        g = a7_img("pantry/a7_godot_lookA_wide.png", 3.3, 0.55, w=5.6)
        self.play(FadeIn(g), run_time=0.5)
        until(self, "look right", lead=0.2)
        tl = a7_lbl("the look", 2.9, -1.75, 40)
        self.play(FadeIn(tl), run_time=0.35)
        until(self, "That judgment", lead=0.1)
        eye = Ellipse(width=0.95, height=0.52, color=INK, stroke_width=5).move_to([4.6, -1.75, 0])
        pupil = Dot([4.6, -1.75, 0], radius=0.14, color=TERRA)
        self.play(Create(eye), FadeIn(pupil), run_time=0.45)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
