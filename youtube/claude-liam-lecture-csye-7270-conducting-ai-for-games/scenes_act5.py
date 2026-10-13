"""ACT V · How the Course Works  (B30-B34, all Manim)

One cast for the act: THE DIRECTOR'S LINE. A terracotta dot (the baton) travels the act's pictures; the tools (Claude Code, Codex)
and the engine (Godot) are shown as their own marks, the game as a real recorded run, the log as the real FRICTIONAL.md text, and
the closing picture is the orchestra of B03 with its podium filled by a person (Professor Bear portrait, PROFESSOR BEAR LAW).

Pacing: a5_at() lands each motion on the real spoken time of a word (faster-whisper times, evidence/act5/word_times.json).
Real evidence only: the Godot page is the real capture (web-captures/godot-home.png, cropped); the game frames are the real
walker-claude run (scripted input, recorded 2026-10-09); the log lines are verbatim from walker-jumpman-clawd/FRICTIONAL.md
(trimmed only with a visible ellipsis; markdown bold marks removed because the page is shown rendered).
"""

A5P = "pantry/"


def a5_at(self, t):
    """Wait until the clip clock reaches t seconds (the real spoken time of a word, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def a5_lab(s, x, y, size=34, color=INK, bold=False):
    return T(s, size, color, bold).move_to([x, y, 0])


def a5_left(s, left, y, w, size=34, color=INK, bold=False):
    """A serif label whose LEFT edge sits at x = left; w = its width, MEASURED with real Manim (evidence/act5/widths.py)
    because Gate A's stub cannot measure text and layout rules forbid reading edges."""
    return T(s, size, color, bold).move_to([left + w / 2.0, y, 0])


def a5_mleft(s, left, y, size=32, color=INK):
    """Menlo line, left edge at x = left; Menlo 32 is 0.2492 units a character (measured)."""
    return M(s, size, color).move_to([left + 0.2492 * len(s) / 2.0, y, 0])


def a5_svg(name, h, x, y, color=INK):
    m = SVGMobject(A5P + name)
    m.set_fill(color, 1)
    m.set_stroke(color, 0)
    m.set_height(h)
    return m.move_to([x, y, 0])


def a5_img(name, w, x, y):
    im = ImageMobject(A5P + name)
    im.set_width(w)
    return im.move_to([x, y, 0])


def a5_frames(folder, n):
    try:
        from PIL import Image
        return [np.array(Image.open(f"{A5P}{folder}/f{i:03d}.png").convert("RGBA")) for i in range(1, n + 1)]
    except Exception:                      # Gate A's stub folder holds only scenes.py
        return [np.zeros((4, 4, 4), dtype=np.uint8)]


def a5_game_tick(m, dt):
    m.a5t += dt
    m.pixel_array = m.a5f[min(int(m.a5t * 12.0), len(m.a5f) - 1)]


def a5_game(w, x, y):
    """The real walker-claude run (scripted input, recorded 2026-10-09), 12 frames a second, played in real time."""
    fr = a5_frames("a5_game_frames", 50)
    g = ImageMobject(fr[0]).set_width(w).move_to([x, y, 0])
    g.a5f, g.a5t = fr, 0.0
    g.add_updater(a5_game_tick)
    return g


# ═════════════════════ B30 · direct Claude Code or Codex to build real games in Godot ═════════════════════
class B30_ToolsAndEngine(Scene):
    def construct(self):
        title = a5_lab("How the Course Works", -3.45, 2.85, 40)
        self.add(title)
        cc, ccl = a5_svg("a5_logo_claude-code.svg", 0.8, -5.45, 1.15), a5_left("Claude Code", -4.6, 1.15, 2.568, 38)
        cx, cxl = a5_svg("a5_logo_codex-openai.svg", 0.8, -5.45, -0.25), a5_left("Codex", -4.6, -0.25, 1.25, 38)
        arrow = Arrow([-1.7, 0.45, 0], [0.15, 0.45, 0], color=INK, stroke_width=6, buff=0, tip_length=0.28)
        godot = a5_img("a5_godot_home_top.png", 5.6, 3.2, 1.85)
        game = a5_game(4.6, 3.2, -0.95)
        cap = a5_left("scripted input, recorded 2026-10-09", 0.3, -2.75, 5.843, 32, DIM)
        a5_at(self, 2.15)
        self.play(FadeIn(cc), FadeIn(ccl), run_time=0.4)                       # "Claude Code"
        a5_at(self, 3.25)
        self.play(FadeIn(cx), FadeIn(cxl), run_time=0.4)                       # "Codex"
        a5_at(self, 3.7)
        self.play(GrowArrow(arrow), run_time=0.45)                              # "to build"
        a5_at(self, 4.3)
        self.add(game)
        self.play(FadeIn(game), FadeIn(cap), run_time=0.3)                      # "real games" (plays on)
        a5_at(self, 4.9)
        self.play(FadeIn(godot), run_time=0.4)                                  # "in Godot"
        done(self)


# ═════════════════════ B31 · brief, one change, predict, choose the check ═════════════════════
class B31_FourSteps(Scene):
    def construct(self):
        xs = [-4.65, -1.55, 1.55, 4.65]
        YN, YR, YP, YL, YC = 2.3, 1.7, 0.2, -1.2, -2.0          # numerals, rail, pictures, labels, captions
        rail = Line([-4.9, YR, 0], [4.9, YR, 0], color=DIM, stroke_width=4)
        nums = [a5_lab(str(i + 1), x, YN, 44) for i, x in enumerate(xs)]
        baton = Dot([xs[0], YR, 0], radius=0.14, color=TERRA)
        self.add(rail, *nums)
        # 1 brief: a page with ghost lines
        pg = Rectangle(width=1.5, height=1.95, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([xs[0], YP, 0])
        pl = VGroup(*[Line([xs[0] - 0.5, YP + dy, 0], [xs[0] + 0.5, YP + dy, 0], color=DIM, stroke_width=4) for dy in (0.5, 0.12, -0.26)])
        pd = Dot([xs[0] - 0.5, YP - 0.7, 0], radius=0.07, color=TERRA)
        l1, c1 = a5_lab("brief", xs[0], YL, 40), a5_lab("player: Clawd", xs[0], YC, 32, DIM)
        # 2 one change: the real starter level, its player (the thing the one change redraws)
        im = a5_img("a5_starter_jump_crop.png", 2.4, xs[1], YP)
        l2, c2 = a5_lab("one change", xs[1], YL, 40), a5_lab("redraw the player", xs[1], YC, 32, DIM)
        # 3 predict: three prediction cards
        cards = VGroup(*[Rectangle(width=0.85, height=1.2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([xs[2] + dx, YP, 0])
                         for dx in (-1.0, 0.0, 1.0)])
        cn = VGroup(*[a5_lab(str(i + 1), xs[2] + dx, YP, 40) for i, dx in enumerate((-1.0, 0.0, 1.0))])
        l3, c3 = a5_lab("predict", xs[2], YL, 40), a5_lab("3 ways it fails", xs[2], YC, 32, DIM)
        # 4 choose the check: a check in a grey ring
        ring = Circle(radius=0.95, stroke_color=DIM, stroke_width=6).move_to([xs[3], YP, 0])
        ck = check(xs[3] - 0.12, YP, 0.42, INK, 9)
        l4, c4 = a5_lab("check", xs[3], YL, 40), a5_lab("1,944 comparisons", xs[3], YC, 32, DIM)

        self.add(baton)
        a5_at(self, 0.15)
        self.play(Create(pg), Create(pl), FadeIn(pd), run_time=0.45)
        self.play(FadeIn(l1), FadeIn(c1), run_time=0.25)                         # "a brief"
        a5_at(self, 1.35)
        self.play(baton.animate.move_to([xs[1], YR, 0]), run_time=0.3)
        self.play(FadeIn(im), run_time=0.3)                                     # "one change"
        self.play(FadeIn(l2), FadeIn(c2), run_time=0.25)
        a5_at(self, 2.85)
        self.play(baton.animate.move_to([xs[2], YR, 0]), run_time=0.25)
        self.play(Create(cards), FadeIn(cn), run_time=0.4)                      # "predict"
        self.play(FadeIn(l3), FadeIn(c3), run_time=0.15)
        a5_at(self, 5.45)
        self.play(baton.animate.move_to([xs[3], YR, 0]), run_time=0.3)
        self.play(Create(ring), Create(ck), run_time=0.45)                      # "choose the check"
        self.play(FadeIn(l4), FadeIn(c4), run_time=0.25)
        done(self)


# ═════════════════════ B32 · the log: what the AI did, what you decided, what you doubted ═════════════════════
class B32_TheLog(Scene):
    def construct(self):
        fname = a5_mleft("FRICTIONAL.md", -6.0, 2.95, 32, DIM)
        page = Rectangle(width=12.0, height=4.5, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([0, 0.35, 0])
        head = a5_left("Frictional \u2014 an honest effort log", -5.6, 1.75, 7.258, 38, INK, True)
        rows = [("Human contribution: Bear chose \u2026", 0.65), ("AI contribution: inspected the \u2026", -0.35),
                ("Prediction: wide art may \u2026", -1.35)]
        lines = [a5_mleft(s, -3.55, y, 32) for s, y in rows]
        self.add(fname)
        a5_at(self, 0.3)
        self.play(Create(page), FadeIn(head), run_time=0.4)                      # "a log"
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.25), run_time=0.6)
        marks = [("did", rows[1][1], 0.571), ("decided", rows[0][1], 1.421), ("doubted", rows[2][1], 1.571)]
        dots = [Dot([-5.65, y, 0], radius=0.1, color=TERRA) for _, y, _w in marks]
        words = [a5_left(w, -5.4, y, ww, 34) for w, y, ww in marks]
        a5_at(self, 1.1)
        self.play(FadeIn(dots[0]), FadeIn(words[0]), run_time=0.2)               # "what the A.I. did"
        a5_at(self, 2.2)
        self.play(FadeIn(dots[1]), FadeIn(words[1]), run_time=0.2)               # "what you decided"
        a5_at(self, 2.8)
        self.play(FadeIn(dots[2]), FadeIn(words[2]), run_time=0.2)               # "what you doubted"
        brace = BraceBetweenPoints([-5.9, -2.0, 0], [5.9, -2.0, 0], direction=[0, -1, 0], color=DIM)
        ev = a5_lab("evidence of your work", 0, -2.85, 38)
        a5_at(self, 3.85)
        self.play(Create(brace), run_time=0.4)                                   # "That log"
        a5_at(self, 4.5)
        self.play(FadeIn(ev), run_time=0.3)                                      # "the evidence"
        done(self)


# ═════════════════════ B33 · the two next films ═════════════════════
class B33_TwoNextFilms(Scene):
    def construct(self):
        ca, cb, cy, W, H = -3.1, 3.1, 0.0, 5.6, 4.6
        gh = [DashedVMobject(Rectangle(width=W, height=H, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([x, cy, 0]), num_dashes=44)
              for x in (ca, cb)]
        sa = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([ca, cy, 0])
        sb = Rectangle(width=W, height=H, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([cb, cy, 0])
        fa, fb = a5_lab("Film 2 of 3", ca, 1.65, 34, DIM), a5_lab("Film 3 of 3", cb, 1.65, 34, DIM)
        ta = a5_lab("Why Godot", ca, 0.55, 56)
        tb1, tb2 = a5_lab("What Is Walker,", cb, 0.85, 50), a5_lab("and Why", cb, 0.1, 50)
        mk, ml = a5_svg("a5_logo_godot.svg", 0.85, ca - 1.0, -1.4), a5_left("the engine", ca - 0.35, -1.4, 1.865, 40)
        rl = VGroup(*[Line([cb - 1.6, -1.05 - 0.3 * i, 0], [cb - 0.6 - 0.2 * (i % 2), -1.05 - 0.3 * i, 0], color=DIM, stroke_width=5) for i in range(3)])
        rd = Dot([cb - 1.6, -1.05, 0], radius=0.08, color=TERRA)
        rt = a5_left("the rules", cb - 0.3, -1.4, 1.528, 40)
        a5_at(self, 0.35)
        self.play(Create(gh[0]), Create(gh[1]), run_time=0.5)                    # "Two more films"
        a5_at(self, 1.35)
        self.play(Create(sa), FadeIn(fa), FadeIn(ta), run_time=0.4)              # "Why Godot"
        self.play(FadeIn(mk), FadeIn(ml), run_time=0.25)
        a5_at(self, 2.5)
        self.play(Create(sb), FadeIn(fb), FadeIn(tb1), FadeIn(tb2), run_time=0.4)   # "what Walker is"
        a5_at(self, 3.4)
        self.play(Create(rl), FadeIn(rd), FadeIn(rt), run_time=0.9)               # "the rules"
        a5_at(self, 4.6)
        self.play(rd.animate.move_to([cb - 1.6, -1.05 - 0.6, 0]), run_time=0.5)  # "works under"
        done(self)


# ═════════════════════ B34 · the baton: conducting it ═════════════════════
class B34_TheBaton(Scene):
    def construct(self):
        iso = Iso(0.0, -2.3, 0.7)
        S_TOP, S_L, S_R = BAR2, BAR1, DIM
        podium = iso.box(-0.6, -0.6, 0, 1.2, 1.2, 0.55, BOX_TOP, BOX_L, BOX_R)
        lights, players = [], []
        for d, js in ((6.5, (-2, -1, 0, 1, 2)), (5.0, (-1.5, -0.5, 0.5, 1.5)), (3.6, (-2, -1, 0, 1, 2))):
            for j in js:
                X, Y = d + j, d - j
                players.append(iso.box(X - 0.4, Y - 0.4, 0, 0.8, 0.8, 0.5, S_TOP, S_L, S_R))
                lights.append(Dot(iso.p(X, Y, 0.95), radius=0.12, color=GHOST))
        ai = a5_lab("A.I.", -4.7, 0.9, 40)
        self.add(podium)
        a5_at(self, 0.1)
        self.play(LaggedStart(*[FadeIn(p) for p in players], lag_ratio=0.05), run_time=0.9)
        self.play(FadeIn(VGroup(*lights)), FadeIn(ai), run_time=0.3)              # "an A.I."
        a5_at(self, 1.45)
        self.play(LaggedStart(*[d.animate.set_color(TERRA) for d in lights], lag_ratio=0.06), run_time=0.8)   # "write code"
        pb = ImageMobject(A5P + "a5_pb_circle_04.png").set_height(1.5).move_to([0, 1.9, 0])
        pbl = a5_left("Professor Bear", -4.6, -1.5, 2.644, 34)
        hand = np.array([0.85, -1.35, 0.0])
        baton = VGroup(Line(hand, hand + np.array([0.95, 0.75, 0.0]), color=INK, stroke_width=6),
                       Dot(hand + np.array([0.95, 0.75, 0.0]), radius=0.1, color=TERRA))
        cond = a5_left("conducting", 2.9, -0.4, 2.598, 44)
        a5_at(self, 2.55)
        self.add(pb)
        self.play(pb.animate.move_to([0, -1.1, 0]), rate_func=ease_in, run_time=0.45)    # "this course is about"
        self.play(FadeIn(pbl), Create(baton), run_time=0.3)
        a5_at(self, 3.25)
        self.play(FadeIn(cond), run_time=0.2)                                     # "conducting"
        self.play(Rotate(baton, 0.45, about_point=hand), run_time=0.25)
        self.play(Rotate(baton, -0.9, about_point=hand), run_time=0.4)
        self.play(Rotate(baton, 0.45, about_point=hand), run_time=0.25)
        done(self)
