"""Act V · When It Looks Wrong (B36 only here; the rest are captures). Numbers measured (Lab 11/15, 10/14 probes): vertex-stage corner (-64, -64);
fragment-stage first pixel of the sprite about (576, 296) in a 1280 x 720 window."""


def a5_dot(p):
    return Dot(np.array(p, dtype=float), radius=0.16, color=TERRA).set_stroke(DIM, width=3)


class B36_TwoMeanings(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        fw, fh, fcx, fcy = 7.6, 4.275, 0.0, 0.95
        k = fw / 1280.0
        frame = Rectangle(width=fw, height=fh, stroke_color=DIM, stroke_width=5).move_to([fcx, fcy, 0])
        sp = Square(side_length=128 * k, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=0.9).move_to([fcx, fcy, 0])
        tl = np.array([fcx - 64 * k, fcy + 64 * k, 0]); mid = np.array([fcx, fcy, 0]); ftl = np.array([fcx - fw / 2, fcy + fh / 2, 0])
        dim = T("1280 × 720", 32, DIM).move_to([fcx + 2.6, fcy - 1.7, 0])
        credit = T("measured in Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -3.1, 0])
        self.add(frame, sp)
        self.play(FadeIn(dim), FadeIn(credit), run_time=0.5)
        corner = a5_dot(tl)
        rg = ring(Circle(radius=0.14).move_to(tl), pad=0.03, sw=6)
        self.play(FadeIn(corner, scale=1.6), FadeIn(rg), run_time=0.5)
        until(self, "In vertex", lead=0.2)
        mk = Dot(mid, radius=0.07, color=INK)
        a1 = arrow(mid, tl + np.array([0.17, -0.17, 0]), color=INK, w=6, tip=0.12)
        n1 = M("vertex()", 32).move_to([-3.4, -1.7, 0]); v1 = M("(-64, -64)", 32).move_to([-3.4, -2.15, 0]); w1 = T("from the node's middle", 32).move_to([-3.4, -2.6, 0])
        self.play(FadeIn(mk), GrowArrow(a1), FadeIn(n1), FadeIn(v1), FadeIn(w1), run_time=0.8)
        until(self, "In fragment", lead=0.2)
        a2 = arrow(ftl, tl + np.array([-0.2, 0.2, 0]), color=INK, w=5, tip=0.16)
        n2 = M("fragment()", 32).move_to([3.4, -1.7, 0]); v2 = M("(576, 296)", 32).move_to([3.4, -2.15, 0]); w2 = T("from the screen's top left", 32).move_to([3.4, -2.6, 0])
        self.play(GrowArrow(a2), FadeIn(n2), FadeIn(v2), FadeIn(w2), run_time=0.8)
        done(self)
