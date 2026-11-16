def a5_dial(x, y, r=0.36):
    c = Circle(radius=r, stroke_color=DIM, stroke_width=6).move_to([x, y, 0])
    p = Line([x, y, 0], [x + 0.26, y + 0.2, 0], color=INK, stroke_width=6)
    return VGroup(c, p)


def a5_cells(cx, cy, pitch=1.35, side=1.0, cols=3, rows=2):
    cells = []
    for r in range(rows):
        for c in range(cols):
            cells.append(Square(side_length=side, stroke_color=DIM, stroke_width=3).move_to([cx + (c - (cols - 1) / 2) * pitch, cy + ((rows - 1) / 2 - r) * pitch, 0]))
    return cells


class B34_SameForAll(Scene):
    def construct(self):
        title = T("Where Am I, and When?", 40).move_to([-3.4, 2.95, 0])
        pitch = 1.35
        lc = a5_cells(-3.3, -0.55, pitch); rc = a5_cells(3.3, -0.55, pitch)
        gl = VGroup(*lc); gr = VGroup(*rc)
        dial = a5_dial(-3.3, 1.95)
        dl = T("uniform", 32).move_to([-1.3, 1.95, 0])
        al = T("address (u, v)", 32).move_to([3.3, 1.95, 0])
        rail_y = 1.05
        lane = [-3.3 + (c - 1) * pitch - 0.7 for c in range(3)]
        wires = [Line([-3.3, 1.59, 0], [-3.3, rail_y, 0], color=DIM, stroke_width=4), Line([lane[0], rail_y, 0], [lane[2], rail_y, 0], color=DIM, stroke_width=4)]
        ends = []
        for c in range(3):
            ybot = lc[3 + c].get_center()[1]
            wires.append(Line([lane[c], rail_y, 0], [lane[c], ybot, 0], color=DIM, stroke_width=4))
            for r in range(2):
                cell = lc[r * 3 + c]
                y = cell.get_center()[1]
                wires.append(Line([lane[c], y, 0], [cell.get_center()[0] - 0.5, y, 0], color=DIM, stroke_width=4))
                ends.append(Dot([cell.get_center()[0] - 0.5, y, 0], radius=0.07, color=DIM))
        fan = VGroup(*wires, *ends)
        nums = VGroup(*[T("0.5", 32).move_to(cl.get_center()) for cl in lc])
        us = ["0.17", "0.50", "0.83"]; vs = ["0.25", "0.75"]
        pairs = VGroup(*[VGroup(T(us[c], 32), T(vs[r], 32)).arrange(DOWN, buff=0.06).move_to(rc[r * 3 + c].get_center()) for r in range(2) for c in range(3)])
        cap1 = T("same everywhere", 32).move_to([-3.3, -2.8, 0])
        cap2 = T("different for each", 32).move_to([3.3, -2.8, 0])
        self.play(FadeIn(title), FadeIn(gl), run_time=0.6)
        self.play(FadeIn(dial), FadeIn(dl), run_time=0.4)
        until(self, "A uniform is one value")
        self.play(LaggedStart(*[Create(w) for w in wires], lag_ratio=0.08), run_time=1.0)
        self.play(FadeIn(VGroup(*ends)), FadeIn(nums), FadeIn(cap1), run_time=0.5)
        until(self, "Some inputs must differ")
        self.play(FadeIn(gr), FadeIn(al), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.1), FadeIn(cap2), run_time=0.9)
        until(self, "The engine hands")
        for k in (0, 4, 2):
            self.play(Indicate(rc[k], color=TEAL, scale_factor=1.12), run_time=0.5)
        done(self)


class B36_Address(Scene):
    def construct(self):
        S0 = 3.4
        sq = uv_square(S0, x=-0.4, y=-0.35)
        x0, y0 = -0.4 - S0 / 2, -0.35 + S0 / 2
        un = T("u", 32).move_to([x0 + S0 + 0.45, y0 + 0.5, 0]); vn = T("v", 32).move_to([x0 - 0.5, y0 - S0 - 0.45, 0])
        c00 = T("(0, 0)", 32).move_to([x0 + 0.75, y0 - 0.4, 0])
        c11 = T("(1, 1)", 32).move_to([x0 + S0 - 0.2, y0 - S0 - 0.45, 0])
        self.play(Create(sq.frame), run_time=0.6)
        self.play(FadeIn(VGroup(*sq.submobjects[1:])), FadeIn(VGroup(un, vn, c00, c11)), run_time=0.7)
        pos = {"u": 0.5, "v": 0.15}
        dot = Dot(sq.pt(0.5, 0.15), radius=0.2, color=TERRA).set_stroke(DIM, width=4)

        def lab():
            u, v = dot.get_center()[0], dot.get_center()[1]
            uu = (u - x0) / S0; vv = (y0 - v) / S0
            t = T(f"({uu:.2f}, {vv:.2f})", 32)
            if uu > 0.6:
                t.move_to(dot.get_center() + np.array([-1.35, 0.55, 0]))
            else:
                t.move_to(dot.get_center() + np.array([1.4, 0.45, 0]))
            return t
        label = always_redraw(lab)
        until(self, "U V runs")
        self.play(FadeIn(dot, scale=0.5), run_time=0.3)
        self.add(label)
        self.play(dot.animate.move_to(sq.pt(0.25, 0.75)), run_time=1.0)
        until(self, "The bottom right")
        self.play(dot.animate.move_to(sq.pt(1.0, 1.0)), run_time=1.0)
        until(self, "the second number counts")
        self.play(dot.animate.move_to(sq.pt(1.0, 0.45)), run_time=0.7)
        self.play(dot.animate.move_to(sq.pt(1.0, 1.0)), run_time=0.9)
        done(self)


class B41_ClockVsDial(Scene):
    def construct(self):
        xa, xb, yc = -5.5, 5.5, 1.2
        n = 44; tw = (xb - xa) / n
        clock = VGroup(*[Rectangle(width=tw * 0.8, height=0.26, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([xa + tw * (i + 0.5), yc, 0]) for i in range(n)])
        cl = T("game clock", 32).move_to([-4.3, yc + 0.6, 0])
        nr = T("never restarts", 32).move_to([4.2, yc + 0.6, 0])
        c0 = T("0", 32).move_to([xa, yc - 0.55, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in clock], lag_ratio=0.02), FadeIn(cl), FadeIn(c0), run_time=1.1)
        play_x = {"x": xa}
        head = Dot([xa, yc, 0], radius=0.15, color=INK)
        speed = 3.3 / 3.7
        self.add(head)

        def adv(m, dt):
            play_x["x"] = min(xa + 9.8, play_x["x"] + speed * dt)
            m.move_to([play_x["x"], yc, 0])
        head.add_updater(adv)
        xm = xa + 3.3
        until(self, "that starts when", lead=1.3)
        mk = Dot([xm, yc, 0], radius=0.2, color=TERRA).set_stroke(DIM, width=4)
        ml = T("something happens", 32).move_to([xm + 0.3, yc + 1.55, 0])
        drop = DashedLine([xm, yc - 0.15, 0], [xm, -0.95, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(mk, scale=0.4), FadeIn(ml), Create(drop), run_time=0.5)
        yp = -1.2; pw = 3.5; m = 28; ptw = pw / m
        prog = VGroup(*[Rectangle(width=ptw * 0.8, height=0.3, fill_color=TEAL, fill_opacity=1, stroke_width=0).move_to([xm + ptw * (i + 0.5), yp, 0]) for i in range(m)])
        pl = T("progress", 32).move_to([-4.0, yp, 0])
        p0 = T("0", 32).move_to([xm, yp - 0.6, 0]); p1 = T("1", 32).move_to([xm + pw, yp - 0.6, 0])
        until(self, "something happens,", lead=0.0)
        self.play(FadeIn(pl), FadeIn(p0), FadeIn(p1), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(t) for t in prog], lag_ratio=0.05), run_time=1.1)
        until(self, "let your game drive")
        dl = T("you drive it", 32).move_to([xm + pw / 2, yp - 1.25, 0])
        self.play(FadeIn(dl), FadeIn(nr), run_time=0.5)
        done(self)
