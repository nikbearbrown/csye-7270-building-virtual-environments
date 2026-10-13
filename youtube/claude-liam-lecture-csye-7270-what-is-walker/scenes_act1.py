"""ACT I · The Problem Walker Answers  (B01-B04, all Manim)

One cast for the act: REAL FILES shown as themselves. The public repo page (B01, a real capture), then the real lines of real
files (legacy/README.md, legacy/AGENTS.md, LICENSE.md, CHANGELOG.md, publish.sh) set in Menlo and quoted with their file and
line (every quote is under 15 words). Drawings only carry ideas (the cost bars, the membrane); the bars are labelled as an
illustration. Nothing is invented: see factcheck/act1.md.

GATE T notes (measured at real 4K, see evidence/act1/gates_act1.py): the capture is zoomed so its type clears the 41 px floor;
ink-coloured outlines never touch a label; the terracotta pointer is always a DOT.
Pacing: until() lands each motion on the spoken word (character share of the measured audio).
"""

A1P = "pantry/"
A1_MW = 0.2459            # Menlo width per character at size 32 (units); scales with size/32


def a1_at(self, t):
    """Wait until the clip clock reaches t seconds (a real spoken time from evidence/act1/word_times.json, minus a small lead)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a1_ml(s, xl, y, size=32, color=INK):
    """Menlo text whose LEFT edge sits at xl (explicit arithmetic: no get_left())."""
    return M(s, size, color).move_to([xl + len(s) * A1_MW * size / 32.0 / 2.0, y, 0])


def a1_mr(s, xr, y, size=32, color=INK):
    """Menlo text whose RIGHT edge sits at xr."""
    return M(s, size, color).move_to([xr - len(s) * A1_MW * size / 32.0 / 2.0, y, 0])


def a1_no(x, y, r=0.27, sw=6):
    """A prohibition mark: ring + bar, drawn BESIDE its label, never around it."""
    ring = Circle(radius=r, stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    d = r * 0.7071
    bar = Line([x - d, y + d, 0], [x + d, y - d, 0], color=INK, stroke_width=sw)
    return VGroup(ring, bar)


def a1_icon_page(x, y):
    """Instructions: a page with three ghost lines and one terracotta dot."""
    body = Rectangle(width=0.56, height=0.72, stroke_color=DIM, stroke_width=4).move_to([x, y, 0])
    ls = VGroup(*[Line([x - 0.16, y + dy, 0], [x + 0.16, y + dy, 0], color=BAR2, stroke_width=4) for dy in (0.16, 0.0, -0.16)])
    return VGroup(body, ls, Dot([x - 0.16, y - 0.27, 0], radius=0.05, color=TERRA))


def a1_icon_tool(x, y):
    """Tools: a hammer (handle and head)."""
    handle = Line([x, y - 0.36, 0], [x, y + 0.14, 0], color=DIM, stroke_width=9)
    head = Rectangle(width=0.58, height=0.22, stroke_color=DIM, stroke_width=5).move_to([x, y + 0.26, 0])
    return VGroup(handle, head)


def a1_icon_loop(x, y):
    """A way of working: a loop with an arrow head."""
    a0, da, r = 0.45, 5.2, 0.3
    arc = Arc(radius=r, start_angle=a0, angle=da, stroke_color=DIM, stroke_width=6).move_to([x, y, 0])
    e = a0 + da
    px, py = x + r * np.cos(e), y + r * np.sin(e)
    tx, ty = -np.sin(e), np.cos(e)
    nx, ny = np.cos(e), np.sin(e)
    tip = Polygon([px + tx * 0.2, py + ty * 0.2, 0], [px + nx * 0.11, py + ny * 0.11, 0], [px - nx * 0.11, py - ny * 0.11, 0],
                  fill_color=DIM, fill_opacity=1, stroke_width=0)
    return VGroup(arc, tip)


# ═════════════════════════════════ B01 · a framework, not a game, not an engine ═════════════════════════════════
class B01_Framework(Scene):
    def construct(self):
        title = T("The Problem Walker Answers", 40).move_to([-2.85, 3.0, 0])
        img = ImageMobject(A1P + "a1_github_walker_crop.png").set_height(4.6).move_to([0, 0.05, 0])
        frame = Rectangle(width=4.0, height=4.72, stroke_color=DIM, stroke_width=3).move_to([0, 0.05, 0])
        addr = M("nikbearbrown/walker", 32).move_to([0, -2.65, 0])
        date = T("public page, captured 2026-10-09", 32).move_to([0, -3.1, 0])
        cap = Group(img, frame, addr, date)
        self.add(title)
        self.play(FadeIn(cap), run_time=0.6)

        # the page slides left to make room (before the midpoint)
        a1_at(self, 2.85)
        self.play(cap.animate.shift(LEFT * 3.5), run_time=0.7)
        g_lab = T("a game", 38).move_to([1.66, 2.0, 0])
        e_lab = T("an engine", 38).move_to([1.99, 1.15, 0])
        self.play(FadeIn(g_lab), FadeIn(e_lab), run_time=0.4)
        a1_at(self, 3.95)
        g_no = a1_no(0.35, 2.0)
        self.play(Create(g_no), run_time=0.35)
        # the midpoint (4.7 s) holds: capture, "a game" struck, "an engine" waiting
        a1_at(self, 5.0)
        e_no = a1_no(0.35, 1.15)
        self.play(Create(e_no), run_time=0.35)

        a1_at(self, 6.15)
        i_ic = a1_icon_page(0.35, -0.05)
        i_lab = T("instructions", 38).move_to([2.22, -0.05, 0])
        self.play(FadeIn(i_ic), FadeIn(i_lab), run_time=0.4)
        a1_at(self, 7.12)
        t_ic = a1_icon_tool(0.35, -0.95)
        t_lab = T("tools", 38).move_to([1.47, -0.95, 0])
        self.play(FadeIn(t_ic), FadeIn(t_lab), run_time=0.4)
        a1_at(self, 7.85)
        w_ic = a1_icon_loop(0.35, -1.85)
        w_lab = T("a way of working", 38).move_to([2.71, -1.85, 0])
        self.play(FadeIn(w_ic), FadeIn(w_lab), run_time=0.4)
        done(self)


# ═════════════════════════════════ B02 · the sentence: execution cheap, judgment not ═════════════════════════════════
class B02_OneSentence(Scene):
    def construct(self):
        q1 = T("AI made execution cheap.", 40).move_to([0, 2.85, 0])
        q2 = T("It  did not make judgment cheap.", 40).move_to([0, 2.22, 0])
        src = M("legacy/README.md, line 7", 32).move_to([0, 1.62, 0])
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(src), run_time=0.6)

        base = -2.45
        bar_a = Rectangle(width=1.5, height=3.2, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.7, base + 1.6, 0])
        bar_b = Rectangle(width=1.5, height=3.2, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([1.7, base + 1.6, 0])
        lab_a = T("execution", 36).move_to([-1.7, -2.9, 0])
        lab_b = T("judgment", 36).move_to([1.7, -2.9, 0])
        cost = T("cost", 32).move_to([-5.0, -0.7, 0])
        note1 = T("illustration,", 32).move_to([4.75, -1.2, 0])
        note2 = T("not data", 32).move_to([4.75, -1.65, 0])
        self.play(FadeIn(bar_a), FadeIn(bar_b), FadeIn(lab_a), FadeIn(lab_b), FadeIn(cost), FadeIn(note1), FadeIn(note2), run_time=0.5)
        axis = Arrow([-4.4, base, 0], [-4.4, 1.0, 0], color=INK, stroke_width=5, buff=0, tip_length=0.2)
        self.play(Create(axis), run_time=0.4)

        # "AI made execution cheap": the execution bar falls (lands before the midpoint at 2.72 s)
        a1_at(self, 2.0)
        small = Rectangle(width=1.5, height=0.55, fill_color=BAR1, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([-1.7, base + 0.275, 0])
        self.play(Transform(bar_a, small), run_time=0.7)

        # "It did not make judgment cheap": a level line from where the cost was, and the judgment bar stays
        a1_at(self, 3.4)
        ghost = DashedLine([-2.45, base + 3.2, 0], [0.95, base + 3.2, 0], color=DIM, stroke_width=5, dash_length=0.18)
        self.play(Create(ghost), run_time=0.5)
        a1_at(self, 3.85)
        dot = Dot([1.7, base + 3.2 + 0.3, 0], radius=0.11, color=TERRA)
        self.play(GrowFromCenter(dot), run_time=0.3)
        done(self)


# ═════════════════════════════════ B03 · the membrane, and a repo of documents ═════════════════════════════════
class B03_Membrane(Scene):
    def construct(self):
        head = T("Doctrine and tooling for AI-assisted Unity work", 36).move_to([0, 2.95, 0])
        src = M("legacy/README.md, line 3", 32).move_to([0, 2.4, 0])
        self.play(FadeIn(head), FadeIn(src), run_time=0.6)

        a1_at(self, 2.45)
        vline = Line([0, 1.95, 0], [0, -1.55, 0], color=INK, stroke_width=9)
        agent = T("agent", 40).move_to([-3.0, 1.6, 0])
        human = T("human", 40).move_to([3.0, 1.6, 0])
        sub_l = T("text layer", 32).move_to([-3.0, 0.98, 0])
        sub_r = T("asset layer", 32).move_to([3.0, 0.98, 0])
        self.play(Create(vline), run_time=0.5)
        self.play(FadeIn(agent), FadeIn(human), FadeIn(sub_l), FadeIn(sub_r), run_time=0.4)

        a1_at(self, 3.95)
        c1, c2 = M("C#", 32).move_to([-3.0, 0.3, 0]), M("config", 32).move_to([-3.0, -0.4, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.5)
        # the midpoint (6.07 s) holds: the line, both columns named, the agent's side filled
        a1_at(self, 4.95)
        r1, r2, r3 = M(".meta", 32).move_to([3.0, 0.3, 0]), M(".prefab", 32).move_to([3.0, -0.4, 0]), M("scenes", 32).move_to([3.0, -1.1, 0])
        self.play(FadeIn(r1), FadeIn(r2), FadeIn(r3), run_time=0.5)

        # then the repo itself: documents only
        a1_at(self, 7.15)
        old = VGroup(vline, agent, human, sub_l, sub_r, c1, c2, r1, r2, r3)
        l1 = a1_ml("legacy/unity/", -5.7, 1.25)
        l2 = a1_ml("  README.md", -5.7, 0.7)
        l3 = a1_ml("  UNITY.md", -5.7, 0.15)
        l4 = a1_ml("  gate-pilot/*.md", -5.7, -0.4)
        cnt = T("18 files in legacy/: 17 .md and one .gitignore", 32).move_to([0, -1.2, 0])
        self.play(FadeOut(old), run_time=0.35)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3), FadeIn(l4), FadeIn(cnt), run_time=0.5)

        a1_at(self, 9.2)
        slot = DashedVMobject(Rectangle(width=4.4, height=1.9, stroke_color=DIM, stroke_width=5), num_dashes=40).move_to([3.3, 0.4, 0])
        tool = T("tooling", 38).move_to([3.3, 0.4, 0])
        self.play(Create(slot), FadeIn(tool), run_time=0.5)
        quote = T("the unity/ tooling does not exist yet", 36).move_to([0, -2.05, 0])
        qsrc = M("legacy/AGENTS.md, line 7", 32).move_to([0, -2.65, 0])
        self.play(FadeIn(quote), FadeIn(qsrc), run_time=0.5)
        done(self)


# ═════════════════════════════════ B04 · Godot, Godogen (MIT), and a skill added on top ═════════════════════════════════
class B04_OnTop(Scene):
    def construct(self):
        SX0, SX1 = -2.5, 6.0                       # slab left / right edge
        TX = -2.2                                    # text left edge inside the slabs
        # bottom slab: publish.sh's real usage line
        s1 = Rectangle(width=SX1 - SX0, height=1.15, stroke_color=INK, stroke_width=4).move_to([(SX0 + SX1) / 2, -2.5, 0])
        t1 = a1_ml("--engine godot|bevy|babylon", TX, -2.68)
        f1 = a1_mr("publish.sh", -2.8, -2.5)
        n1 = T("this film: godot", 32).move_to([-4.55, -3.02, 0])
        self.play(FadeIn(s1), FadeIn(t1), FadeIn(f1), FadeIn(n1), run_time=0.5)
        a1_at(self, 0.9)
        dot = Dot([TX + 9.5 * A1_MW + 0.5 * 5 * A1_MW - 0.5 * A1_MW, -2.17, 0], radius=0.09, color=TERRA)
        self.play(GrowFromCenter(dot), run_time=0.3)

        # middle slab: Godogen's own line, then the licence
        a1_at(self, 3.75)
        s2 = Rectangle(width=SX1 - SX0, height=2.15, stroke_color=INK, stroke_width=4).move_to([(SX0 + SX1) / 2, -0.52, 0])
        t3 = a1_ml("Initial Godogen release ...", TX, -1.1)
        f3 = a1_mr("CHANGELOG.md", -2.8, -1.1)
        self.play(FadeIn(s2), FadeIn(t3), FadeIn(f3), dot.animate.move_to([5.7, -1.1, 0]), run_time=0.5)
        # the midpoint (5.5 s) holds: the engine line and Godogen's line

        a1_at(self, 4.75)
        t_a = a1_ml("The MIT License", TX, 0.0)
        t_b = a1_ml("Copyright 2026 Alex Ermolov", TX, -0.55)
        f_a = a1_mr("LICENSE.md", -2.8, 0.0)
        self.play(FadeIn(t_a), FadeIn(t_b), FadeIn(f_a), dot.animate.move_to([5.7, 0.0, 0]), run_time=0.5)
        a1_at(self, 6.7)
        self.play(dot.animate.move_to([5.7, -0.55, 0]), Indicate(t_b, scale_factor=1.06, color=INK), run_time=0.6)

        # the added layer lands on top
        a1_at(self, 8.4)
        s3 = Rectangle(width=SX1 - SX0, height=1.7, stroke_color=INK, stroke_width=4).move_to([(SX0 + SX1) / 2, 1.9, 0])
        t5 = a1_ml("2026-09-18", TX, 2.3)
        t6 = a1_ml("Added gdd/, the Zelda GDD skill", TX, 1.65)
        f5 = a1_mr("CHANGELOG.md", -2.8, 2.3)
        n5a = T("working copy:", 32).move_to([-4.45, 1.8, 0])
        n5b = T("not in public repo", 32).move_to([-4.45, 1.4, 0])
        top = VGroup(s3, t5, t6, f5)
        self.play(FadeIn(top, shift=DOWN * 0.6), dot.animate.move_to([5.7, 1.65, 0]), run_time=0.7)
        # "so far only in the working copy" (10.46 s): the label lands on those words
        a1_at(self, 10.35)
        self.play(FadeIn(n5a), FadeIn(n5b), run_time=0.5)
        done(self)
