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
"""ACT I · One Pixel, All at Once (Manim beats B02, B03, B05, B07, B08).

Cast for the act: the teal test sprite (sprite_icon), the pixel grid of OUTLINE cells, the 0 to 1 ramp colours (ghost to teal).
Every number on screen is from the lane / FACTCHECK: 55 ms (52 to 58 over five runs), 16.7 ms frame, about 0.04 ms CPU hand-over, M4 Pro, Godot 4.7.2.
"""


def a1_pair(y=0.25, w=4.6, h=3.4, x=3.8, lt="game code · CPU", rt="the shader · GPU", size=36):
    """Two outlined boxes (CPU left, GPU right) with their titles. Returns (L, R, ltxt, rtxt)."""
    L = box(-x, y, w, h)
    R = box(x, y, w, h)
    a = T(lt, size).move_to([-x, y + h / 2 - 0.5, 0])
    b = T(rt, size).move_to([x, y + h / 2 - 0.5, 0])
    return L, R, a, b


def a1_wobble(cx, cy, r=0.78, amp=0.07, k=9):
    """A wavy ring round a picture: the 'restyled by the shader' mark (a drawing, not a render)."""
    return ParametricFunction(
        lambda t: np.array([cx + (r + amp * np.sin(k * t)) * np.cos(t), cy + (r + amp * np.sin(k * t)) * np.sin(t), 0.0]),
        t_range=[0, TAU, 0.05], color=INK, stroke_width=5)


# ───────────────────────────────────────────────────────────────────────────
class B02_WhatAndWhere(Scene):
    def construct(self):
        L, R, lt, rt = a1_pair(y=0.25)
        ico = sprite_icon(-3.8, 0.4, 0.45)
        self.wait(0.3)
        self.play(Create(L), FadeIn(lt), FadeIn(ico), run_time=0.9)
        until(self, "the G P U")
        ar = arrow([-1.4, 0.4, 0], [1.4, 0.4, 0])
        self.play(Create(R), FadeIn(rt), GrowArrow(ar), run_time=0.9)
        until(self, "It decides")
        moved = ico.copy()
        self.add(moved)
        self.play(moved.animate.move_to([3.8, 0.4, 0]), run_time=1.5)
        wob = a1_wobble(3.8, 0.4, r=0.68)
        self.play(Create(wob), run_time=0.6)
        until(self, "Your game code")
        ls = T("what exists, where", 34).move_to([-3.8, -1.0, 0])
        self.play(FadeIn(ls), run_time=0.5)
        until(self, "The shader decides")
        rs = T("how each part looks", 34).move_to([3.8, -1.0, 0])
        self.play(FadeIn(rs), run_time=0.6)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B03_ManyWorkers(Scene):
    def construct(self):
        g1 = pixel_grid(12, 6, 0.42, x=2.8, y=1.5)
        g2 = pixel_grid(12, 6, 0.42, x=2.8, y=-1.7)
        l1a = T("CPU", 38).move_to([-3.4, 2.15, 0])
        l1b = T("one job after another", 34).move_to([-3.4, 1.55, 0])
        l2a = T("GPU", 38).move_to([-3.4, -1.05, 0])
        l2b = T("the same job at once", 34).move_to([-3.4, -1.65, 0])
        cnt = T("0 / 72", 34).move_to([-3.4, 0.85, 0])
        worker = sprite_icon(*cell_center(g1, 0, 0)[:2], r=0.17)
        self.wait(0.2)
        self.play(FadeIn(g1), FadeIn(l1a), FadeIn(l1b), FadeIn(cnt), FadeIn(worker), run_time=0.8)
        until(self, "The C P U")
        tgt = _TARGET.get("B03", 12.0)
        t_s = _elapsed(self)
        rate = max(0.05, (tgt - 0.9 - t_s) / 72.0)
        st = dict(acc=0.0, k=0, cnt=cnt)

        def tick(m, dt):
            st["acc"] += dt
            k = min(72, int(st["acc"] / rate))
            if k != st["k"]:
                for i in range(st["k"], k):
                    c = g1.cells[i // 12][i % 12]
                    c.set_fill(TEAL, opacity=0.9).set_stroke(TEAL, width=2)
                st["k"] = k
                new = T(f"{k} / 72", 34).move_to([-3.4, 0.85, 0])
                st["cnt"].become(new)
                p = cell_center(g1, min(k, 71) % 12, min(k, 71) // 12)
                m.move_to([p[0], p[1], 0])
        worker.add_updater(tick)
        until(self, "The G P U is a crowd")
        self.play(FadeIn(g2), FadeIn(l2a), FadeIn(l2b), run_time=0.5)
        crowd = VGroup(*[Dot(s.get_center(), radius=0.08, color=INK) for row in g2.cells for s in row])
        self.play(FadeIn(crowd), run_time=0.5)
        self.play(*[tint(s, TEAL, 0.9) for row in g2.cells for s in row], run_time=0.5)
        self.wait(max(0.1, tgt - 0.75 - _elapsed(self)))
        worker.clear_updaters()
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B05_FrameBudget(Scene):
    def construct(self):
        x0 = -5.5
        sc = 11.0 / 60.0
        ya = -0.5
        axis = Line([x0, ya, 0], [x0 + 11.0, ya, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([x0 + v * sc, ya, 0], [x0 + v * sc, ya - 0.18, 0], color=INK, stroke_width=4) for v in (0, 20, 40, 60)])
        labs = VGroup(*[T(s, 32).move_to([x0 + v * sc, ya - 0.5, 0]) for s, v in (("0", 0), ("20", 20), ("40", 40), ("60 ms", 60))])
        labs[3].shift([-0.3, 0, 0])
        self.wait(0.3)
        self.play(Create(axis), FadeIn(ticks), FadeIn(labs), run_time=0.8)
        until(self, "On this Mac")
        tiles = VGroup(*[Rectangle(width=sc * 0.8, height=0.6, fill_color=(TEAL if i + 0.5 < 16.7 else GOLD), fill_opacity=1, stroke_width=0)
                         .move_to([x0 + (i + 0.5) * sc, 0.1, 0]) for i in range(55)])
        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.12), run_time=2.6)
        bl = T("the loop · about 55 ms", 34).move_to([2.6, 1.0, 0])
        self.play(FadeIn(bl), run_time=0.4)
        until(self, "sixteen and a half")
        xb = x0 + 16.7 * sc
        line = DashedLine([xb, -0.85, 0], [xb, 1.75, 0], color=INK, stroke_width=5, dash_length=0.18)
        bt = T("one frame at 60 per second", 34).move_to([xb + 0.4, 2.25, 0])
        self.play(Create(line), FadeIn(bt), run_time=0.8)
        until(self, "This is one gradient")
        cr = T("Apple M4 Pro · Godot 4.7.2 · five runs: 52 to 58 ms", 32, DIM).move_to([0, -2.6, 0])
        self.play(FadeIn(cr), run_time=0.6)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B07_HandOver(Scene):
    def construct(self):
        L, R, lt, rt = a1_pair(y=0.25, w=3.6, h=3.0, x=4.4, size=34)
        lt.move_to([-4.4, 1.25, 0]); rt.move_to([4.4, 1.25, 0])
        speck = Dot([-4.4, 0.25, 0], radius=0.06, color=INK)
        ar = arrow([-2.5, 0.25, 0], [2.5, 0.25, 0])
        h1 = T("hands over the job", 34).move_to([0, 1.2, 0])
        h2 = T("about 0.04 ms", 34).move_to([0, 0.72, 0])
        gg = pixel_grid(8, 4, 0.32, x=4.4, y=0.2)
        self.wait(0.3)
        self.play(Create(L), Create(R), FadeIn(lt), FadeIn(rt), GrowArrow(ar), run_time=0.9)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.5)
        until(self, "cost the processor")
        self.play(FadeIn(speck), run_time=0.3)
        until(self, "only to hand over")
        pkg = RoundedRectangle(width=0.5, height=0.38, corner_radius=0.08, stroke_color=DIM, stroke_width=4, fill_color=CARD, fill_opacity=1).move_to([-4.4, 0.25, 0])
        self.add(pkg)
        self.play(pkg.animate.move_to([2.5, 0.25, 0]), run_time=1.3)
        self.play(FadeOut(pkg), FadeIn(gg), run_time=0.4)
        until(self, "The graphics card did the pixels")
        self.play(*[tint(s, _rgb(c / 7.0), 1.0) for row in gg.cells for c, s in enumerate(row)], run_time=0.8)
        until(self, "Its own time")
        note = T("its own time: not readable on this setup", 32, DIM).move_to([1.6, -1.95, 0])
        cr = T("Apple M4 Pro · Godot 4.7.2", 32, DIM).move_to([1.6, -2.7, 0])
        self.play(FadeIn(note), FadeIn(cr), run_time=0.6)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B08_OnePixelThenAll(Scene):
    def construct(self):
        g = pixel_grid(16, 9, 0.42, x=-2.6, y=0.45)
        cc, rr = 13, 3
        cell = g.cells[rr][cc]
        rg = ring(cell, pad=0.05, sw=6)
        card = code_card("COLOR = …", x=4.5, y=cell.get_center()[1], size=34)
        cw = card.W
        con = arrow([4.5 - cw / 2, cell.get_center()[1], 0], [cell.get_center()[0] + 0.33, cell.get_center()[1], 0], color=DIM, w=5)
        lab_a = T("one pixel's rule", 34)
        lab_b = T("every pixel", 34)
        ab = arrow([0, 0, 0], [0.9, 0, 0], w=5)
        row = VGroup(lab_a, ab, lab_b).arrange(RIGHT, buff=0.3).move_to([-2.6, -2.35, 0])
        self.wait(0.3)
        self.play(FadeIn(g), run_time=0.8)
        until(self, "write down what one pixel")
        self.play(Create(rg), FadeIn(card), GrowArrow(con), run_time=0.9)
        self.play(FadeIn(row), run_time=0.5)
        until(self, "let the card do it everywhere", lead=0.9)
        self.play(*[tint(g.cells[r][c], _rgb(c / 15.0), 1.0) for r in range(9) for c in range(16)], run_time=1.0)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Setting Up a Shader (Manim beats B09, B12). Cast: the node, ShaderMaterial and shader boxes (outlined)."""


def a2_cube(cx, cy, k=0.8):
    """A small isometric cube (three faces, light to mid teal, no near-black fills)."""
    P = lambda x, y: np.array([cx + x * k, cy + y * k, 0.0])
    top = Polygon(P(0, 1), P(0.87, 0.5), P(0, 0), P(-0.87, 0.5), fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4)
    lf = Polygon(P(-0.87, 0.5), P(0, 0), P(0, -1), P(-0.87, -0.5), fill_color=TEAL, fill_opacity=1, stroke_color=INK, stroke_width=4)
    rt = Polygon(P(0, 0), P(0.87, 0.5), P(0.87, -0.5), P(0, -1), fill_color="#7FB8A8", fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(top, lf, rt)


# ───────────────────────────────────────────────────────────────────────────
class B09_ThreeBoxes(Scene):
    def construct(self):
        title = T("Setting Up  a  Shader", 40)
        title.move_to([-6.2 + title.width / 2, 3.0, 0])
        y = -0.1
        b1 = box(-4.4, y, 3.5, 2.6); b2 = box(0, y, 3.5, 2.6); b3 = box(4.4, y, 3.5, 2.6)
        t1 = VGroup(T("a node", 36).move_to([-4.4, y + 0.8, 0]), T("Sprite2D", 32).move_to([-4.4, y + 0.15, 0]), T("ColorRect…", 32).move_to([-4.4, y - 0.4, 0]))
        t2 = T("ShaderMaterial", 36).move_to([0, y, 0])
        t3 = VGroup(T("your shader", 36).move_to([4.4, y + 0.6, 0]), T(".gdshader file", 32).move_to([4.4, y - 0.1, 0]))
        a12 = arrow([-2.6, y, 0], [-1.85, y, 0], w=5)
        a23 = arrow([1.85, y, 0], [2.6, y, 0], w=5)
        self.wait(0.3)
        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(b1, shift=RIGHT * 0.5), FadeIn(t1, shift=RIGHT * 0.5), run_time=0.6)
        until(self, "You attach")
        self.play(FadeIn(b2, shift=RIGHT * 0.5), FadeIn(t2, shift=RIGHT * 0.5), GrowArrow(a12), run_time=0.6)
        until(self, "through a material")
        self.play(FadeIn(b3, shift=RIGHT * 0.5), FadeIn(t3, shift=RIGHT * 0.5), GrowArrow(a23), run_time=0.6)
        until(self, "and the Shader Material holds", lead=0.5)
        p0 = np.array([4.4, y + 1.3, 0.0]); p1 = np.array([-4.4, y + 1.3, 0.0])
        path = VMobject()
        path.set_points([p0, p0 + np.array([-1.5, 1.4, 0]), p1 + np.array([1.5, 1.4, 0]), p1])
        dashed = DashedVMobject(path, num_dashes=24).set_stroke(DIM, width=4)
        dot = Dot(p0, radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.add(dashed)
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=1.6, rate_func=smooth)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B12_TwoWorlds(Scene):
    def construct(self):
        lead = T("the first line", 36, DIM).move_to([0, 3.0, 0])
        l1 = M("shader_type canvas_item;", 32)
        l2 = M("shader_type spatial;", 32)
        print("[width] canvas", l1.width, "spatial", l2.width)
        l1.move_to([-5.9 + l1.width / 2 + 0.0, 2.0, 0])
        l2.move_to([6.2 - l2.width / 2, 2.0, 0])
        spr = sprite_icon(-3.1, 0.2, 0.8)
        cube = a2_cube(3.6, 0.2, 0.95)
        d2 = T("2D", 36).move_to([-3.1, -1.0, 0])
        d3 = T("3D", 36).move_to([3.6, -1.0, 0])
        self.wait(0.3)
        self.play(FadeIn(lead), run_time=0.5)
        until(self, "Canvas item is")
        self.play(AddTextLetterByLetter(l1, time_per_char=0.05), FadeIn(spr), run_time=1.4)
        self.play(FadeIn(d2), run_time=0.3)
        until(self, "Spatial is")
        self.play(AddTextLetterByLetter(l2, time_per_char=0.05), FadeIn(cube), run_time=1.2)
        self.play(FadeIn(d3), run_time=0.3)
        until(self, "Particles, sky")
        names = ["particles", "sky", "fog"]
        xs = [-3.4, 0.0, 3.4]
        tiles = VGroup()
        icons = VGroup()
        for n, x in zip(names, xs):
            tiles.add(box(x, -2.4, 3.0, 1.5, color=DIM, sw=4), T(n, 34).move_to([x, -2.75, 0]))
        icons.add(VGroup(*[Dot([-3.4 + dx, -1.95 + dy, 0], radius=0.07, color=TEAL) for dx, dy in ((-0.4, 0.05), (-0.1, 0.15), (0.2, -0.05), (0.45, 0.1), (0.05, -0.12))]))
        icons.add(VGroup(Arc(radius=0.5, start_angle=0, angle=PI, stroke_color=INK, stroke_width=4).move_to([0, -2.0, 0]),
                         Circle(radius=0.14, stroke_color=GOLD, stroke_width=5).move_to([0, -1.95, 0])))
        icons.add(VGroup(*[Line([3.4 - 0.55 + 0.1 * i, -1.85 - 0.14 * i, 0], [3.4 + 0.55 - 0.1 * i, -1.85 - 0.14 * i, 0], color=DIM, stroke_width=5) for i in range(3)]))
        self.play(FadeIn(tiles), FadeIn(icons), run_time=0.8)
        until(self, "This film uses canvas item")
        rg = ring(l1, pad=0.14, sw=6)
        self.play(Create(rg), run_time=0.7)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · The Three Functions  (B15, B17, B18, B19, B22, B23: Manim; B16/B20/B21 are captures, B24 a table)

Cast for the act: the test rectangle with four terracotta corner dots (B15, B18), the pixel grid of outline cells (B18), the leaning square's
left edge (B17, five REAL measured shifts from evidence/planning-checks/lean-edge.txt), a teal fragment token (B19, B22).
Drawings are drawings: B18's grid is not to scale, B17's edge is drawn from measured numbers.
"""


def a3_row(items, y, gap=0.3, cx=0.0):
    """Centre a row of mobjects horizontally at cx with explicit gaps (no Pango spacing involved)."""
    total = sum(m.width for m in items) + gap * (len(items) - 1)
    x = cx - total / 2.0
    for m in items:
        m.move_to([x + m.width / 2.0, y, 0])
        x += m.width + gap
    return VGroup(*items)


# ═════════════════════════════ B15 · vertex runs once per corner ═════════════════════════════
class B15_FourCorners(Scene):
    def construct(self):
        title = T("The Three Functions", 40).to_corner(UL, buff=0.95)
        q = vertex_quad(4.6, 2.5, 0.0, 0.1)
        lab = M("vertex() runs", 32)
        num = T("1", 56)
        row = a3_row([lab, num], -1.75, gap=0.55)
        cap = T("its job: place the corners", 36).move_to([0, -2.75, 0])
        self.add(title)
        self.play(Create(q.body), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in q.corners], lag_ratio=0.2), run_time=0.9)
        until(self, "once for each vertex")
        self.play(FadeIn(lab), run_time=0.3)
        for i, c in enumerate(q.corners):
            new = T(str(i + 1), 56).move_to(num.get_center()) if i else num
            if i == 0:
                self.play(FadeIn(num), Indicate(c, scale_factor=2.0, color=TERRA), run_time=0.6)
            else:
                self.play(Indicate(c, scale_factor=2.0, color=TERRA), Transform(num, new), run_time=0.6)
            self.wait(0.15)
        until(self, "Its job")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        done(self)


# ═════════════════════════════ B17 · even steps down the edge (five real measurements) ═════════════════════════════
class B17_EvenSteps(Scene):
    def construct(self):
        # measured (lean-edge.txt, white-square render, left edge x at rows 0.02/0.25/0.50/0.75/0.98; first row 256):
        # x = 257, 268, 281, 293, 305  ->  shifts +1, +12, +25, +37, +49 px (rounded to whole pixels, as measured)
        meas = [(0.02, 257), (0.25, 268), (0.50, 281), (0.75, 293), (0.98, 305)]
        shifts = [x - 256 for _, x in meas]
        assert shifts == [1, 12, 25, 37, 49]
        H = 4.0                                    # 128 rows drawn 4.0 units tall (31.25 rows per unit)
        k = H / 128.0                              # units per pixel, same scale both ways
        top = np.array([-1.7, 1.95, 0.0])
        bot = top + np.array([50 * k, -H, 0.0])
        guide = DashedLine(top, top + np.array([0, -H, 0]), color=DIM, stroke_width=4, dash_length=0.18)
        edge = Line(top, bot, color=INK, stroke_width=7)
        ttl = T("left edge", 36).move_to([top[0] + 0.1, top[1] + 0.5, 0])
        gl = T("not leaned", 32, DIM).move_to([top[0] - 1.1, top[1] - 0.4, 0])
        self.add(ttl)
        until(self, "Between the corners", lead=0.0)
        self.play(Create(guide), run_time=0.6)
        self.play(Create(edge), FadeIn(gl), run_time=0.9)
        until(self, "The left edge slides evenly")
        dots, labs = [], []
        for (f, _), s in zip(meas, shifts):
            p = top + (bot - top) * f
            d = Dot(p, radius=0.16, color=TERRA).set_stroke(DIM, width=3)
            lb = M("+%d px" % s, 32).move_to([p[0] + 1.75, p[1], 0])
            ln = Line(p + np.array([0.28, 0, 0]), p + np.array([0.62, 0, 0]), color=DIM, stroke_width=4)
            dots.append(d); labs.append(lb)
            self.play(FadeIn(d, scale=0.4), Create(ln), FadeIn(lb, shift=LEFT * 0.2), run_time=0.7)
            self.wait(0.1)
        cap = a3_row([T("four corners", 36), arrow([0, 0, 0], [0.9, 0, 0]), T("straight edges", 36)], -2.9, gap=0.3, cx=0.0)
        until(self, "Four corners can only")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        done(self)


# ═════════════════════════════ B18 · fragment runs once per covered pixel ═════════════════════════════
class B18_FillIn(Scene):
    def construct(self):
        cell = 0.55
        g = pixel_grid(14, 6, cell, 0.0, 0.1, color=DIM, sw=2)
        q = vertex_quad(4.4, 2.2, 0.0, 0.1)
        tag = M("fragment()", 32)
        tag.move_to([0, 2.95, 0])
        lab = T("every covered pixel", 36).move_to([0, -2.55, 0])
        self.add(g)
        self.play(Create(q.body), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in q.corners], lag_ratio=0.15), run_time=0.6)
        # covered cells in reading order
        xs = [p[0] for p in q.pts]; ys = [p[1] for p in q.pts]
        cov = []
        for r in range(g.rows):
            for c in range(g.cols):
                p = g.cells[r][c].get_center()
                if min(xs) <= p[0] <= max(xs) and min(ys) <= p[1] <= max(ys):
                    cov.append((r, c))
        first = [rc for rc in cov if rc[0] == cov[0][0]]
        rest = [rc for rc in cov if rc[0] != cov[0][0]]
        until(self, "It runs once for each pixel")
        pc = g.cells[first[0][0]][first[0][1]].get_center()
        tag.move_to([pc[0], 2.95, 0])
        ptr = Line([pc[0], 2.62, 0], [pc[0], pc[1] + cell * 0.5, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(tag), Create(ptr), run_time=0.35)
        for (r, c) in first:
            pc = g.cells[r][c].get_center()
            nptr = Line([pc[0], 2.62, 0], [pc[0], pc[1] + cell * 0.5, 0], color=DIM, stroke_width=4)
            self.play(tag.animate.move_to([pc[0], 2.95, 0]), Transform(ptr, nptr), tint(g.cells[r][c], TEAL, 0.9), run_time=0.26, rate_func=linear)
        self.play(LaggedStart(*[tint(g.cells[r][c], TEAL, 0.9) for (r, c) in rest], lag_ratio=0.08), run_time=1.5)
        until(self, "The shape is already decided")
        self.play(FadeIn(lab, shift=UP * 0.15), run_time=0.5)
        done(self)


# ═════════════════════════════ B19 · two names, one job ═════════════════════════════
class B19_TwoNames(Scene):
    def construct(self):
        bx = box(2.9, 1.75, 3.6, 1.3, DIM, 5, fill=PALEBOX)
        same = T("same job", 36).move_to(bx.get_center())
        l1 = T("pixel shader", 36)
        l2 = T("fragment shader", 36)
        l1.move_to([-3.9, 2.4, 0]); l2.move_to([-3.9, 1.1, 0])
        a1 = arrow([-2.2, 2.4, 0], [1.0, 1.95, 0], DIM, 5)
        a2 = arrow([-2.2, 1.1, 0], [1.0, 1.55, 0], DIM, 5)
        self.add(bx, same)
        self.play(FadeIn(l1, shift=RIGHT * 0.9), FadeIn(l2, shift=RIGHT * 0.9), run_time=0.8)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.7)
        # the strip: fragment -> tests, blending -> pixel
        y = -0.95
        bs = [box(-4.2, y, 2.5, 1.0, DIM, 4, fill=PALEBOX), box(0.0, y, 3.9, 1.0, DIM, 4, fill=PALEBOX), box(4.3, y, 1.9, 1.0, DIM, 4, fill=PALEBOX)]
        ts = [T("fragment", 36).move_to([-4.2, y, 0]), T("tests, blending", 36).move_to([0.0, y, 0]), T("pixel", 36).move_to([4.3, y, 0])]
        ar = [arrow([-2.8, y, 0], [-2.2, y, 0], INK, 5, 0.2), arrow([2.1, y, 0], [2.75, y, 0], INK, 5, 0.2)]
        until(self, "Microsoft")
        self.play(*[Create(b) for b in bs], *[FadeIn(t) for t in ts], run_time=0.8)
        self.play(*[GrowArrow(a) for a in ar], run_time=0.5)
        cap = T("a fragment is a pixel-to-be", 36).move_to([0, -2.7, 0])
        tok = Circle(radius=0.22, stroke_color=TEAL, stroke_width=6).move_to([-4.2, -0.05, 0])
        until(self, "The careful word")
        self.play(FadeIn(tok, scale=0.4), run_time=0.4)
        until(self, "because a fragment", lead=1.2)
        self.play(tok.animate.move_to([0.0, -0.05, 0]), run_time=0.9)
        self.play(tok.animate.move_to([4.3, -0.05, 0]), run_time=0.9)
        self.play(tok.animate.set_fill(TEAL, opacity=1), FadeIn(cap, shift=UP * 0.15), run_time=0.6)
        done(self)


# ═════════════════════════════ B22 · the fixed order ═════════════════════════════
def a3_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B22_Order(Scene):
    def construct(self):
        xs = [-4.35, 0.0, 4.35]
        y = 0.9
        bxs = [box(x, y, 3.4, 1.9, DIM, 5, fill=PALEBOX) for x in xs]
        top = [M("vertex()", 32), T("the GPU", 36), M("fragment()", 32)]
        bot = [T("places corners", 36), T("fills the shape", 36), T("colors pixels", 36)]
        grp = []
        for x, t, b in zip(xs, top, bot):
            t.move_to([x, y + 0.38, 0]); b.move_to([x, y - 0.4, 0])
            grp.append(VGroup(t, b))
        ar = [arrow([-2.55, y, 0], [-1.8, y, 0], INK, 6, 0.24), arrow([1.8, y, 0], [2.55, y, 0], INK, 6, 0.24)]
        track = Line([-4.35, -1.1, 0], [4.35, -1.1, 0], color=GHOST, stroke_width=6)
        tok = sprite_icon(-4.35, -1.1, 0.34)
        self.add(track)
        until(self, "order of work", lead=0.0)
        self.play(*[Create(b) for b in bxs], *[FadeIn(g) for g in grp], run_time=0.8)
        self.play(*[GrowArrow(a) for a in ar], FadeIn(tok), run_time=0.6)
        until(self, "First vertex")
        r1 = a3_ubar(bxs[0], pad=0.1)
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "Then the card")
        r2 = a3_ubar(bxs[1], pad=0.1)
        self.play(tok.animate.move_to([0.0, -1.1, 0]), FadeOut(r1), FadeIn(r2), run_time=0.9)
        until(self, "Then fragment")
        r3 = a3_ubar(bxs[2], pad=0.1)
        self.play(tok.animate.move_to([4.35, -1.1, 0]), FadeOut(r2), FadeIn(r3), run_time=0.9)
        # never back: a grey backward arrow with a prohibition mark
        back = arrow([3.2, -2.25, 0], [-0.6, -2.25, 0], DIM, 6, 0.24)
        no = a1_no_mark(-1.35, -2.25)
        fwd = T("forward only", 36).move_to([2.1, -2.95, 0])
        until(self, "Information flows")
        self.play(GrowArrow(back), FadeIn(no), FadeIn(fwd), run_time=0.6)
        done(self)


def a1_no_mark(x, y, r=0.3, sw=6):
    """A prohibition mark in grey: ring + bar (series idiom), sits beside an arrow."""
    rg = Circle(radius=r, stroke_color=DIM, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=DIM, stroke_width=sw)
    return VGroup(rg, bar)


# ═════════════════════════════ B23 · built-ins in, color out ═════════════════════════════
class B23_FunctionBox(Scene):
    def construct(self):
        y0 = 0.35
        fb = box(0.0, y0, 3.6, 2.4, INK, 5)
        fl = M("fragment()", 32).move_to([0.0, y0, 0])
        ins = [("UV", 1.25), ("TIME", 0.35), ("TEXTURE", -0.55)]
        groups = []
        for name, dy in ins:
            lb = M(name, 32)
            lb.move_to([-5.8 + lb.width / 2.0, y0 + dy + 0.0, 0])
            ar = arrow([-3.0, y0 + dy, 0], [-1.95, y0 + dy, 0], INK, 6, 0.22)
            groups.append(VGroup(lb, ar))
        out_ar = arrow([1.95, y0, 0], [3.5, y0, 0], INK, 6, 0.22)
        out_lb = M("COLOR", 32)
        out_lb.move_to([3.7 + out_lb.width / 2.0, y0, 0])
        cap = a3_row([T("built-ins", 36), Dot(radius=0.07, color=INK), T("capital letters", 36)], -2.55, gap=0.3)
        self.play(Create(fb), FadeIn(fl), run_time=0.8)
        until(self, "called built-ins")
        self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
        until(self, "Some come in")
        for g in groups:
            self.play(FadeIn(g, shift=RIGHT * 0.8), run_time=0.7)
            self.wait(0.15)
        until(self, "One goes out")
        self.play(GrowArrow(out_ar), FadeIn(out_lb, shift=RIGHT * 0.3), run_time=0.7)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
class B25_OutOfReach(Scene):
    def construct(self):
        title = T("Dials: Uniforms", 40).move_to([-4.3, 2.9, 0])
        left = box(-3.6, 0, 3.6, 2.0, DIM, 4, fill=PALEBOX)
        l1 = T("your game", 32).move_to([-3.6, 0.35, 0]); l2 = M("GDScript", 32).move_to([-3.6, -0.3, 0])
        right = box(4.2, 0, 3.4, 2.0, DIM, 4, fill=PALEBOX)
        r1 = T("the shader", 32).move_to([4.2, 0.35, 0]); r2 = T("GPU", 32).move_to([4.2, -0.3, 0])
        glass = Rectangle(width=0.32, height=3.6, stroke_color=TEAL, stroke_width=5).set_fill(TEAL, opacity=0.22).move_to([1.0, 0, 0])
        sh1 = Line([0.93, 1.2, 0], [1.07, 0.5, 0], color=CARD, stroke_width=4)
        sh2 = Line([0.93, -0.2, 0], [1.07, -0.9, 0], color=CARD, stroke_width=4)
        self.play(FadeIn(title), FadeIn(VGroup(left, l1, l2, right, r1, r2)), run_time=0.8)
        self.play(Create(glass), Create(sh1), Create(sh2), run_time=0.6)
        until(self, "Your game needs", lead=0.9)
        dot = Dot([-1.95, 0, 0], radius=0.22, color=TERRA).set_stroke(DIM, width=4)
        self.play(FadeIn(dot, scale=0.5), run_time=0.3)
        self.play(dot.animate.move_to([0.6, 0, 0]), run_time=0.9, rate_func=linear)
        self.play(dot.animate.move_to([0.0, 0.0, 0]), run_time=0.3)
        self.play(dot.animate.move_to([0.6, 0, 0]), run_time=0.15)
        q = T("?", 40).move_to([0.55, 1.35, 0])
        self.play(FadeIn(q), run_time=0.3)
        until(self, "How do you talk")
        for i in range(1):
            self.play(dot.animate.move_to([-0.9, 0.0, 0]), run_time=0.5)
            self.play(dot.animate.move_to([0.6, 0, 0]), run_time=0.35, rate_func=linear)
            self.play(dot.animate.move_to([0.1, 0, 0]), run_time=0.15)
            self.play(dot.animate.move_to([0.6, 0, 0]), run_time=0.15)
        done(self)


class B30_NoClamp(Scene):
    def construct(self):
        x0, x1, y = -5.0, 0.0, 0.5
        track = Line([x0, y, 0], [x1, y, 0], color=DIM, stroke_width=10)
        e0 = Line([x0, y - 0.3, 0], [x0, y + 0.3, 0], color=INK, stroke_width=6)
        e1 = Line([x1, y - 0.45, 0], [x1, y + 0.45, 0], color=INK, stroke_width=8)
        t0 = T("0", 32).move_to([x0, y - 0.7, 0]); t1 = T("1", 32).move_to([x1, y - 0.7, 0])
        knob = Circle(radius=0.3, stroke_color=INK, stroke_width=5).set_fill(CARD, opacity=1).move_to([-2.5, y, 0])
        cap = T("slider: editor only", 32).move_to([-2.5, 1.6, 0])
        self.play(Create(track), Create(e0), Create(e1), FadeIn(VGroup(t0, t1)), FadeIn(knob), run_time=0.9)
        self.play(FadeIn(cap), run_time=0.4)
        until(self, "If your game code")
        card = code_card('mat.set_shader_parameter("red", 7.0)', x=-1.0, y=-1.9, size=32)
        self.play(FadeIn(card), run_time=0.5)
        until(self, "the shader receives")
        arr = arrow([-2.2, y + 0.0, 0], [3.2, y, 0], color=INK, w=7, tip=0.3)
        lab = T("stored: 7.0", 32).move_to([4.7, y, 0])
        spark = Dot([3.2, y, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3)
        self.play(GrowArrow(arr), knob.animate.move_to([x1, y, 0]), run_time=0.9, rate_func=linear)
        self.play(FadeIn(lab), FadeIn(spark, scale=0.4), run_time=0.4)
        until(self, "enforce it in your code")
        self.play(Indicate(e1, color=INK, scale_factor=1.2), run_time=0.7)
        self.play(Indicate(lab, color=INK, scale_factor=1.1), run_time=0.7)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
def a5_dial(x, y, r=0.36):
    c = Circle(radius=r, stroke_color=DIM, stroke_width=6).move_to([x, y, 0])
    p = Line([x, y, 0], [x + 0.26, y + 0.2, 0], color=INK, stroke_width=6)
    return VGroup(c, p)


def a5_cells(cx, cy, pitch=1.35, side=1.0, cols=3, rows=2):
    cells = []
    for r in range(rows):
        for c in range(cols):
            cells.append(Square(side_length=side, stroke_color=DIM, stroke_width=3).move_to([cx + (c - (cols - 1) / 2) * pitch, cy + ((rows - 1) / 2 - r) * pitch, 0]))
    return cells


class B34_SameForAll(Scene):
    def construct(self):
        title = T("Where Am I, and When?", 40).move_to([-3.4, 2.95, 0])
        pitch = 1.35
        lc = a5_cells(-3.3, -0.55, pitch); rc = a5_cells(3.3, -0.55, pitch)
        gl = VGroup(*lc); gr = VGroup(*rc)
        dial = a5_dial(-3.3, 1.95)
        dl = T("uniform", 32).move_to([-1.3, 1.95, 0])
        al = T("address (u, v)", 32).move_to([3.3, 1.95, 0])
        rail_y = 1.05
        lane = [-3.3 + (c - 1) * pitch - 0.7 for c in range(3)]
        wires = [Line([-3.3, 1.59, 0], [-3.3, rail_y, 0], color=DIM, stroke_width=4), Line([lane[0], rail_y, 0], [lane[2], rail_y, 0], color=DIM, stroke_width=4)]
        ends = []
        for c in range(3):
            ybot = lc[3 + c].get_center()[1]
            wires.append(Line([lane[c], rail_y, 0], [lane[c], ybot, 0], color=DIM, stroke_width=4))
            for r in range(2):
                cell = lc[r * 3 + c]
                y = cell.get_center()[1]
                wires.append(Line([lane[c], y, 0], [cell.get_center()[0] - 0.5, y, 0], color=DIM, stroke_width=4))
                ends.append(Dot([cell.get_center()[0] - 0.5, y, 0], radius=0.07, color=DIM))
        fan = VGroup(*wires, *ends)
        nums = VGroup(*[T("0.5", 32).move_to(cl.get_center()) for cl in lc])
        us = ["0.17", "0.50", "0.83"]; vs = ["0.25", "0.75"]
        pairs = VGroup(*[VGroup(T(us[c], 32), T(vs[r], 32)).arrange(DOWN, buff=0.06).move_to(rc[r * 3 + c].get_center()) for r in range(2) for c in range(3)])
        cap1 = T("same everywhere", 32).move_to([-3.3, -2.8, 0])
        cap2 = T("different for each", 32).move_to([3.3, -2.8, 0])
        self.play(FadeIn(title), FadeIn(gl), run_time=0.6)
        self.play(FadeIn(dial), FadeIn(dl), run_time=0.4)
        until(self, "A uniform is one value")
        self.play(LaggedStart(*[Create(w) for w in wires], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(VGroup(*ends)), FadeIn(nums), FadeIn(cap1), run_time=0.5)
        until(self, "Some inputs must differ")
        self.play(FadeIn(gr), FadeIn(al), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.1), FadeIn(cap2), run_time=0.9)
        until(self, "The engine hands")
        for k in (0, 4, 2):
            self.play(Indicate(rc[k], color=TEAL, scale_factor=1.12), run_time=0.5)
        done(self)


class B36_Address(Scene):
    def construct(self):
        S0 = 3.4
        sq = uv_square(S0, x=-0.4, y=-0.35)
        x0, y0 = -0.4 - S0 / 2, -0.35 + S0 / 2
        un = T("u", 32).move_to([x0 + S0 + 0.45, y0 + 0.5, 0]); vn = T("v", 32).move_to([x0 - 0.5, y0 - S0 - 0.45, 0])
        c00 = T("(0, 0)", 32).move_to([x0 + 0.75, y0 - 0.4, 0])
        c11 = T("(1, 1)", 32).move_to([x0 + S0 - 0.2, y0 - S0 - 0.45, 0])
        self.play(Create(sq.frame), run_time=0.6)
        self.play(FadeIn(VGroup(*sq.submobjects[1:])), FadeIn(VGroup(un, vn, c00, c11)), run_time=0.7)
        pos = {"u": 0.5, "v": 0.15}
        dot = Dot(sq.pt(0.5, 0.15), radius=0.2, color=TERRA).set_stroke(DIM, width=4)

        def lab():
            u, v = dot.get_center()[0], dot.get_center()[1]
            uu = (u - x0) / S0; vv = (y0 - v) / S0
            t = T(f"({uu:.2f}, {vv:.2f})", 32)
            if uu > 0.6:
                t.move_to(dot.get_center() + np.array([-1.35, 0.55, 0]))
            else:
                t.move_to(dot.get_center() + np.array([1.4, 0.45, 0]))
            return t
        label = always_redraw(lab)
        until(self, "U V runs")
        self.play(FadeIn(dot, scale=0.5), run_time=0.3)
        self.add(label)
        self.play(dot.animate.move_to(sq.pt(0.25, 0.75)), run_time=1.0)
        until(self, "The bottom right")
        self.play(dot.animate.move_to(sq.pt(1.0, 1.0)), run_time=1.0)
        until(self, "the second number counts")
        self.play(dot.animate.move_to(sq.pt(1.0, 0.45)), run_time=0.7)
        self.play(dot.animate.move_to(sq.pt(1.0, 1.0)), run_time=0.9)
        done(self)


class B41_ClockVsDial(Scene):
    def construct(self):
        xa, xb, yc = -5.5, 5.5, 1.2
        n = 44; tw = (xb - xa) / n
        clock = VGroup(*[Rectangle(width=tw * 0.8, height=0.26, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([xa + tw * (i + 0.5), yc, 0]) for i in range(n)])
        cl = T("game clock", 32).move_to([-4.3, yc + 0.6, 0])
        nr = T("never restarts", 32).move_to([4.2, yc + 0.6, 0])
        c0 = T("0", 32).move_to([xa, yc - 0.55, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in clock], lag_ratio=0.02), FadeIn(cl), FadeIn(c0), run_time=1.1)
        play_x = {"x": xa}
        head = Dot([xa, yc, 0], radius=0.15, color=INK)
        speed = 3.3 / 3.7
        self.add(head)

        def adv(m, dt):
            play_x["x"] = min(xa + 9.8, play_x["x"] + speed * dt)
            m.move_to([play_x["x"], yc, 0])
        head.add_updater(adv)
        xm = xa + 3.3
        until(self, "that starts when", lead=1.3)
        mk = Dot([xm, yc, 0], radius=0.2, color=TERRA).set_stroke(DIM, width=4)
        ml = T("something happens", 32).move_to([xm + 0.3, yc + 1.55, 0])
        drop = DashedLine([xm, yc - 0.15, 0], [xm, -0.95, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(mk, scale=0.4), FadeIn(ml), Create(drop), run_time=0.5)
        yp = -1.2; pw = 3.5; m = 28; ptw = pw / m
        prog = VGroup(*[Rectangle(width=ptw * 0.8, height=0.3, fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to([xm + ptw * (i + 0.5), yp, 0]) for i in range(m)])
        pl = T("progress", 32).move_to([-4.0, yp, 0])
        p0 = T("0", 32).move_to([xm, yp - 0.6, 0]); p1 = T("1", 32).move_to([xm + pw, yp - 0.6, 0])
        until(self, "something happens,", lead=0.0)
        self.play(FadeIn(pl), FadeIn(p0), FadeIn(p1), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(t) for t in prog], lag_ratio=0.05), run_time=1.1)
        until(self, "let your game drive")
        dl = T("you drive it", 32).move_to([xm + pw / 2, yp - 1.25, 0])
        self.play(FadeIn(dl), FadeIn(nr), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
