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
"""Act I (B02, B08, B09, B11; the rest of the act is captures and Remotion). Manim only, kit objects, real Godot 4.7.2 renders through lab_window.
Cast: the stage palette, the sand/rock/buoy/water set, one terracotta dot or ring per picture (never text). Numbers are the measured ones from the lane visual_intent
(B08: 25,115,178 / 184,157,110 / 108,129,162, predicted 108,129,161, screen 108,129,162; B09: red 108 and 71, ticks 73 and 108). B11 is a drawing and says so."""

a1_BLUE = "#6E9BC7"; a1_WATER = "#1973B2"; a1_SAND = "#B89D6E"; a1_RESULT = "#6C81A2"; a1_ROCK = "#8E877B"; a1_SANDDK = "#8F7A52"


def a1_left(mob, x, y):
    """Put a mob's LEFT edge at x, centred on y."""
    mob.move_to([x + mob.width / 2.0, y, 0])
    return mob


def a1_right(mob, x, y):
    """Put a mob's RIGHT edge at x, centred on y."""
    mob.move_to([x - mob.width / 2.0, y, 0])
    return mob


def a1_tdot(p, r=0.17):
    return Dot(np.array([p[0], p[1], 0.0], dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a1_pring(p, r=0.3):
    """A terracotta ring on a point, over a wider grey backing (never accent text). No fill: the pixel inside stays visible."""
    c = np.array([p[0], p[1], 0.0])
    back = Circle(radius=r + 0.04, stroke_color=DIM, stroke_width=13, stroke_opacity=0.6).move_to(c)
    rr = Circle(radius=r, stroke_color=TERRA, stroke_width=7).move_to(c)
    return VGroup(back, rr)


def a1_pulse(r, k=1.15):
    """Pulse a ring (grey backing + terracotta) without Indicate's default yellow: each part keeps its own colour."""
    return [Indicate(r[0], scale_factor=k, color=DIM), Indicate(r[1], scale_factor=k, color=TERRA)]


def a1_tile(cx, cy, w=2.2, h=1.1, th=0.15):
    """A flat isometric plane tile: a diamond top, a thin slab edge, two grid lines."""
    L, R, Tp, B = [cx - w / 2, cy, 0], [cx + w / 2, cy, 0], [cx, cy + h / 2, 0], [cx, cy - h / 2, 0]
    side_l = Polygon(L, B, [cx, cy - h / 2 - th, 0], [cx - w / 2, cy - th, 0], stroke_color=INK, stroke_width=3, fill_color=GHOST, fill_opacity=1)
    side_r = Polygon(B, R, [cx + w / 2, cy - th, 0], [cx, cy - h / 2 - th, 0], stroke_color=INK, stroke_width=3, fill_color=LAB_STAGE, fill_opacity=1)
    top = Polygon(L, Tp, R, B, stroke_color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1)
    g1 = Line([cx - w / 4, cy + h / 4, 0], [cx + w / 4, cy - h / 4, 0], color=DIM, stroke_width=3)
    g2 = Line([cx + w / 4, cy + h / 4, 0], [cx - w / 4, cy - h / 4, 0], color=DIM, stroke_width=3)
    return VGroup(side_l, side_r, top, g1, g2)


def a1_ball(cx, cy, r=0.5):
    """A round material preview tile: a pale water-blue ball with a cream glint."""
    b = Circle(radius=r, stroke_color=INK, stroke_width=4, fill_color=a1_BLUE, fill_opacity=0.65).move_to([cx, cy, 0])
    gl = Circle(radius=r * 0.2, stroke_width=0, fill_color=CARD, fill_opacity=0.95).move_to([cx - r * 0.35, cy + r * 0.35, 0])
    return VGroup(b, gl)


def a1_card(cx, cy, w=1.3, h=1.5):
    """A small code-card icon: a cream card with four short grey lines (no text on it)."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_color=PALEBOX, fill_opacity=1).move_to([cx, cy, 0])
    lines = VGroup(*[Line([cx - w / 2 + 0.22, cy + h / 2 - 0.3 - 0.3 * i, 0], [cx - w / 2 + 0.22 + ln, cy + h / 2 - 0.3 - 0.3 * i, 0], color=DIM, stroke_width=6)
                     for i, ln in enumerate((0.8, 0.55, 0.85, 0.45))])
    return VGroup(fr, lines)


# ═════════════════════════ B02 · three links ═════════════════════════
class B02_ThreeLinks(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        bx = box(-1.65, -0.4, 8.0, 4.0, color=INK, sw=5)                        # the MeshInstance3D node: x -5.65..2.35, y -2.4..1.6
        slot = box(0.0, -0.3, 3.5, 2.4, color=DIM, sw=4)                          # the Material Override slot
        title = T("MeshInstance3D", 36).move_to([-1.65, 2.3, 0])
        slot_lab = T("Material  Override", 36).move_to([0.0, -1.95, 0])
        card = a1_card(5.35, 0.3); card_lab = T("shader", 36).move_to([5.35, -0.8, 0])
        plane = a1_tile(-3.3, 0.35); plane_lab = T("PlaneMesh", 36).move_to([-3.3, -0.75, 0])
        ball = a1_ball(0.0, 0.3); ball_lab = T("ShaderMaterial", 36).move_to([0.0, -0.75, 0])
        # a shader alone: the card sits by itself on the empty stage
        self.play(FadeIn(card), FadeIn(card_lab), run_time=0.5)
        # link 1: the mesh (the plane) and the node that holds it
        until(self, "A mesh gives it a shape", lead=0.4)
        self.play(FadeIn(plane, shift=DOWN * 0.3), FadeIn(plane_lab), run_time=0.5)
        self.play(Create(bx), Create(slot), FadeIn(title), FadeIn(slot_lab), run_time=0.8)
        a_1 = arrow([-3.3, 0.95, 0], [-3.3, 2.0, 0], w=6)
        until(self, "here a flat plane", lead=0.3)
        self.play(GrowArrow(a_1), run_time=0.4)
        # link 2: the shader goes into the material
        until(self, "A material holds the shader", lead=0.8)
        self.play(FadeIn(ball, scale=0.6), FadeIn(ball_lab), run_time=0.4)
        a_2 = arrow([4.55, 0.3, 0], [0.62, 0.3, 0], w=6)
        self.play(GrowArrow(a_2), run_time=0.5)
        # link 3: the node holds the material (after the midpoint: the picture before it is a settled still)
        until(self, "the mesh node holds", lead=0.4)
        a_3 = arrow([0.0, 0.88, 0], [0.0, 2.0, 0], w=6)
        self.play(GrowArrow(a_3), run_time=0.5)
        self.play(Indicate(bx, color=TEAL, scale_factor=1.0), run_time=0.7)
        until(self, "Those three links", lead=0.2)
        self.play(*[Indicate(a, color=TEAL, scale_factor=1.0) for a in (a_1, a_2, a_3)], run_time=0.9)
        done(self)


# ═════════════════════════ B08 · the blend, as arithmetic ═════════════════════════
def a1_swatch(x, y, hexcol, s=0.8):
    return Square(side_length=s, stroke_color=INK, stroke_width=3, fill_color=hexcol, fill_opacity=1).move_to([x, y, 0])


def a1_numrow(label, nums, y, x_label=-5.95, x_nums=(-3.6, -2.25, -0.9), size=40):
    """A row 'label  n1, n2, n3' with the three numbers left-aligned in FIXED columns, so two rows sit exactly one under the other."""
    lab = a1_left(T(label, 36), x_label, y)
    ns = [a1_left(T(n, size), x_nums[i], y) for i, n in enumerate(nums)]
    g = VGroup(lab, *ns)
    g.lab = lab; g.ns = ns
    return g


class B08_BlendArithmetic(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        sx = -5.55
        sw_w = a1_swatch(sx, 2.75, a1_WATER); lw_ = a1_left(T("water  (25, 115, 178)", 34), -4.85, 2.75)
        sw_s = a1_swatch(sx, 1.75, a1_SAND); ls_ = a1_left(T("sand  (184, 157, 110)", 34), -4.85, 1.75)
        by = 0.1
        wbar = Rectangle(width=3.5, height=0.4, stroke_width=0, fill_color=a1_WATER, fill_opacity=1).move_to([-4.2, by, 0])
        sbar = Rectangle(width=1.5, height=0.4, stroke_width=0, fill_color=a1_SAND, fill_opacity=1).move_to([-0.8, by, 0])
        plus = VGroup(Line([-2.15, by, 0], [-1.85, by, 0], color=DIM, stroke_width=6), Line([-2.0, by - 0.15, 0], [-2.0, by + 0.15, 0], color=DIM, stroke_width=6))
        p70 = T("70%", 36).move_to([-4.2, by + 0.6, 0]); p30 = T("30%", 36).move_to([-0.8, by + 0.6, 0])
        # the real Forward+ render, shown as itself, probe ringed just outside
        Wd, wx, wy = 5.2, 3.5, 0.5
        win = lab_window("pantry/blend-fp.png", width=Wd, x=wx, y=wy, caption="Forward+")
        probe = [wx - 0.2 * Wd, wy]                      # plate over floor: x 0.30 of the image, y 0.5
        pr = a1_pring(probe, 0.3)
        # rows
        pred = a1_numrow("predicted", ["108,", "129,", "161"], -1.85)
        scr = a1_numrow("screen", ["108,", "129,", "162"], -2.7)
        res_sw = a1_swatch(sx, -0.85, a1_RESULT); res_lab = a1_left(T("result", 36), -4.85, -0.85)

        # the sum: seventy percent water plus thirty percent of what is behind
        until(self, "seventy percent water", lead=0.5)
        self.play(FadeIn(sw_w), FadeIn(lw_), GrowFromEdge(wbar, LEFT), FadeIn(p70), run_time=0.6)
        until(self, "plus thirty percent", lead=0.5)
        self.play(FadeIn(sw_s), FadeIn(ls_), FadeIn(plus), GrowFromEdge(sbar, LEFT), FadeIn(p30), run_time=0.6)
        # one pixel, checked in the real render
        until(self, "We checked one pixel", lead=0.5)
        self.play(FadeIn(win), run_time=0.5)
        until(self, "water over sand", lead=0.7)
        self.play(FadeIn(pr, scale=1.6), run_time=0.5)
        # --- after the midpoint: the bars slide together into the result swatch; the predicted row lands ---
        until(self, "The blend predicts", lead=-1.3)                      # lands after the 45 to 55 percent window
        self.play(sbar.animate.shift(LEFT * 0.9), p30.animate.shift(LEFT * 0.9), FadeOut(plus), FadeIn(pred.lab), FadeIn(pred.ns[0]), run_time=0.5)
        wt = Rectangle(width=0.56, height=0.8, stroke_width=0, fill_color=a1_WATER, fill_opacity=1).move_to([-5.67, -0.85, 0])
        st = Rectangle(width=0.24, height=0.8, stroke_width=0, fill_color=a1_SAND, fill_opacity=1).move_to([-5.27, -0.85, 0])
        self.play(Transform(wbar, wt), Transform(sbar, st), FadeOut(p70), FadeOut(p30), FadeIn(pred.ns[1]), run_time=0.7)
        self.play(FadeIn(res_sw), FadeIn(res_lab), FadeOut(wbar), FadeOut(sbar), run_time=0.4)
        until(self, "one sixty-one", lead=0.1)
        self.play(FadeIn(pred.ns[2]), run_time=0.3)
        # the screen reads
        until(self, "The screen reads", lead=0.1)
        self.play(FadeIn(scr.lab), run_time=0.3)
        until(self, "reads one hundred eight", lead=-0.45)
        self.play(FadeIn(scr.ns[0]), run_time=0.3)
        until(self, "twenty-nine, one sixty-two", lead=-0.2)
        self.play(FadeIn(scr.ns[1]), run_time=0.3)
        until(self, "one sixty-two", lead=0.4)
        self.play(FadeIn(scr.ns[2]), run_time=0.3)
        self.play(Indicate(pred.ns[2], color=TEAL, scale_factor=1.0), Indicate(scr.ns[2], color=TEAL, scale_factor=1.0), *a1_pulse(pr), run_time=0.4)
        done(self)


# ═════════════════════════ B09 · two renderers, one number line ═════════════════════════
def a1_xline(v, x0=-5.6, x1=5.6):
    return x0 + (x1 - x0) * v / 255.0


class B09_TwoRenderers(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        Wd, lx, rx, iy = 5.0, -3.1, 3.1, 1.85
        lw = lab_window("pantry/blend-fp.png", width=Wd, x=lx, y=iy, caption="Forward+")
        rw = lab_window("pantry/blend-compat.png", width=Wd, x=rx, y=iy, caption="Compatibility")
        pl = a1_pring([lx - 0.2 * Wd, iy], 0.26); pr_ = a1_pring([rx - 0.2 * Wd, iy], 0.26)
        # the red channel reads, under each render
        def reading(x, n):
            red = T("red", 32, DIM); num = T(n, 56, bold=True)
            return VGroup(red, num).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([x, -0.75, 0])
        rd_l = reading(lx, "108"); rd_r = reading(rx, "71")
        # the number line 0 to 255 with two ticks
        ly = -1.95
        line = Line([-5.6, ly, 0], [5.6, ly, 0], color=INK, stroke_width=5)
        e0 = T("0", 32, DIM).move_to([-5.6, -1.45, 0]); e1 = T("255", 32, DIM).move_to([5.6, -1.45, 0])
        x73, x108, x71 = a1_xline(73), a1_xline(108), a1_xline(71)
        tk73 = Line([x73, ly - 0.22, 0], [x73, ly + 0.22, 0], color=INK, stroke_width=7)
        tk108 = Line([x108, ly - 0.22, 0], [x108, ly + 0.22, 0], color=INK, stroke_width=7)
        n73 = a1_right(T("typed-number mix", 36), x73 + 0.45, -2.6); v73 = T("73", 36).move_to([x73, -3.1, 0])
        n108 = a1_left(T("linear-light blend", 36), x108 - 0.45, -2.6); v108 = T("108", 36).move_to([x108, -3.1, 0])
        d108 = a1_tdot([lx, -1.4]); d71 = a1_tdot([rx, -1.4])

        # both real renders, the probe point ringed in each
        self.play(FadeIn(lw), FadeIn(rw), run_time=0.7)
        self.play(FadeIn(pl, scale=1.6), FadeIn(pr_, scale=1.6), run_time=0.5)
        # Forward+ blends in linear light: the line and its linear-light tick
        until(self, "Forward Plus blends in linear light", lead=0.5)
        self.play(Create(line), FadeIn(e0), FadeIn(e1), run_time=0.5)
        self.play(FadeIn(tk108), FadeIn(n108), FadeIn(v108), run_time=0.4)
        until(self, "mixing the typed numbers", lead=0.4)
        self.play(FadeIn(tk73), FadeIn(n73), FadeIn(v73), run_time=0.4)
        until(self, "would predict", lead=0.1)
        self.play(FadeIn(rd_l), FadeIn(rd_r), run_time=0.4)
        # --- after the 45 to 55 percent window: the two readings drop onto the line and snap to their ticks ---
        until(self, "not one hundred eight", lead=-0.2)
        self.play(FadeIn(d108), run_time=0.15)
        self.play(d108.animate.move_to([x108, -1.4, 0]), run_time=0.6, rate_func=smooth)
        self.play(d108.animate.move_to([x108, ly, 0]), run_time=0.25, rate_func=ease_in)
        self.play(Indicate(tk108, scale_factor=1.6, color=TEAL), run_time=0.4)
        until(self, "the typed numbers directly", lead=0.3)
        self.play(*a1_pulse(pr_), run_time=0.5)
        until(self, "so the same water reads", lead=1.0)
        self.play(FadeIn(d71), run_time=0.15)
        self.play(d71.animate.move_to([x71, -1.4, 0]), run_time=0.8, rate_func=smooth)
        self.play(d71.animate.move_to([x71, ly, 0]), run_time=0.25, rate_func=ease_in)
        self.play(Indicate(tk73, scale_factor=1.6, color=TEAL), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""Act II (B14, B16; the rest of the act is captures and Remotion). Manim only, kit objects. Both beats are DRAWINGS (B14 says so in a corner tag).
Cast: the series pixel grid (six by four outline squares), one terracotta dot (grey-ringed) in each square, one cream pixel with a dark ring.
The 24 points are the SAME in both beats (one seeded layout below), and the dashed line in B14 is the true cell edge: it runs only as far as those two points
are still the two closest of all 24, so nothing on screen claims more than the drawing shows. Numbers: none are invented (no figures on screen)."""

a2_COLS, a2_ROWS = 6, 4
a2_OWN = (2, 2)                       # (col, row) of the square the pixel sits in; its right-hand neighbour is (3, 2)
a2_SEED = 66


def a2_points(seed):
    """24 points in CELL UNITS (cell centre (c - 2.5, 1.5 - r), a jitter of up to 0.36 so every point stays well inside its square)."""
    rng = np.random.RandomState(seed)
    J = rng.uniform(-0.36, 0.36, size=(a2_ROWS, a2_COLS, 2))
    pts = np.zeros((a2_ROWS, a2_COLS, 2))
    for r in range(a2_ROWS):
        for c in range(a2_COLS):
            pts[r, c] = (c - 2.5 + J[r, c, 0], 1.5 - r + J[r, c, 1])
    return pts


def a2_edge(pts, P, Q):
    """The part of the perpendicular bisector of P and Q where P and Q are still the closest points of all 24 (the true cell edge)."""
    allp = pts.reshape(-1, 2)
    M = (P + Q) / 2.0
    d = Q - P
    n = np.array([-d[1], d[0]]) / np.linalg.norm(d)

    def ok(t):
        x = M + t * n
        return np.linalg.norm(x - P) <= np.linalg.norm(allp - x, axis=1).min() + 1e-9
    lo = 0.0
    while lo > -4 and ok(lo - 0.005):
        lo -= 0.005
    hi = 0.0
    while hi < 4 and ok(hi + 0.005):
        hi += 0.005
    return M + lo * n, M + hi * n


def a2_layout():
    pts = a2_points(a2_SEED)
    c, r = a2_OWN
    P, Q = pts[r, c], pts[r, c + 1]
    e0, e1 = a2_edge(pts, P, Q)
    block = [pts[rr, cc] for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)]
    best = None
    for py in np.arange((1.5 - r) - 0.42, (1.5 - r) + 0.42, 0.02):          # the pixel: just inside the right border of its own square
        p = np.array([-0.09, py])
        d = np.array([np.linalg.norm(p - b) for b in block])
        o = np.argsort(d)
        if np.allclose(block[o[0]], Q) and np.allclose(block[o[1]], P):    # nearest is the neighbour's point, second is its own
            s = min(d[o[1]] - d[o[0]], d[o[2]] - d[o[1]])
            if best is None or s > best[0]:
                best = (s, p)
    return pts, P, Q, (e0, e1), best[1], block


a2_PTS, a2_P, a2_Q, a2_EDGE, a2_PIX, a2_BLOCK = a2_layout()


def a2_sc(p, cell, gx, gy):
    """Cell units -> scene point."""
    return np.array([gx + p[0] * cell, gy + p[1] * cell, 0.0])


def a2_dot(p, r=0.11):
    return Dot(np.array([p[0], p[1], 0.0], dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a2_left(mob, x, y):
    mob.move_to([x + mob.width / 2.0, y, 0])
    return mob


# ═════════════════════════ B14 · one point each ═════════════════════════
class B14_OnePointEach(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        cell, gx, gy = 1.2, 0.0, 0.05
        grid = pixel_grid(cols=a2_COLS, rows=a2_ROWS, cell=cell, x=gx, y=gy, color=DIM, sw=2)
        dots = [[a2_dot(a2_sc(a2_PTS[r, c], cell, gx, gy), 0.12) for c in range(a2_COLS)] for r in range(a2_ROWS)]
        flat = [d for row in dots for d in row]
        P, Q = dots[a2_OWN[1]][a2_OWN[0]], dots[a2_OWN[1]][a2_OWN[0] + 1]
        e0, e1 = a2_sc(a2_EDGE[0], cell, gx, gy), a2_sc(a2_EDGE[1], cell, gx, gy)
        p_sc, q_sc = a2_sc(a2_P, cell, gx, gy), a2_sc(a2_Q, cell, gx, gy)
        join = Line(p_sc, q_sc, color=INK, stroke_width=3)
        mp = (p_sc + q_sc) / 2.0
        half_a = DashedLine(mp, e0, color=DIM, stroke_width=5, dash_length=0.12)
        half_b = DashedLine(mp, e1, color=DIM, stroke_width=5, dash_length=0.12)
        l_one = T("one  point  each", 40).move_to([0, 2.95, 0])
        l_eq = T("equally close", 40).move_to([e0[0], -2.9, 0])
        lead = arrow([e0[0], -2.55, 0], [e0[0], e0[1] - 0.14, 0], color=DIM, w=3, tip=0.16)       # a callout, so the label never reads as a longer dashed line
        tag = a2_left(T("drawing", 32, DIM), -6.0, -3.15)

        # the surface cut into squares
        self.play(FadeIn(VGroup(*[s for row in grid.cells for s in row]), lag_ratio=0.03), FadeIn(tag), run_time=0.9)
        # one point drops into each square, at a different spot
        until(self, "put one point in each", lead=0.5)
        self.play(FadeIn(l_one), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.5) for d in flat], lag_ratio=0.05), run_time=1.5)
        # --- after the 45 to 55 percent window: two neighbours, the line of equal distance ---
        until(self, "Foam will live", lead=-0.1)
        self.play(Create(join), Indicate(P, scale_factor=1.9, color=TERRA), Indicate(Q, scale_factor=1.9, color=TERRA), run_time=0.7)
        until(self, "where two points", lead=0.4)
        self.play(Create(half_a), Create(half_b), run_time=1.0)
        until(self, "equally close", lead=0.5)
        self.play(FadeIn(l_eq), Create(lead), run_time=0.5)
        done(self)


# ═════════════════════════ B16 · the nine squares ═════════════════════════
class B16_NineSquares(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        cell, gx, gy = 1.2, -2.2, 0.05
        grid = pixel_grid(cols=a2_COLS, rows=a2_ROWS, cell=cell, x=gx, y=gy, color=DIM, sw=2)
        dots = [[a2_dot(a2_sc(a2_PTS[r, c], cell, gx, gy), 0.12) for c in range(a2_COLS)] for r in range(a2_ROWS)]
        c0, r0 = a2_OWN
        inside = [dots[r][c] for r in range(r0 - 1, r0 + 2) for c in range(c0 - 1, c0 + 2)]
        outside = [dots[r][c] for r in range(a2_ROWS) for c in range(a2_COLS) if not (c0 - 1 <= c <= c0 + 1 and r0 - 1 <= r <= r0 + 1)]
        own, nb = dots[r0][c0], dots[r0][c0 + 1]
        pix_p = a2_sc(a2_PIX, cell, gx, gy)
        pix = Dot(pix_p, radius=0.12, color=CARD).set_stroke(INK, width=5)
        # the 3 by 3 block of squares around the pixel's own square
        bx = gx + (c0 - 2.5) * cell; by = gy + (1.5 - r0) * cell
        block = RoundedRectangle(width=3 * cell, height=3 * cell, corner_radius=0.1, stroke_color=INK, stroke_width=6).move_to([bx, by, 0])
        in_sc = [a2_sc(b, cell, gx, gy) for b in a2_BLOCK]                   # the nine points, in the same order as `inside`
        lines = [Line(pix_p, q, color=DIM, stroke_width=3) for q in in_sc]
        self.add(a2_left(T("drawing", 32, DIM), -6.0, -3.15))                                    # the same small tag as B14: this is a schematic
        near_i = inside.index(nb); sec_i = inside.index(own)
        lnear, lsec = lines[near_i], lines[sec_i]
        others = [ln for i, ln in enumerate(lines) if i not in (near_i, sec_i)]
        # legend for the two lines that will be kept
        ly1, ly2 = 0.8, -0.05
        k1 = Line([2.9, ly1, 0], [4.1, ly1, 0], color=INK, stroke_width=12); t1 = a2_left(T("nearest", 40), 4.35, ly1)
        k2 = Line([2.9, ly2, 0], [4.1, ly2, 0], color=INK, stroke_width=6); t2 = a2_left(T("second", 40), 4.35, ly2)

        self.play(FadeIn(VGroup(*[s for row in grid.cells for s in row]), lag_ratio=0.02), FadeIn(VGroup(*[d for row in dots for d in row])), run_time=0.8)
        # one pixel, near the border of its square
        until(self, "A pixel can be closest", lead=0.0)
        self.play(FadeIn(pix, scale=1.8), run_time=0.4)
        until(self, "neighboring square", lead=0.4)
        self.play(Indicate(nb, scale_factor=2.0, color=TERRA), run_time=0.6)
        # check all nine squares around it
        until(self, "check all nine squares", lead=0.55)
        self.play(Create(block), *[d.animate.set_opacity(0.3) for d in outside], run_time=0.7)
        self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.07), FadeIn(VGroup(k1, k2, t1, t2)), run_time=0.7)
        self.bring_to_front(*inside, pix)
        # --- after the 45 to 55 percent window ---
        until(self, "its own and the eight", lead=-0.2)
        self.play(Indicate(own, scale_factor=2.0, color=TERRA), run_time=0.6)
        # keep the nearest distance, and the second nearest
        until(self, "Keep the nearest", lead=0.3)
        self.play(*[FadeOut(ln) for ln in others], lnear.animate.set_stroke(INK, width=12), run_time=0.7)
        until(self, "the second nearest", lead=0.4)
        self.play(lsec.animate.set_stroke(INK, width=6), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""Act III (B26, B27): the normal map. Manim only, kit objects, real Godot 4.7.2 images through lab_window.
B26: the real normal map with two grey-backed rings, two swatches in real pixel colours with arrows, a colour legend, the steepest lean 13 degrees.
B27: two real 2 x 2 tilings (seam off / seam on), the two switch chips, the measured edge jump (53 times a normal step / about 1).
Numbers are the measured ones from the lane visual_intent (FACTCHECK facts2); nothing is recomputed on screen."""

A3_RED = "#C94A45"; A3_GREEN = "#4E9B5C"; A3_BLUE = "#4A6FD6"


def a3_at(mob, x, y, left=False):
    """Place a mob by its left edge (left=True) or centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a3_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def a3_pix_ring(p, r=0.2):
    """A terracotta ring over a wider grey backing, centred on a point: the point itself stays uncovered (the ring sits just outside it)."""
    back = Circle(radius=r, stroke_color=DIM, stroke_width=12, stroke_opacity=0.55).move_to(np.array(p, dtype=float))
    rg = Circle(radius=r, stroke_color=TERRA, stroke_width=6).move_to(np.array(p, dtype=float))
    return VGroup(back, rg)


def a3_chip(text, x, y):
    """An outlined switch chip: a toggle circle and the switch name. Unlit = grey outline and hollow circle."""
    t = T(text, 32)
    w = t.width + 0.95
    rect = RoundedRectangle(width=w, height=0.66, corner_radius=0.33, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
    dot = Circle(radius=0.12, stroke_color=DIM, stroke_width=4).move_to([x - w / 2 + 0.38, y, 0])
    t.move_to([x - w / 2 + 0.7 + t.width / 2, y, 0])
    g = VGroup(rect, dot, t)
    g.rect = rect; g.dot = dot; g.w = w
    return g


def a3_light(chip):
    """Animations that light a chip: teal outline, filled toggle."""
    return [chip.rect.animate.set_stroke(TEAL, width=6), chip.dot.animate.set_fill(TEAL, opacity=1).set_stroke(TEAL, width=4)]


# ═════════════════════════ B26 · colour is direction ═════════════════════════
class B26_ColorIsDirection(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        W, wx, wy = 5.4, -3.35, 0.4
        lw = lab_window("pantry/normal_a.png", width=W, x=wx, y=wy, caption="real normal map")

        def px(row, col):
            return np.array([wx - W / 2 + (col + 0.5) / 512.0 * W, wy + W / 2 - (row + 0.5) / 512.0 * W, 0.0])
        ring_l = a3_pix_ring(px(100, 100))           # the 'leans' pixel: normal_a.png (100, 100) = (124, 133, 254)
        ring_s = a3_pix_ring(px(285, 226))           # the steepest pixel of the map (12.8 degrees, quoted as 13)

        sx, tx = 0.95, 1.95                           # swatch centre x, text left edge
        yl, yf = 2.45, -1.2                           # 'leans' row, 'flat' row
        sw_l = Square(side_length=1.2, fill_color=a3_hex(124, 133, 254), fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([sx, yl, 0])
        sw_f = Square(side_length=1.2, fill_color=a3_hex(127, 127, 254), fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([sx, yf, 0])
        t_l = a3_at(T("leans", 36), tx, yl + 0.38, left=True); n_l = a3_at(M("(124, 133, 254)", 32), tx, yl - 0.3, left=True)
        t_f = a3_at(T("flat", 36), tx, yf + 0.38, left=True); n_f = a3_at(M("(127, 127, 254)", 32), tx, yf - 0.3, left=True)
        # the arrows: upright for flat; about 3 degrees off upright for the sample pixel (modest: it is one sample)
        tilt = np.radians(3.0)
        base_l = np.array([sx, yl - 0.45, 0.0]); tip_l = base_l + 1.0 * np.array([-np.sin(tilt), np.cos(tilt), 0.0])
        base_f = np.array([sx, yf - 0.45, 0.0]); tip_f = base_f + np.array([0.0, 1.0, 0.0])
        ar_l = arrow(base_l, tip_l, color=INK, w=6, tip=0.22)
        ref_l = DashedLine(base_l, base_l + np.array([0.0, 1.0, 0.0]), color=CARD, stroke_width=3, dash_length=0.1)
        ar_f = arrow(base_f, tip_f, color=INK, w=6, tip=0.22)
        # legend: three arrow shapes in the channel colours, labelled by what each channel does
        ly = [1.15, 0.6, 0.05]
        lg_r = dim_arrow([sx - 0.6, ly[0], 0], [sx + 0.6, ly[0], 0], color=A3_RED, w=7, tip=0.2)
        lg_g = dim_arrow([sx, ly[1] - 0.26, 0], [sx, ly[1] + 0.26, 0], color=A3_GREEN, w=7, tip=0.2)
        lg_b = arrow([sx, ly[2] - 0.26, 0], [sx, ly[2] + 0.26, 0], color=A3_BLUE, w=7, tip=0.2)
        lb_r = a3_at(T("left or right", 32), tx, ly[0], left=True)
        lb_g = a3_at(T("up or down", 32), tx, ly[1], left=True)
        lb_b = a3_at(T("upright", 32), tx, ly[2], left=True)
        # the steepest lean: an upright reference, a 13 degree arrow, the angle, the number
        B = np.array([sx, -3.05, 0.0]); a13 = np.radians(13.0)
        ref13 = DashedLine(B, B + np.array([0.0, 0.95, 0.0]), color=DIM, stroke_width=3, dash_length=0.1)
        ar13 = arrow(B, B + 0.95 * np.array([np.sin(a13), np.cos(a13), 0.0]), color=INK, w=6, tip=0.2)
        arc13 = Arc(radius=0.62, start_angle=PI / 2 - a13, angle=a13, arc_center=B, color=DIM, stroke_width=4)
        n13 = a3_at(T("13°", 64, bold=True), tx, -2.45, left=True)
        s13 = a3_at(T("steepest", 32), tx + 1.45, -2.45, left=True)

        rg_sw = ring(sw_l, pad=0.1, sw=6)            # pairs the swatch with its pixel ring
        rg_13 = ring(n13, pad=0.1, sw=6)             # pairs the number with the steepest pixel's ring
        self.wait(0.2)
        self.play(FadeIn(lw), run_time=0.7)
        # "Red leans left or right": the sample pixel, its colour and its arrow
        until(self, "Red leans", lead=0.35)
        self.play(FadeIn(ring_l), FadeIn(sw_l), FadeIn(rg_sw), FadeIn(t_l), FadeIn(n_l), run_time=0.5)
        self.play(GrowArrow(ar_l), Create(ref_l), run_time=0.6)
        # the legend, one arrow per channel as the voice names it (all before the midpoint)
        until(self, "left or right", lead=0.3)
        self.play(GrowArrow(lg_r), FadeIn(lb_r), run_time=0.45)
        until(self, "green leans", lead=0.2)
        self.play(GrowArrow(lg_g), FadeIn(lb_g), run_time=0.45)
        until(self, "blue is how", lead=1.1)
        self.play(GrowArrow(lg_b), FadeIn(lb_b), run_time=0.45)
        # "A flat pixel is half, half, one"
        until(self, "A flat pixel", lead=0.3)
        self.play(FadeIn(sw_f), FadeIn(t_f), FadeIn(n_f), run_time=0.45)
        self.play(GrowArrow(ar_f), run_time=0.55)
        # "The steepest pixel here leans thirteen degrees"
        until(self, "steepest pixel", lead=0.2)
        self.play(FadeIn(ring_s), run_time=0.4)
        until(self, "thirteen", lead=0.45)
        self.play(Create(ref13), GrowArrow(ar13), Create(arc13), run_time=0.5)
        self.play(FadeIn(n13), FadeIn(rg_13), FadeIn(s13), run_time=0.4)
        done(self)


# ═════════════════════════ B27 · seamless ═════════════════════════
class B27_Seamless(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        W, lx, rx, iy = 3.8, -3.0, 3.0, 0.4
        lw = lab_window("pantry/tiles-not-seamless.png", width=W, x=lx, y=iy, caption="Seamless off")
        rw = lab_window("pantry/tiles-seamless.png", width=W, x=rx, y=iy, caption="Seamless on")
        top, edge_l, edge_r = iy + W / 2, lx - W / 2, rx + W / 2
        # two thin grey ticks per tiling, just outside the picture, marking where the tile edges cross (the seam pixels stay uncovered)
        ticks = VGroup(
            Line([lx, top + 0.08, 0], [lx, top + 0.26, 0], color=DIM, stroke_width=4), Line([edge_l - 0.1, iy, 0], [edge_l - 0.34, iy, 0], color=DIM, stroke_width=4),
            Line([rx, top + 0.08, 0], [rx, top + 0.26, 0], color=DIM, stroke_width=4), Line([edge_r + 0.1, iy, 0], [edge_r + 0.34, iy, 0], color=DIM, stroke_width=4))
        ca = a3_chip("As Normal Map", -1.48, 2.95)
        cb = a3_chip("Seamless", 2.185, 2.95)
        seam = a3_pix_ring([lx - W / 2 + 0.72 * W, iy, 0.0], r=0.3)
        n_off = T("53 times", 48, bold=True).move_to([lx, -2.55, 0]); u_off = T("a normal step", 32, DIM).move_to([lx, -3.05, 0])
        n_on = T("about 1", 48, bold=True).move_to([rx, -2.55, 0]); u_on = T("a normal step", 32, DIM).move_to([rx, -3.05, 0])

        self.wait(0.2)
        self.play(FadeIn(lw), FadeIn(rw), FadeIn(ca), FadeIn(cb), Create(ticks), run_time=0.9)
        # "switch on As Normal Map": the first chip lights
        until(self, "switch on As Normal Map", lead=0.3)
        self.play(*a3_light(ca), run_time=0.45)
        # "Also switch on Seamless": the second chip lights
        until(self, "Also switch on Seamless", lead=0.3)
        self.play(*a3_light(cb), run_time=0.45)
        # "the tile edges show a jump": the ring on the visible seam in the left tiling
        until(self, "tile edges show", lead=0.2)
        self.play(FadeIn(seam), run_time=0.45)
        # "fifty-three times a normal step": the measured jump under each tiling
        until(self, "fifty-three times", lead=0.3)
        self.play(FadeIn(n_off), FadeIn(u_off), run_time=0.45)
        until(self, "normal step", lead=0.15)
        self.play(FadeIn(n_on), FadeIn(u_on), run_time=0.45)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""Act IV (B40): one clock. A schematic (tagged 'drawing'): two time lines, the gap between their starts on three real runs, a uniform that carries one number.
Measured offsets (script clock minus shader TIME, E10 real-time runs, logs/e10-clock.txt and logs/e10-clock-rerun.txt): 0.32 s, 0.28 s, 0.31 s. Drawn to one scale (2.4 units per second), so the bars are honest."""


def a4_at(mob, x, y, left=False):
    """Place a mob by its left edge (left=True) or centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a4_dot(p, r=0.14):
    return Dot(np.array(p, dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════ B40 · one clock ═════════════════════════
class B40_OneClock(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        X0, LEN, K = -4.5, 8.6, 2.4                 # line start x, line length, scene units per second
        ys, yc = 1.9, -1.2                          # shader line, script line
        ym = (ys + yc) / 2.0                        # the strip between them
        rows = [1.1, 0.5, -0.1]                     # one bracket row per run

        def clock(y, color):
            line = arrow([X0, y, 0], [X0 + LEN, y, 0], color=color, w=6, tip=0.24)
            ticks = VGroup(*[Line([X0 + 0.5 * K * k, y - 0.14, 0], [X0 + 0.5 * K * k, y + 0.14, 0], color=DIM, stroke_width=4) for k in range(1, 7)])
            return VGroup(line, ticks, a4_dot([X0, y, 0]))

        sh = clock(ys, INK); shl = a4_at(T("shader time", 36), X0 - 0.1, ys + 0.5, left=True)
        sc = clock(yc, TEAL); scl = a4_at(T("script clock", 36), X0 - 0.1, yc - 0.55, left=True)
        scg = VGroup(sc, scl)
        drawing = T("drawing", 32, DIM).move_to([5.3, -3.05, 0])

        self.wait(0.3)
        self.play(Create(sh[0]), FadeIn(sh[1]), FadeIn(sh[2]), FadeIn(shl), FadeIn(drawing), run_time=0.9)
        # "the script's clock": the second line, starting level with the first (the naive picture)
        until(self, "the script's clock", lead=0.3)
        self.play(Create(sc[0]), FadeIn(sc[1]), FadeIn(sc[2]), FadeIn(scl), run_time=0.9)

        # "start at different moments ... on three runs": the script line slides to the right, once per run, one bracket per run
        gaps = [0.32, 0.28, 0.31]
        cur = 0.0
        brs, lbs, prev_guide = [], [], None
        sg = DashedLine([X0, ys - 0.2, 0], [X0, rows[-1] - 0.2, 0], color=DIM, stroke_width=3, dash_length=0.1)   # the shader's start, carried down
        until(self, "start at different", lead=0.3)
        for k, g in enumerate(gaps):
            ex = X0 + g * K
            slide = [scg.animate.shift([(g - cur) * K, 0, 0])]
            if prev_guide is not None:
                slide.append(FadeOut(prev_guide))
            self.play(*slide, run_time=0.85 if k == 0 else 0.5, rate_func=smooth)
            cur = g
            guide = DashedLine([ex, yc + 0.12, 0], [ex, rows[k], 0], color=DIM, stroke_width=3, dash_length=0.1)
            br = dim_arrow([X0, rows[k], 0], [ex, rows[k], 0], color=DIM, w=5, tip=0.14)
            lb = a4_at(T(f"{g:.2f} s", 36), ex + 0.2, rows[k], left=True)
            anims = [Create(br), Create(guide), FadeIn(lb)]
            if k == 0:
                anims.append(Create(sg))
            self.play(*anims, run_time=0.4)
            brs.append(br); lbs.append(lb); prev_guide = guide

        # "So the script writes its clock into a uniform": clear the runs, the uniform box appears
        until(self, "So the script writes", lead=0.4)
        self.play(FadeOut(VGroup(*brs, *lbs, prev_guide, sg)), run_time=0.4)
        bx = box(1.0, ym, 3.1, 0.95, color=INK, sw=5)
        wl = M("wave_clock", 32).move_to([1.0, ym, 0])
        self.play(Create(bx), FadeIn(wl), run_time=0.5)
        # "writes its clock": an arrow from the script line into the box, and the script line is pulled into line with the shader's
        until(self, "writes its clock", lead=0.15)
        a_in = arrow([1.0, yc + 0.06, 0], [1.0, ym - 0.475, 0], color=INK, w=6, tip=0.2)
        self.play(GrowArrow(a_in), scg.animate.shift([-cur * K, 0, 0]), run_time=0.9, rate_func=smooth)
        # "the shader reads that": an arrow out of the box into the shader line; both lines now run on one number
        until(self, "the shader reads", lead=0.3)
        a_out = arrow([1.0, ym + 0.475, 0], [1.0, ys - 0.07, 0], color=INK, w=6, tip=0.2)
        self.play(GrowArrow(a_out), Indicate(sh[0], color=TEAL, scale_factor=1.0), run_time=0.55)
        one = a4_at(T("one number", 36), -3.5, ym, left=True)
        self.play(FadeIn(one), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""Act V (B42): the depth texture. A schematic (tagged 'drawing'): a camera, the water surface, the sand, one view ray; the depth texture holds the floor, not the water.
Measured test geometry (E8): camera 6 m above the water, floor 0.5 m below; the gap read 0.500 m, so the depth texture held the floor (6.5 m) and not the water (6.0 m).
The picture is not to scale (the 0.5 m gap is exaggerated so the two hit points can be told apart)."""

A5_WATER = "#6E9BC7"; A5_SAND = "#B89D6E"


def a5_at(mob, x, y, left=False):
    """Place a mob by its left edge (left=True) or centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a5_dot(p, r=0.15):
    return Dot(np.array(p, dtype=float), radius=r, color=TERRA).set_stroke(DIM, width=3)


def a5_wave(x):
    return -0.2 + 0.05 * np.sin(3.0 * x)


# ═════════════════════════ B42 · the depth texture ═════════════════════════
class B42_DepthTexture(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        ttl = T("The Shore", 40)
        ttl.move_to([-6.2 + ttl.width / 2, 3.05, 0])
        self.add(ttl)

        # the cast: camera, surface, sand
        cam_body = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.1, stroke_color=INK, stroke_width=5).move_to([-5.0, 1.2, 0])
        cam_lens = Polygon([-4.55, 1.35, 0], [-4.25, 1.5, 0], [-4.25, 0.9, 0], [-4.55, 1.05, 0], stroke_color=INK, stroke_width=5)
        cam_lab = T("camera", 32).move_to([-5.0, 0.55, 0])
        surface = ParametricFunction(lambda t: np.array([t, a5_wave(t), 0.0]), t_range=[-5.9, 5.9], stroke_color=A5_WATER, stroke_width=7)
        ysand = -1.9
        sand = Line([-5.9, ysand, 0], [5.9, ysand, 0], color=A5_SAND, stroke_width=8)
        rs = np.random.RandomState(4)
        specks = VGroup(*[Dot([float(rs.uniform(-5.7, 5.7)), float(rs.uniform(ysand - 0.28, ysand - 0.1)), 0], radius=0.035, color=A5_SAND) for _ in range(26)])
        drawing = T("drawing", 32, DIM).move_to([5.3, -3.05, 0])

        # the ray: camera -> water point W -> floor point F (W found where the ray meets the wavy surface)
        C = np.array([-4.25, 1.2, 0.0]); F = np.array([-0.4, ysand, 0.0])
        wx = -2.5
        for _ in range(6):
            yw = a5_wave(wx)
            wx = C[0] + (C[1] - yw) / (C[1] - F[1]) * (F[0] - C[0])
        W = np.array([wx, a5_wave(wx), 0.0])
        ray1 = Line(C, W, color=INK, stroke_width=6)
        ray2 = Line(W, F, color=INK, stroke_width=6)
        dw = a5_dot(W); df = a5_dot(F)
        lw = T("water 6.0 m", 32).move_to([-3.95, -0.85, 0])
        lw_lead = Line([W[0] - 0.12, W[1] - 0.12, 0], [W[0] - 0.42, W[1] - 0.45, 0], color=DIM, stroke_width=3)
        lf = T("floor 6.5 m", 32).move_to([F[0], ysand - 0.75, 0])
        lf_lead = Line([F[0], ysand - 0.2, 0], [F[0], ysand - 0.5, 0], color=DIM, stroke_width=3)

        # the depth texture box, holding only the floor value
        bx = box(3.6, 1.95, 3.9, 1.6, color=INK, sw=5)
        bt = T("depth texture", 32).move_to([3.6, 3.15, 0])
        bv = T("6.5 m", 48, bold=True).move_to([3.6, 1.5, 0])
        f_from = F + np.array([0.2, 0.18, 0.0])
        a_floor = arrow(f_from, np.array([2.9, 1.12, 0.0]), color=INK, w=6, tip=0.22)
        flow = a5_dot(f_from, r=0.1)
        # the water's arrow, grey and struck out
        w_from = W + np.array([0.1, 0.12, 0.0]); w_to = np.array([1.52, 1.7, 0.0])
        a_water = arrow(w_from, w_to, color=DIM, w=6, tip=0.22)
        mid = (w_from + w_to) / 2.0
        cross = VGroup(Line(mid + np.array([-0.27, -0.27, 0.0]), mid + np.array([0.27, 0.27, 0.0]), color=INK, stroke_width=7),
                       Line(mid + np.array([-0.27, 0.27, 0.0]), mid + np.array([0.27, -0.27, 0.0]), color=INK, stroke_width=7))
        notin = T("not in it", 32).move_to([mid[0] - 0.55, mid[1] + 0.8, 0])

        self.wait(0.2)
        self.play(FadeIn(VGroup(cam_body, cam_lab)), Create(cam_lens), Create(surface), Create(sand), FadeIn(specks), FadeIn(drawing), run_time=0.9)
        # "To know that, the water must know how deep": the ray draws from the camera, a dot marks each hit
        until(self, "To know that", lead=0.2)
        self.play(Create(ray1), run_time=0.8, rate_func=linear)
        self.play(FadeIn(dw, scale=1.6), FadeIn(lw), Create(lw_lead), run_time=0.35)
        until(self, "the water must", lead=0.2)
        self.play(Create(ray2), run_time=0.5, rate_func=linear)
        self.play(FadeIn(df, scale=1.6), FadeIn(lf), Create(lf_lead), run_time=0.35)
        # "how deep it is" / "A texture with the hint": the box, then only the floor value flows into it (all before the midpoint)
        until(self, "how deep it is", lead=0.3)
        self.play(Create(bx), FadeIn(bt), run_time=0.5)
        until(self, "A texture", lead=0.95)
        self.play(Create(a_floor), FadeIn(flow), run_time=0.35)
        self.play(flow.animate.move_to([2.9, 1.12, 0]), run_time=0.6, rate_func=linear)
        self.play(FadeOut(flow), FadeIn(bv), run_time=0.3)
        # "The water itself is not in it": the water's arrow, grey, struck out
        until(self, "The water itself", lead=0.3)
        self.play(Create(a_water), run_time=0.5)
        self.play(Create(cross), FadeIn(notin), run_time=0.35)
        # "so it can look beneath": the ray runs on through the water to the floor
        until(self, "look beneath", lead=0.3)
        self.play(Indicate(ray2, color=TEAL, scale_factor=1.0), run_time=0.7)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
