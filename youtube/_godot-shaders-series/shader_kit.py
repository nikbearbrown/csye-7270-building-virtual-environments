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
