"""ACT IV · An Orbit Around an Orbit  (B26, B30; Manim)

Cast: screen orientation for B26 (y down: a screen angle a puts a point at c + r*(cos a, -sin a) in scene coordinates); planet teal, moon slate-blue,
meteor amber, the same colours as the Lab renders. B30 is a drawing of the pattern (labelled by its two lines), paper orientation.
"""
A4_PLANET = "#5EA391"; A4_MOON = "#8099BF"; A4_METEOR = "#E6A640"


def a4_pt(c, r, a):
    """Scene point of a SCREEN angle a (clockwise, y down) at radius r round c (a scene point)."""
    return np.array([c[0] + r * np.cos(a), c[1] - r * np.sin(a), 0.0])


def a4_shaft(p, q, t0, t1, color=INK, w=9):
    """A thick arrow from p to q shortened by t0 at the tail and t1 at the tip (so it stops at the edge of a body)."""
    u = (q - p) / max(1e-6, np.linalg.norm(q - p))
    return arrow(p + u * t0, q - u * t1, color=color, w=w, tip=0.3)


class B26_Chain(Scene):
    def construct(self):
        title = T("An Orbit Around an Orbit", 40).to_corner(UL, buff=0.95)
        P = np.array([-0.9, -0.45, 0.0]); R = 2.55; r2 = 1.25
        am = ValueTracker(0.1); ab = ValueTracker(-2.3)
        moon_at = lambda: a4_pt(P, R, am.get_value())
        met_at = lambda: a4_pt(moon_at(), r2, ab.get_value())
        planet = Circle(radius=0.5, fill_color=A4_PLANET, fill_opacity=1, stroke_width=0).move_to(P)
        big_ring = Circle(radius=R, stroke_color=DIM, stroke_width=4).move_to(P)
        moon = always_redraw(lambda: Circle(radius=0.3, fill_color=A4_MOON, fill_opacity=1, stroke_width=0).move_to(moon_at()))
        small_ring = always_redraw(lambda: Circle(radius=r2, stroke_color=DIM, stroke_width=4).move_to(moon_at()))
        meteor = always_redraw(lambda: Circle(radius=0.2, fill_color=A4_METEOR, fill_opacity=1, stroke_width=0).move_to(met_at()))
        arr1 = always_redraw(lambda: a4_shaft(P, moon_at(), 0.5, 0.34))
        arr2 = always_redraw(lambda: a4_shaft(moon_at(), met_at(), 0.34, 0.24))
        dash = always_redraw(lambda: DashedLine(P, met_at(), color=DIM, stroke_width=5, dash_length=0.18))

        def lab(word, f, side, t=0.5, off=0.62):
            def mk():
                a, b = f()
                m = a + (b - a) * t; d = b - a
                n = np.array([-d[1], d[0], 0.0]); n = n / max(1e-6, np.linalg.norm(n)) * side
                return T(word, 32).move_to(m + n * off)
            return always_redraw(mk)
        l_moon = lab("moon", lambda: (P, moon_at()), -1, 0.4, 0.55)
        def mk_met():
            m0, m1 = moon_at(), met_at(); u = (m1 - m0) / np.linalg.norm(m1 - m0)
            return T("meteor", 32).move_to(m1 + u * 0.3 + np.array([u[0] * 0.55, u[1] * 0.3, 0]))
        l_met = always_redraw(mk_met)

        self.add(title, planet, big_ring)
        until(self, "Now a meteor")
        self.play(FadeIn(moon, scale=0.6), run_time=0.5)
        until(self, "The moon moves")
        self.play(FadeIn(arr1), FadeIn(l_moon), run_time=0.6)
        self.play(FadeIn(small_ring), FadeIn(meteor, scale=0.6), run_time=0.5)
        self.play(FadeIn(arr2), FadeIn(l_met), run_time=0.6)
        self.play(FadeIn(dash), run_time=0.5)
        until(self, "Positions add")
        self.play(am.animate.set_value(0.1 + 0.4), ab.animate.set_value(-0.8), run_time=1.8, rate_func=linear)
        done(self)


# ─────────────────────────── B30 · the arm ───────────────────────────
def a4_up(p, L, a):
    """Paper-orientation endpoint (y up) of a segment of length L at angle a from p."""
    return np.array([p[0] + L * np.cos(a), p[1] + L * np.sin(a), 0.0])


class B30_Arm(Scene):
    def construct(self):
        S0 = np.array([-2.0, -1.1, 0.0]); L1, L2, L3 = 2.3, 1.9, 1.5
        a1 = ValueTracker(0.6); a2 = ValueTracker(0.2); a3 = ValueTracker(0.5); k3 = ValueTracker(0.0)
        e1 = lambda: a4_up(S0, L1, a1.get_value())
        e2 = lambda: a4_up(e1(), L2, a2.get_value())
        e3 = lambda: a4_up(e2(), L3 * max(0.001, k3.get_value()), a3.get_value())
        seg1 = always_redraw(lambda: Line(S0, e1(), color=INK, stroke_width=14))
        seg2 = always_redraw(lambda: Line(e1(), e2(), color=INK, stroke_width=14))
        seg3 = always_redraw(lambda: Line(e2(), e3(), color=INK, stroke_width=14))
        j1 = always_redraw(lambda: Dot(e1(), radius=0.17, color=TEAL))
        j2 = always_redraw(lambda: Dot(e2(), radius=0.17, color=TEAL))
        j3 = always_redraw(lambda: Dot(e3(), radius=0.17, color=TEAL))
        shoulder = Dot(S0, radius=0.2, color=TERRA).set_stroke(DIM, width=3)

        l1 = M("center + radius * vec2(cos(a), sin(a))", 32)
        l1.move_to([-5.9 + l1.width / 2, -2.3, 0])
        l2 = M("elbow  + radius * vec2(cos(b), sin(b))", 32)
        l2.move_to([-5.9 + l2.width / 2, -3.0, 0])
        lab_e = always_redraw(lambda: T("elbow", 32).move_to(e1() + np.array([0.15, 0.55, 0])))
        lab_h = always_redraw(lambda: T("hand", 32).move_to((e3() if k3.get_value() > 0.05 else e2()) + np.array([0.75, 0.0, 0])))

        self.add(shoulder)
        until(self, "Any depth works", lead=0.0)
        self.play(Create(seg1), FadeIn(j1), run_time=0.7)
        self.add(seg1, j1)
        self.play(FadeIn(l1), run_time=0.5)
        until(self, "Each level")
        self.play(Create(seg2), FadeIn(j2), run_time=0.7)
        self.add(seg2, j2)
        self.play(FadeIn(l2), run_time=0.5)
        # a small wave of the two segments, back to rest before the midpoint
        self.play(a1.animate.set_value(0.85), a2.animate.set_value(0.0), run_time=0.8)
        self.play(a1.animate.set_value(0.6), a2.animate.set_value(0.2), run_time=0.8)
        until(self, "Chain two")
        self.play(FadeIn(lab_e), FadeIn(lab_h), run_time=0.5)
        until(self, "Chain three")
        self.add(seg3, j3)
        self.play(k3.animate.set_value(1.0), run_time=0.7)
        self.play(a1.animate.set_value(0.35), a2.animate.set_value(0.55), a3.animate.set_value(0.0), run_time=0.9)
        self.play(a1.animate.set_value(0.75), a2.animate.set_value(0.05), a3.animate.set_value(0.9), run_time=0.6)
        done(self)
