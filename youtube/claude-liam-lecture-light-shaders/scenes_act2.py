"""ACT II · The Light Function  (B11, B12: Manim)

Cast for the act: the lamp is a gold dot with a grey ring (a2_lamp); an answer from one lamp is a small ramp-coloured swatch (a2_swatch);
built-ins are Menlo capitals; arrows are shapes pointing only forward. Pictures are drawings and labelled as such by their plain words.
"""


def a2_lamp(x, y, r=0.2):
    d = Dot([x, y, 0], radius=r, color=GOLD)
    d.set_stroke(DIM, width=3)
    return d


def a2_swatch(x, y, v, s=0.5):
    """A small square of the ramp colour for value v (an answer from one lamp)."""
    return Square(side_length=s, fill_color=_rgb(v), fill_opacity=1, stroke_color=DIM, stroke_width=3).move_to([x, y, 0])


def a2_input(name, y, x0=-6.1, x1=-1.95):
    """An input arrow into the function box with its monospace label above the shaft."""
    a = arrow([x0, y, 0], [x1, y, 0], w=6)
    lab = M(name, 32).move_to([x0 + 0.1, y + 0.36, 0])
    lab.move_to([x0 + lab.width / 2 + 0.1, y + 0.36, 0])
    return VGroup(a, lab)


class B11_FunctionBox(Scene):
    def construct(self):
        fb = box(0.0, 0.55, 3.6, 3.5, color=INK, sw=5)
        fl = M("light()", 32).move_to([0.0, 0.55, 0])
        self.play(Create(fb), FadeIn(fl), run_time=0.8)
        names = ["COLOR", "UV", "LIGHT_COLOR", "LIGHT_ENERGY"]
        ys = [1.85, 1.0, 0.15, -0.7]
        ins = [a2_input(n, y) for n, y in zip(names, ys)]
        until(self, "Color is")
        self.play(FadeIn(ins[0], shift=RIGHT * 0.7), run_time=0.7)
        until(self, "U V is")
        self.play(FadeIn(ins[1], shift=RIGHT * 0.7), run_time=0.7)
        until(self, "Light color and")
        self.play(FadeIn(ins[2], shift=RIGHT * 0.7), run_time=0.6)
        until(self, "light energy describe")
        self.play(FadeIn(ins[3], shift=RIGHT * 0.7), run_time=0.6)
        cap = VGroup(T("built-in: a value the engine hands to a function,", 32), T("or collects from it", 32)).arrange(DOWN, buff=0.12).move_to([0, -2.0, 0])
        note = T("more in the docs: NORMAL, SCREEN_UV ...", 32, DIM).move_to([0, -3.0, 0])
        until(self, "values written")
        self.play(FadeIn(cap), run_time=0.6)
        self.play(FadeIn(note), run_time=0.5)
        until(self, "You hand back")
        out = arrow([1.8, 0.55, 0], [4.2, 0.55, 0], w=7)
        tip = Dot([4.2, 0.55, 0], radius=0.14, color=TERRA).set_stroke(DIM, width=3)
        ol = M("LIGHT", 32).move_to([5.3, 0.55, 0])
        self.play(GrowArrow(out), FadeIn(tip), run_time=0.8)
        self.play(FadeIn(ol), run_time=0.4)
        done(self)


class B12_Order(Scene):
    def construct(self):
        frag = box(-4.6, 0.0, 2.8, 1.3, DIM, 5, fill=PALEBOX)
        fl = M("fragment()", 32).move_to([-4.6, 0.0, 0])
        fs = T("sets color", 32).move_to([-4.6, -1.05, 0])
        lit = box(-1.2, 0.0, 2.6, 1.3, DIM, 5, fill=PALEBOX)
        ll = M("light()", 32).move_to([-1.2, 0.0, 0])
        amb = box(2.5, 0.0, 3.2, 1.6, DIM, 5, fill=PALEBOX)
        al = T("+ ambient look", 32).move_to([2.5, 0.3, 0])
        pix = Square(side_length=1.1, stroke_color=INK, stroke_width=5).move_to([5.5, 0.0, 0])
        a1 = arrow([-3.2, 0, 0], [-2.5, 0, 0], w=6, tip=0.2)
        a2 = arrow([0.1, 0, 0], [0.9, 0, 0], w=6, tip=0.2)
        a3 = arrow([4.1, 0, 0], [4.9, 0, 0], w=6, tip=0.2)
        strip = VGroup(frag, fl, fs, lit, ll, amb, al, pix, a1, a2, a3)
        self.play(FadeIn(strip), run_time=0.8)
        until(self, "Fragment runs first")
        tok = Dot([-6.15, 0, 0], radius=0.17, color=TEAL).set_stroke(DIM, width=3)
        self.play(FadeIn(tok), run_time=0.3)
        self.play(tok.animate.move_to([-2.45, 0, 0]), run_time=1.5, rate_func=linear)
        until(self, "once for each lamp")
        l1, l2 = a2_lamp(-1.9, 2.0), a2_lamp(-0.5, 2.0)
        lt = T("per lamp", 32).move_to([-1.2, 2.75, 0])
        d1 = arrow([-1.9, 1.75, 0], [-1.9, 0.7, 0], w=5, tip=0.18)
        d2 = arrow([-0.5, 1.75, 0], [-0.5, 0.7, 0], w=5, tip=0.18)
        self.play(FadeIn(VGroup(l1, l2, lt)), GrowArrow(d1), GrowArrow(d2), run_time=0.8)
        s1, s2 = a2_swatch(-1.9, -1.55, 0.3), a2_swatch(-0.5, -1.55, 0.45)
        e1 = arrow([-1.9, -0.7, 0], [-1.9, -1.2, 0], w=5, tip=0.16)
        e2 = arrow([-0.5, -0.7, 0], [-0.5, -1.2, 0], w=5, tip=0.16)
        k1 = Dot([-1.9, -0.7, 0], radius=0.17, color=TEAL).set_stroke(DIM, width=3)
        k2 = Dot([-0.5, -0.7, 0], radius=0.17, color=TEAL).set_stroke(DIM, width=3)
        self.play(FadeOut(tok), FadeIn(k1), FadeIn(k2), run_time=0.5)
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(s1), FadeIn(s2), FadeOut(k1), FadeOut(k2), run_time=0.8)
        until(self, "adds all the answers")
        self.play(s1.animate.move_to([1.9, -1.55, 0]), s2.animate.move_to([3.1, -1.55, 0]), FadeOut(VGroup(e1, e2)), run_time=0.9)
        self.play(s1.animate.move_to([1.9, -0.28, 0]).scale(0.7), s2.animate.move_to([3.1, -0.28, 0]).scale(0.7), run_time=0.8)
        until(self, "That sum is")
        self.play(pix.animate.set_fill(_rgb(0.7), opacity=1), run_time=0.9)
        done(self)
