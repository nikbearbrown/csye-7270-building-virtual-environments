"""ACT I · Ramps and Plots (B02, B04, B05, B06).  Manim scenes; kit + _kit_extra pasted above by the assembler.
Cast: the ramp strip (64 narrow true-gray tiles with gaps) with its terracotta dot; the standard plot frame (axes, curve, dot, drop line, strip)."""


def a1_tag(s, x, y, size=32):
    return M(s, size).move_to([x, y, 0])


def a1_plot(fn_ref, x=-2.4, y=0.85, size=3.8):
    """The standard plot via plot_with_strip, with a1 fixes: the 'input' label moved off the drop line, strip end labels, an 'output' label up the side.
    fn_ref is a callable on a numpy array (may read a mutable blend)."""
    g = plot_with_strip(fn_ref, x=x, y=y, size=size)
    lab = g[3]
    lab[2].move_to([g.x1 + 1.0, g.y0 - 0.38, 0])
    out_l = T("output", 32).rotate(PI / 2).move_to([g.x0 - 0.5, g.y0 + size / 2 + 0.2, 0])
    one = T("1", 32).move_to([g.x0 - 0.3, g.y0 + size, 0])
    s0 = T("0", 32).move_to([g.x0, g.ystrip - 0.55, 0]); s1 = T("1", 32).move_to([g.x1, g.ystrip - 0.55, 0])
    g.axlabels = VGroup(one)   # the bottom 0/1 ticks are dropped: the drop line crosses them; the strip end labels carry 0 and 1
    g.input_lab = lab[2]; g.output_lab = VGroup(out_l); g.stripends = VGroup(s0, s1)
    return g


def a1_fill_updater(g, level):
    """Tiles whose centre x is left of the drop line become visible (true gray stays)."""
    tiles = g.tiles
    pitch = g.size / len(tiles)

    def upd(m):
        lim = g.x0 + g.tracker.get_value() * g.size + pitch * 0.6
        for t in m:
            t.set_fill(opacity=1.0 if t.get_center()[0] <= lim else 0.0)
    return upd


def a1_gray_strip(width=9.6, n=64, height=0.9, y=0.2):
    """ramp_strip's shape with TRUE grays (value v drawn as gray v) per the standard-plot law; kit ramp_strip is a teal-cream ramp."""
    pitch = width / n
    tiles = VGroup()
    for i in range(n):
        gg = int(round(255 * i / (n - 1)))
        tiles.add(Rectangle(width=pitch * 0.78, height=height, fill_color="#%02x%02x%02x" % (gg, gg, gg), fill_opacity=1, stroke_width=0).move_to([-width / 2 + pitch * (i + 0.5), y, 0]))
    g = VGroup(tiles, T("0", 32).move_to([-width / 2, y - height / 2 - 0.35, 0]), T("1", 32).move_to([width / 2, y - height / 2 - 0.35, 0]))
    g.x0 = -width / 2; g.x1 = width / 2; g.y = y; g.width_s = width
    return g


class B02_RampStrip(Scene):
    def construct(self):
        st = a1_gray_strip()
        self.add(st)
        cap = VGroup(T("ramp", 44, bold=True), T("a smooth run of values from 0 up to 1", 32)).arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to([0, 2.3, 0])
        until(self, "Start with a ramp", lead=0.1)
        self.play(FadeIn(cap), run_time=0.8)
        until(self, "The simplest ramp")
        tr = ValueTracker(0.0)
        dot = Dot([st.x0, st.y, 0], radius=0.2, color=TERRA).set_stroke(DIM, width=3)
        dot.add_updater(lambda m: m.move_to([st.x0 + st.width_s * tr.get_value(), st.y, 0]))
        lbl = always_redraw(lambda: T("pixel  %.1f" % tr.get_value(), 32).move_to([max(st.x0 + 0.4, min(st.x1 - 0.8, st.x0 + st.width_s * tr.get_value())), st.y + 1.0, 0]))
        self.play(FadeIn(dot, scale=0.4), FadeIn(lbl), run_time=0.6)
        until(self, "zero at the left edge")
        self.play(tr.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        until(self, "In code")
        tag = a1_tag("UV.x  ·  across the shape", 0, -1.75)
        self.play(FadeIn(tag), run_time=0.6)
        done(self)


class B04_ReadThePlot(Scene):
    def construct(self):
        g = a1_plot(lambda xs: PD.CURVES["identity"][1](xs) if PD else xs)
        g.tiles.set_fill(opacity=0)
        self.add(g.axes, g.axlabels)
        ghost = Rectangle(width=g.size + 0.15, height=0.62, stroke_color=GHOST, stroke_width=3).move_to([g.x0 + g.size / 2, g.ystrip, 0])
        until(self, "The input runs")
        self.play(FadeIn(g.input_lab), run_time=0.6)
        until(self, "the output up the side")
        self.play(FadeIn(g.output_lab), run_time=0.6)
        until(self, "A dot travels", lead=1.4)
        g.tiles.add_updater(a1_fill_updater(g, 0))
        self.add(g.tiles)
        self.play(Create(g.curve), FadeIn(ghost), FadeIn(g.stripends), run_time=1.0)
        g.tracker.set_value(0.0)
        self.add(g.drop, g.dot)
        self.play(FadeIn(g.dot, scale=0.4), run_time=0.4)
        self.play(g.tracker.animate.set_value(0.5), run_time=0.7)
        until(self, "and the strip below shows", lead=0.0)
        self.play(g.tracker.animate.set_value(1.0), run_time=2.2, rate_func=linear)
        until(self, "A function that changes nothing")
        tag = a1_tag("f(x) = x", 3.3, 1.9)
        credit = T("curves drawn from the formulas  ·  checked against Godot 4.7.2 renders", 32, color=DIM).move_to([0, -3.05, 0])
        self.play(g.curve.animate.set_stroke(color=INK, width=10), FadeIn(tag), FadeIn(credit), run_time=0.8)
        done(self)


class B05_BendTheLine(Scene):
    def construct(self):
        K = [0.0]   # line blend: 0 = x, 1 = 1 - x
        S = ValueTracker(0.0)   # strip blend
        kt = ValueTracker(0.0)
        fn = lambda xs: (1 - K[0]) * xs + K[0] * (1 - xs)
        g = a1_plot(fn)
        # curve and tiles follow the blends
        xs = np.linspace(0, 1, 120)

        def curve_upd(m):
            K[0] = kt.get_value()
            m.set_points_as_corners([g.pt(v) for v in xs])
        g.curve.add_updater(curve_upd)
        pitch = g.size / 64

        def tile_upd(m):
            s = S.get_value()
            for i, t in enumerate(m):
                v0 = i / 63.0
                v = (1 - s) * v0 + s * (1 - v0)
                gg = int(round(255 * v))
                t.set_fill(color="#%02x%02x%02x" % (gg, gg, gg), opacity=1)
        g.tiles.add_updater(tile_upd)
        g.curve.set_stroke(color=INK, width=10)
        ghost = Rectangle(width=g.size + 0.15, height=0.62, stroke_color=GHOST, stroke_width=3).move_to([g.x0 + g.size / 2, g.ystrip, 0])
        tag = a1_tag("f(x) = x", 3.3, 1.9)
        self.add(g.axes, g.axlabels, g.input_lab, g.output_lab, g.stripends, ghost, g.tiles, g.curve, tag)
        until(self, "Bend the line", lead=0.0)
        self.wait(0.3)
        until(self, "Here the function is one minus x", lead=0.6)
        tag2 = a1_tag("f(x) = 1 - x", 3.3, 1.9)
        self.play(FadeTransform(tag, tag2), kt.animate.set_value(1.0), run_time=1.7)
        until(self, "The line runs downhill", lead=0.0)
        g.tracker.set_value(0.0)
        self.add(g.drop, g.dot)
        self.play(FadeIn(g.dot, scale=0.4), run_time=0.4)
        self.play(g.tracker.animate.set_value(0.5), run_time=0.6)
        # midpoint hold: strip still shows the old ramp
        until(self, "so the strip runs from white to black", lead=0.0)
        self.play(S.animate.set_value(1.0), run_time=1.0)
        until(self, "Read the line", lead=0.5)
        cap = T("predict the strip", 32, color=INK).move_to([3.3, -1.2, 0])
        self.play(g.tracker.animate.set_value(1.0), FadeIn(cap), run_time=1.6, rate_func=linear)
        done(self)


def a1_chip(text, x, y):
    t = M(text, 32)
    b = RoundedRectangle(width=t.width + 0.4, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3)
    g = VGroup(b, t).move_to([x, y, 0])
    return g


class B06_ToolkitMap(Scene):
    def construct(self):
        cols = [(-4.6, "Cut and blend", ["step", "smoothstep", "mix", "clamp"]),
                (-1.5, "Repeat and fold", ["abs", "fract", "floor", "mod"]),
                (2.35, "Distance and curves", ["length", "normalize", "distance", "pow", "sin"])]
        rows = [1.35, 0.5, -0.35, -1.2, -2.05]
        ring_c = np.array([5.45, -0.35, 0.0])
        titles = []; chips = []
        for cx, ttl, names in cols:
            titles.append(T(ttl, 32, bold=True).move_to([cx, 2.35, 0]))
            chips.append([a1_chip(n, cx, rows[i]) for i, n in enumerate(names)])
        outline = Annulus(inner_radius=0.5, outer_radius=0.8, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to(ring_c)
        self.add(outline)
        until(self, "About a dozen", lead=0.0)
        self.play(*[FadeIn(t) for t in titles], run_time=0.8)
        until(self, "Cut and blend:", lead=0.0)
        for c in chips[0]:
            self.play(FadeIn(c, scale=0.7), run_time=0.35)
            self.wait(0.15)
        until(self, "Repeat and fold:", lead=0.0)
        self.play(*[FadeIn(c, scale=0.7) for c in chips[1]], run_time=0.5)
        until(self, "Distance and curves:", lead=0.9)
        self.play(*[FadeIn(c, scale=0.7) for c in chips[2]], run_time=0.5)
        until(self, "Then we use three")
        # routes: smoothstep -> gap above mix row; mix -> gap below mix row; distance straight
        sm = chips[0][1]; mx = chips[0][2]; di = chips[2][2]
        def route(chip_, gap_y, tgt_dy):
            p0 = chip_.get_right() + np.array([0.0, 0.0, 0.0])
            p1 = np.array([p0[0] + 0.12, gap_y, 0.0]); p2 = np.array([4.3, gap_y, 0.0])
            p3 = ring_c + np.array([-0.8, tgt_dy, 0.0])
            return VMobject(stroke_color=DIM, stroke_width=3).set_points_as_corners([p0, p1, p2, p3])
        lines = [route(sm, 0.075, 0.30), route(mx, -0.775, -0.30), route(di, di.get_center()[1], 0.0)]
        self.play(*[Create(l) for l in lines], run_time=1.4)
        fill = Annulus(inner_radius=0.5, outer_radius=0.8, fill_opacity=0.95, fill_color=TEAL, stroke_color=INK, stroke_width=5).move_to(ring_c)
        self.play(FadeIn(fill), run_time=0.6)
        done(self)
