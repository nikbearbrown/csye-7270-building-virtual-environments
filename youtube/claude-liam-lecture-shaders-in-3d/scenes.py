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
"""ACT I · Same Shape, New Names  (B02 B03 B04 B05 B09, all Manim; the kit is pasted above this file by assemble_scenes.py)

Cast for the act: the skeleton code card (lab-shaders/03-skeleton-3d.gdshader, typed in here so scenes.py stands alone), the teal flat square and its
four terracotta corner dots, the teal cube (the same teal, 0.37 0.64 0.57), the pixel grid of outline cells. Code is typed word by word at exact monospace
columns (Menlo is 0.2496 wide per character at size 32) so Pango can never fuse a space; every token sits on one shared baseline.
"""

A1_CW = 0.24962           # width of one Menlo character at size 32 (measured)
A1_LH = 0.40              # line pitch of the act's code cards
A1_TEAL_D = "#4A8A79"; A1_TEAL_L = "#86BFAE"


def a1_toks(line, left, ybase, size=32):
    """The words of one code line, each a VGroup of glyphs, on the baseline ybase; word k starts at its exact column. Returns a list of VGroups."""
    out = []
    col = 0
    for w in line.replace("\t", "  ").split(" "):
        if w:
            t = Text("H" + w + "H", font=MONO, color=INK, font_size=size)
            if len(t.submobjects) >= len(w) + 2:
                h0 = t.submobjects[0]
                t.shift([left + (col - 0.5) * A1_CW - h0.get_center()[0], ybase - h0.get_bottom()[1], 0])
                out.append(VGroup(*t.submobjects[1:-1]))
            else:                                    # (static-check stub without glyph children)
                out.append(M(w, size).move_to([left + (col + len(w) / 2.0) * A1_CW, ybase + 0.16, 0]))
        col += len(w) + 1
    return out


def a1_card(lines, xc, yc, ncols=None, lh=0.46, blank=0.22, pad_l=0.6, pad_r=0.35):
    """A white code card with the lines typed as word tokens (blank lines are thinner). Returns VGroup(frame, *tokens) with .frame, .tok (list per line of
    token VGroups), .left, .base (baselines), .cy (line centres), .W, .H."""
    ncols = ncols or max(len(l.replace("\t", "  ")) for l in lines)
    pitch = [lh if ln.strip() else blank for ln in lines]
    W = ncols * A1_CW + pad_l + pad_r
    H = sum(pitch) + 0.3
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4).set_fill(PALEBOX, opacity=1).move_to([xc, yc, 0])
    left = xc - W / 2 + pad_l
    y = yc + H / 2 - 0.15
    toks, bases, cys = [], [], []
    for i, ln in enumerate(lines):
        cy = y - pitch[i] / 2
        y -= pitch[i]
        cys.append(cy); bases.append(cy - 0.16)
        toks.append(a1_toks(ln, left, cy - 0.16))
    g = VGroup(frame, *[t for row in toks for t in row])
    g.frame = frame; g.tok = toks; g.left = left; g.base = bases; g.cy = cys; g.W = W; g.H = H
    return g


def a1_cap(s, x, y):
    return T(s, 32).move_to([x, y, 0])


def a1_bracket(x, y0, y1, color=INK):
    """A right-hand square bracket from y0 (top) down to y1, opening towards the code."""
    return VGroup(Line([x - 0.14, y0, 0], [x, y0, 0], color=color, stroke_width=6), Line([x, y0, 0], [x, y1, 0], color=color, stroke_width=6),
                  Line([x, y1, 0], [x - 0.14, y1, 0], color=color, stroke_width=6))


def a1_cube(x, y, s=1.0, faces=True):
    """An isometric cube in the series teal with faint triangle edges. s is the half-width of the hexagon."""
    cx, cy = x, y
    dx, dy = s, s * 0.5
    top = Polygon([cx, cy + s, 0], [cx + dx, cy + dy, 0], [cx, cy, 0], [cx - dx, cy + dy, 0], fill_color=A1_TEAL_L, fill_opacity=1, stroke_color=INK, stroke_width=3)
    left = Polygon([cx - dx, cy + dy, 0], [cx, cy, 0], [cx, cy - s, 0], [cx - dx, cy - dy, 0], fill_color=TEAL, fill_opacity=1, stroke_color=INK, stroke_width=3)
    right = Polygon([cx + dx, cy + dy, 0], [cx, cy, 0], [cx, cy - s, 0], [cx + dx, cy - dy, 0], fill_color=A1_TEAL_D, fill_opacity=1, stroke_color=INK, stroke_width=3)
    g = VGroup(top, left, right)
    if faces:
        g.add(Line([cx, cy + s, 0], [cx, cy, 0], color=GHOST, stroke_width=2), Line([cx - dx, cy + dy, 0], [cx, cy - s, 0], color=GHOST, stroke_width=2),
              Line([cx + dx, cy + dy, 0], [cx, cy - s, 0], color=GHOST, stroke_width=2))
    return g


def a1_lamp(x, y, color=INK):
    """A drawn bulb with rays pointing down. Returns VGroup with .bulb and .rays."""
    bulb = Circle(radius=0.2, stroke_color=color, stroke_width=4).move_to([x, y, 0])
    base = Line([x - 0.1, y - 0.28, 0], [x + 0.1, y - 0.28, 0], color=color, stroke_width=5)
    rays = VGroup(*[Line([x + 0.34 * np.cos(a), y + 0.34 * np.sin(a), 0], [x + 0.5 * np.cos(a), y + 0.5 * np.sin(a), 0], color=GOLD, stroke_width=4)
                    for a in np.radians([180, 225, 270, 315, 360])])
    g = VGroup(bulb, base, rays)
    g.bulb = bulb; g.rays = rays
    return g


# ═════════════════════════════════════════ B02 ═════════════════════════════════════════
class B02_Anatomy(Scene):
    """The skeleton file: a program counter steps down it, then three brackets say its shape: a first line, up to three functions, dials."""

    def construct(self):
        src = ["shader_type spatial;", "", "uniform float amount;", "", "void vertex() {", "}", "", "void fragment() {", "}", "", "void light() {", "}"]
        # the file has 12 lines; line 3 is the uniform (the dial), lines 5 to 12 the three functions
        card = a1_card(src, -2.5, -0.72, ncols=20, lh=0.5, blank=0.2)
        c1 = a1_cap("shader: a small program the graphics card", 0, 2.95)
        c2 = a1_cap("runs to decide how something is drawn", 0, 2.45)
        self.add(card, c1, c2)
        dot = Dot([card.frame.get_left()[0] + 0.3, card.cy[0], 0], radius=0.11, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(dot), run_time=0.4)
        for ln in (2, 4, 7, 10):                       # zero-based: uniform, vertex, fragment, light
            self.play(dot.animate.move_to([dot.get_center()[0], card.cy[ln], 0]), run_time=0.32)
            self.wait(0.22)
        self.play(FadeOut(dot), run_time=0.3)
        bx = card.frame.get_right()[0] + 0.45
        lx = bx + 0.3
        until(self, "a first line")
        b1 = a1_bracket(bx, card.cy[0] + 0.17, card.cy[0] - 0.17)
        l1 = T("type", 32).move_to([lx + 0.4, card.cy[0], 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.7)
        until(self, "up to three functions")
        b2 = a1_bracket(bx, card.cy[4] + 0.2, card.cy[11] - 0.2)
        l2 = T("functions", 32).move_to([lx + 0.75, (card.cy[4] + card.cy[11]) / 2, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.8)
        until(self, "dials")
        b3 = a1_bracket(bx, card.cy[2] + 0.17, card.cy[2] - 0.17)
        l3 = T("dials", 32).move_to([lx + 0.5, card.cy[2], 0])
        dc = np.array([bx + 2.2, card.cy[2], 0])
        dial = Circle(radius=0.38, stroke_color=INK, stroke_width=5).move_to(dc)
        tick = VGroup(Line(dc, dc + np.array([0, 0.3, 0]), color=INK, stroke_width=5), Dot(dc + np.array([0, 0.3, 0]), radius=0.1, color=TERRA).set_stroke(DIM, width=3))
        hub = Dot(dc, radius=0.06, color=INK)
        self.play(Create(b3), FadeIn(l3), Create(dial), Create(tick), FadeIn(hub), run_time=0.5)
        self.play(Rotate(tick, angle=-TAU * 0.75, about_point=dc), run_time=0.8)
        done(self)


# ═════════════════════════════════════════ B03 ═════════════════════════════════════════
class B03_TwoTypes(Scene):
    """The first line names the type: canvas_item is replaced by spatial and the flat square becomes a cube."""

    def construct(self):
        left = -2.5
        ybase = 1.45
        w_type = a1_toks("shader_type", left, ybase)[0]
        w_a = a1_toks("            canvas_item;", left, ybase)[0]
        w_b = a1_toks("            spatial;", left, ybase)[0]
        cap = a1_cap("shader type: the first line; says what the shader is for", 0, 2.75)
        sq = Square(side_length=2.1, stroke_color=INK, stroke_width=5, fill_color=TEAL, fill_opacity=1).move_to([0, -0.7, 0])
        lab2 = T("2D", 32).move_to([0, -2.45, 0])
        self.add(cap, w_type, w_a, sq, lab2)
        until(self, "Canvas item means two-D")
        self.play(Indicate(w_a, scale_factor=1.06, color=INK), run_time=0.7)
        until(self, "three-D, where the shader", lead=0.0)
        w_b.shift([0, 0.5, 0]).set_opacity(0)
        cube = a1_cube(0, -0.7, 1.15)
        lab3 = T("3D", 32).move_to([0, -2.45, 0])
        self.play(w_a.animate.shift([0, -0.5, 0]).set_opacity(0), w_b.animate.shift([0, -0.5, 0]).set_opacity(1), ReplacementTransform(sq, cube),
                  ReplacementTransform(lab2, lab3), run_time=1.1)
        until(self, "the points and triangles")
        mesh = T("mesh", 32).move_to([3.4, -0.7, 0])
        arr = arrow([2.75, -0.7, 0], [1.55, -0.7, 0])
        self.play(FadeIn(mesh), GrowArrow(arr), run_time=0.7)
        done(self)


# ═════════════════════════════════════════ B04 ═════════════════════════════════════════
class B04_ThreeFunctions(Scene):
    """Counts as motion: four corner dots flash 1 to 4, the covered cells tint one by one, two lamps brighten the cells in turn."""

    def construct(self):
        cy = 0.2
        quad = vertex_quad(3.0, 2.2, -4.0, cy)
        grid = pixel_grid(12, 8, 0.4, 3.3, cy)
        foot = vertex_quad(2.4, 1.6, 3.3, cy)
        foot_out = Rectangle(width=2.4, height=1.6, stroke_color=INK, stroke_width=5).move_to([3.3, cy, 0])
        cap1 = a1_cap("vertex: a corner point of a shape", 0, -2.55)
        cap2 = a1_cap("pixel: one dot of the picture on screen", 0, -3.05)
        qbody = quad.body.set_fill(TEAL, opacity=0.9)
        self.add(qbody, grid, foot_out, cap1, cap2)
        until(self, "Vertex runs")
        vlab = M("vertex()", 32).move_to([-4.0, -1.85, 0])
        nums = [("1", [-5.95, cy + 1.45]), ("2", [-2.05, cy + 1.45]), ("3", [-2.05, cy - 1.45]), ("4", [-5.95, cy - 1.45])]
        self.play(FadeIn(vlab), run_time=0.4)
        for d, (s, p) in zip(quad.corners, nums):
            n = T(s, 32).move_to([p[0], p[1], 0])
            self.play(FadeIn(d, scale=0.4), FadeIn(n), run_time=0.45)
            self.play(Indicate(d, scale_factor=1.7, color=TERRA), run_time=0.4)
        until(self, "pixel the mesh covers", lead=0.9)
        flab = M("fragment()", 32).move_to([2.2, -1.85, 0])
        covered = fill_in(grid, foot, TEAL)
        self.play(FadeIn(flab), run_time=0.3)
        self.play(LaggedStart(*covered, lag_ratio=0.1), run_time=1.9)
        until(self, "Light runs")
        l1 = a1_lamp(2.3, 2.75)
        l2 = a1_lamp(4.3, 2.75)
        lt = M("light()", 32).move_to([4.9, -1.85, 0])
        cells = [s for row in grid.cells for s in row if min(p[0] for p in foot.pts) <= s.get_center()[0] <= max(p[0] for p in foot.pts)
                 and min(p[1] for p in foot.pts) <= s.get_center()[1] <= max(p[1] for p in foot.pts)]
        self.play(FadeIn(l1), FadeIn(lt), run_time=0.4)
        self.play(*[c.animate.set_fill("#A9D8CB", 1) for c in cells], Indicate(l1.rays, color=GOLD), run_time=0.7)
        until(self, "for every light")
        self.play(FadeIn(l2), run_time=0.3)
        self.play(*[c.animate.set_fill("#D2EDE4", 1) for c in cells], Indicate(l2.rays, color=GOLD), run_time=0.7)
        done(self)


# ═════════════════════════════════════════ B05 ═════════════════════════════════════════
def a1_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B05_CodeMorph(Scene):
    """The 2D file and the 3D file, line for line: COLOR becomes ALBEDO, vec4 becomes vec3, the alpha number goes."""

    def construct(self):
        cw = A1_CW
        top_src = ["shader_type canvas_item;", "", "void fragment() {", "  COLOR = vec4(0.37, 0.64, 0.57, 1.0);", "}"]
        bot_src = ["shader_type spatial;", "", "void fragment() {", "  COLOR = vec4(0.37, 0.64, 0.57, 1.0);", "}"]
        top = a1_card(top_src, 0.0, 1.85, ncols=38, lh=0.5, blank=0.24, pad_r=0.6)
        bot = a1_card(bot_src, 0.0, -0.95, ncols=38, lh=0.5, blank=0.24, pad_r=0.6)
        self.add(top, bot)
        xin = bot.frame.get_right()[0] - 1.4            # empty space inside the card, right of the short lines

        def under(txt, x):
            lab = T(txt, 32).move_to([x, -2.65, 0])
            return VGroup(lab, Line([x, -2.42, 0], [x, -2.2, 0], color=DIM, stroke_width=4))
        # the first lines already differ (canvas_item above, spatial below): label 'type'
        ltype = T("type", 32).move_to([xin, bot.cy[0], 0])
        self.play(FadeIn(ltype), run_time=0.4)
        color, eq, v4, n2, n3, n4 = bot.tok[3]           # COLOR, =, vec4(0.37,, 0.64,, 0.57,, 1.0);
        until(self, "the output")
        albedo = a1_toks("  ALBEDO", bot.left, bot.base[3])[0]
        r1 = a1_ubar(color, pad=0.06)
        lout = under("output", color.get_center()[0] + 0.1)
        self.play(Create(r1), FadeIn(lout), run_time=0.4)
        rest = [eq, v4, n2, n3, n4]
        self.play(ReplacementTransform(color, albedo), r1.animate.become(a1_ubar(albedo)), *[m.animate.shift([cw, 0, 0]) for m in rest], run_time=0.8)
        self.play(FadeOut(r1), run_time=0.3)
        until(self, "four numbers")
        nums = VGroup(v4, n2, n3, n4)
        r2 = a1_ubar(nums, pad=0.05)
        lfour = under("four numbers", nums.get_center()[0])
        self.play(FadeOut(lout), run_time=0.2)
        self.play(Create(r2), FadeIn(lfour), run_time=0.5)
        until(self, "and alpha")
        cap = a1_cap("alpha: how visible a pixel is: 0 invisible, 1 solid", 0, -3.15)
        r3 = a1_ubar(n4, pad=0.05)
        self.play(Transform(r2, r3), FadeOut(lfour), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.4)
        until(self, "three numbers")
        v3 = a1_toks("vec3(0.37,", bot.left + 11 * cw, bot.base[3])[0]
        end57 = a1_toks("0.57);", bot.left + 28 * cw, bot.base[3])[0]
        l3 = under("three numbers", (v4.get_left()[0] + n3.get_right()[0]) / 2)
        self.play(FadeOut(r2), ReplacementTransform(v4, v3), ReplacementTransform(n3, end57), FadeOut(n4), FadeIn(l3), run_time=0.8)
        until(self, "Alpha becomes")
        chip = VGroup(box(0, 0, 1.7, 0.48, color=INK, sw=3, radius=0.24), T("ALPHA", 32)).move_to([xin - 0.1, bot.cy[2] + 0.1, 0])
        self.play(FadeIn(chip, shift=LEFT * 0.3), run_time=0.5)
        done(self)


# ═════════════════════════════════════════ B09 ═════════════════════════════════════════
def a1_file_icon(x, y, h=0.9):
    w = h * 0.78
    c = h * 0.28
    page = Polygon([x - w / 2, y + h / 2, 0], [x + w / 2 - c, y + h / 2, 0], [x + w / 2, y + h / 2 - c, 0], [x + w / 2, y - h / 2, 0], [x - w / 2, y - h / 2, 0],
                   stroke_color=INK, stroke_width=4, fill_color=PALEBOX, fill_opacity=1)
    fold = VGroup(Line([x + w / 2 - c, y + h / 2, 0], [x + w / 2 - c, y + h / 2 - c, 0], color=INK, stroke_width=4),
                  Line([x + w / 2 - c, y + h / 2 - c, 0], [x + w / 2, y + h / 2 - c, 0], color=INK, stroke_width=4))
    return VGroup(page, fold)


class B09_AttachChain(Scene):
    """Three boxes link left to right: mesh instance, ShaderMaterial, shader. The slot tab lands on the first link; a dot travels back to the node."""

    def construct(self):
        xs = [-4.5, 0.0, 4.5]
        bw, bh = 3.3, 2.5
        b1 = box(xs[0], 0.2, bw, bh); b2 = box(xs[1], 0.2, bw, bh); b3 = box(xs[2], 0.2, bw, bh)
        cube = a1_cube(xs[0], 0.55, 0.55)
        t1 = T("mesh instance", 32).move_to([xs[0], -0.55, 0])
        t2 = T("ShaderMaterial", 32).move_to([xs[1], 0.2, 0])
        fic = a1_file_icon(xs[2], 0.65, 0.85)
        t3 = T("shader", 32).move_to([xs[2], -0.05, 0])
        t3b = M(".gdshader", 32).move_to([xs[2], -0.6, 0])
        g1 = VGroup(b1, cube, t1); g2 = VGroup(b2, t2); g3 = VGroup(b3, fic, t3, t3b)
        cap1 = a1_cap("mesh instance: the node that draws a mesh", 0, -2.35)
        cap2 = a1_cap("ShaderMaterial: a material that holds your shader and its settings", 0, -2.9)
        self.play(FadeIn(g1, shift=RIGHT * 0.4), FadeIn(cap1), run_time=0.5)
        until(self, "a shader material")
        lk1 = arrow([xs[0] + bw / 2 + 0.05, 0.2, 0], [xs[1] - bw / 2 - 0.05, 0.2, 0])
        self.play(FadeIn(g2, shift=RIGHT * 0.5), GrowArrow(lk1), FadeIn(cap2), run_time=0.6)
        until(self, "material override")
        tab = VGroup(pill(0, 0, 3.5, 0.62), T("material override", 32)).move_to([(xs[0] + xs[1]) / 2, 2.2, 0])
        stem = Line([(xs[0] + xs[1]) / 2, 1.88, 0], [(xs[0] + xs[1]) / 2, 0.25, 0], color=DIM, stroke_width=5)
        self.play(Create(stem), FadeIn(tab, shift=DOWN * 0.3), run_time=0.5)
        until(self, "The material holds")
        lk2 = arrow([xs[1] + bw / 2 + 0.05, 0.2, 0], [xs[2] - bw / 2 - 0.05, 0.2, 0])
        self.play(FadeIn(g3, shift=RIGHT * 0.5), GrowArrow(lk2), run_time=0.5)
        dot = Dot([xs[2], -1.65, 0], radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        path = Line([xs[2], -1.65, 0], [xs[0], -1.65, 0], color=DIM, stroke_width=4)
        self.add(path)
        self.play(FadeIn(dot), run_time=0.15)
        self.play(MoveAlongPath(dot, path), run_time=0.9)
        self.play(Create(ring(b1)), run_time=0.35)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Lit or Unlit  (B13, B18; Manim)

B13 a work flow: a `fragment()` box emits a card of the five surface outputs, the card enters "Godot's lighting", two lamps feed the same box, one pixel
comes out. B18 a decision sketch: "looks wrong" splits into two questions, a dot walks each branch and lights its one-word remedy.
Everything here is a drawing (labelled by its words); no Godot output is claimed.
"""


def a2_at(self, t_abs):
    """Wait until absolute scene time t_abs (seconds)."""
    gap = t_abs - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a2_lamp(x, y):
    """A lamp icon drawn from shapes: a bulb, a neck and a cap."""
    bulb = Circle(radius=0.3, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    neck = Line([x - 0.14, y - 0.34, 0], [x + 0.14, y - 0.34, 0], color=INK, stroke_width=5)
    cap = Line([x - 0.1, y - 0.46, 0], [x + 0.1, y - 0.46, 0], color=INK, stroke_width=5)
    ray = VGroup(*[Line([x + 0.46 * np.cos(a), y + 0.46 * np.sin(a), 0], [x + 0.62 * np.cos(a), y + 0.62 * np.sin(a), 0], color=DIM, stroke_width=4)
                   for a in (np.pi * 0.25, np.pi * 0.5, np.pi * 0.75)])
    return VGroup(bulb, neck, cap, ray)


def a2_tag(text, x, y, w=None):
    t = T(text, 32)
    w = w or t.width + 0.5
    b = box(x, y, w, 0.7, color=INK, sw=3)
    t.move_to([x, y, 0])
    g = VGroup(b, t)
    g.b = b
    return g


# ═════════════════════════════ B13 · the lit pipeline ═════════════════════════════
class B13_LitPipeline(Scene):
    def construct(self):
        fbox = box(-4.7, 0.0, 2.7, 0.9, color=INK, sw=4)
        ftxt = M("fragment()", 32).move_to([-4.7, 0.0, 0])
        you = T("you describe", 32).move_to([-4.7, -0.95, 0])
        names = ["ALBEDO", "ALPHA", "EMISSION", "ROUGHNESS", "METALLIC"]
        chips = VGroup(*[M(n, 32).move_to([0, 0.95 - i * 0.48, 0]) for i, n in enumerate(names)])
        cframe = box(0, 0.0, chips.width + 0.5, 3.05, color=DIM, sw=4)
        cframe.set_fill(PALEBOX, opacity=1)
        csurf = T("surface", 32).move_to([0, 1.82, 0])
        card = VGroup(cframe, chips)
        cardall = VGroup(card, csurf)
        cardall.move_to([-1.9, 0.0, 0])
        lbox = box(1.9, 0.0, 3.5, 2.0, color=INK, sw=4)
        ltxt = T("Godot's lighting", 32).move_to([1.9, 0.0, 0])
        flow = arrow([-3.3, 0.0, 0], [0.05, 0.0, 0], color=GHOST, w=7)
        self.add(fbox, ftxt, flow)
        self.play(FadeIn(you), GrowFromCenter(cardall), run_time=0.7)
        self.play(FadeIn(lbox), FadeIn(ltxt), run_time=0.5)
        # the card enters the lighting box (done well before the midpoint)
        a2_at(self, 1.4)
        self.play(cardall.animate.scale(0.32).move_to([1.9, 0.0, 0]).set_opacity(0.0), run_time=1.4)
        ltxt.set_opacity(1)
        # every lamp feeds the same box from above
        until(self, "and every lamp")
        lamps = VGroup(a2_lamp(0.95, 2.75), a2_lamp(2.85, 2.75))
        beams = VGroup(arrow([0.95, 2.1, 0], [1.2, 1.1, 0], color=DIM, w=7, tip=0.24), arrow([2.85, 2.1, 0], [2.6, 1.1, 0], color=DIM, w=7, tip=0.24))
        self.play(FadeIn(lamps), run_time=0.5)
        self.play(*[GrowArrow(b) for b in beams], run_time=0.6)
        # one pixel comes out on the right
        a2_at(self, 5.65)
        out = arrow([3.75, 0.0, 0], [4.85, 0.0, 0], w=7)
        pix = Square(side_length=0.62, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([5.4, 0.0, 0])
        plab = T("one pixel", 32).move_to([5.4, -0.8, 0])
        self.play(GrowArrow(out), run_time=0.4)
        self.play(FadeIn(pix, scale=0.5), FadeIn(plab), run_time=0.5)
        done(self)


# ═════════════════════════════ B18 · two checks ═════════════════════════════
def a2_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B18_TwoChecks(Scene):
    def construct(self):
        top = Square(side_length=0.7, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([-1.3, 2.55, 0])
        toplab = T("looks wrong", 32).move_to([0.5, 2.55, 0])
        lx, rx = -3.7, 3.7
        # skeleton of both branches (grey), lit as the dot walks them
        bl = arrow([-1.0, 2.1, 0], [lx, 1.8, 0], color=DIM, w=5)
        br = arrow([1.0, 2.1, 0], [rx, 1.8, 0], color=DIM, w=5)
        self.add(top, toplab)
        self.play(GrowArrow(bl), GrowArrow(br), run_time=0.6)
        dot = Dot([0, 2.1, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.add(dot)
        # left: is a lamp changing my color?
        until(self, "Is a lamp")
        lamp = a2_lamp(lx, 0.95)
        q = T("?", 40).move_to([lx + 0.95, 0.95, 0])
        self.play(dot.animate.move_to([lx, 1.8, 0]), FadeIn(lamp), FadeIn(q), run_time=0.7)
        a1 = arrow([lx, 0.38, 0], [lx, -0.15, 0], color=DIM, w=5)
        sph = Circle(radius=0.62, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([lx, -0.85, 0])
        hi = Circle(radius=0.26, stroke_width=0).set_fill(CARD, opacity=0.65).move_to([lx - 0.2, -0.65, 0])
        self.play(GrowArrow(a1), dot.animate.move_to([lx, -0.15, 0]), run_time=0.5)
        self.play(FadeIn(sph), FadeIn(hi), run_time=0.4)
        until(self, "Add unshaded")
        tagl = a2_tag("add unshaded", lx, -2.5, 3.5)
        self.play(FadeOut(hi), sph.animate.set_fill(TEAL, opacity=1), dot.animate.move_to([lx, -1.8, 0]), run_time=0.6)
        self.play(FadeIn(tagl), run_time=0.4)
        rl = a2_ubar(tagl)
        self.play(FadeIn(rl), run_time=0.4)
        # right: is the back side being skipped?
        until(self, "Is the back side")
        self.play(dot.animate.move_to([rx, 1.8, 0]), run_time=0.7)
        back = Square(side_length=1.1, stroke_color=DIM, stroke_width=4).move_to([rx, 0.95, 0])
        a2 = arrow([rx, 0.3, 0], [rx, -0.2, 0], color=DIM, w=5)
        sq = Square(side_length=1.1, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([rx, -0.9, 0])
        self.play(FadeIn(back), run_time=0.4)
        self.play(GrowArrow(a2), dot.animate.move_to([rx, -0.2, 0]), run_time=0.4)
        self.play(FadeIn(sq), run_time=0.4)
        until(self, "Add cull disabled")
        tagr = a2_tag("add cull disabled", rx, -2.5, 4.6)
        self.play(dot.animate.move_to([rx, -1.8, 0]), FadeIn(tagr), run_time=0.5)
        rr = a2_ubar(tagr)
        self.play(FadeIn(rr), run_time=0.4)
        # a faint third tag
        until(self, "blend add")
        tagb = a2_tag("blend add", 0, 0.7, 2.8).set_opacity(0.45)
        cap = T("more modes in the docs", 32).move_to([0, -0.05, 0])
        self.play(FadeIn(tagb), FadeIn(cap), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · A Surface That Changes  (B20, B21, B22, B24; Manim)

One cast: the ramp strip (ghost to teal, narrow tiles with gaps), a terracotta dot with a grey ring, the sawtooth drawn from eight separate teeth.
The curves are written inline (x, fract(x * 8), step(0.5, .), mix): no file outside this one is read. Everything is a drawing of arithmetic.
"""


def a3_at(self, t_abs):
    gap = t_abs - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a3_dot(x=0.0, y=0.0, r=0.16):
    return Dot([x, y, 0], radius=r, color=TERRA).set_stroke(DIM, width=3)


class a3_Axes:
    """Scene-space mapping for a small plot at centre (x, y), size (w, h): value (u in 0..1, v in 0..1) -> scene point. No drawing of its own."""
    def __init__(self, x, y, w, h):
        self.x0, self.y0, self.w, self.h = x - w / 2, y - h / 2, w, h

    def pt(self, u, v):
        return np.array([self.x0 + u * self.w, self.y0 + v * self.h, 0])

    def frame(self):
        return VGroup(Line(self.pt(0, 0), self.pt(1, 0), color=INK, stroke_width=5), Line(self.pt(0, 0), self.pt(0, 1), color=INK, stroke_width=5))


def a3_saw_teeth(ax, n=8, color=INK, sw=6):
    """n separate slanted teeth (0 up to 1) with grey drops between them."""
    teeth = VGroup(*[Line(ax.pt(i / n, 0), ax.pt((i + 1) / n, 1), color=color, stroke_width=sw) for i in range(n)])
    drops = VGroup(*[Line(ax.pt((i + 1) / n, 1), ax.pt((i + 1) / n, 0), color=DIM, stroke_width=3) for i in range(n - 1)])
    return VGroup(teeth, drops)


# ═════════════════════════════ B20 · the ramp ═════════════════════════════
class B20_Ramp(Scene):
    def construct(self):
        sq = uv_square(size=3.0, x=-2.2, y=0.6)
        xlab = T("x", 40).move_to([-2.2 + 1.5 + 0.55, 0.6 + 1.5 + 0.5, 0])
        self.add(sq)
        self.play(sq[1].animate.set_color(INK).set_stroke(width=7), FadeIn(xlab), run_time=0.6)
        until(self, "It is a ramp")
        strip = ramp_strip(width=3.0, x=-2.2, y=-1.75)
        mid_y = 0.6
        dot = a3_dot(-2.2 - 1.5, mid_y)
        mk = ramp_marker(strip, 0.0)
        guide = always_redraw(lambda: Line([dot.get_center()[0], dot.get_center()[1] - 0.16, 0], [dot.get_center()[0], strip.y + 0.25, 0], color=GHOST, stroke_width=4))
        self.play(LaggedStart(*[FadeIn(t) for t in strip.tiles], lag_ratio=0.02), FadeIn(strip.labels), run_time=0.6)
        self.add(guide, dot, mk)
        tr = ValueTracker(0.0)
        dot.add_updater(lambda m: m.move_to([-3.7 + 3.0 * tr.get_value(), mid_y, 0]))
        mk.add_updater(lambda m: m.move_to([strip.x0 + strip.width_s * tr.get_value(), strip.y, 0]))
        cap = T("ramp: a smooth run of values from 0 up to 1", 32).move_to([0.0, -3.0, 0])
        self.play(tr.animate.set_value(1.0), FadeIn(cap), run_time=1.6, rate_func=linear)
        dot.clear_updaters(); mk.clear_updaters()
        self.remove(guide)
        # the value on the right: UV.x is the whole story
        code = M("UV.x", 32).move_to([3.6, 0.6, 0])
        until(self, "Everything that follows")
        self.play(FadeIn(code), run_time=0.5)
        r = ring(strip.tiles, pad=0.12)
        self.play(FadeIn(r), run_time=0.5)
        done(self)


# ═════════════════════════════ B21 · fract ═════════════════════════════
class B21_FractRamp(Scene):
    def construct(self):
        cx, w = 1.3, 6.4
        s1 = ramp_strip(width=w, x=cx, y=2.65, labels=True)
        l1 = T("x", 32).move_to([cx - w / 2 - 0.5, 2.65, 0])
        self.play(FadeIn(s1), FadeIn(l1), run_time=0.5)
        until(self, "Multiply x by eight")
        s2 = ramp_strip(width=w, x=cx, y=1.45, label0="0", label1="8", labels=True)
        l2 = T("x ×  8", 32).move_to([cx - w / 2 - 0.9, 1.45, 0])
        ticks = VGroup(*[Line([cx - w / 2 + w * i / 8, 1.45 + 0.28, 0], [cx - w / 2 + w * i / 8, 1.45 + 0.52, 0], color=INK, stroke_width=4) for i in range(1, 8)])
        self.play(FadeIn(s2), FadeIn(l2), run_time=0.5)
        self.play(Create(ticks), run_time=0.5)
        # fract: a sawtooth with eight teeth, settled before the midpoint
        a3_at(self, 2.7)
        ax = a3_Axes(cx, -0.1, w, 1.4)
        frame = ax.frame()
        l3 = T("fract(x ×  8)", 32).move_to([cx - w / 2 - 1.6, -0.1, 0])
        teeth = a3_saw_teeth(ax)
        cap1 = T("fract(x): the part after the point: x minus floor(x)", 32).move_to([0.0, -2.55, 0])
        cap2 = T("floor(x): rounds down to the whole number below", 32).move_to([0.0, -3.05, 0])
        self.play(FadeIn(frame), FadeIn(l3), FadeIn(cap1), FadeIn(cap2), run_time=0.5)
        self.play(Create(teeth[0], lag_ratio=0.1), run_time=0.9)
        self.play(FadeIn(teeth[1]), run_time=0.3)
        dot = a3_dot(*ax.pt(0, 0)[:2])
        self.add(dot)
        # the dot waits at the start, then travels, snapping back at every whole number
        until(self, "so it starts over")
        tr = ValueTracker(0.0)
        dot.add_updater(lambda m: m.move_to(ax.pt(tr.get_value() / 8.0, tr.get_value() % 1.0 if tr.get_value() < 8 else 1.0)))
        for i in range(8):
            self.play(tr.animate.set_value(i + 0.999), run_time=0.34, rate_func=linear)
            tr.set_value(i + 1.0 if i == 7 else i + 1.0)
            if i < 7:
                self.wait(0.02)
        dot.clear_updaters()
        # eight repeated ramps in a row
        until(self, "eight ramps in a row", lead=0.0)
        row = VGroup(*[ramp_strip(width=0.74, n=8, height=0.3, x=cx - w / 2 + w * (i + 0.5) / 8, y=-1.55, labels=False) for i in range(8)])
        self.play(LaggedStart(*[FadeIn(r) for r in row], lag_ratio=0.08), run_time=0.8)
        done(self)


# ═════════════════════════════ B22 · step ═════════════════════════════
class B22_StepSwitch(Scene):
    def construct(self):
        cx, w = 1.3, 6.4
        ax1 = a3_Axes(cx, 1.65, w, 1.3)
        fr1 = ax1.frame()
        teeth = a3_saw_teeth(ax1)
        thr = DashedLine(ax1.pt(0, 0.5), ax1.pt(1, 0.5), color=DIM, stroke_width=4, dash_length=0.18)
        l1 = T("fract", 32).move_to([cx - w / 2 - 0.9, 1.65, 0])
        l1b = T("0.5", 32).move_to([cx + w / 2 + 0.5, ax1.pt(1, 0.5)[1], 0])
        self.add(fr1, teeth, thr, l1, l1b)
        until(self, "Step of point five")
        ax2 = a3_Axes(cx, -0.1, w, 0.9)
        fr2 = ax2.frame()
        l2 = T("step", 32).move_to([cx - w / 2 - 0.85, -0.1, 0])
        wave = VGroup()
        for i in range(8):
            a, b, c = i / 8, (i + 0.5) / 8, (i + 1) / 8
            wave.add(Line(ax2.pt(a, 0), ax2.pt(b, 0), color=DIM, stroke_width=6), Line(ax2.pt(b, 0), ax2.pt(b, 1), color=DIM, stroke_width=4),
                     Line(ax2.pt(b, 1), ax2.pt(c, 1), color=INK, stroke_width=6), Line(ax2.pt(c, 1), ax2.pt(c, 0), color=DIM, stroke_width=4) if i < 7 else VGroup())
        cap = T("step(edge, x): 0 below the edge, 1 from the edge up", 32).move_to([0.0, -2.75, 0])
        self.play(FadeIn(fr2), FadeIn(l2), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(wave), run_time=0.5)
        # the stripe strip: sixteen separate tiles, outlined until the dot passes
        tiles = VGroup(*[Rectangle(width=w / 16 * 0.82, height=0.36, stroke_color=GHOST, stroke_width=2).move_to([cx - w / 2 + w * (k + 0.5) / 16, -1.6, 0]) for k in range(16)])
        l3 = T("stripes", 32).move_to([cx - w / 2 - 0.95, -1.6, 0])
        self.play(FadeIn(tiles), FadeIn(l3), run_time=0.4)
        dot = a3_dot(*ax1.pt(0, 0)[:2])
        dot2 = a3_dot(*ax2.pt(0, 0)[:2], r=0.13)
        self.add(dot, dot2)
        tr = ValueTracker(0.0)

        def place(m):
            s = tr.get_value()
            fr = s % 1.0 if s < 8 else 1.0
            m.move_to(ax1.pt(s / 8.0, fr))
        dot.add_updater(place)
        dot2.add_updater(lambda m: m.move_to(ax2.pt(min(tr.get_value(), 8.0) / 8.0, 1.0 if (tr.get_value() % 1.0) >= 0.5 else 0.0)))
        until(self, "Feed it the repeating ramp")
        for i in range(8):
            self.play(tr.animate.set_value(i + 0.5), run_time=0.17, rate_func=linear)
            tr.set_value(i + 0.5)
            spark = Circle(radius=0.15, stroke_color=TERRA, stroke_width=6).move_to(ax2.pt((i + 0.5) / 8, 0.5))
            self.add(spark)
            tiles[2 * i].set_fill(DIM, opacity=1).set_stroke(DIM, width=2)
            self.play(tr.animate.set_value(i + 0.999), FadeOut(spark, scale=2.6), tiles[2 * i + 1].animate.set_fill(GHOST, opacity=1).set_stroke(GHOST, width=2),
                      run_time=0.17, rate_func=linear)
        dot.clear_updaters(); dot2.clear_updaters()
        done(self)


# ═════════════════════════════ B24 · mix ═════════════════════════════
class B24_MixLine(Scene):
    def construct(self):
        cx, w = 1.4, 6.4
        s_t = ramp_strip(width=w, x=cx, y=1.5, label0="0", label1="1", labels=True)
        s_m = ramp_strip(width=w, x=cx, y=-0.45, label0="a = 0.2", label1="b = 0.8", labels=True)
        lt = T("t", 32).move_to([cx - w / 2 - 0.5, 1.5, 0])
        lm = T("mix(a, b, t)", 32).move_to([cx - w / 2 - 1.5, -0.45, 0])
        cap = T("mix(a, b, t): blends from a to b: t of 0 gives a, 1 gives b", 32).move_to([0.0, -2.0, 0])
        d_t = a3_dot(cx - w / 2, 1.5)
        d_m = a3_dot(cx - w / 2, -0.45)
        self.add(s_t, s_m, lt, lm, cap)
        self.wait(0.4)
        self.play(FadeIn(d_t), FadeIn(d_m), run_time=0.4)
        tr = ValueTracker(0.0)
        d_t.add_updater(lambda m: m.move_to([cx - w / 2 + w * tr.get_value(), 1.5, 0]))
        d_m.add_updater(lambda m: m.move_to([cx - w / 2 + w * tr.get_value(), -0.45, 0]))
        a3_at(self, 1.2)
        self.play(tr.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        d_t.clear_updaters(); d_m.clear_updaters()
        until(self, "Mix of a", lead=0.1)
        form = T("a ×  (1 −  t)  +  b ×  t", 36).move_to([0.0, -2.9, 0])
        self.play(FadeIn(form), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · Read a Real One  (B35 only here, Manim; the kit is pasted above by assemble_scenes.py)

The pad shader's fragment function (lines 6 to 10 of lab-shaders/12-signal-pad.gdshader) as the one filled slot of the skeleton from Act I, with the
two empty slots (vertex, light) as dashed boxes above and below, all three on one width and one alignment. Two lines of the real file are wrapped
at an operator (marked in the report) because at the type floor (32) they are wider than the frame; the tokens themselves are untouched.
"""

A4_CW = 0.24962


def a4_toks(line, left, ybase, size=32):
    """Words of one code line on a shared baseline at exact monospace columns (see act 1's a1_toks)."""
    out = []
    col = 0
    for w in line.split(" "):
        if w:
            t = Text("H" + w + "H", font=MONO, color=INK, font_size=size)
            if len(t.submobjects) >= len(w) + 2:
                h0 = t.submobjects[0]
                t.shift([left + (col - 0.5) * A4_CW - h0.get_center()[0], ybase - h0.get_bottom()[1], 0])
                out.append(VGroup(*t.submobjects[1:-1]))
            else:
                out.append(M(w, size).move_to([left + (col + len(w) / 2.0) * A4_CW, ybase + 0.16, 0]))
        col += len(w) + 1
    return out


class B35_MissingSlots(Scene):
    """Two dashed slots draw in around the one filled function; then the filled one is outlined solid."""

    def construct(self):
        W = 12.3
        xc = 0.0
        src = ["void fragment() {",
               "  float stripe = step(0.5, fract(UV.x * 8.0));",
               "  vec3 base = quiet_color.rgb *",
               "      mix(0.65, 1.0, stripe);",
               "  ALBEDO = mix(base, active_color.rgb,",
               "      activation);",
               "}"]
        lh = 0.5
        H = len(src) * lh + 0.3
        cy = 0.0
        frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4).set_fill(PALEBOX, opacity=1).move_to([xc, cy, 0])
        left = xc - W / 2 + 0.45
        toks = []
        for i, ln in enumerate(src):
            y = cy + H / 2 - 0.15 - lh * (i + 0.5)
            toks += a4_toks(ln, left, y - 0.16)
        fn = VGroup(frame, *toks)
        top_y = cy + H / 2 + 0.3 + 0.4
        bot_y = cy - H / 2 - 0.3 - 0.4

        def slot(y):
            r = RoundedRectangle(width=W, height=0.8, corner_radius=0.14, stroke_color=DIM, stroke_width=5).move_to([xc, y, 0])
            return DashedVMobject(r, num_dashes=60, dashed_ratio=0.55)
        s_top = slot(top_y)
        s_bot = slot(bot_y)
        l_top = T("vertex(): Godot's default", 32).move_to([xc, top_y, 0])
        l_bot = T("light(): skipped by unshaded", 32).move_to([xc, bot_y, 0])
        self.add(fn)
        until(self, "no vertex function")
        self.play(Create(s_top), run_time=0.9)
        self.play(FadeIn(l_top), run_time=0.3)
        until(self, "no light function")
        self.play(Create(s_bot), run_time=0.9)
        self.play(FadeIn(l_bot), run_time=0.3)
        until(self, "The pad needs only fragment", lead=0.5)
        self.play(Indicate(s_top, scale_factor=1.03, color=DIM), Indicate(s_bot, scale_factor=1.03, color=DIM), run_time=0.8)
        self.play(frame.animate.set_stroke(INK, width=7), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Which Renderer?  (B40, B41; Manim)

B40 two lanes: the same chip 0.5 goes through "linear to sRGB" in Forward+ and comes out 0.74; straight through in Compatibility and stays 0.50; a small plot
(the diagonal against the standard screen curve) shows the lift once. B41 one channel on one line (red: rust 0.40, green 0.12): one dot, two midpoints.
Numbers are the measured ones in FACTCHECK.md (Apple M4 Pro, Godot 4.7.2); the curve is the standard sRGB encoding, written inline.
"""


def a5_at(self, t_abs):
    gap = t_abs - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a5_dot(x=0.0, y=0.0, r=0.16):
    return Dot([x, y, 0], radius=r, color=TERRA).set_stroke(DIM, width=3)


def a5_srgb(v):
    return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def a5_chip(text, x, y, w=1.3):
    b = box(x, y, w, 0.7, color=INK, sw=4, fill=CARD)
    t = T(text, 32).move_to([x, y, 0])
    g = VGroup(b, t)
    g.b = b; g.t = t
    return g


# ═════════════════════════════ B40 · two lanes ═════════════════════════════
class B40_TwoLanes(Scene):
    def construct(self):
        # the plot, once: diagonal (Compatibility) against the screen curve (Forward+)
        px, py, pw, ph = -0.4, 2.15, 2.1, 1.75
        x0, y0 = px - pw / 2, py - ph / 2
        P = lambda u, v: np.array([x0 + u * pw, y0 + v * ph, 0])
        axes = VGroup(Line(P(0, 0), P(1, 0), color=INK, stroke_width=5), Line(P(0, 0), P(0, 1), color=INK, stroke_width=5))
        diag = Line(P(0, 0), P(1, 1), color=DIM, stroke_width=6)
        curve = VMobject(stroke_color=INK, stroke_width=6).set_points_smoothly([P(u, a5_srgb(u)) for u in np.linspace(0.0, 1.0, 60)])
        k1 = VGroup(Line([1.3, 2.75, 0], [1.75, 2.75, 0], color=INK, stroke_width=6), T("Forward+", 32).move_to([3.15, 2.75, 0]))
        k2 = VGroup(Line([1.3, 1.95, 0], [1.75, 1.95, 0], color=DIM, stroke_width=6), T("Compatibility", 32).move_to([3.45, 1.95, 0]))
        # lanes
        ly1, ly2 = 0.2, -0.95
        n1 = T("Forward+", 32).move_to([-5.0, ly1, 0])
        n2 = T("Compatibility", 32).move_to([-4.65, ly2, 0])
        sx, ex = -2.6, 4.9
        track1 = arrow([sx - 0.6, ly1 - 0.52, 0], [ex + 0.6, ly1 - 0.52, 0], color=GHOST, w=6)
        track2 = arrow([sx - 0.6, ly2 - 0.52, 0], [ex + 0.6, ly2 - 0.52, 0], color=GHOST, w=6)
        blk = box(0.9, ly1, 3.5, 0.85, color=INK, sw=4)
        blkt = T("linear to sRGB", 32).move_to([0.9, ly1, 0])
        cap1 = T("linear: the scale light adds up on, in a straight line", 32).move_to([0.0, -1.95, 0])
        cap2 = T("sRGB: the scale a color picker's numbers use, spaced for the eye", 32).move_to([0.0, -2.45, 0])
        credit = T("measured · Apple M4 Pro · Godot 4.7.2", 32).move_to([0.0, -3.15, 0])
        c1 = a5_chip("0.5", sx, ly1)
        c2 = a5_chip("0.5", sx, ly2)
        self.add(axes, diag, curve, k1, k2, n1, n2, track1, track2, blk, blkt, cap1, cap2, credit)
        self.wait(0.3)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        # Forward+: through the block, out as 0.74; the plot dot rises with it
        ddot = a5_dot(*P(0.5, 0.5)[:2])
        gdot = Circle(radius=0.14, stroke_color=DIM, stroke_width=5).move_to(P(0.5, 0.5))
        self.add(gdot)
        self.play(FadeIn(ddot), run_time=0.3)
        until(self, "Forward Plus", lead=0.0)
        self.play(c1.animate.move_to([-1.6, ly1, 0]), run_time=0.7)
        c1n = a5_chip("0.74", 3.4, ly1)
        self.play(FadeOut(c1, shift=RIGHT * 0.6), run_time=0.4)
        self.play(FadeIn(c1n, shift=RIGHT * 0.3), ddot.animate.move_to(P(0.5, a5_srgb(0.5))), run_time=0.5)
        self.play(c1n.animate.move_to([ex, ly1, 0]), run_time=0.6)
        # Compatibility: straight through, still 0.50
        until(self, "Compatibility skips", lead=0.2)
        self.play(c2.animate.move_to([ex, ly2, 0]), run_time=1.4)
        c2n = a5_chip("0.50", ex, ly2)
        self.play(ReplacementTransform(c2, c2n), run_time=0.4)
        done(self)


# ═════════════════════════════ B41 · two midpoints ═════════════════════════════
class B41_TwoMidpoints(Scene):
    def construct(self):
        L, R, y = -4.5, 4.5, 0.4
        X = lambda v: L + (0.40 - v) / 0.28 * (R - L)            # red 0.40 at left, 0.12 at right
        head = T("red channel", 32).move_to([0.0, 2.7, 0])
        line = Line([L, y, 0], [R, y, 0], color=DIM, stroke_width=7)
        sw1 = Square(side_length=0.45, stroke_color=INK, stroke_width=3).set_fill("#66291A", opacity=1).move_to([L, y, 0])
        sw2 = Square(side_length=0.45, stroke_color=INK, stroke_width=3).set_fill("#1FB885", opacity=1).move_to([R, y, 0])
        e1 = T("rust 0.40", 32).move_to([L, y - 0.65, 0])
        e2 = T("green 0.12", 32).move_to([R - 0.2, y - 0.65, 0])
        cred = T("measured 0.26 and 0.30 · Apple M4 Pro · Godot 4.7.2", 32).move_to([0.0, -3.05, 0])
        self.add(head, line, e1, e2, cred)
        self.play(FadeIn(sw1), FadeIn(sw2), run_time=0.4)
        dot = a5_dot(L, y)
        self.play(FadeIn(dot), run_time=0.3)
        # the tag by the two ends, on "marked source color"
        until(self, "marked source color", lead=0.3)
        tag = T("source_color: numbers are sRGB: convert to light first", 32).move_to([0.0, -2.35, 0])
        self.play(FadeIn(tag), run_time=0.5)
        # Forward+: linear light first, the midpoint lands at 0.30
        a5_at(self, 3.6)
        self.play(dot.animate.move_to([X(0.30), y, 0]), run_time=0.9)
        pf = Triangle(color=INK, fill_opacity=1).scale(0.16).rotate(PI).move_to([X(0.30), y + 0.35, 0])
        self.play(FadeIn(pf, shift=DOWN * 0.3), run_time=0.3)
        lf1 = T("Forward+", 32).move_to([X(0.30), y + 1.55, 0])
        lf2 = T("linear light 0.30", 32).move_to([X(0.30), y + 1.0, 0])
        self.play(FadeIn(lf1), FadeIn(lf2), run_time=0.4)
        # Compatibility: the numbers as written, midpoint 0.26
        until(self, "Compatibility blends", lead=0.2)
        self.play(dot.animate.move_to([X(0.26), y, 0]), run_time=0.9)
        pc = Triangle(color=DIM, fill_opacity=1).scale(0.16).move_to([X(0.26), y - 0.35, 0])
        self.play(FadeIn(pc, shift=UP * 0.3), run_time=0.3)
        cm1 = T("Compatibility", 32).move_to([X(0.26) + 0.6, y - 1.1, 0])
        cm2 = T("as written 0.26", 32).move_to([X(0.26) + 0.6, y - 1.55, 0])
        self.play(FadeIn(cm1), FadeIn(cm2), run_time=0.4)
        until(self, "One dial, two midpoints", lead=0.0)
        gap = Line([X(0.30), y, 0], [X(0.26), y, 0], color=DIM)
        self.play(FadeIn(ring(gap, pad=0.22)), run_time=0.5)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
