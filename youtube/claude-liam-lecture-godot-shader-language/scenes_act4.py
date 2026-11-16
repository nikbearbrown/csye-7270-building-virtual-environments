"""ACT IV · Choices and Loops  (B29, B32: the Manim beats of this act that this file carries)

Cast for the act: the split picture (a real Lab render, teal left and pale right, shown as itself), the pixel row of the float-equality scene
(a schematic, labelled as one), and the real 1920-wide renders. Code lines are lines of real files in lab-shaders/ (16-split-if, 17-split-ternary,
19-float-equals, 20-float-range), placed on a measured character grid so Pango can never drop a space.
"""

A4P = "pantry/"


def a4_cw(size=32):
    """Advance of one Menlo character at this size, measured once with Manim 0.20.1 (font scaling is not linear in size: 32 -> 0.25, 40 -> 0.35).
    Constants, not a runtime measurement: Gate A's stub Text has no real widths."""
    return {32: 0.25, 36: 0.30, 40: 0.35}.get(size, 0.25 * size / 32)


def a4_mono(s, xl, y, size=32, color=INK):
    """One code line, LEFT edge on the character grid (leading spaces are columns)."""
    ind = len(s) - len(s.lstrip(" "))
    t = Text(s.lstrip(" "), font=MONO, color=color, font_size=size)
    t.move_to([xl + ind * a4_cw(size) + t.width / 2, y, 0])
    return t


def a4_x(xl, col, size=32):
    return xl + col * a4_cw(size)


def a4_t(s, x, y, size=32, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a4_equals(x, y, w=0.7, gap=0.2):
    return VGroup(Line([x - w / 2, y + gap / 2, 0], [x + w / 2, y + gap / 2, 0], color=INK, stroke_width=7),
                  Line([x - w / 2, y - gap / 2, 0], [x + w / 2, y - gap / 2, 0], color=INK, stroke_width=7))


def a4_glyphs(lines):
    return VGroup(*[g for ln in lines for g in ln.submobjects])


# ═════════════════════════════ B29 · the ternary is a one-line if ═════════════════════════════
class B29_Collapse(Scene):
    def construct(self):
        xl = -4.25
        six = ["vec3 c;", "if (UV.x < 0.5) {", "  c = teal;", "} else {", "  c = pale;", "}"]
        one = "vec3 c = UV.x < 0.5 ? teal : pale;"
        lh = 0.5
        ytop = 3.0
        sixl = [a4_mono(s, xl, ytop - lh * i) for i, s in enumerate(six)]
        yone = ytop - lh * 1.0
        onel = a4_mono(one, xl, yone)
        gs, g1 = a4_glyphs(sixl), a4_glyphs([onel])
        cap = a4_t("ternary: a one-line if", 0, 0.3)
        # brackets under the three parts of the one line (cols: "vec3 c = " is 9, condition 9..18, ? at 20, teal 22..25, : at 27, pale 29..32)
        by = yone - 0.42
        t_cond = type_tag("condition", a4_x(xl, 9), a4_x(xl, 19) - 0.05, by)
        t_true = type_tag("if true", a4_x(xl, 22), a4_x(xl, 26) - 0.05, by)
        t_false = type_tag("if false", a4_x(xl, 29), a4_x(xl, 33) - 0.05, by)
        t_true.tag.shift(LEFT * 0.35)
        t_false.tag.shift(RIGHT * 0.45)
        q = a4_x(xl, 20) + a4_cw() * 0.45
        c_ = a4_x(xl, 27) + a4_cw() * 0.45
        # the ? and : are marked by a terracotta dot (grey-ringed) just above each glyph: a ring round one glyph of a line would cut its neighbours
        rq = Dot([q, yone + 0.4, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3)
        rc = Dot([c_, yone + 0.4, 0], radius=0.12, color=TERRA).set_stroke(DIM, width=3)
        pic = lab_window(A4P + "split-if.png", 2.6, -2.7, -1.6, "")
        pcap = a4_t("Godot 4.7.2 · Forward+ · same pixels", -0.0, -2.9)
        eq = a4_equals(0.55, -1.6)
        same = a4_t("same pixels", 2.7, -1.6)

        self.play(FadeIn(gs), FadeIn(pic), FadeIn(pcap), run_time=0.7)
        until(self, "Write the condition", lead=0.0)
        self.play(Transform(gs, g1), run_time=1.0)
        self.play(FadeIn(cap), run_time=0.3)
        until(self, "Write the condition", lead=0.0)
        self.play(FadeIn(t_cond), run_time=0.4)
        until(self, "a question mark", lead=0.1)
        self.play(FadeIn(rq), run_time=0.3)
        until(self, "the value if true", lead=0.1)
        self.play(FadeIn(t_true), run_time=0.3)
        until(self, "a colon", lead=0.1)
        self.play(FadeIn(rc), run_time=0.3)
        until(self, "then the value if false", lead=0.1)
        self.play(FadeIn(t_false), run_time=0.3)
        until(self, "Same picture", lead=0.1)
        self.play(FadeIn(eq), FadeIn(same), run_time=0.5)
        done(self)


# ═════════════════════════════ B32 · no pixel lands on one half ═════════════════════════════
class B32_NoPixelLands(Scene):
    def construct(self):
        grid = pixel_grid(cols=12, rows=1, cell=0.7, x=0.0, y=2.2, color=DIM, sw=3)
        cells = grid.cells[0]
        dots = VGroup(*[Dot(c.get_center(), radius=0.07, color=INK) for c in cells])
        half = Line([0, 2.8, 0], [0, 1.35, 0], color=INK, stroke_width=6)
        ax = Line([-4.2, 1.35, 0], [4.2, 1.35, 0], color=INK, stroke_width=5)
        l0 = a4_t("0", -4.2, 1.0)
        l1 = a4_t("1", 4.2, 1.0)
        lh = a4_t("0.5", 0.0, 1.0)
        slab = a4_t("schematic: 12 pixels", -4.0, 3.3 - 0.0, 32)
        slab.move_to([0.0, 3.0, 0])
        xl = -6.0
        c1 = a4_mono("if (UV.x == 0.5)", xl, 0.5)
        c2 = a4_mono("if (abs(UV.x - 0.5) < 0.005)", xl, 0.0)
        none = a4_t("no pixel center is exactly 0.5", 2.15, 0.5)
        absl = a4_t("abs: drops the minus sign: -0.3 becomes 0.3", -1.6, -0.5)
        probe = Dot([-4.2, 2.2, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        pa = lab_window(A4P + "float-equals-1920.png", 3.0, -3.2, -1.75, "")
        pb = lab_window(A4P + "float-range-1920.png", 3.0, 3.2, -1.75, "")
        ca = a4_t("Forward+ · 1920 wide", -3.2, -3.0)
        cb = a4_t("Forward+ · 1920 wide", 3.2, -3.0)

        self.play(Create(grid), FadeIn(slab), run_time=0.6)
        self.play(FadeIn(dots), Create(ax), Create(half), FadeIn(l0), FadeIn(l1), FadeIn(lh), run_time=0.6)
        until(self, "Light U V dot X", lead=0.1)
        self.play(FadeIn(c1), run_time=0.4)
        # the probe sweeps the row: nothing lights
        self.play(FadeIn(probe), run_time=0.2)
        self.play(probe.animate.move_to([4.2, 2.2, 0]), run_time=1.6, rate_func=linear)
        self.play(FadeIn(none), FadeOut(probe), run_time=0.4)
        until(self, "A small range", lead=0.1)
        self.play(FadeIn(c2), FadeIn(absl), FadeOut(none), run_time=0.4)
        probe2 = Dot([-4.2, 2.2, 0], radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.play(FadeIn(probe2), run_time=0.15)
        self.play(probe2.animate.move_to([-0.35, 2.2, 0]), run_time=0.8, rate_func=linear)
        self.play(tint(cells[5], TEAL, 0.9), probe2.animate.move_to([0.35, 2.2, 0]), run_time=0.4)
        self.play(tint(cells[6], TEAL, 0.9), run_time=0.3)
        self.play(FadeOut(probe2), run_time=0.2)
        until(self, "documentation warns", lead=0.9)
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(ca), FadeIn(cb), run_time=0.6)
        done(self)
