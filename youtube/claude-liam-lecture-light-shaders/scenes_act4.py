"""ACT IV · A Lighthouse (Manim beats B24, B25). Cast: the unit circle and the two arrows. Screen orientation: the vertical axis points DOWN,
so an angle `a` clockwise from right puts the arrow tip at (cos a, -sin a) in Manim's y-up frame. Drawings; the angle values are the lane's."""


def a4_tip(c, L, deg):
    r = np.radians(deg)
    return np.array([c[0] + L * np.cos(r), c[1] - L * np.sin(r), 0])


class B24_AimArrow(Scene):
    def construct(self):
        C = np.array([0.6, -0.3, 0.0]); R = 2.0
        title = T("A Lighthouse", 40).move_to([-6.1 + 1.3, 3.0, 0])
        circ = Circle(radius=R, stroke_color=INK, stroke_width=5).move_to(C)
        hline = Line(C + np.array([-R - 0.3, 0, 0]), C + np.array([R + 0.3, 0, 0]), color=GHOST, stroke_width=4)
        yax = arrow([-3.9, 1.3, 0], [-3.9, -1.6, 0], DIM, 5)
        ylab = T("y points down", 32).move_to([-4.2, -2.15, 0])
        ylab.set_x(-3.9)
        a = ValueTracker(20.0)
        def tip(): return a4_tip(C, R, a.get_value())
        arr = always_redraw(lambda: Arrow(C, tip(), buff=0, color=INK, stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.3))
        hseg = always_redraw(lambda: Line(C, [tip()[0], C[1], 0], color=DIM, stroke_width=9))
        vseg = always_redraw(lambda: Line([tip()[0], C[1], 0], tip(), color=DIM, stroke_width=9))
        arc = always_redraw(lambda: Arc(radius=0.7, start_angle=0, angle=-np.radians(a.get_value()), arc_center=C, color=INK, stroke_width=5))
        dot = always_redraw(lambda: Dot(tip(), radius=0.14, color=TERRA).set_stroke(DIM, width=3))
        lab = T("(cos a, sin a)", 32).move_to([4.4, 1.3, 0])
        cl = always_redraw(lambda: T("cos", 32, DIM).move_to([(C[0] + tip()[0]) / 2, C[1] + 0.4 if tip()[1] < C[1] else C[1] + 0.4, 0]))
        sl = always_redraw(lambda: T("sin", 32, DIM).move_to([tip()[0] + 0.55, (C[1] + tip()[1]) / 2, 0]))
        self.wait(0.3)
        self.play(FadeIn(title), Create(circ), FadeIn(hline), Create(yax), FadeIn(ylab), run_time=1.0)
        until(self, "Cosine and sine")
        self.add(arr, hseg, vseg, arc, dot)
        self.play(FadeIn(lab), FadeIn(cl), FadeIn(sl), run_time=0.6)
        self.wait(0.5)
        until(self, "Turn the angle")
        self.play(a.animate.set_value(85.0), run_time=2.2, rate_func=smooth)
        done(self)


class B25_Agree(Scene):
    def construct(self):
        P = np.array([-3.4, 0.9, 0.0]); L = 2.4; PIX = 25.0
        aim = ValueTracker(-40.0)
        pixarr = Arrow(P, a4_tip(P, L, PIX), buff=0, color=DIM, stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.3)
        pixlab = T("pixel arrow", 32, DIM).move_to([P[0] - 1.3, P[1] + 0.55, 0])
        aimarr = always_redraw(lambda: Arrow(P, a4_tip(P, L, aim.get_value()), buff=0, color=INK, stroke_width=8, tip_length=0.3, max_tip_length_to_length_ratio=0.3))
        aimdot = always_redraw(lambda: Dot(a4_tip(P, L, aim.get_value()), radius=0.14, color=TERRA).set_stroke(DIM, width=3))
        aimlab = always_redraw(lambda: T("aim", 32).move_to(a4_tip(P, L + 0.45, aim.get_value()) + np.array([0.45, 0.45, 0])))
        def dv(): return float(np.cos(np.radians(aim.get_value() - PIX)))
        def kept(): return dv() >= 0.95
        sector = always_redraw(lambda: Sector(radius=1.7, start_angle=-np.radians(PIX), angle=-np.radians(aim.get_value() - PIX), arc_center=P, fill_color=TEAL, fill_opacity=0.65, stroke_width=0)
                               if kept() and abs(aim.get_value() - PIX) > 0.5 else Sector(radius=1.7, start_angle=-np.radians(PIX), angle=0.0001, arc_center=P, fill_opacity=0, stroke_width=0))
        keptlab = always_redraw(lambda: T("kept", 32).move_to([P[0] + 0.9, P[1] - 1.55, 0]) if kept() else T("", 32).move_to([P[0] + 0.9, P[1] - 1.55, 0]))
        BX0, BX1, BY = 1.2, 5.8, 0.2
        def bx(v): return BX0 + (v + 1) / 2 * (BX1 - BX0)
        track = Line([BX0, BY, 0], [BX1, BY, 0], color=DIM, stroke_width=6)
        ticks = VGroup(*[Line([bx(v), BY - 0.15, 0], [bx(v), BY + 0.15, 0], color=DIM, stroke_width=5) for v in (-1, 0, 1)])
        tl = VGroup(*[T(s, 32).move_to([bx(v), BY - 0.5, 0]) for s, v in (("-1", -1), ("0", 0), ("1", 1))])
        t95 = Line([bx(0.95), BY - 0.3, 0], [bx(0.95), BY + 0.3, 0], color=INK, stroke_width=6)
        t95l = T("0.95", 32).move_to([bx(0.95) - 0.1, BY + 0.65, 0])
        mark = always_redraw(lambda: Dot([bx(dv()), BY, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3))
        dlab = T("dot =", 48).move_to([2.7, 1.9, 0])
        num = always_redraw(lambda: T("%.2f" % dv(), 48).move_to([3.6 + 0.0, 1.9, 0]).align_to([3.55, 0, 0], LEFT))
        cap1 = T("dot(a, b): multiply the matching parts and add them;", 32).move_to([0, -2.55, 0])
        cap2 = T("with a unit direction, how far a point lies along it", 32).move_to([0, -3.0, 0])
        self.wait(0.3)
        self.play(Create(pixarr), FadeIn(pixlab), FadeIn(track), FadeIn(ticks), FadeIn(tl), FadeIn(t95), FadeIn(t95l), FadeIn(dlab), run_time=0.9)
        self.add(aimarr, aimdot, aimlab, mark, num, sector, keptlab)
        self.play(FadeIn(cap1), FadeIn(cap2), run_time=0.5)
        until(self, "It is one when")
        self.play(aim.animate.set_value(PIX), run_time=2.0, rate_func=smooth)
        until(self, "zero at right angles")
        self.play(aim.animate.set_value(90.0), run_time=1.9, rate_func=smooth)
        until(self, "Keep the pixels")
        self.play(aim.animate.set_value(PIX + 4), run_time=1.5, rate_func=smooth)
        self.play(FadeIn(ring(t95l, pad=0.08)), run_time=0.4)
        done(self)
