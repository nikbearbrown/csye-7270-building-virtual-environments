"""ACT III · Repeat and Fold  (B17 B18 B19 B21 B22 B24, Manim; B20 B23 are ShaderLab captures, B25 is a table)

Cast for the act (ACTS.md): the ramp strip with re-labelled ticks; the number line with the dot at 2.75; the standard plot frame.

a3_plot is this act's fixed variant of plot_with_strip: the kit-extra helper draws the strip under the axes as a plain 0..1 ramp whatever the curve is
(its tiles ignore fn) and joins the jumps of fract / floor / mod with slanted lines. a3_plot draws the strip tiles from the curve's own values
(true grays: value v drawn as gray v) and the curve as separate pieces so a jump is a jump. _kit_extra.py itself is untouched.
"""

A3C = "#6B6760"          # the curve's ink-grey

# PD (plot_data.py) is imported by _kit_extra when evidence/ is reachable; Gate A runs scenes.py alone, so the same four formulas are kept here as a fallback
_A3_FALLBACK = {
    "abs_centered": lambda x: np.abs(x * 2.0 - 1.0),
    "fract_4": lambda x: (x * 4.0) - np.floor(x * 4.0),
    "floor_4_over_3": lambda x: np.floor(x * 4.0) / 3.0,
    "mod_quarter_x4": lambda x: (x - 0.25 * np.floor(x / 0.25)) * 4.0,
}


def a3_curve(name):
    """The numpy function of a named curve: from plot_data.py when it is importable, else the identical fallback above."""
    try:
        return PD.CURVES[name][1]
    except Exception:
        return _A3_FALLBACK[name]


def a3_plot(fn, pieces, strip_fn=None, x=-1.8, y=0.6, size=4.2, y_range=(0.0, 1.0), in_labels=("0", "1"), out_labels=("0", "1"), n=64):
    """Standard plot, fixed. fn / strip_fn: numpy functions of x in 0..1. pieces: list of (xa, xb) so jumps are not joined. Returns a VGroup (frame +
    labels) with .parts (curve pieces), .tiles (true-gray strip, 64 narrow tiles with gaps), .dot, .drop, .tr (ValueTracker of x), .pt, .x0 .y0 .size .ystrip."""
    x0, y0 = x - size / 2, y - size / 2
    lo, hi = y_range
    sfn = strip_fn or fn

    def pt(xv):
        return np.array([x0 + xv * size, y0 + (float(fn(np.array([float(xv)]))[0]) - lo) / (hi - lo) * size, 0.0])
    axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + size, 0], color=INK, stroke_width=5))
    parts = VGroup()
    for a, b in pieces:
        c = VMobject(stroke_color=A3C, stroke_width=7)
        c.set_points_as_corners([pt(v) for v in np.linspace(a, b - 1e-6, 81)])
        parts.add(c)
    ystrip = y0 - 0.95
    tiles = VGroup()
    pitch = size / n
    for i in range(n):
        v = float(np.clip(sfn(np.array([(i + 0.5) / n]))[0], 0.0, 1.0))
        gv = int(round(255 * v))
        tiles.add(Rectangle(width=pitch * 0.78, height=0.5, fill_color="#%02x%02x%02x" % (gv, gv, gv), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), ystrip, 0]))
    tr = ValueTracker(0.0)
    dot = Dot(pt(0.0), radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    dot.add_updater(lambda m: m.move_to(pt(tr.get_value())))
    drop = DashedLine(pt(0.0), [x0, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
    drop.add_updater(lambda m: m.become(DashedLine(pt(tr.get_value()), [x0 + tr.get_value() * size, ystrip + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)))
    k = len(in_labels) - 1
    # the end labels sit just outside the ends so the dashed drop line never runs through a label
    labs = VGroup(*[T(s, 32).move_to([x0 + size * i / k + (-0.3 if i == 0 else (0.3 if i == k else 0.0)), y0 - 0.38, 0]) for i, s in enumerate(in_labels)])
    outs = VGroup(T(out_labels[0], 32).move_to([x0 - 0.4, y0, 0]), T(out_labels[1], 32).move_to([x0 - 0.4, y0 + size, 0]))
    g = VGroup(axes, labs, outs)
    g.parts = parts; g.tiles = tiles; g.dot = dot; g.drop = drop; g.tr = tr; g.pt = pt
    g.x0 = x0; g.y0 = y0; g.size = size; g.ystrip = ystrip; g.axes = axes
    return g


def a3_reveal(g, lo_op=0.14):
    """The strip lights tile by tile as the dot passes (an updater on the tiles; do not FadeIn the tiles after this)."""
    nt = len(g.tiles)

    def f(m):
        v = g.tr.get_value()
        for i, t in enumerate(m):
            t.set_fill(opacity=1.0 if (i + 0.5) / nt <= v else lo_op)
    g.tiles.add_updater(f)
    f(g.tiles)


def a3_open(p):
    return Circle(radius=0.1, stroke_color=A3C, stroke_width=5).set_fill(STAGE, opacity=1).move_to(p)


def a3_closed(p):
    return Dot(p, radius=0.1, color=A3C)


def a3_bracket(xa, xb, y, color=DIM, cap=0.14, sw=6):
    return VGroup(Line([xa, y, 0], [xb, y, 0], color=color, stroke_width=sw), Line([xa, y, 0], [xa, y + cap, 0], color=color, stroke_width=sw),
                  Line([xb, y, 0], [xb, y + cap, 0], color=color, stroke_width=sw))


def a3_row(mobs, gap, cx, cy):
    """Centre a row of mobjects with a fixed gap between them."""
    tot = sum(m.width for m in mobs) + gap * (len(mobs) - 1)
    x = cx - tot / 2.0
    for m in mobs:
        m.move_to([x + m.width / 2.0, cy, 0])
        x += m.width + gap
    return mobs


# ═════════════════════════════ B17 · re-centering a ramp ═════════════════════════════
class B17_Recenter(Scene):
    def construct(self):
        title = T("Repeat and Fold", 40).to_corner(UL, buff=0.95)
        strip = ramp_strip(width=8.0, n=56, height=0.5, y=0.3, labels=False)
        x0, x1, xm = strip.x0, strip.x1, 0.0
        ly = 0.3 - 0.25 - 0.45
        lab0 = T("0", 36).move_to([x0, ly, 0])
        lab1 = T("1", 36).move_to([x1, ly, 0])
        dot = ramp_marker(strip, 0.5)
        self.add(title, strip, lab0, lab1)
        self.play(GrowFromCenter(dot), run_time=0.4)
        # x * 2: the number 1 slides to the middle, a 2 takes the end
        until(self, "Multiply by two")
        tag1 = chip("x × 2", -1.9, 1.75)
        lab2 = T("2", 36).move_to([x1, ly, 0])
        self.play(FadeIn(tag1), lab1.animate.move_to([xm, ly, 0]), FadeIn(lab2), run_time=0.9)
        # - 1: every label slides one step down the number line
        until(self, "and subtract one")
        tag2 = chip("− 1", 1.9, 1.75)
        n0 = T("−1", 36).move_to([x0, ly, 0])
        nm = T("0", 36).move_to([xm, ly, 0])
        n1 = T("1", 36).move_to([x1, ly, 0])
        self.play(FadeIn(tag2), ReplacementTransform(lab0, n0), ReplacementTransform(lab1, nm), ReplacementTransform(lab2, n1), run_time=1.0)
        # zero lands under the dot
        until(self, "with zero in the middle")
        zm = ring(nm)
        self.play(FadeIn(zm, shift=DOWN * 0.4), run_time=0.5)
        until(self, "Now negative numbers")
        cap = T("zero here", 36).move_to([0, -1.6, 0])
        pt_ = arrow([0, -1.25, 0], [0, -0.85, 0], color=DIM)
        hl = RoundedRectangle(width=4.1, height=0.8, corner_radius=0.16, stroke_color=TEAL, stroke_width=7).move_to([-2.0, 0.3, 0])
        self.play(FadeIn(cap), GrowArrow(pt_), Create(hl), run_time=0.6)
        done(self)


# ═════════════════════════════ B18 · abs folds the ramp at zero ═════════════════════════════
class B18_FoldAtZero(Scene):
    def construct(self):
        SX, SY = -1.2, 2.15
        strip = ramp_strip(width=5.2, n=56, height=0.45, x=SX, y=SY, labels=False)
        ly = SY - 0.225 - 0.4
        labs = VGroup(T("−1", 36).move_to([strip.x0, ly, 0]), T("0", 36).move_to([SX, ly, 0]), T("1", 36).move_to([strip.x1, ly, 0]))
        dot = ramp_marker(strip, 0.5)
        tag = chip("abs(x)", 4.0, 2.2)
        tag2 = T("drops the minus sign", 36).move_to([4.0, 1.55, 0])
        self.add(strip, labs, dot, tag, tag2)
        axis = DashedLine([SX, SY + 0.45, 0], [SX, SY - 0.45, 0], color=DIM, stroke_width=4, dash_length=0.1)
        self.play(Create(axis), run_time=0.4)
        # the left half folds over the right half like a page
        until(self, "Fold the ramp at zero")
        left = VGroup(*strip.tiles[:28])
        left.set_z_index(3)
        self.play(FadeOut(labs[0]), left.animate.flip(UP, about_point=np.array([SX, SY, 0])), run_time=1.6, rate_func=smooth)
        # the V draws under the strip
        until(self, "The plot is a V")
        pl = a3_plot(a3_curve("abs_centered"), [(0.0, 1.0)], x=SX, y=-0.4, size=3.0, in_labels=("−1", "0", "1"), out_labels=("0", "1"))
        self.play(Create(pl), run_time=0.5)
        self.add(pl.tiles)
        a3_reveal(pl)
        self.play(Create(pl.parts), run_time=0.7)
        self.add(pl.drop, pl.dot)
        until(self, "and the strip is a mirror", lead=0.1)
        self.play(pl.tr.animate.set_value(1.0), run_time=2.1, rate_func=linear)
        mir = DashedLine([SX, pl.ystrip + 0.45, 0], [SX, pl.ystrip - 0.45, 0], color=DIM, stroke_width=4, dash_length=0.1)
        self.play(Create(mir), run_time=0.4)
        done(self)


# ═════════════════════════════ B19 · fract: the ramp restarts ═════════════════════════════
class B19_RampRestarts(Scene):
    def construct(self):
        RX = 3.95
        tag = chip("fract(x)", RX, 2.55)
        t1 = T("the part after the point", 32).move_to([RX, 1.85, 0])
        t2 = M("x − floor(x)", 32).move_to([RX, 1.3, 0])
        self.play(FadeIn(tag), FadeIn(t1), FadeIn(t2), run_time=0.6)
        # inset: 2.75 splits into 2 and 0.75
        nl = number_line(-5.2, 0.8, 0.2, lo=0.0, hi=3.0, ticks=(0.0, 1.0, 2.0, 3.0))
        until(self, "Two point seven five")
        d = Dot(nl.at(2.75), radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        self.play(Create(nl), run_time=0.5)
        self.play(GrowFromCenter(d), run_time=0.3)
        until(self, "becomes", lead=0.3)
        b1 = a3_bracket(nl.at(0)[0], nl.at(2)[0], -0.75, DIM)
        b2 = a3_bracket(nl.at(2)[0], nl.at(2.75)[0], -0.75, TEAL)
        l1 = T("2", 36).move_to([(nl.at(0)[0] + nl.at(2)[0]) / 2, -1.25, 0])
        l2 = T("0.75", 36).move_to([(nl.at(2)[0] + nl.at(2.75)[0]) / 2, -1.25, 0])
        self.play(Create(b1), Create(b2), FadeIn(l1), FadeIn(l2), run_time=0.6)
        r1 = T("2.75", 44).move_to([-3.9, -2.2, 0])
        ar = arrow([-3.05, -2.2, 0], [-1.95, -2.2, 0])
        r2 = T("0.75", 44).move_to([-1.2, -2.2, 0])
        self.play(FadeIn(r1), GrowArrow(ar), FadeIn(r2), run_time=0.6)
        inset = VGroup(nl, d, b1, b2, l1, l2, r1, ar, r2)
        # the standard plot: a steep dashed 4x leaves the top, fract(4x) is four teeth
        until(self, "Multiply the ramp", lead=0.0)
        self.play(FadeOut(inset), run_time=0.4)
        pl = a3_plot(a3_curve("fract_4"), [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)], x=-1.8, y=0.6, size=4.2,
                     in_labels=("0", "1"), out_labels=("0", "1"))
        dash = DashedLine(pl.pt(0.0), pl.pt(0.0) + np.array([0.275 * 4.2, 1.1 * 4.2, 0]), color=DIM, stroke_width=4, dash_length=0.14)
        self.play(Create(pl), Create(dash), run_time=0.6)
        self.add(pl.tiles)
        a3_reveal(pl)
        until(self, "and fract gives four ramps", lead=0.0)
        self.play(LaggedStart(*[Create(c) for c in pl.parts], lag_ratio=0.7), run_time=1.3)
        marks = VGroup()
        for i in range(4):
            marks.add(a3_closed(pl.pt(i * 0.25 + 1e-6)))
        for i in range(1, 5):
            marks.add(a3_open(np.array([pl.x0 + i * 0.25 * 4.2, pl.y0 + 4.2, 0.0])))
        self.play(FadeIn(marks), run_time=0.3)
        self.add(pl.drop, pl.dot)
        until(self, "each starting over at zero", lead=0.2)
        self.play(pl.tr.animate.set_value(0.9999), run_time=1.7, rate_func=linear)
        done(self)


# ═════════════════════════════ B21 · floor rounds down ═════════════════════════════
class B21_RoundDown(Scene):
    def construct(self):
        RX = 3.95
        tag = chip("floor(x)", RX, 2.55)
        t1 = T("rounds down to the", 32).move_to([RX, 1.9, 0])
        t2 = T("whole number below", 32).move_to([RX, 1.45, 0])
        self.play(FadeIn(tag), FadeIn(t1), FadeIn(t2), run_time=0.6)
        until(self, "It rounds down", lead=0.1)
        i1 = T("2.75", 40).move_to([2.9, 0.5, 0])
        ia = arrow([3.65, 0.5, 0], [4.55, 0.5, 0])
        i2 = T("2", 40).move_to([5.15, 0.5, 0])
        self.play(FadeIn(i1), GrowArrow(ia), FadeIn(i2), run_time=0.7)
        # the plot: dashed 4x diagonal and the first step
        until(self, "Multiply the ramp", lead=0.7)
        fl = lambda x: np.floor(x * 4.0)
        pl = a3_plot(fl, [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)], strip_fn=a3_curve("floor_4_over_3"), x=-1.8, y=0.6, size=4.2,
                     y_range=(0.0, 4.0), in_labels=("0", "1"), out_labels=("0", "4"))
        diag = DashedLine(pl.pt(0.0), [pl.x0 + 4.2, pl.y0 + 4.2, 0], color=DIM, stroke_width=4, dash_length=0.14)
        self.play(Create(pl), Create(diag), run_time=0.45)
        self.add(pl.tiles)
        a3_reveal(pl)
        step0 = pl.parts[0]
        c0 = a3_closed(pl.pt(1e-6)); o0 = a3_open(np.array([pl.x0 + 0.25 * 4.2, pl.y0, 0.0]))
        bl = [T(str(k), 36).move_to([pl.x0 + (k + 0.5) * 0.25 * 4.2, pl.ystrip - 0.5, 0]) for k in range(4)]
        note = T("÷ 3 to fit", 32).move_to([2.0, pl.ystrip, 0])
        self.play(Create(step0), FadeIn(c0), FadeIn(o0), FadeIn(bl[0]), FadeIn(note), run_time=0.35)
        self.add(pl.drop, pl.dot)
        self.play(pl.tr.animate.set_value(0.24), run_time=0.3, rate_func=linear)
        for k, ph in ((1, "one, two"), (2, "two, three"), (3, "three, four")):
            until(self, ph, lead=0.3)
            pl.tr.set_value(0.25 * k + 1e-4)
            self.play(Create(pl.parts[k]), pl.tr.animate.set_value(0.25 * (k + 1) - 1e-4), FadeIn(a3_closed(pl.pt(0.25 * k + 1e-6))),
                      FadeIn(a3_open(np.array([pl.x0 + 0.25 * (k + 1) * 4.2, pl.y0 + k * 1.05, 0.0]))), FadeIn(bl[k]), run_time=0.7, rate_func=linear)
        pl.tr.set_value(0.9999)
        self.wait(0.1)
        done(self)


# ═════════════════════════════ B22 · whole and leftover ═════════════════════════════
class B22_WholeAndLeftover(Scene):
    def construct(self):
        nl = number_line(-5.0, 5.0, 1.2, lo=0.0, hi=4.0, ticks=(0.0, 1.0, 2.0, 3.0, 4.0))
        ay = 1.2
        d = Dot(nl.at(2.75), radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.add(nl)
        self.play(GrowFromCenter(d), run_time=0.4)
        until(self, "Floor is the whole part")
        b1 = a3_bracket(nl.at(0)[0], nl.at(2)[0], 0.15, DIM)
        l1 = M("floor = 2", 32).move_to([(nl.at(0)[0] + nl.at(2)[0]) / 2, -0.4, 0])
        self.play(Create(b1), FadeIn(l1), run_time=0.7)
        until(self, "fract is the leftover")
        b2 = a3_bracket(nl.at(2)[0], nl.at(2.75)[0], 0.15, TEAL)
        l2 = M("fract = 0.75", 32).move_to([(nl.at(2)[0] + nl.at(2.75)[0]) / 2 + 0.1, -0.4, 0])
        self.play(Create(b2), FadeIn(l2), run_time=0.7)
        until(self, "Two point seven five is")
        eq = T("2.75 = 2 + 0.75", 44).move_to([0.0, -1.5, 0])
        self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.6)
        # the dot slides 0 to 4: floor steps, fract resets
        until(self, "So floor says", lead=0.3)
        tr = ValueTracker(2.75)
        self.play(FadeOut(b1), FadeOut(b2), FadeOut(l1), FadeOut(l2), d.animate.move_to(nl.at(0.0)), run_time=0.5)
        tr.set_value(0.0)
        fl = lambda: int(np.floor(tr.get_value() + 1e-9))
        fr = lambda: tr.get_value() - np.floor(tr.get_value() + 1e-9)
        whole = always_redraw(lambda: Dot(nl.at(float(fl())), radius=0.1, color=DIM))
        left = always_redraw(lambda: Line(nl.at(float(fl())), nl.at(tr.get_value()), color=TEAL, stroke_width=9).shift(DOWN * 0.0))
        rl = T("floor", 36).move_to([-3.6, -2.55, 0])
        rr = T("fract", 36).move_to([1.4, -2.55, 0])
        rn1 = always_redraw(lambda: M(str(fl()), 36).move_to([-2.5, -2.55, 0]))
        rn2 = always_redraw(lambda: M("%.2f" % fr(), 36).move_to([3.0, -2.55, 0]))
        d.add_updater(lambda m: m.move_to(nl.at(tr.get_value())))
        self.add(whole, left, rl, rr, rn1, rn2)
        self.play(tr.animate.set_value(4.0), run_time=2.7, rate_func=linear)
        done(self)


# ═════════════════════════════ B24 · mod, the remainder ═════════════════════════════
class B24_Remainder(Scene):
    def construct(self):
        parts = [M("mod(x, y)", 32), M("=", 32), M("x", 32), M("−", 32), M("y", 32), M("·", 32), M("floor(x / y)", 32)]
        a3_row(parts, 0.3, 0.0, 2.7)
        self.play(FadeIn(parts[0]), FadeIn(parts[1]), run_time=0.5)
        until(self, "x minus", lead=0.2)
        self.play(FadeIn(parts[2], shift=UP * 0.2), FadeIn(parts[3], shift=UP * 0.2), run_time=0.5)
        until(self, "y times", lead=0.2)
        self.play(FadeIn(parts[4], shift=UP * 0.2), FadeIn(parts[5], shift=UP * 0.2), run_time=0.5)
        until(self, "floor of", lead=0.2)
        self.play(FadeIn(parts[6], shift=UP * 0.2), run_time=0.6)
        # card: y = 1 is fract
        until(self, "With y equal to one", lead=0.2)
        card = RoundedRectangle(width=5.0, height=1.6, corner_radius=0.16, stroke_color=DIM, stroke_width=3).set_fill("#FFFFFF", opacity=1).move_to([3.5, 0.7, 0])
        c1 = M("y = 1", 32).move_to([3.5, 1.05, 0])
        c2a = T("same as", 32); c2b = M("fract(x)", 32)
        a3_row([c2a, c2b], 0.25, 3.5, 0.35)
        self.play(Create(card), FadeIn(c1), FadeIn(c2a), FadeIn(c2b), run_time=0.7)
        # y = 0.25: four teeth
        until(self, "With y of point two five", lead=0.6)
        pl = a3_plot(lambda x: a3_curve("mod_quarter_x4")(x) / 4.0, [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0)],
                     strip_fn=a3_curve("mod_quarter_x4"), x=-2.2, y=0.0, size=3.6, y_range=(0.0, 0.25), in_labels=("0", "1"), out_labels=("0", "0.25"))
        self.play(Create(pl), run_time=0.5)
        self.add(pl.tiles)
        a3_reveal(pl)
        self.play(LaggedStart(*[Create(c) for c in pl.parts], lag_ratio=0.6), run_time=0.9)
        sz = pl.size
        marks = VGroup(*[a3_closed(pl.pt(i * 0.25 + 1e-6)) for i in range(4)],
                       *[a3_open(np.array([pl.x0 + i * 0.25 * sz, pl.y0 + sz, 0.0])) for i in range(1, 5)])
        cap1 = M("y = 0.25", 32).move_to([3.5, -0.75, 0])
        cap2 = T("repeats every 0.25", 32).move_to([3.5, -1.3, 0])
        note = T("× 4 to fit", 32).move_to([1.7, pl.ystrip, 0])
        self.play(FadeIn(marks), FadeIn(cap1), FadeIn(cap2), FadeIn(note), run_time=0.4)
        self.add(pl.drop, pl.dot)
        self.play(pl.tr.animate.set_value(0.9999), run_time=1.8, rate_func=linear)
        done(self)
