"""
shader_kit.py: the Godot shader series' shared Manim helper kit (built 2026-10-14 in the Godot Shaders pilot build).
NOT imported: assemble_scenes.py pastes it at the top of scenes.py (Gate A copies only scenes.py).
Palette, pacing (narration is the clock), the midpoint guard, and the series' drawings: ramp strip, pixel grid, plot, vertex quad,
UV square, worker grid, code card. All in the Claude palette; terracotta only as dots, rings and small sparks, never as text.
Laws (BUILDER-BRIEF-COMMON.md section 6): Gate A needs at least one new non-text non-Rectangle shape after the first frame; the 45-55 % frame is a settled
still with the labels that matter; no ease_in_quad / ease_out_cubic (use ease_in); no .animate(path_arc=); stay inside +-6.2 x +-3.3; type >= 32
(act titles 40); no fill behind text; dark ink shapes packed together fuse into a text blob (draw bars and ramps as separate narrow tiles with gaps).
"""
from manim import *
import numpy as np
import json as _json, os as _os

STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
TEAL = "#5FA391"; LAB_STAGE = "#D9D5CA"; PALEBOX = "#FFFFFF"; GOLD = "#C9A227"
SERIF = "EB Garamond"
MONO = "Menlo"
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


def M(s, size=32, color=INK):
    """Monospace text for real code lines (Menlo). Size floor 32 at this frame. Pango may drop single spaces: LOOK at the still."""
    return Text(s, font=MONO, color=color, font_size=size)


def ease_in(t):
    """Quadratic ease-in. Local: Gate A's stub has no ease_in_quad."""
    return t * t


def dim_arrow(a, b, color=INK, w=5, tip=0.16):
    return DoubleArrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def arrow(a, b, color=INK, w=6, tip=0.22):
    """A single-headed arrow drawn as a shape (the '->' glyph is under the type floor)."""
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def box(x, y, w, h, color=INK, sw=4, fill=None, radius=0.12):
    """An outlined rounded box centred at (x, y). No fill behind text: leave fill=None when text sits inside."""
    r = RoundedRectangle(width=w, height=h, corner_radius=radius, stroke_color=color, stroke_width=sw)
    if fill:
        r.set_fill(fill, opacity=1)
    return r.move_to([x, y, 0])


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def sprite_icon(x, y, r=0.45):
    """The series' test sprite: a teal blob with two cream eyes (same as lab/runner.gd's sprite)."""
    body = Circle(radius=r, fill_color=TEAL, fill_opacity=1, stroke_width=0)
    e1 = Circle(radius=r * 0.12, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([-r * 0.33, r * 0.2, 0])
    e2 = Circle(radius=r * 0.12, fill_color=CARD, fill_opacity=1, stroke_width=0).move_to([r * 0.33, r * 0.2, 0])
    return VGroup(body, e1, e2).move_to([x, y, 0])


# ═════════════════════════════ the series' drawings ═════════════════════════════
RAMP_A = np.array([217, 212, 199]); RAMP_B = np.array([95, 163, 145])      # ghost -> teal: outside the 27-113 grey band GATE T reads as text


def _rgb(v):
    c = RAMP_A + (RAMP_B - RAMP_A) * v
    return "#%02x%02x%02x" % tuple(int(round(x)) for x in c)


def ramp_strip(width=6.0, label0="0", label1="1", n=56, height=0.32, y=0.0, x=0.0, labels=True):
    """THE signature object of the series: a ramp from 0 to 1, drawn as a row of narrow tiles WITH GAPS (a continuous strip of mid-dark greys is read by
    GATE T as a text-like run). Returns a VGroup: .tiles (VGroup), .x0, .x1 (scene x of the ends), .y, .labels (VGroup or empty)."""
    tw = width / n
    tiles = VGroup(*[Rectangle(width=tw * 0.82, height=height, fill_color=_rgb(i / (n - 1)), fill_opacity=1, stroke_width=0).move_to([x - width / 2 + tw * (i + 0.5), y, 0]) for i in range(n)])
    g = VGroup(tiles)
    g.tiles = tiles; g.x0 = x - width / 2; g.x1 = x + width / 2; g.y = y; g.width_s = width
    g.labels = VGroup()
    if labels:
        l0 = T(label0, 32).move_to([g.x0, y - height / 2 - 0.35, 0]); l1 = T(label1, 32).move_to([g.x1, y - height / 2 - 0.35, 0])
        g.labels = VGroup(l0, l1); g.add(g.labels)
    return g


def ramp_marker(strip, v, r=0.15):
    """A terracotta dot riding the ramp at value v (0..1), with a grey ring so it never reads as accent text."""
    d = Dot([strip.x0 + strip.width_s * v, strip.y, 0], radius=r, color=TERRA)
    d.set_stroke(DIM, width=3)
    return d


def pixel_grid(cols=12, rows=6, cell=0.42, x=0.0, y=0.0, color=DIM, sw=2):
    """A grid of OUTLINE-only cells (no fill behind anything). Returns VGroup with .cells (list of list [row][col] of Squares), .cell, .origin.
    highlight(grid, cells, color) -> list of animations that tint those cells."""
    cells = []
    g = VGroup()
    x0 = x - cols * cell / 2 + cell / 2; y0 = y + rows * cell / 2 - cell / 2
    for r in range(rows):
        row = []
        for c in range(cols):
            s = Square(side_length=cell * 0.94, stroke_color=color, stroke_width=sw).move_to([x0 + c * cell, y0 - r * cell, 0])
            row.append(s); g.add(s)
        cells.append(row)
    g.cells = cells; g.cell = cell; g.cols = cols; g.rows = rows; g.cx = x; g.cy = y
    return g


def cell_center(grid, c, r):
    return grid.cells[r][c].get_center()


def tint(cell, color, opacity=1.0):
    """Animation: fill an outline cell with a colour (use on cells that carry no text)."""
    return cell.animate.set_fill(color, opacity=opacity).set_stroke(color, width=2)


def plot(fn, x_range=(0, 1), y_range=(0, 1), size=(4.0, 2.4), x=0.0, y=0.0, color=INK, label_x="", label_y="", samples=80):
    """Axes + a curve + (via plot_dot) a travelling dot. No LaTeX: ticks are plain Text. Returns VGroup with .curve, .pt(xv) -> scene point, .axes."""
    w, h = size
    x0, y0 = x - w / 2, y - h / 2
    axes = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + h, 0], color=INK, stroke_width=5))

    def pt(xv):
        yv = fn(xv)
        return np.array([x0 + (xv - x_range[0]) / (x_range[1] - x_range[0]) * w, y0 + (yv - y_range[0]) / (y_range[1] - y_range[0]) * h, 0])
    xs = np.linspace(x_range[0], x_range[1], samples)
    curve = VMobject(stroke_color=color, stroke_width=7).set_points_smoothly([pt(v) for v in xs])
    g = VGroup(axes, curve)
    g.curve = curve; g.pt = pt; g.axes = axes
    if label_x:
        g.add(T(label_x, 32).move_to([x0 + w / 2, y0 - 0.4, 0]))
    if label_y:
        g.add(T(label_y, 32).move_to([x0 - 0.5, y0 + h / 2, 0]))
    return g


def vertex_quad(w=3.2, h=2.0, x=0.0, y=0.0, color=INK, corner_color=TERRA):
    """A rectangle with four terracotta corner dots (grey-ringed). Returns VGroup with .body (outline), .corners (list of 4 Dots, TL TR BR BL), .pts."""
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=5).move_to([x, y, 0])
    pts = [np.array([x - w / 2, y + h / 2, 0]), np.array([x + w / 2, y + h / 2, 0]), np.array([x + w / 2, y - h / 2, 0]), np.array([x - w / 2, y - h / 2, 0])]
    corners = [Dot(p, radius=0.16, color=corner_color).set_stroke(DIM, width=3) for p in pts]
    g = VGroup(body, *corners)
    g.body = body; g.corners = corners; g.pts = pts
    return g


def fill_in(grid, quad_group, color=TEAL):
    """Animations that tint every grid cell whose centre lies inside the quad (the GPU filling between the corners)."""
    xs = [p[0] for p in quad_group.pts]; ys = [p[1] for p in quad_group.pts]
    out = []
    for row in grid.cells:
        for s in row:
            c = s.get_center()
            if min(xs) <= c[0] <= max(xs) and min(ys) <= c[1] <= max(ys):
                out.append(tint(s, color, 0.9))
    return out


def uv_square(size=3.4, x=0.0, y=0.0):
    """A square with 0 to 1 axes, V pointing DOWN. Returns VGroup with .pt(u, v) -> scene point, .frame, .size, .labels."""
    x0, y0 = x - size / 2, y + size / 2          # (0,0) top-left
    frame = Square(side_length=size, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    ax = Arrow([x0, y0 + 0.5, 0], [x0 + size, y0 + 0.5, 0], buff=0, color=DIM, stroke_width=4, tip_length=0.2)
    ay = Arrow([x0 - 0.5, y0, 0], [x0 - 0.5, y0 - size, 0], buff=0, color=DIM, stroke_width=4, tip_length=0.2)
    g = VGroup(frame, ax, ay)
    g.frame = frame; g.size = size
    g.pt = lambda u, v: np.array([x0 + u * size, y0 - v * size, 0])
    g.labels = VGroup(T("0", 32).move_to([x0, y0 + 0.85, 0]), T("1", 32).move_to([x0 + size, y0 + 0.85, 0]),
                      T("0", 32).move_to([x0 - 0.95, y0, 0]), T("1", 32).move_to([x0 - 0.95, y0 - size, 0]))
    g.add(g.labels)
    return g


def worker_grid(rows=4, cols=10, x=0.0, y=0.0, gap=0.42, r=0.12, color=TEAL):
    """Many small workers: a grid of dots. Returns VGroup with .dots."""
    dots = VGroup(*[Dot([x + (c - (cols - 1) / 2) * gap, y + ((rows - 1) / 2 - rr) * gap, 0], radius=r, color=color) for rr in range(rows) for c in range(cols)])
    g = VGroup(dots); g.dots = dots
    return g


def worker_one(x=0.0, y=0.0, r=0.2, color=TEAL):
    """One fast worker: a single larger dot with two cream eyes."""
    return sprite_icon(x, y, r * 2)


def code_card(text, x=0.0, y=0.0, size=32, mark=None, pad=0.25):
    """A card of monospace code lines with EXPLICIT coordinates (Pango may drop single spaces: LOOK at the still). `mark` = list of 1-based lines to
    highlight with a terracotta bar at the left. Returns VGroup with .lines (list of Text), .frame, .bars (dict line->bar). Lines are left-aligned."""
    rows = text.split("\n")
    lh = size / 32 * 0.46
    ws = []
    lines = []
    for i, ln in enumerate(rows):
        t = M(ln.replace("\t", "    ") or " ", size)
        lines.append(t); ws.append(t.width)
    W = max(ws) + 2 * pad; H = len(rows) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4)
    frame.set_fill(PALEBOX, opacity=1)
    frame.move_to([x, y, 0])
    left = x - W / 2 + pad
    for i, t in enumerate(lines):
        t.move_to([left + t.width / 2, y + H / 2 - pad - lh * (i + 0.5), 0])
    g = VGroup(frame, *lines)
    g.lines = lines; g.frame = frame; g.bars = {}; g.W = W; g.H = H; g.lh = lh
    for k in (mark or []):
        bar = Rectangle(width=0.1, height=lh * 0.92, fill_color=TERRA, fill_opacity=1, stroke_width=0).move_to([x - W / 2 + 0.05, lines[k - 1].get_center()[1], 0])
        g.bars[k] = bar; g.add(bar)
    return g


def ring(mob, color=TERRA, pad=0.12, sw=7, backing=True):
    """A terracotta ring round a mobject, over a wider grey backing so it never reads as accent text. Returns VGroup(backing, ring)."""
    w, h = mob.width + 2 * pad, mob.height + 2 * pad
    r = RoundedRectangle(width=w, height=h, corner_radius=0.16, stroke_color=color, stroke_width=sw).move_to(mob.get_center())
    if not backing:
        return VGroup(r)
    b = RoundedRectangle(width=w + 0.1, height=h + 0.1, corner_radius=0.18, stroke_color=DIM, stroke_width=sw + 5, stroke_opacity=0.55).move_to(mob.get_center())
    return VGroup(b, r)

def lab_window(png, width=5.0, x=0.0, y=0.0, caption=""):
    """A real Lab PNG (path under the film folder, e.g. "pantry/pastel.png") as itself: the image, a grey frame just outside its edge and a one-line caption
    under it. Returns Group with .im, .fr, .cap (cap is None without a caption). Never draw over the picture."""
    im = ImageMobject(png)
    im.set_width(width)
    im.move_to([x, y, 0])
    fr = Rectangle(width=width + 0.1, height=im.height + 0.1, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
    cap = T(caption, 32).move_to([x, y - im.height / 2 - 0.4, 0]) if caption else None
    g = Group(im, fr) if cap is None else Group(im, fr, cap)
    g.im = im; g.fr = fr; g.cap = cap
    return g


def type_tag(text, x0, x1, y, size=32):
    """A small outlined tag under a span of a code line with a drawn bracket: the bracket runs from x0 to x1 at height y (just under the line), the tag
    hangs below its middle. Returns VGroup with .bracket, .tag (outlined box with the text). Text is ink on cream; the bracket is grey."""
    bracket = VGroup(Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=5), Line([x0, y, 0], [x0, y + 0.14, 0], color=DIM, stroke_width=5),
                     Line([x1, y, 0], [x1, y + 0.14, 0], color=DIM, stroke_width=5))
    t = T(text, size)
    tag = VGroup(RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1), t)
    tag.move_to([(x0 + x1) / 2, y - 0.5 - t.height / 2, 0])
    g = VGroup(bracket, tag)
    g.bracket = bracket; g.tag = tag
    return g

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
"""ACT I · Lights in 2D (Manim beats B02, B07, B08). Cast: the warm lamp (gold disc with grey rim), the floor as outlined tiles, the teal-free swatches.
Drawings only; the measured numbers in B07 are the film's FACTCHECK figures (0.5 x (0.2 + 0.4 + 0.4) = 0.5; 0 to 3 lamps: 0.1, 0.3, 0.5, 0.7)."""


def a1_lamp(x, y, r=0.34):
    """The lamp: a pale bulb disc with a grey rim (the series' lamp marker)."""
    return Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=GOLD, stroke_width=8).move_to([x, y, 0])


def a1_strip(cx, y, n=6, tw=0.8):
    """A short strip of outlined floor tiles; returns VGroup with .tops (top-centre of each tile)."""
    tiles = VGroup(*[Square(side_length=tw * 0.94, stroke_color=DIM, stroke_width=3).move_to([cx + (i - (n - 1) / 2) * tw, y, 0]) for i in range(n)])
    tiles.tops = [np.array([cx + (i - (n - 1) / 2) * tw, y + tw * 0.47, 0]) for i in range(n)]
    return tiles


class B02_TwoLights(Scene):
    def construct(self):
        LX, RX, SY = -3.4, 3.4, -1.3
        lt = T("point light", 40).move_to([LX, 3.0, 0]); rt = T("directional light", 40).move_to([RX, 3.0, 0])
        ls = a1_strip(LX, SY); rs = a1_strip(RX, SY)
        lamp = a1_lamp(LX, 1.4)
        sun = a1_lamp(RX - 1.9, 2.1, 0.5); sun.set_stroke(GOLD, width=8)
        cl = T("like a lamp", 32, DIM).move_to([LX, -2.55, 0]); cr = T("like the sun", 32, DIM).move_to([RX, -2.55, 0])
        self.wait(0.3)
        self.play(FadeIn(ls), FadeIn(rs), FadeIn(lt), FadeIn(rt), FadeIn(lamp), FadeIn(sun), run_time=0.8)
        until(self, "A point light")
        self.play(FadeIn(cl), run_time=0.4)
        fan = VGroup(*[Line(lamp.get_center() + np.array([0, -0.34, 0]), p, color=GOLD, stroke_width=5) for p in ls.tops])
        self.play(LaggedStart(*[Create(l) for l in fan], lag_ratio=0.12), run_time=1.5)
        until(self, "A directional light")
        par = VGroup(*[Line(p + np.array([-1.3, 2.2, 0]), p, color=GOLD, stroke_width=5) for p in rs.tops])
        self.play(FadeIn(cr), run_time=0.4)
        self.play(LaggedStart(*[Create(l) for l in par], lag_ratio=0.12), run_time=1.5)
        until(self, "This film works")
        self.play(FadeIn(ring(lamp, pad=0.1)), run_time=0.6)
        done(self)


def a1_sw(v, x, y, label, num, s=1.0):
    """A swatch box (outline, filled with the grey of its number; no text inside) with its word and number under it."""
    g = 114 + int(round(141 * v))
    col = "#%02x%02x%02x" % (g, g, g)
    b = Square(side_length=s, stroke_color=DIM, stroke_width=4).set_fill(col, opacity=1).move_to([x, y, 0])
    w = T(label, 32).move_to([x, y - s / 2 - 0.35, 0]); n = T(num, 32).move_to([x, y - s / 2 - 0.8, 0])
    return b, VGroup(w, n)


class B07_Formula(Scene):
    def construct(self):
        Y = 0.7
        surf, surf_l = a1_sw(0.5, -5.6, Y, "surface", "0.5")
        amb, amb_l = a1_sw(0.2, -2.9, Y, "ambient", "0.2")
        l1, l1_l = a1_sw(0.4, -0.7, Y, "lamp", "0.4")
        l2, l2_l = a1_sw(0.4, 1.5, Y, "lamp", "0.4")
        pix_box = Square(side_length=1.0, stroke_color=DIM, stroke_width=4).move_to([4.9, Y, 0])
        pix_l = VGroup(T("pixel", 32).move_to([4.9, Y - 0.85, 0]), T("0.5", 32).move_to([4.9, Y - 1.3, 0]))
        ops = VGroup(T("x", 40).move_to([-4.55, Y, 0]), T("(", 64).move_to([-3.95, Y, 0]), T("+", 48).move_to([-1.8, Y, 0]),
                     T("+", 48).move_to([0.4, Y, 0]), T(")", 64).move_to([2.45, Y, 0]), T("=", 48).move_to([3.4, Y, 0]))
        self.wait(0.3)
        until(self, "The pixel is the surface")
        self.play(FadeIn(surf), FadeIn(surf_l), FadeIn(ops[0]), FadeIn(ops[1]), FadeIn(ops[4]), FadeIn(ops[5]), FadeIn(pix_box), FadeIn(pix_l[0]), run_time=0.7)
        until(self, "the ambient")
        self.play(FadeIn(amb), FadeIn(amb_l), run_time=0.5)
        until(self, "two lamps of")
        self.add(ops[2])
        l1.shift(UP * 1.2); l1_l.shift(UP * 1.2)
        self.add(l1, l1_l)
        self.play(l1.animate.shift(DOWN * 1.2), l1_l.animate.shift(DOWN * 1.2), run_time=0.6)
        self.play(FadeIn(ops[3]), run_time=0.2)
        l2.shift(UP * 1.2); l2_l.shift(UP * 1.2)
        self.add(l2, l2_l)
        self.play(l2.animate.shift(DOWN * 1.2), l2_l.animate.shift(DOWN * 1.2), run_time=0.6)
        until(self, "the pixel reads", lead=0.9)
        fillr = Rectangle(width=0.94, height=0.02, fill_color="#%02x%02x%02x" % (114 + 70, 114 + 70, 114 + 70), fill_opacity=1, stroke_width=0).move_to([4.9, Y - 0.47 + 0.01, 0])
        self.add(fillr)
        self.play(fillr.animate.stretch_to_fit_height(0.94).move_to([4.9, Y, 0]), run_time=0.7)
        self.play(FadeIn(pix_l[1]), run_time=0.3)
        c1 = T("measured · Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -2.25, 0])
        c2 = T("0, 1, 2, 3 lamps: 0.1, 0.3, 0.5, 0.7", 32, DIM).move_to([0, -2.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        done(self)


class B08_PerLamp(Scene):
    def construct(self):
        names = ["vertex()  corners", "fragment()  pixels", "light()  lamps"]
        hb = [box(x, 2.55, 3.8, 0.85, DIM, 4, fill=PALEBOX) for x in (-4.2, 0.0, 4.2)]
        ht = [T(n, 32).move_to(b.get_center()) for n, b in zip(names, hb)]
        floor = VGroup(*[Square(side_length=0.94, stroke_color=DIM, stroke_width=3).move_to([(i - 2) * 1.0, -1.3, 0]) for i in range(5) if i != 2])
        cell = Square(side_length=1.0, stroke_color=INK, stroke_width=6).move_to([0, -1.3, 0])
        celllab = T("pixel", 32).move_to([0, -2.1, 0])
        lampL = a1_lamp(-4.9, 0.4); lampR = a1_lamp(4.9, 0.4)
        cap = T("light(): once per pixel, for each light that touches it", 32).move_to([0, -3.0, 0])
        self.wait(0.3)
        until(self, "A two-D shader")
        self.play(*[Create(b) for b in hb], *[FadeIn(t) for t in ht], run_time=0.9)
        self.play(FadeIn(floor), FadeIn(cell), FadeIn(celllab), FadeIn(lampL), FadeIn(lampR), run_time=0.7)
        until(self, "The third")
        rg = VGroup(Rectangle(width=3.8, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).next_to(hb[2], DOWN, buff=0.1), Rectangle(width=3.8, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).next_to(hb[2], DOWN, buff=0.14))  # terracotta underline bar over a grey backing (a bar, never text)
        self.play(FadeIn(rg), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.5)
        until(self, "and every light")
        aL = arrow(lampL.get_center() + np.array([0.4, -0.1, 0]), np.array([-0.55, -0.85, 0]), INK, 6)
        aR = arrow(lampR.get_center() + np.array([-0.4, -0.1, 0]), np.array([0.55, -0.85, 0]), INK, 6)
        bL = box(-2.55, -0.15, 1.5, 0.62, INK, 3, fill=PALEBOX); bR = box(2.55, -0.15, 1.5, 0.62, INK, 3, fill=PALEBOX)
        tL = T("light()", 32).move_to(bL); tR = T("light()", 32).move_to(bR)
        self.play(Create(aL), Create(aR), run_time=0.8)
        self.play(FadeIn(bL), FadeIn(tL), FadeIn(bR), FadeIn(tR), run_time=0.4)
        until(self, "how much does", lead=0.5)
        sw1 = Square(side_length=0.36, stroke_color=DIM, stroke_width=2).set_fill(_rgb(0.45), opacity=1).move_to(bL.get_center() + DOWN * 0.7)
        self.play(FadeIn(sw1), run_time=0.15)
        self.play(sw1.animate.move_to([-0.2, -1.3, 0]), run_time=0.5)
        sw2 = Square(side_length=0.36, stroke_color=DIM, stroke_width=2).set_fill(_rgb(0.45), opacity=1).move_to(bR.get_center() + DOWN * 0.7)
        self.play(FadeIn(sw2), run_time=0.15)
        self.play(sw2.animate.move_to([0.2, -1.3, 0]), run_time=0.5)
        self.play(sw1.animate.set_fill(_rgb(1.0)), sw2.animate.set_fill(_rgb(1.0)), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · The Light Function  (B11, B12: Manim)

Cast for the act: the lamp is a gold dot with a grey ring (a2_lamp); an answer from one lamp is a small ramp-coloured swatch (a2_swatch);
built-ins are Menlo capitals; arrows are shapes pointing only forward. Pictures are drawings and labelled as such by their plain words.
"""


def a2_lamp(x, y, r=0.2):
    d = Dot([x, y, 0], radius=r, color=GOLD)
    d.set_stroke(DIM, width=3)
    return d


def a2_swatch(x, y, v, s=0.5):
    """A small square of the ramp colour for value v (an answer from one lamp)."""
    return Square(side_length=s, fill_color=_rgb(v), fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])


def a2_input(name, y, x0=-6.1, x1=-1.95):
    """An input arrow into the function box with its monospace label above the shaft."""
    a = arrow([x0, y, 0], [x1, y, 0], w=6)
    lab = M(name, 32).move_to([x0 + 0.1, y + 0.36, 0])
    lab.move_to([x0 + lab.width / 2 + 0.1, y + 0.36, 0])
    return VGroup(a, lab)


class B11_FunctionBox(Scene):
    def construct(self):
        fb = box(0.0, 0.55, 3.6, 3.5, color=INK, sw=5)
        fl = M("light()", 32).move_to([0.0, 0.55, 0])
        self.play(Create(fb), FadeIn(fl), run_time=0.8)
        names = ["COLOR", "UV", "LIGHT_COLOR", "LIGHT_ENERGY"]
        ys = [1.85, 1.0, 0.15, -0.7]
        ins = [a2_input(n, y) for n, y in zip(names, ys)]
        until(self, "Color is")
        self.play(FadeIn(ins[0], shift=RIGHT * 0.7), run_time=0.7)
        until(self, "U V is")
        self.play(FadeIn(ins[1], shift=RIGHT * 0.7), run_time=0.7)
        until(self, "Light color and")
        self.play(FadeIn(ins[2], shift=RIGHT * 0.7), run_time=0.6)
        until(self, "light energy describe")
        self.play(FadeIn(ins[3], shift=RIGHT * 0.7), run_time=0.6)
        cap = VGroup(T("built-in: a value the engine hands to a function,", 32), T("or collects from it", 32)).arrange(DOWN, buff=0.12).move_to([0, -2.0, 0])
        note = T("more in the docs: NORMAL, SCREEN_UV ...", 32, DIM).move_to([0, -3.0, 0])
        until(self, "values written")
        self.play(FadeIn(cap), run_time=0.6)
        self.play(FadeIn(note), run_time=0.5)
        until(self, "You hand back")
        out = arrow([1.8, 0.55, 0], [4.2, 0.55, 0], w=7)
        tip = Dot([4.2, 0.55, 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        ol = M("LIGHT", 32).move_to([5.3, 0.55, 0])
        self.play(GrowArrow(out), FadeIn(tip), run_time=0.8)
        self.play(FadeIn(ol), run_time=0.4)
        done(self)


class B12_Order(Scene):
    def construct(self):
        frag = box(-4.6, 0.0, 2.8, 1.3, DIM, 5, fill=PALEBOX)
        fl = M("fragment()", 32).move_to([-4.6, 0.0, 0])
        fs = T("sets color", 32).move_to([-4.6, -1.05, 0])
        lit = box(-1.2, 0.0, 2.6, 1.3, DIM, 5, fill=PALEBOX)
        ll = M("light()", 32).move_to([-1.2, 0.0, 0])
        amb = box(2.5, 0.0, 3.2, 1.6, DIM, 5, fill=PALEBOX)
        al = T("+ ambient look", 32).move_to([2.5, 0.3, 0])
        pix = Square(side_length=1.1, stroke_color=INK, stroke_width=5).move_to([5.5, 0.0, 0])
        a1 = arrow([-3.2, 0, 0], [-2.5, 0, 0], w=6, tip=0.2)
        a2 = arrow([0.1, 0, 0], [0.9, 0, 0], w=6, tip=0.2)
        a3 = arrow([4.1, 0, 0], [4.9, 0, 0], w=6, tip=0.2)
        strip = VGroup(frag, fl, fs, lit, ll, amb, al, pix, a1, a2, a3)
        self.play(FadeIn(strip), run_time=0.8)
        until(self, "Fragment runs first")
        tok = Dot([-6.15, 0, 0], radius=0.17, color=TEAL).set_stroke(DIM, width=3)
        self.play(FadeIn(tok), run_time=0.3)
        self.play(tok.animate.move_to([-2.45, 0, 0]), run_time=1.5, rate_func=linear)
        until(self, "once for each lamp")
        l1, l2 = a2_lamp(-1.9, 2.0), a2_lamp(-0.5, 2.0)
        lt = T("per lamp", 32).move_to([-1.2, 2.75, 0])
        d1 = arrow([-1.9, 1.75, 0], [-1.9, 0.7, 0], w=5, tip=0.18)
        d2 = arrow([-0.5, 1.75, 0], [-0.5, 0.7, 0], w=5, tip=0.18)
        self.play(FadeIn(VGroup(l1, l2, lt)), GrowArrow(d1), GrowArrow(d2), run_time=0.8)
        s1, s2 = a2_swatch(-1.9, -1.55, 0.3), a2_swatch(-0.5, -1.55, 0.45)
        e1 = arrow([-1.9, -0.7, 0], [-1.9, -1.2, 0], w=5, tip=0.16)
        e2 = arrow([-0.5, -0.7, 0], [-0.5, -1.2, 0], w=5, tip=0.16)
        k1 = Dot([-1.9, -0.7, 0], radius=0.17, color=TEAL).set_stroke(DIM, width=3)
        k2 = Dot([-0.5, -0.7, 0], radius=0.17, color=TEAL).set_stroke(DIM, width=3)
        self.play(FadeOut(tok), FadeIn(k1), FadeIn(k2), run_time=0.5)
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(s1), FadeIn(s2), FadeOut(k1), FadeOut(k2), run_time=0.8)
        until(self, "adds all the answers")
        self.play(s1.animate.move_to([1.9, -1.55, 0]), s2.animate.move_to([3.1, -1.55, 0]), FadeOut(VGroup(e1, e2)), run_time=0.9)
        self.play(s1.animate.move_to([1.9, -0.28, 0]).scale(0.7), s2.animate.move_to([3.1, -0.28, 0]).scale(0.7), run_time=0.8)
        until(self, "That sum is")
        self.play(pix.animate.set_fill(_rgb(0.7), opacity=1), run_time=0.9)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · Which Way Is the Light?  (B19, B23: Manim)

Cast: the lamp is a gold dot with a grey ring; pixel dots are teal; a unit arrow is an ink arrow of one fixed length (a3_unit);
terracotta only as rings and small dots. Screen orientation throughout (y up here is the picture's up).
"""


def a3_lamp(x, y, r=0.24):
    d = Dot([x, y, 0], radius=r, color=GOLD)
    d.set_stroke(DIM, width=3)
    return d


def a3_pix(x, y, r=0.13):
    return Dot([x, y, 0], radius=r, color=TEAL)


def a3_unit(p, toward, length=0.8, gap=0.2):
    """A unit arrow of fixed drawn length starting just off the pixel dot p and pointing toward the point `toward`."""
    p = np.array(p, dtype=float); q = np.array(toward, dtype=float)
    u = (q - p) / np.linalg.norm(q - p)
    return arrow(p + u * gap, p + u * (gap + length), w=6, tip=0.2)


class B19_Arrows(Scene):
    def construct(self):
        title = T("Which Way Is the Light?", 40)
        title.move_to([-6.1 + title.width / 2, 3.0, 0])
        cx, cy, R = -1.5, -0.25, 1.55
        grid = pixel_grid(cols=12, rows=7, cell=0.55, x=cx, y=cy, color=GHOST, sw=2)
        lamp = a3_lamp(cx, cy)
        angs = [0, 45, 90, 135, 180, 225, 270, 315]
        pts = [np.array([cx + R * np.cos(np.radians(a)), cy + R * np.sin(np.radians(a)), 0]) for a in angs]
        dots = [a3_pix(*p[:2]) for p in pts]
        self.play(FadeIn(title), FadeIn(grid), FadeIn(lamp), FadeIn(VGroup(*dots)), run_time=0.9)
        until(self, "Light direction is a vector")
        lab = M("LIGHT_DIRECTION", 32).move_to([4.35, 1.2, 0])
        ln = T("length 1", 32).move_to([4.35, 0.55, 0])
        cap = T("vector: a bundle of two to four numbers", 32).move_to([0.0, -2.95, 0])
        self.play(FadeIn(lab), FadeIn(ln), FadeIn(cap), run_time=0.6)
        until(self, "an arrow from this pixel")
        arrs = [a3_unit(p, [cx, cy, 0]) for p in pts]
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.12), run_time=1.6)
        until(self, "A pixel left")
        rl = ring(VGroup(dots[4], arrs[4]))
        tag = T("points right", 32).move_to([4.35, -0.2, 0])
        self.play(FadeIn(rl), FadeIn(tag), run_time=0.5)
        until(self, "A pixel above")
        rt = ring(VGroup(dots[2], arrs[2]))
        tag2 = T("points down", 32).move_to([4.35, -0.2, 0])
        self.play(FadeOut(rl), FadeIn(rt), FadeOut(tag), FadeIn(tag2), run_time=0.6)
        done(self)


class B23_Sun(Scene):
    def construct(self):
        xs = [-2.2, -1.1, 0.0, 1.1, 2.2]
        div = Line([0, 2.3, 0], [0, -2.4, 0], color=GHOST, stroke_width=4)
        lx, sx = -3.3, 3.3
        lamp = a3_lamp(lx, 1.5)
        lp = [np.array([lx + dx, -0.4, 0]) for dx in xs]
        ld = [a3_pix(*p[:2]) for p in lp]
        la = [a3_unit(p, [lx, 1.5, 0]) for p in lp]
        cap1 = VGroup(T("point light:", 32), T("a different arrow per pixel", 32)).arrange(DOWN, buff=0.1).move_to([lx, -1.45, 0])
        self.play(Create(div), FadeIn(lamp), FadeIn(VGroup(*ld)), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(a) for a in la], lag_ratio=0.2), FadeIn(cap1), run_time=1.0)
        # the sun: a disc with short rays
        sun = Circle(radius=0.42, fill_color=GOLD, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([sx, 1.6, 0])
        rays = VGroup(*[Line([sx + 0.6 * np.cos(np.radians(a)), 1.6 + 0.6 * np.sin(np.radians(a)), 0], [sx + 0.85 * np.cos(np.radians(a)), 1.6 + 0.85 * np.sin(np.radians(a)), 0], color=GOLD, stroke_width=5) for a in range(0, 360, 45)])
        rp = [np.array([sx + dx, -0.4, 0]) for dx in xs]
        rd = [a3_pix(*p[:2]) for p in rp]
        ra = [arrow(p + np.array([0, 0.2, 0]), p + np.array([0, 1.0, 0]), w=6, tip=0.2) for p in rp]
        until(self, "A directional light is different")
        self.play(FadeIn(VGroup(sun, rays)), FadeIn(VGroup(*rd)), run_time=0.6)
        until(self, "Its arrow is the same")
        self.play(LaggedStart(*[GrowArrow(a) for a in ra], lag_ratio=0.25), run_time=1.5)
        cap2 = VGroup(T("directional light:", 32), T("the same arrow everywhere", 32)).arrange(DOWN, buff=0.1).move_to([sx, -1.45, 0])
        self.play(FadeIn(cap2), run_time=0.5)
        until(self, "and its position")
        note = T("its position is always (0, 0, 0) · Godot docs", 32, DIM).move_to([0, -2.95, 0])
        self.play(FadeIn(note), run_time=0.6)
        until(self, "So a direction mask")
        al = T("all or nothing", 32).move_to([sx, 2.75, 0])
        self.play(FadeIn(al), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · A Lighthouse (Manim beats B24, B25). Cast: the unit circle and the two arrows. Screen orientation: the vertical axis points DOWN,
so an angle `a` clockwise from right puts the arrow tip at (cos a, -sin a) in Manim's y-up frame. Drawings; the angle values are the lane's."""


def a4_tip(c, L, deg):
    r = np.radians(deg)
    return np.array([c[0] + L * np.cos(r), c[1] - L * np.sin(r), 0])


class B24_AimArrow(Scene):
    def construct(self):
        C = np.array([0.6, -0.3, 0.0]); R = 2.0
        title = T("A Lighthouse", 40).move_to([-6.1 + 1.3, 3.0, 0])
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(C)
        hline = Line(C + np.array([-R - 0.3, 0, 0]), C + np.array([R + 0.3, 0, 0]), color=GHOST, stroke_width=4)
        yax = arrow([-3.9, 1.3, 0], [-3.9, -1.6, 0], DIM, 5)
        ylab = T("y points down", 32).move_to([-4.2, -2.15, 0])
        ylab.set_x(-3.9)
        a = ValueTracker(20.0)
        def tip(): return a4_tip(C, R, a.get_value())
        arr = always_redraw(lambda: Arrow(C, tip(), buff=0, color=INK, stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.3))
        hseg = always_redraw(lambda: Line(C, [tip()[0], C[1], 0], color=DIM, stroke_width=9))
        vseg = always_redraw(lambda: Line([tip()[0], C[1], 0], tip(), color=DIM, stroke_width=9))
        arc = always_redraw(lambda: Arc(radius=0.7, start_angle=0, angle=-np.radians(a.get_value()), arc_center=C, color=INK, stroke_width=5))
        dot = always_redraw(lambda: Dot(tip(), radius=0.14, color=TERRA).set_stroke(DIM, width=3))
        lab = T("(cos a, sin a)", 32).move_to([4.4, 1.3, 0])
        cl = always_redraw(lambda: T("cos", 32, DIM).move_to([(C[0] + tip()[0]) / 2, C[1] + 0.4 if tip()[1] < C[1] else C[1] + 0.4, 0]))
        sl = always_redraw(lambda: T("sin", 32, DIM).move_to([tip()[0] + 0.55, (C[1] + tip()[1]) / 2, 0]))
        self.wait(0.3)
        self.play(FadeIn(title), Create(circ), FadeIn(hline), Create(yax), FadeIn(ylab), run_time=1.0)
        until(self, "Cosine and sine")
        self.add(arr, hseg, vseg, arc, dot)
        self.play(FadeIn(lab), FadeIn(cl), FadeIn(sl), run_time=0.6)
        self.wait(0.5)
        until(self, "Turn the angle")
        self.play(a.animate.set_value(85.0), run_time=2.2, rate_func=smooth)
        done(self)


class B25_Agree(Scene):
    def construct(self):
        P = np.array([-3.4, 0.9, 0.0]); L = 2.4; PIX = 25.0
        aim = ValueTracker(-40.0)
        pixarr = Arrow(P, a4_tip(P, L, PIX), buff=0, color=DIM, stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.3)
        pixlab = T("pixel arrow", 32, DIM).move_to([P[0] - 1.3, P[1] + 0.55, 0])
        aimarr = always_redraw(lambda: Arrow(P, a4_tip(P, L, aim.get_value()), buff=0, color=INK, stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.3))
        aimdot = always_redraw(lambda: Dot(a4_tip(P, L, aim.get_value()), radius=0.14, color=TERRA).set_stroke(DIM, width=3))
        aimlab = always_redraw(lambda: T("aim", 32).move_to(a4_tip(P, L + 0.45, aim.get_value()) + np.array([0.45, 0.45, 0])))
        def dv(): return float(np.cos(np.radians(aim.get_value() - PIX)))
        def kept(): return dv() >= 0.95
        sector = always_redraw(lambda: Sector(radius=1.7, start_angle=-np.radians(PIX), angle=-np.radians(aim.get_value() - PIX), arc_center=P, fill_color=TEAL, fill_opacity=0.65, stroke_width=0)
                               if kept() and abs(aim.get_value() - PIX) > 0.5 else Sector(radius=1.7, start_angle=-np.radians(PIX), angle=0.0001, arc_center=P, fill_opacity=0, stroke_width=0))
        keptlab = always_redraw(lambda: T("kept", 32).move_to([P[0] + 0.9, P[1] - 1.55, 0]) if kept() else T("", 32).move_to([P[0] + 0.9, P[1] - 1.55, 0]))
        BX0, BX1, BY = 1.2, 5.8, 0.2
        def bx(v): return BX0 + (v + 1) / 2 * (BX1 - BX0)
        track = Line([BX0, BY, 0], [BX1, BY, 0], color=DIM, stroke_width=6)
        ticks = VGroup(*[Line([bx(v), BY - 0.15, 0], [bx(v), BY + 0.15, 0], color=DIM, stroke_width=5) for v in (-1, 0, 1)])
        tl = VGroup(*[T(s, 32).move_to([bx(v), BY - 0.5, 0]) for s, v in (("-1", -1), ("0", 0), ("1", 1))])
        t95 = Line([bx(0.95), BY - 0.3, 0], [bx(0.95), BY + 0.3, 0], color=INK, stroke_width=6)
        t95l = T("0.95", 32).move_to([bx(0.95) - 0.1, BY + 0.65, 0])
        mark = always_redraw(lambda: Dot([bx(dv()), BY, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3))
        dlab = T("dot =", 48).move_to([2.7, 1.9, 0])
        num = always_redraw(lambda: T("%.2f" % dv(), 48).move_to([3.6 + 0.0, 1.9, 0]).align_to([3.55, 0, 0], LEFT))
        cap1 = T("dot(a, b): multiply the matching parts and add them;", 32).move_to([0, -2.55, 0])
        cap2 = T("with a unit direction, how far a point lies along it", 32).move_to([0, -3.0, 0])
        self.wait(0.3)
        self.play(Create(pixarr), FadeIn(pixlab), FadeIn(track), FadeIn(ticks), FadeIn(tl), FadeIn(t95), FadeIn(t95l), FadeIn(dlab), run_time=0.9)
        self.add(aimarr, aimdot, aimlab, mark, num, sector, keptlab)
        self.play(FadeIn(cap1), FadeIn(cap2), run_time=0.5)
        until(self, "It is one when")
        self.play(aim.animate.set_value(PIX), run_time=2.0, rate_func=smooth)
        until(self, "zero at right angles")
        self.play(aim.animate.set_value(90.0), run_time=1.9, rate_func=smooth)
        until(self, "Keep the pixels")
        self.play(aim.animate.set_value(PIX + 4), run_time=1.5, rate_func=smooth)
        self.play(FadeIn(ring(t95l, pad=0.08)), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Where Is the Light?  (B31, B32, B34: Manim)

Cast: the window frame (a 1920 x 1080 window drawn at 0.00375 units per pixel, origin dot at the top left, y axis pointing DOWN), the gold lamp dot,
the terracotta pixel dot, the ring. Screen-space numbers are window pixels: (960, 540) lamp, (1130, 640) pixel (measured, verify2 P/V, verify6).
"""


def a5_lamp(x, y, r=0.2):
    d = Dot([x, y, 0], radius=r, color=GOLD)
    d.set_stroke(DIM, width=3)
    return d


def a5_pixdot(x, y, r=0.16):
    d = Dot([x, y, 0], radius=r, color=TERRA)
    d.set_stroke(DIM, width=3)
    return d


def a5_put(t, anchor, side):
    """Place text t so its left ('l'), right ('r') or centre ('c') edge sits at anchor (x, y)."""
    w = t.width / 2.0
    dx = {"l": w, "r": -w, "c": 0.0}[side]
    return t.move_to([anchor[0] + dx, anchor[1], 0])


def a5_count(fmt, a, b, anchor, side):
    """UpdateFromAlphaFunc helper: replace a label by fmt(value) counting from a to b, edge-aligned at anchor."""
    def f(m, al):
        v = int(round(a + (b - a) * al))
        m.become(a5_put(T(fmt(v), 32, DIM), anchor, side))
    return f


class B31_ScreenSpace(Scene):
    def construct(self):
        title = T("Where Is the Light?", 40)
        title.move_to([-6.1 + title.width / 2, 3.1, 0])
        sc = 0.0042
        W, H = 1920 * sc, 1080 * sc
        wx, wy = -1.0, -0.3
        ox, oy = wx - W / 2, wy + H / 2          # window top-left in the scene
        P = lambda px, py: np.array([ox + px * sc, oy - py * sc, 0])
        win = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=5).move_to([wx, wy, 0])
        origin = Dot(P(0, 0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        o_lab = T("(0, 0)", 32).move_to(P(0, 0) + np.array([0.85, -0.4, 0]))
        xa = arrow([ox, oy + 0.4, 0], [ox + W + 0.2, oy + 0.4, 0], color=DIM, w=5)
        ya = arrow([ox - 0.4, oy, 0], [ox - 0.4, oy - H - 0.2, 0], color=DIM, w=5)
        xl = T("x", 32).move_to([ox + W + 0.5, oy + 0.4, 0])
        yl = T("y", 32).move_to([ox - 0.4, oy - H - 0.55, 0])
        self.play(FadeIn(title), Create(win), run_time=0.9)
        self.play(FadeIn(origin), FadeIn(o_lab), GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl), run_time=0.8)
        # lamp
        until(self, "Light position")
        LP, PP = P(960, 540), P(1130, 640)
        lamp = a5_lamp(*LP[:2])
        la_n = LP[:2] + np.array([-0.35, 0.28]); la_c = LP[:2] + np.array([-0.35, -0.22])
        l_name = a5_put(M("LIGHT_POSITION", 32), la_n, "r")
        l_xy = a5_put(T("(0, 0)", 32, DIM), la_c, "r")
        hz = DashedLine(P(0, 0), P(960, 0), color=DIM, stroke_width=4)
        vt = DashedLine(P(960, 0), P(960, 540), color=DIM, stroke_width=4)
        self.play(FadeOut(o_lab), FadeIn(l_name), FadeIn(l_xy), run_time=0.4)
        self.play(Create(hz), UpdateFromAlphaFunc(l_xy, a5_count(lambda v: "(%d, 0)" % v, 0, 960, la_c, "r")), run_time=0.6)
        self.play(Create(vt), FadeIn(lamp), UpdateFromAlphaFunc(l_xy, a5_count(lambda v: "(960, %d)" % v, 0, 540, la_c, "r")), run_time=0.6)
        # pixel
        until(self, "light vertex")
        pix = a5_pixdot(*PP[:2])
        pn = PP[:2] + np.array([-0.2, -0.6]); pc = PP[:2] + np.array([-0.2, -1.05])
        p_name = a5_put(M("LIGHT_VERTEX", 32), pn, "l")
        p_xy = a5_put(T("(0, 0)", 32, DIM), pc, "l")
        hz2 = DashedLine(P(0, 0), P(1130, 0), color=DIM, stroke_width=4)
        vt2 = DashedLine(P(1130, 0), P(1130, 640), color=DIM, stroke_width=4)
        self.play(hz.animate.set_opacity(0.3), vt.animate.set_opacity(0.3), FadeIn(p_name), FadeIn(p_xy), run_time=0.4)
        self.play(Create(hz2), UpdateFromAlphaFunc(p_xy, a5_count(lambda v: "(%d, 0)" % v, 0, 1130, pc, "l")), run_time=0.5)
        self.play(Create(vt2), FadeIn(pix), UpdateFromAlphaFunc(p_xy, a5_count(lambda v: "(1130, %d)" % v, 0, 640, pc, "l")), run_time=0.5)
        note = T("window 1920 x 1080", 32, DIM).move_to([4.5, 3.1, 0])
        until(self, "Both are in screen space")
        cap = T("screen space: pixels of the window, from the top left", 32).move_to([0.0, -3.0, 0])
        self.play(FadeIn(cap), FadeIn(note), run_time=0.7)
        done(self)


class B32_Subtract(Scene):
    def construct(self):
        # small window with the two dots, and a loupe that enlarges the neighbourhood
        sc = 0.0027
        W, H = 1920 * sc, 1080 * sc
        wx, wy = -3.4, 0.2
        ox, oy = wx - W / 2, wy + H / 2
        P = lambda px, py: np.array([ox + px * sc, oy - py * sc, 0])
        win = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=5).move_to([wx, wy, 0])
        og = Dot(P(0, 0), radius=0.1, color=TERRA).set_stroke(DIM, width=3)
        sl, sp = a5_lamp(*P(960, 540)[:2], r=0.1), a5_pixdot(*P(1130, 640)[:2], r=0.1)
        cx0 = (P(960, 540)[0] + P(1130, 640)[0]) / 2; cy0 = (P(960, 540)[1] + P(1130, 640)[1]) / 2
        zb = Rectangle(width=0.9, height=0.7, stroke_color=DIM, stroke_width=4).move_to([cx0, cy0, 0])
        # the enlarged panel
        k = 5.0
        px, py = 3.7, 0.3
        panel = Rectangle(width=5.0, height=3.9, stroke_color=DIM, stroke_width=4).move_to([px, py, 0])
        Lp = np.array([2.0, 1.2, 0])
        Pp = Lp + np.array([170 * sc * k, -100 * sc * k, 0])
        ll = a5_lamp(*Lp[:2], r=0.2)
        pl = a5_pixdot(*Pp[:2], r=0.2)
        l_t = T("lamp", 32).move_to(Lp + np.array([0.0, 0.55, 0]))
        z_t = T("zoomed in", 32, DIM).move_to([px, py - 2.3, 0])
        c1 = Line(zb.get_corner(UR), panel.get_corner(UL), color=GHOST, stroke_width=3)
        c2 = Line(zb.get_corner(DR), panel.get_corner(DL), color=GHOST, stroke_width=3)
        self.play(Create(win), FadeIn(og), run_time=0.6)
        self.play(FadeIn(sl), FadeIn(sp), Create(zb), Create(c1), Create(c2), Create(panel), run_time=0.8)
        self.play(FadeIn(ll), FadeIn(pl), FadeIn(l_t), FadeIn(z_t), run_time=0.5)
        # the arrow lamp -> pixel
        until(self, "Subtract")
        u = (Pp - Lp) / np.linalg.norm(Pp - Lp)
        ar = arrow(Lp + u * 0.28, Pp - u * 0.3, w=7, tip=0.24)
        self.play(GrowArrow(ar), run_time=1.6)
        lab = T("pixel - lamp", 32).move_to((Lp + Pp) / 2 + np.array([0.55, 0.6, 0]))
        until(self, "an arrow from the lamp")
        self.play(FadeIn(lab), run_time=0.5)
        off = T("(170, 100)", 32, DIM).move_to(Pp + np.array([0.75, 0.55, 0]))
        self.play(FadeIn(off), run_time=0.4)
        # dimension line (below-left of the arrow) with a counting label
        until(self, "Its length")
        nrm = np.array([-u[1], u[0], 0])
        if nrm[1] > 0:
            nrm = -nrm
        o = nrm * 0.55
        a0, a1 = Lp + o, Pp + o
        dl = Line(a0, a1, color=INK, stroke_width=5)
        t0 = Line(a0 - nrm * 0.12, a0 + nrm * 0.12, color=INK, stroke_width=5)
        t1 = Line(a1 - nrm * 0.12, a1 + nrm * 0.12, color=INK, stroke_width=5)
        mid = (a0 + a1) / 2 + nrm * 1.2 + np.array([0.4, 0, 0])
        cnt = T("length 0 px", 32).move_to(mid)
        self.play(Create(dl), FadeIn(t0), FadeIn(t1), run_time=0.5)
        self.play(UpdateFromAlphaFunc(cnt, lambda m, al: m.become(T("length %d px" % int(round(197 * al)), 32).move_to(mid))), run_time=1.1)
        until(self, "That is what the length")
        cap = T("length(v): the length of a vector; of an offset, the distance", 32).move_to([0.0, -3.0, 0])
        self.play(FadeIn(cap), run_time=0.6)
        done(self)


class B34_RingFromSteps(Scene):
    def construct(self):
        sc = 0.0045
        cx, cy = -2.0, -0.1
        r1, r2, RG = 390 * sc, 450 * sc, 2.6
        gframe = Circle(radius=RG, stroke_color=GHOST, stroke_width=4).move_to([cx, cy, 0])
        gframe.set_z_index(3)
        c1 = Circle(radius=r1, stroke_color=TEAL, stroke_width=6).move_to([cx, cy, 0]); c1.set_z_index(4)
        c2 = Circle(radius=r2, stroke_color=INK, stroke_width=6).move_to([cx, cy, 0]); c2.set_z_index(4)
        lamp = Dot([cx, cy, 0], radius=0.2, color=GOLD).set_stroke(DIM, width=3); lamp.set_z_index(5)
        chip1 = VGroup(RoundedRectangle(width=3.7, height=0.8, corner_radius=0.12, stroke_color=TEAL, stroke_width=4), M("step(390, d)", 32)).move_to([3.6, 1.7, 0])
        chip2 = VGroup(RoundedRectangle(width=3.7, height=0.8, corner_radius=0.12, stroke_color=INK, stroke_width=4), M("step(450, d)", 32)).move_to([3.6, 0.2, 0])
        rl1 = T("radius 390", 32).move_to([3.6, 1.0, 0])
        rl2 = T("radius 450", 32).move_to([3.6, -0.5, 0])
        cap = T("step(edge, x): 0 below the edge, 1 from the edge up", 32).move_to([0.0, -3.05, 0])
        self.play(FadeIn(gframe), FadeIn(lamp), Create(c1), Create(c2), FadeIn(cap), run_time=1.0)
        self.play(FadeIn(chip1), FadeIn(rl1), FadeIn(chip2), FadeIn(rl2), run_time=0.7)
        # the ground splits: outside the small circle
        until(self, "the ground splits")
        A = Annulus(inner_radius=r1, outer_radius=RG, fill_color="#E2DDD1", fill_opacity=0.95, stroke_width=0).move_to([cx, cy, 0])
        A.set_z_index(1)
        out_t = T("outside", 32).move_to([cx, cy + 2.31, 0]); out_t.set_z_index(6)
        in_t = T("inside", 32).move_to([cx, cy - 0.7, 0]); in_t.set_z_index(6)
        self.play(FadeIn(A), run_time=0.6)
        self.play(FadeIn(out_t), FadeIn(in_t), run_time=0.4)
        # the second fill is subtracted
        until(self, "subtract one from the other")
        B = Annulus(inner_radius=r2, outer_radius=RG + 0.05, fill_color=STAGE, fill_opacity=1, stroke_width=0).move_to([cx, cy, 0])
        B.set_z_index(2)
        self.play(FadeOut(out_t), FadeOut(in_t), FadeIn(B), run_time=0.9)
        # the ring that is left
        until(self, "the band between")
        self.play(A.animate.set_fill(TEAL, opacity=0.85), run_time=0.5)
        rt = T("a ring", 32).move_to([3.6, -1.9, 0])
        pt = np.array([cx + 1.9 * np.cos(np.radians(-35)), cy + 1.9 * np.sin(np.radians(-35)), 0])
        ar = arrow([2.5, -1.9, 0], pt + np.array([0.25, -0.05, 0]), w=6, tip=0.2); ar.set_z_index(8)
        dot = Dot(pt, radius=0.12, color=TERRA).set_stroke(DIM, width=3); dot.set_z_index(7)
        self.play(FadeIn(rt), GrowArrow(ar), FadeIn(dot), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
