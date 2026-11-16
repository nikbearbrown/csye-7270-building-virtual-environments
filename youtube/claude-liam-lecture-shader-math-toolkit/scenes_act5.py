"""ACT V · Build a Ring (B37).  The standard plot with the input as the distance d (0 to 0.7)."""


def a5_step(edge, x):
    """Same formula as plot_data.step (a5_ copy: Gate A runs scenes.py without evidence/, where PD is None)."""
    return np.where(x < edge, 0.0, 1.0)


class B37_TwoCuts(Scene):
    def construct(self):
        fA = lambda u: a5_step(0.3, 0.7 * u)
        fB = lambda u: a5_step(0.38, 0.7 * u)
        fR = lambda u: a5_step(0.3, 0.7 * u) - a5_step(0.38, 0.7 * u)   # = PD.CURVES["ring_profile_hard"]
        g = plot_with_strip(fR, x=-1.2, y=0.45, size=3.8)
        lab = g[3]
        lab[2].become(T("distance", 32).move_to([g.x1 + 1.1, g.y0 - 0.38, 0]))
        lab[1].become(T("0.7", 32).move_to([g.x1, g.y0 - 0.38, 0]))
        one = T("1", 32).move_to([g.x0 - 0.3, g.y0 + g.size, 0])
        s0 = T("0", 32).move_to([g.x0, g.ystrip - 0.55, 0]); s1 = T("0.7", 32).move_to([g.x1, g.ystrip - 0.55, 0])
        ghost = Rectangle(width=g.size + 0.15, height=0.62, stroke_color=GHOST, stroke_width=3).move_to([g.x0 + g.size / 2, g.ystrip, 0])

        def curve(fn, color, w):
            xs = np.linspace(0, 1, 400)
            ys = [g.pt(v)[1] for v in xs]
            pts = [np.array([g.x0 + v * g.size, g.y0 + float(fn(np.array([v]))[0]) * g.size, 0.0]) for v in xs]
            return VMobject(stroke_color=color, stroke_width=w).set_points_as_corners(pts)
        cA = curve(fA, "#B9B4A6", 8); cB = curve(fB, DIM, 8)
        pulse = curve(fR, INK, 12)
        tag = a1_tag = M("ring = step(0.3, d) - step(0.38, d)", 32).move_to([0.2, 3.05, 0])
        # legend (right)
        def leg(txt, y, color, w):
            return VGroup(Line([2.9, y, 0], [3.5, y, 0], color=color, stroke_width=w), T(txt, 32).move_to([4.35, y, 0]))
        lA = leg("A", 1.5, "#B9B4A6", 8); lB = leg("B", 0.8, DIM, 8); lR = leg("A - B", 0.1, INK, 12)
        g.tiles.set_fill(opacity=0)
        self.add(g.axes, lab[2], one, s0, s1, ghost, tag)
        until(self, "Step at point three is", lead=0.1)
        self.play(Create(cA), FadeIn(lA), run_time=1.0)
        until(self, "Step at point three eight", lead=0.1)
        self.play(Create(cB), FadeIn(lB), run_time=0.9)
        until(self, "The first minus the second", lead=0.0)
        for t in g.tiles:
            pass
        # light the strip band: true gray of the pulse value
        pitch = g.size / 64
        for i, t in enumerate(g.tiles):
            v = float(fR(np.array([i / 63.0]))[0])
            gg = int(round(255 * v)); t.set_fill(color="#%02x%02x%02x" % (gg, gg, gg))
        fade_lim = ValueTracker(0.0)
        g.tiles.add_updater(lambda m: [t.set_fill(opacity=1.0 if t.get_center()[0] <= g.x0 + fade_lim.get_value() * g.size + pitch * 0.5 else 0.0) for t in m])
        self.add(g.tiles)
        self.play(Create(pulse), FadeIn(lR), fade_lim.animate.set_value(1.0), run_time=1.1)
        until(self, "a pulse", lead=0.9)
        g.tracker.set_value(0.0)
        self.add(g.drop, g.dot)
        self.play(FadeIn(g.dot, scale=0.4), run_time=0.3)
        self.play(g.tracker.animate.set_value(1.0), run_time=0.8, rate_func=linear)
        done(self)
