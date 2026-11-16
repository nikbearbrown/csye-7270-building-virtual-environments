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
"""Act I · Corners (B02, B03, B04, B08, B10; B01/B05-B07/B09 are captures). Manim only, kit objects.
Cast: the test rectangle with four terracotta corner dots. Numbers are the measured ones (CAPTURE-PLAN, evidence/planning-checks/measurements.txt)."""


def a1_at(mob, x, y, left=False, right=False):
    """Place a mob by an edge: left=True puts its left edge at x, right=True its right edge at x; else centred."""
    if left:
        mob.move_to([x + mob.width / 2.0, y, 0])
    elif right:
        mob.move_to([x - mob.width / 2.0, y, 0])
    else:
        mob.move_to([x, y, 0])
    return mob


def a1_dot(p):
    return Dot(np.array(p, dtype=float), radius=0.16, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════ B02 · four corners ═════════════════════════
class B02_FourCorners(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        W, H, cy = 4.4, 2.6, 0.3
        P0 = [np.array(p, dtype=float) for p in ([-W / 2, cy + H / 2, 0], [W / 2, cy + H / 2, 0], [W / 2, cy - H / 2, 0], [-W / 2, cy - H / 2, 0])]
        dots = [a1_dot(p) for p in P0]
        body = Polygon(*P0, stroke_color=INK, stroke_width=5)
        offs = [np.array(o) for o in ([-0.42, 0.38, 0], [0.42, 0.38, 0], [0.42, -0.38, 0], [-0.42, -0.38, 0])]
        nums = [T(str(i + 1), 36).move_to(P0[i] + offs[i]) for i in range(4)]
        cap = T("vertex(): runs once for each vertex; places the corners", 32).move_to([0, -2.75, 0])
        self.add(body)
        self.play(FadeIn(VGroup(*dots)), FadeIn(cap), run_time=0.7)
        self.wait(0.3)
        for i in range(4):
            self.play(FadeIn(nums[i], run_time=0.2), Indicate(dots[i], scale_factor=1.9, color=TERRA), run_time=0.55)
        until(self, "where does this corner go", lead=2.6)
        q = T("where?", 36).move_to([0, cy, 0])
        self.play(FadeIn(q), run_time=0.3)
        until(self, "where does this corner go", lead=0.2)
        P1 = [[-1.4, cy + H / 2, 0], [3.0, cy + H / 2, 0], [1.7, cy - H / 2, 0], [-2.7, cy - H / 2, 0]]
        trails = VGroup(*[Line(np.array(P0[i]), np.array(P1[i], dtype=float), color=DIM, stroke_width=4) for i in range(4)])
        newbody = Polygon(*[np.array(p, dtype=float) for p in P1], stroke_color=INK, stroke_width=5)
        self.play(FadeOut(q), Create(trails), Transform(body, newbody), *[dots[i].animate.move_to(P1[i]) for i in range(4)],
                  *[nums[i].animate.move_to(np.array(P1[i], dtype=float) + offs[i]) for i in range(4)], run_time=1.5, rate_func=smooth)
        done(self)


# ═════════════════════════ B03 · in and out ═════════════════════════
class B03_InAndOut(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        bx = box(0, 0.65, 5.7, 2.5, color=INK, sw=4)
        title = M("vertex()", 32).move_to([0, 1.5, 0])
        code = M("VERTEX.x += 40.0;", 32).move_to([0, 0.85, 0])
        cap = T("built-in: a value the engine hands to a function", 32).move_to([0, -2.75, 0])
        self.play(Create(bx), FadeIn(title), FadeIn(code), FadeIn(cap), run_time=0.9)
        yy = 0.0
        ghost = Dot([-4.5, yy, 0], radius=0.2, color=DIM)
        d = Dot([-6.0, yy, 0], radius=0.2, color=TERRA).set_stroke(DIM, width=3)
        nm = M("VERTEX", 32).move_to([-4.5, yy + 0.6, 0])
        lab_in = M("(-64, -64)", 32).move_to([-4.5, yy - 0.6, 0])
        self.play(d.animate.move_to([-4.5, yy, 0]), FadeIn(ghost), FadeIn(nm), FadeIn(lab_in), run_time=1.0, rate_func=smooth)
        self.remove(ghost); self.add(ghost)
        until(self, "a value it gives", lead=0.0)
        hl = VGroup(Rectangle(width=code.width + 0.3, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).next_to(code, DOWN, buff=0.08), Rectangle(width=code.width + 0.3, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).next_to(code, DOWN, buff=0.12))  # terracotta underline bar over a grey backing (a bar, never text)
        self.play(d.animate.move_to([4.5, yy, 0]), FadeIn(hl), run_time=1.6, rate_func=linear)
        lab_out = M("(-24, -64)", 32).move_to([4.5, yy - 0.6, 0])
        nm2 = M("VERTEX", 32).move_to([4.5, yy + 0.6, 0])
        self.play(FadeIn(lab_out), FadeIn(nm2), FadeOut(hl), run_time=0.4)
        until(self, "Whatever you leave", lead=0.1)
        self.play(Indicate(d, scale_factor=1.7, color=TERRA), run_time=0.6)
        done(self)


# ═════════════════════════ B04 · pixels from the middle ═════════════════════════
class B04_PixelsFromTheMiddle(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        S, cy = 2.8, 0.2
        sq = Square(side_length=S, stroke_color=INK, stroke_width=5).move_to([0, cy, 0])
        cross = VGroup(Line([-0.2, cy, 0], [0.2, cy, 0], color=INK, stroke_width=5), Line([0, cy - 0.2, 0], [0, cy + 0.2, 0], color=INK, stroke_width=5))
        ax = arrow([0.25, cy, 0], [2.5, cy, 0], color=INK, w=5)
        ay = arrow([0, cy - 0.25, 0], [0, cy - 2.2, 0], color=INK, w=5)
        lx = T("x", 36).move_to([2.8, cy, 0]); ly = T("y", 36).move_to([0.85, cy - 2.0, 0])
        bar = dim_arrow([-S / 2, 2.05, 0], [S / 2, 2.05, 0], color=DIM)
        bl = T("128 px", 32).move_to([0, 2.55, 0])
        credit = T("measured in Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -3.0, 0])
        self.play(Create(sq), FadeIn(cross), FadeIn(bar), FadeIn(bl), run_time=0.8)
        self.play(GrowArrow(ax), GrowArrow(ay), FadeIn(lx), FadeIn(ly), FadeIn(credit), run_time=0.8)
        until(self, "corners at minus", lead=0.4)
        h = S / 2
        specs = [("(-64, -64)", -h, cy + h, True), ("(64, -64)", h, cy + h, False), ("(-64, 64)", -h, cy - h, True), ("(64, 64)", h, cy - h, False)]
        dots = []
        for s, px, py, isl in specs:
            dt = a1_dot([px, py, 0])
            lb = M(s, 32)
            a1_at(lb, px - 0.35, py, right=True) if isl else a1_at(lb, px + 0.35, py, left=True)
            self.play(FadeIn(dt, scale=1.6), FadeIn(lb), run_time=0.45)
        until(self, "The y axis points down", lead=0.1)
        r = ring(ay, pad=0.18)
        self.play(FadeIn(r), run_time=0.5)
        self.play(Indicate(ly, scale_factor=1.5, color=INK), run_time=0.6)
        done(self)


# ═════════════════════════ B08 · the address ═════════════════════════
class B08_Address(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        S, cy = 2.8, 0.3
        h = S / 2
        sq = Square(side_length=S, stroke_color=INK, stroke_width=5).move_to([0, cy, 0])
        cs = [(-h, cy + h, True, "(-64, -64)", "(0, 0)"), (h, cy + h, False, "(64, -64)", "(1, 0)"),
              (-h, cy - h, True, "(-64, 64)", "(0, 1)"), (h, cy - h, False, "(64, 64)", "(1, 1)")]
        pix = []; adr = []
        for x, y, isl, p, a in cs:
            pl = M(p, 32, DIM); al = M(a, 32, INK)
            if isl:
                a1_at(pl, x - 0.4, y + 0.3, right=True); a1_at(al, x - 0.4, y - 0.3, right=True)
            else:
                a1_at(pl, x + 0.4, y + 0.3, left=True); a1_at(al, x + 0.4, y - 0.3, left=True)
            pix.append(pl); adr.append(al)
        cd = [Dot([x, y, 0], radius=0.09, color=DIM) for x, y, *_ in cs]
        lg1 = T("pixels", 32, DIM).move_to([-1.3, -2.3, 0]); lg2 = T("address", 32, INK).move_to([1.3, -2.3, 0])
        cap = T("UV: a point's address on the shape: 0 to 1 across, 0 to 1 down", 32).move_to([0, -3.0, 0])
        self.play(Create(sq), FadeIn(VGroup(*cd)), FadeIn(VGroup(*pix)), FadeIn(lg1), run_time=0.9)
        until(self, "The engine gives each", lead=0.3)
        self.play(FadeIn(lg2), FadeIn(cap), run_time=0.5)
        walker = a1_dot([cs[0][0], cs[0][1], 0])
        self.play(FadeIn(walker, scale=1.5), FadeIn(adr[0]), run_time=0.4)
        for i in (1, 2, 3):
            self.play(walker.animate.move_to([cs[i][0], cs[i][1], 0]), run_time=0.5, rate_func=smooth)
            self.play(FadeIn(adr[i]), run_time=0.2)
        until(self, "Top left is zero", lead=0.1)
        r1 = ring(adr[0], pad=0.06, sw=6)
        self.play(FadeIn(r1), run_time=0.4)
        until(self, "Bottom right is one", lead=0.1)
        r2 = ring(adr[3], pad=0.06, sw=6)
        self.play(FadeIn(r2), run_time=0.4)
        done(self)


# ═════════════════════════ B10 · even steps ═════════════════════════
class B10_EvenSteps(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        k = 3.6 / 128.0                     # one pixel row/column in scene units
        x0, ytop = -1.4, 1.95
        P = lambda shift, row: np.array([x0 + shift * k, ytop - row * k, 0])
        ref = DashedLine(P(0, 0), P(0, 128), color=DIM, stroke_width=4, dash_length=0.12)
        edge = Line(P(0, 0), P(50, 128), color=INK, stroke_width=6)
        self.play(Create(ref), run_time=0.6)
        self.play(Create(edge), run_time=1.2)
        until(self, "in even steps", lead=0.3)
        for shift, row in [(1, 2), (12, 31), (25, 63), (37, 95), (49, 124)]:
            d = a1_dot(P(shift, row))
            lb = T(f"+{shift} px", 32)
            a1_at(lb, P(shift, row)[0] + 0.4, P(shift, row)[1], left=True)
            self.play(FadeIn(d, scale=1.7), FadeIn(lb), run_time=0.4)
            self.wait(0.1)
        cap = T("four corners: straight edges", 36).move_to([0, -2.2, 0])
        until(self, "on a straight line", lead=0.3)
        self.play(FadeIn(cap), run_time=0.4)
        c1 = T("Apple M4 Pro · Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -2.65, 0])
        c2 = T("straight to within half a pixel", 32, DIM).move_to([0, -3.05, 0])
        until(self, "to within half", lead=0.3)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        until(self, "Remember that", lead=0.1)
        self.play(Indicate(edge, color=TEAL, scale_factor=1.0), run_time=0.8)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
def a2_poly(g, n):
    return [g.pt(i / (n - 1)) for i in range(n)]


def a2_tdot(p, r=0.15):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


class B13_OnlyWhatExists(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        g = plot(lambda v: 0.5 + 0.45 * np.sin(2.2 * np.pi * v), size=(9.0, 3.4), x=0.0, y=0.4, color=DIM)
        self.add(g.axes)
        self.wait(0.3)
        self.play(Create(g.curve), run_time=1.2)
        pts = a2_poly(g, 2)
        chord = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts)
        dots = VGroup(*[a2_tdot(p) for p in pts])
        lab = T("2 vertices", 40).move_to([0, -1.9, 0])
        self.play(Create(chord), FadeIn(dots), FadeIn(lab), run_time=0.8)
        until(self, "Between two corners")
        for n, nm in ((3, "3 vertices"), (5, "5 vertices")):
            pts = a2_poly(g, n)
            new_chord = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts)
            new_dots = VGroup(*[a2_tdot(p) for p in pts])
            new_lab = T(nm, 40).move_to([0, -1.9, 0])
            self.play(Transform(chord, new_chord), ReplacementTransform(dots, new_dots), ReplacementTransform(lab, new_lab), run_time=0.7)
            dots, lab = new_dots, new_lab
            self.wait(0.35)
        until(self, "A curve needs corners")
        pts = a2_poly(g, 9)
        new_chord = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts)
        new_dots = VGroup(*[a2_tdot(p) for p in pts])
        new_lab = T("9 vertices", 40).move_to([0, -1.9, 0])
        self.play(Transform(chord, new_chord), ReplacementTransform(dots, new_dots), ReplacementTransform(lab, new_lab), run_time=1.0)
        until(self, "for vertex to push up")
        cap = T("vertex moves only the vertices that exist", 36).move_to([0, -2.8, 0])
        self.play(FadeIn(cap), run_time=0.5)
        done(self)


class B14_TwoWays(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        lx, rx, py = -3.3, 3.3, 0.8
        pl = box(lx, py, 5.8, 3.1, color=DIM, sw=4)
        pr = box(rx, py, 5.8, 3.1, color=DIM, sw=4)
        nl = M("Polygon2D", 32).move_to([lx, 2.9, 0])
        nr = M("MeshInstance2D", 32).move_to([rx, 2.9, 0])
        self.add(pl, pr)
        self.play(FadeIn(nl), FadeIn(nr), run_time=0.5)
        sl = T("you place the points", 32).move_to([lx, -1.1, 0])
        sr = T("a mesh cut into a grid", 32).move_to([rx, -1.1, 0])
        self.play(FadeIn(sl), FadeIn(sr), run_time=0.4)
        until(self, "A polygon node")
        # polygon points placed one at a time
        P = [(-4.9, 0.2), (-4.3, 1.7), (-3.2, 2.0), (-2.2, 1.3), (-2.3, 0.2), (-3.5, -0.1)]
        P = [np.array([x, y, 0.0]) for x, y in P]
        placed = []
        lines = []
        for i, p in enumerate(P):
            d = a2_tdot(p, 0.14)
            anims = [FadeIn(d, scale=1.6)]
            if i:
                ln = Line(P[i - 1], p, color=INK, stroke_width=5)
                lines.append(ln); anims.append(Create(ln))
            self.play(*anims, run_time=0.32)
            placed.append(d)
        closer = Line(P[-1], P[0], color=INK, stroke_width=5)
        self.play(Create(closer), run_time=0.4)
        until(self, "Or a mesh node")
        W, H = 4.4, 2.4
        cx, cy = rx, py
        rect = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=5).move_to([cx, cy, 0])
        self.play(Create(rect), run_time=0.5)
        vl = [Line([cx - W / 2 + W * k / 6, cy - H / 2, 0], [cx - W / 2 + W * k / 6, cy + H / 2, 0], color=DIM, stroke_width=3) for k in range(1, 6)]
        hl = [Line([cx - W / 2, cy - H / 2 + H * k / 4, 0], [cx + W / 2, cy - H / 2 + H * k / 4, 0], color=DIM, stroke_width=3) for k in range(1, 4)]
        self.play(LaggedStart(*[Create(l) for l in vl + hl], lag_ratio=0.15), run_time=1.2)
        gd = VGroup(*[Dot([cx - W / 2 + W * i / 6, cy - H / 2 + H * j / 4, 0], radius=0.09, color=TERRA).set_stroke(DIM, width=2) for i in range(7) for j in range(5)])
        self.play(LaggedStart(*[FadeIn(d, scale=1.4) for d in gd], lag_ratio=0.03), run_time=1.0)
        until(self, "the vertices and triangles")
        cap = T("mesh: the vertices and triangles that make a shape", 36).move_to([0, -2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        done(self)


def a2_num(n, x, y, size=64):
    return T(str(n), size, bold=True).move_to([x, y, 0])


class B16_CountThem(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        lx, rx, gy = -3.6, 3.45, 0.3
        l1 = T("cut 3 by 3", 40).move_to([lx, 2.3, 0])
        self.add(l1)
        until(self, "Cut a quad mesh")
        cnt = a2_num(0, lx, -1.3)
        self.add(cnt)
        gap = 0.55
        total = 0
        for r in range(5):
            row = VGroup(*[Dot([lx + (c - 2) * gap, gy + (2 - r) * gap + 0.0, 0], radius=0.1, color=TERRA).set_stroke(DIM, width=2) for c in range(5)])
            total += 5
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in row], lag_ratio=0.12), run_time=0.55)
            self.remove(cnt); cnt = a2_num(total, lx, -1.3); self.add(cnt)
        until(self, "Always two more")
        f = T("(cuts + 2) x (cuts + 2)", 40).move_to([0, -2.4, 0])
        self.play(FadeIn(f), run_time=0.5)
        l2 = T("cut 31 by 7", 40).move_to([rx, 2.3, 0])
        fr = Rectangle(width=5.5, height=1.45, stroke_color=GHOST, stroke_width=3).move_to([rx, gy, 0])
        self.play(FadeIn(l2), Create(fr), run_time=0.5)
        until(self, "The flag's thirty-one")
        cnt2 = a2_num(0, rx, -1.3)
        self.add(cnt2)
        g2 = 0.165
        total = 0
        for r in range(9):
            row = VGroup(*[Dot([rx + (c - 16) * g2, gy + (4 - r) * g2, 0], radius=0.045, color=TERRA) for c in range(33)])
            total += 33
            self.play(LaggedStart(*[FadeIn(d) for d in row], lag_ratio=0.02), run_time=0.3)
            self.remove(cnt2); cnt2 = a2_num(total, rx, -1.3); self.add(cnt2)
        cr = T("counted from the mesh in Godot 4.7.2", 32, color=DIM).move_to([0, -3.1, 0])
        self.play(FadeIn(cr), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
def a4_tdot(p, r=0.15):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


class B27_FragmentCannotSee(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        ttl = T("Passing Data Forward", 40)
        ttl.move_to([-6.2 + ttl.width / 2, 3.05, 0])
        self.add(ttl)
        y = 0.7
        xs = (-4.4, 0.0, 4.4)
        q = vertex_quad(w=2.1, h=1.4, x=xs[0], y=y)
        l1 = M("vertex()", 32).move_to([xs[0], y + 1.35, 0])
        card = Rectangle(width=2.1, height=1.4, stroke_color=DIM, stroke_width=4).move_to([xs[1], y, 0])
        tiles = VGroup(*[Rectangle(width=0.2, height=1.2, fill_color=_rgb(i / 7), fill_opacity=1, stroke_width=0).move_to([xs[1] - 0.9 + i * 0.257, y, 0]) for i in range(8)])
        l2 = T("card fills shape", 32).move_to([xs[1], y + 1.35, 0])
        pg = pixel_grid(cols=6, rows=4, cell=0.38, x=xs[2], y=y)
        l3 = M("fragment()", 32).move_to([xs[2], y + 1.35, 0])
        a1 = arrow([xs[0] + 1.35, y, 0], [xs[1] - 1.35, y, 0])
        a2 = arrow([xs[1] + 1.35, y, 0], [xs[2] - 1.35, y, 0])
        self.wait(0.3)
        self.play(FadeIn(q), FadeIn(l1), run_time=0.6)
        self.play(Create(a1), FadeIn(card), FadeIn(l2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.1), run_time=0.7)
        self.play(Create(a2), FadeIn(pg), FadeIn(l3), run_time=0.6)
        until(self, "the function that colors")
        cap = T("fragment(): runs once for each pixel the shape covers;", 32).move_to([0, -1.55, 0])
        cap2 = T("sets its color", 32).move_to([0, -2.1, 0])
        self.play(FadeIn(cap), FadeIn(cap2), run_time=0.5)
        until(self, "But fragment runs later")
        glass = VGroup(RoundedRectangle(width=0.3, height=2.6, corner_radius=0.08, stroke_color=TEAL, stroke_width=6).move_to([-2.65, y, 0]),
                       Line([-2.7, y - 0.6, 0], [-2.6, y - 0.2, 0], color=TEAL, stroke_width=3), Line([-2.7, y + 0.2, 0], [-2.6, y + 0.6, 0], color=TEAL, stroke_width=3))
        self.play(Create(glass), run_time=0.6)
        qm = T("?", 64, bold=True).move_to([xs[2] - 0.0, y - 1.15, 0])
        trail = Dot(qm.get_center() + [0, -0.5, 0], radius=0.1, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(qm), FadeIn(trail), run_time=0.3)
        self.play(qm.animate.move_to([-2.2, y - 1.15, 0]), trail.animate.move_to([-2.2, y - 1.65, 0]), run_time=1.7, rate_func=linear)
        self.play(qm.animate.shift([0.12, 0, 0]), run_time=0.12)
        self.play(qm.animate.shift([-0.12, 0, 0]), run_time=0.12)
        done(self)


class B28_Varying(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        cx, cy = 0.0, 1.35
        q = vertex_quad(w=5.0, h=2.4, x=cx, y=cy)
        self.wait(0.3)
        self.play(FadeIn(q), run_time=0.6)
        nums = VGroup(*[T(s, 44, bold=True).move_to(p + np.array([dx, 0, 0])) for s, p, dx in
                        (("0", q.pts[0], -0.5), ("1", q.pts[1], 0.5), ("1", q.pts[2], 0.5), ("0", q.pts[3], -0.5))])
        self.play(FadeIn(nums), run_time=0.5)
        until(self, "In vertex")
        ay = -1.05
        ls = T("set in vertex()", 36).move_to([-4.5, ay, 0])
        lr = T("read in fragment()", 36).move_to([4.2, ay, 0])
        ar = arrow([-2.8, ay, 0], [2.0, ay, 0])
        self.play(FadeIn(ls), run_time=0.4)
        self.play(Create(ar), run_time=0.5)
        self.play(FadeIn(lr), run_time=0.4)
        until(self, "The graphics card interpolates")
        n = 36
        w = 4.6
        cols = VGroup(*[Rectangle(width=w / n * 0.8, height=2.0, fill_color=_rgb(i / (n - 1)), fill_opacity=1, stroke_width=0).move_to([cx - w / 2 + w / n * (i + 0.5), cy, 0]) for i in range(n)])
        self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.05), run_time=1.6)
        until(self, "it flows one way", lead=0.5)
        fw = T("forward", 36).move_to([-0.5, ay + 0.5, 0])
        d = Dot([-2.8, ay, 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(fw), FadeIn(d), run_time=0.3)
        self.play(d.animate.move_to([2.0, ay, 0]), run_time=0.7, rate_func=linear)
        c1 = T("varying: a value set at each corner, blended across", 32).move_to([0, -2.2, 0])
        c2 = T("the shape for fragment() to read", 32).move_to([0, -2.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        done(self)


def a4_checker(x, y, size, c1, c2, n=4):
    s = size / n
    g = VGroup()
    for i in range(n):
        for j in range(n):
            g.add(Square(side_length=s * 0.94, stroke_width=0, fill_color=c1 if (i + j) % 2 == 0 else c2, fill_opacity=1).move_to([x - size / 2 + s * (i + 0.5), y + size / 2 - s * (j + 0.5), 0]))
    return g


class B31_BuiltInVaryings(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        rs = ramp_strip(width=6.0, y=2.3, label0="0", label1="1", n=40, height=0.4)
        for t in rs.tiles:
            t.set_fill(opacity=0)
        self.add(rs.labels)
        d0 = a4_tdot(np.array([rs.x0 - 0.22, rs.y, 0.0]))
        d1 = a4_tdot(np.array([rs.x1 + 0.22, rs.y, 0.0]))
        self.wait(0.3)
        self.play(FadeIn(d0), FadeIn(d1), run_time=0.5)
        until(self, "U V is set")
        lab = T("U V: set at the corners, blended", 36).move_to([0, 1.2, 0])
        self.play(FadeIn(lab), run_time=0.4)
        self.play(LaggedStart(*[t.animate.set_fill(opacity=1) for t in rs.tiles], lag_ratio=0.05), run_time=1.6)
        by = -0.3
        until(self, "The color from vertex")
        block = Square(side_length=1.2, fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to([-2.4, by, 0])
        chk = a4_checker(-0.4, by, 1.4, "#F2F0E9", "#D9D4C7")
        self.play(FadeIn(block), run_time=0.4)
        self.play(FadeIn(chk), run_time=0.4)
        until(self, "and multiplied", lead=0.8)
        xs = VGroup(Line([-1.65, by + 0.18, 0], [-1.3, by - 0.18, 0], color=INK, stroke_width=6), Line([-1.65, by - 0.18, 0], [-1.3, by + 0.18, 0], color=INK, stroke_width=6)).shift([0.0, 0, 0])
        xs.move_to([-1.4, by, 0])
        eq = VGroup(Line([0.5, by + 0.1, 0], [0.9, by + 0.1, 0], color=INK, stroke_width=6), Line([0.5, by - 0.1, 0], [0.9, by - 0.1, 0], color=INK, stroke_width=6))
        res = a4_checker(2.0, by, 1.4, TEAL, "#8DBDAE")
        self.play(Create(xs), run_time=0.4)
        self.play(Create(eq), run_time=0.4)
        self.play(FadeIn(res), run_time=0.6)
        l1 = T("color from vertex x the picture", 32).move_to([-1.5, -1.45, 0])
        l2 = T("= color in fragment", 32).move_to([2.9, -1.45, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        cap = T("COLOR: the color being drawn", 36).move_to([0, -2.6, 0])
        self.play(FadeIn(cap), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""Act V · When It Looks Wrong (B36 only here; the rest are captures). Numbers measured (Lab 11/15, 10/14 probes): vertex-stage corner (-64, -64);
fragment-stage first pixel of the sprite about (576, 296) in a 1280 x 720 window."""


def a5_dot(p):
    return Dot(np.array(p, dtype=float), radius=0.16, color=TERRA).set_stroke(DIM, width=3)


class B36_TwoMeanings(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        fw, fh, fcx, fcy = 7.6, 4.275, 0.0, 0.95
        k = fw / 1280.0
        frame = Rectangle(width=fw, height=fh, stroke_color=DIM, stroke_width=5).move_to([fcx, fcy, 0])
        sp = Square(side_length=128 * k, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=0.9).move_to([fcx, fcy, 0])
        tl = np.array([fcx - 64 * k, fcy + 64 * k, 0]); mid = np.array([fcx, fcy, 0]); ftl = np.array([fcx - fw / 2, fcy + fh / 2, 0])
        dim = T("1280 × 720", 32, DIM).move_to([fcx + 2.6, fcy - 1.7, 0])
        credit = T("measured in Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -3.1, 0])
        self.add(frame, sp)
        self.play(FadeIn(dim), FadeIn(credit), run_time=0.5)
        corner = a5_dot(tl)
        rg = ring(Circle(radius=0.14).move_to(tl), pad=0.03, sw=6)
        self.play(FadeIn(corner, scale=1.6), FadeIn(rg), run_time=0.5)
        until(self, "In vertex", lead=0.2)
        mk = Dot(mid, radius=0.07, color=INK)
        a1 = arrow(mid, tl + np.array([0.17, -0.17, 0]), color=INK, w=6, tip=0.12)
        n1 = M("vertex()", 32).move_to([-3.4, -1.7, 0]); v1 = M("(-64, -64)", 32).move_to([-3.4, -2.15, 0]); w1 = T("from the node's middle", 32).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(mk), GrowArrow(a1), FadeIn(n1), FadeIn(v1), FadeIn(w1), run_time=0.8)
        until(self, "In fragment", lead=0.2)
        a2 = arrow(ftl, tl + np.array([-0.2, 0.2, 0]), color=INK, w=5, tip=0.16)
        n2 = M("fragment()", 32).move_to([3.4, -1.7, 0]); v2 = M("(576, 296)", 32).move_to([3.4, -2.15, 0]); w2 = T("from the screen's top left", 32).move_to([3.4, -2.6, 0])
        self.play(GrowArrow(a2), FadeIn(n2), FadeIn(v2), FadeIn(w2), run_time=0.8)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
