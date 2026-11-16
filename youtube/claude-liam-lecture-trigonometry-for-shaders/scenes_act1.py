"""ACT I · One Angle, Two Numbers  (B02-B05, Manim)

Cast for the act: the right triangle with its marked 30-degree corner at the lower left, right angle at the lower right.
Grey outline; a side that is being talked about thickens to ink. Drawings only (no captures); the numbers are the film's measured ones
(sin 30 = 0.50, sin 50 = 0.77, cos 30 = 0.87).
"""

A1_C30 = float(np.cos(np.radians(30))); A1_S30 = float(np.sin(np.radians(30)))


def a1_tri(ax, ay, hyp, deg):
    """Corners of a right triangle: A (marked corner, lower left), C (right angle, lower right), B (top). hyp = hypotenuse length."""
    a = np.radians(deg)
    A = np.array([ax, ay, 0.0]); C = A + np.array([hyp * np.cos(a), 0.0, 0.0]); B = C + np.array([0.0, hyp * np.sin(a), 0.0])
    return A, C, B


def a1_sides(A, C, B, color=DIM, w=5):
    """(hypotenuse A-B, opposite C-B, adjacent A-C) as separate Lines."""
    return (Line(A, B, color=color, stroke_width=w), Line(C, B, color=color, stroke_width=w), Line(A, C, color=color, stroke_width=w))


def a1_square_mark(C, s=0.28, color=DIM):
    """Right-angle mark at C (lower right): a small square tucked into the corner."""
    return VGroup(Line(C + [-s, 0, 0], C + [-s, s, 0], color=color, stroke_width=4), Line(C + [-s, s, 0], C + [0, s, 0], color=color, stroke_width=4))


def a1_arc_mark(A, r=0.85, deg=30):
    """The marked angle: a thick terracotta arc over a grey backing, and a small terracotta dot on the corner."""
    back = Arc(radius=r, start_angle=0, angle=np.radians(deg), arc_center=A, stroke_color=DIM, stroke_width=16, stroke_opacity=0.55)
    arc = Arc(radius=r, start_angle=0, angle=np.radians(deg), arc_center=A, stroke_color=TERRA, stroke_width=9)
    dot = Dot(A, radius=0.14, color=TERRA).set_stroke(DIM, width=3)
    return VGroup(back, arc, dot)


def a1_thick(mob, on=True):
    return mob.animate.set_color(INK if on else DIM).set_stroke(width=11 if on else 5)


# ═════════════════════════════ B02 · the names of the sides ═════════════════════════════
class B02_RightTriangle(Scene):
    def construct(self):
        A, C, B = a1_tri(-2.5, -1.55, 4.9, 30)
        hy, op, ad = a1_sides(A, C, B)
        sq = a1_square_mark(C)
        mark = a1_arc_mark(A)
        l_hy = T("hypotenuse", 40).move_to([-1.6, 0.85, 0])
        l_op = T("opposite", 40).move_to([C[0] + 1.35, (C[1] + B[1]) / 2, 0])
        l_ad = T("adjacent", 40).move_to([(A[0] + C[0]) / 2, C[1] - 0.7, 0])
        # the three sides draw as one triangle
        self.play(Create(ad), Create(op), Create(hy), run_time=1.0)
        self.play(Create(sq), run_time=0.3)
        until(self, "hypotenuse", lead=0.1)
        self.play(a1_thick(hy), FadeIn(l_hy), run_time=0.4)
        until(self, "Now pick another corner", lead=0.1)
        self.play(FadeIn(mark), run_time=0.5)
        until(self, "opposite", lead=0.1)
        self.play(a1_thick(op), FadeIn(l_op), run_time=0.4)
        until(self, "adjacent", lead=0.1)
        self.play(a1_thick(ad), FadeIn(l_ad), run_time=0.4)
        done(self)


# ═════════════════════════════ B03 · the ratio belongs to the angle ═════════════════════════════
class B03_SameRatio(Scene):
    def construct(self):
        ax, ay = -5.7, -1.9
        ang = ValueTracker(30.0)
        scl = ValueTracker(1.0)
        H0 = 4.0

        def pts():
            return a1_tri(ax, ay, H0 * scl.get_value(), ang.get_value())

        def live_tri():
            A, C, B = pts()
            hy, op, ad = a1_sides(A, C, B, color=INK, w=7)
            return VGroup(hy, op, ad)

        tri = always_redraw(live_tri)
        corner = always_redraw(lambda: Dot(pts()[2], radius=0.16, color=TERRA).set_stroke(DIM, width=3))
        arc = always_redraw(lambda: a1_arc_mark(pts()[0], 0.85, ang.get_value()))
        deg = always_redraw(lambda: T("%d°" % round(ang.get_value()), 40).move_to([ax + 0.75, ay - 0.5, 0]))
        head = T("opposite  ÷  hypotenuse", 36).move_to([3.2, 1.6, 0])
        num = always_redraw(lambda: T("%.2f" % np.sin(np.radians(ang.get_value())), 110).move_to([3.2, 0.1, 0]))
        sub = T("the ratio", 32, DIM).move_to([3.2, -1.1, 0])
        self.add(tri, arc, deg, corner)
        self.play(FadeIn(head), FadeIn(num), FadeIn(sub), run_time=0.5)
        until(self, "Fix the angle", lead=0.1)
        ghosts = VGroup()
        for s in (0.55, 1.3):
            old = a1_tri(ax, ay, H0 * scl.get_value(), 30.0)
            g = Polygon(old[0], old[1], old[2], stroke_color=DIM, stroke_width=3, stroke_opacity=0.85)
            ghosts.add(g)
            self.add(g)
            self.play(scl.animate.set_value(s), run_time=1.1)
            self.wait(0.3)
        until(self, "At thirty degrees", lead=0.0)
        self.wait(0.2)
        until(self, "At fifty", lead=0.15)
        o30 = a1_tri(ax, ay, H0 * scl.get_value(), 30.0)
        self.add(Polygon(o30[0], o30[1], o30[2], stroke_color=DIM, stroke_width=3, stroke_opacity=0.85))
        self.play(ang.animate.set_value(50.0), run_time=1.6)
        done(self)


# ═════════════════════════════ B04 · three ratios, three names ═════════════════════════════
class B04_SohCahToa(Scene):
    def construct(self):
        A, C, B = a1_tri(-6.1, -1.4, 3.9, 30)
        hy, op, ad = a1_sides(A, C, B)
        sq = a1_square_mark(C, 0.24)
        mark = a1_arc_mark(A, 0.7)
        l_hy = T("hypotenuse", 32).move_to([-4.85, 0.2, 0])
        l_op = T("opposite", 32).move_to([C[0] + 0.1, (C[1] + B[1]) / 2 - 1.15, 0]).shift([0.0, 0, 0])
        l_ad = T("adjacent", 32).move_to([(A[0] + C[0]) / 2, C[1] - 0.5, 0])
        l_op.move_to([C[0] + 0.95, (C[1] + B[1]) / 2, 0])
        rows = []
        specs = (("sine  ·  opposite  ÷  hypotenuse", 2.0), ("cosine  ·  adjacent  ÷  hypotenuse", 0.7), ("tangent  ·  opposite  ÷  adjacent", -0.6))
        for s, y in specs:
            t = T(s, 34)
            r = box(2.55, y, 6.6, 1.0, color=INK, sw=4)
            t.move_to(r.get_center())
            rows.append(VGroup(r, t))
        self.add(ad, op, hy, sq, mark, l_hy, l_op, l_ad)
        ghost_rows = [box(2.55, y, 6.6, 1.0, color=GHOST, sw=3) for _, y in specs]
        self.play(*[Create(g) for g in ghost_rows], run_time=0.6)

        def light(sides):
            return [a1_thick(s, s in sides) for s in (hy, op, ad)]

        until(self, "sine", lead=0.2)
        self.play(FadeIn(rows[0]), *light([op, hy]), run_time=0.5)
        until(self, "Adjacent over hypotenuse", lead=0.2)
        self.play(FadeIn(rows[1]), *light([ad, hy]), run_time=0.5)
        until(self, "Opposite over adjacent", lead=0.2)
        self.play(FadeIn(rows[2]), run_time=0.5)
        until(self, "The memory trick", lead=0.5)
        self.play(*light([op, ad]), run_time=0.4)
        until(self, "S O H", lead=0.1)
        word = VGroup(T("SOH", 48, INK, True), T("CAH", 48, INK, True), T("TOA", 48, INK, True))
        for w, x in zip(word, (-0.1, 2.55, 5.2)):
            w.move_to([x, -2.35, 0])
        self.play(FadeIn(word, shift=UP * 0.2), run_time=0.5)
        done(self)


# ═════════════════════════════ B05 · sine and cosine are lookups ═════════════════════════════
def a1_token(txt, x, y, w=1.3):
    p = RoundedRectangle(width=w, height=0.72, corner_radius=0.36, fill_color=PALEBOX, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])
    t = T(txt, 36).move_to([x, y, 0])
    return VGroup(p, t)


class B05_Lookup(Scene):
    def construct(self):
        ys = (1.15, -1.0)
        names = ("sine", "cosine")
        outs = ("0.50", "0.87")
        boxes = []
        for y, n in zip(ys, names):
            b = box(0.0, y, 2.9, 1.3, color=INK, sw=5)
            t = T(n, 44).move_to(b.get_center())
            boxes.append(VGroup(b, t))
        a_in = [arrow([-4.2, y, 0], [-1.6, y, 0], color=DIM) for y in ys]
        a_out = [arrow([1.6, y, 0], [3.0, y, 0], color=DIM) for y in ys]
        cap = T("angle in, number out", 40).move_to([0.0, -2.7, 0])
        self.play(*[Create(b) for b in boxes], *[Create(a) for a in a_in], *[Create(a) for a in a_out], run_time=0.8)
        for i in range(2):
            y = ys[i]
            until(self, ("Sine of thirty", "Cosine of thirty")[i], lead=0.1)
            tok = a1_token("30°", -5.0, y, 1.4)
            self.play(FadeIn(tok), run_time=0.25)
            self.play(tok.animate.move_to([-1.55, y, 0]).scale(0.5).set_opacity(0.0), run_time=0.7, rate_func=linear)
            self.remove(tok)
            res = a1_token(outs[i], 1.75, y, 1.5)
            self.play(FadeIn(res), run_time=0.2)
            self.play(res.animate.move_to([4.6, y, 0]), run_time=0.6)
        until(self, "An angle goes in", lead=0.1)
        self.play(FadeIn(cap), run_time=0.4)
        done(self)
