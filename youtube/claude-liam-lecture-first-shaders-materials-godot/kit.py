"""
kit.py — the lecture's shared drawing + pacing kit (Assignment-walkthrough film: shaders, materials, the Godot shading language). NOT imported: assemble_scenes.py pastes it at the top of
scenes.py (Gate A copies only scenes.py). It is show-tell's iso_kit (palette, Iso projection, pacing helpers
until/finish) plus the midpoint guard (ST/guard/done) from show-tell-context-is-a-budget, plus a few lecture helpers.
"""
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


# ═════════════════════════════ shader-film helpers (added for this film) ═════════════════════════════
# Everything below is pure drawing: no helper invents data. Real numbers, real code lines and real captures are passed IN by the scene.
TEAL = "#5FA391"; PALEBOX = "#FFFFFF"; GOLD = "#C9A227"
PB_PATH_HINT = "/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/professor-bear"


def box(x, y, w, h, color=INK, sw=4, radius=0.12):
    """An OUTLINED rounded box centred at (x, y). No fill: text may sit inside with >= 0.25 padding."""
    return RoundedRectangle(width=w, height=h, corner_radius=radius, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([x, y, 0])


def arrow(a, b, color=INK, w=6, tip=0.22):
    """A single-headed arrow drawn as a shape (the '->' glyph is under the type floor)."""
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, color=color, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.45)


def ring(mob, color=TERRA, pad=0.12, sw=7, backing=True):
    """A terracotta ring round a mobject over a wider GREY backing so it never reads as accent text (GATE T). Returns VGroup(backing, ring).
    Never ring TEXT in ink (Gate B overlap); a grey/terracotta ring round text is fine when padded >= 0.12."""
    w, h = mob.width + 2 * pad, mob.height + 2 * pad
    r = RoundedRectangle(width=w, height=h, corner_radius=0.16, stroke_color=color, stroke_width=sw).move_to(mob.get_center())
    if not backing:
        return VGroup(r)
    b = RoundedRectangle(width=w + 0.1, height=h + 0.1, corner_radius=0.18, stroke_color=DIM, stroke_width=sw + 5, stroke_opacity=0.55).move_to(mob.get_center())
    return VGroup(b, r)


def tick_mark(x, y, s=0.2, color=INK, w=7):
    return check(x, y, s, color, w)


def cross_mark(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w), Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def open_circle(x, y, r=0.2, color=INK, w=5):
    """An OPEN circle: the mark for 'not done' (ledger of what the example did not do)."""
    return Circle(radius=r, stroke_color=color, stroke_width=w, fill_opacity=0).move_to([x, y, 0])


def eye_icon(x, y, s=0.6, color=INK):
    """A drawn eye: the mark for 'a human check' (almond outline, iris ring, one terracotta pupil dot). Pure drawing, no person."""
    top = ArcBetweenPoints(np.array([x - s, y, 0.0]), np.array([x + s, y, 0.0]), angle=-PI / 2.4, stroke_color=color, stroke_width=6)
    bot = ArcBetweenPoints(np.array([x + s, y, 0.0]), np.array([x - s, y, 0.0]), angle=-PI / 2.4, stroke_color=color, stroke_width=6)
    iris = Circle(radius=s * 0.36, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([x, y, 0])
    pupil = Dot([x, y, 0], radius=s * 0.15, color=TERRA)
    return VGroup(top, bot, iris, pupil)


def terminal_icon(x, y, s=0.6, color=INK):
    """A drawn terminal window (outline, a chevron and a cursor bar): the mark for 'a headless test'."""
    frame = RoundedRectangle(width=2 * s, height=1.5 * s, corner_radius=0.1, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([x, y, 0])
    chev = VGroup(Line([x - 0.55 * s, y + 0.2 * s, 0], [x - 0.2 * s, y, 0], color=color, stroke_width=6), Line([x - 0.2 * s, y, 0], [x - 0.55 * s, y - 0.2 * s, 0], color=color, stroke_width=6))
    bar = Line([x + 0.0 * s, y - 0.2 * s, 0], [x + 0.5 * s, y - 0.2 * s, 0], color=color, stroke_width=6)
    return VGroup(frame, chev, bar)


def example_tag(x=3.05, y=-3.0, text="instructor example · A. I.-written"):
    """THE HONESTY CHIP (Films = things actually done). Put it on every beat that shows a file or run of the instructor example. Outline pill, DIM text,
    sized for the 4K type floor (>= 32 at this frame is about 24 px on a 1080 view; keep to <= 7 units wide)."""
    t = T(text, 32, DIM)
    p = RoundedRectangle(width=t.width + 0.5, height=0.62, corner_radius=0.31, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x, y, 0])
    t.move_to([x, y, 0])
    return VGroup(p, t)


def status_tag(text, x, y, size=32):
    """A small outline pill for 'documented, not run' / 'scripted input' / 'recorded output' / 'reconstruction' / 'illustrative'."""
    t = T(text, size, DIM)
    p = RoundedRectangle(width=t.width + 0.5, height=0.6, corner_radius=0.3, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x, y, 0])
    t.move_to([x, y, 0])
    return VGroup(p, t)


def img(path, w=None, h=None, x=0.0, y=0.0):
    """A real picture from pantry/ or captures/ as itself. Set EITHER w or h. Never draw over it; rings go beside or after the midpoint."""
    im = ImageMobject(path)
    if w is not None:
        im.set_width(w)
    elif h is not None:
        im.set_height(h)
    return im.move_to([x, y, 0])


def framed(im, color=DIM, pad=0.06, sw=4):
    """A thin grey frame just outside a real picture. Returns Group(im, frame)."""
    fr = Rectangle(width=im.width + 2 * pad, height=im.height + 2 * pad, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to(im.get_center())
    g = Group(im, fr)
    g.im, g.fr = im, fr
    return g


def crop_img(path, box, out_name, scratch="media/_crops"):
    """Crop a real image (PIL) to box=(x0,y0,x1,y1) in source pixels and cache it under media/_crops/ (a NEW file name, so Manim's cache never replays old pixels).
    Returns the path to use with img()."""
    from PIL import Image as _Im
    _os.makedirs(scratch, exist_ok=True)
    out = _os.path.join(scratch, out_name)
    if not _os.path.exists(out):
        _Im.open(path).convert("RGB").crop(box).save(out)
    return out


def code_block(lines, x=0.0, y=0.0, size=24, first=1, numbers=True, pad=0.3, width=None, dim_lines=()):
    """Real code, Menlo, with line numbers, OUTLINE-only frame (no fill behind text). `lines` = list of str (verbatim; tabs become 4 spaces); `first` = the number of the
    first line (so an excerpt keeps its REAL line numbers). Leading indentation is kept (Pango trims leading spaces, so each row is placed by an explicit x).
    Positions use the MEASURED glyph advance (not Text.width, which the Gate A stub overestimates), so a long row passes the static check.
    Returns VGroup with .rows (list of VGroup(num, text)), .frame, .W, .H, .lh, .cw, .row(n) -> the row of REAL line number n, .ring_line(n) -> a ring round that line.
    Line numbers are DIM, code is INK. LOOK at the still: if Pango fuses two words, double the space at that boundary in the scene (never in the source).
    SIZES (measured on this Mac, Manim 0.20.1, Menlo): size 24 = 0.2000 units/char, x-height 49 px at 4K (max ~58 characters in a 12.4-unit column);
    size 20 = 0.1500 units/char, x-height 41 px at 4K = exactly GATE T's floor (max ~78 characters; borderline: prove it with the real 4K gate); sizes 28 and 32 =
    0.2500 units/char (max ~46 characters). The house floor of 32 applies to serif LABELS (`T`); real code is never reflowed and never shrunk below size 20, so a block
    picks the size its longest REAL line needs (signal.gdshader has two 70-character lines: use 20, or show those two lines elsewhere)."""
    cw = {20: 0.15, 22: 0.2, 24: 0.2, 28: 0.25, 32: 0.25}.get(int(size), 0.0078 * size)
    lh = max(0.30, size / 32 * 0.46)
    ns = [str(first + i) for i in range(len(lines))]
    nw = (max(len(n) for n in ns) * cw + 0.25) if numbers else 0.0
    expanded = [(ln.replace("\t", "    ")) for ln in lines]
    longest = max(len(e) for e in expanded)
    W = (width or (longest * cw + nw + 2 * pad)); H = len(lines) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, e in enumerate(expanded):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        body = e.lstrip(" ")
        indent = len(e) - len(body)
        n = M(ns[i], size, GHOST if i in dim_lines else DIM).move_to([left + len(ns[i]) * cw / 2, yy, 0]) if numbers else VGroup()
        t = M(body if body else " ", size, DIM if i in dim_lines else INK)
        if body:
            t.move_to([left + nw + indent * cw + len(body) * cw / 2, yy, 0])
        else:
            t.move_to([left + nw, yy, 0])
        rows.add(VGroup(n, t))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.cw, g.first, g.size_ = frame, rows, W, H, lh, cw, first, size
    g.row = lambda n: rows[n - first]
    def _ring_line(n, color=TERRA):
        r_ = rows[n - first]
        return RoundedRectangle(width=W - 0.3, height=lh * 0.98, corner_radius=0.1, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, r_.get_center()[1], 0])
    g.ring_line = _ring_line
    return g


def pixel_grid(cols=12, rows=6, cell=0.42, x=0.0, y=0.0, color=DIM, sw=2):
    """A grid of OUTLINE-only cells. Returns VGroup with .cells ([row][col] Squares), .cell, .cols, .rows."""
    cells = []; g = VGroup()
    x0 = x - cols * cell / 2 + cell / 2; y0 = y + rows * cell / 2 - cell / 2
    for r in range(rows):
        row = []
        for c in range(cols):
            sq = Square(side_length=cell * 0.94, stroke_color=color, stroke_width=sw).move_to([x0 + c * cell, y0 - r * cell, 0])
            row.append(sq); g.add(sq)
        cells.append(row)
    g.cells, g.cell, g.cols, g.rows = cells, cell, cols, rows
    return g


def tint(cell, color, opacity=1.0):
    """Animation: fill an outline cell with a colour (use on cells that carry no text)."""
    return cell.animate.set_fill(color, opacity=opacity).set_stroke(color, width=2)


def plot(fn, x_range=(0, 1), y_range=(0, 1), size=(4.0, 2.4), x=0.0, y=0.0, color=INK, samples=80, step=False):
    """Axes + a curve. No LaTeX. Returns VGroup with .curve, .pt(xv) -> scene point, .axes, .x0, .y0, .w, .h. step=True draws vertical jumps (use for step())."""
    w, h = size; x0, y0 = x - w / 2, y - h / 2
    axes = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + h, 0], color=INK, stroke_width=5))

    def pt(xv):
        yv = fn(xv)
        return np.array([x0 + (xv - x_range[0]) / (x_range[1] - x_range[0]) * w, y0 + (yv - y_range[0]) / (y_range[1] - y_range[0]) * h, 0])
    xs = np.linspace(x_range[0], x_range[1], samples)
    curve = VMobject(stroke_color=color, stroke_width=7)
    pts = [pt(v) for v in xs]
    if step:
        curve.set_points_as_corners(pts)
    else:
        curve.set_points_smoothly(pts)
    g = VGroup(axes, curve)
    g.curve, g.pt, g.axes, g.x0, g.y0, g.w, g.h = curve, pt, axes, x0, y0, w, h
    return g


def swatch(rgb8, x, y, w=1.0, h=0.7):
    """A solid colour chip showing a REAL measured or computed RGB8 triple (0-255 ints). Outline-free; keep text BESIDE it."""
    col = "#%02x%02x%02x" % tuple(max(0, min(255, int(v))) for v in rgb8)
    return Rectangle(width=w, height=h, fill_color=col, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def logo_chip(company, x, y, h=1.35, n=1):
    """A white pill carrying the company's LOGO (LOGO LAW, Bear 2026-10-12): brutalist.art/icons/logos/<company>/<company>-NN.png. Falls back to a text pill
    if the file is missing (then say so in the report). Returns a Group (it holds an image)."""
    cands = []
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(9):
        cands.append(_os.path.join(here, "brutalist.art", "icons", "logos")); here = _os.path.dirname(here)
    cands.append("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/icons/logos")
    p = None
    for c in cands:
        q = _os.path.join(c, company, f"{company}-{n:02d}.png")
        if _os.path.exists(q):
            p = q; break
    w = h * 1.35
    if p is None:
        t = T(company, 34)
        return Group(pill(x + 0.08, y - 0.08, t.width + 0.8, h=0.8, fill=BOX_L), pill(x, y, t.width + 0.8, h=0.8), t.move_to([x, y, 0]))
    shadow = pill(x + 0.08, y - 0.08, w, h=h, fill=BOX_L); body = pill(x, y, w, h=h)
    im = ImageMobject(p); im.scale_to_fit_height(h * 0.78); im.move_to([x, y, 0])
    g = Group(shadow, body, im); g.pill = body
    return g


# ── Professor Bear portrait (PROFESSOR BEAR LAW: a person / "you" is never an icon) ──
def _pb_dir():
    cands = []
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(9):
        cands.append(_os.path.join(here, "brutalist.art", "professor-bear")); here = _os.path.dirname(here)
    cands.append(PB_PATH_HINT)
    for c in cands:
        if _os.path.isdir(c):
            return c
    return PB_PATH_HINT


_PB_RATIOS = {"1x1": (1.0, 229), "2x3": (2 / 3, 28), "16x9": (16 / 9, 13)}


def _pb_circle(path):
    from PIL import Image as _Im, ImageDraw as _Dr
    out_dir = _os.path.join(_os.path.dirname(path), "_crops"); _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, _os.path.splitext(_os.path.basename(path))[0] + "-circle.png")
    if not _os.path.exists(out):
        im = _Im.open(path).convert("RGBA"); w, h = im.size; s = min(w, h); top = max(0, (h - s) // 3)
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s))
        mask = _Im.new("L", (s, s), 0); _Dr.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
        im.putalpha(mask); im.save(out)
    return out


def professor_bear(ratio="1x1", height=2.4, seed=None, x=0.0, y=0.0, frame=True, shape="rect"):
    """A Professor Bear portrait (random within `ratio`; `seed` = a LITERAL string such as the beat id, for a stable pick across re-renders). Returns a Group."""
    import random as _random
    ar, n = _PB_RATIOS[ratio]
    k = _random.Random(str(seed) if seed is not None else None).randint(1, n)
    path = _os.path.join(_pb_dir(), f"professor-bear-{ratio}-{k:02d}.png")
    circle = shape == "circle"
    if circle:
        ar = 1.0
    w = height * ar
    if circle:
        shadow = Circle(radius=height / 2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Circle(radius=height / 2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    else:
        shadow = Rectangle(width=w, height=height, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Rectangle(width=w, height=height, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    try:
        im = ImageMobject(_pb_circle(path) if circle else path); im.height = height; im.move_to([x, y, 0])
    except Exception:
        im = Rectangle(width=w, height=height, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = Group(shadow, im, border) if frame else Group(im)
    g.path = path
    return g


def chip(text, x, y, w=None, mono=False, size=34):
    """A white pill with a short label (no outline, so text and outline never fuse)."""
    lab = M(text, size - 2) if mono else T(text, size)
    w = w or (lab.width + 0.8)
    shadow = pill(x + 0.08, y - 0.08, w, h=0.8, fill=BOX_L)
    p = pill(x, y, w, h=0.8)
    lab.move_to([x, y, 0])
    g = VGroup(shadow, p, lab)
    g.pill, g.label = p, lab
    return g
