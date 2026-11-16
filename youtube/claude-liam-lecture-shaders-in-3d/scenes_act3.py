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
