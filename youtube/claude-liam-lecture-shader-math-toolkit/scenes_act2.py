"""ACT II · Cut and Blend  (B07, B09, B10, B11, B14, B16: all Manim; B08, B12, B13, B15 are captures)

Cast for the act: the series' STANDARD PLOT (square axes, a grey curve, a terracotta dot riding it, a dashed drop line to a strip of 64 narrow tiles in true
grays under the axes at the same x scale), drawn from the shader's own formulas in evidence/planning-checks/plot_data.py (PD.CURVES[name][1]); the teal-to-gold
blend strips in B16 (PD.BLENDS). Terracotta only as the dot, small marker dots and grey-backed rings; never as text.

NOTE ON _kit_extra.plot_with_strip: it colours strip tile i by the INPUT value (gray = i / (n - 1)) instead of the curve's OUTPUT, so every strip but the identity
would be wrong. Not edited (the assembler pastes it); this act uses its own fixed variant, a2_plot(), which draws tile gray = fn(x) and honours a y range.
"""


def _a2_ss(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _a2_st(e, x):
    return np.where(x < e, 0.0, 1.0)


# The same formulas as evidence/planning-checks/plot_data.py, used only when that file cannot be imported (Gate A runs scenes.py alone in an empty folder).
_A2_CURVES = {
    "step_half": lambda x: _a2_st(0.5, x),
    "clamp_overshoot": lambda x: np.clip(x * 2.0 - 0.5, 0.0, 1.0),
    "smoothstep_3_7": lambda x: _a2_ss(0.3, 0.7, x),
    "smoothstep_0_10_over_0_10": lambda x: _a2_ss(0.0, 10.0, x * 10.0),
    "blend_plain_ramp": lambda x: x,
    "blend_step": lambda x: _a2_st(0.5, x),
    "blend_smoothstep": lambda x: _a2_ss(0.4, 0.6, x),
}


def a2_fn(name):
    if PD is not None:
        if name in PD.CURVES:
            return PD.CURVES[name][1]
        if name in PD.BLENDS:
            return PD.BLENDS[name][1]
    return _A2_CURVES[name]


def a2_blend_rgb(w):
    if PD is not None:
        return PD.blend_rgb(w)
    teal = np.array([0.37, 0.64, 0.57]); gold = np.array([0.96, 0.80, 0.45])
    return teal * (1.0 - w) + gold * w


def a2_t(s, x, y, size=32, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def a2_left(mob, x_left, y):
    """Place a mob so its left edge is at x_left (explicit coordinates; Pango widths vary)."""
    mob.move_to([x_left + mob.width / 2.0, y, 0])
    return mob


def a2_right(mob, x_right, y):
    mob.move_to([x_right - mob.width / 2.0, y, 0])
    return mob


def a2_tag(fn_text, gloss_lines, x_left, y_top):
    """The function tag: the mono signature, then the GLOSSARY wording in serif under it (left aligned at x_left, first line centred at y_top)."""
    rows = [M(fn_text, 32)] + [T(s, 32) for s in gloss_lines]
    y = y_top
    out = VGroup()
    for r in rows:
        a2_left(r, x_left, y)
        out.add(r)
        y -= 0.6 if r is rows[0] else 0.5
    return out


def a2_plot(fn, x=-2.8, y=0.2, size=4.4, y_range=(0.0, 1.0), n=64, strip=True, ylabels=((0.0, "0"), (1.0, "1"))):
    """The standard plot, fixed variant. fn: numpy function of x in 0..1 (PD.CURVES[name][1]); the strip tile at x has gray = fn(x) clipped to 0..1.
    Returns VGroup(axes, curve, tiles, lab) with .axes .curve .tiles .lab .dot .drop .tracker .ptf (replaceable point function) .pt .x0 .y0 .size .ystrip .yv(v)."""
    lo, hi = y_range
    x0, y0 = x - size / 2.0, y - size / 2.0

    def pt(xv):
        return np.array([x0 + xv * size, y0 + (float(fn(np.array([xv]))[0]) - lo) / (hi - lo) * size, 0.0])
    axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + size, 0], color=INK, stroke_width=5))
    curve = VMobject(stroke_color="#6B6760", stroke_width=7)
    curve.set_points_as_corners([pt(v) for v in np.linspace(0.0, 1.0, 120)])
    ystrip = y0 - 0.9
    tiles = VGroup()
    if strip:
        pitch = size / n
        for i in range(n):
            v = (i + 0.5) / n
            gv = int(round(255 * float(np.clip(fn(np.array([v]))[0], 0.0, 1.0))))
            t = Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (gv, gv, gv), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ystrip, 0])
            t.v = v
            tiles.add(t)
    lab = VGroup(a2_t("0", x0 - 0.3, ystrip), a2_t("1", x0 + size + 0.3, ystrip), a2_t("input", x0 + size + 0.8, y0))
    ol = T("output", 32).rotate(PI / 2).move_to([x0 - 0.85, y0 + size / 2.0, 0])
    lab.add(ol)
    for val, txt in ylabels:
        lab.add(a2_t(txt, x0 - 0.3, y0 + (val - lo) / (hi - lo) * size))
    g = VGroup(axes, curve, tiles, lab)
    g.axes = axes; g.curve = curve; g.tiles = tiles; g.lab = lab
    g.x0 = x0; g.y0 = y0; g.size = size; g.ystrip = ystrip; g.pt = pt; g.ptf = pt
    g.yv = lambda v: y0 + (v - lo) / (hi - lo) * size
    g.tracker = ValueTracker(0.0)
    dot = Dot(pt(0.0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    dot.add_updater(lambda m: m.move_to(g.ptf(g.tracker.get_value())))
    drop = DashedLine(pt(0.0), [x0, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
    drop.add_updater(lambda m: m.become(DashedLine(g.ptf(g.tracker.get_value()), [x0 + g.tracker.get_value() * size, ystrip + 0.25, 0],
                                                    color=DIM, stroke_width=3, dash_length=0.1)))
    g.dot = dot; g.drop = drop
    return g


def a2_paint(tiles, lo, hi=None, ghost=0.16):
    """Strip tiles light up as the dot passes: tile painted when its x <= lo (or >= hi); the rest stay a pale ghost."""
    def upd(m):
        l = lo.get_value()
        h = hi.get_value() if hi is not None else 9.0
        for t in m:
            t.set_fill(opacity=1.0 if (t.v <= l or t.v >= h) else ghost)
    tiles.add_updater(upd)
    upd(tiles)


def a2_follow(lo, tr, st=None):
    """lo keeps the furthest value the tracker has reached (st['on'] False pauses it)."""
    def upd(m):
        if st is None or st.get("on", True):
            m.set_value(max(m.get_value(), tr.get_value()))
    lo.add_updater(upd)


def a2_mid(self, frac=0.56):
    """Wait until 56 % of the clip, so the whole 45-55 % window is a settled hold and the next motion starts after it."""
    tgt = _TARGET.get(type(self).__name__.split("_")[0], 0)
    if tgt:
        gap = tgt * frac - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)


def a2_vguide(g, xv, color=DIM, sw=5):
    ex = g.x0 + xv * g.size
    return DashedLine([ex, g.y0, 0], [ex, g.y0 + g.size, 0], color=color, stroke_width=sw, dash_length=0.14)


def a2_marker(p, r=0.12):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


# ═════════════════════════════ B07 · step is a switch ═════════════════════════════
class B07_StepSwitch(Scene):
    def construct(self):
        title = T("Cut  and Blend", 40).to_corner(UL, buff=0.95)
        g = a2_plot(a2_fn("step_half"), x=-2.5, y=0.1)
        ex = g.x0 + 0.5 * g.size
        top = g.y0 + g.size
        edge = a2_vguide(g, 0.5)
        edge_lab = a2_t("edge", ex + 0.6, top - 0.45)
        tag = a2_tag("step(edge, x)", ["0 below the edge,", "1 from the edge up"], 0.7, 1.5)
        lo = ValueTracker(0.0)
        a2_paint(g.tiles, lo)
        a2_follow(lo, g.tracker)
        self.add(title, lo, g.tracker, g.tiles)
        self.play(Create(g.axes), FadeIn(g.lab), Create(g.curve), Create(edge), FadeIn(edge_lab), FadeIn(tag), run_time=0.8)
        # the edge, highlighted on "an edge"
        until(self, "Give it an edge", lead=0.0)
        self.play(edge.animate.set_color(INK).set_stroke(width=8), run_time=0.4)
        # the dot rides the 0 level up to the edge
        until(self, "Where the ramp is below", lead=0.5)
        self.play(FadeIn(g.dot), FadeIn(g.drop), run_time=0.3)
        self.play(g.tracker.animate.set_value(0.47), run_time=1.4)
        # midpoint hold: the dot rests just left of the edge on the 0 level
        until(self, "At the edge or above", lead=0.15)
        a, b = 59 / 119.0, 60 / 119.0           # the curve's own two samples around the edge

        def pj(v):
            yv = 0.0 if v <= a else (1.0 if v >= b else (v - a) / (b - a))
            return np.array([g.x0 + v * g.size, g.y0 + yv * g.size, 0.0])
        g.ptf = pj
        open_c = Circle(radius=0.14, stroke_color=INK, stroke_width=5, fill_color=STAGE, fill_opacity=1).move_to([ex, g.y0, 0])
        closed = Dot([ex, top, 0], radius=0.14, color=INK)
        self.play(g.tracker.animate.set_value(0.5042), FadeIn(open_c), run_time=0.7)
        self.add(closed)
        # it rides on at 1; the strip's hard split lights up
        until(self, "The plot is a single jump", lead=0.2)
        self.play(g.tracker.animate.set_value(0.97), run_time=1.5)
        done(self)


# ═════════════════════════════ B09 · clamp pins ═════════════════════════════
class B09_ClampPins(Scene):
    def construct(self):
        fn = a2_fn("clamp_overshoot")
        g = a2_plot(fn, x=-2.9, y=0.2, y_range=(-0.5, 1.5))
        x0, y0, S = g.x0, g.y0, g.size
        x1 = x0 + S
        y_lo, y_hi = g.yv(0.0), g.yv(1.0)
        guide_lo = Line([x0, y_lo, 0], [x1 + 0.2, y_lo, 0], color=DIM, stroke_width=3)
        guide_hi = Line([x0, y_hi, 0], [x1 + 0.2, y_hi, 0], color=DIM, stroke_width=3)
        lab_hi = a2_t("high end", x0 + 1.15, y_hi + 0.32)
        lab_lo = a2_t("low end", x0 + 3.0, y_lo - 0.32)
        tag = VGroup(M("clamp(x, low, high)", 32), M("= min(max(x, low), high)", 32))
        a2_left(tag[0], 0.15, 2.85)
        a2_left(tag[1], 0.15, 2.3)
        ramp = DashedLine([x0, y0, 0], [x1, y0 + S, 0], color=DIM, stroke_width=5, dash_length=0.15)
        # the solid curve is drawn BY the dot: a trace that grows to the furthest point the dot has reached
        full = g.curve.copy()
        trace = full.copy()
        reach = ValueTracker(0.0)
        a2_follow(reach, g.tracker)

        def upd_trace(m):
            a = reach.get_value()
            if a < 0.004:
                m.set_stroke(opacity=0)
            else:
                m.pointwise_become_partial(full, 0, min(a, 1.0))
                m.set_stroke(opacity=1)
        trace.add_updater(upd_trace)
        upd_trace(trace)
        a2_paint(g.tiles, reach)
        self.add(reach, g.tracker, g.tiles, trace)
        self.play(Create(g.axes), FadeIn(g.lab), Create(guide_lo), Create(guide_hi), FadeIn(lab_hi), FadeIn(lab_lo), FadeIn(tag), run_time=0.9)
        # the dashed ramp overshoots both guides
        until(self, "Below the low end", lead=0.2)
        self.play(Create(ramp), run_time=1.2)
        # low end: the dot sits on the flat low part, pinned
        until(self, "you get the low end", lead=0.1)
        g.tracker.set_value(0.12)
        pin_lo = a2_left(T("pinned", 32), x0 + 0.15, y_lo + 0.6)
        self.play(FadeIn(g.dot), FadeIn(g.drop), FadeIn(pin_lo), run_time=0.5)
        # high end: the dot rides to the flat high part, drawing the middle ramp on the way
        until(self, "Above the high end", lead=0.15)
        a2_mid(self)
        self.play(g.tracker.animate.set_value(0.9), run_time=1.0)
        pin_hi = a2_left(T("pinned", 32), x0 + 0.9 * S + 0.2, y_hi - 0.5)
        self.play(FadeIn(pin_hi), run_time=0.3)
        # in between: back along the middle ramp
        until(self, "In between", lead=0.1)
        self.play(g.tracker.animate.set_value(0.5), run_time=1.0)
        # max first, then min: labels land on the two corners
        until(self, "It is max first", lead=0.1)
        c_lo, c_hi = a2_marker(g.pt(0.25)), a2_marker(g.pt(0.75))
        ext_lo = DashedLine([x1 + 0.2, y_lo, 0], [0.5, y_lo, 0], color=DIM, stroke_width=3, dash_length=0.12)
        ext_hi = DashedLine([x1 + 0.2, y_hi, 0], [0.5, y_hi, 0], color=DIM, stroke_width=3, dash_length=0.12)
        l_max = a2_left(T("max · the higher of two", 32), 0.65, y_lo)
        l_min = a2_left(T("min · the lower of two", 32), 0.65, y_hi)
        self.play(GrowFromCenter(c_lo), Create(ext_lo), FadeIn(l_max), run_time=0.5)
        self.play(GrowFromCenter(c_hi), Create(ext_hi), FadeIn(l_min), run_time=0.5)
        done(self)


# ═════════════════════════════ B10 · smoothstep, the soft switch ═════════════════════════════
class B10_SoftSwitch(Scene):
    def construct(self):
        g = a2_plot(a2_fn("smoothstep_3_7"), x=-2.9, y=0.3)
        x0, y0, S = g.x0, g.y0, g.size
        top = y0 + S
        e1, e2 = a2_vguide(g, 0.3), a2_vguide(g, 0.7)
        x_e1, x_e2 = x0 + 0.3 * S, x0 + 0.7 * S
        l1 = a2_right(T("first edge", 32), x_e1, top + 0.4)
        l2 = a2_left(T("second edge", 32), x_e2, top + 0.4)
        tag = a2_tag("smoothstep(a, b, x)", ["a smooth S between", "two edges"], 0.5, 1.5)
        lo, hi = ValueTracker(0.0), ValueTracker(9.0)
        st = {"on": True}
        a2_paint(g.tiles, lo, hi)
        a2_follow(lo, g.tracker, st)
        self.add(lo, hi, g.tracker, g.tiles)
        self.play(Create(g.axes), FadeIn(g.lab), FadeIn(tag), Create(g.curve), run_time=1.7)
        # two edges
        until(self, "Give it two edges", lead=0.1)
        self.play(Create(e1), Create(e2), FadeIn(l1), FadeIn(l2), run_time=0.7)
        # below the first edge: zero (dot rests on the flat left part)
        until(self, "Below the first edge", lead=0.9)
        g.tracker.set_value(0.08)
        zero = a2_t("0", x0 + 0.08 * S, g.yv(0.0) + 0.5)
        self.play(FadeIn(g.dot), FadeIn(g.drop), FadeIn(zero), run_time=0.5)
        # rides the flat 0 part to the first edge
        until(self, "zero. Above", lead=0.5)
        a2_mid(self)
        self.play(g.tracker.animate.set_value(0.3), run_time=0.6)
        # above the second edge: one (the dot jumps ahead to the flat 1 part)
        until(self, "Above the second", lead=0.1)
        st["on"] = False
        p_a, p_b = g.pt(0.3), g.pt(0.85)
        hop = CurvedArrow(p_a + np.array([0.2, -0.1, 0]), p_b + np.array([-0.2, -0.3, 0]), color=DIM, stroke_width=5, angle=-TAU / 5)
        self.play(Create(hop), run_time=0.4)
        g.tracker.set_value(0.85)
        one = a2_t("1", p_b[0], p_b[1] - 0.5)
        self.play(FadeIn(one), hi.animate.set_value(0.7), FadeOut(hop), run_time=0.5)
        # the S between the edges: back to the first edge, then ride the S
        until(self, "Between them", lead=0.1)
        self.play(FadeOut(g.dot), run_time=0.2)
        g.tracker.set_value(0.3)
        st["on"] = True
        self.play(FadeIn(g.dot), run_time=0.2)
        self.play(g.tracker.animate.set_value(0.7), run_time=1.7)
        done(self)


# ═════════════════════════════ B11 · smoothstep is not a straight line ═════════════════════════════
class B11_NotALine(Scene):
    def construct(self):
        W, H = 9.0, 4.4
        x0, y0 = -4.9, -1.9
        X = lambda v: x0 + v * W / 10.0
        O = lambda u: y0 + u * H
        top = O(1.0)
        fn = a2_fn("smoothstep_0_10_over_0_10")
        axes = VGroup(Line([x0, y0, 0], [x0 + W, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, top, 0], color=INK, stroke_width=5))
        ticks = VGroup(a2_t("0", x0, y0 - 0.4), a2_t("10", x0 + W, y0 - 0.4), a2_t("input", x0 + W + 0.85, y0), a2_t("1", x0 - 0.3, top),
                       a2_left(T("output", 32), x0 + 0.25, top + 0.4))
        line = DashedLine([X(0), O(0), 0], [X(10), O(1), 0], color=DIM, stroke_width=6, dash_length=0.16)
        scurve = VMobject(stroke_color="#6B6760", stroke_width=7)
        scurve.set_points_as_corners([np.array([X(10 * u), O(float(fn(np.array([u]))[0])), 0.0]) for u in np.linspace(0, 1, 160)])
        lab_line = a2_t("a straight line", X(2.9), O(0.58))
        lab_s = a2_t("the S", X(6.5), O(0.93))
        self.play(Create(axes), FadeIn(ticks), Create(line), Create(scurve), FadeIn(lab_line), FadeIn(lab_s), run_time=1.6)
        # the guide at x = 1 drops; two dots land on the two curves
        until(self, "Say the edges", lead=0.2)
        v_line, v_s = 0.1, float(fn(np.array([0.1]))[0])        # 0.1 and 0.02797
        guide = DashedLine([X(1), top, 0], [X(1), y0, 0], color=DIM, stroke_width=4, dash_length=0.12)
        self.play(Create(guide), run_time=0.7)
        d_line = a2_marker([X(1), top, 0], 0.12)
        d_s = a2_marker([X(1), top, 0], 0.12)
        self.add(d_line, d_s)
        self.play(d_line.animate.move_to([X(1), O(v_line), 0]), d_s.animate.move_to([X(1), O(v_s), 0]), run_time=0.9, rate_func=ease_in)
        # read-out on the straight line: 0.1
        until(self, "would give point one", lead=0.2)
        h1 = DashedLine([X(1), O(v_line), 0], [x0, O(v_line), 0], color=DIM, stroke_width=3, dash_length=0.1)
        r1 = a2_right(T("0.1", 34), x0 - 0.2, O(v_line) + 0.2)
        self.play(Create(h1), FadeIn(r1), run_time=0.5)
        # read-out on the S: 0.028, and the ring on the slow start
        until(self, "The S gives point zero", lead=0.1)
        h2 = DashedLine([X(1), O(v_s), 0], [x0, O(v_s), 0], color=DIM, stroke_width=3, dash_length=0.1)
        r2 = a2_right(T("0.028", 34), x0 - 0.2, O(v_s) - 0.12)
        slow = ring(Rectangle(width=1.95, height=0.6).move_to([x0 + 1.25, y0 + 0.35, 0]))
        self.play(Create(h2), FadeIn(r2), run_time=0.5)
        self.play(Create(slow), run_time=0.6)
        # the credit line
        until(self, "because it starts out slowly", lead=0.3)
        credit = a2_t("checked in Godot 4.7.2 · Forward+", 0.0, -3.05, 32, DIM)
        self.play(FadeIn(credit), run_time=0.5)
        done(self)


# ═════════════════════════════ B14 · mix slides ═════════════════════════════
class B14_MixSlides(Scene):
    def construct(self):
        A, B = 0.2, 0.9
        f = lambda t: A * (1.0 - t) + B * t
        unit, H = 2.7, 4.4
        x0, y0 = -4.15, -1.9
        ymax = 1.75
        X = lambda t: x0 + t * unit
        Y = lambda v: y0 + v / ymax * H
        axes = VGroup(Line([x0, y0, 0], [X(2), y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + H, 0], color=INK, stroke_width=5))
        xl = VGroup(a2_t("0", X(0) - 0.3, y0 - 0.38), a2_t("1", X(1) + 0.3, y0 - 0.38), a2_t("2", X(2), y0 - 0.38), a2_left(T("t · weight", 32), X(2) + 0.3, y0))
        solid = Line([X(0), Y(f(0)), 0], [X(1), Y(f(1)), 0], color="#6B6760", stroke_width=7)
        dashed = DashedLine([X(1), Y(f(1)), 0], [X(2), Y(f(2)), 0], color="#6B6760", stroke_width=7, dash_length=0.16)
        tag1 = a2_left(M("mix(a, b, t)", 32), -6.1, 3.0)
        tag2 = a2_left(T("blends from a to b: t of 0 gives a, 1 gives b", 32), -2.55, 3.0)
        form = a2_left(M("a x (1 - t) + b x t", 32), 1.5, 0.9)
        # strip for weights 0 to 1 only: gray of 0.2 up to gray of 0.9
        n = 32
        pitch = unit / n
        ys = y0 - 0.9
        tiles = VGroup()
        for i in range(n):
            v = (i + 0.5) / n
            gv = int(round(255 * f(v)))
            t = Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (gv, gv, gv), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ys, 0])
            t.v = v
            tiles.add(t)
        tr = ValueTracker(0.0)
        reach = ValueTracker(-1.0)
        a2_paint(tiles, reach)
        a2_follow(reach, tr)
        dot = Dot([X(0), Y(f(0)), 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        dot.add_updater(lambda m: m.move_to([X(tr.get_value()), Y(f(tr.get_value())), 0]))
        drop = DashedLine([X(0), Y(f(0)), 0], [X(0), ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)

        def upd_drop(m):
            t = tr.get_value()
            m.become(DashedLine([X(t), Y(f(t)), 0], [X(min(t, 1.0)), ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1))
            m.set_stroke(opacity=1.0 if t <= 1.0001 else 0.0)
        drop.add_updater(upd_drop)
        self.add(tr, reach, tiles)
        self.play(Create(axes), FadeIn(xl), FadeIn(tag1), FadeIn(tag2), FadeIn(form), Create(solid), run_time=0.9)
        # the start and end ticks land on the y axis
        until(self, "Give it a start", lead=0.1)
        tk_a = VGroup(Line([x0 - 0.12, Y(A), 0], [x0 + 0.12, Y(A), 0], color=INK, stroke_width=5), a2_right(T("a · start", 32), x0 - 0.22, Y(A)))
        tk_b = VGroup(Line([x0 - 0.12, Y(B), 0], [x0 + 0.12, Y(B), 0], color=INK, stroke_width=5), a2_right(T("b · end", 32), x0 - 0.22, Y(B)))
        self.play(FadeIn(tk_a), run_time=0.5)
        self.play(FadeIn(tk_b), run_time=0.5)
        # weight 0: start
        until(self, "Weight zero", lead=0.1)
        self.play(FadeIn(dot), FadeIn(drop), run_time=0.3)
        r_start = a2_t("start", X(0) + 1.0, y0 + 0.3)
        self.play(FadeIn(r_start), run_time=0.3)
        # weight 1: end
        until(self, "one returns the end", lead=0.9)
        self.play(tr.animate.set_value(1.0), run_time=0.6)
        r_end = a2_t("end", X(1) + 0.6, Y(B) - 0.45)
        self.play(FadeIn(r_end), run_time=0.25)
        # one half: halfway
        until(self, "one half", lead=0.1)
        a2_mid(self)
        self.play(tr.animate.set_value(0.5), run_time=0.6)
        r_half = a2_t("halfway", X(0.5) + 1.0, Y(f(0.5)) - 0.5)
        self.play(FadeIn(r_half), run_time=0.3)
        # the line carries on, dashed, past weight 1
        until(self, "It does not pin", lead=0.1)
        self.play(Create(dashed), run_time=0.6)
        until(self, "a weight of two", lead=0.1)
        self.play(tr.animate.set_value(2.0), run_time=1.1)
        r_over = a2_left(T("overshoots: 1.6", 32), X(2) + 0.3, Y(f(2)))
        self.play(FadeIn(r_over), run_time=0.4)
        # clamp first: the safe range 0 to 1 on the weight axis
        until(self, "so clamp it first", lead=0.1)
        br = VGroup(Line([X(0), y0, 0], [X(1), y0, 0], color=TEAL, stroke_width=11), Line([X(0), y0 - 0.14, 0], [X(0), y0 + 0.14, 0], color=TEAL, stroke_width=7),
                    Line([X(1), y0 - 0.14, 0], [X(1), y0 + 0.14, 0], color=TEAL, stroke_width=7))
        cl = a2_left(M("clamp(t, 0, 1)", 32), X(1) + 0.3, ys)
        self.play(Create(br), FadeIn(cl), run_time=0.6)
        done(self)


# ═════════════════════════════ B16 · any reshaped ramp can be the weight ═════════════════════════════
def a2_mini(wfn, cx, cy, w=2.0, h=1.1):
    """A small weight plot: axes and a grey curve (no dot). Returns VGroup with .curve and .axes."""
    x0, y0 = cx - w / 2.0, cy - h / 2.0
    axes = VGroup(Line([x0, y0, 0], [x0 + w, y0, 0], color=INK, stroke_width=4), Line([x0, y0, 0], [x0, y0 + h, 0], color=INK, stroke_width=4))
    curve = VMobject(stroke_color="#6B6760", stroke_width=6)
    curve.set_points_as_corners([np.array([x0 + v * w, y0 + float(wfn(np.array([v]))[0]) * h, 0.0]) for v in np.linspace(0.0, 1.0, 100)])
    g = VGroup(axes, curve)
    g.axes = axes; g.curve = curve
    return g


def a2_blend_strip(wfn, x_left, y, width=5.7, height=0.6, n=48):
    """A teal-to-gold strip blended with the weight wfn (colours from PD.blend_rgb); narrow tiles with gaps."""
    pitch = width / n
    tiles = VGroup()
    for i in range(n):
        v = (i + 0.5) / n
        rgb = a2_blend_rgb(float(wfn(np.array([v]))[0]))
        col = "#%02x%02x%02x" % tuple(int(round(255 * c)) for c in rgb)
        tiles.add(Rectangle(width=pitch * 0.8, height=height, fill_color=col, fill_opacity=1, stroke_width=0).move_to([x_left + pitch * (i + 0.5), y, 0]))
    return tiles


class B16_AnyWeight(Scene):
    def construct(self):
        rows = [("plain ramp", "blend_plain_ramp", 2.35, "The plain ramp", 0.15), ("step", "blend_step", 0.85, "Step gives", 0.9), ("smoothstep", "blend_smoothstep", -0.65, "Smooth step gives", 1.05)]
        caps, minis, arrs, strips = [], [], [], []
        for cap, name, ry, _, _l in rows:
            caps.append(a2_left(T(cap, 32), -6.1, ry))
            minis.append(a2_mini(a2_fn(name), -2.6, ry))
            arrs.append(arrow([-1.1, ry, 0], [-0.3, ry, 0], color=INK, w=5, tip=0.2))
            strips.append(a2_blend_strip(a2_fn(name), 0.2, ry))
        self.play(*[FadeIn(c) for c in caps], run_time=0.6)
        for i, (cap, name, ry, ph, ld) in enumerate(rows):
            until(self, ph, lead=ld)
            self.play(Create(minis[i].axes), Create(minis[i].curve), run_time=0.35)
            self.play(Create(arrs[i]), run_time=0.15)
            self.play(LaggedStart(*[FadeIn(t) for t in strips[i]], lag_ratio=0.03), run_time=0.4)
        # the grey-backed bracket round the three weight plots
        until(self, "A weight like this", lead=0.2)
        bracket = ring(VGroup(*minis), pad=0.22, sw=6)
        self.play(Create(bracket), run_time=0.8)
        # the definition types in; then the word "mask" is marked
        until(self, "a number from zero to one", lead=0.2)
        mask = T("mask", 38, INK, True)
        rest = T("· a number from 0 to 1 per pixel", 36)
        l1 = VGroup(mask, rest).arrange(RIGHT, buff=0.22)
        l1.move_to([0.0, -2.2, 0])
        l2 = T("saying how much of something to show", 36).move_to([0.0, -2.78, 0])
        self.play(AddTextLetterByLetter(l1[0], time_per_char=0.07), run_time=0.45)
        self.play(AddTextLetterByLetter(l1[1], time_per_char=0.05), run_time=1.1)
        self.play(AddTextLetterByLetter(l2, time_per_char=0.04), run_time=1.1)
        until(self, "is called a mask", lead=0.1)
        self.play(Create(ring(mask, pad=0.1, sw=6)), run_time=0.6)
        done(self)
