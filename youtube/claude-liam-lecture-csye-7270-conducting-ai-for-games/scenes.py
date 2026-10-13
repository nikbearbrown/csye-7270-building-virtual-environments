"""
kit.py — the lecture's shared drawing + pacing kit. NOT imported: assemble_scenes.py pastes it at the top of
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


# ══════════════════════════════ scenes_act1.py ══════════════════════════════
"""ACT I · The Empty Podium  (B01-B05, all Manim)

One cast for the act (ACTS.md "cast per act"):
  THE ORCHESTRA  - an isometric stage: a kraft podium (empty) and two arcs of player seats, each seat a kraft block with an instrument
                   standing on it (B03 builds it, B04 reuses the same drawing as the parts of a game, B05 keeps only the podium);
  THE BATON      - a thin ink line with ONE terracotta dot at its tip (B02 draws it, B03/B05 show where it is missing);
  THE GAME       - real frames of the real Walker Jumpman project with Clawd (EVID/godot-captures/walker-claude, Godot 4.7.2,
                   scripted input recorded 2026-10-09), stepped in time from pantry/a1_g_###.png (frames 3-70 of the 12 fps extract);
  THE RECORDED RUN - the four real tool calls of the recorded Godot run (EVID/godot-evidence/part2): Read, Edit, Write, godot --headless.
Pacing: a1_at() lands each motion on the real spoken word (faster-whisper times, evidence/act1/word_times.json).
GATE T: the real game window is a capture with dark navy ground and small HUD type; it is checked at real 4K (evidence/act1/gates_act1.py).
"""

A1P = "pantry/"
A1_KR = "#A38A60"                      # mid kraft: outline for the many SMALL objects (a lighter outline than the kit's #917A55, which GATE T counts as text ink)


def a1_at(self, t):
    """Wait until the clip clock reaches t seconds (a real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a1_lab(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a1_no(x, y, r=0.5, sw=8):
    """A prohibition mark (ink ring + bar)."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


# ───────────── the real game, stepped frame by frame from pantry/ ─────────────
A1_FR = {}


def a1_frame(i):
    if i not in A1_FR:
        from PIL import Image
        A1_FR[i] = np.array(Image.open(f"{A1P}a1_g_{i:03d}.png").convert("RGBA"))
    return A1_FR[i]


def a1_game(self, w, x, y, f0=3, f1=70, fps=12.0):
    """The Walker Jumpman capture as an ImageMobject; call a1_game_play(...) to start stepping it with the clip clock."""
    im = ImageMobject(f"{A1P}a1_g_{f0:03d}.png")
    im.set_width(w)
    im.move_to(np.array([x, y, 0.0]))
    return im


def a1_game_play(self, im, f0=3, f1=70, fps=12.0):
    st = {"i": f0, "t0": _elapsed(self)}

    def upd(m):
        i = min(f1, f0 + int(max(0.0, _elapsed(self) - st["t0"]) * fps))
        if i != st["i"]:
            st["i"] = i
            m.pixel_array = a1_frame(i)
    im.add_updater(upd)


def a1_win(w, h, x, y, color=DIM):
    """The thin grey frame around a real capture (grey, never ink: ink touching capture pixels fails GATE T)."""
    return Rectangle(width=w + 0.12, height=h + 0.12, stroke_color=color, stroke_width=4, fill_opacity=0).move_to([x, y, 0])


# ───────────── the orchestra (isometric) ─────────────
A1_ROWS = [(2.8, [-48, -24, 0, 24, 48]), (4.2, [-48, -32, -16, 0, 16, 32, 48])]
A1_SW, A1_SD, A1_SH = 0.62, 0.62, 0.30         # a seat block: width, depth, height
A1_IW = 0.17                                   # an instrument's footprint
A1_H0, A1_H1 = 0.32, 0.78                      # instrument height before / after it improves


def a1_xy(r, phi):
    a = np.radians(45 + phi)
    return r * np.cos(a), r * np.sin(a)


def a1_box(iso, x0, y0, z0, w, d, h, top, left, right, stroke=INK, sw=4):
    x1, y1, z1 = x0 + w, y0 + d, z0 + h
    return VGroup(
        iso.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, stroke=stroke, sw=sw),
        iso.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, stroke=stroke, sw=sw),
        iso.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, stroke=stroke, sw=sw))


def a1_inst_draw(g):
    """Redraws an instrument (a thin kraft block standing on its seat) at the height held by its tracker."""
    iso, x0, y0, z0, w, h = g.a1["iso"], g.a1["x0"], g.a1["y0"], g.a1["z0"], g.a1["w"], g.a1["h"].get_value()
    x1, y1, z1 = x0 + w, y0 + w, z0 + h
    faces = [[(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],
             [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],
             [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    for poly, f in zip(g, faces):
        pts = [iso.p(*q) for q in f]
        poly.set_points_as_corners(pts + [pts[0]])


def a1_orch(iso):
    """Builds the orchestra. Returns dict: floor, pod (podium), seats (back to front; each seat = VGroup(block, instrument)),
    inst (the height trackers), dots (terracotta lights on the seat tops, opacity 0), phi (each seat's angle), gate (the empty baton)."""
    floor = iso.quad([(-0.5, -0.5, 0), (5.0, -0.5, 0), (5.0, 5.0, 0), (-0.5, 5.0, 0)], "#EAE6DA", stroke="#EAE6DA", sw=0)
    pod = a1_box(iso, -0.55, -0.55, 0, 1.1, 1.1, 0.34, BOX_TOP, BOX_L, BOX_R, stroke=INK, sw=4)
    items = []
    for r, phis in A1_ROWS:
        for ph in phis:
            x, y = a1_xy(r, ph)
            items.append((x + y, x, y, ph))
    items.sort(reverse=True)                      # back (large x + y) first
    seats, inst, dots, phis = [], [], [], []
    for _, x, y, ph in items:
        blk = a1_box(iso, x - A1_SW / 2, y - A1_SD / 2, 0, A1_SW, A1_SD, A1_SH, BOX_TOP, BOX_L, BOX_R, stroke=A1_KR, sw=3)
        trk = ValueTracker(A1_H0)
        ins = VGroup(*[Polygon([0, 0, 0], [1, 0, 0], [1, 1, 0], fill_color=c, fill_opacity=1, stroke_color=A1_KR, stroke_width=3)
                       for c in (BOX_L, BOX_R, BOX_TOP)])
        ins.a1 = dict(iso=iso, x0=x - A1_IW / 2 + 0.06, y0=y - A1_IW / 2 + 0.06, z0=A1_SH, w=A1_IW, h=trk)
        a1_inst_draw(ins)
        ins.add_updater(a1_inst_draw)
        dot = Dot(iso.p(x - A1_SW / 2 + 0.16, y - A1_SD / 2 + 0.16, A1_SH), radius=0.085, color=TERRA)
        dot.set_opacity(0)
        seats.append(VGroup(blk, ins))
        inst.append(trk)
        dots.append(dot)
        phis.append(ph)
    gate = DashedVMobject(Line(iso.p(0, 0, 0.34), iso.p(0, 0, 0.34) + np.array([0.85, 1.05, 0]), stroke_width=6), num_dashes=7)
    gate.set_stroke(DIM, 6)
    return dict(floor=floor, pod=pod, seats=seats, inst=inst, dots=dots, phi=phis, gate=gate)


def a1_ellipse(iso, c=(2.55, 2.55), half_along=1.95, half_across=3.7, n=80):
    """A flat ring on the stage floor around all the players (the whole performance), as a dashed grey curve."""
    u, v = np.array([1.0, 1.0]) / np.sqrt(2), np.array([1.0, -1.0]) / np.sqrt(2)
    pts = []
    for k in range(n + 1):
        t = 2 * np.pi * k / n
        q = np.array(c) + half_along * np.cos(t) * u + half_across * np.sin(t) * v
        pts.append(iso.p(q[0], q[1], 0.0))
    ring = VMobject()
    ring.set_points_as_corners(pts)
    return DashedVMobject(ring, num_dashes=70).set_stroke(DIM, 5)


# ── B01 · the AI writes the code: a page of code writes itself, then the real recorded run, then the real game; you do not type it ──
class B01_AIWritesCode(Scene):
    def construct(self):
        title = T("The Empty Podium", 40).move_to([-6.05, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        px, py, pw, ph = -2.95, 0.3, 6.3, 3.9
        panel = RoundedRectangle(width=pw, height=ph, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0
                                 ).move_to([px, py, 0])
        a1_at(self, 0.1)
        self.play(Create(panel), run_time=0.4)
        # "the A. I. writes the code": lines of code write themselves into the page, a terracotta cursor at the end of each
        lens = [4.2, 3.0, 4.8, 2.2, 3.9, 3.4, 2.6]
        ys = [py + 1.4 - i * 0.46 for i in range(7)]
        x0 = px - 2.7
        cur = Dot([x0, ys[0], 0], radius=0.09, color=TERRA)
        self.add(cur)
        wl = VGroup()
        for y, w in zip(ys, lens):
            ln = Line([x0, y, 0], [x0 + w, y, 0], color=BAR1, stroke_width=9)
            wl.add(ln)
            self.play(Create(ln), cur.animate.move_to([x0 + w + 0.2, y, 0]), run_time=0.2, rate_func=linear)
        a1_at(self, 2.1)                                              # "Claude Code or Codex": the page becomes the tool's own window
        head = a1_lab("Claude Code", px, py + 1.6, 36)
        r_l = a1_lab("recorded run", px, py - ph / 2 - 0.45, 34)
        self.play(FadeOut(wl), FadeOut(cur), FadeIn(head), FadeIn(r_l), run_time=0.5)
        rows_y = [py + 0.8, py + 0.25, py - 0.3, py - 0.85, py - 1.4]
        X0 = px - 2.75

        def row(txt, y):
            t = M(txt, 32).move_to([X0 + 0.3, y, 0], aligned_edge=LEFT)
            d = Dot([X0, y, 0], radius=0.07, color=TERRA)
            return VGroup(d, t)
        r1, r2, r3, r4 = row("Read pong.tscn", rows_y[0]), row("Edit pong.tscn", rows_y[1]), \
            row("Write check_label.gd", rows_y[2]), row("godot --headless …", rows_y[3])
        a1_at(self, 3.62)                                             # "reads your project"
        self.play(FadeIn(r1, shift=RIGHT * 0.15), run_time=0.3)
        # (midpoint 4.25: the tool's window with its first real tool call; the game lands right after, as the project)
        gx, gy, gw = 3.35, 0.4, 5.55
        gh = gw * 9 / 16
        a1_at(self, 4.32)                                             # "your project": the real game it works on
        game = a1_game(self, gw, gx, gy)
        frame = a1_win(gw, gh, gx, gy)
        g_l = a1_lab("Walker Jumpman", gx, gy - gh / 2 - 0.5, 36)
        self.play(FadeIn(game), Create(frame), FadeIn(g_l), run_time=0.4)
        a1_game_play(self, game)
        a1_at(self, 4.72)                                             # "edits it"
        self.play(FadeIn(r2, shift=RIGHT * 0.15), FadeIn(r3, shift=RIGHT * 0.15), run_time=0.3)
        a1_at(self, 5.22)                                             # "runs it"
        self.play(FadeIn(r4, shift=RIGHT * 0.15), run_time=0.25)
        a1_at(self, 5.74)                                             # "and reports back"
        ok = check(X0 + 0.0, rows_y[4] - 0.02, s=0.2, color=INK, w=7)
        pas = M("PASS", 32).move_to([X0 + 0.55, rows_y[4], 0], aligned_edge=LEFT)
        self.play(Create(ok), FadeIn(pas), run_time=0.3)
        a1_at(self, 6.72)                                             # "You do not type the game"
        kx, ky = gx, -2.55
        kb = RoundedRectangle(width=2.9, height=0.9, corner_radius=0.14, stroke_color=DIM, stroke_width=5, fill_opacity=0
                              ).move_to([kx, ky, 0])
        keys = VGroup(*[Line([kx - 1.2, ky + dy, 0], [kx + 1.2, ky + dy, 0], color=GHOST, stroke_width=9) for dy in (0.2, -0.05)],
                      Line([kx - 0.8, ky - 0.28, 0], [kx + 0.8, ky - 0.28, 0], color=GHOST, stroke_width=9))
        self.play(FadeIn(kb), FadeIn(keys), run_time=0.3)
        no = a1_no(kx, ky, 0.52, 8)
        self.play(Create(no), run_time=0.4)
        done(self)


# ── B02 · less work, different work: the typing pile shrinks, a baton rises ─────────────────────────────────────────────────
class B02_DifferentWork(Scene):
    def construct(self):
        lx, ly = -3.5, 0.45
        page = RoundedRectangle(width=3.6, height=3.9, corner_radius=0.12, stroke_color=DIM, stroke_width=5, fill_opacity=0
                                ).move_to([lx, ly, 0])
        lens = [2.5, 1.8, 2.6, 1.4, 2.3, 1.9, 2.4, 1.6]
        lines = VGroup(*[Line([lx - 1.4, ly + 1.55 - i * 0.44, 0], [lx - 1.4 + w, ly + 1.55 - i * 0.44, 0], color=BAR1, stroke_width=10)
                         for i, w in enumerate(lens)])
        pile = VGroup(page, lines)
        t_l = a1_lab("typing", lx, -2.05, 40)
        self.play(FadeIn(pile, shift=UP * 0.15), FadeIn(t_l), run_time=0.45)
        a1_at(self, 0.58)                                             # "less work"
        self.play(pile.animate.scale(0.5, about_point=np.array([lx, ly - 1.95, 0])), run_time=0.75)
        a1_at(self, 1.6)                                              # "different work"
        arr = Arrow([-1.55, 0.0, 0], [0.9, 0.0, 0], buff=0, color=INK, stroke_width=8, tip_length=0.32)
        self.play(GrowArrow(arr), run_time=0.4)
        hx, hy = 2.2, -1.5
        tx, ty = 5.3, 1.9
        L = np.hypot(tx - hx, ty - hy)
        shaft = Line([hx, hy, 0], [tx, ty, 0], color=INK, stroke_width=11)
        grip = Line([hx, hy, 0], [hx + 0.55 * (tx - hx) / L, hy + 0.55 * (ty - hy) / L, 0], color=INK, stroke_width=26)
        tip = Dot([tx, ty, 0], radius=0.14, color=TERRA)
        c_l = a1_lab("conducting", 3.75, -2.05, 40)
        self.play(Create(shaft), FadeIn(grip), FadeIn(tip, scale=0.5), run_time=0.5)
        self.play(FadeIn(c_l), run_time=0.3)
        baton = VGroup(shaft, grip, tip)
        # (midpoint: the shrunken pile, the arrow, the baton and both labels)
        a1_at(self, 2.8)                                              # "the work this course teaches": the baton conducts
        H = np.array([hx, hy, 0.0])
        self.play(Rotate(baton, angle=0.16, about_point=H), run_time=0.4)
        self.play(Rotate(baton, angle=-0.32, about_point=H), run_time=0.55)
        self.play(Rotate(baton, angle=0.16, about_point=H), run_time=0.4)
        done(self)


# ── B03 · the orchestra with an empty podium: every player and instrument better, nobody conducting ──────────────────────────
class B03_EmptyPodium(Scene):
    def construct(self):
        iso = Iso(0.0, -2.55, 1.1)
        o = a1_orch(iso)
        a1_at(self, 0.2)                                              # "Picture an orchestra"
        self.add(o["floor"], o["pod"])
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in o["seats"]], lag_ratio=0.06), run_time=1.3)
        orch_l = a1_lab("orchestra", -4.3, 1.9, 38)
        self.play(FadeIn(orch_l), run_time=0.3)
        a1_at(self, 1.5)                                              # "every player has just got better": each seat lights up
        self.play(LaggedStart(*[d.animate.set_opacity(1) for d in o["dots"]], lag_ratio=0.07), run_time=1.2)
        a1_at(self, 3.0)                                              # "Every instrument improved": the instruments grow
        self.play(LaggedStart(*[t.animate.set_value(A1_H1) for t in o["inst"]], lag_ratio=0.06), run_time=1.1)
        a1_at(self, 4.2)                                              # "and nobody is conducting": the baton is missing
        self.play(Create(o["gate"]), run_time=0.8)
        # (midpoint 5.6: the orchestra, lit and grown, the missing baton drawn dashed over the podium)
        a1_at(self, 5.8)                                              # "Each player is brilliant": a spark visits every seat
        spark = Dot(o["dots"][0].get_center(), radius=0.1, color=TERRA).set_z_index(30)
        self.add(spark)
        order = sorted(range(len(o["dots"])), key=lambda i: (o["phi"][i], -i))
        for i in order:
            self.play(spark.animate.move_to(o["dots"][i].get_center()), run_time=0.085, rate_func=linear)
        a1_at(self, 7.3)                                              # "Nobody is holding the whole performance"
        ring = a1_ellipse(iso)
        self.play(Create(ring), run_time=1.0)
        w_l = a1_lab("whole performance", 4.1, -2.45, 36)
        self.play(FadeIn(w_l), FadeOut(spark), run_time=0.4)
        a1_at(self, 9.35)                                             # "The podium is empty"
        e_l = a1_lab("empty podium", -3.7, -2.65, 38)
        self.play(FadeIn(e_l), *[d.animate.set_opacity(0.25) for d in o["dots"]], run_time=0.6)
        self.play(o["gate"].animate.set_stroke(INK, 8), run_time=0.5)
        done(self)


# ── B04 · the same orchestra is a game: each part polished, the game wrong, because nobody held the whole thing ─────────────────
class B04_NobodyHeldIt(Scene):
    def construct(self):
        iso = Iso(-3.05, -2.3, 0.72)
        o = a1_orch(iso)
        for t in o["inst"]:
            t.set_value(A1_H1)
        for sg in o["seats"]:
            a1_inst_draw(sg[1])
            sg[1].clear_updaters()
        o["gate"].set_stroke(INK, 8)
        stage = VGroup(o["floor"], o["pod"], *o["seats"], o["gate"])
        self.add(stage)
        gp_x, gp_y = 3.6, 0.3                                         # the game: a plain drawn panel (an illustration)
        a1_at(self, 0.35)                                             # "a game built by an A. I.": the game appears beside the players
        panel = RoundedRectangle(width=3.9, height=2.6, corner_radius=0.12, stroke_color=INK, stroke_width=5, fill_color=CARD,
                                 fill_opacity=1).move_to([gp_x, gp_y, 0])
        gl1 = Line([gp_x - 1.7, gp_y - 0.75, 0], [gp_x - 0.35, gp_y - 0.75, 0], color=DIM, stroke_width=7)
        gl2 = Line([gp_x + 0.35, gp_y - 0.75, 0], [gp_x + 1.7, gp_y - 0.75, 0], color=DIM, stroke_width=7)
        gbl = Rectangle(width=0.36, height=0.36, stroke_color=A1_KR, stroke_width=4, fill_color=BOX_L, fill_opacity=1
                        ).move_to([gp_x - 1.1, gp_y - 0.52, 0])
        g_l = a1_lab("game", gp_x, gp_y - 1.8, 40)
        self.play(FadeIn(panel), Create(gl1), Create(gl2), FadeIn(gbl), FadeIn(g_l), run_time=0.6)
        left = VGroup(*[s for s, p in zip(o["seats"], o["phi"]) if p <= -20])
        right = VGroup(*[s for s, p in zip(o["seats"], o["phi"]) if p >= 20])
        mid = VGroup(*[s for s, p in zip(o["seats"], o["phi"]) if -20 < p < 20])
        a1_at(self, 1.9)                                              # "with nobody directing": the empty podium is marked
        self.play(Indicate(o["gate"], color=INK, scale_factor=1.15), run_time=0.7)
        a1_at(self, 3.05)                                             # "Each script can be fluent"
        l1 = a1_lab("script", -4.95, 1.3, 36)
        k1 = check(-4.15, 1.34, s=0.2, color=INK, w=7)
        self.play(FadeIn(l1), Create(k1), run_time=0.45)
        a1_at(self, 4.45)                                             # "each scene can look right"
        l2 = a1_lab("scene", -3.15, 1.3, 36)
        k2 = check(-2.35, 1.34, s=0.2, color=INK, w=7)
        self.play(FadeIn(l2), Create(k2), run_time=0.45)
        l3 = a1_lab("art", -1.4, 1.3, 36)
        k3 = check(-0.85, 1.34, s=0.2, color=INK, w=7)
        self.play(FadeIn(l3), Create(k3), run_time=0.4)
        # (midpoint 4.79: script, scene and art each checked; the game panel waits to the right)
        a1_at(self, 5.8)                                              # "and the game can still be wrong": an ink cross on the game
        x0, y0, s = gp_x, gp_y + 0.2, 0.62
        cross = VGroup(Line([x0 - s, y0 + s, 0], [x0 + s, y0 - s, 0], color=INK, stroke_width=14),
                       Line([x0 - s, y0 - s, 0], [x0 + s, y0 + s, 0], color=INK, stroke_width=14))
        self.play(Create(cross), run_time=0.5)
        a1_at(self, 7.35)                                             # "because nobody held the whole thing": the parts drift apart
        self.play(left.animate.shift(LEFT * 0.3), right.animate.shift(RIGHT * 0.25), mid.animate.shift(UP * 0.2),
                  run_time=0.9)
        done(self)


# ── B05 · the question: "can the AI write the code?" answered (it can); "what is left for you?" is the work ──────────────────
class B05_TheQuestion(Scene):
    def construct(self):
        wx, wy, ww = -3.0, 0.2, 5.9
        wh = ww * 9 / 16
        a1_at(self, 0.35)                                             # "the question": a page of code, as in the first beats
        page = RoundedRectangle(width=ww, height=wh, corner_radius=0.12, stroke_color=DIM, stroke_width=5, fill_opacity=0
                                ).move_to([wx, wy, 0])
        lens = [4.6, 3.2, 5.0, 2.4, 4.2, 3.7, 2.8]
        lines = VGroup(*[Line([wx - 2.6, wy + 1.2 - i * 0.4, 0], [wx - 2.6 + w, wy + 1.2 - i * 0.4, 0], color=BAR1, stroke_width=9)
                         for i, w in enumerate(lens)])
        q1 = a1_lab("write the code?", wx, wy + wh / 2 + 0.55, 40)
        self.play(FadeIn(page), FadeIn(lines), run_time=0.4)
        a1_at(self, 1.75)                                             # "can the A. I. write the code"
        self.play(FadeIn(q1), run_time=0.4)
        # (midpoint 3.74: the question over a page of code; the real answer lands right after)
        a1_at(self, 3.82)                                             # "It can." the real game it wrote
        game = ImageMobject(f"{A1P}a1_g_034.png")
        game.set_width(ww)
        game.move_to([wx, wy, 0])
        frame = a1_win(ww, wh, wx, wy)
        ok = check(wx - 0.95, wy - wh / 2 - 0.62, s=0.24, color=INK, w=8)
        yes = a1_lab("yes", wx - 0.05, wy - wh / 2 - 0.6, 40)
        self.play(FadeOut(page), FadeOut(lines), FadeIn(game), Create(frame), Create(ok), FadeIn(yes), run_time=0.45)
        a1_at(self, 4.3)                                              # "The question is what is left for you"
        iso = Iso(3.95, -1.45, 1.3)
        pod = a1_box(iso, -0.55, -0.55, 0, 1.1, 1.1, 0.34, BOX_TOP, BOX_L, BOX_R, stroke=INK, sw=4)
        gate = DashedVMobject(Line(iso.p(0, 0, 0.34), iso.p(0, 0, 0.34) + np.array([1.05, 1.4, 0]), stroke_width=7), num_dashes=7)
        gate.set_stroke(DIM, 7)
        self.play(FadeIn(pod, shift=DOWN * 0.2), Create(gate), run_time=0.6)
        q2 = a1_lab("what is left?", 3.95, 1.5, 40)
        self.play(FadeIn(q2), run_time=0.35)
        a1_at(self, 6.0)                                              # "and how to do it well"
        h_l = a1_lab("done well", 3.95, -2.7, 38)
        self.play(FadeIn(h_l), gate.animate.set_stroke(INK, 9), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · What the AI Does, What You Do  (B06-B15, all Manim)

One cast for the act:
  THE CHANNEL AND THE GATE (B06-B08): kraft crates (game parts) stream out of a grey maker block along a channel and meet a
    wall with ONE person-sized slot. The channel widens, the slot does not (the make/check asymmetry, drawn like water and a sluice).
  YOU = one Professor Bear portrait (pantry/a2_bear_*.png, 1x1 #71, the same one in every beat that needs "you").
  REAL EVIDENCE, shown as itself: a real check receipt (S/evidence/mechanics-*.json), real code and scene lines of walker-claude,
    real captures of the Claude Walker game (frames from walker-claude-jumpman-gameplay.mp4 stepped in time), the project's own
    brief and signature-slot file. Drawn pictures of an idea are labelled "example".
Pacing: a2_at() waits for the real spoken time of a word (faster-whisper times, evidence/act2/word_times.json).
GATE T notes: grey (BAR1/BAR2/DIM) for big blocks, never ink fills; terracotta only as dots; no ring around capture pixels.
"""

A2P = "pantry/"
A2_BEAR = A2P + "a2_bear_head.png"
A2_CRATE_F, A2_CRATE_T = "#DCC9AA", "#F3E9D8"


def a2_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a2_lab(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a2_img(name, h=None, w=None, at=(0.0, 0.0)):
    im = ImageMobject(A2P + name)
    if h is not None:
        im.set_height(h)
    if w is not None:
        im.set_width(w)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a2_x(x, y, s=0.17, color=INK, w=7):
    """An ink cross."""
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w))


def a2_crate(x, y, s=0.8):
    """A kraft crate (a game part): front face + a slanted top face. (x, y) = centre of the front face."""
    k = s * 0.22
    front = Square(side_length=s, fill_color=A2_CRATE_F, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    top = Polygon([x - s / 2, y + s / 2, 0], [x + s / 2, y + s / 2, 0], [x + s / 2 + k, y + s / 2 + k * 0.8, 0],
                  [x - s / 2 + k, y + s / 2 + k * 0.8, 0], fill_color=A2_CRATE_T, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(front, top)


def a2_portrait(x, y, h=1.5, ring=True):
    """Professor Bear = 'you' (the PROFESSOR BEAR LAW): the same circular portrait in every beat of the act."""
    im = ImageMobject(A2_BEAR)
    im.set_height(h)
    im.move_to([x, y, 0])
    return im


def a2_portrait_ring(x, y, h=1.5):
    return Circle(radius=h / 2, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([x, y, 0])


# ── real game footage: frames of walker-claude-jumpman-gameplay.mp4 (12 fps, 1280x720), stepped in time ─────────────────
_A2_FR = {}


def a2_frames():
    if not _A2_FR:
        import glob
        from PIL import Image as _Im
        for f in sorted(glob.glob(A2P + "a2_gp/f*.jpg")):
            _A2_FR[len(_A2_FR)] = np.array(_Im.open(f).convert("RGBA"))
    return _A2_FR


def a2_clip(h, at, start=0.0, fps=12.0):
    """The real gameplay capture as a stepped image: shows source time `start + (scene time since creation)`; holds the last frame."""
    fr = a2_frames()
    n = len(fr)
    if n == 0:                                   # (Gate A's folder holds only scenes.py: no frames there)
        im = ImageMobject(np.zeros((72, 128, 4), dtype=np.uint8))
        im.set_height(h)
        im.move_to([at[0], at[1], 0])
        return im
    im = ImageMobject(fr[min(n - 1, int(start * fps))])
    im.set_height(h)
    im.move_to([at[0], at[1], 0])
    im._a2 = dict(t=0.0, last=-1)

    def tick(m, dt):
        m._a2["t"] += dt
        i = min(n - 1, int((start + m._a2["t"]) * fps))
        if i != m._a2["last"]:
            m._a2["last"] = i
            m.pixel_array = fr[i]
    im.add_updater(tick)
    return im


def a2_window(cx, cy, w, h, color=DIM):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=5, fill_opacity=0).move_to([cx, cy, 0])


# ── the channel and the gate (B06-B08) ──────────────────────────────────────────────────────────────────────────
A2_FLOOR = -0.9            # channel floor (crate bottoms)
A2_GATE_X = 3.0            # the wall


def a2_gate(slot_top=0.1):
    """The wall with ONE person-sized slot (1.0 high) and its (unlit) lamp. Returns (wall, lamp)."""
    wx = A2_GATE_X
    low = Rectangle(width=0.34, height=0.6, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([wx, A2_FLOOR - 0.3, 0])
    up = Rectangle(width=0.34, height=1.9, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([wx, slot_top + 0.95, 0])
    lamp = Circle(radius=0.13, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([wx, slot_top + 0.4, 0])
    return VGroup(low, up), lamp


def a2_maker(h=1.9, cy=-0.2):
    """The grey maker block with its mouth facing the channel."""
    body = Rectangle(width=1.5, height=h, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-5.45, cy, 0])
    mouth = Rectangle(width=0.5, height=0.8, fill_color=STAGE, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-4.95, A2_FLOOR + 0.4, 0])
    return VGroup(body, mouth)


def a2_channel_lines(h=0.9, x0=-4.7, x1=A2_GATE_X - 0.17):
    """Floor and roof of the channel (roof at floor + h + 0.1)."""
    fl = Line([x0, A2_FLOOR, 0], [x1, A2_FLOOR, 0], color=INK, stroke_width=5)
    rf = Line([x0, A2_FLOOR + h + 0.1, 0], [x1, A2_FLOOR + h + 0.1, 0], color=INK, stroke_width=5)
    return fl, rf


# ── B06 · two jobs: making is cheap, checking is not ───────────────────────────────────────────────────────────────
class B06_TwoJobs(Scene):
    def construct(self):
        title = T("What the AI Does, What You Do", 40).move_to([-3.1, 2.95, 0])
        title.set_x(-6.2 + title.width / 2)
        maker = a2_maker()
        wall, lamp = a2_gate()
        fl, rf = a2_channel_lines()
        self.add(title, maker, wall, lamp, fl)
        # the pass tray after the gate
        tray = Line([3.55, A2_FLOOR, 0], [6.0, A2_FLOOR, 0], color=INK, stroke_width=5)
        self.add(tray)
        a2_at(self, 1.2)                                       # "making an answer"
        mk_l = a2_lab("make", -5.45, -2.05, 36)
        c1 = a2_crate(-4.95, A2_FLOOR + 0.4)
        self.play(FadeIn(mk_l), FadeIn(c1, shift=RIGHT * 0.3), run_time=0.4)
        self.play(c1.animate.shift(RIGHT * 6.9), run_time=1.0)       # rolls to the gate (x = 1.95)
        a2_at(self, 2.2)                                       # "checking an answer"
        ck_l = a2_lab("check", A2_GATE_X, -2.05, 36)
        self.play(FadeIn(ck_l), run_time=0.3)
        lit = Dot(lamp.get_center(), radius=0.13, color=TERRA)
        self.play(FadeIn(lit), run_time=0.2)
        self.play(c1.animate.shift(RIGHT * 3.35), run_time=0.9)      # slowly through the slot -> x = 5.3
        self.play(FadeOut(lit), run_time=0.15)
        tick = check(5.3, 0.45, s=0.24, color=INK, w=8)
        self.play(Create(tick), run_time=0.35)
        # (midpoint 4.35: one crate made, checked, in the tray; labels in place)
        a2_at(self, 4.55)                                      # "The A.I. made the first one cheap"
        crates = [a2_crate(-4.95, A2_FLOOR + 0.4) for _ in range(5)]
        self.add(*crates)
        dest = [1.95 - 0.88 * k for k in range(5)]
        self.play(LaggedStart(*[c.animate.shift(RIGHT * (d + 4.95)) for c, d in zip(crates, dest)], lag_ratio=0.28), run_time=1.5)
        ok = check(-5.95, -2.8, s=0.2, color=INK, w=7)
        ch_l = a2_lab("cheap", -5.0, -2.8, 36)
        self.play(Create(ok), FadeIn(ch_l), run_time=0.35)
        a2_at(self, 6.3)                                       # "It did not make the second one cheap"
        lit2 = Dot(lamp.get_center(), radius=0.13, color=TERRA)
        self.play(FadeIn(lit2), run_time=0.15)
        self.play(crates[0].animate.shift(RIGHT * 2.4), run_time=1.3)
        nx = a2_x(A2_GATE_X - 1.25, -2.8)
        nc_l = a2_lab("not cheap", A2_GATE_X + 0.35, -2.8, 36)
        self.play(Create(nx), FadeIn(nc_l), run_time=0.35)
        done(self)


# ── B07 · the channel widens, the gate stays person-sized ───────────────────────────────────────────────────────────
class B07_WiderChannel(Scene):
    def construct(self):
        maker = a2_maker()
        wall, lamp = a2_gate()
        fl, rf = a2_channel_lines()
        mk_l = a2_lab("make", -5.45, -2.05, 36)
        ck_l = a2_lab("check", A2_GATE_X, -2.05, 36)
        tray = Line([3.55, A2_FLOOR, 0], [6.0, A2_FLOOR, 0], color=INK, stroke_width=5)
        q = [a2_crate(1.95 - 0.88 * k, A2_FLOOR + 0.4) for k in range(3)]
        self.add(maker, wall, lamp, fl, tray, mk_l, ck_l, *q)
        a2_at(self, 0.3)                                       # "it gets harder, not easier"
        lit = Dot(lamp.get_center(), radius=0.13, color=TERRA)
        self.play(FadeIn(lit), run_time=0.2)
        a2_at(self, 1.7)                                       # "The faster the A.I. makes things"
        more = [a2_crate(-4.95, A2_FLOOR + 0.4) for _ in range(4)]
        self.add(*more)
        dest = [1.95 - 0.88 * (k + 3) for k in range(4)]
        self.play(LaggedStart(*[c.animate.shift(RIGHT * (d + 4.95)) for c, d in zip(more, dest)], lag_ratio=0.2), run_time=1.9)
        # the queue is now 8 deep, backed up to the maker (the midpoint frame is a still)
        a2_at(self, 4.9)                                       # "The channel for making gets wider"
        up_h = 2.7
        rf2 = Line([-4.7, A2_FLOOR + up_h + 0.1, 0], [A2_GATE_X - 0.17, A2_FLOOR + up_h + 0.1, 0], color=INK, stroke_width=5)
        w_arr = dim_arrow([-4.2, A2_FLOOR + 0.0, 0], [-4.2, A2_FLOOR + up_h + 0.1, 0], color=INK, w=5)
        wide_l = a2_lab("wider", -3.2, 1.35, 36)
        rows = VGroup(*[a2_crate(1.95 - 0.88 * k, A2_FLOOR + 0.4 + 0.9 * r) for r in (1, 2) for k in range(3)])
        self.play(Create(rf2), GrowArrow(w_arr), FadeIn(wide_l), run_time=0.7)
        self.play(FadeIn(rows, shift=RIGHT * 0.3), run_time=0.5)
        a2_at(self, 6.6)                                       # "the gate for checking stays person-sized"
        g_arr = dim_arrow([3.62, A2_FLOOR, 0], [3.62, A2_FLOOR + 1.0, 0], color=INK, w=5)
        who = a2_portrait(5.05, 1.2, 1.5)
        who_l = a2_lab("person-sized", 5.05, 0.15, 32)
        self.play(GrowArrow(g_arr), FadeIn(who, scale=0.85), run_time=0.5)
        self.play(FadeIn(who_l), run_time=0.3)
        done(self)


# ── B08 · the claim has limits: a tool measures, but a person chose the check and decides what was meant ────────────────
class B08_ClaimWithLimits(Scene):
    def construct(self):
        # an argument, not a law: the person-sized gate drawn dashed
        g1 = DashedVMobject(Rectangle(width=0.4, height=0.5).move_to([-5.6, 1.65, 0]), num_dashes=48).set_stroke(DIM, 5)
        g2 = DashedVMobject(Rectangle(width=0.4, height=0.8).move_to([-5.6, 2.85, 0]), num_dashes=64).set_stroke(DIM, 5)
        g_l = a2_lab("argument, not law", -3.35, 2.15, 36)
        a2_at(self, 1.4)                                        # "an argument with limits"
        self.play(Create(g1), Create(g2), FadeIn(g_l), run_time=0.7)
        # the real receipt pane
        pane = RoundedRectangle(width=8.95, height=3.55, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([1.85, -0.35, 0])
        cap = a2_lab("recorded receipt", 1.85, -2.55, 34)
        X0 = -2.35
        lines = [M('"id": "fixed-jump-and-no-double",', 32), M("…", 32), M('"rise_px": 56.07470703125', 32), M("…", 32), M('"status": "PASS"', 32)]
        ys = [0.95, 0.4, -0.15, -0.7, -1.25]
        for ln, y in zip(lines, ys):
            ln.move_to([X0 + ln.width / 2, y, 0])
        a2_at(self, 3.45)                                       # "A tool that runs your game and measures it"
        self.play(Create(pane), FadeIn(cap), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.25), run_time=1.4)
        a2_at(self, 5.35)                                       # "does check something"
        tick = check(5.3, -1.25, s=0.22, color=INK, w=8)
        self.play(Create(tick), run_time=0.3)
        # (midpoint 5.95: the real receipt, ticked)
        a2_at(self, 6.75)                                       # "a person chose that check"
        who = a2_portrait(-4.35, -0.2, 1.4)
        arr = Arrow([-3.55, -0.2, 0], [-2.55, 0.8, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        dot = Dot([X0 - 0.2, 0.95, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(who, scale=0.85), run_time=0.3)
        self.play(GrowArrow(arr), FadeIn(dot), run_time=0.4)
        a2_at(self, 8.3)                                        # "a person decides whether the result is what was meant"
        arr2 = Arrow([-3.55, -0.2, 0], [-2.55, -0.15, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        lead = Line([4.2, -0.15, 0], [4.5, -0.15, 0], color=DIM, stroke_width=3)
        q_l = T("meant?", 36).move_to([5.3, -0.15, 0])
        self.play(FadeOut(arr), FadeOut(dot), run_time=0.2)
        self.play(GrowArrow(arr2), Create(lead), FadeIn(q_l), run_time=0.5)
        done(self)


# ── B09 · the split: the A.I. does the typing (five real kinds of file from the Claude Walker game) ───────────────────────
class B09_TheTyping(Scene):
    def construct(self):
        a2_at(self, 2.0)                                        # "The A.I. does the typing"
        hd = T("the A.I. types", 38).move_to([-4.6, 2.9, 0])
        hd.set_x(-5.9 + hd.width / 2)
        hdot = Dot([-6.15, 2.9, 0], radius=0.09, color=TERRA)
        self.play(FadeIn(hd), FadeIn(hdot), run_time=0.3)
        YS = [1.9, 0.85, -0.2, -1.15, -2.1]
        X_ART = -2.2

        def row_label(s, y):
            t = T(s, 36).move_to([0, y, 0])
            t.set_x(-5.9 + t.width / 2)
            return t

        def mono(s, y):
            m = M(s, 32)
            m.move_to([X_ART + m.width / 2, y, 0])
            return m
        # 1 scenes: a real scene file
        a2_at(self, 3.5)                                        # "scenes"
        l1 = row_label("scenes", YS[0])
        a1 = VGroup(mono('[node name="ClawdGallery" …]', YS[0] + 0.25), mono('script = ExtResource("1")', YS[0] - 0.25))
        self.play(FadeIn(l1), FadeIn(a1, shift=RIGHT * 0.2), run_time=0.3)
        # 2 scripts: real GDScript
        a2_at(self, 4.15)                                       # "scripts"
        l2 = row_label("scripts", YS[1])
        a2 = VGroup(mono("extends CharacterBody2D", YS[1] + 0.25), mono("var tuning = Tuning.new()", YS[1] - 0.25))
        self.play(FadeIn(l2), FadeIn(a2, shift=RIGHT * 0.2), run_time=0.3)
        # (midpoint 4.48: scene and script rows in place)
        a2_at(self, 4.62)                                       # "placeholder art"
        l3 = row_label("placeholder art", YS[2])
        a3 = a2_img("a2_clawd_idle.png", h=0.9, at=(X_ART + 0.7, YS[2]))
        self.play(FadeIn(l3), FadeIn(a3, scale=0.9), run_time=0.3)
        # 4 repeated variants: real gallery frames
        a2_at(self, 5.55)                                       # "repeated variants"
        l4 = row_label("repeated variants", YS[3])
        a4 = Group(*[a2_img(f"a2_clawd_{n}.png", h=0.9, at=(X_ART + 0.7 + 1.5 * i, YS[3])) for i, n in enumerate(("bounce", "wave", "run"))])
        self.play(FadeIn(l4), LaggedStart(*[FadeIn(im, scale=0.9) for im in a4], lag_ratio=0.3), run_time=0.9)
        # 5 tests: a real receipt line
        a2_at(self, 6.5)                                        # "tests"
        l5 = row_label("tests", YS[4])
        a5 = VGroup(mono('"failures": 0', YS[4] + 0.25), mono('"status": "PASS"', YS[4] - 0.25))
        self.play(FadeIn(l5), FadeIn(a5, shift=RIGHT * 0.2), run_time=0.3)
        a2_at(self, 7.4)                                        # "from a clear description"
        src = a2_lab("real files, Claude Walker game", 3.2, -3.0, 32)
        self.play(FadeIn(src), run_time=0.4)
        done(self)


# ── B10 · you decide what the game is for and who for; the A.I. builds any version flawlessly, the wrong one too ────────────
class B10_YouDecide(Scene):
    def construct(self):
        a2_at(self, 0.9)                                        # "You decide what the game is for"
        who = a2_portrait(-5.3, 2.2, 1.5)
        pg = RoundedRectangle(width=9.9, height=2.75, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0.95, 1.85, 0])
        hd = M("GAME-BRIEF.md", 32)
        hd.move_to([-3.8 + hd.width / 2, 2.95, 0])

        def tl(s, y):
            t = T(s, 34)
            t.move_to([-3.8 + t.width / 2, y, 0])
            return t
        q1 = VGroup(tl("Clawd, a coding agent, goes through an", 2.4), tl("agentic loop on every level: …", 1.95))
        self.play(FadeIn(who, scale=0.85), Create(pg), FadeIn(hd), run_time=0.5)
        self.play(FadeIn(q1, shift=RIGHT * 0.2), run_time=0.4)
        a2_at(self, 2.3)                                        # "and who it is for"
        q2 = VGroup(tl("keyboard players who know what", 1.35), tl("a coding agent is, …", 0.9))
        self.play(FadeIn(q2, shift=RIGHT * 0.2), run_time=0.4)
        # (midpoint 4.27: the brief's two real lines, you at the left; rows start landing after)
        a2_at(self, 3.7)                                        # "an A.I. will build any version you hand it"
        rows = VGroup()
        labs = ["(a) undo most recent task, station re-reachable", "(b) undo becomes a 2 s freeze", "(c) malware is a plain hazard, no undo"]
        ys = [-0.4, -1.25, -2.1]
        checks = []
        for lab, y in zip(labs, ys):
            r = RoundedRectangle(width=10.5, height=0.8, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0.95, y, 0])
            t = T(lab, 34)
            t.move_to([-4.1 + t.width / 2, y, 0])
            rows.add(VGroup(r, t))
        self.play(FadeIn(rows[0], shift=UP * 0.2), run_time=0.35)
        a2_at(self, 4.5)
        self.play(FadeIn(rows[1], shift=UP * 0.2), run_time=0.3)
        a2_at(self, 5.0)
        self.play(FadeIn(rows[2], shift=UP * 0.2), run_time=0.3)
        a2_at(self, 5.95)                                       # "flawlessly": each version builds, each is checked off
        cks = [check(5.6, y, s=0.2, color=INK, w=7) for y in ys]
        self.play(LaggedStart(*[Create(c) for c in cks], lag_ratio=0.35), run_time=0.9)
        a2_at(self, 7.1)                                        # "including the wrong one"
        q = a2_lab("which is wrong?", 0.95, -3.0, 34)
        dot = Dot([-5.0, ys[0], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(q), FadeIn(dot), run_time=0.3)
        self.play(dot.animate.move_to([-5.0, ys[1], 0]), run_time=0.3)
        self.play(dot.animate.move_to([-5.0, ys[2], 0]), run_time=0.3)
        done(self)


# ── B11 · you hear that something is wrong before any check says so: three drawn examples ──────────────────────────────────
def a2_clawd_sprite(x, y, h=0.55):
    """A drawn player (grey body, ink outline): a stand-in for the game's hero, so a drawn example never wears the real art."""
    w = h * 1.0
    body = Rectangle(width=w * 0.7, height=h * 0.6, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h * 0.1, 0])
    arms = Rectangle(width=w, height=h * 0.2, fill_color=BAR2, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y + h * 0.05, 0])
    legs = VGroup(*[Line([x + dx, y - h * 0.2, 0], [x + dx, y - h * 0.5, 0], color=INK, stroke_width=6) for dx in (-0.2 * w, -0.07 * w, 0.07 * w, 0.2 * w)])
    return VGroup(arms, body, legs)


class B11_HearWrong(Scene):
    def construct(self):
        a2_at(self, 0.2)                                        # "You hear that something is wrong"
        who = a2_portrait(-5.45, 2.45, 1.3)
        arcs = [Arc(radius=r, start_angle=-PI / 4, angle=PI / 2, color=DIM, stroke_width=5, arc_center=[-4.6, 2.45, 0]) for r in (0.4, 0.8, 1.2)]
        self.play(FadeIn(who, scale=0.85), run_time=0.3)
        for a in arcs:
            self.play(Create(a), run_time=0.22)
        a2_at(self, 1.5)                                        # "before any check says so": the check lamp stays unlit
        lamp = Circle(radius=0.24, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([-1.9, 2.45, 0])
        lamp_l = a2_lab("check: not yet", 0.2, 2.45, 34)
        self.play(Create(lamp), FadeIn(lamp_l), run_time=0.4)
        # panels
        PW, PH, PY = 3.8, 3.2, -0.45
        cx = [-4.2, 0.0, 4.2]
        pans = [Rectangle(width=PW, height=PH, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, PY, 0]) for x in cx]
        ex_l = a2_lab("drawn examples", 0.0, -2.85, 32)
        # 1 · a jump that cannot clear the gap
        a2_at(self, 2.75)                                       # "a jump that cannot clear the gap"
        gx = cx[0]
        ground_l = Line([gx - 1.8, -1.0, 0], [gx - 0.55, -1.0, 0], color=INK, stroke_width=6)
        ground_r = Line([gx + 0.95, -1.0, 0], [gx + 1.8, -1.0, 0], color=INK, stroke_width=6)
        clawd = a2_clawd_sprite(gx - 1.2, -0.65, 0.55)
        self.play(Create(pans[0]), Create(ground_l), Create(ground_r), FadeIn(clawd), FadeIn(ex_l), run_time=0.5)
        arc = ArcBetweenPoints(np.array([gx - 0.95, -0.5, 0.0]), np.array([gx + 0.05, -1.15, 0.0]), angle=-PI / 1.9)
        arc.set_stroke(INK, 5)
        self.play(Create(arc), run_time=0.7)
        land = Dot([gx + 0.05, -1.15, 0], radius=0.11, color=TERRA)
        cap1 = a2_lab("gap too wide", gx, -1.7, 34)
        self.play(FadeIn(land), FadeIn(cap1), run_time=0.3)
        # (midpoint 4.3: the short jump, its landing in the gap, the caption)
        # 2 · an enemy that cannot be dodged
        a2_at(self, 4.75)                                       # "an enemy that cannot be dodged"
        ex = cx[1]
        floor = Line([ex - 1.8, -1.0, 0], [ex + 1.8, -1.0, 0], color=INK, stroke_width=6)
        roof = Line([ex - 1.8, 0.75, 0], [ex + 1.8, 0.75, 0], color=INK, stroke_width=6)
        clawd2 = a2_clawd_sprite(ex - 1.2, -0.65, 0.55)
        self.play(Create(pans[1]), Create(floor), Create(roof), FadeIn(clawd2), run_time=0.4)
        spikes = VGroup(*[Polygon([ex + 0.5, y, 0], [ex + 0.5, y + 0.35, 0], [ex + 0.05, y + 0.175, 0], fill_color=BAR2, fill_opacity=1,
                                  stroke_color=INK, stroke_width=4) for y in (-1.0, -0.65, -0.3, 0.05, 0.4)])
        self.play(LaggedStart(*[GrowFromCenter(sp) for sp in spikes], lag_ratio=0.15), run_time=0.7)
        cap2 = a2_lab("no way past", ex, -1.7, 34)
        self.play(FadeIn(cap2), run_time=0.25)
        # 3 · a number that is too perfect
        a2_at(self, 6.4)                                        # "a number that is too perfect"
        nx = cx[2]
        self.play(Create(pans[2]), run_time=0.3)
        big = T("100%", 90).move_to([nx, -0.15, 0])
        cap3 = a2_lab("too perfect", nx, -1.7, 34)
        self.play(FadeIn(big, scale=0.9), run_time=0.4)
        self.play(FadeIn(cap3), run_time=0.25)
        done(self)


# ── B12 · you choose the checks, and you look at the real running game, not the report ────────────────────────────────────
class B12_RealGame(Scene):
    def construct(self):
        who = a2_portrait(-5.3, 0.6, 1.5)
        ids = ["launch-grounded", "speed-cap", "coyote-5", "respawn"]
        rows = VGroup(*[M(s, 32) for s in ids])
        for i, r in enumerate(rows):
            r.move_to([-3.4 + r.width / 2, 1.5 - 0.75 * i, 0])
        self.add(who)
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=0.7)
        a2_at(self, 0.75)                                       # "which checks matter"
        t1 = check(-3.7, 0.0, s=0.18, color=INK, w=7)
        t2 = check(-3.7, -0.75, s=0.18, color=INK, w=7)
        self.play(Create(t1), Create(t2), run_time=0.4)
        # (midpoint 2.57: the chosen checks, you; the real game lands just after, so no real pixels are in the GATE T frame)
        a2_at(self, 2.65)                                       # "the real running game"
        win = a2_window(0.7, 0.2, 6.5, 3.66)
        clip = a2_clip(3.66, (0.7, 0.2), start=0.5)
        self.play(FadeOut(rows), FadeOut(t1), FadeOut(t2), FadeIn(clip), Create(win), run_time=0.3)
        real_l = a2_lab("real running game", 0.7, -2.15, 34)
        look = Arrow([-4.45, 0.5, 0], [-2.9, 0.3, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        self.play(GrowArrow(look), FadeIn(real_l), run_time=0.3)
        a2_at(self, 3.55)                                       # "not the report about it"
        pg = RoundedRectangle(width=1.5, height=2.3, corner_radius=0.08, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([5.45, 0.3, 0])
        pl = VGroup(*[Line([4.9, y, 0], [6.0, y, 0], color=GHOST, stroke_width=7) for y in (0.9, 0.5, 0.1, -0.3)])
        rp_l = a2_lab("report", 5.45, -1.2, 34)
        cross = a2_x(5.45, 1.8, s=0.22, w=8)
        self.play(Create(pg), FadeIn(pl), FadeIn(rp_l), Create(cross), run_time=0.5)
        done(self)


# ── B13 · you judge fun, fairness and meaning: the real game plays, the questions stay open ───────────────────────────────
class B13_TasteIsYours(Scene):
    def construct(self):
        qs = ["fun?", "fair?", "what I meant?"]
        ys = [1.9, 1.05, 0.2]
        who = a2_portrait(-3.95, -1.75, 1.7)
        rings = [DashedVMobject(Circle(radius=0.2).move_to([-5.6, y, 0]), num_dashes=12).set_stroke(DIM, 5) for y in ys]
        words = []
        for s_, y in zip(qs, ys):
            t = T(s_, 40)
            t.move_to([-5.1 + t.width / 2, y, 0])
            words.append(t)
        a2_at(self, 0.75)                                       # "fun"
        self.play(Create(rings[0]), FadeIn(words[0]), run_time=0.3)
        a2_at(self, 1.75)                                       # "fair"
        self.play(Create(rings[1]), FadeIn(words[1]), run_time=0.3)
        a2_at(self, 2.55)                                       # "means what you intended"
        self.play(Create(rings[2]), FadeIn(words[2]), FadeIn(who, scale=0.85), run_time=0.4)
        # (midpoint 3.33: three open questions and you; the real game lands just after, so no real pixels are in the GATE T frame)
        a2_at(self, 3.45)
        win = a2_window(2.3, 0.45, 6.5, 3.66)
        clip = a2_clip(3.66, (2.3, 0.45), start=3.6)
        self.play(FadeIn(clip), Create(win), run_time=0.3)
        a2_at(self, 4.35)                                       # "Taste and intent are yours"
        ar = Arrow([-5.2, -0.5, 0], [-4.45, -1.2, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        mine = a2_lab("yours", -2.3, -1.75, 40)
        self.play(GrowArrow(ar), FadeIn(mine), run_time=0.4)
        dot = Dot([-5.6, ys[0], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(dot), run_time=0.2)
        self.play(dot.animate.move_to([-5.6, ys[1], 0]), run_time=0.25)
        self.play(dot.animate.move_to([-5.6, ys[2], 0]), run_time=0.25)
        done(self)


# ── B14 · you sign what ships; the A.I. faces no consequence (real status file: every signature slot is empty) ───────────
class B14_YouSign(Scene):
    def construct(self):
        a2_at(self, 0.05)                                       # "And you sign what ships"
        pg = RoundedRectangle(width=9.0, height=3.5, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-1.55, 0.45, 0])
        hd = M("DESIGN-STATUS.json", 32)
        hd.move_to([-5.8 + hd.width / 2, 1.85, 0])
        src = ['"vision":  {"signed_by": null, …}', '"systems": {"signed_by": null, …}', '"world":   {"signed_by": null, …}', '"scope":   {"signed_by": null, …}']
        rows = VGroup(*[M(t, 32) for t in src])
        ys = [1.1, 0.5, -0.1, -0.7]
        for r, y in zip(rows, ys):
            r.move_to([-5.8 + r.width / 2, y, 0])
        self.play(Create(pg), FadeIn(hd), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=0.9)
        note = T("“… Gates are signed by humans only.”", 34).move_to([-1.55, -2.0, 0])
        a2_at(self, 1.2)                                        # "The A.I. faces no consequence"
        dot = Dot([-6.15, ys[0], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(dot), FadeIn(note), run_time=0.3)
        for y in ys[1:]:
            self.play(dot.animate.move_to([-6.15, y, 0]), run_time=0.35)
        # (the slots stay empty: nobody has signed)
        a2_at(self, 3.0)                                        # "You do"
        who = a2_portrait(4.75, 1.6, 1.5)
        line = Line([3.4, -0.5, 0], [6.1, -0.5, 0], color=INK, stroke_width=5)
        sig = ParametricFunction(lambda t: np.array([3.55 + 2.4 * t, 0.0 + 0.22 * np.sin(9 * t) * (1 - 0.4 * t) + 0.08 * np.sin(23 * t), 0]),
                                 t_range=[0.0, 1.0], color=INK, stroke_width=6)
        sg_l = a2_lab("sign", 4.75, -1.05, 36)
        self.play(FadeIn(who, scale=0.85), Create(line), FadeIn(sg_l), run_time=0.35)
        self.play(Create(sig), run_time=0.6)
        done(self)


# ── B15 · an honest note: medicine, law and software come from teaching people to supervise AI; games are our own extension ──
def a2_icon(name, x, y, h=1.3):
    ic = SVGMobject(A2P + f"a2_icon_{name}.svg")
    ic.set_stroke(INK, width=6).set_fill(opacity=0)
    ic.set_height(h)
    ic.move_to([x, y, 0])
    return ic


class B15_HonestNote(Scene):
    def construct(self):
        a2_at(self, 0.1)                                        # "One honest note"
        note = T("one honest note", 40)
        note.move_to([-5.9 + note.width / 2, 3.0, 0])
        card = RoundedRectangle(width=12.0, height=3.5, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0, 0.85, 0])
        self.play(FadeIn(note), Create(card), run_time=0.5)
        xs = [-4.1, -1.35, 1.4]
        names = [("stethoscope", "medicine"), ("gavel", "law"), ("terminal", "software")]
        icons, labs = [], []
        for (ic, lab), x, t in zip(names, xs, (3.9, 4.75, 5.15)):
            a2_at(self, t - 0.2 if t > 4 else t)                # medicine, law, software
            i = a2_icon(ic, x, 1.35, 1.2)
            l = a2_lab(lab, x, 0.25, 36)
            self.play(FadeIn(i, scale=0.8), FadeIn(l), run_time=0.3)
            icons.append(i)
        # (midpoint 5.73: three icons, three words)
        a2_at(self, 6.35)                                       # "Games are where this course applies them"
        g = a2_icon("gamepad-2", 4.15, 1.35, 1.2)
        g_l = a2_lab("games", 4.15, 0.25, 36)
        fence = DashedVMobject(RoundedRectangle(width=2.3, height=2.4, corner_radius=0.2).move_to([4.15, 0.85, 0]), num_dashes=40).set_stroke(DIM, 5)
        self.play(FadeIn(g, scale=0.8), FadeIn(g_l), Create(fence), run_time=0.5)
        a2_at(self, 8.8)                                        # "That application is ours"
        ours = a2_lab("ours", 4.15, -1.7, 38)
        od = Dot([3.45, -1.7, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(ours), FadeIn(od), run_time=0.3)
        a2_at(self, 9.8)                                        # "you will be testing it"
        who = a2_portrait(-1.2, -2.15, 1.2)
        arr = Arrow([-0.45, -2.0, 0], [3.0, -1.72, 0], buff=0, color=DIM, stroke_width=5, tip_length=0.2)
        t_l = a2_lab("to be tested", 1.45, -2.85, 34)
        self.play(FadeIn(who, scale=0.85), GrowArrow(arr), FadeIn(t_l), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · A Real Record  (B16–B22, all Manim)  — "Conducting AI for Games"

One cast for the act: THE GAME WINDOW (a real Godot capture in a thin grey frame, the cream stage around it) and THE RECORD (the
project's own words and receipt names, set as text). Nothing is redrawn: the pictures of the game are the walker-jumpman starter's own
rendered screenshots (pantry/a3_starter_*.png) and Godot 4.7.2 captures of Clawd in the same level (pantry/a3_clawd_jump.png,
pantry/a3_edgeb_*.png, built by evidence/act3/make_assets_act3.py). The drawings (the 25 checks, the gate, the three predictions, the
changed / left-alone ledger) show an IDEA and carry only names and numbers that are in the record (factcheck/act3.md).

GATE T notes (measured at real 4K, evidence/act3/gates_act3.py): dark game art (the navy ground strip, dark blocks) and the flat
terracotta-ish mascot read as "text" to GATE T, so every real capture is cropped to the part the sentence names, kept small enough
not to fuse with text, and the 50% frame is always a settled still.
"""

A3P = "pantry/"


def a3_at(self, t):
    """Wait until the clip clock reaches t seconds (a real spoken time, from evidence/act3/word_times.json, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a3_t(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a3_m(s, x, y, size=32, color=INK):
    """Menlo text with its LEFT edge at x (explicit coordinates, no get_left)."""
    return M(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a3_img(name, w, x, y):
    im = ImageMobject(A3P + name)
    im.set_width(w)
    im.move_to([x, y, 0])
    return im


def a3_frame(w, h, x, y, color=DIM, sw=4):
    """A thin outline just outside a captured picture (never touching its pixels)."""
    return Rectangle(width=w + 0.2, height=h + 0.2, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([x, y, 0])


def a3_card(w, h, x, y, color=DIM, sw=4):
    return RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color, stroke_width=sw,
                            fill_opacity=0).move_to([x, y, 0])


def a3_x(x, y, s=0.12, color=INK, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a3_equal(x, y, s=0.16, color=INK, w=6):
    return VGroup(Line([x - s, y + 0.07, 0], [x + s, y + 0.07, 0], color=color, stroke_width=w),
                  Line([x - s, y - 0.07, 0], [x + s, y - 0.07, 0], color=color, stroke_width=w))


# ───────────────────────── B16 · the request ─────────────────────────
class B16_OneRequest(Scene):
    def construct(self):
        title = a3_t("A Real Record", -4.55, 3.0, 40)          # the act title is the first picture's label
        self.add(title)
        win = a3_img("a3_starter_jump_full.png", 6.9, -2.65, -0.3)
        fr = a3_frame(6.9, 3.88, -2.65, -0.3)
        game_lab = a3_t("Walker Jumpman", -2.65, -2.85, 34)
        card = a3_card(4.3, 2.3, 4.05, 0.2)
        cap = a3_t("the one request", 4.05, 1.85, 34)
        q = VGroup(a3_t("Build a simple level", 4.05, 0.6, 36), a3_t("for walker-jumpman.", 4.05, -0.1, 36))
        date = a3_t("September 10, 2026", 4.05, -1.3, 32)
        arrow = Arrow([1.75, 0.2, 0], [1.0, 0.2, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        a3_at(self, 2.0)                                        # "a small platformer"
        self.play(Create(fr), FadeIn(win), run_time=0.7)
        a3_at(self, 3.25)                                       # "called Walker Jumpman"
        self.play(FadeIn(game_lab), run_time=0.4)
        a3_at(self, 6.3)                                        # "from one request"
        self.play(Create(card), FadeIn(cap), run_time=0.5)
        a3_at(self, 6.9)                                        # "build a simple level"
        self.play(Write(q, run_time=1.2))
        self.play(Create(arrow), run_time=0.4)
        self.play(FadeIn(date), run_time=0.4)
        done(self)


# ───────────────────────── B17 · 25 checks, 4 failed, 25 passed ─────────────────────────
A3_FAILED = [(18, "respawn"), (19, "manual-restart-not-death"), (20, "twenty-retries"), (23, "complete-real-route")]


def a3_pos(cx, cy, i, pitch=0.5):
    return [cx + (i % 5 - 2) * pitch, cy - (i // 5 - 2) * pitch]


def a3_grid(cx, cy, pitch=0.5, cell=0.4):
    return VGroup(*[Square(side_length=cell, stroke_color=DIM, stroke_width=3)
                    .move_to([cx + (c - 2) * pitch, cy - (r - 2) * pitch, 0]) for r in range(5) for c in range(5)])


class B17_TwentyFiveChecks(Scene):
    def construct(self):
        g1x, g2x, gy = -4.85, 4.85, -0.35
        g1, g2 = a3_grid(g1x, gy), a3_grid(g2x, gy)
        cap1, cap2 = a3_t("first run", g1x, 1.4, 36), a3_t("next run", g2x, 1.4, 36)
        res1, res2 = a3_t("4 failed", g1x, -2.15, 40), a3_t("25 passed", g2x, -2.15, 40)
        fails = [i for i, _ in A3_FAILED]

        def mark_pass(cx, skip=()):
            return VGroup(*[check(a3_pos(cx, gy, i)[0], a3_pos(cx, gy, i)[1] - 0.02, s=0.11, color=DIM, w=5)
                            for i in range(25) if i not in skip])

        a3_at(self, 0.1)                                        # "Its first run of 25 checks"
        self.play(FadeIn(cap1), Create(g1, lag_ratio=0.04), run_time=1.0)
        a3_at(self, 1.5)
        p1 = mark_pass(g1x, fails)
        self.play(Create(p1, lag_ratio=0.03), run_time=0.7)
        xs = VGroup(*[a3_x(a3_pos(g1x, gy, i)[0], a3_pos(g1x, gy, i)[1]) for i in fails])
        a3_at(self, 2.2)                                        # "failed four"
        self.play(Create(xs), FadeIn(res1), run_time=0.5)
        # the four failing cells step out into a list of their real receipt names
        rows = [0.7, 0.05, -0.6, -1.25]
        chips, names = [], []
        for k, (i, nm) in enumerate(A3_FAILED):
            chip = VGroup(Square(side_length=0.34, stroke_color=INK, stroke_width=4).move_to([-3.2, rows[k], 0]),
                          a3_x(-3.2, rows[k], s=0.1, w=6))
            chips.append(chip)
            names.append(a3_m(nm, -2.75, rows[k]))
        a3_at(self, 3.1)                                        # "Dead on respawn"
        self.play(FadeIn(chips[0]), Write(names[0]), run_time=0.6)
        a3_at(self, 4.35)                                       # "Restart counted as a death"
        self.play(FadeIn(chips[1]), Write(names[1]), FadeIn(chips[2]), Write(names[2]), run_time=0.7)
        a3_at(self, 5.95)                                       # "A route with no safe landing"
        self.play(FadeIn(chips[3]), Write(names[3]), run_time=0.7)
        a3_at(self, 8.9)                                        # "the next run passed all twenty-five"
        self.play(FadeIn(cap2), Create(g2, lag_ratio=0.04), run_time=0.9)
        p2 = mark_pass(g2x)
        a3_at(self, 9.9)
        self.play(Create(p2, lag_ratio=0.03), FadeIn(res2), run_time=0.8)
        a3_at(self, 10.95)                                      # "seventy-one seconds later"
        dim = dim_arrow([g1x, 2.25, 0], [g2x, 2.25, 0], color=INK, w=5)
        lab = a3_t("71 s", 0.0, 2.75, 44)
        self.play(Create(dim), FadeIn(lab), run_time=0.8)
        done(self)


# ───────────────────────── B18 · the test stayed hard ─────────────────────────
class B18_TestStayedHard(Scene):
    def construct(self):
        page = a3_card(9.4, 2.0, 0.0, 2.0)
        line1 = a3_t("The jump tuning and acceptance tolerances", 0.0, 2.35, 38)
        line2 = a3_t("were not weakened.", 0.0, 1.65, 38)
        src = a3_m("BUILD-REPORT.md", -4.7, 0.65)
        # the gate: a fixed bar and two posts; the game is a box that has to clear it
        bar = Line([-3.8, -1.5, 0], [3.8, -1.5, 0], color=DIM, stroke_width=14)
        posts = VGroup(Line([-3.8, -2.15, 0], [-3.8, -0.85, 0], color=DIM, stroke_width=9),
                       Line([3.8, -2.15, 0], [3.8, -0.85, 0], color=DIM, stroke_width=9))
        test_lab = a3_t("the test", 5.3, -1.5, 38)
        box = Rectangle(width=1.7, height=1.0, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0, -2.75, 0])
        game_lab = a3_t("the game", -2.7, -2.75, 38)
        game_lab2 = a3_t("the game", -2.7, -0.4, 38)
        a3_at(self, 0.2)                                        # "Look at how the record says it did it"
        self.play(Create(bar), Create(posts), FadeIn(test_lab), run_time=0.7)
        self.play(FadeIn(box), FadeIn(game_lab), run_time=0.5)
        a3_at(self, 1.85)                                       # "The jump tuning and acceptance tolerances were not weakened"
        self.play(Create(page), run_time=0.5)
        self.play(Write(VGroup(line1, line2)), FadeIn(src), run_time=1.5)
        a3_at(self, 5.1)                                        # "The test stayed hard"
        self.play(bar.animate.set_color(INK), run_time=0.5)
        a3_at(self, 6.4)                                        # "the game changed"
        self.play(box.animate.move_to([0, -0.4, 0]), FadeOut(game_lab), run_time=0.9)
        tick = check(1.6, -0.45, s=0.22, color=INK, w=9)
        self.play(Create(tick), FadeIn(game_lab2), run_time=0.5)
        done(self)


# ───────────────────────── B19 · one change: Clawd ─────────────────────────
class B19_OneChange(Scene):
    def construct(self):
        w, h = 5.7, 2.27
        a_img = a3_img("a3_starter_jump.png", w, -3.15, 1.2)
        a_fr = a3_frame(w, h, -3.15, 1.2)
        b_img = a3_img("a3_clawd_jump.png", w, 3.15, 1.2)
        b_fr = a3_frame(w, h, 3.15, 1.2)
        a_lab = a3_t("Walker Jumpman", -3.15, -0.45, 36)
        b_lab = a3_t("Clawd", 3.15, -0.45, 36)
        arrow = Arrow([-1.2, -0.45, 0], [2.0, -0.45, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        q1 = a3_t("“… the player to be a coding agent, represented by Clawd.”", 0.0, -1.55, 38)
        q2 = a3_t("“Clawd first, one change at a time”", 0.0, -1.55, 38)
        src = a3_m("CHANGE-BRIEF.md", -1.9, -2.5)
        self.add(a_fr, a_img, a_lab)
        a3_at(self, 1.9)                                        # "wanted the player to be a coding agent"
        self.play(FadeIn(q1), FadeIn(src), run_time=0.5)
        a3_at(self, 4.3)                                        # "the Claude mascot": Clawd lands after the 50% frame (GATE T trap)
        self.play(Create(b_fr), FadeIn(b_img), FadeIn(b_lab), run_time=0.6)
        self.play(Create(arrow), run_time=0.3)
        a3_at(self, 5.85)                                       # "One change."
        self.play(FadeOut(q1), run_time=0.3)
        self.play(FadeIn(q2), run_time=0.5)
        done(self)


# ───────────────────────── B20 · three predictions, three cards ─────────────────────────
A3_CX = [-4.2, 0.0, 4.2]


def a3_pred_card(x):
    return a3_card(3.8, 4.5, x, -0.35)


def a3_art_rects(ox, oy, u, color=DIM, sw=4):
    """Clawd's real rects (torso 96x60, arms 20x20 at -20/96, legs 11x26 at 11/32/64/85), outline only, feet at oy, centre ox."""
    R = [(0, 0, 96, 60), (-20, 20, 20, 20), (96, 20, 20, 20), (11, 60, 11, 26), (32, 60, 11, 26), (64, 60, 11, 26), (85, 60, 11, 26)]
    return VGroup(*[Rectangle(width=w * u, height=h * u, stroke_color=color, stroke_width=sw, fill_opacity=0)
                    .move_to([ox + (x + w / 2 - 48) * u, oy + (86 - y - h / 2) * u, 0]) for x, y, w, h in R])


class B20_ThreePredictions(Scene):
    def construct(self):
        head = a3_t("Predict", -5.3, 2.95, 40)
        src = a3_m("CHANGE-BRIEF.md", 2.3, 2.95)
        self.add(head, src)
        c1, c2, c3 = [a3_pred_card(x) for x in A3_CX]
        n1, n2, n3 = [a3_t(s, x - 1.45, 1.6, 40) for s, x in zip("123", A3_CX)]
        l1 = a3_t("overhangs the box", A3_CX[0], -2.0, 34)
        l2 = a3_t("two jump arcs", A3_CX[1], -2.0, 34)
        l3 = a3_t("mistaken for abilities", A3_CX[2], -2.0, 32)
        # 1: the art (136 units wide) against the unchanged 18 x 28 collider (the game's pixels; the art is drawn at 0.32 of its units)
        u = 0.021
        feet = -1.35
        art = a3_art_rects(A3_CX[0], feet, u)
        collider = Rectangle(width=56.25 * u, height=87.5 * u, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to(
            [A3_CX[0], feet + 87.5 * u / 2, 0])
        # 2: two arcs stacked on one jump
        ground = Line([A3_CX[1] - 1.5, feet, 0], [A3_CX[1] + 1.5, feet, 0], color=DIM, stroke_width=6)
        arc1 = ArcBetweenPoints([A3_CX[1] - 1.4, feet, 0], [A3_CX[1] + 1.4, feet, 0], angle=-PI * 0.55, color=DIM, stroke_width=8)
        arc2 = ArcBetweenPoints([A3_CX[1] - 0.9, feet + 0.62, 0], [A3_CX[1] + 0.9, feet + 0.62, 0], angle=-PI * 0.7, color=INK, stroke_width=8)
        # 3: eighteen small squares, 3 rows x 6
        sq = VGroup(*[Square(side_length=0.42, stroke_color=DIM, stroke_width=4).move_to(
            [A3_CX[2] + (c - 2.5) * 0.56, 0.35 - r * 0.62, 0]) for r in range(3) for c in range(6)])
        a3_at(self, 2.0)                                        # "three ways it could go wrong"
        self.play(Create(c1), FadeIn(n1), run_time=0.4)
        self.play(Create(c2), FadeIn(n2), run_time=0.4)
        self.play(Create(c3), FadeIn(n3), run_time=0.4)
        a3_at(self, 3.7)                                       # "The wide body might overhang the collision box"
        self.play(Create(art), Create(collider), run_time=0.9)
        a3_at(self, 4.9)
        self.play(FadeIn(l1), run_time=0.4)
        a3_at(self, 6.35)                                        # "A jump animation on a jumping body"
        self.play(Create(ground), Create(arc1), run_time=0.6)
        a3_at(self, 8.55)                                        # "might make two jump arcs"
        self.play(Create(arc2), FadeIn(l2), run_time=0.6)
        a3_at(self, 9.85)                                       # "And eighteen animations"
        self.play(Create(sq, lag_ratio=0.06), run_time=1.0)
        a3_at(self, 11.2)                                      # "mistaken for eighteen abilities"
        self.play(FadeIn(l3), run_time=0.5)
        done(self)


# ───────────────────────── B21 · drawing changed, the rest left alone, 1,944 compared ─────────────────────────
class B21_DrawingOnly(Scene):
    def construct(self):
        h_a, h_b = a3_t("changed", -4.9, 2.7, 40), a3_t("left alone", 0.35, 2.7, 40)
        r_a = [a3_m("clawd_art.gd", -6.1, 1.7, 36), a3_m("player.gd", -6.1, 0.9, 36)]
        r_b = [a3_m("_physics_process()", -1.5, 1.7, 36), a3_m("tuning.gd", -1.5, 0.9, 36), a3_m("first_steps.json", -1.5, 0.1, 36)]
        divider = Line([-2.2, 3.1, 0], [-2.2, -0.3, 0], color=DIM, stroke_width=5)
        hero = a3_t("1,944", -3.5, -1.85, 100)
        lab = VGroup(a3_t("numbers compared with", 2.6, -1.55, 38), a3_t("an independent reference", 2.6, -2.2, 38))
        sep = Line([-6.1, -0.7, 0], [6.1, -0.7, 0], color=GHOST, stroke_width=4)
        self.add(sep)
        a3_at(self, 0.15)                                       # "Then it changed the drawing and the animation choice only"
        self.play(FadeIn(h_a), run_time=0.3)
        a3_at(self, 0.65)                                       # "the drawing"
        self.play(Write(r_a[0]), run_time=0.5)
        a3_at(self, 1.3)                                        # "the animation choice"
        self.play(Write(r_a[1]), run_time=0.5)
        a3_at(self, 2.95)                                       # "The physics"
        self.play(Create(divider), FadeIn(h_b), Write(r_b[0]), run_time=0.7)
        a3_at(self, 3.75)                                       # "the tuning"
        self.play(Write(r_b[1]), run_time=0.5)
        a3_at(self, 4.45)                                       # "the level and the hazards"
        self.play(Write(r_b[2]), run_time=0.6)
        a3_at(self, 7.1)                                        # "A separate test compared"
        self.play(FadeIn(lab), run_time=0.5)
        a3_at(self, 8.0)                                        # "1,944"
        self.play(FadeIn(hero), run_time=0.5)
        done(self)


# ───────────────────────── B22 · the arms past the left edge ─────────────────────────
A3_EDGE = list(range(46, 62))


class B22_ArmsPastTheEdge(Scene):
    def construct(self):
        wx, wy, ww = -2.2, -0.2, 7.6
        wh = ww * 620 / 1500
        fr = a3_frame(ww, wh, wx, wy)
        first = a3_img("a3_edgeb_046.png", ww, wx, wy)
        cap = a3_t("scripted input, slow motion", wx, wy - 2.2, 32)
        # prediction 1, the card from before, now ticked
        card = a3_card(3.8, 1.6, 4.2, 1.5)
        n1 = a3_t("1", 2.65, 1.5, 40)
        l1 = a3_t("overhangs", 3.95, 1.8, 34)
        l1b = a3_t("the box", 3.95, 1.2, 34)
        tick = check(5.45, 1.55, s=0.2, color=INK, w=8)
        ring = Circle(radius=0.3, stroke_color=INK, stroke_width=6).move_to([2.75, -0.9, 0])
        open_lab = a3_t("left open", 4.35, -0.9, 38)
        edge = Line([wx - ww / 2 - 0.1, wy - wh / 2 - 0.1, 0], [wx - ww / 2 - 0.1, wy + wh / 2 + 0.1, 0], color=INK, stroke_width=10)
        edge_lab = a3_t("left edge of the world", -4.1, 2.4, 34)
        edge_arrow = Arrow([-5.6, 2.0, 0], [-6.0, 1.45, 0], buff=0, color=INK, stroke_width=5, tip_length=0.18)
        self.add(fr, first)
        a3_at(self, 0.1)                                        # "The first prediction"
        self.play(FadeIn(card), FadeIn(n1), FadeIn(l1), FadeIn(l1b), run_time=0.4)
        a3_at(self, 0.7)                                        # "came true"
        self.play(Create(tick), run_time=0.3)
        a3_at(self, 0.95)
        self.add(cap)
        prev = first
        for n in A3_EDGE[1:]:                                   # the real frames, each held two render frames (slow motion)
            nxt = a3_img(f"a3_edgeb_{n:03d}.png", ww, wx, wy)
            self.remove(prev)
            self.add(nxt)
            prev = nxt
            self.wait(0.0834)
        a3_at(self, 2.4)                                        # "past the left edge of the world"
        self.play(Create(edge), FadeIn(edge_lab), Create(edge_arrow), run_time=0.7)
        a3_at(self, 5.6)                                        # "It leaves it open"
        self.play(Create(ring), FadeIn(open_lab), run_time=0.6)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · Why You Check the World  (B23-B29, all Manim)

Cast for the act: THE RECEIPT (a saved record, shown as the REAL text of the file, trimmed only by dropping whole lines), THE COUNT
(one bar of frames: filled = saved, dashed = still missing), and THE TWO PANES (what was said / what changed). Every line of file text is
quoted from a real file of walker-jumpman-clawd (see factcheck/act4.md): gallery-two-receipt.json, gallery-two-v2-receipt.json,
inspector-v2-process.json, evidence/clawd/build-manifest.json, CLAWD-STATUS.json, design/decisions.md, and `git diff --stat` / `--numstat`
(re-run by evidence/act4/b26_check.py). B29's moving picture is 12 REAL frames of the Godot capture walker-claude-jumpman-gameplay.mp4
(scripted input, recorded 2026-10-09), cropped by evidence/act4/make_a4_pantry.py.
Pacing: a4_at(t) lands each motion on the real spoken time of a word (faster-whisper, evidence/act4/word_times.json).
"""

A4P = "pantry/"


def a4_at(self, t, lead=0.12):
    """Wait until the clip clock reaches t - lead seconds (t = the real spoken start time of a word)."""
    gap = t - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a4_left(mob, x, y):
    """Place a text left-aligned at x (explicit coordinates; never read back a text's edge)."""
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def a4_card(cx, cy, w, h, dashed=False, color=DIM):
    """An outline-only card (no fill behind text)."""
    r = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=color, stroke_width=4, fill_opacity=0).move_to([cx, cy, 0])
    return DashedVMobject(r, num_dashes=44, dashed_ratio=0.55) if dashed else r


def a4_cross(x, y, s=0.22, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w))


def a4_bar(x0, y, w, h, color=BAR1):
    """A filled grey bar whose left end sits at x0 (the count of frames saved)."""
    return Rectangle(width=w, height=h, fill_color=color, fill_opacity=1, stroke_width=0).move_to([x0 + w / 2.0, y, 0])


def a4_gap(x0, y, w, h):
    """The part of the count that is missing: an outline-only dashed box."""
    return a4_card(x0 + w / 2.0, y, w, h, dashed=True)


def a4_lines(rows, x, y0, dy=0.5, size=32):
    """Real file text, one Menlo line per row, left-aligned at x."""
    return VGroup(*[a4_left(M(s, size), x, y0 - i * dy) for i, s in enumerate(rows)])


# ── B23 · ACT TITLE · a receipt that said PASS held 343 of the 540 frames the plan needed ───────────────────────────
class B23_ReceiptSaidPass(Scene):
    def construct(self):
        title = a4_left(T("Why You Check the World", 40), -6.1, 3.0)
        self.add(title)
        card = a4_card(-3.1, 1.05, 6.0, 2.0)
        rows = a4_lines(['"take": "gallery-two",', '"frames": 343,', '"status": "PASS",'], -5.85, 1.5, 0.5)
        lab = a4_left(T("the receipt, as saved", 36), 0.35, 1.6)
        lab2 = a4_left(T("a gallery take, not gameplay", 32), 0.35, 1.05)
        a4_at(self, 4.0)                                                   # "One recording of the game came with a receipt"
        self.play(FadeIn(card), FadeIn(rows), FadeIn(lab), FadeIn(lab2), run_time=0.6)
        a4_at(self, 6.14)                                                  # "that said pass"
        ok = check(0.55, 0.4, s=0.28)
        self.play(Create(ok), run_time=0.35)
        a4_at(self, 7.3)                                                   # "It held 343 frames"
        saved = a4_bar(-6.0, -1.3, 343 / 540.0 * 12.0, 0.8)
        n343 = T("343", 72).move_to([-2.2, -2.5, 0])
        s343 = a4_left(T("saved", 36), -1.2, -2.5)
        self.play(GrowFromEdge(saved, LEFT), FadeIn(n343), FadeIn(s343), run_time=0.8)
        a4_at(self, 9.5)                                                   # "The plan needed 540"
        gap = a4_gap(-6.0 + 343 / 540.0 * 12.0, -1.3, 12.0 * 197 / 540.0, 0.8)
        n540 = T("540", 72).move_to([2.9, -2.5, 0])
        s540 = a4_left(T("needed", 36), 3.7, -2.5)
        self.play(Create(gap), FadeIn(n540), FadeIn(s540), run_time=0.7)
        done(self)


# ── B24 · the AI rejected the recording, kept it as evidence, and now requires 600 frames ────────────────────────────
class B24_RejectedKept(Scene):
    def construct(self):
        t1 = a4_left(T("gallery-two", 36), -5.8, 2.2)
        c1 = a4_card(-3.4, 1.0, 4.8, 1.5)
        r1 = a4_lines(['"frames": 343,', '"status": "PASS"'], -5.55, 1.25, 0.5)
        self.add(t1, c1, r1)
        a4_at(self, 1.22)                                                  # "rejected the recording"
        x1 = a4_cross(-5.3, -0.4)
        l1 = a4_left(T("rejected", 36), -4.85, -0.4)
        self.play(Create(x1), FadeIn(l1), run_time=0.4)
        a4_at(self, 2.5)                                                   # "kept it as evidence"
        d1 = Dot([-5.3, -1.2, 0], radius=0.1, color=DIM)
        l2 = a4_left(T("kept as evidence", 36), -4.85, -1.2)
        self.play(GrowFromCenter(d1), FadeIn(l2), run_time=0.4)
        a4_at(self, 3.86)                                                  # "and changed its method"
        arr = Arrow([-0.7, 1.0, 0], [0.8, 1.0, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        t2 = a4_left(T("gallery-two-v2", 36), 1.1, 2.2)
        c2 = a4_card(3.5, 1.0, 4.8, 1.5)
        r2 = a4_lines(['"frames": 600,', '"status": "PASS"'], 1.35, 1.25, 0.5)
        self.play(Create(arr), FadeIn(t2), FadeIn(c2), FadeIn(r2), run_time=0.6)
        a4_at(self, 5.3)                                                   # "to require 600 frames"
        n600 = T("600", 72).move_to([2.4, -0.6, 0])
        s600 = a4_left(T("frames required", 36), 3.3, -0.65)
        self.play(FadeIn(n600, shift=UP * 0.15), FadeIn(s600), run_time=0.5)
        done(self)


# ── B25 · exit code 0, no completion receipt, 416 of 600 frames ──────────────────────────────────────────────────────
class B25_ExitCodeZero(Scene):
    def construct(self):
        a4_at(self, 0.74)                                                  # "ended with exit code 0"
        lab = a4_left(T("process record", 36), -6.0, 2.85)
        card = a4_card(-3.8, 1.9, 4.4, 0.9)
        row = a4_left(M('"exit_code": 0,', 32), -5.75, 1.9)
        self.play(FadeIn(lab), FadeIn(card), FadeIn(row), run_time=0.5)
        a4_at(self, 2.7)                                                   # "the code that means success"
        ok = check(-0.9, 1.9, s=0.28)
        oks = a4_left(T("success", 36), -0.35, 1.9)
        self.play(Create(ok), FadeIn(oks), run_time=0.4)
        a4_at(self, 4.4)                                                   # "no completion receipt"
        page = a4_card(3.6, 1.9, 3.0, 1.4, dashed=True)
        pl = T("no receipt", 36).move_to([3.6, 0.85, 0])
        self.play(Create(page), FadeIn(pl), run_time=0.5)
        a4_at(self, 5.9)                                                   # "only 416 of 600 frames"
        saved = a4_bar(-6.0, -0.35, 416 / 600.0 * 12.0, 0.7)
        n416 = T("416", 72).move_to([-2.6, -1.4, 0])
        s416 = a4_left(T("saved", 36), -1.8, -1.4)
        self.play(GrowFromEdge(saved, LEFT), FadeIn(n416), FadeIn(s416), run_time=0.55)
        a4_at(self, 7.4)
        gap = a4_gap(-6.0 + 416 / 600.0 * 12.0, -0.35, 12.0 * 184 / 600.0, 0.7)
        n600 = T("600", 72).move_to([3.2, -1.4, 0])
        s600 = a4_left(T("required", 36), 4.0, -1.4)
        self.play(Create(gap), FadeIn(n600), FadeIn(s600), run_time=0.6)
        a4_at(self, 10.1)                                                  # "In the record's own words: exit code 0 did not establish success"
        ring = DashedVMobject(Circle(radius=0.3, stroke_color=DIM, stroke_width=6).move_to([-0.9, 1.9, 0]), num_dashes=14, dashed_ratio=0.55)
        q = T("Exit code zero did not establish success.", 40).move_to([0, -2.55, 0])
        qa = T("the project's own record", 32).move_to([0, -3.05, 0])
        self.play(FadeOut(ok), Create(ring), FadeIn(q), FadeIn(qa), run_time=0.7)
        done(self)


# ── B26 · "byte-identical" was true of one function; the same file changed by 33 lines ──────────────────────────────
# player.gd at the Clawd commit is 93 lines. `func _physics_process(` runs from line 44 to 72 (the record's own slice, 29 lines).
# git diff -U0: lines 4-6 added, 73-91 added, 93 added (23 added) and 10 old lines removed (evidence/act4/b26_check.log).
A4_N, A4_TOP, A4_PITCH = 93, 2.5, 5.1 / 93.0
A4_CHANGED = list(range(4, 7)) + list(range(73, 92)) + [93]


def a4_row_y(k):
    return A4_TOP - (k - 0.5) * A4_PITCH


class B26_OneFunction(Scene):
    def construct(self):
        head = a4_left(M("player.gd", 32), -5.3, 3.0)
        frame = Rectangle(width=3.9, height=5.3, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([-3.35, -0.1, 0])
        rows = VGroup(*[Rectangle(width=3.6 * (0.4 + 0.6 * (((k * 37) % 11) / 11.0)), height=0.034, fill_color=BAR2, fill_opacity=1, stroke_width=0)
                        .move_to([-5.15 + 1.8 * (0.4 + 0.6 * (((k * 37) % 11) / 11.0)), a4_row_y(k), 0]) for k in range(1, A4_N + 1)])
        self.add(head, frame, rows)
        a4_at(self, 2.4)                                                   # "the physics function"
        sl = VGroup(*[rows[k - 1] for k in range(44, 73)])
        br = VGroup(Line([-1.3, a4_row_y(44) + 0.03, 0], [-1.3, a4_row_y(72) - 0.03, 0], color=INK, stroke_width=5),
                    Line([-1.3, a4_row_y(44) + 0.03, 0], [-1.45, a4_row_y(44) + 0.03, 0], color=INK, stroke_width=5),
                    Line([-1.3, a4_row_y(72) - 0.03, 0], [-1.45, a4_row_y(72) - 0.03, 0], color=INK, stroke_width=5))
        ld = Line([-1.3, -0.65, 0], [-0.7, -0.65, 0], color=INK, stroke_width=5)
        fn = a4_left(M("_physics_process", 32), -0.25, -0.65)
        self.play(*[r.animate.set_fill(DIM) for r in sl], Create(br), Create(ld), FadeIn(fn), run_time=0.7)
        a4_at(self, 4.12)                                                  # "byte-identical"
        bi = a4_left(T("byte-identical", 40), -0.25, -1.4)
        ok = check(2.9, -1.4, s=0.28)
        self.play(FadeIn(bi), Create(ok), run_time=0.5)
        a4_at(self, 5.9)                                                   # "that check compares one function"
        one = a4_left(T("the check reads this one function", 36), -0.25, -2.15)
        self.play(FadeIn(one), run_time=0.4)
        a4_at(self, 7.7)                                                   # "The same file changed by 33 lines"
        ch = VGroup(*[rows[k - 1] for k in A4_CHANGED])
        dots = VGroup(*[Dot([-5.55, a4_row_y(m), 0], radius=0.09, color=TERRA) for m in (5, 82, 93)])
        n33 = T("33", 120).move_to([1.2, 1.75, 0])
        l33 = a4_left(T("lines changed", 36), 2.3, 1.95)
        l23 = VGroup(a4_left(T("23 added", 36), 2.3, 1.4), a4_left(T("10 removed", 36), 2.3, 0.95))
        self.play(*[r.animate.set_fill(DIM) for r in ch], FadeIn(dots), FadeIn(n33), FadeIn(l33), FadeIn(l23), run_time=0.7)
        done(self)


# ── B27 · two panes: what was said / what changed ────────────────────────────────────────────────────────────────────
class B27_SaidVersusChanged(Scene):
    def construct(self):
        pl = a4_card(-3.15, 0.6, 5.5, 3.0)
        pr = a4_card(3.15, 0.6, 5.5, 3.0)
        a4_at(self, 0.35)
        self.play(Create(pl), Create(pr), run_time=0.5)
        a4_at(self, 2.4)                                                   # "A success statement records what was said"
        hl = T("what was said", 38).move_to([-3.15, 2.6, 0])
        tl = a4_lines(['"physics_function":', '"byte-identical"'], -5.65, 0.95, 0.65)
        self.play(FadeIn(hl), FadeIn(tl), run_time=0.5)
        a4_at(self, 4.7)                                                   # "The state records what actually changed"
        hr = T("what changed", 38).move_to([3.15, 2.6, 0])
        tr = a4_lines(['…/player.gd | 33 +-', '+23  -10'], 0.65, 0.95, 0.65)
        ne = VGroup(Line([-0.2, -1.55, 0], [0.2, -1.55, 0], color=INK, stroke_width=8), Line([-0.2, -1.8, 0], [0.2, -1.8, 0], color=INK, stroke_width=8),
                    Line([-0.12, -1.95, 0], [0.12, -1.4, 0], color=INK, stroke_width=8))
        self.play(FadeIn(hr), FadeIn(tr), Create(ne), run_time=0.5)
        a4_at(self, 6.84)                                                  # "You read the state"
        cur = cursor(0.0, -2.2)
        self.add(cur)
        ok = check(5.0, 2.6, s=0.26)
        self.play(cur.animate.move_to([3.4, 0.25, 0]), Create(ok), run_time=0.7)
        done(self)


# ── B28 · the records are the AI's own, no human finding, play-test pending, eight questions open ───────────────────
class B28_NoHumanFinding(Scene):
    def construct(self):
        a4_at(self, 0.12)                                                  # "these records were written by the AI itself"
        pg = Polygon([-5.9, 2.75, 0], [-5.35, 2.75, 0], [-5.15, 2.55, 0], [-5.15, 1.85, 0], [-5.9, 1.85, 0],
                     fill_opacity=0, stroke_color=INK, stroke_width=4)
        pls = VGroup(*[Line([-5.7, y, 0], [-5.35, y, 0], color=GHOST, stroke_width=4) for y in (2.2, 2.05)])
        w1 = a4_left(T("written by the AI", 38), -4.8, 2.3)
        self.play(Create(pg), Create(pls), FadeIn(w1), run_time=0.5)
        a4_at(self, 3.44)                                                  # "look for the human finding"
        w2 = a4_left(T("human finding", 38), -6.0, 1.05)
        slot = a4_card(-0.4, 1.05, 4.6, 0.9, dashed=True)
        self.play(FadeIn(w2), Create(slot), run_time=0.5)
        a4_at(self, 5.3)                                                   # "There is none"
        none = a4_left(T("none recorded", 38), 2.2, 1.05)
        self.play(FadeIn(none), run_time=0.35)
        a4_at(self, 6.04)                                                  # "The human play-test is still marked pending"
        hp = a4_left(M('"human_playtest": "pending"', 32), -6.0, -0.35)
        self.play(FadeIn(hp, shift=RIGHT * 0.2), run_time=0.45)
        a4_at(self, 8.62)                                                  # "Eight design questions are still open"
        cells = VGroup(*[a4_card(-5.55 + 0.65 + i * 1.4, -1.75, 1.3, 0.8) for i in range(8)])
        qs = VGroup(*[M(f"Q-0{i + 1}", 32).move_to([-5.55 + 0.65 + i * 1.4, -1.75, 0]) for i in range(8)])
        self.play(LaggedStart(*[AnimationGroup(Create(c), FadeIn(q)) for c, q in zip(cells, qs)], lag_ratio=0.25), run_time=1.5)
        a4_at(self, 10.64)                                                 # "each with a person's name on it"
        ow = T("every one: owner Bear, status Open", 36).move_to([0, -2.75, 0])
        self.play(FadeIn(ow), run_time=0.45)
        done(self)


# ── B29 · HINGE · the machine says passed; a person says whether it is fun ──────────────────────────────────────────
class B29_PassedVersusFun(Scene):
    def construct(self):
        # GATE T reads the flat terracotta Clawd (a mascot wider than 1.5x its height) as accent text at the 50% frame, so the real
        # capture window lands AFTER the midpoint (3.9 s of 7.64 s); before it the frame holds the machine's side.
        frames = [ImageMobject(A4P + f"a4_g{i:02d}.png").set_width(5.6).move_to([3.3, 1.0, 0]) for i in range(12)]
        for f in frames:
            f.set_opacity(0.0)
            self.add(f)
        box = Rectangle(width=5.6, height=5.6 * 530 / 1120.0, stroke_color=DIM, stroke_width=3, fill_opacity=0).move_to([3.3, 1.0, 0])
        cap1 = T("scripted input", 32).move_to([3.3, -0.6, 0])
        cap2 = T("recorded 2026-10-09", 32).move_to([3.3, -1.0, 0])
        mid = Line([0.0, 3.0, 0], [0.0, -3.0, 0], color=GHOST, stroke_width=5)
        live = [False]
        tm = [0.0]

        def upd(_m, dt):
            tm[0] += dt
            i = int(tm[0] * 10) % 12
            for j, f in enumerate(frames):
                f.set_opacity(1.0 if (live[0] and j == i) else 0.0)
        frames[0].add_updater(upd)
        self.play(Create(mid), run_time=0.3)
        a4_at(self, 2.5)                                                   # "The machine can tell you 100 things passed"
        hm = T("the machine", 40).move_to([-3.0, 2.9, 0])
        dots = VGroup(*[Dot([-4.35 + (j % 10) * 0.3, 1.9 - (j // 10) * 0.3, 0], radius=0.07, color=BAR1) for j in range(100)])
        self.play(FadeIn(hm), LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.012), run_time=1.1)
        a4_at(self, 3.95)                                                  # "passed" (the real game starts running)
        ps = T("passed", 44).move_to([-3.0, -1.45, 0])
        ok = check(-4.4, -1.45, s=0.3)
        ex = T("an example: 100 checks", 32).move_to([-3.0, -2.05, 0])
        rt = guard(self, 0.5)                                              # keep the capture window off the midpoint frame
        live[0] = True
        self.play(Create(box), FadeIn(cap1), FadeIn(cap2), FadeIn(ps), Create(ok), FadeIn(ex), run_time=rt)
        a4_at(self, 4.9)                                                   # "Only a person can say whether it is fun"
        hp = T("a person", 40).move_to([3.3, 2.9, 0])
        fun = T("fun?", 60).move_to([2.6, -2.2, 0])
        ring = DashedVMobject(Circle(radius=0.55, stroke_color=DIM, stroke_width=6).move_to([4.5, -2.2, 0]), num_dashes=18, dashed_ratio=0.55)
        self.play(FadeIn(hp), FadeIn(fun), Create(ring), run_time=0.7)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · How the Course Works  (B30-B34, all Manim)

One cast for the act: THE DIRECTOR'S LINE. A terracotta dot (the baton) travels the act's pictures; the tools (Claude Code, Codex)
and the engine (Godot) are shown as their own marks, the game as a real recorded run, the log as the real FRICTIONAL.md text, and
the closing picture is the orchestra of B03 with its podium filled by a person (Professor Bear portrait, PROFESSOR BEAR LAW).

Pacing: a5_at() lands each motion on the real spoken time of a word (faster-whisper times, evidence/act5/word_times.json).
Real evidence only: the Godot page is the real capture (web-captures/godot-home.png, cropped); the game frames are the real
walker-claude run (scripted input, recorded 2026-10-09); the log lines are verbatim from walker-jumpman-clawd/FRICTIONAL.md
(trimmed only with a visible ellipsis; markdown bold marks removed because the page is shown rendered).
"""

A5P = "pantry/"


def a5_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a5_lab(s, x, y, size=34, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def a5_left(s, left, y, w, size=34, color=INK, bold=False):
    """A serif label whose LEFT edge sits at x = left; w = its width, MEASURED with real Manim (evidence/act5/widths.py)
    because Gate A's stub cannot measure text and layout rules forbid reading edges."""
    return T(s, size, color, bold).move_to([left + w / 2.0, y, 0])


def a5_mleft(s, left, y, size=32, color=INK):
    """Menlo line, left edge at x = left; Menlo 32 is 0.2492 units a character (measured)."""
    return M(s, size, color).move_to([left + 0.2492 * len(s) / 2.0, y, 0])


def a5_svg(name, h, x, y, color=INK):
    m = SVGMobject(A5P + name)
    m.set_fill(color, 1)
    m.set_stroke(color, 0)
    m.set_height(h)
    return m.move_to([x, y, 0])


def a5_img(name, w, x, y):
    im = ImageMobject(A5P + name)
    im.set_width(w)
    return im.move_to([x, y, 0])


def a5_frames(folder, n):
    try:
        from PIL import Image
        return [np.array(Image.open(f"{A5P}{folder}/f{i:03d}.png").convert("RGBA")) for i in range(1, n + 1)]
    except Exception:                      # Gate A's stub folder holds only scenes.py
        return [np.zeros((4, 4, 4), dtype=np.uint8)]


def a5_game_tick(m, dt):
    m.a5t += dt
    m.pixel_array = m.a5f[min(int(m.a5t * 12.0), len(m.a5f) - 1)]


def a5_game(w, x, y):
    """The real walker-claude run (scripted input, recorded 2026-10-09), 12 frames a second, played in real time."""
    fr = a5_frames("a5_game_frames", 50)
    g = ImageMobject(fr[0]).set_width(w).move_to([x, y, 0])
    g.a5f, g.a5t = fr, 0.0
    g.add_updater(a5_game_tick)
    return g


# ═════════════════════ B30 · direct Claude Code or Codex to build real games in Godot ═════════════════════
class B30_ToolsAndEngine(Scene):
    def construct(self):
        title = a5_lab("How the Course Works", -3.45, 2.85, 40)
        self.add(title)
        cc, ccl = a5_svg("a5_logo_claude-code.svg", 0.8, -5.45, 1.15), a5_left("Claude Code", -4.6, 1.15, 2.568, 38)
        cx, cxl = a5_svg("a5_logo_codex-openai.svg", 0.8, -5.45, -0.25), a5_left("Codex", -4.6, -0.25, 1.25, 38)
        arrow = Arrow([-1.7, 0.45, 0], [0.15, 0.45, 0], color=INK, stroke_width=6, buff=0, tip_length=0.28)
        godot = a5_img("a5_godot_home_top.png", 5.6, 3.2, 1.85)
        game = a5_game(4.6, 3.2, -0.95)
        cap = a5_left("scripted input, recorded 2026-10-09", 0.3, -2.75, 5.843, 32, DIM)
        a5_at(self, 2.15)
        self.play(FadeIn(cc), FadeIn(ccl), run_time=0.4)                       # "Claude Code"
        a5_at(self, 3.25)
        self.play(FadeIn(cx), FadeIn(cxl), run_time=0.4)                       # "Codex"
        a5_at(self, 3.7)
        self.play(GrowArrow(arrow), run_time=0.45)                              # "to build"
        a5_at(self, 4.3)
        self.add(game)
        self.play(FadeIn(game), FadeIn(cap), run_time=0.3)                      # "real games" (plays on)
        a5_at(self, 4.9)
        self.play(FadeIn(godot), run_time=0.4)                                  # "in Godot"
        done(self)


# ═════════════════════ B31 · brief, one change, predict, choose the check ═════════════════════
class B31_FourSteps(Scene):
    def construct(self):
        xs = [-4.65, -1.55, 1.55, 4.65]
        YN, YR, YP, YL, YC = 2.3, 1.7, 0.2, -1.2, -2.0          # numerals, rail, pictures, labels, captions
        rail = Line([-4.9, YR, 0], [4.9, YR, 0], color=DIM, stroke_width=4)
        nums = [a5_lab(str(i + 1), x, YN, 44) for i, x in enumerate(xs)]
        baton = Dot([xs[0], YR, 0], radius=0.14, color=TERRA)
        self.add(rail, *nums)
        # 1 brief: a page with ghost lines
        pg = Rectangle(width=1.5, height=1.95, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([xs[0], YP, 0])
        pl = VGroup(*[Line([xs[0] - 0.5, YP + dy, 0], [xs[0] + 0.5, YP + dy, 0], color=DIM, stroke_width=4) for dy in (0.5, 0.12, -0.26)])
        pd = Dot([xs[0] - 0.5, YP - 0.7, 0], radius=0.07, color=TERRA)
        l1, c1 = a5_lab("brief", xs[0], YL, 40), a5_lab("player: Clawd", xs[0], YC, 32, DIM)
        # 2 one change: the real starter level, its player (the thing the one change redraws)
        im = a5_img("a5_starter_jump_crop.png", 2.4, xs[1], YP)
        l2, c2 = a5_lab("one change", xs[1], YL, 40), a5_lab("redraw the player", xs[1], YC, 32, DIM)
        # 3 predict: three prediction cards
        cards = VGroup(*[Rectangle(width=0.85, height=1.2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([xs[2] + dx, YP, 0])
                         for dx in (-1.0, 0.0, 1.0)])
        cn = VGroup(*[a5_lab(str(i + 1), xs[2] + dx, YP, 40) for i, dx in enumerate((-1.0, 0.0, 1.0))])
        l3, c3 = a5_lab("predict", xs[2], YL, 40), a5_lab("3 ways it fails", xs[2], YC, 32, DIM)
        # 4 choose the check: a check in a grey ring
        ring = Circle(radius=0.95, stroke_color=DIM, stroke_width=6).move_to([xs[3], YP, 0])
        ck = check(xs[3] - 0.12, YP, 0.42, INK, 9)
        l4, c4 = a5_lab("check", xs[3], YL, 40), a5_lab("1,944 comparisons", xs[3], YC, 32, DIM)

        self.add(baton)
        a5_at(self, 0.15)
        self.play(Create(pg), Create(pl), FadeIn(pd), run_time=0.45)
        self.play(FadeIn(l1), FadeIn(c1), run_time=0.25)                         # "a brief"
        a5_at(self, 1.35)
        self.play(baton.animate.move_to([xs[1], YR, 0]), run_time=0.3)
        self.play(FadeIn(im), run_time=0.3)                                     # "one change"
        self.play(FadeIn(l2), FadeIn(c2), run_time=0.25)
        a5_at(self, 2.85)
        self.play(baton.animate.move_to([xs[2], YR, 0]), run_time=0.25)
        self.play(Create(cards), FadeIn(cn), run_time=0.4)                      # "predict"
        self.play(FadeIn(l3), FadeIn(c3), run_time=0.15)
        a5_at(self, 5.45)
        self.play(baton.animate.move_to([xs[3], YR, 0]), run_time=0.3)
        self.play(Create(ring), Create(ck), run_time=0.45)                      # "choose the check"
        self.play(FadeIn(l4), FadeIn(c4), run_time=0.25)
        done(self)


# ═════════════════════ B32 · the log: what the AI did, what you decided, what you doubted ═════════════════════
class B32_TheLog(Scene):
    def construct(self):
        fname = a5_mleft("FRICTIONAL.md", -6.0, 2.95, 32, DIM)
        page = Rectangle(width=12.0, height=4.5, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([0, 0.35, 0])
        head = a5_left("Frictional \u2014 an honest effort log", -5.6, 1.75, 7.258, 38, INK, True)
        rows = [("Human contribution: Bear chose \u2026", 0.65), ("AI contribution: inspected the \u2026", -0.35),
                ("Prediction: wide art may \u2026", -1.35)]
        lines = [a5_mleft(s, -3.55, y, 32) for s, y in rows]
        self.add(fname)
        a5_at(self, 0.3)
        self.play(Create(page), FadeIn(head), run_time=0.4)                      # "a log"
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.25), run_time=0.6)
        marks = [("did", rows[1][1], 0.571), ("decided", rows[0][1], 1.421), ("doubted", rows[2][1], 1.571)]
        dots = [Dot([-5.65, y, 0], radius=0.1, color=TERRA) for _, y, _w in marks]
        words = [a5_left(w, -5.4, y, ww, 34) for w, y, ww in marks]
        a5_at(self, 1.1)
        self.play(FadeIn(dots[0]), FadeIn(words[0]), run_time=0.2)               # "what the A.I. did"
        a5_at(self, 2.2)
        self.play(FadeIn(dots[1]), FadeIn(words[1]), run_time=0.2)               # "what you decided"
        a5_at(self, 2.8)
        self.play(FadeIn(dots[2]), FadeIn(words[2]), run_time=0.2)               # "what you doubted"
        brace = BraceBetweenPoints([-5.9, -2.0, 0], [5.9, -2.0, 0], direction=[0, -1, 0], color=DIM)
        ev = a5_lab("evidence of your work", 0, -2.85, 38)
        a5_at(self, 3.85)
        self.play(Create(brace), run_time=0.4)                                   # "That log"
        a5_at(self, 4.5)
        self.play(FadeIn(ev), run_time=0.3)                                      # "the evidence"
        done(self)


# ═════════════════════ B33 · the two next films ═════════════════════
class B33_TwoNextFilms(Scene):
    def construct(self):
        ca, cb, cy, W, H = -3.1, 3.1, 0.0, 5.6, 4.6
        gh = [DashedVMobject(Rectangle(width=W, height=H, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, cy, 0]), num_dashes=44)
              for x in (ca, cb)]
        sa = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([ca, cy, 0])
        sb = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cb, cy, 0])
        fa, fb = a5_lab("Film 2 of 3", ca, 1.65, 34, DIM), a5_lab("Film 3 of 3", cb, 1.65, 34, DIM)
        ta = a5_lab("Why Godot", ca, 0.55, 56)
        tb1, tb2 = a5_lab("What Is Walker,", cb, 0.85, 50), a5_lab("and Why", cb, 0.1, 50)
        mk, ml = a5_svg("a5_logo_godot.svg", 0.85, ca - 1.0, -1.4), a5_left("the engine", ca - 0.35, -1.4, 1.865, 40)
        rl = VGroup(*[Line([cb - 1.6, -1.05 - 0.3 * i, 0], [cb - 0.6 - 0.2 * (i % 2), -1.05 - 0.3 * i, 0], color=DIM, stroke_width=5) for i in range(3)])
        rd = Dot([cb - 1.6, -1.05, 0], radius=0.08, color=TERRA)
        rt = a5_left("the rules", cb - 0.3, -1.4, 1.528, 40)
        a5_at(self, 0.35)
        self.play(Create(gh[0]), Create(gh[1]), run_time=0.5)                    # "Two more films"
        a5_at(self, 1.35)
        self.play(Create(sa), FadeIn(fa), FadeIn(ta), run_time=0.4)              # "Why Godot"
        self.play(FadeIn(mk), FadeIn(ml), run_time=0.25)
        a5_at(self, 2.5)
        self.play(Create(sb), FadeIn(fb), FadeIn(tb1), FadeIn(tb2), run_time=0.4)   # "what Walker is"
        a5_at(self, 3.4)
        self.play(Create(rl), FadeIn(rd), FadeIn(rt), run_time=0.9)               # "the rules"
        a5_at(self, 4.6)
        self.play(rd.animate.move_to([cb - 1.6, -1.05 - 0.6, 0]), run_time=0.5)  # "works under"
        done(self)


# ═════════════════════ B34 · the baton: conducting it ═════════════════════
class B34_TheBaton(Scene):
    def construct(self):
        iso = Iso(0.0, -2.3, 0.7)
        S_TOP, S_L, S_R = BAR2, BAR1, DIM
        podium = iso.box(-0.6, -0.6, 0, 1.2, 1.2, 0.55, BOX_TOP, BOX_L, BOX_R)
        lights, players = [], []
        for d, js in ((6.5, (-2, -1, 0, 1, 2)), (5.0, (-1.5, -0.5, 0.5, 1.5)), (3.6, (-2, -1, 0, 1, 2))):
            for j in js:
                X, Y = d + j, d - j
                players.append(iso.box(X - 0.4, Y - 0.4, 0, 0.8, 0.8, 0.5, S_TOP, S_L, S_R))
                lights.append(Dot(iso.p(X, Y, 0.95), radius=0.12, color=GHOST))
        ai = a5_lab("A.I.", -4.7, 0.9, 40)
        self.add(podium)
        a5_at(self, 0.1)
        self.play(LaggedStart(*[FadeIn(p) for p in players], lag_ratio=0.05), run_time=0.9)
        self.play(FadeIn(VGroup(*lights)), FadeIn(ai), run_time=0.3)              # "an A.I."
        a5_at(self, 1.45)
        self.play(LaggedStart(*[d.animate.set_color(TERRA) for d in lights], lag_ratio=0.06), run_time=0.8)   # "write code"
        pb = ImageMobject(A5P + "a5_pb_circle_04.png").set_height(1.5).move_to([0, 1.9, 0])
        pbl = a5_left("Professor Bear", -4.6, -1.5, 2.644, 34)
        hand = np.array([0.85, -1.35, 0.0])
        baton = VGroup(Line(hand, hand + np.array([0.95, 0.75, 0.0]), color=INK, stroke_width=6),
                       Dot(hand + np.array([0.95, 0.75, 0.0]), radius=0.1, color=TERRA))
        cond = a5_left("conducting", 2.9, -0.4, 2.598, 44)
        a5_at(self, 2.55)
        self.add(pb)
        self.play(pb.animate.move_to([0, -1.1, 0]), rate_func=ease_in, run_time=0.45)    # "this course is about"
        self.play(FadeIn(pbl), Create(baton), run_time=0.3)
        a5_at(self, 3.25)
        self.play(FadeIn(cond), run_time=0.2)                                     # "conducting"
        self.play(Rotate(baton, 0.45, about_point=hand), run_time=0.25)
        self.play(Rotate(baton, -0.9, about_point=hand), run_time=0.4)
        self.play(Rotate(baton, 0.45, about_point=hand), run_time=0.25)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
