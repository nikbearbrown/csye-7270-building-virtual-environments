"""ACT V · Why It Fits, and What This Proves  (B25-B27, all Manim)

One cast for the act: THE THREE EXHIBITS (B25) and THE TABLE (B26) and THE TWO EMPTY CELLS (B27) - one grid language: outline-only
cells in grey, real text in Menlo, labels in EB Garamond, a terracotta dot as the only accent.
B25 shows three REAL exhibits from the earlier acts: the real scene text (godot-evidence/part2/pong.tscn.after), the real command and its
real exit line (part2/independent-checks.txt section 4), and the real download button on godotengine.org (web-captures, cropped).
B26 is a dated table; every cell is traceable in factcheck/act5.md. B27 draws what is NOT shown, as empty cells.
"""

A5P = "pantry/"


def a5_at(self, t):
    """Wait until the clip clock reaches t seconds (word times measured from mp3/beat-<ID>.mp3 with faster-whisper base.en)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a5_lab(s, x, y, size=36, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a5_left(s, x, y, size=36, color=INK):
    """A label whose LEFT edge sits at x (explicit coordinates, never get_left)."""
    t = T(s, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


def a5_mleft(s, x, y, size=32, color=INK):
    t = M(s, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


def a5_slot(cx, cy, w, h, color=DIM, sw=4):
    """An empty slot: dashed outline, no fill."""
    return DashedVMobject(RoundedRectangle(width=w, height=h, corner_radius=0.12).move_to([cx, cy, 0]),
                          num_dashes=44).set_stroke(color, sw)


def a5_cell(cx, cy, w, h, color=DIM, sw=3):
    return Rectangle(width=w, height=h, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([cx, cy, 0])


def a5_cross(x, y, s=0.17, color=INK, w=7):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w))


# ── B25 · three properties as three real exhibits: plain text / command line / no account ─────────────────────────────
class B25_WhyItFits(Scene):
    def construct(self):
        title = T("Why It Fits, and What This Proves", 40)
        title.move_to([-6.0 + title.width / 2, 2.95, 0])
        self.add(title)
        ys = [1.4, -0.5, -2.4]
        BX, BW, BH = -1.8, 8.6, 1.6                       # exhibit slots: x from -6.1 to 2.5
        slots = [a5_slot(BX, y, BW, BH) for y in ys]
        a5_at(self, 1.6)                                           # "not because it has the best A. I. features": three empty places
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.3), run_time=1.2)       # three empty places to fill
        ptr = Dot([2.8, ys[0], 0], radius=0.1, color=TERRA)
        # 1 - plain text: the real scene text of the Pong game, typed in
        a5_at(self, 4.45)                                          # "everything you need to inspect"
        l1 = a5_mleft('[node name="HelloLabel" …', -5.8, ys[0] + 0.33)
        l2 = a5_mleft('text = "Hello from a text file"', -5.8, ys[0] - 0.33)
        lab1 = a5_left("plain text", 3.1, ys[0], 40)
        self.play(FadeOut(slots[0]), FadeIn(ptr), run_time=0.25)
        box1 = a5_cell(BX, ys[0], BW, BH)
        self.play(Create(box1), AddTextLetterByLetter(l1, time_per_char=0.015), FadeIn(lab1), run_time=0.45)
        self.play(AddTextLetterByLetter(l2, time_per_char=0.015), run_time=0.45)
        # (midpoint: title, the scene text with its label, two empty slots waiting)
        # 2 - command line: the real command and its real exit line
        a5_at(self, 6.95)                                          # "everything you need to run"
        c1 = a5_mleft("$ godot --headless …", -5.8, ys[1] + 0.47)
        c1b = a5_mleft("… --quit-after 60", -5.8, ys[1])
        c2 = a5_mleft("exit=0  wall=0.56s", -5.8, ys[1] - 0.47)
        lab2 = a5_left("command line", 3.1, ys[1], 40)
        box2 = a5_cell(BX, ys[1], BW, BH)
        self.play(FadeOut(slots[1]), ptr.animate.move_to([2.8, ys[1], 0]), run_time=0.35)
        self.play(Create(box2), AddTextLetterByLetter(c1, time_per_char=0.03), run_time=0.6)
        self.play(AddTextLetterByLetter(c1b, time_per_char=0.03), run_time=0.5)
        self.play(AddTextLetterByLetter(c2, time_per_char=0.04), FadeIn(lab2), run_time=0.6)
        # 3 - no account: the real download button
        a5_at(self, 9.3)                                           # "nothing sits behind an account"
        btn = ImageMobject(A5P + "a5_download_button_r.png").set_width(4.4).move_to([BX, ys[2], 0])
        lab3 = a5_left("no account", 3.1, ys[2], 40)
        self.play(FadeOut(slots[2]), ptr.animate.move_to([2.8, ys[2], 0]), FadeIn(btn, scale=0.96), FadeIn(lab3), run_time=0.7)
        done(self)


# ── B26 · a dated snapshot: the table, 9 October 2026 ─────────────────────────────────────────────────────────────────
A5_COLX = [-1.775, 1.375, 4.525]                            # Godot, Unity, Unreal column centres (each 3.15 wide)
A5_ROWY = [0.5, -0.7, -1.9]                                 # scene files, official MCP, licence (each 1.2 tall)


class B26_Snapshot(Scene):
    def construct(self):
        # the grid draws while the voice says "Unity is close on text"
        heads = [a5_lab(n, x, 1.75, 38) for n, x in zip(["Godot", "Unity", "Unreal"], A5_COLX)]
        rows = [a5_left(n, -6.0, y, 34) for n, y in zip(["scene files", "official MCP", "licence"], A5_ROWY)]
        cells = [[a5_cell(x, y, 3.15, 1.2) for x in A5_COLX] for y in A5_ROWY]
        self.play(FadeIn(VGroup(*heads)), FadeIn(VGroup(*rows)),
                  LaggedStart(*[Create(c) for c in cells[0]], lag_ratio=0.2), run_time=0.9)
        # row 1: text / text (YAML) / binary
        g = a5_lab("text", A5_COLX[0] + 0.3, A5_ROWY[0], 32)
        u = a5_lab("text (YAML)", A5_COLX[1] + 0.3, A5_ROWY[0], 32)
        r = a5_lab("binary", A5_COLX[2] + 0.3, A5_ROWY[0], 32)
        a5_at(self, 0.9)                                           # "Unity is close on text"
        self.play(FadeIn(g), Create(check(A5_COLX[0] - 1.2, A5_ROWY[0], s=0.15, w=6)),
                  FadeIn(u), Create(check(A5_COLX[1] - 1.2, A5_ROWY[0], s=0.15, w=6)), run_time=0.7)
        a5_at(self, 1.7)                                           # "Unreal is furthest"
        self.play(FadeIn(r), Create(a5_cross(A5_COLX[2] - 1.2, A5_ROWY[0], s=0.13, w=6)), run_time=0.5)
        # row 2: the official MCP: none / open beta / Experimental (their own labels: features may change)
        a5_at(self, 2.85)                                          # "and both say their features may change"
        self.play(*[Create(c) for c in cells[1]], run_time=0.5)
        m_g = a5_lab("none", A5_COLX[0], A5_ROWY[1], 34)
        m_u = a5_lab("open beta", A5_COLX[1], A5_ROWY[1], 34)
        m_r = a5_lab("Experimental", A5_COLX[2], A5_ROWY[1], 34)
        self.play(FadeIn(m_g), FadeIn(m_u), FadeIn(m_r), run_time=0.5)
        # row 3: licence
        self.play(*[Create(c) for c in cells[2]], run_time=0.4)
        l_g = a5_lab("MIT", A5_COLX[0], A5_ROWY[2], 34)
        l_u = a5_lab("proprietary", A5_COLX[1], A5_ROWY[2], 34)
        l_r = a5_lab("proprietary", A5_COLX[2], A5_ROWY[2], 34)
        self.play(FadeIn(l_g), FadeIn(l_u), FadeIn(l_r), run_time=0.4)
        # (midpoint: the whole table, filled)
        # the date: stamped on "the ninth of October"
        a5_at(self, 6.05)                                          # "the ninth of October"
        stamp = RoundedRectangle(width=3.8, height=0.85, corner_radius=0.12, stroke_color=DIM, stroke_width=5, fill_opacity=0
                                 ).move_to([4.2, 2.95, 0])
        date = a5_lab("9 October 2026", 4.2, 2.95, 36)
        dot = Dot([2.05, 2.95, 0], radius=0.1, color=TERRA)
        self.play(Create(stamp), FadeIn(date, scale=1.15), GrowFromCenter(dot), run_time=0.6)
        # check again: a circular arrow draws round
        a5_at(self, 8.25)                                          # "Check it again"
        arc = Arc(radius=0.34, start_angle=0.5, angle=4.9, stroke_color=INK, stroke_width=6).move_to([-1.3, -2.95, 0])
        tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-2.2).move_to([-1.05, -2.74, 0])
        again = a5_left("check again before you rely on it", -0.7, -2.95, 34)
        self.play(Create(arc), FadeIn(tip), FadeIn(again), run_time=0.7)
        done(self)


# ── B27 · what this film does not show: two empty cells, yours to test ────────────────────────────────────────────────
class B27_NotShown(Scene):
    def construct(self):
        CX = [-3.1, 3.1]
        w1 = a5_lab("better games?", CX[0], 1.75, 38)
        w2 = a5_lab("large, complicated scenes?", CX[1], 1.75, 38)
        c1 = a5_slot(CX[0], -0.35, 5.6, 3.0)
        c2 = a5_slot(CX[1], -0.35, 5.6, 3.0)
        a5_at(self, 1.45)                                          # "that Godot makes better games"
        self.play(FadeIn(w1), Create(c1), run_time=0.7)
        a5_at(self, 3.15)                                          # "or that an agent handles large, complicated scenes"
        self.play(FadeIn(w2), Create(c2), run_time=0.7)
        # (midpoint: two labelled empty cells)
        a5_at(self, 6.95)                                          # "Those are for you to test"
        k1, k2 = cursor(CX[0] - 0.9, -0.15), cursor(CX[1] - 0.9, -0.15)
        d1, d2 = Dot([CX[0] + 0.45, -0.55, 0], radius=0.1, color=TERRA), Dot([CX[1] + 0.45, -0.55, 0], radius=0.1, color=TERRA)
        you = a5_lab("yours to test", 0.0, -2.75, 40)
        self.play(FadeIn(k1, shift=UP * 0.3), FadeIn(k2, shift=UP * 0.3), run_time=0.4)
        self.play(GrowFromCenter(d1), GrowFromCenter(d2), FadeIn(you), run_time=0.4)
        done(self)
