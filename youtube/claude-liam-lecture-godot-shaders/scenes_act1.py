"""ACT I · One Pixel, All at Once (Manim beats B02, B03, B05, B07, B08).

Cast for the act: the teal test sprite (sprite_icon), the pixel grid of OUTLINE cells, the 0 to 1 ramp colours (ghost to teal).
Every number on screen is from the lane / FACTCHECK: 55 ms (52 to 58 over five runs), 16.7 ms frame, about 0.04 ms CPU hand-over, M4 Pro, Godot 4.7.2.
"""


def a1_pair(y=0.25, w=4.6, h=3.4, x=3.8, lt="game code · CPU", rt="the shader · GPU", size=36):
    """Two outlined boxes (CPU left, GPU right) with their titles. Returns (L, R, ltxt, rtxt)."""
    L = box(-x, y, w, h)
    R = box(x, y, w, h)
    a = T(lt, size).move_to([-x, y + h / 2 - 0.5, 0])
    b = T(rt, size).move_to([x, y + h / 2 - 0.5, 0])
    return L, R, a, b


def a1_wobble(cx, cy, r=0.78, amp=0.07, k=9):
    """A wavy ring round a picture: the 'restyled by the shader' mark (a drawing, not a render)."""
    return ParametricFunction(
        lambda t: np.array([cx + (r + amp * np.sin(k * t)) * np.cos(t), cy + (r + amp * np.sin(k * t)) * np.sin(t), 0.0]),
        t_range=[0, TAU, 0.05], color=INK, stroke_width=5)


# ───────────────────────────────────────────────────────────────────────────
class B02_WhatAndWhere(Scene):
    def construct(self):
        L, R, lt, rt = a1_pair(y=0.25)
        ico = sprite_icon(-3.8, 0.4, 0.45)
        self.wait(0.3)
        self.play(Create(L), FadeIn(lt), FadeIn(ico), run_time=0.9)
        until(self, "the G P U")
        ar = arrow([-1.4, 0.4, 0], [1.4, 0.4, 0])
        self.play(Create(R), FadeIn(rt), GrowArrow(ar), run_time=0.9)
        until(self, "It decides")
        moved = ico.copy()
        self.add(moved)
        self.play(moved.animate.move_to([3.8, 0.4, 0]), run_time=1.5)
        wob = a1_wobble(3.8, 0.4, r=0.68)
        self.play(Create(wob), run_time=0.6)
        until(self, "Your game code")
        ls = T("what exists, where", 34).move_to([-3.8, -1.0, 0])
        self.play(FadeIn(ls), run_time=0.5)
        until(self, "The shader decides")
        rs = T("how each part looks", 34).move_to([3.8, -1.0, 0])
        self.play(FadeIn(rs), run_time=0.6)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B03_ManyWorkers(Scene):
    def construct(self):
        g1 = pixel_grid(12, 6, 0.42, x=2.8, y=1.5)
        g2 = pixel_grid(12, 6, 0.42, x=2.8, y=-1.7)
        l1a = T("CPU", 38).move_to([-3.4, 2.15, 0])
        l1b = T("one job after another", 34).move_to([-3.4, 1.55, 0])
        l2a = T("GPU", 38).move_to([-3.4, -1.05, 0])
        l2b = T("the same job at once", 34).move_to([-3.4, -1.65, 0])
        cnt = T("0 / 72", 34).move_to([-3.4, 0.85, 0])
        worker = sprite_icon(*cell_center(g1, 0, 0)[:2], r=0.17)
        self.wait(0.2)
        self.play(FadeIn(g1), FadeIn(l1a), FadeIn(l1b), FadeIn(cnt), FadeIn(worker), run_time=0.8)
        until(self, "The C P U")
        tgt = _TARGET.get("B03", 12.0)
        t_s = _elapsed(self)
        rate = max(0.05, (tgt - 0.9 - t_s) / 72.0)
        st = dict(acc=0.0, k=0, cnt=cnt)

        def tick(m, dt):
            st["acc"] += dt
            k = min(72, int(st["acc"] / rate))
            if k != st["k"]:
                for i in range(st["k"], k):
                    c = g1.cells[i // 12][i % 12]
                    c.set_fill(TEAL, opacity=0.9).set_stroke(TEAL, width=2)
                st["k"] = k
                new = T(f"{k} / 72", 34).move_to([-3.4, 0.85, 0])
                st["cnt"].become(new)
                p = cell_center(g1, min(k, 71) % 12, min(k, 71) // 12)
                m.move_to([p[0], p[1], 0])
        worker.add_updater(tick)
        until(self, "The G P U is a crowd")
        self.play(FadeIn(g2), FadeIn(l2a), FadeIn(l2b), run_time=0.5)
        crowd = VGroup(*[Dot(s.get_center(), radius=0.08, color=INK) for row in g2.cells for s in row])
        self.play(FadeIn(crowd), run_time=0.5)
        self.play(*[tint(s, TEAL, 0.9) for row in g2.cells for s in row], run_time=0.5)
        self.wait(max(0.1, tgt - 0.75 - _elapsed(self)))
        worker.clear_updaters()
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B05_FrameBudget(Scene):
    def construct(self):
        x0 = -5.5
        sc = 11.0 / 60.0
        ya = -0.5
        axis = Line([x0, ya, 0], [x0 + 11.0, ya, 0], color=INK, stroke_width=5)
        ticks = VGroup(*[Line([x0 + v * sc, ya, 0], [x0 + v * sc, ya - 0.18, 0], color=INK, stroke_width=4) for v in (0, 20, 40, 60)])
        labs = VGroup(*[T(s, 32).move_to([x0 + v * sc, ya - 0.5, 0]) for s, v in (("0", 0), ("20", 20), ("40", 40), ("60 ms", 60))])
        labs[3].shift([-0.3, 0, 0])
        self.wait(0.3)
        self.play(Create(axis), FadeIn(ticks), FadeIn(labs), run_time=0.8)
        until(self, "On this Mac")
        tiles = VGroup(*[Rectangle(width=sc * 0.8, height=0.6, fill_color=(TEAL if i + 0.5 < 16.7 else GOLD), fill_opacity=1, stroke_width=0)
                         .move_to([x0 + (i + 0.5) * sc, 0.1, 0]) for i in range(55)])
        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.12), run_time=2.6)
        bl = T("the loop · about 55 ms", 34).move_to([2.6, 1.0, 0])
        self.play(FadeIn(bl), run_time=0.4)
        until(self, "sixteen and a half")
        xb = x0 + 16.7 * sc
        line = DashedLine([xb, -0.85, 0], [xb, 1.75, 0], color=INK, stroke_width=5, dash_length=0.18)
        bt = T("one frame at 60 per second", 34).move_to([xb + 0.4, 2.25, 0])
        self.play(Create(line), FadeIn(bt), run_time=0.8)
        until(self, "This is one gradient")
        cr = T("Apple M4 Pro · Godot 4.7.2 · five runs: 52 to 58 ms", 32, DIM).move_to([0, -2.6, 0])
        self.play(FadeIn(cr), run_time=0.6)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B07_HandOver(Scene):
    def construct(self):
        L, R, lt, rt = a1_pair(y=0.25, w=3.6, h=3.0, x=4.4, size=34)
        lt.move_to([-4.4, 1.25, 0]); rt.move_to([4.4, 1.25, 0])
        speck = Dot([-4.4, 0.25, 0], radius=0.06, color=INK)
        ar = arrow([-2.5, 0.25, 0], [2.5, 0.25, 0])
        h1 = T("hands over the job", 34).move_to([0, 1.2, 0])
        h2 = T("about 0.04 ms", 34).move_to([0, 0.72, 0])
        gg = pixel_grid(8, 4, 0.32, x=4.4, y=0.2)
        self.wait(0.3)
        self.play(Create(L), Create(R), FadeIn(lt), FadeIn(rt), GrowArrow(ar), run_time=0.9)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.5)
        until(self, "cost the processor")
        self.play(FadeIn(speck), run_time=0.3)
        until(self, "only to hand over")
        pkg = RoundedRectangle(width=0.5, height=0.38, corner_radius=0.08, stroke_color=DIM, stroke_width=4, fill_color=CARD, fill_opacity=1).move_to([-4.4, 0.25, 0])
        self.add(pkg)
        self.play(pkg.animate.move_to([2.5, 0.25, 0]), run_time=1.3)
        self.play(FadeOut(pkg), FadeIn(gg), run_time=0.4)
        until(self, "The graphics card did the pixels")
        self.play(*[tint(s, _rgb(c / 7.0), 1.0) for row in gg.cells for c, s in enumerate(row)], run_time=0.8)
        until(self, "Its own time")
        note = T("its own time: not readable on this setup", 32, DIM).move_to([1.6, -1.95, 0])
        cr = T("Apple M4 Pro · Godot 4.7.2", 32, DIM).move_to([1.6, -2.7, 0])
        self.play(FadeIn(note), FadeIn(cr), run_time=0.6)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B08_OnePixelThenAll(Scene):
    def construct(self):
        g = pixel_grid(16, 9, 0.42, x=-2.6, y=0.45)
        cc, rr = 13, 3
        cell = g.cells[rr][cc]
        rg = ring(cell, pad=0.05, sw=6)
        card = code_card("COLOR = …", x=4.5, y=cell.get_center()[1], size=34)
        cw = card.W
        con = arrow([4.5 - cw / 2, cell.get_center()[1], 0], [cell.get_center()[0] + 0.33, cell.get_center()[1], 0], color=DIM, w=5)
        lab_a = T("one pixel's rule", 34)
        lab_b = T("every pixel", 34)
        ab = arrow([0, 0, 0], [0.9, 0, 0], w=5)
        row = VGroup(lab_a, ab, lab_b).arrange(RIGHT, buff=0.3).move_to([-2.6, -2.35, 0])
        self.wait(0.3)
        self.play(FadeIn(g), run_time=0.8)
        until(self, "write down what one pixel")
        self.play(Create(rg), FadeIn(card), GrowArrow(con), run_time=0.9)
        self.play(FadeIn(row), run_time=0.5)
        until(self, "let the card do it everywhere", lead=0.9)
        self.play(*[tint(g.cells[r][c], _rgb(c / 15.0), 1.0) for r in range(9) for c in range(16)], run_time=1.0)
        done(self)
