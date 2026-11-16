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


# ═════════════════ _kit_extra.py: this film's four helpers (pasted above the scenes by assemble_scenes.py) ═════════════════
# The standard plot (SHOTLIST.md): square axes, a curve, a terracotta dot riding it, a dashed drop line to a ramp strip of 64 narrow tiles in TRUE grays
# (value v drawn as gray v) under the axes at the same x scale. Curves come from evidence/planning-checks/plot_data.py (the shader's own formulas).
import sys as _sys
_sys.path.insert(0, "evidence/planning-checks")
try:
    import plot_data as PD
except Exception:
    PD = None


def plot_with_strip(fn, x=0.0, y=0.5, size=4.4, y_range=(0.0, 1.0), strip=True, n=64, tracker=None):
    """fn: numpy function of x in 0..1 (use PD.CURVES[name][1]). Returns VGroup with .axes, .curve, .dot, .drop, .tiles, .tracker (ValueTracker of x),
    .pt(xv) -> point on the curve, .x0/.x1/.ystrip (strip geometry). Animate with g.tracker.animate.set_value(v); dot and drop follow by updaters."""
    h = size
    x0, y0 = x - size / 2, y - h / 2
    axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + h, 0], color=INK, stroke_width=5))
    lo, hi = y_range

    def pt(xv):
        return np.array([x0 + xv * size, y0 + (float(fn(np.array([xv]))[0]) - lo) / (hi - lo) * h, 0.0])
    xs = np.linspace(0, 1, 120)
    curve = VMobject(stroke_color=DIM, stroke_width=7).set_points_smoothly([pt(v) for v in xs]) if False else VMobject(stroke_color="#6B6760", stroke_width=7)
    curve.set_points_as_corners([pt(v) for v in xs])
    tr = tracker or ValueTracker(0.0)
    dot = Dot(pt(0.0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    dot.add_updater(lambda m: m.move_to(pt(tr.get_value())))
    ystrip = y0 - 0.95
    drop = DashedLine(pt(0.0), [x0, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
    drop.add_updater(lambda m: m.become(DashedLine(pt(tr.get_value()), [x0 + tr.get_value() * size, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)))
    tiles = VGroup()
    if strip:
        pitch = size / n
        for i in range(n):
            v = i / (n - 1)
            g = int(round(255 * v))
            tiles.add(Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (g, g, g), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ystrip, 0]))
    l0 = T("0", 32).move_to([x0, y0 - 0.38, 0]); l1 = T("1", 32).move_to([x0 + size, y0 - 0.38, 0])
    lab = VGroup(l0, l1, T("input", 32).move_to([x + 0.0, y0 - 0.38, 0]))
    out = VGroup(axes, curve, tiles, lab)
    out.axes = axes; out.curve = curve; out.dot = dot; out.drop = drop; out.tiles = tiles; out.tracker = tr; out.pt = pt
    out.x0 = x0; out.x1 = x0 + size; out.ystrip = ystrip; out.y0 = y0; out.size = size
    return out


def number_line(x0, x1, y, lo=0.0, hi=1.0, ticks=(0.0, 1.0), color=INK, size=32):
    """A horizontal number line with labelled ticks. Returns VGroup with .at(v) -> scene point."""
    line = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=5)
    g = VGroup(line)
    at = lambda v: np.array([x0 + (v - lo) / (hi - lo) * (x1 - x0), y, 0.0])
    for t in ticks:
        p = at(t)
        g.add(Line(p + [0, 0.12, 0], p - [0, 0.12, 0], color=color, stroke_width=5), T(("%g" % t), size).move_to(p - [0, 0.45, 0]))
    g.at = at
    return g


def vec_arrow(a, b, color=INK, w=6):
    """An arrow from a to b (scene points) drawn as a shape."""
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=0.22, max_tip_length_to_length_ratio=0.45)


def chip(text, x, y, size=32):
    """A mono function-name chip: outlined rounded box (no fill behind text), Menlo text."""
    t = M(text, size)
    box_ = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.35, corner_radius=0.14, stroke_color=INK, stroke_width=3)
    g = VGroup(box_, t).move_to([x, y, 0])
    g.box = box_; g.label = t
    return g




# ══════════════════════════════ scenes_act1.py ══════════════════════════════
"""ACT I · Ramps and Plots (B02, B04, B05, B06).  Manim scenes; kit + _kit_extra pasted above by the assembler.
Cast: the ramp strip (64 narrow true-gray tiles with gaps) with its terracotta dot; the standard plot frame (axes, curve, dot, drop line, strip)."""


def a1_tag(s, x, y, size=32):
    return M(s, size).move_to([x, y, 0])


def a1_plot(fn_ref, x=-2.4, y=0.85, size=3.8):
    """The standard plot via plot_with_strip, with a1 fixes: the 'input' label moved off the drop line, strip end labels, an 'output' label up the side.
    fn_ref is a callable on a numpy array (may read a mutable blend)."""
    g = plot_with_strip(fn_ref, x=x, y=y, size=size)
    lab = g[3]
    lab[2].move_to([g.x1 + 1.0, g.y0 - 0.38, 0])
    out_l = T("output", 32).rotate(PI / 2).move_to([g.x0 - 0.5, g.y0 + size / 2 + 0.2, 0])
    one = T("1", 32).move_to([g.x0 - 0.3, g.y0 + size, 0])
    s0 = T("0", 32).move_to([g.x0, g.ystrip - 0.55, 0]); s1 = T("1", 32).move_to([g.x1, g.ystrip - 0.55, 0])
    g.axlabels = VGroup(one)   # the bottom 0/1 ticks are dropped: the drop line crosses them; the strip end labels carry 0 and 1
    g.input_lab = lab[2]; g.output_lab = VGroup(out_l); g.stripends = VGroup(s0, s1)
    return g


def a1_fill_updater(g, level):
    """Tiles whose centre x is left of the drop line become visible (true gray stays)."""
    tiles = g.tiles
    pitch = g.size / len(tiles)

    def upd(m):
        lim = g.x0 + g.tracker.get_value() * g.size + pitch * 0.6
        for t in m:
            t.set_fill(opacity=1.0 if t.get_center()[0] <= lim else 0.0)
    return upd


def a1_gray_strip(width=9.6, n=64, height=0.9, y=0.2):
    """ramp_strip's shape with TRUE grays (value v drawn as gray v) per the standard-plot law; kit ramp_strip is a teal-cream ramp."""
    pitch = width / n
    tiles = VGroup()
    for i in range(n):
        gg = int(round(255 * i / (n - 1)))
        tiles.add(Rectangle(width=pitch * 0.78, height=height, fill_color="#%02x%02x%02x" % (gg, gg, gg), fill_opacity=1, stroke_width=0).move_to([-width / 2 + pitch * (i + 0.5), y, 0]))
    g = VGroup(tiles, T("0", 32).move_to([-width / 2, y - height / 2 - 0.35, 0]), T("1", 32).move_to([width / 2, y - height / 2 - 0.35, 0]))
    g.x0 = -width / 2; g.x1 = width / 2; g.y = y; g.width_s = width
    return g


class B02_RampStrip(Scene):
    def construct(self):
        st = a1_gray_strip()
        self.add(st)
        cap = VGroup(T("ramp", 44, bold=True), T("a smooth run of values from 0 up to 1", 32)).arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to([0, 2.3, 0])
        until(self, "Start with a ramp", lead=0.1)
        self.play(FadeIn(cap), run_time=0.8)
        until(self, "The simplest ramp")
        tr = ValueTracker(0.0)
        dot = Dot([st.x0, st.y, 0], radius=0.2, color=TERRA).set_stroke(DIM, width=3)
        dot.add_updater(lambda m: m.move_to([st.x0 + st.width_s * tr.get_value(), st.y, 0]))
        lbl = always_redraw(lambda: T("pixel  %.1f" % tr.get_value(), 32).move_to([max(st.x0 + 0.4, min(st.x1 - 0.8, st.x0 + st.width_s * tr.get_value())), st.y + 1.0, 0]))
        self.play(FadeIn(dot, scale=0.4), FadeIn(lbl), run_time=0.6)
        until(self, "zero at the left edge")
        self.play(tr.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        until(self, "In code")
        tag = a1_tag("UV.x  ·  across the shape", 0, -1.75)
        self.play(FadeIn(tag), run_time=0.6)
        done(self)


class B04_ReadThePlot(Scene):
    def construct(self):
        g = a1_plot(lambda xs: PD.CURVES["identity"][1](xs) if PD else xs)
        g.tiles.set_fill(opacity=0)
        self.add(g.axes, g.axlabels)
        ghost = Rectangle(width=g.size + 0.15, height=0.62, stroke_color=GHOST, stroke_width=3).move_to([g.x0 + g.size / 2, g.ystrip, 0])
        until(self, "The input runs")
        self.play(FadeIn(g.input_lab), run_time=0.6)
        until(self, "the output up the side")
        self.play(FadeIn(g.output_lab), run_time=0.6)
        until(self, "A dot travels", lead=1.4)
        g.tiles.add_updater(a1_fill_updater(g, 0))
        self.add(g.tiles)
        self.play(Create(g.curve), FadeIn(ghost), FadeIn(g.stripends), run_time=1.0)
        g.tracker.set_value(0.0)
        self.add(g.drop, g.dot)
        self.play(FadeIn(g.dot, scale=0.4), run_time=0.4)
        self.play(g.tracker.animate.set_value(0.5), run_time=0.7)
        until(self, "and the strip below shows", lead=0.0)
        self.play(g.tracker.animate.set_value(1.0), run_time=2.2, rate_func=linear)
        until(self, "A function that changes nothing")
        tag = a1_tag("f(x) = x", 3.3, 1.9)
        credit = T("curves drawn from the formulas  ·  checked against Godot 4.7.2 renders", 32, color=DIM).move_to([0, -3.05, 0])
        self.play(g.curve.animate.set_stroke(color=INK, width=10), FadeIn(tag), FadeIn(credit), run_time=0.8)
        done(self)


class B05_BendTheLine(Scene):
    def construct(self):
        K = [0.0]   # line blend: 0 = x, 1 = 1 - x
        S = ValueTracker(0.0)   # strip blend
        kt = ValueTracker(0.0)
        fn = lambda xs: (1 - K[0]) * xs + K[0] * (1 - xs)
        g = a1_plot(fn)
        # curve and tiles follow the blends
        xs = np.linspace(0, 1, 120)

        def curve_upd(m):
            K[0] = kt.get_value()
            m.set_points_as_corners([g.pt(v) for v in xs])
        g.curve.add_updater(curve_upd)
        pitch = g.size / 64

        def tile_upd(m):
            s = S.get_value()
            for i, t in enumerate(m):
                v0 = i / 63.0
                v = (1 - s) * v0 + s * (1 - v0)
                gg = int(round(255 * v))
                t.set_fill(color="#%02x%02x%02x" % (gg, gg, gg), opacity=1)
        g.tiles.add_updater(tile_upd)
        g.curve.set_stroke(color=INK, width=10)
        ghost = Rectangle(width=g.size + 0.15, height=0.62, stroke_color=GHOST, stroke_width=3).move_to([g.x0 + g.size / 2, g.ystrip, 0])
        tag = a1_tag("f(x) = x", 3.3, 1.9)
        self.add(g.axes, g.axlabels, g.input_lab, g.output_lab, g.stripends, ghost, g.tiles, g.curve, tag)
        until(self, "Bend the line", lead=0.0)
        self.wait(0.3)
        until(self, "Here the function is one minus x", lead=0.6)
        tag2 = a1_tag("f(x) = 1 - x", 3.3, 1.9)
        self.play(FadeTransform(tag, tag2), kt.animate.set_value(1.0), run_time=1.7)
        until(self, "The line runs downhill", lead=0.0)
        g.tracker.set_value(0.0)
        self.add(g.drop, g.dot)
        self.play(FadeIn(g.dot, scale=0.4), run_time=0.4)
        self.play(g.tracker.animate.set_value(0.5), run_time=0.6)
        # midpoint hold: strip still shows the old ramp
        until(self, "so the strip runs from white to black", lead=0.0)
        self.play(S.animate.set_value(1.0), run_time=1.0)
        until(self, "Read the line", lead=0.5)
        cap = T("predict the strip", 32, color=INK).move_to([3.3, -1.2, 0])
        self.play(g.tracker.animate.set_value(1.0), FadeIn(cap), run_time=1.6, rate_func=linear)
        done(self)


def a1_chip(text, x, y):
    t = M(text, 32)
    b = RoundedRectangle(width=t.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3)
    g = VGroup(b, t).move_to([x, y, 0])
    return g


class B06_ToolkitMap(Scene):
    def construct(self):
        cols = [(-4.6, "Cut and blend", ["step", "smoothstep", "mix", "clamp"]),
                (-1.5, "Repeat and fold", ["abs", "fract", "floor", "mod"]),
                (2.35, "Distance and curves", ["length", "normalize", "distance", "pow", "sin"])]
        rows = [1.35, 0.5, -0.35, -1.2, -2.05]
        ring_c = np.array([5.45, -0.35, 0.0])
        titles = []; chips = []
        for cx, ttl, names in cols:
            titles.append(T(ttl, 32, bold=True).move_to([cx, 2.35, 0]))
            chips.append([a1_chip(n, cx, rows[i]) for i, n in enumerate(names)])
        outline = Annulus(inner_radius=0.5, outer_radius=0.8, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to(ring_c)
        self.add(outline)
        until(self, "About a dozen", lead=0.0)
        self.play(*[FadeIn(t) for t in titles], run_time=0.8)
        until(self, "Cut and blend:", lead=0.0)
        for c in chips[0]:
            self.play(FadeIn(c, scale=0.7), run_time=0.35)
            self.wait(0.15)
        until(self, "Repeat and fold:", lead=0.0)
        self.play(*[FadeIn(c, scale=0.7) for c in chips[1]], run_time=0.5)
        until(self, "Distance and curves:", lead=0.9)
        self.play(*[FadeIn(c, scale=0.7) for c in chips[2]], run_time=0.5)
        until(self, "Then we use three")
        # routes: smoothstep -> gap above mix row; mix -> gap below mix row; distance straight
        sm = chips[0][1]; mx = chips[0][2]; di = chips[2][2]
        def route(chip_, gap_y, tgt_dy):
            p0 = chip_.get_right() + np.array([0.0, 0.0, 0.0])
            p1 = np.array([p0[0] + 0.12, gap_y, 0.0]); p2 = np.array([4.3, gap_y, 0.0])
            p3 = ring_c + np.array([-0.8, tgt_dy, 0.0])
            return VMobject(stroke_color=DIM, stroke_width=3).set_points_as_corners([p0, p1, p2, p3])
        lines = [route(sm, 0.075, 0.30), route(mx, -0.775, -0.30), route(di, di.get_center()[1], 0.0)]
        self.play(*[Create(l) for l in lines], run_time=1.4)
        fill = Annulus(inner_radius=0.5, outer_radius=0.8, fill_opacity=0.95, fill_color=TEAL, stroke_color=INK, stroke_width=5).move_to(ring_c)
        self.play(FadeIn(fill), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Cut and Blend  (B07, B09, B10, B11, B14, B16: all Manim; B08, B12, B13, B15 are captures)

Cast for the act: the series' STANDARD PLOT (square axes, a grey curve, a terracotta dot riding it, a dashed drop line to a strip of 64 narrow tiles in true
grays under the axes at the same x scale), drawn from the shader's own formulas in evidence/planning-checks/plot_data.py (PD.CURVES[name][1]); the teal-to-gold
blend strips in B16 (PD.BLENDS). Terracotta only as the dot, small marker dots and grey-backed rings; never as text.

NOTE ON _kit_extra.plot_with_strip: it colours strip tile i by the INPUT value (gray = i / (n - 1)) instead of the curve's OUTPUT, so every strip but the identity
would be wrong. Not edited (the assembler pastes it); this act uses its own fixed variant, a2_plot(), which draws tile gray = fn(x) and honours a y range.
"""


def _a2_ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _a2_st(e, x):
    return np.where(x < e, 0.0, 1.0)


# The same formulas as evidence/planning-checks/plot_data.py, used only when that file cannot be imported (Gate A runs scenes.py alone in an empty folder).
_A2_CURVES = {
    "step_half": lambda x: _a2_st(0.5, x),
    "clamp_overshoot": lambda x: np.clip(x * 2.0 - 0.5, 0.0, 1.0),
    "smoothstep_3_7": lambda x: _a2_ss(0.3, 0.7, x),
    "smoothstep_0_10_over_0_10": lambda x: _a2_ss(0.0, 10.0, x * 10.0),
    "blend_plain_ramp": lambda x: x,
    "blend_step": lambda x: _a2_st(0.5, x),
    "blend_smoothstep": lambda x: _a2_ss(0.4, 0.6, x),
}


def a2_fn(name):
    if PD is not None:
        if name in PD.CURVES:
            return PD.CURVES[name][1]
        if name in PD.BLENDS:
            return PD.BLENDS[name][1]
    return _A2_CURVES[name]


def a2_blend_rgb(w):
    if PD is not None:
        return PD.blend_rgb(w)
    teal = np.array([0.37, 0.64, 0.57]); gold = np.array([0.96, 0.80, 0.45])
    return teal * (1.0 - w) + gold * w


def a2_t(s, x, y, size=32, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def a2_left(mob, x_left, y):
    """Place a mob so its left edge is at x_left (explicit coordinates; Pango widths vary)."""
    mob.move_to([x_left + mob.width / 2.0, y, 0])
    return mob


def a2_right(mob, x_right, y):
    mob.move_to([x_right - mob.width / 2.0, y, 0])
    return mob


def a2_tag(fn_text, gloss_lines, x_left, y_top):
    """The function tag: the mono signature, then the GLOSSARY wording in serif under it (left aligned at x_left, first line centred at y_top)."""
    rows = [M(fn_text, 32)] + [T(s, 32) for s in gloss_lines]
    y = y_top
    out = VGroup()
    for r in rows:
        a2_left(r, x_left, y)
        out.add(r)
        y -= 0.6 if r is rows[0] else 0.5
    return out


def a2_plot(fn, x=-2.8, y=0.2, size=4.4, y_range=(0.0, 1.0), n=64, strip=True, ylabels=((0.0, "0"), (1.0, "1"))):
    """The standard plot, fixed variant. fn: numpy function of x in 0..1 (PD.CURVES[name][1]); the strip tile at x has gray = fn(x) clipped to 0..1.
    Returns VGroup(axes, curve, tiles, lab) with .axes .curve .tiles .lab .dot .drop .tracker .ptf (replaceable point function) .pt .x0 .y0 .size .ystrip .yv(v)."""
    lo, hi = y_range
    x0, y0 = x - size / 2.0, y - size / 2.0

    def pt(xv):
        return np.array([x0 + xv * size, y0 + (float(fn(np.array([xv]))[0]) - lo) / (hi - lo) * size, 0.0])
    axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + size, 0], color=INK, stroke_width=5))
    curve = VMobject(stroke_color="#6B6760", stroke_width=7)
    curve.set_points_as_corners([pt(v) for v in np.linspace(0.0, 1.0, 120)])
    ystrip = y0 - 0.9
    tiles = VGroup()
    if strip:
        pitch = size / n
        for i in range(n):
            v = (i + 0.5) / n
            gv = int(round(255 * float(np.clip(fn(np.array([v]))[0], 0.0, 1.0))))
            t = Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (gv, gv, gv), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ystrip, 0])
            t.v = v
            tiles.add(t)
    lab = VGroup(a2_t("0", x0 - 0.3, ystrip), a2_t("1", x0 + size + 0.3, ystrip), a2_t("input", x0 + size + 0.8, y0))
    ol = T("output", 32).rotate(PI / 2).move_to([x0 - 0.85, y0 + size / 2.0, 0])
    lab.add(ol)
    for val, txt in ylabels:
        lab.add(a2_t(txt, x0 - 0.3, y0 + (val - lo) / (hi - lo) * size))
    g = VGroup(axes, curve, tiles, lab)
    g.axes = axes; g.curve = curve; g.tiles = tiles; g.lab = lab
    g.x0 = x0; g.y0 = y0; g.size = size; g.ystrip = ystrip; g.pt = pt; g.ptf = pt
    g.yv = lambda v: y0 + (v - lo) / (hi - lo) * size
    g.tracker = ValueTracker(0.0)
    dot = Dot(pt(0.0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    dot.add_updater(lambda m: m.move_to(g.ptf(g.tracker.get_value())))
    drop = DashedLine(pt(0.0), [x0, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
    drop.add_updater(lambda m: m.become(DashedLine(g.ptf(g.tracker.get_value()), [x0 + g.tracker.get_value() * size, ystrip + 0.25, 0],
                                                    color=DIM, stroke_width=3, dash_length=0.1)))
    g.dot = dot; g.drop = drop
    return g


def a2_paint(tiles, lo, hi=None, ghost=0.16):
    """Strip tiles light up as the dot passes: tile painted when its x <= lo (or >= hi); the rest stay a pale ghost."""
    def upd(m):
        l = lo.get_value()
        h = hi.get_value() if hi is not None else 9.0
        for t in m:
            t.set_fill(opacity=1.0 if (t.v <= l or t.v >= h) else ghost)
    tiles.add_updater(upd)
    upd(tiles)


def a2_follow(lo, tr, st=None):
    """lo keeps the furthest value the tracker has reached (st['on'] False pauses it)."""
    def upd(m):
        if st is None or st.get("on", True):
            m.set_value(max(m.get_value(), tr.get_value()))
    lo.add_updater(upd)


def a2_mid(self, frac=0.56):
    """Wait until 56 % of the clip, so the whole 45-55 % window is a settled hold and the next motion starts after it."""
    tgt = _TARGET.get(type(self).__name__.split("_")[0], 0)
    if tgt:
        gap = tgt * frac - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)


def a2_vguide(g, xv, color=DIM, sw=5):
    ex = g.x0 + xv * g.size
    return DashedLine([ex, g.y0, 0], [ex, g.y0 + g.size, 0], color=color, stroke_width=sw, dash_length=0.14)


def a2_marker(p, r=0.12):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════════ B07 · step is a switch ═════════════════════════════
class B07_StepSwitch(Scene):
    def construct(self):
        title = T("Cut  and Blend", 40).to_corner(UL, buff=0.95)
        g = a2_plot(a2_fn("step_half"), x=-2.5, y=0.1)
        ex = g.x0 + 0.5 * g.size
        top = g.y0 + g.size
        edge = a2_vguide(g, 0.5)
        edge_lab = a2_t("edge", ex + 0.6, top - 0.45)
        tag = a2_tag("step(edge, x)", ["0 below the edge,", "1 from the edge up"], 0.7, 1.5)
        lo = ValueTracker(0.0)
        a2_paint(g.tiles, lo)
        a2_follow(lo, g.tracker)
        self.add(title, lo, g.tracker, g.tiles)
        self.play(Create(g.axes), FadeIn(g.lab), Create(g.curve), Create(edge), FadeIn(edge_lab), FadeIn(tag), run_time=0.8)
        # the edge, highlighted on "an edge"
        until(self, "Give it an edge", lead=0.0)
        self.play(edge.animate.set_color(INK).set_stroke(width=8), run_time=0.4)
        # the dot rides the 0 level up to the edge
        until(self, "Where the ramp is below", lead=0.5)
        self.play(FadeIn(g.dot), FadeIn(g.drop), run_time=0.3)
        self.play(g.tracker.animate.set_value(0.47), run_time=1.4)
        # midpoint hold: the dot rests just left of the edge on the 0 level
        until(self, "At the edge or above", lead=0.15)
        a, b = 59 / 119.0, 60 / 119.0           # the curve's own two samples around the edge

        def pj(v):
            yv = 0.0 if v <= a else (1.0 if v >= b else (v - a) / (b - a))
            return np.array([g.x0 + v * g.size, g.y0 + yv * g.size, 0.0])
        g.ptf = pj
        open_c = Circle(radius=0.14, stroke_color=INK, stroke_width=5, fill_color=STAGE, fill_opacity=1).move_to([ex, g.y0, 0])
        closed = Dot([ex, top, 0], radius=0.14, color=INK)
        self.play(g.tracker.animate.set_value(0.5042), FadeIn(open_c), run_time=0.7)
        self.add(closed)
        # it rides on at 1; the strip's hard split lights up
        until(self, "The plot is a single jump", lead=0.2)
        self.play(g.tracker.animate.set_value(0.97), run_time=1.5)
        done(self)


# ═════════════════════════════ B09 · clamp pins ═════════════════════════════
class B09_ClampPins(Scene):
    def construct(self):
        fn = a2_fn("clamp_overshoot")
        g = a2_plot(fn, x=-2.9, y=0.2, y_range=(-0.5, 1.5))
        x0, y0, S = g.x0, g.y0, g.size
        x1 = x0 + S
        y_lo, y_hi = g.yv(0.0), g.yv(1.0)
        guide_lo = Line([x0, y_lo, 0], [x1 + 0.2, y_lo, 0], color=DIM, stroke_width=3)
        guide_hi = Line([x0, y_hi, 0], [x1 + 0.2, y_hi, 0], color=DIM, stroke_width=3)
        lab_hi = a2_t("high end", x0 + 1.15, y_hi + 0.32)
        lab_lo = a2_t("low end", x0 + 3.0, y_lo - 0.32)
        tag = VGroup(M("clamp(x, low, high)", 32), M("= min(max(x, low), high)", 32))
        a2_left(tag[0], 0.15, 2.85)
        a2_left(tag[1], 0.15, 2.3)
        ramp = DashedLine([x0, y0, 0], [x1, y0 + S, 0], color=DIM, stroke_width=5, dash_length=0.15)
        # the solid curve is drawn BY the dot: a trace that grows to the furthest point the dot has reached
        full = g.curve.copy()
        trace = full.copy()
        reach = ValueTracker(0.0)
        a2_follow(reach, g.tracker)

        def upd_trace(m):
            a = reach.get_value()
            if a < 0.004:
                m.set_stroke(opacity=0)
            else:
                m.pointwise_become_partial(full, 0, min(a, 1.0))
                m.set_stroke(opacity=1)
        trace.add_updater(upd_trace)
        upd_trace(trace)
        a2_paint(g.tiles, reach)
        self.add(reach, g.tracker, g.tiles, trace)
        self.play(Create(g.axes), FadeIn(g.lab), Create(guide_lo), Create(guide_hi), FadeIn(lab_hi), FadeIn(lab_lo), FadeIn(tag), run_time=0.9)
        # the dashed ramp overshoots both guides
        until(self, "Below the low end", lead=0.2)
        self.play(Create(ramp), run_time=1.2)
        # low end: the dot sits on the flat low part, pinned
        until(self, "you get the low end", lead=0.1)
        g.tracker.set_value(0.12)
        pin_lo = a2_left(T("pinned", 32), x0 + 0.15, y_lo + 0.6)
        self.play(FadeIn(g.dot), FadeIn(g.drop), FadeIn(pin_lo), run_time=0.5)
        # high end: the dot rides to the flat high part, drawing the middle ramp on the way
        until(self, "Above the high end", lead=0.15)
        a2_mid(self)
        self.play(g.tracker.animate.set_value(0.9), run_time=1.0)
        pin_hi = a2_left(T("pinned", 32), x0 + 0.9 * S + 0.2, y_hi - 0.5)
        self.play(FadeIn(pin_hi), run_time=0.3)
        # in between: back along the middle ramp
        until(self, "In between", lead=0.1)
        self.play(g.tracker.animate.set_value(0.5), run_time=1.0)
        # max first, then min: labels land on the two corners
        until(self, "It is max first", lead=0.1)
        c_lo, c_hi = a2_marker(g.pt(0.25)), a2_marker(g.pt(0.75))
        ext_lo = DashedLine([x1 + 0.2, y_lo, 0], [0.5, y_lo, 0], color=DIM, stroke_width=3, dash_length=0.12)
        ext_hi = DashedLine([x1 + 0.2, y_hi, 0], [0.5, y_hi, 0], color=DIM, stroke_width=3, dash_length=0.12)
        l_max = a2_left(T("max · the higher of two", 32), 0.65, y_lo)
        l_min = a2_left(T("min · the lower of two", 32), 0.65, y_hi)
        self.play(GrowFromCenter(c_lo), Create(ext_lo), FadeIn(l_max), run_time=0.5)
        self.play(GrowFromCenter(c_hi), Create(ext_hi), FadeIn(l_min), run_time=0.5)
        done(self)


# ═════════════════════════════ B10 · smoothstep, the soft switch ═════════════════════════════
class B10_SoftSwitch(Scene):
    def construct(self):
        g = a2_plot(a2_fn("smoothstep_3_7"), x=-2.9, y=0.3)
        x0, y0, S = g.x0, g.y0, g.size
        top = y0 + S
        e1, e2 = a2_vguide(g, 0.3), a2_vguide(g, 0.7)
        x_e1, x_e2 = x0 + 0.3 * S, x0 + 0.7 * S
        l1 = a2_right(T("first edge", 32), x_e1, top + 0.4)
        l2 = a2_left(T("second edge", 32), x_e2, top + 0.4)
        tag = a2_tag("smoothstep(a, b, x)", ["a smooth S between", "two edges"], 0.5, 1.5)
        lo, hi = ValueTracker(0.0), ValueTracker(9.0)
        st = {"on": True}
        a2_paint(g.tiles, lo, hi)
        a2_follow(lo, g.tracker, st)
        self.add(lo, hi, g.tracker, g.tiles)
        self.play(Create(g.axes), FadeIn(g.lab), FadeIn(tag), Create(g.curve), run_time=1.7)
        # two edges
        until(self, "Give it two edges", lead=0.1)
        self.play(Create(e1), Create(e2), FadeIn(l1), FadeIn(l2), run_time=0.7)
        # below the first edge: zero (dot rests on the flat left part)
        until(self, "Below the first edge", lead=0.9)
        g.tracker.set_value(0.08)
        zero = a2_t("0", x0 + 0.08 * S, g.yv(0.0) + 0.5)
        self.play(FadeIn(g.dot), FadeIn(g.drop), FadeIn(zero), run_time=0.5)
        # rides the flat 0 part to the first edge
        until(self, "zero. Above", lead=0.5)
        a2_mid(self)
        self.play(g.tracker.animate.set_value(0.3), run_time=0.6)
        # above the second edge: one (the dot jumps ahead to the flat 1 part)
        until(self, "Above the second", lead=0.1)
        st["on"] = False
        p_a, p_b = g.pt(0.3), g.pt(0.85)
        hop = CurvedArrow(p_a + np.array([0.2, -0.1, 0]), p_b + np.array([-0.2, -0.3, 0]), color=DIM, stroke_width=5, angle=-TAU / 5)
        self.play(Create(hop), run_time=0.4)
        g.tracker.set_value(0.85)
        one = a2_t("1", p_b[0], p_b[1] - 0.5)
        self.play(FadeIn(one), hi.animate.set_value(0.7), FadeOut(hop), run_time=0.5)
        # the S between the edges: back to the first edge, then ride the S
        until(self, "Between them", lead=0.1)
        self.play(FadeOut(g.dot), run_time=0.2)
        g.tracker.set_value(0.3)
        st["on"] = True
        self.play(FadeIn(g.dot), run_time=0.2)
        self.play(g.tracker.animate.set_value(0.7), run_time=1.7)
        done(self)


# ═════════════════════════════ B11 · smoothstep is not a straight line ═════════════════════════════
class B11_NotALine(Scene):
    def construct(self):
        W, H = 9.0, 4.4
        x0, y0 = -4.9, -1.9
        X = lambda v: x0 + v * W / 10.0
        O = lambda u: y0 + u * H
        top = O(1.0)
        fn = a2_fn("smoothstep_0_10_over_0_10")
        axes = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, top, 0], color=INK, stroke_width=5))
        ticks = VGroup(a2_t("0", x0, y0 - 0.4), a2_t("10", x0 + W, y0 - 0.4), a2_t("input", x0 + W + 0.85, y0), a2_t("1", x0 - 0.3, top),
                       a2_left(T("output", 32), x0 + 0.25, top + 0.4))
        line = DashedLine([X(0), O(0), 0], [X(10), O(1), 0], color=DIM, stroke_width=6, dash_length=0.16)
        scurve = VMobject(stroke_color="#6B6760", stroke_width=7)
        scurve.set_points_as_corners([np.array([X(10 * u), O(float(fn(np.array([u]))[0])), 0.0]) for u in np.linspace(0, 1, 160)])
        lab_line = a2_t("a straight line", X(2.9), O(0.58))
        lab_s = a2_t("the S", X(6.5), O(0.93))
        self.play(Create(axes), FadeIn(ticks), Create(line), Create(scurve), FadeIn(lab_line), FadeIn(lab_s), run_time=1.6)
        # the guide at x = 1 drops; two dots land on the two curves
        until(self, "Say the edges", lead=0.2)
        v_line, v_s = 0.1, float(fn(np.array([0.1]))[0])        # 0.1 and 0.02797
        guide = DashedLine([X(1), top, 0], [X(1), y0, 0], color=DIM, stroke_width=4, dash_length=0.12)
        self.play(Create(guide), run_time=0.7)
        d_line = a2_marker([X(1), top, 0], 0.12)
        d_s = a2_marker([X(1), top, 0], 0.12)
        self.add(d_line, d_s)
        self.play(d_line.animate.move_to([X(1), O(v_line), 0]), d_s.animate.move_to([X(1), O(v_s), 0]), run_time=0.9, rate_func=ease_in)
        # read-out on the straight line: 0.1
        until(self, "would give point one", lead=0.2)
        h1 = DashedLine([X(1), O(v_line), 0], [x0, O(v_line), 0], color=DIM, stroke_width=3, dash_length=0.1)
        r1 = a2_right(T("0.1", 34), x0 - 0.2, O(v_line) + 0.2)
        self.play(Create(h1), FadeIn(r1), run_time=0.5)
        # read-out on the S: 0.028, and the ring on the slow start
        until(self, "The S gives point zero", lead=0.1)
        h2 = DashedLine([X(1), O(v_s), 0], [x0, O(v_s), 0], color=DIM, stroke_width=3, dash_length=0.1)
        r2 = a2_right(T("0.028", 34), x0 - 0.2, O(v_s) - 0.12)
        slow = ring(Rectangle(width=1.95, height=0.6).move_to([x0 + 1.25, y0 + 0.35, 0]))
        self.play(Create(h2), FadeIn(r2), run_time=0.5)
        self.play(Create(slow), run_time=0.6)
        # the credit line
        until(self, "because it starts out slowly", lead=0.3)
        credit = a2_t("checked in Godot 4.7.2 · Forward+", 0.0, -3.05, 32, DIM)
        self.play(FadeIn(credit), run_time=0.5)
        done(self)


# ═════════════════════════════ B14 · mix slides ═════════════════════════════
class B14_MixSlides(Scene):
    def construct(self):
        A, B = 0.2, 0.9
        f = lambda t: A * (1.0 - t) + B * t
        unit, H = 2.7, 4.4
        x0, y0 = -4.15, -1.9
        ymax = 1.75
        X = lambda t: x0 + t * unit
        Y = lambda v: y0 + v / ymax * H
        axes = VGroup(Line([x0, y0, 0], [X(2), y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + H, 0], color=INK, stroke_width=5))
        xl = VGroup(a2_t("0", X(0) - 0.3, y0 - 0.38), a2_t("1", X(1) + 0.3, y0 - 0.38), a2_t("2", X(2), y0 - 0.38), a2_left(T("t · weight", 32), X(2) + 0.3, y0))
        solid = Line([X(0), Y(f(0)), 0], [X(1), Y(f(1)), 0], color="#6B6760", stroke_width=7)
        dashed = DashedLine([X(1), Y(f(1)), 0], [X(2), Y(f(2)), 0], color="#6B6760", stroke_width=7, dash_length=0.16)
        tag1 = a2_left(M("mix(a, b, t)", 32), -6.1, 3.0)
        tag2 = a2_left(T("blends from a to b: t of 0 gives a, 1 gives b", 32), -2.55, 3.0)
        form = a2_left(M("a x (1 - t) + b x t", 32), 1.5, 0.9)
        # strip for weights 0 to 1 only: gray of 0.2 up to gray of 0.9
        n = 32
        pitch = unit / n
        ys = y0 - 0.9
        tiles = VGroup()
        for i in range(n):
            v = (i + 0.5) / n
            gv = int(round(255 * f(v)))
            t = Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (gv, gv, gv), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ys, 0])
            t.v = v
            tiles.add(t)
        tr = ValueTracker(0.0)
        reach = ValueTracker(-1.0)
        a2_paint(tiles, reach)
        a2_follow(reach, tr)
        dot = Dot([X(0), Y(f(0)), 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        dot.add_updater(lambda m: m.move_to([X(tr.get_value()), Y(f(tr.get_value())), 0]))
        drop = DashedLine([X(0), Y(f(0)), 0], [X(0), ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)

        def upd_drop(m):
            t = tr.get_value()
            m.become(DashedLine([X(t), Y(f(t)), 0], [X(min(t, 1.0)), ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1))
            m.set_stroke(opacity=1.0 if t <= 1.0001 else 0.0)
        drop.add_updater(upd_drop)
        self.add(tr, reach, tiles)
        self.play(Create(axes), FadeIn(xl), FadeIn(tag1), FadeIn(tag2), FadeIn(form), Create(solid), run_time=0.9)
        # the start and end ticks land on the y axis
        until(self, "Give it a start", lead=0.1)
        tk_a = VGroup(Line([x0 - 0.12, Y(A), 0], [x0 + 0.12, Y(A), 0], color=INK, stroke_width=5), a2_right(T("a · start", 32), x0 - 0.22, Y(A)))
        tk_b = VGroup(Line([x0 - 0.12, Y(B), 0], [x0 + 0.12, Y(B), 0], color=INK, stroke_width=5), a2_right(T("b · end", 32), x0 - 0.22, Y(B)))
        self.play(FadeIn(tk_a), run_time=0.5)
        self.play(FadeIn(tk_b), run_time=0.5)
        # weight 0: start
        until(self, "Weight zero", lead=0.1)
        self.play(FadeIn(dot), FadeIn(drop), run_time=0.3)
        r_start = a2_t("start", X(0) + 1.0, y0 + 0.3)
        self.play(FadeIn(r_start), run_time=0.3)
        # weight 1: end
        until(self, "one returns the end", lead=0.9)
        self.play(tr.animate.set_value(1.0), run_time=0.6)
        r_end = a2_t("end", X(1) + 0.6, Y(B) - 0.45)
        self.play(FadeIn(r_end), run_time=0.25)
        # one half: halfway
        until(self, "one half", lead=0.1)
        a2_mid(self)
        self.play(tr.animate.set_value(0.5), run_time=0.6)
        r_half = a2_t("halfway", X(0.5) + 1.0, Y(f(0.5)) - 0.5)
        self.play(FadeIn(r_half), run_time=0.3)
        # the line carries on, dashed, past weight 1
        until(self, "It does not pin", lead=0.1)
        self.play(Create(dashed), run_time=0.6)
        until(self, "a weight of two", lead=0.1)
        self.play(tr.animate.set_value(2.0), run_time=1.1)
        r_over = a2_left(T("overshoots: 1.6", 32), X(2) + 0.3, Y(f(2)))
        self.play(FadeIn(r_over), run_time=0.4)
        # clamp first: the safe range 0 to 1 on the weight axis
        until(self, "so clamp it first", lead=0.1)
        br = VGroup(Line([X(0), y0, 0], [X(1), y0, 0], color=TEAL, stroke_width=11), Line([X(0), y0 - 0.14, 0], [X(0), y0 + 0.14, 0], color=TEAL, stroke_width=7),
                    Line([X(1), y0 - 0.14, 0], [X(1), y0 + 0.14, 0], color=TEAL, stroke_width=7))
        cl = a2_left(M("clamp(t, 0, 1)", 32), X(1) + 0.3, ys)
        self.play(Create(br), FadeIn(cl), run_time=0.6)
        done(self)


# ═════════════════════════════ B16 · any reshaped ramp can be the weight ═════════════════════════════
def a2_mini(wfn, cx, cy, w=2.0, h=1.1):
    """A small weight plot: axes and a grey curve (no dot). Returns VGroup with .curve and .axes."""
    x0, y0 = cx - w / 2.0, cy - h / 2.0
    axes = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=INK, stroke_width=4), Line([x0, y0, 0], [x0, y0 + h, 0], color=INK, stroke_width=4))
    curve = VMobject(stroke_color="#6B6760", stroke_width=6)
    curve.set_points_as_corners([np.array([x0 + v * w, y0 + float(wfn(np.array([v]))[0]) * h, 0.0]) for v in np.linspace(0.0, 1.0, 100)])
    g = VGroup(axes, curve)
    g.axes = axes; g.curve = curve
    return g


def a2_blend_strip(wfn, x_left, y, width=5.7, height=0.6, n=48):
    """A teal-to-gold strip blended with the weight wfn (colours from PD.blend_rgb); narrow tiles with gaps."""
    pitch = width / n
    tiles = VGroup()
    for i in range(n):
        v = (i + 0.5) / n
        rgb = a2_blend_rgb(float(wfn(np.array([v]))[0]))
        col = "#%02x%02x%02x" % tuple(int(round(255 * c)) for c in rgb)
        tiles.add(Rectangle(width=pitch * 0.8, height=height, fill_color=col, fill_opacity=1, stroke_width=0).move_to([x_left + pitch * (i + 0.5), y, 0]))
    return tiles


class B16_AnyWeight(Scene):
    def construct(self):
        rows = [("plain ramp", "blend_plain_ramp", 2.35, "The plain ramp", 0.15), ("step", "blend_step", 0.85, "Step gives", 0.9), ("smoothstep", "blend_smoothstep", -0.65, "Smooth step gives", 1.05)]
        caps, minis, arrs, strips = [], [], [], []
        for cap, name, ry, _, _l in rows:
            caps.append(a2_left(T(cap, 32), -6.1, ry))
            minis.append(a2_mini(a2_fn(name), -2.6, ry))
            arrs.append(arrow([-1.1, ry, 0], [-0.3, ry, 0], color=INK, w=5, tip=0.2))
            strips.append(a2_blend_strip(a2_fn(name), 0.2, ry))
        self.play(*[FadeIn(c) for c in caps], run_time=0.6)
        for i, (cap, name, ry, ph, ld) in enumerate(rows):
            until(self, ph, lead=ld)
            self.play(Create(minis[i].axes), Create(minis[i].curve), run_time=0.35)
            self.play(Create(arrs[i]), run_time=0.15)
            self.play(LaggedStart(*[FadeIn(t) for t in strips[i]], lag_ratio=0.03), run_time=0.4)
        # the grey-backed bracket round the three weight plots
        until(self, "A weight like this", lead=0.2)
        bracket = ring(VGroup(*minis), pad=0.22, sw=6)
        self.play(Create(bracket), run_time=0.8)
        # the definition types in; then the word "mask" is marked
        until(self, "a number from zero to one", lead=0.2)
        mask = T("mask", 38, INK, True)
        rest = T("· a number from 0 to 1 per pixel", 36)
        l1 = VGroup(mask, rest).arrange(RIGHT, buff=0.22)
        l1.move_to([0.0, -2.2, 0])
        l2 = T("saying how much of something to show", 36).move_to([0.0, -2.78, 0])
        self.play(AddTextLetterByLetter(l1[0], time_per_char=0.07), run_time=0.45)
        self.play(AddTextLetterByLetter(l1[1], time_per_char=0.05), run_time=1.1)
        self.play(AddTextLetterByLetter(l2, time_per_char=0.04), run_time=1.1)
        until(self, "is called a mask", lead=0.1)
        self.play(Create(ring(mask, pad=0.1, sw=6)), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · Repeat and Fold  (B17 B18 B19 B21 B22 B24, Manim; B20 B23 are ShaderLab captures, B25 is a table)

Cast for the act (ACTS.md): the ramp strip with re-labelled ticks; the number line with the dot at 2.75; the standard plot frame.

a3_plot is this act's fixed variant of plot_with_strip: the kit-extra helper draws the strip under the axes as a plain 0..1 ramp whatever the curve is
(its tiles ignore fn) and joins the jumps of fract / floor / mod with slanted lines. a3_plot draws the strip tiles from the curve's own values
(true grays: value v drawn as gray v) and the curve as separate pieces so a jump is a jump. _kit_extra.py itself is untouched.
"""

A3C = "#6B6760"          # the curve's ink-grey

# PD (plot_data.py) is imported by _kit_extra when evidence/ is reachable; Gate A runs scenes.py alone, so the same four formulas are kept here as a fallback
_A3_FALLBACK = {
    "abs_centered": lambda x: np.abs(x * 2.0 - 1.0),
    "fract_4": lambda x: (x * 4.0) - np.floor(x * 4.0),
    "floor_4_over_3": lambda x: np.floor(x * 4.0) / 3.0,
    "mod_quarter_x4": lambda x: (x - 0.25 * np.floor(x / 0.25)) * 4.0,
}


def a3_curve(name):
    """The numpy function of a named curve: from plot_data.py when it is importable, else the identical fallback above."""
    try:
        return PD.CURVES[name][1]
    except Exception:
        return _A3_FALLBACK[name]


def a3_plot(fn, pieces, strip_fn=None, x=-1.8, y=0.6, size=4.2, y_range=(0.0, 1.0), in_labels=("0", "1"), out_labels=("0", "1"), n=64):
    """Standard plot, fixed. fn / strip_fn: numpy functions of x in 0..1. pieces: list of (xa, xb) so jumps are not joined. Returns a VGroup (frame +
    labels) with .parts (curve pieces), .tiles (true-gray strip, 64 narrow tiles with gaps), .dot, .drop, .tr (ValueTracker of x), .pt, .x0 .y0 .size .ystrip."""
    x0, y0 = x - size / 2, y - size / 2
    lo, hi = y_range
    sfn = strip_fn or fn

    def pt(xv):
        return np.array([x0 + xv * size, y0 + (float(fn(np.array([float(xv)]))[0]) - lo) / (hi - lo) * size, 0.0])
    axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + size, 0], color=INK, stroke_width=5))
    parts = VGroup()
    for a, b in pieces:
        c = VMobject(stroke_color=A3C, stroke_width=7)
        c.set_points_as_corners([pt(v) for v in np.linspace(a, b - 1e-6, 81)])
        parts.add(c)
    ystrip = y0 - 0.95
    tiles = VGroup()
    pitch = size / n
    for i in range(n):
        v = float(np.clip(sfn(np.array([(i + 0.5) / n]))[0], 0.0, 1.0))
        gv = int(round(255 * v))
        tiles.add(Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (gv, gv, gv), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ystrip, 0]))
    tr = ValueTracker(0.0)
    dot = Dot(pt(0.0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    dot.add_updater(lambda m: m.move_to(pt(tr.get_value())))
    drop = DashedLine(pt(0.0), [x0, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
    drop.add_updater(lambda m: m.become(DashedLine(pt(tr.get_value()), [x0 + tr.get_value() * size, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)))
    k = len(in_labels) - 1
    # the end labels sit just outside the ends so the dashed drop line never runs through a label
    labs = VGroup(*[T(s, 32).move_to([x0 + size * i / k + (-0.3 if i == 0 else (0.3 if i == k else 0.0)), y0 - 0.38, 0]) for i, s in enumerate(in_labels)])
    outs = VGroup(T(out_labels[0], 32).move_to([x0 - 0.4, y0, 0]), T(out_labels[1], 32).move_to([x0 - 0.4, y0 + size, 0]))
    g = VGroup(axes, labs, outs)
    g.parts = parts; g.tiles = tiles; g.dot = dot; g.drop = drop; g.tr = tr; g.pt = pt
    g.x0 = x0; g.y0 = y0; g.size = size; g.ystrip = ystrip; g.axes = axes
    return g


def a3_reveal(g, lo_op=0.14):
    """The strip lights tile by tile as the dot passes (an updater on the tiles; do not FadeIn the tiles after this)."""
    nt = len(g.tiles)

    def f(m):
        v = g.tr.get_value()
        for i, t in enumerate(m):
            t.set_fill(opacity=1.0 if (i + 0.5) / nt <= v else lo_op)
    g.tiles.add_updater(f)
    f(g.tiles)


def a3_open(p):
    return Circle(radius=0.1, stroke_color=A3C, stroke_width=5).set_fill(STAGE, opacity=1).move_to(p)


def a3_closed(p):
    return Dot(p, radius=0.1, color=A3C)


def a3_bracket(xa, xb, y, color=DIM, cap=0.14, sw=6):
    return VGroup(Line([xa, y, 0], [xb, y, 0], color=color, stroke_width=sw), Line([xa, y, 0], [xa, y + cap, 0], color=color, stroke_width=sw),
                  Line([xb, y, 0], [xb, y + cap, 0], color=color, stroke_width=sw))


def a3_row(mobs, gap, cx, cy):
    """Centre a row of mobjects with a fixed gap between them."""
    tot = sum(m.width for m in mobs) + gap * (len(mobs) - 1)
    x = cx - tot / 2.0
    for m in mobs:
        m.move_to([x + m.width / 2.0, cy, 0])
        x += m.width + gap
    return mobs


# ═════════════════════════════ B17 · re-centering a ramp ═════════════════════════════
class B17_Recenter(Scene):
    def construct(self):
        title = T("Repeat and Fold", 40).to_corner(UL, buff=0.95)
        strip = ramp_strip(width=8.0, n=56, height=0.5, y=0.3, labels=False)
        x0, x1, xm = strip.x0, strip.x1, 0.0
        ly = 0.3 - 0.25 - 0.45
        lab0 = T("0", 36).move_to([x0, ly, 0])
        lab1 = T("1", 36).move_to([x1, ly, 0])
        dot = ramp_marker(strip, 0.5)
        self.add(title, strip, lab0, lab1)
        self.play(GrowFromCenter(dot), run_time=0.4)
        # x * 2: the number 1 slides to the middle, a 2 takes the end
        until(self, "Multiply by two")
        tag1 = chip("x × 2", -1.9, 1.75)
        lab2 = T("2", 36).move_to([x1, ly, 0])
        self.play(FadeIn(tag1), lab1.animate.move_to([xm, ly, 0]), FadeIn(lab2), run_time=0.9)
        # - 1: every label slides one step down the number line
        until(self, "and subtract one")
        tag2 = chip("− 1", 1.9, 1.75)
        n0 = T("−1", 36).move_to([x0, ly, 0])
        nm = T("0", 36).move_to([xm, ly, 0])
        n1 = T("1", 36).move_to([x1, ly, 0])
        self.play(FadeIn(tag2), ReplacementTransform(lab0, n0), ReplacementTransform(lab1, nm), ReplacementTransform(lab2, n1), run_time=1.0)
        # zero lands under the dot
        until(self, "with zero in the middle")
        zm = ring(nm)
        self.play(FadeIn(zm, shift=DOWN * 0.4), run_time=0.5)
        until(self, "Now negative numbers")
        cap = T("zero here", 36).move_to([0, -1.6, 0])
        pt_ = arrow([0, -1.25, 0], [0, -0.85, 0], color=DIM)
        hl = RoundedRectangle(width=4.1, height=0.8, corner_radius=0.16, stroke_color=TEAL, stroke_width=7).move_to([-2.0, 0.3, 0])
        self.play(FadeIn(cap), GrowArrow(pt_), Create(hl), run_time=0.6)
        done(self)


# ═════════════════════════════ B18 · abs folds the ramp at zero ═════════════════════════════
class B18_FoldAtZero(Scene):
    def construct(self):
        SX, SY = -1.2, 2.15
        strip = ramp_strip(width=5.2, n=56, height=0.45, x=SX, y=SY, labels=False)
        ly = SY - 0.225 - 0.4
        labs = VGroup(T("−1", 36).move_to([strip.x0, ly, 0]), T("0", 36).move_to([SX, ly, 0]), T("1", 36).move_to([strip.x1, ly, 0]))
        dot = ramp_marker(strip, 0.5)
        tag = chip("abs(x)", 4.0, 2.2)
        tag2 = T("drops the minus sign", 36).move_to([4.0, 1.55, 0])
        self.add(strip, labs, dot, tag, tag2)
        axis = DashedLine([SX, SY + 0.45, 0], [SX, SY - 0.45, 0], color=DIM, stroke_width=4, dash_length=0.1)
        self.play(Create(axis), run_time=0.4)
        # the left half folds over the right half like a page
        until(self, "Fold the ramp at zero")
        left = VGroup(*strip.tiles[:28])
        left.set_z_index(3)
        self.play(FadeOut(labs[0]), left.animate.flip(UP, about_point=np.array([SX, SY, 0])), run_time=1.6, rate_func=smooth)
        # the V draws under the strip
        until(self, "The plot is a V")
        pl = a3_plot(a3_curve("abs_centered"), [(0.0, 1.0)], x=SX, y=-0.4, size=3.0, in_labels=("−1", "0", "1"), out_labels=("0", "1"))
        self.play(Create(pl), run_time=0.5)
        self.add(pl.tiles)
        a3_reveal(pl)
        self.play(Create(pl.parts), run_time=0.7)
        self.add(pl.drop, pl.dot)
        until(self, "and the strip is a mirror", lead=0.1)
        self.play(pl.tr.animate.set_value(1.0), run_time=2.1, rate_func=linear)
        mir = DashedLine([SX, pl.ystrip + 0.45, 0], [SX, pl.ystrip - 0.45, 0], color=DIM, stroke_width=4, dash_length=0.1)
        self.play(Create(mir), run_time=0.4)
        done(self)


# ═════════════════════════════ B19 · fract: the ramp restarts ═════════════════════════════
class B19_RampRestarts(Scene):
    def construct(self):
        RX = 3.95
        tag = chip("fract(x)", RX, 2.55)
        t1 = T("the part after the point", 32).move_to([RX, 1.85, 0])
        t2 = M("x − floor(x)", 32).move_to([RX, 1.3, 0])
        self.play(FadeIn(tag), FadeIn(t1), FadeIn(t2), run_time=0.6)
        # inset: 2.75 splits into 2 and 0.75
        nl = number_line(-5.2, 0.8, 0.2, lo=0.0, hi=3.0, ticks=(0.0, 1.0, 2.0, 3.0))
        until(self, "Two point seven five")
        d = Dot(nl.at(2.75), radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        self.play(Create(nl), run_time=0.5)
        self.play(GrowFromCenter(d), run_time=0.3)
        until(self, "becomes", lead=0.3)
        b1 = a3_bracket(nl.at(0)[0], nl.at(2)[0], -0.75, DIM)
        b2 = a3_bracket(nl.at(2)[0], nl.at(2.75)[0], -0.75, TEAL)
        l1 = T("2", 36).move_to([(nl.at(0)[0] + nl.at(2)[0]) / 2, -1.25, 0])
        l2 = T("0.75", 36).move_to([(nl.at(2)[0] + nl.at(2.75)[0]) / 2, -1.25, 0])
        self.play(Create(b1), Create(b2), FadeIn(l1), FadeIn(l2), run_time=0.6)
        r1 = T("2.75", 44).move_to([-3.9, -2.2, 0])
        ar = arrow([-3.05, -2.2, 0], [-1.95, -2.2, 0])
        r2 = T("0.75", 44).move_to([-1.2, -2.2, 0])
        self.play(FadeIn(r1), GrowArrow(ar), FadeIn(r2), run_time=0.6)
        inset = VGroup(nl, d, b1, b2, l1, l2, r1, ar, r2)
        # the standard plot: a steep dashed 4x leaves the top, fract(4x) is four teeth
        until(self, "Multiply the ramp", lead=0.0)
        self.play(FadeOut(inset), run_time=0.4)
        pl = a3_plot(a3_curve("fract_4"), [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)], x=-1.8, y=0.6, size=4.2,
                     in_labels=("0", "1"), out_labels=("0", "1"))
        dash = DashedLine(pl.pt(0.0), pl.pt(0.0) + np.array([0.275 * 4.2, 1.1 * 4.2, 0]), color=DIM, stroke_width=4, dash_length=0.14)
        self.play(Create(pl), Create(dash), run_time=0.6)
        self.add(pl.tiles)
        a3_reveal(pl)
        until(self, "and fract gives four ramps", lead=0.0)
        self.play(LaggedStart(*[Create(c) for c in pl.parts], lag_ratio=0.7), run_time=1.3)
        marks = VGroup()
        for i in range(4):
            marks.add(a3_closed(pl.pt(i * 0.25 + 1e-6)))
        for i in range(1, 5):
            marks.add(a3_open(np.array([pl.x0 + i * 0.25 * 4.2, pl.y0 + 4.2, 0.0])))
        self.play(FadeIn(marks), run_time=0.3)
        self.add(pl.drop, pl.dot)
        until(self, "each starting over at zero", lead=0.2)
        self.play(pl.tr.animate.set_value(0.9999), run_time=1.7, rate_func=linear)
        done(self)


# ═════════════════════════════ B21 · floor rounds down ═════════════════════════════
class B21_RoundDown(Scene):
    def construct(self):
        RX = 3.95
        tag = chip("floor(x)", RX, 2.55)
        t1 = T("rounds down to the", 32).move_to([RX, 1.9, 0])
        t2 = T("whole number below", 32).move_to([RX, 1.45, 0])
        self.play(FadeIn(tag), FadeIn(t1), FadeIn(t2), run_time=0.6)
        until(self, "It rounds down", lead=0.1)
        i1 = T("2.75", 40).move_to([2.9, 0.5, 0])
        ia = arrow([3.65, 0.5, 0], [4.55, 0.5, 0])
        i2 = T("2", 40).move_to([5.15, 0.5, 0])
        self.play(FadeIn(i1), GrowArrow(ia), FadeIn(i2), run_time=0.7)
        # the plot: dashed 4x diagonal and the first step
        until(self, "Multiply the ramp", lead=0.7)
        fl = lambda x: np.floor(x * 4.0)
        pl = a3_plot(fl, [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)], strip_fn=a3_curve("floor_4_over_3"), x=-1.8, y=0.6, size=4.2,
                     y_range=(0.0, 4.0), in_labels=("0", "1"), out_labels=("0", "4"))
        diag = DashedLine(pl.pt(0.0), [pl.x0 + 4.2, pl.y0 + 4.2, 0], color=DIM, stroke_width=4, dash_length=0.14)
        self.play(Create(pl), Create(diag), run_time=0.45)
        self.add(pl.tiles)
        a3_reveal(pl)
        step0 = pl.parts[0]
        c0 = a3_closed(pl.pt(1e-6)); o0 = a3_open(np.array([pl.x0 + 0.25 * 4.2, pl.y0, 0.0]))
        bl = [T(str(k), 36).move_to([pl.x0 + (k + 0.5) * 0.25 * 4.2, pl.ystrip - 0.5, 0]) for k in range(4)]
        note = T("÷ 3 to fit", 32).move_to([2.0, pl.ystrip, 0])
        self.play(Create(step0), FadeIn(c0), FadeIn(o0), FadeIn(bl[0]), FadeIn(note), run_time=0.35)
        self.add(pl.drop, pl.dot)
        self.play(pl.tr.animate.set_value(0.24), run_time=0.3, rate_func=linear)
        for k, ph in ((1, "one, two"), (2, "two, three"), (3, "three, four")):
            until(self, ph, lead=0.3)
            pl.tr.set_value(0.25 * k + 1e-4)
            self.play(Create(pl.parts[k]), pl.tr.animate.set_value(0.25 * (k + 1) - 1e-4), FadeIn(a3_closed(pl.pt(0.25 * k + 1e-6))),
                      FadeIn(a3_open(np.array([pl.x0 + 0.25 * (k + 1) * 4.2, pl.y0 + k * 1.05, 0.0]))), FadeIn(bl[k]), run_time=0.7, rate_func=linear)
        pl.tr.set_value(0.9999)
        self.wait(0.1)
        done(self)


# ═════════════════════════════ B22 · whole and leftover ═════════════════════════════
class B22_WholeAndLeftover(Scene):
    def construct(self):
        nl = number_line(-5.0, 5.0, 1.2, lo=0.0, hi=4.0, ticks=(0.0, 1.0, 2.0, 3.0, 4.0))
        ay = 1.2
        d = Dot(nl.at(2.75), radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.add(nl)
        self.play(GrowFromCenter(d), run_time=0.4)
        until(self, "Floor is the whole part")
        b1 = a3_bracket(nl.at(0)[0], nl.at(2)[0], 0.15, DIM)
        l1 = M("floor = 2", 32).move_to([(nl.at(0)[0] + nl.at(2)[0]) / 2, -0.4, 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.7)
        until(self, "fract is the leftover")
        b2 = a3_bracket(nl.at(2)[0], nl.at(2.75)[0], 0.15, TEAL)
        l2 = M("fract = 0.75", 32).move_to([(nl.at(2)[0] + nl.at(2.75)[0]) / 2 + 0.1, -0.4, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.7)
        until(self, "Two point seven five is")
        eq = T("2.75 = 2 + 0.75", 44).move_to([0.0, -1.5, 0])
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.6)
        # the dot slides 0 to 4: floor steps, fract resets
        until(self, "So floor says", lead=0.3)
        tr = ValueTracker(2.75)
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(l1), FadeOut(l2), d.animate.move_to(nl.at(0.0)), run_time=0.5)
        tr.set_value(0.0)
        fl = lambda: int(np.floor(tr.get_value() + 1e-9))
        fr = lambda: tr.get_value() - np.floor(tr.get_value() + 1e-9)
        whole = always_redraw(lambda: Dot(nl.at(float(fl())), radius=0.1, color=DIM))
        left = always_redraw(lambda: Line(nl.at(float(fl())), nl.at(tr.get_value()), color=TEAL, stroke_width=9).shift(DOWN * 0.0))
        rl = T("floor", 36).move_to([-3.6, -2.55, 0])
        rr = T("fract", 36).move_to([1.4, -2.55, 0])
        rn1 = always_redraw(lambda: M(str(fl()), 36).move_to([-2.5, -2.55, 0]))
        rn2 = always_redraw(lambda: M("%.2f" % fr(), 36).move_to([3.0, -2.55, 0]))
        d.add_updater(lambda m: m.move_to(nl.at(tr.get_value())))
        self.add(whole, left, rl, rr, rn1, rn2)
        self.play(tr.animate.set_value(4.0), run_time=2.7, rate_func=linear)
        done(self)


# ═════════════════════════════ B24 · mod, the remainder ═════════════════════════════
class B24_Remainder(Scene):
    def construct(self):
        parts = [M("mod(x, y)", 32), M("=", 32), M("x", 32), M("−", 32), M("y", 32), M("·", 32), M("floor(x / y)", 32)]
        a3_row(parts, 0.3, 0.0, 2.7)
        self.play(FadeIn(parts[0]), FadeIn(parts[1]), run_time=0.5)
        until(self, "x minus", lead=0.2)
        self.play(FadeIn(parts[2], shift=UP * 0.2), FadeIn(parts[3], shift=UP * 0.2), run_time=0.5)
        until(self, "y times", lead=0.2)
        self.play(FadeIn(parts[4], shift=UP * 0.2), FadeIn(parts[5], shift=UP * 0.2), run_time=0.5)
        until(self, "floor of", lead=0.2)
        self.play(FadeIn(parts[6], shift=UP * 0.2), run_time=0.6)
        # card: y = 1 is fract
        until(self, "With y equal to one", lead=0.2)
        card = RoundedRectangle(width=5.0, height=1.6, corner_radius=0.16, stroke_color=DIM, stroke_width=3).set_fill("#FFFFFF", opacity=1).move_to([3.5, 0.7, 0])
        c1 = M("y = 1", 32).move_to([3.5, 1.05, 0])
        c2a = T("same as", 32); c2b = M("fract(x)", 32)
        a3_row([c2a, c2b], 0.25, 3.5, 0.35)
        self.play(Create(card), FadeIn(c1), FadeIn(c2a), FadeIn(c2b), run_time=0.7)
        # y = 0.25: four teeth
        until(self, "With y of point two five", lead=0.6)
        pl = a3_plot(lambda x: a3_curve("mod_quarter_x4")(x) / 4.0, [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)],
                     strip_fn=a3_curve("mod_quarter_x4"), x=-2.2, y=0.0, size=3.6, y_range=(0.0, 0.25), in_labels=("0", "1"), out_labels=("0", "0.25"))
        self.play(Create(pl), run_time=0.5)
        self.add(pl.tiles)
        a3_reveal(pl)
        self.play(LaggedStart(*[Create(c) for c in pl.parts], lag_ratio=0.6), run_time=0.9)
        sz = pl.size
        marks = VGroup(*[a3_closed(pl.pt(i * 0.25 + 1e-6)) for i in range(4)],
                       *[a3_open(np.array([pl.x0 + i * 0.25 * sz, pl.y0 + sz, 0.0])) for i in range(1, 5)])
        cap1 = M("y = 0.25", 32).move_to([3.5, -0.75, 0])
        cap2 = T("repeats every 0.25", 32).move_to([3.5, -1.3, 0])
        note = T("× 4 to fit", 32).move_to([1.7, pl.ystrip, 0])
        self.play(FadeIn(marks), FadeIn(cap1), FadeIn(cap2), FadeIn(note), run_time=0.4)
        self.add(pl.drop, pl.dot)
        self.play(pl.tr.animate.set_value(0.9999), run_time=1.8, rate_func=linear)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · Distance and Curves (B26 B27 B28 B30 B32 B34), Manim drawings only.

Cast: the vector arrow (3, 4) on axes with the origin at the TOP LEFT (y counts down, labelled once in B26); the UV square with the "middle" dot;
the standard plot frame. Own plot helper a4_* replaces _kit_extra.plot_with_strip, whose strip tiles are the identity ramp for every curve (it ignores fn):
here every tile is the true gray of the CURVE's value at that x (PD.CURVES formulas), revealed as the dot passes.
"""
try:
    PD
except NameError:
    PD = None


def a4_f(name):
    """numpy function for a curve name from plot_data (fallbacks are the same formulas)."""
    if PD is not None and name in PD.CURVES:
        return PD.CURVES[name][1]
    return {"pow_3": lambda x: x ** 3.0, "pow_half": lambda x: x ** 0.5, "identity": lambda x: x,
            "sine_two_cycles": lambda x: 0.5 + 0.5 * np.sin(x * 4.0 * np.pi)}[name]


def a4_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a4_m(s, x, y, size=32, color=INK):
    return M(s, size, color).move_to([x, y, 0])


def a4_axes(O, s, lx, ly):
    """Axes with the origin at the top left, y counting down. lx, ly = lengths in units."""
    ax = arrow([O[0], O[1], 0], [O[0] + lx * s, O[1], 0], color=DIM, w=5, tip=0.2)
    ay = arrow([O[0], O[1], 0], [O[0], O[1] - ly * s, 0], color=DIM, w=5, tip=0.2)
    return VGroup(ax, ay)


def a4_strip(fn, x0, size, y, n=64, h=0.5):
    """64 narrow tiles with gaps in TRUE grays: tile i is gray(fn(i/(n-1))). Returns VGroup with .xs (x of each tile in 0..1)."""
    pitch = size / n
    tiles = VGroup()
    for i in range(n):
        v = float(np.clip(fn(np.array([i / (n - 1)]))[0], 0.0, 1.0))
        g = int(round(255 * v))
        tiles.add(Rectangle(width=pitch * 0.78, height=h, fill_color="#%02x%02x%02x" % (g, g, g), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), y, 0]))
    tiles.xs = [i / (n - 1) for i in range(n)]
    return tiles


def a4_reveal(tiles, tr):
    """Tiles are visible only up to the dot's x (the strip fills as the dot passes)."""
    def up(m):
        v = tr.get_value()
        for t, xv in zip(m, m.xs):
            t.set_fill(opacity=1.0 if xv <= v + 1e-6 else 0.0)
    tiles.add_updater(up)
    up(tiles)


# ═══════════════════════════════════════════ B26 ═══════════════════════════════════════════
class B26_HowLong(Scene):
    def construct(self):
        title = T("Distance and Curves", 40).to_corner(UL, buff=0.95)
        O = np.array([-4.2, 1.5, 0]); s = 0.85
        axes = a4_axes(O, s, 5.4, 4.0)
        xl = a4_t("x", O[0] + 5.4 * s + 0.4, O[1])
        ydown = a4_t("y counts down", O[0], O[1] - 4.0 * s - 0.4)
        tip = O + np.array([3 * s, -4 * s, 0])
        corner = O + np.array([3 * s, 0, 0])
        tag = chip("length(v)", 3.6, 2.45)
        gloss = a4_t("the length of a vector", 3.6, 1.7)
        self.add(title)
        self.play(Create(axes), FadeIn(xl), FadeIn(ydown), FadeIn(tag), FadeIn(gloss), run_time=1.0)
        until(self, "A vector bundles them")
        vec = vec_arrow(O, tip, color=INK, w=8)
        vlab = a4_t("v = (3, 4)", tip[0] + 0.15 + 1.1, tip[1] - 0.15)
        self.play(Create(vec), run_time=1.1)
        self.play(FadeIn(vlab), run_time=0.5)
        until(self, "Three across and four down")
        leg_a = DashedLine(O, corner, color=TEAL, stroke_width=8, dash_length=0.14)
        leg_b = DashedLine(corner, tip, color=TEAL, stroke_width=8, dash_length=0.14)
        la = a4_t("3", (O[0] + corner[0]) / 2, O[1] + 0.4)
        lb = a4_t("4", corner[0] + 0.4, (corner[1] + tip[1]) / 2)
        self.play(Create(leg_a), FadeIn(la), run_time=0.7)
        self.play(Create(leg_b), FadeIn(lb), run_time=0.8)
        until(self, "has length five")
        mid = (O + tip) / 2
        five = a4_t("5", mid[0] + 0.55, mid[1] + 0.05, 48)
        self.play(FadeIn(five, scale=1.6), run_time=0.5)
        until(self, "the square root of nine")
        f1 = a4_m("√(x² + y²)", 3.6, 0.55)
        f2 = a4_m("3² + 4² = 25", 3.6, -0.45)
        self.play(FadeIn(f1), run_time=0.5)
        self.play(FadeIn(f2), run_time=0.5)
        done(self)


# ═══════════════════════════════════════════ B27 ═══════════════════════════════════════════
class B27_UnitArrow(Scene):
    def construct(self):
        O = np.array([-4.5, 2.3, 0]); s = 1.0
        axes = a4_axes(O, s, 5.0, 4.6)
        arc = Arc(radius=1.0, start_angle=0, angle=-PI / 2, arc_center=O, stroke_color=TEAL, stroke_width=8)
        ulab = a4_t("unit circle", O[0] + 1.5, O[1] + 0.55)
        tag = chip("normalize(v)", 3.4, 2.4)
        sub = a4_t("same direction, length 1", 3.4, 1.65)
        self.play(Create(axes), Create(arc), FadeIn(ulab), FadeIn(tag), FadeIn(sub), run_time=1.0)
        d = np.array([0.6, -0.8, 0])
        tip = O + d * 5.0
        until(self, "Take the arrow")
        ghost = vec_arrow(O, tip, color=DIM, w=7)
        l5 = a4_t("length 5", tip[0] + 1.35, tip[1] + 1.2)
        self.play(Create(ghost), run_time=1.1)
        self.play(FadeIn(l5), run_time=0.5)
        until(self, "Normalize it and you get")
        k = ValueTracker(5.0)
        live = always_redraw(lambda: vec_arrow(O, O + d * k.get_value(), color=INK, w=8))
        self.add(live)
        self.play(k.animate.set_value(1.0), run_time=1.5, rate_func=smooth)
        land = Dot(O + d * 1.0, radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        pl = a4_t("(0.6, 0.8)", O[0] + 0.6 + 1.75, O[1] - 0.8 + 0.1)
        self.play(FadeIn(land), FadeIn(pl), run_time=0.5)
        until(self, "length one")
        l1 = a4_t("length 1", O[0] + 0.6 + 1.5, O[1] - 0.8 - 0.55)
        self.play(ReplacementTransform(l5, l1), run_time=0.6)
        done(self)


# ═══════════════════════════════════════════ B28 ═══════════════════════════════════════════
class B28_AskEveryPixel(Scene):
    def construct(self):
        uv = uv_square(size=4.4, x=-1.8, y=-0.35)
        t1 = a4_m("distance(a, b)", 3.2, 2.25)
        t2 = a4_m("= length(a − b)", 3.2, 1.6)
        self.play(Create(uv), FadeIn(t1), FadeIn(t2), run_time=1.0)
        until(self, "Pick the middle")
        P = uv.pt
        mid = Dot(P(0.5, 0.5), radius=0.18, color=TERRA).set_stroke(DIM, width=3)
        mlab = a4_t("middle", P(0.5, 0.5)[0] - 0.95, P(0.5, 0.5)[1] + 0.4)
        self.play(FadeIn(mid, scale=1.5), FadeIn(mlab), run_time=0.6)

        def pix(u, v, txt, off):
            p = P(u, v)
            dot = Dot(p, radius=0.15, color=TEAL)
            ln = DashedLine(P(0.5, 0.5), p, color=DIM, stroke_width=4, dash_length=0.12)
            lab = a4_t(txt, p[0] + off[0], p[1] + off[1])
            return ln, dot, lab

        until(self, "ask every pixel")
        for (u, v, txt, off) in [(0.9, 0.5, "0.40", (0.8, 0.0)), (0.5, 0.2, "0.30", (0.0, 0.42)), (0.15, 0.85, "0.49", (0.0, -0.42))]:
            ln, dot, lab = pix(u, v, txt, off)
            self.play(Create(ln), FadeIn(dot, scale=1.4), FadeIn(lab), run_time=0.6)
        until(self, "small numbers")
        ln, dot, lab = pix(0.55, 0.55, "0.07", (0.65, -0.1))
        self.play(Create(ln), FadeIn(dot, scale=1.4), FadeIn(lab), run_time=0.7)
        until(self, "big ones", lead=0.6)
        ln, dot, lab = pix(0.95, 0.95, "0.64", (-0.75, 0.0))
        self.play(Create(ln), FadeIn(dot, scale=1.4), FadeIn(lab), run_time=0.5)
        done(self)


# ═══════════════════════════════════════════ B30 ═══════════════════════════════════════════
def a4_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B30_RoundOnSquare(Scene):
    def construct(self):
        L = -2.5; cy = -0.3; S = 3.0
        sq = Rectangle(width=S, height=S, stroke_color=INK, stroke_width=6).move_to([L + S / 2, cy, 0])
        circ = Ellipse(width=0.6 * S, height=0.6 * S, stroke_color=TEAL, stroke_width=8).move_to([L + S / 2, cy, 0])

        def top(width):
            y = cy + S / 2 + 0.55
            g = VGroup(a4_t("0", L, y), a4_t("1", L + width, y), arrow([L + 0.45, y, 0], [L + width - 0.45, y, 0], color=DIM, w=5, tip=0.2))
            return g
        t0 = top(S)
        y_top = cy + S / 2; y_bot = cy - S / 2
        lx = L - 0.65
        left = VGroup(a4_t("0", lx, y_top - 0.1), a4_t("1", lx, y_bot + 0.1), arrow([lx, y_top - 0.6, 0], [lx, y_bot + 0.6, 0], color=DIM, w=5, tip=0.2))
        cap1 = a4_t("square: round", L + S / 2, -2.35)
        self.play(Create(sq), Create(circ), FadeIn(t0), FadeIn(left), FadeIn(cap1), run_time=1.0)
        until(self, "On a wide one")
        pt = np.array([L, cy, 0])
        t1 = top(2 * S)
        self.play(sq.animate.stretch(2, 0, about_point=pt), circ.animate.stretch(2, 0, about_point=pt),
                  ReplacementTransform(t0, t1), run_time=1.6, rate_func=smooth)
        cap2 = a4_t("wide: oval", L + S, -2.35)
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)
        until(self, "The address always runs")
        r1 = a4_ubar(t1, pad=0.15); r2 = a4_ubar(left, pad=0.15)
        self.play(Create(r1), Create(r2), run_time=0.7)
        until(self, "whatever the proportions")
        cr = a4_t("measured: 384 × 192 px · Godot 4.7.2 · Forward+", 0.0, -3.0, 32, DIM)
        self.play(FadeIn(cr), run_time=0.6)
        done(self)


# ═══════════════════════════════════════════ B32 ═══════════════════════════════════════════
class B32_BendTheCurve(Scene):
    def construct(self):
        size = 4.0; cx = -2.0; cy = 0.9
        x0 = cx - size / 2; y0 = cy - size / 2; ys = y0 - 0.95
        axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + size, 0], color=INK, stroke_width=5))
        labs = VGroup(a4_t("0", x0, y0 - 0.38), a4_t("1", x0 + size, y0 - 0.38), a4_t("input", cx, ys - 0.55),
                      a4_t("1", x0 - 0.35, y0 + size), a4_t("0", x0 - 0.35, y0))
        outl = T("output", 32).rotate(PI / 2).move_to([x0 - 0.95, cy, 0])
        tag = chip("pow(x, y)", 3.5, 2.45)
        sub = a4_t("x to the power y", 3.5, 1.7)

        def pt_of(fn):
            return lambda xv: np.array([x0 + xv * size, y0 + float(fn(np.array([xv]))[0]) * size, 0.0])

        def mk_curve(fn, color, w=8):
            p = pt_of(fn)
            c = VMobject(stroke_color=color, stroke_width=w)
            c.set_points_as_corners([p(v) for v in np.linspace(0, 1, 100)])
            return c

        tr = ValueTracker(0.0)

        def mk_dot(fn):
            p = pt_of(fn)
            d = Dot(p(0.0), radius=0.15, color=TERRA).set_stroke(DIM, width=3)
            d.add_updater(lambda m: m.move_to(p(tr.get_value())))
            dl = DashedLine(p(0.0), [x0, ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
            dl.add_updater(lambda m: m.become(DashedLine(p(tr.get_value()), [x0 + tr.get_value() * size, ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)))
            return d, dl

        f3, fh, f1 = a4_f("pow_3"), a4_f("pow_half"), a4_f("identity")
        self.play(Create(axes), FadeIn(labs), FadeIn(outl), FadeIn(tag), FadeIn(sub), run_time=1.0)

        def legend(row, txt, color):
            y = 0.8 - row * 0.75
            return VGroup(Line([1.7, y, 0], [2.4, y, 0], color=color, stroke_width=9), a4_m(txt, 0, y).align_to([2.7, y, 0], LEFT))

        until(self, "On a ramp from zero to one")
        c3 = mk_curve(f3, INK); lg3 = legend(0, "x^3", INK)
        d, dl = mk_dot(f3)
        tiles = a4_strip(f3, x0, size, ys)
        tr.set_value(0.0)
        a4_reveal(tiles, tr)
        self.add(tiles)
        self.play(Create(c3), FadeIn(lg3), run_time=1.2)
        self.add(d, dl)
        until(self, "a power above one")
        self.play(tr.animate.set_value(0.5), run_time=1.0, rate_func=linear)
        until(self, "so only the far end")
        self.play(tr.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        # power 1/2
        until(self, "Below one")
        tiles.clear_updaters(); d.clear_updaters(); dl.clear_updaters()
        self.remove(d, dl, tiles)
        c3.set_stroke(opacity=0.35)
        ch = mk_curve(fh, TEAL); lgh = legend(1, "x^0.5", TEAL)
        tiles = a4_strip(fh, x0, size, ys)
        tr.set_value(0.0)
        d, dl = mk_dot(fh)
        a4_reveal(tiles, tr)
        self.add(tiles)
        self.play(Create(ch), FadeIn(lgh), run_time=0.8)
        self.add(d, dl)
        self.play(tr.animate.set_value(1.0), run_time=1.1, rate_func=linear)
        until(self, "Exactly one")
        tiles.clear_updaters(); d.clear_updaters(); dl.clear_updaters()
        self.remove(d, dl, tiles)
        ch.set_stroke(opacity=0.35)
        c1 = mk_curve(f1, DIM); lg1 = legend(2, "x", DIM)
        tiles = a4_strip(f1, x0, size, ys)
        tr.set_value(0.0)
        d, dl = mk_dot(f1)
        a4_reveal(tiles, tr)
        self.add(tiles)
        self.play(Create(c1), FadeIn(lg1), run_time=0.6)
        self.add(d, dl)
        self.play(tr.animate.set_value(1.0), run_time=0.7, rate_func=linear)
        done(self)


# ═══════════════════════════════════════════ B34 ═══════════════════════════════════════════
class B34_SmoothRepeat(Scene):
    def construct(self):
        W = 4.6; H = 2.6; cx = -2.3; cy = 0.65
        x0 = cx - W / 2; yb = cy - H / 2; ym = cy
        sf = a4_f("sine_two_cycles")
        raw = lambda x: 2.0 * sf(x) - 1.0
        ys = yb - 0.95
        axes = VGroup(Line([x0, yb, 0], [x0, yb + H, 0], color=INK, stroke_width=5), Line([x0, ym, 0], [x0 + W, ym, 0], color=INK, stroke_width=5))
        tick_lo = a4_t("−1", x0 - 0.55, yb); tick_hi = a4_t("1", x0 - 0.35, yb + H)
        tick_0 = a4_t("0", x0 - 0.35, ym)
        ainp = a4_t("input", cx, yb - 0.4)
        a = ValueTracker(1.0); c = ValueTracker(0.0); tr = ValueTracker(0.0)

        def pt(xv):
            lv = c.get_value() + a.get_value() * float(raw(np.array([xv]))[0])
            return np.array([x0 + xv * W, ym + lv * H / 2, 0.0])

        curve = always_redraw(lambda: VMobject(stroke_color=INK, stroke_width=8).set_points_as_corners([pt(v) for v in np.linspace(0, 1, 140)]))
        dot = Dot(pt(0.0), radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        dot.add_updater(lambda m: m.move_to(pt(tr.get_value())))
        tag = a4_m("sin(x)", 3.3, 2.45)
        s1 = a4_t("a smooth wave", 3.4, 1.7)
        s2 = a4_t("between −1 and 1", 3.4, 1.15)
        self.play(Create(axes), FadeIn(ainp), FadeIn(tag), run_time=0.9)
        until(self, "Sine repeats smoothly")
        self.add(curve)
        self.play(FadeIn(tick_lo), FadeIn(tick_hi), FadeIn(tick_0), FadeIn(s1), FadeIn(s2), run_time=0.6)
        self.add(dot)
        self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=linear)
        until(self, "Half of sine")
        newhi = a4_t("1", x0 - 0.35, ym + H / 2)
        newlo = a4_t("0", x0 - 0.35, ym)
        tiles = a4_strip(sf, x0, W, ys)
        for t in tiles:
            t.set_fill(opacity=0)
        self.play(a.animate.set_value(0.5), c.animate.set_value(0.5), FadeOut(tick_lo), FadeOut(tick_hi), FadeOut(tick_0),
                  FadeOut(s1), FadeOut(s2), run_time=1.4, rate_func=smooth)
        sq = a4_m("0.5 + 0.5 · sin(x)", 3.3, 1.7)
        self.play(FadeIn(newhi), FadeIn(newlo), FadeIn(sq), run_time=0.5)
        self.add(tiles)
        self.play(*[t.animate.set_fill(opacity=1) for t in tiles], run_time=0.8)
        until(self, "smooth cousin")
        # fract(2x) teeth in 0..1, a faint ghost
        ph = lambda xv, v: [x0 + xv * W, ym + v * H / 2, 0]
        ghost = VGroup(Line(ph(0, 0), ph(0.5, 1), color=DIM, stroke_width=5), Line(ph(0.5, 0), ph(1, 1), color=DIM, stroke_width=5),
                       DashedLine(ph(0.5, 1), ph(0.5, 0), color=DIM, stroke_width=4, dash_length=0.1)).set_opacity(0.8)
        cap = a4_t("smooth cousin", 3.4, 0.4)
        cap2 = a4_t("of fract", 3.4, -0.2)
        self.play(Create(ghost), FadeIn(cap), FadeIn(cap2), run_time=1.0)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Build a Ring (B37).  The standard plot with the input as the distance d (0 to 0.7)."""


def a5_step(edge, x):
    """Same formula as plot_data.step (a5_ copy: Gate A runs scenes.py without evidence/, where PD is None)."""
    return np.where(x < edge, 0.0, 1.0)


class B37_TwoCuts(Scene):
    def construct(self):
        fA = lambda u: a5_step(0.3, 0.7 * u)
        fB = lambda u: a5_step(0.38, 0.7 * u)
        fR = lambda u: a5_step(0.3, 0.7 * u) - a5_step(0.38, 0.7 * u)   # = PD.CURVES["ring_profile_hard"]
        g = plot_with_strip(fR, x=-1.2, y=0.45, size=3.8)
        lab = g[3]
        lab[2].become(T("distance", 32).move_to([g.x1 + 1.1, g.y0 - 0.38, 0]))
        lab[1].become(T("0.7", 32).move_to([g.x1, g.y0 - 0.38, 0]))
        one = T("1", 32).move_to([g.x0 - 0.3, g.y0 + g.size, 0])
        s0 = T("0", 32).move_to([g.x0, g.ystrip - 0.55, 0]); s1 = T("0.7", 32).move_to([g.x1, g.ystrip - 0.55, 0])
        ghost = Rectangle(width=g.size + 0.15, height=0.62, stroke_color=GHOST, stroke_width=3).move_to([g.x0 + g.size / 2, g.ystrip, 0])

        def curve(fn, color, w):
            xs = np.linspace(0, 1, 400)
            ys = [g.pt(v)[1] for v in xs]
            pts = [np.array([g.x0 + v * g.size, g.y0 + float(fn(np.array([v]))[0]) * g.size, 0.0]) for v in xs]
            return VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(pts)
        cA = curve(fA, "#B9B4A6", 8); cB = curve(fB, DIM, 8)
        pulse = curve(fR, INK, 12)
        tag = a1_tag = M("ring = step(0.3, d) - step(0.38, d)", 32).move_to([0.2, 3.05, 0])
        # legend (right)
        def leg(txt, y, color, w):
            return VGroup(Line([2.9, y, 0], [3.5, y, 0], color=color, stroke_width=w), T(txt, 32).move_to([4.35, y, 0]))
        lA = leg("A", 1.5, "#B9B4A6", 8); lB = leg("B", 0.8, DIM, 8); lR = leg("A - B", 0.1, INK, 12)
        g.tiles.set_fill(opacity=0)
        self.add(g.axes, lab[2], one, s0, s1, ghost, tag)
        until(self, "Step at point three is", lead=0.1)
        self.play(Create(cA), FadeIn(lA), run_time=1.0)
        until(self, "Step at point three eight", lead=0.1)
        self.play(Create(cB), FadeIn(lB), run_time=0.9)
        until(self, "The first minus the second", lead=0.0)
        for t in g.tiles:
            pass
        # light the strip band: true gray of the pulse value
        pitch = g.size / 64
        for i, t in enumerate(g.tiles):
            v = float(fR(np.array([i / 63.0]))[0])
            gg = int(round(255 * v)); t.set_fill(color="#%02x%02x%02x" % (gg, gg, gg))
        fade_lim = ValueTracker(0.0)
        g.tiles.add_updater(lambda m: [t.set_fill(opacity=1.0 if t.get_center()[0] <= g.x0 + fade_lim.get_value() * g.size + pitch * 0.5 else 0.0) for t in m])
        self.add(g.tiles)
        self.play(Create(pulse), FadeIn(lR), fade_lim.animate.set_value(1.0), run_time=1.1)
        until(self, "a pulse", lead=0.9)
        g.tracker.set_value(0.0)
        self.add(g.drop, g.dot)
        self.play(FadeIn(g.dot, scale=0.4), run_time=0.3)
        self.play(g.tracker.animate.set_value(1.0), run_time=0.8, rate_func=linear)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
