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
"""ACT I · The Problem Walker Answers  (B01-B04, all Manim)

One cast for the act: REAL FILES shown as themselves. The public repo page (B01, a real capture), then the real lines of real
files (legacy/README.md, legacy/AGENTS.md, LICENSE.md, CHANGELOG.md, publish.sh) set in Menlo and quoted with their file and
line (every quote is under 15 words). Drawings only carry ideas (the cost bars, the membrane); the bars are labelled as an
illustration. Nothing is invented: see factcheck/act1.md.

GATE T notes (measured at real 4K, see evidence/act1/gates_act1.py): the capture is zoomed so its type clears the 41 px floor;
ink-coloured outlines never touch a label; the terracotta pointer is always a DOT.
Pacing: until() lands each motion on the spoken word (character share of the measured audio).
"""

A1P = "pantry/"
A1_MW = 0.2459            # Menlo width per character at size 32 (units); scales with size/32


def a1_at(self, t):
    """Wait until the clip clock reaches t seconds (a real spoken time from evidence/act1/word_times.json, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a1_ml(s, xl, y, size=32, color=INK):
    """Menlo text whose LEFT edge sits at xl (explicit arithmetic: no get_left())."""
    return M(s, size, color).move_to([xl + len(s) * A1_MW * size / 32.0 / 2.0, y, 0])


def a1_mr(s, xr, y, size=32, color=INK):
    """Menlo text whose RIGHT edge sits at xr."""
    return M(s, size, color).move_to([xr - len(s) * A1_MW * size / 32.0 / 2.0, y, 0])


def a1_no(x, y, r=0.27, sw=6):
    """A prohibition mark: ring + bar, drawn BESIDE its label, never around it."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a1_icon_page(x, y):
    """Instructions: a page with three ghost lines and one terracotta dot."""
    body = Rectangle(width=0.56, height=0.72, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
    ls = VGroup(*[Line([x - 0.16, y + dy, 0], [x + 0.16, y + dy, 0], color=BAR2, stroke_width=4) for dy in (0.16, 0.0, -0.16)])
    return VGroup(body, ls, Dot([x - 0.16, y - 0.27, 0], radius=0.05, color=TERRA))


def a1_icon_tool(x, y):
    """Tools: a hammer (handle and head)."""
    handle = Line([x, y - 0.36, 0], [x, y + 0.14, 0], color=DIM, stroke_width=9)
    head = Rectangle(width=0.58, height=0.22, stroke_color=DIM, stroke_width=5).move_to([x, y + 0.26, 0])
    return VGroup(handle, head)


def a1_icon_loop(x, y):
    """A way of working: a loop with an arrow head."""
    a0, da, r = 0.45, 5.2, 0.3
    arc = Arc(radius=r, start_angle=a0, angle=da, stroke_color=DIM, stroke_width=6).move_to([x, y, 0])
    e = a0 + da
    px, py = x + r * np.cos(e), y + r * np.sin(e)
    tx, ty = -np.sin(e), np.cos(e)
    nx, ny = np.cos(e), np.sin(e)
    tip = Polygon([px + tx * 0.2, py + ty * 0.2, 0], [px + nx * 0.11, py + ny * 0.11, 0], [px - nx * 0.11, py - ny * 0.11, 0],
                  fill_color=DIM, fill_opacity=1, stroke_width=0)
    return VGroup(arc, tip)


# ═════════════════════════════════ B01 · a framework, not a game, not an engine ═════════════════════════════════
class B01_Framework(Scene):
    def construct(self):
        title = T("The Problem Walker Answers", 40).move_to([-2.85, 3.0, 0])
        img = ImageMobject(A1P + "a1_github_walker_crop.png").set_height(4.6).move_to([0, 0.05, 0])
        frame = Rectangle(width=4.0, height=4.72, stroke_color=DIM, stroke_width=3).move_to([0, 0.05, 0])
        addr = M("nikbearbrown/walker", 32).move_to([0, -2.65, 0])
        date = T("public page, captured 2026-10-09", 32).move_to([0, -3.1, 0])
        cap = Group(img, frame, addr, date)
        self.add(title)
        self.play(FadeIn(cap), run_time=0.6)

        # the page slides left to make room (before the midpoint)
        a1_at(self, 2.85)
        self.play(cap.animate.shift(LEFT * 3.5), run_time=0.7)
        g_lab = T("a game", 38).move_to([1.66, 2.0, 0])
        e_lab = T("an engine", 38).move_to([1.99, 1.15, 0])
        self.play(FadeIn(g_lab), FadeIn(e_lab), run_time=0.4)
        a1_at(self, 3.95)
        g_no = a1_no(0.35, 2.0)
        self.play(Create(g_no), run_time=0.35)
        # the midpoint (4.7 s) holds: capture, "a game" struck, "an engine" waiting
        a1_at(self, 5.0)
        e_no = a1_no(0.35, 1.15)
        self.play(Create(e_no), run_time=0.35)

        a1_at(self, 6.15)
        i_ic = a1_icon_page(0.35, -0.05)
        i_lab = T("instructions", 38).move_to([2.22, -0.05, 0])
        self.play(FadeIn(i_ic), FadeIn(i_lab), run_time=0.4)
        a1_at(self, 7.12)
        t_ic = a1_icon_tool(0.35, -0.95)
        t_lab = T("tools", 38).move_to([1.47, -0.95, 0])
        self.play(FadeIn(t_ic), FadeIn(t_lab), run_time=0.4)
        a1_at(self, 7.85)
        w_ic = a1_icon_loop(0.35, -1.85)
        w_lab = T("a way of working", 38).move_to([2.71, -1.85, 0])
        self.play(FadeIn(w_ic), FadeIn(w_lab), run_time=0.4)
        done(self)


# ═════════════════════════════════ B02 · the sentence: execution cheap, judgment not ═════════════════════════════════
class B02_OneSentence(Scene):
    def construct(self):
        q1 = T("AI made execution cheap.", 40).move_to([0, 2.85, 0])
        q2 = T("It  did not make judgment cheap.", 40).move_to([0, 2.22, 0])
        src = M("legacy/README.md, line 7", 32).move_to([0, 1.62, 0])
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(src), run_time=0.6)

        base = -2.45
        bar_a = Rectangle(width=1.5, height=3.2, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.7, base + 1.6, 0])
        bar_b = Rectangle(width=1.5, height=3.2, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([1.7, base + 1.6, 0])
        lab_a = T("execution", 36).move_to([-1.7, -2.9, 0])
        lab_b = T("judgment", 36).move_to([1.7, -2.9, 0])
        cost = T("cost", 32).move_to([-5.0, -0.7, 0])
        note1 = T("illustration,", 32).move_to([4.75, -1.2, 0])
        note2 = T("not data", 32).move_to([4.75, -1.65, 0])
        self.play(FadeIn(bar_a), FadeIn(bar_b), FadeIn(lab_a), FadeIn(lab_b), FadeIn(cost), FadeIn(note1), FadeIn(note2), run_time=0.5)
        axis = Arrow([-4.4, base, 0], [-4.4, 1.0, 0], color=INK, stroke_width=5, buff=0, tip_length=0.2)
        self.play(Create(axis), run_time=0.4)

        # "AI made execution cheap": the execution bar falls (lands before the midpoint at 2.72 s)
        a1_at(self, 2.0)
        small = Rectangle(width=1.5, height=0.55, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.7, base + 0.275, 0])
        self.play(Transform(bar_a, small), run_time=0.7)

        # "It did not make judgment cheap": a level line from where the cost was, and the judgment bar stays
        a1_at(self, 3.4)
        ghost = DashedLine([-2.45, base + 3.2, 0], [0.95, base + 3.2, 0], color=DIM, stroke_width=5, dash_length=0.18)
        self.play(Create(ghost), run_time=0.5)
        a1_at(self, 3.85)
        dot = Dot([1.7, base + 3.2 + 0.3, 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(dot), run_time=0.3)
        done(self)


# ═════════════════════════════════ B03 · the membrane, and a repo of documents ═════════════════════════════════
class B03_Membrane(Scene):
    def construct(self):
        head = T("Doctrine and tooling for AI-assisted Unity work", 36).move_to([0, 2.95, 0])
        src = M("legacy/README.md, line 3", 32).move_to([0, 2.4, 0])
        self.play(FadeIn(head), FadeIn(src), run_time=0.6)

        a1_at(self, 2.45)
        vline = Line([0, 1.95, 0], [0, -1.55, 0], color=INK, stroke_width=9)
        agent = T("agent", 40).move_to([-3.0, 1.6, 0])
        human = T("human", 40).move_to([3.0, 1.6, 0])
        sub_l = T("text layer", 32).move_to([-3.0, 0.98, 0])
        sub_r = T("asset layer", 32).move_to([3.0, 0.98, 0])
        self.play(Create(vline), run_time=0.5)
        self.play(FadeIn(agent), FadeIn(human), FadeIn(sub_l), FadeIn(sub_r), run_time=0.4)

        a1_at(self, 3.95)
        c1, c2 = M("C#", 32).move_to([-3.0, 0.3, 0]), M("config", 32).move_to([-3.0, -0.4, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        # the midpoint (6.07 s) holds: the line, both columns named, the agent's side filled
        a1_at(self, 4.95)
        r1, r2, r3 = M(".meta", 32).move_to([3.0, 0.3, 0]), M(".prefab", 32).move_to([3.0, -0.4, 0]), M("scenes", 32).move_to([3.0, -1.1, 0])
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.5)

        # then the repo itself: documents only
        a1_at(self, 7.15)
        old = VGroup(vline, agent, human, sub_l, sub_r, c1, c2, r1, r2, r3)
        l1 = a1_ml("legacy/unity/", -5.7, 1.25)
        l2 = a1_ml("  README.md", -5.7, 0.7)
        l3 = a1_ml("  UNITY.md", -5.7, 0.15)
        l4 = a1_ml("  gate-pilot/*.md", -5.7, -0.4)
        cnt = T("18 files in legacy/: 17 .md and one .gitignore", 32).move_to([0, -1.2, 0])
        self.play(FadeOut(old), run_time=0.35)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3), FadeIn(l4), FadeIn(cnt), run_time=0.5)

        a1_at(self, 9.2)
        slot = DashedVMobject(Rectangle(width=4.4, height=1.9, stroke_color=DIM, stroke_width=5), num_dashes=40).move_to([3.3, 0.4, 0])
        tool = T("tooling", 38).move_to([3.3, 0.4, 0])
        self.play(Create(slot), FadeIn(tool), run_time=0.5)
        quote = T("the unity/ tooling does not exist yet", 36).move_to([0, -2.05, 0])
        qsrc = M("legacy/AGENTS.md, line 7", 32).move_to([0, -2.65, 0])
        self.play(FadeIn(quote), FadeIn(qsrc), run_time=0.5)
        done(self)


# ═════════════════════════════════ B04 · Godot, Godogen (MIT), and a skill added on top ═════════════════════════════════
class B04_OnTop(Scene):
    def construct(self):
        SX0, SX1 = -2.5, 6.0                       # slab left / right edge
        TX = -2.2                                    # text left edge inside the slabs
        # bottom slab: publish.sh's real usage line
        s1 = Rectangle(width=SX1 - SX0, height=1.15, stroke_color=INK, stroke_width=4).move_to([(SX0 + SX1) / 2, -2.5, 0])
        t1 = a1_ml("--engine godot|bevy|babylon", TX, -2.68)
        f1 = a1_mr("publish.sh", -2.8, -2.5)
        n1 = T("this film: godot", 32).move_to([-4.55, -3.02, 0])
        self.play(FadeIn(s1), FadeIn(t1), FadeIn(f1), FadeIn(n1), run_time=0.5)
        a1_at(self, 0.9)
        dot = Dot([TX + 9.5 * A1_MW + 0.5 * 5 * A1_MW - 0.5 * A1_MW, -2.17, 0], radius=0.09, color=TERRA)
        self.play(GrowFromCenter(dot), run_time=0.3)

        # middle slab: Godogen's own line, then the licence
        a1_at(self, 3.75)
        s2 = Rectangle(width=SX1 - SX0, height=2.15, stroke_color=INK, stroke_width=4).move_to([(SX0 + SX1) / 2, -0.52, 0])
        t3 = a1_ml("Initial Godogen release ...", TX, -1.1)
        f3 = a1_mr("CHANGELOG.md", -2.8, -1.1)
        self.play(FadeIn(s2), FadeIn(t3), FadeIn(f3), dot.animate.move_to([5.7, -1.1, 0]), run_time=0.5)
        # the midpoint (5.5 s) holds: the engine line and Godogen's line

        a1_at(self, 4.75)
        t_a = a1_ml("The MIT License", TX, 0.0)
        t_b = a1_ml("Copyright 2026 Alex Ermolov", TX, -0.55)
        f_a = a1_mr("LICENSE.md", -2.8, 0.0)
        self.play(FadeIn(t_a), FadeIn(t_b), FadeIn(f_a), dot.animate.move_to([5.7, 0.0, 0]), run_time=0.5)
        a1_at(self, 6.7)
        self.play(dot.animate.move_to([5.7, -0.55, 0]), Indicate(t_b, scale_factor=1.06, color=INK), run_time=0.6)

        # the added layer lands on top
        a1_at(self, 8.4)
        s3 = Rectangle(width=SX1 - SX0, height=1.7, stroke_color=INK, stroke_width=4).move_to([(SX0 + SX1) / 2, 1.9, 0])
        t5 = a1_ml("2026-09-18", TX, 2.3)
        t6 = a1_ml("Added gdd/, the Zelda GDD skill", TX, 1.65)
        f5 = a1_mr("CHANGELOG.md", -2.8, 2.3)
        n5a = T("working copy:", 32).move_to([-4.45, 1.8, 0])
        n5b = T("not in public repo", 32).move_to([-4.45, 1.4, 0])
        top = VGroup(s3, t5, t6, f5)
        self.play(FadeIn(top, shift=DOWN * 0.6), dot.animate.move_to([5.7, 1.65, 0]), run_time=0.7)
        # "so far only in the working copy" (10.46 s): the label lands on those words
        a1_at(self, 10.35)
        self.play(FadeIn(n5a), FadeIn(n5b), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act2.py ══════════════════════════════
"""ACT II · The Loop and Who Decides  (B05–B07, all Manim)

One cast for the act: THE LOOP (six outlined nodes on a ring, one terracotta dot that travels it), then the same six steps as a
table of what each one produces and where it stops (the real table cells of Walker's workflow document, trimmed only with a visible
ellipsis), then the split between the agent and the human (the real README sentence cut at its semicolon).

Real material shown as itself:
- B05: frames of the REAL recorded run of the walker-claude Godot project (Godot 4.7.2 Movie Maker, scripted keyboard input,
  recorded 2026-10-09): pantry/a2_play_NNN.png are ffmpeg frames (15 per second, 960x540) of
  _conducting-series-evidence/godot-captures/walker-claude/walker-claude-jumpman-gameplay.mp4 from 0.3 s. It is the game the loop
  produces, played in the middle of the loop; it is not mapped to a step (the recording is not a play-test).
- B06: Walker docs/zelda-gdd-workflow.md lines 37-44, "Output / boundary" column.
- B07: Walker README.md lines 5-6.
Pacing: until() lands each motion on its spoken phrase (character share of the measured audio).
"""

A2P = "pantry/"
A2_FPS = 15.0
A2_NFRAMES = 93          # a2_play_001.png .. a2_play_093.png = clip time 0.3 s .. 6.5 s


def a2_lab(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a2_left(s, x, y, size=36, color=INK):
    """Text whose left edge sits at x (aligned_edge only; the position is an explicit coordinate)."""
    return T(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a2_right(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0], aligned_edge=RIGHT)


def a2_frame_tick(im, dt):
    """Updater: steps the real recorded frames in time (15 per second, from clip time 0.3 s)."""
    im.a2_t += dt
    k = min(A2_NFRAMES - 1, int(im.a2_t * A2_FPS) + im.a2_k0 - 1) + 1
    if k != im.a2_k:
        im.a2_k = k
        from PIL import Image
        arr = np.array(Image.open(A2P + "a2_play_%03d.png" % k).convert("RGBA"))
        im.pixel_array = arr


def a2_video(w, x, y, k0=1):
    """A moving picture of the real recording: an ImageMobject whose pixels step through the extracted frames."""
    im = ImageMobject(A2P + "a2_play_%03d.png" % k0)
    im.set_width(w)
    im.move_to([x, y, 0])
    im.a2_t, im.a2_k, im.a2_k0 = 0.0, k0, k0
    im.add_updater(a2_frame_tick)
    return im


# ───────────── the loop ring ─────────────
A2_CX, A2_CY, A2_RX, A2_RY = 0.0, -0.15, 4.0, 2.0
A2_STEPS = ["Game brief", "Build", "Play-test", "Inspect", "Revise", "Export"]
A2_ANG = [150, 90, 30, -30, -90, -150]       # clockwise from the upper left


def a2_pt(deg):
    r = np.radians(deg)
    return np.array([A2_CX + A2_RX * np.cos(r), A2_CY + A2_RY * np.sin(r), 0.0])


def a2_arc(d0, d1, color=INK, sw=6):
    """The ring between two angles (degrees, running clockwise: d0 > d1)."""
    return ParametricFunction(lambda t: a2_pt(t), t_range=[d1, d0], color=color, stroke_width=sw).reverse_points()


# ── B05 · the six steps as one loop ──────────────────────────────────────────────────────────────────────────────
class B05_TheLoop(Scene):
    def construct(self):
        title = a2_lab("The Loop and Who Decides", 0.0, 2.95, 40)
        self.add(title)
        ring = Ellipse(width=2 * A2_RX, height=2 * A2_RY, color=DIM, stroke_width=4).move_to([A2_CX, A2_CY, 0])
        self.add(ring)
        # the centre starts as the real GAME-BRIEF.md (its promise line, verbatim); the real recorded run replaces it on "Build"
        page = RoundedRectangle(width=5.4, height=2.7, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                stroke_width=4).move_to([0, A2_CY, 0])
        fname = M("GAME-BRIEF.md", 32).move_to([-2.45, A2_CY + 0.9, 0], aligned_edge=LEFT)
        q1 = a2_lab("I can see why that failed,", 0.0, A2_CY + 0.05, 34)
        q2 = a2_lab("and I want one more try.", 0.0, A2_CY - 0.5, 34)
        ln = a2_right("line 11", 2.45, A2_CY - 0.95, 32, DIM)
        card = VGroup(page, fname, q1, q2, ln)
        self.add(card)
        vid = a2_video(4.6, 0.0, A2_CY, k0=20)
        cap = a2_right("recorded run, scripted input", 6.0, -3.0, 32)      # appears with the recording
        # labels: beside their nodes (left nodes: to the left; right nodes: to the right; top above; bottom below)
        labs = VGroup(
            a2_right("Game brief", a2_pt(150)[0] - 0.45, a2_pt(150)[1], 36),
            a2_lab("Build", 0.0, a2_pt(90)[1] + 0.5, 36),
            a2_left("Play-test", a2_pt(30)[0] + 0.45, a2_pt(30)[1], 36),
            a2_left("Inspect", a2_pt(-30)[0] + 0.45, a2_pt(-30)[1], 36),
            a2_lab("Revise", 0.0, a2_pt(-90)[1] - 0.5, 36),
            a2_right("Export", a2_pt(-150)[0] - 0.45, a2_pt(-150)[1], 36))
        nodes = VGroup(*[Circle(radius=0.17, stroke_color=INK, stroke_width=5, fill_color=STAGE, fill_opacity=1).move_to(a2_pt(a))
                         for a in A2_ANG])
        self.play(LaggedStart(*[Create(n) for n in nodes], lag_ratio=0.3), run_time=1.3)     # "six steps": six nodes, one by one
        self.play(FadeIn(labs), run_time=0.4)
        until(self, "Game brief.", lead=0.3)                    # the dot arrives on "Game brief"
        dot = Dot(a2_pt(150), radius=0.14, color=TERRA).set_z_index(10)
        self.play(FadeIn(dot, scale=0.5), nodes[0].animate.set_fill(INK, opacity=1), run_time=0.2)
        # (midpoint: six nodes, six labels, the game playing in the middle, the dot on "Game brief")
        marks = [("Build", 150, 90), ("Play-test", 90, 30), ("Inspect", 30, -30), ("Revise", -30, -90), ("Export", -90, -150)]
        for i, (ph, a0, a1) in enumerate(marks):
            until(self, ph + ".", lead=0.45)
            path = a2_arc(a0, a1)
            drawn = path.copy()
            extra, rt = [], 0.35
            if i == 0:                                           # "Build": the brief gives way to the game it produced
                rt = guard(self, 0.35)                           # (settle the midpoint wait BEFORE the video is staged)
                self.add(vid)
                extra = [FadeOut(card), FadeIn(cap)]
            self.play(MoveAlongPath(dot, path), Create(drawn), nodes[i + 1].animate.set_fill(INK, opacity=1), *extra,
                      run_time=rt, rate_func=smooth)
        closing = a2_arc(-150, -210)                             # the loop closes: Export back round to the brief
        self.play(Create(closing), run_time=0.2)

        done(self)


# ── B06 · what each step produces, and where it stops ────────────────────────────────────────────────────────────
A2_ROWS = [("Game brief", "Human-reviewed target revision … authorized build"),
           ("Build", "Runnable project … not a completion claim"),
           ("Play-test", "Recorded attempts, … and human feedback"),
           ("Inspect", "Defects, … prioritized next change"),
           ("Revise", "New revision, … approvals may become stale"),
           ("Export", "Versioned package and evidence;")]
A2_RY0, A2_RSTEP = 1.8, 0.72           # first row's y, row spacing
A2_XS, A2_XC, A2_XBAR = -6.0, -3.6, 6.15


class B06_OutputAndBoundary(Scene):
    def construct(self):
        ys = [A2_RY0 - i * A2_RSTEP for i in range(6)]
        h1 = a2_left("Stage", A2_XS, 2.65, 34)
        h2 = a2_left("Output / boundary", A2_XC, 2.65, 34)
        rule = Line([-6.1, 2.3, 0], [6.1, 2.3, 0], color=DIM, stroke_width=4)
        steps = VGroup(*[a2_left(s, A2_XS, y, 32) for (s, _), y in zip(A2_ROWS, ys)])
        cells = VGroup(*[a2_left(c, A2_XC, y, 32) for (_, c), y in zip(A2_ROWS, ys)])
        self.play(FadeIn(h1), FadeIn(h2), Create(rule), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(VGroup(s, c), shift=UP * 0.1) for s, c in zip(steps, cells)], lag_ratio=0.2), run_time=0.9)
        until(self, "stops somewhere", lead=0.5)                # "and stops somewhere": a stop bar closes each row's boundary
        bars = VGroup(*[Line([A2_XBAR, y - 0.27, 0], [A2_XBAR, y + 0.27, 0], color=INK, stroke_width=9) for y in ys])
        self.play(LaggedStart(*[Create(b) for b in bars], lag_ratio=0.2), run_time=0.8)
        until(self, "Build produces", lead=0.25)                # the Build row comes forward, the others step back
        mark = Dot([-6.15, ys[1], 0], radius=0.09, color=TERRA)
        others = [i for i in range(6) if i != 1]
        self.play(*[steps[i].animate.set_color(DIM) for i in others], *[cells[i].animate.set_color(DIM) for i in others],
                  FadeIn(mark, scale=0.5), run_time=0.4)
        # (midpoint: the Build row in ink with its dot, the other five rows grey, a stop bar on every row)
        until(self, "Export produces", lead=0.25)               # the Export row comes forward
        mark2 = Dot([-6.15, ys[5], 0], radius=0.09, color=TERRA)
        self.play(steps[1].animate.set_color(DIM), cells[1].animate.set_color(DIM), steps[5].animate.set_color(INK),
                  cells[5].animate.set_color(INK), FadeOut(mark), FadeIn(mark2, scale=0.5), run_time=0.4)
        until(self, "Publishing", lead=0.2)                     # "Publishing is a separate step": an arrow runs on and stops at a wall
        arr = Arrow([A2_XBAR - 0.45, ys[5] - 0.1, 0], [A2_XBAR - 0.45, -2.35, 0], buff=0, color=INK, stroke_width=6,
                    tip_length=0.28, max_tip_length_to_length_ratio=0.5)
        wall = Line([-3.7, -2.5, 0], [6.1, -2.5, 0], color=INK, stroke_width=9)
        sep = a2_left("publication remains separate", -3.7, -2.95, 32)
        self.play(GrowArrow(arr), Create(wall), FadeIn(sep), run_time=0.7)
        done(self)


# ── B07 · the split, in one line ──────────────────────────────────────────────────────────────────────────────────
class B07_TheSplit(Scene):
    def construct(self):
        top = Line([-6.1, 3.05, 0], [6.1, 3.05, 0], color=INK, stroke_width=6)
        self.play(Create(top), run_time=0.6)                    # "stated in one line": one line
        until(self, "in one line", lead=-0.2)
        mid = Line([0, 3.05, 0], [0, -2.55, 0], color=INK, stroke_width=6)
        self.play(Create(mid), run_time=0.6)                    # ... and it splits
        until(self, "The agent helps", lead=0.2)
        robot = SVGMobject(A2P + "a2_robot_face.svg", stroke_color=INK, stroke_width=5, fill_opacity=0).scale_to_fit_height(1.6)
        robot.move_to([-3.2, 1.2, 0])
        h_a = a2_lab("Agent", -3.2, 2.45, 40)
        self.play(FadeIn(h_a), Create(robot), run_time=0.5)
        l1 = a2_lab("helps execute", -3.2, -0.25, 38)
        l2 = a2_lab("and check changes", -3.2, -0.9, 38)
        until(self, "execute and check", lead=0.15)
        ck = check(-0.7, -0.9, s=0.2, w=7)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.35)
        self.play(Create(ck), run_time=0.3)
        # (midpoint: the agent side complete: icon, "helps execute and check changes", a check; the human side still empty)
        until(self, "The human decides", lead=0.2)
        face = ImageMobject(A2P + "a2_professor_bear_avatar.png").scale_to_fit_height(1.6).move_to([3.2, 1.2, 0])
        h_h = a2_lab("Human", 3.2, 2.45, 40)
        self.play(FadeIn(h_h), FadeIn(face), run_time=0.5)
        r1 = VGroup(a2_lab("decides what", 3.2, -0.25, 38), a2_lab("the game should be", 3.2, -0.9, 38))
        self.play(FadeIn(r1), run_time=0.35)
        until(self, "whether it feels right", lead=0.35)
        r2 = VGroup(a2_lab("and whether", 3.2, -1.65, 38), a2_lab("it feels right", 3.2, -2.3, 38))
        spark = Dot([0.4, -2.3, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(r2), FadeIn(spark, scale=0.5), run_time=0.4)
        src = a2_lab("Walker README, lines 5 to 6", -3.2, -2.9, 32, DIM)
        self.play(FadeIn(src), run_time=0.3)
        done(self)


# ══════════════════════════════ scenes_act3.py ══════════════════════════════
"""ACT III · What the AI Must Not Do  (B08-B13, all Manim)

The material is Walker's own rules, quoted verbatim (<= 15 words, ellipsis where a cut is made) with the file and line they come from,
and one tag for where each rule lives: "installed" (publish.sh copies it into every game), "doc" (a framework document, NOT installed),
"game file" (the game's own hand-written file). Sources: EVID/research/walker-brief.md section 2 (rule numbers in factcheck/act3.md),
checked against the files themselves: walker/prompts/zelda-gdd.md, prompts/runtime.md, README.md, asset-gen/SKILL.md (line numbers are the
working tree of 2026-10-09, which is what the research brief cites); walker-jumpman-clawd/AGENTS.md, design/DESIGN-STATUS.json.
Real game frames in B11 are Godot's own output of the walker-claude project (EVID/godot-captures/walker-claude, scripted input recorded
2026-10-09), shown as frames of that recording.

One cast for the act: THE AGENT (a terracotta dot), THE LOOP (an outlined track), a BARRIER (a short ink bar the dot stops at), and the
rule SLIP (outlined card: verbatim quote, source in Menlo, where-it-lives tag). Pacing: every cue is set from the REAL word times of the
narration audio (evidence/act3/word_times.json, faster-whisper) through a3_at().
"""
import glob as _glob

A3_X0 = -6.2                    # left text margin (serif labels)
A3_LP = 0.5                     # line pitch of a size-34 serif quote
A3_TAG = {"I": "installed", "D": "doc", "G": "game file"}
A3_CACHE = {}


def a3_at(self, t):
    """Wait until absolute beat time t (seconds of the narration audio)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a3_tb(s, size, color):
    """EB Garamond with hidden bars at both ends (every label shares one ascender/descender box); returns (text, width of the two bars)."""
    t = T("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    bw = T("|a|", size, color).width - T("a", size, color).width
    return t, bw


def a3_tl(s, x, y, size=36, color=INK):
    """Serif label whose LEFT edge (of the visible text) sits at x: the hidden left bar hangs ~0.0025*size outside it (measured in
    Pango: |a| minus a is ~0.005 units per point of size; a constant, so Gate A's stub, which cannot measure text, sees sane coordinates)."""
    t, bw = a3_tb(s, size, color)
    return t.move_to([x - 0.0025 * size, y, 0], aligned_edge=LEFT)


def a3_tc(s, cx, y, size=36, color=INK):
    """Serif label CENTRED on cx (the two hidden bars are symmetric, so the text's centre is the visible centre)."""
    t, bw = a3_tb(s, size, color)
    return t.move_to([cx, y, 0])


def a3_tr(s, x, y, size=36, color=INK):
    t, bw = a3_tb(s, size, color)
    return t.move_to([x + 0.0025 * size, y, 0], aligned_edge=RIGHT)


def a3_tw(s, size=34):
    """Visible width of a serif string (cached)."""
    k = (s, size)
    if k not in A3_CACHE:
        t, bw = a3_tb(s, size, INK)
        A3_CACHE[k] = t.width - bw
    return A3_CACHE[k]


def a3_m(s, x, y, size=32, color=INK):
    """Menlo text whose first character cell starts at x (0.25 units per character at size 32)."""
    t = M("|" + s + "|", size, color)
    t[0].set_opacity(0)
    t[-1].set_opacity(0)
    return t.move_to([x - 0.243 * size / 32, y, 0], aligned_edge=LEFT)


def a3_cx(x, nch, size=32):
    """x of the END of a Menlo run of nch characters that starts at x."""
    return x + nch * 0.25 * size / 32


def a3_pill(word, x, y, size=32):
    """Outlined tag, left edge at x. Returns (VGroup, right edge x)."""
    w = a3_tw(word, size) + 0.5
    ring = RoundedRectangle(width=w, height=0.54, corner_radius=0.31, fill_opacity=0, stroke_color=DIM,
                            stroke_width=4).move_to([x + w / 2, y, 0])
    lab = a3_tl(word, x + 0.25, y, size)
    return VGroup(ring, lab), x + w


def a3_slip(lines, src, tag, x, ytop, w, size=34, stack=False):
    """The rule slip: outlined card with the verbatim quote (lines are wrapped BY HAND: Gate A's stub cannot measure text), the source
    (Menlo) and the where-it-lives pill. Returns (group, bottom y)."""
    pad = 0.25
    h = 2 * pad + len(lines) * A3_LP + (1.27 if stack else 0.72)
    card = RoundedRectangle(width=w, height=h, corner_radius=0.15, fill_opacity=0, stroke_color=DIM,
                            stroke_width=4).move_to([x + w / 2, ytop - h / 2, 0])
    g = VGroup(card)
    for i, ln in enumerate(lines):
        g.add(a3_tl(ln, x + pad, ytop - pad - (i + 0.5) * A3_LP, size))
    ys = ytop - pad - len(lines) * A3_LP - 0.37
    g.add(a3_m(src, x + pad, ys))
    if stack:    # narrow slip: the tag goes on its own row under the source
        pill, _ = a3_pill(A3_TAG[tag], x + pad, ys - 0.55)
    else:
        pill, _ = a3_pill(A3_TAG[tag], a3_cx(x + pad, len(src)) + 0.35, ys)
    g.add(pill)
    return g, ytop - h


def a3_bar(x, y, h=0.5):
    """A barrier: a short ink bar across a path."""
    return Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=INK, stroke_width=9)


def a3_check(x, y, s=0.2):
    return check(x, y, s, INK, 7)


def a3_cross(x, y, r=0.17, sw=7):
    return VGroup(Line([x - r, y + r, 0], [x + r, y - r, 0], color=INK, stroke_width=sw),
                  Line([x - r, y - r, 0], [x + r, y + r, 0], color=INK, stroke_width=sw))


def a3_bump(self, dot, bar, x_in, x_back, y):
    """The agent walks into the barrier, is stopped, and comes back."""
    self.play(dot.animate.move_to([x_in, y, 0]), run_time=0.24)
    self.play(Indicate(bar, scale_factor=1.5, color=INK), run_time=0.22)
    self.play(dot.animate.move_to([x_back, y, 0]), run_time=0.2)


# ── B08 · scope (ACT TITLE) ─────────────────────────────────────────────────────────────────────────────────────────────
# zelda-gdd.md:13 (engines) and :40 (just to keep a loop running); the agent walks the loop and is stopped at each exit.
A3_STUBS = [("switch engine", 1.7), ("cut requirements", 1.05), ("extend schedule", 0.4), ("spend money", -0.25), ("publish", -0.9)]


class B08_Scope(Scene):
    def construct(self):
        title = a3_tl("What the AI Must Not Do", A3_X0, 3.0, 40)
        self.add(title)
        loop_pts = [[0.9, 2.3, 0], [1.9, 2.3, 0], [1.9, -1.25, 0], [0.9, -1.25, 0], [0.9, 2.3, 0]]
        track = VMobject(stroke_color=DIM, stroke_width=5).set_points_as_corners(loop_pts)
        dot = Dot([1.9, 2.3, 0], radius=0.15, color=TERRA)
        agent = a3_tl("the agent", 2.3, 2.3, 32)
        loopl = a3_tc("loop", 1.4, 0.6, 32)
        self.play(Create(track), run_time=0.7)
        self.play(FadeIn(dot), FadeIn(agent), FadeIn(loopl), run_time=0.4)
        a3_at(self, 2.5)
        scope = a3_tl("scope", 0.9, 3.0, 36)
        self.play(FadeIn(scope), run_time=0.3)
        # the where-it-lives legend (the first tag the viewer sees)
        a3_at(self, 3.2)
        leg = VGroup()
        for i, (k, gloss) in enumerate((("I", "in every game"), ("D", "framework only"), ("G", "that game's own"))):
            pill, _ = a3_pill(A3_TAG[k], 0.9, -1.85 - 0.57 * i)
            leg.add(pill, a3_tl(gloss, 3.25, -1.85 - 0.57 * i, 32, INK))
        s1, b1 = a3_slip(["“Do not silently use Unity,", "Bevy, Babylon.js, or a hosted", "game generator.”"],
                         "zelda-gdd.md:13", "D", -6.1, 2.5, 6.5)
        self.play(FadeIn(s1), FadeIn(leg), run_time=0.45)
        # stub 1 (engines) and the agent stopped at it
        stubs = [Line([1.9, y, 0], [2.9, y, 0], color=DIM, stroke_width=4) for lab, y in A3_STUBS]
        bars = [a3_bar(2.9, y) for lab, y in A3_STUBS]
        labs = [a3_tl(lab, 3.2, y, 32) for lab, y in A3_STUBS]
        a3_at(self, 3.85)
        self.play(Create(stubs[0]), Create(bars[0]), FadeIn(labs[0]), run_time=0.3)
        self.play(dot.animate.move_to([1.9, 1.7, 0]), run_time=0.15)
        a3_bump(self, dot, bars[0], 2.62, 1.9, 1.7)
        # the cut-requirements rule, then the other four exits drawn before the midpoint
        a3_at(self, 4.75)
        s2, b2 = a3_slip(["“Do not cut requirements,", "extend schedules, spend, publish", "… just to keep a loop running.”"],
                         "zelda-gdd.md:40", "D", -6.1, b1 - 0.15, 6.5)
        self.play(FadeIn(s2), Create(VGroup(*stubs[1:])), Create(VGroup(*bars[1:])), FadeIn(VGroup(*labs[1:])), run_time=0.7)
        for i, t in ((1, 6.36), (2, 7.52), (3, 8.4), (4, 9.08)):
            lab, y = A3_STUBS[i]
            a3_at(self, t - 0.62)
            self.play(dot.animate.move_to([1.9, y, 0]), run_time=0.16)
            a3_bump(self, dot, bars[i], 2.62, 1.9, y)
        # "just to keep the loop running": the agent runs the whole loop
        a3_at(self, 9.72)
        run = VMobject().set_points_as_corners([[1.9, -0.9, 0], [1.9, -1.25, 0], [0.9, -1.25, 0], [0.9, 2.3, 0], [1.9, 2.3, 0]])
        self.play(MoveAlongPath(dot, run), run_time=1.5)
        done(self)


# ── B09 · drafting is not permission (zelda-gdd.md:44 and :21) ──────────────────────────────────────────────────────────
class B09_DraftNotPermission(Scene):
    def construct(self):
        spine = Line([-5.6, 1.5, 0], [-5.6, -2.2, 0], color=DIM, stroke_width=4)
        p_draft = Line([-5.6, 1.5, 0], [-4.85, 1.5, 0], color=DIM, stroke_width=4)
        p_appr = Line([-5.6, -0.55, 0], [-4.2, -0.55, 0], color=DIM, stroke_width=4)
        p_run = Line([-5.6, -2.2, 0], [-4.2, -2.2, 0], color=DIM, stroke_width=4)
        bar_appr, bar_run = a3_bar(-4.2, -0.55, 0.8), a3_bar(-4.2, -2.2, 0.8)
        page = RoundedRectangle(width=2.2, height=2.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                stroke_width=5).move_to([-3.7, 1.5, 0])
        slot = DashedVMobject(RoundedRectangle(width=2.4, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                               stroke_width=4).move_to([-2.75, -0.55, 0]), num_dashes=28)
        runbox = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                  stroke_width=4).move_to([-2.95, -2.2, 0])
        draft_l = a3_tl("draft", -4.8, 2.85, 36)
        appr_l = a3_tl("approval", -3.55, -0.55, 32)
        run_l = a3_tl("run", -3.7, -2.2, 32)
        dot = Dot([-5.6, 1.5, 0], radius=0.15, color=TERRA)
        self.add(draft_l, page, appr_l, run_l)
        self.play(Create(VGroup(spine, p_draft, p_appr, p_run)), Create(VGroup(bar_appr, bar_run)), Create(slot), Create(runbox),
                  FadeIn(dot), run_time=0.7)
        # the draft is written line by line
        ends = [-2.95, -3.15, -2.9, -3.35, -3.05]
        ys = [2.15, 1.8, 1.45, 1.1, 0.75]
        lns = [Line([-4.5, y, 0], [e, y, 0], color=DIM, stroke_width=5) for y, e in zip(ys, ends)]
        a3_at(self, 0.35)
        s1, b1 = a3_slip(["\u201cDrafting tasks is not", "authorization to", "execute them.\u201d"], "zelda-gdd.md:44", "D", 0.2, 2.0, 5.95)
        self.play(LaggedStart(*[Create(l) for l in lns[:3]], lag_ratio=0.35), FadeIn(s1), run_time=0.9)
        # "not permission to run it": the agent goes to the run exit and is stopped
        a3_at(self, 1.25)
        self.play(dot.animate.move_to([-5.6, -2.2, 0]), run_time=0.3)
        a3_bump(self, dot, bar_run, -4.55, -5.6, -2.2)
        self.play(dot.animate.move_to([-5.6, 1.5, 0]), run_time=0.3)
        # "A direct request for a complete draft allows the draft": the quote changes, the page fills
        a3_at(self, 2.55)
        s2, b2 = a3_slip(["\u201c\u2026 authorizes drafting with", "named assumptions; it does", "not authorize inventing", "approvals \u2026\u201d"],
                         "zelda-gdd.md:21", "D", 0.2, 2.0, 5.95)
        self.play(FadeOut(s1), FadeIn(s2), run_time=0.4)
        a3_at(self, 3.7)
        self.play(LaggedStart(*[Create(l) for l in lns[3:]], lag_ratio=0.5), run_time=0.7)
        a3_at(self, 4.3)
        self.play(dot.animate.move_to([-4.95, 1.5, 0]), run_time=0.3)
        # "with its assumptions named"
        a3_at(self, 5.75)
        asm = VGroup(a3_tl("assumptions", -2.3, 2.15, 36))
        for y in (1.55, 1.1, 0.65):
            asm.add(Dot([-2.15, y, 0], radius=0.06, color=DIM), Line([-1.9, y, 0], [-0.5, y, 0], color=DIM, stroke_width=5))
        self.play(FadeIn(asm), run_time=0.5)
        # "does not allow inventing approvals": the agent goes to the approval slot and is stopped; the slot stays empty
        a3_at(self, 7.05)
        self.play(dot.animate.move_to([-5.6, 1.5, 0]), run_time=0.2)
        self.play(dot.animate.move_to([-5.6, -0.55, 0]), run_time=0.3)
        a3_bump(self, dot, bar_appr, -4.55, -5.6, -0.55)
        done(self)


# ── B10 · four gates, signed by humans only (C/design/DESIGN-STATUS.json:10-13 and :19) ────────────────────────────────
A3_GATES = [("vision", -3.9, "  "), ("systems", -1.4, " "), ("world", 1.1, "   "), ("scope", 3.6, "   ")]


class B10_FourGates(Scene):
    def construct(self):
        path = Line([-6.0, 2.5, 0], [6.0, 2.5, 0], color=DIM, stroke_width=4)
        dot = Dot([-5.8, 2.5, 0], radius=0.15, color=TERRA)
        self.add(path)
        self.play(FadeIn(dot), run_time=0.4)
        bars, labs = [], []
        for (name, gx, _), t in zip(A3_GATES, (0.92, 1.34, 2.2, 2.62)):
            a3_at(self, t)
            b = a3_bar(gx, 2.5, 0.9)
            lb = a3_tc(name, gx, 1.8, 36)
            bars.append(b)
            labs.append(lb)
            self.play(Create(b), FadeIn(lb), run_time=0.3)
        # the real status file: every gate unsigned
        a3_at(self, 2.95)
        head = a3_m("DESIGN-STATUS.json:10-13, 19", -6.0, 1.0)
        pill, _ = a3_pill(A3_TAG["G"], a3_cx(-6.0, 28) + 0.35, 1.0)
        rows, nulls = VGroup(), []
        for i, (name, gx, pad) in enumerate(A3_GATES):
            y = 0.3 - 0.7 * i
            pre = f'  "{name}":{pad}{{"signed_by": '
            rows.add(a3_m(pre + "null, …},", -6.0, y))
            nulls.append(rows[-1])
        notes = a3_m('"notes": "… Gates are signed by humans only."', -6.0, -2.7)
        self.play(FadeIn(head), FadeIn(pill), FadeIn(rows), FadeIn(notes), run_time=0.5)
        # "The agent never signs a gate": it walks to the first gate and is stopped; every signed_by is still null
        a3_at(self, 4.75)
        self.play(dot.animate.move_to([-4.3, 2.5, 0]), run_time=0.6)
        self.play(Indicate(bars[0], scale_factor=1.5, color=INK), run_time=0.25)
        self.play(LaggedStart(*[Indicate(n, scale_factor=1.06, color=INK) for n in nulls], lag_ratio=0.3), run_time=1.1)
        done(self)


# ── B11 · proof (runtime.md:10, README.md:28, AGENTS.md:13, zelda-gdd.md:52) ───────────────────────────────────────────
# The picture is the REAL running game (frames of walker-claude-jumpman-gameplay.mp4, scripted input recorded 2026-10-09, every 3rd
# frame = 10 fps in pantry/a3_run_001..072.jpg). The rule slips swap in the right column; four small cards light up in turn.
A3_RUN = "pantry/a3_run_%03d.jpg"
A3_RUN_N = 72


def a3_run_window(self, cx, cy, w, t0, speed=1.0):
    """The recorded run as an ImageMobject whose pixels follow scene time (an updater): frame k shows from t0 + k*0.1/speed;
    it loops (the run is 7.2 s). Returns the image."""
    img = ImageMobject(A3_RUN % 1).scale_to_fit_width(w).move_to([cx, cy, 0])
    st = {"t": -t0, "i": 0}

    def up(m, dt):
        st["t"] += dt
        i = int(st["t"] * speed / 0.1) % A3_RUN_N
        if i != st["i"]:
            st["i"] = i
            try:
                from PIL import Image as _PI
                m.pixel_array = np.array(_PI.open(A3_RUN % (i + 1)).convert("RGBA"))
            except Exception:
                pass
    img.add_updater(up)
    return img


def a3_glyph(k, cx, cy):
    """The four small proof glyphs (B11 cards)."""
    if k == 0:       # a running game: a screen with a play triangle
        return VGroup(RoundedRectangle(width=0.95, height=0.6, corner_radius=0.08, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0]),
                      Polygon([cx - 0.12, cy - 0.16, 0], [cx - 0.12, cy + 0.16, 0], [cx + 0.18, cy, 0], fill_color=INK, fill_opacity=1,
                              stroke_width=0))
    if k == 1:       # build passed  !=  a human played it
        return VGroup(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([cx - 0.62, cy, 0]),
                      a3_check(cx - 0.62, cy, 0.14),
                      Line([cx - 0.2, cy + 0.09, 0], [cx + 0.2, cy + 0.09, 0], color=INK, stroke_width=6),
                      Line([cx - 0.2, cy - 0.09, 0], [cx + 0.2, cy - 0.09, 0], color=INK, stroke_width=6),
                      Line([cx - 0.12, cy - 0.26, 0], [cx + 0.12, cy + 0.26, 0], color=INK, stroke_width=6),
                      DashedVMobject(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.06, fill_opacity=0, stroke_color=DIM,
                                                      stroke_width=4).move_to([cx + 0.62, cy, 0]), num_dashes=16))
    if k == 2:       # an invented pass: an empty (dashed) result, crossed
        return VGroup(DashedVMobject(RoundedRectangle(width=0.95, height=0.6, corner_radius=0.08, fill_opacity=0, stroke_color=DIM,
                                                      stroke_width=4).move_to([cx, cy, 0]), num_dashes=24),
                      a3_cross(cx, cy, 0.17, 7))
    # k == 3: a weakened test: the pass line is pushed down
    return VGroup(Line([cx - 0.55, cy + 0.24, 0], [cx + 0.2, cy + 0.24, 0], color=DIM, stroke_width=5),
                  Arrow([cx - 0.3, cy + 0.2, 0], [cx - 0.3, cy - 0.28, 0], buff=0, color=INK, stroke_width=6, tip_length=0.16),
                  a3_cross(cx + 0.45, cy - 0.02, 0.15, 7))


A3_B11_CARDS = [("running game", -4.675), ("not a play-test", -1.555), ("invented passes", 1.565), ("weakened test", 4.685)]


class B11_Proof(Scene):
    def construct(self):
        cx, cy, w = -3.15, 1.14, 5.9
        h = w * 9 / 16
        frame = RoundedRectangle(width=w + 0.2, height=h + 0.2, corner_radius=0.1, fill_opacity=0, stroke_color=DIM,
                                 stroke_width=4).move_to([cx, cy, 0])
        win = a3_run_window(self, cx, cy, w, -0.55)
        cap1 = a3_tl("recorded run, looping", cx - w / 2, -0.95, 36)
        cap2 = a3_tl("scripted input, 2026-10-09", cx - w / 2, -1.4, 32, DIM)
        cap2b = a3_tl("scripted input: not a play-test", cx - w / 2, -1.4, 32, DIM)
        self.add(win, frame, cap1, cap2)
        # While the voice says "build is not a play-test" the real run steps aside (a real game frame is read by GATE T as text and
        # terracotta, so the 50% frame must not hold one) and the same idea is drawn large; the run returns after the midpoint.
        bx, by = -5.3, 1.3
        big = VGroup(RoundedRectangle(width=1.8, height=1.8, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([bx, by, 0]),
                     check(bx, by, 0.5, INK, 10),
                     a3_tc("build", bx, 0.0, 36),
                     Line([-3.9, by + 0.22, 0], [-3.1, by + 0.22, 0], color=INK, stroke_width=9),
                     Line([-3.9, by - 0.22, 0], [-3.1, by - 0.22, 0], color=INK, stroke_width=9),
                     Line([-3.65, by - 0.65, 0], [-3.35, by + 0.65, 0], color=INK, stroke_width=9),
                     DashedVMobject(RoundedRectangle(width=1.8, height=1.8, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                                     stroke_width=5).move_to([-1.7, by, 0]), num_dashes=36),
                     a3_tc("human play-test", -1.7, 0.0, 36))
        slips = [
            (["“Judge progress from the", "running game, never from a", "clean build …”"], "runtime.md:10", "I"),
            (["“A successful build is not", "evidence of a successful", "human playtest.”"], "README.md:28", "D"),
            (["“Never invent human", "playtests, … approvals or", "test passes.”"], "AGENTS.md:13", "G"),
            (["“… instead of weakening", "the test to make it pass.”"], "zelda-gdd.md:52", "D")]
        cur = None
        times = [0.3, 3.45, 6.85, 11.3]
        for k, (lines, src, tag) in enumerate(slips):
            a3_at(self, times[k])
            sl, _ = a3_slip(lines, src, tag, 0.3, 2.8, 5.85)
            pill = sl[-1]
            if k == 2:      # the "game file" pill lands on "The game's own file adds" (7.4 s); the quote is already up before the midpoint
                sl.remove(pill)
            # the card for this rule, lit as the rule is spoken
            lab, ccx = A3_B11_CARDS[k]
            card = RoundedRectangle(width=2.85, height=1.3, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                    stroke_width=4).move_to([ccx, -2.45, 0])
            glyph = a3_glyph(k, ccx, -2.2)
            label = a3_tc(lab, ccx, -2.82, 32)
            if cur is None:
                self.play(FadeIn(sl), FadeIn(card), Create(glyph), FadeIn(label), run_time=0.45)
            else:
                self.play(FadeOut(cur), FadeIn(sl), FadeIn(card), Create(glyph), FadeIn(label), run_time=0.45)
            cur = sl
            if k == 1:      # the run steps aside while the build/play-test idea is drawn large
                a3_at(self, 5.6)
                self.play(FadeOut(win), FadeOut(frame), FadeOut(cap1), FadeOut(cap2), Create(big), run_time=0.45)
            if k == 2:      # pill on the words, then the run returns after the midpoint, captioned as what it is: scripted input
                a3_at(self, 7.6)
                sl.add(pill)
                self.play(FadeIn(pill), FadeOut(big), FadeIn(win), FadeIn(frame), FadeIn(cap1), FadeIn(cap2b), run_time=0.45)
        done(self)


# ── B12 · money and safety (runtime.md:4, asset-gen SKILL.md:92, README.md:71 and :63, zelda-gdd.md:56) ──────────────────
# Three zones, side by side (money | credentials | publishing). The headers are on screen from the first frame; each zone draws on its cue.
# The prices are asset-gen's own quick-reference line (asset-gen/SKILL.md:92), quoted as written, not checked against today's price lists.
class B12_MoneySafety(Scene):
    def construct(self):
        ax, bx, cx = -6.1, -1.4, 2.35
        hA, hB, hC = a3_tl("money", ax, 3.0, 36), a3_tl("credentials", bx, 3.0, 36), a3_tl("publishing", cx, 3.0, 36)
        self.add(hA, hB, hC)
        # zone A: what a call costs (hero number), then the agent stopped at "confirm" before the first paid call
        src_l = a3_m("SKILL.md:92", -4.4, 2.2)
        path = Line([-5.9, 0.85, 0], [-4.5, 0.85, 0], color=DIM, stroke_width=4)
        bar = a3_bar(-4.5, 0.85, 0.7)
        box = DashedVMobject(RoundedRectangle(width=1.5, height=0.7, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                              stroke_width=4).move_to([-3.45, 0.85, 0]), num_dashes=22)
        boxl = a3_tc("call", -3.45, 0.85, 32)
        conf = a3_tl("confirm", -2.55, 0.85, 32)
        dot = Dot([-5.8, 0.85, 0], radius=0.15, color=TERRA)
        a3_at(self, 1.5)
        self.play(FadeIn(src_l), Create(path), Create(bar), Create(box), FadeIn(boxl), FadeIn(dot), run_time=0.5)
        cur = None
        for (num, lab), t in zip((("2¢", "asset-gen: sprite"), ("37¢", "asset-gen: 3D asset"), ("≈92¢", "asset-gen: rigged character")), (2.1, 3.1, 4.0)):
            a3_at(self, t)
            pair = VGroup(a3_tl(num, ax, 2.2, 56), a3_tl(lab, ax, 1.6, 32))
            self.play(*([FadeOut(cur)] if cur is not None else []), FadeIn(pair), run_time=0.3)
            cur = pair
        a3_at(self, 4.85)
        sA, _ = a3_slip(["“Confirm the spend …", "before the first paid", "generation.”"], "runtime.md:4", "I", ax, 0.0, 4.5, 32, stack=True)
        self.play(FadeIn(sA), run_time=0.4)
        a3_at(self, 5.45)
        self.play(dot.animate.move_to([-4.85, 0.85, 0]), FadeIn(conf), run_time=0.35)
        self.play(Indicate(bar, scale_factor=1.5, color=INK), run_time=0.25)
        self.play(dot.animate.move_to([-5.8, 0.85, 0]), run_time=0.25)
        # the other two zones' containers are laid out before the midpoint; their rules arrive on their own cues
        a3_at(self, 6.15)
        bbar = a3_bar(0.55, 1.9, 0.9)
        bbox = RoundedRectangle(width=1.4, height=0.95, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([1.5, 1.9, 0])
        bboxl = a3_tc("commit", 1.5, 1.9, 32)
        comp = RoundedRectangle(width=1.35, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.5, 1.9, 0])
        compl = a3_tc("computer", 3.5, 1.2, 32)
        gh = RoundedRectangle(width=1.2, height=1.0, corner_radius=0.12, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([5.5, 1.9, 0])
        ghl = a3_tc("GitHub", 5.5, 1.2, 32)
        self.play(Create(bbar), Create(bbox), FadeIn(bboxl), Create(comp), FadeIn(compl), Create(gh), FadeIn(ghl), run_time=0.6)
        # zone B: a key goes toward the commit and is stopped
        a3_at(self, 7.3)
        ring = Circle(radius=0.22, color=INK, stroke_width=6).move_to([-1.0, 1.9, 0])
        shaft = Line([-0.78, 1.9, 0], [-0.05, 1.9, 0], color=INK, stroke_width=6)
        teeth = VGroup(Line([-0.3, 1.9, 0], [-0.3, 1.68, 0], color=INK, stroke_width=6), Line([-0.05, 1.9, 0], [-0.05, 1.68, 0], color=INK, stroke_width=6))
        key = VGroup(ring, shaft, teeth)
        sB, _ = a3_slip(["“Never commit", "credentials.”"], "README.md:71", "D", bx, 0.0, 3.55, 32, stack=True)
        self.play(FadeIn(key), FadeIn(sB), run_time=0.5)
        a3_at(self, 7.95)
        self.play(key.animate.shift(RIGHT * 0.55), run_time=0.3)
        self.play(Indicate(bbar, scale_factor=1.5, color=INK), run_time=0.25)
        self.play(key.animate.shift(LEFT * 0.55), run_time=0.25)
        # zone C: files written on the computer are not an upload to GitHub
        a3_at(self, 8.85)
        sC, _ = a3_slip(["“… write runtime", "files locally, not", "upload to GitHub.”"], "README.md:63", "D", cx, 0.0, 3.8, 32, stack=True)
        self.play(FadeIn(sC), run_time=0.5)
        a3_at(self, 9.3)
        page = RoundedRectangle(width=0.4, height=0.55, corner_radius=0.05, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([3.5, 1.9, 0])
        pl = VGroup(*[Line([3.37, 1.9 + dy, 0], [3.63, 1.9 + dy, 0], color=DIM, stroke_width=4) for dy in (0.1, -0.02, -0.14)])
        self.play(Create(page), Create(pl), run_time=0.4)
        a3_at(self, 10.9)
        arr = Line([4.18, 1.9, 0], [4.9, 1.9, 0], color=DIM, stroke_width=4)
        cbar = a3_bar(4.5, 1.9, 0.7)
        self.play(Create(arr), Create(cbar), run_time=0.35)
        a3_at(self, 12.3)
        sep = a3_tc("separate action", 4.5, 0.6, 32)
        self.play(FadeIn(sep), Indicate(cbar, scale_factor=1.5, color=INK), run_time=0.5)
        done(self)


# ── B13 · size: one reviewable change, and the failure predicted first (C/AGENTS.md:11) ─────────────────────────────────
# The grid is a DRAWING of an idea (a game as a few cells), not a game capture; "one change" is one cell, "predicted failure" is a note
# written before the cell is built.
class B13_OneChange(Scene):
    def construct(self):
        gx0, gy0, cw, ch = 0.7, 2.6, 1.35, 1.15
        hdr = a3_tl("the game", gx0, 2.95, 36)
        self.add(hdr)
        cells = VGroup(*[Rectangle(width=cw, height=ch, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to(
            [gx0 + cw * (c + 0.5), gy0 - ch * (r + 0.5), 0]) for r in range(3) for c in range(4)])
        self.play(Create(cells), run_time=0.7)
        a3_at(self, 0.45)
        sl, _ = a3_slip(["“Make one reviewable change.", "Predict a failure, preserve", "unrelated behavior …”"], "AGENTS.md:11", "G", -6.1, 1.3, 6.4)
        self.play(FadeIn(sl), run_time=0.4)
        # "Make one reviewable change": ONE cell is marked
        a3_at(self, 0.9)
        tx, ty = gx0 + cw * 2.5, gy0 - ch * 2.5
        one = Rectangle(width=cw, height=ch, stroke_color=INK, stroke_width=9, fill_opacity=0).move_to([tx, ty, 0])
        one_l = a3_tr("one change", gx0 + cw * 4, 2.95, 36)
        pt = Dot([tx, ty + ch / 2 + 0.28, 0], radius=0.0)
        self.play(Create(one), FadeIn(one_l), run_time=0.5)
        # "Predict how it could fail": the note is written first, pointing at the cell
        a3_at(self, 2.9)
        note = RoundedRectangle(width=3.4, height=0.8, corner_radius=0.14, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([tx, -1.85, 0])
        note_l = a3_tc("predicted failure", tx, -1.85, 32)
        arr = Arrow([tx, -1.45, 0], [tx, -0.98, 0], buff=0, color=INK, stroke_width=6, tip_length=0.18)
        self.play(FadeIn(note), FadeIn(note_l), Create(arr), run_time=0.5)
        # "before you build it": only then is the cell built (the agent's dot lands in it)
        a3_at(self, 4.3)
        built = Dot([tx, ty, 0], radius=0.17, color=TERRA)
        self.play(GrowFromCenter(built), run_time=0.4)
        done(self)


# ══════════════════════════════ scenes_act4.py ══════════════════════════════
"""ACT IV · How the AI Writes Code  (B14-B17, all Manim)

Cast for the act: the REAL text of the installed Godot guide (godot.md, lines 3 / 10 / 49) and the installed manifest line
(CLAUDE.md:10), the four conventions of the GDScript prompt (godot-scripting-conventions-research-prompt.md, lines 136-168) with
their own example lines, the three-way disagreement (godot.md:3 C#, /gdd p3.md:6 typed GDScript, the real walker-claude/godot tree:
0 .cs / 0 .csproj / 11 .gd, counted 2026-10-09) and the REAL installed tree of the publisher run (installed-tree.txt: 54 files, none
ending .gd). Every quote is <= 15 words, cut with a visible ellipsis, and carries its file:line. Nothing is a mock-up of an interface:
the files are shown as text, which is what they are. Sources and counts: factcheck/act4.md.
Pacing: until(self, "exact phrase", lead) waits for the spoken word; nothing straddles the clip midpoint (the kit's guard).
"""


def a4_L(mob, x, y):
    """Place a text left-aligned at x (explicit coordinates; never read back a text's edge)."""
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def a4_at(self, t):
    """Wait until the clip clock reaches t seconds (t from faster-whisper word times, evidence/act4/word_times.json, minus a lead).
    Used by B15 and B17, whose narration was re-voiced on 2026-10-09."""
    g = t - _elapsed(self)
    if g > 0.03:
        self.wait(g)


def a4_C(mob, x, y):
    return mob.move_to([x, y, 0])


def a4_page(x, y, w=0.46, h=0.58, fold=0.16, color=INK, fill=CARD):
    """A small page mark (dog-eared top right) centred at (x, y)."""
    l, r, t, b = x - w / 2, x + w / 2, y + h / 2, y - h / 2
    return Polygon([l, t, 0], [r - fold, t, 0], [r, t - fold, 0], [r, b, 0], [l, b, 0],
                   fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)


def a4_slab(x, y, w, h, stroke=DIM, fill=None, sw=5):
    """A flat slab drawn as a Polygon (a Rectangle would not count as a new shape for Gate A)."""
    pts = [[x - w / 2, y + h / 2, 0], [x + w / 2, y + h / 2, 0], [x + w / 2, y - h / 2, 0], [x - w / 2, y - h / 2, 0]]
    if fill is None:
        return Polygon(*pts, stroke_color=stroke, stroke_width=sw, fill_opacity=0)
    return Polygon(*pts, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=1)


def a4_down(x, y0, y1, w=5, tip=0.12):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=INK, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.5)


# ═════════════════════════════ B14 · ACT TITLE · layer one: the installed Godot guide ═════════════════════════════
class B14_LayerOneGuide(Scene):
    def construct(self):
        title = a4_L(T("How the AI Writes Code", 40), -6.1, 3.05)
        self.add(title)
        until(self, "in two layers", lead=0.6)
        s2 = a4_slab(4.95, 3.0, 2.5, 0.46)
        s1 = a4_slab(4.95, 2.4, 2.5, 0.46)
        n2 = a4_C(T("2", 36), 3.35, 3.0)
        n1 = a4_C(T("1", 36), 3.35, 2.4)
        self.play(Create(s1), FadeIn(n1), run_time=0.3)
        self.play(Create(s2), FadeIn(n2), run_time=0.3)
        until(self, "Layer one is installed", lead=0.3)
        spark = Dot([4.95, 2.4, 0], radius=0.11, color=TERRA)
        chip = a4_L(T("Layer one: installed in every game", 36), -6.1, 2.4)
        frame = Rectangle(width=12.2, height=4.6, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, -0.5, 0])
        vdiv = Line([1.4, 1.8, 0], [1.4, -2.8, 0], color=DIM, stroke_width=4)
        page = a4_page(-5.75, 1.35)
        fname = a4_L(M("godot.md", 32), -5.3, 1.35)
        self.play(FadeIn(spark, scale=0.4), FadeIn(chip), Create(frame), Create(vdiv), FadeIn(page), FadeIn(fname), run_time=0.55)
        # the build gate, in order (godot.md:10)
        ys = [0.65, -0.3, -1.55]
        cmds = ["dotnet build", "godot --headless --import", "godot --headless --quit"]
        nums = [a4_C(T(str(i + 1), 36), -5.8, ys[i]) for i in range(3)]
        lines = [a4_L(M(c, 32), -5.3, ys[i]) for i, c in enumerate(cmds)]
        qual = a4_L(T("after asset changes", 32), -4.5, -0.82)
        a1 = a4_down(-5.8, 0.38, -0.0)
        a2 = a4_down(-5.8, -0.55, -1.25)
        until(self, "It says build", lead=0.3)
        self.play(FadeIn(nums[0]), FadeIn(lines[0]), run_time=0.3)
        until(self, "then import", lead=0.35)
        self.play(GrowArrow(a1), FadeIn(nums[1]), FadeIn(lines[1]), FadeIn(qual), run_time=0.3)
        until(self, "then run headless", lead=0.3)
        self.play(GrowArrow(a2), FadeIn(nums[2]), FadeIn(lines[2]), run_time=0.35)
        # verify against the installed Godot (godot.md:49)
        until(self, "Verify against", lead=0.3)
        v1 = a4_L(T("\u201cVerify against the", 32), 1.85, 1.15)
        v2 = a4_L(T("installed Godot \u2026\u201d", 32), 1.85, 0.65)
        vs = a4_L(M("godot.md:49", 32), 1.85, 0.1)
        lens = Circle(radius=0.2, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([5.55, 0.95, 0])
        handle = Line([5.69, 0.81, 0], [5.9, 0.6, 0], color=DIM, stroke_width=7)
        self.play(FadeIn(v1), FadeIn(v2), FadeIn(vs), Create(lens), Create(handle), run_time=0.5)
        sep = Line([1.85, -0.45, 0], [5.95, -0.45, 0], color=DIM, stroke_width=3)
        # judge from the running game (CLAUDE.md:10)
        until(self, "And judge from the running game", lead=0.35)
        j1 = a4_L(T("\u201cJudge progress from", 32), 1.85, -1.0)
        j2 = a4_L(T("the running game \u2026\u201d", 32), 1.85, -1.5)
        js = a4_L(M("CLAUDE.md:10", 32), 1.85, -2.05)
        ring = Circle(radius=0.28, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([5.45, -2.05, 0])
        tri = Polygon([5.36, -1.9, 0], [5.36, -2.2, 0], [5.62, -2.05, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
        self.play(Create(sep), FadeIn(j1), FadeIn(j2), FadeIn(js), Create(ring), FadeIn(tri, scale=0.4), run_time=0.5)
        done(self)


# ═════════════════════════════ B15 · layer two: four conventions, each with its own line ═════════════════════════════
class B15_LayerTwoConventions(Scene):
    def construct(self):
        head = a4_L(T("Layer two: conventions for GDScript", 40), -6.1, 3.0)
        fname = a4_L(M("godot-scripting-conventions-research-prompt.md", 32), -6.1, 2.3)
        s2 = a4_slab(5.0, 3.0, 2.0, 0.46)
        n2 = a4_C(T("2", 36), 3.75, 3.0)
        spark = Dot([5.0, 3.0, 0], radius=0.11, color=TERRA)
        rules = VGroup(*[Line([-6.1, y, 0], [6.1, y, 0], color=GHOST, stroke_width=3) for y in (1.95, 0.8, -0.65, -1.62)])
        self.add(head, s2, n2, spark, rules)
        a4_at(self, 0.7)
        self.play(FadeIn(fname), run_time=0.4)
        TAGX, X0 = -3.95, -3.25
        # row 1 · type every variable
        a4_at(self, 2.65)
        box = a4_slab(-5.7, 1.35, 0.62, 0.62, stroke=INK, sw=5)
        tag = Polygon([-5.28, 1.62, 0], [-4.82, 1.62, 0], [-4.62, 1.35, 0], [-4.82, 1.08, 0], [-5.28, 1.08, 0],
                      fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5)
        t1 = a4_C(M("L137", 32), TAGX, 1.35)
        r1 = a4_L(M("var hp: int = 100", 32), X0, 1.35)
        self.play(Create(box), FadeIn(t1), FadeIn(r1), run_time=0.4)
        self.play(FadeIn(tag, shift=LEFT * 0.25), run_time=0.3)
        # row 2 · signals, not reaching up
        a4_at(self, 4.1)
        par = a4_slab(-5.7, 0.5, 0.5, 0.34, stroke=INK, sw=5)
        chi = a4_slab(-5.7, -0.3, 0.5, 0.34, stroke=INK, sw=5)
        sig = Arrow([-5.7, -0.1, 0], [-5.7, 0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.15,
                    max_tip_length_to_length_ratio=0.5)
        pulse = Dot([-5.7, -0.1, 0], radius=0.085, color=TERRA)
        t2 = a4_C(M("L158", 32), TAGX, 0.1)
        r2 = a4_L(M("Never call a method on get_parent()", 32), X0, 0.1)
        self.play(Create(par), Create(chi), FadeIn(t2), FadeIn(r2), run_time=0.4)
        self.play(GrowArrow(sig), FadeIn(pulse), run_time=0.25)
        self.play(pulse.animate.move_to([-5.7, 0.3, 0]), run_time=0.5, rate_func=linear)
        a4_at(self, 5.95)
        reach = VGroup(Line([-5.4, -0.3, 0], [-5.22, -0.3, 0], color=DIM, stroke_width=4),
                       Line([-5.22, -0.3, 0], [-5.22, 0.5, 0], color=DIM, stroke_width=4),
                       Line([-5.22, 0.5, 0], [-5.4, 0.5, 0], color=DIM, stroke_width=4))
        cross = VGroup(Line([-5.32, 0.05, 0], [-5.12, 0.25, 0], color=INK, stroke_width=7),
                       Line([-5.32, 0.25, 0], [-5.12, 0.05, 0], color=INK, stroke_width=7))
        self.play(Create(reach), run_time=0.35)
        self.play(Create(cross), run_time=0.25)
        # row 3 · small, single-purpose scenes
        a4_at(self, 7.75)
        big = a4_slab(-5.7, -1.1, 1.0, 0.62, stroke=INK, sw=5)
        parts = VGroup(*[a4_slab(-6.02 + 0.32 * i, -1.1, 0.26, 0.4, stroke=DIM, sw=4) for i in range(3)])
        t3 = a4_C(M("L167", 32), TAGX, -1.1)
        r3 = a4_L(T("\u201ccomposing small, single-purpose scenes/components\u201d", 32), X0, -1.1)
        self.play(Create(big), FadeIn(t3), FadeIn(r3), run_time=0.35)
        self.play(LaggedStart(*[Create(p) for p in parts], lag_ratio=0.25), run_time=0.7)
        # row 4 · each feature's files together (the Clawd game's own folder)
        a4_at(self, 9.85)
        folder = Polygon([-6.1, -1.95, 0], [-5.55, -1.95, 0], [-5.4, -1.8, 0], [-5.1, -1.8, 0], [-5.1, -2.95, 0], [-6.1, -2.95, 0],
                         fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5)
        files = VGroup(*[a4_page(-5.84 + 0.36 * i, -2.5, w=0.26, h=0.36, fold=0.09, color=DIM) for i in range(3)])
        h4 = a4_L(T("Kept together in the Clawd game:", 32), X0 - 0.9, -1.95)
        d1 = a4_L(M("features/player/", 32), X0 - 0.9, -2.45)
        d2 = a4_L(M("  player.gd  tuning.gd  clawd_art.gd", 32), X0 - 0.9, -2.95)
        self.play(Create(folder), FadeIn(h4), FadeIn(d1), FadeIn(d2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.15) for f in files], lag_ratio=0.25), run_time=0.6)
        done(self)


# ═════════════════════════════ B16 · the honest problem: C# in the guide, GDScript everywhere else ═════════════════════════════
class B16_TwoLanguages(Scene):
    def construct(self):
        head = a4_L(T("C# or GDScript?", 40), -6.1, 3.05)
        self.add(head)
        divider = Line([0, 2.5, 0], [0, -3.2, 0], color=DIM, stroke_width=4)
        # left: the installed guide, C# (godot.md:3)
        until(self, "The installed guide assumes", lead=0.4)
        lt = a4_L(T("Installed guide", 36), -5.9, 2.1)
        hero_l = a4_C(T("C#", 110), -3.6, 1.0)
        dot_l = Dot([-2.35, 1.55, 0], radius=0.11, color=TERRA)
        q1a = a4_L(T("\u201cStack: Godot 4", 32), -5.9, 0.1)
        q1b = a4_L(T("(.NET / Mono build), C#.\u201d", 32), -5.9, -0.4)
        s1 = a4_L(M("godot.md:3", 32), -5.9, -0.95)
        self.play(Create(divider), FadeIn(lt), FadeIn(hero_l), FadeIn(q1a), FadeIn(q1b), FadeIn(s1), FadeIn(dot_l, scale=0.4),
                  run_time=0.6)
        # right: the example games and the design skill
        until(self, "The example games", lead=0.3)
        rt = a4_L(T("Games and design skill", 36), 0.3, 2.1)
        g1 = a4_L(M("walker-claude/godot/", 32), 0.3, 0.1)
        g2 = a4_L(M("11 files end .gd", 32), 0.3, -0.4)
        g3 = a4_L(M("0 files end .cs", 32), 0.3, -0.9)
        self.play(FadeIn(rt), FadeIn(g1), FadeIn(g2), FadeIn(g3), run_time=0.45)
        until(self, "the design skill installed", lead=0.3)
        sep2 = Line([0.3, -1.4, 0], [5.95, -1.4, 0], color=DIM, stroke_width=3)
        q2 = a4_L(T("\u201cdefault Godot 4, typed GDScript\u201d", 32), 0.3, -1.75)
        s2 = a4_L(M("gdd/commands/p3.md:6", 32), 0.3, -2.25)
        note = a4_L(T("working-tree install, 9 Oct 2026", 32), 0.3, -2.75)
        self.play(Create(sep2), FadeIn(q2), FadeIn(s2), FadeIn(note), run_time=0.45)
        until(self, "use G D script", lead=0.2)
        hero_r = a4_L(T("GDScript", 80), 0.3, 1.0)
        dot_r = Dot([5.3, 1.55, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(hero_r, shift=UP * 0.15), FadeIn(dot_r, scale=0.4), run_time=0.45)
        until(self, "Walker's own readme", lead=0.3)
        sep1 = Line([-5.9, -1.4, 0], [-0.4, -1.4, 0], color=DIM, stroke_width=3)
        q3a = a4_L(T("\u201cIt does not yet select", 32), -5.9, -1.85)
        q3b = a4_L(T("a GDScript guide.\u201d", 32), -5.9, -2.35)
        s3 = a4_L(M("walker/README.md:45", 32), -5.9, -2.9)
        self.play(Create(sep1), FadeIn(q3a), FadeIn(q3b), FadeIn(s3), run_time=0.5)
        done(self)


# ═════════════════════════════ B17 · a prompt you can copy, vs what the publisher installs ═════════════════════════════
class B17_CopyVsInstalled(Scene):
    def construct(self):
        lab = a4_C(T("A prompt you can copy", 36), -3.2, 2.9)
        pg = a4_slab(-3.2, 0.9, 2.9, 3.4, stroke=INK, fill=CARD, sw=5)
        ghost = VGroup(*[Line([-4.45, 2.35 - 0.42 * i, 0], [-1.95 - (0.5 if i % 2 else 0.0), 2.35 - 0.42 * i, 0], color=GHOST, stroke_width=6)
                         for i in range(8)])
        pdot = Dot([-4.45, 0.25, 0], radius=0.09, color=TERRA)
        sep = Line([-5.9, -1.4, 0], [5.9, -1.4, 0], color=DIM, stroke_width=3)
        self.add(lab, pg, ghost, pdot, sep)
        a4_at(self, 1.6)
        dup = a4_slab(-3.2, 0.9, 2.9, 3.4, stroke=DIM, fill=CARD, sw=5)
        dup.set_z_index(-1)
        self.add(dup)
        self.play(dup.animate.shift(RIGHT * 0.35 + DOWN * 0.35), run_time=0.6)
        # installed side
        a4_at(self, 2.9)
        rlab = a4_C(T("Installed: 54 files", 36), 3.35, 2.9)
        rows = [("CLAUDE.md", ""), ("godot.md", ""), (".gitignore", ""), ("asset-gen/", "8 files"), ("gdd/", "43 files")]
        ys = [2.05, 1.5, 0.95, 0.4, -0.15]
        items = VGroup()
        for (nm, cnt), y in zip(rows, ys):
            items.add(a4_L(M(nm, 32), 0.85, y))
            if cnt:
                items.add(a4_L(M(cnt, 32), 3.9, y))
        rframe = Line([0.4, 2.5, 0], [0.4, -1.0, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(rlab), Create(rframe), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.12), run_time=0.75)
        a4_at(self, 3.95)
        gd = a4_L(M("files ending .gd: 0", 32), 0.85, -0.7)
        zdot = Dot([0.65, -0.7, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(gd, shift=UP * 0.1), FadeIn(zdot, scale=0.4), run_time=0.4)
        # the example games: GDScript, and the conventions are in none of their instructions
        a4_at(self, 5.4)
        gl = a4_L(T("In the example game, walker-claude:", 34), -5.9, -1.8)
        self.play(FadeIn(gl), run_time=0.4)
        a4_at(self, 6.4)
        pa = a4_page(-5.65, -2.35, w=0.34, h=0.44, fold=0.12)
        gn = a4_L(M("GDD.md:324", 32), -5.25, -2.35)
        gq = a4_L(T("\u201cProposed game code is typed GDScript.\u201d", 34), -2.4, -2.35)
        self.play(FadeIn(pa), FadeIn(gn), FadeIn(gq), run_time=0.5)
        a4_at(self, 8.6)
        pb = a4_page(-5.65, -2.95, w=0.34, h=0.44, fold=0.12)
        an = a4_L(M("AGENTS.md", 32), -5.25, -2.95)
        ah = a4_L(T("hand-written, no typing or signal rules", 34), -2.4, -2.95)
        self.play(FadeIn(pb), FadeIn(an), FadeIn(ah), run_time=0.5)
        done(self)


# ══════════════════════════════ scenes_act5.py ══════════════════════════════
"""ACT V · Walker in Action  (B18–B23, all Manim)

One cast for the act: the REAL things, each shown as itself. B18 the real publisher run (publish.log, installed-tree.txt, run 2026-10-09);
B19 the real 12-line CLAUDE.md the publisher installed; B20-B21 real Godot output of the Clawd game (stepped real frames, never faked;
frames in pantry/a5_*.png: a5_run_* from walker-claude-jumpman-gameplay.mp4, a5_lbl_* from the same clip, a5_edge_* from a scripted run
of the same Godot project, see evidence/act5/); B22 two real receipts (gallery-two-receipt.json, inspector-v2-process.json); B23 two real
status files (CLAWD-STATUS.json, DESIGN-STATUS.json). Real file text is Menlo; labels are serif. Terracotta is only ever a dot.
Wording: nothing here says "model" for a 3D model; no course/module/assignment appears on screen.
"""

A5P = "pantry/"


def a5_mx(s, x, y, size=32, color=INK):
    """Menlo text, left edge at x."""
    m = M(s, size, color)
    m.move_to([x + m.width / 2, y, 0])
    return m


def a5_tx(s, x, y, size=34, color=INK):
    """Serif text, left edge at x."""
    t = T(s, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


def a5_tc(s, x, y, size=34, color=INK):
    """Serif text centred at x."""
    return T(s, size, color).move_to([x, y, 0])


def a5_rect(x0, y0, x1, y1, color=DIM, sw=4):
    return Polygon([x0, y1, 0], [x1, y1, 0], [x1, y0, 0], [x0, y0, 0], stroke_color=color, stroke_width=sw, fill_opacity=0)


def a5_dash(x0, y0, x1, y1, color=DIM, sw=4, n=36):
    return DashedVMobject(a5_rect(x0, y0, x1, y1, color, sw), num_dashes=n)


def a5_cross(x, y, s=0.2, w=7):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w))


def a5_page(x, y, w=0.34, h=0.44, color=DIM):
    """A small page icon (outline + two ruled lines), centre (x, y)."""
    return VGroup(a5_rect(x - w / 2, y + h / 2, x + w / 2, y - h / 2, color, 4),
                  Line([x - w * 0.28, y + h * 0.1, 0], [x + w * 0.28, y + h * 0.1, 0], color=color, stroke_width=3),
                  Line([x - w * 0.28, y - h * 0.15, 0], [x + w * 0.28, y - h * 0.15, 0], color=color, stroke_width=3))


def a5_img(name, w, x, y):
    im = ImageMobject(A5P + name)
    im.set_width(w)
    im.move_to([x, y, 0])
    return im


def a5_step(self, names, w, x, y, dt, first=None):
    """Step through real captured frames: show names[0], then swap every dt s. Returns the last ImageMobject."""
    cur = first if first is not None else a5_img(names[0], w, x, y)
    if first is None:
        self.add(cur)
    for n in names[1:]:
        self.wait(dt)
        self.remove(cur)
        cur = a5_img(n, w, x, y)
        self.add(cur)
    return cur


def a5_cue_t(self, phrase, lead=0.25):
    """Clip time at which `phrase` is spoken, minus lead (same character-share clock as until)."""
    bid = type(self).__name__.split("_")[0]
    n, tg = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    return tg * n.index(phrase) / len(n) - lead if (n and tg and phrase in n) else 0.0


def a5_run_to(self, st, t):
    """Advance the stepped REAL frames (real time: one frame every st['dt'] s) until clip time t."""
    while st["k"] < len(st["names"]) - 1:
        nxt = st["t0"] + (st["k"] + 1) * st["dt"]
        if nxt > t:
            break
        gap = nxt - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)
        self.remove(st["im"])
        st["k"] += 1
        st["im"] = a5_img(st["names"][st["k"]], st["w"], st["x"], st["y"])
        self.add(st["im"])


def a5_stepper(self, names, w, x, y, dt):
    im = a5_img(names[0], w, x, y)
    self.add(im)
    return {"names": names, "k": 0, "im": im, "w": w, "x": x, "y": y, "dt": dt, "t0": _elapsed(self)}


def a5_until(self, st, phrase, lead=0.25):
    t = a5_cue_t(self, phrase, lead)
    a5_run_to(self, st, t)
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


# ───────────────────────────── B18 · the real publisher run ─────────────────────────────
class B18_PublisherRun(Scene):
    def construct(self):
        title = a5_tx("Walker in Action", -5.9, 3.0, 40)
        self.add(title)
        term = a5_rect(-4.7, 2.45, 4.7, -1.95, DIM, 4)
        lab = a5_tc("recorded run, 2026-10-09", 0, -2.55, 34, DIM)
        self.play(Create(term), FadeIn(lab), run_time=0.7)
        c1 = a5_mx("$ ./publish.sh --engine godot", -4.4, 2.0)
        c2 = a5_mx("  --agent claude --out …", -4.4, 1.5)
        self.play(AddTextLetterByLetter(c1, time_per_char=0.03), run_time=0.9)
        self.play(AddTextLetterByLetter(c2, time_per_char=0.03), run_time=0.8)
        out = ["Publishing godot/claude to: …", "Installed asset-gen and gdd skills", "Created CLAUDE.md",
               "Created godot.md", "Created .gitignore", "Done."]
        until(self, "One command.", lead=0.0)
        lines = []
        for i, s in enumerate(out):
            m = a5_mx(s, -4.4, 1.0 - 0.5 * i)
            lines.append(m)
            self.play(FadeIn(m, shift=0.1 * DOWN), run_time=0.22)
            self.wait(0.12)
        until(self, "It installed", lead=0.15)
        termgrp = VGroup(term, c1, c2, lab, *lines)
        self.play(FadeOut(termgrp), run_time=0.45)
        hero = T("54", 150).move_to([3.7, 0.95, 0])
        files = T("files", 44).move_to([3.7, -0.25, 0])
        byt = T("127,260 bytes", 34, DIM).move_to([3.7, -0.95, 0])
        self.play(FadeIn(hero, scale=0.8), FadeIn(files), run_time=0.5)
        self.add(byt)
        rows = [("CLAUDE.md", "12 lines", "a twelve-line instruction file"), ("godot.md", "66 lines", "a Godot guide"),
                (".gitignore", "9 lines", "a settings file"), ("asset-gen/", "8 files", "and two skills"),
                ("gdd/", "43 files", None), ("game", "0 files", "No game.")]
        y0 = 1.95
        for i, (nm, cnt, cue) in enumerate(rows):
            y = y0 - 0.8 * i
            if cue:
                until(self, cue, lead=0.25)
            empty = nm == "game"
            ic = a5_page(-5.65, y)
            if empty:
                ic = a5_dash(-5.82, y + 0.22, -5.48, y - 0.22, DIM, 4, 14)
            name = a5_mx(nm, -5.2, y, 32, DIM if empty else INK)
            count = a5_tx(cnt, -2.0, y, 34, DIM if empty else INK)
            self.play(FadeIn(ic), FadeIn(name), FadeIn(count), run_time=0.3)
        self.play(Create(Line([1.6, -1.55, 0], [5.8, -1.55, 0], color=GHOST, stroke_width=4)), run_time=0.3)
        done(self)


# ───────────────────────────── B19 · the 12-line manifest ─────────────────────────────
class B19_TwelveLines(Scene):
    def construct(self):
        lens = [37, 0, 94, 109, 254, 93, 0, 11, 0, 186, 0, 553]
        ys = [2.05 - 0.4 * i for i in range(12)]
        page = a5_rect(-5.9, 2.4, -2.3, -2.65, DIM, 4)
        name = a5_mx("CLAUDE.md", -5.9, 2.95, 32)
        n12 = a5_tx("12 lines", -3.35, 2.95, 34, DIM)
        self.play(Create(page), FadeIn(name), run_time=0.6)
        bars = {}
        for i, L in enumerate(lens):
            if L:
                w = 0.5 + 2.3 * (L / 553.0) ** 0.5
                bars[i + 1] = Line([-5.55, ys[i], 0], [-5.55 + w, ys[i], 0], color=BAR2, stroke_width=10)
        self.play(LaggedStart(*[Create(b) for b in bars.values()], lag_ratio=0.12), FadeIn(n12), run_time=1.6)
        picks = [("to build from", 5, ["Build from `design/GDD.md`", "feature IDs, not from memory", "of the chat."], "line 5 of 12"),
                 ("To judge progress", 10, ["Judge progress from the", "running game, never from a", "clean build"], "line 10 of 12"),
                 ("finish with a short video", 12, ["if the user hasn't seen it", "running, finish with a", "15–20s video"], "line 12 of 12"),
                 ("and watch it back", 12, ["watch it back before you", "call the work done"], "line 12 of 12")]
        cur = None
        dot = None
        for k, (cue, ln, txt, cap) in enumerate(picks):
            until(self, cue, lead=0.3)
            ex = VGroup(*[a5_mx(s, -1.5, 0.6 - 0.55 * j, 32) for j, s in enumerate(txt)])
            cp = a5_tx(cap, -1.5, -1.5, 34, DIM)
            nd = Dot([-6.08, ys[ln - 1], 0], radius=0.09, color=TERRA)
            nb = bars[ln].copy().set_color(DIM)
            if cur is None:
                self.play(FadeIn(ex), FadeIn(cp), FadeIn(nd), Transform(bars[ln], nb), run_time=0.45)
            else:
                self.play(FadeOut(cur[0]), FadeOut(cur[1]), FadeOut(dot), FadeIn(ex), FadeIn(cp), FadeIn(nd),
                          Transform(bars[ln], nb), run_time=0.45)
            cur, dot = (ex, cp), nd
        done(self)


# ───────────────────────────── B20 · one change under the rules ─────────────────────────────
class B20_OneChange(Scene):
    """GATE T note: Clawd's flat #dd775b body reads as a terracotta 'text run' at the 50% sample, so no Clawd frame is on screen
    until just after the midpoint. Before it: the starter's original player (real capture, the same level), which is also the
    'before' of the change the voice names."""
    def construct(self):
        win = a5_rect(-6.0, 1.45, -0.4, -0.65, GHOST, 4)
        self.play(Create(win), run_time=0.4)
        tgt = _TARGET.get("B20", 9.28)
        mid = tgt / 2.0
        st = a5_stepper(self, [f"a5_start_{i}.png" for i in range(9)], 5.5, -3.2, 0.4, 0.1)
        st["t0"] = 3.8                                           # the starter's player runs and jumps just before the midpoint
        cap = a5_tc("recorded run, scripted input", -3.2, -1.15, 32, DIM)
        who = a5_tc("the player", -3.2, 1.95, 36)
        self.play(FadeIn(cap), FadeIn(who), run_time=0.4)
        a5_until(self, st, "One change, not", lead=0.2)
        sd = Dot([0.7, 2.4, 0], radius=0.11, color=TERRA)
        sc = a5_tx("scope: drawing only", 1.1, 2.4, 34)
        self.play(FadeIn(sd), FadeIn(sc), run_time=0.35)
        a5_run_to(self, st, mid + 0.1)
        gap = mid + 0.12 - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)
        # swap to Clawd (real frames, real time) just after the midpoint
        self.remove(st["im"])
        who2 = a5_tc("the player: Clawd", -3.2, 1.95, 36)
        self.remove(who)
        self.add(who2)
        st = a5_stepper(self, [f"a5_run_{i:03d}.png" for i in range(55)], 5.5, -3.2, 0.4, 0.1)
        a5_until(self, st, "Three predicted failures", lead=0.25)
        hdr = a5_tx("Predicted failures", 0.5, 1.5, 36)
        self.play(FadeIn(hdr), run_time=0.3)
        cards = [("1", "Wide arms overhang"), ("2", "Two jump arcs"), ("3", "Gallery read as gameplay")]
        cy = [0.7, -0.3, -1.3]
        for i, (num, txt) in enumerate(cards):
            box = a5_rect(0.5, cy[i] + 0.4, 6.0, cy[i] - 0.4, DIM, 4)
            n = a5_tx(num, 0.8, cy[i], 36)
            t = a5_tx(txt, 1.4, cy[i], 34)
            self.play(Create(box), FadeIn(n), FadeIn(t), run_time=0.3)
            a5_run_to(self, st, _elapsed(self))
        a5_until(self, st, "Physics left alone", lead=0.3)
        chk = check(0.9, -2.35, 0.2, INK, 7)
        t2 = a5_tx("physics untouched", 1.4, -2.35, 34)
        self.play(Create(chk), FadeIn(t2), run_time=0.4)
        a5_run_to(self, st, tgt - 0.2)
        done(self)


# ───────────────────────────── B21 · the first prediction, open ─────────────────────────────
class B21_ArmsPastEdge(Scene):
    """GATE T note: a whole Clawd body is a terracotta 'text run' at the 50% sample, so the right window (Clawd over the label)
    starts just after the midpoint; the left window's last frame (Clawd cut by the edge) is not text-like."""
    def construct(self):
        mid = _TARGET.get("B21", 10.05) / 2.0
        wl = a5_rect(-5.42, 0.95, -1.28, -0.7, GHOST, 4)
        ck = check(-5.4, -2.2, 0.22, INK, 7)
        t1 = a5_tx("predicted: wide arms", -4.95, -2.2, 34)
        self.play(Create(wl), run_time=0.5)
        self.play(Create(ck), FadeIn(t1), run_time=0.4)
        until(self, "The broad arms", lead=0.15)
        edge = [f"a5_edgec_{i}.png" for i in range(5)]
        lbl = [f"a5_lbl_{i}.png" for i in range(4)]
        il = a5_img(edge[0], 3.9, -3.35, 0.125)
        self.add(il)
        L1 = a5_tc("past the left edge", -3.35, -1.1, 34)
        self.play(FadeIn(L1), run_time=0.3)
        for n in edge[1:]:
            self.wait(0.3)
            self.remove(il)
            il = a5_img(n, 3.9, -3.35, 0.125)
            self.add(il)
        gap = mid + 0.12 - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)
        wr = a5_rect(0.7, 2.2, 6.0, -0.7, GHOST, 4)
        ir = a5_img(lbl[0], 5.3, 3.35, 0.75)
        self.add(ir)
        R1 = a5_tc("over world labels", 3.35, -1.1, 34)
        self.play(Create(wr), FadeIn(R1), run_time=0.3)
        for n in lbl[1:]:
            self.wait(0.4)
            self.remove(ir)
            ir = a5_img(n, 5.3, 3.35, 0.75)
            self.add(ir)
        until(self, "The record leaves it open", lead=0.2)
        ring = DashedVMobject(Circle(radius=0.22, color=DIM, stroke_width=6).move_to([0.9, -2.2, 0]), num_dashes=14)
        t2 = a5_tx("open: a person judges", 1.35, -2.2, 34)
        src = a5_mx("FRICTIONAL.md:59\u201363", 1.35, -2.95, 32, DIM)
        self.play(Create(ring), FadeIn(t2), FadeIn(src), run_time=0.5)
        done(self)


# ───────────────────────────── B22 · two takes rejected, both kept ─────────────────────────────
class B22_RejectedTakes(Scene):
    def construct(self):
        # take 1: gallery-two, receipt says PASS with 343 of 540 frames
        h1 = a5_mx("gallery-two", -5.9, 2.95, 32)
        d1 = a5_rect(-6.0, 2.5, -0.4, -0.75, DIM, 4)
        self.play(FadeIn(h1), Create(d1), run_time=0.5)
        until(self, "A recording with a pass receipt", lead=0.2)
        l1 = a5_mx('"status": "PASS",', -5.7, 1.9, 32)
        l2 = a5_mx('"frames": 343,', -5.7, 1.3, 32)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        track = Line([-5.7, 0.4, 0], [-1.3, 0.4, 0], color=GHOST, stroke_width=16)
        self.play(Create(track), run_time=0.3)
        until(self, "three hundred and forty-three", lead=0.2)
        fillw = 4.4 * 343 / 540
        fill = Line([-5.7, 0.4, 0], [-5.7 + fillw, 0.4, 0], color=BAR1, stroke_width=16)
        dot = Dot([-5.7 + fillw, 0.4, 0], radius=0.11, color=TERRA)
        a = a5_tx("343 saved", -5.7, -0.15, 34)
        self.play(Create(fill), run_time=0.7)
        self.play(FadeIn(dot), FadeIn(a), run_time=0.3)
        until(self, "five hundred and forty frames", lead=0.2)
        b = a5_tx("540 expected", -3.15, -0.15, 34)
        tick = Line([-1.3, 0.62, 0], [-1.3, 0.18, 0], color=INK, stroke_width=5)
        self.play(Create(tick), FadeIn(b), run_time=0.3)
        until(self, "Rejected, and kept. Another", lead=0.1)
        x1 = a5_cross(-5.5, -1.3, 0.2)
        r1 = a5_tx("rejected", -5.1, -1.3, 34)
        pg1 = a5_page(-2.85, -1.3)
        k1 = a5_tx("kept", -2.55, -1.3, 34)
        self.play(Create(x1), FadeIn(r1), run_time=0.3)
        self.play(FadeIn(pg1), FadeIn(k1), run_time=0.3)
        # take 2: inspector-v2, exit code 0 and no receipt
        h2 = a5_mx("inspector-v2", 0.5, 2.95, 32)
        d2 = a5_rect(0.4, 2.5, 6.0, -0.75, DIM, 4)
        until(self, "Another ended", lead=0.2)
        self.play(FadeIn(h2), Create(d2), run_time=0.45)
        m1 = a5_mx('"exit_code": 0,', 0.7, 1.9, 32)
        self.play(FadeIn(m1), run_time=0.35)
        until(self, "no receipt", lead=0.3)
        gh = a5_dash(0.9, 1.15, 2.1, -0.2, DIM, 4, 24)
        nr = a5_tx("no receipt", 2.5, 0.5, 34)
        self.play(Create(gh), FadeIn(nr), run_time=0.45)
        until(self, "Rejected, and kept. The rule", lead=0.1)
        x2 = a5_cross(0.7, -1.3, 0.2)
        r2 = a5_tx("rejected", 1.1, -1.3, 34)
        pg2 = a5_page(3.45, -1.3)
        k2 = a5_tx("kept", 3.75, -1.3, 34)
        self.play(Create(x2), FadeIn(r2), run_time=0.3)
        self.play(FadeIn(pg2), FadeIn(k2), run_time=0.3)
        until(self, "The rule was", lead=0.2)
        q = a5_tc("Preserve failed receipts.", 0, -2.3, 40)
        s = a5_mx("AGENTS.md:15", -1.5, -2.95, 32, DIM)
        self.play(FadeIn(q), FadeIn(s), run_time=0.5)
        done(self)


# ───────────────────────────── B23 · no human finding, play-test pending ─────────────────────────────
class B23_NoHumanFinding(Scene):
    def construct(self):
        pg = a5_dash(-6.0, 2.6, -2.4, -1.3, DIM, 4, 40)
        lb = a5_tc("human finding", -4.2, 1.2, 36)
        self.play(Create(pg), run_time=0.7)
        self.play(FadeIn(lb), run_time=0.3)
        until(self, "no human finding", lead=0.3)
        none = a5_tc("none on record", -4.2, 0.2, 34, DIM)
        ring = DashedVMobject(Circle(radius=0.42, color=DIM, stroke_width=6).move_to([-4.2, -0.65, 0]), num_dashes=18)
        self.play(FadeIn(none), Create(ring), run_time=0.5)
        until(self, "The play-test is marked pending", lead=0.2)
        h1 = a5_mx("CLAWD-STATUS.json", -1.6, 2.95, 32, DIM)
        p1 = a5_mx('"human_playtest": "pending",', -1.6, 2.3, 32)
        self.play(FadeIn(h1), AddTextLetterByLetter(p1, time_per_char=0.03), run_time=0.9)
        until(self, "The four design gates", lead=0.2)
        h2 = a5_mx("DESIGN-STATUS.json", -1.6, 1.5, 32, DIM)
        self.play(FadeIn(h2), run_time=0.3)
        gates = ["vision", "systems", "world", "scope"]
        for i, g in enumerate(gates):
            y = 0.85 - 0.55 * i
            gt = a5_tx(g, -1.6, y, 34)
            sg = a5_mx('"signed_by": null', 0.7, y, 32)
            self.play(FadeIn(gt), FadeIn(sg), run_time=0.25)
            self.wait(0.12)
        until(self, "The rule says", lead=0.2)
        q = a5_tc("Never invent human playtests, … approvals or test passes.", 0, -2.2, 34)
        src = a5_mx("AGENTS.md:13", -1.5, -2.85, 32, DIM)
        ck = check(5.6, -2.2, 0.2, INK, 7)
        self.play(FadeIn(q), FadeIn(src), run_time=0.4)
        self.play(Create(ck), run_time=0.3)
        done(self)


# ══════════════════════════════ scenes_act6.py ══════════════════════════════
"""ACT VI · What Walker Is Not  (B24-B26, all Manim)

One cast for the act, drawn from REAL things only:
  B24  the real design-status file of the Clawd game (game folder design/DESIGN-STATUS.json, lines 9-14: the four gate lines, every
       "signed_by": null), its real file mode (-rw-r--r--, from `ls -l`), and Walker's own sentence (docs/zelda-gdd-workflow.md:66,
       the LOCAL working copy: it is not in the committed version). The open padlock is a drawing of the idea, not an observed lock.
  B25  a real run of `walker gdd` on this Mac (zsh:1: command not found: walker, exit 127), the repo search for a test framework,
       the REAL public GitHub page of nikbearbrown/walker (captured 2026-10-09T18:03Z, folder list cropped: no gdd folder) and the
       real file counts of the two publisher runs (11 files from the committed version, 54 from the local working copy).
  B26  the habit as five verbs, each with the exhibit it came from in Act V: CHANGE-BRIEF.md (three predictions, scope), a real frame
       of the running Clawd game, the rejected takes (343 of 540 frames; exit 0, no receipt) and CLAWD-STATUS.json ("human_playtest": "pending").
Every file name, number and line on screen is printed, with its source, by evidence/act6/make_evidence.sh (a plain shell script).
Pacing: a6_at() lands each motion on the real spoken word (faster-whisper times, evidence/act6/word_times.json).
Wording rules: no "this chapter", "the book", "the course", assignment or module on screen; "3D model" never appears bare; AI is "AI".
"""

A6P = "pantry/"
A6_GREY = DIM                 # outlines around text are grey, never ink (GATE T 8.6b)


def a6_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a6_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a6_mono(s, x, y, size=32, left=False):
    t = M(s, size)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a6_img(name, w=None, h=None, at=(0.0, 0.0)):
    im = ImageMobject(A6P + name)
    if w is not None:
        im.set_width(w)
    if h is not None:
        im.set_height(h)
    im.move_to(np.array([at[0], at[1], 0.0]))
    return im


def a6_box(cx, cy, w, h, color=A6_GREY, sw=4, dashed=False):
    """An outline-only cell (never a fill behind text). dashed = drawn but not built."""
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])
    if dashed:
        n = int(2 * (w + h) / 0.42)
        return DashedVMobject(r, num_dashes=n, dashed_ratio=0.6)
    return r


# ── B24 · not an enforcer: the gates live in a file the agent could edit ────────────────────────────────────────────
class B24_NotAnEnforcer(Scene):
    def construct(self):
        # real word times (s): enforcer 1.74 · Gates 2.70 · status file 3.70 · could edit 4.90-5.14 · Walker's own document 5.88 · convention 8.40
        title = T("What Walker Is Not", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(title)
        # the real file, drawn as itself: its name, the four gate rows, each "signed_by": null exactly as the file prints it
        PX0, PX1, PY0, PY1 = -6.15, 0.75, -1.55, 2.2
        panel = Rectangle(width=PX1 - PX0, height=PY1 - PY0, stroke_color=A6_GREY, stroke_width=4, fill_opacity=0).move_to(
            [(PX0 + PX1) / 2, (PY0 + PY1) / 2, 0])
        head = a6_mono("design/DESIGN-STATUS.json", -5.95, 1.78, 32, left=True)
        rows = [("vision", 0.95), ("systems", 0.25), ("world", -0.45), ("scope", -1.15)]
        labs = [a6_lab(n, -5.45, y, 34, left=True) for n, y in rows]
        nulls = [a6_mono('"signed_by": null', -3.7, y, 32, left=True) for n, y in rows]
        self.play(Create(panel), FadeIn(head), run_time=0.45)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(a), FadeIn(b)) for a, b in zip(labs, nulls)], lag_ratio=0.35), run_time=0.9)
        # "it is not an enforcer": a padlock drawn closed, then the shackle lifts open ("no lock")
        a6_at(self, 1.25)
        RX = 2.9
        body = Rectangle(width=0.8, height=0.6, stroke_color=A6_GREY, stroke_width=6, fill_opacity=0).move_to([RX, 1.2, 0])
        arc = Arc(radius=0.28, start_angle=0, angle=PI, arc_center=[RX, 1.85, 0], color=A6_GREY, stroke_width=6)
        legR = Line([RX + 0.28, 1.85, 0], [RX + 0.28, 1.5, 0], color=A6_GREY, stroke_width=6)
        legL = Line([RX - 0.28, 1.85, 0], [RX - 0.28, 1.5, 0], color=A6_GREY, stroke_width=6)
        key = Dot([RX, 1.2, 0], radius=0.07, color=TERRA)
        self.play(Create(body), Create(arc), Create(legR), Create(legL), FadeIn(key), run_time=0.5)
        a6_at(self, 1.78)
        no_l = a6_lab("no lock", RX + 0.85, 1.55, 34, left=True)
        self.play(arc.animate.shift(UP * 0.22), legL.animate.shift(UP * 0.22), legR.animate.put_start_and_end_on([RX + 0.28, 2.07, 0], [RX + 0.28, 1.5, 0]),
                  FadeIn(no_l), run_time=0.4)
        # "Gates are recorded in a status file": a terracotta dot lands beside each gate row
        a6_at(self, 2.65)
        dots = [Dot([-5.85, y, 0], radius=0.09, color=TERRA) for n, y in rows]
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.3), run_time=0.7)
        # "the agent could edit": an edit caret appears after the first null and blinks
        a6_at(self, 4.6)
        caret = Line([0.58, 1.15, 0], [0.58, 0.75, 0], color=INK, stroke_width=6)
        self.play(Create(caret), run_time=0.25)
        st = {"t": 0.0}

        def blink(m, dt):
            st["t"] += dt
            m.set_stroke(opacity=1.0 if (st["t"] % 0.9) < 0.55 else 0.0)
        caret.add_updater(blink)
        a6_at(self, 5.0)
        perm = a6_mono("-rw-r--r--", -6.0, -2.35, 32, left=True)
        perm_l = a6_lab("plain file, owner can write", -3.3, -2.35, 32, left=True)
        self.play(FadeIn(perm), FadeIn(perm_l), run_time=0.35)
        # "Walker's own document says...": the sentence, quoted (13 words), with its file and line
        a6_at(self, 6.25)
        QX = 2.0
        q = [a6_lab(s, QX, y, 34, left=True) for s, y in [("Gate validation is a", 0.35), ("convention the skill", -0.15),
                                                           ("follows, not code that", -0.65), ("enforces it.", -1.15)]]
        self.play(LaggedStart(*[FadeIn(x) for x in q], lag_ratio=0.25), run_time=0.75)
        a6_at(self, 7.15)
        s1 = a6_lab("zelda-gdd-workflow.md,", QX, -1.85, 32, left=True)
        s2 = a6_lab("line 66, local copy", QX, -2.3, 32, left=True)
        self.play(FadeIn(s1), FadeIn(s2), run_time=0.35)
        # "convention": the file's own note is one more sentence, not a lock (DESIGN-STATUS.json line 19)
        a6_at(self, 8.2)
        nt = a6_lab("the file's own note:", -6.0, -3.0, 34, left=True)
        nq = a6_lab("\u201cGates are signed by humans only.\u201d", -2.2, -3.0, 34, left=True)
        self.play(FadeIn(nt), FadeIn(nq), run_time=0.4)
        # "not code that enforces it": the open lock pulses
        a6_at(self, 9.9)
        self.play(Indicate(VGroup(body, arc, legR, legL, key), scale_factor=1.15, color=A6_GREY), run_time=0.7)
        done(self)


# ── B25 · not finished: a specification, no test framework, and the public version is smaller ───────────────────────
class B25_NotFinished(Scene):
    def construct(self):
        # real word times (s): command line adapter 1.06 · specification 2.56 · test framework 4.56 · And on the day 5.62 · recorded 6.48 ·
        # public version 7.16 · GitHub 8.06 · installed 8.22 · asset tool 9.48 · eleven-line 10.34 · Godot guide 12.14 · ignore file 13.26 · larger kit 14.48
        head = T("Not finished", 40).move_to([-6.0, 2.95, 0], aligned_edge=LEFT)
        self.add(head)
        # (1) the command-line adapter: a dashed cell (drawn, not built) holding the real run of `walker gdd` on this Mac
        a6_at(self, 0.85)
        box1 = a6_box(-1.85, 1.35, 8.5, 1.55, dashed=True)
        c1 = a6_mono("$ walker gdd", -5.85, 1.62, 32, left=True)
        self.play(Create(box1), FadeIn(c1), run_time=0.5)
        a6_at(self, 1.9)
        c2 = a6_mono("zsh:1: command not found: walker", -5.85, 1.06, 32, left=True)
        self.play(FadeIn(c2), run_time=0.3)
        a6_at(self, 2.4)
        s1a = a6_lab("still a", 2.85, 1.62, 36, left=True)
        s1b = a6_lab("specification", 2.85, 1.07, 36, left=True)
        cap1 = a6_lab("recorded run, this Mac, 9 October 2026", -6.0, 0.1, 32, left=True)
        self.play(FadeIn(s1a), FadeIn(s1b), FadeIn(cap1), run_time=0.35)
        # (2) no test framework: another dashed cell, with the search that backs it
        a6_at(self, 4.1)
        box2 = a6_box(-4.0, -1.0, 4.2, 0.95, dashed=True)
        c3 = a6_mono("test framework", -5.85, -1.0, 32, left=True)
        self.play(Create(box2), FadeIn(c3), run_time=0.45)
        a6_at(self, 4.6)
        s2 = a6_lab("none ships with Walker", -1.5, -1.0, 36, left=True)
        cap2 = a6_lab("repo searched, 9 October 2026", -6.0, -1.9, 32, left=True)
        self.play(FadeIn(s2), FadeIn(cap2), run_time=0.35)
        ledger = VGroup(head, box1, c1, c2, s1a, s1b, cap1, box2, c3, s2, cap2)
        # (3) "on the day this was recorded": the ledger clears, the real public page of the repo arrives
        a6_at(self, 5.6)
        self.play(FadeOut(ledger), run_time=0.45)
        a6_at(self, 6.15)
        cap = a6_img("a6_github_list.png", w=5.0, at=(-3.5, 1.5))
        self.play(FadeIn(cap), run_time=0.4)
        c_a = a6_lab("public page,", -0.5, 2.1, 38, left=True)
        c_b = a6_lab("captured 9 Oct 2026", -0.5, 1.5, 38, left=True)
        self.play(FadeIn(c_a), FadeIn(c_b), run_time=0.3)
        # (4) the two publisher runs as file counts: 11 from the committed (public) version, 54 from the local working copy
        U, X0 = 0.1, -1.7
        a6_at(self, 7.7)
        r1c = a6_lab("public, on GitHub", -6.0, -1.5, 32, left=True)
        self.play(FadeIn(r1c), run_time=0.25)
        a6_at(self, 9.3)
        seg_a = Rectangle(width=8 * U, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([X0 + 4 * U, -0.95, 0])
        self.play(GrowFromEdge(seg_a, LEFT), run_time=0.45)
        a6_at(self, 10.2)
        seg_b = Rectangle(width=3 * U, height=0.34, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([X0 + 8.4 * U + 1.5 * U, -0.95, 0])
        r1a = a6_lab("asset tool, CLAUDE.md (11 lines),", -0.15, -0.75, 32, left=True)
        r1b = a6_lab("godot.md, .gitignore", -0.15, -1.2, 32, left=True)
        self.play(GrowFromEdge(seg_b, LEFT), FadeIn(r1a), run_time=0.5)
        a6_at(self, 12.0)
        self.play(FadeIn(r1b), run_time=0.3)
        a6_at(self, 13.6)
        n1 = a6_lab("11 files", -6.0, -0.95, 44, left=True)
        self.play(FadeIn(n1), run_time=0.3)
        a6_at(self, 14.4)
        n2 = a6_lab("54 files", -6.0, -2.45, 44, left=True)
        r2c = a6_lab("local copy", -6.0, -2.95, 32, left=True)
        seg_a2 = Rectangle(width=8 * U, height=0.34, fill_color=BAR1, fill_opacity=1, stroke_width=0).move_to([X0 + 4 * U, -2.45, 0])
        seg_b2 = Rectangle(width=3 * U, height=0.34, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([X0 + 8.4 * U + 1.5 * U, -2.45, 0])
        self.play(FadeIn(n2), FadeIn(r2c), FadeIn(seg_a2), FadeIn(seg_b2), run_time=0.35)
        a6_at(self, 14.9)
        gdd = a6_box(X0 + 11.8 * U + 21.5 * U, -2.45, 43 * U, 0.34, dashed=True, sw=4)
        gl = a6_lab("the /gdd skill, 43 files", 1.63, -1.95, 32)
        gl2 = a6_lab("not on the page above", 1.63, -2.95, 32)
        self.play(Create(gdd), FadeIn(gl), FadeIn(gl2), run_time=0.7)
        done(self)


# ── B26 · why use it: a rule you can check, and the habit of five verbs, each from the real record ───────────────────
class B26_TheHabit(Scene):
    def construct(self):
        # real word times (s): rule 1.06 · check 2.74 · The value 4.26 · habit 5.00 · predict 5.52 · change 6.04 · run 7.16 · keep 8.24 · leave 9.40 · human 10.62
        # phase A (to 3.9 s): a real rule from the installed instructions, checked against the running game
        a6_at(self, 0.3)
        r_lab = a6_lab("a rule", -6.0, 2.3, 40, left=True)
        qs = [a6_lab(s, -6.0, y, 36, left=True) for s, y in [("Judge progress from the", 1.35), ("running game, never", 0.75),
                                                              ("from a clean build", 0.15)]]
        self.play(FadeIn(r_lab), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(x) for x in qs], lag_ratio=0.3), run_time=0.9)
        a6_at(self, 1.9)
        src = a6_mono("CLAUDE.md, line 10", -6.0, -0.55, 32, left=True)
        src2 = a6_lab("installed by Walker's publisher", -6.0, -1.1, 32, left=True)
        self.play(FadeIn(src), FadeIn(src2), run_time=0.3)
        a6_at(self, 2.1)
        fr = a6_img("a6_frame_jump.png", w=5.8, at=(3.2, 0.55))
        self.play(FadeIn(fr), run_time=0.4)
        g_lab = a6_lab("the running game", 3.2, -1.6, 36)
        g_c1 = a6_lab("recorded run, scripted input,", 3.2, -2.2, 32)
        g_c2 = a6_lab("9 October 2026", 3.2, -2.7, 32)
        a6_at(self, 2.65)
        arr = Arrow([-1.15, 0.55, 0], [0.05, 0.55, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        self.play(Create(arr), FadeIn(g_lab), FadeIn(g_c1), FadeIn(g_c2), run_time=0.5)
        phaseA = Group(r_lab, *qs, src, src2, fr, arr, g_lab, g_c1, g_c2)
        # "The value is the habit": the picture clears, the heading arrives
        a6_at(self, 3.9)
        self.play(FadeOut(phaseA), run_time=0.35)
        a6_at(self, 4.3)
        hab = a6_lab("The habit", -6.0, 3.0, 40, left=True)
        self.play(FadeIn(hab), run_time=0.25)
        EX = -1.3
        ys = [2.0, 1.0, -0.1, -1.35, -2.55]
        # the five verbs stand as a list first (the habit), then each row's real exhibit lands on its spoken word
        v1 = a6_lab("Predict.", -6.0, ys[0], 36, left=True)
        v2 = a6_lab("Change one thing.", -6.0, ys[1], 36, left=True)
        v3 = a6_lab("Run the real game.", -6.0, ys[2], 36, left=True)
        v4 = a6_lab("Keep the failed receipts.", -6.0, ys[3], 36, left=True)
        v5 = VGroup(a6_lab("Leave the judgment", -6.0, ys[4] + 0.27, 36, left=True), a6_lab("to the human.", -6.0, ys[4] - 0.27, 36, left=True))
        a6_at(self, 4.5)
        self.play(LaggedStart(*[FadeIn(v, shift=RIGHT * 0.15) for v in (v1, v2, v3, v4, v5)], lag_ratio=0.25), run_time=0.7)
        # 1 Predict: the three predictions, in the brief (CHANGE-BRIEF.md lines 16-21)
        cells = VGroup(*[VGroup(a6_box(EX + 0.33 + 0.75 * i, ys[0], 0.65, 0.65), T(str(i + 1), 36).move_to([EX + 0.33 + 0.75 * i, ys[0], 0]))
                         for i in range(3)])
        w1 = a6_lab("in the change brief", EX + 2.45, ys[0], 34, left=True)
        a6_at(self, 5.25)
        self.play(FadeIn(cells, scale=0.8), FadeIn(w1), run_time=0.25)
        # 2 Change one thing: the scope: drawing only, physics left alone (CHANGE-BRIEF.md 25-27)
        a6_at(self, 6.0)
        e2 = VGroup(a6_box(EX + 1.35, ys[1], 2.7, 0.75), a6_lab("drawing only", EX + 1.35, ys[1], 34),
                    a6_box(EX + 4.6, ys[1], 3.6, 0.75), a6_lab("physics left alone", EX + 4.6, ys[1], 34))
        self.play(FadeIn(e2, shift=RIGHT * 0.2), run_time=0.35)
        # 3 Run the real game: what the game itself printed when the scripted run ended (raw-log-game.txt: LEVEL COMPLETE f=205 deaths=0 time=5.63)
        a6_at(self, 7.1)
        r1 = a6_mono("LEVEL COMPLETE", EX, ys[2] + 0.28, 32, left=True)
        r2 = a6_mono("deaths=0 time=5.63", EX, ys[2] - 0.28, 32, left=True)
        r3 = a6_lab("game's own log", EX + 3.8, ys[2] + 0.28, 34, left=True)
        self.play(FadeIn(r1), FadeIn(r3), run_time=0.3)
        self.play(FadeIn(r2), run_time=0.3)
        # 4 Keep the failed receipts: the two rejected takes (FRICTIONAL.md lines 39-44, 48-50)
        a6_at(self, 8.2)
        m1 = a6_mono("343 of 540 frames", EX, ys[3] + 0.28, 32, left=True)
        m1b = a6_lab("said PASS", EX + 4.7, ys[3] + 0.28, 34, left=True)
        m2 = a6_mono("exit 0, no receipt", EX, ys[3] - 0.28, 32, left=True)
        self.play(FadeIn(m1), FadeIn(m1b), run_time=0.3)
        self.play(FadeIn(m2), run_time=0.3)
        # 5 Leave the judgment to the human: the status file still says pending (CLAWD-STATUS.json line 12)
        a6_at(self, 9.5)
        m3 = a6_mono('"human_playtest": "pending"', EX, ys[4], 32, left=True)
        self.play(FadeIn(m3), run_time=0.4)
        # the habit repeats: an arrow runs from the last row back up to the first
        a6_at(self, 10.5)
        loop = VMobject(color=A6_GREY, stroke_width=5)
        loop.set_points_as_corners([[5.75, ys[4], 0], [6.0, ys[4], 0], [6.0, ys[0], 0], [5.8, ys[0], 0]])
        tip = Arrow([5.95, ys[0], 0], [5.7, ys[0], 0], buff=0, color=A6_GREY, stroke_width=5, tip_length=0.2)
        self.play(Create(loop), run_time=0.5)
        self.play(Create(tip), run_time=0.15)
        done(self)


# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh's scene discovery
import re as _re
for _n, _c in list(globals().items()):
    if isinstance(_c, type) and issubclass(_c, Scene) and _c is not Scene and _re.match(r"^B[A-Z0-9]+_", _n):
        _c.play = ST.play
