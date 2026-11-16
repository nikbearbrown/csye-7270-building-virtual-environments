"""ACT II · Lit or Unlit  (B13, B18; Manim)

B13 a work flow: a `fragment()` box emits a card of the five surface outputs, the card enters "Godot's lighting", two lamps feed the same box, one pixel
comes out. B18 a decision sketch: "looks wrong" splits into two questions, a dot walks each branch and lights its one-word remedy.
Everything here is a drawing (labelled by its words); no Godot output is claimed.
"""


def a2_at(self, t_abs):
    """Wait until absolute scene time t_abs (seconds)."""
    gap = t_abs - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a2_lamp(x, y):
    """A lamp icon drawn from shapes: a bulb, a neck and a cap."""
    bulb = Circle(radius=0.3, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    neck = Line([x - 0.14, y - 0.34, 0], [x + 0.14, y - 0.34, 0], color=INK, stroke_width=5)
    cap = Line([x - 0.1, y - 0.46, 0], [x + 0.1, y - 0.46, 0], color=INK, stroke_width=5)
    ray = VGroup(*[Line([x + 0.46 * np.cos(a), y + 0.46 * np.sin(a), 0], [x + 0.62 * np.cos(a), y + 0.62 * np.sin(a), 0], color=DIM, stroke_width=4)
                   for a in (np.pi * 0.25, np.pi * 0.5, np.pi * 0.75)])
    return VGroup(bulb, neck, cap, ray)


def a2_tag(text, x, y, w=None):
    t = T(text, 32)
    w = w or t.width + 0.5
    b = box(x, y, w, 0.7, color=INK, sw=3)
    t.move_to([x, y, 0])
    g = VGroup(b, t)
    g.b = b
    return g


# ═════════════════════════════ B13 · the lit pipeline ═════════════════════════════
class B13_LitPipeline(Scene):
    def construct(self):
        fbox = box(-4.7, 0.0, 2.7, 0.9, color=INK, sw=4)
        ftxt = M("fragment()", 32).move_to([-4.7, 0.0, 0])
        you = T("you describe", 32).move_to([-4.7, -0.95, 0])
        names = ["ALBEDO", "ALPHA", "EMISSION", "ROUGHNESS", "METALLIC"]
        chips = VGroup(*[M(n, 32).move_to([0, 0.95 - i * 0.48, 0]) for i, n in enumerate(names)])
        cframe = box(0, 0.0, chips.width + 0.5, 3.05, color=DIM, sw=4)
        cframe.set_fill(PALEBOX, opacity=1)
        csurf = T("surface", 32).move_to([0, 1.82, 0])
        card = VGroup(cframe, chips)
        cardall = VGroup(card, csurf)
        cardall.move_to([-1.9, 0.0, 0])
        lbox = box(1.9, 0.0, 3.5, 2.0, color=INK, sw=4)
        ltxt = T("Godot's lighting", 32).move_to([1.9, 0.0, 0])
        flow = arrow([-3.3, 0.0, 0], [0.05, 0.0, 0], color=GHOST, w=7)
        self.add(fbox, ftxt, flow)
        self.play(FadeIn(you), GrowFromCenter(cardall), run_time=0.7)
        self.play(FadeIn(lbox), FadeIn(ltxt), run_time=0.5)
        # the card enters the lighting box (done well before the midpoint)
        a2_at(self, 1.4)
        self.play(cardall.animate.scale(0.32).move_to([1.9, 0.0, 0]).set_opacity(0.0), run_time=1.4)
        ltxt.set_opacity(1)
        # every lamp feeds the same box from above
        until(self, "and every lamp")
        lamps = VGroup(a2_lamp(0.95, 2.75), a2_lamp(2.85, 2.75))
        beams = VGroup(arrow([0.95, 2.1, 0], [1.2, 1.1, 0], color=DIM, w=7, tip=0.24), arrow([2.85, 2.1, 0], [2.6, 1.1, 0], color=DIM, w=7, tip=0.24))
        self.play(FadeIn(lamps), run_time=0.5)
        self.play(*[GrowArrow(b) for b in beams], run_time=0.6)
        # one pixel comes out on the right
        a2_at(self, 5.65)
        out = arrow([3.75, 0.0, 0], [4.85, 0.0, 0], w=7)
        pix = Square(side_length=0.62, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([5.4, 0.0, 0])
        plab = T("one pixel", 32).move_to([5.4, -0.8, 0])
        self.play(GrowArrow(out), run_time=0.4)
        self.play(FadeIn(pix, scale=0.5), FadeIn(plab), run_time=0.5)
        done(self)


# ═════════════════════════════ B18 · two checks ═════════════════════════════
def a2_ubar(mob, pad=0.08):
    """terracotta underline bar over a grey backing (a bar, never text): the emphasis mark that does not read as accent text"""
    w = mob.width + 2 * pad
    return VGroup(Rectangle(width=w, height=0.2, stroke_width=0).set_fill(DIM, opacity=0.55).move_to(mob.get_bottom() + DOWN * 0.18),
                  Rectangle(width=w, height=0.12, stroke_width=0).set_fill(TERRA, opacity=1).move_to(mob.get_bottom() + DOWN * 0.18))


class B18_TwoChecks(Scene):
    def construct(self):
        top = Square(side_length=0.7, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([-1.3, 2.55, 0])
        toplab = T("looks wrong", 32).move_to([0.5, 2.55, 0])
        lx, rx = -3.7, 3.7
        # skeleton of both branches (grey), lit as the dot walks them
        bl = arrow([-1.0, 2.1, 0], [lx, 1.8, 0], color=DIM, w=5)
        br = arrow([1.0, 2.1, 0], [rx, 1.8, 0], color=DIM, w=5)
        self.add(top, toplab)
        self.play(GrowArrow(bl), GrowArrow(br), run_time=0.6)
        dot = Dot([0, 2.1, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.add(dot)
        # left: is a lamp changing my color?
        until(self, "Is a lamp")
        lamp = a2_lamp(lx, 0.95)
        q = T("?", 40).move_to([lx + 0.95, 0.95, 0])
        self.play(dot.animate.move_to([lx, 1.8, 0]), FadeIn(lamp), FadeIn(q), run_time=0.7)
        a1 = arrow([lx, 0.38, 0], [lx, -0.15, 0], color=DIM, w=5)
        sph = Circle(radius=0.62, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([lx, -0.85, 0])
        hi = Circle(radius=0.26, stroke_width=0).set_fill(CARD, opacity=0.65).move_to([lx - 0.2, -0.65, 0])
        self.play(GrowArrow(a1), dot.animate.move_to([lx, -0.15, 0]), run_time=0.5)
        self.play(FadeIn(sph), FadeIn(hi), run_time=0.4)
        until(self, "Add unshaded")
        tagl = a2_tag("add unshaded", lx, -2.5, 3.5)
        self.play(FadeOut(hi), sph.animate.set_fill(TEAL, opacity=1), dot.animate.move_to([lx, -1.8, 0]), run_time=0.6)
        self.play(FadeIn(tagl), run_time=0.4)
        rl = a2_ubar(tagl)
        self.play(FadeIn(rl), run_time=0.4)
        # right: is the back side being skipped?
        until(self, "Is the back side")
        self.play(dot.animate.move_to([rx, 1.8, 0]), run_time=0.7)
        back = Square(side_length=1.1, stroke_color=DIM, stroke_width=4).move_to([rx, 0.95, 0])
        a2 = arrow([rx, 0.3, 0], [rx, -0.2, 0], color=DIM, w=5)
        sq = Square(side_length=1.1, stroke_color=INK, stroke_width=4).set_fill(TEAL, opacity=1).move_to([rx, -0.9, 0])
        self.play(FadeIn(back), run_time=0.4)
        self.play(GrowArrow(a2), dot.animate.move_to([rx, -0.2, 0]), run_time=0.4)
        self.play(FadeIn(sq), run_time=0.4)
        until(self, "Add cull disabled")
        tagr = a2_tag("add cull disabled", rx, -2.5, 4.6)
        self.play(dot.animate.move_to([rx, -1.8, 0]), FadeIn(tagr), run_time=0.5)
        rr = a2_ubar(tagr)
        self.play(FadeIn(rr), run_time=0.4)
        # a faint third tag
        until(self, "blend add")
        tagb = a2_tag("blend add", 0, 0.7, 2.8).set_opacity(0.45)
        cap = T("more modes in the docs", 32).move_to([0, -0.05, 0])
        self.play(FadeIn(tagb), FadeIn(cap), run_time=0.5)
        done(self)
