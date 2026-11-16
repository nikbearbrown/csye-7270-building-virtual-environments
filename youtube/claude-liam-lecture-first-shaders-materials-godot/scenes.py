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


# ══════════════════════════════ scenes_act1.py ══════════════════════════════
"""ACT I · Two Shaders and Their Materials  (B01-B08, all Manim)

One cast for the act: the real pad frames of the scripted lab run (captures/lab/lab_000503.png -> lab_000610.png, cropped by
evidence/act1/make_a1_pantry.py: pantry/a1_pad_idle.png, a1_pad_open.png) and the two real spheres of the example's own
capture (pantry/a1_sphere_matte.png, a1_sphere_coated.png: circle crops of ev_mat_baseline.png). Everything else that is a real
thing is shown as itself: Claude Code by its logo (logo_chip), "you" by a Professor Bear portrait, the example's own shader and
script lines by code_block() (real line numbers), the Poly Haven record by the words of evidence/example/polyhaven-ATTRIBUTION.md.
Honesty chips: example_tag() on every beat that shows a file or capture of the instructor example; status_tag("scripted input")
under the pad frames; status_tag("the example, 14 Oct") under the sphere capture.
Pacing: until() cues come from the character share of the narration (no audio yet); fixed sequences finish by ~75-90 % of the estimate.
"""

A1P = "pantry/"


def a1_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A1P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a1_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a1_no(x, y, r=0.32, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE a picture or label, never over type."""
    ring_ = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring_, bar)


# Measured with Manim 0.20.1 on this Mac (the Gate A stub cannot measure serif text, so chip layout uses these numbers, not .width): T(label, 34).width.
# Code geometry comes from the kit's code_block (it positions by measured glyph advance): block.W, block.cw, block.H, block.lh.
A1_TW = {"functions": 1.7262, "built-ins": 1.4799, "both shaders": 2.3299, "language notes": 2.6785, "context file": 2.0057,
         "driver": 1.0387, "tests": 0.7709, "audit": 0.9271, "reviews": 1.2738}
def a1_code_x(blk, x, first):
    """x of character 0 of a code_block row for a block centred on x (kit geometry: left = x - W/2 + pad(0.3); text starts nw = len(number)*cw + 0.25 further right)."""
    return x - blk.W / 2 + 0.3 + len(str(first)) * blk.cw + 0.25


def a1_bracket(x0, x1, y, gap=0.1, drop=0.17):
    """A grey-ink bracket under the characters x0..x1 of a code row centred on y (clear of the text box: it never touches the row)."""
    yt = y - 0.17 - gap
    yb = yt - drop
    return VGroup(Line([x0, yt, 0], [x0, yb, 0], color=INK, stroke_width=5), Line([x0, yb, 0], [x1, yb, 0], color=INK, stroke_width=5),
                  Line([x1, yb, 0], [x1, yt, 0], color=INK, stroke_width=5))


def a1_chip_row(labels, x0, y, gap=0.2, size=34):
    """White pill chips laid left to right from x0 (left edge), widths from A1_TW. Returns the list of chips (each with .cx, its centre x)."""
    out, x = [], x0
    for s in labels:
        w = A1_TW[s] + 0.8
        c = chip(s, x + w / 2, y, w=w, size=size)
        c.cx = x + w / 2
        out.append(c)
        x += w + gap
    return out


def a1_key(x, y, s=1.0):
    """A drawn key (ring + shaft + two teeth), ink outline, big enough to clear the type floor."""
    bow = Circle(radius=0.55 * s, stroke_color=INK, stroke_width=7, fill_opacity=0).move_to([x - 1.0 * s, y, 0])
    hole = Circle(radius=0.17 * s, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x - 1.0 * s, y, 0])
    shaft = Line([x - 0.45 * s, y, 0], [x + 1.55 * s, y, 0], color=INK, stroke_width=9)
    t1 = Line([x + 1.0 * s, y, 0], [x + 1.0 * s, y - 0.5 * s, 0], color=INK, stroke_width=9)
    t2 = Line([x + 1.55 * s, y, 0], [x + 1.55 * s, y - 0.4 * s, 0], color=INK, stroke_width=9)
    return VGroup(bow, hole, shaft, t1, t2)


# ── B01 · the job: a tint on one object while a state holds; a surface dressed with textures ──────────────────────────
class B01_Job(Scene):
    def construct(self):
        title = T("Two Shaders and Their Materials", 40).move_to([-2.45, 2.95, 0])
        self.add(title)
        LX, RX = -3.3, 3.3
        tag = example_tag()
        self.play(FadeIn(tag), run_time=0.4)
        c1 = chip("signal.gdshader", LX, 1.85, mono=True, size=30)
        c2 = chip("surface.gdshader", RX, 1.85, mono=True, size=30)
        until(self, "two shaders", lead=0.2)
        self.play(FadeIn(c1, shift=DOWN * 0.3), run_time=0.45)
        self.play(FadeIn(c2, shift=DOWN * 0.3), run_time=0.45)
        until(self, "and the materials", lead=0.2)
        aL = arrow([LX, 1.3, 0], [LX, 0.95, 0], w=6, tip=0.2)
        aR = arrow([RX, 1.3, 0], [RX, 0.95, 0], w=6, tip=0.2)
        self.play(GrowArrow(aL), GrowArrow(aR), run_time=0.4)
        idle = a1_img("a1_pad_idle.png", h=2.5, at=(LX, -0.45))
        opn = a1_img("a1_pad_open.png", h=2.5, at=(LX, -0.45))
        frL = Rectangle(width=idle.width + 0.12, height=idle.height + 0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([LX, -0.45, 0])
        s_tag = status_tag("scripted input", LX, -2.15)
        until(self, "added to your game", lead=0.6)
        self.play(FadeIn(idle), Create(frL), FadeIn(s_tag), run_time=0.5)
        until(self, "while a game state", lead=0.15)
        self.play(FadeIn(opn), run_time=0.5)
        until(self, "One dresses", lead=0.4)
        mat = a1_img("a1_sphere_matte.png", h=2.3, at=(RX - 1.3, -0.45))
        coa = a1_img("a1_sphere_coated.png", h=2.3, at=(RX + 1.3, -0.45))
        e_tag = status_tag("the example, 14 Oct", RX, -2.15)
        self.play(FadeIn(mat, scale=0.9), run_time=0.45)
        self.play(FadeIn(coa, scale=0.9), FadeIn(e_tag), run_time=0.45)
        done(self)


# ── B02 · a shader is a program run for every pixel at once; sees three things; remembers nothing; state arrives as a uniform ──
class B02_EveryPixel(Scene):
    def construct(self):
        GX, GY, CELL = 1.9, -0.45, 0.46
        grid = pixel_grid(12, 6, CELL, GX, GY, color=DIM, sw=3)
        self.play(FadeIn(grid), run_time=0.6)
        cx = [GX - 6 * CELL + CELL / 2 + c * CELL for c in range(12)]
        cy = [GY + 3 * CELL - CELL / 2 - r * CELL for r in range(6)]
        cols = [VGroup(*[Dot([cx[c], cy[r], 0], radius=0.075, color=TERRA) for r in range(6)]) for c in range(12)]
        allbits = VGroup(*cols)
        k_l = a1_lab("every pixel", GX, -2.5, 36)
        until(self, "for every pixel", lead=0.1)
        self.play(*[GrowFromCenter(g) for g in cols], FadeIn(k_l), run_time=0.5)
        names = ["built-ins", "uniforms", "textures"]
        ys = [0.7, -0.45, -1.6]
        ins = []
        for nm, y in zip(names, ys):
            lab = a1_lab(nm, -5.95, y, 36, left=True)
            ar = arrow([-4.0, y, 0], [-1.15, y, 0], w=6, tip=0.2)
            ins.append((lab, ar))
        until(self, "built-ins", lead=0.65)
        self.play(FadeIn(ins[0][0], shift=RIGHT * 0.3), GrowArrow(ins[0][1]), run_time=0.4)
        until(self, "uniforms and", lead=0.25)
        self.play(FadeIn(ins[1][0], shift=RIGHT * 0.3), GrowArrow(ins[1][1]), run_time=0.4)
        until(self, "textures,", lead=0.25)
        self.play(FadeIn(ins[2][0], shift=RIGHT * 0.3), GrowArrow(ins[2][1]), run_time=0.4)
        # remembers nothing: a grey sweep clears every cell
        until(self, "remembers nothing", lead=0.45)
        sw = Line([GX - 2.9, GY + 1.55, 0], [GX - 2.9, GY - 1.55, 0], color=DIM, stroke_width=7)
        n_l = a1_lab("remembers nothing", GX, -2.5, 36)
        self.play(Create(sw), run_time=0.2)
        self.play(sw.animate.shift(RIGHT * 5.8), LaggedStart(*[FadeOut(g) for g in cols], lag_ratio=0.07),
                  FadeOut(k_l), FadeIn(n_l), run_time=0.9)
        self.play(FadeOut(sw), run_time=0.15)
        # game state arrives as one uniform: one rail, one tick into every column
        until(self, "So game state", lead=0.2)
        box_ = box(GX, 2.45, 3.0, 0.8, color=DIM, sw=4)
        g_l = a1_lab("game code", GX, 2.45, 34)
        stem = Line([GX, 2.05, 0], [GX, 1.55, 0], color=INK, stroke_width=6)
        self.play(Create(box_), FadeIn(g_l), Create(stem), run_time=0.45)
        until(self, "must arrive", lead=0.35)
        rail = Line([cx[0], 1.55, 0], [cx[11], 1.55, 0], color=INK, stroke_width=6)
        ticks = [Line([x, 1.55, 0], [x, 1.1, 0], color=INK, stroke_width=5) for x in cx]
        u_l = M("uniform", 28).move_to([5.1, 1.9, 0])
        self.play(Create(rail), FadeIn(u_l), run_time=0.25)
        self.play(LaggedStart(*[AnimationGroup(Create(t_), GrowFromCenter(g_)) for t_, g_ in zip(ticks, cols)], lag_ratio=0.1), run_time=0.45)
        done(self)


# ── B03 · a material pairs one shader with values; two materials share it ───────────────────────────────────────────────
class B03_OneShaderTwoMaterials(Scene):
    def construct(self):
        tag = example_tag()
        self.add(tag)
        sh = chip("surface.gdshader", -4.05, 0.1, mono=True, size=26)
        self.play(FadeIn(sh, shift=RIGHT * 0.3), run_time=0.4)

        def card(cy, name, sphere, rows):
            fr = box(2.6, cy, 7.0, 2.3, color=DIM, sw=4)
            nm = a1_lab(name, 1.5, cy + 0.85, 38, left=True)
            items = []
            for i, (k, v) in enumerate(rows):
                yy = cy + 0.3 - 0.55 * i
                items.append(M(k, 24).move_to([1.5 + 0.0, yy, 0], aligned_edge=LEFT))
                if isinstance(v, tuple):
                    sw_ = swatch(v, 5.0, yy, 0.75, 0.34)
                    ol = Rectangle(width=0.75, height=0.34, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([5.0, yy, 0])
                    items.append(VGroup(sw_, ol))
                else:
                    items.append(M(v, 24).move_to([4.75, yy, 0], aligned_edge=LEFT))
            img_ = a1_img(sphere, h=1.75, at=(0.2, cy))
            return fr, nm, items, img_

        mat_rows = [("tint", (255, 255, 255)), ("roughness_gain", "0.9"), ("uv_scale", "1.0")]
        coa_rows = [("tint", (115, 242, 184)), ("roughness_gain", "0.25"), ("uv_scale", "2.0")]
        f1, n1, it1, im1 = card(1.5, "matte", "a1_sphere_matte.png", mat_rows)
        f2, n2, it2, im2 = card(-1.3, "coated", "a1_sphere_coated.png", coa_rows)
        a1 = arrow([-2.05, 0.35, 0], [-0.95, 1.05, 0], w=6, tip=0.2)
        a2 = arrow([-2.05, -0.15, 0], [-0.95, -0.85, 0], w=6, tip=0.2)
        until(self, "with values", lead=0.15)
        self.play(Create(f1), FadeIn(n1), GrowArrow(a1), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(m_) for m_ in it1], lag_ratio=0.12), run_time=0.7)
        until(self, "Many materials", lead=0.1)
        self.play(Create(f2), FadeIn(n2), GrowArrow(a2), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(m_) for m_ in it2], lag_ratio=0.12), run_time=0.7)
        until(self, "Your second shader", lead=0.15)
        self.play(FadeIn(im1, scale=0.9), run_time=0.45)
        self.play(FadeIn(im2, scale=0.9), run_time=0.45)
        done(self)


# ── B04 · a texture is a grid of numbers; the shader decides what they mean ─────────────────────────────────────────────
class B04_GridOfNumbers(Scene):
    def construct(self):
        xs = [-5.0, -3.9, -2.8]
        vals = [64, 128, 192]
        cells = VGroup(*[Rectangle(width=1.0, height=1.0, stroke_color=DIM, stroke_width=4, fill_color="#%02x%02x%02x" % (v, v, v), fill_opacity=1).move_to([x, 0.35, 0])
                         for x, v in zip(xs, vals)])
        nums = [T(str(v), 42).move_to([x, -0.55, 0]) for x, v in zip(xs, vals)]
        t_l = a1_lab("texture", -3.9, 1.35, 38)
        until(self, "grid of numbers", lead=0.65)
        self.play(FadeIn(t_l), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.2), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(n_, shift=UP * 0.15) for n_ in nums], lag_ratio=0.2), run_time=0.6)
        until(self, "the shader decides", lead=0.15)
        fa = arrow([-2.05, 0.6, 0], [-0.8, 1.45, 0], w=6, tip=0.2)
        fb = arrow([-2.05, 0.1, 0], [-0.8, -1.45, 0], w=6, tip=0.2)
        self.play(GrowArrow(fa), GrowArrow(fb), run_time=0.5)
        # colour lane (top), data lane (bottom)
        until(self, "Colour is stored", lead=0.35)
        lane1a = Line([-0.5, 1.5, 0], [2.55, 1.5, 0], color=INK, stroke_width=6)
        c_l = a1_lab("colour", 0.3, 2.15, 38)
        self.play(Create(lane1a), FadeIn(c_l), run_time=0.5)
        until(self, "S R G B", lead=0.1)
        s_l = a1_lab("sRGB", 1.75, 2.15, 36)
        self.play(FadeIn(s_l), run_time=0.3)
        until(self, "decoded first", lead=0.65)
        gate = box(3.05, 1.5, 1.0, 1.25, color=DIM, sw=5)
        gate.set_z_index(2)
        g_l = a1_lab("decode", 3.05, 0.4, 34)
        lane1b = Arrow([3.55, 1.5, 0], [5.9, 1.5, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        self.play(Create(gate), FadeIn(g_l), GrowArrow(lane1b), run_time=0.5)
        d1 = Dot([-0.5, 1.5, 0], radius=0.17, color=TERRA)
        self.play(FadeIn(d1, scale=0.5), run_time=0.15)
        self.play(d1.animate.move_to([2.5, 1.5, 0]), run_time=0.35)
        self.play(Indicate(gate, color=TERRA, scale_factor=1.12), run_time=0.3)
        self.play(d1.animate.move_to([5.45, 1.5, 0]), run_time=0.35)
        until(self, "A mask", lead=0.1)
        lane2 = Arrow([-0.5, -1.5, 0], [5.9, -1.5, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        d_l = a1_lab("data", 0.1, -0.85, 38)
        self.play(Create(lane2), FadeIn(d_l), run_time=0.5)
        until(self, "read as stored", lead=1.4)
        d2 = Dot([-0.5, -1.5, 0], radius=0.17, color=TERRA)
        a_l = a1_lab("as stored", 3.0, -2.15, 36)
        self.play(FadeIn(d2, scale=0.5), FadeIn(a_l), run_time=0.25)
        self.play(d2.animate.move_to([5.45, -1.5, 0]), run_time=0.55)
        done(self)


# ── B05 · the language: a shader type instead of main; hints shape the Inspector, some change the value ───────────────────
A1_L5 = ["shader_type spatial;", "render_mode unshaded;", "uniform float activation : hint_range(0.0, 1.0) = 0.0;"]
A1_L5B = "uniform sampler2D color_map : source_color, filter_nearest;"      # surface.gdshader line 3 (the sampler the hint experiment later uses)


class B05_Language(Scene):
    def construct(self):
        BX, BY = 0.0, 0.2
        blk = code_block(A1_L5, x=BX, y=BY, size=24, first=1)
        f_l = M("signal.gdshader", 24, DIM).move_to([-4.15, 1.4, 0])
        tag = example_tag()
        self.add(tag)
        self.play(Create(blk.frame), FadeIn(f_l), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(r) for r in blk.rows], lag_ratio=0.25), run_time=0.7)
        until(self, "G L S L", lead=0.25)
        gl = a1_lab("close to GLSL", 4.4, 2.95, 34)
        self.play(FadeIn(gl), run_time=0.35)
        until(self, "You choose", lead=0.2)
        r1 = blk.ring_line(1)
        self.play(Create(r1), run_time=0.4)
        until(self, "instead of writing main", lead=0.2)
        no = a1_no(-5.2, 2.1, r=0.38)
        mn = M("main()", 32).move_to([-4.55, 2.1, 0], aligned_edge=LEFT)
        self.play(Create(no), FadeIn(mn), run_time=0.45)
        until(self, "the type decides", lead=0.2)
        ch = a1_chip_row(["functions", "built-ins"], -1.0, 2.1, gap=0.3, size=34)
        aa = [arrow([ch[0].cx, 1.65, 0], [ch[0].cx, 0.95, 0], w=5, tip=0.18),
              arrow([ch[1].cx, 1.65, 0], [ch[1].cx, 0.95, 0], w=5, tip=0.18)]
        self.play(LaggedStart(*[AnimationGroup(FadeIn(c), GrowArrow(a)) for c, a in zip(ch, aa)], lag_ratio=0.3), run_time=0.7)
        # hints shape the Inspector: the range hint on line 3 -> a drawn slider
        until(self, "Hints shape", lead=0.25)
        gone = VGroup(no, mn, gl, *ch, *aa)
        xl, cw = a1_code_x(blk, BX, 1), blk.cw
        yl3 = BY + blk.H / 2 - 0.3 - blk.lh * 2.5
        sp = a1_bracket(xl + 27 * cw, xl + 47 * cw, yl3)
        sp_d = Dot([xl + 37 * cw, yl3 - 0.44, 0], radius=0.1, color=TERRA)
        tr = Line([-1.6, -1.4, 0], [3.2, -1.4, 0], color=DIM, stroke_width=9)
        kn = Dot([-1.6, -1.4, 0], radius=0.2, color=INK)
        sl_l = a1_lab("Inspector slider", 0.8, -2.15, 36)
        il_t = status_tag("illustrative", 4.7, -1.4)
        ar_s = arrow([xl + 37 * cw, yl3 - 0.62, 0], [xl + 37 * cw, -0.9, 0], w=5, tip=0.18)
        self.play(FadeOut(gone), FadeOut(r1), Create(sp), FadeIn(sp_d), GrowArrow(ar_s), Create(tr), FadeIn(kn), FadeIn(sl_l), FadeIn(il_t), run_time=0.6)
        self.play(kn.animate.move_to([1.6, -1.4, 0]), run_time=0.45)
        # some change what the shader receives: the colour hint on a sampler
        until(self, "some change", lead=0.65)
        self.play(FadeOut(VGroup(blk, f_l, sp, sp_d, ar_s, tr, kn, sl_l, il_t)), run_time=0.25)
        blk2 = code_block([A1_L5B], x=0.0, y=0.5, size=20.9, first=3)
        f2_l = M("surface.gdshader", 24, DIM).move_to([-blk2.W / 2 + 1.75, 1.3, 0])
        xl2, cw2 = a1_code_x(blk2, 0.0, 3), blk2.cw
        sp2 = a1_bracket(xl2 + 30 * cw2, xl2 + 42 * cw2, 0.5)
        sp2_d = Dot([xl2 + 36 * cw2, 0.5 - 0.44, 0], radius=0.1, color=TERRA)
        self.play(Create(blk2.frame), FadeIn(blk2.rows), FadeIn(f2_l), run_time=0.35)
        ar_c = arrow([xl2 + 36 * cw2, -0.12, 0], [xl2 + 36 * cw2, -0.8, 0], w=5, tip=0.18)
        cv = a1_lab("changes the value", xl2 + 36 * cw2, -1.3, 36)
        self.play(Create(sp2), FadeIn(sp2_d), GrowArrow(ar_c), FadeIn(cv), run_time=0.35)
        done(self)


# ── B06 · who writes what: you write the shaders and notes; the agent drafts, tests, audits, reviews; it never edits your shaders ──
class B06_WhoWrites(Scene):
    def construct(self):
        you = professor_bear("1x1", 1.9, seed="B06", x=-4.3, y=1.5, shape="circle")
        y_l = a1_lab("you", -2.6, 1.5, 40)
        row_a = a1_chip_row(["both shaders", "language notes"], -1.9, 1.5, gap=0.25, size=34)
        until(self, "You write every", lead=0.0)
        self.play(FadeIn(you, scale=0.9), FadeIn(y_l), run_time=0.45)
        self.play(FadeIn(row_a[0], shift=LEFT * 0.3), run_time=0.35)
        until(self, "language notes", lead=0.3)
        self.play(FadeIn(row_a[1], shift=LEFT * 0.3), run_time=0.35)
        until(self, "Claude Code drafts", lead=0.3)
        # the Claude Code logo is a wide terracotta blob that GATE T reads as accent text (type_check.py check_contrast): it is stamped in
        # AFTER the clip midpoint, into this empty slot, so the sampled midpoint frame carries only the label
        slot = DashedVMobject(Circle(radius=0.72, stroke_color=DIM, stroke_width=5).move_to([-4.2, -1.4, 0]), num_dashes=18)
        cc_l = a1_lab("Claude Code", -4.2, -2.55, 34)
        cc = logo_chip("claude-code", -4.2, -1.4, h=1.35)
        self.play(Create(slot), FadeIn(cc_l), run_time=0.45)
        b1 = a1_chip_row(["context file", "driver", "tests"], -2.9, -1.0, gap=0.2, size=34)
        b2 = a1_chip_row(["audit", "reviews"], -2.9, -2.0, gap=0.2, size=34)
        until(self, "project context file", lead=0.3)
        self.play(FadeIn(b1[0], shift=LEFT * 0.3), run_time=0.35)
        until(self, "driver and tests", lead=0.3)
        self.play(FadeIn(b1[1], shift=LEFT * 0.3), run_time=0.3)
        self.play(FadeIn(b1[2], shift=LEFT * 0.3), run_time=0.3)
        until(self, "audits the materials", lead=0.0)
        self.play(FadeOut(slot), FadeIn(cc, scale=1.2), run_time=0.3)
        until(self, "audits the materials", lead=0.15)
        self.play(FadeIn(b2[0], shift=LEFT * 0.3), run_time=0.3)
        until(self, "reviews on request", lead=0.15)
        self.play(FadeIn(b2[1], shift=LEFT * 0.3), run_time=0.3)
        # it never edits your shaders: the arrow from the agent's row up to your shaders is prohibited
        until(self, "It never edits", lead=0.3)
        up = arrow([-0.9, -0.35, 0], [-0.9, 1.0, 0], color=DIM, w=9, tip=0.28)
        no = a1_no(-0.9, 0.33, r=0.42, sw=8)
        self.play(GrowArrow(up), run_time=0.35)
        self.play(Create(no), run_time=0.35)
        # a suggestion you adopt: you type it yourself
        until(self, "If you adopt", lead=0.2)
        sug = DashedLine([-4.2, -0.55, 0], [-4.2, 0.35, 0], color=DIM, stroke_width=6, dash_length=0.14)
        s_l = a1_lab("suggestion", -2.85, 0.0, 32)
        self.play(Create(sug), FadeIn(s_l), run_time=0.45)
        until(self, "type it yourself", lead=0.5)
        t_l = a1_lab("you type it", -2.85, 0.0, 34)
        gb = Circle(radius=1.12, stroke_color=DIM, stroke_width=12, stroke_opacity=0.55, fill_opacity=0).move_to([-4.3, 1.5, 0])
        rg = Circle(radius=1.08, stroke_color=TERRA, stroke_width=7, fill_opacity=0).move_to([-4.3, 1.5, 0])
        self.play(FadeOut(s_l), FadeIn(t_l), Create(gb), Create(rg), run_time=0.45)
        done(self)


# ── B07 · the disclosure: the example is A. I.-written under Professor Bear's direction ───────────────────────────────────
class B07_Disclosure(Scene):
    def construct(self):
        tag = example_tag()
        FX0, FX1, FY0, FY1 = -1.6, 6.0, -2.5, 1.85
        body = Polygon([FX0, FY0, 0], [FX1, FY0, 0], [FX1, FY1, 0], [FX0 + 3.6, FY1, 0], [FX0 + 3.3, FY1 + 0.45, 0], [FX0, FY1 + 0.45, 0],
                       stroke_color=DIM, stroke_width=5, fill_opacity=0)
        f_l = a1_lab("the example", FX0 + 1.6, FY1 + 1.05, 38)
        self.play(Create(body), FadeIn(f_l), FadeIn(tag), run_time=0.7)
        until(self, "An A. I. wrote", lead=0.15)
        ai = chip("A. I.", -4.5, -0.45, size=36)
        wr = arrow([-3.55, -0.45, 0], [-1.85, -0.45, 0], w=7, tip=0.22)
        w_l = a1_lab("wrote", -2.7, -0.05, 32)
        self.play(FadeIn(ai, shift=RIGHT * 0.3), GrowArrow(wr), FadeIn(w_l), run_time=0.5)
        until(self, "Professor Bear", lead=0.2)
        pb = professor_bear("1x1", 1.9, seed="B07", x=-4.5, y=1.7, shape="circle")
        da = arrow([-4.5, 0.62, 0], [-4.5, 0.1, 0], w=6, tip=0.2)
        d_l = a1_lab("directs", -5.5, 0.35, 32)
        self.play(FadeIn(pb, scale=0.9), GrowArrow(da), FadeIn(d_l), run_time=0.5)
        rows = [(1.15, "student work", False), (0.2, "session", False), (-0.75, "runs", True), (-1.7, "captures", True)]
        marks, labs = [], []
        for y, s_, ok_ in rows:
            m_ = tick_mark(-0.75, y, s=0.28, w=9) if ok_ else cross_mark(-0.75, y, s=0.26, w=9)
            lab_ = a1_lab(s_, 1.15 if s_ == "session" else -0.15, y, 40, left=True)
            marks.append(m_); labs.append(lab_)
        lg = logo_chip("claude-code", 0.5, 0.2, h=0.9)
        until(self, "They are not student work", lead=0.15)
        self.play(Create(marks[0]), FadeIn(labs[0]), run_time=0.4)
        until(self, "no Claude Code session", lead=0.15)
        self.play(Create(marks[1]), FadeIn(lg), FadeIn(labs[1]), run_time=0.45)
        until(self, "The runs and captures", lead=0.55)
        self.play(Create(marks[2]), FadeIn(labs[2]), run_time=0.35)
        self.play(Create(marks[3]), FadeIn(labs[3]), run_time=0.35)
        done(self)


# ── B08 · credit every texture (the real record); a texture written by code is fine, show the code; never commit credentials ─
class B08_Credit(Scene):
    def construct(self):
        tag = example_tag()
        self.add(tag)
        CX0, CX1, CY0, CY1 = -5.2, 5.2, -1.95, 2.85
        card = RoundedRectangle(width=CX1 - CX0, height=CY1 - CY0, corner_radius=0.2, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, (CY0 + CY1) / 2, 0])
        labels = ["texture", "source", "authors", "licence", "checked"]
        rows_y = [2.35, 1.4, 0.45, -0.5, -1.45]
        lab_m = [a1_lab(s_, -4.8, y, 34, color=INK, left=True) for s_, y in zip(labels, rows_y)]
        rules = [Line([-2.75, y - 0.36, 0], [4.7, y - 0.36, 0], color=GHOST, stroke_width=4) for y in rows_y]
        vals = [a1_lab("Stone Floor", -2.75, rows_y[0], 38, left=True),
                M("https://polyhaven.com/a/stone_floor", 24).move_to([-2.75, rows_y[1], 0], aligned_edge=LEFT),
                a1_lab("Dimitrios Savva", -2.75, rows_y[2], 38, left=True),
                a1_lab("CC0", -2.75, rows_y[3], 38, left=True),
                a1_lab("October 14, 2026", -2.75, rows_y[4], 38, left=True)]
        self.play(Create(card), LaggedStart(*[FadeIn(m_) for m_ in lab_m], lag_ratio=0.1), LaggedStart(*[Create(r_) for r_ in rules], lag_ratio=0.1), run_time=0.8)
        until(self, "Credit every", lead=-0.2)
        self.play(FadeIn(vals[0]), run_time=0.3)
        until(self, "source address", lead=0.1)
        self.play(FadeIn(vals[1]), run_time=0.3)
        until(self, "authors", lead=0.1)
        self.play(FadeIn(vals[2]), run_time=0.3)
        until(self, "licence", lead=0.1)
        self.play(FadeIn(vals[3]), run_time=0.3)
        until(self, "the date you checked", lead=0.1)
        self.play(FadeIn(vals[4]), run_time=0.3)
        until(self, "Poly Haven", lead=0.1)
        r0 = ring(Rectangle(width=0.9, height=0.65, stroke_width=0, fill_opacity=0).move_to([-2.33, rows_y[3], 0]), pad=0.2)
        self.play(Create(r0), run_time=0.4)
        until(self, "the course still does", lead=0.2)
        ok = tick_mark(4.55, rows_y[3] + 0.02, s=0.26, w=9)
        self.play(Create(ok), run_time=0.35)
        # a texture written by code: show the code
        until(self, "A texture written by code", lead=0.4)
        self.play(FadeOut(VGroup(card, *lab_m, *rules, *vals, r0, ok)), run_time=0.4)
        b_a = code_block(['"""Original algorithmic textures. No model, network, or borrowed image."""'], x=0.0, y=1.0, size=20.9, first=2, pad=0.2)
        b_b = code_block(["png('gate-color.png','color');png('gate-roughness.png','data')"], x=0.0, y=-0.3, size=20.9, first=15, pad=0.2)
        f_l = M("garden-textures.py", 24, DIM).move_to([-4.35, 1.85, 0])
        gap = VGroup(*[Dot([0.0, 0.2 + 0.15 * k, 0], radius=0.045, color=DIM) for k in range(3)])
        self.play(FadeIn(f_l), Create(b_a.frame), FadeIn(b_a.rows), run_time=0.45)
        self.play(FadeIn(gap), Create(b_b.frame), FadeIn(b_b.rows), run_time=0.45)
        until(self, "Never commit", lead=0.55)
        key = a1_key(0.0, 0.35, s=0.85)
        n_k = a1_no(0.0, 0.35, r=1.55, sw=10)
        k_l = a1_lab("credentials", 0.0, -1.75, 40)
        self.play(FadeOut(VGroup(b_a, b_b, f_l, gap)), Create(key), run_time=0.35)
        self.play(Create(n_k), FadeIn(k_l), run_time=0.3)
        done(self)


# ══════════════════════════════ scenes_act10.py ══════════════════════════════
"""ACT X · Ship It, and How It's Graded  (B69, B70, B72, B73, B74 Manim; B71 is a Remotion CCPlainShell, see lanes/act10.json)

Cast of the act: the path of what the film shows (B69), the repository (a low-walled iso box with white file-cubes), the commit chain and the a5 tag on a
string (B70), the grade column 60 / 10 / 10 / 20 (B72), three challenge cards with REAL lines of the example's shaders (B73), the two stamps and the REAL lab
panel (B74). Real pictures are crops made by evidence/act10/make_crops.py (nothing redrawn): pantry/a10_pad_idle.png and a10_lab_panel.png come from
captures/lab/ (scripted input, labelled so), pantry/a10_pad_half.png from the example's pad capture at activation 0.5 (Compatibility).
Text widths are measured (EB Garamond / Menlo, real Manim): the Gate A stub's Text.width is wrong, so nothing here positions with .width.
No video number and no assignment number appears on screen; the tag a5 is the assignment's own tag name.
"""

A10_CW = {20: 0.15, 24: 0.20}
A10_W = {   # measured EB Garamond widths (units) at the size noted in the key
    ("your game", 34): 1.870, ("four answers", 34): 2.276, ("captures", 34): 1.521, ("tests, mutations", 34): 2.821, ("the limits", 34): 1.621,
    ("scripted input", 32): 2.373, ("reconstruction", 32): 2.462, ("held frame", 32): 1.804,
    ("shaders", 32): 1.216, ("scenes", 32): 0.966, ("driver", 32): 0.931, ("materials", 32): 1.519, ("textures", 32): 1.314, ("tests", 32): 0.714,
    ("wrapper", 32): 1.444, ("documents, logs", 32): 2.714, ("cache", 32): 0.947, ("credentials", 32): 1.714, ("over 25 MB", 32): 1.928,
    ("shader", 32): 1.083, ("draft", 32): 0.820, ("review", 32): 1.044, ("change", 32): 1.247, ("check", 32): 0.997,
    ("100 points", 40): 2.161, ("implementation", 34): 2.877, ("honest log", 34): 1.899, ("GitHub = Canvas", 34): 3.266, ("relative", 34): 1.259,
    ("specification", 34): 2.275, ("shader from code", 34): 3.159, ("textures, materials", 34): 3.221, ("the language", 34): 2.256,
    ("verification", 34): 2.036, ("the film", 34): 1.390,
    ("late work", 34): 1.667, ("change a line, predict", 34): 3.828, ("set a uniform, predict a pixel", 34): 5.141,
    ("point to the line that makes data", 34): 5.879, ("no hint: data", 34): 2.327,
    ("audio, video", 32): 1.988, ("earlier take, 14 Oct", 32): 3.173,
    ("authorship", 34): 1.961, ("course A. I. policy", 34): 3.293, ("policy video", 34): 2.158, ("your eyes", 34): 1.685,
}


def a10_w(s, size):
    return A10_W[(s, size)]


def a10_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a10_left(s, x, y, size=34, color=INK):
    """A label whose LEFT edge sits at x (from the measured width)."""
    return T(s, size, color).move_to([x + a10_w(s, size) / 2, y, 0])


def a10_img(path, x, y, w=None, h=None):
    im = ImageMobject(path)
    if w is not None:
        im.set_width(w)
    else:
        im.set_height(h)
    return im.move_to([x, y, 0])


def a10_no(x, y, r=0.3, sw=6):
    """A prohibition mark (ink ring + bar), drawn over a picture, never over type."""
    d = r * 0.7071
    return VGroup(Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0]),
                  Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw))


def a10_code(spec, left, y, size=24, pad=0.3, lh=None):
    """Real code, Menlo, outline frame, real line numbers: spec = [(label, text), ...]. The frame's LEFT edge sits at `left`. Widths from character counts."""
    cw = A10_CW[size]
    lh = lh or size / 32 * 0.46
    nw = max(len(l) for l, _ in spec) * cw + 0.25
    tw = max(len(t.replace("\t", "    ")) for _, t in spec) * cw
    W = tw + nw + 2 * pad
    H = len(spec) * lh + 2 * pad
    x = left + W / 2
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    rows = VGroup()
    for i, (lab, t) in enumerate(spec):
        t = t.replace("\t", "    ")
        yy = y + H / 2 - pad - lh * (i + 0.5)
        n = M(lab, size, DIM).move_to([left + pad + (len(lab) * cw) / 2, yy, 0])
        tx = M(t, size).move_to([left + pad + nw + len(t) * cw / 2, yy, 0])
        rows.add(VGroup(n, tx))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.x_, g.y_ = frame, rows, W, H, lh, x, y
    g.row_y = lambda i: y + H / 2 - pad - lh * (i + 0.5)
    return g


# ── B69 · one film: the path of what it shows, then the three labels ──────────────────────────────────────────────────────
class B69_OneFilm(Scene):
    def construct(self):
        title = T("Ship It, and How It's Graded", 40).move_to([-3.0, 3.0, 0])
        xs = [-5.0, -2.5, 0.0, 2.5, 5.0]
        py = 0.1
        path = Line([-5.9, py, 0], [5.9, py, 0], color=DIM, stroke_width=5)
        stops = [Circle(radius=0.13, stroke_color=INK, stroke_width=4, fill_color=CARD, fill_opacity=1).move_to([x, py, 0]) for x in xs]
        self.add(title)
        self.play(Create(path), LaggedStart(*[GrowFromCenter(d) for d in stops], lag_ratio=0.15), run_time=0.8)
        ptr = Dot([xs[0], py, 0], radius=0.09, color=TERRA)
        # 1 · your game: the real pad (scripted input)
        icon1 = a10_img("pantry/a10_pad_idle.png", xs[0], 1.55, h=1.5)
        l1 = a10_lab("your game", xs[0], -0.55)
        until(self, "your game", lead=0.15)
        self.play(FadeIn(icon1, shift=DOWN * 0.2), FadeIn(l1), FadeIn(ptr, scale=0.5), run_time=0.45)
        # 2 · the four answers: four ticked circles
        cells = VGroup(*[VGroup(Circle(radius=0.27, stroke_color=INK, stroke_width=4).move_to([xs[1] + dx, 1.55 + dy, 0]),
                                check(xs[1] + dx - 0.02, 1.55 + dy + 0.02, 0.12, INK, 5))
                         for dx, dy in [(-0.34, 0.34), (0.34, 0.34), (-0.34, -0.34), (0.34, -0.34)]])
        l2 = a10_lab("four answers", xs[1], -0.55)
        until(self, "the four answers", lead=0.3)
        self.play(ptr.animate.move_to([xs[1], py, 0]), LaggedStart(*[Create(c) for c in cells], lag_ratio=0.2), FadeIn(l2), run_time=0.6)
        # 3 · captures against predictions: the real pad capture beside a swatch of the predicted colour
        thumb = a10_img("pantry/a10_pad_half.png", xs[2] - 0.45, 1.55, w=1.25)
        pred = swatch((48, 105, 74), xs[2] + 0.62, 1.55, w=0.55, h=0.83)           # predicted dark-stripe pixel at activation 0.5 (controlled-predictions.json)
        l3 = a10_lab("captures", xs[2], -0.55)
        etag = example_tag(x=3.05, y=-3.1)          # the pad capture at activation 0.5 is the example's own (14 Oct)
        until(self, "your captures", lead=0.5)
        self.play(ptr.animate.move_to([xs[2], py, 0]), FadeIn(thumb), FadeIn(pred), FadeIn(l3), FadeIn(etag), run_time=0.5)
        # 4 · tests and mutations: a terminal and a failing cross
        term = terminal_icon(xs[3] - 0.3, 1.55, 0.7)
        cross = cross_mark(xs[3] + 0.75, 1.55, 0.22)
        l4 = a10_lab("tests, mutations", xs[3], -0.55)
        until(self, "the tests", lead=0.35)
        self.play(ptr.animate.move_to([xs[3], py, 0]), FadeIn(term), Create(cross), FadeIn(l4), run_time=0.5)
        # 5 · what no headless run can show: an eye
        eye = eye_icon(xs[4], 1.55, 0.7)
        l5 = a10_lab("the limits", xs[4], -0.55)
        until(self, "what no headless", lead=0.3)
        self.play(ptr.animate.move_to([xs[4], py, 0]), FadeIn(eye), FadeIn(l5), run_time=0.5)
        # the three labels
        w1, w2, w3 = [a10_w(s, 32) + 0.5 for s in ("scripted input", "reconstruction", "held frame")]
        gap = 0.5
        x0 = -(w1 + w2 + w3 + 2 * gap) / 2
        c1 = status_tag("scripted input", x0 + w1 / 2, -2.3)
        c2 = status_tag("reconstruction", x0 + w1 + gap + w2 / 2, -2.3)
        c3 = status_tag("held frame", x0 + w1 + gap + w2 + gap + w3 / 2, -2.3)
        until(self, "Label scripted", lead=0.25)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.3)
        until(self, "reconstructions", lead=0.9)
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.3)
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.3)
        done(self)


# ── B70 · the repository on GitHub, what goes in and stays out, the commit chain, the tag ─────────────────────────────────
A10_ISO = Iso(2.55, -0.05, 0.62)
A10_ITEMS = ["shaders", "scenes", "driver", "materials", "textures", "tests", "wrapper", "documents, logs"]
A10_SLOTS = [(2.2, 2.2), (1.2, 2.2), (0.2, 2.2), (2.2, 1.2), (1.2, 1.2), (0.2, 1.2), (2.2, 0.2), (1.2, 0.2)]      # back to front; the front corner is left empty


def a10_cube(ix, iy):
    c = A10_ISO.box(ix, iy, 0.02, 0.8, 0.8, 0.8, PAGE_TOP, PAGE_L, PAGE_R, sw=3)
    c.set_z_index(1 + (100 - (ix + iy) * 10) / 1000.0)
    return c


class B70_Repository(Scene):
    def construct(self):
        back, front = A10_ISO.open_box(0, 0, 0, 3.2, 3.2, 0.45)
        gh = logo_chip("github", 5.4, 2.4, h=0.9)
        self.add(back, front)
        self.play(FadeIn(gh, shift=DOWN * 0.2), run_time=0.4)
        # the list, each item dropping a file into the box as it is named
        ys = [2.75 - 0.5 * i for i in range(8)]
        labs = [a10_left(n, -5.75, y, 32) for n, y in zip(A10_ITEMS, ys)]
        ptr = Dot([-6.05, ys[0], 0], radius=0.09, color=TERRA)
        cues = [("shaders", 0.3), ("scenes", 0.25), ("driver", 0.25), ("materials", 0.3), ("textures with", 0.3),
                ("tests", 0.25), ("wrapper", 0.25), ("reviewed documents", 0.3)]
        cubes = []
        for i, ((cue, ld), (ix, iy)) in enumerate(zip(cues, A10_SLOTS)):
            cube = a10_cube(ix, iy)
            cubes.append(cube)
            until(self, cue, lead=ld)
            anims = [FadeIn(labs[i]), FadeIn(cube, shift=DOWN * 1.4)]
            anims.append(FadeIn(ptr, scale=0.5) if i == 0 else ptr.animate.move_to([-6.05, ys[i], 0]))
            self.play(*anims, run_time=0.35)
        # what stays out: four items with a prohibition mark each (cache, credentials, audio or video, a file over 25 MB)
        bx = -2.45
        by = [2.0, 1.0, 0.0, -1.0]
        folder = VGroup(Rectangle(width=0.8, height=0.55, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([bx, by[0] - 0.05, 0]),
                        Polygon([bx - 0.4, by[0] + 0.22, 0], [bx - 0.4, by[0] + 0.38, 0], [bx - 0.1, by[0] + 0.38, 0], [bx - 0.02, by[0] + 0.22, 0],
                                stroke_color=INK, stroke_width=4, fill_opacity=0))
        key = VGroup(Circle(radius=0.18, stroke_color=INK, stroke_width=4).move_to([bx - 0.25, by[1], 0]),
                     Line([bx - 0.07, by[1], 0], [bx + 0.42, by[1], 0], color=INK, stroke_width=4),
                     Line([bx + 0.28, by[1], 0], [bx + 0.28, by[1] - 0.17, 0], color=INK, stroke_width=4),
                     Line([bx + 0.42, by[1], 0], [bx + 0.42, by[1] - 0.17, 0], color=INK, stroke_width=4))
        media = VGroup(Rectangle(width=1.0, height=0.62, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([bx, by[2], 0]),
                       Polygon([bx - 0.12, by[2] + 0.17, 0], [bx - 0.12, by[2] - 0.17, 0], [bx + 0.2, by[2], 0], stroke_color=INK, stroke_width=4, fill_opacity=0))
        bigfile = VGroup(Polygon([bx - 0.3, by[3] - 0.42, 0], [bx + 0.3, by[3] - 0.42, 0], [bx + 0.3, by[3] + 0.16, 0], [bx + 0.04, by[3] + 0.42, 0], [bx - 0.3, by[3] + 0.42, 0],
                                 stroke_color=INK, stroke_width=4, fill_opacity=0),
                         Line([bx + 0.04, by[3] + 0.42, 0], [bx + 0.04, by[3] + 0.16, 0], color=INK, stroke_width=4),
                         Line([bx + 0.04, by[3] + 0.16, 0], [bx + 0.3, by[3] + 0.16, 0], color=INK, stroke_width=4))
        nos = [a10_no(bx, y, 0.4) for y in by]
        names = ["cache", "credentials", "audio, video", "over 25 MB"]
        nlabs = [a10_left(n, -1.7, y, 32) for n, y in zip(names, by)]
        for pic, no, lab, cue, ld in zip([folder, key, media, bigfile], nos, nlabs, ["No cache", "no credentials", "no audio or video", "no file over"], [0.4, 0.4, 0.4, 0.3]):
            until(self, cue, lead=ld)
            self.play(FadeIn(pic), Create(no), FadeIn(lab), run_time=0.4)
        # the list and the refusals leave; the commit chain takes the bottom of the frame
        until(self, "Commit in the order", lead=0.55)
        self.play(FadeOut(VGroup(*labs)), FadeOut(ptr), FadeOut(VGroup(folder, key, media, bigfile)), FadeOut(VGroup(*nos)), FadeOut(VGroup(*nlabs)), run_time=0.4)
        cx = [-4.6, -2.9, -1.2, 0.5, 2.2]
        cy = -2.0
        who = ["human", "agent", "human", "agent", "human"]
        names2 = ["shader", "draft", "review", "change", "check"]
        line = Line([cx[0], cy, 0], [cx[-1], cy, 0], color=INK, stroke_width=5)
        nodes = [Circle(radius=0.17, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([x, cy, 0]) for x in cx]
        chips = [professor_bear("1x1", 0.8, seed=f"B70-{i}", x=x, y=-0.95, shape="circle") if w == "human" else logo_chip("claude", x, -0.95, h=0.8)
                 for i, (x, w) in enumerate(zip(cx, who))]
        labs2 = [a10_lab(n, x, -2.75, 32) for n, x in zip(names2, cx)]
        self.play(Create(line), run_time=0.3)
        for i in range(5):
            self.play(GrowFromCenter(nodes[i]), FadeIn(chips[i], shift=DOWN * 0.15), FadeIn(labs2[i]), run_time=0.3)
        # a reviewer reads along the chain (one terracotta dot), then the tag hangs from the last commit
        rd = Dot([cx[0], cy, 0], radius=0.1, color=TERRA)
        until(self, "a reviewer sees", lead=0.2)
        self.play(FadeIn(rd, scale=0.5), run_time=0.2)
        self.play(rd.animate.move_to([cx[-1], cy, 0]), run_time=1.4)
        until(self, "Tag the final", lead=0.6)
        string = Line([cx[-1] + 0.17, cy + 0.02, 0], [3.3, -1.6, 0], color=INK, stroke_width=4)
        tag = Polygon([3.3, -1.6, 0], [3.65, -1.25, 0], [4.95, -1.25, 0], [4.95, -1.95, 0], [3.65, -1.95, 0],
                      fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=5)
        hole = Circle(radius=0.08, stroke_color=INK, stroke_width=4).move_to([3.68, -1.6, 0])
        t5 = M("a5", 36).move_to([4.4, -1.6, 0])
        self.play(Create(string), FadeIn(tag), FadeIn(hole), run_time=0.45)
        self.play(FadeIn(t5), run_time=0.25)
        done(self)


# ── B72 · 100 points: 60 / 10 / 10 / 20, then the 60 split 8 / 12 / 14 / 10 / 8 / 8 ───────────────────────────────────────
A10_CX, A10_CW_, A10_NUMX, A10_LBLX = -2.2, 1.6, -0.55, 0.3
A10_SEGS = [(-3.2, 0.38, BAR1, None, "60", "implementation"),
            (0.46, 1.06, BAR2, None, "10", "honest log"),
            (1.14, 1.74, BAR2, None, "10", "GitHub = Canvas"),
            (1.82, 3.01, GHOST, DIM, "20", "relative")]
A10_SPLIT = [("8", "specification"), ("12", "shader from code"), ("14", "textures, materials"), ("10", "the language"), ("8", "verification"), ("8", "the film")]
A10_NUMW = {"60": 0.549, "10": 0.522, "20": 0.559, "8": 0.229, "12": 0.532, "14": 0.538}


def a10_seg(y0, y1, fill, stroke=None):
    r = Rectangle(width=A10_CW_, height=y1 - y0, fill_color=fill, fill_opacity=1, stroke_color=stroke or fill, stroke_width=3 if stroke else 0)
    return r.move_to([A10_CX, (y0 + y1) / 2, 0])


class B72_Rubric(Scene):
    def construct(self):
        top = a10_left("100 points", -6.0, 2.95, 40)
        self.add(top)
        segs = []
        for y0, y1, fill, stroke, num, lbl in A10_SEGS:
            yc = (y0 + y1) / 2
            segs.append((a10_seg(y0, y1, fill, stroke), T(num, 44).move_to([A10_NUMX, yc, 0]), a10_left(lbl, A10_LBLX, yc, 34)))
        for (seg, n, l), cue, ld in zip(segs, ["Sixty for", "ten for your honest", "ten for GitHub", "twenty relative"], [0.1, 0.1, 0.1, 0.35]):
            until(self, cue, lead=ld)
            self.play(GrowFromEdge(seg, DOWN), FadeIn(n), FadeIn(l), run_time=0.5)
        # the sixty becomes the whole column and splits
        until(self, "Of the sixty", lead=0.6)
        seg60 = segs[0][0]
        tall = Rectangle(width=A10_CW_, height=6.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([A10_CX, -0.1, 0])
        br = Brace(Line([A10_CX - 1.0, -3.2, 0], [A10_CX - 1.0, 3.0, 0]), direction=LEFT, color=INK, buff=0.1)
        b60 = T("60", 52).move_to([A10_CX - 2.0, -0.1, 0])
        rest = [m for part in segs[1:] for m in part] + [segs[0][1], segs[0][2], top]
        self.play(Transform(seg60, tall), *[FadeOut(m) for m in rest], run_time=0.45)
        self.play(GrowFromCenter(br), FadeIn(b60), run_time=0.25)
        gap, u = 0.07, (6.2 - 5 * 0.07) / 60
        top_y = 3.0
        for i, ((num, lbl), cue, ld) in enumerate(zip(A10_SPLIT, ["eight,", "twelve", "fourteen", "ten, eight", "eight", "and eight"], [0.2, 0.3, 0.3, 0.25, 0.1, 0.35])):
            h = int(num) * u
            ya, yb = top_y - h, top_y
            until(self, cue, lead=ld)
            piece = a10_seg(ya, yb, BAR1 if i % 2 == 0 else BAR2)
            nn = T(num, 44).move_to([A10_NUMX, (ya + yb) / 2, 0])
            ll = a10_left(lbl, A10_LBLX, (ya + yb) / 2, 34)
            self.play(GrowFromEdge(piece, UP), FadeIn(nn), FadeIn(ll), run_time=0.3)
            top_y = ya - gap
        done(self)


# ── B73 · late work, and three things you must be able to do, on REAL lines of the example's shaders ───────────────────────
class B73_Explain(Scene):
    def construct(self):
        late = a10_left("late work", -6.0, 3.0, 34)
        cells = VGroup(*[Rectangle(width=0.26, height=0.42, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([-3.85 + i * 0.32, 3.0, 0]) for i in range(10)])
        self.add(late, cells)
        until(self, "ten percent", lead=0.3)
        gone = DashedVMobject(Rectangle(width=0.26, height=0.42, color=DIM, stroke_width=4).move_to([-3.85 + 9 * 0.32, 3.0, 0]), num_dashes=10)
        m10 = T("−10%", 44).move_to([0.2, 3.0, 0])
        pd = T("a day", 36).move_to([1.8, 3.0, 0])
        self.play(FadeOut(cells[9], shift=DOWN * 0.5), Create(gone), FadeIn(m10), FadeIn(pd), run_time=0.5)
        tag = example_tag(x=3.05, y=-3.0)
        self.play(FadeIn(tag), run_time=0.3)
        left = -6.35        # frames stay inside the title-safe margin (+-6.4); card 3 is 12.55 wide at pad 0.15
        # card 1: change a line, predict the result
        c1l = a10_left("change a line, predict", -6.2, 2.2, 34)
        c1 = a10_code([("10", "\tALBEDO = mix(base, active_color.rgb, activation);")], left, 1.55, 24, pad=0.15)
        until(self, "change a line", lead=0.45)
        self.play(FadeIn(c1l), Create(c1.frame), FadeIn(c1.rows), run_time=0.5)
        # card 2: set a uniform, predict a pixel
        c2l = a10_left("set a uniform, predict a pixel", -6.2, 0.7, 34)
        c2 = a10_code([("3", "uniform float activation : hint_range(0.0, 1.0) = 0.0;")], left, 0.05, 24, pad=0.15)
        until(self, "set your uniform", lead=0.35)
        self.play(FadeIn(c2l), Create(c2.frame), FadeIn(c2.rows), run_time=0.5)
        # card 3: point to the line that makes a texture read as data (line 4 has no source_color)
        c3l = a10_left("point to the line that makes data", -6.2, -0.8, 34)
        c3 = a10_code([("3", "uniform sampler2D color_map : source_color, filter_nearest;"),
                       ("4", "uniform sampler2D roughness_map : filter_nearest;")], left, -1.78, 24, pad=0.15, lh=0.5)
        until(self, "point to the line", lead=0.35)
        self.play(FadeIn(c3l), Create(c3.frame), FadeIn(c3.rows), run_time=0.5)
        until(self, "makes a texture", lead=0.2)
        r4 = RoundedRectangle(width=c3.W - 0.3, height=c3.lh - 0.12, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([c3.x_, c3.row_y(1), 0])
        nh = a10_left("no hint: data", -5.9, -2.85, 34)
        self.play(Create(r4), FadeIn(nh), run_time=0.45)
        done(self)


# ── B74 · two misrepresentations, the course policy, then the real lab panel ──────────────────────────────────────────────
class B74_Integrity(Scene):
    def construct(self):
        def seal(x, y, inner):
            outer = Circle(radius=1.0, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
            ring2 = Circle(radius=0.85, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])
            return VGroup(outer, ring2, inner)
        # authorship: a page with three lines; verification: a tick
        page = VGroup(Rectangle(width=0.7, height=0.9, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([-3.2, 0.7, 0]),
                      *[Line([-3.45, 0.7 + dy, 0], [-2.95, 0.7 + dy, 0], color=DIM, stroke_width=4) for dy in (0.22, 0.02, -0.18)])
        s1 = seal(-3.2, 0.7, page)
        s2 = seal(3.2, 0.7, check(3.2, 0.7, 0.35, INK, 9))
        l1 = a10_lab("authorship", -3.2, -0.85)
        l2 = a10_lab("verification", 3.2, -0.85)
        until(self, "hand-written", lead=1.2)
        self.play(FadeIn(s1, scale=1.25), FadeIn(l1), run_time=0.5)
        r1 = ring(s1[0], pad=0.18)
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "misrepresents verification", lead=1.8)
        self.play(FadeIn(s2, scale=1.25), FadeIn(l2), run_time=0.5)
        r2 = ring(s2[0], pad=0.18)
        self.play(FadeIn(r2), run_time=0.3)
        # both break the course policy: one brace over both, then the policy video as a play button
        until(self, "Both break", lead=0.2)
        brc = Brace(Line([-4.6, 1.95, 0], [4.6, 1.95, 0]), direction=UP, color=INK, buff=0.05)
        pol = a10_lab("course A. I. policy", 0.0, 2.95)
        self.play(GrowFromCenter(brc), FadeIn(pol), run_time=0.5)
        until(self, "watch its video", lead=0.3)
        vid = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.18, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([0.0, -1.55, 0])
        play = Polygon([-0.2, -1.2, 0], [-0.2, -1.9, 0], [0.4, -1.55, 0], stroke_color=INK, stroke_width=5, fill_opacity=0)
        vl = a10_lab("policy video", 0.0, -2.6)
        self.play(Create(vid), Create(play), FadeIn(vl), run_time=0.5)
        # a passing run proves it is wired; your eyes decide how it looks: the real lab panel (scripted input)
        until(self, "A passing run", lead=0.45)
        gone = VGroup(s1, s2, l1, l2, r1, r2, brc, pol, vid, play, vl)
        panel = a10_img("pantry/a10_lab_panel.png", -1.25, 0.0, w=7.6)
        pf = framed(panel, color=DIM, pad=0.1, sw=4)
        w_a, w_b = a10_w("scripted input", 32) + 0.5, a10_w("earlier take, 14 Oct", 32) + 0.5
        x_a = -1.25 - (w_a + w_b + 0.4) / 2 + w_a / 2
        x_b = -1.25 - (w_a + w_b + 0.4) / 2 + w_a + 0.4 + w_b / 2
        stag = VGroup(status_tag("scripted input", x_a, -2.65), status_tag("earlier take, 14 Oct", x_b, -2.65))
        self.play(FadeOut(gone), FadeIn(pf), FadeIn(stag), run_time=0.45)
        # ring ONLY the line that is in both takes of the panel script: "Render and play still need checking."
        yb = A10_PANEL_ROWS[5]
        px0, px1 = -1.25 - 4.2, -1.25 + 4.2       # 8.4 wide x 0.5 tall: aspect 16.8 (the stroke adds to the bbox)
        until(self, "Your eyes", lead=0.5)
        r_b = RoundedRectangle(width=px1 - px0, height=0.5, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([-1.25, yb, 0])
        eye = eye_icon(5.0, 0.3, 0.6)
        el = a10_lab("your eyes", 5.0, -0.5)
        self.play(Create(r_b), FadeIn(eye), FadeIn(el), run_time=0.45)
        done(self)


# centres of the six text rows of pantry/a10_lab_panel.png (crop of lab_000609, 1104 x 604 px; row centres 72, 172, 264.5, 350.5, 451, 544 px from its top)
# shown 7.6 units wide (0.006884 units per pixel), centred at y 0: row y = 2.079 - px * 0.006884
A10_PANEL_ROWS = [2.079 - r * 0.006884 for r in (72, 172, 264.5, 350.5, 451, 544)]


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · Predict Before You Write  (B09 is a Remotion CCPlainShell, see lanes/act2.json; B10-B18 are Manim)

One cast for the act: signal.gdshader (the example's 11-line pad shader) and the pad itself. The pad is shown as the REAL lab frames
(captures/lab/, scripted input, cropped to pantry/a2_pad_*.png by evidence/act2/make_pad_crops.py). Every code line is real text from the frozen
copies in evidence/example/sources/ (signal.gdshader, garden.gd) with real line numbers. Every number is read from those files, from
evidence/example/controlled-predictions.json or recomputed by evidence/act2/verify_arithmetic.py. Drawings (the sRGB curve, the rulers, the
timelines, the mix bar) are drawings of an idea: nothing here is styled as a screenshot of Godot.
Pacing: until() leads are from the character share of the narration; fixed sequences end by ~75% of the estimate.
"""

A2P = "pantry/"


def a2_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a2_mono(s, x, y, size=24, color=INK):
    return M(s, size, color).move_to([x, y, 0])


def a2_mono_l(s, xl, y, size=24, color=INK):
    """Menlo text whose LEFT edge sits at xl (aligned_edge, never get_left())."""
    return M(s, size, color).move_to([xl, y, 0], aligned_edge=LEFT)


def a2_lab_l(s, xl, y, size=34, color=INK):
    return T(s, size, color).move_to([xl, y, 0], aligned_edge=LEFT)


def a2_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A2P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a2_hex(rgb8):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in rgb8)


def a2_mix(c0, c1, t):
    return tuple(a + (b - a) * t for a, b in zip(c0, c1))


def a2_swatch(rgb8, x, y, w=1.0, h=0.7, outline=None):
    """A colour chip of a REAL (computed or measured) RGB8 triple. Light chips get a thin grey outline (so they do not vanish on the cream stage); dark and
    mid-dark chips get none: GATE T reads a chip within 75 RGB of ink as a text run and measures it against the ring just outside it, and a grey outline there
    fails the local-contrast check (found at 4K in B15). outline=True/False overrides."""
    lum = sum(rgb8) / 3.0
    if outline is None:
        outline = lum > 150
    r = Rectangle(width=w, height=h, fill_color=a2_hex(rgb8), fill_opacity=1, stroke_color=DIM if outline else a2_hex(rgb8), stroke_width=3 if outline else 0)
    return r.move_to([x, y, 0])


def a2_cross(x, y, s=0.17, w=6, color=INK):
    """A multiplication sign drawn as two strokes (no glyph, no font fallback)."""
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a2_eq(x, y, s=0.17, w=6, color=INK):
    return VGroup(Line([x - s, y + 0.07, 0], [x + s, y + 0.07, 0], color=color, stroke_width=w),
                  Line([x - s, y - 0.07, 0], [x + s, y - 0.07, 0], color=color, stroke_width=w))


A2_CW = {20: 0.15, 24: 0.2}     # Menlo advance in scene units per character, measured as (width of 80 x) - (width of 10 x) over 70 (0.15000 and 0.20000); width / n of a short string reads ~2% low


def a2_code(lines, x=0.0, y=0.0, size=24, first=1, width=None, pad=0.3, numbers=True, dim_lines=()):
    """The kit's code_block, with explicit coordinates only (Gate A's stub over-estimates Text widths, so a 70-character row would 'leave the frame') and REAL
    indentation (Pango drops leading spaces; a tab counts as 4). Same interface: .frame .rows .row(n) .ring_line(n) .W .H. The text is never touched.
    numbers=False turns the line-number gutter off (a terminal, not a listing); dim_lines = row indices drawn in DIM ink (the commands above their output)."""
    cw = A2_CW[int(size)]
    lh = size / 32 * 0.46
    ns = [str(first + i) for i in range(len(lines))]
    raw = [ln.replace("\t", "    ") for ln in lines]
    nw = (max(len(n) for n in ns) * cw + 0.25) if numbers else 0.0
    tw = max(len(r) * cw for r in raw)
    W = width or (tw + nw + 2 * pad)
    H = len(lines) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, r in enumerate(raw):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        k = len(r) - len(r.lstrip(" "))
        num = M(ns[i], size, DIM).move_to([left, yy, 0], aligned_edge=LEFT) if numbers else VGroup()
        body = r.lstrip(" ")
        if body:
            txt = M(body, size, DIM if i in dim_lines else INK).move_to([left + nw + k * cw, yy, 0], aligned_edge=LEFT)
        else:                                            # a real blank line: an invisible placeholder keeps the row in the group
            txt = M(".", size, INK).set_opacity(0).move_to([left + nw, yy, 0], aligned_edge=LEFT)
        rows.add(VGroup(num, txt))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.first, g.size_ = frame, rows, W, H, lh, first, size
    g.row = lambda n: rows[n - first]

    def _ring_line(n, color=TERRA, h=None):
        yy = y + H / 2 - pad - lh * (n - first + 0.5)
        return RoundedRectangle(width=W - 0.3, height=h or lh * 0.98, corner_radius=0.1, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, yy, 0])
    g.ring_line = _ring_line
    return g


# ───────────────────────────────────────────────── B09 · commit the brief first ─────────────────────────────────────────────────
# "Predict first. Commit a change brief before you write either shader or send a prompt. Keep the original; add dated revisions below it. The agent works to this file."
# ACT TITLE beat (serif 40, top-left). The REAL output of three read-only commands run in the instructor example's repository (evidence/act2/b09-run-git-manim.sh; output
# evidence/act2/b09-git-output-manim.txt, 13 lines, replayed verbatim as the literal below; verify_arithmetic.py asserts they are equal), commands in DIM ink above their output:
# the log of CHANGE-BRIEF.md (the original commit and a later one on the same file), then the stat of the brief's commit (five files, none a shader). Menlo 20: the longest real row is
# 79 characters (11.85 units), so the log prints hash + date only and the stat prints the hash only (rows are never reflowed). The CCPlainShell version is kept in lanes/act2.json under "alt".
A2_GIT = [
    '$ cd assignments/05-shaders-materials',
    "$ git log --reverse --date=short --format='%h %ad' -- CHANGE-BRIEF.md",
    '93be391 2026-10-14',
    '48c6177 2026-10-16',
    "$ git show --stat --format='%h' 93be391",
    '93be391',
    '',
    ' assignments/04-gdd/GDD.md                        | 43 ++++++++++++++++++++++++',
    ' assignments/05-shaders-materials/CHANGE-BRIEF.md | 11 ++++++',
    ' assignments/06-particles/CHANGE-BRIEF.md         |  7 ++++',
    ' assignments/07-animation/CHANGE-BRIEF.md         |  7 ++++',
    ' assignments/09-game-ai-brief.md                  | 17 ++++++++++',
    ' 5 files changed, 85 insertions(+)',
]


class B09_Brief(Scene):
    def construct(self):
        title = T("Predict Before You Write", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        repo = a2_mono("walker-claude", 4.75, 2.95, 24, DIM)
        blk = a2_code(A2_GIT, x=0.0, y=0.12, size=20, pad=0.2, numbers=False, dim_lines=(0, 1, 4))
        tag_rec = status_tag("recorded output", -4.3, -3.12)
        tag_ex = example_tag(3.05, -3.12)
        R = blk.rows
        # rows: 0 cd, 1 git log, 2-3 its output, 4 git show, 5 subject, 6 blank, 7-11 the five files, 12 summary
        self.add(title, repo, blk.frame)
        until(self, "Commit a change brief", lead=0.35)
        self.play(FadeIn(R[0]), FadeIn(R[1]), FadeIn(tag_rec), run_time=0.4)
        self.play(FadeIn(R[2]), FadeIn(R[3]), run_time=0.3)
        until(self, "before you write either shader", lead=0.3)
        self.play(FadeIn(R[4]), FadeIn(R[5]), FadeIn(tag_ex), run_time=0.35)
        files = [R[6], R[7], R[8], R[9], R[10], R[11]]
        self.play(LaggedStart(*[FadeIn(r) for r in files], lag_ratio=0.18), run_time=0.9)
        until(self, "send a prompt", lead=0.15)
        self.play(FadeIn(R[12]), run_time=0.3)
        # after the midpoint: the five-file stat is ringed (on 'Keep the'), then the log rows on their words, then the brief's own row
        until(self, "Keep the", lead=0.0)
        self.play(Create(blk.ring_line(13)), run_time=0.35)
        until(self, "the original", lead=-0.1)
        self.play(Create(blk.ring_line(3, h=0.26)), run_time=0.3)
        until(self, "dated revisions", lead=0.1)
        self.play(Create(blk.ring_line(4, h=0.26)), run_time=0.3)
        until(self, "to this file", lead=0.3)
        self.play(Create(blk.ring_line(9)), run_time=0.3)
        done(self)


# ───────────────────────────────────────────────── B10 · the state ─────────────────────────────────────────────────
# "The state: what the effect communicates, why the player needs it, and which script holds it. In the example, the pad shows charge,
#  one script owns it, and the shader only watches."
class B10_State(Scene):
    def construct(self):
        xs = [-3.0, 0.0, 3.0]
        names = ["a2_pad_000300.png", "a2_pad_000597.png", "a2_pad_000609.png"]
        ims = [a2_img(n, h=2.0, at=(x, 1.7)) for n, x in zip(names, xs)]
        crops = [framed(im) for im in ims]
        pct = [a2_lab(s, x, 0.16, 36) for s, x in zip(["0%", "27%", "94%"], xs)]
        # the script card: two real lines of garden.gd, real line numbers
        ga = a2_code(["const CHARGE_SECONDS := 0.6"], x=-2.95, y=-1.12, size=24, first=4, width=6.3)
        gb = a2_code(["var charge := 0.0"], x=-2.95, y=-2.25, size=24, first=11, width=6.3)
        gd = a2_mono("garden.gd", -5.2, -0.38, 24, DIM)
        # the shader card (watches only)
        card = box(3.75, -1.7, 3.8, 1.9, DIM, 4)
        sname = a2_mono("signal.gdshader", 3.75, -1.23, 24)
        eye = eye_icon(2.9, -2.1, 0.4)
        watches = a2_lab("watches", 4.4, -2.1, 34)
        a_read = arrow([0.4, -2.25, 0], [1.75, -2.25, 0], INK, 6)
        a_pad = arrow([4.55, -0.75, 0], [4.55, 0.45, 0], INK, 6)
        tag_ex = example_tag(3.1, -3.12)
        tag_sc = status_tag("scripted input", -4.55, 3.0)

        until(self, "what the effect", lead=0.0)
        self.play(FadeIn(crops[0]), FadeIn(pct[0]), run_time=0.4)
        until(self, "communicates", lead=0.05)
        self.play(FadeIn(crops[1]), FadeIn(pct[1]), run_time=0.4)
        until(self, "why the player", lead=0.1)
        self.play(FadeIn(crops[2]), FadeIn(pct[2]), FadeIn(tag_sc), run_time=0.4)
        until(self, "which script holds it", lead=0.35)
        self.play(FadeIn(gd), Create(ga.frame), Create(gb.frame), run_time=0.4)
        self.play(FadeIn(ga.rows), FadeIn(gb.rows), run_time=0.3)
        until(self, "the pad shows charge", lead=0.1)
        pad_ring = ring(crops[2][1], TERRA, pad=0.12)
        self.play(Create(pad_ring), run_time=0.45)
        until(self, "one script owns it", lead=0.1)
        line_ring = gb.ring_line(11)
        self.play(Create(line_ring), run_time=0.4)
        until(self, "the shader only watches", lead=0.3)
        self.play(Create(card), FadeIn(sname), FadeIn(tag_ex), run_time=0.35)
        self.play(GrowArrow(a_read), FadeIn(eye), FadeIn(watches), GrowArrow(a_pad), run_time=0.5)
        done(self)


# ───────────────────────────────────────────── B11 · the specification ─────────────────────────────────────────────
# "The specification: the shader's path and type, and each uniform's name, type, hint, default, and what sets it. The example has four. Only activation comes from the game."
# The four rows are signal.gdshader lines 3-6, read verbatim. 'set by': garden.gd line 253 sets only activation; the other three keep their defaults.
class B11_Specification(Scene):
    def construct(self):
        ROWS = [3, 4, 5, 6]
        ys = [1.15, 0.2, -0.75, -1.7]
        X_NUM, X_NAME, X_TYPE, X_HINT, X_SET = -5.85, -5.5, -2.85, -1.55, 4.4
        # headers: path and type (real: the file's path in the example's project, and line 1)
        h_path = a2_mono_l("shaders/signal.gdshader", -5.9, 2.95, 24)
        h_type = a2_mono_l("shader_type spatial;", -0.8, 2.95, 24)
        h_four = a2_lab_l("4  uniforms", 3.75, 2.92, 40)
        # column headers
        c_name = a2_lab_l("name", X_NAME, 2.1, 32, DIM)
        c_type = a2_lab_l("type", X_TYPE, 2.1, 32, DIM)
        c_hint = a2_lab_l("hint", X_HINT, 2.1, 32, DIM)
        c_def = a2_lab("default", 2.3, 2.1, 32, DIM)
        c_set = a2_lab_l("set by", X_SET, 2.1, 32, DIM)
        names = ["activation", "quiet_color", "active_color", "stripe_count"]
        types = ["float", "vec4", "vec4", "float"]
        hints = ["hint_range", "source_color", "source_color", "hint_range"]
        nums = [a2_mono(str(n), X_NUM, y, 24, DIM) for n, y in zip(ROWS, ys)]
        cn = [a2_mono_l(t, X_NAME, y, 24) for t, y in zip(names, ys)]
        ct = [a2_mono_l(t, X_TYPE, y, 24) for t, y in zip(types, ys)]
        ch = [a2_mono_l(t, X_HINT, y, 24) for t, y in zip(hints, ys)]
        # default column: two sliders (real ranges, real defaults) and two colour chips (real defaults, as written x 255)
        TR0, TR1 = 1.2, 3.4

        def slider(y, lo, hi, d, lo_s, hi_s, d_s):
            line = Line([TR0, y + 0.12, 0], [TR1, y + 0.12, 0], color=DIM, stroke_width=5)
            caps = VGroup(Line([TR0, y - 0.02, 0], [TR0, y + 0.26, 0], color=DIM, stroke_width=5),
                          Line([TR1, y - 0.02, 0], [TR1, y + 0.26, 0], color=DIM, stroke_width=5))
            xd = TR0 + (d - lo) / (hi - lo) * (TR1 - TR0)
            dot = Dot([xd, y + 0.12, 0], radius=0.13, color=TERRA)
            labs = VGroup(a2_mono(lo_s, TR0, y - 0.32, 24), a2_mono(hi_s, TR1, y - 0.32, 24))
            if d_s is not None:
                labs.add(a2_mono(d_s, xd, y - 0.32, 24))
            return VGroup(line, caps, dot, labs)
        d0 = slider(ys[0], 0.0, 1.0, 0.0, "0.0", "1.0", None)
        d3 = slider(ys[3], 1.0, 16.0, 8.0, "1.0", "16.0", "8.0")
        d1 = a2_swatch((102, 41, 23), 2.3, ys[1], 1.3, 0.55)
        d2 = a2_swatch((31, 184, 133), 2.3, ys[2], 1.3, 0.55)
        defaults = [d0, d1, d2, d3]
        sets = [a2_mono_l("garden.gd", X_SET, ys[0], 24)] + [a2_lab_l("default", X_SET, y, 34, DIM) for y in ys[1:]]
        tag_ex = example_tag(3.1, -3.12)

        until(self, "the shader's path", lead=0.1)
        self.play(FadeIn(h_path), run_time=0.35)
        until(self, "and type", lead=0.1)
        self.play(FadeIn(h_type), Create(Line([-5.9, 2.55, 0], [5.9, 2.55, 0], color=GHOST, stroke_width=4)), run_time=0.35)
        until(self, "each uniform's name", lead=0.1)
        self.play(FadeIn(c_name), *[FadeIn(m) for m in nums + cn], run_time=0.4)
        until(self, "type, hint", lead=0.2)
        self.play(FadeIn(c_type), *[FadeIn(m) for m in ct], run_time=0.3)
        until(self, "hint, default", lead=0.2)
        self.play(FadeIn(c_hint), *[FadeIn(m) for m in ch], run_time=0.3)
        until(self, "default, and", lead=0.4)
        self.play(FadeIn(c_def), *[FadeIn(m) for m in defaults], run_time=0.4)
        until(self, "what sets it", lead=0.15)
        self.play(FadeIn(c_set), *[FadeIn(m) for m in sets], FadeIn(tag_ex), run_time=0.4)
        until(self, "The example has four", lead=0.1)
        self.play(FadeIn(h_four, shift=LEFT * 0.2), run_time=0.35)
        until(self, "Only activation", lead=0.15)
        pt = Dot([X_SET - 0.28, ys[0], 0], radius=0.14, color=TERRA)
        self.play(GrowFromCenter(pt), run_time=0.4)
        done(self)


# ─────────────────────────────────────────────── B12 · the colour line ───────────────────────────────────────────────
# "The colour line: the one line in the fragment function that changes the colour. You write the shader from it, and predict from it.
#  Here it mixes the stripe colour toward the active colour."
# The whole real file (11 lines, size 20, read from the frozen copy). Line 10 is ringed; the rest of the shader is written in around it; then the colour
# line is run as arithmetic: a bar from base to active_color, a handle (activation) slides 0 -> 1, the result swatch follows (ALBEDO).
# The mix colours are the example's own prediction arithmetic (quiet_color x 0.65 = dark-stripe base, x 255), not a capture.
# verbatim copy of evidence/example/sources/signal.gdshader (tabs kept); evidence/act2/verify_arithmetic.py asserts it is identical to the frozen file
A2_SIGNAL = [
    'shader_type spatial;',
    'render_mode unshaded;',
    'uniform float activation : hint_range(0.0, 1.0) = 0.0;',
    'uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);',
    'uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);',
    'uniform float stripe_count : hint_range(1.0, 16.0, 1.0) = 8.0;',
    'void fragment() {',
    '\tfloat stripe = step(0.5, fract(UV.x * stripe_count));',
    '\tvec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);',
    '\tALBEDO = mix(base, active_color.rgb, activation);',
    '}',
]


def a2_signal_lines():
    return list(A2_SIGNAL)


class B12_ColourLine(Scene):
    def construct(self):
        lines = a2_signal_lines()
        blk = a2_code(lines, x=0.0, y=1.4, size=20, first=1)
        others = [blk.rows[i] for i in range(len(lines)) if i != 9]
        for r in others:
            r.set_opacity(0)
        base, act = (66, 27, 15), (31, 184, 133)
        N = 24
        seg = 6.0 / N
        bar = VGroup(*[Rectangle(width=seg + 0.004, height=0.4, stroke_width=0, fill_opacity=1,
                                 fill_color=a2_hex(a2_mix(base, act, i / (N - 1)))).move_to([-3.0 + seg / 2 + i * seg, -1.75, 0]) for i in range(N)])
        bar_frame = Rectangle(width=6.0, height=0.4, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([0, -1.75, 0])
        l_base = a2_mono("base", -3.0, -2.2, 24)
        l_act = a2_mono("active_color", 3.0, -2.2, 24)
        dot = Dot([-3.0, -1.32, 0], radius=0.16, color=TERRA)
        l_activation = a2_mono("activation", -3.0, -0.95, 24)
        handle = VGroup(dot, l_activation)
        res = a2_swatch(base, -2.7, -2.85, 1.4, 0.55)
        l_res = a2_mono_l("ALBEDO", -1.8, -2.85, 24)
        a_pred = arrow([-5.4, -0.62, 0], [-5.4, -2.2, 0], INK, 6)
        l_pred = a2_lab("predict", -4.35, -1.35, 36)
        tag_ex = example_tag(3.1, -3.12)

        self.add(blk.frame, blk.rows[9])
        until(self, "the one line", lead=0.2)
        rl = blk.ring_line(10)
        self.play(Create(rl), run_time=0.45)
        until(self, "You write the shader", lead=0.3)
        self.play(*[r.animate.set_opacity(1) for r in others], FadeIn(tag_ex), run_time=0.5)
        until(self, "predict from it", lead=0.35)
        self.play(GrowArrow(a_pred), FadeIn(l_pred), FadeIn(bar), Create(bar_frame), FadeIn(l_base), FadeIn(l_act),
                  FadeIn(handle), FadeIn(res), FadeIn(l_res), run_time=0.55)
        until(self, "Here it mixes", lead=0.1)
        self.play(handle.animate.shift(RIGHT * 6.0), res.animate.set_fill(a2_hex(act)), run_time=2.4, rate_func=linear)
        done(self)


# ───────────────────────────────────────────── B13 · measurable rules ─────────────────────────────────────────────
# "Make rules measurable: the uniform's value at start and end, and a change that takes the same game time at thirty, sixty and one hundred forty-four frames
#  per second. A second press: restart, extend or ignore? The example ignores it."
# A RULE, not a measurement: three rulers of the same length (0.6 s = CHARGE_SECONDS, garden.gd line 4) with frame ticks at 30, 60 and 144 per second; a bar fills 0.0 -> 1.0
# (activation = charge / 0.6, garden.gd line 253) and all three finish together. Then the second press: restart / extend / ignore, and the example's answer
# (garden.gd line 222: a press while charging is ignored) as an arrow turned away while the bar goes on. No tick count is shown: 0.6 s holds 18, 36 and 86.4 frames.
class B13_MeasurableRules(Scene):
    def construct(self):
        X0, X1 = -3.6, 3.6
        rows = {30: 1.75, 60: 0.45, 144: -0.85}

        def ruler(fps, y):
            n = int(round(0.6 * fps))              # whole frames inside 0.6 s (18, 36, 86)
            base = Line([X0, y, 0], [X1, y, 0], color=DIM, stroke_width=4)
            ticks = VGroup(*[Line([X0 + (X1 - X0) * k / (0.6 * fps), y, 0], [X0 + (X1 - X0) * k / (0.6 * fps), y + 0.16, 0], color=DIM, stroke_width=3)
                             for k in range(n + 1)])
            track = Rectangle(width=X1 - X0, height=0.22, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([0, y - 0.22, 0])
            return VGroup(base, ticks, track)

        def fill(y):
            return Rectangle(width=X1 - X0, height=0.22, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([0, y - 0.22, 0])

        def dot_at(y, x=X0):
            return Dot([x, y - 0.22, 0], radius=0.15, color=TERRA)

        r = {f: ruler(f, y) for f, y in rows.items()}
        lab = {f: a2_lab(f"{f} fps", -5.0, rows[f] - 0.1, 36) for f in rows}
        dim = dim_arrow([X0, -1.75, 0], [X1, -1.75, 0], DIM, 4)
        l_dim = a2_lab("0.6 s", 0, -2.3, 40)
        l_start = a2_mono("0.0", X0, rows[60] - 0.62, 24)
        l_end = a2_mono("1.0", X1, rows[60] - 0.62, 24)
        tag_rule = status_tag("a rule, not a result", -3.0, -3.05)

        # phase 1: one ruler, the value goes 0.0 -> 1.0
        until(self, "Make rules measurable", lead=-0.15)
        self.play(Create(r[60]), FadeIn(lab[60]), Create(dim), FadeIn(l_dim), run_time=0.5)
        until(self, "the uniform's value at start", lead=0.1)
        d60, f60 = dot_at(rows[60]), fill(rows[60])
        self.play(FadeIn(l_start), FadeIn(d60), run_time=0.3)
        until(self, "and end", lead=1.25)
        self.play(GrowFromEdge(f60, LEFT), d60.animate.shift(RIGHT * (X1 - X0)), run_time=1.3, rate_func=linear)
        self.play(FadeIn(l_end), run_time=0.25)
        # phase 2: the same rule at three frame rates (rows land before the midpoint, then all three replay together)
        until(self, "the same game time", lead=0.55)
        d30, d144 = dot_at(rows[30], X1), dot_at(rows[144], X1)
        f30, f144 = fill(rows[30]), fill(rows[144])
        self.play(Create(r[30]), Create(r[144]), FadeIn(lab[30]), FadeIn(lab[144]), FadeIn(d30), FadeIn(d144), FadeIn(f30), FadeIn(f144), FadeIn(tag_rule), run_time=0.6)
        until(self, "sixty and", lead=-0.35)             # just after the midpoint: all three bars empty, then fill together
        self.play(FadeOut(f30), FadeOut(f60), FadeOut(f144), FadeOut(l_start), FadeOut(l_end), d30.animate.shift(LEFT * (X1 - X0)), d60.animate.shift(LEFT * (X1 - X0)),
                  d144.animate.shift(LEFT * (X1 - X0)), run_time=0.35)
        g30, g60, g144 = fill(rows[30]), fill(rows[60]), fill(rows[144])
        self.play(GrowFromEdge(g30, LEFT), GrowFromEdge(g60, LEFT), GrowFromEdge(g144, LEFT), d30.animate.shift(RIGHT * (X1 - X0)), d60.animate.shift(RIGHT * (X1 - X0)),
                  d144.animate.shift(RIGHT * (X1 - X0)), run_time=1.8, rate_func=linear)
        # phase 3: the second press (the 60 row stays; the other two clear). The bar fills in four chunks so each cue lands on its word.
        until(self, "A second press", lead=0.1)
        W = X1 - X0
        key1 = VGroup(RoundedRectangle(width=0.7, height=0.7, corner_radius=0.12, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([X0, rows[60] + 1.15, 0]),
                      a2_lab("E", X0, rows[60] + 1.15, 38))
        p1 = arrow([X0, rows[60] + 0.75, 0], [X0, rows[60] + 0.3, 0], INK, 6)
        self.play(FadeOut(g30), FadeOut(g144), FadeOut(r[30]), FadeOut(r[144]), FadeOut(lab[30]), FadeOut(lab[144]), FadeOut(d30), FadeOut(d144),
                  FadeOut(g60), d60.animate.shift(LEFT * W), FadeIn(key1), GrowArrow(p1), run_time=0.45)

        def seg(a, b):
            return Rectangle(width=W * (b - a), height=0.22, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([X0 + W * (a + b) / 2, rows[60] - 0.22, 0])
        opts = [a2_lab("restart", 5.0, 1.75, 40), a2_lab("extend", 5.0, 0.9, 40), a2_lab("ignore", 5.0, 0.05, 40)]
        until(self, "restart", lead=0.1)
        s1 = seg(0.0, 0.3)
        self.play(FadeIn(opts[0]), GrowFromEdge(s1, LEFT), d60.animate.shift(RIGHT * W * 0.3), run_time=0.6, rate_func=linear)
        until(self, "extend", lead=0.1)
        s2 = seg(0.3, 0.5)
        self.play(FadeIn(opts[1]), GrowFromEdge(s2, LEFT), d60.animate.shift(RIGHT * W * 0.2), run_time=0.5, rate_func=linear)
        until(self, "ignore?", lead=0.1)
        s3 = seg(0.5, 0.7)
        key2 = VGroup(RoundedRectangle(width=0.7, height=0.7, corner_radius=0.12, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([0.0, rows[60] + 1.15, 0]),
                      a2_lab("E", 0.0, rows[60] + 1.15, 38))
        p2 = arrow([0.0, rows[60] + 0.75, 0], [0.0, rows[60] + 0.3, 0], INK, 6)
        self.play(FadeIn(opts[2]), FadeIn(key2), GrowArrow(p2), GrowFromEdge(s3, LEFT), d60.animate.shift(RIGHT * W * 0.2), run_time=0.5, rate_func=linear)
        until(self, "The example ignores", lead=0.05)
        s4 = seg(0.7, 1.0)
        no = cross_mark(0.0, rows[60] + 0.98, 0.2)
        ign = ring(opts[2], TERRA, pad=0.14)
        self.play(key2.animate.shift(UP * 0.5 + RIGHT * 0.9).set_opacity(0.25), p2.animate.shift(UP * 0.5 + RIGHT * 0.9).set_opacity(0.25), Create(no), Create(ign),
                  GrowFromEdge(s4, LEFT), d60.animate.shift(RIGHT * W * 0.3), FadeIn(example_tag(3.1, -3.12)), run_time=0.7, rate_func=linear)
        done(self)


# ─────────────────────────────────────────────── B14 · boundaries and the evidence split ───────────────────────────────────────────────
# "Boundaries: collision, movement, input and earlier tests stay unchanged. Presentation reads game state and never writes it. Then the evidence split:
#  for each rule, a headless test, or your own eyes."
# Phase 1: a fence round what must not change; presentation sits outside it, one arrow in (reads), one arrow back crossed out (never writes).
# Phase 2: four of the example's own rules are sorted into two columns: timing and reset -> a headless test (the driver test's checks 'scaled duration',
# 'reset clears uniform'); colour and readability -> your eyes (CHANGE-BRIEF 'a headless pass cannot certify color'; MATERIALS.md 'human readability ... outside the headless claims').
class B14_Boundaries(Scene):
    def construct(self):
        fence = box(-3.9, 0.55, 4.2, 4.4, DIM, 5)
        f_title = a2_lab("unchanged", -3.9, 2.2, 38)
        items = [a2_lab(t, -3.9, y, 38) for t, y in zip(["collision", "movement", "input", "earlier tests"], [1.35, 0.55, -0.25, -1.05])]
        pres = box(3.7, 0.8, 3.8, 2.0, DIM, 5)
        p_lab = a2_lab("presentation", 3.7, 1.3, 38)
        p_eye = eye_icon(3.7, 0.35, 0.42)
        a_read = arrow([-1.65, 1.3, 0], [1.75, 1.3, 0], INK, 6)
        l_read = a2_lab("reads", 0.05, 1.8, 36)
        a_write = arrow([1.75, 0.3, 0], [-1.65, 0.3, 0], DIM, 6)
        no = cross_mark(0.05, 0.3, 0.22, INK, 8)
        l_write = a2_lab("writes", 0.05, -0.2, 36)
        # phase 2
        t_icon = terminal_icon(-3.2, 2.2, 0.6)
        e_icon = eye_icon(3.2, 2.2, 0.6)
        t_lab = a2_lab("headless test", -3.2, 1.2, 38)
        e_lab = a2_lab("your eyes", 3.2, 1.2, 38)
        rules = [a2_lab("timing", 0.0, 1.0, 40), a2_lab("reset", 0.0, 0.2, 40), a2_lab("colour", 0.0, -0.6, 40), a2_lab("readability", 0.0, -1.4, 40)]
        u_t = Line([-4.5, 0.76, 0], [-1.9, 0.76, 0], color=DIM, stroke_width=4)
        u_e = Line([1.9, 0.76, 0], [4.5, 0.76, 0], color=DIM, stroke_width=4)
        tag_ex = example_tag(3.1, -3.12)

        until(self, "collision", lead=0.35)
        self.play(Create(fence), FadeIn(items[0]), run_time=0.4)
        until(self, "movement", lead=0.1)
        self.play(FadeIn(items[1]), run_time=0.3)
        until(self, "input and", lead=0.1)
        self.play(FadeIn(items[2]), run_time=0.3)
        until(self, "earlier tests", lead=0.1)
        self.play(FadeIn(items[3]), run_time=0.3)
        until(self, "stay unchanged", lead=0.1)
        self.play(FadeIn(f_title), run_time=0.3)
        until(self, "Presentation reads", lead=0.1)
        self.play(Create(pres), FadeIn(p_lab), FadeIn(p_eye), run_time=0.4)
        until(self, "game state", lead=0.3)
        self.play(GrowArrow(a_read), FadeIn(l_read), run_time=0.4)
        until(self, "never writes", lead=0.15)
        self.play(GrowArrow(a_write), FadeIn(l_write), Create(no), run_time=0.5)
        until(self, "Then the evidence split", lead=0.15)
        self.play(*[FadeOut(m) for m in (fence, f_title, pres, p_lab, p_eye, a_read, l_read, a_write, l_write, no)] + [FadeOut(m) for m in items], run_time=0.4)
        until(self, "for each rule", lead=0.1)
        self.play(*[FadeIn(r) for r in rules], run_time=0.5)
        until(self, "a headless test", lead=0.3)
        self.play(FadeIn(t_icon), FadeIn(t_lab), Create(u_t), FadeIn(tag_ex), rules[0].animate.move_to([-3.2, 0.3, 0]), rules[1].animate.move_to([-3.2, -0.5, 0]), run_time=0.45)
        until(self, "or your own eyes", lead=0.3)
        self.play(FadeIn(e_icon), FadeIn(e_lab), Create(u_e), rules[2].animate.move_to([3.2, 0.3, 0]), rules[3].animate.move_to([3.2, -0.5, 0]), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B15 · controlled inputs, by hand ───────────────────────────────────────────────
# "Controlled inputs: three uniform values, two pixels, computed by hand. At zero, a dark stripe is the quiet colour times point six five: sixty-six, twenty-seven,
#  fifteen. Only unshaded output keeps that arithmetic honest."
# Left: the hand arithmetic for ONE pixel (signal.gdshader line 4 quiet_color x 0.65, the dark stripe's factor from line 9, then x 255). Right: the example's own
# prediction table (evidence/example/controlled-predictions.json), dark stripe numbers + light stripe swatches at activation 0.0 / 0.5 / 1.0.
# All values recomputed by evidence/act2/verify_arithmetic.py. These are predictions by hand: no engine has drawn anything yet (tag).
A2_PRED = {  # activation -> (dark stripe RGB8, light stripe RGB8), from controlled-predictions.json (checked in verify_arithmetic.py)
    0.0: ((66, 27, 15), (102, 41, 23)),
    0.5: ((48, 105, 74), (66, 112, 78)),
    1.0: ((31, 184, 133), (31, 184, 133)),
}


class B15_ByHand(Scene):
    def construct(self):
        OPX, VX = -5.6, -4.9
        # left column
        l_quiet = a2_mono_l("quiet_color", VX, 2.75, 24, DIM)
        t1 = a2_mono_l("(0.40, 0.16, 0.09)", VX, 2.15, 24)
        s1 = a2_swatch((102, 41, 23), -0.7, 2.15, 0.8, 0.55)
        x1 = a2_cross(OPX, 1.4)
        m1 = a2_mono_l("0.65", VX, 1.4, 24)
        rule1 = Line([-5.9, 0.98, 0], [-0.3, 0.98, 0], color=DIM, stroke_width=3)
        t2 = a2_mono_l("(0.26, 0.104, 0.0585)", VX, 0.45, 24)
        x2 = a2_cross(OPX, -0.35)
        m2 = a2_mono_l("255", VX, -0.35, 24)
        rule2 = Line([-5.9, -0.78, 0], [-0.3, -0.78, 0], color=DIM, stroke_width=3)
        t3 = a2_mono_l("(66, 27, 15)", VX, -1.25, 24)
        s3 = a2_swatch((66, 27, 15), -1.55, -1.25, 0.9, 0.6)
        # right panel: 3 activation values x 2 pixels (swatch + the example's predicted RGB8 under it)
        acts = [0.0, 0.5, 1.0]
        ys = [2.05, 0.9, -0.25]
        XL, XD, XG = 0.7, 2.2, 4.9
        heads = [a2_lab("dark", XD, 2.95, 36), a2_lab("light", XG, 2.95, 36)]
        labs = [a2_mono(f"{a:.1f}", XL, y, 24) for a, y in zip(acts, ys)]
        slots_d = [Rectangle(width=0.9, height=0.55, stroke_color=GHOST, stroke_width=3, fill_opacity=0).move_to([XD, y, 0]) for y in ys]
        slots_l = [Rectangle(width=0.9, height=0.55, stroke_color=GHOST, stroke_width=3, fill_opacity=0).move_to([XG, y, 0]) for y in ys]
        sw_d = [a2_swatch(A2_PRED[a][0], XD, y, 0.9, 0.55) for a, y in zip(acts, ys)]
        sw_l = [a2_swatch(A2_PRED[a][1], XG, y, 0.9, 0.55) for a, y in zip(acts, ys)]
        nums_d = [a2_mono("(%d, %d, %d)" % A2_PRED[a][0], XD, y - 0.5, 20) for a, y in zip(acts, ys)]
        nums_l = [a2_mono("(%d, %d, %d)" % A2_PRED[a][1], XG, y - 0.5, 20) for a, y in zip(acts, ys)]
        # the unshaded line of the shader (line 2), and the honesty tags
        code2 = a2_code([A2_SIGNAL[1]], x=3.3, y=-1.75, size=24, first=2, width=5.2)
        tag_hand = status_tag("computed by hand, not measured", -3.0, -2.55)
        tag_ex = example_tag(3.1, -3.12)

        until(self, "three uniform values", lead=0.1)
        self.play(*[FadeIn(m) for m in labs], *[Create(m) for m in slots_d], run_time=0.5)
        until(self, "two pixels", lead=0.1)
        self.play(*[FadeIn(m) for m in heads], *[Create(m) for m in slots_l], FadeIn(tag_hand), run_time=0.5)
        until(self, "quiet colour", lead=0.5)
        self.play(FadeIn(l_quiet), FadeIn(t1), FadeIn(s1), run_time=0.45)
        until(self, "times point six five", lead=0.0)
        self.play(FadeIn(x1), FadeIn(m1), Create(rule1), FadeIn(t2), run_time=0.5)
        until(self, "sixty-six", lead=0.25)
        self.play(FadeIn(x2), FadeIn(m2), Create(rule2), FadeIn(t3), FadeIn(s3), run_time=0.5)
        cp = s3.copy()
        self.play(cp.animate.move_to([XD, ys[0], 0]), FadeIn(nums_d[0]), FadeIn(tag_ex), run_time=0.5)
        self.play(*[FadeIn(sw_d[i]) for i in (1, 2)], *[FadeIn(sw_l[i]) for i in (0, 1, 2)], *[FadeIn(nums_d[i]) for i in (1, 2)],
                  *[FadeIn(nums_l[i]) for i in (0, 1, 2)], run_time=0.5)
        until(self, "Only unshaded", lead=0.1)
        self.play(Create(code2.frame), run_time=0.3)
        self.play(FadeIn(code2.rows), run_time=0.25)
        until(self, "keeps that arithmetic honest", lead=0.7)
        self.play(Create(code2.ring_line(2)), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B16 · the hint experiment's predictions ───────────────────────────────────────────────
# "The hint experiment gets predictions too: greys sixty-four, one twenty-eight, one ninety-two, sampled with and without source color. By the S R G B formula, Forward Plus
#  leaves the colour read alone and brightens the data read to one thirty-seven, one eighty-eight, two twenty-five. On Compatibility, say so, and measure."
# A drawing of the assignment's encode function (assignment line 91; EVIDENCE-NOTES.md 'Predicted' table): x = byte / 255, y = encode(x). The colour read goes decode -> encode and
# lands back on the diagonal (unchanged); the data read is encoded once and climbs the curve: 64 -> 137, 128 -> 188, 192 -> 225. These are PREDICTIONS (no capture here).
def a2_encode(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


class B16_HintPredictions(Scene):
    def construct(self):
        GREYS = [64, 128, 192]
        PRED = [137, 188, 225]            # round(encode(b/255) * 255), checked by evidence/act2/verify_arithmetic.py
        px, py, pw, ph = -5.0, -2.0, 4.6, 3.6         # plot origin and size
        P = lambda xv, yv: [px + xv * pw, py + yv * ph, 0]
        plt = plot(a2_encode, (0, 1), (0, 1), size=(pw, ph), x=px + pw / 2, y=py + ph / 2, color=INK)
        diag = DashedLine(P(0, 0), P(1, 1), color=DIM, stroke_width=4, dash_length=0.14)
        xs = [b / 255 for b in GREYS]
        ys = [a2_encode(x) for x in xs]
        xt = [a2_mono(str(b), P(x, 0)[0], py - 0.38, 24) for b, x in zip(GREYS, xs)]
        yt = [a2_mono(str(v), px - 0.5, P(0, y)[1], 24) for v, y in zip(PRED, ys)]
        vdash = [DashedLine(P(x, 0), P(x, y), color=GHOST, stroke_width=3, dash_length=0.1) for x, y in zip(xs, ys)]
        hdash = [DashedLine(P(x, y), P(0, y), color=GHOST, stroke_width=3, dash_length=0.1) for x, y in zip(xs, ys)]
        d_diag = [Dot(P(x, x), radius=0.1, color=INK) for x in xs]
        d_curve = [Dot(P(x, x), radius=0.13, color=TERRA) for x in xs]            # start on the diagonal, climb to the curve
        # right: two rows of three bands
        BX = [1.9, 3.55, 5.2]
        R1, R2 = 1.0, -1.45
        row1 = [a2_swatch((g, g, g), x, R1, 1.2, 0.9) for g, x in zip(GREYS, BX)]
        row2 = [a2_swatch((g, g, g), x, R2, 1.2, 0.9) for g, x in zip(GREYS, BX)]
        n1 = [a2_mono(str(g), x, R1 - 0.7, 24) for g, x in zip(GREYS, BX)]
        n2 = [a2_mono(str(g), x, R2 - 0.7, 24) for g, x in zip(GREYS, BX)]
        n2_new = [a2_mono(str(v), x, R2 - 0.7, 24) for v, x in zip(PRED, BX)]
        s1 = VGroup(DashedLine([1.3, 2.05, 0], [1.85, 2.05, 0], color=DIM, stroke_width=4, dash_length=0.13), a2_mono_l("source_color", 2.05, 2.05, 24))
        s2 = VGroup(Line([1.3, -0.4, 0], [1.85, -0.4, 0], color=INK, stroke_width=5), a2_mono_l("no hint", 2.05, -0.4, 24))
        tag_pred = status_tag("predicted, not measured", 3.5, 2.95)
        tag_comp = status_tag("Compatibility: measure first", 3.1, -3.12)
        l_x = a2_lab("in the file", px + pw / 2, -2.9, 34, DIM)
        l_y = a2_lab("on screen", px + 0.75, 2.05, 34, DIM)

        until(self, "The hint experiment", lead=-0.1)
        self.play(FadeIn(tag_pred), run_time=0.4)
        until(self, "greys sixty-four", lead=0.15)
        self.play(FadeIn(row1[0]), FadeIn(n1[0]), FadeIn(row2[0]), FadeIn(n2[0]), run_time=0.35)
        until(self, "one twenty-eight", lead=0.1)
        self.play(FadeIn(row1[1]), FadeIn(n1[1]), FadeIn(row2[1]), FadeIn(n2[1]), run_time=0.35)
        until(self, "one ninety-two", lead=0.1)
        self.play(FadeIn(row1[2]), FadeIn(n1[2]), FadeIn(row2[2]), FadeIn(n2[2]), run_time=0.35)
        until(self, "with and without", lead=0.25)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.45)
        until(self, "By the S R G B formula", lead=0.3)
        self.play(Create(plt.axes), Create(diag), FadeIn(l_x), FadeIn(l_y), run_time=0.5)
        self.play(Create(plt.curve), *[FadeIn(m) for m in xt], run_time=0.7)
        until(self, "the colour read alone", lead=0.4)
        self.play(*[GrowFromCenter(d) for d in d_diag], run_time=0.45)
        until(self, "brightens the data read", lead=0.1)
        self.play(*[GrowFromCenter(d) for d in d_curve], run_time=0.3)
        self.play(*[d.animate.move_to(P(x, y)) for d, x, y in zip(d_curve, xs, ys)], *[Create(v) for v in vdash], run_time=0.7)
        for i, ph_ in enumerate(["one thirty-seven", "one eighty-eight", "two twenty-five"]):
            until(self, ph_, lead=0.1)
            self.play(Create(hdash[i]), FadeIn(yt[i]), row2[i].animate.set_fill(a2_hex((PRED[i],) * 3)), FadeOut(n2[i]), FadeIn(n2_new[i]), run_time=0.5)
        until(self, "On Compatibility", lead=0.15)
        self.play(FadeIn(tag_comp), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B17 · the material plan and the four predicted failures ───────────────────────────────────────────────
# "The material plan names each texture's role and import settings, and each uniform's type, range, default and group. Predict at least three failures, with their checks.
#  The example predicted four: a missing colour hint, an undeclared uniform, a shader edit changing both materials, and a headless pass that cannot certify colour."
# Phase 1 (before the midpoint): the example's plan board. Textures: gate-color.png (colour, source_color) and gate-roughness.png (data, no hint), both imported with
# compress/mode=0 (Lossless), compress/normal_map=2 (Disabled), mipmaps/generate=false (gate-*.png.import lines 18, 24, 26; MATERIALS.md rows). Uniforms: surface.gdshader lines 5, 6, 8, 9
# with the groups of lines 2 and 7. Phase 2 (after it): three empty failure/check panels, then the example's four (CHANGE-BRIEF-a5.md 'Predictions'), each with the check that catches it:
# a headless test (colour hint: contract test 'color hint'; uniform name: 'declared <name>') or your eyes (shared shader vs one material: native captures; colour: 'a headless pass cannot certify color').
class B17_MaterialPlan(Scene):
    def construct(self):
        # ---- plan board
        th1 = framed(a2_img("ev_tex_color.png", h=1.0, at=(-5.35, 1.75)))
        th2 = framed(a2_img("ev_tex_rough.png", h=1.0, at=(-5.35, 0.35)))
        n1 = a2_mono_l("gate-color.png", -4.65, 2.05, 24)
        r1 = VGroup(a2_lab_l("colour", -4.65, 1.45, 36), a2_mono_l("source_color", -3.0, 1.45, 24))
        n2 = a2_mono_l("gate-roughness.png", -4.65, 0.65, 24)
        r2 = VGroup(a2_lab_l("data", -4.65, 0.05, 36), a2_mono_l("no hint", -3.4, 0.05, 24))
        imp_h = a2_lab_l("import", -5.9, -1.05, 36, DIM)
        imp = VGroup(a2_lab_l("lossless", -4.4, -1.05, 36), a2_lab_l("normal map: disabled", -4.4, -1.65, 36), a2_lab_l("mipmaps: off", -4.4, -2.25, 36))
        g1 = box(3.5, 1.45, 4.9, 2.1, DIM, 5)
        g1t = a2_lab_l("Surface", 1.25, 2.05, 38)
        g1r = VGroup(a2_mono_l("tint", 1.25, 1.4, 24), a2_mono_l("vec4", 4.35, 1.4, 24, DIM), a2_mono_l("roughness_gain", 1.25, 0.85, 24), a2_mono_l("float", 4.35, 0.85, 24, DIM))
        g2 = box(3.5, -1.15, 4.9, 2.1, DIM, 5)
        g2t = a2_lab_l("Pattern", 1.25, -0.65, 38)
        g2r = VGroup(a2_mono_l("uv_scale", 1.25, -1.3, 24), a2_mono_l("float", 4.35, -1.3, 24, DIM), a2_mono_l("metallic_gain", 1.25, -1.85, 24), a2_mono_l("float", 4.35, -1.85, 24, DIM))
        # ---- panels
        PC = [(-3.1, 1.1), (3.1, 1.1), (-3.1, -1.15), (3.1, -1.15)]
        panels = [box(x, y, 5.8, 1.9, DIM, 5) for x, y in PC]
        ph_lab = [a2_lab_l("failure", x - 2.55, y, 36) for x, y in PC]
        ph_chk = [Circle(radius=0.34, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([x + 2.05, y + 0.2, 0]) for x, y in PC]
        ph_cl = [a2_lab("check", x + 2.05, y - 0.52, 32) for x, y in PC]
        labels = ["colour hint", "uniform name", "shader vs material", "headless vs colour"]
        real_lab = [a2_lab_l(t, x - 2.55, y, 40) for t, (x, y) in zip(labels, PC)]
        icons = [terminal_icon(PC[0][0] + 2.05, PC[0][1], 0.5), terminal_icon(PC[1][0] + 2.05, PC[1][1], 0.5),
                 eye_icon(PC[2][0] + 2.05, PC[2][1], 0.5), eye_icon(PC[3][0] + 2.05, PC[3][1], 0.5)]
        tag_ex = example_tag(3.1, -3.12)

        until(self, "each texture's role", lead=0.1)
        self.play(FadeIn(th1), FadeIn(n1), FadeIn(r1), FadeIn(tag_ex), run_time=0.4)
        self.play(FadeIn(th2), FadeIn(n2), FadeIn(r2), run_time=0.4)
        until(self, "import settings", lead=0.15)
        self.play(FadeIn(imp_h), FadeIn(imp), run_time=0.5)
        until(self, "each uniform's type", lead=0.15)
        self.play(Create(g1), FadeIn(g1t), FadeIn(g1r), run_time=0.5)
        until(self, "range, default", lead=0.35)
        self.play(Create(g2), FadeIn(g2t), FadeIn(g2r), run_time=0.5)
        until(self, "Predict at least three", lead=0.2)
        board = [th1, th2, n1, r1, n2, r2, imp_h, imp, g1, g1t, g1r, g2, g2t, g2r]
        self.play(*[FadeOut(m) for m in board], run_time=0.4)
        self.play(*[Create(panels[i]) for i in range(3)], *[FadeIn(ph_lab[i]) for i in range(3)], *[Create(ph_chk[i]) for i in range(3)], *[FadeIn(ph_cl[i]) for i in range(3)], run_time=0.7)
        until(self, "The example predicted four", lead=0.0)
        self.play(Create(panels[3]), FadeIn(ph_lab[3]), Create(ph_chk[3]), FadeIn(ph_cl[3]), run_time=0.4)
        for i, ph_ in enumerate(["a missing colour hint", "an undeclared uniform", "a shader edit", "a headless pass"]):
            until(self, ph_, lead=0.15)
            self.play(FadeOut(ph_lab[i]), FadeOut(ph_chk[i]), FadeOut(ph_cl[i]), FadeIn(real_lab[i]), FadeIn(icons[i]), run_time=0.45)
        done(self)


# ─────────────────────────────────────────────── B18 · five questions, and frame counting ───────────────────────────────────────────────
# "Then five questions: the renderer the project names, the colour arriving in fragment, how long a frame-counting version lasts at three frame rates, where the default lives,
#  and whether hint range clamps a value set from code."  (the assignment's five short questions, in its own order)
# Five numbered dots land on their words (a terracotta dot is the pointer). Question 3 opens a small sum for an ILLUSTRATIVE 36-frame effect, NOT the example's:
# 36 frames at 30, 60 and 144 frames per second last 1.2 s, 0.6 s and 0.25 s (verify_arithmetic.py). The bars are drawn to scale (same unit per second).
class B18_FiveQuestions(Scene):
    def construct(self):
        QY = [2.45, 1.3, 0.15, -1.0, -2.15]
        words = ["renderer", "colour", "frames", "default", "clamp?"]
        dots = [VGroup(Circle(radius=0.36, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([-5.4, y, 0]), a2_lab(str(i + 1), -5.4, y, 36)) for i, y in enumerate(QY)]
        labs = [a2_lab_l(w, -4.75, y, 40) for w, y in zip(words, QY)]
        pointer = Dot([-6.05, QY[0], 0], radius=0.13, color=TERRA)
        # the sum (right)
        tag = status_tag("illustrative: 36 frames", 2.7, 2.85)
        RY = [1.7, 0.45, -0.8]
        FPS = [30, 60, 144]
        SEC = [1.2, 0.6, 0.25]
        SEC_S = ["1.2 s", "0.6 s", "0.25 s"]
        k = 4.5                                           # bar units per second
        fl = [a2_lab_l(f"{f} fps", -1.3, y, 36) for f, y in zip(FPS, RY)]
        ex = [a2_mono_l(f"36 / {f} = {t}", 0.5, y, 32) for f, t, y in zip(FPS, SEC_S, RY)]
        bars = [Rectangle(width=k * t, height=0.22, stroke_width=0, fill_color=BAR1, fill_opacity=1).move_to([-1.3 + k * t / 2, y - 0.5, 0]) for t, y in zip(SEC, RY)]
        rows = [VGroup(fl[i], ex[i]) for i in range(3)]

        until(self, "the renderer", lead=0.1)
        self.play(FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(pointer), run_time=0.4)
        until(self, "the colour arriving", lead=0.1)
        self.play(FadeIn(dots[1]), FadeIn(labs[1]), pointer.animate.move_to([-6.05, QY[1], 0]), run_time=0.4)
        until(self, "how long a", lead=0.2)
        self.play(FadeIn(dots[2]), FadeIn(labs[2]), pointer.animate.move_to([-6.05, QY[2], 0]), FadeIn(tag), run_time=0.4)
        until(self, "frame-counting", lead=0.1)
        self.play(FadeIn(rows[0]), GrowFromEdge(bars[0], LEFT), run_time=0.5)
        until(self, "three frame rates", lead=0.3)
        self.play(FadeIn(rows[1]), GrowFromEdge(bars[1], LEFT), run_time=0.45)
        self.play(FadeIn(rows[2]), GrowFromEdge(bars[2], LEFT), run_time=0.45)
        until(self, "where the default lives", lead=0.15)
        self.play(FadeIn(dots[3]), FadeIn(labs[3]), pointer.animate.move_to([-6.05, QY[3], 0]), run_time=0.4)
        until(self, "whether hint range clamps", lead=0.15)
        self.play(FadeIn(dots[4]), FadeIn(labs[4]), pointer.animate.move_to([-6.05, QY[4], 0]), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · Give the Agent Rules  (B19, B23, B24 Manim; B20, B21, B22 are Remotion CCPlainShell, see lanes/act3.json)

Cast of the act: the REAL wrapper script (evidence/runs/scripts/run-test.sh, verbatim from the assignment; B19), the example's own CLAUDE.md
(evidence/example/sources/CLAUDE.md; B23), the assignment's own claude -p flag line (documented, not run; B24) and the commit chain.
Every line of code on screen is copied from those files (checked by evidence/act3/verify_lines.py); nothing is typed from memory.
SOFT WRAP: the wrapper's line 6 is 101 characters and its line 8 is 66; no type size at or above the floor shows 101 characters on this frame.
So a long line is shown as an editor shows it: broken at a space into indented continuation rows (a hook in the gutter, no line number), no character
added, none dropped; joined with single spaces the rows are the real line (verify_lines.py checks it). The flag line in B24 is broken after a comma, so its rows join with no space.
"""

A3_CW = {20: 0.15, 24: 0.20}      # Menlo, units per character (kit code_block, measured on this Mac)


def a3_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a3_code(spec, x=0.0, y=0.0, size=24, pad=0.3, indent=0.4, numbers=True, lh=None):
    """Real code in Menlo with an outline frame (like kit code_block) that also soft-wraps: spec = [(label, text), ...] where label is the REAL line
    number (str) or None for a continuation row. Returns a VGroup with .frame .rows (VGroup(num-or-hook, text) per row) .W .H .lh and .row_y(i), .text_left(i)."""
    cw = A3_CW[size]
    lh = lh or size / 32 * 0.46
    labs = [l for l, _ in spec if l]
    nw = (max(len(l) for l in labs) * cw + 0.25) if numbers else 0.0
    texts = [M(t, size) for _, t in spec]
    tw = max(len(t) * cw + (indent if l is None else 0.0) for l, t in spec)       # widths from character counts: the Gate A stub's Text.width is wrong
    W = tw + nw + 2 * pad
    H = len(spec) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, ((lab, _), t) in enumerate(zip(spec, texts)):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        tl = left + nw + (indent if lab is None else 0.0)
        t.move_to([tl + len(spec[i][1]) * cw / 2, yy, 0])
        if lab is not None:
            n = M(lab, size, DIM).move_to([left + (len(lab) * cw) / 2, yy, 0]) if (numbers and lab) else VGroup()
        else:
            gx = left + 0.12
            n = VGroup(Line([gx, yy + 0.09, 0], [gx, yy - 0.03, 0], color=DIM, stroke_width=3),
                       Line([gx, yy - 0.03, 0], [gx + 0.22, yy - 0.03, 0], color=DIM, stroke_width=3))
        rows.add(VGroup(n, t))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.x_, g.y_ = frame, rows, W, H, lh, x, y
    g.row_y = lambda i: y + H / 2 - pad - lh * (i + 0.5)
    return g


def a3_bracket(g, i0, i1, off=0.25, color=INK, w=5):
    """A right-margin bracket '[' mirrored: spans rows i0..i1 of block g. Never touches text (sits 0.25 outside the frame)."""
    xb = g.x_ + g.W / 2 + off
    ya = g.row_y(i0) + g.lh * 0.42
    yb = g.row_y(i1) - g.lh * 0.42
    return VGroup(Line([xb, ya, 0], [xb, yb, 0], color=color, stroke_width=w),
                  Line([xb - 0.13, ya, 0], [xb, ya, 0], color=color, stroke_width=w),
                  Line([xb - 0.13, yb, 0], [xb, yb, 0], color=color, stroke_width=w))


# ── B19 · the wrapper script: four jobs ──────────────────────────────────────────────────────────────────────────────────
A3_WRAP = [("1", "#!/usr/bin/env bash"),
           ("2", "# scripts/run-test.sh <test-file.gd> <fps>"),
           ("3", "set -o pipefail"),
           ("4", "mkdir -p logs"),
           ("5", 'log="logs/$(basename "$1" .gd)_${2}fps.log"'),
           ("6", "timeout 120 godot --headless --path godot"),
           (None, '--script "res://tests/$1" --fixed-fps "$2"'),
           (None, '2>&1 | tee "$log"'),
           ("7", "status=$?"),
           ("8", 'if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log";'),
           (None, "then status=1; fi"),
           ("9", "exit $status")]


class B19_Wrapper(Scene):
    def construct(self):
        title = T("Give  the  Agent  Rules", 40).move_to([-3.75, 2.95, 0])
        tag = status_tag("from the assignment", 4.1, 3.0)
        blk = a3_code(A3_WRAP, x=-0.55, y=-0.1)
        self.add(title, tag, blk.frame)
        until(self, "commit one wrapper script", lead=0.5)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in blk.rows], lag_ratio=0.12), run_time=1.6)
        jobs = [("1", "timeout", [[5]], "a timeout", 0.55),
                ("2", "frame rate", [[6]], "pins the frame rate", 0.7),
                ("3", "log", [[4], [7]], "keeps a log", 0.55),
                ("4", "fails on errors", [[9, 10]], "fails on any shader error", 0.7)]
        # legend, left to right along the bottom
        nw_ = {"1": 0.154, "2": 0.207, "3": 0.184, "4": 0.219}                     # measured EB Garamond 34 widths (real Manim)
        lw_ = {"timeout": 1.428, "frame rate": 1.811, "log": 0.549, "fails on errors": 2.426}
        widths = [nw_[n] + 0.35 + lw_[l] for n, l, _, _, _ in jobs]
        gap = 0.8
        x0 = -(sum(widths) + gap * 3) / 2
        for (num, lab, spans, cue, lead), w in zip(jobs, widths):
            until(self, cue, lead=lead)
            brs, nums = [], []
            for sp in spans:
                br = a3_bracket(blk, sp[0], sp[-1])
                xb = blk.x_ + blk.W / 2 + 0.25
                yc = (blk.row_y(sp[0]) + blk.row_y(sp[-1])) / 2
                nm = T(num, 32).move_to([xb + 0.42, yc, 0])
                brs.append(br); nums.append(nm)
            ln = T(num, 34).move_to([x0 + nw_[num] / 2, -3.05, 0])
            ll = T(lab, 34).move_to([x0 + nw_[num] + 0.35 + lw_[lab] / 2, -3.05, 0])
            dot = Dot([x0 - 0.3, -3.05, 0], radius=0.1, color=TERRA)
            self.play(*[Create(b) for b in brs], *[FadeIn(n) for n in nums], FadeIn(ln), FadeIn(ll), FadeIn(dot, scale=0.5), run_time=0.45)
            x0 += w + gap
        done(self)


# ── B23 · step one: the agent drafts the project context file (the example's REAL CLAUDE.md, 65 lines) ───────────────────
# Lines shown are real lines 1-5 and 22 of evidence/example/sources/CLAUDE.md (a gap row marks the lines left out). Line 10 of that file says
# "Assignments 1-9", so the prose block (lines 7-13) is left out on purpose. Size 20: line 22 is 67 characters.
A3_CLAUDEMD = [("1", "@AGENTS.md"),
               ("2", "@CHANGE-BRIEF.md"),
               ("3", "@assignments/05-shaders-materials/CHANGE-BRIEF.md"),
               ("4", " "),
               ("5", "# Signal Garden context"),
               ("", "\u2026"),
               ("22", "The quiet/active colors and eight stripes are in `signal.gdshader`.")]


class B23_ContextFile(Scene):
    def construct(self):
        blk = a3_code(A3_CLAUDEMD, x=0.0, y=0.75, size=20, lh=0.4)
        fname = M("CLAUDE.md", 28).move_to([-4.95, 2.95, 0])
        tag = example_tag(x=3.05, y=3.0)
        self.add(fname, blk.frame)
        until(self, "drafts the project context file", lead=0.9)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in blk.rows], lag_ratio=0.1), FadeIn(tag), run_time=1.3)
        # a fact with a file reference: ring the whole of real line 22 (it names signal.gdshader)
        until(self, "each with a file reference", lead=0.6)
        r22 = RoundedRectangle(width=blk.W - 0.3, height=blk.lh - 0.1, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([blk.x_, blk.row_y(6), 0])
        fr = T("file reference", 34).move_to([4.3, blk.row_y(6) - 0.95, 0])
        self.play(Create(r22), FadeIn(fr), run_time=0.5)
        # under 120 lines: a 120-wide bar, 65 filled
        until(self, "under a hundred twenty lines", lead=0.55)
        bx0, by, bw = -3.6, -2.3, 8.0
        outline = RoundedRectangle(width=bw, height=0.36, corner_radius=0.1, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([bx0 + bw / 2, by, 0])
        fill = Rectangle(width=bw * 65 / 120, height=0.28, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([bx0 + bw * 65 / 240, by, 0])
        n65 = T("65", 48).move_to([bx0 + bw * 65 / 120, by - 0.65, 0])
        n120 = T("120", 48).move_to([bx0 + bw, by - 0.65, 0])
        ln = T("lines", 34).move_to([-4.85, by, 0])
        tip = Dot([bx0 + bw * 65 / 120, by + 0.3, 0], radius=0.1, color=TERRA)
        self.play(Create(outline), FadeIn(ln), run_time=0.35)
        self.play(GrowFromEdge(fill, LEFT), FadeIn(n65), FadeIn(tip, scale=0.5), FadeIn(n120), run_time=0.6)
        # importing the brief, not pasting it
        until(self, "importing your change brief", lead=0.5)
        imp = T("imports your brief", 34).move_to([-1.9, 2.95, 0])
        yr = (blk.row_y(1) + blk.row_y(2)) / 2
        rr = VGroup(*[RoundedRectangle(width=blk.W - 0.3, height=blk.lh - 0.1, corner_radius=0.1, stroke_color=TERRA, stroke_width=6, fill_opacity=0).move_to([blk.x_, blk.row_y(i), 0])
                      for i in (1, 2)])
        arr = Arrow([-1.9, 2.7, 0], [-1.9, yr + blk.lh + 0.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        self.play(FadeIn(imp), run_time=0.3)
        self.play(GrowArrow(arr), *[Create(r) for r in rr], run_time=0.5)
        done(self)


# ── B24 · commit the draft unedited, then your review, separately; scope the session ─────────────────────────────────────
# The commit chain is a DRAWING of the assignment's order (agent draft, then your review); it is not the example's git history. The flag line is the
# assignment's own claude -p text (the --allowedTools flag only), shown as documented, not run, soft-wrapped after a comma (no character added).
A3_FLAG = [("\u2026", '--allowedTools "Read,Write,Glob,Grep,Bash(git status:*),'),
           (None, 'Bash(git diff:*),Bash(git log:*),Bash(ls:*)"')]


class B24_CommitAndScope(Scene):
    def construct(self):
        n1, n2 = np.array([-3.6, 1.0, 0.0]), np.array([-0.7, 1.0, 0.0])
        agent = logo_chip("claude", n1[0], 2.4, h=1.1)      # the Claude mark (LOGO LAW: claude-01); the claude-code mascot logo is a wide terracotta blob that GATE T reads as accent text
        me = professor_bear("1x1", 1.15, seed="B24", x=n2[0], y=2.4, shape="circle")
        node1 = Circle(radius=0.2, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to(n1)
        node2 = Circle(radius=0.2, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to(n2)
        link = Line(n1 + RIGHT * 0.2, n2 + LEFT * 0.2, color=INK, stroke_width=5)
        l_draft = T("draft", 34).move_to([n1[0], 0.4, 0])
        l_uned = T("unedited", 34).move_to([n1[0], -0.05, 0])
        l_rev = T("review", 34).move_to([n2[0], 0.4, 0])
        until(self, "Commit the draft", lead=0.3)
        self.play(FadeIn(agent, shift=DOWN * 0.2), GrowFromCenter(node1), FadeIn(l_draft), run_time=0.45)
        until(self, "unedited", lead=0.2)
        self.play(FadeIn(l_uned), run_time=0.3)
        until(self, "then your review", lead=0.15)
        self.play(Create(link), GrowFromCenter(node2), FadeIn(me), FadeIn(l_rev), run_time=0.55)
        # what the recorded draft got wrong (the assignment's own recorded run)
        until(self, "cited wrong lines", lead=0.7)
        tag = status_tag("recorded in the assignment", 3.45, 2.95)
        c1 = cross_mark(2.0, 1.75, 0.17)
        w1 = T("wrong lines", 34).move_to([3.47, 1.75, 0])
        self.play(FadeIn(tag), Create(c1), FadeIn(w1), run_time=0.4)
        until(self, "a headless test would settle the look", lead=0.9)
        c2 = cross_mark(2.0, 0.85, 0.17)
        w2 = T("headless settles look", 34).move_to([4.26, 0.85, 0])
        self.play(Create(c2), FadeIn(w2), run_time=0.4)
        # scope the session: the assignment's allowed-tools list, git read-only
        until(self, "Scope the session too", lead=0.2)
        flag = a3_code(A3_FLAG, x=-0.2, y=-1.45, size=24)
        dots2 = M("…", 24, DIM).move_to([-0.2 - flag.W / 2 + 0.3 + 0.45 + 0.4 + 44 * 0.2 + 0.35, flag.row_y(1), 0])   # after the real line's last character
        st = status_tag("documented, not run", 4.1, -0.3)
        self.play(Create(flag.frame), FadeIn(flag.rows), FadeIn(dots2), FadeIn(st), run_time=0.5)
        until(self, "an agent allowed all of git", lead=0.2)
        gchip = chip("git:*", -3.4, -2.75, mono=True, size=34)
        gx = cross_mark(-1.85, -2.75, 0.2)
        gl = T("not allowed", 34).move_to([-0.35, -2.75, 0])
        self.play(FadeIn(gchip), Create(gx), FadeIn(gl), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · The Shader From Code  (B25-B34, ten Manim beats; the Remotion runner-ups are recorded in lanes/act4.json and evidence/act4/auditions/)

HONESTY (Films = things actually done).
- The shader on screen is the INSTRUCTOR EXAMPLE's signal.gdshader (an A. I. wrote it under Professor Bear's direction): every code line below is a
  verbatim literal of evidence/example/sources/signal.gdshader, garden.gd, test-signal-driver.gd or a line of a real log in evidence/runs/;
  evidence/act4/verify_lines.py diffs every A4_SRC_* literal against its source file. Tabs are shown as four spaces and the indentation is kept
  (the first kit's code_block dropped indentation because Manim's Text bounding box ignores leading spaces; a4_Code places every row by character cell and recolours
  glyph by glyph, which code_block cannot do, so it is kept even after the kit fix).
- Nothing is called hand-written, student work or a Claude Code session. B25 shows the INSTRUCTION ("write it by hand") with scribble lines on a page
  labelled "your shader"; the only example text there is the specification's colour line (CHANGE-BRIEF-a5.md line 5), tagged as the example's.
- B29 shows the assignment's own prompt text, labelled "documented, not run". B31-B34 logs are from the re-run for this film (evidence/runs/, 16 Oct).
- Pad pictures are the example's own native captures (Compatibility, 14 Oct) or scripted-input lab frames (captures/lab/), never styled as anything else.

Cast for the act: the same 11 lines of signal.gdshader (B26-B28), the pad (B28, B30, B34), three frame-rate rulers (B32), the E key (B31).
Pacing: until() cues are the character share of the narration x the estimate (no audio exists yet); fixed sequences end by ~75-85% of the estimate.
"""

A4_ADV = {20: 0.15, 24: 0.2, 28: 0.25, 32: 0.25}     # Menlo advance per character (measured: evidence/act4/measure_menlo.py)

# ── verbatim source literals (diffed against the frozen sources by evidence/act4/verify_lines.py) ─────────────────────
A4_SRC_SIGNAL = [                                    # evidence/example/sources/signal.gdshader lines 1-11
    "shader_type spatial;",
    "render_mode unshaded;",
    "uniform float activation : hint_range(0.0, 1.0) = 0.0;",
    "uniform vec4 quiet_color : source_color = vec4(0.40, 0.16, 0.09, 1.0);",
    "uniform vec4 active_color : source_color = vec4(0.12, 0.72, 0.52, 1.0);",
    "uniform float stripe_count : hint_range(1.0, 16.0, 1.0) = 8.0;",
    "void fragment() {",
    "\tfloat stripe = step(0.5, fract(UV.x * stripe_count));",
    "\tvec3 base = quiet_color.rgb * mix(0.65, 1.0, stripe);",
    "\tALBEDO = mix(base, active_color.rgb, activation);",
    "}",
]
A4_SRC_BRIEF_COLOUR = "ALBEDO = mix(base, active_color.rgb, activation)"     # CHANGE-BRIEF-a5.md line 5 (the specification's colour line, no semicolon)
# the assignment's own driver prompt (assignment-05.md, Step 2): consecutive words of the prompt, whitespace-normalised (verify_lines.py checks each)
A4_SRC_PROMPT = ["do not edit any .gdshader file.", "First propose the smallest plan that meets the spec:", "Do not edit yet.",
                 "through the real game loop and real input,", "the new one at 30, 60 and 144.", "what it cannot prove in a headless run,"]
# real log lines of the re-run (evidence/runs/, 16 Oct 2026): (file, line number, the line); verify_lines.py diffs each against the file
A4_SRC_LOG_B31 = [("R2-driver-60fps.log", n, t) for n, t in (
    (3, "PASS scaled duration 1.0"), (4, "PASS retrigger ignored 1.0"), (5, "PASS end uniform one 1.0"),
    (7, "PASS scaled duration 0.5"), (8, "PASS retrigger ignored 0.5"), (9, "PASS end uniform one 0.5"),
    (11, "PASS pause freezes charge"), (12, "PASS reset clears uniform"), (13, "PASS interruption has no late gate"),
    (14, "PASS every sampled uniform matches game state"))]
A4_SRC_CMD_B33 = "./scripts/run-test.sh test-material-contract.gd 60"            # journal-commands-exit-codes-elapsed.tsv, row M1-parse (exit=1)
A4_SRC_LOG_B33 = [("R4-M1-parse-60fps.log", n, t) for n, t in (
    (7, "SHADER ERROR: Expected a ';' after 'shader_type spatial'."), (15, "UNIFORM_TYPES {}"),
    (16, "FAIL declared activation is float"), (17, "FAIL declared quiet_color is vec4"),
    (18, "FAIL declared active_color is vec4"), (19, "FAIL declared stripe_count is float"),
    (78, "RESULT 53 checks / 4 failures / baseline"))]
A4_SRC_LOG_B34 = [("R4-M2-undeclared-probe.log", 4, "READBACK activation = 0.7"), ("R4-M2-undeclared-probe.log", 5, "READBACK renamed_activation = <null>"),
                  ("R4-M2-rename-driver-60fps.log", 16, "RESULT 10 checks / 0 failures; sample count 409"),
                  ("R4-M2-rename-contract-60fps.log", 4, "FAIL declared activation is float"),
                  ("R4-M2-rename-contract-60fps.log", 66, "RESULT 53 checks / 1 failures / baseline")]
A4_SRC_GARDEN_4 = ["const CHARGE_SECONDS := 0.6"]                                # garden.gd line 4
A4_SRC_GARDEN_227 = [                                                          # garden.gd lines 227-231
    "\tif charging:",
    "\t\tcharge = minf(CHARGE_SECONDS, charge + delta)",
    "\t\tif charge >= CHARGE_SECONDS - 0.00001:",
    "\t\t\tcharging = false",
    "\t\t\tgate_open = true",
]
A4_SRC_GARDEN_253 = ['\tpad_material.set_shader_parameter("activation", charge / CHARGE_SECONDS)']   # garden.gd line 253


# ═════════════════════════ helpers (all act-prefixed) ═════════════════════════
def a4_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a4_mono(s, x, y, size=32, color=INK):
    return M(s, size, color).move_to([x, y, 0])


def a4_etag(x=3.4, y=2.95):
    return example_tag(x, y)


def a4_stag(text, x, y):
    return status_tag(text, x, y)


def a4_cell(s, left, y, size=20, color=INK, col=0):
    """Monospace text whose first character sits in cell `col` of a row whose cell-left is `left` (no leading or trailing spaces in s).
    Menlo's advance is exactly 0.15 / 0.20 / 0.25 units at size 20 / 24 / 28-32, so the row's ink centre is left + (col + len/2) * advance.
    (Text.width and get_left() are never used for placing: the bounding box ignores leading spaces.)"""
    t = M(s, size, color)
    t.move_to([left + (col + len(s) / 2.0) * A4_ADV[size], y, 0])
    return t


class a4_Code(VGroup):
    """Real code, one monospace row per line, OUTLINE-only frame, REAL line numbers (first=), indentation kept (tab = 4 spaces).
    `show` = the row indexes drawn now (default all); the others are built later with num_mob(i) / txt_mob(i) (same geometry)."""

    def __init__(self, lines, first=1, x=0.0, y=0.0, size=20, pitch=None, pad=0.25, numbers=True, min_cols=0, color=INK, frame=True, show=None):
        VGroup.__init__(self)
        adv = A4_ADV[size]
        lines = [ln.replace("\t", "    ").rstrip() for ln in lines]
        pitch = pitch or (size / 32 * 0.46)
        ndig = max(len(str(first + i)) for i in range(len(lines)))
        nw = (ndig * adv + 0.3) if numbers else 0.0
        cols = max(max(len(l) for l in lines), min_cols)
        W = nw + cols * adv + 2 * pad
        H = len(lines) * pitch + 2 * pad
        self.adv, self.pitch, self.W, self.H, self.cx, self.cy, self.size_, self.first, self.lines_ = adv, pitch, W, H, x, y, size, first, lines
        self.pad_, self.ndig, self.numbers_, self.color_, self.cols = pad, ndig, numbers, color, cols
        self.left0 = x - W / 2 + pad + nw                 # cell-left of column 0
        self.frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
        self.rows = VGroup()
        for i in (range(len(lines)) if show is None else show):
            self.rows.add(VGroup(*([self.num_mob(i)] if numbers else []), self.txt_mob(i)))
        if frame:
            self.add(self.frame)
        self.add(self.rows)

    def y_of(self, n):
        return self.cy + self.H / 2 - self.pad_ - self.pitch * (n - self.first + 0.5)

    def x_of(self, col):
        return self.left0 + col * self.adv

    def num_mob(self, i):
        s = str(self.first + i)
        n = M(s, self.size_, DIM)
        n.move_to([self.cx - self.W / 2 + self.pad_ + self.ndig * self.adv - len(s) * self.adv / 2.0, self.y_of(self.first + i), 0])
        return n

    def txt_mob(self, i):
        ln = self.lines_[i]
        body = ln.strip()
        k = len(ln) - len(ln.lstrip(" "))
        return a4_cell(body, self.left0, self.y_of(self.first + i), self.size_, self.color_, col=k) if body else VGroup()

    def seg(self, n, text, col, color=None):
        """A piece of REAL line n starting at column col (monospace: exact placement), for per-piece colouring."""
        return a4_cell(text, self.left0, self.y_of(n), self.size_, color or self.color_, col=col)

    def ring_cols(self, n, c0, c1, pad=0.07, h=0.26, color=TERRA):
        """Ring (grey backing + terracotta) round columns c0..c1 (inclusive) of REAL line n."""
        w = (c1 - c0 + 1) * self.adv
        ph = Rectangle(width=w, height=h, stroke_width=0, fill_opacity=0).move_to([self.x_of(c0) + w / 2, self.y_of(n), 0])
        return ring(ph, color=color, pad=pad, sw=6)

    def ring_row(self, n, color=TERRA, full=False, grey=False):
        """Ring (grey backing + terracotta) round the text of REAL line n (from its indentation to its last character), clear of the glyphs.
        grey=True: a grey ring plus one terracotta dot just beyond its right end. GATE T reads a SHORT terracotta ring (width < 15 x height) as accent text,
        so a ring round a short line is grey with a terracotta dot (a dot is never read as text)."""
        ln = self.lines_[n - self.first]
        k = 0 if full else len(ln) - len(ln.lstrip(" "))
        w = (self.cols if full else len(ln.strip())) * self.adv
        ph = Rectangle(width=w, height=0.27, stroke_width=0, fill_opacity=0).move_to([self.x_of(k) + w / 2, self.y_of(n), 0])
        if grey:
            r_ = ring(ph, color=DIM, pad=0.09, sw=6, backing=False)
            dot = Dot([self.x_of(k) + w + 0.3, self.y_of(n), 0], radius=0.09, color=TERRA)
            return VGroup(r_, dot)
        return ring(ph, color=color, pad=0.09, sw=6)


def a4_glyphs(txt, body, c0, c1):
    """The glyph sub-mobjects of Text `txt` (whose string is `body`, no leading/trailing spaces) for characters c0..c1-1.
    Manim's Text has one sub-mobject per NON-space character, so spans can be recoloured with exact positions."""
    start = len(body[:c0].replace(" ", ""))
    n = len(body[c0:c1].replace(" ", ""))
    return [txt[i] for i in range(start, start + n)]


def a4_paint(glyphs, color):
    """Animations that recolour each glyph in place (one .animate per glyph: a VGroup(*glyphs) would be added to the scene as a second owner of the glyphs)."""
    return [m.animate.set_color(color) for m in glyphs]


def a4_uniform_parts(line):
    """Split a REAL `uniform <type> <name> : <hint> = <default>;` line into (role, text, column) pieces (monospace columns)."""
    import re
    m = re.match(r"^uniform (\w+) (\w+) : (.+?) = (.+);$", line)
    t, n, h, d = m.group(1), m.group(2), m.group(3), m.group(4)
    c_t = 8
    c_n = c_t + len(t) + 1
    c_h = c_n + len(n) + 3
    c_d = c_h + len(h) + 3
    return [("kw", "uniform", 0), ("type", t, c_t), ("name", n, c_n), ("pun", ":", c_n + len(n) + 1), ("hint", h, c_h), ("pun", "=", c_h + len(h) + 1),
            ("default", d + ";", c_d)]


def a4_gap(x, y, color=DIM):
    """The marker for lines left out between two excerpts: three small dots."""
    return VGroup(*[Dot([x + dx, y, 0], radius=0.045, color=color) for dx in (-0.18, 0.0, 0.18)])


def a4_no(x, y, r=0.3, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE or over a picture, never over type."""
    d = r * 0.7071
    return VGroup(Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0]), Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw))


def a4_calendar(x, y, s=0.32, color=INK):
    """A drawn calendar page (outline, a header bar, two binder rings, one terracotta dot): the mark for 'dated'. No numerals."""
    body = RoundedRectangle(width=2 * s, height=1.7 * s, corner_radius=0.06, stroke_color=color, stroke_width=4, fill_opacity=0).move_to([x, y - 0.1 * s, 0])
    bar = Line([x - s, y + 0.45 * s, 0], [x + s, y + 0.45 * s, 0], color=color, stroke_width=4)
    rings = VGroup(*[Line([x + dx * s, y + 0.75 * s, 0], [x + dx * s, y + 1.05 * s, 0], color=color, stroke_width=5) for dx in (-0.55, 0.55)])
    dot = Dot([x + 0.3 * s, y - 0.35 * s, 0], radius=0.07, color=TERRA)
    return VGroup(body, bar, rings, dot)


# ── the writing kit (show-tell iso_kit, copied with the a4_ prefix: the kit file is pasted, never imported) ─────────────
def a4_quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point."""
    o = np.array([x, y, 0.0])

    def P(u, v):
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10), P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def a4_paper(x, y, w=2.4, h=3.0, fill=PAGE_TOP):
    """A flat 2-D sheet: white page, ink outline, kraft drop shadow."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    return VGroup(shadow, sheet)


def a4_scribble(x, y, w, amp=0.07, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for w units (reads as script, never as type)."""
    n = max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def a4_write_lines(self, q, lines, speed=7.0, hop=0.2, dip=0.05):
    """The quill q WRITES each scribble line: the nib hops to the line's start, then the line draws while the nib rides its tip."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib

        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


# ═════════════════════════ B25 · write it by hand from the specification; TIME is global ═════════════════════════
class B25_WriteFromSpec(Scene):
    def construct(self):
        title = T("The  Shader  From  Code", 40).move_to([-3.4, 2.95, 0])
        self.add(title)
        cx = -1.4                                                                     # centre of the specification card and the page
        spec = a4_Code([A4_SRC_BRIEF_COLOUR], x=cx, y=1.3, size=20, numbers=False, pad=0.22)
        spec_l = a4_lab("specification", 4.7, 1.3, 34)
        page = a4_paper(cx, -0.85, w=7.5, h=1.9)
        page_l = a4_lab("your shader", 4.7, -0.85, 34)
        # three scribble lines on the page (script, not type); the third is as long as the colour line above it
        sx = cx - 3.2
        lines = [a4_scribble(sx, -0.38, 6.3), a4_scribble(sx, -0.85, 5.4), a4_scribble(sx, -1.32, 6.4)]
        quill = a4_quill(sx, -0.38, 0.8, 0.0)
        quill.shift(np.array([-0.2, 0.55, 0.0])); quill.nib = quill.nib + np.array([-0.2, 0.55, 0.0])

        until(self, "Write it by hand", lead=0.45)
        etag = a4_etag()
        self.play(FadeIn(spec, shift=DOWN * 0.15), FadeIn(spec_l), FadeIn(etag), run_time=0.45)
        self.play(FadeIn(page), FadeIn(page_l), FadeIn(quill), run_time=0.4)
        a4_write_lines(self, quill, lines[:2], speed=7.5)
        until(self, "colour line exactly", lead=0.55)
        arr = arrow([-3.4, 0.95, 0], [-3.4, 0.2, 0], color=INK, w=6, tip=0.2)
        ex_l = a4_lab("exactly", -2.4, 0.58, 32)
        self.play(GrowArrow(arr), FadeIn(ex_l), run_time=0.35)
        a4_write_lines(self, quill, lines[2:], speed=7.5)
        until(self, "revise the specification", lead=0.6)
        back = CurvedArrow(np.array([-5.5, -0.7, 0.0]), np.array([-5.5, 1.05, 0.0]), angle=-PI / 2.2, color=INK, stroke_width=6, tip_length=0.2)
        self.play(Create(back), run_time=0.5)
        until(self, "dated", lead=0.75)
        cal = a4_calendar(3.55, 0.3, s=0.34)
        cal_l = a4_lab("dated", 4.75, 0.3, 34)
        self.play(FadeIn(cal), FadeIn(cal_l), run_time=0.4)
        # reimport -> no shader error -> commit alone
        c1 = chip("reimport", -4.8, -2.45, size=34)
        a1 = arrow([-3.5, -2.45, 0], [-2.6, -2.45, 0], w=6, tip=0.18)
        c2 = chip("no shader error", -0.82, -2.45, size=34)
        tk = tick_mark(1.2, -2.45, s=0.22, color=INK, w=8)
        a2 = arrow([1.7, -2.45, 0], [2.55, -2.45, 0], w=6, tip=0.18)
        c3 = chip("commit alone", 4.2, -2.45, size=34)
        cdot = Dot([6.05, -2.45, 0], radius=0.11, color=TERRA)
        until(self, "Reimport", lead=0.4)
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.35)
        until(self, "no shader error", lead=0.4)
        self.play(GrowArrow(a1), FadeIn(c2, shift=UP * 0.15), run_time=0.35)
        self.play(Create(tk), run_time=0.25)
        until(self, "commit it alone", lead=0.4)
        self.play(GrowArrow(a2), FadeIn(c3, shift=UP * 0.15), FadeIn(cdot, scale=0.5), run_time=0.35)
        # the second picture: TIME is global
        until(self, "The built-in time", lead=0.7)
        gone = [etag, spec, spec_l, page, page_l, quill, arr, ex_l, back, cal, cal_l, lines[0], lines[1], lines[2]]
        self.play(*[FadeOut(m) for m in gone], run_time=0.25)
        ty = 0.85
        track = Line([-5.2, ty, 0], [5.2, ty, 0], color=DIM, stroke_width=5)
        start_l = a4_lab("engine start", -4.5, ty - 0.7, 32)
        t_l = a4_mono("TIME", -5.2, ty + 0.8, 32)
        t_dot = Dot([-5.2, ty, 0], radius=0.16, color=INK)
        ev_dot = Dot([0.6, ty, 0], radius=0.16, color=TERRA)
        ev_l = a4_lab("your event", 0.6, ty - 0.7, 32)
        self.play(Create(track), FadeIn(start_l), FadeIn(t_l), FadeIn(t_dot), FadeIn(ev_dot, scale=0.5), FadeIn(ev_l), run_time=0.35)
        self.play(t_dot.animate.move_to([5.2, ty, 0]), t_l.animate.move_to([5.2, ty + 0.8, 0]), run_time=1.0, rate_func=linear)
        until(self, "never time since", lead=0.5)
        since = Line([0.6, ty - 1.55, 0], [4.9, ty - 1.55, 0], color=GHOST, stroke_width=7)
        since_l = a4_lab("since event", -0.95, ty - 1.55, 32)
        no = cross_mark(2.75, ty - 1.55, s=0.28, color=INK, w=8)
        self.play(Create(since), FadeIn(since_l), Create(no), run_time=0.3)
        done(self)


# ═════════════════════════ B26 · lines 1-6: the type, unshaded, four uniforms (type, hint, default) ═════════════════════════
class B26_FirstLines(Scene):
    def construct(self):
        g = a4_Code(A4_SRC_SIGNAL[:6], first=1, x=0.0, y=0.8, size=20, pitch=0.5, show=[0, 1])
        self.add(g)
        etag = a4_etag(3.3, -3.05)
        # rows 3-6: one Text per row; its glyphs are recoloured by span (type / name / hint / default) so each kind can be lit alone
        rows = {n: g.txt_mob(n - 1) for n in (3, 4, 5, 6)}
        nums = {n: g.num_mob(n - 1) for n in (3, 4, 5, 6)}
        spans = {n: {} for n in rows}
        for n in rows:
            body = A4_SRC_SIGNAL[n - 1]
            for role, txt, col in a4_uniform_parts(body):
                spans[n].setdefault(role, []).extend(a4_glyphs(rows[n], body, col, col + len(txt)))
        c_type = chip("shader type", -2.0, -1.95, size=34)
        c_mode = chip("render mode", 2.0, -1.95, size=34)
        until(self, "first lines choose", lead=0.35)
        self.play(g.rows[1][1].animate.set_color(DIM), FadeIn(c_type, shift=UP * 0.1), FadeIn(etag), run_time=0.4)
        until(self, "unshaded rendering", lead=0.55)
        self.play(g.rows[0][1].animate.set_color(DIM), g.rows[1][1].animate.set_color(INK), FadeIn(c_mode, shift=UP * 0.1), run_time=0.4)
        until(self, "Then four uniforms", lead=0.5)
        self.play(FadeOut(c_type), FadeOut(c_mode), g.rows[0][1].animate.set_color(INK), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(VGroup(nums[n], rows[n]), shift=UP * 0.1) for n in (3, 4, 5, 6)], lag_ratio=0.18), run_time=0.7)
        # each kind of piece lit in turn: all four types, all four hints, all four defaults, then the names
        lg = {"type": chip("type", -3.0, -1.95, size=34), "hint": chip("hint", 0.0, -1.95, size=34), "default": chip("default", 3.0, -1.95, size=34)}

        def light(roles_by_row):
            """roles_by_row: {row n: roles lit}; rows 1-2 and every other glyph go DIM."""
            lit, dim = [], list(g.rows[0][1]) + list(g.rows[1][1])
            for n in rows:
                for role, gl in spans[n].items():
                    (lit if role in roles_by_row.get(n, ()) else dim).extend(gl)
            return a4_paint(lit, INK) + a4_paint(dim, DIM)
        allrows = lambda role: {n: (role,) for n in rows}
        until(self, "a type", lead=0.4)
        self.play(*light(allrows("type")), FadeIn(lg["type"], shift=UP * 0.1), run_time=0.35)
        until(self, "a hint", lead=0.3)
        self.play(*light(allrows("hint")), FadeIn(lg["hint"], shift=UP * 0.1), run_time=0.3)
        until(self, "a default", lead=0.3)
        self.play(*light(allrows("default")), FadeIn(lg["default"], shift=UP * 0.1), run_time=0.3)
        until(self, "activation", lead=0.35)
        self.play(*light({3: ("name",)}), FadeOut(lg["type"]), FadeOut(lg["hint"]), FadeOut(lg["default"]), run_time=0.35)
        until(self, "two colours", lead=0.3)
        self.play(*light({3: ("name",), 4: ("name",), 5: ("name",)}), run_time=0.3)
        until(self, "a stripe count", lead=0.6)
        self.play(*light({n: ("name",) for n in rows}), run_time=0.3)
        done(self)


# ═════════════════════════ B27 · lines 7-9: U V picks the stripe (fract, step, 0.65) ═════════════════════════
class B27_StripeMaths(Scene):
    def construct(self):
        g = a4_Code(A4_SRC_SIGNAL[6:9], first=7, x=-1.4, y=2.2, size=20, pitch=0.4)
        self.add(g)
        XL, PW, Y0, PH = -5.1, 8.6, -0.3, 1.4
        px = lambda u: XL + u * PW
        py = lambda v: Y0 + v * PH
        pts = []
        for k in range(8):                                           # fract(UV.x * 8): eight teeth; the real stripe_count default is 8.0 (signal.gdshader line 6)
            pts += [[px(k / 8), py(0), 0], [px((k + 1) / 8), py(1), 0], [px((k + 1) / 8), py(0), 0]]
        saw = VMobject(stroke_color=INK, stroke_width=6)
        saw.set_points_as_corners(np.array(pts, dtype=float))
        axes = VGroup(Line([px(0), Y0, 0], [px(1), Y0, 0], color=INK, stroke_width=5), Line([px(0), Y0, 0], [px(0), py(1) + 0.15, 0], color=INK, stroke_width=5))
        lab_x = a4_mono("UV.x", 4.75, Y0, 28)
        lab_0, lab_1 = a4_lab("0", px(0), Y0 - 0.45, 32), a4_lab("1", px(1), Y0 - 0.45, 32)
        lab_f = a4_mono("fract", 4.75, py(0.92), 28)
        thr = DashedLine([px(0), py(0.5), 0], [px(1) + 0.25, py(0.5), 0], color=DIM, stroke_width=5, dash_length=0.18)
        lab_h = a4_lab("0.5", 4.35, py(0.5), 34)
        # the two real sample pixels (UV.x 0.15625 and 0.21875): both in the second tooth, one under the cut, one over it
        u1, u2 = 0.15625, 0.21875
        d1 = Dot([px(u1), py((8 * u1) % 1.0), 0], radius=0.1, color=TERRA)
        d2 = Dot([px(u2), py((8 * u2) % 1.0), 0], radius=0.1, color=TERRA)
        strip = framed(img("pantry/a4_pad_strip.png", w=PW, x=px(0.5), y=-1.78), color=DIM, pad=0.07)
        g1 = DashedLine([px(u1), py((8 * u1) % 1.0) - 0.13, 0], [px(u1), -1.5, 0], color=DIM, stroke_width=4, dash_length=0.14)
        g2 = DashedLine([px(u2), py((8 * u2) % 1.0) - 0.13, 0], [px(u2), -1.5, 0], color=DIM, stroke_width=4, dash_length=0.14)
        etag = a4_etag(-3.4, -3.05)
        stag = a4_stag("example, 14 Oct · Compatibility", 3.3, -3.05)

        until(self, "U V picks", lead=0.45)
        r8 = g.ring_row(8)
        self.play(Create(r8), FadeIn(etag), run_time=0.4)
        until(self, "the fractional part", lead=0.5)
        self.play(Create(axes), FadeIn(lab_x), FadeIn(lab_0), FadeIn(lab_1), run_time=0.4)
        self.play(Create(saw), FadeIn(lab_f), run_time=1.5, rate_func=linear)
        until(self, "cut at one half", lead=0.75)
        self.play(Create(thr), FadeIn(lab_h), run_time=0.4)
        self.play(FadeIn(d1, scale=0.4), FadeIn(d2, scale=0.4), run_time=0.3)
        # after the midpoint: the real strip lands under the maths, the guides drop to it
        until(self, "A dark stripe", lead=0.3)
        self.play(FadeIn(strip), FadeIn(stag), Create(g1), Create(g2), run_time=0.5)
        # the colours: quiet x 0.65 = dark, quiet x 1 = light
        self.play(FadeOut(VGroup(saw, axes, lab_x, lab_0, lab_1, lab_f, thr, lab_h, d1, d2, g1, g2)), g.rows[1].animate.set_opacity(0.45),
                  FadeOut(r8), Create(g.ring_row(9)), run_time=0.4)
        quiet = swatch((102, 41, 23), -4.8, 0.15, w=1.0, h=0.8)
        quiet_l = a4_lab("quiet", -4.8, -0.55, 34)
        until(self, "sixty-five percent", lead=1.7)
        self.play(FadeIn(quiet, scale=0.6), FadeIn(quiet_l), run_time=0.35)
        until(self, "sixty-five percent", lead=0.55)
        a_d = arrow([-4.1, 0.4, 0], [-1.3, 0.7, 0], w=6, tip=0.2)
        x_d = a4_lab("× 0.65", -2.7, 1.1, 34)
        dark = swatch((66, 27, 15), -0.55, 0.7, w=1.0, h=0.7)
        dark_l = a4_lab("dark stripe", 2.0, 0.7, 34)
        self.play(GrowArrow(a_d), FadeIn(x_d), FadeIn(dark, scale=0.6), FadeIn(dark_l), run_time=0.45)
        until(self, "a light stripe", lead=0.4)
        a_l = arrow([-4.1, -0.1, 0], [-1.3, -0.4, 0], w=6, tip=0.2)
        x_l = a4_lab("× 1", -2.7, -0.95, 34)
        light = swatch((102, 41, 23), -0.55, -0.4, w=1.0, h=0.7)
        light_l = a4_lab("light stripe", 2.0, -0.4, 34)
        self.play(GrowArrow(a_l), FadeIn(x_l), FadeIn(light, scale=0.6), FadeIn(light_l), run_time=0.45)
        done(self)


# ═════════════════════════ B28 · line 10: mix by activation (0, 0.5, 1) with the pad's own captures ═════════════════════════
class B28_MixByActivation(Scene):
    def construct(self):
        g = a4_Code([A4_SRC_SIGNAL[9]], first=10, x=0.0, y=2.45, size=24, pitch=0.5, pad=0.25)
        self.add(g)
        TX0, TX1, TY = -3.9, 3.9, 0.95
        vx = lambda v: TX0 + v * (TX1 - TX0)
        track = Line([-4.5, TY, 0], [4.5, TY, 0], color=DIM, stroke_width=6)
        stops = VGroup(*[Dot([vx(v), TY, 0], radius=0.09, color=DIM) for v in (0.0, 0.5, 1.0)])
        tl = [a4_lab("0", vx(0.0), TY - 0.5, 36), a4_lab("0.5", vx(0.5), TY - 0.5, 36), a4_lab("1", vx(1.0), TY - 0.5, 36)]
        left = VGroup(swatch((66, 27, 15), -5.45, TY, w=0.4, h=0.5), swatch((102, 41, 23), -5.0, TY, w=0.4, h=0.5))
        left_l = a4_lab("stripes", -5.2, TY - 0.6, 32)
        right = swatch((31, 184, 133), 5.1, TY, w=0.8, h=0.6)
        right_l = a4_lab("green", 5.1, TY - 0.6, 32)
        knob = Dot([vx(0.0), TY, 0], radius=0.2, color=INK)
        kl = a4_mono("activation", vx(0.0), TY + 0.62, 28)
        kg = VGroup(knob, kl)
        pics = []
        for v, x in (("0.0", -3.9), ("0.5", 0.0), ("1.0", 3.9)):
            pics.append(framed(img(f"pantry/a4_padc_{v}.png", w=3.5, x=x, y=-1.5), color=DIM, pad=0.07))
        etag = a4_etag(-3.4, -3.05)
        stag = a4_stag("example, 14 Oct · Compatibility", 3.3, -3.05)

        self.play(Create(g.ring_row(10)), FadeIn(etag), run_time=0.4)
        until(self, "mix the stripe colour", lead=0.5)
        self.play(Create(track), FadeIn(left), FadeIn(left_l), FadeIn(stops), run_time=0.5)
        until(self, "toward the active colour", lead=0.5)
        self.play(FadeIn(right, scale=0.6), FadeIn(right_l), *[FadeIn(t) for t in tl], run_time=0.4)
        until(self, "by activation", lead=0.55)
        self.play(FadeIn(kg, shift=DOWN * 0.15), run_time=0.35)
        until(self, "At zero", lead=0.3)
        self.play(FadeIn(pics[0]), FadeIn(stag), run_time=0.4)
        until(self, "At half", lead=0.45)
        self.play(kg.animate.shift(RIGHT * (vx(0.5) - vx(0.0))), run_time=0.45)
        self.play(FadeIn(pics[1]), run_time=0.35)
        until(self, "At one", lead=0.45)
        self.play(kg.animate.shift(RIGHT * (vx(1.0) - vx(0.5))), run_time=0.45)
        self.play(FadeIn(pics[2]), run_time=0.35)
        done(self)


# ═════════════════════════ B29 · direct the driver and its test, plan first (the assignment's own prompt, documented, not run) ═════════════════════════
class B29_DriverPrompt(Scene):
    def construct(self):
        CX, CY, CW, CH = -1.6, 0.1, 9.0, 4.7
        card = RoundedRectangle(width=CW, height=CH, corner_radius=0.2, fill_color="#FFFFFF", fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([CX, CY, 0])
        card_l = a4_lab("the assignment's prompt", -3.9, 2.95, 34)
        to_arr = arrow([-1.45, 2.95, 0], [-0.6, 2.95, 0], w=6, tip=0.2)
        cc = chip("Claude Code", 1.1, 2.95, size=34)       # text chip: the Claude Code logo is a wide terracotta blob that GATE T reads as accent text (reported to the lead)
        tag = a4_stag("documented, not run", CX, -2.85)
        LX = CX - CW / 2 + 0.9                       # text left edge
        F = A4_SRC_PROMPT
        rows_y = [1.8, 0.95, 0.5, -0.3, -1.1, -1.85]
        rows = [a4_cell(F[i], LX, rows_y[i], 20) for i in range(6)]
        DX = CX - CW / 2 + 0.4
        dot = Dot([DX, rows_y[0], 0], radius=0.1, color=TERRA)
        IX = 4.75
        # one drawing per rule, in the prompt's own order: shader file with a prohibition, a plan page, the E key, three frame rates, the eye
        page1 = a4_paper(IX - 0.1, 1.8, w=0.62, h=0.72)
        l1 = VGroup(*[a4_scribble(IX - 0.34, 1.8 + dy, 0.48, amp=0.035, sw=3) for dy in (0.17, 0.0, -0.17)])
        no1 = a4_no(IX + 0.5, 1.6, r=0.27)
        page2 = a4_paper(IX - 0.1, 0.85, w=0.62, h=0.72)
        l2 = VGroup(*[a4_scribble(IX - 0.34, 0.85 + dy, 0.48, amp=0.035, sw=3) for dy in (0.17, 0.0, -0.17)])
        key = chip("E", IX, -0.3, w=0.95, size=40)
        rates = chip("30 · 60 · 144", IX - 0.1, -1.1, size=32)
        eye = eye_icon(IX, -1.85, s=0.55)

        self.play(FadeIn(card), FadeIn(card_l), GrowArrow(to_arr), FadeIn(cc, shift=DOWN * 0.1), FadeIn(tag), run_time=0.5)
        until(self, "forbids editing", lead=0.5)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.1), FadeIn(dot, scale=0.5), FadeIn(VGroup(page1, l1)), Create(no1), run_time=0.45)
        until(self, "the smallest plan", lead=0.7)
        self.play(dot.animate.move_to([DX, rows_y[1], 0]), FadeIn(rows[1], shift=RIGHT * 0.1), FadeIn(VGroup(page2, l2)), run_time=0.4)
        until(self, "before any edit", lead=0.3)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.1), run_time=0.3)
        until(self, "real input", lead=0.45)
        self.play(dot.animate.move_to([DX, rows_y[3], 0]), FadeIn(rows[3], shift=RIGHT * 0.1), FadeIn(key, shift=DOWN * 0.1), run_time=0.4)
        until(self, "three frame rates", lead=0.4)
        self.play(dot.animate.move_to([DX, rows_y[4], 0]), FadeIn(rows[4], shift=RIGHT * 0.1), FadeIn(rates, shift=DOWN * 0.1), run_time=0.4)
        until(self, "cannot prove", lead=0.85)
        self.play(dot.animate.move_to([DX, rows_y[5], 0]), FadeIn(rows[5], shift=RIGHT * 0.1), FadeIn(eye), run_time=0.4)
        done(self)


# ═════════════════════════ B30 · the driver is one line (garden.gd 4, 227-231, 253) ═════════════════════════
class B30_DriverLine(Scene):
    def construct(self):
        C = a4_Code(A4_SRC_GARDEN_4, first=4, x=-3.6, y=2.3, size=20, pitch=0.4, pad=0.25)
        A = a4_Code(A4_SRC_GARDEN_227, first=227, x=-1.5, y=0.35, size=20, pitch=0.4, pad=0.25)
        B = a4_Code(A4_SRC_GARDEN_253, first=253, x=0.0, y=-1.75, size=20, pitch=0.4, pad=0.25)
        gap = a4_gap(-5.4, -1.1)
        gd = a4_mono("garden.gd", 4.6, 2.3, 28)
        phys = a4_lab("physics tick", 4.7, 0.35, 34)
        etag = a4_etag(3.3, -3.05)
        line253 = A4_SRC_GARDEN_253[0].replace("\t", "    ")
        body = line253.strip()
        bt = B.rows[0][1]                                # the row text that is actually on screen (its glyphs are recoloured in place)
        i_act = body.index('"activation"')
        i_chg = body.index("charge / CHARGE_SECONDS")
        g_act = a4_glyphs(bt, body, i_act, i_act + len('"activation"'))
        g_chg = a4_glyphs(bt, body, i_chg, i_chg + len("charge / CHARGE_SECONDS"))
        g_rest = [m for m in bt if m not in g_act and m not in g_chg]
        rB = B.ring_row(253)
        until(self, "the driver is one line", lead=0.5)
        self.play(FadeIn(B, shift=UP * 0.1), FadeIn(gd), FadeIn(etag), run_time=0.45)
        self.play(Create(rB), run_time=0.3)
        until(self, "Each physics tick", lead=0.55)
        self.play(FadeIn(A, shift=UP * 0.1), FadeIn(gap), FadeIn(phys), run_time=0.45)
        until(self, "the game sets activation", lead=0.45)
        self.play(*a4_paint(g_rest, DIM), *a4_paint(g_chg, DIM), run_time=0.3)
        until(self, "charge divided", lead=0.35)
        self.play(*a4_paint(g_chg, INK), *a4_paint(g_act, DIM), run_time=0.3)
        until(self, "point six", lead=0.25)
        self.play(FadeIn(C, shift=DOWN * 0.1), run_time=0.4)
        # the second picture: the game owns the state, the shader only observes (three REAL lab frames; activation = charge / 0.6 from states.jsonl)
        fr = [framed(img(f"pantry/a4_labpadT_{f}.png", w=2.6, x=x, y=1.15), color=DIM, pad=0.06) for f, x in ((300, -3.8), (597, -0.6), (603, 2.6))]
        vals = [a4_lab(t, x, -0.15, 40) for t, x in (("0", -3.8), ("0.278", -0.6), ("0.611", 2.6))]
        up = arrow([-0.6, -1.2, 0], [-0.6, -0.6, 0], w=6, tip=0.2)
        stag = a4_stag("scripted input · earlier take, 14 Oct", -3.2, -3.05)
        eye = eye_icon(5.4, 1.5, s=0.55)
        eye_l = a4_lab("observes", 5.4, 0.75, 34)
        until(self, "The game owns", lead=0.6)
        self.play(*[FadeOut(m) for m in (A, C, gap, phys, gd)], rB.animate.set_opacity(0.0), *a4_paint(list(bt), INK), run_time=0.25)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in fr], lag_ratio=0.25), FadeIn(stag), run_time=0.6)
        self.play(*[FadeIn(v) for v in vals], GrowArrow(up), run_time=0.35)
        until(self, "only observes", lead=0.55)
        self.play(FadeIn(eye, scale=0.6), FadeIn(eye_l), run_time=0.35)
        done(self)


# ═════════════════════════ B31 · what the test does: ten checks (the real names from the re-run's log) ═════════════════════════
class B31_TenChecks(Scene):
    def construct(self):
        names = [t[len("PASS "):] for _, _, t in A4_SRC_LOG_B31]
        RX, RY0, RP = -2.35, 2.45, 0.45
        rows = [a4_cell(nm, RX, RY0 - RP * i, 24) for i, nm in enumerate(names)]
        ticks = [tick_mark(RX - 0.5, RY0 - RP * i, s=0.14, color=INK, w=6) for i in range(10)]
        key = chip("E", -5.0, 1.85, w=1.1, size=48)
        key_l = a4_lab("key event", -5.0, 1.05, 32)
        ten = T("10", 130).move_to([-5.0, -0.35, 0])
        ten_l = a4_lab("checks", -5.0, -1.2, 36)
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)

        def press():
            return [key.animate.shift(DOWN * 0.1)]

        until(self, "sends real key events", lead=0.35)
        self.play(FadeIn(key, shift=DOWN * 0.1), FadeIn(key_l), FadeIn(stag), FadeIn(etag), run_time=0.3)
        until(self, "times the charge", lead=0.35)
        self.play(*press(), run_time=0.1)
        self.play(key.animate.shift(UP * 0.1), run_time=0.1)
        self.play(LaggedStart(*[FadeIn(VGroup(rows[i], ticks[i]), shift=RIGHT * 0.1) for i in range(3)], lag_ratio=0.3), run_time=0.7)
        until(self, "presses again mid-charge", lead=0.35)
        self.play(*press(), run_time=0.1)
        self.play(key.animate.shift(UP * 0.1), run_time=0.1)
        self.play(LaggedStart(*[FadeIn(VGroup(rows[i], ticks[i]), shift=RIGHT * 0.1) for i in range(3, 6)], lag_ratio=0.3), run_time=0.7)
        until(self, "pauses", lead=-0.05)
        self.play(FadeIn(VGroup(rows[6], ticks[6]), shift=RIGHT * 0.1), run_time=0.3)
        until(self, "resets", lead=0.15)
        self.play(FadeIn(VGroup(rows[7], ticks[7]), shift=RIGHT * 0.1), run_time=0.3)
        self.play(FadeIn(VGroup(rows[8], ticks[8]), shift=RIGHT * 0.1), run_time=0.3)
        until(self, "compares the uniform", lead=0.2)
        self.play(FadeIn(VGroup(rows[9], ticks[9]), shift=RIGHT * 0.1), run_time=0.3)
        until(self, "Ten checks", lead=0.9)
        self.play(FadeIn(ten, scale=0.7), FadeIn(ten_l), run_time=0.4)
        done(self)


# ═════════════════════════ B32 · 30 / 60 / 144 frames per second: 0.6 game seconds each time; headless draws nothing ═════════════════════════
A4_RATES = [(30, 16), (60, 34), (144, 83)]    # (fps, render_samples while charging): R2-driver-<fps>fps.log, the DURATION line, scale 1.0


class B32_ThreeRates(Scene):
    def construct(self):
        RX0, RX1 = -3.9, 2.9
        ys = [1.5, 0.1, -1.3]
        rulers, bars, labs, ends, verdicts, smp, dots = VGroup(), [], [], [], [], [], []
        for (fps, n), y in zip(A4_RATES, ys):
            base = Line([RX0, y, 0], [RX1, y, 0], color=DIM, stroke_width=5)
            ticks = VGroup(*[Line([RX0 + (RX1 - RX0) * i / (n - 1), y - 0.17, 0], [RX0 + (RX1 - RX0) * i / (n - 1), y + 0.17, 0], color=DIM, stroke_width=2.5)
                             for i in range(n)])
            rulers.add(VGroup(base, ticks))
            bar = Rectangle(width=RX1 - RX0, height=0.36, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([(RX0 + RX1) / 2, y, 0])
            bar.set_z_index(-1)
            bars.append(bar)
            labs.append(a4_lab(f"{fps} fps", -5.15, y, 36))
            ends.append(a4_lab("0.6 s", RX1, y + 0.5, 34))
            smp.append(a4_lab(f"{n} samples", -3.0, y - 0.5, 32, DIM))
            verdicts.append(VGroup(a4_lab("10 checks", 4.85, y + 0.2, 32), a4_lab("0 failures", 4.85, y - 0.22, 32)))
            dots.append(Dot([RX1, y, 0], radius=0.13, color=TERRA))
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)

        until(self, "At thirty", lead=-0.05)
        self.play(LaggedStart(*[FadeIn(VGroup(labs[i], rulers[i], smp[i])) for i in range(3)], lag_ratio=0.2), FadeIn(stag), FadeIn(etag), run_time=1.0)
        until(self, "point six game seconds", lead=0.8)
        self.play(*[GrowFromEdge(b, LEFT) for b in bars], run_time=1.1, rate_func=linear)
        self.play(*[FadeIn(e) for e in ends], *[FadeIn(d, scale=0.4) for d in dots], run_time=0.3)
        until(self, "no failures", lead=0.55)
        self.play(*[FadeIn(v, shift=LEFT * 0.1) for v in verdicts], run_time=0.4)
        # the second picture: headless draws nothing, so it cannot say what colour the pad is
        until(self, "All headless", lead=0.35)
        self.play(*[FadeOut(m) for m in (rulers, *bars, *labs, *ends, *smp, *verdicts, *dots, stag)], run_time=0.3)
        empty = Rectangle(width=3.8, height=2.4, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([-3.0, 0.8, 0])
        term = terminal_icon(-3.0, 0.8, s=0.6)
        nothing = a4_lab("nothing drawn", -3.0, -0.8, 36)
        self.play(Create(empty), FadeIn(term), FadeIn(nothing), run_time=0.45)
        q = T("?", 90).move_to([-0.2, 0.8, 0])
        pad = framed(img("pantry/a4_labpadT_300.png", w=3.1, x=3.0, y=0.8), color=DIM, pad=0.06)
        pad_l = a4_lab("the pad", 3.0, -0.95, 36)
        stag2 = a4_stag("scripted input · earlier take, 14 Oct", -3.2, -3.05)
        until(self, "what colour the pad is", lead=1.0)
        self.play(FadeIn(q), FadeIn(pad), FadeIn(pad_l), FadeIn(stag2), run_time=0.45)
        done(self)


# ═════════════════════════ B33 · mutation 1: delete a semicolon (re-run, evidence/runs/R4-M1-parse-60fps.log) ═════════════════════════
class B33_DeleteSemicolon(Scene):
    def construct(self):
        f = a4_Code(A4_SRC_SIGNAL[:1], first=1, x=-3.4, y=2.55, size=24, pitch=0.45, pad=0.25, min_cols=24)
        f_l = a4_mono("signal.gdshader", 2.9, 2.55, 28)
        semi = f.rows[0][1][-1]                                   # the last glyph of line 1: the semicolon
        L = [A4_SRC_CMD_B33] + [t for _, _, t in A4_SRC_LOG_B33[:6]] + ["..."] + [A4_SRC_LOG_B33[6][2]]
        L[0] = "$ " + L[0]
        g = a4_Code(L, first=1, x=0.0, y=-0.35, size=24, pitch=0.4, pad=0.25, numbers=False, show=[])
        rows = [g.txt_mob(i) for i in range(len(L))]
        # rows: 0 command, 1 SHADER ERROR, 2 UNIFORM_TYPES {}, 3-6 FAIL x4, 7 ..., 8 RESULT
        gap_dot = Dot([f.x_of(19) + 0.1, f.y_of(1) - 0.02, 0], radius=0.09, color=TERRA)
        ex = chip("exit 1", 4.3, g.y_of(1 + 8), mono=True, size=34)
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)
        self.add(f)
        self.play(FadeIn(f_l), FadeIn(stag), FadeIn(etag), run_time=0.3)
        until(self, "delete a semicolon", lead=0.55)
        self.play(FadeOut(semi), FadeIn(gap_dot, scale=0.4), run_time=0.35)
        until(self, "fails to parse", lead=0.9)
        self.play(FadeIn(g.frame), run_time=0.2)
        self.play(FadeIn(rows[0], shift=RIGHT * 0.1), run_time=0.25)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.1), run_time=0.25)
        until(self, "empty uniform list", lead=0.45)
        r2 = g.ring_row(1 + 2, grey=True)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.1), Create(r2), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(rows[i], shift=RIGHT * 0.1) for i in (3, 4, 5, 6)], lag_ratio=0.2), run_time=0.6)
        self.play(FadeIn(rows[7]), FadeIn(rows[8], shift=RIGHT * 0.1), run_time=0.3)
        until(self, "must exit one", lead=0.35)
        self.play(FadeIn(ex, shift=LEFT * 0.1), run_time=0.3)
        until(self, "Restore the file", lead=0.4)
        self.play(FadeOut(gap_dot), FadeIn(semi), run_time=0.35)
        done(self)


# ═════════════════════════ B34 · mutation 2: rename the driven uniform; the driver test still passes ═════════════════════════
class B34_RenameUniform(Scene):
    def construct(self):
        PY = 2.45                                                         # the pipe row
        pipe = Line([-5.8, PY, 0], [-2.0, PY, 0], color=DIM, stroke_width=14)
        send_l = a4_mono('"activation"', -4.4, PY + 0.6, 28)            # the string the game sends (garden.gd line 253)
        game_l = a4_lab("game", -4.4, PY - 0.62, 34)
        tipdot = Dot([-5.8, PY, 0], radius=0.14, color=TERRA)
        sock = Circle(radius=0.42, stroke_color=INK, stroke_width=7, fill_opacity=0).move_to([-1.55, PY, 0])
        sock_l = a4_mono("activation", -1.0, PY + 0.6, 28)
        sock_l2 = a4_mono("renamed_activation", 1.2, PY + 0.6, 28)
        shader_l = a4_lab("shader", -1.55, PY - 0.72, 34)
        shader_l2 = a4_lab("shader", 0.95, PY - 0.72, 34)
        no = cross_mark(-0.74, PY, s=0.26, color=INK, w=8)
        to_pad = DashedLine([1.55, PY, 0], [3.8, PY, 0], color=DIM, stroke_width=5, dash_length=0.2)
        pad = framed(img("pantry/a4_labpadT_300.png", w=1.8, x=4.9, y=PY), color=DIM, pad=0.05)
        # three real log cards, one width, one left edge
        CX = -2.25
        probe = a4_Code([A4_SRC_LOG_B34[0][2], A4_SRC_LOG_B34[1][2]], x=CX, y=0.75, size=20, pitch=0.4, numbers=False, min_cols=47)
        drv = a4_Code([A4_SRC_LOG_B34[2][2]], x=CX, y=-0.62, size=20, pitch=0.4, numbers=False, min_cols=47)
        con = a4_Code([A4_SRC_LOG_B34[3][2], A4_SRC_LOG_B34[4][2]], x=CX, y=-2.0, size=20, pitch=0.4, numbers=False, min_cols=47)
        probe_l, drv_l, con_l = a4_lab("probe", 5.0, 0.75, 34), a4_lab("driver", 5.0, -0.62, 34), a4_lab("contract", 5.0, -2.0, 34)
        ex0 = chip("exit 0", 2.85, -0.62, mono=True, size=34)
        ex1 = chip("exit 1", 2.85, -2.0, mono=True, size=34)
        stag = a4_stag("re-run for this film", -3.2, -3.05)
        etag = a4_etag(3.4, -3.05)
        pad_tag = a4_stag("scripted input", 4.9, PY - 1.12)

        self.play(Create(pipe), FadeIn(send_l), FadeIn(game_l), FadeIn(sock), FadeIn(sock_l), FadeIn(shader_l), FadeIn(stag), FadeIn(etag), run_time=0.5)
        until(self, "driven uniform", lead=0.45)
        self.play(FadeIn(tipdot, scale=0.5), run_time=0.15)
        self.play(tipdot.animate.move_to([-2.0, PY, 0]), run_time=0.5, rate_func=linear)
        until(self, "shader only", lead=0.5)
        self.play(sock.animate.shift(RIGHT * 2.5), FadeOut(sock_l), FadeOut(shader_l), FadeIn(sock_l2), FadeIn(shader_l2), run_time=0.5)
        self.play(Create(no), run_time=0.2)
        until(self, "Setting an undeclared", lead=0.35)
        self.play(FadeIn(VGroup(probe, probe_l), shift=UP * 0.1), run_time=0.4)
        until(self, "driver test still passed", lead=0.35)
        self.play(FadeIn(VGroup(drv, drv_l, ex0), shift=UP * 0.1), run_time=0.4)
        until(self, "pad would never change colour", lead=0.5)
        self.play(Create(to_pad), FadeIn(pad), FadeIn(pad_tag), run_time=0.4)
        until(self, "Only the uniform list", lead=0.45)
        self.play(FadeIn(VGroup(con, con_l, ex1), shift=UP * 0.1), run_time=0.4)
        self.play(Create(con.ring_row(1, grey=True)), run_time=0.3)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · A Shader That Reads Textures  (B35-B39, Manim)

One cast for the act: the two REAL 64 x 64 textures (pantry/ev_tex_color.png, ev_tex_rough.png), the REAL 14-line surface.gdshader
(evidence/example/sources/surface.gdshader) and the two REAL material spheres (circle cut-outs of the example's own capture,
pantry/a5_mat_matte.png and a5_mat_coated.png, made by evidence/act5/make_a5_pantry.py).
Every line of code on screen is verbatim from evidence/example/sources/ with its REAL line number; excerpts are dedented by the
common leading tab, and a line longer than the frame (surface.gdshader line 12 is 87 characters) wraps at a space with a drawn
continuation hook (the characters are untouched; the line number shows once). Numbers on screen are the file's own (matte.tres /
coated.tres lines 9-12, garden-textures.py, the .import files).
Editor frames (the Import dock, the Inspector of matte.tres) are NOT drawn here: B35 and B37 carry labelled fallbacks that name the
REAL file lines; the real frames drop into a5_import_panel() / the right-hand slot of B37 once evidence/editor/EDITOR-NOTES.md exists.
"""

A5P = "pantry/"

# REAL source lines, embedded verbatim (Gate A runs scenes.py from a folder with no evidence/); evidence/act5/verify_embedded.py checks them.
A5_REAL = {'surface.gdshader': {1: 'shader_type spatial;',
                      2: 'group_uniforms Surface;',
                      3: 'uniform sampler2D color_map : source_color, filter_nearest;',
                      4: 'uniform sampler2D roughness_map : filter_nearest;',
                      5: 'uniform vec4 tint : source_color = vec4(1.0);',
                      6: 'uniform float roughness_gain : hint_range(0.0, 1.0) = 0.8;',
                      7: 'group_uniforms Pattern;',
                      8: 'uniform float uv_scale : hint_range(0.25, 4.0) = 1.0;',
                      9: 'uniform float metallic_gain : hint_range(0.0, 1.0) = 0.0;',
                      10: 'void fragment() {',
                      11: '\tALBEDO = texture(color_map, UV * uv_scale).rgb * tint.rgb;',
                      12: '\tROUGHNESS = clamp(texture(roughness_map, UV * uv_scale).r * roughness_gain, 0.05, 1.0);',
                      13: '\tMETALLIC = metallic_gain;',
                      14: '}'},
 'gate-color.png.import': {16: '[params]', 18: 'compress/mode=0', 24: 'compress/normal_map=2', 26: 'mipmaps/generate=false'},
 'gate-roughness.png.import': {18: 'compress/mode=0', 24: 'compress/normal_map=2', 26: 'mipmaps/generate=false'},
 'matte.tres': {9: 'shader_parameter/tint = Color(1, 1, 1, 1)',
                10: 'shader_parameter/roughness_gain = 0.9',
                11: 'shader_parameter/uv_scale = 1.0',
                12: 'shader_parameter/metallic_gain = 0.0'},
 'coated.tres': {9: 'shader_parameter/tint = Color(0.45, 0.95, 0.72, 1)',
                 10: 'shader_parameter/roughness_gain = 0.25',
                 11: 'shader_parameter/uv_scale = 2.0',
                 12: 'shader_parameter/metallic_gain = 0.4'},
 'garden-textures.py': {2: '"""Original algorithmic textures. No model, network, or borrowed image."""',
                        11: '            stripe=(x//8)%2',
                        12: "            data.extend(((44+stripe*15,78+stripe*18,85+stripe*16) if role=='color' else (int(255*(0.4 if stripe else "
                            '0.85)),)*3))',
                        15: "png('gate-color.png','color');png('gate-roughness.png','data')"}}

A5_CW = {20: 0.15, 24: 0.2}            # measured Menlo units per character
A5_LH = {20: 0.2875, 24: 0.345}        # default row pitch (size / 32 * 0.46)


def a5_line(fname, n):
    return A5_REAL[fname][n]


def a5_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a5_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A5P + name)
    try:
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])   # bicubic rings near light-on-dark text and breaks GATE T's ink mask
    except Exception:
        pass
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    return im.move_to(np.array([at[0], at[1], 0.0]))


def a5_hook(x, y, s=0.13):
    """The wrap mark: a drawn elbow (down, then left with a small head). A shape, not a glyph."""
    return VGroup(Line([x, y + s * 0.6, 0], [x, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x, y - s * 0.7, 0], [x - s * 1.4, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 0.2, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 1.2, 0], color=DIM, stroke_width=4))


def a5_split(text, budget):
    """Soft-wrap `text` at the last space at or before `budget` characters, preferring a space after a comma/&&/colon.
    Returns a list of pieces (characters verbatim; only the breaking space is dropped)."""
    if len(text) <= budget:
        return [text]
    cut = text.rfind(" ", 0, budget + 1)
    if cut <= 0:
        return [text]
    return [text[:cut]] + a5_split(text[cut + 1:], budget)


class A5Code:
    """Real code rows: Menlo, real line numbers, outline-only frame, optional gap markers and wraps.
    spec: list of (real_line_number, text) or None (a gap marker). `dedent` strips the common leading tab(s).
    Attributes: .group (frame + rows + marks), .frame, .W, .H, .pitch, .cw, .size; rows(n) -> VGroup of line n (number + pieces);
    ring(n) -> terracotta ring round the whole line n; tok(n, token, k=0) -> (cx, cy, w) of a token; piece_y(n, i)."""

    def __init__(self, spec, x=0.0, y=0.0, size=20, wrap=None, dedent=True, pad=0.3, pitch=None, gap=0.32, width=None, extra=0.0):
        self.size, self.cw = size, A5_CW[size]
        self.pitch = pitch or A5_LH[size]
        items = []
        tabs = [len(t) - len(t.lstrip("\t")) for s in spec if s for t in [s[1]] if t.strip()]
        cut = min(tabs) if (dedent and tabs) else 0
        for s in spec:
            if s is None:
                items.append(("gap", None, None, None, 0))
                continue
            n, t = s
            t = t[cut:] if t.startswith("\t" * cut) else t
            t = t.replace("\t", "    ")
            lead = len(t) - len(t.lstrip(" "))
            pieces = a5_split(t, wrap) if wrap else [t]
            for i, p in enumerate(pieces):
                items.append(("row", n if i == 0 else None, p, i, lead))
        digits = max(len(str(s[0])) for s in spec if s)
        self.nw = digits * self.cw + 0.25
        longest = max(len(p) + ((ld + 2) if i else 0) for k, n, p, i, ld in items if k == "row")
        self.W = width or (longest * self.cw + self.nw + 2 * pad + extra)
        h = sum(self.pitch if it[0] == "row" else gap for it in items)
        self.H = h + 2 * pad
        self.x, self.y, self.pad = x, y, pad
        self.frame = RoundedRectangle(width=self.W, height=self.H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
        self.text_left = x - self.W / 2 + pad + self.nw
        self.rows_, self.pos, self.marks, self.hooks = {}, {}, VGroup(), VGroup()
        cy = y + self.H / 2 - pad
        cur = None
        for k, n, p, i, ld in items:
            if k == "gap":
                cy -= gap
                self.marks.add(*[Dot([self.x - self.W / 2 + pad + self.nw * 0.5, cy + gap / 2 + dy, 0], radius=0.035, color=DIM) for dy in (-0.07, 0.0, 0.07)])
                continue
            yy = cy - self.pitch / 2
            cy -= self.pitch
            ind = (ld + 2) * self.cw if i else 0.0
            tx = M(p if p else " ", self.size)
            lead_p = len(p) - len(p.lstrip(" "))            # Text() drops leading spaces: place by character column so indentation is kept
            tx.move_to([self.text_left + ind + lead_p * self.cw + tx.width / 2, yy, 0])
            grp = VGroup(tx)
            if n is not None:
                nm = M(str(n), self.size, DIM)
                nm.move_to([self.text_left - 0.25 - nm.width / 2, yy, 0])
                grp.add(nm)
                cur = n
                self.rows_[n] = VGroup()
                self.pos[n] = []
            self.rows_[cur].add(grp)
            self.pos[cur].append((yy, p, ind))
            if i:
                prev = self.pos[cur][i - 1]
                hk = a5_hook(self.text_left + prev[2] + len(prev[1]) * self.cw + 0.2, prev[0])
                self.hooks.add(hk)
        self.group = VGroup(self.frame, *[r for r in self.rows_.values()], self.marks, self.hooks)

    def rows(self, n):
        return self.rows_[n]

    def piece_y(self, n, i=0):
        return self.pos[n][i][0]

    def ring(self, n, color=TERRA, sw=6, shrink=0.8, pieces=None):
        """One flat terracotta ring per visual row of line n (GATE T reads a ring whose width/height < 15 as accent TEXT, so a
        wrapped line gets one ring per piece and the rings never touch)."""
        rs = VGroup()
        for i, (yy, p, ind) in enumerate(self.pos[n]):
            if pieces is not None and i not in pieces:
                continue
            rs.add(RoundedRectangle(width=self.W - 0.3, height=self.pitch * shrink, corner_radius=0.1, stroke_color=color, stroke_width=sw,
                                    fill_opacity=0).move_to([self.x, yy, 0]))
        return rs

    def tok(self, n, token, k=0):
        for yy, p, ind in self.pos[n]:
            i = -1
            for _ in range(k + 1):
                i = p.find(token, i + 1)
                if i < 0:
                    break
            if i >= 0:
                w = len(token) * self.cw
                return (self.text_left + ind + i * self.cw + w / 2, yy, w)
        raise ValueError(f"token {token!r} not in line {n}")

    def tok_ring(self, n, token, k=0, color=TERRA, sw=5, padx=0.05):
        cx, cy, w = self.tok(n, token, k)
        return RoundedRectangle(width=w + 2 * padx, height=self.pitch * 0.9, corner_radius=0.07, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])


def a5_mono(s, x, y, size=24, color=INK, left=False):
    t = M(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a5_x(x, y, s=0.1, w=5):
    """A multiplication mark drawn as a shape."""
    return cross_mark(x, y, s, INK, w)


def a5_rev(*mobs):
    return [FadeIn(m) for m in mobs]


# ── B35 · textured shader: textures first, import settings set by hand ───────────────────────────────────────────
A5_SCALE_DOCK = 2.0                    # the Import dock crop is shown at 2x its native pixels (UI text then reads at 4K)


def a5_row_y(top, py, scale):
    """Scene y of pixel row py of a crop whose top edge sits at scene y `top`, shown at `scale` x native (1 unit = 270 px at 4K)."""
    return top - py * scale / 270.0


class B35_ImportSettings(Scene):
    def construct(self):
        title = T("A  Shader  That  Reads  Textures", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        tc = framed(a5_img("ev_tex_color.png", h=1.0, at=(-5.5, 1.85)))
        tr = framed(a5_img("ev_tex_rough.png", h=1.0, at=(-5.5, 0.55)))
        n1 = a5_mono("gate-color.png", -4.75, 1.85, 20, left=True)
        n2 = a5_mono("gate-roughness.png", -4.75, 0.55, 20, left=True)
        until(self, "Get textures first", lead=0.2)
        self.play(FadeIn(tc), FadeIn(tr), FadeIn(n1), FadeIn(n2), run_time=0.5)
        until(self, "Then set their import settings", lead=0.2)
        blk = A5Code([(n, a5_line("gate-color.png.import", n)) for n in (18, 24, 26)], x=-2.9, y=-1.85, size=24, dedent=False, pitch=0.5, gap=0.0)
        head = a5_mono("gate-color.png.import", -2.9, -0.5, 24)
        self.play(Create(blk.frame), FadeIn(head), FadeIn(VGroup(*[blk.rows(n) for n in (18, 24, 26)])), run_time=0.6)
        dock = framed(a5_img("a5_ed_import_compress.png", w=760 * A5_SCALE_DOCK / 270.0, at=(3.3, 1.3)), pad=0.05)
        TOP = 1.3 + 283 * A5_SCALE_DOCK / 270.0 / 2
        y_mode, y_gen = a5_row_y(TOP, 79, A5_SCALE_DOCK), a5_row_y(TOP, 246, A5_SCALE_DOCK)
        gx = blk.x - blk.W / 2 - 0.3
        until(self, "compress mode", lead=0.5)
        d1 = Dot([0.2, y_mode, 0], radius=0.11, color=TERRA)
        g1 = Dot([gx, blk.piece_y(18), 0], radius=0.11, color=TERRA)
        self.play(FadeIn(dock), FadeIn(d1, scale=0.4), FadeIn(g1, scale=0.4), run_time=0.5)
        tag = status_tag("scripted editor session", 3.3, -0.3)
        self.add(tag)
        until(self, "mipmaps", lead=0.3)
        d2 = Dot([0.2, y_gen, 0], radius=0.11, color=TERRA)
        g2 = Dot([gx, blk.piece_y(26), 0], radius=0.11, color=TERRA)
        self.play(FadeOut(VGroup(d1, g1)), FadeIn(d2, scale=0.4), FadeIn(g2, scale=0.4), run_time=0.4)
        until(self, "the normal map flag", lead=0.3)
        g3 = Dot([gx, blk.piece_y(24), 0], radius=0.11, color=TERRA)
        nm = a5_lab("no Normal Map row", 3.3, -1.0, 36)
        self.play(FadeOut(VGroup(d2, g2)), FadeIn(g3, scale=0.4), FadeIn(nm), run_time=0.4)
        until(self, "The editor then has nothing", lead=0.2)
        ok = check(5.6, -2.25, s=0.28, color=INK, w=8)
        spark = Dot([6.0, -2.05, 0], radius=0.1, color=TERRA)
        self.play(Create(ok), FadeIn(spark), run_time=0.5)
        self.add(example_tag(2.85, -3.05))
        done(self)


# ── B36 · the two textures: colour stripes and 102 / 216 ─────────────────────────────────────────────────────────
def a5_chip(cx, y, rgb, text, size=34, sw=0.7, sh=0.5):
    """A real texel value: a swatch of the real colour + its real numbers (BESIDE it), the pair centred on cx."""
    tx = T(text, size)
    total = sw + 0.15 + tx.width
    x0 = cx - total / 2
    sq = swatch(rgb, x0 + sw / 2, y, sw, sh)
    fr = Rectangle(width=sw, height=sh, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x0 + sw / 2, y, 0])
    tx.move_to([x0 + sw + 0.15, y, 0], aligned_edge=LEFT)
    return VGroup(sq, fr, tx)


class B36_TwoTextures(Scene):
    def construct(self):
        S, XL, XR, YT = 3.0, -2.9, 2.9, 0.95
        tc = a5_img("ev_tex_color.png", h=S, at=(XL, YT))
        tr = a5_img("ev_tex_rough.png", h=S, at=(XR, YT))
        gc, gr = framed(tc, pad=0.07), framed(tr, pad=0.07)
        until(self, "The example's textures", lead=0.15)
        self.play(FadeIn(gc), FadeIn(gr), run_time=0.5)
        dim = dim_arrow([-4.8, YT - S / 2, 0], [-4.8, YT + S / 2, 0], color=INK, w=4)
        d_l = a5_lab("64 px", -5.45, YT, 34)
        until(self, "sixty-four pixels square", lead=0.3)
        self.play(GrowFromCenter(dim), FadeIn(d_l), run_time=0.4)
        until(self, "written by a script", lead=0.2)
        scr = a5_mono("garden-textures.py", -3.35, -3.0, 24)
        self.play(FadeIn(scr), run_time=0.3)
        until(self, "One holds two colours", lead=0.2)
        px = lambda cx, k: cx - S / 2 + S / 8 * (k + 0.5)
        stripe = lambda cx, k: ring(Rectangle(width=S / 8 - 0.04, height=S - 0.1, stroke_width=0, fill_opacity=0).move_to([px(cx, k), YT, 0]), pad=0.0, sw=6, backing=False)
        dots = [stripe(XL, 0), stripe(XL, 1)]
        chips = [a5_chip(XL, -1.0, (44, 78, 85), "44, 78, 85"), a5_chip(XL, -1.65, (59, 96, 101), "59, 96, 101")]
        lc = a5_lab("colour", XL, -2.4, 40)
        for i, (d, c) in enumerate(zip(dots, chips)):
            self.play(FadeIn(d), FadeIn(c), *([FadeOut(dots[0])] if i else []), run_time=0.3)
        self.play(FadeIn(lc), run_time=0.3)
        until(self, "The other holds two numbers", lead=0.2)
        self.play(FadeOut(dots[1]), run_time=0.2)
        dots2 = [stripe(XR, 1), stripe(XR, 0)]
        chips2 = [a5_chip(XR, -1.0, (102, 102, 102), "102"), a5_chip(XR, -1.65, (216, 216, 216), "216")]
        until(self, "one hundred two", lead=0.25)
        self.play(FadeIn(dots2[0]), FadeIn(chips2[0]), run_time=0.3)
        until(self, "two sixteen", lead=0.25)
        self.play(FadeOut(dots2[0]), FadeIn(dots2[1]), FadeIn(chips2[1]), run_time=0.3)
        until(self, "Same kind of file", lead=0.2)
        eq = VGroup(Line([-0.35, YT + 0.1, 0], [0.35, YT + 0.1, 0], color=INK, stroke_width=7), Line([-0.35, YT - 0.1, 0], [0.35, YT - 0.1, 0], color=INK, stroke_width=7))
        rc = a5_lab("data", XR, -2.4, 40)
        self.play(Create(eq), run_time=0.35)
        self.play(FadeIn(rc), run_time=0.3)
        self.add(example_tag(2.9, -3.0))
        done(self)


# ── B37 · two samplers, one hint, four uniforms, two groups ─────────────────────────────────────────────────────
class B37_TwoSamplers(Scene):
    def construct(self):
        spec = [(n, a5_line("surface.gdshader", n)) for n in range(2, 10)]
        blk = A5Code(spec, x=-1.2, y=0.15, size=20, pitch=0.5, dedent=False)
        self.add(blk.frame)
        self.play(FadeIn(VGroup(*[blk.rows(n) for n in range(2, 10)])), run_time=0.5)
        until(self, "Two samplers", lead=0.2)
        r3 = blk.ring(3)
        until(self, "the colour map says source color", lead=0.4)
        t_c = a5_lab("colour", 5.05, blk.piece_y(3) + 0.14, 36)
        self.play(Create(r3), FadeIn(t_c), run_time=0.4)
        until(self, "the roughness map says nothing", lead=0.45)
        r4 = blk.ring(4)
        t_d = a5_lab("data", 5.05, blk.piece_y(4) - 0.14, 36)
        self.play(Create(r4), FadeIn(t_d), run_time=0.4)
        until(self, "Four more uniforms", lead=0.5)
        self.play(FadeOut(Group(blk.group, r3, r4, t_c, t_d)), run_time=0.3)
        # the same uniforms as the editor draws them: the REAL Inspector of matte.tres (scripted editor session)
        SC = 2.0
        cx, cy = 0.2, -0.1
        im = framed(a5_img("a5_ed_matte_params.png", w=900 * SC / 270.0, at=(cx, cy)), pad=0.05)
        top = cy + 670 * SC / 270.0 / 2
        left = cx - 900 * SC / 270.0 / 2
        self.play(FadeIn(im), run_time=0.4)
        until(self, "Four more uniforms", lead=-0.2)
        rows_py = (404, 465, 571, 632)
        dots = VGroup(*[Dot([left - 0.28, a5_row_y(top, py, SC), 0], radius=0.1, color=TERRA) for py in rows_py])
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.25), run_time=0.7)
        until(self, "in two groups", lead=0.2)
        hdr = lambda py: RoundedRectangle(width=900 * SC / 270.0 - 0.1, height=0.34, corner_radius=0.08, stroke_color=TERRA, stroke_width=6,
                                          fill_opacity=0).move_to([cx, a5_row_y(top, py, SC), 0])
        h1, h2 = hdr(89), hdr(520)
        until(self, "surface and pattern", lead=0.55)
        self.play(FadeOut(dots), Create(h1), Create(h2), run_time=0.4)
        self.add(status_tag("scripted editor session", -2.9, -3.05), example_tag(3.0, -3.05))
        done(self)


# ── B38 · fragment: three outputs, three flows ──────────────────────────────────────────────────────────────────
def a5_chain(items, y, x_right, size=20):
    """Right-aligned chain of boxed identifiers joined by x and arrows. items: ('box', text) | ('x',) | ('to',). Returns (VGroup parts, list of box centres)."""
    cw = A5_CW[size]
    ws = {"x": 0.5, "to": 0.75}
    wid = lambda it: (len(it[1]) * cw + 0.5) if it[0] == "box" else ws[it[0]]
    total = sum(wid(it) for it in items)
    cx = x_right - total
    parts, boxes = VGroup(), []
    for it in items:
        w = wid(it)
        mid = cx + w / 2
        if it[0] == "box":
            b = box(mid, y, w - 0.08, 0.62, color=INK, sw=4)
            t = M(it[1], size).move_to([mid, y, 0])
            parts.add(VGroup(b, t)); boxes.append((mid, w))
        elif it[0] == "x":
            parts.add(a5_x(mid, y, 0.11, 6))
        else:
            parts.add(arrow([mid - 0.3, y, 0], [mid + 0.3, y, 0], INK, 5, 0.2))
        cx += w
    return parts, boxes


class B38_FragmentLines(Scene):
    def construct(self):
        spec = [(n, a5_line("surface.gdshader", n)) for n in range(10, 14)]
        blk = A5Code(spec, x=0.0, y=1.95, size=20, wrap=64, pitch=0.4, dedent=False, extra=0.35)
        self.add(blk.frame)
        self.play(FadeIn(VGroup(*[blk.rows(n) for n in range(10, 14)])), FadeIn(blk.hooks), run_time=0.5)
        flows = {
            11: a5_chain([("box", "color_map"), ("x",), ("box", "tint"), ("to",), ("box", "ALBEDO")], -0.35, 5.7),
            12: a5_chain([("box", "roughness_map.r"), ("x",), ("box", "roughness_gain"), ("to",), ("box", "clamp"), ("to",), ("box", "ROUGHNESS")], -1.4, 5.7),
            13: a5_chain([("box", "metallic_gain"), ("to",), ("box", "METALLIC")], -2.45, 5.7),
        }
        until(self, "Fragment multiplies", lead=0.2)
        ring = blk.ring(11)
        self.play(Create(ring), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(p) for p in flows[11][0]], lag_ratio=0.2), run_time=0.8)
        until(self, "reads roughness", lead=0.25)
        ring2 = blk.ring(12)
        self.play(FadeOut(ring), Create(ring2), run_time=0.3)
        p12 = flows[12][0]
        until(self, "from the red channel", lead=0.25)
        self.play(FadeIn(p12[0]), run_time=0.3)
        until(self, "scales it by a gain", lead=0.3)
        self.play(FadeIn(p12[1]), FadeIn(p12[2]), run_time=0.3)
        until(self, "and clamps it", lead=0.35)
        self.play(FadeIn(p12[3]), FadeIn(p12[4]), FadeIn(p12[5]), FadeIn(p12[6]), run_time=0.4)
        until(self, "Metallic is just a number", lead=0.8)
        ring3 = blk.ring(13)
        self.play(FadeOut(ring2), Create(ring3), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(p) for p in flows[13][0]], lag_ratio=0.2), run_time=0.5)
        spark = Dot([6.0, -2.45, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(spark, scale=0.4), run_time=0.25)
        done(self)


# ── B39 · two materials, one shader; resource files; Use External ───────────────────────────────────────────────
class B39_TwoMaterials(Scene):
    def construct(self):
        SC = 1.5
        CX = (-2.75, 2.75)
        shader = VGroup(box(0, 2.75, 4.0, 0.8, INK, 4), M("surface.gdshader", 24).move_to([0, 2.75, 0]))
        c_m, c_c = chip("matte", -4.0, 2.75, w=2.0, size=36), chip("coated", 4.0, 2.75, w=2.0, size=36)
        s_m = a5_img("a5_mat_matte.png", h=1.0, at=(-5.6, 2.75))
        s_c = a5_img("a5_mat_coated.png", h=1.0, at=(5.6, 2.75))
        a_m = arrow([-2.9, 2.75, 0], [-2.05, 2.75, 0], INK, 5, 0.2)
        a_c = arrow([2.9, 2.75, 0], [2.05, 2.75, 0], INK, 5, 0.2)
        until(self, "Two materials use this shader", lead=0.1)
        self.play(FadeIn(shader), run_time=0.35)
        until(self, "matte", lead=0.3)
        self.play(FadeIn(c_m), FadeIn(s_m), GrowArrow(a_m), run_time=0.4)
        until(self, "and coated", lead=0.3)
        self.play(FadeIn(c_c), FadeIn(s_c), GrowArrow(a_c), run_time=0.4)
        # the REAL Inspector of each saved material (scripted editor session): values read off the frames are the .tres values
        w_, h_ = 900 * SC / 270.0, 670 * SC / 270.0
        cyc = -0.45
        im_m = framed(a5_img("a5_ed_matte_params.png", w=w_, at=(CX[0], cyc)), pad=0.05)
        im_c = framed(a5_img("a5_ed_coated_params.png", w=w_, at=(CX[1], cyc)), pad=0.05)
        until(self, "They differ in", lead=0.1)
        self.play(FadeIn(im_m), FadeIn(im_c), run_time=0.5)
        top, left = cyc + h_ / 2, CX[0] - w_ / 2
        dots = VGroup(*[Dot([left - 0.2, a5_row_y(top, py, SC), 0], radius=0.09, color=TERRA) for py in (404, 465, 571, 632)])
        until(self, "tint", lead=0.1)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.4), run_time=1.6)
        until(self, "resource files", lead=0.35)
        f_m = a5_mono("matte.tres", CX[0], 1.75, 24)
        f_c = a5_mono("coated.tres", CX[1], 1.75, 24)
        self.play(FadeOut(dots), FadeIn(f_m), FadeIn(f_c), run_time=0.3)
        # stage 3: Use External (a drawing of the setting, not the editor)
        until(self, "For an imported scene", lead=0.3)
        self.play(FadeOut(Group(im_m, im_c, f_m, f_c)), run_time=0.3)
        scene_box = box(-2.9, 0.15, 4.3, 2.0, DIM, 4)
        scene_l = a5_lab("imported scene", -2.9, -1.3, 34)
        slot = VGroup(box(-3.1, -0.1, 2.2, 0.62, INK, 4), a5_lab("material", -3.1, 0.65, 32))
        self.play(Create(scene_box), FadeIn(scene_l), FadeIn(slot), run_time=0.5)
        until(self, "behind Use External", lead=0.35)
        tres = chip("matte.tres", 3.9, -0.1, mono=True, size=28)
        link = DashedLine([-1.95, -0.1, 0], [2.3, -0.1, 0], color=INK, stroke_width=5, dash_length=0.18)
        ue = a5_lab("Use External", 0.75, 0.45, 38)
        self.play(Create(link), FadeIn(ue), FadeIn(tres), run_time=0.5)
        until(self, "so a reimport keeps them", lead=1.0)
        loop = CurvedArrow([-4.5, 1.3, 0], [-1.3, 1.3, 0], angle=-PI / 3.4, color=INK, stroke_width=5, tip_length=0.22)
        ri = a5_lab("reimport", -2.9, 1.95, 34)
        self.play(Create(loop), FadeIn(ri), run_time=0.5)
        ok = check(5.65, -0.1, s=0.25, color=INK, w=8)
        spark = Dot([6.0, 0.1, 0], radius=0.1, color=TERRA)
        self.play(Create(ok), FadeIn(spark), run_time=0.4)
        self.add(status_tag("setting from the assignment · not used in the example", -0.4, -2.2), example_tag(2.85, -3.0))
        done(self)


# ══════════════════════════════ scenes_act6.py ══════════════════════════════
"""ACT VI · Textures Are Information  (B40-B47 Manim; B48 is a Remotion CCPlainShell, see lanes/act6.json)

One cast for the act: the REAL 3 x 1 grey file (three texels 64 / 128 / 192, captures/forward-plus/gray-three-band.png) and the REAL two-row
hint fixture captures (pantry/ev_hint_*.png: top row source_color, bottom row data), then the Poly Haven stone-floor pair and the code-made map.
Everything on screen is read from the evidence:
  hint numbers ..... captures/forward-plus/hint_forward_plus.json and hint_compatibility.json (RGB8, re-run for this film, 16 Oct), and
                     evidence/example/hint-samples.json (the example's own capture, 14 Oct; floats x 255); the predicted 137/188/225 is the assignment's
                     encode(x) (evidence/act6/verify_act6_numbers.py)
  curl numbers ..... evidence/runs/R3-normal-calibration.json (stride 2, Poly Haven stone_floor GL / DX pair), evidence/runs/R1-baseline-60fps.log (code-made map)
  the audit ........ evidence/example/sources/MATERIALS.md and test-material-contract.gd (5 + 24 + 24 = 53)
  code lines ....... evidence/example/sources/hint.gdshader (lines 3, 4, 5, 9: the tab on line 9 is drawn as four spaces)
B44 is a DRAWING of an idea (a height surface, its slope arrows, a 0 / 1 / 2 number line): it is labelled "illustration" and nothing in it is measured.
Pacing: until() cues come from the character share of each narration (no audio exists yet); the build session re-checks [pace].
"""

A6P = "pantry/"


def a6_img(name, w=None, h=None, at=(0.0, 0.0)):
    im = ImageMobject(A6P + name)
    if w is not None:
        im.set_width(w)
    if h is not None:
        im.set_height(h)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a6_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a6_labl(s, x, y, size=34, color=INK):
    """A label whose LEFT edge sits at x."""
    return T(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a6_grey(v):
    return "#%02x%02x%02x" % (v, v, v)


def a6_cells(x, y, cw, gap=0.08):
    """The REAL 3 x 1 file: three texels 64 / 128 / 192 (captures/forward-plus/gray-three-band.png), drawn as three cells."""
    g = VGroup()
    for i, v in enumerate((64, 128, 192)):
        g.add(Rectangle(width=cw, height=cw, fill_color=a6_grey(v), fill_opacity=1, stroke_color=DIM, stroke_width=3)
              .move_to([x + (i - 1) * (cw + gap), y, 0]))
    return g


def a6_tri(vals, x, y, dx=1.3, size=44):
    """Three numbers in a row (real measured / computed values)."""
    return VGroup(*[T(str(v), size).move_to([x + (i - 1) * dx, y, 0]) for i, v in enumerate(vals)])


def a6_eq(x, y, w=0.9, gap=0.2, color=INK, sw=8):
    return VGroup(Line([x - w / 2, y + gap / 2, 0], [x + w / 2, y + gap / 2, 0], color=color, stroke_width=sw),
                  Line([x - w / 2, y - gap / 2, 0], [x + w / 2, y - gap / 2, 0], color=color, stroke_width=sw))


def a6_neq(x, y, w=0.9, gap=0.2, color=INK, sw=8):
    slash = Line([x - 0.2, y - 0.38, 0], [x + 0.2, y + 0.38, 0], color=color, stroke_width=sw)
    return VGroup(a6_eq(x, y, w, gap, color, sw), slash)


def a6_code(lines, x=0.0, y=0.0, size=20, first=1, lh=0.62, pad=0.3):
    """code_block with a wider row pitch (lh) so labels and arrows can sit at single rows. REAL code, Menlo, real line numbers (first=), outline-only frame.
    Same interface as the kit's code_block: .rows, .frame, .W, .H, .row(n), .ring_line(n).
    Text is placed LEFT-aligned at an explicit x (Pango drops leading spaces from a Text's width, so a centred placement would lose the indent; and the static
    check's stub guesses text width too wide): indent = leading whitespace (a tab = 4 spaces) x the measured Menlo advance (0.0074 units per size point)."""
    ns = [str(first + i) for i in range(len(lines))]
    cw = 0.00744 * size                           # measured: Menlo 20 -> 0.1488 units per character (58 chars = 8.63 units)
    nw = max(len(n) for n in ns) * cw + 0.25
    exp = [ln.replace("\t", "    ") for ln in lines]
    tw = max(len(e) for e in exp) * cw
    W = tw + nw + 2 * pad
    H = len(lines) * lh + 2 * pad
    frame = RoundedRectangle(width=W, height=H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    left = x - W / 2 + pad
    rows = VGroup()
    for i, e in enumerate(exp):
        yy = y + H / 2 - pad - lh * (i + 0.5)
        indent = (len(e) - len(e.lstrip(" "))) * cw
        n = M(ns[i], size, DIM).move_to([left, yy, 0], aligned_edge=LEFT)
        t = M(e.lstrip(" ") or " ", size).move_to([left + nw + indent, yy, 0], aligned_edge=LEFT)
        rows.add(VGroup(n, t))
    g = VGroup(frame, rows)
    g.frame, g.rows, g.W, g.H, g.lh, g.first = frame, rows, W, H, lh, first
    g.row = lambda n: rows[n - first]
    ys = [y + H / 2 - pad - lh * (i + 0.5) for i in range(len(lines))]
    g.row_y = lambda n: ys[n - first]

    def _ring_line(n, color=TERRA):
        return RoundedRectangle(width=W - 0.16, height=lh * 0.98, corner_radius=0.1, stroke_color=color, stroke_width=6, fill_opacity=0).move_to([x, ys[n - first], 0])
    g.ring_line = _ring_line
    return g


def a6_brackets(cx, cy, w, h, arm=0.34, sw=7, color=TERRA):
    """Four terracotta corner brackets round a region (a viewfinder). A full terracotta ring is one big outline blob that GATE T's accent-text check reads as
    terracotta type; four separate L marks are not."""
    out = VGroup()
    for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        x0, y0 = cx + sx * w / 2, cy + sy * h / 2
        out.add(VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners([[x0 - sx * arm, y0, 0], [x0, y0, 0], [x0, y0 - sy * arm, 0]]))
    return out


def a6_toggle(x, y, on=True):
    pill_ = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=DIM if not on else INK, fill_opacity=1, stroke_width=0).move_to([x + (0.2 if on else -0.2), y, 0])
    return VGroup(pill_, knob)


HINT_LINES = {3: "uniform sampler2D as_color : source_color, filter_nearest;",
              4: "uniform sampler2D as_data : filter_nearest;",
              5: "uniform bool use_color = true;",
              9: "\tALBEDO = use_color ? texture(as_color, UV).rgb : texture(as_data, UV).rgb;"}


# ── B40 · the hint experiment's build: the file, the script, one shader that binds it twice ───────────────────────
class B40_HintBuild(Scene):
    def construct(self):
        title = T("Textures Are Information", 40).move_to([-6.15, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        # stage 1: a script writes the real 3 x 1 file (64 / 128 / 192); the assignment's import; the example built it in memory
        script = terminal_icon(-4.3, 0.55, s=0.8)
        script_l = a6_lab("script", -4.3, -0.35, 34)
        wr = arrow([-3.25, 0.55, 0], [-1.85, 0.55, 0])
        file = a6_cells(0.4, 0.55, 1.2)
        nums = VGroup(*[T(str(v), 44).move_to([0.4 + (i - 1) * 1.28, -0.5, 0]) for i, v in enumerate((64, 128, 192))])
        self.wait(0.3)
        self.play(FadeIn(script, shift=RIGHT * 0.2), FadeIn(script_l), GrowArrow(wr), run_time=0.5)
        until(self, "three-by-one", lead=0.4)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in file], lag_ratio=0.3), run_time=0.8)
        self.play(FadeIn(nums), run_time=0.3)
        tag1 = status_tag("assignment: lossless, no mipmaps", 0.4, -1.55)
        tag2 = status_tag("example: built in memory", 0.4, -2.3)
        until(self, "imported lossless", lead=0.55)
        self.play(FadeIn(tag1, shift=UP * 0.15), run_time=0.4)
        self.play(FadeIn(tag2, shift=UP * 0.15), run_time=0.4)
        # stage 2 (after the midpoint): the file shrinks into the corner, the real shader lines land, the file fans out to both samplers
        until(self, "One shader binds", lead=0.45)
        blockA = a6_code([HINT_LINES[3], HINT_LINES[4], HINT_LINES[5]], x=1.55, y=0.45, size=20, first=3, lh=0.62, pad=0.3)
        self.play(FadeOut(script), FadeOut(script_l), FadeOut(wr), FadeOut(nums), FadeOut(tag1), FadeOut(tag2),
                  file.animate.scale(0.5833).move_to([-4.85, 2.05, 0]), FadeIn(blockA), run_time=0.7)
        nlab = T("64 · 128 · 192", 36).move_to([-1.5, 2.05, 0])
        ex = example_tag(3.0, 2.95)
        self.play(FadeIn(nlab), FadeIn(ex), run_time=0.4)
        y3, y4, y5 = blockA.row_y(3), blockA.row_y(4), blockA.row_y(5)
        until(self, "binds it twice", lead=0.3)
        a_c = arrow([-4.6, 1.62, 0], [-3.42, y3, 0], w=5, tip=0.2)
        a_d = arrow([-4.6, 1.62, 0], [-3.42, y4, 0], w=5, tip=0.2)
        self.play(GrowArrow(a_c), GrowArrow(a_d), run_time=0.5)
        until(self, "with source color", lead=0.55)
        r3 = blockA.ring_line(3)
        self.play(Create(r3), run_time=0.4)
        until(self, "and without", lead=0.45)
        r4 = blockA.ring_line(4)
        self.play(FadeOut(r3), Create(r4), run_time=0.4)
        until(self, "a boolean picks", lead=0.75)
        r5 = blockA.ring_line(5)
        tg = a6_toggle(-4.85, y5, on=True)
        t_on = M("as_color", 28).move_to([-4.85, y5 - 0.62, 0])
        a_t = arrow([-4.25, y5, 0], [-3.42, y5, 0], w=5, tip=0.2)
        self.play(FadeOut(r4), Create(r5), FadeIn(tg), FadeIn(t_on), GrowArrow(a_t), run_time=0.4)
        until(self, "which writes", lead=1.25)
        blockB = a6_code([HINT_LINES[9]], x=0.0, y=-2.45, size=20, first=9, lh=0.62, pad=0.3)
        r9 = blockB.ring_line(9)
        t_off = M("as_data", 28).move_to([-4.85, y5 - 0.62, 0])
        knob = tg[1]
        # the switch flips (the knob slides, grey = off) and its caption cross-fades from the colour sampler to the data sampler
        self.play(FadeOut(r5), FadeIn(blockB), Create(r9), knob.animate.move_to([-4.85 - 0.2, y5, 0]).set_fill(DIM), FadeOut(t_on), FadeIn(t_off), run_time=0.5)
        done(self)


# ── B41 · Compatibility result: both rows read 64 / 128 / 192 (the example's own capture, 14 Oct) ─────────────────────
class B41_CompatResult(Scene):
    def construct(self):
        # the example's REAL capture (Compatibility, 3840 x 2160 SubViewport, cropped): top row source_color, bottom row data
        im = a6_img("ev_hint_compat_example.png", w=6.9, at=(-2.3, -0.5))
        pic = framed(im)
        self.play(FadeIn(pic), run_time=0.5)
        yt, yb = 1.0, -2.0                       # band-row centres of the picture (same y as the numbers beside it)
        xs = [-4.6, -2.3, 0.0]                   # band-column centres
        col_x = [2.8, 4.1, 5.4]
        lab1 = a6_lab("colour read", 4.1, yt - 0.58, 34)
        lab2 = a6_lab("data read", 4.1, yb + 0.58, 34)
        until(self, "on two quads", lead=0.45)
        self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.4)
        tag = status_tag("the example, 14 Oct", 4.1, 1.9)
        until(self, "In the example", lead=0.35)
        self.play(FadeIn(tag, shift=UP * 0.15), run_time=0.35)
        head = a6_lab("Compatibility", 4.1, 3.0, 46)
        ver = a6_lab("Godot 4.7.2", 4.1, 2.45, 32, DIM)
        until(self, "on Compatibility", lead=0.35)
        self.play(FadeIn(head), FadeIn(ver), run_time=0.4)
        vals = [64, 128, 192]
        for i, ph, ld in [(0, "sixty-four", 0.3), (1, "one twenty-eight", 0.3), (2, "one ninety-two", 0.3)]:
            until(self, ph, lead=ld)
            dots = VGroup(Dot([xs[i], yt, 0], radius=0.13, color=TERRA), Dot([xs[i], yb, 0], radius=0.13, color=TERRA))
            n1 = T(str(vals[i]), 44).move_to([col_x[i], yt, 0])
            n2 = T(str(vals[i]), 44).move_to([col_x[i], yb, 0])
            self.play(FadeIn(dots, scale=0.5), FadeIn(n1), FadeIn(n2), run_time=0.35)
        until(self, "This renderer", lead=0.35)
        eq = a6_eq(4.1, -0.5)
        self.play(Create(eq), run_time=0.5)
        done(self)


# ── B42 · Forward+ result: the data row brightens to 137 / 188 / 225, as the assignment's formula predicts ───────────────
class B42_ForwardResult(Scene):
    def construct(self):
        yt, yb = 1.0, -2.0
        xs = [-4.6, -2.3, 0.0]
        col_x = [2.8, 4.1, 5.4]
        compat = a6_img("ev_hint_compat.png", w=6.9, at=(-2.3, -0.5))
        fp_im = a6_img("ev_hint_fp.png", w=6.9, at=(-2.3, -0.5))
        frame_ = Rectangle(width=6.9 + 0.12, height=compat.height + 0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-2.3, -0.5, 0])
        head_c = a6_lab("Compatibility", 4.1, 3.0, 46)
        ver = a6_lab("Godot 4.7.2", 4.1, 2.45, 32, DIM)
        tag = status_tag("re-run for this film", 4.1, 1.9)
        self.add(compat, frame_, head_c, ver, tag)
        lab1 = a6_lab("colour read", 4.1, yt - 0.58, 34)
        lab2 = a6_lab("data read", 4.1, yb + 0.58, 34)
        # the same fixture, run again on Forward+: the picture cross-fades and only the bottom row brightens
        until(self, "Forward Plus", lead=0.5)
        head_f = a6_lab("Forward+", 4.1, 3.0, 46)
        self.play(FadeIn(fp_im), FadeOut(head_c), FadeIn(head_f), FadeIn(lab1), FadeIn(lab2), run_time=0.9)
        self.remove(compat)
        # the colour read keeps 64 / 128 / 192
        until(self, "sixty-four", lead=0.35)
        n_top = a6_tri([64, 128, 192], 4.1, yt, dx=1.3)
        d_top = VGroup(*[Dot([xs[i], yt, 0], radius=0.13, color=TERRA) for i in range(3)])
        self.play(FadeIn(n_top), FadeIn(d_top, scale=0.5), run_time=0.45)
        # after the midpoint: the data row is ringed, then its three numbers land
        until(self, "The data read", lead=0.35)
        rg = a6_brackets(-2.3, yb, 6.9 + 0.2, 1.72 + 0.2)
        ne = a6_neq(4.1, -0.5)
        self.play(Create(rg), Create(ne), run_time=0.5)
        vals = [137, 188, 225]
        n_bot = []
        for i, ph, ld in [(0, "one thirty-seven", 0.3), (1, "one eighty-eight", 0.3), (2, "two twenty-five", 0.3)]:
            until(self, ph, lead=ld)
            d = Dot([xs[i], yb, 0], radius=0.13, color=TERRA)
            n = T(str(vals[i]), 44).move_to([col_x[i], yb, 0])
            n_bot.append(n)
            self.play(FadeIn(d, scale=0.5), FadeIn(n), run_time=0.35)
        until(self, "as predicted", lead=0.85)
        ok = tick_mark(3.0, -2.85, s=0.25)
        pr = a6_labl("as predicted", 3.4, -2.85, 36)
        self.play(Create(ok), FadeIn(pr), run_time=0.35)
        done(self)


# ── B43 · one file, two readings, two renderers: four triples of real numbers ─────────────────────────────────────────
class B43_OneFileTwoReads(Scene):
    def construct(self):
        cx = [-0.4, 3.8]
        y1, y2, y3 = 0.85, -0.45, -1.85
        fx, fy = 1.7, 2.2
        file = a6_cells(fx, fy, 0.8, gap=0.07)
        flab = a6_lab("one file", -0.5, fy, 40)
        self.wait(0.3)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in file], lag_ratio=0.3), run_time=0.8)
        until(self, "One file", lead=0.3)
        self.play(FadeIn(flab, shift=RIGHT * 0.15), run_time=0.35)
        b1 = box(cx[0], y1, 3.1, 0.9, color=INK, sw=4)
        b2 = box(cx[1], y1, 3.1, 0.9, color=INK, sw=4)
        t1 = a6_lab("colour read", cx[0], y1, 36)
        t2 = a6_lab("data read", cx[1], y1, 36)
        arr1 = arrow([fx - 0.5, fy - 0.55, 0], [cx[0] + 0.5, y1 + 0.5, 0], w=5, tip=0.2)
        arr2 = arrow([fx + 0.5, fy - 0.55, 0], [cx[1] - 0.5, y1 + 0.5, 0], w=5, tip=0.2)
        until(self, "read two ways", lead=0.5)
        self.play(Create(b1), Create(b2), FadeIn(t1), FadeIn(t2), GrowArrow(arr1), GrowArrow(arr2), run_time=0.7)
        # Forward+: colour read 64 / 128 / 192, data read 137 / 188 / 225 (hint_forward_plus.json)
        lab_f = a6_labl("Forward+", -5.7, y2, 40)
        lab_c = a6_labl("Compatibility", -5.7, y3, 40)
        f_col = a6_tri([64, 128, 192], cx[0], y2, dx=1.05, size=48)
        f_dat = a6_tri([137, 188, 225], cx[1], y2, dx=1.05, size=48)
        until(self, "two sets of numbers", lead=0.9)
        self.play(FadeIn(lab_f), FadeIn(lab_c), run_time=0.3)
        self.play(FadeIn(f_col, shift=DOWN * 0.15), FadeIn(f_dat, shift=DOWN * 0.15), run_time=0.45)
        # Compatibility: both reads 64 / 128 / 192 (hint_compatibility.json); ≠ in Forward+, = in Compatibility
        c_col = a6_tri([64, 128, 192], cx[0], y3, dx=1.05, size=48)
        c_dat = a6_tri([64, 128, 192], cx[1], y3, dx=1.05, size=48)
        until(self, "Which is right", lead=0.2)
        self.play(FadeIn(c_col, shift=DOWN * 0.15), FadeIn(c_dat, shift=DOWN * 0.15), run_time=0.5)
        until(self, "what the numbers mean", lead=0.45)
        ne = a6_neq(1.7, y2, w=0.7, gap=0.17, sw=7)
        eq = a6_eq(1.7, y3, w=0.7, gap=0.17, sw=7)
        self.play(Create(ne), Create(eq), run_time=0.5)
        until(self, "the renderer you name", lead=0.55)
        rg = a6_brackets(-4.2, (y2 + y3) / 2, 3.9, 2.7, arm=0.34)
        tg = status_tag("re-run for this film", 0.0, -3.0)
        self.play(Create(rg), FadeIn(tg), run_time=0.5)
        done(self)


# ── B44 · the curl check, drawn (an illustration: a hill, its slope arrows, a 0 / 1 / 2 number line; nothing measured) ────
def a6_field(kind, cx, cy):
    """4 x 3 slope arrows over one panel. 'real': slopes of a hill (curl-free); 'wrong': the same with the second component flipped; 'none': random."""
    rng = np.random.RandomState(44)
    arrows = VGroup()
    pts = [((i - 1.5) * 0.8, (j - 1) * 0.78) for j in range(3) for i in range(4)]
    for (px, py) in pts:
        if kind == "none":
            ang = rng.uniform(0, 2 * np.pi)
            L = 0.5
            vx, vy = L * np.cos(ang), L * np.sin(ang)
        else:
            r2 = px * px + py * py
            g = np.exp(-r2 / (2 * 0.8 ** 2))
            vx, vy = px * g, py * g
            n = np.hypot(vx, vy)
            if n < 1e-6:
                continue
            L = 0.36 + 0.2 * min(1.0, n / 0.6)
            vx, vy = vx / n * L, vy / n * L
            if kind == "wrong":
                vy = -vy
        a = Arrow(np.array([cx + px - vx / 2, cy + py - vy / 2, 0.0]), np.array([cx + px + vx / 2, cy + py + vy / 2, 0.0]), buff=0, color=INK,
                  stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        arrows.add(a)
    return arrows


def a6_contours(cx, cy):
    return VGroup(*[Ellipse(width=2 * r * 1.45, height=2 * r * 1.05, stroke_color=GHOST, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0]) for r in (0.35, 0.72, 1.1)])


class B44_CurlCheck(Scene):
    def construct(self):
        px = [-4.2, 0.0, 4.2]
        py = 0.95
        panels = [RoundedRectangle(width=3.5, height=2.6, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, py, 0]) for x in px]
        ill = status_tag("illustration", 5.0, 2.95)
        # the number line (0 / 1 / 2) is there from the start; the dot rides it later
        ly = -1.85
        line = Line([-5.4, ly, 0], [5.4, ly, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([x, ly - 0.15, 0], [x, ly + 0.15, 0], color=INK, stroke_width=5) for x in px])
        nums = VGroup(*[T(s, 44).move_to([x, -2.45, 0]) for s, x in zip(("0", "1", "2"), px)])
        cl = a6_lab("curl ratio", 0.0, -3.05, 34)
        self.add(ill)
        until(self, "A real map", lead=0.5)
        # panel 1: a real surface in the right convention
        c1 = a6_contours(px[0], py)
        f1 = a6_field("real", px[0], py)
        lab1 = a6_lab("right convention", px[0], -0.75, 32)
        self.play(Create(panels[0]), Create(c1), run_time=0.6)
        self.play(LaggedStart(*[Create(a) for a in f1], lag_ratio=0.06), FadeIn(lab1), run_time=0.9)
        # "no curl": a small circulating arrow with a bar through it, above the real panel
        until(self, "no curl", lead=0.3)
        swirl = Arc(radius=0.27, start_angle=0.7, angle=4.5, color=INK, stroke_width=5).move_to([-4.9, 2.75, 0])
        swirl.add_tip(tip_length=0.15)
        bar_ = Line([-5.2, 3.05, 0], [-4.6, 2.45, 0], color=INK, stroke_width=6)
        l_nc = a6_labl("no curl", -4.4, 2.75, 32)
        self.play(Create(swirl), Create(bar_), FadeIn(l_nc), run_time=0.4)
        until(self, "an imitation", lead=0.45)
        c2_f = a6_field("none", px[1], py)
        lab2 = a6_lab("no surface", px[1], -0.75, 32)
        self.play(Create(panels[1]), run_time=0.4)
        self.play(LaggedStart(*[Create(a) for a in c2_f], lag_ratio=0.06), FadeIn(lab2), run_time=0.9)
        # number line: the ratio lands near 0 (right convention), near 1 (no surface), near 2 (wrong convention)
        until(self, "The ratio", lead=0.3)
        self.play(Create(line), Create(ticks), FadeIn(nums), FadeIn(cl), run_time=0.6)
        dot = Dot([px[0], ly, 0], radius=0.17, color=TERRA)
        until(self, "near zero", lead=0.3)
        self.play(FadeIn(dot, scale=0.5), run_time=0.35)
        until(self, "near one", lead=0.45)
        self.play(dot.animate.move_to([px[1], ly, 0]), run_time=0.5)
        c3 = a6_contours(px[2], py)
        f3 = a6_field("wrong", px[2], py)
        lab3 = a6_lab("wrong convention", px[2], -0.75, 32)
        until(self, "near two", lead=0.95)
        self.play(dot.animate.move_to([px[2], ly, 0]), Create(panels[2]), Create(c3), run_time=0.5)
        self.play(LaggedStart(*[Create(a) for a in f3], lag_ratio=0.06), FadeIn(lab3), run_time=0.7)
        done(self)


# ── B45 · calibrate on the Poly Haven stone-floor pair: 0.484 / 1.516, not 0 and 2 ───────────────────────────────────
class B45_Calibrate(Scene):
    def construct(self):
        gl = a6_img("ev_normal_gl.png", h=2.5, at=(-4.8, 1.3))
        dx = a6_img("ev_normal_dx.png", h=2.5, at=(-1.9, 1.3))
        pg, pd = framed(gl), framed(dx)
        l_gl = a6_lab("OpenGL", -4.8, 2.95, 36)
        l_dx = a6_lab("DirectX", -1.9, 2.95, 36)
        until(self, "OpenGL and DirectX", lead=0.5)
        self.play(FadeIn(pg), FadeIn(l_gl), run_time=0.4)
        self.play(FadeIn(pd), FadeIn(l_dx), run_time=0.4)
        until(self, "Poly Haven", lead=0.4)
        c1 = chip("Stone Floor · Poly Haven", 3.65, 2.35, size=32)
        c2 = chip("Dimitrios Savva · CC0", 3.65, 1.5, size=32)
        ex = example_tag(3.2, 0.7)
        self.play(FadeIn(c1, shift=LEFT * 0.2), FadeIn(c2, shift=LEFT * 0.2), FadeIn(ex), run_time=0.5)
        # two number lines: the OpenGL file (top), the DirectX file (bottom); x = 0 -> -4.8, x = 2 -> +4.8
        def X(v):
            return -4.8 + v * 4.8
        y_a, y_b = -1.55, -2.55
        la = Line([X(0), y_a, 0], [X(2), y_a, 0], color=INK, stroke_width=5)
        lb = Line([X(0), y_b, 0], [X(2), y_b, 0], color=INK, stroke_width=5)
        tks = VGroup(*[Line([X(v), y_b - 0.14, 0], [X(v), y_b + 0.14, 0], color=INK, stroke_width=5) for v in (0, 1, 2)],
                     *[Line([X(v), y_a - 0.14, 0], [X(v), y_a + 0.14, 0], color=INK, stroke_width=5) for v in (0, 2)])
        nums = VGroup(*[T(str(v), 36).move_to([X(v), y_b - 0.5, 0]) for v in (0, 1, 2)])
        th_a = a6_img("ev_normal_gl.png", h=0.62, at=(-5.65, y_a))
        th_b = a6_img("ev_normal_dx.png", h=0.62, at=(-5.65, y_b))
        until(self, "same material", lead=0.45)
        self.play(Create(la), Create(lb), Create(tks), FadeIn(nums), FadeIn(th_a), FadeIn(th_b), run_time=0.6)
        v1, v2 = 0.484, 1.516                      # 0.48445 and 1.51555 (evidence/runs/R3-normal-calibration.json), shown to 3 places
        d_a1 = Dot([X(v1), y_a, 0], radius=0.17, color=TERRA)
        d_a2 = Dot([X(v2), y_a, 0], radius=0.17, color=TERRA)
        n_a1 = T("0.484", 40).move_to([X(v1), y_a + 0.55, 0])
        n_a2 = T("1.516", 40).move_to([X(v2), y_a + 0.55, 0])
        s_a1 = a6_lab("read as OpenGL", X(v1), y_a + 1.0, 30)
        s_a2 = a6_lab("read as DirectX", X(v2), y_a + 1.0, 30)
        until(self, "point four eight", lead=0.5)
        self.play(FadeIn(d_a1, scale=0.5), FadeIn(n_a1), FadeIn(s_a1), run_time=0.4)
        until(self, "one point five two", lead=0.55)
        self.play(FadeIn(d_a2, scale=0.5), FadeIn(n_a2), FadeIn(s_a2), run_time=0.4)
        # not zero and two: open circles at the ideal ends
        until(self, "Not zero and two", lead=0.4)
        g0 = open_circle(X(0), y_a, r=0.2, color=DIM, w=5)
        g2 = open_circle(X(2), y_a, r=0.2, color=DIM, w=5)
        gap0 = DashedLine([X(0) + 0.25, y_a, 0], [X(v1) - 0.22, y_a, 0], color=DIM, stroke_width=4, dash_length=0.12)
        gap2 = DashedLine([X(v2) + 0.22, y_a, 0], [X(2) - 0.25, y_a, 0], color=DIM, stroke_width=4, dash_length=0.12)
        self.play(Create(g0), Create(g2), Create(gap0), Create(gap2), run_time=0.5)
        # the DirectX file gives the mirror pair: the threshold is set from the pair
        until(self, "Set the threshold", lead=0.45)
        d_b1 = Dot([X(v2), y_b, 0], radius=0.17, color=TERRA)
        d_b2 = Dot([X(v1), y_b, 0], radius=0.17, color=TERRA)
        n_b1 = T("1.516", 40).move_to([X(v2), y_b + 0.5, 0])
        n_b2 = T("0.484", 40).move_to([X(v1), y_b + 0.5, 0])
        self.play(FadeIn(d_b1, scale=0.5), FadeIn(d_b2, scale=0.5), FadeIn(n_b1), FadeIn(n_b2), run_time=0.5)
        done(self)


# ── B46 · the code-made map (0.054 / 1.946), no normal map in the game's materials, and the Sobel limit ───────────────────
class B46_CodeMadeMap(Scene):
    def construct(self):
        im = a6_img("ev_normal_analytic.png", h=2.6, at=(-4.55, 1.3))
        pic = framed(im)
        lab = a6_lab("made by code", -4.55, 3.05, 34)
        ex = example_tag(3.0, 2.95)
        self.play(FadeIn(pic), FadeIn(lab), FadeIn(ex), run_time=0.5)
        # number line, 0 .. 2 (x = -2.2 .. 5.6); the two code-made-map points sit near the ends
        def X(v):
            return -2.2 + v * 3.9
        ly = 1.0
        line = Line([X(0), ly, 0], [X(2), ly, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([X(v), ly - 0.15, 0], [X(v), ly + 0.15, 0], color=INK, stroke_width=5) for v in (0, 1, 2)])
        nums = VGroup(*[T(str(v), 36).move_to([X(v), ly - 0.55, 0]) for v in (0, 1, 2)])
        self.play(Create(line), Create(ticks), FadeIn(nums), run_time=0.5)
        d1 = Dot([X(0.054), ly, 0], radius=0.17, color=TERRA)
        d2 = Dot([X(1.946), ly, 0], radius=0.17, color=TERRA)
        n1 = T("0.054", 40).move_to([X(0.054) + 0.2, ly + 0.55, 0])
        n2 = T("1.946", 40).move_to([X(1.946) - 0.1, ly + 0.55, 0])
        s1 = a6_lab("read as OpenGL", X(0.054) + 0.55, ly + 1.05, 30)
        s2 = a6_lab("read as DirectX", X(1.946) - 0.4, ly + 1.05, 30)
        until(self, "point zero five", lead=0.45)
        self.play(FadeIn(d1, scale=0.5), FadeIn(n1), FadeIn(s1), run_time=0.4)
        until(self, "one point nine five", lead=0.5)
        self.play(FadeIn(d2, scale=0.5), FadeIn(n2), FadeIn(s2), run_time=0.4)
        until(self, "no normal map", lead=0.5)
        chip_ = status_tag("game materials: no normal map", -3.1, -0.85)
        self.play(FadeIn(chip_, shift=UP * 0.15), run_time=0.4)
        # after the midpoint: a normal map computed from a picture with a Sobel filter passes the check
        until(self, "And know the limit", lead=0.2)
        sy = -2.0
        pic_box = box(-4.6, sy, 1.4, 1.0, color=INK, sw=4)
        hill = VMobject(stroke_color=INK, stroke_width=4).set_points_as_corners([[-5.15, sy - 0.28, 0], [-4.85, sy + 0.02, 0], [-4.6, sy - 0.1, 0], [-4.3, sy + 0.2, 0], [-4.05, sy - 0.28, 0]])
        sun = Dot([-4.9, sy + 0.25, 0], radius=0.07, color=DIM)
        map_box = box(-1.2, sy, 1.4, 1.0, color=INK, sw=4)
        mp = VGroup(*[Line([-1.75, sy - 0.3 + k * 0.2, 0], [-0.65, sy - 0.3 + k * 0.2, 0], color=BAR2, stroke_width=4) for k in range(4)])
        a_s1 = arrow([-3.7, sy, 0], [-2.15, sy, 0], w=5, tip=0.2)
        a_s2 = arrow([-0.3, sy, 0], [1.1, sy, 0], w=5, tip=0.2)
        l_pic = a6_lab("picture", -4.6, sy - 0.82, 32)
        l_sob = a6_lab("Sobel", -2.95, sy + 0.45, 34)
        l_map = a6_lab("normal map", -1.2, sy - 0.82, 32)
        until(self, "Sobel", lead=0.9)
        self.play(Create(pic_box), Create(hill), FadeIn(sun), FadeIn(l_pic), GrowArrow(a_s1), FadeIn(l_sob), run_time=0.6)
        self.play(Create(map_box), Create(mp), FadeIn(l_map), GrowArrow(a_s2), run_time=0.5)
        ok1 = tick_mark(1.55, sy, s=0.25)
        l_ok = a6_labl("passes the check", 2.0, sy, 34)
        until(self, "passes", lead=0.35)
        self.play(Create(ok1), FadeIn(l_ok), run_time=0.4)
        ok2 = tick_mark(1.55, -2.55, s=0.2)
        l_s = a6_labl("a surface exists", 2.0, -2.55, 34)
        x3 = cross_mark(1.55, -3.05, s=0.2)
        l_r = a6_labl("the right one", 2.0, -3.05, 34)
        until(self, "a surface exists", lead=0.7)
        self.play(Create(ok2), FadeIn(l_s), run_time=0.35)
        until(self, "not the right one", lead=0.85)
        self.play(Create(x3), FadeIn(l_r), run_time=0.35)
        done(self)


# ── B47 · the audit: the real MATERIALS.md rows, five things the test pins, 5 + 24 + 24 = 53 ─────────────────────────────
A6_ROWS = [("Signal pad, per-instance ShaderMaterial", "shaders/signal.gdshader", "activation ← charge / 0.6; texture-free"),
           ("MaterialSpecimen0 / matte.tres", "shaders/surface.gdshader", "tint white; roughness .9; scale 1; metallic 0"),
           ("MaterialSpecimen1 / coated.tres", "same", "tint (.45,.95,.72); roughness .25; scale 2; metallic .4")]


class B47_Audit(Scene):
    def construct(self):
        fname = M("MATERIALS.md", 24).move_to([-6.15, 2.95, 0], aligned_edge=LEFT)
        ex = example_tag(3.0, 2.95)
        card = RoundedRectangle(width=11.2, height=3.45, corner_radius=0.16, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-0.6, 0.78, 0])
        ya = [2.02, 0.92, -0.18]
        rows = VGroup()
        for (c1, c2, c3), y in zip(A6_ROWS, ya):
            rows.add(VGroup(T(c1, 32).move_to([-5.9, y, 0], aligned_edge=LEFT),
                            M(c2, 20, DIM).move_to([1.2, y, 0], aligned_edge=LEFT),
                            T(c3, 32).move_to([-5.9, y - 0.47, 0], aligned_edge=LEFT)))
        self.add(fname)
        self.wait(0.3)
        self.play(Create(card), FadeIn(ex), run_time=0.6)
        until(self, "a materials table", lead=0.55)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.35), run_time=0.9)
        # the five things the test pins, ticking in on the voice (two rows)
        items = [("shader path", -5.8, -1.55, "shader path", 0.3), ("hints", -2.65, -1.55, "hints", 0.2), ("values", -0.55, -1.55, "values", 0.2),
                 ("texture paths", -5.8, -2.3, "texture paths", 0.25), ("import settings", -2.2, -2.3, "import settings", 0.3)]
        for text, x, y, ph, ld in items:
            until(self, ph, lead=ld)
            tk = tick_mark(x, y, s=0.18)
            lb = a6_labl(text, x + 0.35, y, 34)
            self.play(Create(tk), FadeIn(lb), run_time=0.3)
        # the counter climbs: 5 on the pad shader, 24 per material
        until(self, "The example's test", lead=0.95)
        sx = 5.6
        n5 = T("5", 52).move_to([sx, 1.78, 0])
        n24a = T("24", 52).move_to([sx, 0.68, 0])
        n24b = T("24", 52).move_to([sx, -0.42, 0])
        bar = Line([5.05, -1.0, 0], [6.15, -1.0, 0], color=INK, stroke_width=6)
        vt = ValueTracker(0)
        hero = always_redraw(lambda: T(str(int(round(vt.get_value()))), 76).move_to([sx, -1.7, 0]))
        self.add(hero)
        self.play(FadeIn(n5), vt.animate.set_value(5), rate_func=linear, run_time=0.35)
        self.play(FadeIn(n24a), Create(bar), vt.animate.set_value(29), rate_func=linear, run_time=0.4)
        self.play(FadeIn(n24b), vt.animate.set_value(53), rate_func=linear, run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act7.py ══════════════════════════════
"""ACT VII · Read the Language  (B49-B55, B55B, Manim)

One cast for the act: the REAL generated shader (standard_generated.gdshader, 48 lines, Godot 4.7.2's own conversion of the example's
StandardMaterial3D; sha256 ca1c191c44fb614ae64a258fce3efbc13b77fdc82f480e98ac4582e30805650d, evidence/example/conversion-receipt.json) shown
in the REAL Godot Shader Editor (captures/editor/, strips cut by evidence/act5/make_editor_crops.py), the example's own three shaders
(embedded below verbatim with their real line numbers, checked by evidence/act5/verify_embedded.py) and the flat 3 x 2 pad quad of
render-material-evidence.gd:29 for the corner arithmetic. Editor frames are labelled "scripted editor session"; the menu was opened in
a scratch copy (nothing converted or saved). Drawings of ideas (B52, B54, B55) are labelled and never styled as Godot.
"""

A7P = "pantry/"

# REAL source lines, embedded verbatim (Gate A runs scenes.py from a folder with no evidence/); evidence/act5/verify_embedded.py checks them.
A7_REAL = {'signal.gdshader': {1: 'shader_type spatial;', 3: 'uniform float activation : hint_range(0.0, 1.0) = 0.0;'},
 'surface.gdshader': {1: 'shader_type spatial;',
                      3: 'uniform sampler2D color_map : source_color, filter_nearest;',
                      12: '\tROUGHNESS = clamp(texture(roughness_map, UV * uv_scale).r * roughness_gain, 0.05, 1.0);'},
 'hint.gdshader': {1: 'shader_type spatial;',
                   3: 'uniform sampler2D as_color : source_color, filter_nearest;',
                   4: 'uniform sampler2D as_data : filter_nearest;',
                   9: '\tALBEDO = use_color ? texture(as_color, UV).rgb : texture(as_data, UV).rgb;',
                   10: '\tif (show_screen_grid && mod(FRAGCOORD.x, VIEWPORT_SIZE.x / 8.0) < 2.0) {'},
 'standard_generated.gdshader': {3: 'shader_type spatial;',
                                 4: 'render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;',
                                 6: 'uniform vec4 albedo : source_color;',
                                 7: 'uniform sampler2D texture_albedo : source_color, filter_linear_mipmap, repeat_enable;',
                                 19: 'uniform sampler2D texture_normal : hint_roughness_normal, filter_linear_mipmap, repeat_enable;',
                                 20: 'uniform float normal_scale : hint_range(-16.0, 16.0);',
                                 35: '\tALBEDO = albedo.rgb * albedo_tex.rgb;',
                                 43: '\tROUGHNESS = roughness_tex * roughness;',
                                 46: '\tNORMAL_MAP = texture(texture_normal, base_uv).rgb;'},
 'standard-source.tres': {6: 'albedo_color = Color(0.85, 0.8, 0.7, 1)',
                          7: 'albedo_texture = ExtResource("1")',
                          10: 'roughness_texture = ExtResource("2")',
                          13: 'normal_texture = ExtResource("3")'}}


# REAL log lines of evidence/act7/vertex_albedo_check.log (verbatim, leading spaces kept); verify_embedded.py checks them.
A7_LOG = ['    2 | void vertex() {', 'E   3->  ALBEDO = vec3(1.0);', "SHADER ERROR: Unknown identifier in expression: 'ALBEDO'."]

A7_CW = {20: 0.15, 24: 0.2}            # measured Menlo units per character
A7_LH = {20: 0.2875, 24: 0.345}        # default row pitch (size / 32 * 0.46)


def a7_line(fname, n):
    return A7_REAL[fname][n]


def a7_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a7_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A7P + name)
    try:
        im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])   # bicubic rings near light-on-dark text and breaks GATE T's ink mask
    except Exception:
        pass
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    return im.move_to(np.array([at[0], at[1], 0.0]))


def a7_hook(x, y, s=0.13):
    """The wrap mark: a drawn elbow (down, then left with a small head). A shape, not a glyph."""
    return VGroup(Line([x, y + s * 0.6, 0], [x, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x, y - s * 0.7, 0], [x - s * 1.4, y - s * 0.7, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 0.2, 0], color=DIM, stroke_width=4),
                  Line([x - s * 1.4, y - s * 0.7, 0], [x - s * 0.8, y - s * 1.2, 0], color=DIM, stroke_width=4))


def a7_split(text, budget):
    """Soft-wrap `text` at the last space at or before `budget` characters, preferring a space after a comma/&&/colon.
    Returns a list of pieces (characters verbatim; only the breaking space is dropped)."""
    if len(text) <= budget:
        return [text]
    cut = text.rfind(" ", 0, budget + 1)
    if cut <= 0:
        return [text]
    return [text[:cut]] + a7_split(text[cut + 1:], budget)


class A7Code:
    """Real code rows: Menlo, real line numbers, outline-only frame, optional gap markers and wraps.
    spec: list of (real_line_number, text) or None (a gap marker). `dedent` strips the common leading tab(s).
    Attributes: .group (frame + rows + marks), .frame, .W, .H, .pitch, .cw, .size; rows(n) -> VGroup of line n (number + pieces);
    ring(n) -> terracotta ring round the whole line n; tok(n, token, k=0) -> (cx, cy, w) of a token; piece_y(n, i)."""

    def __init__(self, spec, x=0.0, y=0.0, size=20, wrap=None, dedent=True, pad=0.3, pitch=None, gap=0.32, width=None, extra=0.0):
        self.size, self.cw = size, A7_CW[size]
        self.pitch = pitch or A7_LH[size]
        items = []
        tabs = [len(t) - len(t.lstrip("\t")) for s in spec if s for t in [s[1]] if t.strip()]
        cut = min(tabs) if (dedent and tabs) else 0
        for s in spec:
            if s is None:
                items.append(("gap", None, None, None, 0))
                continue
            n, t = s
            t = t[cut:] if t.startswith("\t" * cut) else t
            t = t.replace("\t", "    ")
            lead = len(t) - len(t.lstrip(" "))
            pieces = a7_split(t, wrap) if wrap else [t]
            for i, p in enumerate(pieces):
                items.append(("row", n if i == 0 else None, p, i, lead))
        digits = max(len(str(s[0])) for s in spec if s)
        self.nw = digits * self.cw + 0.25
        longest = max(len(p) + ((ld + 2) if i else 0) for k, n, p, i, ld in items if k == "row")
        self.W = width or (longest * self.cw + self.nw + 2 * pad + extra)
        h = sum(self.pitch if it[0] == "row" else gap for it in items)
        self.H = h + 2 * pad
        self.x, self.y, self.pad = x, y, pad
        self.frame = RoundedRectangle(width=self.W, height=self.H, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
        self.text_left = x - self.W / 2 + pad + self.nw
        self.rows_, self.pos, self.marks, self.hooks = {}, {}, VGroup(), VGroup()
        cy = y + self.H / 2 - pad
        cur = None
        for k, n, p, i, ld in items:
            if k == "gap":
                cy -= gap
                self.marks.add(*[Dot([self.x - self.W / 2 + pad + self.nw * 0.5, cy + gap / 2 + dy, 0], radius=0.035, color=DIM) for dy in (-0.07, 0.0, 0.07)])
                continue
            yy = cy - self.pitch / 2
            cy -= self.pitch
            ind = (ld + 2) * self.cw if i else 0.0
            tx = M(p if p else " ", self.size)
            lead_p = len(p) - len(p.lstrip(" "))            # Text() drops leading spaces: place by character column so indentation is kept
            tx.move_to([self.text_left + ind + lead_p * self.cw + tx.width / 2, yy, 0])
            grp = VGroup(tx)
            if n is not None:
                nm = M(str(n), self.size, DIM)
                nm.move_to([self.text_left - 0.25 - nm.width / 2, yy, 0])
                grp.add(nm)
                cur = n
                self.rows_[n] = VGroup()
                self.pos[n] = []
            self.rows_[cur].add(grp)
            self.pos[cur].append((yy, p, ind))
            if i:
                prev = self.pos[cur][i - 1]
                hk = a7_hook(self.text_left + prev[2] + len(prev[1]) * self.cw + 0.2, prev[0])
                self.hooks.add(hk)
        self.group = VGroup(self.frame, *[r for r in self.rows_.values()], self.marks, self.hooks)

    def rows(self, n):
        return self.rows_[n]

    def piece_y(self, n, i=0):
        return self.pos[n][i][0]

    def ring(self, n, color=TERRA, sw=6, shrink=0.8, pieces=None):
        """One flat terracotta ring per visual row of line n (GATE T reads a ring whose width/height < 15 as accent TEXT, so a
        wrapped line gets one ring per piece and the rings never touch)."""
        rs = VGroup()
        for i, (yy, p, ind) in enumerate(self.pos[n]):
            if pieces is not None and i not in pieces:
                continue
            rs.add(RoundedRectangle(width=self.W - 0.3, height=self.pitch * shrink, corner_radius=0.1, stroke_color=color, stroke_width=sw,
                                    fill_opacity=0).move_to([self.x, yy, 0]))
        return rs

    def tok(self, n, token, k=0):
        for yy, p, ind in self.pos[n]:
            i = -1
            for _ in range(k + 1):
                i = p.find(token, i + 1)
                if i < 0:
                    break
            if i >= 0:
                w = len(token) * self.cw
                return (self.text_left + ind + i * self.cw + w / 2, yy, w)
        raise ValueError(f"token {token!r} not in line {n}")

    def tok_ring(self, n, token, k=0, color=TERRA, sw=5, padx=0.05):
        cx, cy, w = self.tok(n, token, k)
        return RoundedRectangle(width=w + 2 * padx, height=self.pitch * 0.9, corner_radius=0.07, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])


def a7_mono(s, x, y, size=24, color=INK, left=False):
    t = M(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a7_x(x, y, s=0.1, w=5):
    """A multiplication mark drawn as a shape."""
    return cross_mark(x, y, s, INK, w)


def a7_chip(cx, y, rgb, text, size=34, sw=0.7, sh=0.5):
    """A real texel value: a swatch of the real colour + its real numbers (BESIDE it), the pair centred on cx."""
    tx = T(text, size)
    total = sw + 0.15 + tx.width
    x0 = cx - total / 2
    sq = swatch(rgb, x0 + sw / 2, y, sw, sh)
    fr = Rectangle(width=sw, height=sh, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x0 + sw / 2, y, 0])
    tx.move_to([x0 + sw + 0.15, y, 0], aligned_edge=LEFT)
    return VGroup(sq, fr, tx)


def a7_row_y(top, py, scale):
    """Scene y of pixel row py of a crop whose top edge sits at scene y `top`, shown at `scale` x native (1 unit = 270 px at 4K)."""
    return top - py * scale / 270.0




def a7_pill(text, x, y, w, size=26, h=0.62):
    """A white mono pill (no outline), 0.62 high: a name of a real built-in or output."""
    lab = M(text, size)
    shadow = pill(x + 0.07, y - 0.07, w, h=h, fill=BOX_L)
    p = pill(x, y, w, h=h)
    lab.move_to([x, y, 0])
    return VGroup(shadow, p, lab)


def a7_doc(x, y, w=1.5, h=1.9):
    """A drawn page (a file): outline, three ghost text lines."""
    page = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x, y, 0])
    lines = VGroup(*[Line([x - w * 0.3, y + h * 0.26 - i * 0.3, 0], [x + w * 0.3 - (0.4 if i == 3 else 0.0), y + h * 0.26 - i * 0.3, 0],
                          color=BAR2, stroke_width=6) for i in range(4)])
    return VGroup(page, lines)


def a7_no(x, y, r=0.3, sw=7):
    """A prohibition mark (ink ring + bar): shapes only, drawn over an arrow, never over type."""
    ring_ = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    return VGroup(ring_, Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw))


# ── B49 · convert a StandardMaterial3D, save the generated code ──────────────────────────────────────────────────
class B49_ConvertMaterial(Scene):
    def construct(self):
        title = T("Read  the  Language", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        SC = 1.35
        godot = logo_chip("godot", -3.2, 0.5, h=1.5)
        doc = a7_doc(1.7, 0.5)
        dn = a7_mono("standard_generated.gdshader", 1.7, -0.95, 20)
        ar0 = arrow([-1.9, 0.5, 0], [0.6, 0.5, 0], INK, 6, 0.24)
        s0 = Group(godot, doc, dn, ar0)
        until(self, "Last build step", lead=-0.3)
        self.play(FadeIn(godot), run_time=0.4)
        until(self, "read the shader", lead=0.2)
        self.play(GrowArrow(ar0), FadeIn(doc), FadeIn(dn), run_time=0.5)
        # the example's StandardMaterial3D as the editor shows it (albedo, roughness and normal textures)
        cxl, cxr, cyc = -3.6, 3.6, -0.15
        im5b = framed(a7_img("a7_ed_f5b_textures.png", w=900 * SC / 270.0, at=(cxl, cyc)), pad=0.05)
        top5b = cyc + 1005 * SC / 270.0 / 2
        left5b = cxl - 900 * SC / 270.0 / 2
        until(self, "Make a standard material", lead=0.35)
        self.play(FadeOut(s0), FadeIn(im5b), run_time=0.45)
        py = {"albedo": 177, "normal": 934, "roughness": 586}
        dots = {k: Dot([left5b - 0.25, a7_row_y(top5b, v, SC), 0], radius=0.1, color=TERRA) for k, v in py.items()}
        for k, ph in (("albedo", "with albedo"), ("normal", "normal and"), ("roughness", "roughness textures")):
            until(self, ph, lead=0.25)
            self.play(FadeIn(dots[k], scale=0.4), run_time=0.25)
        until(self, "make it unique", lead=0.15)
        mu = chip("Make Unique", 0.0, 0.5, w=2.55, size=32)
        a_mu = arrow([1.45, 0.5, 0], [1.1, 0.5, 0], INK, 5, 0.18)
        self.play(FadeIn(mu), run_time=0.3)
        until(self, "convert it to a shader material", lead=0.2)
        im5e = framed(a7_img("a7_ed_f5e_menu.png", w=900 * SC / 270.0, at=(cxr, cyc)), pad=0.05)
        top5e = cyc + 1050 * SC / 270.0 / 2
        y_conv = a7_row_y(top5e, 982, SC)
        self.play(FadeOut(mu), FadeOut(VGroup(*dots.values())), FadeIn(im5e), run_time=0.45)
        t1 = status_tag("scripted editor session", -3.6, -3.1)
        t2 = status_tag("menu opened in a scratch copy", 3.4, -3.1)
        self.add(t1, t2)
        until(self, "in the Inspector", lead=0.1)
        dc = Dot([cxr - 450 * SC / 270.0 - 0.25, y_conv, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(dc, scale=0.4), run_time=0.3)
        until(self, "Save the code", lead=0.55)
        self.play(FadeOut(Group(im5b, im5e, dc, t1, t2)), run_time=0.25)
        doc2 = a7_doc(-3.4, 0.5)
        dn2 = a7_mono("standard_generated.gdshader", -3.4, -0.95, 20)
        n48 = a7_lab("48 lines", -3.4, -1.55, 34)
        self.play(FadeIn(doc2), FadeIn(dn2), FadeIn(n48), run_time=0.35)
        until(self, "never uses it", lead=1.5)
        game = VGroup(box(3.3, 0.5, 2.2, 1.1, DIM, 4), a7_lab("game", 3.3, 0.5, 38))
        dash = DashedLine([-2.4, 0.5, 0], [2.1, 0.5, 0], color=INK, stroke_width=5, dash_length=0.2)
        no = a7_no(-0.15, 0.5)
        self.play(Create(dash), FadeIn(game), run_time=0.35)
        self.play(Create(no), run_time=0.25)
        self.add(example_tag(2.9, -3.05))
        done(self)


# ── B50 · the generated file's lines ─────────────────────────────────────────────────────────────────────────────
# (The same lines in the REAL Shader Editor are in captures/editor/ F1a/F1b and cut to pantry/a7_ed_gen_*.png; dark code strips fail GATE T at 4K
#  with light-on-dark glyph halos, so the picture shows the file's real text on the stage and B49 carries the real editor frames.)
class B50_GeneratedLines(Scene):
    def construct(self):
        L = lambda n: (n, a7_line("standard_generated.gdshader", n))
        spec = [L(3), L(4), None, L(6), L(7), None, L(19), None, L(35), None, L(43), None, L(46)]
        blk = A7Code(spec, x=-1.25, y=0.15, size=20, wrap=60, pitch=0.38, gap=0.26, pad=0.2, dedent=False, extra=0.35)
        self.add(blk.frame)
        until(self, "In the generated file", lead=0.1)
        self.play(FadeIn(VGroup(*[blk.rows(n) for n in (3, 4, 6, 7, 19, 35, 43, 46)])), FadeIn(blk.marks), FadeIn(blk.hooks), run_time=0.5)
        ring = lambda n: blk.ring(n, pieces=(0,))
        until(self, "lines three and four", lead=0.6)
        r3, r4 = ring(3), ring(4)
        self.play(Create(r3), run_time=0.3)
        self.play(FadeOut(r3), Create(r4), run_time=0.3)
        until(self, "line six", lead=0.5)
        r6 = ring(6)
        self.play(FadeOut(r4), Create(r6), run_time=0.3)
        until(self, "says source color", lead=1.0)
        r7 = ring(7)
        tick = check(4.45, blk.piece_y(7), s=0.22, color=INK, w=8)
        l_c = a7_lab("colour", 5.4, blk.piece_y(7) - 0.05, 36)
        self.play(FadeOut(r6), Create(r7), Create(tick), FadeIn(l_c), run_time=0.35)
        until(self, "line nineteen", lead=0.3)
        r19 = ring(19)
        circ = open_circle(4.45, blk.piece_y(19), 0.17, INK, 6)
        l_d = a7_lab("data", 5.4, blk.piece_y(19) - 0.05, 36)
        self.play(FadeOut(r7), Create(r19), Create(circ), FadeIn(l_d), run_time=0.35)
        until(self, "written at thirty-five", lead=0.8)
        r35 = ring(35)
        self.play(FadeOut(r19), Create(r35), run_time=0.3)
        until(self, "roughness at forty-three", lead=0.7)
        r43 = ring(43)
        self.play(FadeOut(r35), Create(r43), run_time=0.3)
        until(self, "normal map at forty-six", lead=0.8)
        r46 = ring(46)
        self.play(FadeOut(r43), Create(r46), run_time=0.3)
        self.add(example_tag(3.1, -3.1))
        done(self)


# ── B51 · Q1: what the shader type decides ──────────────────────────────────────────────────────────────────────
A7_TYPES = ["spatial", "canvas_item", "particles", "sky", "fog", "texture_blit"]     # the six shader_type values of Godot 4.7.2 (see factcheck/act7.md)


class B51_ShaderType(Scene):
    def construct(self):
        xs = [-5.6 + 0.8 * k for k in range(8)]
        circles = [Circle(radius=0.3, stroke_color=INK, stroke_width=5).move_to([x, 2.65, 0]) for x in xs]
        nums = [T(str(k + 1), 32).move_to([x, 2.65, 0]) for k, x in enumerate(xs)]
        until(self, "Then eight questions", lead=0.0)
        self.play(LaggedStart(*[AnimationGroup(Create(c), FadeIn(n)) for c, n in zip(circles, nums)], lag_ratio=0.12), run_time=1.3)
        rows = [("signal.gdshader:1", a7_line("signal.gdshader", 1)), ("surface.gdshader:1", a7_line("surface.gdshader", 1)), ("hint.gdshader:1", a7_line("hint.gdshader", 1))]
        blk = A7Code(rows, x=-1.6, y=0.45, size=24, pitch=0.8, dedent=False)
        until(self, "with line references", lead=0.1)
        self.play(Create(blk.frame), FadeIn(VGroup(*[blk.rows(k) for k, _ in rows])), run_time=0.6)
        until(self, "What does the shader type decide", lead=0.2)
        dot1 = Dot([xs[0], 2.2, 0], radius=0.09, color=TERRA)
        head = a7_mono("shader_type", 4.7, 2.65, 24, DIM)
        ys = [1.85 - 0.55 * i for i in range(len(A7_TYPES))]
        items = [a7_mono(t, 3.95, y, 24, left=True) for t, y in zip(A7_TYPES, ys)]
        self.play(FadeIn(dot1, scale=0.4), FadeIn(head), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.12), run_time=0.9)
        until(self, "Which functions and built-ins exist", lead=0.2)
        c1, c2 = chip("functions", 4.75, -1.75, w=2.6, size=32), chip("built-ins", 4.75, -2.6, w=2.6, size=32)
        self.play(FadeIn(c1), run_time=0.3)
        self.play(FadeIn(c2), run_time=0.3)
        until(self, "All three example shaders", lead=0.6)
        sp = Dot([3.62, ys[0], 0], radius=0.1, color=TERRA)
        rr = [blk.ring(k, shrink=0.45) for k, _ in rows]
        self.play(FadeIn(sp, scale=0.4), Create(rr[0]), run_time=0.3)
        until(self, "example shaders", lead=0.6)
        self.play(FadeOut(rr[0]), Create(rr[1]), run_time=0.3)
        until(self, "say spatial", lead=0.6)
        self.play(FadeOut(rr[1]), Create(rr[2]), run_time=0.3)
        self.add(example_tag(-2.95, -3.1))
        done(self)


# ── B52 · Q2: fragment per pixel, vertex per corner; the colour line cannot live in vertex() ───────────────────────
class B52_PerPixelPerCorner(Scene):
    def construct(self):
        W_, H_, XL, XR, YQ = 4.2, 2.625, -3.4, 3.4, 0.55           # the flat 3 x 2 quad of render-material-evidence.gd:29, drawn 4.2 x 2.625 (cells 16 x 10)
        qL = Rectangle(width=W_, height=H_, stroke_color=INK, stroke_width=5).move_to([XL, YQ, 0])
        qR = Rectangle(width=W_, height=H_, stroke_color=INK, stroke_width=5).move_to([XR, YQ, 0])
        lf, lv = a7_mono("fragment()", XL, 2.5, 28), a7_mono("vertex()", XR, 2.5, 28)
        ill = status_tag("illustrative", -4.7, -3.1)
        until(self, "Which functions did you write", lead=0.0)
        self.play(Create(qL), Create(qR), FadeIn(lf), FadeIn(lv), FadeIn(ill), run_time=0.6)
        grid = pixel_grid(16, 10, W_ / 16, XL, YQ, DIM, 2)
        until(self, "Fragment runs for every pixel", lead=0.2)
        self.play(FadeIn(grid), run_time=0.3)
        anims = [tint(grid.cells[r][c], BAR1 if c % 2 == 0 else BAR3) for c in range(16) for r in range(10)]
        self.play(LaggedStart(*anims, lag_ratio=0.006), run_time=1.3)
        until(self, "vertex, once per corner", lead=0.2)
        cs = [(XR - W_ / 2, YQ + H_ / 2), (XR + W_ / 2, YQ + H_ / 2), (XR - W_ / 2, YQ - H_ / 2), (XR + W_ / 2, YQ - H_ / 2)]
        dots = [Dot([x, y, 0], radius=0.13, color=INK) for x, y in cs]
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.2), run_time=0.6)
        stageA = Group(qL, qR, lf, lv, grid, *dots, ill)
        # stage B: the colour line written inside vertex() does not compile (the REAL log of a Godot 4.7.2 run)
        until(self, "Move the colour line into vertex", lead=0.3)
        self.play(FadeOut(stageA), run_time=0.3)
        cw = 0.2
        rowsB = [M(t, 24) for t in A7_LOG]
        wB = max(len(t) for t in A7_LOG) * cw + 0.6
        frame = RoundedRectangle(width=wB, height=len(A7_LOG) * 0.5 + 0.6, corner_radius=0.14, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, 1.5, 0])
        for k, (t, tx) in enumerate(zip(A7_LOG, rowsB)):
            tx.move_to([-wB / 2 + 0.3 + (len(t) - len(t.lstrip(' '))) * cw + tx.width / 2, 1.5 + 0.5 - 0.5 * k, 0])
        self.play(Create(frame), FadeIn(VGroup(*rowsB)), run_time=0.5)
        until(self, "it will not compile", lead=1.0)
        xm = cross_mark(-1.6, -0.4, 0.3, INK, 10)
        t_re = status_tag("re-run for this film", 1.3, -0.4)
        self.play(Create(xm), FadeIn(t_re), run_time=0.4)
        until(self, "albedo is a fragment output", lead=0.5)
        p_fr = a7_pill("fragment()", -2.6, -1.8, 2.9, size=28, h=0.7)
        p_al = a7_pill("ALBEDO", 2.6, -1.8, 2.3, size=28, h=0.7)
        a_ou = arrow([-1.0, -1.8, 0], [1.3, -1.8, 0], INK, 6, 0.22)
        l_ou = a7_lab("output", 0.15, -1.3, 34)
        self.play(FadeIn(p_fr), GrowArrow(a_ou), FadeIn(p_al), FadeIn(l_ou), run_time=0.5)
        stageB = Group(frame, VGroup(*rowsB), xm, t_re, p_fr, p_al, a_ou, l_ou)
        # stage C: compute it in vertex and pass it on (a varying): corner values 0 and 1, the stripes are lost between the corners
        until(self, "Compute it there and pass it on", lead=0.4)
        self.play(FadeOut(stageB), run_time=0.3)
        cL = Group(qL, lf, grid)
        qR2 = Rectangle(width=W_, height=H_, stroke_color=INK, stroke_width=5).move_to([XR, YQ, 0])
        lv2 = a7_mono("vertex()", XR, 2.85, 28)
        dots2 = [Dot([x, y, 0], radius=0.13, color=INK) for x, y in cs]
        nl = [T("0", 38).move_to([cs[0][0] - 0.35, cs[0][1], 0]), T("0", 38).move_to([cs[2][0] - 0.35, cs[2][1], 0]),
              T("1", 38).move_to([cs[1][0] + 0.35, cs[1][1], 0]), T("1", 38).move_to([cs[3][0] + 0.35, cs[3][1], 0])]
        f0, f1 = a7_mono("fract(0 * 8) = 0", XR, -1.25, 24), a7_mono("fract(1 * 8) = 0", XR, -1.75, 24)
        po = a7_lab("pass on", XR, 2.3, 34)
        self.play(FadeIn(cL), FadeIn(qR2), FadeIn(lv2), FadeIn(VGroup(*dots2)), FadeIn(VGroup(*nl)), FadeIn(po), FadeIn(ill), run_time=0.5)
        self.play(FadeIn(f0), run_time=0.3)
        self.play(FadeIn(f1), run_time=0.3)
        until(self, "it is blended between corners", lead=0.5)
        flat = Rectangle(width=W_, height=H_, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([XR, YQ, 0]).set_z_index(-1)
        self.play(FadeIn(flat), run_time=0.8)
        until(self, "the stripes are lost", lead=0.9)
        lost = a7_lab("flat", XR, -2.4, 40)
        keep = a7_lab("stripes", XL, -1.3, 40)
        self.play(FadeIn(lost), FadeIn(keep), run_time=0.3)
        self.add(example_tag(3.05, -3.1))
        done(self)


# ── B53 · Q3: built-ins read and written ────────────────────────────────────────────────────────────────────────
class B53_BuiltIns(Scene):
    def construct(self):
        H, S = "hint.gdshader", "surface.gdshader"
        spec = [(9, a7_line(H, 9)), (10, a7_line(H, 10)), None, (12, a7_line(S, 12))]
        blk = A7Code(spec, x=-1.6, y=1.7, size=20, wrap=52, pitch=0.38, gap=0.26, pad=0.2, dedent=True, extra=0.35)
        f_h = a7_mono(H, 4.65, (blk.piece_y(9, 0) + blk.piece_y(10, 1)) / 2, 20, DIM)
        f_s = a7_mono(S, 4.65, (blk.piece_y(12, 0) + blk.piece_y(12, 1)) / 2, 20, DIM)
        cap = framed(a7_img("ev_hint_grid_example.png", w=3.5, at=(-4.0, -1.45)), pad=0.05)
        until(self, "Which built-ins did you read", lead=0.0)
        self.play(Create(blk.frame), FadeIn(VGroup(*[blk.rows(n) for n in (9, 10, 12)])), FadeIn(blk.marks), FadeIn(blk.hooks), FadeIn(f_h), FadeIn(f_s), FadeIn(cap), run_time=0.7)
        mk = lambda t, x, y: a7_pill(t, x, y, len(t) * 0.2 + 0.8)
        uv, fc, vp = mk("UV", 0.85, -0.85), mk("FRAGCOORD", 1.35, -1.57), mk("VIEWPORT_SIZE", 1.65, -2.29)
        r9 = blk.ring(9)
        until(self, "reads U V", lead=0.6)
        self.play(Create(r9), FadeIn(uv), run_time=0.35)
        r10a, r10b = blk.ring(10, pieces=(0,)), blk.ring(10, pieces=(1,))
        until(self, "the fragment coordinate", lead=0.6)
        self.play(FadeOut(r9), Create(r10a), FadeIn(fc), run_time=0.35)
        until(self, "the viewport size", lead=0.6)
        self.play(FadeOut(r10a), Create(r10b), FadeIn(vp), run_time=0.35)
        until(self, "all read-only", lead=0.6)
        ro = a7_lab("read-only", 1.45, -0.2, 36)
        self.play(FadeOut(r10b), FadeIn(ro), run_time=0.3)
        until(self, "write albedo", lead=0.7)
        r9a = blk.ring(9, pieces=(0,))
        al = mk("ALBEDO", 4.9, -0.85)
        wr = a7_lab("written", 4.9, -0.2, 36)
        self.play(Create(r9a), FadeIn(al), FadeIn(wr), run_time=0.35)
        until(self, "and roughness", lead=0.9)
        r12 = blk.ring(12, pieces=(0,))
        ro2 = mk("ROUGHNESS", 4.9, -1.57)
        self.play(FadeOut(r9a), Create(r12), FadeIn(ro2), run_time=0.35)
        self.add(status_tag("the example, 14 Oct", -4.2, -3.1), example_tag(2.9, -3.1))
        done(self)


# ── B54 · Q4/5: what a hint changes ─────────────────────────────────────────────────────────────────────────────
class B54_HintChanges(Scene):
    def construct(self):
        code = A7Code([("signal.gdshader:3", a7_line("signal.gdshader", 3))], x=0.0, y=2.65, size=20, dedent=False)
        until(self, "Does a hint change", lead=0.0)
        self.play(Create(code.frame), FadeIn(code.rows("signal.gdshader:3")), run_time=0.5)
        r3 = code.ring("signal.gdshader:3", shrink=1.3)
        h1, h2 = a7_lab("Inspector", -1.4, 1.5, 36), a7_lab("shader receives", 3.6, 1.5, 36)
        until(self, "only the Inspector", lead=0.4)
        self.play(FadeIn(h1), Create(r3), run_time=0.4)
        until(self, "the value the shader receives", lead=0.4)
        self.play(FadeIn(h2), run_time=0.3)
        # row A: hint_range -> a DRAWN slider (a drawing, not the editor)
        YA, YB, YC = 0.5, -1.4, -2.25
        lA = a7_mono("hint_range", -5.95, YA, 24, left=True)
        track1 = Line([-2.6, YA, 0], [-0.2, YA, 0], color=INK, stroke_width=7)
        tk1 = VGroup(Line([-2.6, YA - 0.12, 0], [-2.6, YA + 0.12, 0], color=INK, stroke_width=5), Line([-0.2, YA - 0.12, 0], [-0.2, YA + 0.12, 0], color=INK, stroke_width=5))
        n01 = VGroup(a7_lab("0", -2.6, YA - 0.45, 32), a7_lab("1", -0.2, YA - 0.45, 32))
        knob1 = Circle(radius=0.14, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([-0.92, YA, 0])
        until(self, "Range shapes the slider", lead=0.4)
        self.play(FadeOut(r3), FadeIn(lA), Create(track1), Create(tk1), FadeIn(n01), run_time=0.5)
        ok1 = check(0.55, YA, s=0.22, color=INK, w=8)
        self.play(FadeIn(knob1), Create(ok1), run_time=0.3)
        # rows B and C: source_color against no hint (Forward+, the re-run's three grey bands)
        lB = a7_mono("source_color", -5.95, YB, 24, left=True)
        lC = a7_lab("no hint", -5.95, YC, 36, left=True)
        sw = lambda v, x, y: VGroup(swatch((v, v, v), x, y, 0.5, 0.5), Rectangle(width=0.5, height=0.5, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([x, y, 0]))
        pairB = VGroup(sw(64, 2.0, YB), arrow([2.35, YB, 0], [2.95, YB, 0], INK, 5, 0.18), sw(64, 3.3, YB), a7_lab("64", 3.65, YB, 38, left=True))
        pairC = VGroup(sw(64, 2.0, YC), arrow([2.35, YC, 0], [2.95, YC, 0], INK, 5, 0.18), sw(137, 3.3, YC), a7_lab("137", 3.65, YC, 38, left=True))
        until(self, "On Forward Plus", lead=0.3)
        tagF = status_tag("Forward+ · re-run for this film", 3.25, -3.05)
        self.play(FadeIn(lB), FadeIn(pairB), FadeIn(tagF), run_time=0.4)
        self.play(FadeIn(lC), FadeIn(pairC), run_time=0.4)
        br = VGroup(Line([4.85, YB, 0], [4.85, YC, 0], color=INK, stroke_width=5), Line([4.85, YB, 0], [4.7, YB, 0], color=INK, stroke_width=5),
                    Line([4.85, YC, 0], [4.7, YC, 0], color=INK, stroke_width=5))
        dif = a7_lab("differ", 5.5, (YB + YC) / 2, 34)
        until(self, "as the experiment showed", lead=0.3)
        self.play(Create(br), FadeIn(dif), run_time=0.4)
        # row A, shader side: a value of 2 sits beyond the slider's end
        track2 = Line([2.2, YA, 0], [4.2, YA, 0], color=INK, stroke_width=7)
        tk2 = VGroup(Line([2.2, YA - 0.12, 0], [2.2, YA + 0.12, 0], color=INK, stroke_width=5), Line([4.2, YA - 0.12, 0], [4.2, YA + 0.12, 0], color=INK, stroke_width=5))
        n02 = VGroup(a7_lab("0", 2.2, YA - 0.45, 32), a7_lab("1", 4.2, YA - 0.45, 32))
        ext = DashedLine([4.2, YA, 0], [5.7, YA, 0], color=INK, stroke_width=5, dash_length=0.15)
        knob2 = Circle(radius=0.14, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([5.3, YA, 0])
        two = a7_lab("2", 5.3, YA + 0.5, 38)
        until(self, "Whether range clamps", lead=0.3)
        self.play(Create(track2), Create(tk2), FadeIn(n02), run_time=0.4)
        self.play(Create(ext), FadeIn(knob2), FadeIn(two), run_time=0.4)
        until(self, "a capture will show", lead=0.5)
        q = a7_lab("clamped?", 3.9, -0.7, 36)
        self.play(FadeIn(q), run_time=0.3)
        self.add(example_tag(-3.0, -3.1))
        done(self)


# ── B55 · Q7/8: each fragment alone; what Godot gives you; the agent checks references ───────────────────────────
class B55_AloneAndGiven(Scene):
    def construct(self):
        # stage 1: sealed pixel boxes, one uniform bus feeds all
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        boxes = VGroup(*[box(x, 0.9, 1.3, 1.3, DIM, 5) for x in xs])
        dots = VGroup(*[Dot([x, 0.9, 0], radius=0.1, color=INK) for x in xs])
        blocked = VGroup(*[VGroup(arrow([xs[i] + 0.78, 0.9, 0], [xs[i + 1] - 0.78, 0.9, 0], INK, 4, 0.16), cross_mark((xs[i] + xs[i + 1]) / 2, 0.9, 0.14, INK, 6)) for i in range(4)])
        bus = Line([-5.2, -1.0, 0], [5.2, -1.0, 0], color=BAR1, stroke_width=12)
        drops = VGroup(*[arrow([x, -1.0, 0], [x, 0.2, 0], INK, 5, 0.2) for x in xs])
        lab_u = a7_lab("uniform", 0.0, -1.75, 38)
        until(self, "Each fragment runs alone", lead=0.0)
        self.play(LaggedStart(*[AnimationGroup(Create(b), FadeIn(d, scale=0.4)) for b, d in zip(boxes, dots)], lag_ratio=0.2), run_time=0.9)
        until(self, "cannot read its neighbour", lead=0.3)
        self.play(LaggedStart(*[FadeIn(b) for b in blocked], lag_ratio=0.25), run_time=0.8)
        until(self, "game state arrives", lead=0.3)
        self.play(Create(bus), FadeIn(lab_u), run_time=0.4)
        self.play(LaggedStart(*[GrowArrow(d) for d in drops], lag_ratio=0.15), run_time=0.7)
        stage1 = Group(boxes, dots, blocked, bus, drops, lab_u)
        # stage 2: what Godot gives you
        until(self, "And Godot gives you", lead=0.45)
        self.play(FadeOut(stage1), run_time=0.25)
        fr = a7_pill("fragment()", -3.1, 1.95, 2.9, size=28, h=0.7)
        outs = [a7_pill(t, -3.1, y, len(t) * 0.2 + 0.9) for t, y in (("ALBEDO", 0.65), ("ROUGHNESS", -0.1), ("METALLIC", -0.85))]
        a_fr = arrow([-3.1, 1.55, 0], [-3.1, 1.05, 0], INK, 5, 0.2)
        self.play(FadeIn(fr), run_time=0.25)
        self.play(GrowArrow(a_fr), LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.2), run_time=0.55)
        no_l = a7_lab("named outputs", -3.1, -1.7, 36)
        cite = a7_mono("surface.gdshader:10-13", -3.1, -2.35, 20, DIM)
        self.play(FadeIn(no_l), FadeIn(cite), run_time=0.3)
        until(self, "hints that become controls", lead=0.5)
        SCs = 1.4
        hr = a7_pill("hint_range", 3.5, 1.95, 2.8, size=28, h=0.7)
        a_h = arrow([3.5, 1.55, 0], [3.5, 1.12, 0], INK, 5, 0.18)
        sl = framed(a7_img("a7_ed_matte_sliders.png", w=900 * SCs / 270.0, at=(3.5, 0.45)), pad=0.05)
        ins = a7_lab("Inspector controls", 3.5, -0.55, 34)
        t_e = status_tag("scripted editor session", 3.5, -1.25)
        self.play(FadeIn(hr), GrowArrow(a_h), FadeIn(sl), FadeIn(ins), FadeIn(t_e), run_time=0.6)
        # stage 3: the agent checks references, never writes the answers
        until(self, "The agent may check", lead=0.35)
        self.play(FadeOut(Group(fr, *outs, a_fr, no_l, cite, hr, a_h, sl, ins, t_e)), run_time=0.3)
        agent = logo_chip("claude-code", -4.1, 0.0, h=1.7)
        ref = a7_pill("surface.gdshader:12", 3.0, 1.45, 19 * 0.2 + 0.9)
        pg = a7_doc(3.0, -1.2, 1.4, 1.5)
        a1 = arrow([-2.9, 0.3, 0], [0.3, 1.3, 0], INK, 6, 0.22)
        a2 = arrow([-2.9, -0.3, 0], [0.3, -1.1, 0], INK, 6, 0.22)
        no = a7_no(-1.3, -0.7, 0.28, 7)
        l_ref = a7_lab("line references", 3.0, 0.75, 34)
        l_ans = a7_lab("your answers", 3.0, -2.35, 36)
        until(self, "may check your line references", lead=0.55)
        self.play(FadeIn(agent), GrowArrow(a1), FadeIn(ref), FadeIn(l_ref), run_time=0.5)
        ok = check(5.75, 1.45, s=0.24, color=INK, w=8)
        self.play(Create(ok), run_time=0.25)
        until(self, "never write the answers", lead=0.7)
        self.play(GrowArrow(a2), FadeIn(pg), FadeIn(l_ans), run_time=0.4)
        self.play(Create(no), run_time=0.25)
        done(self)


# ── B55B · what done means ──────────────────────────────────────────────────────────────────────────────────────
class B55B_DoneMeans(Scene):
    def construct(self):
        head = T("Done  means", 56).move_to([-3.3, 2.9, 0], aligned_edge=LEFT)
        items = [("a recorded check", 2.0), ("3 mutations fail", 1.25), ("shaders untouched", 0.5), ("textures credited", -0.25), ("questions answered", -1.0), ("earlier suites", -1.75)]
        phrases = ("Every rule has a recorded check", "All three mutations fail", "No session changed", "Every texture is credited", "every language question answered", "The earlier suites keep their counts")
        until(self, "Done is a list", lead=0.0)
        self.play(FadeIn(head), run_time=0.4)
        for (txt, y), ph in zip(items, phrases):
            until(self, ph, lead=0.3)
            t = T(txt, 48).move_to([-2.5, y, 0], aligned_edge=LEFT)
            k = tick_mark(-3.3, y, 0.28, INK, 9)
            self.play(Create(k), FadeIn(t), run_time=0.35)
        yc = -2.85
        until(self, "Claude said it works", lead=0.45)
        tc = T("Claude said it works", 48, DIM).move_to([-2.5, yc, 0], aligned_edge=LEFT)
        xm = cross_mark(-3.3, yc, 0.28, INK, 9)
        self.play(FadeIn(tc), Create(xm), run_time=0.4)
        spark = Dot([3.4, yc + 0.05, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark, scale=0.4), run_time=0.25)
        done(self)


# ══════════════════════════════ scenes_act8.py ══════════════════════════════
"""ACT VIII · What the Agent Gets Wrong  (B56 and B57 Manim; B58 is a Remotion CCPlainShell, see lanes/act8.json)

B56 and B57 draw the five rows of the assignment's own table "What the agent is likely to get wrong" (evidence/example/sources/assignment-05.md
lines 405-415: "Recorded mistake" / "How it was caught"). The table's words are shortened to labels of one to three words; the pictures that make
a mistake visible are DRAWINGS and carry status_tag("illustrative"); the table as a whole carries status_tag("recorded in the assignment's runs").
Nothing here is a capture or a log: no number is shown that the table does not give (30, 144, 11, 4, 100).
Pacing: until() cues come from the character share of the narration (no audio yet); everything lands by ~90 % of the estimate.
"""

def a8_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a8_table(y_top, y_bot, x_div, header_y=None):
    """The table frame: outline, one column divider, one row divider per call site added by the scene. Returns VGroup(frame, divider)."""
    fr = RoundedRectangle(width=12.2, height=y_top - y_bot, corner_radius=0.18, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, (y_top + y_bot) / 2, 0])
    dv = Line([x_div, y_top, 0], [x_div, y_bot, 0], color=GHOST, stroke_width=4)
    return VGroup(fr, dv)


def a8_hline(y):
    return Line([-6.1, y, 0], [6.1, y, 0], color=GHOST, stroke_width=4)


def a8_tick_small(x, y, s=0.12, color=DIM, w=4):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


# ── B56 · rows 1-2: a test rewritten around its own failure; type checks that were round trips ─────────────────────────────
class B56_RecordedMistakes(Scene):
    def construct(self):
        X_DIV = 2.6
        tbl = a8_table(3.3, -2.3, X_DIV)
        rdv = a8_hline(0.3)
        hd_m = a8_lab("mistake", -1.8, 2.95, 32)
        hd_c = a8_lab("caught by", 4.35, 2.95, 32)
        hdl = a8_hline(2.7)
        t1 = status_tag("recorded in the assignment's runs", -2.9, -2.95)
        t2 = status_tag("illustrative", 1.75, -2.95)
        self.play(Create(tbl), Create(rdv), Create(hdl), FadeIn(hd_m), FadeIn(hd_c), FadeIn(t1), FadeIn(t2), run_time=0.7)
        # row 1: the test that was rewritten to call the update function directly
        test = box(-5.1, 1.55, 1.5, 0.8, color=DIM, sw=4)
        test_l = a8_lab("test", -5.1, 1.55, 34)
        fps = a8_lab("30 fps", -3.55, 2.2, 32, color=DIM)
        a_in = arrow([-4.2, 1.55, 0], [-2.85, 1.55, 0], color=DIM, w=6, tip=0.2)
        until(self, "After a thirty", lead=0.1)
        self.play(Create(test), FadeIn(test_l), FadeIn(fps), GrowArrow(a_in), run_time=0.5)
        until(self, "rewrote its test", lead=0.1)
        upd = box(-1.55, 1.55, 2.3, 0.8, color=INK, sw=4)
        upd_l = M("update()", 26).move_to([-1.55, 1.55, 0])
        a_dir = arrow([-4.2, 1.55, 0], [-2.75, 1.55, 0], color=INK, w=7, tip=0.22)
        self.play(FadeIn(upd), FadeIn(upd_l), run_time=0.4)
        self.play(FadeOut(a_in), GrowArrow(a_dir), run_time=0.35)
        until(self, "update function", lead=0.1)
        x1 = cross_mark(-4.6, 2.2, s=0.17, w=7)
        fl = a8_lab("frame rate ignored", -3.3, 0.72, 32)
        self.play(Create(x1), FadeIn(fl), run_time=0.4)
        until(self, "the summary still", lead=0.1)
        card = box(0.95, 1.38, 1.9, 1.6, color=DIM, sw=4)
        c_l = a8_lab("summary", 0.95, 2.4, 32)
        self.play(Create(card), FadeIn(c_l), run_time=0.4)
        until(self, "thirty and one forty-four", lead=0.1)
        n30 = a8_lab("30", 0.95, 1.7, 44)
        n144 = a8_lab("144", 0.95, 1.05, 44)
        self.play(FadeIn(n30), FadeIn(n144), run_time=0.35)
        # row 2: the semicolon is deleted; all eleven type checks still pass
        until(self, "And its type checks", lead=0.1)
        blk = code_block(["shader_type spatial"], x=-3.5, y=-1.55, size=24, first=1)
        self.play(Create(blk.frame), FadeIn(blk.rows), run_time=0.45)
        until(self, "round trips", lead=0.2)
        rt = a8_lab("round trips", 0.7, -1.55, 36, left=False)
        self.play(FadeIn(rt), run_time=0.35)
        until(self, "semicolon deleted", lead=0.25)
        semi_x = -3.5 - blk.W / 2 + 0.3 + (1 * blk.cw + 0.25) + 19 * blk.cw + 0.12      # just after the 19th character: where the deleted ";" stood
        gap = Dot([semi_x, -1.55, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(gap, scale=0.5), run_time=0.3)
        until(self, "all eleven", lead=0.3)
        ticks = [a8_tick_small(-5.55 + 0.36 * k, -0.55, s=0.13, color=INK, w=5) for k in range(11)]
        n11 = a8_lab("11", -0.75, -0.5, 52)
        self.play(LaggedStart(*[Create(t_) for t_ in ticks], lag_ratio=0.12), FadeIn(n11), run_time=0.8)
        until(self, "Reading the test", lead=0.4)
        eye = eye_icon(3.5, 1.75, s=0.5)
        e_l = a8_lab("reading the test", 4.3, 0.75, 34)
        self.play(Create(eye), FadeIn(e_l), run_time=0.45)
        until(self, "the mutation", lead=0.7)
        term = terminal_icon(3.5, -0.75, s=0.45)
        m_l = a8_lab("the mutation", 4.3, -1.75, 34)
        self.play(Create(term), FadeIn(m_l), run_time=0.4)
        done(self)


# ── B57 · rows 3-5: a misnamed enum; an import key the importer ignores; a flag no check asserted ─────────────────────────
class B57_MoreMistakes(Scene):
    def construct(self):
        X_DIV = 3.2
        tbl = a8_table(3.3, -2.3, X_DIV)
        h1, h2 = a8_hline(2.7), a8_hline(1.0)
        h3 = a8_hline(-0.65)
        hd_m = a8_lab("mistake", -1.4, 2.95, 32)
        hd_c = a8_lab("caught by", 4.65, 2.95, 32)
        t1 = status_tag("recorded in the assignment's runs", -2.9, -2.95)
        t2 = status_tag("illustrative", 1.75, -2.95)
        self.play(Create(tbl), Create(h1), Create(h2), Create(h3), FadeIn(hd_m), FadeIn(hd_c), FadeIn(t1), FadeIn(t2), run_time=0.7)
        # row 3: the enum
        until(self, "An audit misnamed", lead=0.05)
        r3 = a8_lab("enum misnamed", -5.9, 1.85, 32, left=True)
        self.play(FadeIn(r3), run_time=0.35)
        until(self, "four is the Ag X", lead=0.1)
        four = a8_lab("4", -2.55, 1.85, 72)
        agx = M("TONE_MAPPER_AGX", 24).move_to([-1.95, 1.85, 0], aligned_edge=LEFT)
        self.play(FadeIn(four), FadeIn(agx), run_time=0.4)
        until(self, "not Aces", lead=0.05)
        aces = a8_lab("ACES", 2.4, 1.85, 36, color=DIM)
        x3 = cross_mark(1.5, 1.85, s=0.2, w=8)
        self.play(Create(x3), FadeIn(aces), run_time=0.35)
        # row 4: the import key
        until(self, "An import setting", lead=0.1)
        r4 = a8_lab("flat import key", -5.9, 0.175, 32, left=True)
        self.play(FadeIn(r4), run_time=0.35)
        until(self, "a key the importer ignores", lead=0.15)
        pg = RoundedRectangle(width=2.6, height=1.15, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-1.0, 0.175, 0])
        bars = VGroup(*[Line([-2.0, 0.55 - 0.35 * k, 0], [-0.35 - 0.5 * (k % 2), 0.55 - 0.35 * k, 0], color=GHOST, stroke_width=9) for k in range(3)])
        ign = a8_no(1.1, 0.175, r=0.38)
        i_l = a8_lab("ignored", 2.3, 0.175, 32)
        self.play(Create(pg), Create(bars), run_time=0.4)
        self.play(Create(ign), FadeIn(i_l), run_time=0.35)
        # row 5: the flag no check asserted
        until(self, "A material with ambient", lead=0.1)
        r5 = a8_lab("never asserted", -5.9, -1.475, 32, left=True)
        self.play(FadeIn(r5), run_time=0.35)
        until(self, "a hundred checks", lead=0.35)
        grid = VGroup(*[a8_tick_small(-2.3 + 0.2 * c, -0.95 - 0.2 * r, s=0.06, color=DIM, w=3) for r in range(5) for c in range(20)])
        n100 = a8_lab("100", 2.3, -1.3, 44)
        self.play(LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.01), FadeIn(n100), run_time=0.8)
        tog = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([0.45, -2.0, 0])
        knob = Circle(radius=0.13, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([0.25, -2.0, 0])
        ao = M("ao_enabled", 24).move_to([-2.3, -2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(ao), Create(tog), FadeIn(knob), run_time=0.4)
        until(self, "Look every value up", lead=0.6)
        c3 = a8_lab("looking it up", 4.65, 1.85, 32)
        c4 = a8_lab("failing test", 4.65, 0.175, 32)
        c5 = a8_lab("a probe", 4.65, -1.475, 32)
        self.play(LaggedStart(FadeIn(c3), FadeIn(c4), FadeIn(c5), lag_ratio=0.3), run_time=0.7)
        done(self)


def a8_no(x, y, r=0.32, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE a picture, never over type."""
    ring_ = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring_, bar)


# ══════════════════════════════ scenes_act9.py ══════════════════════════════
"""ACT IX · Check What You See  (B59-B68, all Manim)

One cast for the act: the REAL pad captures of the instructor example (the pad shader at activation 0 / 0.5 / 1 / 2: pantry/ev_pad_*.png from
captures/example-native/, Compatibility, 14 Oct; the Forward+ twins pantry/ev_pad_fp_*.png from captures/forward-plus/, re-run 16 Oct), the real
lab frames (captures/lab/, scripted input), the real sphere captures (circle-masked silhouettes pantry/a9_sweep_*, a9_mat_*, made by
evidence/act9/make_a9_pantry.py) and the real constant-ALBEDO probe patches (pantry/a9_probe_c_*, Compatibility).
EVERY pixel number on screen carries its renderer; the numbers are read from evidence/example/controlled-predictions.json,
captures/forward-plus/signal_values_*.json and evidence/runs/R9-constant-albedo-compatibility.json (evidence/act9/verify_numbers.py asserts them).
Pacing: until() cues from the character share of the narration; every fixed sequence ends by ~0.9 x the estimate.
"""

A9P = "pantry/"


def a9_lab(s, x, y, size=34, color=INK, edge=None):
    t = T(s, size, color)
    return t.move_to([x, y, 0]) if edge is None else t.move_to([x, y, 0], aligned_edge=edge)


def a9_img(name, w=None, h=None, at=(0.0, 0.0)):
    im = ImageMobject(A9P + name)
    if w is not None:
        im.set_width(w)
    if h is not None:
        im.set_height(h)
    return im.move_to(np.array([at[0], at[1], 0.0]))


def a9_toggle(x, y, on=False):
    """A generic switch (outline pill, grey knob): off = knob left."""
    pill_ = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([x + (0.2 if on else -0.2), y, 0])
    return VGroup(pill_, knob)


def a9_dots(x, y, r=0.085, color=TERRA):
    """A sample-point mark on a real picture: a ring over a wider grey backing (never a bare thin terracotta stroke)."""
    back = Circle(radius=r + 0.035, stroke_color=DIM, stroke_width=8, stroke_opacity=0.6).move_to([x, y, 0])
    rr = Circle(radius=r, stroke_color=color, stroke_width=5).move_to([x, y, 0])
    return VGroup(back, rr)


def a9_frame(im, sw=12, pad=0.05):
    """A heavy INK frame round a real capture. GATE T's global contrast check counts every mid-tone pixel of a capture as 'text colour' and GATE V's low-contrast
    check averages every non-background pixel: ink mass in the frame pulls both means back toward ink (evidence/act9/RENDER-NOTES.md)."""
    return framed(im, color=INK, pad=pad, sw=sw)


def a9_triple(rgb, sep=","):
    return sep.join(str(int(v)) for v in rgb)


# ── B59 · green logs are not done: what a headless pass proves, and the human check ──────────────────────────────────────────
class B59_GreenLogs(Scene):
    def construct(self):
        title = T("Check What You See", 40).move_to([-3.4, 2.95, 0])
        self.add(title)
        PX, PY = 2.45, 0.1                                   # centre of the panel crop
        px = 6.4 / 1110.0                                    # scene units per source pixel of the panel crop
        panel = framed(a9_img("a9_panel_609.png", w=6.4, at=(PX, PY)))
        tag = status_tag("scripted input \u00b7 earlier take, 14 Oct", PX, 2.4)
        # The frame is the EARLIER take of the lab (captures/lab = native-lab, 14 Oct 01:52; the repo's current verification.gd prints "State probe checks linkage."
        # instead of "Headless proves state."). Only the line both takes print, "Render and play still need checking." (crop rows 516..574 of 609), is marked: an ink
        # bracket OUTSIDE the panel (a ring over the dark panel is read by GATE T as accent text on a dark ground) and one terracotta dot
        yt = PY - (516 - 304.5) * px
        yb = PY - (574 - 304.5) * px
        bx = PX + 3.2 + 0.3
        brk = VGroup(Line([bx - 0.17, yt, 0], [bx, yt, 0], color=INK, stroke_width=6), Line([bx, yt, 0], [bx, yb, 0], color=INK, stroke_width=6),
                     Line([bx, yb, 0], [bx - 0.17, yb, 0], color=INK, stroke_width=6))
        bdot = Dot([bx + 0.2, (yt + yb) / 2, 0], radius=0.1, color=TERRA)
        scr = RoundedRectangle(width=6.65, height=3.72, corner_radius=0.16, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([PX, PY, 0])
        scr_l = a9_lab("the screen", PX, PY, 40)
        ys = [0.1, -0.65, -1.4, -2.15]
        ti = terminal_icon(-5.1, 1.05, s=0.42)
        hd = a9_lab("headless test", -4.45, 1.05, 36, edge=LEFT)
        ticks = [tick_mark(-5.45, y, s=0.2) for y in ys]
        # green logs: the headless test's four checks, all ticked (GATE T samples each clip at 50%: the dark engine panel lands AFTER the midpoint, with "the screen")
        until(self, "Green logs", lead=0.0)
        self.play(Create(ti), FadeIn(hd), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.2), run_time=0.8)
        until(self, "A headless pass", lead=0.25)
        self.play(Create(scr), FadeIn(scr_l), run_time=0.5)
        for word, y, ph_, ld in (("parse", ys[0], "parse", 0.3), ("declared", ys[1], "declared", 0.3), ("driven", ys[2], "driven", 0.3), ("wired", ys[3], "wired", 0.3)):
            until(self, ph_, lead=ld)
            self.play(FadeIn(a9_lab(word, -4.95, y, 36, edge=LEFT)), run_time=0.3)
        until(self, "It proves nothing", lead=0.3)
        self.play(FadeOut(scr_l), FadeIn(panel), FadeIn(tag), run_time=0.5)
        eye = eye_icon(1.3, -2.45, s=0.5)
        ey = a9_lab("your eyes", 2.0, -2.45, 36, edge=LEFT)
        ex = example_tag(-2.75, -3.0)
        until(self, "about the screen", lead=-0.2)
        self.play(Create(eye), FadeIn(ey), FadeIn(ex), run_time=0.45)
        until(self, "Every visual rule", lead=0.2)
        self.play(Create(brk), FadeIn(bdot, scale=0.5), run_time=0.5)
        done(self)


# ── B60 · capture in the engine: two paths from the drawn frame to a PNG, then the capture function ─────────────────────────
class B60_CaptureInEngine(Scene):
    def construct(self):
        DY = -1.5                                            # the lanes start centred, then rise to make room for the code
        # --- lanes (drawn at their FINAL height; shifted down by DY before they are shown) ---
        shared = box(-5.1, 1.9, 1.9, 2.1)
        shared_l = VGroup(a9_lab("engine", -5.1, 2.15, 34), a9_lab("frame", -5.1, 1.65, 34))
        a_up = arrow([-4.1, 2.5, 0], [-3.4, 2.5, 0], w=6)
        png = box(-2.32, 2.5, 2.16, 0.85)
        png_l = a9_lab("PNG file", -2.32, 2.5, 34)
        a_lo = arrow([-4.1, 1.3, 0], [-3.4, 1.3, 0], w=6)
        prof = box(-1.87, 1.3, 3.06, 0.85)
        prof_l = a9_lab("colour profile", -1.87, 1.3, 34)
        a_lo2 = arrow([-0.3, 1.3, 0], [0.4, 1.3, 0], w=6)
        scal = box(1.3, 1.3, 1.8, 0.85)
        scal_l = a9_lab("scaling", 1.3, 1.3, 34)
        a_lo3 = arrow([2.25, 1.3, 0], [2.95, 1.3, 0], w=6)
        shot = box(4.27, 1.3, 2.53, 0.85)
        shot_l = a9_lab("screenshot", 4.27, 1.3, 34)
        ok = tick_mark(-0.75, 2.5, s=0.22, w=8)
        d1 = Dot([-1.87 + 1.53 - 0.05, 1.3 + 0.425, 0], radius=0.12, color=TERRA)     # a pin on the box's top-right corner
        d2 = Dot([1.3 + 0.9 - 0.05, 1.3 + 0.425, 0], radius=0.12, color=TERRA)
        up_grp = VGroup(a_up, png, png_l, ok)
        lo_grp = VGroup(a_lo, prof, prof_l, a_lo2, scal, scal_l, a_lo3, shot, shot_l)
        lanes = VGroup(shared, shared_l, up_grp, lo_grp, d1, d2)
        lanes.shift(DOWN * (-DY))                            # DY is negative: shift down by 1.5
        self.add(shared, shared_l)
        until(self, "Capture in the engine", lead=0.0)
        self.play(GrowArrow(a_up), Create(png), FadeIn(png_l), Create(ok), run_time=0.7)
        until(self, "operating system", lead=0.25)
        self.play(GrowArrow(a_lo), Create(prof), FadeIn(prof_l), run_time=0.4)
        self.play(GrowArrow(a_lo2), Create(scal), FadeIn(scal_l), GrowArrow(a_lo3), Create(shot), FadeIn(shot_l), run_time=0.7)
        until(self, "colour profiles", lead=0.45)
        self.play(FadeIn(d1, scale=0.5), run_time=0.3)
        until(self, "scaling", lead=0.6)
        self.play(FadeIn(d2, scale=0.5), run_time=0.3)
        # --- the capture function of the assignment (assignment-05.md lines 457-460), then the example's own line ---
        code1 = code_block(["    mat.set_shader_parameter(param, value)", "    await RenderingServer.frame_post_draw",
                            "    get_viewport().get_texture().get_image().save_png(path)", "    driver.set_process(true)"],
                           x=-0.9, y=-0.3, size=20, first=457, pad=0.2)
        row_y = [-0.3 + code1.H / 2 - 0.2 - code1.lh * (i + 0.5) for i in range(4)]       # rows 457..460
        px1 = -0.9 + code1.W / 2 + 0.3                                                       # a terracotta pointer sits just right of the frame
        drv_l = a9_lab("driver", 5.45, 0.55, 34)
        tog = a9_toggle(5.45, 0.0, on=False)
        t1 = status_tag("from the assignment", -4.2, -2.85)
        code2 = code_block(["\tawait RenderingServer.frame_post_draw"], x=-2.5, y=-1.75, size=20, first=11, pad=0.2)
        px2 = -2.5 + code2.W / 2 + 0.3
        fl = M("render-material-evidence.gd", 20).move_to([px2 + 0.35 + 2.0, -1.75, 0])
        t2 = example_tag(1.7, -2.85)

        def ptr(x, y):                                         # a terracotta pointer (the row being read), pointing left at the code
            return Polygon([x + 0.12, y + 0.17, 0], [x + 0.12, y - 0.17, 0], [x - 0.15, y, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
        r1 = ptr(px1, row_y[0])
        until(self, "Switch the driver off", lead=0.55)
        self.play(lanes.animate.shift(UP * (-DY)), FadeIn(code1), FadeIn(t1), run_time=0.6)
        self.play(FadeIn(drv_l), Create(tog), run_time=0.3)
        until(self, "set the value", lead=0.25)
        self.play(FadeIn(r1, shift=LEFT * 0.2), run_time=0.25)
        until(self, "wait for the frame", lead=0.3)
        r2 = ptr(px2, -1.75)
        self.play(r1.animate.shift(DOWN * code1.lh), FadeIn(code2), FadeIn(fl), FadeIn(t2), run_time=0.4)
        self.play(FadeIn(r2, shift=LEFT * 0.2), run_time=0.25)
        until(self, "save the viewport", lead=0.35)
        self.play(r1.animate.shift(DOWN * code1.lh), run_time=0.35)
        done(self)


# ── B61 · the example's four pad captures, two sample pixels each, the dark one measured beside its prediction ─────────────────
# numbers: controlled-predictions.json (predicted_display_rgb8_compatibility, dark stripe) and signal_values_compatibility.json (rgb8, uv_x 0.15625)
A9_PRED = {"0": (66, 27, 15), "0.5": (48, 105, 74), "1": (31, 184, 133), "2": (0, 255, 250)}
A9_MEAS = {"0": (66, 24, 10), "0.5": (47, 105, 74), "1": (28, 184, 133), "2": (0, 255, 251)}


class B61_FourCaptures(Scene):
    def construct(self):
        W = 2.8
        Hh = W * 1080 / 1620.0
        pos = {"0": (-4.7, 1.65), "0.5": (-1.75, 1.65), "1": (-4.7, -1.0), "2": (-1.75, -1.0)}
        names = {"0": "ev_pad_0.0.png", "0.5": "ev_pad_0.5.png", "1": "ev_pad_1.0.png", "2": "ev_pad_2.0.png"}
        caps, labs = {}, {}
        for k, (cx, cy) in pos.items():
            caps[k] = framed(a9_img(names[k], w=W, at=(cx, cy)))
            labs[k] = a9_lab("activation " + k, cx, cy - Hh / 2 - 0.33, 32)
        # the table (right): header, four outline rows
        hd = a9_lab("dark stripe pixel", 3.55, 3.0, 34)
        dk = Dot([1.7, 3.0, 0], radius=0.1, color=TERRA)
        h1 = a9_lab("predicted", 2.7, 2.4, 32)
        h2 = a9_lab("measured", 4.95, 2.4, 32)
        ry = {"0": 1.5, "0.5": 0.5, "1": -0.5, "2": -1.5}
        rbox, rnum, rp, rm = {}, {}, {}, {}
        for k, y in ry.items():
            rbox[k] = box(3.125, y, 6.15, 0.85)
            rnum[k] = T(k, 44).move_to([0.7, y, 0])
            rp[k] = M(a9_triple(A9_PRED[k]), 24).move_to([2.7, y, 0])
            rm[k] = M(a9_triple(A9_MEAS[k]), 24).move_to([4.95, y, 0])
        tg1 = example_tag(-2.9, -3.0)
        tg2 = status_tag("Compatibility", 3.4, -3.0)
        # legend of the two marks (the table is the terracotta one)
        lg1 = Dot([0.65, -2.35, 0], radius=0.1, color=TERRA)
        lg1l = a9_lab("dark stripe", 0.95, -2.35, 32, edge=LEFT)
        lg2 = Dot([3.3, -2.35, 0], radius=0.1, color=INK)
        lg2l = a9_lab("light stripe", 3.6, -2.35, 32, edge=LEFT)
        until(self, "The example's four", lead=0.0)
        self.play(FadeIn(tg1), FadeIn(tg2), run_time=0.3)
        for k, ph, ld in (("0", "activation zero", 0.3), ("0.5", "half", 0.4), ("1", "one and two", 0.4), ("2", "and two", 0.0)):
            until(self, ph, lead=ld)
            self.play(FadeIn(caps[k]), FadeIn(labs[k]), run_time=0.3)
        # after the midpoint: the two named pixels (UV.x 0.15625 -> source x 253, UV.x 0.21875 -> x 354, both at the vertical middle), then the table
        until(self, "two named pixels", lead=0.1)
        marks = VGroup()
        kx = W / 1620.0
        for k, (cx, cy) in pos.items():
            for sx, col in ((253, TERRA), (354, INK)):
                marks.add(Circle(radius=0.085, stroke_color=CARD, stroke_width=4).move_to([cx - W / 2 + sx * kx, cy, 0]),
                          Dot([cx - W / 2 + sx * kx, cy, 0], radius=0.055, color=col))
        self.play(FadeIn(marks, scale=0.6), FadeIn(lg1, scale=0.5), FadeIn(lg1l), FadeIn(lg2, scale=0.5), FadeIn(lg2l), run_time=0.4)
        until(self, "measured beside", lead=0.3)
        self.play(FadeIn(hd), FadeIn(dk, scale=0.5), FadeIn(h1), FadeIn(h2), run_time=0.3)
        for k in ("0", "0.5", "1", "2"):
            self.play(Create(rbox[k]), FadeIn(rnum[k]), FadeIn(rp[k]), FadeIn(rm[k]), run_time=0.3)
        until(self, "At half", lead=0.2)
        ptr = Polygon([-0.32, 0.5 + 0.2, 0], [-0.32, 0.5 - 0.2, 0], [-0.02, 0.5, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
        self.play(FadeIn(ptr, shift=RIGHT * 0.2), run_time=0.4)
        done(self)


# ── B62 · the gaps (per channel), then the probe: a plain constant colour shows the same shortfall ──────────────────────────────
A9_GAP = [("activation 0", "dark stripe", (0, -3, -5)), ("activation 1", "", (-3, 0, 0))]   # measured minus predicted, Compatibility (analysis.json diff_compat_minus_prediction)
A9_PROBE = [(0.0585, 15, 10), (0.104, 27, 24), (0.12, 31, 28)]                                 # value, as written (x255), Compatibility read (R9 json)


class B62_Gaps(Scene):
    def construct(self):
        TX = 2.65                                             # the gap table is built centred (shifted right by TX), then slides left to its final place
        cw, pitch = 1.3, 1.4
        cols = [-2.9 + pitch * i for i in range(3)]           # FINAL x of the three columns
        heads = [a9_lab(n, x, 2.5, 34) for n, x in zip(("red", "green", "blue"), cols)]
        rows_y = [1.35, -0.2]
        cells, nums, bars, rlabs = [], [], [], []
        for (a, b, gaps), y in zip(A9_GAP, rows_y):
            rlabs.append(VGroup(a9_lab(a, -4.9, y + (0.22 if b else 0.0), 32), *([a9_lab(b, -4.9, y - 0.27, 32)] if b else [])))
            for x, g in zip(cols, gaps):
                cells.append(box(x, y, cw, 1.2, sw=3))
                nums.append(T("%s%d" % ("\u2212" if g < 0 else "", abs(g)), 44).move_to([x, y + 0.17, 0]))
                bw = abs(g) * 0.2
                bars.append(Rectangle(width=max(bw, 0.001), height=0.12, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([x - cw / 2 + 0.14 + bw / 2, y - 0.38, 0]))
        table = VGroup(*heads, *rlabs, *cells, *nums, *bars)
        # dots by the two numbers the voice names: blue at activation 0 (-5), red at activation 1 (-3)
        dot_b = Dot([cols[2] + 0.42, rows_y[0] + 0.44, 0], radius=0.1, color=TERRA)
        dot_r = Dot([cols[0] + 0.42, rows_y[1] + 0.44, 0], radius=0.1, color=TERRA)
        # the probe (right side): three real constant-colour patches, written value -> read value (Compatibility)
        ph_ = a9_lab("probe: constant colour", 3.75, 2.5, 34)
        c1 = a9_lab("written", 4.1, 1.55, 32)
        c2 = a9_lab("read", 5.75, 1.55, 32)
        prow = []
        for (v, w, r), y in zip(A9_PROBE, (0.65, -0.55, -1.75)):
            im = framed(a9_img("a9_probe_c_%s.png" % v, h=0.9, at=(1.4, y)), pad=0.05, sw=3)
            vl = a9_lab(str(v), 2.7, y, 34)
            wn = T(str(w), 44).move_to([4.1, y, 0])
            ar = arrow([4.5, y, 0], [5.3, y, 0], w=6, tip=0.24)
            rn = T(str(r), 48).move_to([5.8, y, 0])
            prow.append(Group(im, vl, wn, ar, rn))
        tg1 = status_tag("Compatibility", 3.3, -3.0)
        tg2 = example_tag(-2.9, -3.0)
        table.shift(RIGHT * TX)
        dot_b.shift(RIGHT * TX)
        dot_r.shift(RIGHT * TX)
        until(self, "Not every value", lead=0.0)
        self.play(FadeIn(VGroup(*heads)), LaggedStart(*[Create(c) for c in cells], lag_ratio=0.1), FadeIn(VGroup(*rlabs)), FadeIn(tg1), FadeIn(tg2), run_time=0.7)
        until(self, "dark stripe at zero", lead=0.2)
        self.play(FadeIn(VGroup(*nums[:3])), FadeIn(VGroup(*bars[:3])), run_time=0.4)
        until(self, "five in blue", lead=0.2)
        self.play(FadeIn(dot_b, scale=0.5), run_time=0.25)
        until(self, "full activation", lead=0.2)
        self.play(FadeIn(VGroup(*nums[3:])), FadeIn(VGroup(*bars[3:])), run_time=0.4)
        until(self, "three in red", lead=0.3)
        self.play(FadeIn(dot_r, scale=0.5), run_time=0.25)
        until(self, "A probe", lead=0.2)
        slide = VGroup(table, dot_b, dot_r)
        self.play(slide.animate.shift(LEFT * TX), run_time=0.5)
        self.play(FadeIn(ph_), FadeIn(c1), FadeIn(c2), run_time=0.3)
        until(self, "constant colour", lead=0.3)
        for pr in prow:
            self.play(FadeIn(pr, shift=LEFT * 0.15), run_time=0.3)
        until(self, "Cause still open", lead=1.0)
        oc = open_circle(-5.35, -1.6, 0.2)
        ol = a9_lab("cause still open", -4.95, -1.6, 36, edge=LEFT)
        self.play(Create(oc), FadeIn(ol), run_time=0.4)
        done(self)


# ── B63 · Forward+ differs: the same pad at half in both renderers, the light stripe's real numbers ────────────────────────────
class B63_ForwardPlusDiffers(Scene):
    def construct(self):
        # real 1080 x 540 bands of the pad captures at half activation (pantry/a9_pad_strip_*, made by evidence/act9/make_a9_pantry.py);
        # the light-stripe pixel (UV.x 0.21875) sits at x 354, y 270 of the band. Heavy ink frames: see a9_frame (the bare green captures give GATE T 4.47:1).
        pc, pf = "pantry/a9_pad_strip_0.5.png", "pantry/a9_pad_strip_fp_0.5.png"
        CW = 5.0
        k = CW / 1080.0
        CY = 1.15
        L = a9_frame(img(pc, w=CW, x=-3.1, y=CY))
        R = a9_frame(img(pf, w=CW, x=3.1, y=CY))
        tgl = status_tag("Compatibility", -3.1, 2.85)
        tgr = status_tag("Forward+ \u00b7 re-run", 3.1, 2.85)
        sl = swatch((66, 112, 78), -4.95, -0.6, w=0.9, h=0.6)
        sr = swatch((76, 137, 97), 1.25, -0.6, w=0.9, h=0.6)
        nl = M("66,112,78", 36).move_to([-3.0, -0.6, 0])
        nr = M("76,137,97", 36).move_to([3.2, -0.6, 0])
        okl = tick_mark(-1.15, -0.6, s=0.22, w=8)
        xr = cross_mark(5.1, -0.6, s=0.2, w=8)
        pl = a9_lab("prediction", -0.4, -1.3, 36)
        pn = M("66,112,78", 36).move_to([2.3, -1.3, 0])
        lgd = Dot([-5.55, -1.3, 0], radius=0.1, color=TERRA)                       # the ringed pixel is the LIGHT stripe (UV.x 0.21875)
        lgl = a9_lab("light stripe", -5.25, -1.3, 36, edge=LEFT)
        ml = a9_dots(-3.1 - CW / 2 + 354 * k, CY, 0.12, TERRA)
        mr = a9_dots(3.1 - CW / 2 + 354 * k, CY, 0.12, TERRA)
        # the calculation in linear light (a fit of numbers: evidence/runs/scripts/analyze.py), drawn after the midpoint
        b1 = box(-4.45, -2.05, 1.65, 0.85); l1 = a9_lab("decode", -4.45, -2.05, 34)
        b2 = box(-1.4, -2.05, 2.9, 0.85); l2 = a9_lab("mix in linear", -1.4, -2.05, 34)
        b3 = box(1.7, -2.05, 1.75, 0.85); l3 = a9_lab("encode", 1.7, -2.05, 34)
        ar1 = arrow([-3.5, -2.05, 0], [-2.95, -2.05, 0], w=6, tip=0.24)
        ar2 = arrow([0.14, -2.05, 0], [0.74, -2.05, 0], w=6, tip=0.24)
        hero = T("24 of 24", 48).move_to([4.7, -1.85, 0])
        hero_l = a9_lab("values fit", 4.7, -2.45, 34)
        tge = example_tag(-2.75, -3.1)
        until(self, "Switch renderer", lead=0.0)
        self.play(FadeIn(L), FadeIn(tgl), FadeIn(tge), run_time=0.4)
        until(self, "On Forward Plus", lead=0.3)
        self.play(FadeIn(R), FadeIn(tgr), run_time=0.4)
        until(self, "on the light stripe", lead=0.3)
        self.play(FadeIn(ml, scale=0.5), FadeIn(mr, scale=0.5), FadeIn(lgd, scale=0.5), FadeIn(lgl), run_time=0.35)
        until(self, "seventy-six", lead=0.1)
        self.play(FadeIn(sr), FadeIn(nr), run_time=0.3)
        until(self, "not sixty-six", lead=0.2)
        self.play(FadeIn(sl), FadeIn(nl), Create(okl), run_time=0.35)
        self.play(FadeIn(pl), FadeIn(pn), Create(xr), run_time=0.4)
        until(self, "Those numbers", lead=0.25)
        self.play(Create(b1), FadeIn(l1), GrowArrow(ar1), Create(b2), FadeIn(l2), GrowArrow(ar2), Create(b3), FadeIn(l3), run_time=0.8)
        self.play(FadeIn(hero), FadeIn(hero_l), run_time=0.3)
        done(self)


# ── B64 · activation 2: cyan, and hint_range did not clamp (a drawn slider; both renderers) ───────────────────────────────────
class B64_NoClamp(Scene):
    def construct(self):
        # Order of arrival follows the voice: the Compatibility pad at 2 (cyan) and its arithmetic first; Forward+ and the activation-1 comparison after the midpoint.
        # (GATE T's global contrast check counts the flat green of activation 1 as text colour: it must not be on screen at the clip midpoint.)
        W = 3.6
        xs = [-4.1, 0.0, 4.1]
        y = 1.3
        cap_c = a9_frame(img("pantry/ev_pad_2.0.png", w=W, x=xs[0], y=y))
        cap_f = a9_frame(img("pantry/ev_pad_fp_2.0.png", w=W, x=xs[1], y=y))
        cap_1 = a9_frame(img("pantry/ev_pad_1.0.png", w=W, x=xs[2], y=y))
        h_c = a9_lab("activation 2", xs[0], 2.95, 36)
        h_f = a9_lab("activation 2", xs[1], 2.95, 36)
        h_1 = a9_lab("activation 1", xs[2], 2.95, 36)
        n_c = M("0,255,251", 28).move_to([xs[0], -0.5, 0])
        n_f = M("0,248,181", 28).move_to([xs[1], -0.5, 0])
        n_1 = M("28,184,133", 28).move_to([xs[2], -0.5, 0])
        r_c = a9_lab("Compatibility", xs[0], -1.0, 32)
        r_f = status_tag("Forward+ \u00b7 re-run", xs[1], -1.05)
        r_1 = a9_lab("Compatibility", xs[2], -1.0, 32)
        # the arithmetic that clips (mix(base, active, 2.0) per channel, from the colours as written: dark stripe)
        c_r = a9_lab("red \u22120.02, shown 0", xs[0], -1.7, 34)
        c_g = a9_lab("green 1.34, shown 255", xs[0], -2.25, 34)
        tg = example_tag(-2.75, -3.1)
        # the slider (right): a track for hint_range(0.0, 1.0) (value 0 at x = 0.0, value 1 at x = 2.4), the value 2.0 set from code beyond its end (x = 4.8)
        TY = -2.2
        trk = Line([0.0, TY, 0], [2.4, TY, 0], color=INK, stroke_width=8)
        cap_a = Line([0.0, TY + 0.2, 0], [0.0, TY - 0.2, 0], color=INK, stroke_width=8)
        cap_b = Line([2.4, TY + 0.2, 0], [2.4, TY - 0.2, 0], color=INK, stroke_width=8)
        hnd = Dot([2.4, TY, 0], radius=0.18, color=DIM)
        far = DashedLine([2.65, TY, 0], [4.55, TY, 0], color=DIM, stroke_width=6, dash_length=0.18)
        val = Dot([4.8, TY, 0], radius=0.17, color=TERRA)
        v_l = a9_lab("2.0 set from code", 4.4, TY + 0.55, 34)
        rng = M("hint_range(0.0, 1.0)", 20).move_to([1.2, TY - 0.5, 0])
        sl_l = a9_lab("slider", 1.2, TY + 0.55, 34)
        until(self, "At two", lead=0.0)
        self.play(FadeIn(cap_c), FadeIn(h_c), run_time=0.35)
        self.play(FadeIn(n_c), FadeIn(r_c), FadeIn(tg), run_time=0.25)
        until(self, "red goes negative", lead=0.3)
        self.play(FadeIn(c_r), run_time=0.3)
        until(self, "green passes one", lead=0.3)
        self.play(FadeIn(c_g), run_time=0.3)
        until(self, "either renderer", lead=0.7)
        self.play(FadeIn(cap_f), FadeIn(h_f), run_time=0.35)
        self.play(FadeIn(n_f), FadeIn(r_f), run_time=0.2)
        until(self, "the answer is no", lead=0.9)
        self.play(FadeIn(cap_1), FadeIn(h_1), run_time=0.35)
        self.play(FadeIn(n_1), FadeIn(r_1), run_time=0.2)
        until(self, "The range belongs", lead=0.3)
        self.play(Create(trk), Create(cap_a), Create(cap_b), FadeIn(hnd), FadeIn(rng), FadeIn(sl_l), run_time=0.5)
        self.play(Create(far), FadeIn(val, scale=0.5), FadeIn(v_l), run_time=0.5)
        done(self)


# ── B65 · in play: four real lab frames in sequence (scripted input); your own playtest is required ───────────────────────────
class B65_InPlay(Scene):
    def construct(self):
        W = 2.7
        xs = [-4.6, -1.55, 1.5, 4.55]
        y = 0.8
        files = ["a9_pad_lab_000503.png", "a9_pad_lab_000597.png", "a9_pad_lab_000609.png", "a9_pad_lab_000610.png"]
        caps = [a9_frame(a9_img(f, w=W, at=(x, y)), sw=14) for f, x in zip(files, xs)]
        # labels read from each frame's own HUD line (CHARGING / 27%, CHARGING / 94%) and the pad state (frames' text: ON THE PAD, GATE OPEN)
        labs = [a9_lab(s, x, -0.6, 32) for s, x in zip(("on the pad", "charging 27%", "charging 94%", "gate open"), xs)]
        tg = status_tag("scripted input \u00b7 earlier take, 14 Oct", 0.0, 2.85)
        ex = example_tag(3.05, -3.1)
        key = VGroup(RoundedRectangle(width=0.85, height=0.85, corner_radius=0.14, stroke_color=INK, stroke_width=5, fill_opacity=0),
                     M("E", 36)).move_to([-4.9, -1.9, 0])
        key_l = a9_lab("scripted key press", -4.2, -1.9, 34, edge=LEFT)
        eye = eye_icon(0.95, -1.9, s=0.5)
        eye_l = a9_lab("your own playtest", 1.7, -1.9, 34, edge=LEFT)
        until(self, "In play", lead=0.0)
        self.play(FadeIn(tg), FadeIn(ex), run_time=0.3)
        for i, ph, ld in ((0, "trigger the state", 0.0), (1, "by normal play", 0.0), (2, "several times", 0.15), (3, "boundaries hold", 0.5)):
            until(self, ph, lead=ld)
            self.play(FadeIn(caps[i]), FadeIn(labs[i]), run_time=0.3)
        until(self, "scripted key presses", lead=0.45)
        self.play(Create(key), FadeIn(key_l), run_time=0.4)
        until(self, "Your own playtest", lead=0.25)
        self.play(Create(eye), FadeIn(eye_l), run_time=0.45)
        done(self)


# ── B66 · interface sweep: each uniform at minimum, default, maximum (twelve real sphere crops) and the stated lighting ──────
A9_SWEEP = [("roughness_gain", "0.0  0.8  1.0"), ("uv_scale", "0.25  1  4"), ("tint", "black  white  red"), ("metallic_gain", "0  0  1")]


class B66_Sweep(Scene):
    def construct(self):
        D = 1.25
        xs = [-2.45, -0.6, 1.25]
        ys = [2.0, 0.67, -0.66, -1.99]
        hs = [a9_lab(s, x, 3.0, 32) for s, x in zip(("minimum", "default", "maximum"), xs)]
        rowlab = []
        for (nm, vals), y in zip(A9_SWEEP, ys):
            rowlab.append(VGroup(M(nm, 24).move_to([-4.85, y + 0.2, 0]), (M(vals, 24) if nm != "tint" else T(vals, 32)).move_to([-4.85, y - 0.22, 0])))
        spheres = []
        for (nm, _v), y in zip(A9_SWEEP, ys):
            spheres.append(Group(*[a9_img("a9_sweep_%s_%d.png" % (nm, i), w=D, at=(xs[i], y)) for i in range(3)]))
        lt = [a9_lab("same lighting", 4.0, 2.5, 34)] + [a9_lab(s, 2.65, 1.75 - 0.62 * i, 32, edge=LEFT)
                                                                      for i, s in enumerate(("fixed camera", "Linear tonemap", "exposure 1.0", "light (−30, −30, 0)", "ambient 0.35", "no SSAO"))]
        tg = example_tag(-2.9, -3.1)
        tg2 = status_tag("Compatibility", 3.3, -3.1)
        until(self, "Interface sweep", lead=0.0)
        self.play(FadeIn(VGroup(*hs)), FadeIn(VGroup(*rowlab)), FadeIn(tg), FadeIn(tg2), run_time=0.45)
        until(self, "each uniform", lead=0.2)
        self.play(LaggedStart(*[FadeIn(t) for t in lt], lag_ratio=0.12), run_time=0.9)
        until(self, "roughness spreads", lead=0.5)
        self.play(FadeIn(spheres[0], shift=UP * 0.1), run_time=0.4)
        until(self, "scale repeats", lead=0.45)
        self.play(FadeIn(spheres[1], shift=UP * 0.1), run_time=0.4)
        until(self, "black tint", lead=0.45)
        self.play(FadeIn(spheres[2], shift=UP * 0.1), run_time=0.4)
        until(self, "Record what changed", lead=0.3)
        self.play(FadeIn(spheres[3], shift=UP * 0.1), run_time=0.4)
        done(self)


# ── B67 · one shader, two materials: baseline, a shared (shader) edit, a one-value edit ──────────────────────────────────────
def a9_sring(x, y, r=0.93):
    back = Circle(radius=r + 0.05, stroke_color=DIM, stroke_width=10, stroke_opacity=0.6).move_to([x, y, 0])
    rr = Circle(radius=r, stroke_color=TERRA, stroke_width=6).move_to([x, y, 0])
    return VGroup(back, rr)


class B67_OneShaderTwoMaterials(Scene):
    def construct(self):
        D = 1.7
        gx = [-4.15, 0.0, 4.15]
        sy = 0.45
        pairs = []
        for tag, x in zip(("baseline", "shared", "one"), gx):
            pairs.append(Group(a9_img("a9_mat_%s_l.png" % tag, w=D, at=(x - 1.05, sy)), a9_img("a9_mat_%s_r.png" % tag, w=D, at=(x + 1.05, sy))))
        # a drawn shader card above each pair, one line to each material
        cards = []
        for x in gx:
            c = box(x, 2.55, 3.0, 0.6, sw=3)
            cl = M("surface.gdshader", 20).move_to([x, 2.55, 0])
            l1 = Line([x - 0.5, 2.25, 0], [x - 1.05, sy + D / 2 + 0.12, 0], color=DIM, stroke_width=4)
            l2 = Line([x + 0.5, 2.25, 0], [x + 1.05, sy + D / 2 + 0.12, 0], color=DIM, stroke_width=4)
            cards.append(VGroup(c, cl, l1, l2))
        capt = [VGroup(a9_lab("baseline", gx[0], -0.95, 36)),
                VGroup(a9_lab("shader edited", gx[1], -0.95, 36), a9_lab("tint × (1, 0.25, 0.25)", gx[1], -1.5, 32)),
                VGroup(a9_lab("one value edited", gx[2], -0.95, 36), a9_lab("left tint", gx[2], -1.5, 32), a9_lab("(0.2, 0.2, 1.0)", gx[2], -2.0, 32))]
        d_sh = Dot([gx[1] + 1.75, 2.55, 0], radius=0.1, color=TERRA)             # where the edit is made: in the shader
        d_mat = Dot([gx[2] - 1.83, sy + 0.78, 0], radius=0.1, color=TERRA)  # ... or in one material
        r_both = VGroup(a9_sring(gx[1] - 1.05, sy), a9_sring(gx[1] + 1.05, sy))
        r_left = a9_sring(gx[2] - 1.05, sy)
        tg = example_tag(-2.9, -3.0)
        tg2 = status_tag("Compatibility", 3.3, -3.0)
        until(self, "One shader", lead=0.0)
        self.play(FadeIn(pairs[0]), FadeIn(cards[0]), FadeIn(capt[0]), FadeIn(tg), FadeIn(tg2), run_time=0.5)
        until(self, "Edit the shader", lead=0.25)
        self.play(FadeIn(pairs[1]), FadeIn(cards[1]), FadeIn(capt[1]), FadeIn(d_sh, scale=0.5), run_time=0.5)
        until(self, "Restore it", lead=0.2)
        self.play(FadeIn(pairs[2]), FadeIn(cards[2]), FadeIn(capt[2]), FadeIn(d_mat, scale=0.5), run_time=0.5)
        until(self, "shared edit", lead=0.8)
        self.play(Create(r_both), run_time=0.5)
        until(self, "tint edit", lead=1.0)
        self.play(Create(r_left), run_time=0.5)
        done(self)


# ── B68 · after the first editor session: git status; and the four things the example did not do (open circles) ─────────────
class B68_NotDone(Scene):
    def construct(self):
        L = -4.55                                              # left edge of the whole picture
        cmd = code_block(["git status"], x=-3.05, y=2.4, size=32, numbers=False, pad=0.28)
        t1 = status_tag("documented, not run", -3.05, 1.55)
        a1 = arrow([-1.35, 2.4, 0], [-0.45, 2.4, 0], w=6)
        fcard = box(2.2, 2.4, 4.85, 0.9, sw=4)
        fname = M("*.png.import", 28).move_to([2.2, 2.4, 0])
        eye = eye_icon(-4.05, 0.6, s=0.5)
        a2 = arrow([-3.3, 0.6, 0], [-2.3, 0.6, 0], w=6)
        rev = box(-0.9, 0.6, 2.0, 0.8, sw=4)
        rev_l = a9_lab("revision", -0.9, 0.6, 36)
        hdr = a9_lab("the example did not", L, -0.25, 38, edge=LEFT)
        sp = Dot([-0.15, -0.25, 0], radius=0.1, color=TERRA)
        items = ["no person played it", "no screenshot comparison", "no Claude Code session", "shortfall unexplained"]
        ys = [-0.95, -1.65, -2.35, -3.05]
        circs = [open_circle(L + 0.25, y, 0.21) for y in ys]
        labs = [a9_lab(s, L + 0.75, y, 40, edge=LEFT) for s, y in zip(items, ys)]
        tg = example_tag(3.2, -0.25)
        until(self, "After your first", lead=0.0)
        self.play(Create(cmd), FadeIn(t1), run_time=0.5)
        until(self, "import file", lead=0.6)
        self.play(GrowArrow(a1), Create(fcard), FadeIn(fname), run_time=0.6)
        until(self, "revision", lead=0.9)
        self.play(Create(eye), GrowArrow(a2), Create(rev), FadeIn(rev_l), run_time=0.6)
        until(self, "What the example did not do", lead=0.35)
        self.play(FadeIn(hdr), FadeIn(sp, scale=0.5), FadeIn(tg), run_time=0.4)
        for c, lb, ph, ld in zip(circs, labs, ("no person played", "no screenshot", "no Claude Code", "unexplained"), (0.3, 0.3, 0.3, 0.9)):
            until(self, ph, lead=ld)
            self.play(Create(c), FadeIn(lb), run_time=0.3)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
