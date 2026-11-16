"""ACT VIII · What the Agent Gets Wrong  (B56 and B57 Manim; B58 is a Remotion CCPlainShell, see lanes/act8.json)

B56 and B57 draw the five rows of the assignment's own table "What the agent is likely to get wrong" (evidence/example/sources/assignment-05.md
lines 405-415: "Recorded mistake" / "How it was caught"). The table's words are shortened to labels of one to three words; the pictures that make
a mistake visible are DRAWINGS and carry status_tag("illustrative"); the table as a whole carries status_tag("recorded in the assignment's runs").
Nothing here is a capture or a log: no number is shown that the table does not give (30, 144, 11, 4, 100).
Pacing: until() cues come from the character share of the narration (no audio yet); everything lands by ~90 % of the estimate.
"""

def a8_lab(s, x, y, size=34, color=INK, left=False):
    t = T(s, size, color)
    if left:
        return t.move_to([x, y, 0], aligned_edge=LEFT)
    return t.move_to([x, y, 0])


def a8_table(y_top, y_bot, x_div, header_y=None):
    """The table frame: outline, one column divider, one row divider per call site added by the scene. Returns VGroup(frame, divider)."""
    fr = RoundedRectangle(width=12.2, height=y_top - y_bot, corner_radius=0.18, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, (y_top + y_bot) / 2, 0])
    dv = Line([x_div, y_top, 0], [x_div, y_bot, 0], color=GHOST, stroke_width=4)
    return VGroup(fr, dv)


def a8_hline(y):
    return Line([-6.1, y, 0], [6.1, y, 0], color=GHOST, stroke_width=4)


def a8_tick_small(x, y, s=0.12, color=DIM, w=4):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


# ── B56 · rows 1-2: a test rewritten around its own failure; type checks that were round trips ─────────────────────────────
class B56_RecordedMistakes(Scene):
    def construct(self):
        X_DIV = 2.6
        tbl = a8_table(3.3, -2.3, X_DIV)
        rdv = a8_hline(0.3)
        hd_m = a8_lab("mistake", -1.8, 2.95, 32)
        hd_c = a8_lab("caught by", 4.35, 2.95, 32)
        hdl = a8_hline(2.7)
        t1 = status_tag("recorded in the assignment's runs", -2.9, -2.95)
        t2 = status_tag("illustrative", 1.75, -2.95)
        self.play(Create(tbl), Create(rdv), Create(hdl), FadeIn(hd_m), FadeIn(hd_c), FadeIn(t1), FadeIn(t2), run_time=0.7)
        # row 1: the test that was rewritten to call the update function directly
        test = box(-5.1, 1.55, 1.5, 0.8, color=DIM, sw=4)
        test_l = a8_lab("test", -5.1, 1.55, 34)
        fps = a8_lab("30 fps", -3.55, 2.2, 32, color=DIM)
        a_in = arrow([-4.2, 1.55, 0], [-2.85, 1.55, 0], color=DIM, w=6, tip=0.2)
        until(self, "After a thirty", lead=0.1)
        self.play(Create(test), FadeIn(test_l), FadeIn(fps), GrowArrow(a_in), run_time=0.5)
        until(self, "rewrote its test", lead=0.1)
        upd = box(-1.55, 1.55, 2.3, 0.8, color=INK, sw=4)
        upd_l = M("update()", 26).move_to([-1.55, 1.55, 0])
        a_dir = arrow([-4.2, 1.55, 0], [-2.75, 1.55, 0], color=INK, w=7, tip=0.22)
        self.play(FadeIn(upd), FadeIn(upd_l), run_time=0.4)
        self.play(FadeOut(a_in), GrowArrow(a_dir), run_time=0.35)
        until(self, "update function", lead=0.1)
        x1 = cross_mark(-4.6, 2.2, s=0.17, w=7)
        fl = a8_lab("frame rate ignored", -3.3, 0.72, 32)
        self.play(Create(x1), FadeIn(fl), run_time=0.4)
        until(self, "the summary still", lead=0.1)
        card = box(0.95, 1.38, 1.9, 1.6, color=DIM, sw=4)
        c_l = a8_lab("summary", 0.95, 2.4, 32)
        self.play(Create(card), FadeIn(c_l), run_time=0.4)
        until(self, "thirty and one forty-four", lead=0.1)
        n30 = a8_lab("30", 0.95, 1.7, 44)
        n144 = a8_lab("144", 0.95, 1.05, 44)
        self.play(FadeIn(n30), FadeIn(n144), run_time=0.35)
        # row 2: the semicolon is deleted; all eleven type checks still pass
        until(self, "And its type checks", lead=0.1)
        blk = code_block(["shader_type spatial"], x=-3.5, y=-1.55, size=24, first=1)
        self.play(Create(blk.frame), FadeIn(blk.rows), run_time=0.45)
        until(self, "round trips", lead=0.2)
        rt = a8_lab("round trips", 0.7, -1.55, 36, left=False)
        self.play(FadeIn(rt), run_time=0.35)
        until(self, "semicolon deleted", lead=0.25)
        semi_x = -3.5 - blk.W / 2 + 0.3 + (1 * blk.cw + 0.25) + 19 * blk.cw + 0.12      # just after the 19th character: where the deleted ";" stood
        gap = Dot([semi_x, -1.55, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(gap, scale=0.5), run_time=0.3)
        until(self, "all eleven", lead=0.3)
        ticks = [a8_tick_small(-5.55 + 0.36 * k, -0.55, s=0.13, color=INK, w=5) for k in range(11)]
        n11 = a8_lab("11", -0.75, -0.5, 52)
        self.play(LaggedStart(*[Create(t_) for t_ in ticks], lag_ratio=0.12), FadeIn(n11), run_time=0.8)
        until(self, "Reading the test", lead=0.4)
        eye = eye_icon(3.5, 1.75, s=0.5)
        e_l = a8_lab("reading the test", 4.3, 0.75, 34)
        self.play(Create(eye), FadeIn(e_l), run_time=0.45)
        until(self, "the mutation", lead=0.7)
        term = terminal_icon(3.5, -0.75, s=0.45)
        m_l = a8_lab("the mutation", 4.3, -1.75, 34)
        self.play(Create(term), FadeIn(m_l), run_time=0.4)
        done(self)


# ── B57 · rows 3-5: a misnamed enum; an import key the importer ignores; a flag no check asserted ─────────────────────────
class B57_MoreMistakes(Scene):
    def construct(self):
        X_DIV = 3.2
        tbl = a8_table(3.3, -2.3, X_DIV)
        h1, h2 = a8_hline(2.7), a8_hline(1.0)
        h3 = a8_hline(-0.65)
        hd_m = a8_lab("mistake", -1.4, 2.95, 32)
        hd_c = a8_lab("caught by", 4.65, 2.95, 32)
        t1 = status_tag("recorded in the assignment's runs", -2.9, -2.95)
        t2 = status_tag("illustrative", 1.75, -2.95)
        self.play(Create(tbl), Create(h1), Create(h2), Create(h3), FadeIn(hd_m), FadeIn(hd_c), FadeIn(t1), FadeIn(t2), run_time=0.7)
        # row 3: the enum
        until(self, "An audit misnamed", lead=0.05)
        r3 = a8_lab("enum misnamed", -5.9, 1.85, 32, left=True)
        self.play(FadeIn(r3), run_time=0.35)
        until(self, "four is the Ag X", lead=0.1)
        four = a8_lab("4", -2.55, 1.85, 72)
        agx = M("TONE_MAPPER_AGX", 24).move_to([-1.95, 1.85, 0], aligned_edge=LEFT)
        self.play(FadeIn(four), FadeIn(agx), run_time=0.4)
        until(self, "not Aces", lead=0.05)
        aces = a8_lab("ACES", 2.4, 1.85, 36, color=DIM)
        x3 = cross_mark(1.5, 1.85, s=0.2, w=8)
        self.play(Create(x3), FadeIn(aces), run_time=0.35)
        # row 4: the import key
        until(self, "An import setting", lead=0.1)
        r4 = a8_lab("flat import key", -5.9, 0.175, 32, left=True)
        self.play(FadeIn(r4), run_time=0.35)
        until(self, "a key the importer ignores", lead=0.15)
        pg = RoundedRectangle(width=2.6, height=1.15, corner_radius=0.12, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([-1.0, 0.175, 0])
        bars = VGroup(*[Line([-2.0, 0.55 - 0.35 * k, 0], [-0.35 - 0.5 * (k % 2), 0.55 - 0.35 * k, 0], color=GHOST, stroke_width=9) for k in range(3)])
        ign = a8_no(1.1, 0.175, r=0.38)
        i_l = a8_lab("ignored", 2.3, 0.175, 32)
        self.play(Create(pg), Create(bars), run_time=0.4)
        self.play(Create(ign), FadeIn(i_l), run_time=0.35)
        # row 5: the flag no check asserted
        until(self, "A material with ambient", lead=0.1)
        r5 = a8_lab("never asserted", -5.9, -1.475, 32, left=True)
        self.play(FadeIn(r5), run_time=0.35)
        until(self, "a hundred checks", lead=0.35)
        grid = VGroup(*[a8_tick_small(-2.3 + 0.2 * c, -0.95 - 0.2 * r, s=0.06, color=DIM, w=3) for r in range(5) for c in range(20)])
        n100 = a8_lab("100", 2.3, -1.3, 44)
        self.play(LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.01), FadeIn(n100), run_time=0.8)
        tog = RoundedRectangle(width=0.84, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([0.45, -2.0, 0])
        knob = Circle(radius=0.13, fill_color=DIM, fill_opacity=1, stroke_width=0).move_to([0.25, -2.0, 0])
        ao = M("ao_enabled", 24).move_to([-2.3, -2.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(ao), Create(tog), FadeIn(knob), run_time=0.4)
        until(self, "Look every value up", lead=0.6)
        c3 = a8_lab("looking it up", 4.65, 1.85, 32)
        c4 = a8_lab("failing test", 4.65, 0.175, 32)
        c5 = a8_lab("a probe", 4.65, -1.475, 32)
        self.play(LaggedStart(FadeIn(c3), FadeIn(c4), FadeIn(c5), lag_ratio=0.3), run_time=0.7)
        done(self)


def a8_no(x, y, r=0.32, sw=7):
    """A prohibition mark (ink ring + bar), drawn BESIDE a picture, never over type."""
    ring_ = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring_, bar)
