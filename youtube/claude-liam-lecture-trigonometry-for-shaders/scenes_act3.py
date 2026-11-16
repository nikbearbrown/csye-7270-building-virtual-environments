"""ACT III · An Orbit  (B16, B17, B20, B25, Manim)

Cast for the act: the centered square p in SCREEN orientation (y counts DOWN), outline cells, a terracotta probe dot,
teal planet and slate-blue moon (same colours as the Lab renders). Drawings only.
"""

A3_PLANET = "#5EA391"; A3_MOON = "#8099BF"


# ═════════════════════════════ B16 · the centered pixel address ═════════════════════════════
class B16_CenterAddress(Scene):
    def construct(self):
        title = T("An Orbit", 40).to_corner(UL, buff=0.95)
        S = 3.2; cx, cy = -3.7, -0.35
        x0, x1, y0, y1 = cx - S / 2, cx + S / 2, cy + S / 2, cy - S / 2
        sq = Square(side_length=S, stroke_color=INK, stroke_width=5).move_to([cx, cy, 0])
        yar = arrow([x0 - 0.55, y0, 0], [x0 - 0.55, y0 - 1.1, 0], color=DIM, w=5)
        ylab = T("y", 32, DIM).move_to([x0 - 0.55, y0 - 1.5, 0])
        uv = T("UV", 40).move_to([cx, y0 + 0.5, 0])
        lab_tl = T("(0, 0)", 32).move_to([x0 + 0.05, y0 + 0.35, 0]).shift([0.0, 0, 0])
        lab_br = T("(1, 1)", 32).move_to([x1 - 0.05, y1 - 0.35, 0])
        lab_mid = T("(0.5, 0.5)", 32).move_to([cx, cy - 0.5, 0])
        dot = Dot([cx, cy, 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        self.add(title)
        self.play(Create(sq), Create(yar), FadeIn(ylab), FadeIn(uv), FadeIn(lab_tl), FadeIn(lab_br), FadeIn(lab_mid), GrowFromCenter(dot), run_time=0.8)
        card = code_card("void fragment() {\n    vec2 p = UV * 2.0 - 1.0;\n}", x=2.45, y=-0.5, size=32)
        line2 = card.lines[1]
        card.remove(line2)
        tagbox = VGroup(RoundedRectangle(width=3.0, height=0.62, corner_radius=0.12, stroke_color=INK, stroke_width=3).set_fill(PALEBOX, opacity=1), T("once per pixel", 32))
        tagbox.move_to([card.lines[0].get_left()[0] + 1.6, card.frame.get_top()[1] + 0.85, 0])
        link = Line(tagbox.get_bottom(), [tagbox.get_center()[0], card.lines[0].get_top()[1] + 0.02, 0], color=DIM, stroke_width=4)
        until(self, "It runs once", lead=0.15)
        self.play(FadeIn(card), FadeIn(tagbox), Create(link), run_time=0.6)
        until(self, "Double it", lead=0.2)
        self.play(FadeIn(line2, shift=RIGHT * 0.2), run_time=0.5)
        until(self, "the range becomes", lead=0.05)
        n_tl = T("(-1, -1)", 32).move_to(lab_tl.get_center())
        n_br = T("(1, 1)", 32).move_to(lab_br.get_center())
        n_mid = T("(0, 0)", 32).move_to(lab_mid.get_center())
        self.play(Transform(lab_tl, n_tl), Transform(lab_mid, n_mid), run_time=0.8)
        until(self, "with zero, zero", lead=0.3)
        self.play(dot.animate.move_to([x0 + 0.0, y0, 0]), run_time=0.6)
        self.play(dot.animate.move_to([cx, cy, 0]), run_time=0.6)
        ptag = always_redraw(lambda: T("p", 40).next_to(dot, UR, buff=0.12))
        self.add(ptag)
        self.play(FadeIn(ptag), run_time=0.2)
        done(self)


# ═════════════════════════════ B17 · the planet is a distance test ═════════════════════════════
class B17_Planet(Scene):
    def construct(self):
        N = 12; cell = 0.42; gx, gy = -3.6, 0.15
        half = N * cell / 2.0
        grid = pixel_grid(N, N, cell, x=gx, y=gy, color=DIM, sw=2)
        rad = 0.25 * half
        planet = Circle(radius=rad, stroke_color=TEAL, stroke_width=4, stroke_opacity=0.9).move_to([gx, gy, 0])
        v = ValueTracker(0.0)          # length(p)
        probe = always_redraw(lambda: Dot([gx + v.get_value() * half, gy, 0], radius=0.13, color=TERRA).set_stroke(DIM, width=3))
        trail = always_redraw(lambda: Line([gx, gy, 0], [gx + v.get_value() * half, gy, 0], color=DIM, stroke_width=4))

        def live_cell():
            inside = v.get_value() < 0.25
            c = Square(side_length=cell * 0.94, stroke_color=TEAL if inside else DIM, stroke_width=5).move_to([gx + v.get_value() * half, gy, 0])
            return c.set_fill(TEAL if inside else GHOST, opacity=0.9)

        pcell = always_redraw(live_cell)
        lab = T("length(p)", 40).move_to([3.5, 1.7, 0])
        num = always_redraw(lambda: T("%.2f" % v.get_value(), 110).move_to([3.5, 0.2, 0]))
        verdict = always_redraw(lambda: T("planet" if v.get_value() < 0.25 else "stage", 40).move_to([3.5, -1.2, 0]))
        code = M("if (length(p) < 0.25)", 32).move_to([gx, -3.0, 0])
        self.play(Create(grid), Create(planet), run_time=0.7)
        self.add(trail, pcell, probe)
        self.play(FadeIn(lab), FadeIn(num), FadeIn(verdict), run_time=0.4)
        until(self, "Length of p", lead=0.1)
        self.play(v.animate.set_value(0.2), run_time=2.6, rate_func=linear)
        self.wait(0.3)
        until(self, "Under the radius", lead=0.2)
        self.play(v.animate.set_value(0.4), run_time=1.4, rate_func=linear)
        self.play(FadeIn(code, shift=UP * 0.2), run_time=0.4)
        until(self, "paint planet color", lead=0.1)
        inside = [s for row in grid.cells for s in row if np.hypot(s.get_center()[0] - gx, s.get_center()[1] - gy) < rad]
        self.play(*[tint(s, TEAL, 0.9) for s in inside], run_time=0.7)
        done(self)


# ═════════════════════════════ B20 · paper against screen ═════════════════════════════
def a3_circ(cx, cy, r, up):
    """A circle with its y arrow and the dot at a quarter turn: up on paper, down on a screen. Returns a VGroup(circle, arrow, radius line, dot)."""
    sgn = 1 if up else -1
    c = Circle(radius=r, stroke_color=INK, stroke_width=5).move_to([cx, cy, 0])
    ar = arrow([cx - r - 0.6, cy - sgn * 0.85, 0], [cx - r - 0.6, cy + sgn * 0.85, 0], color=DIM, w=6)
    rl = Line([cx, cy, 0], [cx, cy + sgn * r, 0], color=DIM, stroke_width=4)
    d = Dot([cx, cy + sgn * r, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3)
    return VGroup(c, ar, rl, d)


class B20_Flip(Scene):
    def construct(self):
        r = 1.3; cy = 0.35
        left = a3_circ(-3.4, cy, r, True)
        right = a3_circ(3.4, cy, r, False)
        l1 = T("on paper", 40).move_to([-3.4, -1.8, 0])
        l2 = T("on a screen", 40).move_to([3.4, -1.8, 0])
        y1 = T("y", 32, DIM).move_to([-3.4 - r - 0.6 - 0.45, cy, 0])
        y2 = T("y", 32, DIM).move_to([3.4 - r - 0.6 - 0.45, cy, 0])
        credit = T("Godot docs  ·  y is down in 2D", 32, DIM).move_to([0, -3.0, 0])
        self.play(Create(left), FadeIn(l1), FadeIn(y1), run_time=0.8)
        until(self, "On a screen", lead=0.2)
        moving = left.copy()
        self.play(ReplacementTransform(moving, right), FadeIn(l2), FadeIn(y2), run_time=1.4)
        self.play(FadeIn(credit), run_time=0.4)
        until(self, "and a growing angle", lead=0.3)
        dot = right[3]
        a = ValueTracker(90.0)
        runner = always_redraw(lambda: Dot([3.4 + r * np.cos(np.radians(a.get_value())), cy - r * np.sin(np.radians(a.get_value())), 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3))
        arc_r = r + 0.35
        back = Arc(radius=arc_r, start_angle=-PI / 2, angle=-5 * PI / 3, arc_center=[3.4, cy, 0], stroke_color=DIM, stroke_width=18, stroke_opacity=0.55)
        arc = Arc(radius=arc_r, start_angle=-PI / 2, angle=-5 * PI / 3, arc_center=[3.4, cy, 0], stroke_color=TERRA, stroke_width=10)
        th = -PI / 2 - 5 * PI / 3
        endp = np.array([3.4 + arc_r * np.cos(th), cy + arc_r * np.sin(th), 0.0])
        tip = Triangle(fill_color=TERRA, fill_opacity=1, stroke_color=DIM, stroke_width=3).scale(0.26)
        tip.rotate(np.arctan2(-np.cos(th), np.sin(th)) - PI / 2).move_to(endp)
        self.remove(dot)
        self.add(runner)
        self.play(a.animate.set_value(450.0), Create(back), Create(arc), run_time=2.2, rate_func=linear)
        self.play(FadeIn(tip), run_time=0.2)
        done(self)


# ═════════════════════════════ B25 · the recipe ═════════════════════════════
def a3_slider(label, x, y, w=3.2):
    track = Line([x - w / 2, y, 0], [x + w / 2, y, 0], color=DIM, stroke_width=7)
    cap = T(label, 36).move_to([x, y + 0.5, 0])
    knob = Dot([x - w / 2 + 0.25 * w, y, 0], radius=0.17, color=TERRA).set_stroke(DIM, width=3)
    g = VGroup(track, cap, knob)
    g.knob = knob; g.track = track; g.x0 = x - w / 2; g.w = w; g.y = y
    return g


def a3_at(sl, f):
    return np.array([sl.x0 + f * sl.w, sl.y, 0])


class B25_Recipe(Scene):
    def construct(self):
        cw = 0.248          # measured width of one Menlo glyph at 32 pt
        text = "center + radius * vec2(cos(a), sin(a))"
        left_x = -len(text) * cw / 2.0
        parts = {}
        for name, (i0, s) in {"center": (0, "center"), "plus": (7, "+"), "radius": (9, "radius"), "star": (16, "*"), "v": (18, "vec2(cos("), "a1": (27, "a"),
                                "m": (28, "),"), "s": (31, "sin("), "a2": (35, "a"), "e": (36, "))")}.items():
            m = M(s, 32)
            m.move_to([left_x + cw * (i0 + len(s) / 2.0), 2.6, 0])
            parts[name] = m
        line = VGroup(*parts.values())
        # orbit
        K = 2.2
        cx = ValueTracker(-3.3); R = ValueTracker(0.4); sp = ValueTracker(1.0); ang = ValueTracker(0.6)
        cyy = -0.45
        ringm = always_redraw(lambda: Circle(radius=K * R.get_value(), stroke_color=DIM, stroke_width=4).move_to([cx.get_value(), cyy, 0]))
        planet = always_redraw(lambda: Circle(radius=0.42, stroke_color=A3_PLANET, stroke_width=0).set_fill(A3_PLANET, opacity=1).move_to([cx.get_value(), cyy, 0]))
        moon_pos = lambda: np.array([cx.get_value() + K * R.get_value() * np.cos(ang.get_value()), cyy + K * R.get_value() * np.sin(ang.get_value()), 0])
        moon = always_redraw(lambda: Dot(moon_pos(), radius=0.2, color=A3_MOON))
        ang.add_updater(lambda m, dt: m.increment_value(dt * sp.get_value()))
        s_r = a3_slider("radius", 3.9, 1.25); s_c = a3_slider("center", 3.9, -0.15); s_s = a3_slider("speed", 3.9, -1.55)
        self.add(ringm, planet, moon)
        self.play(FadeIn(line), *[Create(s) for s in (s_r, s_c, s_s)], run_time=0.8)
        # the speed marks: two short strokes trailing the moon, shown while fast
        trail_on = ValueTracker(0.0)

        def speed_marks():
            op = trail_on.get_value()
            a = ang.get_value()
            tang = np.array([np.sin(a), -np.cos(a), 0.0])        # opposite to the direction of travel
            p = moon_pos()
            return VGroup(*[Line(p + tang * (0.38 + 0.3 * k), p + tang * (0.55 + 0.3 * k), color=INK, stroke_width=6, stroke_opacity=op) for k in range(2)])
        sm = always_redraw(speed_marks)
        self.add(sm)

        def hit(keys, mobs=None):
            # terracotta underline bars over a grey backing (a bar, never text; the ring read as accent text)
            return VGroup(*[VGroup(Rectangle(width=parts[k].width + 0.2, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).next_to(parts[k], DOWN, buff=0.08),
                                   Rectangle(width=parts[k].width + 0.2, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).next_to(parts[k], DOWN, buff=0.12)) for k in keys])

        until(self, "The radius sets", lead=0.35)
        h1 = hit(["radius"])
        self.play(FadeIn(h1), s_r.knob.animate.move_to(a3_at(s_r, 0.75)), R.animate.set_value(0.8), run_time=1.2)
        until(self, "The center sets", lead=0.3)
        h2 = hit(["center"])
        self.play(FadeOut(h1), FadeIn(h2), s_c.knob.animate.move_to(a3_at(s_c, 0.75)), cx.animate.set_value(-1.0), run_time=1.3)
        until(self, "The angle's speed", lead=0.3)
        h3 = hit(["a1", "a2"])
        self.play(FadeOut(h2), FadeIn(h3), s_s.knob.animate.move_to(a3_at(s_s, 0.8)), sp.animate.set_value(3.0), trail_on.animate.set_value(1.0), run_time=1.0)
        done(self)
