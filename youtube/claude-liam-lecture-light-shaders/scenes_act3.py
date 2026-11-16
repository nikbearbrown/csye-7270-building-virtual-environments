"""ACT III · Which Way Is the Light?  (B19, B23: Manim)

Cast: the lamp is a gold dot with a grey ring; pixel dots are teal; a unit arrow is an ink arrow of one fixed length (a3_unit);
terracotta only as rings and small dots. Screen orientation throughout (y up here is the picture's up).
"""


def a3_lamp(x, y, r=0.24):
    d = Dot([x, y, 0], radius=r, color=GOLD)
    d.set_stroke(DIM, width=3)
    return d


def a3_pix(x, y, r=0.13):
    return Dot([x, y, 0], radius=r, color=TEAL)


def a3_unit(p, toward, length=0.8, gap=0.2):
    """A unit arrow of fixed drawn length starting just off the pixel dot p and pointing toward the point `toward`."""
    p = np.array(p, dtype=float); q = np.array(toward, dtype=float)
    u = (q - p) / np.linalg.norm(q - p)
    return arrow(p + u * gap, p + u * (gap + length), w=6, tip=0.2)


class B19_Arrows(Scene):
    def construct(self):
        title = T("Which Way Is the Light?", 40)
        title.move_to([-6.1 + title.width / 2, 3.0, 0])
        cx, cy, R = -1.5, -0.25, 1.55
        grid = pixel_grid(cols=12, rows=7, cell=0.55, x=cx, y=cy, color=GHOST, sw=2)
        lamp = a3_lamp(cx, cy)
        angs = [0, 45, 90, 135, 180, 225, 270, 315]
        pts = [np.array([cx + R * np.cos(np.radians(a)), cy + R * np.sin(np.radians(a)), 0]) for a in angs]
        dots = [a3_pix(*p[:2]) for p in pts]
        self.play(FadeIn(title), FadeIn(grid), FadeIn(lamp), FadeIn(VGroup(*dots)), run_time=0.9)
        until(self, "Light direction is a vector")
        lab = M("LIGHT_DIRECTION", 32).move_to([4.35, 1.2, 0])
        ln = T("length 1", 32).move_to([4.35, 0.55, 0])
        cap = T("vector: a bundle of two to four numbers", 32).move_to([0.0, -2.95, 0])
        self.play(FadeIn(lab), FadeIn(ln), FadeIn(cap), run_time=0.6)
        until(self, "an arrow from this pixel")
        arrs = [a3_unit(p, [cx, cy, 0]) for p in pts]
        self.play(LaggedStart(*[GrowArrow(a) for a in arrs], lag_ratio=0.12), run_time=1.6)
        until(self, "A pixel left")
        rl = ring(VGroup(dots[4], arrs[4]))
        tag = T("points right", 32).move_to([4.35, -0.2, 0])
        self.play(FadeIn(rl), FadeIn(tag), run_time=0.5)
        until(self, "A pixel above")
        rt = ring(VGroup(dots[2], arrs[2]))
        tag2 = T("points down", 32).move_to([4.35, -0.2, 0])
        self.play(FadeOut(rl), FadeIn(rt), FadeOut(tag), FadeIn(tag2), run_time=0.6)
        done(self)


class B23_Sun(Scene):
    def construct(self):
        xs = [-2.2, -1.1, 0.0, 1.1, 2.2]
        div = Line([0, 2.3, 0], [0, -2.4, 0], color=GHOST, stroke_width=4)
        lx, sx = -3.3, 3.3
        lamp = a3_lamp(lx, 1.5)
        lp = [np.array([lx + dx, -0.4, 0]) for dx in xs]
        ld = [a3_pix(*p[:2]) for p in lp]
        la = [a3_unit(p, [lx, 1.5, 0]) for p in lp]
        cap1 = VGroup(T("point light:", 32), T("a different arrow per pixel", 32)).arrange(DOWN, buff=0.1).move_to([lx, -1.45, 0])
        self.play(Create(div), FadeIn(lamp), FadeIn(VGroup(*ld)), run_time=0.7)
        self.play(LaggedStart(*[GrowArrow(a) for a in la], lag_ratio=0.2), FadeIn(cap1), run_time=1.0)
        # the sun: a disc with short rays
        sun = Circle(radius=0.42, fill_color=GOLD, fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([sx, 1.6, 0])
        rays = VGroup(*[Line([sx + 0.6 * np.cos(np.radians(a)), 1.6 + 0.6 * np.sin(np.radians(a)), 0], [sx + 0.85 * np.cos(np.radians(a)), 1.6 + 0.85 * np.sin(np.radians(a)), 0], color=GOLD, stroke_width=5) for a in range(0, 360, 45)])
        rp = [np.array([sx + dx, -0.4, 0]) for dx in xs]
        rd = [a3_pix(*p[:2]) for p in rp]
        ra = [arrow(p + np.array([0, 0.2, 0]), p + np.array([0, 1.0, 0]), w=6, tip=0.2) for p in rp]
        until(self, "A directional light is different")
        self.play(FadeIn(VGroup(sun, rays)), FadeIn(VGroup(*rd)), run_time=0.6)
        until(self, "Its arrow is the same")
        self.play(LaggedStart(*[GrowArrow(a) for a in ra], lag_ratio=0.25), run_time=1.5)
        cap2 = VGroup(T("directional light:", 32), T("the same arrow everywhere", 32)).arrange(DOWN, buff=0.1).move_to([sx, -1.45, 0])
        self.play(FadeIn(cap2), run_time=0.5)
        until(self, "and its position")
        note = T("its position is always (0, 0, 0) · Godot docs", 32, DIM).move_to([0, -2.95, 0])
        self.play(FadeIn(note), run_time=0.6)
        until(self, "So a direction mask")
        al = T("all or nothing", 32).move_to([sx, 2.75, 0])
        self.play(FadeIn(al), run_time=0.6)
        done(self)
