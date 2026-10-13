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
"""ACT I · One Column, Three Arrivals  (B01–B06 Manim; B07 is a Remotion LibraryIconRow, see lanes/act1.json)

One cast for the act: the COLUMN. B01 stands it up in isometric with its three dimensions. B03–B05 read it the way
Godot does, in a SIDE VIEW (Godot's Y up, Z across, X toward you): the same 0.2 x 1.8 x 0.2 m column arriving three ways.
Numbers on screen are the real probe output (evidence/probe/godot-mutations.log); nothing is invented.
"""

A1_U = 1.5                                    # side view: scene units per metre
A1_O = np.array([-3.3, -2.55, 0.0])           # side view: ground point under the column's bottom-right corner
A1_W, A1_H = 0.2, 1.8                         # the column, metres


def a1_ground():
    """Axes of the side view: Y up, Z across (Godot's), meeting at the left of the ground line."""
    y_ax = Arrow([-6.0, -2.55, 0], [-6.0, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    z_ax = Arrow([-6.0, -2.55, 0], [-0.9, -2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    ly = T("Y up", 34).move_to([-5.25, 1.1, 0])
    lz = T("Z", 34).move_to([-0.55, -2.55, 0])
    return y_ax, z_ax, ly, lz


def a1_rect(w_m, h_m, fill=BOX_L):
    """A column in the side view standing on the ground with its bottom-RIGHT corner at A1_O."""
    r = Rectangle(width=w_m * A1_U, height=h_m * A1_U, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5)
    r.move_to(A1_O + np.array([-w_m * A1_U / 2, h_m * A1_U / 2, 0]))
    return r


def a1_chips(vals, x0=1.0, y=1.15, hi=None):
    """Three outlined cells X / Y / Z with their numbers. No fill behind text; `hi` rings one cell."""
    cells = VGroup()
    for i, (ax, v) in enumerate(zip("XYZ", vals)):
        x = x0 + i * 1.95
        box = RoundedRectangle(width=1.6, height=1.55, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == hi else DIM,
                               stroke_width=6 if i == hi else 4).move_to([x, y, 0])
        a = T(ax, 36, DIM).move_to([x, y + 0.42, 0])
        n = T(v, 62).move_to([x, y - 0.22, 0])
        cells.add(VGroup(box, a, n))
    return cells


def a1_logline(s, y=-2.45, x=2.5):
    return M(s, 32, DIM).move_to([x, y, 0])


# ── B01 · the column and its three dimensions ──────────────────────────────────────────────────────────────
class B01_Column(Scene):
    def construct(self):
        iso = Iso(-0.6, -2.3, 2.3)
        floor = iso.quad([(-0.5, -0.5, 0), (0.7, -0.5, 0), (0.7, 0.7, 0), (-0.5, 0.7, 0)], GHOST, stroke=GHOST, sw=0)
        col = iso.box(0, 0, 0, 0.2, 0.2, 1.8, top="#C7AE86", left="#A38C66", right="#8F7A57", sw=6)
        title = T("One Column, Three Arrivals", 40).move_to([-3.1, 3.05, 0])
        self.add(floor, col, title)
        until(self, "point two metres wide", lead=0.15)
        w_a = dim_arrow(iso.p(0, 0, 0) + np.array([0, -0.55, 0]), iso.p(0.2, 0, 0) + np.array([0, -0.55, 0]))
        w_l = T("0.2 m wide", 36).move_to([1.35, -3.1, 0])
        self.play(Create(w_a), FadeIn(w_l), run_time=0.5)
        until(self, "point two deep", lead=0.15)
        d_a = dim_arrow(iso.p(0, 0, 0) + np.array([-0.55, -0.35, 0]), iso.p(0, 0.2, 0) + np.array([-0.55, -0.35, 0]))
        d_l = T("0.2 m deep", 36).move_to([-3.05, -2.6, 0])
        self.play(Create(d_a), FadeIn(d_l), run_time=0.5)
        until(self, "one point eight metres tall", lead=0.15)
        h_a = dim_arrow(iso.p(0.2, 0, 0) + np.array([1.1, 0, 0]), iso.p(0.2, 0, 1.8) + np.array([1.1, 0, 0]))
        h_l = T("1.8 m tall", 36).move_to([2.45, -0.4, 0])
        self.play(Create(h_a), FadeIn(h_l), run_time=0.6)
        done(self)


# ── B02 · one script, three builds, one engine ───────────────────────────────────────────────────────────────
class B02_ThreeBuilds(Scene):
    def construct(self):
        bl = ImageMobject("pantry/icon_blender.png").set_height(1.5).move_to([-5.5, -0.25, 0])
        bl_l = T("Blender", 34).move_to([-5.5, -1.45, 0])
        self.add(bl, bl_l)
        xs = [-2.7, 0.2, 3.1]
        cols = VGroup(*[Iso(x, -2.15, 1.0).box(0, 0, 0, 0.2, 0.2, 1.8) for x in xs])
        shadows = VGroup(*[Iso(x, -2.15, 1.0).quad([(-0.3, -0.3, 0), (0.5, -0.3, 0), (0.5, 0.5, 0), (-0.3, 0.5, 0)], GHOST, stroke=GHOST, sw=0)
                           for x in xs])
        src = Arrow([-4.6, -0.25, 0], [-3.7, -0.25, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(shadows), Create(src), run_time=0.4)
        until(self, "three times", lead=0.3)
        for c in cols:
            self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.35)
        until(self, "changing one setting", lead=0.2)
        labs = [T("default", 32).move_to([xs[0] + 0.25, -2.85, 0]),
                T("Y up off", 32).move_to([xs[1] + 0.25, -2.85, 0]),
                T("scale not\napplied", 32).move_to([xs[2] + 0.25, -2.85, 0])]
        for l in labs:
            self.play(FadeIn(l), run_time=0.25)
        until(self, "Godot game engine", lead=1.0)
        to_g = Arrow([4.4, -0.25, 0], [4.85, -0.25, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        gd = ImageMobject("pantry/icon_godot.png").set_height(1.5).move_to([5.55, -0.25, 0])
        gd_l = T("Godot", 34).move_to([5.55, -1.45, 0])
        self.play(Create(to_g), FadeIn(gd), FadeIn(gd_l), run_time=0.5)
        done(self)


# ── B03 · the good arrival ──────────────────────────────────────────────────────────────────────────────────
class B03_Good(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        self.add(y_ax, z_ax, ly, lz)
        col = a1_rect(A1_W, A1_H)
        cap = T("bounding box, in metres", 36).move_to([2.6, 2.45, 0])
        self.play(GrowFromEdge(col, DOWN), FadeIn(cap), run_time=0.6)
        chips = a1_chips(["0.2", "1.8", "0.2"], hi=1)
        until(self, "point two, one point eight, point two", lead=0.2)
        self.play(FadeIn(chips[0]), run_time=0.3)
        self.play(FadeIn(chips[1]), run_time=0.3)
        self.play(FadeIn(chips[2]), run_time=0.3)
        until(self, "vertical axis", lead=0.6)
        ring = Dot([A1_O[0] - 0.15, A1_O[1] + 1.8 * A1_U + 0.2, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(ring), run_time=0.3)
        until(self, "a scale of one", lead=0.2)
        sc = a1_logline("node scale (1.0, 1.0, 1.0)", y=-0.75)
        lg = a1_logline("mesh AABB size (0.2, 1.8, 0.2)", y=-1.5)
        self.play(FadeIn(sc), FadeIn(lg), run_time=0.4)
        done(self)


# ── B04 · the same column, Y-up off: it lies down ───────────────────────────────────────────────────────────────
class B04_LiesDown(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        col = a1_rect(A1_W, A1_H)
        cap = T("bounding box, in metres", 36).move_to([2.6, 2.45, 0])
        chips = a1_chips(["0.2", "1.8", "0.2"], hi=1)
        ring = Dot([A1_O[0] - 0.15, A1_O[1] + 1.8 * A1_U + 0.2, 0], radius=0.12, color=TERRA)
        sc = a1_logline("node scale (1.0, 1.0, 1.0)", y=-0.75)
        self.add(y_ax, z_ax, ly, lz, col, cap, chips, ring, sc)
        until(self, "lying on its side", lead=0.3)
        self.play(FadeOut(ring), Rotate(col, angle=-PI / 2, about_point=A1_O.copy()), run_time=1.0)
        lab = T("1.8 now along Z", 34).move_to([-3.7, -1.5, 0])
        self.play(FadeIn(lab), run_time=0.3)
        until(self, "the one point eight now sits on the depth axis", lead=0.2)
        newvals = a1_chips(["0.2", "0.2", "1.8"], hi=2)
        self.play(Transform(chips[1][2], newvals[1][2]), Transform(chips[2][2], newvals[2][2]),
                  chips[1][0].animate.set_stroke(DIM, 4), chips[2][0].animate.set_stroke(INK, 6), run_time=0.7)
        ring2 = Dot([1.0 + 2 * 1.95 + 0.62, 1.15 + 0.62, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(ring2), run_time=0.3)
        until(self, "One setting about which way is up", lead=0.2)
        lg = a1_logline("mesh AABB size (0.2, 0.2, 1.8)", y=-1.5)
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ── B05 · looks identical; the mesh is a two-metre cube wearing a scale ───────────────────────────────────────────
class B05_Disguise(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        col = a1_rect(A1_W, A1_H)
        cap = T("node scale", 36).move_to([2.6, 2.45, 0])
        self.add(y_ax, z_ax, ly, lz, col, cap)
        until(self, "But its mesh", lead=0.2)
        cube = Rectangle(width=2.0 * A1_U, height=2.0 * A1_U, fill_opacity=0, stroke_color=DIM, stroke_width=6)
        cube.move_to(A1_O + np.array([-0.1 * A1_U, 0.9 * A1_U, 0]))
        cl = T("mesh: 2 × 2 × 2 m", 36).move_to([-3.4, 1.7, 0])
        self.play(Create(cube), FadeIn(cl), run_time=0.8)
        until(self, "wearing a scale of", lead=0.2)
        chips = a1_chips(["0.1", "0.9", "0.1"], hi=None)
        self.play(FadeIn(chips[0]), run_time=0.3)
        self.play(FadeIn(chips[1]), run_time=0.3)
        self.play(FadeIn(chips[2]), run_time=0.3)
        until(self, "point one, point nine, point one", lead=0.1)
        lg = a1_logline("mesh AABB size (2.0, 2.0, 2.0)", y=-0.75)
        lg2 = a1_logline("node scale (0.1, 0.9, 0.1)", y=-1.5)
        self.play(FadeIn(lg), FadeIn(lg2), run_time=0.4)
        done(self)


# ── B06 · inherited scale, and the fourth failure: a collider that is only a box ───────────────────────────────────
class B06_Inherited(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a1_ground()
        col = a1_rect(A1_W, A1_H)
        cube = Rectangle(width=2.0 * A1_U, height=2.0 * A1_U, fill_opacity=0, stroke_color=DIM, stroke_width=6)
        cube.move_to(A1_O + np.array([-0.1 * A1_U, 0.9 * A1_U, 0]))
        self.add(y_ax, z_ax, ly, lz, col, cube)
        until(self, "generated from that mesh", lead=0.3)
        shape = cube.copy().set_stroke(INK, 8)
        sl = T("a collider built from it", 34).move_to([-3.4, 1.7, 0])
        self.play(Create(shape), FadeIn(sl), run_time=0.7)
        until(self, "a fourth failure", lead=0.3)
        box = Square(side_length=2.6, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([3.6, -0.55, 0])
        bl = T("a visible box", 34).move_to([3.6, 1.35, 0])
        self.play(FadeIn(box), FadeIn(bl), run_time=0.5)
        until(self, "no collision at all", lead=0.4)
        ring = Circle(radius=0.55, stroke_color=INK, stroke_width=8).move_to([3.6, -0.55, 0])
        bar = Line([3.21, -0.16, 0], [3.99, -0.94, 0], color=INK, stroke_width=8)
        nl = T("no collision", 34).move_to([3.6, -2.55, 0])
        self.play(Create(ring), Create(bar), FadeIn(nl), run_time=0.7)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Two Ways to Let an Agent Drive Blender  (B08–B10, B12–B18 Manim; B11 is a Remotion BrowserCapture, see lanes/act2.json)

One cast for the act, so the two routes read as two consistent things across eleven beats:
  LIVE route   = the agent (rounded box with a spark) -> a small dark MCP server block -> a socket ring on the edge of the REAL Blender window
                 (pantry/blender_window.png, a real Blender 5.1.2 screenshot). Tool calls are terracotta dots riding deep-kraft cables.
  SCRIPT route = a script PAGE (white slab, terracotta dot) -> Blender's real icon (no window) -> a .glb file; the window stays a ghost outline
                 with a strike through it. The command line is Menlo text, one flag per row (same rows in B14 and B15).
Real things on screen: Blender's window and icon, the real post render (a2_post.png), the real exit-code output (evidence/act2/exit_code_transcript.txt),
the real Lab-page warning (a2_lab_warning.png, captured 2026-10-06; evidence/act2/capture_pages.py). Nothing is drawn onto the Blender window itself.
"""

A2_ASPECT = 3456.0 / 2006.0          # the real window screenshot
A2_CABLE = "#9C8462"                 # deep kraft for connectors (ink-edged pipes fuse blocks into one text blob)
A2_XL = -6.25                        # left edge of the command block (Menlo 32 = 0.25 units per character)
A2_DX = -6.05                        # x of the terracotta 'you are here' dot beside the flag rows (flags are indented two characters)


# ═════════════════════════════ cast helpers ═════════════════════════════
def a2_iso(cx, cy, s, W, D, H=0.0):
    """An Iso whose projected footprint W x D x H is centred on the scene point (cx, cy)."""
    ox = cx - (W - D) * C30 * s / 2
    oy = cy - ((W + D) / 2 + H) * s / 2
    return Iso(ox, oy, s)


def a2_agent(x, y, s=1.0):
    """The coding agent: a rounded box with a four-point spark in it (generic, not any one product)."""
    box = RoundedRectangle(width=1.5 * s, height=1.2 * s, corner_radius=0.22 * s, fill_color=CARD, fill_opacity=1,
                           stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    r, q = 0.34 * s, 0.09 * s
    star = Polygon([x, y + r, 0], [x + q, y + q, 0], [x + r, y, 0], [x + q, y - q, 0], [x, y - r, 0], [x - q, y - q, 0],
                   [x - r, y, 0], [x - q, y + q, 0], fill_color=INK, fill_opacity=1, stroke_width=0)
    return VGroup(box, star)


def a2_term(x, y, s=1.0):
    """A terminal chip: rounded box, a > chevron and an underscore (commands)."""
    box = RoundedRectangle(width=1.5 * s, height=1.2 * s, corner_radius=0.22 * s, fill_opacity=0,
                           stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    a = Line([x - 0.38 * s, y + 0.24 * s, 0], [x - 0.1 * s, y, 0], color=INK, stroke_width=7)
    b = Line([x - 0.1 * s, y, 0], [x - 0.38 * s, y - 0.24 * s, 0], color=INK, stroke_width=7)
    u = Line([x + 0.06 * s, y - 0.26 * s, 0], [x + 0.42 * s, y - 0.26 * s, 0], color=INK, stroke_width=7)
    return VGroup(box, a, b, u)


def a2_page(cx, cy, s=1.0):
    """The script page (kit page: white slab, ghost lines, one terracotta dot), centred on (cx, cy)."""
    return a2_iso(cx, cy, s, 1.1, 1.4, 0.06).page(0, 0, 0, 1.1, 1.4)


def a2_server(cx, cy, s=1.0):
    """The small MCP server: the kit's dark block with two ports (the act's one dark object)."""
    return a2_iso(cx, cy, s, 1.3, 1.3, 0.7).mcp(0, 0, 0)


def a2_window(cx, cy, w):
    """The REAL Blender window (screenshot) with an ink outline. Returns (image, outline, height)."""
    h = w / A2_ASPECT
    img = ImageMobject("pantry/blender_window.png").set_height(h).move_to([cx, cy, 0])
    frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([cx, cy, 0])
    return img, frame, h


def a2_icon(cx, cy, h):
    return ImageMobject("pantry/icon_blender.png").set_height(h).move_to([cx, cy, 0])


def a2_ghost_window(cx, cy, w, h):
    """An empty window outline (where the live route's window would be): DIM frame + title bar."""
    fr = Rectangle(width=w, height=h, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([cx, cy, 0])
    bar = Line([cx - w / 2, cy + h / 2 - 0.4, 0], [cx + w / 2, cy + h / 2 - 0.4, 0], color=DIM, stroke_width=4)
    return VGroup(fr, bar)


def a2_strike(cx, cy, w, h, color=INK):
    """Two crossing lines (a cross-out) over an object of size w x h."""
    return VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=color, stroke_width=8),
                  Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=color, stroke_width=8))


def a2_socket(x, y):
    """The add-on's socket: a ring with a terracotta dot, sitting on the edge of the window."""
    ring = Circle(radius=0.3, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    dot = Dot([x, y, 0], radius=0.09, color=TERRA)
    return VGroup(ring, dot)


def a2_cable(p, q):
    return Line(p, q, color=A2_CABLE, stroke_width=8)


def a2_eye(x, y, s=1.0):
    """An eye (review): almond outline plus a pupil."""
    top = ArcBetweenPoints([x - 0.62 * s, y, 0], [x + 0.62 * s, y, 0], angle=-1.0, color=INK, stroke_width=6)
    bot = ArcBetweenPoints([x - 0.62 * s, y, 0], [x + 0.62 * s, y, 0], angle=1.0, color=INK, stroke_width=6)
    return VGroup(top, bot, Circle(radius=0.2 * s, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([x, y, 0]),
                  Dot([x, y, 0], radius=0.07 * s, color=INK))


def a2_mline(s, y, indent=0, color=INK):
    """One line of the command block (Menlo 32), left edge at A2_XL + indent characters."""
    return M(s, 32, color).move_to([A2_XL + (indent + len(s) / 2.0) * 0.25, y, 0])


# the command block rows (y). The row at A2_Y3 is empty in B14 and holds `--python-exit-code 1 \` in B15
A2_Y0, A2_Y1, A2_Y2, A2_Y3, A2_Y4 = 3.05, 2.2, 1.35, 0.5, -0.35


def a2_cmd(with_flag=False):
    """The real command, one flag per row: (path, -b, --factory-startup, [--python-exit-code 1], --python script). Same rows in B14 and B15."""
    rows = [a2_mline("/Applications/Blender.app/Contents/MacOS/Blender \\", A2_Y0),
            a2_mline("-b \\", A2_Y1, 2), a2_mline("--factory-startup \\", A2_Y2, 2),
            a2_mline("--python tools/blender/build_checkpoint_post.py", A2_Y4, 2)]
    flag = a2_mline("--python-exit-code 1 \\", A2_Y3, 2)
    return rows, flag


# ── B08 · what a coding agent is, then the two ways ────────────────────────────────────────────────────────
class B08_TwoWays(Scene):
    def construct(self):
        ag = a2_agent(-5.0, 0.1)
        ag_l = T("coding agent", 34).move_to([-5.0, -1.15, 0])
        self.play(FadeIn(ag), FadeIn(ag_l), run_time=0.5)
        until(self, "edits files", lead=0.4)
        pg = a2_page(-2.0, 1.45, 0.8)
        pg_l = T("files", 34).move_to([-0.55, 1.45, 0])
        ar1 = Arrow([-4.1, 0.45, 0], [-3.25, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(ar1), FadeIn(pg), FadeIn(pg_l), run_time=0.5)
        until(self, "runs commands", lead=0.4)
        tm = a2_term(-2.0, -1.35, 0.9)
        tm_l = T("commands", 34).move_to([-0.2, -1.35, 0])
        ar2 = Arrow([-4.1, -0.25, 0], [-3.1, -0.95, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(ar2), FadeIn(tm), FadeIn(tm_l), run_time=0.5)
        until(self, "When it builds a model", lead=0.0)
        self.play(FadeOut(VGroup(pg, pg_l, ar1, tm, tm_l, ar2)), run_time=0.4)
        img, fr, h = a2_window(2.9, 1.55, 3.6)
        pg2 = a2_page(2.9, -1.55, 0.95)
        self.play(FadeIn(img), Create(fr), FadeIn(pg2), run_time=0.5)
        until(self, "two ways", lead=1.4)
        a_top = Arrow([-4.05, 0.5, 0], [0.95, 1.45, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
        a_bot = Arrow([-4.05, -0.2, 0], [1.65, -1.5, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
        self.play(Create(a_top), Create(a_bot), run_time=0.6)
        l_live = T("live", 38).move_to([2.9, 0.1, 0])
        l_scr = T("script", 38).move_to([2.9, -2.85, 0])
        self.play(FadeIn(l_live), FadeIn(l_scr), run_time=0.4)
        done(self)


# ── B09 · the live route: add-on socket, small server, tool calls into the open window ──────────────────────
class B09_LiveRoute(Scene):
    def construct(self):
        img, fr, h = a2_window(2.95, 0.25, 6.2)
        win_l = T("Blender, open", 34).move_to([2.95, -1.95, 0])
        note = T("route documented, not run", 32).move_to([0.0, -3.0, 0])      # honesty: the MCP route was read about, never run
        self.play(FadeIn(img), Create(fr), FadeIn(win_l), FadeIn(note), run_time=0.4)
        until(self, "opens a local socket", lead=0.9)
        sock = a2_socket(-0.15, 0.25)
        sock_l = T("socket", 34).move_to([-0.95, 1.0, 0])
        self.play(GrowFromCenter(sock), FadeIn(sock_l), run_time=0.5)
        until(self, "a small server", lead=1.5)
        srv = a2_server(-2.85, -0.1, 0.95)
        srv_l = T("server", 34).move_to([-2.85, -1.45, 0])
        self.play(FadeIn(srv), FadeIn(srv_l), run_time=0.4)
        ag = a2_agent(-5.45, 0.15, 0.9)
        ag_l = T("agent", 34).move_to([-5.45, -0.75, 0])
        self.play(FadeIn(ag), FadeIn(ag_l), run_time=0.3)
        c1 = a2_cable([-4.75, 0.15, 0], [-3.85, 0.05, 0])
        c2 = a2_cable([-1.7, -0.05, 0], [-0.45, 0.22, 0])
        c1.set_z_index(-1); c2.set_z_index(-1)
        self.play(Create(c1), Create(c2), run_time=0.4)
        until(self, "relays the agent's tool calls", lead=0.0)
        ring = Rectangle(width=6.4, height=h + 0.2, stroke_color=TERRA, stroke_width=8, fill_opacity=0).move_to([2.95, 0.25, 0])
        for i in range(3):
            d = Dot([-4.7, 0.15, 0], radius=0.14, color=TERRA)
            self.add(d)
            self.play(d.animate.move_to([-3.2, 0.05, 0]), run_time=0.25, rate_func=linear)
            self.play(d.animate.move_to([-0.15, 0.25, 0]), run_time=0.4, rate_func=linear)
            if i == 2:
                self.play(d.animate.move_to([1.4, 0.25, 0]), Create(ring), run_time=0.45, rate_func=linear)
            else:
                self.play(d.animate.move_to([1.4, 0.25, 0]), run_time=0.25, rate_func=linear)
            self.play(FadeOut(d), run_time=0.1)
        until(self, "M C P route", lead=0.3)
        mcp_l = T("MCP", 40).move_to([-2.85, 1.55, 0])
        self.play(FadeIn(mcp_l), run_time=0.4)
        done(self)


# ── B10 · two projects, both do both ──────────────────────────────────────────────────────────────────────────
class B10_TwoProjects(Scene):
    def construct(self):
        xs = [0.5, 4.35]                                   # the two project columns
        blk = [a2_server(x, 2.75, 0.5) for x in xs]
        self.play(FadeIn(blk[0]), FadeIn(blk[1]), run_time=0.5)
        until(self, "a community one", lead=0.3)
        n1 = T("MCP for Blender", 34).move_to([xs[0], 1.85, 0])
        s1 = T("community", 34).move_to([xs[0], 1.3, 0])
        self.play(FadeIn(n1), FadeIn(s1), run_time=0.4)
        until(self, "the Blender Lab", lead=0.4)
        n2 = T("Blender MCP", 34).move_to([xs[1], 1.85, 0])
        s2 = T("Blender Lab", 34).move_to([xs[1], 1.3, 0])
        self.play(FadeIn(n2), FadeIn(s2), run_time=0.4)
        cells = VGroup()
        for x in xs:
            for y in (0.1, -1.45):
                cells.add(RoundedRectangle(width=3.3, height=1.15, corner_radius=0.2, fill_opacity=0, stroke_color=DIM,
                                           stroke_width=4).move_to([x, y, 0]))
        r1 = T("run Python", 36).move_to([-3.95, 0.1, 0])
        r2 = T("screenshots", 36).move_to([-3.95, -1.45, 0])
        self.play(FadeIn(cells), FadeIn(r1), FadeIn(r2), run_time=0.5)
        until(self, "run Python", lead=0.2)
        for x in xs:
            self.play(Create(check(x, 0.1, 0.3)), run_time=0.3)
        until(self, "screenshots", lead=0.2)
        for x in xs:
            self.play(Create(check(x, -1.45, 0.3)), run_time=0.3)
        done(self)


# ── B12 · the Lab page says the same; two rules, shown as rules ───────────────────────────────────────────────
class B12_TwoRules(Scene):
    def construct(self):
        warn = ImageMobject("pantry/a2_lab_warning.png").set_width(11.8).move_to([0.2, 1.95, 0])
        edge = Rectangle(width=11.8, height=11.8 * 430.0 / 2640.0, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0.2, 1.95, 0])
        src = T("blender.org/lab/mcp-server, captured 2026-10-06", 32).move_to([0.2, 0.65, 0])
        spark = Dot([-6.0, 1.95, 0], radius=0.13, color=TERRA)
        self.play(FadeIn(warn), Create(edge), FadeIn(src), run_time=0.5)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "So two rules", lead=0.0)
        # rule 1 (left): localhost only. A boundary around this machine; a remote box is stopped at the edge.
        bound = RoundedRectangle(width=3.5, height=2.1, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=7).move_to([-2.05, -1.6, 0])
        win, wfr, wh = a2_window(-1.75, -1.6, 2.0)
        sock = a2_socket(-2.75, -1.6)
        remote = RoundedRectangle(width=1.0, height=0.8, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([-5.4, -1.6, 0])
        out_l = T("outside", 34).move_to([-5.4, -2.4, 0])
        self.play(Create(bound), FadeIn(win), Create(wfr), GrowFromCenter(sock), FadeIn(remote), FadeIn(out_l), run_time=0.5)
        until(self, "Keep the port on localhost", lead=0.0)
        host = M("localhost", 32).move_to([-2.05, -3.1, 0])
        wall = Line([-3.8, -2.2, 0], [-3.8, -1.0, 0], color=INK, stroke_width=10)
        d = Dot([-4.7, -1.6, 0], radius=0.14, color=TERRA)
        self.play(FadeIn(host), Create(wall), FadeIn(d), run_time=0.4)
        self.play(d.animate.move_to([-4.05, -1.6, 0]), run_time=0.5, rate_func=linear)
        # rule 2 (right): three generation services, switched on at first, each calling out to a remote service
        until(self, "And leave", lead=0.0)
        names = ["Rodin", "Hunyuan3D", "Tripo"]
        ys = [-0.85, -1.85, -2.85]
        pills, knobs, nms, cabs, boxes = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        for n, y in zip(names, ys):
            pills.add(RoundedRectangle(width=0.95, height=0.5, corner_radius=0.25, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([0.8, y, 0]))
            knobs.add(Circle(radius=0.17, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0.98, y, 0]))
            nms.add(T(n, 34).move_to([1.7 + {"Rodin": 0.55, "Hunyuan3D": 1.05, "Tripo": 0.5}[n], y, 0]))
            cabs.add(a2_cable([4.3, y, 0], [5.05, y, 0]))
            boxes.add(RoundedRectangle(width=0.9, height=0.7, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([5.5, y, 0]))
        self.play(FadeIn(pills), FadeIn(knobs), FadeIn(nms), FadeIn(cabs), FadeIn(boxes), run_time=0.45)
        until(self, "services off", lead=0.0)
        self.play(*[k.animate.move_to([0.62, y, 0]) for k, y in zip(knobs, ys)], FadeOut(cabs), run_time=0.7)
        until(self, "approved the spend", lead=0.2)
        spend = T("$", 44).move_to([0.8, -0.15, 0])
        self.play(FadeIn(spend), run_time=0.3)
        until(self, "remote services", lead=0.3)
        rem = T("remote", 34).move_to([5.5, -0.15, 0])
        self.play(FadeIn(rem), run_time=0.3)
        done(self)


# ── B13 · the script route: no window; a script runs in Blender, builds, exports, exits ───────────────────────
class B13_ScriptRoute(Scene):
    def construct(self):
        gw = a2_ghost_window(-4.9, 0.55, 2.4, 1.6)
        gw_l = T("window", 34).move_to([-4.9, -0.7, 0])
        self.play(FadeIn(gw), FadeIn(gw_l), run_time=0.5)
        until(self, "no window at all", lead=0.3)
        stk = a2_strike(-4.9, 0.55, 2.4, 1.6)
        self.play(Create(stk), run_time=0.5)
        until(self, "Blender can run", lead=0.0)
        pg = a2_page(-2.0, 0.45, 1.0)
        pg_l = T("script", 34).move_to([-2.0, -0.95, 0])
        self.play(FadeIn(pg), FadeIn(pg_l), run_time=0.5)
        bl = a2_icon(1.2, 0.4, 1.5)
        bl_l = T("Blender", 34).move_to([1.2, -0.7, 0])
        self.play(FadeIn(bl), FadeIn(bl_l), run_time=0.5)
        until(self, "in the background", lead=0.0)
        ar1 = Arrow([-0.85, 0.4, 0], [0.3, 0.4, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(ar1), run_time=0.4)
        until(self, "it builds the model", lead=0.0)
        post = ImageMobject("pantry/a2_post.png").set_height(1.75).move_to([1.2, 2.25, 0])
        post_l = T("model", 34).move_to([2.6, 2.25, 0])
        self.play(FadeIn(post), FadeIn(post_l), run_time=0.5)
        until(self, "exports it", lead=0.0)
        ar2 = Arrow([2.15, 0.4, 0], [3.85, 0.4, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        glb = a2_iso(5.0, 0.4, 0.9, 1.0, 1.0, 0.5).box(0, 0, 0, 1.0, 1.0, 0.5)
        glb_l = T(".glb", 34).move_to([5.0, -0.75, 0])
        self.play(Create(ar2), FadeIn(glb), FadeIn(glb_l), run_time=0.5)
        until(self, "and exits", lead=0.0)
        self.play(bl.animate.fade(0.8), FadeOut(bl_l), run_time=0.4)
        done(self)


# ── B14 · read the flags: -b, --factory-startup, --python ─────────────────────────────────────────────────────
class B14_Flags(Scene):
    def construct(self):
        rows, flag = a2_cmd()
        self.play(FadeIn(VGroup(*rows)), run_time=0.4)
        dot = Dot([A2_DX, A2_Y1, 0], radius=0.12, color=TERRA)
        until(self, "Dash b", lead=0.2)
        gw = a2_ghost_window(-0.9, A2_Y1, 1.2, 0.6)
        stk = a2_strike(-0.9, A2_Y1, 1.2, 0.6)
        l1 = T("no window", 34).move_to([1.2, A2_Y1, 0])
        self.play(FadeIn(dot), FadeIn(gw), Create(stk), FadeIn(l1), run_time=0.5)
        until(self, "Factory startup", lead=0.3)
        pref = a2_page(0.0, A2_Y2, 0.45)
        stk2 = a2_strike(0.0, A2_Y2, 1.0, 0.6)
        l2 = T("your settings, skipped", 34).move_to([3.0, A2_Y2, 0])
        self.play(dot.animate.move_to([A2_DX, A2_Y2, 0]), run_time=0.25)
        self.play(FadeIn(pref), Create(stk2), FadeIn(l2), run_time=0.5)
        until(self, "every run starts the same", lead=0.2)
        l3 = T("same every run", 34).move_to([3.0, A2_Y3, 0])
        self.play(FadeIn(l3), run_time=0.4)
        until(self, "python runs the script", lead=0.5)
        self.play(dot.animate.move_to([A2_DX, A2_Y4, 0]), run_time=0.25)
        pg = a2_page(-3.2, -2.0, 1.0)
        ar = Arrow([-1.9, -1.9, 0], [-0.4, -1.9, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        bl = a2_icon(1.0, -1.9, 1.5)
        bl_l = T("Blender runs it", 34).move_to([3.7, -1.9, 0])
        self.play(FadeIn(pg), Create(ar), FadeIn(bl), FadeIn(bl_l), run_time=0.5)
        done(self)


# ── B15 · one more flag: the same error, exit 0 without it, exit 1 with it (real output) ─────────────────────
class B15_ExitCode(Scene):
    def construct(self):
        rows, flag = a2_cmd()
        self.add(VGroup(*rows))
        dot = Dot([A2_DX, A2_Y3, 0], radius=0.12, color=TERRA)
        until(self, "python exit code one", lead=0.25)
        self.play(FadeIn(flag), FadeIn(dot), run_time=0.4)
        until(self, "Without it", lead=0.1)
        pan_l = RoundedRectangle(width=5.8, height=2.55, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.15, -2.1, 0])
        h_l = T("without the flag", 34).move_to([-3.15, -1.3, 0])
        self.play(flag.animate.set_color(GHOST), FadeOut(dot), Create(pan_l), FadeIn(h_l), run_time=0.4)
        until(self, "Blender exits with zero", lead=-0.2)
        x_l = T("exit code", 34).move_to([-4.3, -2.85, 0])
        n0 = T("0", 96).move_to([-1.6, -2.7, 0])
        self.play(FadeIn(x_l), FadeIn(n0), run_time=0.4)
        until(self, "raises an exception", lead=1.6)
        e_l = M("ValueError: boom", 32).move_to([-3.15, -1.95, 0])
        self.play(FadeIn(e_l), run_time=0.4)
        until(self, "the same error both ways", lead=0.3)
        pan_r = RoundedRectangle(width=5.8, height=2.55, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.15, -2.1, 0])
        h_r = T("with the flag", 34).move_to([3.15, -1.3, 0])
        e_r = M("ValueError: boom", 32).move_to([3.15, -1.95, 0])
        dot2 = Dot([A2_DX, A2_Y3, 0], radius=0.12, color=TERRA)
        self.play(Create(pan_r), FadeIn(h_r), FadeIn(e_r), flag.animate.set_color(INK), FadeIn(dot2), run_time=0.5)
        until(self, "and one", lead=0.15)
        x_r = T("exit code", 34).move_to([2.0, -2.85, 0])
        n1 = T("1", 96).move_to([4.5, -2.7, 0])
        self.play(FadeIn(x_r), FadeIn(n1), run_time=0.35)
        done(self)


# ── B16 · exits zero looks like success downstream; the one flag is the difference ──────────────────────────
class B16_LooksLikeSuccess(Scene):
    def construct(self):
        y1, y2 = 1.25, -1.55
        ds_l = T("downstream", 34).move_to([3.4, 3.0, 0])
        l1 = T("no flag", 34).move_to([-4.6, y1 + 1.05, 0])
        l2 = M("--python-exit-code 1", 32).move_to([-3.3, y2 + 1.05, 0])
        gt_l = T("exit check", 34).move_to([-0.6, 2.2, 0])
        pgs = [a2_page(-4.7, y, 0.75) for y in (y1, y2)]
        bxs = [a2_iso(3.4, y, 0.9, 1.1, 1.1, 0.8).box(0, 0, 0, 1.1, 1.1, 0.8) for y in (y1, y2)]
        # the gate beside each row: raised (open) above the path at first
        gates = [Line([1.0, y + 0.6, 0], [1.0, y + 1.5, 0], color=INK, stroke_width=12) for y in (y1, y2)]
        self.add(ds_l, l1, l2, gt_l, *pgs, *bxs, *gates)
        until(self, "fails", lead=0.3)
        xs = [a2_strike(-4.7, y, 0.9, 0.9) for y in (y1, y2)]
        self.play(Create(xs[0]), Create(xs[1]), run_time=0.4)
        until(self, "exits zero", lead=0.4)
        c0 = T("0", 72).move_to([-2.5, y1, 0])
        c1 = T("1", 72).move_to([-2.5, y2, 0])
        self.play(FadeIn(c0), FadeIn(c1), run_time=0.3)
        until(self, "looks like success", lead=0.55)
        self.play(c0.animate.move_to([2.0, y1, 0]), c1.animate.move_to([0.2, y2, 0]),
                  gates[1].animate.shift(DOWN * 1.1), run_time=0.8, rate_func=linear)
        ok = check(3.4, y1 + 1.2, 0.3, INK)
        ok_l = T("looks like success", 34).move_to([3.4, y1 - 1.3, 0])
        no_l = T("stops here", 34).move_to([0.6, y2 - 0.95, 0])
        self.play(Create(ok), FadeIn(ok_l), FadeIn(no_l), run_time=0.4)
        until(self, "That one flag", lead=0.1)
        sp = Dot([-6.2, y2 + 1.05, 0], radius=0.13, color=TERRA)
        self.play(FadeIn(sp), run_time=0.3)
        done(self)


# ── B17 · what you keep from each route ────────────────────────────────────────────────────────────────────────
class B17_WhatYouKeep(Scene):
    def construct(self):
        img, fr, h = a2_window(-3.2, 2.4, 2.4)
        pg = a2_page(3.2, 2.4, 0.7)
        h_l = T("live", 38).move_to([-5.45, 2.4, 0])
        h_s = T("script", 38).move_to([1.3, 2.4, 0])
        div = Line([0.0, 3.2, 0], [0.0, -3.1, 0], color=GHOST, stroke_width=5)
        self.add(img, fr, pg, h_l, h_s, div)
        until(self, "a transcript of tool calls", lead=0.4)
        rows = VGroup()
        for i in range(4):
            y = 0.9 - i * 0.62
            rows.add(VGroup(Dot([-5.55, y, 0], radius=0.09, color=TERRA), Line([-5.3, y, 0], [-3.2 - 0.25 * (i % 2), y, 0], color=DIM, stroke_width=7)))
        tl = T("tool calls", 34).move_to([-4.2, -1.4, 0])
        for r in rows:
            self.play(FadeIn(r), run_time=0.2)
        self.play(FadeIn(tl), run_time=0.2)
        until(self, "a scene that changed", lead=0.4)
        q = T("?", 110).move_to([-1.7, -0.2, 0])
        q_l = T("no record", 34).move_to([-1.9, -1.3, 0])
        self.play(FadeIn(q), FadeIn(q_l), run_time=0.4)
        until(self, "you keep a Python file", lead=0.0)
        pg_d = a2_page(1.55, -0.1, 0.75)
        self.play(FadeIn(pg_d), run_time=0.4)
        until(self, "diff,", lead=0.35)
        pg_d2 = a2_page(1.95, 0.15, 0.75)
        d_l = T("diff", 34).move_to([1.75, -1.3, 0])
        self.play(FadeIn(pg_d2), FadeIn(d_l), run_time=0.3)
        until(self, "rerun", lead=0.2)
        arc = Arc(radius=0.55, start_angle=0.5, angle=4.9, color=INK, stroke_width=7).move_to([3.7, -0.1, 0])
        tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.14).move_to([3.7 + 0.55 * np.cos(0.5), -0.1 + 0.55 * np.sin(0.5), 0])
        r_l = T("rerun", 34).move_to([3.7, -1.3, 0])
        self.play(Create(arc), FadeIn(tip), FadeIn(r_l), run_time=0.3)
        until(self, "review", lead=0.2)
        ey = a2_eye(5.45, -0.1, 0.9)
        e_l = T("review", 34).move_to([5.45, -1.3, 0])
        self.play(Create(ey), FadeIn(e_l), run_time=0.3)
        done(self)


# ── B18 · the script repeats a wrong assumption faithfully; neither route makes it look right; both hand you numbers ──
class B18_NumbersNotLooks(Scene):
    def construct(self):
        pg = a2_page(-4.6, 0.3, 1.1)
        pg_l = T("script", 34).move_to([-4.6, -1.3, 0])
        self.play(FadeIn(pg), FadeIn(pg_l), run_time=0.4)
        until(self, "a wrong assumption", lead=0.6)
        wd = Dot([-4.65, 0.45, 0], radius=0.16, color=TERRA)
        wl = T("wrong assumption", 34).move_to([-4.6, 1.95, 0])
        self.play(FadeIn(wd), FadeIn(wl), run_time=0.3)
        until(self, "repeat it faithfully", lead=1.4)
        outs = VGroup()
        xs = (-1.4, 0.9, 3.2)
        for x in xs:
            b = a2_iso(x, 0.3, 0.8, 1.0, 1.0, 0.6).box(0, 0, 0, 1.0, 1.0, 0.6)
            outs.add(VGroup(b, a2_strike(x, 0.3, 0.7, 0.7)))
        ars = VGroup(*[Arrow([x - 1.35, 0.3, 0], [x - 0.85, 0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.18) for x in xs])
        for i in range(3):
            self.play(Create(ars[i]), FadeIn(outs[i]), run_time=0.3)
        rl = T("same wrong result", 34).move_to([0.9, -1.45, 0])
        self.play(FadeIn(rl), run_time=0.3)
        until(self, "Neither route", lead=0.1)
        self.play(FadeOut(VGroup(pg, pg_l, wd, wl, outs, ars, rl)), run_time=0.4)
        img, fr, h = a2_window(-4.7, 1.3, 2.6)
        pg2 = a2_page(-4.7, -1.4, 0.8)
        self.play(FadeIn(img), Create(fr), FadeIn(pg2), run_time=0.4)
        a1 = Arrow([-3.25, 1.2, 0], [0.0, 0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        a2 = Arrow([-3.6, -1.4, 0], [0.0, -0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        ey = a2_eye(1.1, 0.0, 1.0)
        self.play(Create(a1), Create(a2), Create(ey), run_time=0.5)
        stk = a2_strike(1.1, 0.0, 1.7, 1.1)
        lk = T("looks right", 34).move_to([1.1, 1.25, 0])
        self.play(Create(stk), FadeIn(lk), run_time=0.4)
        until(self, "hand you numbers", lead=0.2)
        cells = VGroup()
        for i, v in enumerate(("0.2", "1.8", "0.2")):
            x = 1.0 + i * 1.75
            cells.add(VGroup(RoundedRectangle(width=1.5, height=1.2, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == 1 else DIM,
                                              stroke_width=6 if i == 1 else 4).move_to([x, 0.0, 0]),
                             T(v, 52).move_to([x, 0.0, 0])))
        nl = T("numbers, in metres", 34).move_to([2.75, -1.2, 0])
        self.play(FadeOut(VGroup(ey, stk, lk)), FadeIn(cells), FadeIn(nl), run_time=0.45)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · Metres, Axes and Applied Scale  (B19-B32, all Manim; B21/B24/B26/B28/B29 carry REAL captures as ImageMobjects)

One cast for the act: the COLUMN and its side view (Act I's language: Godot's Y up, Z across, 1.5 scene units per metre),
the 1 m dimension bar, the player's capsule, and one 2 m cube that is scaled down to the column. Numbers on screen are real
probe output (evidence/probe/*.log, evidence/act3/*.log) or values read from the real captures; nothing is invented.
Captures (all real): pantry/a3_demo_capsule_lit.png (Godot's platformer demo, collision shapes on, orthographic side view),
pantry/a3_yup_on|off_tight.png (Blender 5.1.2's glTF export dialog), pantry/a3_bl_transform_*.png and a3_bl_apply_menu.png
(Blender's Properties editor and Apply menu), pantry/a3_docs_*.png (two public Godot docs pages).
"""

A3_U = 1.5                                   # side view: scene units per metre (same as Act I)
A3_O = np.array([-3.3, -2.55, 0.0])          # side view: ground point under the column's bottom-right corner
A3_W, A3_H = 0.2, 1.8                        # the column, metres


# ───────────────────────── shared pieces ─────────────────────────
def a3_axes(up="Y up", across="Z"):
    """Side-view axes (Act I's): vertical up, horizontal across, meeting at the left of the ground line."""
    y_ax = Arrow([-6.0, -2.55, 0], [-6.0, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    z_ax = Arrow([-6.0, -2.55, 0], [-0.1, -2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    ly = T(up, 34).move_to([-5.25, 1.1, 0])
    lz = T(across, 34).move_to([0.3, -2.55, 0])
    return y_ax, z_ax, ly, lz


def a3_rect(w_m, h_m, fill=BOX_L):
    """A column in the side view standing on the ground with its bottom-RIGHT corner at A3_O."""
    r = Rectangle(width=w_m * A3_U, height=h_m * A3_U, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5)
    r.move_to(A3_O + np.array([-w_m * A3_U / 2, h_m * A3_U / 2, 0]))
    return r


def a3_chips(vals, x0=1.0, y=1.15, hi=None, labels="XYZ", dx=1.95):
    """Three outlined cells X / Y / Z with their numbers. No fill behind text; `hi` rings one cell."""
    cells = VGroup()
    for i, (ax, v) in enumerate(zip(labels, vals)):
        x = x0 + i * dx
        box = RoundedRectangle(width=1.6, height=1.55, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == hi else DIM,
                               stroke_width=6 if i == hi else 4).move_to([x, y, 0])
        a = T(ax, 36, DIM).move_to([x, y + 0.42, 0])
        n = T(v, 62).move_to([x, y - 0.22, 0])
        cells.add(VGroup(box, a, n))
    return cells


def a3_file(x, y, w=0.95, h=1.2):
    """A drawn file icon (for the glTF/glb file): page outline with a folded corner."""
    x0, x1, y0, y1, f = x - w / 2, x + w / 2, y - h / 2, y + h / 2, 0.3
    page = Polygon([x0, y0, 0], [x1, y0, 0], [x1, y1 - f, 0], [x1 - f, y1, 0], [x0, y1, 0],
                   fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5)
    fold = Polygon([x1 - f, y1, 0], [x1 - f, y1 - f, 0], [x1, y1 - f, 0], fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(page, fold)


def a3_mark(kind, x, y, h=1.2):
    if kind == "blender":
        return ImageMobject("pantry/icon_blender.png").set_height(h).move_to([x, y, 0])
    if kind == "godot":
        return ImageMobject("pantry/icon_godot.png").set_height(h).move_to([x, y, 0])
    return a3_file(x, y, 0.95 * h / 1.2, h)


def a3_bar(x, y, half=1.2):
    """The 1 m bar of the unit beats: one dimension line, the same length in every place it appears."""
    return dim_arrow([x - half, y, 0], [x + half, y, 0])


def a3_cross(x, y, s=0.22, color=INK, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a3_capsule(cx, cy, u=1.0, color=INK, sw=5):
    """The player's collision capsule drawn to scale: 0.4 m radius, 2.1 m tall, `u` scene units per metre."""
    return RoundedRectangle(width=0.8 * u, height=2.1 * u, corner_radius=0.4 * u, fill_opacity=0, stroke_color=color,
                            stroke_width=sw).move_to([cx, cy, 0])


# ═════════════════════════ B19 · units: one bar, three places ═════════════════════════
A3_UX = [-4.4, 0.0, 4.4]                       # the three places: Blender, glTF, Godot
A3_UKIND = ["blender", "gltf", "godot"]
A3_UNAME = ["Blender", "glTF", "Godot"]
A3_UNOTE = ["1 unit = 1 m", "all in metres", "1 unit = 1 m"]
A3_UY = dict(mark=1.65, name=0.25, bar=-0.85, note=-1.6)


def a3_unit_place(i):
    """(mark, name, bar, note) for place i of the unit beats."""
    x = A3_UX[i]
    return (a3_mark(A3_UKIND[i], x, A3_UY["mark"], 1.9), T(A3_UNAME[i], 44).move_to([x, A3_UY["name"], 0]),
            a3_bar(x, A3_UY["bar"], 1.5), T(A3_UNOTE[i], 44).move_to([x, A3_UY["note"], 0]))


class B19_UnitBar(Scene):
    def construct(self):
        title = T("Metres, Axes and Applied Scale", 40).move_to([-2.6, 3.05, 0])
        self.add(title)
        parts = [a3_unit_place(i) for i in range(3)]
        for mark, name, bar, note in parts:           # the pipeline is on stage from the start: Blender, glTF file, Godot
            self.add(mark, name)
        phrases = ["one unit is one metre", "every linear distance is in metres", "one unit in three-D is one metre"]
        for i in range(3):
            mark, name, bar, note = parts[i]
            until(self, phrases[i], lead=0.35)
            self.play(Create(bar), FadeIn(note), run_time=0.5)
        done(self)


# ═════════════════════════ B20 · no conversion on the way ═════════════════════════
class B20_NoConversion(Scene):
    def construct(self):
        for i in range(3):
            self.add(*a3_unit_place(i))
        y = A3_UY["mark"]
        a1 = Arrow([-3.3, y, 0], [-1.2, y, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        a2 = Arrow([1.2, y, 0], [3.3, y, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        x1 = T("× 1", 40).move_to([-2.25, y + 0.5, 0])
        x2 = T("× 1", 40).move_to([2.25, y + 0.5, 0])
        until(self, "no conversion", lead=0.1)
        self.play(Create(a1), FadeIn(x1), run_time=0.4)
        self.play(Create(a2), FadeIn(x2), run_time=0.4)
        rider = Dot([-3.3, y, 0], radius=0.13, color=TERRA)
        self.add(rider)
        self.play(rider.animate.move_to([3.3, y, 0]), run_time=1.0, rate_func=linear)
        until(self, "as long as Blender's unit scale", lead=0.1)
        cell = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-4.4, -2.75, 0])
        cl = T("unit scale", 34, DIM).move_to([-4.4, -2.5, 0])
        cn = T("1.0", 50).move_to([-4.4, -2.97, 0])
        self.play(Create(cell), FadeIn(cl), FadeIn(cn), run_time=0.5)
        lg = M("scale_length=1.0", 32, DIM).move_to([-1.0, -2.75, 0])
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ═════════════════════════ B21 · the platformer demo's capsule: 2.1 m, gravity 22, 120 ticks ═════════════════════════
# Real capture: Godot's 3D platformer demo, Debug > Visible Collision Shapes on, orthographic side view whose 3.6 m tall view
# is shown 4.05 units tall (1.125 units per metre), the capsule centred on the picture. (evidence/act3/capture_demo.gd)
A3_IMG = np.array([2.6, 0.0, 0.0])
A3_K = 1.125                                   # scene units per metre inside the capture


class B21_Capsule(Scene):
    def construct(self):
        img = ImageMobject("pantry/a3_demo_capsule_lit.png").set_width(7.2).move_to(A3_IMG)
        cap = T("3D platformer demo", 36).move_to([2.6, 2.5, 0])
        self.play(FadeIn(img), FadeIn(cap), run_time=0.7)
        until(self, "collision capsule", lead=0.3)
        shape = a3_capsule(2.6, 0.0, A3_K, CARD, 8)
        hh = 2.1 * A3_K / 2
        dim = dim_arrow([-1.4, -hh, 0], [-1.4, hh, 0])
        dl = T("2.1 m", 48).move_to([-2.45, 0.0, 0])
        self.play(Create(shape), Create(dim), FadeIn(dl), run_time=0.8)
        until(self, "under gravity of", lead=0.2)
        g = VGroup(RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-4.75, 1.6, 0]),
                   T("gravity", 34, DIM).move_to([-4.75, 1.97, 0]), T("22", 56).move_to([-4.4, 1.38, 0]))
        garrow = Arrow([-5.5, 1.65, 0], [-5.5, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(g), Create(garrow), run_time=0.5)
        gl = M("3d/default_gravity=22.0", 32, DIM).move_to([-3.1, -2.6, 0])
        self.play(FadeIn(gl), run_time=0.3)
        until(self, "at a hundred and twenty", lead=0.2)
        t = VGroup(RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-4.75, -0.3, 0]),
                   T("ticks / s", 34, DIM).move_to([-4.75, 0.07, 0]), T("120", 56).move_to([-4.75, -0.52, 0]))
        self.play(FadeIn(t), run_time=0.5)
        tl = M("common/physics_ticks_per_second=120", 32, DIM).move_to([-1.6, -3.05, 0])
        self.play(FadeIn(tl), run_time=0.3)
        done(self)


# ═════════════════════════ B22 · a prop at the wrong scale: a wall, or a step it never notices ═════════════════════════
class B22_WrongScale(Scene):
    def construct(self):
        g1, g2 = 0.55, -2.75
        ground1 = Line([-6.0, g1, 0], [6.0, g1, 0], color=INK, stroke_width=5)
        ground2 = Line([-6.0, g2, 0], [6.0, g2, 0], color=INK, stroke_width=5)
        cap1 = a3_capsule(-4.4, g1 + 1.05, 1.0, INK, 5)
        cap2 = a3_capsule(-4.4, g2 + 1.05, 1.0, INK, 5)
        self.add(ground1, ground2, cap1, cap2)
        until(self, "wrong scale", lead=0.4)
        wall = Rectangle(width=0.6, height=2.4, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.9, g1 + 1.2, 0])
        step = Rectangle(width=0.6, height=0.14, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.9, g2 + 0.07, 0])
        self.play(GrowFromEdge(wall, DOWN), GrowFromEdge(step, DOWN), run_time=0.5)
        until(self, "a wall the robot", lead=0.6)
        self.play(cap1.animate.shift(RIGHT * 4.6), run_time=1.0, rate_func=smooth)
        spark = Dot([0.6, g1 + 1.3, 0], radius=0.12, color=TERRA)
        wl = T("wall", 40).move_to([2.3, g1 + 1.2, 0])
        self.play(FadeIn(spark), FadeIn(wl), run_time=0.3)
        until(self, "or a step it never notices", lead=0.3)
        sl = T("step", 40).move_to([4.7, g2 + 0.45, 0])
        self.play(FadeIn(sl), run_time=0.3)
        self.play(cap2.animate.shift(RIGHT * 4.2), run_time=0.7, rate_func=smooth)
        self.play(cap2.animate.shift(RIGHT * 2.6 + UP * 0.14), run_time=0.5, rate_func=smooth)
        done(self)


# ═════════════════════════ B23 · direction: Blender's Z-up world, glTF/Godot's Y-up world (isometric) ═════════════════════════
class B23_Turn(Scene):
    def construct(self):
        ib = Iso(-3.7, -1.7, 1.5)         # Blender's world (left): X back-right, Y back-left, Z up
        ig = Iso(3.4, -1.7, 1.5)          # glTF / Godot's world (right): X back-right, Y up, Z toward the viewer (iso -y)
        o = ib.p(0, 0, 0)
        ebx, eby, ebz = ib.p(1.55, 0, 0), ib.p(0, 1.55, 0), ib.p(0, 0, 2.09)
        bx, by, bz = [Arrow(o, tip, buff=0, color=INK, stroke_width=5, tip_length=0.22) for tip in (ebx, eby, ebz)]
        lbx = T("X", 40).move_to(ebx + np.array([0.35, 0.12, 0]))
        lby = T("Y", 40).move_to(eby + np.array([-0.35, 0.12, 0]))
        lbz = T("Z", 40).move_to(ebz + np.array([0.0, 0.42, 0]))
        bicon = a3_mark("blender", -3.7, 2.65, 0.95)
        o2 = ig.p(0, 0, 0)
        egx, egy, egz = ig.p(1.55, 0, 0), ig.p(0, 0, 2.09), ig.p(0, -1.55, 0)
        gx, gy, gz = [Arrow(o2, tip, buff=0, color=INK, stroke_width=5, tip_length=0.22) for tip in (egx, egy, egz)]
        lgx = T("X", 40).move_to(egx + np.array([0.35, 0.12, 0]))
        lgy = T("Y", 40).move_to(egy + np.array([0.0, 0.42, 0]))
        lgz = T("Z", 40).move_to(egz + np.array([0.38, -0.1, 0]))
        gfile = a3_file(2.55, 2.65, 0.75, 0.95)
        gicon = a3_mark("godot", 3.9, 2.65, 0.95)
        cap_b = T("Z up", 40).move_to([-3.7, -3.0, 0])
        cap_g = T("Y up", 40).move_to([3.4, -3.0, 0])
        self.add(bicon)
        until(self, "Blender is right-handed", lead=0.2)
        self.play(Create(bx), Create(by), FadeIn(lbx), FadeIn(lby), run_time=0.6)
        until(self, "Z pointing up", lead=0.45)
        up = Dot(ebz, radius=0.11, color=TERRA)
        self.play(Create(bz), FadeIn(lbz), FadeIn(cap_b), run_time=0.5)
        self.play(FadeIn(up), run_time=0.2)
        until(self, "The glTF format and Godot", lead=0.2)
        self.play(FadeIn(gfile), FadeIn(gicon), Create(gx), Create(gz), FadeIn(lgx), FadeIn(lgz), run_time=0.7)
        until(self, "Y pointing up", lead=0.45)
        up2 = Dot(egy, radius=0.11, color=TERRA)
        self.play(Create(gy), FadeIn(lgy), FadeIn(cap_g), run_time=0.5)
        self.play(FadeIn(up2), run_time=0.2)
        until(self, "Somebody has to turn the world", lead=0.2)
        arc = ArcBetweenPoints(np.array([-1.9, 2.1, 0]), np.array([1.1, 2.1, 0]), angle=-TAU / 5)
        arc.add_tip(tip_length=0.22)
        arc.set_stroke(INK, 5)
        turn = T("turn", 40).move_to([-0.4, 3.1, 0])
        self.play(Create(arc), FadeIn(turn), run_time=0.7)
        done(self)


# ═════════════════════════ B24 · the exporter's +Y Up option maps Blender's Z extent onto Godot's Y ═════════════════════════
# Real captures: Blender 5.1.2's glTF export dialog, Transform panel (pantry/a3_yup_on_row.png).
# Real numbers: evidence/act3/extents_probe.log - a box with THREE different extents, so a swap cannot hide.
class B24_YUp(Scene):
    def construct(self):
        panel = ImageMobject("pantry/a3_yup_on_row.png").set_width(5.2).move_to([-3.4, 1.5, 0])
        pcap = T("glTF export dialog", 36).move_to([-3.4, 2.95, 0])
        self.add(panel, pcap)
        until(self, "plus Y up", lead=0.3)
        # the +Y Up row sits at 0.7 of the crop's height
        spark = Dot([-6.15, 1.5 + 1.105 - 0.768 * 2.21, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "on by default", lead=0.3)
        dflt = T("on by default", 38).move_to([-3.4, -0.2, 0])
        self.play(FadeIn(dflt), run_time=0.3)
        until(self, "It puts", lead=1.0)
        X0, DX = 1.7, 1.8
        bicon = a3_mark("blender", 0.1, 1.75, 0.7)
        gicon = a3_mark("godot", 0.1, -1.1, 0.7)
        brow = a3_chips(["0.2", "0.6", "1.8"], x0=X0, y=1.75, hi=2, dx=DX)
        grow = VGroup(*[RoundedRectangle(width=1.6, height=1.55, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == 1 else DIM,
                                          stroke_width=6 if i == 1 else 4).move_to([X0 + i * DX, -1.1, 0]) for i in range(3)])
        glet = VGroup(*[T(ax, 36, DIM).move_to([X0 + i * DX, -1.1 + 0.42, 0]) for i, ax in enumerate("XYZ")])
        tb = T("test box", 38).move_to([X0 + DX, 2.95, 0])
        self.play(FadeIn(bicon), FadeIn(brow), FadeIn(gicon), FadeIn(grow), FadeIn(glet), FadeIn(tb), run_time=0.6)
        until(self, "Blender's Z extent", lead=0.1)
        n18 = brow[2][2].copy()
        self.play(n18.animate.move_to([X0 + DX, -1.1 - 0.22, 0]), run_time=0.6)
        until(self, "and Blender's Y extent", lead=0.1)
        n06 = brow[1][2].copy()
        self.play(n06.animate.move_to([X0 + 2 * DX, -1.1 - 0.22, 0]), run_time=0.6)
        n02 = brow[0][2].copy()
        self.play(n02.animate.move_to([X0, -1.1 - 0.22, 0]), run_time=0.5)
        until(self, "a claim a test can check", lead=0.2)
        l1 = M("Blender extents X, Y, Z = (0.2, 0.6, 1.8)", 32, DIM).move_to([-0.9, -2.55, 0])
        l2 = M("Godot extents X, Y, Z = (0.2, 1.8, 0.6)", 32).move_to([-1.15, -3.05, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        done(self)


# ═════════════════════════ B25 · switch +Y Up off: the second column lies on its side ═════════════════════════
class B25_YUpOff(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a3_axes("Y up", "Z")
        col = a3_rect(A3_W, A3_H)
        cap = T("bounding box, in metres", 36).move_to([2.6, 2.45, 0])
        chips = a3_chips(["0.2", "1.8", "0.2"], hi=1)
        ring = Dot([A3_O[0] - 0.15, A3_O[1] + 1.8 * A3_U + 0.2, 0], radius=0.12, color=TERRA)
        on = ImageMobject("pantry/a3_yup_on_row.png").set_width(4.2).move_to([-3.5, 2.35, 0])
        off = ImageMobject("pantry/a3_yup_off_row.png").set_width(4.2).move_to([-3.5, 2.35, 0])
        self.add(y_ax, z_ax, ly, lz, col, cap, chips, ring, on)
        until(self, "Switch the option off", lead=0.2)
        self.play(FadeOut(on), FadeIn(off), run_time=0.3)
        until(self, "second column", lead=0.5)
        self.play(FadeOut(ring), Rotate(col, angle=-PI / 2, about_point=A3_O.copy()), run_time=1.0)
        lab = T("1.8 now along Z", 34).move_to([-3.7, -1.5, 0])
        self.play(FadeIn(lab), run_time=0.3)
        until(self, "one point eight on the wrong axis", lead=0.2)
        newvals = a3_chips(["0.2", "0.2", "1.8"], hi=2)
        self.play(Transform(chips[1][2], newvals[1][2]), Transform(chips[2][2], newvals[2][2]),
                  chips[1][0].animate.set_stroke(DIM, 4), chips[2][0].animate.set_stroke(INK, 6), run_time=0.7)
        ring2 = Dot([1.0 + 2 * 1.95 + 0.62, 1.15 + 0.62, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(ring2), run_time=0.3)
        until(self, "and a column lying on its side", lead=0.2)
        lg = M("mesh AABB size (0.2, 0.2, 1.8)", 32, DIM).move_to([2.2, -1.5, 0])
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ═════════════════════════ B26 · a transform vs. mesh data: the vertices still describe a 2 m cube ═════════════════════════
# Real captures: Blender 5.1.2's Properties > Object > Transform panel (a3_bl_transform_after.png = scale 1.000, as the 2 m cube is added;
# a3_bl_transform_before.png = scale 0.1, 0.1, 0.9). Real numbers: evidence/act3/apply_probe.log (vertices span 2.0, 2.0, 2.0).
A3_OB = np.array([-3.4, -0.1, 0.0])           # the object (cube -> pole), centre
A3_OU = 1.35                                  # scene units per metre


def a3_cube_parts(c=A3_OB, u=A3_OU):
    cube = Rectangle(width=2 * u, height=2 * u, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(c)
    ghost = Rectangle(width=2 * u, height=2 * u, fill_opacity=0, stroke_color=DIM, stroke_width=6).move_to(c)
    pole = Rectangle(width=0.2 * u, height=1.8 * u, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(c)
    dots = VGroup(*[Dot([c[0] + sx * u, c[1] + sy * u, 0], radius=0.11, color=TERRA) for sx in (-1, 1) for sy in (-1, 1)])
    return cube, ghost, pole, dots


class B26_TransformVsMesh(Scene):
    def construct(self):
        cube, ghost, pole, dots = a3_cube_parts()
        self.add(ghost, cube)
        p_after = ImageMobject("pantry/a3_bl_transform_after.png").set_width(6.4).move_to([2.9, 0.3, 0])
        p_before = ImageMobject("pantry/a3_bl_transform_before.png").set_width(6.4).move_to([2.9, 0.3, 0])
        tl = T("transform", 40).move_to([2.9, 2.1, 0])
        ml = T("mesh data", 40).move_to([-3.4, 1.8, 0])
        vl = T("vertices", 36).move_to([-3.4, -1.8, 0])
        until(self, "a transform", lead=0.2)
        self.play(FadeIn(p_after), FadeIn(tl), run_time=0.5)
        until(self, "separate mesh data", lead=0.6)
        self.play(FadeIn(ml), Create(dots), run_time=0.5)
        until(self, "the vertices", lead=0.9)
        self.play(FadeIn(vl), run_time=0.3)
        until(self, "scale it down to a pole", lead=0.2)
        ring = RoundedRectangle(width=5.65, height=0.82, corner_radius=0.12, fill_opacity=0, stroke_color=TERRA, stroke_width=6).move_to([2.96, 0.3 + (0.5 - 0.845) * 2.738, 0])
        self.play(Transform(cube, pole), FadeOut(p_after), FadeIn(p_before), run_time=1.0)
        self.play(Create(ring), run_time=0.4)
        until(self, "still describe", lead=0.4)
        lg = M("vertices span (2.0, 2.0, 2.0)", 32, DIM).move_to([-2.5, -2.75, 0])
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ═════════════════════════ B27 · the exporter writes that scale onto the node; Godot draws right and measures wrong ═════════════════════════
# Real: the exported file's own JSON (evidence/act3/glb_json.log, float32 noise rounded) and Godot's own readout (evidence/probe/godot-mutations.log).
class B27_NodeScale(Scene):
    def construct(self):
        cube, ghost, pole, dots = a3_cube_parts(np.array([-4.3, 0.1, 0.0]), 1.25)
        bicon = a3_mark("blender", -4.3, 2.55, 1.0)
        self.add(ghost, pole, dots, bicon)
        spark = Dot([-4.3, 0.1 + 0.9 * 1.25 + 0.25, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "The exporter writes", lead=0.3)
        file = a3_file(-0.6, 2.55, 0.75, 0.95)
        arr1 = Arrow([-3.4, 2.55, 0], [-1.4, 2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(file), Create(arr1), run_time=0.5)
        until(self, "onto the node", lead=0.2)
        j1 = M('"scale": [0.1, 0.9, 0.1]', 32).move_to([-2.2 + 3.0, 1.55, 0])
        self.play(FadeIn(j1), run_time=0.3)
        j2 = M('"min": [-1, -1, -1]', 32, DIM).move_to([-2.2 + 2.375, 1.0, 0])
        j3 = M('"max": [1, 1, 1]', 32, DIM).move_to([-2.2 + 2.0, 0.45, 0])
        self.play(FadeIn(j2), FadeIn(j3), run_time=0.3)
        until(self, "and Godot shows", lead=0.1)
        gicon = a3_mark("godot", 4.0, 2.55, 1.0)
        arr2 = Arrow([0.3, 2.55, 0], [3.2, 2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(gicon), Create(arr2), run_time=0.5)
        until(self, "a scale that isn't one", lead=0.2)
        r1 = M("node scale (0.1, 0.9, 0.1)", 32).move_to([6.2 - 3.25, -0.9, 0])
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "It draws right", lead=0.2)
        r2 = M("AABB in scene (0.2, 1.8, 0.2)", 32).move_to([6.2 - 3.625, -1.6, 0])
        ok = check(-1.75, -1.6, 0.2, INK, 7)
        self.play(FadeIn(r2), Create(ok), run_time=0.4)
        until(self, "and measures wrong", lead=0.2)
        r3 = M("mesh AABB size (2.0, 2.0, 2.0)", 32).move_to([6.2 - 3.75, -2.3, 0])
        no = a3_cross(-1.75, -2.3, 0.2, INK, 7)
        self.play(FadeIn(r3), Create(no), run_time=0.4)
        done(self)


# ═════════════════════════ B28 · what Godot's own documentation says (two public pages, as themselves) ═════════════════════════
# Real captures (evidence/act3/capture_docs.py, 2026-10-06, stable docs): the section's heading + paragraph, crops of the live pages.
class B28_GodotDocs(Scene):
    def construct(self):
        W = 11.4
        c1 = ImageMobject("pantry/a3_docs_collision.png").set_width(W).move_to([0, 1.55, 0])
        h1 = W * 579 / 2637
        c2 = ImageMobject("pantry/a3_docs_export.png").set_width(W).move_to([0, -1.55, 0])
        h2 = W * 250 / 2637
        f1 = Rectangle(width=W, height=h1, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([0, 1.55, 0])
        f2 = Rectangle(width=W, height=h2, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([0, -1.55, 0])
        k1 = T("docs.godotengine.org: Collision shapes (3D)", 36).move_to([0, 1.55 - h1 / 2 - 0.4, 0])
        k2 = T("docs.godotengine.org: Model export considerations", 36).move_to([0, -1.55 - h2 / 2 - 0.4, 0])
        dt = T("stable docs, captured 6 October 2026", 32, DIM).move_to([0, -3.1, 0])
        # the phrase boxes (fractions of each crop, from capture_docs.json)
        def ring(cx, cy, w, h, box, pad=0.07):
            x0, y0, x1, y1 = box
            return Rectangle(width=(x1 - x0) * w + 2 * pad, height=(y1 - y0) * h + 2 * pad, fill_color=TERRA, fill_opacity=0.28,
                             stroke_width=0).move_to([cx - w / 2 + (x0 + x1) / 2 * w, cy + h / 2 - (y0 + y1) / 2 * h, 0])
        r1 = ring(0, 1.55, W, h1, [0.3562, 0.6575, 0.8416, 0.7680])
        r2a = ring(0, -1.55, W, h2, [0.6433, 0.2051, 0.9722, 0.4615])
        r2b = ring(0, -1.55, W, h2, [0.0170, 0.5256, 0.4397, 0.7821])
        r1b = ring(0, 1.55, W, h1, [0.0175, 0.8000, 0.4110, 0.9500])
        self.play(FadeIn(c1), Create(f1), FadeIn(k1), run_time=0.5)
        until(self, "avoid scaling collision shapes", lead=0.5)
        self.play(FadeIn(r1), run_time=0.5)
        until(self, "so the physics engine", lead=0.4)
        self.play(FadeIn(r1b), run_time=0.4)
        until(self, "export guidance", lead=0.9)
        self.play(FadeIn(c2), Create(f2), FadeIn(k2), FadeIn(dt), run_time=0.5)
        until(self, "apply the object transform", lead=0.3)
        self.play(FadeIn(r2a), run_time=0.4)
        until(self, "in the modelling software", lead=0.3)
        self.play(FadeIn(r2b), run_time=0.4)
        done(self)


# ═════════════════════════ B29 · Object > Apply > Rotation & Scale; afterwards the scale is one ═════════════════════════
# Real: Blender 5.1.2's own Apply menu and Transform panel (pantry/a3_bl_apply_menu.png, a3_bl_transform_*.png);
# the one-call form is the line from evidence/probe/make_mutations.py; the result is evidence/act3/apply_probe.log.
class B29_ApplyScale(Scene):
    def construct(self):
        menu = ImageMobject("pantry/a3_bl_apply_menu.png").set_width(4.6).move_to([-2.2, 1.45, 0])
        mframe = Rectangle(width=4.6, height=4.6 * 570 / 810, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([-2.2, 1.45, 0])
        path = T("Object > Apply", 40).move_to([2.2, 2.55, 0])
        bicon = a3_mark("blender", 4.9, 2.55, 0.8)
        p_before = ImageMobject("pantry/a3_bl_transform_before.png").set_width(5.6).move_to([3.3, 0.35, 0])
        p_after = ImageMobject("pantry/a3_bl_transform_after.png").set_width(5.6).move_to([3.3, 0.35, 0])
        self.play(FadeIn(menu), Create(mframe), FadeIn(path), FadeIn(bicon), FadeIn(p_before), run_time=0.5)
        until(self, "Rotation and Scale", lead=0.5)
        spark = Dot([0.3, 1.45 + 1.62 - 0.84 * 3.237, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "In a script", lead=0.2)
        c1 = M("bpy.ops.object.transform_apply(", 32).move_to([-5.7 + 15.5 * 0.5 + 0.0, -2.2, 0])
        c1.move_to([-5.7 + len("bpy.ops.object.transform_apply(") * 0.125, -2.2, 0])
        c2 = M("    location=False, rotation=True, scale=True)", 32).move_to([-5.7 + len("    location=False, rotation=True, scale=True)") * 0.125, -2.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        until(self, "Afterwards", lead=0.3)
        cube, ghost, pole, dots = a3_cube_parts(np.array([-2.4, 1.0, 0.0]), 1.2)
        old = Group(menu, mframe, spark, path)
        self.play(FadeOut(old), run_time=0.3)
        self.add(ghost, pole, dots)
        self.play(FadeIn(ghost), FadeIn(pole), FadeIn(dots), run_time=0.4)
        until(self, "the scale is one", lead=0.2)
        ring = RoundedRectangle(width=5.65, height=0.82, corner_radius=0.12, fill_opacity=0, stroke_color=TERRA, stroke_width=6).move_to([3.06, 0.35 + (0.5 - 0.845) * 5.6 * 1020 / 2384, 0])
        self.play(FadeOut(p_before), FadeIn(p_after), run_time=0.3)
        self.play(Create(ring), run_time=0.3)
        until(self, "the vertices carry the real size", lead=0.2)
        targets = [np.array([-2.4 + sx * 0.12, 1.0 + sy * 1.08, 0]) for sx in (-1, 1) for sy in (-1, 1)]
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], FadeOut(ghost), run_time=0.8)
        lg = M("vertices span (0.2, 0.2, 1.8)", 32, DIM).move_to([2.5, -1.5, 0])
        self.play(FadeIn(lg), run_time=0.3)
        done(self)


# ═════════════════════════ B30 · a test checks both halves ═════════════════════════
# Real: the 'good' line of evidence/probe/godot-mutations.log (the column that arrives right).
class B30_BothHalves(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a3_axes("Y up", "Z")
        col = a3_rect(A3_W, A3_H)
        l1 = T("unit scale", 40).move_to([4.6, 1.5, 0])
        l2 = T("size in metres", 40).move_to([3.9, -0.5, 0])
        self.add(y_ax, z_ax, ly, lz, col, l1, l2)
        until(self, "unit scale on every node", lead=0.4)
        r1 = M("node scale (1.0, 1.0, 1.0)", 32).move_to([6.2 - 3.25, 0.85, 0])
        k1 = check(-0.75, 0.85, 0.22, INK, 8)
        self.play(FadeIn(r1), Create(k1), run_time=0.4)
        until(self, "the right size in metres", lead=0.3)
        r2 = M("mesh AABB size (0.2, 1.8, 0.2)", 32).move_to([6.2 - 3.75, -1.15, 0])
        k2 = check(-1.75, -1.15, 0.22, INK, 8)
        self.play(FadeIn(r2), Create(k2), run_time=0.4)
        done(self)


# ═════════════════════════ B31 · the stale-dimensions trap: set the scale, print right away, get the old size ═════════════════════════
# Real: evidence/probe/stale_dimensions.py (wrapped over two lines for width: same tokens) and its output, evidence/probe/stale-dimensions.log
A3_CX = -5.7                                   # code block left edge
A3_CH = 0.125                                  # Menlo 32: scene units per character


def a3_code(s, y, color=INK):
    return M(s, 32, color).move_to([A3_CX + len(s) * A3_CH, y, 0])


A3_STALE = dict(
    r1=('o.scale = (0.1, 0.1, 0.9)', 2.35),
    r2=('print("BEFORE view_layer.update():",', 1.8),
    r3=('      tuple(round(v, 4) for v in o.dimensions))', 1.3),
    r4=('bpy.context.view_layer.update()', 0.55),
    r5=('print("AFTER  view_layer.update():",', 0.0),
    r6=('      tuple(round(v, 4) for v in o.dimensions))', -0.5),
    o1=('BEFORE view_layer.update(): (2.0, 2.0, 2.0)', -1.7),
    o2=('AFTER  view_layer.update(): (0.2, 0.2, 1.8)', -2.3),
)


def a3_num_dots(key, nums, dy=-0.33):
    """Terracotta dots under the numbers of one output line (so the voice can point at each one)."""
    text, y = A3_STALE[key]
    out, start = [], 0
    for n in nums:
        i = text.index(n, start)
        start = i + len(n)
        out.append(Dot([A3_CX + (i + len(n) / 2.0) * 2 * A3_CH, y + dy, 0], radius=0.09, color=TERRA))
    return out


class B31_StaleDims(Scene):
    def construct(self):
        P = A3_STALE
        bicon = a3_mark("blender", 5.4, 2.35, 0.8)
        bl = T("Blender 5.1", 36).move_to([3.1, 2.35, 0])
        self.add(bicon, bl)
        until(self, "In Blender five point one", lead=0.3)
        r1 = a3_code(*P["r1"])
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "dimensions don't refresh", lead=0.5)
        r2, r3 = a3_code(*P["r2"]), a3_code(*P["r3"])
        self.play(FadeIn(r2), FadeIn(r3), run_time=0.4)
        until(self, "Set the scale", lead=0.2)
        ptr = Dot([A3_CX - 0.4, P["r1"][1], 0], radius=0.11, color=TERRA)
        self.play(FadeIn(ptr), run_time=0.2)
        until(self, "print the dimensions", lead=0.3)
        self.play(ptr.animate.move_to([A3_CX - 0.4, P["r2"][1], 0]), run_time=0.4)
        until(self, "you get the old size", lead=0.5)
        o1 = a3_code(*P["o1"])
        self.play(ptr.animate.move_to([A3_CX - 0.4, P["o1"][1], 0]), FadeIn(o1), run_time=0.5)
        d1, d2, d3 = a3_num_dots("o1", ["2.0", "2.0", "2.0"])
        until(self, "two, two, two", lead=0.4)
        self.play(FadeIn(d1), run_time=0.12)
        self.wait(0.1)
        self.play(FadeIn(d2), run_time=0.12)
        self.wait(0.1)
        self.play(FadeIn(d3), run_time=0.12)
        done(self)


# ═════════════════════════ B32 · update the view layer first, and the log is current ═════════════════════════
class B32_Update(Scene):
    def construct(self):
        P = A3_STALE
        bicon = a3_mark("blender", 5.4, 2.35, 0.8)
        bl = T("Blender 5.1", 36).move_to([3.1, 2.35, 0])
        rows = [a3_code(*P[k]) for k in ("r1", "r2", "r3")]
        o1 = a3_code(*P["o1"])
        self.add(bicon, bl, *rows, o1)
        until(self, "Update the view layer", lead=0.1)
        r4 = a3_code(*P["r4"])
        ptr = Dot([A3_CX - 0.4, P["r4"][1], 0], radius=0.11, color=TERRA)
        self.play(FadeIn(r4), FadeIn(ptr), run_time=0.3)
        until(self, "you get point two", lead=0.9)
        r5, r6 = a3_code(*P["r5"]), a3_code(*P["r6"])
        self.play(FadeIn(r5), FadeIn(r6), ptr.animate.move_to([A3_CX - 0.4, P["r5"][1], 0]), run_time=0.4)
        until(self, "point two, point two", lead=0.5)
        o2 = a3_code(*P["o2"])
        self.play(ptr.animate.move_to([A3_CX - 0.4, P["o2"][1], 0]), FadeIn(o2), run_time=0.4)
        e1, e2, e3 = a3_num_dots("o2", ["0.2", "0.2", "1.8"])
        until(self, "point two, point two", lead=0.0)
        self.play(FadeIn(e1), run_time=0.12)
        self.wait(0.4)
        self.play(FadeIn(e2), run_time=0.12)
        until(self, "one point eight", lead=0.1)
        self.play(FadeIn(e3), run_time=0.12)
        until(self, "If an agent's log is its evidence", lead=0.1)
        ok = check(A3_CX + 2 * len(P["o2"][0]) * A3_CH + 0.6, P["o2"][1], 0.22, INK, 8)
        self.play(o1.animate.set_color(DIM), Create(ok), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · What Godot Builds From a File  (B33A–B41, B43, B44 Manim; B42 is a Remotion BrowserCapture, see lanes/act4.json)

One cast for the act, one story: FILE -> IMPORT SETTINGS -> NAMES -> COLLIDERS.
  * the checkpoint post: the real Blender renders (pantry/a4_post.png, a4_post_hull.png) and its side-view silhouette
    (base 0.6 x 0.1 m, pole 0.16 m wide, 1.8 m tall: the real geometry of the post's final script);
  * the Godot icon as the destination of every file;
  * ONE import file: the demo's enemy.glb.import, quoted line for line (its lines 24 and 25 are the two that matter).
Everything typed in Menlo is real: lines of enemy.glb.import, lines of a recorded glTF export, recorded git output, the
recorded import trees of Godot 4.7.2 (evidence/act4/out/*.log), or the real scene text of enemy.tscn. Nothing is invented.
"""

A4_K = 2.0                                     # side-view silhouette: scene units per metre


# ═════════════════════════════ helpers ═════════════════════════════
def a4_mw(s, size=32):
    """Menlo width of a string, exact at the sizes used (Pango quantises the size: 32 -> 0.2483, 34-38 -> 0.297, 40-44 -> 0.347)."""
    per = 0.2483 if size <= 32 else 0.2975 if size <= 38 else 0.347 if size <= 44 else 0.396
    return per * len(s)


def a4_put(mob, x, y):
    """Place a Text/Group so its LEFT edge sits at x (measured width, never get_left())."""
    return mob.move_to([x + mob.width / 2, y, 0])


def a4_chip(s, x, y, size=36, mono=True, color=INK, sw=4, padx=0.34, hgt=None, dash=False):
    """An outline-only chip with its text. Returns VGroup(box, text). No fill behind text."""
    t = (M(s, size, color) if mono else T(s, size, color)).move_to([x, y, 0])
    w = t.width + 2 * padx
    h = hgt if hgt else 0.0125 * size + 0.55
    if dash:
        box = DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=color, stroke_width=sw),
                             num_dashes=26, dashed_ratio=0.55)
    else:
        box = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=color, stroke_width=sw, fill_opacity=0)
    box.move_to([x, y, 0])
    return VGroup(box, t)


def a4_arrow(a, b, color=INK, w=5, tip=0.2):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.5)


def a4_x(x, y, s=0.17, color=INK, w=7):
    """A cross mark (two lines) centred on (x, y)."""
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a4_godot(x=5.3, y=0.1, h=1.7):
    ic = ImageMobject("pantry/icon_godot.png").set_height(h).move_to([x, y, 0])
    lb = T("Godot", 34).move_to([x, y - h / 2 - 0.2, 0])
    return ic, lb


# --- side-view silhouette of the post's base + pole, and its colliders (metres -> scene units) ---
A4_MESH = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.08, 0.1), (-0.3, 0.1)]
A4_CONCAVE = [(-0.37, -0.07), (0.37, -0.07), (0.37, 0.17), (0.15, 0.17), (0.15, 1.87), (-0.15, 1.87),
              (-0.15, 0.17), (-0.37, 0.17)]                          # the same outline, offset 7 cm so it can be seen
A4_HULL = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.3, 0.1)]    # the real convex hull of the silhouette


def a4_offset_convex(pts, d):
    """Offset a convex polygon (counter-clockwise or clockwise) outward by d: intersect the shifted neighbouring edges."""
    P = [np.array(p, dtype=float) for p in pts]
    n = len(P)
    area = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))
    sgn = 1.0 if area > 0 else -1.0                                   # +1 = counter-clockwise
    lines = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        e = (b - a) / np.linalg.norm(b - a)
        nrm = np.array([e[1], -e[0]]) * sgn                           # outward normal
        lines.append((a + nrm * d, e))
    out = []
    for i in range(n):
        (p1, e1), (p2, e2) = lines[i - 1], lines[i]
        m = np.array([[e1[0], -e2[0]], [e1[1], -e2[1]]])
        t = np.linalg.solve(m, p2 - p1)
        out.append(tuple(p1 + e1 * t[0]))
    return out


def a4_poly(pts, ox, oy, k=A4_K, fill=None, stroke=INK, sw=6, op=1.0):
    """A polygon from metre coordinates; (ox, oy) is where (0, 0) lands (the base's underside centre)."""
    P = [[ox + x * k, oy + y * k, 0] for x, y in pts]
    if fill is None:
        return Polygon(*P, stroke_color=stroke, stroke_width=sw, fill_opacity=0)
    return Polygon(*P, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=op)


# ═════════════════════════════ B33A · glTF is the recommended format, in two forms ═════════════════════════════
class B33A_Formats(Scene):
    def construct(self):
        # act title (Title Case serif), as Act I's first picture carries its own
        act = a4_put(T("What  Godot  Builds From a  File", 40), -6.0, 3.0)
        post = ImageMobject("pantry/a4_post.png").set_height(4.1).move_to([-5.3, -0.85, 0])
        gd, gdl = a4_godot(5.3, -0.5, 1.7)
        self.add(act, post, gd, gdl)
        until(self, "Godot lists", lead=0.1)
        title = T("glTF 2.0", 48).move_to([-1.6, 2.0, 0])
        self.play(FadeIn(title), run_time=0.4)
        until(self, "recommended", lead=0.2)
        dot = Dot([0.15, 2.0, 0], radius=0.13, color=TERRA)
        rec = T("recommended", 36).move_to([1.9, 2.0, 0])
        self.play(FadeIn(dot), FadeIn(rec), run_time=0.4)
        until(self, "text form", lead=0.25)
        c1 = a4_chip(".gltf", -0.2, 0.4, 42)
        t1 = T("text", 36).move_to([-0.2, 1.25, 0])
        a1 = a4_arrow([-4.15, -0.6, 0], [-1.7, 0.35, 0])
        a1b = a4_arrow([1.3, 0.35, 0], [4.15, -0.4, 0])
        self.play(FadeIn(c1), FadeIn(t1), Create(a1), Create(a1b), run_time=0.5)
        until(self, "binary form", lead=0.3)
        c2 = a4_chip(".glb", -0.2, -1.7, 42)
        t2 = T("binary", 36).move_to([-0.2, -0.85, 0])
        a2 = a4_arrow([-4.15, -1.2, 0], [-1.7, -1.65, 0])
        a2b = a4_arrow([1.3, -1.65, 0], [4.15, -0.9, 0])
        self.play(FadeIn(c2), FadeIn(t2), Create(a2), Create(a2b), run_time=0.5)
        done(self)


# ═════════════════════════════ B33B · .blend, only through Blender's own exporter ═════════════════════════════
class B33B_Blend(Scene):
    def construct(self):
        chip = a4_chip(".blend", -5.0, 0.1, 44)
        gd, gdl = a4_godot(5.3, 0.1, 1.7)
        self.add(chip, gd, gdl)
        until(self, "directly", lead=0.8)
        left = Line([-3.55, 0.1, 0], [-1.45, 0.1, 0], color=INK, stroke_width=5)           # a line with a gap in the middle
        right = a4_arrow([1.5, 0.1, 0], [4.2, 0.1, 0])
        self.play(Create(left), Create(right), run_time=0.5)
        until(self, "Blender's own exporter", lead=0.3)
        bl = ImageMobject("pantry/icon_blender.png").set_height(1.6).move_to([0.0, 0.1, 0])
        lab = T("its own exporter", 36).move_to([0.0, -1.15, 0])
        self.play(FadeIn(bl, shift=DOWN * 0.3), run_time=0.45)
        self.play(FadeIn(lab), run_time=0.3)
        until(self, "has to be installed", lead=0.3)
        ins = T("installed", 36).move_to([0.45, -1.9, 0])
        ck = check(-0.65, -1.9, 0.2, INK, 8)
        self.play(FadeIn(ins), Create(ck), run_time=0.4)
        done(self)


# ═════════════════════════════ B34 · FBX through ufbx; OBJ cannot carry four things ═════════════════════════════
class B34_FbxObj(Scene):
    def construct(self):
        fbx = a4_chip(".fbx", -5.1, 1.65, 42)
        gd, gdl = a4_godot(5.3, 0.55, 1.6)
        self.add(fbx, gd, gdl)
        until(self, "goes through", lead=0.2)
        l1 = a4_arrow([-3.9, 1.65, 0], [-2.0, 1.65, 0])
        self.play(Create(l1), run_time=0.35)
        uf = a4_chip("ufbx", -0.3, 1.65, 42)
        self.play(FadeIn(uf), run_time=0.35)
        l2 = a4_arrow([1.5, 1.65, 0], [4.2, 0.95, 0])
        self.play(Create(l2), run_time=0.35)
        until(self, "O B J", lead=0.3)
        obj = a4_chip(".obj", -5.1, -1.45, 42)
        self.play(FadeIn(obj), run_time=0.4)
        until(self, "skinning", lead=0.35)
        # (cross x, label left edge, y, text): a cross, then the missing thing
        items = [(-3.2, -2.75, -0.75, "skinning"), (0.6, 1.05, -0.75, "animation"),
                 (-3.2, -2.75, -2.15, "UV2"), (0.6, 1.05, -2.15, "PBR materials")]
        for i, (mx, lx, y, s) in enumerate(items):
            if i == 1:
                until(self, "animation,", lead=0.3)
            if i == 2:
                until(self, "a second U V set", lead=0.3)
            if i == 3:
                until(self, "physically based", lead=0.3)
            self.play(Create(a4_x(mx, y, 0.17)), FadeIn(a4_put(T(s, 36), lx, y)), run_time=0.3)
        done(self)


# ═════════════════════════════ B35 · GLB for a prop, the text form for diffs, the script is the source ═════════════════════════════
A4_DIFF_M = '"metallicFactor":0.800000011920929,'                 # recorded: git diff of the two .gltf exports (evidence/act4/out/forms.log)
A4_DIFF_P = '"metallicFactor":0.20000000298023224,'
A4_DIFF_B = 'Binary files a/old.glb and b/new.glb differ'


class B35_ScriptSource(Scene):
    def construct(self):
        # tableau 1: one file against loose files
        glb = a4_chip(".glb", -3.4, 0.9, 48, sw=5)
        one = T("one file", 40).move_to([-3.4, -0.45, 0])
        self.add(glb)
        until(self, "use G L B", lead=0.2)
        self.play(FadeIn(one), run_time=0.35)
        until(self, "no loose textures", lead=0.35)
        gl = a4_chip(".gltf", 0.7, 0.9, 36)
        bn = a4_chip(".bin", 3.0, 0.9, 36)
        png = a4_chip(".png", 5.1, 0.9, 36, color=DIM, dash=True)
        loose = T("loose files", 40).move_to([3.0, -0.45, 0])
        self.play(FadeIn(gl), FadeIn(bn), FadeIn(png), FadeIn(loose), run_time=0.5)
        # tableau 2: what version control shows
        until(self, "Use the text form", lead=0.05)
        self.play(FadeOut(VGroup(glb, one, gl, bn, png, loose)), run_time=0.3)
        h1 = a4_chip(".gltf", -4.9, 1.75, 36)
        m1 = M("-", 32).move_to([-3.45, 2.05, 0])
        d1 = a4_put(M(A4_DIFF_M, 32), -3.1, 2.05)
        m2 = M("+", 32).move_to([-3.45, 1.45, 0])
        d2 = a4_put(M(A4_DIFF_P, 32), -3.1, 1.45)
        h2 = a4_chip(".glb", -4.9, -0.45, 36)
        d3 = a4_put(M(A4_DIFF_B, 32), -6.0, -1.45)
        self.play(FadeIn(h1), FadeIn(m1), FadeIn(d1), FadeIn(m2), FadeIn(d2), run_time=0.4)
        self.play(FadeIn(h2), FadeIn(d3), run_time=0.4)
        # tableau 3: the script is the source of truth
        until(self, "Either way", lead=0.3)
        self.play(FadeOut(VGroup(h1, m1, d1, m2, d2, h2, d3)), run_time=0.3)
        sc = a4_chip("build_checkpoint_post.py", 0.0, 2.35, 32, sw=5)
        dot = Dot([-3.85, 2.35, 0], radius=0.14, color=TERRA)
        o1 = a4_chip(".glb", -3.2, -0.6, 44)
        o2 = a4_chip(".gltf", 3.2, -0.6, 44)
        ar1 = a4_arrow([-1.3, 1.75, 0], [-2.9, 0.1, 0])
        ar2 = a4_arrow([1.3, 1.75, 0], [2.9, 0.1, 0])
        truth = T("source of truth", 40).move_to([0.0, 0.9, 0])
        self.play(FadeIn(sc), FadeIn(dot), run_time=0.4)
        self.play(Create(ar1), Create(ar2), FadeIn(o1), FadeIn(o2), run_time=0.5)
        self.play(FadeIn(truth), run_time=0.3)
        done(self)


# ═════════════════════════════ B36 · materials cross; shader nodes and lights do not ═════════════════════════════
def a4_lamp(x, y, r=0.3):
    rays = VGroup(*[Line([x + 1.45 * r * np.cos(a), y + 1.45 * r * np.sin(a), 0], [x + 2.0 * r * np.cos(a), y + 2.0 * r * np.sin(a), 0],
                         color=INK, stroke_width=6) for a in [i * PI / 4 for i in range(8)]])
    return VGroup(Circle(radius=r, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([x, y, 0]), rays)


def a4_nodes(x, y):
    n1 = RoundedRectangle(width=0.8, height=0.55, corner_radius=0.1, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x - 0.7, y + 0.15, 0])
    n2 = RoundedRectangle(width=0.8, height=0.55, corner_radius=0.1, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x + 0.7, y - 0.15, 0])
    wire = Line([x - 0.3, y + 0.15, 0], [x + 0.3, y - 0.15, 0], color=INK, stroke_width=5)
    return VGroup(n1, wire, n2)


class B36_Materials(Scene):
    def construct(self):
        # tableau 1: one name, three places (recorded: the glTF export's JSON, Godot's import log)
        bl = ImageMobject("pantry/icon_blender.png").set_height(1.5).move_to([-4.3, 2.3, 0])
        nm = a4_put(M("PostMetal", 44), -3.0, 2.3)
        self.add(bl, nm)
        until(self, "metallic-roughness", lead=0.2)
        a1 = a4_arrow([-4.3, 1.45, 0], [-4.3, 1.0, 0])
        gt = T("glTF", 46).move_to([-4.3, 0.55, 0])
        j1 = a4_put(M('"name":"PostMetal",', 36), -3.0, 0.9)
        j2 = a4_put(M('"pbrMetallicRoughness":{', 36), -3.0, 0.2)
        self.play(Create(a1), FadeIn(gt), FadeIn(j1), FadeIn(j2), run_time=0.6)
        until(self, "arrives as a standard material", lead=0.3)
        a2 = a4_arrow([-4.3, 0.05, 0], [-4.3, -0.5, 0])
        gd = ImageMobject("pantry/icon_godot.png").set_height(1.5).move_to([-4.3, -1.5, 0])
        l1 = a4_put(M("StandardMaterial3D", 36), -3.0, -1.2)
        l2 = a4_put(M("resource_name=PostMetal", 36), -3.0, -1.9)
        self.play(Create(a2), FadeIn(gd), FadeIn(l1), FadeIn(l2), run_time=0.6)
        # tableau 2: what stays behind
        until(self, "Blender-only shader nodes", lead=0.45)
        self.play(FadeOut(Group(bl, nm, a1, gt, j1, j2, a2, gd, l1, l2)), run_time=0.3)
        bl2 = ImageMobject("pantry/icon_blender.png").set_height(1.6).move_to([-5.5, 0.5, 0])
        gd2 = ImageMobject("pantry/icon_godot.png").set_height(1.6).move_to([5.5, 0.5, 0])
        wall = Line([1.3, 2.3, 0], [1.3, -2.0, 0], color=INK, stroke_width=9)
        gl = T("glTF", 40).move_to([1.3, 2.75, 0])
        ndg = VGroup(a4_nodes(-3.0, 1.3), T("shader nodes", 36).move_to([-3.0, 0.5, 0]))
        lp = a4_lamp(-3.0, -0.9, 0.3)
        lpl = T("lights", 36).move_to([-3.0, -2.0, 0])
        self.play(FadeIn(bl2), FadeIn(gd2), Create(wall), FadeIn(gl), FadeIn(ndg), FadeIn(lp), FadeIn(lpl), run_time=0.4)
        until(self, "don't cross", lead=0.2)
        self.play(ndg.animate.shift(RIGHT * 2.4), run_time=0.55)
        self.play(ndg.animate.shift(LEFT * 1.0), run_time=0.3)
        until(self, "lights don't", lead=0.2)
        self.play(lp.animate.shift(RIGHT * 2.4), run_time=0.55)
        self.play(lp.animate.shift(LEFT * 1.0), run_time=0.3)
        until(self, "unless you ask", lead=0.2)
        sw = RoundedRectangle(width=1.2, height=0.6, corner_radius=0.3, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([-2.4, -2.75, 0])
        knob = Dot([-2.65, -2.75, 0], radius=0.2, color=DIM)
        swl = a4_put(T("Punctual Lights", 34), -1.5, -2.75)
        self.play(FadeIn(sw), FadeIn(knob), FadeIn(swl), run_time=0.3)
        on = Dot([-2.15, -2.75, 0], radius=0.2, color=TERRA)
        self.play(FadeOut(knob), FadeIn(on), lp.animate.shift(RIGHT * 4.8), run_time=0.6)
        om = M("OmniLight3D", 32).move_to([3.3, -2.0, 0])
        self.play(FadeIn(om), run_time=0.3)
        done(self)


# ═════════════════════════════ B37 / B38 · the import file ═════════════════════════════
A4_IMPORT = [(23, "nodes/import_as_skeleton_bones=false"), (24, "nodes/use_name_suffixes=false"),
             (25, "nodes/use_node_type_suffixes=false"), (26, "meshes/ensure_tangents=true"),
             (27, "meshes/generate_lods=true")]                       # enemy.glb.import, lines 23-27, verbatim
A4_Y = [1.55, 0.6, -0.35, -1.3, -2.25]                              # line y positions in the card


class B37_ImportFile(Scene):
    def construct(self):
        glb = a4_chip("enemy.glb", -4.35, 2.72, 32, sw=4)
        imp = a4_chip("enemy.glb.import", -0.2, 2.72, 32, sw=4)
        self.add(glb, imp)
        until(self, "with import settings", lead=0.25)
        card = RoundedRectangle(width=11.9, height=5.5, corner_radius=0.25, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-0.05, -0.68, 0])
        self.play(Create(card), run_time=0.4)
        until(self, "These lines decide", lead=0.2)
        rows = []
        for (n, s), y in zip(A4_IMPORT, A4_Y):
            num = M(str(n), 32, DIM).move_to([-4.55, y, 0])
            ln = a4_put(M(s, 32), -3.9, y)
            rows.append(VGroup(num, ln))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.18), run_time=1.0)
        until(self, "use name suffixes", lead=0.35)
        ring = RoundedRectangle(width=10.6, height=0.72, corner_radius=0.2, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0.2, A4_Y[1], 0])
        dot = Dot([-5.55, A4_Y[1], 0], radius=0.13, color=TERRA)
        self.play(Create(ring), FadeIn(dot), run_time=0.35)
        until(self, "use node type suffixes", lead=0.35)
        ring2 = RoundedRectangle(width=10.6, height=0.72, corner_radius=0.2, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0.2, A4_Y[2], 0])
        dot2 = Dot([-5.55, A4_Y[2], 0], radius=0.13, color=TERRA)
        self.play(Create(ring2), FadeIn(dot2), run_time=0.35)
        done(self)


def a4_pair(y, lines, x0=-3.0):
    """A two-line card of key=value lines (Menlo 32, the value bold). Returns (card, lines VGroup)."""
    card = RoundedRectangle(width=9.5, height=1.6, corner_radius=0.22, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x0 + 4.4, y, 0])
    g = VGroup()
    for i, (key, val) in enumerate(lines):
        yy = y + 0.38 - 0.76 * i
        k = M(key, 32).move_to([x0 + a4_mw(key) / 2, yy, 0])
        v = Text(val, font=MONO, color=INK, font_size=32, weight="BOLD").move_to([x0 + a4_mw(key) + a4_mw(val) / 2, yy, 0])
        g.add(VGroup(k, v))
    return card, g


class B38_Template(Scene):
    def construct(self):
        k1, k2 = "nodes/use_name_suffixes=", "nodes/use_node_type_suffixes="
        c1, g1 = a4_pair(1.95, [(k1, "false"), (k2, "false")])
        l1 = T("enemy and\nplayer files", 34).move_to([-5.0, 1.95, 0])
        self.add(c1, g1, l1)
        d1 = VGroup(Dot([4.55, 2.33, 0], radius=0.11, color=TERRA), Dot([5.75, 1.57, 0], radius=0.11, color=TERRA))
        until(self, "those two lines are false", lead=0.3)
        self.play(FadeIn(d1), run_time=0.3)
        until(self, "A fresh import", lead=0.2)
        c2, g2 = a4_pair(0.05, [(k1, "true"), (k2, "true")])
        l2 = T("fresh\nimport", 34).move_to([-5.0, 0.05, 0])
        self.play(Create(c2), FadeIn(g2), FadeIn(l2), run_time=0.5)
        until(self, "Copy the demo's import file", lead=0.2)
        l3 = T("your post", 34).move_to([-5.0, -1.85, 0])
        c3, g3 = a4_pair(-1.85, [(k1, "false"), (k2, "false")])
        cp = VGroup(c1.copy(), g1.copy())
        self.play(FadeIn(l3), run_time=0.25)
        self.play(cp.animate.shift(DOWN * 3.8), run_time=0.8)
        self.remove(cp)
        self.add(c3, g3)
        until(self, "collision hints", lead=0.5)
        d3 = VGroup(Dot([4.55, -1.47, 0], radius=0.11, color=TERRA), Dot([5.75, -2.23, 0], radius=0.11, color=TERRA))
        ig = T("naming hints ignored", 36).move_to([1.7, -3.05, 0])
        self.play(FadeIn(d3), FadeIn(ig), run_time=0.4)
        done(self)


# ═════════════════════════════ B39 / B40 · what each suffix builds from one mesh ═════════════════════════════
# The silhouette is the post's base + pole in side view (metres). Recorded in Godot 4.7.2 (evidence/act4/out/suffix-probe.log, fresh import):
#   -col -> MeshInstance3D kept + StaticBody3D/CollisionShape3D ConcavePolygonShape3D;  -convcol -> same, ConvexPolygonShape3D
#   -colonly -> StaticBody3D, ConcavePolygonShape3D (mesh gone);  -convcolonly -> StaticBody3D, ConvexPolygonShape3D;  -noimp -> node gone
def a4_post_mesh(ox, oy, k, faded=False):
    return a4_poly(A4_MESH, ox, oy, k, fill=BAR2, stroke=DIM, sw=4)


class B39_Keeps(Scene):
    def construct(self):
        k, oy = 2.0, -2.75
        ax, bx = -4.7, 1.2
        mA, mB = a4_post_mesh(ax, oy, k), a4_post_mesh(bx, oy, k)
        tA = M("Mesh1-col", 34).move_to([ax, 1.95, 0])
        tB = M("Mesh2-convcol", 34).move_to([bx, 1.95, 0])
        self.add(mA, mB, tA, tB)
        until(self, "keeps its mesh", lead=0.3)
        kept = a4_put(T("mesh kept", 36), -3.3, 0.4)
        self.play(FadeIn(kept), run_time=0.3)
        until(self, "gains a static collision body", lead=0.25)
        oA = a4_poly(A4_CONCAVE, ax, oy, k, stroke=INK, sw=8)
        self.play(Create(oA), run_time=0.7)
        sb = a4_put(T("static body", 36), -3.3, -0.15)
        self.play(FadeIn(sb), run_time=0.25)
        until(self, "same geometry", lead=0.3)
        cv = a4_put(T("concave", 36), -3.3, -0.7)
        self.play(FadeIn(cv), run_time=0.25)
        until(self, "Dash conv col", lead=0.3)
        oB = a4_poly(a4_offset_convex(A4_HULL, 0.07), bx, oy, k, stroke=INK, sw=8)
        self.play(Create(oB), run_time=0.7)
        until(self, "convex shape", lead=0.35)
        kept2 = a4_put(T("mesh kept", 36), 2.7, 0.4)
        sb2 = a4_put(T("static body", 36), 2.7, -0.15)
        cx = a4_put(T("convex", 36), 2.7, -0.7)
        self.play(FadeIn(kept2), FadeIn(sb2), FadeIn(cx), run_time=0.35)
        done(self)


class B40_Removes(Scene):
    def construct(self):
        k, oy = 1.45, -1.55
        xs = [-4.4, 0.1, 4.3]
        m = [a4_post_mesh(x, oy, k) for x in xs]
        tg = [M("Mesh3-colonly", 32).move_to([-4.3, 2.55, 0]), M("Mesh4-convcolonly", 32).move_to([0.15, 2.55, 0]),
              M("Mesh5-noimp", 32).move_to([4.3, 2.55, 0])]
        self.add(*m, *tg)
        until(self, "Dash col only removes", lead=0.2)
        o1 = a4_poly(A4_CONCAVE, xs[0], oy, k, stroke=INK, sw=8)
        self.play(Create(o1), FadeOut(m[0]), run_time=0.7)
        l1 = T("mesh removed", 34).move_to([xs[0], -2.35, 0])
        l1b = T("concave body", 34).move_to([xs[0], -2.9, 0])
        self.play(FadeIn(l1), FadeIn(l1b), run_time=0.3)
        until(self, "Dash conv col only removes", lead=0.2)
        o2 = a4_poly(a4_offset_convex(A4_HULL, 0.07), xs[1], oy, k, stroke=INK, sw=8)
        self.play(Create(o2), FadeOut(m[1]), run_time=0.7)
        l2 = T("mesh removed", 34).move_to([xs[1], -2.35, 0])
        l2b = T("convex body", 34).move_to([xs[1], -2.9, 0])
        self.play(FadeIn(l2), FadeIn(l2b), run_time=0.3)
        until(self, "dash no imp", lead=0.2)
        self.play(FadeOut(m[2]), run_time=0.4)
        xm = a4_x(xs[2], oy + 1.0, 0.45, w=9)
        l3 = T("node removed", 34).move_to([xs[2], -2.35, 0])
        self.play(Create(xm), FadeIn(l3), run_time=0.4)
        done(self)


# ═════════════════════════════ B41 · a collider has to be a mesh in glTF; the usual pattern ═════════════════════════════
def a4_wire_cube(x, y, s=0.5):
    """A Blender empty drawn as a cube: twelve edges in isometric, centred on (x, y)."""
    iso = Iso(x, y - s, 1.0)
    c = [(0, 0, 0), (s, 0, 0), (s, s, 0), (0, s, 0), (0, 0, s), (s, 0, s), (s, s, s), (0, s, s)]
    E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    return VGroup(*[Line(iso.p(*c[a]), iso.p(*c[b]), color=INK, stroke_width=5) for a, b in E])


class B41_Empties(Scene):
    def construct(self):
        # tableau 1: three rows. Recorded in Godot 4.7.2 for glTF (a mesh and an empty, both named ...-colonly); the Collada row is Godot's documentation.
        r1, r2, r3 = 2.0, 0.1, -1.8
        tg1 = T("glTF", 40).move_to([-5.2, r1, 0])
        it1 = a4_poly(A4_MESH, -3.35, r1 - 0.58, 0.65, fill=BAR2, stroke=DIM, sw=4)
        ar1 = a4_arrow([-2.4, r1, 0], [-0.9, r1, 0])
        res1 = a4_put(M("StaticBody3D", 36), -0.55, r1)
        self.add(tg1)
        until(self, "a collider has to be a mesh", lead=0.3)
        self.play(FadeIn(it1), Create(ar1), FadeIn(res1), Create(check(4.3, r1, 0.22, INK, 8)), run_time=0.6)
        until(self, "A Blender empty", lead=0.2)
        tg2 = T("glTF", 40).move_to([-5.2, r2, 0])
        it2 = a4_wire_cube(-3.35, r2, 0.5)
        ar2 = a4_arrow([-2.4, r2, 0], [-0.9, r2, 0])
        res2 = a4_put(M("Node3D", 36), -0.55, r2)
        self.play(FadeIn(tg2), FadeIn(it2), Create(ar2), FadeIn(res2), Create(a4_x(4.3, r2, 0.2)), run_time=0.6)
        until(self, "only with Collada", lead=0.3)
        tg3 = T("Collada", 40).move_to([-4.9, r3, 0])
        it3 = a4_wire_cube(-3.35, r3, 0.5)
        ar3 = a4_arrow([-2.4, r3, 0], [-0.9, r3, 0])
        res3 = a4_put(M("BoxShape3D", 36), -0.55, r3)
        doc = a4_put(T("documented, not run", 32, DIM), -0.55, -2.6)
        self.play(FadeIn(tg3), FadeIn(it3), Create(ar3), FadeIn(res3), Create(check(4.3, r3, 0.22, INK, 8)), FadeIn(doc), run_time=0.6)
        # tableau 2: the pattern, on the real Blender renders of the post and its collision hull (after the midpoint: tableau 1 is on screen at 50%)
        until(self, "the usual pattern", lead=0.1)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)
        post = ImageMobject("pantry/a4_post.png").set_height(4.7).move_to([-2.6, -0.5, 0])
        hull = ImageMobject("pantry/a4_post_hull.png").set_height(4.7).move_to([2.9, -0.5, 0])
        tag = a4_chip("Collision-convcolonly", 2.9, 2.75, 32, sw=4)
        self.play(FadeIn(post), run_time=0.3)
        until(self, "a separate, simple mesh", lead=0.0)
        self.play(FadeIn(hull), FadeIn(tag), run_time=0.45)
        until(self, "invisible", lead=0.3)
        self.play(hull.animate.set_opacity(0.35).move_to([-2.6, -0.5, 0]), tag.animate.move_to([-2.6, 2.75, 0]), run_time=0.7)
        lab = [a4_put(T("invisible", 40), 1.6, 1.2), a4_put(T("convex", 40), 1.6, 0.3),
               a4_put(T("cheap", 40), 1.6, -0.6), a4_put(T("shaped by you", 40), 1.6, -1.5)]
        self.play(FadeIn(lab[0]), run_time=0.25)
        until(self, "convex,", lead=0.25)
        self.play(FadeIn(lab[1]), run_time=0.25)
        until(self, "cheap", lead=0.25)
        self.play(FadeIn(lab[2]), run_time=0.25)
        until(self, "shaped by you", lead=0.25)
        self.play(FadeIn(lab[3]), run_time=0.25)
        done(self)


# ═════════════════════════════ B43 / B44 · the demo's enemy: names against shapes ═════════════════════════════
# enemy.tscn: the five CollisionShape3D nodes sit at lines 472, 476, 480, 484, 488; their shapes are sub-resources at lines 416-423:
#   SubResource("11") SphereShape3D radius 0.68 | ("12") SphereShape3D radius 0.4 | ("13") BoxShape3D size (1.14506, 0.776818, 1.12102)
A4_ENEMY = [("Sphere1", "SphereShape3D"), ("Sphere2", "SphereShape3D"), ("Sphere3", "SphereShape3D"),
            ("Sphere4", "BoxShape3D"), ("Box", "SphereShape3D")]
A4_EY = [1.75, 0.75, -0.25, -1.25, -2.25]


def a4_glyph(kind, x, y, s=0.7):
    if kind == "SphereShape3D":
        return Circle(radius=s / 2, stroke_color=INK, stroke_width=6, fill_color=BAR3, fill_opacity=1).move_to([x, y, 0])
    return Square(side_length=s, stroke_color=INK, stroke_width=6, fill_color=BAR3, fill_opacity=1).move_to([x, y, 0])


class B43_Enemy(Scene):
    def construct(self):
        hdr = a4_put(M("enemy.tscn", 32), -5.9, 2.85)
        self.add(hdr)
        until(self, "wrapper scene", lead=0.2)
        rows = []
        for (name, shape), y in zip(A4_ENEMY, A4_EY):
            chip = a4_put(a4_chip(name, 0.0, y, 34, sw=4, hgt=0.72), -5.9, y)
            ar = a4_arrow([-5.9 + chip.width + 0.2, y, 0], [-2.5, y, 0])
            gl = a4_glyph(shape, -1.8, y)
            tx = a4_put(M(shape, 34), -1.1, y)
            rows.append(VGroup(chip, ar, gl, tx))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=1.1)
        until(self, "five collision shapes", lead=0.2)
        five = T("5", 110).move_to([5.1, -0.2, 0])
        cite = a4_put(M("lines 472-490", 32, DIM), -5.9, -3.1)
        self.play(FadeIn(five), FadeIn(cite), run_time=0.35)
        until(self, "named Box", lead=0.1)
        d5 = Dot([3.4, A4_EY[4], 0], radius=0.14, color=TERRA)
        self.play(FadeIn(d5), run_time=0.3)
        until(self, "Sphere four", lead=0.1)
        d4 = Dot([3.4, A4_EY[3], 0], radius=0.14, color=TERRA)
        self.play(FadeIn(d4), run_time=0.3)
        done(self)


class B44_Names(Scene):
    def construct(self):
        cx = [-3.1, 3.1]
        kinds = ["SphereShape3D", "BoxShape3D"]
        tags = [a4_chip("Box", cx[0], 2.2, 38), a4_chip("Sphere4", cx[1], 2.2, 38)]
        gl = [a4_glyph("SphereShape3D", cx[0], 0.2, 1.7), a4_glyph("BoxShape3D", cx[1], 0.2, 1.7)]
        self.add(*tags, *gl)
        until(self, "The shape is the fact", lead=0.1)
        cls = [M(kinds[0], 34).move_to([cx[0] + 0.3, -1.35, 0]), M(kinds[1], 34).move_to([cx[1] + 0.3, -1.35, 0])]
        cks = [check(cx[0] - 1.95, -1.35, 0.2, INK, 8), check(cx[1] - 1.55, -1.35, 0.2, INK, 8)]
        self.play(FadeIn(cls[0]), FadeIn(cls[1]), Create(cks[0]), Create(cks[1]), run_time=0.45)
        until(self, "finds collision by name", lead=0.15)
        cur = cursor(5.0, 1.0, 0.5)
        self.add(cur)
        self.play(cur.animate.move_to([cx[0] + 1.0, 1.55, 0]), run_time=0.5)
        until(self, "trusting a label", lead=0.1)
        tl = a4_put(T("a label", 40), -1.6, 2.2)
        self.play(FadeIn(tl), run_time=0.3)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Building the Post, Then Checking the Builder — part 1 (B45–B58)

One cast for the act: the CHECKPOINT POST, as the REAL Blender render (pantry/a5_post.png, Blender 5.1.2 Workbench, same camera as
the act-6 builder's pantry/post_visual.png, re-rendered at 2x from the first agent's own run-1 script), with every mark placed on
the real pixels through the camera projection of the real script's 3D points (evidence/act5/post_anchors.json, inlined below
because Gate A copies only scenes.py). The run-1 collision BOX (0.6 x 0.6 x 1.8 m) is pantry/a5_box.png, same crop.
B48, B49, B50, B51 and B54 (the Claude Code session) are Remotion `CCSession` beats: see lanes/act5.json and SESSION-act5.md.
B45–B47B, B52, B53, B55 and B56–B58 are Manim and live here (B52/B53/B55 are drawn from the session's result and system events, which a
`-p` run never printed on a screen). B58_X0 / B58_YF / B58_S fix the post's place on the floor if a later beat wants to continue it.
"""

# ── the real post: crop-pixel anchors from evidence/act5/post_anchors.json (crop 1457 x 1943 px, origin top-left) ─────────────────
A5_PT = {
    "z0_c": (735.5, 1723.2), "pole_top_c": (731.0, 104.3), "pole_bot_c": (735.3, 1637.7), "w_a": (195.7, 1792.1),
    "w_b": (611.1, 1915.8), "h_a": (37.4, 1744.9), "h_b": (-5.9, 106.7), "t_edge": (356.1, 1692.0),
    "pen_tl": (788.8, 105.9), "pen_tr": (1092.9, 114.4), "pen_br": (1090.7, 362.0), "pen_bl": (789.0, 343.2),
    "pen_len_a": (715.0, 108.9), "pen_len_b": (1020.8, 117.7), "pen_h_a": (1148.9, 115.9),
    "pen_h_b": (1146.2, 365.5), "floor_a": (-480.9, 1761.0), "floor_b": (860.9, 2201.3), "floor_c": (1903.2, 1687.0),
    "floor_d": (653.4, 1410.4), "lift16": (735.1, 1586.2), "lift158": (735.1, 1587.8), "ray_start158": (730.0, -239.2), "ray_top": (730.4, -86.6), "ray_bot": (735.5, 1723.2),
    "base_mm_0": (356.8, 1735.0), "base_mp_0": (706.1, 1611.2), "base_pm_0": (769.0, 1851.1),
    "base_pp_0": (1109.4, 1711.6), "base_mm_1": (355.4, 1649.0), "base_mp_1": (705.8, 1530.7),
    "base_pm_1": (768.9, 1759.9), "base_pp_1": (1110.2, 1626.6), "box_mm_0": (356.8, 1735.0),
    "box_mm_18": (331.3, 105.6), "box_mp_0": (706.1, 1611.2), "box_mp_18": (700.4, 91.9),
    "box_pm_0": (769.0, 1851.1), "box_pm_18": (766.2, 118.6), "box_pp_0": (1109.4, 1711.6),
    "box_pp_18": (1125.2, 103.0), "pole_top_0": (788.8, 105.9), "pole_top_1": (805.7, 104.0),
    "pole_top_2": (779.1, 102.4), "pole_top_3": (724.9, 101.8), "pole_top_4": (674.2, 102.7),
    "pole_top_5": (656.0, 104.5), "pole_top_6": (681.9, 106.2), "pole_top_7": (737.2, 106.8),
}
A5_CROP_W, A5_CROP_H = 1457, 1943
A5_S = 0.0030                                   # scene units per crop pixel (the 1.8 m pole is ~4.4 units tall)
A5_ORG = (735.5, 1723.2)                        # crop pixel of the pole's foot (world 0, 0, 0)


def a5_P(key, x0, yf, s=A5_S):
    """Scene point of a real anchor when the pole's foot sits at scene (x0, yf)."""
    px, py = A5_PT[key]
    return np.array([x0 + (px - A5_ORG[0]) * s, yf + (A5_ORG[1] - py) * s, 0.0])


def a5_img(path, x0, yf, s=A5_S, opacity=1.0):
    """The real render, placed so the pole's foot lands on (x0, yf)."""
    im = ImageMobject(path)
    im.set_height(A5_CROP_H * s)
    im.move_to([x0 + (A5_CROP_W / 2 - A5_ORG[0]) * s, yf + (A5_ORG[1] - A5_CROP_H / 2) * s, 0])
    if opacity < 1.0:
        im.set_opacity(opacity)
    return im


def a5_floor(x0, yf, k=0.72, s=A5_S):
    """A ghost floor tile under the post (the real floor quad's corners, pulled in so it stays on stage)."""
    org = a5_P("z0_c", x0, yf, s)
    pts = []
    for key in ("floor_a", "floor_b", "floor_c", "floor_d"):
        p = a5_P(key, x0, yf, s)
        pts.append(org + (p - org) * k)
    return Polygon(*pts, fill_color=GHOST, fill_opacity=1, stroke_width=0)


def a5_lbl(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


# ── B45 · the job, drawn on the real render ──────────────────────────────────────────────────────────────────────────────────
A5_X0, A5_YF = -0.3, -2.25


def a5_b45_marks(x0, yf):
    """Every B45 mark, built in one place so B46 can start from exactly B45's last frame."""
    s = A5_S
    # base: 0.6 m x 0.6 m, one arrow along each front edge (offset outward from the edge, in screen space)
    a0, a1 = a5_P("base_mm_0", x0, yf), a5_P("base_pm_0", x0, yf)
    b0, b1 = a5_P("base_pm_0", x0, yf), a5_P("base_pp_0", x0, yf)
    wl = dim_arrow(a0 + np.array([-0.08, -0.3, 0]), a1 + np.array([-0.08, -0.3, 0]))
    wr = dim_arrow(b0 + np.array([0.12, -0.28, 0]), b1 + np.array([0.12, -0.28, 0]))
    wl_l = a5_lbl("0.6 m", a0[0] - 0.95, a0[1] - 0.62)
    wr_l = a5_lbl("0.6 m", b1[0] + 1.0, b1[1] - 0.55)
    # thickness: a leader from the base's left corner edge to its label, terracotta dot on the edge
    te = a5_P("t_edge", x0, yf)
    th_dot = Dot(te + np.array([0.0, 0.0, 0]), radius=0.1, color=TERRA)
    th_ld = Line(te + np.array([-0.12, 0.0, 0]), [te[0] - 1.35, te[1] + 0.35, 0], color=INK, stroke_width=4)
    th_l = a5_lbl("0.1 m", te[0] - 2.05, te[1] + 0.4)
    # eight-sided pole: a top-down octagon (vertex on +X, as the script builds it), leader to a dot on the pole
    oct_c = np.array([x0 - 3.05, yf + 2.35, 0])
    octo = RegularPolygon(n=8, radius=0.5, start_angle=0, color=INK, stroke_width=6).move_to(oct_c)
    oct_l = a5_lbl("8 sides", oct_c[0], oct_c[1] - 0.95)
    pole_pt = np.array([x0 - 0.12, yf + 2.35, 0])
    o_ld = Line([oct_c[0] + 0.62, oct_c[1], 0], [pole_pt[0] - 0.12, pole_pt[1], 0], color=INK, stroke_width=4)
    o_dot = Dot(pole_pt, radius=0.1, color=TERRA)
    # height: 1.8 m, to the right of the pennant, on the world line (0.55, 0, 0..1.8)
    ha = a5_P("pen_h_a", x0, yf)
    hb = np.array([ha[0] + 0.0, yf + 0.0, 0.0])
    h_arrow = dim_arrow(hb + np.array([0.72, -0.05, 0]), ha + np.array([0.72, 0.0, 0]))
    h_l = a5_lbl("1.8 m", ha[0] + 1.95, yf + 2.3)
    return dict(wl=wl, wr=wr, wl_l=wl_l, wr_l=wr_l, th_dot=th_dot, th_ld=th_ld, th_l=th_l, octo=octo, oct_l=oct_l, o_ld=o_ld,
                o_dot=o_dot, h_arrow=h_arrow, h_l=h_l)


class B45_TheJob(Scene):
    def construct(self):
        x0, yf = A5_X0, A5_YF
        title = T("Building the Post, Then Checking the Builder", 40).move_to([-0.2, 3.1, 0])
        floor = a5_floor(x0, yf)
        post = a5_img("pantry/a5_post.png", x0, yf)
        self.add(floor, title)
        m = a5_b45_marks(x0, yf)
        until(self, "a low-poly", lead=0.2)
        self.play(FadeIn(post), run_time=0.7)
        until(self, "point six", lead=0.35)
        self.play(Create(m["wl"]), Create(m["wr"]), FadeIn(m["wl_l"]), FadeIn(m["wr_l"]), run_time=0.6)
        until(self, "a tenth", lead=0.65)
        self.play(FadeIn(m["th_dot"]), Create(m["th_ld"]), FadeIn(m["th_l"]), run_time=0.5)
        until(self, "eight-sided", lead=0.4)
        self.play(Create(m["octo"]), FadeIn(m["oct_l"]), run_time=0.5)
        self.play(Create(m["o_ld"]), FadeIn(m["o_dot"]), run_time=0.4)
        until(self, "one point eight", lead=0.3)
        self.play(Create(m["h_arrow"]), FadeIn(m["h_l"]), run_time=0.6)
        done(self)


# ── B46 · pennant, two materials, a separate collision box ───────────────────────────────────────────────────────────────────
class B46_PennantMaterialsCollider(Scene):
    def construct(self):
        x0, yf = A5_X0, A5_YF
        title = T("Building the Post, Then Checking the Builder", 40).move_to([-0.2, 3.1, 0])
        floor = a5_floor(x0, yf)
        post = a5_img("pantry/a5_post.png", x0, yf)
        m = a5_b45_marks(x0, yf)
        old = VGroup(*[m[k] for k in m], title)
        self.add(floor, post, old)
        # the base and pole marks go; the pennant's arrive
        bl, br = a5_P("pen_bl", x0, yf), a5_P("pen_br", x0, yf)
        tr, brr = a5_P("pen_h_a", x0, yf), a5_P("pen_h_b", x0, yf)
        pen_len = dim_arrow(bl + np.array([0.0, -0.4, 0]), br + np.array([0.0, -0.4, 0]))
        pen_len_l = a5_lbl("0.4 m", (bl[0] + br[0]) / 2 + 0.55, bl[1] - 0.95)
        pen_h = dim_arrow(brr + np.array([0.5, 0.0, 0]), tr + np.array([0.5, 0.0, 0]))
        pen_h_l = a5_lbl("0.25 m", tr[0] + 1.6, (tr[1] + brr[1]) / 2)
        att = Dot(a5_P("pen_tl", x0, yf) + np.array([0.0, -0.03, 0]), radius=0.1, color=TERRA)
        self.play(FadeOut(old), run_time=0.4)
        until(self, "point four", lead=0.2)
        self.play(Create(pen_len), FadeIn(pen_len_l), run_time=0.5)
        until(self, "a quarter", lead=0.25)
        self.play(Create(pen_h), FadeIn(pen_h_l), run_time=0.5)
        until(self, "hangs from the top", lead=0.25)
        self.play(FadeIn(att), run_time=0.3)
        # the materials: a leader and a swatch per name (after the midpoint: the dims leave as the tags land)
        pole_pt = np.array([x0 - 0.1, yf + 1.5, 0])
        pm_dot = Dot(pole_pt, radius=0.1, color=TERRA)
        pm_ld = Line([pole_pt[0] - 0.12, pole_pt[1], 0], [x0 - 2.2, pole_pt[1], 0], color=INK, stroke_width=4)
        pm_sw = Circle(radius=0.22, fill_color="#7C8088", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x0 - 2.5, pole_pt[1], 0])
        pm_l = a5_lbl("PostMetal", x0 - 4.3, pole_pt[1])
        pen_c = np.array([(bl[0] + br[0]) / 2, (bl[1] + a5_P("pen_tl", x0, yf)[1]) / 2, 0])
        fc_dot = Dot(pen_c, radius=0.1, color=TERRA)
        fc_ld = Line([pen_c[0] + 0.12, pen_c[1], 0], [pen_c[0] + 0.55, pen_c[1], 0], color=INK, stroke_width=4)
        fc_sw = Circle(radius=0.22, fill_color="#9B6150", fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([pen_c[0] + 0.8, pen_c[1], 0])
        fc_l = a5_lbl("FlagCloth", pen_c[0] + 2.15, pen_c[1])
        until(self, "PostMetal", lead=0.3)
        self.play(FadeOut(VGroup(pen_len, pen_len_l, pen_h, pen_h_l, att)), FadeIn(pm_dot), Create(pm_ld), FadeIn(pm_sw), FadeIn(pm_l), run_time=0.5)
        until(self, "FlagCloth", lead=0.3)
        self.play(FadeIn(fc_dot), Create(fc_ld), FadeIn(fc_sw), FadeIn(fc_l), run_time=0.5)
        # the collider: a separate box, same crop and scale, off to the side
        bx = 5.0
        box = a5_img("pantry/a5_box.png", bx, yf, opacity=0.55)
        edges = VGroup(*[Line(a5_P(a, bx, yf), a5_P(b, bx, yf), color=DIM, stroke_width=4) for a, b in [
            ("box_mm_0", "box_pm_0"), ("box_pm_0", "box_pp_0"), ("box_mm_18", "box_pm_18"), ("box_pm_18", "box_pp_18"),
            ("box_mm_0", "box_mm_18"), ("box_pm_0", "box_pm_18"), ("box_pp_0", "box_pp_18")]])
        bx_l = a5_lbl("collider", bx, yf + 5.2)
        bx_l2 = a5_lbl("base + pole", bx, yf - 0.83, 34)
        until(self, "separate collision", lead=0.3)
        self.play(FadeIn(box), Create(edges), FadeIn(bx_l), run_time=0.7)
        until(self, "around the base", lead=0.25)
        self.play(FadeIn(bx_l2), run_time=0.4)
        done(self)


# ── B47A / B47B · four predictions on one board ──────────────────────────────────────────────────────────────────────────────
A5_CELLS = [(-3.15, 1.15), (3.15, 1.15), (-3.15, -1.8), (3.15, -1.8)]
A5_CW, A5_CH = 5.8, 2.6


def a5_cell(i):
    """One prediction cell: (frame, [cue parts in draw order]). Every part is drawn small and outline-only."""
    cx, cy = A5_CELLS[i]
    frame = RoundedRectangle(width=A5_CW, height=A5_CH, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([cx, cy, 0])
    parts = []
    if i == 0:                                      # which Godot axis carries the 1.8?
        thumb = a5_img("pantry/a5_post.png", cx - 1.9, cy - 0.78, s=0.0009)
        l18 = T("1.8 m", 34).move_to([cx - 0.95, cy - 0.05, 0])
        o = np.array([cx + 1.0, cy - 0.2, 0])
        ax = Arrow(o, o + np.array([0.85, -0.4, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.16)
        ay = Arrow(o, o + np.array([0.0, 0.9, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.16)
        az = Arrow(o, o + np.array([-0.85, -0.4, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.16)
        lx = T("X", 34).move_to(o + np.array([1.15, -0.62, 0])); ly = T("Y", 34).move_to(o + np.array([0.0, 1.2, 0]))
        lz = T("Z", 34).move_to(o + np.array([-1.15, -0.62, 0]))
        q = T("?", 64).move_to([cx + 2.4, cy + 0.3, 0])
        parts = [Group(thumb, l18), VGroup(ax, ay, az, lx, ly, lz), q]
    elif i == 1:                                    # the bounding box with +Y up off
        chips = VGroup()
        for k, ax_ in enumerate("XYZ"):
            x = cx - 1.55 + k * 1.55
            ch = RoundedRectangle(width=1.15, height=1.25, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([x, cy + 0.2, 0])
            chips.add(VGroup(ch, T(ax_, 34, DIM).move_to([x, cy + 0.48, 0]), T("?", 54).move_to([x, cy + 0.0, 0])))
        lab = T("Y up off", 36).move_to([cx, cy - 0.85, 0])
        parts = [chips, lab]
    elif i == 2:                                    # a scale that was never applied
        tag = RoundedRectangle(width=3.3, height=1.15, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([cx - 0.2, cy + 0.12, 0])
        hole = Circle(radius=0.11, color=INK, stroke_width=4).move_to([cx + 1.25, cy + 0.12, 0])
        string = Line([cx + 1.33, cy + 0.2, 0], [cx + 2.15, cy + 0.9, 0], color=INK, stroke_width=4)
        t1 = T("scale", 34).move_to([cx - 0.35, cy + 0.37, 0]); t2 = T("? ? ?", 44).move_to([cx - 0.35, cy - 0.05, 0])
        lab = T("never applied", 34).move_to([cx - 0.2, cy - 0.85, 0])
        parts = [VGroup(tag, hole, string), VGroup(t1, t2), lab]
    else:                                           # a collider named -convcolonly, demo's import file copied
        pg = Rectangle(width=0.8, height=1.05, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([cx - 2.0, cy + 0.2, 0])
        ln = VGroup(*[Line([cx - 2.22, cy + 0.2 + dy, 0], [cx - 1.78, cy + 0.2 + dy, 0], color=DIM, stroke_width=4) for dy in (0.25, 0.05, -0.15)])
        pl = T("import", 32).move_to([cx - 2.0, cy - 0.82, 0])
        arr = Arrow([cx - 1.35, cy + 0.2, 0], [cx - 0.1, cy + 0.2, 0], buff=0, color=INK, stroke_width=5, tip_length=0.16)
        thumb = a5_img("pantry/a5_box.png", cx + 0.9, cy - 0.45, s=0.0007, opacity=0.6)
        nm = M("-convcolonly", 32).move_to([cx + 1.2, cy - 0.95, 0])
        q = T("?", 64).move_to([cx + 2.3, cy + 0.3, 0])
        parts = [VGroup(pg, ln, pl), arr, Group(thumb, nm), q]
    return frame, parts


class B47A_ThreePredictions(Scene):
    def construct(self):
        head = T("Predict", 40).move_to([-5.2, 3.0, 0])
        self.add(head)
        f1, p1 = a5_cell(0); f2, p2 = a5_cell(1); f3, p3 = a5_cell(2)
        until(self, "Which Godot axis", lead=0.3)
        self.play(Create(f1), run_time=0.4)
        self.play(FadeIn(p1[0]), run_time=0.4)
        self.play(Create(p1[1]), run_time=0.6)
        self.play(FadeIn(p1[2]), run_time=0.3)
        until(self, "What does the bounding", lead=0.45)
        self.play(Create(f2), run_time=0.4)
        self.play(FadeIn(p2[0]), run_time=0.4)
        until(self, "plus Y up off", lead=0.2)
        self.play(FadeIn(p2[1]), run_time=0.3)
        until(self, "What does Godot report", lead=0.3)
        self.play(Create(f3), run_time=0.4)
        self.play(Create(p3[0]), run_time=0.5)
        self.play(FadeIn(p3[1]), run_time=0.3)
        until(self, "never applied", lead=0.25)
        self.play(FadeIn(p3[2]), run_time=0.3)
        done(self)


class B47B_FourthPrediction(Scene):
    def construct(self):
        head = T("Predict", 40).move_to([-5.2, 3.0, 0])
        cells = [a5_cell(i) for i in range(4)]
        self.add(head)
        for f, p in cells[:3]:
            self.add(f, *p)
        f4, p4 = cells[3]
        until(self, "collider named", lead=0.5)
        self.play(Create(f4), run_time=0.4)
        self.play(FadeIn(p4[0]), run_time=0.4)
        until(self, "dash conv col only", lead=0.2)
        self.play(FadeIn(p4[2]), run_time=0.4)
        until(self, "import file", lead=0.6)
        self.play(Create(p4[1]), FadeIn(p4[3]), run_time=0.4)
        done(self)


# ── B56 · our own run: the finished test, then a fresh import ────────────────────────────────────────────────────────────────
A5_MW = 0.2485          # Menlo at size 32: scene units per character (measured)


def a5_mline(text, x_left, y, size=32, color=INK):
    """A Menlo line whose LEFT edge sits at x_left (width = chars * 0.2485 at size 32, measured)."""
    w = len(text) * A5_MW * size / 32.0
    return M(text, size, color).move_to([x_left + w / 2.0, y, 0])


class B56_OurOwnRun(Scene):
    def construct(self):
        # part 1: the finished test's real log, one tick per PASS line (15 PASS, 0 FAIL: logs/verify1-test_checkpoint_post.log)
        tiles, ticks = VGroup(), VGroup()
        for r in range(3):
            for c in range(5):
                x, y = -2.4 + c * 1.2, 1.35 - r * 1.2
                tiles.add(RoundedRectangle(width=0.95, height=0.95, corner_radius=0.14, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([x, y, 0]))
                ticks.add(check(x - 0.03, y + 0.04, s=0.2, color=INK, w=8))
        pass_l = T("PASS", 40).move_to([0, 2.75, 0])
        fail_l = M("Failures: 0", 32).move_to([0, -2.55, 0])
        self.add(tiles)
        until(self, "Fifteen of fifteen", lead=0.35)
        self.play(FadeIn(pass_l), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.12), run_time=1.9)
        self.play(FadeIn(fail_l), run_time=0.3)
        until(self, "Then we checked", lead=0.1)
        self.play(FadeOut(VGroup(tiles, ticks, pass_l, fail_l)), run_time=0.4)
        # part 2: a fresh import of the same file
        x0, yf, s = -4.3, -2.6, 0.003
        box = a5_img("pantry/a5_box.png", x0, yf, s=s, opacity=0.6)
        edges = VGroup(*[Line(a5_P(a, x0, yf, s), a5_P(b, x0, yf, s), color=DIM, stroke_width=4) for a, b in [
            ("box_mm_0", "box_pm_0"), ("box_pm_0", "box_pp_0"), ("box_mm_18", "box_pm_18"), ("box_pm_18", "box_pp_18"),
            ("box_mm_0", "box_mm_18"), ("box_pm_0", "box_pm_18"), ("box_pp_0", "box_pp_18")]])
        fresh = T("fresh import", 40).move_to([x0, 2.75, 0])
        until(self, "A fresh import", lead=0.5)
        self.play(FadeIn(box), Create(edges), FadeIn(fresh), run_time=0.5)
        l1 = a5_mline("nodes/use_name_suffixes=true", -2.3, 1.5)
        l2 = a5_mline("nodes/use_node_type_suffixes=true", -2.3, 0.85)
        until(self, "both suffix settings", lead=0.6)
        self.play(FadeIn(l1), run_time=0.3)
        self.play(FadeIn(l2), run_time=0.3)
        d1 = Dot([-4.75, -0.5, 0], radius=0.1, color=TERRA); ld1 = Line([-4.63, -0.5, 0], [-2.45, -0.5, 0], color=INK, stroke_width=4)
        t1 = T("StaticBody3D", 36).move_to([-0.65, -0.5, 0])
        d2 = Dot([-4.75, -1.4, 0], radius=0.1, color=TERRA); ld2 = Line([-4.63, -1.4, 0], [-2.45, -1.4, 0], color=INK, stroke_width=4)
        t2 = T("ConvexPolygonShape3D", 36).move_to([0.4, -1.4, 0])
        until(self, "builds a static", lead=0.35)
        self.play(FadeIn(d1), Create(ld1), FadeIn(t1), run_time=0.4)
        until(self, "convex shape", lead=0.55)
        self.play(FadeIn(d2), Create(ld2), FadeIn(t2), run_time=0.4)
        done(self)


# ── B57 · only that setting off: the collider comes back as a visible box ───────────────────────────────────────────────────────
def a5_toggle(on, x, y):
    """A switch: outlined pill, knob on the right when ON, on the left when OFF (the knob is a grey dot with an ink outline)."""
    pill = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.4, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    knob = Circle(radius=0.27, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x + (0.37 if on else -0.37), y, 0])
    return pill, knob


class B57_SuffixAlone(Scene):
    def construct(self):
        x0, yf, s = 3.9, -2.55, 0.0026
        pill, knob = a5_toggle(True, -4.9, 1.9)
        name = a5_mline("use_node_type_suffixes", -3.75, 1.9)
        ghost = a5_img("pantry/a5_box.png", x0, yf, s=s, opacity=0.6)
        edges = VGroup(*[Line(a5_P(a, x0, yf, s), a5_P(b, x0, yf, s), color=DIM, stroke_width=4) for a, b in [
            ("box_mm_0", "box_pm_0"), ("box_pm_0", "box_pp_0"), ("box_mm_18", "box_pm_18"), ("box_pm_18", "box_pp_18"),
            ("box_mm_0", "box_mm_18"), ("box_pm_0", "box_pm_18"), ("box_pp_0", "box_pp_18")]])
        solid = a5_img("pantry/a5_boxopaque.png", x0, yf, s=s)
        self.add(pill, knob, name, ghost, edges)
        until(self, "Turn off", lead=0.1)
        self.play(knob.animate.move_to([-4.9 - 0.37, 1.9, 0]), run_time=0.45)
        until(self, "reimport", lead=0.2)
        loop = CurvedArrow([-1.6, 0.85, 0], [1.9, 0.2, 0], angle=-TAU / 6, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(loop), run_time=0.5)
        until(self, "visible box", lead=0.9)
        self.play(FadeOut(Group(ghost, edges)), FadeIn(solid), run_time=0.5)
        vb = T("visible box", 38).move_to([x0, 2.55, 0])
        self.play(FadeIn(vb), run_time=0.3)
        # no collision: a ring with a bar through it, on the box's lit face
        ring = Circle(radius=0.62, stroke_color=INK, stroke_width=9).move_to([x0 - 0.45, -0.2, 0])
        bar = Line([x0 - 0.45 - 0.44, -0.2 + 0.44, 0], [x0 - 0.45 + 0.44, -0.2 - 0.44, 0], color=INK, stroke_width=9)
        nc = T("no collision", 38).move_to([0.55, -0.3, 0])
        until(self, "no collision", lead=0.05)
        self.play(Create(ring), Create(bar), FadeIn(nc), run_time=0.6)
        # the suffix alone was enough; the extra physics block was redundant
        keep = RoundedRectangle(width=8.2, height=1.3, corner_radius=0.25, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-2.0, 1.9, 0])
        until(self, "The suffix setting alone", lead=0.1)
        self.play(Create(keep), run_time=0.5)
        sub = a5_mline("_subresources", -3.75, -1.9)
        xa = Line([-5.25, -1.65, 0], [-4.55, -2.15, 0], color=DIM, stroke_width=7)
        xb = Line([-5.25, -2.15, 0], [-4.55, -1.65, 0], color=DIM, stroke_width=7)
        until(self, "The extra physics", lead=0.1)
        self.play(FadeIn(sub), run_time=0.3)
        until(self, "redundant", lead=0.3)
        self.play(Create(xa), Create(xb), run_time=0.4)
        done(self)


# ── B58 · the floor check that was not a floor check ───────────────────────────────────────────────────────────────────────────
B58_X0, B58_YF, B58_S = -3.4, -2.75, 0.0026      # act 6 (B59+) continues this exact layout: pole foot on the floor at (B58_X0, B58_YF)


class B58_RayThroughNothing(Scene):
    def construct(self):
        x0, yf, s = B58_X0, B58_YF, B58_S
        lift = (A5_ORG[1] - A5_PT["lift158"][1]) * s            # the 15.8 cm the post floated, in scene units, from the real camera
        floor = a5_floor(x0, yf, s=s)
        fl = T("floor", 36).move_to([x0 - 1.85, yf + 0.65, 0])
        post = a5_img("pantry/a5_post.png", x0, yf + lift, s=s)
        self.add(floor, fl)
        until(self, "The agent had first", lead=0.3)
        self.play(FadeIn(post), run_time=0.5)
        # the gap: a dimension arrow on extension lines, to the right of the base
        pb = a5_P("base_pp_0", x0, yf + lift, s)
        xa = pb[0] + 0.85
        e1 = Line([pb[0] + 0.12, pb[1], 0], [xa + 0.2, pb[1], 0], color=DIM, stroke_width=3)
        e2 = Line([pb[0] + 0.12, pb[1] - lift, 0], [xa + 0.2, pb[1] - lift, 0], color=DIM, stroke_width=3)
        gap = dim_arrow([xa, pb[1] - lift, 0], [xa, pb[1], 0], tip=0.1)
        gl = T("16 cm", 36).move_to([xa + 1.0, pb[1] - lift / 2, 0])
        until(self, "sixteen centimetres", lead=0.35)
        self.play(Create(e1), Create(e2), Create(gap), FadeIn(gl), run_time=0.5)
        # the first test's ray: from 2 m above the post's base, straight down the pole's axis, through the missing collider, to the floor
        top = a5_P("ray_start158", x0, yf, s)
        bot = np.array([x0, yf, 0.0])
        ray = Arrow(top, bot, buff=0, color=INK, stroke_width=6, tip_length=0.22)
        hit = Dot(bot, radius=0.13, color=TERRA)
        ray_l = T("ray", 36).move_to([x0 + 0.75, top[1] - 0.15, 0])
        until(self, "Its first test", lead=0.0)
        self.play(Create(ray), FadeIn(ray_l), run_time=0.85)
        self.play(FadeIn(hit), run_time=0.2)
        nc = T("no collider", 36).move_to([x0 + 2.1, yf + 2.3, 0])
        ncd = Dot([x0 + 0.1, yf + 2.3, 0], radius=0.1, color=TERRA)
        ncl = Line([x0 + 0.22, yf + 2.3, 0], [x0 + 1.0, yf + 2.3, 0], color=INK, stroke_width=4)
        until(self, "straight through", lead=0.1)
        self.play(FadeIn(ncd), Create(ncl), FadeIn(nc), run_time=0.4)
        # what the first test printed (verbatim pieces of the real log line), joined to the dot and to the base by a leader each
        hit_l = a5_mline("ray hit at y=-4.0000", 1.2, -1.3)
        hit_ld = Line([x0 + 0.17, yf + 0.03, 0], [1.1, -1.3, 0], color=INK, stroke_width=4)
        until(self, "found the floor", lead=0.45)
        self.play(Create(hit_ld), FadeIn(hit_l), run_time=0.4)
        base_l2 = a5_mline("post base y=-3.8419", 1.2, -0.45)
        base_ld = Line([pb[0] + 0.05, pb[1] + 0.05, 0], [1.1, -0.45, 0], color=INK, stroke_width=4)
        self.play(Create(base_ld), FadeIn(base_l2), run_time=0.4)
        # the agent moved the post down onto the floor
        until(self, "so the agent moved", lead=0.2)
        new_l = a5_mline("post base y=-4.0", 1.2, -0.45)
        self.play(post.animate.shift(DOWN * lift), FadeOut(VGroup(e1, e2, gap, gl, base_ld)), run_time=0.7)
        base_ld2 = Line([pb[0] + 0.05, pb[1] - lift + 0.05, 0], [1.1, -0.45, 0], color=INK, stroke_width=4)
        self.play(FadeOut(base_l2), FadeIn(new_l), Create(base_ld2), run_time=0.3)
        done(self)


# ── B52 / B53 · the session on a timeline (numbers from the first run's own result events; transcripts/run1-claude.jsonl) ───────────────
A5_TL_X0, A5_TL_Y, A5_TL_U = -6.0, -2.45, 0.2927        # timeline: left edge, bar centre line, scene units per minute (41 min span)
A5_P1_MIN, A5_GAP_MIN, A5_P2_MIN = 21.2, 7.8, 11.96      # 1,271,707 ms | hung debug process | 717,737 ms


def a5_tl_x(minutes):
    return A5_TL_X0 + minutes * A5_TL_U


def a5_bar(m0, m1, y=A5_TL_Y, fill=BAR2):
    w = (m1 - m0) * A5_TL_U
    return Rectangle(width=w, height=0.55, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([a5_tl_x(m0) + w / 2.0, y, 0])


def a5_refusal_dots():
    """Nine refusals, drawn above the first bar (the nine 'requires approval' results in phase 1; see SESSION-act5.md)."""
    return VGroup(*[Dot([-5.35 + k * 0.62, A5_TL_Y + 0.8, 0], radius=0.12, color=TERRA) for k in range(9)])


class B52_TurnLimit(Scene):
    def construct(self):
        x_l = -5.45
        f = a5_mline("debug_options.gd", x_l, 2.85, color=DIM)
        n6, n8, n14 = a5_mline("6", -6.05, 2.2, color=DIM), a5_mline("8", -6.05, 1.55, color=DIM), a5_mline("14", -6.2, 0.9, color=DIM)
        l6 = a5_mline("var importer := ResourceImporterScene.new()", x_l, 2.2)
        l8 = a5_mline('importer.get_import_options("", opts, 0)', x_l, 1.55)
        l14 = a5_mline("quit(0)", x_l, 0.9, color=DIM)
        e1 = a5_mline("SCRIPT ERROR: Invalid call.", x_l, 0.05)
        e2 = a5_mline("Nonexistent function 'get_import_options'", x_l, -0.55)
        e3 = a5_mline("in base 'Nil'.", x_l, -1.15)
        fail = Dot([5.1, 1.55, 0], radius=0.11, color=TERRA)
        nev = T("never reached", 34).move_to([-2.35, 0.9, 0])
        run = T("kept running", 34).move_to([4.65, -1.45, 0])
        until(self, "It wrote", lead=0.0)
        self.play(FadeIn(f), FadeIn(VGroup(n6, l6)), run_time=0.4)
        self.play(FadeIn(VGroup(n8, l8)), run_time=0.3)
        until(self, "a method that", lead=0.45)
        self.play(FadeIn(fail), FadeIn(e1), run_time=0.3)
        self.play(FadeIn(e2), run_time=0.25)
        self.play(FadeIn(e3), run_time=0.25)
        until(self, "The script never", lead=0.3)
        self.play(FadeIn(VGroup(n14, l14)), FadeIn(nev), run_time=0.4)
        until(self, "kept running", lead=0.3)
        ring = Circle(radius=0.4, stroke_color=INK, stroke_width=6).move_to([5.5, -0.3, 0])
        arc = Arc(radius=0.4, start_angle=PI / 2, angle=-PI * 0.9, arc_center=[5.5, -0.3, 0], stroke_color=INK, stroke_width=12)
        self.play(Create(ring), Create(arc), FadeIn(run), run_time=0.4)
        bar1 = a5_bar(0, A5_P1_MIN)
        lab1 = T("61 turns · 21 min", 40).move_to([a5_tl_x(A5_P1_MIN / 2.0), A5_TL_Y - 0.65, 0])
        until(self, "At sixty-one", lead=0.0)
        self.play(GrowFromEdge(bar1, LEFT), FadeIn(lab1), run_time=0.9)
        lim = Line([a5_tl_x(A5_P1_MIN), A5_TL_Y - 0.5, 0], [a5_tl_x(A5_P1_MIN), A5_TL_Y + 0.5, 0], color=INK, stroke_width=8)
        limt = T("turn limit", 34).move_to([a5_tl_x(A5_P1_MIN) + 1.35, A5_TL_Y, 0])
        until(self, "turn limit", lead=0.45)
        self.play(Create(lim), FadeIn(limt), run_time=0.4)
        dots = a5_refusal_dots()
        ref = T("9 refused", 38).move_to([1.3, A5_TL_Y + 0.8, 0])
        until(self, "Nine commands", lead=0.15)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15), run_time=1.1)
        self.play(FadeIn(ref), run_time=0.3)
        done(self)


class B53_Resumed(Scene):
    def construct(self):
        bar1 = a5_bar(0, A5_P1_MIN)
        lab1 = T("61 turns · 21 min", 40).move_to([a5_tl_x(A5_P1_MIN / 2.0), A5_TL_Y - 0.65, 0])
        lim = Line([a5_tl_x(A5_P1_MIN), A5_TL_Y - 0.5, 0], [a5_tl_x(A5_P1_MIN), A5_TL_Y + 0.5, 0], color=INK, stroke_width=8)
        dots = a5_refusal_dots()
        ref = T("9 refused", 38).move_to([1.3, A5_TL_Y + 0.8, 0])
        self.add(bar1, lab1, lim, dots, ref)
        # the gap: the hung debug process, until we stopped it
        g0, g1 = a5_tl_x(A5_P1_MIN), a5_tl_x(A5_P1_MIN + A5_GAP_MIN)
        gap = Rectangle(width=g1 - g0, height=0.55, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([(g0 + g1) / 2.0, A5_TL_Y, 0])
        gap_l = T("hung", 36).move_to([(g0 + g1) / 2.0, A5_TL_Y - 0.65, 0])
        until(self, "When we stopped", lead=0.3)
        self.play(Create(gap), FadeIn(gap_l), run_time=0.7)
        # the completion notice that woke the agent (two real rows from the record)
        nt = a5_mline("task_notification", -5.0, 2.7, color=DIM)
        n1 = a5_mline('Background command "Print available', -5.0, 2.0)
        n2 = a5_mline('import options" completed (exit code 0)', -5.0, 1.4)
        arrow = Arrow([g1, A5_TL_Y + 0.4, 0], [g1, 0.95, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        until(self, "background task", lead=0.5)
        self.play(FadeIn(nt), FadeIn(n1), run_time=0.35)
        self.play(FadeIn(n2), Create(arrow), run_time=0.35)
        bar2 = a5_bar(A5_P1_MIN + A5_GAP_MIN, A5_P1_MIN + A5_GAP_MIN + A5_P2_MIN)
        lab2 = T("24 turns · 12 min", 40).move_to([a5_tl_x(A5_P1_MIN + A5_GAP_MIN + A5_P2_MIN / 2.0), A5_TL_Y - 0.65, 0])
        until(self, "woke the agent", lead=0.3)
        self.play(GrowFromEdge(bar2, LEFT), run_time=0.9)
        until(self, "twenty-four more", lead=0.45)
        self.play(FadeIn(lab2), run_time=0.3)
        done(self)


# ── B55 · the context is compacted; the full path is tried seven times ─────────────────────────────────────────────────────────
class B55_Compacted(Scene):
    def construct(self):
        # gauge: 172390 tokens -> 10266 tokens (compact_boundary event, transcripts/run1-claude.jsonl line 219)
        gx, gy0, gh = -5.45, -1.6, 3.2
        gauge = Rectangle(width=1.0, height=gh, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([gx, gy0 + gh / 2.0, 0])
        fill = Rectangle(width=1.0, height=gh, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([gx, gy0 + gh / 2.0, 0])
        small = Rectangle(width=1.0, height=gh * 10266 / 172390.0, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(
            [gx, gy0 + gh * 10266 / 172390.0 / 2.0, 0])
        ctx = T("context", 38).move_to([gx, gy0 + gh + 1.0, 0])
        n_pre = a5_mline("172390", gx - 0.75, gy0 + gh + 0.45)
        n_post = a5_mline("10266", gx - 0.62, gy0 - 0.45)
        self.add(gauge, ctx)
        self.play(FadeIn(fill), FadeIn(n_pre), run_time=0.5)
        until(self, "Then its context", lead=0.0)
        self.wait(0.3)
        self.play(Transform(fill, small), FadeIn(n_post), run_time=0.9)
        # what it forgot: the plain command that had worked every time before
        x_l = -3.6
        ok = a5_mline("godot --headless … --import", x_l, 2.45, color=DIM)
        okc = check(x_l - 0.38, 2.43, s=0.17, color=INK, w=7)
        until(self, "forgot that", lead=0.4)
        self.play(FadeIn(ok), Create(okc), run_time=0.5)
        # then the full application path, seven times, each one refused
        rows = VGroup(*[a5_mline("/Applications/Godot.app/…/Godot", x_l, 1.55 - k * 0.5) for k in range(7)])
        xs = VGroup(*[VGroup(Line([4.55, 1.55 - k * 0.5 + 0.17, 0], [4.9, 1.55 - k * 0.5 - 0.17, 0], color=INK, stroke_width=7),
                             Line([4.55, 1.55 - k * 0.5 - 0.17, 0], [4.9, 1.55 - k * 0.5 + 0.17, 0], color=INK, stroke_width=7)) for k in range(7)])
        until(self, "full application path", lead=0.9)
        for k in range(7):
            self.play(FadeIn(rows[k]), Create(xs[k]), run_time=0.3)
        ask = T("Please approve the Godot command …", 38).move_to([0.5, -2.15, 0])
        until(self, "asking a human", lead=0.2)
        self.play(FadeIn(ask), run_time=0.4)
        test = a5_mline("test_checkpoint_post.gd", -3.0, -2.95, color=DIM)
        nr = T("never ran", 36).move_to([4.5, -2.95, 0])
        until(self, "never ran", lead=0.35)
        self.play(FadeIn(test), FadeIn(nr), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act6.py ══════════════════════════════
"""ACT V (second half) · Building the Post, Then Checking the Builder  (B59-B71B)

One cast for the act: the CHECKPOINT POST drawn in Godot's side view (x across, Y up, metres), the pennant at its top right,
the collider outline around it (first the 0.6 m box, then the tapered hull), and Godot's floor line at y = -4.0.
The real Blender renders appear where the picture IS the thing: B59 continues act 5's layout (the real render on its ghost floor tile, marks placed through the render's camera), B70 and B71 use crops of post_visual.png / post_collider_only.png.
Every number on screen is a real log line, a real transcript line, or arithmetic reproduced by evidence/act6/derive_geometry.py.
"""
# ───────────────────────── act-6 helpers ─────────────────────────
A6_PENN_X0, A6_PENN_X1, A6_PENN_Y0, A6_PENN_Y1 = 0.08, 0.48, 1.55, 1.80      # the pennant, metres (Godot axes: x across, y up)


def a6_P(U, ox, oy):
    """Metres (x across, y up, y = 0 at the post's base underside) -> scene point."""
    return lambda x, y: np.array([ox + x * U, oy + y * U, 0.0])


def a6_rect(P, x0, y0, x1, y1, fill=None, stroke=INK, sw=4, fo=1.0):
    """Axis-aligned rectangle between two metre corners (explicit corners, no get_left)."""
    pts = [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]
    return Polygon(*pts, fill_color=fill if fill else STAGE, fill_opacity=fo if fill else 0, stroke_color=stroke, stroke_width=sw)


def a6_post(P, ghost=False, sw=4, metal=BAR3):
    """The post in Godot's side view: base slab, pole, pennant. ghost=True redraws it faded (an excluded body)."""
    if ghost:
        c = GHOST
        return VGroup(a6_rect(P, -0.3, 0.0, 0.3, 0.1, None, DIM, 3), a6_rect(P, -0.08, 0.1, 0.08, 1.8, None, DIM, 3),
                      a6_rect(P, A6_PENN_X0, A6_PENN_Y0, A6_PENN_X1, A6_PENN_Y1, None, DIM, 3))
    return VGroup(a6_rect(P, -0.3, 0.0, 0.3, 0.1, metal, INK, sw), a6_rect(P, -0.08, 0.1, 0.08, 1.8, metal, INK, sw),
                  a6_rect(P, A6_PENN_X0, A6_PENN_Y0, A6_PENN_X1, A6_PENN_Y1, BOX_L, INK, sw))


def a6_hull_pts():
    """The tapered hull's silhouette in the side view (6 corners): base slab +-0.30 up to y = 0.1, straight slope to +-0.08 at y = 1.8."""
    return [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.3, 0.1)]


def a6_hw(y):
    """Hull half-width at height y (metres): reproduces evidence/act6/derive_geometry.py."""
    return 0.30 if y <= 0.1 else 0.30 - 0.22 * (y - 0.1) / 1.7


def a6_mono(s, xl, y, size=32, color=INK):
    """Menlo line whose LEFT edge sits at xl (Menlo is 0.25 units per character at size 32)."""
    return M(s, size, color).move_to([xl + 0.25 * (size / 32.0) * len(s) / 2.0, y, 0])


# ── the real render (pantry/a6_post_run1.png, the act-V post, same camera as post_visual.png): marks are placed through the camera model ──
A6_CAM_LOC, A6_CAM_TGT, A6_FOCAL_PX = np.array([3.9, -4.6, 2.0]), np.array([0.12, 0.0, 0.9]), 42.0 / 36.0 * 4800     # evidence/act6/project_points.py
A6_CROP_W, A6_CROP_H, A6_CROP_ORG, A6_RENDER_ORG = 1457, 1943, (735.5, 1723.2), (1582, 402)                          # crop px of the pole's foot
A6_FLOOR_PX = [(-480.9, 1761.0), (860.9, 2201.3), (1903.2, 1687.0), (653.4, 1410.4)]                                 # the floor tile's corners (act 5's anchors)


def a6_proj(P):
    """World point (Blender x, y, z up) -> pixel in the crop."""
    f = A6_CAM_TGT - A6_CAM_LOC
    f = f / np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1])
    r = r / np.linalg.norm(r)
    u = np.cross(r, f)
    v = np.array(P, dtype=float) - A6_CAM_LOC
    return (2400.0 + A6_FOCAL_PX * (v @ r) / (v @ f) - A6_RENDER_ORG[0], 1350.0 - A6_FOCAL_PX * (v @ u) / (v @ f) - A6_RENDER_ORG[1])


def a6_pt(px, py, x0, yf, s):
    """Crop pixel -> scene point when the pole's foot is at scene (x0, yf) and one crop pixel is s scene units."""
    return np.array([x0 + (px - A6_CROP_ORG[0]) * s, yf + (A6_CROP_ORG[1] - py) * s, 0.0])


def a6_wp(P, x0, yf, s):
    px, py = a6_proj(P)
    return a6_pt(px, py, x0, yf, s)


def a6_img(path, x0, yf, s, opacity=1.0):
    im = ImageMobject(path)
    im.set_height(A6_CROP_H * s)
    im.move_to([x0 + (A6_CROP_W / 2 - A6_CROP_ORG[0]) * s, yf + (A6_CROP_ORG[1] - A6_CROP_H / 2) * s, 0])
    if opacity < 1.0:
        im.set_opacity(opacity)
    return im


def a6_tile(x0, yf, s, k=0.72):
    """The ghost floor tile under the post (the same tile as the preceding beats)."""
    org = a6_pt(A6_CROP_ORG[0], A6_CROP_ORG[1], x0, yf, s)
    pts = [org + (a6_pt(px, py, x0, yf, s) - org) * k for px, py in A6_FLOOR_PX]
    return Polygon(*pts, fill_color=GHOST, fill_opacity=1, stroke_width=0)


def a6_grid(P, only_x_below=None, hull=False):
    """The 41 x 26 sample grid of the physics query (1 cm pitch). Returns (all dots, inside dots, outside dots, n_inside).
    Inside = strictly inside the collider surface, the rule that reproduces the logged 572 (box) and 55 (hull)."""
    allg, ins, outs = [], [], []
    n = 0
    for i in range(41):
        x = round(0.08 + 0.01 * i, 2)
        for j in range(26):
            y = round(1.55 + 0.01 * j, 2)
            inside = (x < a6_hw(y) - 1e-9) if hull else (x < only_x_below - 1e-9)
            d = Dot(P(x, y), radius=0.03, color=BAR2)
            allg.append(d)
            (ins if inside else outs).append(d)
            n += 1 if inside else 0
    return VGroup(*allg), VGroup(*ins), VGroup(*outs), n


# ── B59 · the finished test's ray stops on the post; ours ignores the post and finds the floor (the real render, as in B58) ──────────
class B59_TwoRays(Scene):
    def construct(self):
        s, yf = 0.0013, -2.1
        xl, xr = -3.2, 2.9
        tile_l, tile_r = a6_tile(xl, yf, s), a6_tile(xr, yf, s)
        post_l = a6_img("pantry/a6_post_run1.png", xl, yf, s)
        post_r = a6_img("pantry/a6_post_run1.png", xr, yf, s)
        cap_l = T("the finished test", 36).move_to([xl, 3.05, 0])
        cap_r = T("our check", 36).move_to([xr, 3.05, 0])
        fl = T("floor", 34).move_to([xl - 2.15, yf - 0.02, 0])
        self.add(tile_l, tile_r, post_l, post_r, cap_l, cap_r, fl)
        top = a6_wp((0, 0, 1.8), xl, yf, s)
        start = a6_wp((0, 0, 3.8), xl, yf, s)               # 2 m above the post's top
        until(self, "starts two metres", lead=0.1)
        sdot = Dot(start, radius=0.1, color=INK)
        dm = dim_arrow([xl - 0.75, top[1] + 0.03, 0], [xl - 0.75, start[1], 0])
        dml = T("2 m", 36).move_to([xl - 1.4, (top[1] + start[1]) / 2, 0])
        self.play(FadeIn(sdot), Create(dm), FadeIn(dml), run_time=0.5)
        until(self, "stops on the post's own collider", lead=0.5)
        ray1 = Arrow(start + np.array([0, -0.12, 0]), top + np.array([0, 0.02, 0]), buff=0, color=INK, stroke_width=6, tip_length=0.22)
        self.play(GrowArrow(ray1), run_time=0.7)
        hit = Dot(top, radius=0.13, color=TERRA)
        hl = T("hit, y = -2.2", 34).move_to([xl + 1.95, top[1] + 0.05, 0])
        self.play(FadeIn(hit), FadeIn(hl), run_time=0.3)
        until(self, "not that it stands on anything", lead=0.0)
        nf = T("floor never reached", 34).move_to([xl, yf - 0.85, 0])
        self.play(FadeIn(nf), run_time=0.4)
        until(self, "Our ray", lead=0.2)
        self.play(post_r.animate.set_opacity(0.3), run_time=0.5)
        s2 = a6_wp((0, 0, 0.5), xr, yf, s)
        foot = a6_wp((0, 0, 0), xr, yf, s)
        sdot2 = Dot(s2, radius=0.1, color=INK)
        self.play(FadeIn(sdot2), run_time=0.25)
        until(self, "found the floor", lead=0.9)
        ray2 = Arrow(s2 + np.array([0, -0.1, 0]), foot + np.array([0, 0.03, 0]), buff=0, color=INK, stroke_width=6, tip_length=0.2)
        self.play(GrowArrow(ray2), run_time=0.6)
        fdot = Dot(foot, radius=0.13, color=TERRA)
        fy = T("y = -4.0", 34).move_to([xr, yf - 0.85, 0])
        self.play(FadeIn(fdot), FadeIn(fy), run_time=0.35)
        until(self, "with a gap of zero", lead=0.1)
        gp = T("gap 0.0 m", 36).move_to([xr + 2.1, yf + 0.55, 0])
        self.play(FadeIn(gp), run_time=0.4)
        done(self)


# ── B60 · the weakened check, in the agent's own two versions ───────────────────────────────────────────────────────
class B60_Weakened(Scene):
    def construct(self):
        XL = -5.0
        tag1 = T("first run", 36).move_to([XL + 0.9, 2.78, 0])
        f1 = a6_mono("FAIL  no unexpected materials", XL, 2.2)
        f2 = a6_mono('[found ["PostMetal", "FlagCloth", ""]]', XL, 1.7)
        tag2 = T("the edit", 36).move_to([XL + 0.78, 0.72, 0])
        tag3 = T("later run", 36).move_to([XL + 0.95, -1.12, 0])
        self.add(tag1, f1, f2)
        until(self, "unnamed default material", lead=0.3)
        # the unnamed entry: the empty name in the found list (index of the "" inside the line)
        s = '[found ["PostMetal", "FlagCloth", ""]]'
        k = s.index('""')
        dx = XL + 0.25 * (k + 1)
        dot = Dot([dx, 1.22, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(dot), run_time=0.3)
        until(self, "later version skips", lead=0.0)
        old = a6_mono("- if mat:", XL, 0.2, color=DIM)
        new = a6_mono('+ if mat and mat.resource_name != "":', XL, -0.32)
        self.play(FadeIn(tag2), FadeIn(old), run_time=0.3)
        self.play(FadeIn(new), run_time=0.5)
        until(self, "unnamed materials", lead=0.0)
        p1 = a6_mono("PASS  no unexpected named materials", XL, -1.72)
        p2 = a6_mono('["PostMetal", "FlagCloth"]', XL + 0.5, -2.22)
        ck = check(XL - 0.35, -1.72, 0.17, INK, 7)
        self.play(FadeIn(tag3), FadeIn(p1), FadeIn(p2), Create(ck), run_time=0.5)
        until(self, "Don't weaken", lead=0.1)
        mk = Dot([XL - 0.4, -0.32, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(mk), run_time=0.3)
        done(self)


# ── B61 · the box ran out to 0.3 m; the pennant runs 0.08 to 0.48 ───────────────────────────────────────────────────
class B61_BoxVsPennant(Scene):
    def construct(self):
        U = 10.0
        P = lambda x, y: np.array([-2.0 + U * x, 2.4 - U * (1.8 - y), 0.0])
        penn = a6_rect(P, 0.08, 1.55, 0.48, 1.80, BOX_R, INK, 5)
        pole = a6_rect(P, -0.08, 1.49, 0.08, 1.8, BAR1, INK, 5)
        lab_p = T("pennant", 36).move_to([4.15, 1.15, 0])
        lab_pole = T("pole", 36).move_to([-3.9, 0.9, 0])
        self.add(pole, penn, lab_p, lab_pole)
        until(self, "inside the collider", lead=1.5)
        top = Line(P(-0.3, 1.8), P(0.3, 1.8), color=INK, stroke_width=6)
        lft = Line(P(-0.3, 1.8), P(-0.3, 1.47), color=INK, stroke_width=6)
        rgt = Line(P(0.3, 1.8), P(0.3, 1.47), color=INK, stroke_width=6)
        lab_b = T("collider box", 36).move_to([-3.3, 2.92, 0])
        self.play(Create(top), Create(lft), Create(rgt), FadeIn(lab_b), run_time=0.9)
        over = a6_rect(P, 0.08, 1.55, 0.30, 1.80, "#A38C66", INK, 5)
        self.play(FadeIn(over), run_time=0.4)
        until(self, "point three metres", lead=0.6)
        d1 = dim_arrow([-2.0, -1.3, 0], [1.0, -1.3, 0])
        e1 = Line(P(0.3, 1.47), [1.0, -1.3, 0], color=DIM, stroke_width=3)
        l1 = T("box edge  0.3 m", 36).move_to([-0.5, -1.78, 0])
        self.play(Create(e1), Create(d1), FadeIn(l1), run_time=0.6)
        until(self, "pennant runs from", lead=0.1)
        d2 = dim_arrow([-1.2, -2.45, 0], [2.8, -2.45, 0])
        l2 = T("pennant  0.08 to 0.48 m", 36).move_to([0.8, -2.93, 0])
        self.play(Create(d2), FadeIn(l2), run_time=0.7)
        done(self)


# ── B62 · 1,066 sample points on a 1 cm grid; 572 inside the box; the agent's check passed anyway ──────────────────────
class B62_Sampled(Scene):
    def construct(self):
        U = 14.0
        P = lambda x, y: np.array([-4.4 + U * (x - 0.08), 1.9 - U * (1.8 - y), 0.0])
        outline = a6_rect(P, 0.08, 1.55, 0.48, 1.80, None, DIM, 4)
        pole = a6_rect(P, -0.0557, 1.53, 0.08, 1.8, BAR1, DIM, 4)
        face = Line(P(0.30, 1.843), P(0.30, 1.53), color=INK, stroke_width=6)
        fl = T("box face 0.3 m", 34).move_to([-1.32, 3.02, 0])
        cap = T("an illustration of the sampling; counts are from the run", 32).move_to([0.0, -3.05, 0])
        allg, ins, outs, n_in = a6_grid(P, only_x_below=0.30)
        self.add(outline, pole, face, fl, cap)
        until(self, "one centimetre grid", lead=1.4)
        gl = T("1 cm grid", 34).move_to([-5.2, 2.55, 0])
        self.play(FadeIn(allg), FadeIn(gl), run_time=0.7)
        until(self, "asked the physics server", lead=0.1)
        self.play(ins.animate.set_color(INK), run_time=0.5)
        until(self, "Five hundred seventy-two", lead=0.2)
        n572 = T("572", 84).move_to([4.1, 1.15, 0])
        self.play(FadeIn(n572), run_time=0.4)
        until(self, "of one thousand sixty-six", lead=0.2)
        n1066 = T("of 1,066 points", 40).move_to([4.1, 0.3, 0])
        lg = Dot([2.35, -0.5, 0], radius=0.1, color=BAR1)
        lgl = T("inside the collider", 34).move_to([4.5, -0.5, 0])
        self.play(FadeIn(n1066), FadeIn(lg), FadeIn(lgl), run_time=0.4)
        until(self, "The agent's check", lead=0.2)
        line1 = a6_mono("PASS  collision X_max ≤ 0.35 … [got 0.300]", -5.0, -2.45)
        self.play(FadeIn(line1), run_time=0.5)
        until(self, "passed anyway", lead=0.1)
        ck = check(-5.4, -2.45, 0.17, INK, 7)
        self.play(Create(ck), run_time=0.4)
        done(self)


# ── B63 · two constants typed into the test, not read from the scenes ───────────────────────────────────────────────
class B63_Constants(Scene):
    def construct(self):
        XL = -5.9
        r1 = a6_mono("PLAYER_CAP_H  := 2.10", XL, 0.7)
        r2 = a6_mono("POST_WORLD    := Vector3(-6.5, -4.0, 3.9334)", XL, -0.4)
        fn = a6_mono("test_checkpoint_post.gd", -4.9, -1.75, color=DIM)
        b1 = RoundedRectangle(width=3.5, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.3, 2.75, 0])
        t1 = a6_mono("player.tscn", -3.3 - 0.25 * 11 / 2, 2.75)
        b2 = RoundedRectangle(width=3.0, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.0, -2.75, 0])
        t2 = a6_mono("game.tscn", 3.0 - 0.25 * 9 / 2, -2.75)
        self.add(fn, b1, t1, b2, t2)
        until(self, "capsule height", lead=0.3)
        self.play(AddTextLetterByLetter(r1, run_time=0.9), run_time=0.9)
        until(self, "post's position", lead=0.3)
        self.play(AddTextLetterByLetter(r2, run_time=1.3), run_time=1.3)
        until(self, "not read from the scenes", lead=0.1)
        a1 = DashedLine([-3.3, 2.3, 0], [-3.3, 1.85, 0], color=DIM, stroke_width=5)
        a2 = DashedLine([3.0, -2.3, 0], [3.0, -1.6, 0], color=DIM, stroke_width=5)
        x1 = VGroup(Line([-3.5, 1.68, 0], [-3.1, 1.32, 0], color=INK, stroke_width=7), Line([-3.5, 1.32, 0], [-3.1, 1.68, 0], color=INK, stroke_width=7))
        x2 = VGroup(Line([2.8, -1.18, 0], [3.2, -1.52, 0], color=INK, stroke_width=7), Line([2.8, -1.52, 0], [3.2, -1.18, 0], color=INK, stroke_width=7))
        self.play(Create(a1), Create(a2), run_time=0.5)
        self.play(Create(x1), Create(x2), run_time=0.3)
        done(self)


# ───────────────────────── Codex beats: a real Codex still, pushed into ─────────────────────────
def a6_cam(st, g, zt, pb):
    """Animation that moves Group g so base-point pb sits at the frame centre at zoom zt. st = {"z":…, "t":…} is the group's current state."""
    r = zt / st["z"]
    t_new = -zt * np.array(pb, dtype=float)
    d = t_new - r * st["t"]
    st["z"], st["t"] = zt, t_new
    return g.animate.scale(r, about_point=ORIGIN).shift(d)


def a6_cur(st, pb):
    """Where base-point pb is on screen under the group's current camera state."""
    return st["z"] * np.array(pb, dtype=float) + st["t"]


# ── B64 · the revision prompt, typed into Codex: five asks ───────────────────────────────────────────────────────────
class B64_CodexAsk(Scene):
    def construct(self):
        W = 9.2
        C0 = np.array([0.0, 0.3, 0.0])
        img = ImageMobject("pantry/a6_codex_ask.png").set_width(W).move_to(C0)
        edge = Rectangle(width=W, height=W * 900 / 1600.0, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to(C0)
        grp = Group(img, edge)
        self.add(grp)
        WC, CY = 11.2, 0.3                                   # the two pre-cropped views of the prompt stay fully inside the title-safe frame
        kc = WC / 900.0
        HC = 450 * kc

        def cropmob(path):
            im = ImageMobject(path).set_width(WC).move_to([0, CY, 0])
            ed = Rectangle(width=WC, height=HC, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([0, CY, 0])
            return Group(im, ed)

        def mark(v, v0):                                      # a terracotta dot beside ask n: preview px (452, v) in the crop whose top is v0
            return Dot([-WC / 2 + (452 - 440) * kc, CY + HC / 2 - (v - v0) * kc, 0.0], radius=0.09, color=TERRA)
        cA, cB = cropmob("pantry/a6_codex_ask_cropA.png"), cropmob("pantry/a6_codex_ask_cropB.png")
        until(self, "session limit", lead=0.5)
        c1 = T("Claude Code, asked first:", 32, DIM).move_to([0, -2.62, 0])
        c2 = T("You've hit your session limit · resets 6:40pm (America/New_York)", 34).move_to([0, -3.06, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        until(self, "Five asks", lead=0.1)
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(grp), FadeIn(cA), run_time=0.5)
        until(self, "fix only the import setting", lead=0.2)
        m1 = mark(272, 115)
        self.play(FadeIn(m1), run_time=0.2)
        until(self, "make the floor check honest", lead=0.2)
        m2 = mark(445, 115)
        self.play(FadeOut(m1), FadeIn(m2), run_time=0.2)
        until(self, "read the capsule height", lead=0.2)
        m3 = mark(532, 115)
        self.play(FadeOut(m2), FadeIn(m3), run_time=0.2)
        until(self, "replace the pennant check", lead=0.7)
        self.play(FadeOut(m3), FadeOut(cA), FadeIn(cB), run_time=0.4)
        m4 = mark(561, 425)
        self.play(FadeIn(m4), run_time=0.2)
        until(self, "then rebuild and report", lead=0.2)
        m5 = mark(677, 425)
        self.play(FadeOut(m4), FadeIn(m5), run_time=0.2)
        done(self)


# ── B65 · what Codex did, then four crashes in its sandbox ───────────────────────────────────────────────────────────
A6_HULL6 = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.08, 1.8), (-0.08, 1.8), (-0.3, 0.1)]
A6_BOX6 = [(-0.3, 0.0), (0.3, 0.0), (0.3, 0.1), (0.3, 1.8), (-0.3, 1.8), (-0.3, 0.1)]


class B65_CodexCrashes(Scene):
    def construct(self):
        # ── Codex's own thread: found in the docs, edited, the hull ──
        W = 12.0
        C0 = np.array([0.0, 0.0, 0.0])
        k = W / 1600.0
        pv = lambda u, v: C0 + np.array([(u - 800) * k, -(v - 285) * k, 0.0])        # preview-pixel (1600 x 569)
        img = ImageMobject("pantry/a6_codex_found.png").set_width(W).move_to(C0)
        edge = Rectangle(width=W, height=W * 569 / 1600.0, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to(C0)
        marks = [Dot(pv(452, y), radius=0.09, color=TERRA).set_opacity(0) for y in (378, 446, 566)]
        grp = Group(img, edge, *marks)
        st = {"z": 1.0, "t": np.zeros(3)}
        self.add(grp)
        self.play(a6_cam(st, grp, 1.75, pv(963, 330)), run_time=0.9)
        until(self, "in the documentation", lead=0.9)
        self.play(marks[0].animate.set_opacity(1), run_time=0.2)
        until(self, "already on", lead=0.2)
        self.play(marks[0].animate.set_opacity(0), marks[1].animate.set_opacity(1), run_time=0.2)
        until(self, "replaced the box", lead=0.3)
        self.play(marks[1].animate.set_opacity(0), marks[2].animate.set_opacity(1), run_time=0.2)
        # ── the box becomes a tapered hull ──
        until(self, "tapered convex hull", lead=1.3)
        U = 2.4
        PH = a6_P(U, -3.4, -2.9)
        post = a6_post(PH)
        box = Polygon(*[PH(x, y) for x, y in A6_BOX6], fill_opacity=0, stroke_color=INK, stroke_width=6)
        hull = Polygon(*[PH(x, y) for x, y in A6_HULL6], fill_opacity=0, stroke_color=INK, stroke_width=6)
        lb = T("a box", 36).move_to([-1.5, 0.5, 0])
        self.play(FadeOut(grp), FadeIn(post), Create(box), FadeIn(lb), run_time=0.5)
        self.play(Transform(box, hull), run_time=0.8)
        lh = T("a tapered convex hull", 36).move_to([0.3, 0.5, 0])
        self.play(FadeOut(lb), FadeIn(lh), run_time=0.3)
        # ── the rebuild: four crashes ──
        until(self, "tried to rebuild", lead=0.2)
        self.play(FadeOut(post), FadeOut(box), FadeOut(lh), run_time=0.3)
        title = T("Blender, inside Codex's sandbox", 38).move_to([0, 2.75, 0])
        labels = ["as written", "private temp folder", "separate config folder", "--gpu-backend flag"]
        rows = [T(s, 36).move_to([-6.0 + 0.19 * len(s) / 2 + 0.0, 1.75 - 0.62 * i, 0]) for i, s in enumerate(labels)]
        exits = [a6_mono("exit 139", 3.9, 1.75 - 0.62 * i) for i in range(4)]
        self.play(FadeIn(title), FadeIn(rows[0]), run_time=0.4)
        until(self, "four times", lead=1.6)
        self.play(FadeIn(rows[1]), run_time=0.25)
        self.play(FadeIn(rows[2]), run_time=0.25)
        self.play(FadeIn(rows[3]), run_time=0.25)
        until(self, "exit code", lead=0.2)
        crosses = VGroup(*[VGroup(Line([3.35, 1.75 - 0.62 * i + 0.14, 0], [3.65, 1.75 - 0.62 * i - 0.14, 0], color=INK, stroke_width=7),
                                  Line([3.35, 1.75 - 0.62 * i - 0.14, 0], [3.65, 1.75 - 0.62 * i + 0.14, 0], color=INK, stroke_width=7)) for i in range(4)])
        self.play(FadeIn(VGroup(*exits)), Create(crosses), run_time=0.5)
        until(self, "graphics-backend check", lead=0.5)
        cl = T("crash site, from Blender's own crash log", 34).move_to([0, -0.95, 0])
        s1 = a6_mono("GPU_backend_type_selection_detect", -4.1, -1.65)
        s2 = a6_mono("metal_is_supported", -4.1, -2.17)
        self.play(FadeIn(cl), run_time=0.3)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.4)
        done(self)


# ── B66 · Codex reaches for the Blender application; the tool refuses; the rule that was not repeated ────────────────────
class B66_CodexRefused(Scene):
    def construct(self):
        W = 11.6
        C0 = np.array([0.0, 0.7, 0.0])
        ia = ImageMobject("pantry/a6_codex_tool_a_crop.png").set_width(W).move_to(C0)
        ib = ImageMobject("pantry/a6_codex_tool_b_crop.png").set_width(W).move_to(C0).set_opacity(0)
        grp = Group(ia, ib)
        self.add(grp)
        until(self, "That tool refused", lead=0.1)
        self.play(ia.animate.set_opacity(0), ib.animate.set_opacity(1), run_time=0.5)
        until(self, "We stopped the run there", lead=0.0)
        stop = Dot([-4.3, -2.45, 0], radius=0.12, color=TERRA)
        sl = T("stopped by the operator, 5 min 31 s in", 36).move_to([0, -2.45, 0])
        self.play(FadeIn(stop), FadeIn(sl), run_time=0.4)
        # ── the missing rule ──
        until(self, "The prompt hadn't repeated", lead=0.0)
        self.play(FadeOut(grp), FadeOut(stop), FadeOut(sl), run_time=0.3)
        cardA = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.4, 1.5, 0])
        cardB = RoundedRectangle(width=4.6, height=2.3, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.4, 1.5, 0])
        ha = T("first prompt", 34).move_to([-3.4, 2.3, 0])
        hb = T("revision prompt", 34).move_to([3.4, 2.3, 0])
        ra1 = a6_mono("Never open", -3.4 - 0.25 * 10 / 2, 1.5)
        ra2 = a6_mono("its window.", -3.4 - 0.25 * 11 / 2, 1.0)
        self.play(FadeIn(cardA), FadeIn(cardB), FadeIn(ha), FadeIn(hb), run_time=0.4)
        self.play(FadeIn(ra1), FadeIn(ra2), run_time=0.3)
        until(self, "never to open the window", lead=0.0)
        g1 = a6_mono("Never open", 3.4 - 0.25 * 10 / 2, 1.5, color=GHOST)
        g2 = a6_mono("its window.", 3.4 - 0.25 * 11 / 2, 1.0, color=GHOST)
        gbox = DashedVMobject(RoundedRectangle(width=3.7, height=1.4, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.4, 1.25, 0]), num_dashes=40)
        self.play(FadeIn(g1), FadeIn(g2), Create(gbox), run_time=0.5)
        # ── another way ──
        until(self, "another way", lead=0.7)
        l1 = T("first way", 34).move_to([-3.4, -0.55, 0])
        l2 = T("another way", 34).move_to([3.4, -0.55, 0])
        b1 = RoundedRectangle(width=3.4, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.4, -1.45, 0])
        t1 = a6_mono("Blender -b", -3.4 - 0.25 * 10 / 2, -1.45)
        x1 = a6_mono("exit 139", -3.4 - 0.25 * 8 / 2, -2.3)
        b2 = RoundedRectangle(width=3.4, height=0.85, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.4, -1.45, 0])
        t2 = a6_mono("cua_repl js", 3.4 - 0.25 * 11 / 2, -1.45)
        ar = Arrow([-1.5, -1.45, 0], [1.5, -1.45, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        self.play(FadeIn(l1), FadeIn(b1), FadeIn(t1), FadeIn(x1), run_time=0.4)
        self.play(Create(ar), FadeIn(l2), FadeIn(b2), FadeIn(t2), run_time=0.6)
        done(self)


# ── B67A · outside the sandbox: every check of the finished test, as a slot that fills ───────────────────────────────────
# The 16 PASS lines of logs/verify2-test_checkpoint_post.log (a count the evidence script re-derives); nothing is typed in by hand but the count source.
A6_PASS_LINES = [
    "visual height (Godot Y = Blender Z) ≈ 1.80 m  [got 1.8000]", "visual depth  (Godot Z = Blender Y) ≈ 0.60 m  [got 0.6000]",
    "visual width  (Godot X = Blender X) ≈ 0.78 m  [got 0.7800]", "all MeshInstance3D have unit scale  [3 meshes checked]",
    "PostMetal material present", "FlagCloth material present", 'no unexpected named materials  ["PostMetal", "FlagCloth"]',
    "at least one StaticBody3D present  [found 1]", "StaticBody3D has a ConvexPolygonShape3D", "collision Y_min ≤ 0.02 (covers base floor)",
    "collision Y_max ≥ 1.75 (covers pole top)  [got 1.800]", "no pennant length lies inside collider  [overlap 0.0000 m]",
    "player scene has a capsule collision shape", "prop height 1.80 m < player capsule 2.10 m",
    "downward ray hits supporting floor with post excluded", "floor is within 0.02 m of post base  [distance 0.0000 m]"]


class B67A_AllPass(Scene):
    def construct(self):
        n = len(A6_PASS_LINES)                                                   # 16, from the log
        sb = DashedVMobject(RoundedRectangle(width=3.5, height=4.1, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-4.4, 0.35, 0]), num_dashes=60)
        sbl = T("Codex's sandbox", 34).move_to([-4.4, 2.0, 0])
        xx = VGroup(Line([-4.8, 1.0, 0], [-4.0, 0.2, 0], color=INK, stroke_width=9), Line([-4.8, 0.2, 0], [-4.0, 1.0, 0], color=INK, stroke_width=9))
        ex = a6_mono("exit 139", -5.0, -0.6)
        ol = T("outside the sandbox", 36).move_to([2.2, 2.95, 0])
        cells = VGroup(*[RoundedRectangle(width=1.2, height=0.7, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4)
                         .move_to([-0.1 + 1.4 * (i % 4), 1.9 - 1.0 * (i // 4), 0]) for i in range(n)])
        self.add(sb, sbl, xx, ex, ol)
        until(self, "outside the sandbox", lead=0.6)
        self.play(FadeIn(cells), run_time=0.4)
        for ph in ("Sixteen of sixteen", "Seventeen of seventeen"):      # the voice now says sixteen (the log holds 16 PASS lines); the old words still cue if the sheet is not yet re-voiced
            if ph in _NARR.get("B67A", ""):
                until(self, ph, lead=0.1)
                break
        ticks = [check(float(cells[i].get_center()[0]) - 0.05, float(cells[i].get_center()[1]) + 0.02, 0.15, INK, 7) for i in range(n)]
        self.play(AnimationGroup(*[Create(t) for t in ticks], lag_ratio=0.18), run_time=1.5)
        hero = T(f"{n} of {n}", 72).move_to([2.2, -2.45, 0])
        self.play(FadeIn(hero), run_time=0.3)
        done(self)


# ── B68 · the vertex-only check: the hull's vertices at the pennant's height are the pole's corners ────────────────────────
class B68_VertexCheck(Scene):
    def construct(self):
        U = 2.6
        PH = a6_P(U, -3.0, -2.75)
        # the real log line, then its tick turns into a cross
        l1 = a6_mono("no pennant length lies inside collider", -4.3, 2.95)
        l2 = a6_mono("[overlap 0.0000 m]", -4.3, 2.5)
        tick = check(-4.75, 2.95, 0.17, INK, 7)
        cross = VGroup(Line([-4.95, 3.1, 0], [-4.6, 2.8, 0], color=INK, stroke_width=7), Line([-4.95, 2.8, 0], [-4.6, 3.1, 0], color=INK, stroke_width=7))
        self.add(l1, l2, tick)
        until(self, "is wrong", lead=0.2)
        self.play(Transform(tick, cross), run_time=0.4)
        # the post and its hull
        post = a6_post(PH, metal=BAR2)
        hull = Polygon(*[PH(x, y) for x, y in A6_HULL6], fill_opacity=0, stroke_color=INK, stroke_width=6)
        until(self, "The check looked only", lead=0.3)
        self.play(FadeIn(post), Create(hull), run_time=0.9)
        until(self, "vertices at", lead=0.2)
        verts = VGroup(*[Dot(PH(x, y), radius=0.09, color=INK) for x, y in A6_HULL6])
        self.play(FadeIn(verts), run_time=0.3)
        vl = T("hull vertices", 34).move_to([0.2, -2.6, 0])
        self.play(FadeIn(vl), run_time=0.2)
        until(self, "pennant's height", lead=0.3)
        band = Polygon(PH(-0.55, 1.55), PH(0.95, 1.55), PH(0.95, 1.8), PH(-0.55, 1.8), fill_opacity=0, stroke_color=DIM, stroke_width=4)
        bl = T("the check's window", 34).move_to([2.55, 1.45, 0])
        self.play(Create(band), FadeIn(bl), run_time=0.45)
        until(self, "pole's corners", lead=0.2)
        rings = VGroup(Dot(PH(0.08, 1.8), radius=0.15, color=TERRA), Dot(PH(-0.08, 1.8), radius=0.15, color=TERRA))
        xl = T("x = 0.08", 34).move_to([2.55, 0.75, 0])
        self.play(FadeIn(rings), FadeIn(xl), run_time=0.3)
        until(self, "slanted faces", lead=0.2)
        slide = Dot(PH(0.08, 1.8), radius=0.12, color=TERRA)
        self.play(FadeIn(slide), run_time=0.15)
        self.play(MoveAlongPath(slide, Line(PH(0.08, 1.8), PH(0.3, 0.1))), run_time=1.3)
        fl = T("a face, not a vertex", 34).move_to([2.55, -0.45, 0])
        self.play(FadeIn(fl), run_time=0.3)
        done(self)


# ── B69 · the same 1,066 points against the tapered hull: 55 inside, a 3 cm sliver ────────────────────────────────────────
class B69_Sliver(Scene):
    def construct(self):
        U = 14.0
        P = lambda x, y: np.array([-4.4 + U * (x - 0.08), 1.9 - U * (1.8 - y), 0.0])
        outline = a6_rect(P, 0.08, 1.55, 0.48, 1.80, None, DIM, 4)
        pole = a6_rect(P, -0.0557, 1.543, 0.08, 1.8, BAR1, DIM, 4)
        yb = 1.543
        face = Line(P(0.08, 1.8), P(a6_hw(yb), yb), color=INK, stroke_width=6)
        cap = T("an illustration of the sampling; counts are from the run", 32).move_to([0.0, -3.15, 0])
        allg, ins, outs, n_in = a6_grid(P, hull=True)
        self.add(outline, pole, face, cap)
        self.play(FadeIn(allg), run_time=0.6)
        until(self, "fifty-five", lead=0.2)
        self.play(ins.animate.set_color(INK), run_time=0.5)
        n55 = T("55", 84).move_to([4.1, 1.15, 0])
        self.play(FadeIn(n55), run_time=0.35)
        until(self, "of one thousand sixty-six", lead=0.1)
        n1066 = T("of 1,066 points", 40).move_to([4.1, 0.3, 0])
        lg = Dot([2.35, -0.5, 0], radius=0.1, color=INK)
        lgl = T("inside the collider", 34).move_to([4.5, -0.5, 0])
        self.play(FadeIn(n1066), FadeIn(lg), FadeIn(lgl), run_time=0.4)
        until(self, "reaching point one one", lead=0.2)
        xm = T("x = 0.11 m", 34).move_to([-2.4, -2.52, 0])
        self.play(FadeIn(xm), run_time=0.3)
        until(self, "three centimetre", lead=0.2)
        d3 = dim_arrow([-4.4, -2.1, 0], [-3.98, -2.1, 0], tip=0.1)
        l3 = T("3 cm", 36).move_to([-4.19, -2.52, 0])
        self.play(Create(d3), FadeIn(l3), run_time=0.45)
        until(self, "box's five hundred", lead=0.1)
        b572 = T("572", 60, DIM).move_to([2.55, -1.4, 0])
        bl = T("with the box", 34).move_to([4.85, -1.4, 0])
        self.play(FadeIn(b572), FadeIn(bl), run_time=0.4)
        until(self, "still not zero", lead=0.0)
        nz = Dot([2.15, 1.15, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(nz), run_time=0.3)
        done(self)


# ── B70 · the invisible collision around the pole: 0.19 m hull half-width at mid-taper against the pole's 0.08 m ─────────────
class B70_Invisible(Scene):
    def construct(self):
        U = 3.0
        PH = a6_P(U, -3.2, -2.85)
        post = a6_post(PH, metal=BAR2)
        img_v = ImageMobject("pantry/a6_post_visual.png").set_height(5.2).move_to([4.3, 0.2, 0])
        img_o = ImageMobject("pantry/a6_post_overlay.png").set_height(5.2).move_to([4.3, 0.2, 0]).set_opacity(0)
        self.add(post, img_v)
        until(self, "invisible collision", lead=1.2)
        hullfill = Polygon(*[PH(x, y) for x, y in A6_HULL6], fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).set_z_index(-1)
        self.add(img_o)
        self.play(FadeIn(hullfill), img_o.animate.set_opacity(1), run_time=0.8)
        il = T("invisible collision", 34).move_to([0.25, 1.3, 0])
        ld = Line([PH(a6_hw(1.38), 1.38)[0] + 0.2, 1.3, 0], [-1.6 - 0.35, 1.3, 0], color=DIM, stroke_width=3)
        ol = T("collider over the post", 32).move_to([4.3, -2.85, 0])
        self.play(FadeIn(il), Create(ld), FadeIn(ol), run_time=0.35)
        until(self, "eleven centimetres", lead=0.1)
        yy = 0.95
        hw = a6_hw(yy)
        dl = dim_arrow(PH(-hw, yy), PH(-0.08, yy), tip=0.1)
        dr = dim_arrow(PH(0.08, yy), PH(hw, yy), tip=0.1)
        ll = T("11 cm", 34).move_to([PH(-hw, yy)[0] - 0.8, PH(-hw, yy)[1], 0])
        lr = T("11 cm", 34).move_to([PH(hw, yy)[0] + 0.8, PH(hw, yy)[1], 0])
        self.play(Create(dl), Create(dr), FadeIn(ll), FadeIn(lr), run_time=0.6)
        until(self, "design judgment", lead=0.1)
        dj = T("a design judgment", 36).move_to([0.25, -1.7, 0])
        self.play(FadeIn(dj), run_time=0.4)
        done(self)


# ── B71A / B71B · what a pass proves and what it does not: the lecture's last picture ───────────────────────────────────
def a6_final_base(self):
    """The shared set of the last two beats: the real post render on its floor line, two column headers and the divider."""
    img = ImageMobject("pantry/a6_post_visual.png").set_height(5.3).move_to([-4.65, 0.1, 0])
    floor = Line([-6.1, -2.55, 0], [-3.2, -2.55, 0], color=DIM, stroke_width=6)
    div = Line([1.15, 2.3, 0], [1.15, -2.2, 0], color=DIM, stroke_width=3)
    ha = T("a test proves", 40).move_to([-1.0, 2.8, 0])
    hb = T("a person judges", 40).move_to([3.45, 2.8, 0])
    self.add(img, floor, div, ha, hb)


A6_PROVES = ["size", "axes", "scale", "materials", "collision shape", "base on the floor"]
A6_NOT = ["looks right, lit", "metal and cloth", "collider feels fair", "suits the level"]


A6_W36 = {"size": 0.618, "axes": 0.727, "scale": 0.818, "materials": 1.634, "collision shape": 2.615, "base on the floor": 3.106,
          "looks right, lit": 2.493, "metal and cloth": 2.884, "collider feels fair": 2.947, "suits the level": 2.396}   # measured: EB Garamond 36


def a6_row(label, xl, y, kind):
    """One row: a mark (ink check, or an empty ring) and its label (left edge xl + 0.5)."""
    t = T(label, 36).move_to([xl + 0.5 + A6_W36[label] / 2.0, y, 0])
    m = check(xl - 0.15, y, 0.17, INK, 7) if kind == "ok" else Circle(radius=0.17, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([xl - 0.1, y, 0])
    return t, m


class B71A_Proves(Scene):
    def construct(self):
        a6_final_base(self)
        until(self, "size,", lead=0.2)
        for i, s in enumerate(A6_PROVES):
            if i == 4:
                until(self, "collision shape", lead=0.15)
            if i == 5:
                until(self, "base touches", lead=0.4)
            if i == 1:
                until(self, "axes", lead=0.1)
            if i == 2:
                until(self, "scale", lead=0.1)
            if i == 3:
                until(self, "materials", lead=0.1)
            t, m = a6_row(s, -2.9, 1.85 - 0.72 * i, "ok")
            self.play(FadeIn(t), Create(m), run_time=0.3)
        dot = Dot([-4.65 + 0.07, -2.5, 0], radius=0.13, color=TERRA)
        self.play(FadeIn(dot), run_time=0.3)
        done(self)


class B71B_Not(Scene):
    def construct(self):
        a6_final_base(self)
        for i, s in enumerate(A6_PROVES):
            t, m = a6_row(s, -2.9, 1.85 - 0.72 * i, "ok")
            self.add(t, m)
        self.add(Dot([-4.65 + 0.07, -2.5, 0], radius=0.13, color=TERRA))
        until(self, "looks right", lead=0.15)
        for i, s in enumerate(A6_NOT):
            if i == 1:
                until(self, "materials read", lead=0.15)
            if i == 2:
                until(self, "collider feels fair", lead=0.15)
            if i == 3:
                until(self, "placement suits", lead=0.15)
            t, m = a6_row(s, 1.75, 1.85 - 0.72 * i, "no")
            self.play(FadeIn(t), Create(m), run_time=0.3)
        until(self, "for a person", lead=0.2)
        eye = VGroup(Ellipse(width=1.5, height=0.8, stroke_color=INK, stroke_width=6, fill_opacity=0), Dot([0, 0, 0], radius=0.17, color=INK)).move_to([3.45, -1.55, 0])
        self.play(Create(eye), run_time=0.5)
        spark = Dot([3.45, -1.55, 0], radius=0.08, color=TERRA)
        self.play(FadeIn(spark), run_time=0.2)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
