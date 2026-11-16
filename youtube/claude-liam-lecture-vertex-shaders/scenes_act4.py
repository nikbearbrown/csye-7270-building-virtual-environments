def a4_tdot(p, r=0.15):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


class B27_FragmentCannotSee(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        ttl = T("Passing Data Forward", 40)
        ttl.move_to([-6.2 + ttl.width / 2, 3.05, 0])
        self.add(ttl)
        y = 0.7
        xs = (-4.4, 0.0, 4.4)
        q = vertex_quad(w=2.1, h=1.4, x=xs[0], y=y)
        l1 = M("vertex()", 32).move_to([xs[0], y + 1.35, 0])
        card = Rectangle(width=2.1, height=1.4, stroke_color=DIM, stroke_width=4).move_to([xs[1], y, 0])
        tiles = VGroup(*[Rectangle(width=0.2, height=1.2, fill_color=_rgb(i / 7), fill_opacity=1, stroke_width=0).move_to([xs[1] - 0.9 + i * 0.257, y, 0]) for i in range(8)])
        l2 = T("card fills shape", 32).move_to([xs[1], y + 1.35, 0])
        pg = pixel_grid(cols=6, rows=4, cell=0.38, x=xs[2], y=y)
        l3 = M("fragment()", 32).move_to([xs[2], y + 1.35, 0])
        a1 = arrow([xs[0] + 1.35, y, 0], [xs[1] - 1.35, y, 0])
        a2 = arrow([xs[1] + 1.35, y, 0], [xs[2] - 1.35, y, 0])
        self.wait(0.3)
        self.play(FadeIn(q), FadeIn(l1), run_time=0.6)
        self.play(Create(a1), FadeIn(card), FadeIn(l2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.1), run_time=0.7)
        self.play(Create(a2), FadeIn(pg), FadeIn(l3), run_time=0.6)
        until(self, "the function that colors")
        cap = T("fragment(): runs once for each pixel the shape covers;", 32).move_to([0, -1.55, 0])
        cap2 = T("sets its color", 32).move_to([0, -2.1, 0])
        self.play(FadeIn(cap), FadeIn(cap2), run_time=0.5)
        until(self, "But fragment runs later")
        glass = VGroup(RoundedRectangle(width=0.3, height=2.6, corner_radius=0.08, stroke_color=TEAL, stroke_width=6).move_to([-2.65, y, 0]),
                       Line([-2.7, y - 0.6, 0], [-2.6, y - 0.2, 0], color=TEAL, stroke_width=3), Line([-2.7, y + 0.2, 0], [-2.6, y + 0.6, 0], color=TEAL, stroke_width=3))
        self.play(Create(glass), run_time=0.6)
        qm = T("?", 64, bold=True).move_to([xs[2] - 0.0, y - 1.15, 0])
        trail = Dot(qm.get_center() + [0, -0.5, 0], radius=0.1, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(qm), FadeIn(trail), run_time=0.3)
        self.play(qm.animate.move_to([-2.2, y - 1.15, 0]), trail.animate.move_to([-2.2, y - 1.65, 0]), run_time=1.7, rate_func=linear)
        self.play(qm.animate.shift([0.12, 0, 0]), run_time=0.12)
        self.play(qm.animate.shift([-0.12, 0, 0]), run_time=0.12)
        done(self)


class B28_Varying(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        cx, cy = 0.0, 1.35
        q = vertex_quad(w=5.0, h=2.4, x=cx, y=cy)
        self.wait(0.3)
        self.play(FadeIn(q), run_time=0.6)
        nums = VGroup(*[T(s, 44, bold=True).move_to(p + np.array([dx, 0, 0])) for s, p, dx in
                        (("0", q.pts[0], -0.5), ("1", q.pts[1], 0.5), ("1", q.pts[2], 0.5), ("0", q.pts[3], -0.5))])
        self.play(FadeIn(nums), run_time=0.5)
        until(self, "In vertex")
        ay = -1.05
        ls = T("set in vertex()", 36).move_to([-4.5, ay, 0])
        lr = T("read in fragment()", 36).move_to([4.2, ay, 0])
        ar = arrow([-2.8, ay, 0], [2.0, ay, 0])
        self.play(FadeIn(ls), run_time=0.4)
        self.play(Create(ar), run_time=0.5)
        self.play(FadeIn(lr), run_time=0.4)
        until(self, "The graphics card interpolates")
        n = 36
        w = 4.6
        cols = VGroup(*[Rectangle(width=w / n * 0.8, height=2.0, fill_color=_rgb(i / (n - 1)), fill_opacity=1, stroke_width=0).move_to([cx - w / 2 + w / n * (i + 0.5), cy, 0]) for i in range(n)])
        self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.05), run_time=1.6)
        until(self, "it flows one way", lead=0.5)
        fw = T("forward", 36).move_to([-0.5, ay + 0.5, 0])
        d = Dot([-2.8, ay, 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(fw), FadeIn(d), run_time=0.3)
        self.play(d.animate.move_to([2.0, ay, 0]), run_time=0.7, rate_func=linear)
        c1 = T("varying: a value set at each corner, blended across", 32).move_to([0, -2.2, 0])
        c2 = T("the shape for fragment() to read", 32).move_to([0, -2.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        done(self)


def a4_checker(x, y, size, c1, c2, n=4):
    s = size / n
    g = VGroup()
    for i in range(n):
        for j in range(n):
            g.add(Square(side_length=s * 0.94, stroke_width=0, fill_color=c1 if (i + j) % 2 == 0 else c2, fill_opacity=1).move_to([x - size / 2 + s * (i + 0.5), y + size / 2 - s * (j + 0.5), 0]))
    return g


class B31_BuiltInVaryings(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        rs = ramp_strip(width=6.0, y=2.3, label0="0", label1="1", n=40, height=0.4)
        for t in rs.tiles:
            t.set_fill(opacity=0)
        self.add(rs.labels)
        d0 = a4_tdot(np.array([rs.x0 - 0.22, rs.y, 0.0]))
        d1 = a4_tdot(np.array([rs.x1 + 0.22, rs.y, 0.0]))
        self.wait(0.3)
        self.play(FadeIn(d0), FadeIn(d1), run_time=0.5)
        until(self, "U V is set")
        lab = T("U V: set at the corners, blended", 36).move_to([0, 1.2, 0])
        self.play(FadeIn(lab), run_time=0.4)
        self.play(LaggedStart(*[t.animate.set_fill(opacity=1) for t in rs.tiles], lag_ratio=0.05), run_time=1.6)
        by = -0.3
        until(self, "The color from vertex")
        block = Square(side_length=1.2, fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to([-2.4, by, 0])
        chk = a4_checker(-0.4, by, 1.4, "#F2F0E9", "#D9D4C7")
        self.play(FadeIn(block), run_time=0.4)
        self.play(FadeIn(chk), run_time=0.4)
        until(self, "and multiplied", lead=0.8)
        xs = VGroup(Line([-1.65, by + 0.18, 0], [-1.3, by - 0.18, 0], color=INK, stroke_width=6), Line([-1.65, by - 0.18, 0], [-1.3, by + 0.18, 0], color=INK, stroke_width=6)).shift([0.0, 0, 0])
        xs.move_to([-1.4, by, 0])
        eq = VGroup(Line([0.5, by + 0.1, 0], [0.9, by + 0.1, 0], color=INK, stroke_width=6), Line([0.5, by - 0.1, 0], [0.9, by - 0.1, 0], color=INK, stroke_width=6))
        res = a4_checker(2.0, by, 1.4, TEAL, "#8DBDAE")
        self.play(Create(xs), run_time=0.4)
        self.play(Create(eq), run_time=0.4)
        self.play(FadeIn(res), run_time=0.6)
        l1 = T("color from vertex x the picture", 32).move_to([-1.5, -1.45, 0])
        l2 = T("= color in fragment", 32).move_to([2.9, -1.45, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.4)
        cap = T("COLOR: the color being drawn", 36).move_to([0, -2.6, 0])
        self.play(FadeIn(cap), run_time=0.4)
        done(self)
