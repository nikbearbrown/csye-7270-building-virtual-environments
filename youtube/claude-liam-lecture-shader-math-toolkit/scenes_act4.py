"""ACT IV · Distance and Curves (B26 B27 B28 B30 B32 B34), Manim drawings only.

Cast: the vector arrow (3, 4) on axes with the origin at the TOP LEFT (y counts down, labelled once in B26); the UV square with the "middle" dot;
the standard plot frame. Own plot helper a4_* replaces _kit_extra.plot_with_strip, whose strip tiles are the identity ramp for every curve (it ignores fn):
here every tile is the true gray of the CURVE's value at that x (PD.CURVES formulas), revealed as the dot passes.
"""
try:
    PD
except NameError:
    PD = None


def a4_f(name):
    """numpy function for a curve name from plot_data (fallbacks are the same formulas)."""
    if PD is not None and name in PD.CURVES:
        return PD.CURVES[name][1]
    return {"pow_3": lambda x: x ** 3.0, "pow_half": lambda x: x ** 0.5, "identity": lambda x: x,
            "sine_two_cycles": lambda x: 0.5 + 0.5 * np.sin(x * 4.0 * np.pi)}[name]


def a4_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a4_m(s, x, y, size=32, color=INK):
    return M(s, size, color).move_to([x, y, 0])


def a4_axes(O, s, lx, ly):
    """Axes with the origin at the top left, y counting down. lx, ly = lengths in units."""
    ax = arrow([O[0], O[1], 0], [O[0] + lx * s, O[1], 0], color=DIM, w=5, tip=0.2)
    ay = arrow([O[0], O[1], 0], [O[0], O[1] - ly * s, 0], color=DIM, w=5, tip=0.2)
    return VGroup(ax, ay)


def a4_strip(fn, x0, size, y, n=64, h=0.5):
    """64 narrow tiles with gaps in TRUE grays: tile i is gray(fn(i/(n-1))). Returns VGroup with .xs (x of each tile in 0..1)."""
    pitch = size / n
    tiles = VGroup()
    for i in range(n):
        v = float(np.clip(fn(np.array([i / (n - 1)]))[0], 0.0, 1.0))
        g = int(round(255 * v))
        tiles.add(Rectangle(width=pitch * 0.78, height=h, fill_color="#%02x%02x%02x" % (g, g, g), fill_opacity=1, stroke_width=0).move_to([x0 + pitch * (i + 0.5), y, 0]))
    tiles.xs = [i / (n - 1) for i in range(n)]
    return tiles


def a4_reveal(tiles, tr):
    """Tiles are visible only up to the dot's x (the strip fills as the dot passes)."""
    def up(m):
        v = tr.get_value()
        for t, xv in zip(m, m.xs):
            t.set_fill(opacity=1.0 if xv <= v + 1e-6 else 0.0)
    tiles.add_updater(up)
    up(tiles)


# ═══════════════════════════════════════════ B26 ═══════════════════════════════════════════
class B26_HowLong(Scene):
    def construct(self):
        title = T("Distance and Curves", 40).to_corner(UL, buff=0.95)
        O = np.array([-4.2, 1.5, 0]); s = 0.85
        axes = a4_axes(O, s, 5.4, 4.0)
        xl = a4_t("x", O[0] + 5.4 * s + 0.4, O[1])
        ydown = a4_t("y counts down", O[0], O[1] - 4.0 * s - 0.4)
        tip = O + np.array([3 * s, -4 * s, 0])
        corner = O + np.array([3 * s, 0, 0])
        tag = chip("length(v)", 3.6, 2.45)
        gloss = a4_t("the length of a vector", 3.6, 1.7)
        self.add(title)
        self.play(Create(axes), FadeIn(xl), FadeIn(ydown), FadeIn(tag), FadeIn(gloss), run_time=1.0)
        until(self, "A vector bundles them")
        vec = vec_arrow(O, tip, color=INK, w=8)
        vlab = a4_t("v = (3, 4)", tip[0] + 0.15 + 1.1, tip[1] - 0.15)
        self.play(Create(vec), run_time=1.1)
        self.play(FadeIn(vlab), run_time=0.5)
        until(self, "Three across and four down")
        leg_a = DashedLine(O, corner, color=TEAL, stroke_width=8, dash_length=0.14)
        leg_b = DashedLine(corner, tip, color=TEAL, stroke_width=8, dash_length=0.14)
        la = a4_t("3", (O[0] + corner[0]) / 2, O[1] + 0.4)
        lb = a4_t("4", corner[0] + 0.4, (corner[1] + tip[1]) / 2)
        self.play(Create(leg_a), FadeIn(la), run_time=0.7)
        self.play(Create(leg_b), FadeIn(lb), run_time=0.8)
        until(self, "has length five")
        mid = (O + tip) / 2
        five = a4_t("5", mid[0] + 0.55, mid[1] + 0.05, 48)
        self.play(FadeIn(five, scale=1.6), run_time=0.5)
        until(self, "the square root of nine")
        f1 = a4_m("√(x² + y²)", 3.6, 0.55)
        f2 = a4_m("3² + 4² = 25", 3.6, -0.45)
        self.play(FadeIn(f1), run_time=0.5)
        self.play(FadeIn(f2), run_time=0.5)
        done(self)


# ═══════════════════════════════════════════ B27 ═══════════════════════════════════════════
class B27_UnitArrow(Scene):
    def construct(self):
        O = np.array([-4.5, 2.3, 0]); s = 1.0
        axes = a4_axes(O, s, 5.0, 4.6)
        arc = Arc(radius=1.0, start_angle=0, angle=-PI / 2, arc_center=O, stroke_color=TEAL, stroke_width=8)
        ulab = a4_t("unit circle", O[0] + 1.5, O[1] + 0.55)
        tag = chip("normalize(v)", 3.4, 2.4)
        sub = a4_t("same direction, length 1", 3.4, 1.65)
        self.play(Create(axes), Create(arc), FadeIn(ulab), FadeIn(tag), FadeIn(sub), run_time=1.0)
        d = np.array([0.6, -0.8, 0])
        tip = O + d * 5.0
        until(self, "Take the arrow")
        ghost = vec_arrow(O, tip, color=DIM, w=7)
        l5 = a4_t("length 5", tip[0] + 1.35, tip[1] + 1.2)
        self.play(Create(ghost), run_time=1.1)
        self.play(FadeIn(l5), run_time=0.5)
        until(self, "Normalize it and you get")
        k = ValueTracker(5.0)
        live = always_redraw(lambda: vec_arrow(O, O + d * k.get_value(), color=INK, w=8))
        self.add(live)
        self.play(k.animate.set_value(1.0), run_time=1.5, rate_func=smooth)
        land = Dot(O + d * 1.0, radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        pl = a4_t("(0.6, 0.8)", O[0] + 0.6 + 1.75, O[1] - 0.8 + 0.1)
        self.play(FadeIn(land), FadeIn(pl), run_time=0.5)
        until(self, "length one")
        l1 = a4_t("length 1", O[0] + 0.6 + 1.5, O[1] - 0.8 - 0.55)
        self.play(ReplacementTransform(l5, l1), run_time=0.6)
        done(self)


# ═══════════════════════════════════════════ B28 ═══════════════════════════════════════════
class B28_AskEveryPixel(Scene):
    def construct(self):
        uv = uv_square(size=4.4, x=-1.8, y=-0.35)
        t1 = a4_m("distance(a, b)", 3.2, 2.25)
        t2 = a4_m("= length(a − b)", 3.2, 1.6)
        self.play(Create(uv), FadeIn(t1), FadeIn(t2), run_time=1.0)
        until(self, "Pick the middle")
        P = uv.pt
        mid = Dot(P(0.5, 0.5), radius=0.18, color=TERRA).set_stroke(DIM, width=3)
        mlab = a4_t("middle", P(0.5, 0.5)[0] - 0.95, P(0.5, 0.5)[1] + 0.4)
        self.play(FadeIn(mid, scale=1.5), FadeIn(mlab), run_time=0.6)

        def pix(u, v, txt, off):
            p = P(u, v)
            dot = Dot(p, radius=0.15, color=TEAL)
            ln = DashedLine(P(0.5, 0.5), p, color=DIM, stroke_width=4, dash_length=0.12)
            lab = a4_t(txt, p[0] + off[0], p[1] + off[1])
            return ln, dot, lab

        until(self, "ask every pixel")
        for (u, v, txt, off) in [(0.9, 0.5, "0.40", (0.8, 0.0)), (0.5, 0.2, "0.30", (0.0, 0.42)), (0.15, 0.85, "0.49", (0.0, -0.42))]:
            ln, dot, lab = pix(u, v, txt, off)
            self.play(Create(ln), FadeIn(dot, scale=1.4), FadeIn(lab), run_time=0.6)
        until(self, "small numbers")
        ln, dot, lab = pix(0.55, 0.55, "0.07", (0.65, -0.1))
        self.play(Create(ln), FadeIn(dot, scale=1.4), FadeIn(lab), run_time=0.7)
        until(self, "big ones", lead=0.6)
        ln, dot, lab = pix(0.95, 0.95, "0.64", (-0.75, 0.0))
        self.play(Create(ln), FadeIn(dot, scale=1.4), FadeIn(lab), run_time=0.5)
        done(self)


# ═══════════════════════════════════════════ B30 ═══════════════════════════════════════════
def a4_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B30_RoundOnSquare(Scene):
    def construct(self):
        L = -2.5; cy = -0.3; S = 3.0
        sq = Rectangle(width=S, height=S, stroke_color=INK, stroke_width=6).move_to([L + S / 2, cy, 0])
        circ = Ellipse(width=0.6 * S, height=0.6 * S, stroke_color=TEAL, stroke_width=8).move_to([L + S / 2, cy, 0])

        def top(width):
            y = cy + S / 2 + 0.55
            g = VGroup(a4_t("0", L, y), a4_t("1", L + width, y), arrow([L + 0.45, y, 0], [L + width - 0.45, y, 0], color=DIM, w=5, tip=0.2))
            return g
        t0 = top(S)
        y_top = cy + S / 2; y_bot = cy - S / 2
        lx = L - 0.65
        left = VGroup(a4_t("0", lx, y_top - 0.1), a4_t("1", lx, y_bot + 0.1), arrow([lx, y_top - 0.6, 0], [lx, y_bot + 0.6, 0], color=DIM, w=5, tip=0.2))
        cap1 = a4_t("square: round", L + S / 2, -2.35)
        self.play(Create(sq), Create(circ), FadeIn(t0), FadeIn(left), FadeIn(cap1), run_time=1.0)
        until(self, "On a wide one")
        pt = np.array([L, cy, 0])
        t1 = top(2 * S)
        self.play(sq.animate.stretch(2, 0, about_point=pt), circ.animate.stretch(2, 0, about_point=pt),
                  ReplacementTransform(t0, t1), run_time=1.6, rate_func=smooth)
        cap2 = a4_t("wide: oval", L + S, -2.35)
        self.play(ReplacementTransform(cap1, cap2), run_time=0.5)
        until(self, "The address always runs")
        r1 = a4_ubar(t1, pad=0.15); r2 = a4_ubar(left, pad=0.15)
        self.play(Create(r1), Create(r2), run_time=0.7)
        until(self, "whatever the proportions")
        cr = a4_t("measured: 384 × 192 px · Godot 4.7.2 · Forward+", 0.0, -3.0, 32, DIM)
        self.play(FadeIn(cr), run_time=0.6)
        done(self)


# ═══════════════════════════════════════════ B32 ═══════════════════════════════════════════
class B32_BendTheCurve(Scene):
    def construct(self):
        size = 4.0; cx = -2.0; cy = 0.9
        x0 = cx - size / 2; y0 = cy - size / 2; ys = y0 - 0.95
        axes = VGroup(Line([x0, y0, 0], [x0 + size, y0, 0], color=INK, stroke_width=5), Line([x0, y0, 0], [x0, y0 + size, 0], color=INK, stroke_width=5))
        labs = VGroup(a4_t("0", x0, y0 - 0.38), a4_t("1", x0 + size, y0 - 0.38), a4_t("input", cx, ys - 0.55),
                      a4_t("1", x0 - 0.35, y0 + size), a4_t("0", x0 - 0.35, y0))
        outl = T("output", 32).rotate(PI / 2).move_to([x0 - 0.95, cy, 0])
        tag = chip("pow(x, y)", 3.5, 2.45)
        sub = a4_t("x to the power y", 3.5, 1.7)

        def pt_of(fn):
            return lambda xv: np.array([x0 + xv * size, y0 + float(fn(np.array([xv]))[0]) * size, 0.0])

        def mk_curve(fn, color, w=8):
            p = pt_of(fn)
            c = VMobject(stroke_color=color, stroke_width=w)
            c.set_points_as_corners([p(v) for v in np.linspace(0, 1, 100)])
            return c

        tr = ValueTracker(0.0)

        def mk_dot(fn):
            p = pt_of(fn)
            d = Dot(p(0.0), radius=0.15, color=TERRA).set_stroke(DIM, width=3)
            d.add_updater(lambda m: m.move_to(p(tr.get_value())))
            dl = DashedLine(p(0.0), [x0, ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)
            dl.add_updater(lambda m: m.become(DashedLine(p(tr.get_value()), [x0 + tr.get_value() * size, ys + 0.25, 0], color=DIM, stroke_width=3, dash_length=0.1)))
            return d, dl

        f3, fh, f1 = a4_f("pow_3"), a4_f("pow_half"), a4_f("identity")
        self.play(Create(axes), FadeIn(labs), FadeIn(outl), FadeIn(tag), FadeIn(sub), run_time=1.0)

        def legend(row, txt, color):
            y = 0.8 - row * 0.75
            return VGroup(Line([1.7, y, 0], [2.4, y, 0], color=color, stroke_width=9), a4_m(txt, 0, y).align_to([2.7, y, 0], LEFT))

        until(self, "On a ramp from zero to one")
        c3 = mk_curve(f3, INK); lg3 = legend(0, "x^3", INK)
        d, dl = mk_dot(f3)
        tiles = a4_strip(f3, x0, size, ys)
        tr.set_value(0.0)
        a4_reveal(tiles, tr)
        self.add(tiles)
        self.play(Create(c3), FadeIn(lg3), run_time=1.2)
        self.add(d, dl)
        until(self, "a power above one")
        self.play(tr.animate.set_value(0.5), run_time=1.0, rate_func=linear)
        until(self, "so only the far end")
        self.play(tr.animate.set_value(1.0), run_time=1.3, rate_func=linear)
        # power 1/2
        until(self, "Below one")
        tiles.clear_updaters(); d.clear_updaters(); dl.clear_updaters()
        self.remove(d, dl, tiles)
        c3.set_stroke(opacity=0.35)
        ch = mk_curve(fh, TEAL); lgh = legend(1, "x^0.5", TEAL)
        tiles = a4_strip(fh, x0, size, ys)
        tr.set_value(0.0)
        d, dl = mk_dot(fh)
        a4_reveal(tiles, tr)
        self.add(tiles)
        self.play(Create(ch), FadeIn(lgh), run_time=0.8)
        self.add(d, dl)
        self.play(tr.animate.set_value(1.0), run_time=1.1, rate_func=linear)
        until(self, "Exactly one")
        tiles.clear_updaters(); d.clear_updaters(); dl.clear_updaters()
        self.remove(d, dl, tiles)
        ch.set_stroke(opacity=0.35)
        c1 = mk_curve(f1, DIM); lg1 = legend(2, "x", DIM)
        tiles = a4_strip(f1, x0, size, ys)
        tr.set_value(0.0)
        d, dl = mk_dot(f1)
        a4_reveal(tiles, tr)
        self.add(tiles)
        self.play(Create(c1), FadeIn(lg1), run_time=0.6)
        self.add(d, dl)
        self.play(tr.animate.set_value(1.0), run_time=0.7, rate_func=linear)
        done(self)


# ═══════════════════════════════════════════ B34 ═══════════════════════════════════════════
class B34_SmoothRepeat(Scene):
    def construct(self):
        W = 4.6; H = 2.6; cx = -2.3; cy = 0.65
        x0 = cx - W / 2; yb = cy - H / 2; ym = cy
        sf = a4_f("sine_two_cycles")
        raw = lambda x: 2.0 * sf(x) - 1.0
        ys = yb - 0.95
        axes = VGroup(Line([x0, yb, 0], [x0, yb + H, 0], color=INK, stroke_width=5), Line([x0, ym, 0], [x0 + W, ym, 0], color=INK, stroke_width=5))
        tick_lo = a4_t("−1", x0 - 0.55, yb); tick_hi = a4_t("1", x0 - 0.35, yb + H)
        tick_0 = a4_t("0", x0 - 0.35, ym)
        ainp = a4_t("input", cx, yb - 0.4)
        a = ValueTracker(1.0); c = ValueTracker(0.0); tr = ValueTracker(0.0)

        def pt(xv):
            lv = c.get_value() + a.get_value() * float(raw(np.array([xv]))[0])
            return np.array([x0 + xv * W, ym + lv * H / 2, 0.0])

        curve = always_redraw(lambda: VMobject(stroke_color=INK, stroke_width=8).set_points_as_corners([pt(v) for v in np.linspace(0, 1, 140)]))
        dot = Dot(pt(0.0), radius=0.15, color=TERRA).set_stroke(DIM, width=3)
        dot.add_updater(lambda m: m.move_to(pt(tr.get_value())))
        tag = a4_m("sin(x)", 3.3, 2.45)
        s1 = a4_t("a smooth wave", 3.4, 1.7)
        s2 = a4_t("between −1 and 1", 3.4, 1.15)
        self.play(Create(axes), FadeIn(ainp), FadeIn(tag), run_time=0.9)
        until(self, "Sine repeats smoothly")
        self.add(curve)
        self.play(FadeIn(tick_lo), FadeIn(tick_hi), FadeIn(tick_0), FadeIn(s1), FadeIn(s2), run_time=0.6)
        self.add(dot)
        self.play(tr.animate.set_value(1.0), run_time=2.4, rate_func=linear)
        until(self, "Half of sine")
        newhi = a4_t("1", x0 - 0.35, ym + H / 2)
        newlo = a4_t("0", x0 - 0.35, ym)
        tiles = a4_strip(sf, x0, W, ys)
        for t in tiles:
            t.set_fill(opacity=0)
        self.play(a.animate.set_value(0.5), c.animate.set_value(0.5), FadeOut(tick_lo), FadeOut(tick_hi), FadeOut(tick_0),
                  FadeOut(s1), FadeOut(s2), run_time=1.4, rate_func=smooth)
        sq = a4_m("0.5 + 0.5 · sin(x)", 3.3, 1.7)
        self.play(FadeIn(newhi), FadeIn(newlo), FadeIn(sq), run_time=0.5)
        self.add(tiles)
        self.play(*[t.animate.set_fill(opacity=1) for t in tiles], run_time=0.8)
        until(self, "smooth cousin")
        # fract(2x) teeth in 0..1, a faint ghost
        ph = lambda xv, v: [x0 + xv * W, ym + v * H / 2, 0]
        ghost = VGroup(Line(ph(0, 0), ph(0.5, 1), color=DIM, stroke_width=5), Line(ph(0.5, 0), ph(1, 1), color=DIM, stroke_width=5),
                       DashedLine(ph(0.5, 1), ph(0.5, 0), color=DIM, stroke_width=4, dash_length=0.1)).set_opacity(0.8)
        cap = a4_t("smooth cousin", 3.4, 0.4)
        cap2 = a4_t("of fract", 3.4, -0.2)
        self.play(Create(ghost), FadeIn(cap), FadeIn(cap2), run_time=1.0)
        done(self)
