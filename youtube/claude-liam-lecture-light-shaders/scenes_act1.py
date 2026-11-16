"""ACT I · Lights in 2D (Manim beats B02, B07, B08). Cast: the warm lamp (gold disc with grey rim), the floor as outlined tiles, the teal-free swatches.
Drawings only; the measured numbers in B07 are the film's FACTCHECK figures (0.5 x (0.2 + 0.4 + 0.4) = 0.5; 0 to 3 lamps: 0.1, 0.3, 0.5, 0.7)."""


def a1_lamp(x, y, r=0.34):
    """The lamp: a pale bulb disc with a grey rim (the series' lamp marker)."""
    return Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=GOLD, stroke_width=8).move_to([x, y, 0])


def a1_strip(cx, y, n=6, tw=0.8):
    """A short strip of outlined floor tiles; returns VGroup with .tops (top-centre of each tile)."""
    tiles = VGroup(*[Square(side_length=tw * 0.94, stroke_color=DIM, stroke_width=3).move_to([cx + (i - (n - 1) / 2) * tw, y, 0]) for i in range(n)])
    tiles.tops = [np.array([cx + (i - (n - 1) / 2) * tw, y + tw * 0.47, 0]) for i in range(n)]
    return tiles


class B02_TwoLights(Scene):
    def construct(self):
        LX, RX, SY = -3.4, 3.4, -1.3
        lt = T("point light", 40).move_to([LX, 3.0, 0]); rt = T("directional light", 40).move_to([RX, 3.0, 0])
        ls = a1_strip(LX, SY); rs = a1_strip(RX, SY)
        lamp = a1_lamp(LX, 1.4)
        sun = a1_lamp(RX - 1.9, 2.1, 0.5); sun.set_stroke(GOLD, width=8)
        cl = T("like a lamp", 32, DIM).move_to([LX, -2.55, 0]); cr = T("like the sun", 32, DIM).move_to([RX, -2.55, 0])
        self.wait(0.3)
        self.play(FadeIn(ls), FadeIn(rs), FadeIn(lt), FadeIn(rt), FadeIn(lamp), FadeIn(sun), run_time=0.8)
        until(self, "A point light")
        self.play(FadeIn(cl), run_time=0.4)
        fan = VGroup(*[Line(lamp.get_center() + np.array([0, -0.34, 0]), p, color=GOLD, stroke_width=5) for p in ls.tops])
        self.play(LaggedStart(*[Create(l) for l in fan], lag_ratio=0.12), run_time=1.5)
        until(self, "A directional light")
        par = VGroup(*[Line(p + np.array([-1.3, 2.2, 0]), p, color=GOLD, stroke_width=5) for p in rs.tops])
        self.play(FadeIn(cr), run_time=0.4)
        self.play(LaggedStart(*[Create(l) for l in par], lag_ratio=0.12), run_time=1.5)
        until(self, "This film works")
        self.play(FadeIn(ring(lamp, pad=0.1)), run_time=0.6)
        done(self)


def a1_sw(v, x, y, label, num, s=1.0):
    """A swatch box (outline, filled with the grey of its number; no text inside) with its word and number under it."""
    g = 114 + int(round(141 * v))
    col = "#%02x%02x%02x" % (g, g, g)
    b = Square(side_length=s, stroke_color=DIM, stroke_width=4).set_fill(col, opacity=1).move_to([x, y, 0])
    w = T(label, 32).move_to([x, y - s / 2 - 0.35, 0]); n = T(num, 32).move_to([x, y - s / 2 - 0.8, 0])
    return b, VGroup(w, n)


class B07_Formula(Scene):
    def construct(self):
        Y = 0.7
        surf, surf_l = a1_sw(0.5, -5.6, Y, "surface", "0.5")
        amb, amb_l = a1_sw(0.2, -2.9, Y, "ambient", "0.2")
        l1, l1_l = a1_sw(0.4, -0.7, Y, "lamp", "0.4")
        l2, l2_l = a1_sw(0.4, 1.5, Y, "lamp", "0.4")
        pix_box = Square(side_length=1.0, stroke_color=DIM, stroke_width=4).move_to([4.9, Y, 0])
        pix_l = VGroup(T("pixel", 32).move_to([4.9, Y - 0.85, 0]), T("0.5", 32).move_to([4.9, Y - 1.3, 0]))
        ops = VGroup(T("x", 40).move_to([-4.55, Y, 0]), T("(", 64).move_to([-3.95, Y, 0]), T("+", 48).move_to([-1.8, Y, 0]),
                     T("+", 48).move_to([0.4, Y, 0]), T(")", 64).move_to([2.45, Y, 0]), T("=", 48).move_to([3.4, Y, 0]))
        self.wait(0.3)
        until(self, "The pixel is the surface")
        self.play(FadeIn(surf), FadeIn(surf_l), FadeIn(ops[0]), FadeIn(ops[1]), FadeIn(ops[4]), FadeIn(ops[5]), FadeIn(pix_box), FadeIn(pix_l[0]), run_time=0.7)
        until(self, "the ambient")
        self.play(FadeIn(amb), FadeIn(amb_l), run_time=0.5)
        until(self, "two lamps of")
        self.add(ops[2])
        l1.shift(UP * 1.2); l1_l.shift(UP * 1.2)
        self.add(l1, l1_l)
        self.play(l1.animate.shift(DOWN * 1.2), l1_l.animate.shift(DOWN * 1.2), run_time=0.6)
        self.play(FadeIn(ops[3]), run_time=0.2)
        l2.shift(UP * 1.2); l2_l.shift(UP * 1.2)
        self.add(l2, l2_l)
        self.play(l2.animate.shift(DOWN * 1.2), l2_l.animate.shift(DOWN * 1.2), run_time=0.6)
        until(self, "the pixel reads", lead=0.9)
        fillr = Rectangle(width=0.94, height=0.02, fill_color="#%02x%02x%02x" % (114 + 70, 114 + 70, 114 + 70), fill_opacity=1, stroke_width=0).move_to([4.9, Y - 0.47 + 0.01, 0])
        self.add(fillr)
        self.play(fillr.animate.stretch_to_fit_height(0.94).move_to([4.9, Y, 0]), run_time=0.7)
        self.play(FadeIn(pix_l[1]), run_time=0.3)
        c1 = T("measured · Godot 4.7.2 · Forward+", 32, DIM).move_to([0, -2.25, 0])
        c2 = T("0, 1, 2, 3 lamps: 0.1, 0.3, 0.5, 0.7", 32, DIM).move_to([0, -2.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        done(self)


class B08_PerLamp(Scene):
    def construct(self):
        names = ["vertex()  corners", "fragment()  pixels", "light()  lamps"]
        hb = [box(x, 2.55, 3.8, 0.85, DIM, 4, fill=PALEBOX) for x in (-4.2, 0.0, 4.2)]
        ht = [T(n, 32).move_to(b.get_center()) for n, b in zip(names, hb)]
        floor = VGroup(*[Square(side_length=0.94, stroke_color=DIM, stroke_width=3).move_to([(i - 2) * 1.0, -1.3, 0]) for i in range(5) if i != 2])
        cell = Square(side_length=1.0, stroke_color=INK, stroke_width=6).move_to([0, -1.3, 0])
        celllab = T("pixel", 32).move_to([0, -2.1, 0])
        lampL = a1_lamp(-4.9, 0.4); lampR = a1_lamp(4.9, 0.4)
        cap = T("light(): once per pixel, for each light that touches it", 32).move_to([0, -3.0, 0])
        self.wait(0.3)
        until(self, "A two-D shader")
        self.play(*[Create(b) for b in hb], *[FadeIn(t) for t in ht], run_time=0.9)
        self.play(FadeIn(floor), FadeIn(cell), FadeIn(celllab), FadeIn(lampL), FadeIn(lampR), run_time=0.7)
        until(self, "The third")
        rg = VGroup(Rectangle(width=3.8, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).next_to(hb[2], DOWN, buff=0.1), Rectangle(width=3.8, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).next_to(hb[2], DOWN, buff=0.14))  # terracotta underline bar over a grey backing (a bar, never text)
        self.play(FadeIn(rg), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.5)
        until(self, "and every light")
        aL = arrow(lampL.get_center() + np.array([0.4, -0.1, 0]), np.array([-0.55, -0.85, 0]), INK, 6)
        aR = arrow(lampR.get_center() + np.array([-0.4, -0.1, 0]), np.array([0.55, -0.85, 0]), INK, 6)
        bL = box(-2.55, -0.15, 1.5, 0.62, INK, 3, fill=PALEBOX); bR = box(2.55, -0.15, 1.5, 0.62, INK, 3, fill=PALEBOX)
        tL = T("light()", 32).move_to(bL); tR = T("light()", 32).move_to(bR)
        self.play(Create(aL), Create(aR), run_time=0.8)
        self.play(FadeIn(bL), FadeIn(tL), FadeIn(bR), FadeIn(tR), run_time=0.4)
        until(self, "how much does", lead=0.5)
        sw1 = Square(side_length=0.36, stroke_color=DIM, stroke_width=2).set_fill(_rgb(0.45), opacity=1).move_to(bL.get_center() + DOWN * 0.7)
        self.play(FadeIn(sw1), run_time=0.15)
        self.play(sw1.animate.move_to([-0.2, -1.3, 0]), run_time=0.5)
        sw2 = Square(side_length=0.36, stroke_color=DIM, stroke_width=2).set_fill(_rgb(0.45), opacity=1).move_to(bR.get_center() + DOWN * 0.7)
        self.play(FadeIn(sw2), run_time=0.15)
        self.play(sw2.animate.move_to([0.2, -1.3, 0]), run_time=0.5)
        self.play(sw1.animate.set_fill(_rgb(1.0)), sw2.animate.set_fill(_rgb(1.0)), run_time=0.4)
        done(self)
