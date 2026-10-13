"""ACT III · A Real Record  (B16–B22, all Manim)  — "Conducting AI for Games"

One cast for the act: THE GAME WINDOW (a real Godot capture in a thin grey frame, the cream stage around it) and THE RECORD (the
project's own words and receipt names, set as text). Nothing is redrawn: the pictures of the game are the walker-jumpman starter's own
rendered screenshots (pantry/a3_starter_*.png) and Godot 4.7.2 captures of Clawd in the same level (pantry/a3_clawd_jump.png,
pantry/a3_edgeb_*.png, built by evidence/act3/make_assets_act3.py). The drawings (the 25 checks, the gate, the three predictions, the
changed / left-alone ledger) show an IDEA and carry only names and numbers that are in the record (factcheck/act3.md).

GATE T notes (measured at real 4K, evidence/act3/gates_act3.py): dark game art (the navy ground strip, dark blocks) and the flat
terracotta-ish mascot read as "text" to GATE T, so every real capture is cropped to the part the sentence names, kept small enough
not to fuse with text, and the 50% frame is always a settled still.
"""

A3P = "pantry/"


def a3_at(self, t):
    """Wait until the clip clock reaches t seconds (a real spoken time, from evidence/act3/word_times.json, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a3_t(s, x, y, size=34, color=INK):
    return T(s, size, color).move_to([x, y, 0])


def a3_m(s, x, y, size=32, color=INK):
    """Menlo text with its LEFT edge at x (explicit coordinates, no get_left)."""
    return M(s, size, color).move_to([x, y, 0], aligned_edge=LEFT)


def a3_img(name, w, x, y):
    im = ImageMobject(A3P + name)
    im.set_width(w)
    im.move_to([x, y, 0])
    return im


def a3_frame(w, h, x, y, color=DIM, sw=4):
    """A thin outline just outside a captured picture (never touching its pixels)."""
    return Rectangle(width=w + 0.2, height=h + 0.2, stroke_color=color, stroke_width=sw, fill_opacity=0).move_to([x, y, 0])


def a3_card(w, h, x, y, color=DIM, sw=4):
    return RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=color, stroke_width=sw,
                            fill_opacity=0).move_to([x, y, 0])


def a3_x(x, y, s=0.12, color=INK, w=8):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a3_equal(x, y, s=0.16, color=INK, w=6):
    return VGroup(Line([x - s, y + 0.07, 0], [x + s, y + 0.07, 0], color=color, stroke_width=w),
                  Line([x - s, y - 0.07, 0], [x + s, y - 0.07, 0], color=color, stroke_width=w))


# ───────────────────────── B16 · the request ─────────────────────────
class B16_OneRequest(Scene):
    def construct(self):
        title = a3_t("A Real Record", -4.55, 3.0, 40)          # the act title is the first picture's label
        self.add(title)
        win = a3_img("a3_starter_jump_full.png", 6.9, -2.65, -0.3)
        fr = a3_frame(6.9, 3.88, -2.65, -0.3)
        game_lab = a3_t("Walker Jumpman", -2.65, -2.85, 34)
        card = a3_card(4.3, 2.3, 4.05, 0.2)
        cap = a3_t("the one request", 4.05, 1.85, 34)
        q = VGroup(a3_t("Build a simple level", 4.05, 0.6, 36), a3_t("for walker-jumpman.", 4.05, -0.1, 36))
        date = a3_t("September 10, 2026", 4.05, -1.3, 32)
        arrow = Arrow([1.75, 0.2, 0], [1.0, 0.2, 0], buff=0, color=INK, stroke_width=6, tip_length=0.2)
        a3_at(self, 2.0)                                        # "a small platformer"
        self.play(Create(fr), FadeIn(win), run_time=0.7)
        a3_at(self, 3.25)                                       # "called Walker Jumpman"
        self.play(FadeIn(game_lab), run_time=0.4)
        a3_at(self, 6.3)                                        # "from one request"
        self.play(Create(card), FadeIn(cap), run_time=0.5)
        a3_at(self, 6.9)                                        # "build a simple level"
        self.play(Write(q, run_time=1.2))
        self.play(Create(arrow), run_time=0.4)
        self.play(FadeIn(date), run_time=0.4)
        done(self)


# ───────────────────────── B17 · 25 checks, 4 failed, 25 passed ─────────────────────────
A3_FAILED = [(18, "respawn"), (19, "manual-restart-not-death"), (20, "twenty-retries"), (23, "complete-real-route")]


def a3_pos(cx, cy, i, pitch=0.5):
    return [cx + (i % 5 - 2) * pitch, cy - (i // 5 - 2) * pitch]


def a3_grid(cx, cy, pitch=0.5, cell=0.4):
    return VGroup(*[Square(side_length=cell, stroke_color=DIM, stroke_width=3)
                    .move_to([cx + (c - 2) * pitch, cy - (r - 2) * pitch, 0]) for r in range(5) for c in range(5)])


class B17_TwentyFiveChecks(Scene):
    def construct(self):
        g1x, g2x, gy = -4.85, 4.85, -0.35
        g1, g2 = a3_grid(g1x, gy), a3_grid(g2x, gy)
        cap1, cap2 = a3_t("first run", g1x, 1.4, 36), a3_t("next run", g2x, 1.4, 36)
        res1, res2 = a3_t("4 failed", g1x, -2.15, 40), a3_t("25 passed", g2x, -2.15, 40)
        fails = [i for i, _ in A3_FAILED]

        def mark_pass(cx, skip=()):
            return VGroup(*[check(a3_pos(cx, gy, i)[0], a3_pos(cx, gy, i)[1] - 0.02, s=0.11, color=DIM, w=5)
                            for i in range(25) if i not in skip])

        a3_at(self, 0.1)                                        # "Its first run of 25 checks"
        self.play(FadeIn(cap1), Create(g1, lag_ratio=0.04), run_time=1.0)
        a3_at(self, 1.5)
        p1 = mark_pass(g1x, fails)
        self.play(Create(p1, lag_ratio=0.03), run_time=0.7)
        xs = VGroup(*[a3_x(a3_pos(g1x, gy, i)[0], a3_pos(g1x, gy, i)[1]) for i in fails])
        a3_at(self, 2.2)                                        # "failed four"
        self.play(Create(xs), FadeIn(res1), run_time=0.5)
        # the four failing cells step out into a list of their real receipt names
        rows = [0.7, 0.05, -0.6, -1.25]
        chips, names = [], []
        for k, (i, nm) in enumerate(A3_FAILED):
            chip = VGroup(Square(side_length=0.34, stroke_color=INK, stroke_width=4).move_to([-3.2, rows[k], 0]),
                          a3_x(-3.2, rows[k], s=0.1, w=6))
            chips.append(chip)
            names.append(a3_m(nm, -2.75, rows[k]))
        a3_at(self, 3.1)                                        # "Dead on respawn"
        self.play(FadeIn(chips[0]), Write(names[0]), run_time=0.6)
        a3_at(self, 4.35)                                       # "Restart counted as a death"
        self.play(FadeIn(chips[1]), Write(names[1]), FadeIn(chips[2]), Write(names[2]), run_time=0.7)
        a3_at(self, 5.95)                                       # "A route with no safe landing"
        self.play(FadeIn(chips[3]), Write(names[3]), run_time=0.7)
        a3_at(self, 8.9)                                        # "the next run passed all twenty-five"
        self.play(FadeIn(cap2), Create(g2, lag_ratio=0.04), run_time=0.9)
        p2 = mark_pass(g2x)
        a3_at(self, 9.9)
        self.play(Create(p2, lag_ratio=0.03), FadeIn(res2), run_time=0.8)
        a3_at(self, 10.95)                                      # "seventy-one seconds later"
        dim = dim_arrow([g1x, 2.25, 0], [g2x, 2.25, 0], color=INK, w=5)
        lab = a3_t("71 s", 0.0, 2.75, 44)
        self.play(Create(dim), FadeIn(lab), run_time=0.8)
        done(self)


# ───────────────────────── B18 · the test stayed hard ─────────────────────────
class B18_TestStayedHard(Scene):
    def construct(self):
        page = a3_card(9.4, 2.0, 0.0, 2.0)
        line1 = a3_t("The jump tuning and acceptance tolerances", 0.0, 2.35, 38)
        line2 = a3_t("were not weakened.", 0.0, 1.65, 38)
        src = a3_m("BUILD-REPORT.md", -4.7, 0.65)
        # the gate: a fixed bar and two posts; the game is a box that has to clear it
        bar = Line([-3.8, -1.5, 0], [3.8, -1.5, 0], color=DIM, stroke_width=14)
        posts = VGroup(Line([-3.8, -2.15, 0], [-3.8, -0.85, 0], color=DIM, stroke_width=9),
                       Line([3.8, -2.15, 0], [3.8, -0.85, 0], color=DIM, stroke_width=9))
        test_lab = a3_t("the test", 5.3, -1.5, 38)
        box = Rectangle(width=1.7, height=1.0, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([0, -2.75, 0])
        game_lab = a3_t("the game", -2.7, -2.75, 38)
        game_lab2 = a3_t("the game", -2.7, -0.4, 38)
        a3_at(self, 0.2)                                        # "Look at how the record says it did it"
        self.play(Create(bar), Create(posts), FadeIn(test_lab), run_time=0.7)
        self.play(FadeIn(box), FadeIn(game_lab), run_time=0.5)
        a3_at(self, 1.85)                                       # "The jump tuning and acceptance tolerances were not weakened"
        self.play(Create(page), run_time=0.5)
        self.play(Write(VGroup(line1, line2)), FadeIn(src), run_time=1.5)
        a3_at(self, 5.1)                                        # "The test stayed hard"
        self.play(bar.animate.set_color(INK), run_time=0.5)
        a3_at(self, 6.4)                                        # "the game changed"
        self.play(box.animate.move_to([0, -0.4, 0]), FadeOut(game_lab), run_time=0.9)
        tick = check(1.6, -0.45, s=0.22, color=INK, w=9)
        self.play(Create(tick), FadeIn(game_lab2), run_time=0.5)
        done(self)


# ───────────────────────── B19 · one change: Clawd ─────────────────────────
class B19_OneChange(Scene):
    def construct(self):
        w, h = 5.7, 2.27
        a_img = a3_img("a3_starter_jump.png", w, -3.15, 1.2)
        a_fr = a3_frame(w, h, -3.15, 1.2)
        b_img = a3_img("a3_clawd_jump.png", w, 3.15, 1.2)
        b_fr = a3_frame(w, h, 3.15, 1.2)
        a_lab = a3_t("Walker Jumpman", -3.15, -0.45, 36)
        b_lab = a3_t("Clawd", 3.15, -0.45, 36)
        arrow = Arrow([-1.2, -0.45, 0], [2.0, -0.45, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        q1 = a3_t("“… the player to be a coding agent, represented by Clawd.”", 0.0, -1.55, 38)
        q2 = a3_t("“Clawd first, one change at a time”", 0.0, -1.55, 38)
        src = a3_m("CHANGE-BRIEF.md", -1.9, -2.5)
        self.add(a_fr, a_img, a_lab)
        a3_at(self, 1.9)                                        # "wanted the player to be a coding agent"
        self.play(FadeIn(q1), FadeIn(src), run_time=0.5)
        a3_at(self, 4.3)                                        # "the Claude mascot": Clawd lands after the 50% frame (GATE T trap)
        self.play(Create(b_fr), FadeIn(b_img), FadeIn(b_lab), run_time=0.6)
        self.play(Create(arrow), run_time=0.3)
        a3_at(self, 5.85)                                       # "One change."
        self.play(FadeOut(q1), run_time=0.3)
        self.play(FadeIn(q2), run_time=0.5)
        done(self)


# ───────────────────────── B20 · three predictions, three cards ─────────────────────────
A3_CX = [-4.2, 0.0, 4.2]


def a3_pred_card(x):
    return a3_card(3.8, 4.5, x, -0.35)


def a3_art_rects(ox, oy, u, color=DIM, sw=4):
    """Clawd's real rects (torso 96x60, arms 20x20 at -20/96, legs 11x26 at 11/32/64/85), outline only, feet at oy, centre ox."""
    R = [(0, 0, 96, 60), (-20, 20, 20, 20), (96, 20, 20, 20), (11, 60, 11, 26), (32, 60, 11, 26), (64, 60, 11, 26), (85, 60, 11, 26)]
    return VGroup(*[Rectangle(width=w * u, height=h * u, stroke_color=color, stroke_width=sw, fill_opacity=0)
                    .move_to([ox + (x + w / 2 - 48) * u, oy + (86 - y - h / 2) * u, 0]) for x, y, w, h in R])


class B20_ThreePredictions(Scene):
    def construct(self):
        head = a3_t("Predict", -5.3, 2.95, 40)
        src = a3_m("CHANGE-BRIEF.md", 2.3, 2.95)
        self.add(head, src)
        c1, c2, c3 = [a3_pred_card(x) for x in A3_CX]
        n1, n2, n3 = [a3_t(s, x - 1.45, 1.6, 40) for s, x in zip("123", A3_CX)]
        l1 = a3_t("overhangs the box", A3_CX[0], -2.0, 34)
        l2 = a3_t("two jump arcs", A3_CX[1], -2.0, 34)
        l3 = a3_t("mistaken for abilities", A3_CX[2], -2.0, 32)
        # 1: the art (136 units wide) against the unchanged 18 x 28 collider (the game's pixels; the art is drawn at 0.32 of its units)
        u = 0.021
        feet = -1.35
        art = a3_art_rects(A3_CX[0], feet, u)
        collider = Rectangle(width=56.25 * u, height=87.5 * u, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to(
            [A3_CX[0], feet + 87.5 * u / 2, 0])
        # 2: two arcs stacked on one jump
        ground = Line([A3_CX[1] - 1.5, feet, 0], [A3_CX[1] + 1.5, feet, 0], color=DIM, stroke_width=6)
        arc1 = ArcBetweenPoints([A3_CX[1] - 1.4, feet, 0], [A3_CX[1] + 1.4, feet, 0], angle=-PI * 0.55, color=DIM, stroke_width=8)
        arc2 = ArcBetweenPoints([A3_CX[1] - 0.9, feet + 0.62, 0], [A3_CX[1] + 0.9, feet + 0.62, 0], angle=-PI * 0.7, color=INK, stroke_width=8)
        # 3: eighteen small squares, 3 rows x 6
        sq = VGroup(*[Square(side_length=0.42, stroke_color=DIM, stroke_width=4).move_to(
            [A3_CX[2] + (c - 2.5) * 0.56, 0.35 - r * 0.62, 0]) for r in range(3) for c in range(6)])
        a3_at(self, 2.0)                                        # "three ways it could go wrong"
        self.play(Create(c1), FadeIn(n1), run_time=0.4)
        self.play(Create(c2), FadeIn(n2), run_time=0.4)
        self.play(Create(c3), FadeIn(n3), run_time=0.4)
        a3_at(self, 3.7)                                       # "The wide body might overhang the collision box"
        self.play(Create(art), Create(collider), run_time=0.9)
        a3_at(self, 4.9)
        self.play(FadeIn(l1), run_time=0.4)
        a3_at(self, 6.35)                                        # "A jump animation on a jumping body"
        self.play(Create(ground), Create(arc1), run_time=0.6)
        a3_at(self, 8.55)                                        # "might make two jump arcs"
        self.play(Create(arc2), FadeIn(l2), run_time=0.6)
        a3_at(self, 9.85)                                       # "And eighteen animations"
        self.play(Create(sq, lag_ratio=0.06), run_time=1.0)
        a3_at(self, 11.2)                                      # "mistaken for eighteen abilities"
        self.play(FadeIn(l3), run_time=0.5)
        done(self)


# ───────────────────────── B21 · drawing changed, the rest left alone, 1,944 compared ─────────────────────────
class B21_DrawingOnly(Scene):
    def construct(self):
        h_a, h_b = a3_t("changed", -4.9, 2.7, 40), a3_t("left alone", 0.35, 2.7, 40)
        r_a = [a3_m("clawd_art.gd", -6.1, 1.7, 36), a3_m("player.gd", -6.1, 0.9, 36)]
        r_b = [a3_m("_physics_process()", -1.5, 1.7, 36), a3_m("tuning.gd", -1.5, 0.9, 36), a3_m("first_steps.json", -1.5, 0.1, 36)]
        divider = Line([-2.2, 3.1, 0], [-2.2, -0.3, 0], color=DIM, stroke_width=5)
        hero = a3_t("1,944", -3.5, -1.85, 100)
        lab = VGroup(a3_t("numbers compared with", 2.6, -1.55, 38), a3_t("an independent reference", 2.6, -2.2, 38))
        sep = Line([-6.1, -0.7, 0], [6.1, -0.7, 0], color=GHOST, stroke_width=4)
        self.add(sep)
        a3_at(self, 0.15)                                       # "Then it changed the drawing and the animation choice only"
        self.play(FadeIn(h_a), run_time=0.3)
        a3_at(self, 0.65)                                       # "the drawing"
        self.play(Write(r_a[0]), run_time=0.5)
        a3_at(self, 1.3)                                        # "the animation choice"
        self.play(Write(r_a[1]), run_time=0.5)
        a3_at(self, 2.95)                                       # "The physics"
        self.play(Create(divider), FadeIn(h_b), Write(r_b[0]), run_time=0.7)
        a3_at(self, 3.75)                                       # "the tuning"
        self.play(Write(r_b[1]), run_time=0.5)
        a3_at(self, 4.45)                                       # "the level and the hazards"
        self.play(Write(r_b[2]), run_time=0.6)
        a3_at(self, 7.1)                                        # "A separate test compared"
        self.play(FadeIn(lab), run_time=0.5)
        a3_at(self, 8.0)                                        # "1,944"
        self.play(FadeIn(hero), run_time=0.5)
        done(self)


# ───────────────────────── B22 · the arms past the left edge ─────────────────────────
A3_EDGE = list(range(46, 62))


class B22_ArmsPastTheEdge(Scene):
    def construct(self):
        wx, wy, ww = -2.2, -0.2, 7.6
        wh = ww * 620 / 1500
        fr = a3_frame(ww, wh, wx, wy)
        first = a3_img("a3_edgeb_046.png", ww, wx, wy)
        cap = a3_t("scripted input, slow motion", wx, wy - 2.2, 32)
        # prediction 1, the card from before, now ticked
        card = a3_card(3.8, 1.6, 4.2, 1.5)
        n1 = a3_t("1", 2.65, 1.5, 40)
        l1 = a3_t("overhangs", 3.95, 1.8, 34)
        l1b = a3_t("the box", 3.95, 1.2, 34)
        tick = check(5.45, 1.55, s=0.2, color=INK, w=8)
        ring = Circle(radius=0.3, stroke_color=INK, stroke_width=6).move_to([2.75, -0.9, 0])
        open_lab = a3_t("left open", 4.35, -0.9, 38)
        edge = Line([wx - ww / 2 - 0.1, wy - wh / 2 - 0.1, 0], [wx - ww / 2 - 0.1, wy + wh / 2 + 0.1, 0], color=INK, stroke_width=10)
        edge_lab = a3_t("left edge of the world", -4.1, 2.4, 34)
        edge_arrow = Arrow([-5.6, 2.0, 0], [-6.0, 1.45, 0], buff=0, color=INK, stroke_width=5, tip_length=0.18)
        self.add(fr, first)
        a3_at(self, 0.1)                                        # "The first prediction"
        self.play(FadeIn(card), FadeIn(n1), FadeIn(l1), FadeIn(l1b), run_time=0.4)
        a3_at(self, 0.7)                                        # "came true"
        self.play(Create(tick), run_time=0.3)
        a3_at(self, 0.95)
        self.add(cap)
        prev = first
        for n in A3_EDGE[1:]:                                   # the real frames, each held two render frames (slow motion)
            nxt = a3_img(f"a3_edgeb_{n:03d}.png", ww, wx, wy)
            self.remove(prev)
            self.add(nxt)
            prev = nxt
            self.wait(0.0834)
        a3_at(self, 2.4)                                        # "past the left edge of the world"
        self.play(Create(edge), FadeIn(edge_lab), Create(edge_arrow), run_time=0.7)
        a3_at(self, 5.6)                                        # "It leaves it open"
        self.play(Create(ring), FadeIn(open_lab), run_time=0.6)
        done(self)
