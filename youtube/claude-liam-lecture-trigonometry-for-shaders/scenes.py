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
"""ACT I · One Angle, Two Numbers  (B02-B05, Manim)

Cast for the act: the right triangle with its marked 30-degree corner at the lower left, right angle at the lower right.
Grey outline; a side that is being talked about thickens to ink. Drawings only (no captures); the numbers are the film's measured ones
(sin 30 = 0.50, sin 50 = 0.77, cos 30 = 0.87).
"""

A1_C30 = float(np.cos(np.radians(30))); A1_S30 = float(np.sin(np.radians(30)))


def a1_tri(ax, ay, hyp, deg):
    """Corners of a right triangle: A (marked corner, lower left), C (right angle, lower right), B (top). hyp = hypotenuse length."""
    a = np.radians(deg)
    A = np.array([ax, ay, 0.0]); C = A + np.array([hyp * np.cos(a), 0.0, 0.0]); B = C + np.array([0.0, hyp * np.sin(a), 0.0])
    return A, C, B


def a1_sides(A, C, B, color=DIM, w=5):
    """(hypotenuse A-B, opposite C-B, adjacent A-C) as separate Lines."""
    return (Line(A, B, color=color, stroke_width=w), Line(C, B, color=color, stroke_width=w), Line(A, C, color=color, stroke_width=w))


def a1_square_mark(C, s=0.28, color=DIM):
    """Right-angle mark at C (lower right): a small square tucked into the corner."""
    return VGroup(Line(C + [-s, 0, 0], C + [-s, s, 0], color=color, stroke_width=4), Line(C + [-s, s, 0], C + [0, s, 0], color=color, stroke_width=4))


def a1_arc_mark(A, r=0.85, deg=30):
    """The marked angle: a thick terracotta arc over a grey backing, and a small terracotta dot on the corner."""
    back = Arc(radius=r, start_angle=0, angle=np.radians(deg), arc_center=A, stroke_color=DIM, stroke_width=16, stroke_opacity=0.55)
    arc = Arc(radius=r, start_angle=0, angle=np.radians(deg), arc_center=A, stroke_color=TERRA, stroke_width=9)
    dot = Dot(A, radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    return VGroup(back, arc, dot)


def a1_thick(mob, on=True):
    return mob.animate.set_color(INK if on else DIM).set_stroke(width=11 if on else 5)


# ═════════════════════════════ B02 · the names of the sides ═════════════════════════════
class B02_RightTriangle(Scene):
    def construct(self):
        A, C, B = a1_tri(-2.5, -1.55, 4.9, 30)
        hy, op, ad = a1_sides(A, C, B)
        sq = a1_square_mark(C)
        mark = a1_arc_mark(A)
        l_hy = T("hypotenuse", 40).move_to([-1.6, 0.85, 0])
        l_op = T("opposite", 40).move_to([C[0] + 1.35, (C[1] + B[1]) / 2, 0])
        l_ad = T("adjacent", 40).move_to([(A[0] + C[0]) / 2, C[1] - 0.7, 0])
        # the three sides draw as one triangle
        self.play(Create(ad), Create(op), Create(hy), run_time=1.0)
        self.play(Create(sq), run_time=0.3)
        until(self, "hypotenuse", lead=0.1)
        self.play(a1_thick(hy), FadeIn(l_hy), run_time=0.4)
        until(self, "Now pick another corner", lead=0.1)
        self.play(FadeIn(mark), run_time=0.5)
        until(self, "opposite", lead=0.1)
        self.play(a1_thick(op), FadeIn(l_op), run_time=0.4)
        until(self, "adjacent", lead=0.1)
        self.play(a1_thick(ad), FadeIn(l_ad), run_time=0.4)
        done(self)


# ═════════════════════════════ B03 · the ratio belongs to the angle ═════════════════════════════
class B03_SameRatio(Scene):
    def construct(self):
        ax, ay = -5.7, -1.9
        ang = ValueTracker(30.0)
        scl = ValueTracker(1.0)
        H0 = 4.0

        def pts():
            return a1_tri(ax, ay, H0 * scl.get_value(), ang.get_value())

        def live_tri():
            A, C, B = pts()
            hy, op, ad = a1_sides(A, C, B, color=INK, w=7)
            return VGroup(hy, op, ad)

        tri = always_redraw(live_tri)
        corner = always_redraw(lambda: Dot(pts()[2], radius=0.16, color=TERRA).set_stroke(DIM, width=3))
        arc = always_redraw(lambda: a1_arc_mark(pts()[0], 0.85, ang.get_value()))
        deg = always_redraw(lambda: T("%d°" % round(ang.get_value()), 40).move_to([ax + 0.75, ay - 0.5, 0]))
        head = T("opposite  ÷  hypotenuse", 36).move_to([3.2, 1.6, 0])
        num = always_redraw(lambda: T("%.2f" % np.sin(np.radians(ang.get_value())), 110).move_to([3.2, 0.1, 0]))
        sub = T("the ratio", 32, DIM).move_to([3.2, -1.1, 0])
        self.add(tri, arc, deg, corner)
        self.play(FadeIn(head), FadeIn(num), FadeIn(sub), run_time=0.5)
        until(self, "Fix the angle", lead=0.1)
        ghosts = VGroup()
        for s in (0.55, 1.3):
            old = a1_tri(ax, ay, H0 * scl.get_value(), 30.0)
            g = Polygon(old[0], old[1], old[2], stroke_color=DIM, stroke_width=3, stroke_opacity=0.85)
            ghosts.add(g)
            self.add(g)
            self.play(scl.animate.set_value(s), run_time=1.1)
            self.wait(0.3)
        until(self, "At thirty degrees", lead=0.0)
        self.wait(0.2)
        until(self, "At fifty", lead=0.15)
        o30 = a1_tri(ax, ay, H0 * scl.get_value(), 30.0)
        self.add(Polygon(o30[0], o30[1], o30[2], stroke_color=DIM, stroke_width=3, stroke_opacity=0.85))
        self.play(ang.animate.set_value(50.0), run_time=1.6)
        done(self)


# ═════════════════════════════ B04 · three ratios, three names ═════════════════════════════
class B04_SohCahToa(Scene):
    def construct(self):
        A, C, B = a1_tri(-6.1, -1.4, 3.9, 30)
        hy, op, ad = a1_sides(A, C, B)
        sq = a1_square_mark(C, 0.24)
        mark = a1_arc_mark(A, 0.7)
        l_hy = T("hypotenuse", 32).move_to([-4.85, 0.2, 0])
        l_op = T("opposite", 32).move_to([C[0] + 0.1, (C[1] + B[1]) / 2 - 1.15, 0]).shift([0.0, 0, 0])
        l_ad = T("adjacent", 32).move_to([(A[0] + C[0]) / 2, C[1] - 0.5, 0])
        l_op.move_to([C[0] + 0.95, (C[1] + B[1]) / 2, 0])
        rows = []
        specs = (("sine  ·  opposite  ÷  hypotenuse", 2.0), ("cosine  ·  adjacent  ÷  hypotenuse", 0.7), ("tangent  ·  opposite  ÷  adjacent", -0.6))
        for s, y in specs:
            t = T(s, 34)
            r = box(2.55, y, 6.6, 1.0, color=INK, sw=4)
            t.move_to(r.get_center())
            rows.append(VGroup(r, t))
        self.add(ad, op, hy, sq, mark, l_hy, l_op, l_ad)
        ghost_rows = [box(2.55, y, 6.6, 1.0, color=GHOST, sw=3) for _, y in specs]
        self.play(*[Create(g) for g in ghost_rows], run_time=0.6)

        def light(sides):
            return [a1_thick(s, s in sides) for s in (hy, op, ad)]

        until(self, "sine", lead=0.2)
        self.play(FadeIn(rows[0]), *light([op, hy]), run_time=0.5)
        until(self, "Adjacent over hypotenuse", lead=0.2)
        self.play(FadeIn(rows[1]), *light([ad, hy]), run_time=0.5)
        until(self, "Opposite over adjacent", lead=0.2)
        self.play(FadeIn(rows[2]), run_time=0.5)
        until(self, "The memory trick", lead=0.5)
        self.play(*light([op, ad]), run_time=0.4)
        until(self, "S O H", lead=0.1)
        word = VGroup(T("SOH", 48, INK, True), T("CAH", 48, INK, True), T("TOA", 48, INK, True))
        for w, x in zip(word, (-0.1, 2.55, 5.2)):
            w.move_to([x, -2.35, 0])
        self.play(FadeIn(word, shift=UP * 0.2), run_time=0.5)
        done(self)


# ═════════════════════════════ B05 · sine and cosine are lookups ═════════════════════════════
def a1_token(txt, x, y, w=1.3):
    p = RoundedRectangle(width=w, height=0.72, corner_radius=0.36, fill_color=PALEBOX, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])
    t = T(txt, 36).move_to([x, y, 0])
    return VGroup(p, t)


class B05_Lookup(Scene):
    def construct(self):
        ys = (1.15, -1.0)
        names = ("sine", "cosine")
        outs = ("0.50", "0.87")
        boxes = []
        for y, n in zip(ys, names):
            b = box(0.0, y, 2.9, 1.3, color=INK, sw=5)
            t = T(n, 44).move_to(b.get_center())
            boxes.append(VGroup(b, t))
        a_in = [arrow([-4.2, y, 0], [-1.6, y, 0], color=DIM) for y in ys]
        a_out = [arrow([1.6, y, 0], [3.0, y, 0], color=DIM) for y in ys]
        cap = T("angle in, number out", 40).move_to([0.0, -2.7, 0])
        self.play(*[Create(b) for b in boxes], *[Create(a) for a in a_in], *[Create(a) for a in a_out], run_time=0.8)
        for i in range(2):
            y = ys[i]
            until(self, ("Sine of thirty", "Cosine of thirty")[i], lead=0.1)
            tok = a1_token("30°", -5.0, y, 1.4)
            self.play(FadeIn(tok), run_time=0.25)
            self.play(tok.animate.move_to([-1.55, y, 0]).scale(0.5).set_opacity(0.0), run_time=0.7, rate_func=linear)
            self.remove(tok)
            res = a1_token(outs[i], 1.75, y, 1.5)
            self.play(FadeIn(res), run_time=0.2)
            self.play(res.animate.move_to([4.6, y, 0]), run_time=0.6)
        until(self, "An angle goes in", lead=0.1)
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Angle In, Position Out  (B06, B07, B09-B15, all Manim; B08 is Remotion)

One cast for the act: the unit circle drawn ON PAPER (y up, angles counterclockwise), the terracotta dot, the triangle inside it,
and the plot beside it. Everything is a drawing and says so ('on paper'). Real numbers only: cos 30 = 0.87, sin 30 = 0.50,
0.6 x cos 30 = 0.52, 0.6 x sin 30 = 0.30, 6.28, sin(30.0) = -0.99, sin(radians(30.0)) = 0.50 (verify-math.gd, Lab 21).
"""

A2_PALE = "#9A8F7A"      # the cosine curve: a lighter grey-brown (mid-tone, outside the text-like grey band)


def a2_d(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def a2_dot(p, r=0.17):
    return Dot(np.array(p, dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a2_arcmark(c, deg, rad=0.7):
    """A thick terracotta arc (never a wedge) over a grey backing."""
    a = max(float(deg), 0.5)
    back = Arc(radius=rad, start_angle=0, angle=np.radians(a), arc_center=c, stroke_color=DIM, stroke_width=17, stroke_opacity=0.55)
    arc = Arc(radius=rad, start_angle=0, angle=np.radians(a), arc_center=c, stroke_color=TERRA, stroke_width=10)
    return VGroup(back, arc)


def a2_foot(c, r, deg):
    return c + np.array([r * np.cos(np.radians(deg)), 0.0, 0.0])


def a2_vleg(c, r, deg, color=INK, w=5):
    return DashedLine(c + r * a2_d(deg), a2_foot(c, r, deg), color=color, stroke_width=w, dash_length=0.12)


def a2_hleg(c, r, deg, color=INK, w=8):
    return Line(c, a2_foot(c, r, deg), color=color, stroke_width=w)


def a2_rt(c, r, deg, s=0.22):
    f = a2_foot(c, r, deg)
    m = VMobject(stroke_color=DIM, stroke_width=4)
    m.set_points_as_corners([f + [-s, 0, 0], f + [-s, s, 0], f + [0, s, 0]])
    return m


def a2_axes(c, ext, extv=None):
    extv = ext if extv is None else extv
    return VGroup(Line(c + [-ext, 0, 0], c + [ext, 0, 0], color=DIM, stroke_width=3, stroke_opacity=0.6),
                  Line(c + [0, -extv, 0], c + [0, extv, 0], color=DIM, stroke_width=3, stroke_opacity=0.6))


def a2_label_beside(txt, mid, n, pad=0.2):
    """A label centred off a point along unit normal n, clear of the line."""
    off = n * (pad + abs(n[0]) * txt.width / 2 + abs(n[1]) * txt.height / 2)
    return txt.move_to(mid + off)


_A2_CW = {}


def a2_cw(size=32):
    if size not in _A2_CW:
        _A2_CW[size] = M("MMMMMMMMMM", size).width / 10
    return _A2_CW[size]


def a2_mline(s, x, y, size=32, align="left", color=INK):
    """A monospace line placed token by token at explicit character positions (Pango drops single spaces here). Returns a VGroup of tokens."""
    import re
    cw = a2_cw(size)
    xl = x if align == "left" else x - len(s) * cw / 2
    toks = []
    for m in re.finditer(r"\S+", s):
        t = M(m.group(0), size, color)
        t.move_to([xl + (m.start() + len(m.group(0)) / 2) * cw, y, 0])
        toks.append(t)
    return VGroup(*toks)


def a2_plot_static(cy, x0=-2.0, W=6.4, R=1.4):
    """The plot of the act: angle along the bottom, 'height' up the side, a faint zero line. Returns (group, px(theta), py(value))."""
    yb = cy - R - 0.3
    px = lambda th: x0 + th / (2 * np.pi) * W
    py = lambda v: cy + v * R
    g = VGroup(Line([x0, yb, 0], [x0, cy + R + 0.3, 0], color=INK, stroke_width=5),
               Line([x0, yb, 0], [x0 + W, yb, 0], color=INK, stroke_width=5),
               DashedLine([x0, cy, 0], [x0 + W, cy, 0], color=DIM, stroke_width=3, dash_length=0.12))
    for th, s in [(np.pi / 2, "π/2"), (np.pi, "π"), (3 * np.pi / 2, "3π/2"), (2 * np.pi, "τ")]:
        g.add(Line([px(th), yb, 0], [px(th), yb - 0.13, 0], color=DIM, stroke_width=4))
        g.add(T(s, 32).move_to([px(th), yb - 0.48, 0]))
    h = T("height", 32).rotate(PI / 2).move_to([x0 - 0.5, cy + 0.85, 0])
    g.add(h)
    g.add(T("angle", 32, DIM).move_to([x0 + W / 2, yb - 1.05, 0]))
    return g, px, py


def a2_curve(fn, px, py, color, th0=0.0, th1=2 * np.pi, n=90, w=7):
    pts = [np.array([px(t), py(fn(t)), 0]) for t in np.linspace(th0, th1, n)]
    m = VMobject(stroke_color=color, stroke_width=w)
    m.set_points_smoothly(pts)
    return m


class B06_UnitCircle(Scene):
    def construct(self):
        c = np.array([0.0, -0.5, 0.0]); r = 2.2
        title = T("Angle In, Position Out", 40)
        title.move_to([-6.0 + title.width / 2, 2.95, 0])
        cap = T("on paper", 32, DIM).move_to([5.0, -2.85, 0])
        axes = a2_axes(c, r + 0.6, r + 0.45)
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        self.play(Create(circ), Create(axes), FadeIn(title), FadeIn(cap), run_time=1.0)
        tr = ValueTracker(0)
        rad = always_redraw(lambda: Line(c, c + r * a2_d(tr.get_value()), color=INK, stroke_width=6))
        arc = always_redraw(lambda: a2_arcmark(c, tr.get_value()))
        self.add(rad, arc)
        until(self, "Walk out")
        self.play(tr.animate.set_value(30), run_time=1.4)
        p = c + r * a2_d(30)
        dot = a2_dot(p)
        n = np.array([-np.sin(np.radians(30)), np.cos(np.radians(30)), 0])
        lab = a2_label_beside(T("radius 1", 32), c + r * a2_d(30) / 2, n, 0.12)
        ang = T("30°", 32).move_to(c + 1.25 * a2_d(14))
        self.play(GrowFromCenter(dot), FadeIn(lab), FadeIn(ang), run_time=0.8)
        until(self, "The triangle's two short")
        vl = a2_vleg(c, r, 30); hl = a2_hleg(c, r, 30); rt = a2_rt(c, r, 30)
        self.add(vl, hl, rt); self.bring_to_front(dot)
        self.remove(vl, hl, rt)
        self.play(Create(vl), Create(hl), FadeIn(rt), run_time=1.3)
        self.bring_to_front(dot)
        done(self)


class B07_LegsAreCosSin(Scene):
    def construct(self):
        c = np.array([-1.8, -0.4, 0.0]); r = 2.2
        tr = ValueTracker(30)
        g = lambda: tr.get_value()
        axes = a2_axes(c, r + 0.6, r + 0.45)
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        rad = always_redraw(lambda: Line(c, c + r * a2_d(g()), color=INK, stroke_width=6))
        arc = always_redraw(lambda: a2_arcmark(c, g()))
        dot = always_redraw(lambda: a2_dot(c + r * a2_d(g())))
        vl = always_redraw(lambda: a2_vleg(c, r, g()))
        hl = always_redraw(lambda: a2_hleg(c, r, g()))
        rt = always_redraw(lambda: a2_rt(c, r, g()))
        radlab = a2_label_beside(T("radius 1", 32), c + r * a2_d(30) / 2, np.array([-0.5, 0.866, 0]), 0.2)
        self.add(axes, circ, rad, arc, hl, vl, rt, dot, radlab)
        self.wait(0.3)
        tl_ = T("unit circle", 36).move_to([-1.8, 2.55, 0])
        tag = VGroup(box(-1.8, 2.55, tl_.width + 0.5, 0.8, color=INK, sw=4), tl_)
        self.play(FadeIn(tag, shift=DOWN * 0.2), run_time=0.7)
        # legs labelled
        coslab = always_redraw(lambda: T("cos", 32).move_to([c[0] + r * np.cos(np.radians(g())) / 2, c[1] - 0.42, 0]))
        sinlab = always_redraw(lambda: T("sin", 32).move_to([c[0] + r * np.cos(np.radians(g())) + 0.5, c[1] + r * np.sin(np.radians(g())) / 2, 0]))
        x0 = 2.6
        w1 = T("cos", 40).move_to([x0 + 0.35, 0.8, 0]); w2 = T("sin", 40).move_to([x0 + 0.35, -0.2, 0])
        n1 = always_redraw(lambda: T(f"{np.cos(np.radians(g())):.2f}", 40).move_to([x0 + 1.55, 0.8, 0]))
        n2 = always_redraw(lambda: T(f"{np.sin(np.radians(g())):.2f}", 40).move_to([x0 + 1.55, -0.2, 0]))
        d1 = T("÷  1", 32, DIM).move_to([x0 + 2.85, 0.8, 0]); d2 = T("÷  1", 32, DIM).move_to([x0 + 2.85, -0.2, 0])
        self.play(FadeIn(coslab), FadeIn(sinlab), FadeIn(w1), FadeIn(w2), FadeIn(n1), FadeIn(n2), FadeIn(d1), FadeIn(d2), run_time=0.9)
        until(self, "dividing by one")
        self.play(*[m.animate.scale(0.05).set_opacity(0) for m in (d1, d2)], run_time=0.8)
        self.remove(d1, d2)
        until(self, "The point sits", lead=0.9)
        cs = always_redraw(lambda: a2_label_beside(T("(cos, sin)", 32), c + r * a2_d(g()), a2_d(20), 0.22))
        self.play(FadeIn(cs), FadeOut(radlab), tr.animate.set_value(60), run_time=1.1)
        self.play(tr.animate.set_value(30), FadeIn(radlab), run_time=1.1)
        done(self)


class B09_RadiusAndCenter(Scene):
    def construct(self):
        u = 1.1
        rs = ValueTracker(1.0); cx = ValueTracker(-2.4)
        cy = 0.6
        C = lambda: np.array([cx.get_value(), cy, 0.0])
        circ = always_redraw(lambda: Circle(radius=u * rs.get_value(), stroke_color=INK, stroke_width=5).move_to(C()))
        rad = always_redraw(lambda: Line(C(), C() + u * rs.get_value() * a2_d(30), color=INK, stroke_width=6))
        dot = always_redraw(lambda: a2_dot(C() + u * rs.get_value() * a2_d(30)))
        self.add(circ, rad, dot)
        y = -2.65
        cw = a2_cw(32)
        s = "c + r * vec2(cos(a), sin(a))"
        xl = -len(s) * cw / 2
        pos = lambda idx, ln: xl + (idx + ln / 2) * cw

        def tok(txt, idx):
            return M(txt, 32).move_to([pos(idx, len(txt)), y, 0])
        base1 = tok("vec2(cos(a),", 8); base2 = tok("sin(a))", 21)
        self.play(FadeIn(base1), FadeIn(base2), run_time=0.7)
        until(self, "Multiply by the radius")
        tr_, ts_ = tok("r", 4), tok("*", 6)
        rlab = always_redraw(lambda: T("r", 36).move_to(C() + u * rs.get_value() * a2_d(30) / 2 + np.array([0.12, -0.38, 0])))
        self.play(FadeIn(tr_, shift=DOWN * 0.2), FadeIn(ts_, shift=DOWN * 0.2), FadeIn(rlab), rs.animate.set_value(1.8), run_time=1.3)
        until(self, "Add the center")
        tc_, tp_ = tok("c", 0), tok("+", 2)
        cross = always_redraw(lambda: VGroup(
            Line(C() + [-0.2, 0, 0], C() + [0.2, 0, 0], color=DIM, stroke_width=15, stroke_opacity=0.55),
            Line(C() + [0, -0.2, 0], C() + [0, 0.2, 0], color=DIM, stroke_width=15, stroke_opacity=0.55),
            Line(C() + [-0.2, 0, 0], C() + [0.2, 0, 0], color=TERRA, stroke_width=9),
            Line(C() + [0, -0.2, 0], C() + [0, 0.2, 0], color=TERRA, stroke_width=9)))
        clab = always_redraw(lambda: T("c", 36).move_to(C() + np.array([-0.45, -0.4, 0])))
        self.play(FadeIn(tc_, shift=DOWN * 0.2), FadeIn(tp_, shift=DOWN * 0.2), FadeIn(cross), FadeIn(clab), run_time=0.6)
        self.play(cx.animate.set_value(2.4), run_time=1.5)
        done(self)


class B10_WorkedExample(Scene):
    def construct(self):
        c = np.array([-3.4, -0.3, 0.0]); R = 1.8
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a2_axes(c, R + 0.5, R + 0.4)
        p = c + R * a2_d(30)
        rad = Line(c, p, color=INK, stroke_width=5)
        hl = a2_hleg(c, R, 30, DIM, 4); vl = Line(p, a2_foot(c, R, 30), color=DIM, stroke_width=4)
        n = np.array([-0.5, 0.866, 0])
        r06 = a2_label_beside(T("0.6", 36), c + (p - c) / 2, n, 0.1)
        self.play(Create(circ), Create(axes), Create(rad), Create(hl), Create(vl), run_time=1.0)
        dot = a2_dot(p)
        self.play(GrowFromCenter(dot), FadeIn(r06), run_time=0.6)
        # equations
        xl = -0.4
        e1a = T("0.6 × cos 30°", 38); e1b = T("=", 38); e1c = T("0.52", 38)
        e2a = T("0.6 × sin 30°", 38); e2b = T("=", 38); e2c = T("0.30", 38)

        def row(a, b, c_, y):
            VGroup(a, b, c_).arrange(RIGHT, buff=0.3).align_to([xl, 0, 0], LEFT).set_y(y)
        row(e1a, e1b, e1c, -0.55); row(e2a, e2b, e2c, -1.55)
        until(self, "The first number")
        self.play(hl.animate.set_stroke(INK, width=10), FadeIn(e1a), run_time=0.6)
        self.play(FadeIn(e1b), FadeIn(e1c), run_time=0.5)
        until(self, "The second is")
        self.play(vl.animate.set_stroke(INK, width=10), FadeIn(e2a), run_time=0.6)
        self.play(FadeIn(e2b), FadeIn(e2c), run_time=0.5)
        until(self, "Hold on")
        bt = T("(0.52, 0.30)", 40).move_to([0.5, 1.4, 0])
        bx = box(0.5, 1.4, bt.width + 0.5, bt.height + 0.4, color=INK, sw=4)
        note = T("hold on to these", 32, DIM).move_to([0.5, 0.65, 0])
        self.play(ReplacementTransform(VGroup(e1c.copy(), e2c.copy()), bt), Create(bx), run_time=1.0)
        self.play(FadeIn(note), run_time=0.5)
        done(self)


class B11_Radians(Scene):
    def construct(self):
        c = np.array([-1.8, -0.2, 0.0]); R = 2.0
        axes = a2_axes(c, R + 0.45, R + 0.4)
        circ = Circle(radius=R, stroke_color=DIM, stroke_width=4).move_to(c)
        bar = Line(c, c + [R, 0, 0], color=INK, stroke_width=11)
        self.play(Create(axes), Create(circ), Create(bar), run_time=0.9)
        cols = [INK, TEAL, INK, TEAL, INK, TEAL]
        arcs = [Arc(radius=R, start_angle=k, angle=1.0, arc_center=c, stroke_color=cols[k], stroke_width=11) for k in range(6)]
        left = Arc(radius=R, start_angle=6.0, angle=2 * np.pi - 6.0, arc_center=c, stroke_color=GOLD, stroke_width=11)
        counter = T("1", 72).move_to([3.9, 0.9, 0])
        cap = T("radii", 32, DIM).move_to([3.9, 0.15, 0])
        until(self, "Lay one radius")
        self.play(TransformFromCopy(bar, arcs[0]), run_time=1.0)
        mark = a2_arcmark(c, np.degrees(1.0), 0.65)
        edge = Line(c, c + R * np.array([np.cos(1.0), np.sin(1.0), 0]), color=DIM, stroke_width=3)
        rlab = T("radian", 32).move_to(c + np.array([1.15, 0.5, 0]))
        self.play(Create(mark), Create(edge), FadeIn(rlab), FadeIn(counter), FadeIn(cap), run_time=0.8)
        for k in (1, 2):
            nc = T(str(k + 1), 72).move_to(counter.get_center())
            self.play(Create(arcs[k]), Transform(counter, nc), run_time=0.55)
        until(self, "A full turn")
        for k in (3, 4, 5):
            nc = T(str(k + 1), 72).move_to(counter.get_center())
            self.play(Create(arcs[k]), Transform(counter, nc), run_time=0.5)
        ll = T("left over", 32).move_to([1.7, -0.9, 0])
        self.play(Create(left), FadeIn(ll), run_time=0.5)
        total = T("6.28 = a full turn", 36).move_to([3.5, -1.8, 0])
        until(self, "about six point")
        self.play(FadeIn(total), run_time=0.6)
        done(self)


class B12_PiTau(Scene):
    def construct(self):
        c = np.array([-2.4, -0.3, 0.0]); R = 1.9
        axes = a2_axes(c, R + 0.4, R + 0.3)
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        a = ValueTracker(0.0)
        rad = always_redraw(lambda: Line(c, c + R * np.array([np.cos(a.get_value()), np.sin(a.get_value()), 0]), color=INK, stroke_width=6))

        def trail():
            v = a.get_value()
            if v < 0.03:
                return VMobject()
            return Arc(radius=R, start_angle=0, angle=v, arc_center=c, stroke_color=TEAL, stroke_width=8)
        tl = always_redraw(trail)
        self.play(Create(circ), Create(axes), run_time=0.8)
        self.add(rad, tl)
        dirs = [(np.pi / 2, "PI / 2", [0, R + 0.6, 0]), (np.pi, "PI", [-R - 0.65, 0, 0]),
                (3 * np.pi / 2, "3 * PI / 2", [0, -R - 0.6, 0]), (2 * np.pi, "TAU", [R + 0.85, 0, 0])]
        until(self, "Pi is half", lead=1.6)
        prev = 0.0
        for th, s, off in dirs:
            tick = Line(c + 0.8 * R * np.array([np.cos(th), np.sin(th), 0]), c + 1.12 * R * np.array([np.cos(th), np.sin(th), 0]), color=INK, stroke_width=8)
            lab = a2_mline(s, c[0] + off[0], c[1] + off[1], 32, "center")
            self.play(a.animate.set_value(th), rate_func=linear, run_time=0.6)
            self.play(Create(tick), FadeIn(lab), run_time=0.25)
            prev = th
        until(self, "And the function")
        self.wait(max(0.05, _TARGET.get("B12", 10.7) / 2 + 0.15 - _elapsed(self)))
        p45 = c + R * a2_d(45)
        edge = Line(c, p45, color=INK, stroke_width=5)
        mark = a2_arcmark(c, 45, 0.95)
        l1 = a2_mline("radians(45.0)", 1.5, 0.5, 32)
        l2 = a2_mline("= PI / 4.0", 1.5, -0.2, 32)
        cr = T("Godot 4.7 docs · Global built-ins", 32, DIM).move_to([2.9, -2.85, 0])
        self.play(Create(edge), Create(mark), run_time=0.8)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(cr), run_time=0.8)
        done(self)


class B13_DegreesTrap(Scene):
    def construct(self):
        R = 1.2; cy = 0.3
        cL = np.array([-3.9, cy, 0.0]); cR = np.array([2.1, cy, 0.0])
        circL = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(cL)
        circR = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(cR)
        axL = a2_axes(cL, R + 0.3, R + 0.3); axR = a2_axes(cR, R + 0.3, R + 0.3)
        tL = a2_mline("sin(30.0)", cL[0] + 0.9, 2.35, 32, "center")
        tRt = a2_mline("sin(radians(30.0))", cR[0] + 1.0, 2.35, 32, "center")
        bxL = cL[0] + 2.0; bxR = cR[0] + 2.0
        zeroL = Line([bxL - 0.4, cy, 0], [bxL + 0.4, cy, 0], color=INK, stroke_width=4)
        zeroR = Line([bxR - 0.4, cy, 0], [bxR + 0.4, cy, 0], color=INK, stroke_width=4)
        cred = T("math values · checked in a Godot 4.7.2 shader", 32, DIM).move_to([0, -3.0, 0])
        self.play(Create(circL), Create(circR), Create(axL), Create(axR), FadeIn(tL), FadeIn(tRt), Create(zeroL), Create(zeroR), FadeIn(cred), run_time=1.0)
        aL = ValueTracker(0.0); aR = ValueTracker(0.0); vL = ValueTracker(0.0); vR = ValueTracker(0.0)
        dL = always_redraw(lambda: a2_dot(cL + R * np.array([np.cos(aL.get_value()), np.sin(aL.get_value()), 0]), 0.16))
        dR = always_redraw(lambda: a2_dot(cR + R * np.array([np.cos(aR.get_value()), np.sin(aR.get_value()), 0]), 0.16))
        rL = always_redraw(lambda: Line(cL, cL + R * np.array([np.cos(aL.get_value()), np.sin(aL.get_value()), 0]), color=DIM, stroke_width=3))
        rR = always_redraw(lambda: Line(cR, cR + R * np.array([np.cos(aR.get_value()), np.sin(aR.get_value()), 0]), color=DIM, stroke_width=3))

        def bar(tr, bx):
            v = tr.get_value()
            h = max(abs(v) * R, 0.01)
            rect = Rectangle(width=0.5, height=h, fill_color=DIM, fill_opacity=1, stroke_width=0)
            rect.move_to([bx, cy + np.sign(v if v else 1) * h / 2, 0])
            return rect
        barL = always_redraw(lambda: bar(vL, bxL)); barR = always_redraw(lambda: bar(vR, bxR))
        cnt = always_redraw(lambda: T(str(int(aL.get_value() / (2 * np.pi))), 56).move_to([cL[0] + 0.9, -1.75, 0]))
        cl = T("turns", 32, DIM).move_to([cL[0] - 0.4, -1.75, 0])
        self.add(rL, rR, dL, dR, barL, barR, cl, cnt)
        until(self, "Thirty radians", lead=0.5)
        self.play(aL.animate.set_value(30.0), rate_func=smooth, run_time=1.8)
        until(self, "near minus one")
        vl = T("-0.99", 40).move_to([bxL + 0.35 + 0.65, cy - 0.99 * R + 0.1, 0])
        self.play(vL.animate.set_value(-0.988), FadeIn(vl), run_time=0.8)
        until(self, "Convert first")
        mk = a2_arcmark(cR, 30, 0.6)
        vr = T("0.50", 40).move_to([bxR + 0.35 + 0.6, cy + 0.5 * R, 0])
        self.play(aR.animate.set_value(np.radians(30)), vR.animate.set_value(0.5), Create(mk), FadeIn(vr), run_time=1.1)
        done(self)


class B14_SineWave(Scene):
    def construct(self):
        cy = 0.5; R = 1.4
        c = np.array([-4.4, cy, 0.0])
        plot, px, py = a2_plot_static(cy, -2.0, 6.4, R)
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a2_axes(c, R + 0.35, R + 0.35)
        self.play(Create(circ), Create(axes), Create(plot), run_time=1.0)
        th = ValueTracker(0.0)
        P = lambda: c + R * np.array([np.cos(th.get_value()), np.sin(th.get_value()), 0])

        def curve():
            v = th.get_value()
            if v < 0.03:
                return VMobject()
            ts = np.linspace(0, v, max(4, int(v / (2 * np.pi) * 90)))
            m = VMobject(stroke_color=INK, stroke_width=7)
            m.set_points_as_corners([np.array([px(t), py(np.sin(t)), 0]) for t in ts])
            return m
        cur = always_redraw(curve)
        dash = always_redraw(lambda: DashedLine(P(), [px(th.get_value()), P()[1], 0], color=DIM, stroke_width=4, dash_length=0.12))
        tip = always_redraw(lambda: Dot([px(th.get_value()), P()[1], 0], radius=0.1, color=TEAL))
        rad = always_redraw(lambda: Line(c, P(), color=INK, stroke_width=5))
        dot = always_redraw(lambda: a2_dot(P()))
        self.add(cur, dash, rad, dot, tip)
        until(self, "Plot the point's")
        self.play(th.animate.set_value(np.pi), rate_func=linear, run_time=3.0)
        until(self, "The height climbs", lead=0.1)
        self.play(th.animate.set_value(2 * np.pi), rate_func=linear, run_time=2.6)
        until(self, "That curve is")
        sl = T("sine", 40).move_to([px(2 * np.pi) + 0.75, py(0), 0])
        self.play(FadeIn(sl), run_time=0.6)
        done(self)


class B15_CosineShift(Scene):
    def construct(self):
        cy = 0.5; R = 1.4
        c = np.array([-4.4, cy, 0.0])
        plot, px, py = a2_plot_static(cy, -2.0, 6.4, R)
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a2_axes(c, R + 0.35, R + 0.35)
        sine = a2_curve(np.sin, px, py, INK)
        sl = T("sine", 40).move_to([px(2 * np.pi) + 0.75, py(0), 0])
        home = a2_dot(c + [R, 0, 0])
        self.add(circ, axes, plot, sine, sl, home)
        self.wait(0.3)
        cosine = a2_curve(np.cos, px, py, A2_PALE)
        cl = T("cosine", 40).move_to([px(2 * np.pi) + 0.85, py(1), 0])
        self.play(Create(cosine), run_time=2.0)
        yt = py(1) + 0.4
        brk = VGroup(Line([px(0), yt, 0], [px(np.pi / 2), yt, 0], color=INK, stroke_width=5),
                     Line([px(0), yt, 0], [px(0), yt - 0.3, 0], color=INK, stroke_width=5),
                     Line([px(np.pi / 2), yt, 0], [px(np.pi / 2), yt - 0.3, 0], color=INK, stroke_width=5))
        ql = T("quarter turn", 36).move_to([(px(0) + px(np.pi / 2)) / 2 + 0.2, yt + 0.45, 0])
        until(self, "a quarter turn earlier")
        self.play(Create(brk), FadeIn(ql), FadeIn(cl), run_time=0.9)
        th = ValueTracker(0.0)
        g = lambda: th.get_value()
        until(self, "Two waves", lead=0.7)
        cursor = always_redraw(lambda: Line([px(g()), cy - R - 0.3, 0], [px(g()), cy + R + 0.3, 0], color=DIM, stroke_width=4))
        sd = always_redraw(lambda: Dot([px(g()), py(np.sin(g())), 0], radius=0.13, color=INK))
        cd = always_redraw(lambda: Dot([px(g()), py(np.cos(g())), 0], radius=0.13, color=A2_PALE).set_stroke(INK, width=2))
        pt = always_redraw(lambda: a2_dot(c + R * np.array([np.cos(g()), np.sin(g()), 0])))

        def trail():
            v = g()
            if v < 0.03:
                return VMobject()
            return Arc(radius=R, start_angle=0, angle=v, arc_center=c, stroke_color=TEAL, stroke_width=8)
        tl = always_redraw(trail)
        self.remove(home)
        self.add(cursor, tl, sd, cd, pt)
        self.play(th.animate.set_value(2 * np.pi), rate_func=linear, run_time=2.4)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · An Orbit  (B16, B17, B20, B25, Manim)

Cast for the act: the centered square p in SCREEN orientation (y counts DOWN), outline cells, a terracotta probe dot,
teal planet and slate-blue moon (same colours as the Lab renders). Drawings only.
"""

A3_PLANET = "#5EA391"; A3_MOON = "#8099BF"


# ═════════════════════════════ B16 · the centered pixel address ═════════════════════════════
class B16_CenterAddress(Scene):
    def construct(self):
        title = T("An Orbit", 40).to_corner(UL, buff=0.95)
        S = 3.2; cx, cy = -3.7, -0.35
        x0, x1, y0, y1 = cx - S / 2, cx + S / 2, cy + S / 2, cy - S / 2
        sq = Square(side_length=S, stroke_color=INK, stroke_width=5).move_to([cx, cy, 0])
        yar = arrow([x0 - 0.55, y0, 0], [x0 - 0.55, y0 - 1.1, 0], color=DIM, w=5)
        ylab = T("y", 32, DIM).move_to([x0 - 0.55, y0 - 1.5, 0])
        uv = T("UV", 40).move_to([cx, y0 + 0.5, 0])
        lab_tl = T("(0, 0)", 32).move_to([x0 + 0.05, y0 + 0.35, 0]).shift([0.0, 0, 0])
        lab_br = T("(1, 1)", 32).move_to([x1 - 0.05, y1 - 0.35, 0])
        lab_mid = T("(0.5, 0.5)", 32).move_to([cx, cy - 0.5, 0])
        dot = Dot([cx, cy, 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        self.add(title)
        self.play(Create(sq), Create(yar), FadeIn(ylab), FadeIn(uv), FadeIn(lab_tl), FadeIn(lab_br), FadeIn(lab_mid), GrowFromCenter(dot), run_time=0.8)
        card = code_card("void fragment() {\n    vec2 p = UV * 2.0 - 1.0;\n}", x=2.45, y=-0.5, size=32)
        line2 = card.lines[1]
        card.remove(line2)
        tagbox = VGroup(RoundedRectangle(width=3.0, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1), T("once per pixel", 32))
        tagbox.move_to([card.lines[0].get_left()[0] + 1.6, card.frame.get_top()[1] + 0.85, 0])
        link = Line(tagbox.get_bottom(), [tagbox.get_center()[0], card.lines[0].get_top()[1] + 0.02, 0], color=DIM, stroke_width=4)
        until(self, "It runs once", lead=0.15)
        self.play(FadeIn(card), FadeIn(tagbox), Create(link), run_time=0.6)
        until(self, "Double it", lead=0.2)
        self.play(FadeIn(line2, shift=RIGHT * 0.2), run_time=0.5)
        until(self, "the range becomes", lead=0.05)
        n_tl = T("(-1, -1)", 32).move_to(lab_tl.get_center())
        n_br = T("(1, 1)", 32).move_to(lab_br.get_center())
        n_mid = T("(0, 0)", 32).move_to(lab_mid.get_center())
        self.play(Transform(lab_tl, n_tl), Transform(lab_mid, n_mid), run_time=0.8)
        until(self, "with zero, zero", lead=0.3)
        self.play(dot.animate.move_to([x0 + 0.0, y0, 0]), run_time=0.6)
        self.play(dot.animate.move_to([cx, cy, 0]), run_time=0.6)
        ptag = always_redraw(lambda: T("p", 40).next_to(dot, UR, buff=0.12))
        self.add(ptag)
        self.play(FadeIn(ptag), run_time=0.2)
        done(self)


# ═════════════════════════════ B17 · the planet is a distance test ═════════════════════════════
class B17_Planet(Scene):
    def construct(self):
        N = 12; cell = 0.42; gx, gy = -3.6, 0.15
        half = N * cell / 2.0
        grid = pixel_grid(N, N, cell, x=gx, y=gy, color=DIM, sw=2)
        rad = 0.25 * half
        planet = Circle(radius=rad, stroke_color=TEAL, stroke_width=4, stroke_opacity=0.9).move_to([gx, gy, 0])
        v = ValueTracker(0.0)          # length(p)
        probe = always_redraw(lambda: Dot([gx + v.get_value() * half, gy, 0], radius=0.13, color=TERRA).set_stroke(DIM, width=3))
        trail = always_redraw(lambda: Line([gx, gy, 0], [gx + v.get_value() * half, gy, 0], color=DIM, stroke_width=4))

        def live_cell():
            inside = v.get_value() < 0.25
            c = Square(side_length=cell * 0.94, stroke_color=TEAL if inside else DIM, stroke_width=5).move_to([gx + v.get_value() * half, gy, 0])
            return c.set_fill(TEAL if inside else GHOST, opacity=0.9)

        pcell = always_redraw(live_cell)
        lab = T("length(p)", 40).move_to([3.5, 1.7, 0])
        num = always_redraw(lambda: T("%.2f" % v.get_value(), 110).move_to([3.5, 0.2, 0]))
        verdict = always_redraw(lambda: T("planet" if v.get_value() < 0.25 else "stage", 40).move_to([3.5, -1.2, 0]))
        code = M("if (length(p) < 0.25)", 32).move_to([gx, -3.0, 0])
        self.play(Create(grid), Create(planet), run_time=0.7)
        self.add(trail, pcell, probe)
        self.play(FadeIn(lab), FadeIn(num), FadeIn(verdict), run_time=0.4)
        until(self, "Length of p", lead=0.1)
        self.play(v.animate.set_value(0.2), run_time=2.6, rate_func=linear)
        self.wait(0.3)
        until(self, "Under the radius", lead=0.2)
        self.play(v.animate.set_value(0.4), run_time=1.4, rate_func=linear)
        self.play(FadeIn(code, shift=UP * 0.2), run_time=0.4)
        until(self, "paint planet color", lead=0.1)
        inside = [s for row in grid.cells for s in row if np.hypot(s.get_center()[0] - gx, s.get_center()[1] - gy) < rad]
        self.play(*[tint(s, TEAL, 0.9) for s in inside], run_time=0.7)
        done(self)


# ═════════════════════════════ B20 · paper against screen ═════════════════════════════
def a3_circ(cx, cy, r, up):
    """A circle with its y arrow and the dot at a quarter turn: up on paper, down on a screen. Returns a VGroup(circle, arrow, radius line, dot)."""
    sgn = 1 if up else -1
    c = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to([cx, cy, 0])
    ar = arrow([cx - r - 0.6, cy - sgn * 0.85, 0], [cx - r - 0.6, cy + sgn * 0.85, 0], color=DIM, w=6)
    rl = Line([cx, cy, 0], [cx, cy + sgn * r, 0], color=DIM, stroke_width=4)
    d = Dot([cx, cy + sgn * r, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3)
    return VGroup(c, ar, rl, d)


class B20_Flip(Scene):
    def construct(self):
        r = 1.3; cy = 0.35
        left = a3_circ(-3.4, cy, r, True)
        right = a3_circ(3.4, cy, r, False)
        l1 = T("on paper", 40).move_to([-3.4, -1.8, 0])
        l2 = T("on a screen", 40).move_to([3.4, -1.8, 0])
        y1 = T("y", 32, DIM).move_to([-3.4 - r - 0.6 - 0.45, cy, 0])
        y2 = T("y", 32, DIM).move_to([3.4 - r - 0.6 - 0.45, cy, 0])
        credit = T("Godot docs  ·  y is down in 2D", 32, DIM).move_to([0, -3.0, 0])
        self.play(Create(left), FadeIn(l1), FadeIn(y1), run_time=0.8)
        until(self, "On a screen", lead=0.2)
        moving = left.copy()
        self.play(ReplacementTransform(moving, right), FadeIn(l2), FadeIn(y2), run_time=1.4)
        self.play(FadeIn(credit), run_time=0.4)
        until(self, "and a growing angle", lead=0.3)
        dot = right[3]
        a = ValueTracker(90.0)
        runner = always_redraw(lambda: Dot([3.4 + r * np.cos(np.radians(a.get_value())), cy - r * np.sin(np.radians(a.get_value())), 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3))
        arc_r = r + 0.35
        back = Arc(radius=arc_r, start_angle=-PI / 2, angle=-5 * PI / 3, arc_center=[3.4, cy, 0], stroke_color=DIM, stroke_width=18, stroke_opacity=0.55)
        arc = Arc(radius=arc_r, start_angle=-PI / 2, angle=-5 * PI / 3, arc_center=[3.4, cy, 0], stroke_color=TERRA, stroke_width=10)
        th = -PI / 2 - 5 * PI / 3
        endp = np.array([3.4 + arc_r * np.cos(th), cy + arc_r * np.sin(th), 0.0])
        tip = Triangle(fill_color=TERRA, fill_opacity=1, stroke_color=DIM, stroke_width=3).scale(0.26)
        tip.rotate(np.arctan2(-np.cos(th), np.sin(th)) - PI / 2).move_to(endp)
        self.remove(dot)
        self.add(runner)
        self.play(a.animate.set_value(450.0), Create(back), Create(arc), run_time=2.2, rate_func=linear)
        self.play(FadeIn(tip), run_time=0.2)
        done(self)


# ═════════════════════════════ B25 · the recipe ═════════════════════════════
def a3_slider(label, x, y, w=3.2):
    track = Line([x - w / 2, y, 0], [x + w / 2, y, 0], color=DIM, stroke_width=7)
    cap = T(label, 36).move_to([x, y + 0.5, 0])
    knob = Dot([x - w / 2 + 0.25 * w, y, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3)
    g = VGroup(track, cap, knob)
    g.knob = knob; g.track = track; g.x0 = x - w / 2; g.w = w; g.y = y
    return g


def a3_at(sl, f):
    return np.array([sl.x0 + f * sl.w, sl.y, 0])


class B25_Recipe(Scene):
    def construct(self):
        cw = 0.248          # measured width of one Menlo glyph at 32 pt
        text = "center + radius * vec2(cos(a), sin(a))"
        left_x = -len(text) * cw / 2.0
        parts = {}
        for name, (i0, s) in {"center": (0, "center"), "plus": (7, "+"), "radius": (9, "radius"), "star": (16, "*"), "v": (18, "vec2(cos("), "a1": (27, "a"),
                                "m": (28, "),"), "s": (31, "sin("), "a2": (35, "a"), "e": (36, "))")}.items():
            m = M(s, 32)
            m.move_to([left_x + cw * (i0 + len(s) / 2.0), 2.6, 0])
            parts[name] = m
        line = VGroup(*parts.values())
        # orbit
        K = 2.2
        cx = ValueTracker(-3.3); R = ValueTracker(0.4); sp = ValueTracker(1.0); ang = ValueTracker(0.6)
        cyy = -0.45
        ringm = always_redraw(lambda: Circle(radius=K * R.get_value(), stroke_color=DIM, stroke_width=4).move_to([cx.get_value(), cyy, 0]))
        planet = always_redraw(lambda: Circle(radius=0.42, stroke_color=A3_PLANET, stroke_width=0).set_fill(A3_PLANET, opacity=1).move_to([cx.get_value(), cyy, 0]))
        moon_pos = lambda: np.array([cx.get_value() + K * R.get_value() * np.cos(ang.get_value()), cyy + K * R.get_value() * np.sin(ang.get_value()), 0])
        moon = always_redraw(lambda: Dot(moon_pos(), radius=0.2, color=A3_MOON))
        ang.add_updater(lambda m, dt: m.increment_value(dt * sp.get_value()))
        s_r = a3_slider("radius", 3.9, 1.25); s_c = a3_slider("center", 3.9, -0.15); s_s = a3_slider("speed", 3.9, -1.55)
        self.add(ringm, planet, moon)
        self.play(FadeIn(line), *[Create(s) for s in (s_r, s_c, s_s)], run_time=0.8)
        # the speed marks: two short strokes trailing the moon, shown while fast
        trail_on = ValueTracker(0.0)

        def speed_marks():
            op = trail_on.get_value()
            a = ang.get_value()
            tang = np.array([np.sin(a), -np.cos(a), 0.0])        # opposite to the direction of travel
            p = moon_pos()
            return VGroup(*[Line(p + tang * (0.38 + 0.3 * k), p + tang * (0.55 + 0.3 * k), color=INK, stroke_width=6, stroke_opacity=op) for k in range(2)])
        sm = always_redraw(speed_marks)
        self.add(sm)

        def hit(keys, mobs=None):
            # terracotta underline bars over a grey backing (a bar, never text; the ring read as accent text)
            return VGroup(*[VGroup(Rectangle(width=parts[k].width + 0.2, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).next_to(parts[k], DOWN, buff=0.08),
                                   Rectangle(width=parts[k].width + 0.2, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).next_to(parts[k], DOWN, buff=0.12)) for k in keys])

        until(self, "The radius sets", lead=0.35)
        h1 = hit(["radius"])
        self.play(FadeIn(h1), s_r.knob.animate.move_to(a3_at(s_r, 0.75)), R.animate.set_value(0.8), run_time=1.2)
        until(self, "The center sets", lead=0.3)
        h2 = hit(["center"])
        self.play(FadeOut(h1), FadeIn(h2), s_c.knob.animate.move_to(a3_at(s_c, 0.75)), cx.animate.set_value(-1.0), run_time=1.3)
        until(self, "The angle's speed", lead=0.3)
        h3 = hit(["a1", "a2"])
        self.play(FadeOut(h2), FadeIn(h3), s_s.knob.animate.move_to(a3_at(s_s, 0.8)), sp.animate.set_value(3.0), trail_on.animate.set_value(1.0), run_time=1.0)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · An Orbit Around an Orbit  (B26, B30; Manim)

Cast: screen orientation for B26 (y down: a screen angle a puts a point at c + r*(cos a, -sin a) in scene coordinates); planet teal, moon slate-blue,
meteor amber, the same colours as the Lab renders. B30 is a drawing of the pattern (labelled by its two lines), paper orientation.
"""
A4_PLANET = "#5EA391"; A4_MOON = "#8099BF"; A4_METEOR = "#E6A640"


def a4_pt(c, r, a):
    """Scene point of a SCREEN angle a (clockwise, y down) at radius r round c (a scene point)."""
    return np.array([c[0] + r * np.cos(a), c[1] - r * np.sin(a), 0.0])


def a4_shaft(p, q, t0, t1, color=INK, w=9):
    """A thick arrow from p to q shortened by t0 at the tail and t1 at the tip (so it stops at the edge of a body)."""
    u = (q - p) / max(1e-6, np.linalg.norm(q - p))
    return arrow(p + u * t0, q - u * t1, color=color, w=w, tip=0.3)


class B26_Chain(Scene):
    def construct(self):
        title = T("An Orbit Around an Orbit", 40).to_corner(UL, buff=0.95)
        P = np.array([-0.9, -0.45, 0.0]); R = 2.55; r2 = 1.25
        am = ValueTracker(0.1); ab = ValueTracker(-2.3)
        moon_at = lambda: a4_pt(P, R, am.get_value())
        met_at = lambda: a4_pt(moon_at(), r2, ab.get_value())
        planet = Circle(radius=0.5, fill_color=A4_PLANET, fill_opacity=1, stroke_width=0).move_to(P)
        big_ring = Circle(radius=R, stroke_color=DIM, stroke_width=4).move_to(P)
        moon = always_redraw(lambda: Circle(radius=0.3, fill_color=A4_MOON, fill_opacity=1, stroke_width=0).move_to(moon_at()))
        small_ring = always_redraw(lambda: Circle(radius=r2, stroke_color=DIM, stroke_width=4).move_to(moon_at()))
        meteor = always_redraw(lambda: Circle(radius=0.2, fill_color=A4_METEOR, fill_opacity=1, stroke_width=0).move_to(met_at()))
        arr1 = always_redraw(lambda: a4_shaft(P, moon_at(), 0.5, 0.34))
        arr2 = always_redraw(lambda: a4_shaft(moon_at(), met_at(), 0.34, 0.24))
        dash = always_redraw(lambda: DashedLine(P, met_at(), color=DIM, stroke_width=5, dash_length=0.18))

        def lab(word, f, side, t=0.5, off=0.62):
            def mk():
                a, b = f()
                m = a + (b - a) * t; d = b - a
                n = np.array([-d[1], d[0], 0.0]); n = n / max(1e-6, np.linalg.norm(n)) * side
                return T(word, 32).move_to(m + n * off)
            return always_redraw(mk)
        l_moon = lab("moon", lambda: (P, moon_at()), -1, 0.4, 0.55)
        def mk_met():
            m0, m1 = moon_at(), met_at(); u = (m1 - m0) / np.linalg.norm(m1 - m0)
            return T("meteor", 32).move_to(m1 + u * 0.3 + np.array([u[0] * 0.55, u[1] * 0.3, 0]))
        l_met = always_redraw(mk_met)

        self.add(title, planet, big_ring)
        until(self, "Now a meteor")
        self.play(FadeIn(moon, scale=0.6), run_time=0.5)
        until(self, "The moon moves")
        self.play(FadeIn(arr1), FadeIn(l_moon), run_time=0.6)
        self.play(FadeIn(small_ring), FadeIn(meteor, scale=0.6), run_time=0.5)
        self.play(FadeIn(arr2), FadeIn(l_met), run_time=0.6)
        self.play(FadeIn(dash), run_time=0.5)
        until(self, "Positions add")
        self.play(am.animate.set_value(0.1 + 0.4), ab.animate.set_value(-0.8), run_time=1.8, rate_func=linear)
        done(self)


# ─────────────────────────── B30 · the arm ───────────────────────────
def a4_up(p, L, a):
    """Paper-orientation endpoint (y up) of a segment of length L at angle a from p."""
    return np.array([p[0] + L * np.cos(a), p[1] + L * np.sin(a), 0.0])


class B30_Arm(Scene):
    def construct(self):
        S0 = np.array([-2.0, -1.1, 0.0]); L1, L2, L3 = 2.3, 1.9, 1.5
        a1 = ValueTracker(0.6); a2 = ValueTracker(0.2); a3 = ValueTracker(0.5); k3 = ValueTracker(0.0)
        e1 = lambda: a4_up(S0, L1, a1.get_value())
        e2 = lambda: a4_up(e1(), L2, a2.get_value())
        e3 = lambda: a4_up(e2(), L3 * max(0.001, k3.get_value()), a3.get_value())
        seg1 = always_redraw(lambda: Line(S0, e1(), color=INK, stroke_width=14))
        seg2 = always_redraw(lambda: Line(e1(), e2(), color=INK, stroke_width=14))
        seg3 = always_redraw(lambda: Line(e2(), e3(), color=INK, stroke_width=14))
        j1 = always_redraw(lambda: Dot(e1(), radius=0.17, color=TEAL))
        j2 = always_redraw(lambda: Dot(e2(), radius=0.17, color=TEAL))
        j3 = always_redraw(lambda: Dot(e3(), radius=0.17, color=TEAL))
        shoulder = Dot(S0, radius=0.2, color=TERRA).set_stroke(DIM, width=3)

        l1 = M("center + radius * vec2(cos(a), sin(a))", 32)
        l1.move_to([-5.9 + l1.width / 2, -2.3, 0])
        l2 = M("elbow  + radius * vec2(cos(b), sin(b))", 32)
        l2.move_to([-5.9 + l2.width / 2, -3.0, 0])
        lab_e = always_redraw(lambda: T("elbow", 32).move_to(e1() + np.array([0.15, 0.55, 0])))
        lab_h = always_redraw(lambda: T("hand", 32).move_to((e3() if k3.get_value() > 0.05 else e2()) + np.array([0.75, 0.0, 0])))

        self.add(shoulder)
        until(self, "Any depth works", lead=0.0)
        self.play(Create(seg1), FadeIn(j1), run_time=0.7)
        self.add(seg1, j1)
        self.play(FadeIn(l1), run_time=0.5)
        until(self, "Each level")
        self.play(Create(seg2), FadeIn(j2), run_time=0.7)
        self.add(seg2, j2)
        self.play(FadeIn(l2), run_time=0.5)
        # a small wave of the two segments, back to rest before the midpoint
        self.play(a1.animate.set_value(0.85), a2.animate.set_value(0.0), run_time=0.8)
        self.play(a1.animate.set_value(0.6), a2.animate.set_value(0.2), run_time=0.8)
        until(self, "Chain two")
        self.play(FadeIn(lab_e), FadeIn(lab_h), run_time=0.5)
        until(self, "Chain three")
        self.add(seg3, j3)
        self.play(k3.animate.set_value(1.0), run_time=0.7)
        self.play(a1.animate.set_value(0.35), a2.animate.set_value(0.55), a3.animate.set_value(0.0), run_time=0.9)
        self.play(a1.animate.set_value(0.75), a2.animate.set_value(0.05), a3.animate.set_value(0.9), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Angle from a Position  (B31, B32, B34, B37; Manim)

Cast: the circle with the pixel dot, SCREEN orientation (y down): a screen angle s puts a point at c + r*(cos s, -sin s) in scene coordinates;
the arc tangent of a pixel p = (x, y) with y down is atan2(y, x). Terracotta only as dots, thick arcs and rings.
"""


def a5_pt(c, r, s):
    return np.array([c[0] + r * np.cos(s), c[1] - r * np.sin(s), 0.0])


def a5_axes(c, r):
    """Small grey axes, the screen way: x to the right, y pointing DOWN."""
    ax = arrow(c + np.array([0.0, 0.0, 0.0]), c + np.array([r + 0.5, 0, 0]), color=DIM, w=4, tip=0.2)
    ay = arrow(c, c + np.array([0, -(r + 0.3), 0]), color=DIM, w=4, tip=0.2)
    lx = T("x", 32, DIM).move_to(c + np.array([r + 0.85, 0, 0]))
    ly = T("y", 32, DIM).move_to(c + np.array([0.4, -(r + 0.15), 0]))
    return VGroup(ax, ay, lx, ly)


def a5_dot(p, r=0.17):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════════ B31 · two ways ═════════════════════════════
class B31_TwoWays(Scene):
    def construct(self):
        title = T("Angle from a Position", 40).to_corner(UL, buff=0.95)
        c = np.array([0.5, 0.1, 0.0]); r = 1.7; s0 = 0.61
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a5_axes(c, r)
        dot = a5_dot(a5_pt(c, r, s0))
        radial = Line(c, a5_pt(c, r, s0), color=DIM, stroke_width=4)
        arc = Arc(radius=1.1, start_angle=0, angle=-s0, arc_center=c, color=TERRA, stroke_width=11)
        arc_back = Arc(radius=1.1, start_angle=0, angle=-s0, arc_center=c, color=DIM, stroke_width=18, stroke_opacity=0.5)
        fwd = arrow([-0.2, 2.35, 0], [4.6, 2.35, 0], color=INK, w=7)
        fwd_l = T("angle in, position out", 32).move_to([2.2, 2.9, 0])
        bwd = arrow([4.6, -2.5, 0], [-0.2, -2.5, 0], color=INK, w=7)
        bwd_l = T("position in, angle out", 32).move_to([2.2, -2.98, 0])
        q = T("?", 40).move_to(a5_pt(c, r + 0.75, s0 / 2))
        word = T("angle", 32).move_to(a5_pt(c, r + 0.85, s0 / 2))

        self.add(title, circ, axes, radial, dot)
        self.wait(0.4)
        self.play(GrowArrow(fwd), FadeIn(fwd_l), run_time=0.6)
        self.play(FadeIn(arc_back), Create(arc), run_time=1.4, rate_func=smooth)
        until(self, "A pixel knows")
        self.play(GrowArrow(bwd), FadeIn(bwd_l), run_time=0.7)
        self.play(FadeIn(q), run_time=0.4)
        until(self, "What angle")
        self.play(ReplacementTransform(q, word), run_time=0.5)
        done(self)


# ═════════════════════════════ B32 · arc tangent: two sides in, angle out ═════════════════════════════
class B32_AtanIdea(Scene):
    def construct(self):
        S = 5.0
        O = np.array([-5.0, 1.5, 0.0])
        A = O + np.array([0.5 * S, 0, 0])
        P = O + np.array([0.5 * S, -0.35 * S, 0])
        hyp = Line(O, P, color=INK, stroke_width=7)
        adj = Line(O, A, color=INK, stroke_width=7)
        opp = Line(A, P, color=INK, stroke_width=7)
        mid_dot = Dot(O, radius=0.1, color=DIM)
        pix = a5_dot(P)
        arc = Arc(radius=1.1, start_angle=0, angle=-np.arctan2(0.35, 0.5), arc_center=O, color=TERRA, stroke_width=11)
        arc_back = Arc(radius=1.1, start_angle=0, angle=-np.arctan2(0.35, 0.5), arc_center=O, color=DIM, stroke_width=18, stroke_opacity=0.5)
        l_adj = T("adjacent", 32).move_to(O + np.array([1.25, 0.45, 0]))
        l_opp = T("opposite", 32).move_to(A + np.array([1.05, -0.65, 0]))
        l_ang = T("angle?", 32).move_to(O + np.array([0.55, -1.3, 0]))
        bx = box(2.9, 0.9, 3.3, 1.1, color=INK, sw=5)
        bt = T("arc tangent", 32).move_to(bx.get_center())
        t_opp = T("0.35", 32).move_to(A + np.array([0.9, -1.45, 0]))
        t_adj = T("0.5", 32).move_to(A + np.array([0.7, 0.45, 0]))
        out = arrow([2.9, 0.3, 0], [2.9, -1.0, 0], color=INK, w=7)
        out_l = T("angle", 32).move_to([4.15, -0.65, 0])
        res = T("0.61 rad", 32).move_to(l_ang.get_center())
        down = T("down", 32).move_to(l_opp.get_center())
        across = T("across", 32).move_to(l_adj.get_center())

        self.add(mid_dot, adj, opp, hyp)
        until(self, "Tangent was", lead=0.0)
        self.play(FadeIn(pix), FadeIn(l_adj), FadeIn(l_opp), run_time=0.6)
        self.play(FadeIn(arc_back), Create(arc), FadeIn(l_ang), run_time=0.7)
        until(self, "Arc tangent undoes")
        self.play(FadeIn(bx), FadeIn(bt), run_time=0.5)
        # the two numbers travel into the box, the angle comes out
        self.play(FadeIn(t_opp), FadeIn(t_adj), run_time=0.3)
        self.play(t_opp.animate.move_to([0.65, 0.65, 0]), t_adj.animate.move_to([0.65, 1.15, 0]), run_time=0.9, rate_func=smooth)
        self.play(FadeOut(t_opp), FadeOut(t_adj), GrowArrow(out), FadeIn(out_l), run_time=0.5)
        self.play(ReplacementTransform(l_ang, res), run_time=0.5)
        until(self, "For a pixel")
        self.play(ReplacementTransform(l_adj, across), ReplacementTransform(l_opp, down), run_time=0.6)
        done(self)


# ═════════════════════════════ B34 · the compass and the seam ═════════════════════════════
def a5_atan(s):
    """arc tangent of the dot at screen angle s: atan2(sin s, cos s) with y down (what the shader sees)."""
    return float(np.arctan2(np.sin(s), np.cos(s)))


class B34_Compass(Scene):
    def construct(self):
        c = np.array([-1.6, 0.0, 0.0]); r = 2.3
        s = ValueTracker(0.0)
        circ = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to(c)
        axes = a5_axes(c, r)
        dot = always_redraw(lambda: a5_dot(a5_pt(c, r, s.get_value()), 0.2))
        rb = box(3.9, 0.1, 3.5, 2.4, color=INK, sw=4)
        rt = T("arc tangent", 32).move_to([3.9, 0.85, 0])
        readout = always_redraw(lambda: T("%.2f" % (a5_atan(s.get_value()) + 0.0 if abs(a5_atan(s.get_value())) > 0.005 else 0.0), 56).move_to([3.9, -0.15, 0]))
        flash = ring(rb, pad=0.1)
        seam = Line(c + np.array([-r - 0.3, 0, 0]), c + np.array([-r + 0.3, 0, 0]), color=DIM, stroke_width=14)
        seam_l = T("seam", 32).move_to(c + np.array([-r - 0.95, 0.5, 0]))
        ghost = lambda a: Dot(a5_pt(c, r, a), radius=0.09, color=DIM)

        self.add(circ, axes, rb, rt, readout, dot)
        until(self, "Straight down")
        self.play(s.animate.set_value(np.pi / 2), run_time=1.0)
        self.add(ghost(np.pi / 2))
        until(self, "Straight left")
        self.play(s.animate.set_value(np.pi - 0.002), run_time=1.2, rate_func=smooth)
        self.play(FadeIn(seam), FadeIn(seam_l), run_time=0.4)
        until(self, "nearly minus pi")
        self.play(FadeIn(flash), s.animate.set_value(np.pi + 0.002), run_time=0.3, rate_func=linear)
        self.play(FadeOut(flash), run_time=0.4)
        until(self, "Past the wrap")
        self.play(s.animate.set_value(1.5 * np.pi), run_time=0.9)
        self.add(ghost(1.5 * np.pi))
        until(self, "straight up is")
        self.play(s.animate.set_value(2 * np.pi), run_time=0.9)
        done(self)


# ═════════════════════════════ B37 · one pixel by hand ═════════════════════════════
class B37_WorkedPixel(Scene):
    def construct(self):
        sq = 3.2; c = np.array([-4.3, 1.0, 0.0])
        frame = Square(side_length=sq, stroke_color=INK, stroke_width=5).move_to(c)
        cross = VGroup(Line(c + np.array([-sq / 2, 0, 0]), c + np.array([sq / 2, 0, 0]), color=DIM, stroke_width=3),
                       Line(c + np.array([0, -sq / 2, 0]), c + np.array([0, sq / 2, 0]), color=DIM, stroke_width=3))
        mid = Dot(c, radius=0.09, color=DIM)
        pp = c + np.array([-0.3, 0.3, 0]) * (sq / 2)
        dot = a5_dot(pp)
        pl = T("p", 36).move_to(pp + np.array([-0.4, 0.3, 0]))
        head = M("p = (-0.3, -0.3)", 32).move_to([-2.2 + 2.0, 2.6, 0]); head.move_to([-2.2 + head.width / 2, 2.6, 0])
        L = [M("atan(-0.3, -0.3) = -3 * PI / 4", 32), M("÷ TAU = -0.375", 32), M("+ 0.5 = 0.125", 32)]
        for i, t in enumerate(L):
            t.move_to([-2.2 + t.width / 2, 1.3 - 0.95 * i, 0])
        rs = ramp_strip(width=4.0, x=-3.9, y=-2.2, labels=True)
        mk = ramp_marker(rs, 0.125, r=0.18)
        eighth = T("1/8", 32).move_to([rs.x0 + rs.width_s * 0.125, -1.6, 0])

        self.add(frame, cross, mid)
        self.play(FadeIn(dot, scale=0.5), FadeIn(pl), FadeIn(head), run_time=0.6)
        self.play(FadeIn(rs), run_time=0.4)
        until(self, "Arc tangent says")
        self.play(FadeIn(L[0], shift=RIGHT * 0.2), run_time=0.7)
        until(self, "Divide by tau")
        self.play(FadeIn(L[1], shift=RIGHT * 0.2), run_time=0.6)
        until(self, "Add one half")
        self.play(FadeIn(L[2], shift=RIGHT * 0.2), run_time=0.6)
        until(self, "One eighth")
        self.play(FadeIn(mk, scale=0.5), FadeIn(eighth), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
