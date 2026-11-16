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
"""ACT I · The Shape of a File  (B03, B04, B07, B08, B09: the Manim beats of this act)

Cast for the act: the shader file as monospace lines placed on an explicit character grid (A1_CW per character, so Pango can never fuse or drop a
space), the real Lab renders shown as themselves (lab_window of pantry/*.png), and drawn marks (ring, check, cross, bracket, arrow) for the claims.
Every code line is a line of a real file in lab-shaders/ (04-globals, 02-spacing-*, 03-comment-*, 41-err-case); nothing is mocked.
"""

A1P = "pantry/"


def a1_cw(size=32):
    """Advance of one Menlo character at this size, measured once with Manim 0.20.1 (font scaling is not linear in size: 32 -> 0.25, 40 -> 0.35).
    Constants, not a runtime measurement: Gate A's stub Text has no real widths."""
    return {32: 0.25, 36: 0.30, 40: 0.35}.get(size, 0.25 * size / 32)


def a1_mono(s, xl, y, size=32, color=INK, t2c=None):
    """One code line, LEFT edge on the character grid: leading spaces become columns, so indentation and spaces are exact."""
    ind = len(s) - len(s.lstrip(" "))
    t = Text(s.lstrip(" "), font=MONO, color=color, font_size=size, t2c=t2c or {})
    t.move_to([xl + ind * a1_cw(size) + t.width / 2, y, 0])
    return t


def a1_x(xl, col, size=32):
    """Scene x of the left edge of column `col` (0-based) of a line whose left edge is xl."""
    return xl + col * a1_cw(size)


def a1_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_check(x, y, s=0.26, color=TEAL, sw=9):
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(
        [np.array([x - s, y, 0]), np.array([x - s * 0.3, y - s * 0.75, 0]), np.array([x + s, y + s * 0.8, 0])])


def a1_cross(x, y, s=0.26, color=INK, sw=8):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=sw),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=sw))


def a1_equals(x, y, w=0.7, gap=0.2):
    return VGroup(Line([x - w / 2, y + gap / 2, 0], [x + w / 2, y + gap / 2, 0], color=INK, stroke_width=7),
                  Line([x - w / 2, y - gap / 2, 0], [x + w / 2, y - gap / 2, 0], color=INK, stroke_width=7))


def a1_glyphs(lines):
    """All the glyph pieces (non-space characters, in reading order) of a list of code-line Texts."""
    return VGroup(*[g for ln in lines for g in ln.submobjects])


# ═════════════════════════════ B03 · the header ═════════════════════════════
def a1_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B03_Header(Scene):
    def construct(self):
        xl = -3.75
        line1 = a1_mono("shader_type canvas_item;", xl, 2.85, 40)
        # tiles: row 1 (the two big types), row 2 (three more)
        def tile(txt, x, y, w):
            b = box(x, y, w, 0.72, INK, 4)
            return VGroup(b, M(txt, 32).move_to([x, y, 0]))
        t_canvas = tile("canvas_item", -2.55, 1.5, 3.3)
        t_spatial = tile("spatial", 2.3, 1.5, 2.5)
        cap_c = a1_t("2D + interface", -2.55, 0.75)
        cap_s = a1_t("3D", 2.3, 0.85)
        t_part = tile("particles", -2.5, -0.35, 2.7)
        t_sky = tile("sky", 0.05, -0.35, 1.5)
        t_fog = tile("fog", 2.0, -0.35, 1.5)
        bx0, bx1, by = -3.85, 2.75, -0.95
        bracket = VGroup(Line([bx0, by, 0], [bx1, by, 0], color=DIM, stroke_width=5), Line([bx0, by, 0], [bx0, by + 0.15, 0], color=DIM, stroke_width=5),
                         Line([bx1, by, 0], [bx1, by + 0.15, 0], color=DIM, stroke_width=5))
        cap_more = a1_t("more", (bx0 + bx1) / 2, by - 0.4)
        lx0, lx1, ly = a1_x(xl, 12, 40) - 0.05, a1_x(xl, 23, 40) - 0.15, 2.38
        ring_line = VGroup(Line([lx0, ly, 0], [lx1, ly, 0], color=DIM, stroke_width=6), Line([lx0, ly, 0], [lx0, ly + 0.14, 0], color=DIM, stroke_width=6),
                           Line([lx1, ly, 0], [lx1, ly + 0.14, 0], color=DIM, stroke_width=6),
                           Dot([(lx0 + lx1) / 2, ly - 0.2, 0], radius=0.11, color=TERRA).set_stroke(DIM, width=3))
        ring_tile = a1_ubar(t_canvas[0], pad=0.1)
        # the optional second line
        rx = -6.0
        line2 = a1_mono("render_mode blend_add;", rx, -2.3, 32, DIM)
        opt = VGroup(box(1.1, -2.3, 2.1, 0.62, DIM, 3), a1_t("optional", 1.1, -2.3))
        sq_a = Square(side_length=1.0, stroke_color=INK, stroke_width=5).move_to([4.0, -2.3, 0])
        sq_b = Square(side_length=1.0, stroke_color=INK, stroke_width=5).move_to([4.55, -2.3 - 0.0, 0]).shift(UP * 0.05)
        overlap = Rectangle(width=0.45, height=0.95, stroke_width=0).set_fill("#CFE3DC", opacity=1).move_to([4.275, -2.275, 0])
        cap_blend = a1_t("blend", 4.28, -3.05)

        until(self, "The header starts", lead=0.0)
        self.play(AddTextLetterByLetter(line1, time_per_char=0.05), run_time=1.3)
        until(self, "Canvas item means", lead=0.9)
        self.play(LaggedStart(Create(t_canvas), Create(t_spatial), Create(t_part), Create(t_sky), Create(t_fog), lag_ratio=0.3), run_time=1.4)
        until(self, "Canvas item means", lead=0.0)
        self.play(FadeIn(ring_line), FadeIn(ring_tile), FadeIn(cap_c), run_time=0.5)
        until(self, "Spatial means", lead=0.1)
        self.play(FadeIn(cap_s), FadeIn(bracket), FadeIn(cap_more), run_time=0.4)
        until(self, "An optional second line", lead=0.0)
        self.play(FadeIn(line2, shift=RIGHT * 0.6), FadeIn(opt, shift=RIGHT * 0.3), run_time=0.6)
        until(self, "such as how a pixel blends", lead=0.1)
        self.play(Create(sq_a), Create(sq_b), run_time=0.5)
        self.play(FadeIn(overlap), FadeIn(cap_blend), run_time=0.4)
        done(self)


# ═════════════════════════════ B04 · globals ═════════════════════════════
class B04_Globals(Scene):
    def construct(self):
        xl = -5.3
        band = box(0.0, 0.8, 12.2, 5.0, DIM, 4)
        lab = a1_t("globals", -4.9, 2.95, 32)
        rows = [
            ("uniform float level = 0.8;", ["a value your game sets from outside;", "every pixel sees the same one"], 2.3),
            ("const vec3 TEAL = vec3(0.37, 0.64, 0.57);", ["a named value that never changes"], 0.8),
            ("varying vec2 corner_uv;", ["a value set at each corner, blended across", "the shape for fragment() to read"], -0.3),
        ]
        groups = []
        for decl, caps, y in rows:
            dot = Dot([-5.75, y, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3)
            d = a1_mono(decl, xl, y)
            cs = VGroup(*[a1_t(c, xl + 0.0, y - 0.5 - 0.42 * i).align_to([xl, 0, 0], LEFT) for i, c in enumerate(caps)])
            groups.append(VGroup(dot, d, cs))
        fbar = box(0.0, -2.9, 12.2, 0.62, INK, 4)
        flab = a1_t("functions", -4.9, -2.9, 32)
        down = arrow([-2.3, -1.75, 0], [-2.3, -2.55, 0], INK, 7)
        rd = a1_t("readable below", 0.1, -2.15)

        self.play(Create(band), FadeIn(lab), Create(fbar), FadeIn(flab), run_time=0.7)
        until(self, "A uniform is", lead=0.1)
        self.play(FadeIn(groups[0], shift=RIGHT * 0.3), run_time=0.5)
        until(self, "A const never", lead=0.1)
        self.play(FadeIn(groups[1], shift=RIGHT * 0.3), run_time=0.5)
        until(self, "A varying hands", lead=0.1)
        self.play(FadeIn(groups[2], shift=RIGHT * 0.3), run_time=0.5)
        until(self, "Declare each one", lead=0.1)
        self.play(GrowArrow(down), FadeIn(rd), run_time=0.6)
        done(self)


# ═════════════════════════════ B07 · three spellings ═════════════════════════════
class B07_ThreeSpellings(Scene):
    def construct(self):
        xl = -6.0
        lh = 0.55
        top, bot = 3.3, -0.45
        cy = (top + bot) / 2
        card = box(0.0, cy, 12.5, top - bot, DIM, 4, fill=PALEBOX, radius=0.14)
        neat = ["shader_type canvas_item;", "", "void fragment() {", "  COLOR = vec4(0.4 + 0.6 * UV, 0.7, 1.0);", "}"]
        squeezed = ["shader_type canvas_item;", "void fragment(){COLOR=vec4(0.4+0.6*UV,0.7,1.0);}"]
        spread = ["shader_type canvas_item;", "", "void fragment() {", "  COLOR = vec4(", "    0.4 + 0.6 * UV,", "    0.7, 1.0);", "}"]

        def build(lines):
            hs = [(lh * 0.5 if not s else lh) for s in lines]
            tot = sum(hs)
            y = cy + tot / 2
            out = []
            for s, h in zip(lines, hs):
                if s:
                    out.append(a1_mono(s, xl, y - h / 2))
                y -= h
            return out
        A, B, C = build(neat), build(squeezed), build(spread)
        gA, gB, gC = a1_glyphs(A), a1_glyphs(B), a1_glyphs(C)
        assert len(gA) == len(gB) == len(gC), (len(gA), len(gB), len(gC))
        names = VGroup()
        pic = lab_window(A1P + "spacing.png", 2.5, -2.6, -1.75, "")
        cap = a1_t("Godot 4.7.2 · Forward+", -2.6, -2.9)
        eq = a1_equals(0.55, -1.75)
        same = a1_t("same picture", 2.6, -1.75)
        tag = a1_t("neat", 5.4, 2.95, 32, DIM)

        self.play(Create(card), run_time=0.4)
        self.add(gA)
        self.play(FadeIn(gA), FadeIn(pic), FadeIn(cap), run_time=0.7)
        until(self, "squeezed onto one line", lead=0.55)
        self.play(Transform(gA, gB), run_time=1.0)
        until(self, "spread over many", lead=0.55)
        self.play(Transform(gA, gC), run_time=1.0)
        until(self, "Godot draws the same", lead=0.2)
        self.play(FadeIn(eq), FadeIn(same), run_time=0.5)
        done(self)


# ═════════════════════════════ B08 · comment out ═════════════════════════════
class B08_CommentOut(Scene):
    def construct(self):
        xl = -6.05
        lh = 0.45
        top = 2.6
        src_on = ["shader_type canvas_item;", "", "/* A note for people,", "   over two lines. */", "void fragment() {",
                  "  vec3 c = vec3(UV, 0.5);", "  c = 0.4 + 0.6 * c; // soften", "  COLOR = vec4(c, 1.0);", "}"]
        card = box(-1.7, top - 0.15 - len(src_on) * lh / 2, 9.0, len(src_on) * lh + 0.3, DIM, 4, fill=PALEBOX, radius=0.14)
        lines = []
        for i, s in enumerate(src_on):
            y = top - 0.15 - lh * (i + 0.5)
            if not s:
                continue
            if i in (2, 3):
                lines.append(a1_mono(s, xl, y, color=DIM))
            elif i == 6:
                lines.append(a1_mono(s, xl, y, t2c={"// soften": DIM}))
            else:
                lines.append(a1_mono(s, xl, y))
        y6 = top - 0.15 - lh * 6.5
        off6 = a1_mono("  // c = 0.4 + 0.6 * c; // soften", xl, y6, color=DIM)
        idx6 = [k for k, s in enumerate([s for s in src_on if s]) if s.startswith("  c = 0.4")][0]
        on6 = lines[idx6]
        xr = 4.7
        on_pic = lab_window(A1P + "comment-on.png", 2.9, xr, 1.45, "Godot 4.7.2")
        off_im = ImageMobject(A1P + "comment-off.png").set_width(2.9).move_to([xr, 1.45, 0])
        # captions with drawn brackets
        bkx = a1_x(xl, 23.5)
        by_top, by_bot = top - 0.15 - lh * 2.5 + 0.18, top - 0.15 - lh * 3.5 - 0.18
        blk = VGroup(Line([bkx, by_top, 0], [bkx, by_bot, 0], color=DIM, stroke_width=5),
                     Line([bkx, by_top, 0], [bkx - 0.14, by_top, 0], color=DIM, stroke_width=5),
                     Line([bkx, by_bot, 0], [bkx - 0.14, by_bot, 0], color=DIM, stroke_width=5))
        blk_cap = a1_t("block comment", bkx + 1.4, (by_top + by_bot) / 2)
        lin_cap = a1_t("line comment", 4.7, y6)
        lin = arrow([3.45, y6, 0], [a1_x(xl, 30) + 0.12, y6, 0], DIM, 5, 0.2)

        self.play(Create(card), run_time=0.4)
        self.play(FadeIn(VGroup(*lines)), FadeIn(on_pic), run_time=0.6)
        until(self, "Two slashes comment out", lead=0.15)
        self.play(GrowArrow(lin), FadeIn(lin_cap), run_time=0.5)
        until(self, "Slash star starts", lead=0.15)
        self.play(Create(blk), FadeIn(blk_cap), run_time=0.5)
        until(self, "Godot skips both", lead=0.3)
        self.play(Transform(on6, off6), FadeOut(lin), FadeOut(lin_cap), FadeIn(off_im), run_time=1.0)
        done(self)


# ═════════════════════════════ B09 · names must match ═════════════════════════════
class B09_NamesMustMatch(Scene):
    def construct(self):
        cap1 = a1_t("GLSL: the OpenGL Shading Language.", 0, 3.0)
        cap2 = a1_t("Godot's is close to GLSL ES 3.0.", 0, 2.5)
        pl = box(-3.2, -0.55, 5.8, 4.2, DIM, 4)
        pr = box(3.2, -0.55, 5.8, 4.2, DIM, 4)

        def tagbox(txt, x, y, w):
            return VGroup(box(x, y, w, 0.78, INK, 4), M(txt, 32).move_to([x, y, 0]))
        lv = tagbox("level", -4.0, 0.7, 2.2)
        LV = tagbox("Level", -4.0, -0.6, 2.2)
        ok = a1_check(-2.2, 0.7)
        bad = a1_cross(-2.2, -0.6)
        cl = LV[1][0]
        ul = Line([cl.get_left()[0], -1.12, 0], [cl.get_right()[0], -1.12, 0], color=DIM, stroke_width=6)
        ringL = VGroup(ul, Dot([cl.get_center()[0], -1.32, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3))
        capL = a1_t("capitals count", -3.0, -1.9)
        gl = tagbox("gl_FragColor", 2.2, 0.7, 3.5)
        badg = a1_cross(4.4, 0.7)
        co = tagbox("COLOR", 2.2, -0.9, 2.2)
        okc = a1_check(4.0, -0.9)
        arr = arrow([2.2, 0.25, 0], [2.2, -0.45, 0], INK, 6)
        capc = a1_t("Godot's name for the output", 3.2, -1.8)

        self.play(FadeIn(cap1), FadeIn(cap2), Create(pl), Create(pr), run_time=0.6)
        self.play(FadeIn(lv), FadeIn(LV), run_time=0.4)
        until(self, "Names must match", lead=0.1)
        self.play(Create(ok), run_time=0.3)
        until(self, "a capital L makes", lead=0.1)
        self.play(Create(bad), FadeIn(ringL), FadeIn(capL), run_time=0.5)
        until(self, "The other language's", lead=0.2)
        self.play(FadeIn(gl), run_time=0.3)
        self.play(Create(badg), run_time=0.3)
        until(self, "Godot calls it", lead=0.2)
        self.play(GrowArrow(arr), FadeIn(co), run_time=0.5)
        self.play(Create(okc), FadeIn(capc), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II . Types and Vectors  (B10, B12, B13, B14, B16, B19; all Manim)

Cast for the act: the bundle, a row of outlined cells (1 to 4 cells; the count IS the size), small type tags, mono code with
explicit per-token coordinates (Pango may drop spaces). Every drawing here is a drawing; the numbers are the Lab's own
(0.4/0.7/0.6/1.0 from 33-swizzle-pick; 0.37/0.64/0.57/1.0 are the sprite centre of 08-texture-vec4 to two places).
"""

_A2_CW = []


def a2_cw():
    """Width of one Menlo character at size 32 (measured once)."""
    if not _A2_CW:
        _A2_CW.append(M("0" * 20).width / 20.0)
    return _A2_CW[0]


def a2_code(line, x_left, y, size=32):
    """A mono code line with EXPLICIT coordinates: one Text per token, each placed by its character index (so a dropped space cannot shift anything).
    Returns VGroup with .tokens (list of (start, end, Text)) and .xs(i) -> scene x of the left edge of character i."""
    cw = a2_cw() * size / 32.0
    g = VGroup()
    toks = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] == " ":
            i += 1
            continue
        j = i
        while j < n and line[j] != " ":
            j += 1
        t = M(line[i:j], size)
        t.move_to([x_left + (i + (j - i) / 2.0) * cw, y, 0])
        g.add(t)
        toks.append((i, j, t))
        i = j
    g.tokens = toks
    g.xs = lambda k: x_left + k * cw
    g.cw = cw
    return g


def a2_cell(x, y, txt="", w=1.05, h=0.82, color=INK, sw=4):
    """One outlined cell of the bundle (no fill behind the text). Returns VGroup(frame, text) with .frame."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=sw).move_to([x, y, 0])
    g = VGroup(fr)
    g.frame = fr
    g.txt = None
    if txt:
        t = T(txt, 32).move_to([x, y, 0])
        g.add(t)
        g.txt = t
    return g


def a2_bundle(vals, x0, y, pitch=1.15, w=1.05, h=0.82):
    """A row of cells starting at x0. Returns VGroup of cells with .cells."""
    cells = [a2_cell(x0 + k * pitch, y, v, w, h) for k, v in enumerate(vals)]
    g = VGroup(*cells)
    g.cells = cells
    return g


def a2_tag(text, x, y, size=32):
    """A small outlined type tag centred at (x, y)."""
    t = T(text, size) if not text.startswith(".") else M(text, size)
    box_ = RoundedRectangle(width=t.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
    g = VGroup(box_, t).move_to([x, y, 0])
    return g


def a2_title(s):
    t = T(s, 40)
    t.move_to([-6.2 + t.width / 2.0, 3.0, 0])
    return t


# ───────────────────────────── B10 . three types ─────────────────────────────
class B10_ThreeTypes(Scene):
    def construct(self):
        title = a2_title("Types and Vectors")
        xs = [-4.5, -1.5, 1.5, 4.5]
        ty = 1.35
        specs = [("float", "0.5", "decimal number"), ("int", "3", "whole number"), ("bool", "true", "true or false"), ("sampler2D", None, "texture's type")]
        tiles = []
        for x, (ty_name, val, lab) in zip(xs, specs):
            fr = box(x, ty, 2.75, 1.5, INK, 4)
            nm = M(ty_name, 32).move_to([x, ty + 0.42, 0])
            if val is not None:
                v = M(val, 32).move_to([x, ty - 0.22, 0])
            else:
                sq = Square(side_length=0.62, stroke_color=INK, stroke_width=4).move_to([x, ty - 0.27, 0])
                hill = VMobject(stroke_color=TEAL, stroke_width=5).set_points_as_corners([[x - 0.26, ty - 0.45, 0], [x - 0.08, ty - 0.2, 0], [x + 0.06, ty - 0.36, 0], [x + 0.26, ty - 0.12, 0]])
                v = VGroup(sq, hill)
            l = T(lab, 32).move_to([x, ty - 1.2, 0])
            tiles.append(VGroup(fr, nm, v, l))
        self.add(title)
        self.wait(0.2)
        self.play(FadeIn(tiles[0], scale=0.8), run_time=0.4)
        until(self, "an int")
        self.play(FadeIn(tiles[1], scale=0.8), run_time=0.4)
        until(self, "a bool")
        self.play(FadeIn(tiles[2], scale=0.8), run_time=0.4)
        until(self, "A texture", lead=0.7)
        self.play(FadeIn(tiles[3], scale=0.8), run_time=0.4)
        cap = T("texture: an image a shader can read by address", 32).move_to([0, -0.55, 0])
        self.play(FadeIn(cap), run_time=0.4)
        # the declaration, typed in
        until(self, "You declare", lead=0.9)
        decl = a2_code("float level = 0.5;", -18 * a2_cw() * 1.25 / 2.0, -1.65, 40)
        self.play(LaggedStart(*[FadeIn(t) for _, _, t in decl.tokens], lag_ratio=0.35), run_time=0.9)
        cw = decl.cw
        y_b = -1.65 - 0.5

        def span(i0, i1):
            return decl.xs(i0), decl.xs(i1)
        tg1 = type_tag("type", *span(0, 5), y_b)
        tg2 = type_tag("name", *span(6, 11), y_b)
        tg3 = type_tag("value", *span(14, 17), y_b)
        until(self, "its type first")
        self.play(Create(tg1.bracket), FadeIn(tg1.tag), run_time=0.35)
        until(self, "then its name", lead=0.1)
        self.play(Create(tg2.bracket), FadeIn(tg2.tag), run_time=0.35)
        self.play(Create(tg3.bracket), FadeIn(tg3.tag), run_time=0.35)
        done(self)


# ───────────────────────────── B12 . bundles ─────────────────────────────
class B12_Bundles(Scene):
    def construct(self):
        x0 = -1.5
        y2, y3, y4 = 2.2, 0.95, -0.3
        r2 = a2_bundle(["", ""], x0, y2)
        r3 = a2_bundle(["", "", ""], x0, y3)
        r4 = a2_bundle(["0.37", "0.64", "0.57", "1.0"], x0, y4)
        n2 = M("vec2", 32).move_to([-2.9, y2, 0])
        n3 = M("vec3", 32).move_to([-2.9, y3, 0])
        n4 = M("vec4", 32).move_to([-2.9, y4, 0])
        letters = VGroup(*[T(c, 32).move_to([x0 + k * 1.15, y4 - 0.78, 0]) for k, c in enumerate("rgba")])
        swatch = RoundedRectangle(width=0.95, height=0.82, corner_radius=0.1, fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to([3.75, y4, 0])
        swl = T("a color", 32).move_to([5.3, y4, 0])
        # a drawn texture: a 4 x 4 gradient of separate tiles
        tex = VGroup()
        for r in range(4):
            for c in range(4):
                tex.add(Rectangle(width=0.27, height=0.27, fill_color=_rgb((r + c) / 6.0), fill_opacity=1, stroke_width=0).move_to([-5.2 + (c - 1.5) * 0.31, y4 + (1.5 - r) * 0.31, 0]))
        texfr = Rectangle(width=1.38, height=1.38, stroke_color=INK, stroke_width=4).move_to([-5.2, y4, 0])
        texl = T("texture lookup", 32).move_to([-5.0, y4 - 1.1, 0])
        tarr = arrow([-4.35, y4, 0], [-3.55, y4, 0])
        cap1 = T("vector: a bundle of two to four numbers", 32).move_to([0, -2.15, 0])
        cap2 = T("alpha: how visible a pixel is: 0 invisible, 1 solid", 32).move_to([0, -2.95, 0])
        self.wait(0.2)
        until(self, "bundles of two")
        self.play(FadeIn(cap1), run_time=0.4)
        until(self, "vec two")
        self.play(FadeIn(n2), LaggedStart(*[FadeIn(c, scale=0.7) for c in r2.cells], lag_ratio=0.3), run_time=0.6)
        until(self, "vec three")
        self.play(FadeIn(n3), LaggedStart(*[FadeIn(c, scale=0.7) for c in r3.cells], lag_ratio=0.3), run_time=0.7)
        until(self, "vec four", lead=0.1)
        self.play(FadeIn(n4), LaggedStart(*[FadeIn(c, scale=0.7) for c in r4.cells], lag_ratio=0.25), FadeIn(letters), run_time=0.9)
        until(self, "A color is")
        self.play(FadeIn(swatch), FadeIn(swl), run_time=0.4)
        until(self, "alpha", lead=0.2)
        self.play(FadeIn(cap2), run_time=0.4)
        until(self, "Reading a texture", lead=0.3)
        self.play(FadeIn(texfr), FadeIn(tex), FadeIn(texl), run_time=0.4)
        self.play(GrowArrow(tarr), run_time=0.4)
        done(self)


# ───────────────────────────── B13 . build a vector ─────────────────────────────
class B13_BuildAVector(Scene):
    def construct(self):
        cw = a2_cw()
        ys = [2.15, 0.1, -1.95]
        lab1 = a2_code("vec3(0.5)", -6.0, ys[0])
        lab2 = a2_code("vec4(c, 1.0)", -6.0, ys[1])
        lab3 = a2_code("vec3(0.1, 0.2)", -6.0, ys[2])
        # (1) one number fills three cells
        c1 = a2_cell(-1.6, ys[0], "0.5")
        c1b = a2_cell(-1.6, ys[0], "0.5")
        c1c = a2_cell(-1.6, ys[0], "0.5")
        # (2) three plus one
        c2 = [a2_cell(-1.6 + k * 1.15, ys[1], "") for k in range(3)]
        dots = [Dot([-1.6 + k * 1.15, ys[1], 0], radius=0.11, color=TEAL) for k in range(3)]
        one = a2_cell(3.2, ys[1], "1.0")
        cnt = T("3 + 1 = 4", 32).move_to([5.0, ys[1], 0])
        # (3) two cells and a gap
        c3 = [a2_cell(-1.6, ys[2], "0.1"), a2_cell(-0.45, ys[2], "0.2")]
        gap = DashedVMobject(RoundedRectangle(width=1.05, height=0.82, corner_radius=0.1, stroke_color=DIM, stroke_width=4).move_to([0.7, ys[2], 0]), num_dashes=24)
        cross = VGroup(Line([0.4, ys[2] - 0.28, 0], [1.0, ys[2] + 0.28, 0], color=INK, stroke_width=7), Line([0.4, ys[2] + 0.28, 0], [1.0, ys[2] - 0.28, 0], color=INK, stroke_width=7))
        cnt3 = T("2 of 3", 32).move_to([3.0, ys[2], 0])
        few = T("too few", 32).move_to([5.0, ys[2], 0])
        self.wait(0.2)
        until(self, "Give vec three one number", lead=0.3)
        self.play(FadeIn(lab1), FadeIn(c1), run_time=0.4)
        self.add(c1b, c1c)
        self.play(c1b.animate.shift(RIGHT * 1.15), c1c.animate.shift(RIGHT * 2.3), run_time=0.7)
        until(self, "Give vec four a vec three", lead=0.3)
        self.play(FadeIn(lab2), LaggedStart(*[FadeIn(c) for c in c2], lag_ratio=0.2), *[FadeIn(d) for d in dots], FadeIn(one), run_time=0.7)
        until(self, "and a number")
        grp1 = VGroup(one)
        self.play(one.animate.move_to([-1.6 + 3 * 1.15, ys[1], 0]), run_time=0.7)
        self.play(FadeIn(cnt), run_time=0.3)
        until(self, "The pieces must add up", lead=0.4)
        self.play(FadeIn(lab3), *[FadeIn(c) for c in c3], FadeIn(gap), run_time=0.5)
        until(self, "Godot refuses", lead=0.3)
        self.play(Create(cross[0]), Create(cross[1]), FadeIn(cnt3), FadeIn(few), run_time=0.6)
        done(self)


# ───────────────────────────── B14 . all at once ─────────────────────────────
class B14_AllAtOnce(Scene):
    def construct(self):
        cols = [-3.8, -2.65, -1.5]
        yt_in, yt_out = 2.5, 1.0
        yb_in, yb_mid, yb_out = -0.45, -1.65, -2.85
        vin = ["0.2", "0.3", "0.4"]
        top_in = [a2_cell(x, yt_in, v) for x, v in zip(cols, vin)]
        top_out = [a2_cell(x, yt_out, v) for x, v in zip(cols, ["0.4", "0.6", "0.8"])]
        two = a2_cell(-5.7, 1.75, "2.0", w=0.9)
        times = VGroup(Line([-4.92, 1.75 - 0.14, 0], [-4.64, 1.75 + 0.14, 0], color=INK, stroke_width=6), Line([-4.92, 1.75 + 0.14, 0], [-4.64, 1.75 - 0.14, 0], color=INK, stroke_width=6))
        lab1 = a2_code("* 2.0", -0.6, 1.75)
        arrs = [arrow([x, yt_in - 0.45, 0], [x, yt_out + 0.45, 0]) for x in cols]
        bot_in = [a2_cell(x, yb_in, v) for x, v in zip(cols, vin)]
        bot_mid = [a2_cell(x, yb_mid, v) for x, v in zip(cols, ["2.0", "1.0", "0.5"])]
        bot_out = [a2_cell(x, yb_out, v) for x, v in zip(cols, ["0.4", "0.3", "0.2"])]
        lab2 = a2_code("* vec3(2.0, 1.0, 0.5)", -0.6, yb_mid)
        pair = [dim_arrow([x, yb_in - 0.43, 0], [x, yb_mid + 0.43, 0], color=DIM, w=5, tip=0.13) for x in cols]
        arrs2 = [arrow([x, yb_mid - 0.43, 0], [x, yb_out + 0.43, 0], w=5, tip=0.14) for x in cols]
        self.wait(0.2)
        self.play(LaggedStart(*[FadeIn(c) for c in top_in], lag_ratio=0.2), run_time=0.6)
        until(self, "by two point zero", lead=0.6)
        self.play(FadeIn(two), FadeIn(times), FadeIn(lab1), run_time=0.4)
        until(self, "all three numbers double", lead=0.5)
        self.play(*[GrowArrow(a) for a in arrs], run_time=0.5)
        self.play(*[FadeIn(c) for c in top_out], run_time=0.3)
        until(self, "Multiply two vectors", lead=0.4)
        self.play(*[FadeIn(c) for c in bot_in], *[FadeIn(c) for c in bot_mid], FadeIn(lab2), run_time=0.5)
        until(self, "each part meets", lead=0.5)
        self.play(*[GrowArrow(a) for a in pair], run_time=0.5)
        self.play(*[GrowArrow(a) for a in arrs2], run_time=0.4)
        self.play(*[FadeIn(c) for c in bot_out], run_time=0.3)
        done(self)


# ───────────────────────────── B16 . swizzle ─────────────────────────────
class B16_Swizzle(Scene):
    def construct(self):
        y0 = -0.35
        xs = [-1.8, -0.6, 0.6, 1.8]
        row = a2_bundle(["0.4", "0.7", "0.6", "1.0"], xs[0], y0)
        xyzw = VGroup(*[T(c, 32).move_to([x, y0 - 0.7, 0]) for x, c in zip(xs, "xyzw")])
        rgba = VGroup(*[T(c, 32).move_to([x, y0 - 1.15, 0]) for x, c in zip(xs, "rgba")])
        stpq = VGroup(*[T(c, 32, DIM).move_to([x, y0 - 1.6, 0]) for x, c in zip(xs, "stpq")])
        n4 = M("vec4", 32).move_to([-3.55, y0, 0])
        cap = T("swizzle: picking or reordering a vector's parts", 32).move_to([0, -2.85, 0])

        def lifted(k, label, dx, dy, tname):
            cells = [a2_cell(xs[i] + dx, y0 + dy, v) for i, v in enumerate(["0.4", "0.7", "0.6", "1.0"][:k])]
            return cells

        xm3 = sum(xs[:3]) / 3.0
        xm2 = sum(xs[:2]) / 2.0
        br3 = VGroup(Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[2] + 0.5, y0 + 0.6, 0], color=DIM, stroke_width=5),
                     Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[0] - 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5),
                     Line([xs[2] + 0.5, y0 + 0.6, 0], [xs[2] + 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5))
        l3 = M(".rgb", 32).move_to([xm3, y0 + 0.98, 0])
        br2 = VGroup(Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[1] + 0.5, y0 + 0.6, 0], color=DIM, stroke_width=5),
                     Line([xs[0] - 0.5, y0 + 0.6, 0], [xs[0] - 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5),
                     Line([xs[1] + 0.5, y0 + 0.6, 0], [xs[1] + 0.5, y0 + 0.45, 0], color=DIM, stroke_width=5))
        l2 = M(".xy", 32).move_to([xm2, y0 + 0.98, 0])
        # lifted copies: vec3 up-left, vec2 up-right
        v3 = [a2_cell(-4.9 + i * 1.15, 1.9, v) for i, v in enumerate(["0.4", "0.7", "0.6"])]
        v3l = M(".rgb", 32).move_to([-3.75, 2.75, 0])
        v3n = M("vec3", 32).move_to([-3.75, 1.05, 0])
        v2 = [a2_cell(2.9 + i * 1.15, 1.9, v) for i, v in enumerate(["0.4", "0.7"])]
        v2l = M(".xy", 32).move_to([3.475, 2.75, 0])
        v2n = M("vec2", 32).move_to([3.475, 1.05, 0])
        self.wait(0.2)
        self.play(FadeIn(row), FadeIn(n4), run_time=0.5)
        self.play(FadeIn(xyzw), FadeIn(rgba), FadeIn(stpq), run_time=0.5)
        until(self, "Dot R G B", lead=0.3)
        self.play(Create(br3), FadeIn(l3), run_time=0.4)
        cp3 = VGroup(*[c.copy() for c in row.cells[:3]])
        self.add(cp3)
        self.play(*[cp3[i].animate.move_to(v3[i].get_center()) for i in range(3)], run_time=0.8)
        self.play(FadeIn(v3l), FadeIn(v3n), FadeOut(br3), FadeOut(l3), run_time=0.3)
        until(self, "Dot X Y", lead=0.3)
        self.play(Create(br2), FadeIn(l2), run_time=0.4)
        cp2 = VGroup(*[c.copy() for c in row.cells[:2]])
        self.add(cp2)
        self.play(*[cp2[i].animate.move_to(v2[i].get_center()) for i in range(2)], run_time=0.8)
        self.play(FadeIn(v2l), FadeIn(v2n), FadeOut(br2), FadeOut(l2), run_time=0.3)
        until(self, "swizzling", lead=0.4)
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ───────────────────────────── B19 . type chain ─────────────────────────────
class B19_TypeChain(Scene):
    def construct(self):
        line = "vec3 c = 0.4 + 0.6 * vec3(UV, 0.5);"
        cw = a2_cw()
        xl = -len(line) * cw / 2.0
        yl = 2.6
        code = a2_code(line, xl, yl)
        xs = code.xs
        y_levels = [yl - 0.5, yl - 1.65, yl - 2.8, yl - 3.95]
        self.add(code)
        self.wait(0.2)
        tg1 = type_tag("vec2", xs(26), xs(28), y_levels[0])
        tg2 = type_tag("vec3", xs(21), xs(34), y_levels[1])
        tg3 = type_tag("vec3", xs(15), xs(34), y_levels[2])
        tg4 = type_tag("vec3", xs(9), xs(34), y_levels[3])
        until(self, "U V is a vec two", lead=0.3)
        self.play(Create(tg1.bracket), FadeIn(tg1.tag), run_time=0.45)
        until(self, "Joined with one half", lead=0.3)
        self.play(Create(tg2.bracket), FadeIn(tg2.tag), run_time=0.45)
        until(self, "Times a float", lead=0.3)
        self.play(Create(tg3.bracket), FadeIn(tg3.tag), run_time=0.45)
        until(self, "Plus a float", lead=0.3)
        self.play(Create(tg4.bracket), FadeIn(tg4.tag), run_time=0.45)
        # a final arrow into c, tagged vec3
        xc = xs(5.5)
        yb = y_levels[3]
        link = Line([xs(9), yb, 0], [xc, yb, 0], color=DIM, stroke_width=5)
        up = arrow([xc, yb, 0], [xc, yl - 0.4, 0], color=DIM)
        ctag = a2_tag("vec3", xc - 1.0, (yb + yl) / 2.0)
        self.play(Create(link), GrowArrow(up), FadeIn(ctag), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · Your Own Functions  (B20, B21, B23, B25 Manim; B22/B24 are other lanes)

Cast: the `soften` function box with its signature; three-cell bundle tokens travelling in and out; the wall between fragment() and your function.
All drawings; the only real text is code and the engine's own message (Lab 45-err-return-type, quoted word for word).
"""


def a3_mono(s, size, xl, y):
    """Monospace line placed by its LEFT edge; .xl, .cw (measured char width) let a3_x find a column."""
    m = M(s, size)
    m.move_to([xl + m.width / 2.0, y, 0])
    m.xl = xl
    m.cw = {32: 0.2461, 36: 0.2950, 40: 0.3440}.get(size, size * 0.0077)   # measured Menlo advance (fixed, so Gate A's stub text agrees)
    return m


def a3_x(m, col):
    return m.xl + col * m.cw


def a3_tag(text, x0, x1, y, up=False, dy=0.55, shift=0.0, size=32):
    """A drawn bracket from x0 to x1 at height y with a stem to an outlined tag. up=False: bracket under the text (ticks point up); up=True: above it."""
    d = 1 if up else -1
    tk = -d * 0.14
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=5), Line([x0, y, 0], [x0, y + tk, 0], color=DIM, stroke_width=5),
                Line([x1, y, 0], [x1, y + tk, 0], color=DIM, stroke_width=5))
    t = T(text, size)
    xm = (x0 + x1) / 2.0
    cy = y + d * dy
    tagbox = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
    tg = VGroup(tagbox, t).move_to([xm + shift, cy, 0])
    stem = Line([xm, y, 0], [xm + shift, cy - d * tagbox.height / 2, 0], color=DIM, stroke_width=4)
    g = VGroup(br, stem, tg)
    g.br = br; g.stem = stem; g.tag = tg; g.d = d
    return g


def a3_show(self, g, rt=0.5):
    self.play(AnimationGroup(Create(g.br), FadeIn(g.stem), FadeIn(g.tag, shift=UP * g.d * 0.15), lag_ratio=0.35), run_time=rt)


def a3_tok(n, x, y, color=TEAL, cell=0.28, gap=0.07):
    """A bundle token: n separate cells (the series' bundle). No text inside, so a fill is fine."""
    cs = VGroup(*[Square(side_length=cell, fill_color=color, fill_opacity=1, stroke_width=0).move_to([(i - (n - 1) / 2.0) * (cell + gap), 0, 0]) for i in range(n)])
    return cs.move_to([x, y, 0])


# ═════════════════════════════ B20 · the signature ═════════════════════════════
class B20_Signature(Scene):
    def construct(self):
        title = T("Your Own Functions", 40).to_corner(UL, buff=0.95)
        xl = -3.9
        l1 = a3_mono("vec3 soften(vec3 c) {", 40, xl, 1.6)
        l2 = a3_mono("    return 0.4 + 0.6 * c;", 40, xl, -1.3)
        l3 = a3_mono("}", 40, xl, -2.0)
        cap = T("signature: the first line of a function", 32).move_to([0, -3.0, 0])
        self.play(FadeIn(title), FadeIn(l1), run_time=0.5)
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.4)
        self.play(FadeIn(cap), run_time=0.4)
        yb = 1.18
        t1 = a3_tag("hands back", a3_x(l1, 0), a3_x(l1, 4), yb, dy=0.62)
        t2 = a3_tag("name", a3_x(l1, 5), a3_x(l1, 11), yb, dy=0.62)
        t3 = a3_tag("arguments, each with a type", a3_x(l1, 11), a3_x(l1, 19), yb, dy=1.45)
        until(self, "It has three parts", lead=0.1)
        a3_show(self, t1, 0.5)
        until(self, "the type it hands back", lead=0.2)
        a3_show(self, t2, 0.5)
        until(self, "its arguments", lead=0.5)
        a3_show(self, t3, 0.6)
        done(self)


# ═════════════════════════════ B21 · call and return ═════════════════════════════
class B21_CallAndReturn(Scene):
    def construct(self):
        call = a3_mono("soften(vec3(UV, 0.5))", 32, -6.0, 2.3)
        body = M("return 0.4 + 0.6 * c;", 32).move_to([3.25, 2.3, 0])
        fbox = box(3.2, 2.3, 5.95, 1.1, color=INK, sw=4)
        slot = Square(side_length=0.62, stroke_color=INK, stroke_width=4).move_to([0.95, 1.4, 0])
        cc = M("c", 32).move_to(slot.get_center())
        func = VGroup(fbox, body)
        self.play(FadeIn(call), FadeIn(func), FadeIn(slot), FadeIn(cc), run_time=0.6)
        path1 = DashedLine([-3.4, 1.4, 0], [0.55, 1.4, 0], color=DIM, stroke_width=4)
        tok = a3_tok(3, -3.4, 1.4)
        until(self, "hands values into", lead=0.6)
        self.play(Create(path1), FadeIn(tok), run_time=0.4)
        self.play(tok.animate.move_to([0.95, 1.4, 0]), run_time=0.9)
        until(self, "The body runs", lead=0.1)
        self.play(FadeOut(tok), func.animate.scale(1.05), run_time=0.3)
        self.play(func.animate.scale(1 / 1.05), run_time=0.3)
        # the bundle comes back, tagged
        path2 = DashedLine([4.2, 1.7, 0], [4.2, 0.55, 0], color=DIM, stroke_width=4)
        path3 = DashedLine([4.2, 0.55, 0], [-3.4, 0.55, 0], color=DIM, stroke_width=4)
        tok2 = a3_tok(3, 4.2, 1.7)
        until(self, "return hands one value back", lead=1.4)
        self.play(FadeIn(tok2), Create(path2), run_time=0.25)
        self.play(tok2.animate.move_to([4.2, 0.55, 0]), Create(path3), run_time=0.3)
        self.play(tok2.animate.move_to([-3.4, 0.55, 0]), run_time=0.8)
        back = T("vec3, as promised", 32).move_to([-3.4, 0.0, 0])
        self.play(FadeIn(back, shift=UP * 0.1), run_time=0.4)
        # the wrong size bounces
        until(self, "Break that promise", lead=1.2)
        bar = Line([-1.7, -1.55, 0], [-1.7, -0.45, 0], color=DIM, stroke_width=16)
        cross = VGroup(Line([-2.1, -0.75, 0], [-1.3, -1.25, 0], color=INK, stroke_width=6), Line([-2.1, -1.25, 0], [-1.3, -0.75, 0], color=INK, stroke_width=6))
        tok4 = VGroup(a3_tok(4, 0, 0), T("vec4", 32).move_to([0, -0.45, 0])).move_to([5.35, 1.7, 0])
        self.play(FadeIn(bar), FadeIn(tok4), run_time=0.3)
        self.play(tok4.animate.move_to([5.35, -1.0, 0]), run_time=0.4)
        self.play(tok4.animate.move_to([-0.7, -1.0, 0]), run_time=0.6)
        self.play(Create(cross), tok4.animate.move_to([0.9, -1.0, 0]), run_time=0.4)
        m1 = a3_mono("Expected return with an expression", 32, -6.0, -2.15)
        m2 = a3_mono("of type 'vec3'.", 32, -6.0, -2.65)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.4)
        done(self)


# ═════════════════════════════ B23 · the wall ═════════════════════════════
class B23_TheWall(Scene):
    def construct(self):
        frag = box(3.6, 0.5, 4.6, 3.3, color=INK, sw=4)
        flab = M("fragment()", 32).move_to([3.6, 1.7, 0])
        chips = []
        for i, w in enumerate(["UV", "COLOR", "TEXTURE"]):
            tx = M(w, 32)
            cb = RoundedRectangle(width=tx.width + 0.4, height=0.6, corner_radius=0.12, stroke_color=INK, stroke_width=3)
            ch = VGroup(cb, tx).move_to([3.6, 0.85 - i * 0.8, 0])
            chips.append(ch)
        soft = box(-3.6, 0.5, 4.0, 3.3, color=INK, sw=4)
        slab = M("soften()", 32).move_to([-3.6, 1.7, 0])
        mine = T("your own", 32).move_to([-3.6, -0.3, 0])
        wall = Line([0, -1.3, 0], [0, 2.2, 0], color=DIM, stroke_width=26)
        self.play(FadeIn(frag), FadeIn(flab), FadeIn(soft), FadeIn(slab), FadeIn(mine), *[FadeIn(c) for c in chips], run_time=0.6)
        self.play(FadeIn(wall), run_time=0.4)
        cap1 = T("built-in: a value the engine hands to a function, or collects from it", 32).move_to([0, -2.5, 0])
        until(self, "A built-in is a value", lead=0.2)
        self.play(FadeIn(cap1), run_time=0.5)
        uv = chips[0]
        until(self, "Use U V inside yours", lead=0.3)
        self.play(uv.animate.move_to([0.95, 0.85, 0]), run_time=0.8, rate_func=linear)
        self.play(uv.animate.move_to([2.6, 0.85, 0]), run_time=0.5)
        self.play(uv.animate.move_to([3.6, 0.85, 0]), run_time=0.4)
        bub = RoundedRectangle(width=3.7, height=0.7, corner_radius=0.3, stroke_color=INK, stroke_width=4).move_to([-0.2, 2.78, 0])
        bt = T("unknown identifier", 32).move_to(bub.get_center())
        tail = Polygon([-0.05, 2.43, 0], [0.2, 2.43, 0], [0.0, 2.15, 0], stroke_color=INK, stroke_width=4, fill_opacity=0)
        until(self, "Godot says unknown identifier", lead=0.1)
        self.play(FadeIn(bub), FadeIn(bt), FadeIn(tail), run_time=0.4)
        done(self)


# ═════════════════════════════ B25 · in, inout, out ═════════════════════════════
def a3_chip(word, cap, xl):
    """A mode chip (outlined, monospace word) with a one-to-three-word caption to its right. Returns VGroup with .chip."""
    tx = M(word, 32)
    cb = RoundedRectangle(width=tx.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3)
    chip = VGroup(cb, tx).move_to([xl + cb.width / 2.0, 2.75, 0])
    c = T(cap, 32).move_to([xl + cb.width + 0.3, 2.75, 0])
    c.shift(RIGHT * c.width / 2.0)
    g = VGroup(chip, c)
    g.chip = chip
    return g


class B25_InOutInout(Scene):
    def construct(self):
        YA, YC = 0.55, -1.4
        c1 = a3_chip("in", "a copy", -6.0)
        c2 = a3_chip("inout", "the original", -2.6)
        c3 = a3_chip("out", "writes back", 2.7)
        scard = box(-1.0, YC, 7.0, 0.95, color=INK, sw=4)
        sig_in = a3_mono("float bump(float x)", 32, -3.4, YC)
        sig_io = a3_mono("void bump(inout float x)", 32, -4.0, YC)
        sig_o = a3_mono("void make(out vec3 c)", 32, -3.6, YC)
        a_box = box(-4.3, YA, 2.5, 0.8, color=INK, sw=4)
        a_t = M("a = 0.25", 32).move_to(a_box.get_center())
        b_box = box(4.3, YA, 2.5, 0.8, color=INK, sw=4)
        b_t = M("b = 0.75", 32).move_to(b_box.get_center())
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(c3), FadeIn(a_box), FadeIn(a_t), FadeIn(scard), FadeIn(sig_in), run_time=0.6)
        rg = ring(c1.chip)
        self.play(FadeIn(rg), run_time=0.3)
        # IN: a ghost copy goes in, changes, comes back to b; a stays
        until(self, "hands over a copy", lead=0.5)
        ghost = M("0.25", 32)
        gbox = RoundedRectangle(width=1.5, height=0.6, corner_radius=0.12, stroke_color=DIM, stroke_width=3)
        gh = VGroup(gbox, ghost).move_to([-2.2, YA, 0])
        self.play(FadeIn(gh), run_time=0.25)
        self.play(gh.animate.move_to([-1.0, YC + 0.95, 0]), run_time=0.5)
        g2 = M("0.75", 32).move_to(gh.get_center())
        self.play(Transform(ghost, g2), run_time=0.3)
        self.play(gh.animate.move_to([2.3, YA, 0]), run_time=0.55)
        self.play(FadeOut(gh), FadeIn(b_box), FadeIn(b_t), run_time=0.3)
        # INOUT: a double-headed arrow ties the function to the original itself; a changes
        until(self, "In out hands over the original", lead=0.3)
        rg2 = ring(c2.chip)
        io_arrow = dim_arrow([-4.3, YC + 0.5, 0], [-4.3, YA - 0.45, 0], color=INK, w=6, tip=0.2)
        a_t2 = M("a = 0.75", 32).move_to(a_box.get_center())
        self.play(FadeOut(b_box), FadeOut(b_t), Transform(rg, rg2), Transform(sig_in, sig_io), run_time=0.4)
        self.play(FadeIn(io_arrow), run_time=0.3)
        self.play(Transform(a_t, a_t2), run_time=0.4)
        # OUT: the function writes into an empty three-cell box
        until(self, "Out is for writing", lead=0.4)
        rg3 = ring(c3.chip)
        cbox = VGroup(*[Rectangle(width=0.95, height=0.8, stroke_color=INK, stroke_width=4).move_to([-4.0 + (i - 1) * 0.95, YA, 0]) for i in range(3)])
        cname = M("c", 32).move_to([-5.75, YA, 0])
        self.play(FadeOut(a_box), FadeOut(a_t), FadeOut(io_arrow), Transform(rg, rg3), Transform(sig_in, sig_o), run_time=0.4)
        self.play(FadeIn(cbox), FadeIn(cname), run_time=0.3)
        wr = arrow([-4.0, YC + 0.5, 0], [-4.0, YA - 0.45, 0], color=INK, w=6, tip=0.2)
        vals = VGroup(*[M(v, 32).move_to(cbox[i].get_center()) for i, v in enumerate(["0.1", "0.5", "0.9"])])
        self.play(FadeIn(wr), run_time=0.25)
        self.play(FadeIn(vals, lag_ratio=0.3), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · Choices and Loops  (B29, B32: the Manim beats of this act that this file carries)

Cast for the act: the split picture (a real Lab render, teal left and pale right, shown as itself), the pixel row of the float-equality scene
(a schematic, labelled as one), and the real 1920-wide renders. Code lines are lines of real files in lab-shaders/ (16-split-if, 17-split-ternary,
19-float-equals, 20-float-range), placed on a measured character grid so Pango can never drop a space.
"""

A4P = "pantry/"


def a4_cw(size=32):
    """Advance of one Menlo character at this size, measured once with Manim 0.20.1 (font scaling is not linear in size: 32 -> 0.25, 40 -> 0.35).
    Constants, not a runtime measurement: Gate A's stub Text has no real widths."""
    return {32: 0.25, 36: 0.30, 40: 0.35}.get(size, 0.25 * size / 32)


def a4_mono(s, xl, y, size=32, color=INK):
    """One code line, LEFT edge on the character grid (leading spaces are columns)."""
    ind = len(s) - len(s.lstrip(" "))
    t = Text(s.lstrip(" "), font=MONO, color=color, font_size=size)
    t.move_to([xl + ind * a4_cw(size) + t.width / 2, y, 0])
    return t


def a4_x(xl, col, size=32):
    return xl + col * a4_cw(size)


def a4_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a4_equals(x, y, w=0.7, gap=0.2):
    return VGroup(Line([x - w / 2, y + gap / 2, 0], [x + w / 2, y + gap / 2, 0], color=INK, stroke_width=7),
                  Line([x - w / 2, y - gap / 2, 0], [x + w / 2, y - gap / 2, 0], color=INK, stroke_width=7))


def a4_glyphs(lines):
    return VGroup(*[g for ln in lines for g in ln.submobjects])


# ═════════════════════════════ B29 · the ternary is a one-line if ═════════════════════════════
class B29_Collapse(Scene):
    def construct(self):
        xl = -4.25
        six = ["vec3 c;", "if (UV.x < 0.5) {", "  c = teal;", "} else {", "  c = pale;", "}"]
        one = "vec3 c = UV.x < 0.5 ? teal : pale;"
        lh = 0.5
        ytop = 3.0
        sixl = [a4_mono(s, xl, ytop - lh * i) for i, s in enumerate(six)]
        yone = ytop - lh * 1.0
        onel = a4_mono(one, xl, yone)
        gs, g1 = a4_glyphs(sixl), a4_glyphs([onel])
        cap = a4_t("ternary: a one-line if", 0, 0.3)
        # brackets under the three parts of the one line (cols: "vec3 c = " is 9, condition 9..18, ? at 20, teal 22..25, : at 27, pale 29..32)
        by = yone - 0.42
        t_cond = type_tag("condition", a4_x(xl, 9), a4_x(xl, 19) - 0.05, by)
        t_true = type_tag("if true", a4_x(xl, 22), a4_x(xl, 26) - 0.05, by)
        t_false = type_tag("if false", a4_x(xl, 29), a4_x(xl, 33) - 0.05, by)
        t_true.tag.shift(LEFT * 0.35)
        t_false.tag.shift(RIGHT * 0.45)
        q = a4_x(xl, 20) + a4_cw() * 0.45
        c_ = a4_x(xl, 27) + a4_cw() * 0.45
        # the ? and : are marked by a terracotta dot (grey-ringed) just above each glyph: a ring round one glyph of a line would cut its neighbours
        rq = Dot([q, yone + 0.4, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3)
        rc = Dot([c_, yone + 0.4, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3)
        pic = lab_window(A4P + "split-if.png", 2.6, -2.7, -1.6, "")
        pcap = a4_t("Godot 4.7.2 · Forward+ · same pixels", -0.0, -2.9)
        eq = a4_equals(0.55, -1.6)
        same = a4_t("same pixels", 2.7, -1.6)

        self.play(FadeIn(gs), FadeIn(pic), FadeIn(pcap), run_time=0.7)
        until(self, "Write the condition", lead=0.0)
        self.play(Transform(gs, g1), run_time=1.0)
        self.play(FadeIn(cap), run_time=0.3)
        until(self, "Write the condition", lead=0.0)
        self.play(FadeIn(t_cond), run_time=0.4)
        until(self, "a question mark", lead=0.1)
        self.play(FadeIn(rq), run_time=0.3)
        until(self, "the value if true", lead=0.1)
        self.play(FadeIn(t_true), run_time=0.3)
        until(self, "a colon", lead=0.1)
        self.play(FadeIn(rc), run_time=0.3)
        until(self, "then the value if false", lead=0.1)
        self.play(FadeIn(t_false), run_time=0.3)
        until(self, "Same picture", lead=0.1)
        self.play(FadeIn(eq), FadeIn(same), run_time=0.5)
        done(self)


# ═════════════════════════════ B32 · no pixel lands on one half ═════════════════════════════
class B32_NoPixelLands(Scene):
    def construct(self):
        grid = pixel_grid(cols=12, rows=1, cell=0.7, x=0.0, y=2.2, color=DIM, sw=3)
        cells = grid.cells[0]
        dots = VGroup(*[Dot(c.get_center(), radius=0.07, color=INK) for c in cells])
        half = Line([0, 2.8, 0], [0, 1.35, 0], color=INK, stroke_width=6)
        ax = Line([-4.2, 1.35, 0], [4.2, 1.35, 0], color=INK, stroke_width=5)
        l0 = a4_t("0", -4.2, 1.0)
        l1 = a4_t("1", 4.2, 1.0)
        lh = a4_t("0.5", 0.0, 1.0)
        slab = a4_t("schematic: 12 pixels", -4.0, 3.3 - 0.0, 32)
        slab.move_to([0.0, 3.0, 0])
        xl = -6.0
        c1 = a4_mono("if (UV.x == 0.5)", xl, 0.5)
        c2 = a4_mono("if (abs(UV.x - 0.5) < 0.005)", xl, 0.0)
        none = a4_t("no pixel center is exactly 0.5", 2.15, 0.5)
        absl = a4_t("abs: drops the minus sign: -0.3 becomes 0.3", -1.6, -0.5)
        probe = Dot([-4.2, 2.2, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        pa = lab_window(A4P + "float-equals-1920.png", 3.0, -3.2, -1.75, "")
        pb = lab_window(A4P + "float-range-1920.png", 3.0, 3.2, -1.75, "")
        ca = a4_t("Forward+ · 1920 wide", -3.2, -3.0)
        cb = a4_t("Forward+ · 1920 wide", 3.2, -3.0)

        self.play(Create(grid), FadeIn(slab), run_time=0.6)
        self.play(FadeIn(dots), Create(ax), Create(half), FadeIn(l0), FadeIn(l1), FadeIn(lh), run_time=0.6)
        until(self, "Light U V dot X", lead=0.1)
        self.play(FadeIn(c1), run_time=0.4)
        # the probe sweeps the row: nothing lights
        self.play(FadeIn(probe), run_time=0.2)
        self.play(probe.animate.move_to([4.2, 2.2, 0]), run_time=1.6, rate_func=linear)
        self.play(FadeIn(none), FadeOut(probe), run_time=0.4)
        until(self, "A small range", lead=0.1)
        self.play(FadeIn(c2), FadeIn(absl), FadeOut(none), run_time=0.4)
        probe2 = Dot([-4.2, 2.2, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(probe2), run_time=0.15)
        self.play(probe2.animate.move_to([-0.35, 2.2, 0]), run_time=0.8, rate_func=linear)
        self.play(tint(cells[5], TEAL, 0.9), probe2.animate.move_to([0.35, 2.2, 0]), run_time=0.4)
        self.play(tint(cells[6], TEAL, 0.9), run_time=0.3)
        self.play(FadeOut(probe2), run_time=0.2)
        until(self, "documentation warns", lead=0.9)
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(ca), FadeIn(cb), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Read One Aloud  (B35 to B39 Manim; B34, B40, B41 are other lanes)

Cast: the real `breathe` file (lab-shaders/01-breathe.gdshader) read line by line: each line zoomed (monospace, as in the file), small outlined
type tags landing under or over its pieces; the gray-to-teal ramp strip. Every line below is copied from that file, nothing is invented.
"""


def a5_line(s, size, xl, y):
    """A real code line placed by its LEFT edge; .xl and .cw (measured character width) let a5_x find a column."""
    m = M(s, size)
    m.move_to([xl + m.width / 2.0, y, 0])
    m.xl = xl
    m.cw = {32: 0.2461, 36: 0.2950, 40: 0.3440}.get(size, size * 0.0077)   # measured Menlo advance (fixed, so Gate A's stub text agrees)
    return m


def a5_x(m, col):
    return m.xl + col * m.cw


def a5_tag(text, x0, x1, y, up=False, dy=0.55, shift=0.0, size=32):
    """A drawn bracket from x0 to x1 at height y with a stem to an outlined tag (under the text by default, above it with up=True)."""
    d = 1 if up else -1
    tk = -d * 0.14
    br = VGroup(Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=5), Line([x0, y, 0], [x0, y + tk, 0], color=DIM, stroke_width=5),
                Line([x1, y, 0], [x1, y + tk, 0], color=DIM, stroke_width=5))
    t = T(text, size)
    xm = (x0 + x1) / 2.0
    tagbox = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=DIM, stroke_width=3).set_fill(PALEBOX, opacity=1)
    tg = VGroup(tagbox, t).move_to([xm + shift, y + d * dy, 0])
    stem = Line([xm, y, 0], [xm + shift, y + d * dy - d * tagbox.height / 2, 0], color=DIM, stroke_width=4)
    g = VGroup(br, stem, tg)
    g.br = br; g.stem = stem; g.tag = tg; g.d = d
    return g


def a5_show(self, g, rt=0.45):
    """The tag flies out to its piece: stem and tag slide in from the line, the bracket closes."""
    self.play(AnimationGroup(Create(g.br), FadeIn(g.stem), FadeIn(g.tag, shift=UP * g.d * 0.2), lag_ratio=0.3), run_time=rt)


def a5_tok(n, x, y, color=TEAL, cell=0.28, gap=0.07):
    cs = VGroup(*[Square(side_length=cell, fill_color=color, fill_opacity=1, stroke_width=0).move_to([(i - (n - 1) / 2.0) * (cell + gap), 0, 0]) for i in range(n)])
    return cs.move_to([x, y, 0])


# ═════════════════════════════ B35 · the two uniform lines ═════════════════════════════
class B35_ReadUniforms(Scene):
    def construct(self):
        xl = -4.87
        l3 = a5_line("uniform vec4 tint : source_color;", 36, xl, 1.4)
        l4 = a5_line("uniform float speed = 2.0;", 36, xl, -1.35)
        cap = T("hint: the word after a colon that tells Godot how to treat a uniform", 32).move_to([0, -3.0, 0])
        self.play(FadeIn(l3), FadeIn(l4), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.4)
        yu, yd = 1.88, 0.93
        t_uni = a5_tag("set from outside", a5_x(l3, 0), a5_x(l3, 7), yu, up=True, dy=0.55)
        t_vec = a5_tag("a color", a5_x(l3, 8), a5_x(l3, 12), yd, dy=0.5)
        t_hint = a5_tag("hint", a5_x(l3, 18), a5_x(l3, 33), yd, dy=0.5)
        sw = Circle(radius=0.22, fill_color=TEAL, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([0.9, -0.22, 0])
        swl = T("treated as a color", 32).move_to([sw.get_center()[0] + 0.45 + 1.5, -0.22, 0])
        t_nod = a5_tag("no default: black", a5_x(l3, 32), a5_x(l3, 33), yu, up=True, dy=0.55, shift=-0.3)
        yd4 = -1.8
        t_flt = a5_tag("a decimal number", a5_x(l4, 8), a5_x(l4, 13), yd4, dy=0.5)
        t_def = a5_tag("default", a5_x(l4, 20), a5_x(l4, 26), yd4, dy=0.5)
        until(self, "Line three is a uniform", lead=0.1)
        a5_show(self, t_uni)
        until(self, "a vec four", lead=0.2)
        a5_show(self, t_vec)
        until(self, "Source color is a hint", lead=0.3)
        a5_show(self, t_hint)
        self.play(FadeIn(sw, scale=0.6), FadeIn(swl), run_time=0.4)
        until(self, "With no default", lead=0.7)
        a5_show(self, t_nod)
        until(self, "Line four is a float", lead=0.4)
        a5_show(self, t_flt)
        until(self, "default of two", lead=0.6)
        a5_show(self, t_def)
        done(self)


# ═════════════════════════════ B36 · the signature of breathe ═════════════════════════════
class B36_ReadSignature(Scene):
    def construct(self):
        xl = -5.0
        l6 = a5_line("vec3 breathe(vec3 base, float t) {", 36, xl, 1.2)
        self.play(FadeIn(l6), run_time=0.5)
        yu, yd = 1.7, 0.7
        t_name = a5_tag("name", a5_x(l6, 5), a5_x(l6, 12), yu, up=True, dy=1.2)
        t_ret = a5_tag("hands back a vec3", a5_x(l6, 0), a5_x(l6, 4), yu, up=True, dy=0.55, shift=-0.1)
        t_a1 = a5_tag("argument: vec3", a5_x(l6, 13), a5_x(l6, 22), yd, dy=0.5)
        t_a2 = a5_tag("argument: float", a5_x(l6, 24), a5_x(l6, 31), yd, dy=1.15)
        # the flow: a three-cell and a one-cell token into the function, a three-cell token out
        fb = box(0.2, -1.55, 2.3, 0.85, color=INK, sw=4)
        fl = M("breathe", 32).move_to(fb.get_center())
        ar_in = arrow([-1.6, -1.55, 0], [-1.0, -1.55, 0], color=DIM, w=5, tip=0.2)
        ar_out = arrow([1.4, -1.55, 0], [2.0, -1.55, 0], color=DIM, w=5, tip=0.2)
        k3 = a5_tok(3, -4.6, -1.55)
        k1 = a5_tok(1, -3.1, -1.55)
        note = T("the body must return a vec3", 32).move_to([0.2, -2.75, 0])
        until(self, "declares breathe", lead=0.2)
        a5_show(self, t_name)
        until(self, "hands back a vec three", lead=0.2)
        a5_show(self, t_ret)
        until(self, "a vec three called base", lead=0.3)
        a5_show(self, t_a1)
        until(self, "a float called t", lead=0.3)
        a5_show(self, t_a2)
        until(self, "So the body gets", lead=0.4)
        self.play(FadeIn(fb), FadeIn(fl), FadeIn(ar_in), FadeIn(ar_out), FadeIn(k3), FadeIn(k1), run_time=0.4)
        self.play(k3.animate.move_to([-1.2, -1.55, 0]), k1.animate.move_to([-0.9, -1.55, 0]), run_time=0.6)
        self.play(FadeOut(k3), FadeOut(k1), fb.animate.scale(1.05), run_time=0.2)
        out = a5_tok(3, 1.5, -1.55)
        self.play(FadeIn(out), fb.animate.scale(1 / 1.05), run_time=0.2)
        self.play(out.animate.move_to([3.6, -1.55, 0]), FadeIn(note), run_time=0.6)
        done(self)


# ═════════════════════════════ B37 · the wave line ═════════════════════════════
class B37_ReadWave(Scene):
    def construct(self):
        xl = -6.0
        l7 = a5_line("float wave = 0.5 + 0.5 * sin(t);", 36, xl, 2.55)
        self.play(FadeIn(l7), run_time=0.5)
        rows = [(29, 29, "t"), (25, 30, "sin(t)"), (19, 30, "0.5 * sin(t)"), (13, 30, "0.5 + 0.5 * sin(t)")]
        yb0, step = 1.85, 0.62
        brs = []
        for k, (c0, c1, nm) in enumerate(rows):
            x0, x1 = a5_x(l7, c0), a5_x(l7, c1 + 1)
            y = yb0 - k * step
            g = a5_tag("float", x0, x1, y, dy=0.0)
            # side tag at the right end of the bracket instead of a stem tag
            t = T("float", 32)
            tb = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
            tg = VGroup(tb, t).move_to([x1 + 0.2 + tb.width / 2.0, y, 0])
            br = g.br
            brs.append(VGroup(br, tg))
        # into wave
        wx0, wx1 = a5_x(l7, 6), a5_x(l7, 10)
        wb = a5_tag("float", wx0, wx1, yb0, dy=0.0)
        wt = T("float", 32)
        wtb = RoundedRectangle(width=wt.width + 0.4, height=wt.height + 0.3, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1)
        wtg = VGroup(wtb, wt).move_to([wx0 - 0.2 - wtb.width / 2.0, yb0, 0])
        wave_t = VGroup(wb.br, wtg)
        into = arrow([a5_x(l7, 13) - 0.15, yb0 - 3 * step, 0], [(wx0 + wx1) / 2, yb0 - 0.12, 0], color=DIM, w=5, tip=0.2)
        # the sine curve: -1..1 squeezed into 0..1
        pl = plot(lambda v: np.sin(v), x_range=(0, 2 * np.pi), y_range=(-1, 1), size=(3.6, 1.7), x=-3.6, y=-1.55, color=DIM)
        pl_labels = VGroup(T("1", 32).move_to([-5.75, -0.7, 0]), T("-1", 32).move_to([-5.8, -2.4, 0]))
        sq = VMobject(stroke_color=INK, stroke_width=7).set_points_smoothly([pl.pt(v) for v in np.linspace(0, 2 * np.pi, 80)])
        sq.set_points_smoothly([pl.pt(v) for v in np.linspace(0, 2 * np.pi, 80)])
        sq2 = VMobject(stroke_color=INK, stroke_width=7)
        sq2_pts = []
        ax_x0, ax_y0 = -3.6 - 1.8, -1.55 - 0.85
        for v in np.linspace(0, 2 * np.pi, 80):
            yv = 0.5 + 0.5 * np.sin(v)
            sq2_pts.append(np.array([ax_x0 + v / (2 * np.pi) * 3.6, ax_y0 + (yv + 1) / 2 * 1.7, 0]))
        sq2.set_points_smoothly(sq2_pts)
        zero = T("0", 32).move_to([-5.7, -1.55, 0])
        until(self, "Sine of t is a float", lead=0.3)
        self.play(FadeIn(brs[0]), FadeIn(brs[1]), run_time=0.5)
        self.play(FadeIn(pl), FadeIn(pl_labels), run_time=0.4)
        until(self, "Half of that", lead=0.4)
        self.play(FadeIn(brs[2]), run_time=0.35)
        self.play(FadeIn(brs[3]), run_time=0.35)
        self.play(Transform(pl.curve, sq2), FadeIn(zero), run_time=0.7)
        dot = Dot(sq2_pts[0], radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        until(self, "now swinging", lead=0.3)
        self.add(dot)
        self.play(MoveAlongPath(dot, pl.curve), run_time=1.5, rate_func=linear)
        until(self, "stored in wave", lead=0.5)
        self.play(FadeIn(wave_t), FadeIn(into), run_time=0.4)
        done(self)


# ═════════════════════════════ B38 · the return line ═════════════════════════════
class B38_ReadReturn(Scene):
    def construct(self):
        xl = -5.0
        l8 = a5_line("return mix(vec3(0.9), base, wave);", 36, xl, 2.0)
        self.play(FadeIn(l8), run_time=0.5)
        yu, yd = 2.5, 1.5
        t_ret = a5_tag("matches the signature", a5_x(l8, 0), a5_x(l8, 6), yu, up=True, dy=0.5, shift=0.3)
        t_mix = a5_tag("vec3", a5_x(l8, 7), a5_x(l8, 33), yu, up=True, dy=0.5)
        t_v09 = a5_tag("fills all three: a pale gray", a5_x(l8, 11), a5_x(l8, 20), yd, dy=1.1, shift=-0.7)
        sw = Rectangle(width=0.5, height=0.5, fill_color="#E4E2DA", fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([(a5_x(l8, 11) + a5_x(l8, 21)) / 2 - 0.7 - 2.2 - 0.45, yd - 1.1, 0])
        t_base = a5_tag("vec3", a5_x(l8, 22), a5_x(l8, 26), yd, dy=0.5)
        t_wave = a5_tag("float: 0 to 1", a5_x(l8, 28), a5_x(l8, 32), yd, dy=0.5, shift=0.55)
        gl = T("mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b", 32).move_to([0, -0.55, 0])
        strip = ramp_strip(width=7.0, label0="0", label1="1", y=-1.55, x=0.0)
        note = T("0 gives the gray, 1 gives base", 32).move_to([0, -2.7, 0])
        dot = ramp_marker(strip, 0.0)
        until(self, "Vec three of zero", lead=0.2)
        a5_show(self, t_v09)
        self.play(FadeIn(sw), run_time=0.3)
        until(self, "Mix blends", lead=0.2)
        self.play(FadeIn(gl), run_time=0.4)
        self.play(FadeIn(strip), FadeIn(note), FadeIn(dot), run_time=0.4)
        until(self, "toward base", lead=0.1)
        a5_show(self, t_base, 0.35)
        a5_show(self, t_wave, 0.35)
        self.play(dot.animate.move_to([strip.x1, strip.y, 0]), run_time=1.5, rate_func=linear)
        until(self, "The result is a vec three", lead=0.3)
        a5_show(self, t_mix, 0.4)
        a5_show(self, t_ret, 0.4)
        done(self)


# ═════════════════════════════ B39 · the two fragment lines ═════════════════════════════
class B39_ReadFragment(Scene):
    def construct(self):
        xl = -5.65
        l12 = a5_line("vec3 color = breathe(tint.rgb, TIME * speed);", 32, xl, 1.75)
        l13 = a5_line("COLOR = vec4(color, tint.a);", 32, xl, -0.7)
        cap1 = T("TIME: seconds on one clock shared by the whole game", 32).move_to([0, -2.55, 0])
        cap2 = T("COLOR: the color of the pixel being drawn; fragment() sets it", 32).move_to([0, -3.05, 0])
        self.play(FadeIn(l12), FadeIn(l13), run_time=0.5)
        yu12, yd12 = 2.12, 1.38
        t_rgb = a5_tag("vec3 (swizzle)", a5_x(l12, 21), a5_x(l12, 29), yd12, dy=0.5, shift=-0.2)
        t_time = a5_tag("float", a5_x(l12, 31), a5_x(l12, 43), yd12, dy=0.5)
        t_br = a5_tag("vec3", a5_x(l12, 13), a5_x(l12, 44), yu12, up=True, dy=0.5)
        t_col = a5_tag("vec3", a5_x(l12, 5), a5_x(l12, 10), yd12, dy=0.5)
        yu13, yd13 = -0.33, -1.07
        t_v4 = a5_tag("vec4(...)", a5_x(l13, 8), a5_x(l13, 27), yd13, dy=0.5)
        t_c4 = a5_tag("vec4", a5_x(l13, 0), a5_x(l13, 5), yu13, up=True, dy=0.5)
        rg = Dot([xl - 0.3, -0.7, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        until(self, "tint dot R G B", lead=0.1)
        a5_show(self, t_rgb)
        until(self, "time times speed", lead=0.2)
        a5_show(self, t_time)
        self.play(FadeIn(cap1), run_time=0.35)
        until(self, "Breathe turns", lead=0.2)
        a5_show(self, t_br)
        a5_show(self, t_col, 0.35)
        until(self, "Vec four adds", lead=0.2)
        a5_show(self, t_v4)
        until(self, "color, a vec four, takes it", lead=0.4)
        self.play(FadeIn(rg), run_time=0.3)
        a5_show(self, t_c4, 0.4)
        self.play(FadeIn(cap2), run_time=0.35)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
