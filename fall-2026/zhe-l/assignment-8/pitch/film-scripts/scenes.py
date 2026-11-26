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


# ═════════════════════════════ film helpers (walker-survival-shooting pitch) ═════════════════════════════
def _target(self):
    return _TARGET.get(type(self).__name__.split("_")[0], 0)


def mid_guard(self, margin=0.32):
    """Hold still across the clip midpoint, where GATE T and Gate V sample: wait until midpoint + margin."""
    t = _target(self)
    if not t:
        return
    gap = t / 2 + margin - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def tag(text):
    """The on-screen disclosure for a drawing (bottom right)."""
    t = T(text, 32)
    return t.move_to([5.9 - t.width / 2, -3.0, 0])


def tablet(iso, x, y, z=0.0, w=2.6, d=1.8):
    """The film's tablet: a dark slab with a pale screen on its top face. Returns (body, screen corners helper)."""
    body = iso.box(x, y, z, w, d, 0.22, DARK_TOP, DARK_L, DARK_R)
    zt = z + 0.22
    screen = iso.quad([(x + 0.18, y + 0.18, zt), (x + w - 0.18, y + 0.18, zt), (x + w - 0.18, y + d - 0.18, zt), (x + 0.18, y + d - 0.18, zt)],
                      CARD, stroke=GHOST, sw=2)
    return VGroup(body, screen)


def screen_line(iso, x, y, z, w, f, frac=1.0):
    """One ghost text line on a tablet screen at depth fraction f."""
    zt = z + 0.22
    d = 1.8
    return Line(iso.p(x + 0.4, y + d * f, zt), iso.p(x + 0.4 + (w - 0.8) * frac, y + d * f, zt), color=BAR1, stroke_width=5)


# ═════════════════════════════ scenes ═════════════════════════════
class B01_OneSentence(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        iso = Iso(-2.2, -1.1, 1.15)
        tab = tablet(iso, 0, 0)
        self.play(FadeIn(tab, shift=DOWN * 0.4), run_time=0.9)
        lines = [screen_line(iso, 0, 0, 0, 2.6, f, fr) for f, fr in ((0.72, 1.0), (0.52, 0.8), (0.32, 0.6))]
        for ln in lines:
            self.play(Create(ln), run_time=0.55)
        face = Circle(radius=0.95, color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([3.6, 0.4, 0])
        hand = Line([3.6, 0.4, 0], [3.6, 1.15, 0], color=INK, stroke_width=7)
        hub = Dot([3.6, 0.4, 0], radius=0.09, color=INK)
        self.play(FadeIn(face), Create(hand), FadeIn(hub), run_time=0.7)
        l1 = T("memo", 40).move_to([-2.2, -2.5, 0])
        l2 = T("keeps running", 40).move_to([3.6, -1.1, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        mid_guard(self)
        self.play(Rotate(hand, angle=-PI * 0.9, about_point=np.array([3.6, 0.4, 0])), run_time=2.4)
        tip = Dot(hand.get_end(), radius=0.1, color=TERRA)
        self.play(FadeIn(tip), run_time=0.3)
        finish(self)


class B02_TheBuild(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · WILL"))
        iso = Iso(-0.6, -1.6, 1.0)
        back, front = iso.open_box(0, 0, 0, 3.0, 3.0, 1.6)
        lid = iso.quad([(0, 0, 1.6), (3.0, 0, 1.6), (3.0, 3.0, 1.6), (0, 3.0, 1.6)], BOX_TOP)
        lid.set_z_index(3)
        plinth = iso.box(-0.35, -0.35, -0.35, 3.7, 3.7, 0.35, DARK_TOP, DARK_L, DARK_R)
        plinth.set_z_index(-1)
        self.play(FadeIn(VGroup(plinth, back, front, lid), shift=DOWN * 0.5), run_time=1.0)
        self.play(lid.animate.shift(UP * 1.6 + RIGHT * 2.2).set_opacity(0), run_time=0.9)
        self.remove(lid)
        floor = iso.quad([(0.5, 0.5, 0.05), (2.5, 0.5, 0.05), (2.5, 2.5, 0.05), (0.5, 2.5, 0.05)], PAGE_TOP, stroke=DIM, sw=2)
        wall1 = iso.quad([(2.5, 0.5, 0.05), (2.5, 2.5, 0.05), (2.5, 2.5, 1.0), (2.5, 0.5, 1.0)], PAGE_L, stroke=DIM, sw=2)
        wall2 = iso.quad([(0.5, 2.5, 0.05), (2.5, 2.5, 0.05), (2.5, 2.5, 1.0), (0.5, 2.5, 1.0)], PAGE_R, stroke=DIM, sw=2)
        desk = iso.box(1.6, 1.6, 0.05, 0.6, 0.5, 0.35, DARK_TOP, DARK_L, DARK_R, sw=2)
        room = VGroup(floor, wall1, wall2, desk)
        room.set_z_index(1)
        self.play(FadeIn(room, shift=UP * 0.6), run_time=1.0)
        l1 = T("Windows build", 40).move_to([-4.3, -1.4, 0])
        l2 = T("one room", 40).move_to([4.0, 1.4, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        mid_guard(self)
        will = VGroup(pill(-4.6, 0.2, 1.6, 0.7, CARD).set_stroke(INK, 3), T("WILL", 36).move_to([-4.6, 0.2, 0]))
        self.play(FadeIn(will), run_time=0.4)
        spark = Dot(iso.p(3.0, 0.0, 1.6), radius=0.1, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        finish(self)


class B03_Difference(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        iso = Iso(-4.2, -1.2, 0.8)
        boxes = VGroup(*[iso.box(i * 2.0, -i * 2.0, 0, 1.6, 1.6, 1.3) for i in range(4)])
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.4) for b in boxes], lag_ratio=0.2), run_time=1.1)
        l1 = T("many examples", 40).move_to([-1.6, -2.6, 0])
        self.play(FadeIn(l1), run_time=0.3)
        last = boxes[3]
        self.play(last[2].animate.shift(UP * 1.2).set_opacity(0), run_time=0.6)
        tab = tablet(Iso(-4.2, -1.2, 0.8), 3 * 2.0 - 0.5, -3 * 2.0 - 0.1, 1.3, 2.6, 1.8).scale(0.8)
        tab.move_to(np.array(last.get_center()) + UP * 0.9 + LEFT * 0.4)
        self.play(FadeIn(tab, shift=UP * 0.6), run_time=0.6)
        l2 = T("the tablet", 40).next_to(tab, LEFT, buff=0.4)
        self.play(FadeIn(l2), run_time=0.3)
        mid_guard(self)
        spark = Dot(np.array(tab.get_center()) + UP * 0.05, radius=0.1, color=TERRA)
        self.play(FadeIn(spark, scale=1.5), run_time=0.4)
        finish(self)


class B04_Checklist(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        card = RoundedRectangle(width=5.2, height=5.0, corner_radius=0.25, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-0.8, -0.3, 0])
        self.play(FadeIn(card, shift=UP * 0.3), run_time=0.6)
        rows = []
        for i in range(4):
            y = 1.4 - i * 1.15
            sq = Square(0.55, color=DIM, stroke_width=4).move_to([-2.6, y, 0])
            ln = Line([-1.9, y, 0], [0.9 - (i % 2) * 0.7, y, 0], color=BAR2, stroke_width=8)
            rows.append((sq, ln, y))
        self.play(*[FadeIn(VGroup(s, l)) for s, l, _ in rows], run_time=0.6)
        l1 = T("quest list", 40).move_to([4.0, 1.8, 0])
        self.play(FadeIn(l1), run_time=0.3)
        for s, l, y in rows[:2]:
            self.play(Create(check(-2.62, y + 0.05, 0.2)), run_time=0.45)
            self.wait(0.6)
        mid_guard(self)
        for s, l, y in rows[2:]:
            self.play(Create(check(-2.62, y + 0.05, 0.2)), run_time=0.45)
            self.wait(0.6)
        arrow = Arrow([1.9, -2.15, 0], [3.6, -2.15, 0], color=INK, stroke_width=6, buff=0)
        self.play(GrowArrow(arrow), run_time=0.5)
        finish(self)


class B05_ClueLoop(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · PLANNED"))
        goal = iso_goal = Iso(-5.0, 1.5, 0.9)
        card = goal.box(0, 0, 0, 1.4, 1.0, 0.5)
        self.play(FadeIn(card, shift=DOWN * 0.3), run_time=0.6)
        lg = T("goal", 40).move_to([-3.0, 2.3, 0])
        self.play(FadeIn(lg), run_time=0.3)
        until(self, "Each faction")
        isoA = Iso(-4.2, -1.6, 1.0)
        pa = isoA.page(0, 0, 0)
        isoB = Iso(-1.6, -1.6, 1.0)
        pb = isoB.page(0, 0, 0)
        self.play(FadeIn(pa, shift=UP * 0.3), FadeIn(pb, shift=UP * 0.3), run_time=0.7)
        lt = T("testimonies", 40).move_to([-2.9, -2.9, 0])
        self.play(FadeIn(lt), run_time=0.3)
        isoC = Iso(2.8, -0.8, 1.4)
        pc = isoC.page(0, 0, 0)
        self.play(FadeIn(pc, shift=LEFT * 0.3), run_time=0.6)
        lm = T("your memo", 40).move_to([3.9, -2.2, 0])
        self.play(FadeIn(lm), run_time=0.3)
        for src, k in ((pa, 0), (pb, 1)):
            piece = src[1][k].copy()
            dest = isoC.p(0.25, 1.4 * (0.32 + 0.2 * k), 0.07)
            self.play(MoveAlongPath(piece, ArcBetweenPoints(np.array(piece.get_center()), dest)), run_time=0.8)
        mid_guard(self)
        ring = Ellipse(width=1.5, height=0.6, color=INK, stroke_width=5).move_to(isoC.p(0.55, 1.4 * 0.42, 0.07))
        self.play(Create(ring), run_time=0.8)
        dot = Dot(np.array(ring.get_right()), radius=0.1, color=TERRA)
        self.play(FadeIn(dot), run_time=0.3)
        finish(self)


class B06_Menus(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        names = ["Phantom Pain", "Subnautica", "Abiotic Factor"]
        xs = [-3.8, -0.2, 3.4]
        tabs, labels = [], []
        for i, (x, name) in enumerate(zip(xs, names)):
            iso = Iso(x - 1.0, -0.6, 0.75)
            t = tablet(iso, 0, 0)
            row = VGroup(*[iso.quad([(0.35 + j * 0.65, 1.2, 0.23), (0.85 + j * 0.65, 1.2, 0.23), (0.85 + j * 0.65, 1.5, 0.23), (0.35 + j * 0.65, 1.5, 0.23)],
                                    GHOST, stroke=DIM, sw=2) for j in range(3)])
            lab = T(name, 36).move_to([x, -1.9, 0])
            tabs.append((iso, t, row))
            labels.append(lab)
            self.play(FadeIn(t, shift=DOWN * 0.3), FadeIn(row), FadeIn(lab), run_time=0.7)
            if i < 2:
                self.wait(1.4)
        for iso, t, row in tabs:
            self.play(row[0].animate.set_fill(BAR1), run_time=0.4)
        mid_guard(self)
        for k in (1, 2):
            for iso, t, row in tabs:
                self.play(row[k].animate.set_fill(BAR1), row[k - 1].animate.set_fill(GHOST), run_time=0.35)
            self.wait(0.6)
        world = Iso(5.0, 1.6, 0.6).box(0, 0, 0, 1.0, 1.0, 0.8)
        self.play(FadeIn(world), run_time=0.4)
        finish(self)


class B14_FirstLoop(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED · WILL"))
        gun = Polygon([-5.6, 1.6, 0], [-3.4, 1.6, 0], [-3.4, 1.15, 0], [-4.3, 1.15, 0], [-4.5, 0.4, 0], [-5.0, 0.4, 0], [-4.85, 1.15, 0], [-5.6, 1.15, 0],
                      fill_color=DARK_TOP, fill_opacity=1, stroke_color=INK, stroke_width=3)
        door = Rectangle(width=1.2, height=1.9, fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.9, 1.0, 0])
        knob = Dot([-2.25, 0.95, 0], radius=0.07, color=INK)
        self.play(FadeIn(gun, shift=RIGHT * 0.3), FadeIn(door), FadeIn(knob), run_time=0.7)
        stamp = VGroup(pill(-3.6, -0.5, 2.8, 0.8, CARD).set_stroke(INK, 4), T("NOT NOW", 40).move_to([-3.6, -0.5, 0]))
        self.play(FadeIn(stamp, scale=1.2), run_time=0.4)
        until(self, "First I will build")
        lf = T("first loop", 40).move_to([2.6, 2.4, 0])
        self.play(FadeIn(lf), run_time=0.3)
        iso = Iso(-0.6, -0.9, 0.6)
        pages = [iso.page(i * 1.3, -i * 1.3, 0, 1.0, 1.2) for i in range(5)]
        for p in pages[:3]:
            self.play(FadeIn(p, shift=UP * 0.25), run_time=0.45)
            self.wait(0.35)
        mid_guard(self)
        for p in pages[3:]:
            self.play(FadeIn(p, shift=UP * 0.25), run_time=0.45)
            self.wait(0.35)
        spark = Dot(np.array(pages[-1].get_center()) + UP * 0.35, radius=0.1, color=TERRA)
        self.play(FadeIn(spark, scale=1.5), run_time=0.4)
        finish(self)


class B15_Shrink(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        iso = Iso(-1.4, -2.4, 1.0)
        big = iso.box(0, 0, 0, 3.2, 3.2, 2.6)
        self.play(FadeIn(big, shift=DOWN * 0.4), run_time=0.7)
        self.wait(0.8)
        core = Iso(-0.5, -1.0, 1.0).box(0, 0, 0, 1.2, 1.2, 1.0)
        self.play(ReplacementTransform(big, core), run_time=1.0)
        lc = T("core idea", 40).move_to([0.0, -2.2, 0])
        self.play(FadeIn(lc), run_time=0.3)
        mid_guard(self)
        names = ["shared code", "named constants", "standalone apps", "request backend", "sheet to data", "body + brain"]
        spots = [(-4.6, 2.0), (-4.6, 0.6), (-4.6, -0.8), (3.0, 2.0), (3.0, 0.6), (3.0, -0.8)]
        for (x, y), name in zip(spots, names):
            blk = Iso(x - 1.3, y - 0.35, 0.55).box(0, 0, 0, 0.8, 0.8, 0.5)
            lab = T(name, 32).next_to(blk, RIGHT, buff=0.35)
            self.play(FadeIn(blk, shift=(RIGHT if x < 0 else LEFT) * 0.3), FadeIn(lab), run_time=0.35)
        finish(self)


class B16_Learning(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        isoL = Iso(-3.6, -2.0, 0.9)
        backL, frontL = isoL.open_box(0, 0, 0, 3.2, 2.4, 0.9)
        isoR = Iso(3.0, -2.0, 0.9)
        backR, frontR = isoR.open_box(0, 0, 0, 1.8, 1.8, 0.9)
        self.play(FadeIn(VGroup(backL, frontL)), FadeIn(VGroup(backR, frontR)), run_time=0.7)
        ln = T("new", 40).move_to([-3.6, 2.4, 0])
        lh = T("had", 40).move_to([3.0, 2.4, 0])
        self.play(FadeIn(ln), FadeIn(lh), run_time=0.3)
        items = [isoL.box(0.3 + i * 0.6, 0.5 + (i % 2) * 0.9, 0.0, 0.45, 0.45, 0.45 + 0.1 * (i % 3)) for i in range(5)]
        for it in items:
            it.set_z_index(1)
        for it in items[:3]:
            self.play(FadeIn(it, shift=DOWN * 0.8, rate_func=ease_in), run_time=0.5)
            self.wait(0.6)
        mid_guard(self)
        for it in items[3:]:
            self.play(FadeIn(it, shift=DOWN * 0.8, rate_func=ease_in), run_time=0.5)
            self.wait(0.6)
        code = isoR.box(0.6, 0.6, 0.0, 0.6, 0.6, 0.5, DARK_TOP, DARK_L, DARK_R)
        code.set_z_index(1)
        self.play(FadeIn(code, shift=DOWN * 0.8, rate_func=ease_in), run_time=0.5)
        finish(self)


class B17_ExistsWill(Scene):
    def construct(self):
        self.add(tag("CONSTRUCTED"))
        isoL = Iso(-4.4, -1.6, 0.8)
        solid = VGroup(*[isoL.box(i * 0.9, 0.3, 0, 0.7, 0.7, 0.6) for i in range(4)])
        le = T("EXISTS", 40).move_to([-3.0, 1.6, 0])
        self.play(FadeIn(solid, shift=DOWN * 0.3), FadeIn(le), run_time=0.7)
        dashed = VGroup(*[DashedVMobject(Square(1.0, color=INK, stroke_width=4), num_dashes=16).move_to([1.6 + i * 1.4, -0.3, 0]) for i in range(3)])
        lw = T("WILL", 40).move_to([3.0, 1.6, 0])
        self.play(FadeIn(dashed), FadeIn(lw), run_time=0.6)
        mid_guard(self)
        q = T("?", 56).move_to([4.4, -0.3, 0])
        self.play(FadeIn(q), run_time=0.3)
        spark = Dot([4.4, 0.55, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        finish(self)
