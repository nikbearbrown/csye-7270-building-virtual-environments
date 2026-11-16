def a2_poly(g, n):
    return [g.pt(i / (n - 1)) for i in range(n)]


def a2_tdot(p, r=0.15):
    return Dot(p, radius=r, color=TERRA).set_stroke(DIM, width=3)


class B13_OnlyWhatExists(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        g = plot(lambda v: 0.5 + 0.45 * np.sin(2.2 * np.pi * v), size=(9.0, 3.4), x=0.0, y=0.4, color=DIM)
        self.add(g.axes)
        self.wait(0.3)
        self.play(Create(g.curve), run_time=1.2)
        pts = a2_poly(g, 2)
        chord = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts)
        dots = VGroup(*[a2_tdot(p) for p in pts])
        lab = T("2 vertices", 40).move_to([0, -1.9, 0])
        self.play(Create(chord), FadeIn(dots), FadeIn(lab), run_time=0.8)
        until(self, "Between two corners")
        for n, nm in ((3, "3 vertices"), (5, "5 vertices")):
            pts = a2_poly(g, n)
            new_chord = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts)
            new_dots = VGroup(*[a2_tdot(p) for p in pts])
            new_lab = T(nm, 40).move_to([0, -1.9, 0])
            self.play(Transform(chord, new_chord), ReplacementTransform(dots, new_dots), ReplacementTransform(lab, new_lab), run_time=0.7)
            dots, lab = new_dots, new_lab
            self.wait(0.35)
        until(self, "A curve needs corners")
        pts = a2_poly(g, 9)
        new_chord = VMobject(stroke_color=INK, stroke_width=6).set_points_as_corners(pts)
        new_dots = VGroup(*[a2_tdot(p) for p in pts])
        new_lab = T("9 vertices", 40).move_to([0, -1.9, 0])
        self.play(Transform(chord, new_chord), ReplacementTransform(dots, new_dots), ReplacementTransform(lab, new_lab), run_time=1.0)
        until(self, "for vertex to push up")
        cap = T("vertex moves only the vertices that exist", 36).move_to([0, -2.8, 0])
        self.play(FadeIn(cap), run_time=0.5)
        done(self)


class B14_TwoWays(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        lx, rx, py = -3.3, 3.3, 0.8
        pl = box(lx, py, 5.8, 3.1, color=DIM, sw=4)
        pr = box(rx, py, 5.8, 3.1, color=DIM, sw=4)
        nl = M("Polygon2D", 32).move_to([lx, 2.9, 0])
        nr = M("MeshInstance2D", 32).move_to([rx, 2.9, 0])
        self.add(pl, pr)
        self.play(FadeIn(nl), FadeIn(nr), run_time=0.5)
        sl = T("you place the points", 32).move_to([lx, -1.1, 0])
        sr = T("a mesh cut into a grid", 32).move_to([rx, -1.1, 0])
        self.play(FadeIn(sl), FadeIn(sr), run_time=0.4)
        until(self, "A polygon node")
        # polygon points placed one at a time
        P = [(-4.9, 0.2), (-4.3, 1.7), (-3.2, 2.0), (-2.2, 1.3), (-2.3, 0.2), (-3.5, -0.1)]
        P = [np.array([x, y, 0.0]) for x, y in P]
        placed = []
        lines = []
        for i, p in enumerate(P):
            d = a2_tdot(p, 0.14)
            anims = [FadeIn(d, scale=1.6)]
            if i:
                ln = Line(P[i - 1], p, color=INK, stroke_width=5)
                lines.append(ln); anims.append(Create(ln))
            self.play(*anims, run_time=0.32)
            placed.append(d)
        closer = Line(P[-1], P[0], color=INK, stroke_width=5)
        self.play(Create(closer), run_time=0.4)
        until(self, "Or a mesh node")
        W, H = 4.4, 2.4
        cx, cy = rx, py
        rect = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=5).move_to([cx, cy, 0])
        self.play(Create(rect), run_time=0.5)
        vl = [Line([cx - W / 2 + W * k / 6, cy - H / 2, 0], [cx - W / 2 + W * k / 6, cy + H / 2, 0], color=DIM, stroke_width=3) for k in range(1, 6)]
        hl = [Line([cx - W / 2, cy - H / 2 + H * k / 4, 0], [cx + W / 2, cy - H / 2 + H * k / 4, 0], color=DIM, stroke_width=3) for k in range(1, 4)]
        self.play(LaggedStart(*[Create(l) for l in vl + hl], lag_ratio=0.15), run_time=1.2)
        gd = VGroup(*[Dot([cx - W / 2 + W * i / 6, cy - H / 2 + H * j / 4, 0], radius=0.09, color=TERRA).set_stroke(DIM, width=2) for i in range(7) for j in range(5)])
        self.play(LaggedStart(*[FadeIn(d, scale=1.4) for d in gd], lag_ratio=0.03), run_time=1.0)
        until(self, "the vertices and triangles")
        cap = T("mesh: the vertices and triangles that make a shape", 36).move_to([0, -2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        done(self)


def a2_num(n, x, y, size=64):
    return T(str(n), size, bold=True).move_to([x, y, 0])


class B16_CountThem(Scene):
    def construct(self):
        self.camera.background_color = STAGE
        lx, rx, gy = -3.6, 3.45, 0.3
        l1 = T("cut 3 by 3", 40).move_to([lx, 2.3, 0])
        self.add(l1)
        until(self, "Cut a quad mesh")
        cnt = a2_num(0, lx, -1.3)
        self.add(cnt)
        gap = 0.55
        total = 0
        for r in range(5):
            row = VGroup(*[Dot([lx + (c - 2) * gap, gy + (2 - r) * gap + 0.0, 0], radius=0.1, color=TERRA).set_stroke(DIM, width=2) for c in range(5)])
            total += 5
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in row], lag_ratio=0.12), run_time=0.55)
            self.remove(cnt); cnt = a2_num(total, lx, -1.3); self.add(cnt)
        until(self, "Always two more")
        f = T("(cuts + 2) x (cuts + 2)", 40).move_to([0, -2.4, 0])
        self.play(FadeIn(f), run_time=0.5)
        l2 = T("cut 31 by 7", 40).move_to([rx, 2.3, 0])
        fr = Rectangle(width=5.5, height=1.45, stroke_color=GHOST, stroke_width=3).move_to([rx, gy, 0])
        self.play(FadeIn(l2), Create(fr), run_time=0.5)
        until(self, "The flag's thirty-one")
        cnt2 = a2_num(0, rx, -1.3)
        self.add(cnt2)
        g2 = 0.165
        total = 0
        for r in range(9):
            row = VGroup(*[Dot([rx + (c - 16) * g2, gy + (4 - r) * g2, 0], radius=0.045, color=TERRA) for c in range(33)])
            total += 33
            self.play(LaggedStart(*[FadeIn(d) for d in row], lag_ratio=0.02), run_time=0.3)
            self.remove(cnt2); cnt2 = a2_num(total, rx, -1.3); self.add(cnt2)
        cr = T("counted from the mesh in Godot 4.7.2", 32, color=DIM).move_to([0, -3.1, 0])
        self.play(FadeIn(cr), run_time=0.4)
        done(self)
