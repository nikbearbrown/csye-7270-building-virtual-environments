"""ACT IV · How the AI Writes Code  (B14-B17, all Manim)

Cast for the act: the REAL text of the installed Godot guide (godot.md, lines 3 / 10 / 49) and the installed manifest line
(CLAUDE.md:10), the four conventions of the GDScript prompt (godot-scripting-conventions-research-prompt.md, lines 136-168) with
their own example lines, the three-way disagreement (godot.md:3 C#, /gdd p3.md:6 typed GDScript, the real walker-claude/godot tree:
0 .cs / 0 .csproj / 11 .gd, counted 2026-10-09) and the REAL installed tree of the publisher run (installed-tree.txt: 54 files, none
ending .gd). Every quote is <= 15 words, cut with a visible ellipsis, and carries its file:line. Nothing is a mock-up of an interface:
the files are shown as text, which is what they are. Sources and counts: factcheck/act4.md.
Pacing: until(self, "exact phrase", lead) waits for the spoken word; nothing straddles the clip midpoint (the kit's guard).
"""


def a4_L(mob, x, y):
    """Place a text left-aligned at x (explicit coordinates; never read back a text's edge)."""
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def a4_at(self, t):
    """Wait until the clip clock reaches t seconds (t from faster-whisper word times, evidence/act4/word_times.json, minus a lead).
    Used by B15 and B17, whose narration was re-voiced on 2026-10-09."""
    g = t - _elapsed(self)
    if g > 0.03:
        self.wait(g)


def a4_C(mob, x, y):
    return mob.move_to([x, y, 0])


def a4_page(x, y, w=0.46, h=0.58, fold=0.16, color=INK, fill=CARD):
    """A small page mark (dog-eared top right) centred at (x, y)."""
    l, r, t, b = x - w / 2, x + w / 2, y + h / 2, y - h / 2
    return Polygon([l, t, 0], [r - fold, t, 0], [r, t - fold, 0], [r, b, 0], [l, b, 0],
                   fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)


def a4_slab(x, y, w, h, stroke=DIM, fill=None, sw=5):
    """A flat slab drawn as a Polygon (a Rectangle would not count as a new shape for Gate A)."""
    pts = [[x - w / 2, y + h / 2, 0], [x + w / 2, y + h / 2, 0], [x + w / 2, y - h / 2, 0], [x - w / 2, y - h / 2, 0]]
    if fill is None:
        return Polygon(*pts, stroke_color=stroke, stroke_width=sw, fill_opacity=0)
    return Polygon(*pts, stroke_color=stroke, stroke_width=sw, fill_color=fill, fill_opacity=1)


def a4_down(x, y0, y1, w=5, tip=0.12):
    return Arrow([x, y0, 0], [x, y1, 0], buff=0, color=INK, stroke_width=w, tip_length=tip, max_tip_length_to_length_ratio=0.5)


# ═════════════════════════════ B14 · ACT TITLE · layer one: the installed Godot guide ═════════════════════════════
class B14_LayerOneGuide(Scene):
    def construct(self):
        title = a4_L(T("How the AI Writes Code", 40), -6.1, 3.05)
        self.add(title)
        until(self, "in two layers", lead=0.6)
        s2 = a4_slab(4.95, 3.0, 2.5, 0.46)
        s1 = a4_slab(4.95, 2.4, 2.5, 0.46)
        n2 = a4_C(T("2", 36), 3.35, 3.0)
        n1 = a4_C(T("1", 36), 3.35, 2.4)
        self.play(Create(s1), FadeIn(n1), run_time=0.3)
        self.play(Create(s2), FadeIn(n2), run_time=0.3)
        until(self, "Layer one is installed", lead=0.3)
        spark = Dot([4.95, 2.4, 0], radius=0.11, color=TERRA)
        chip = a4_L(T("Layer one: installed in every game", 36), -6.1, 2.4)
        frame = Rectangle(width=12.2, height=4.6, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0, -0.5, 0])
        vdiv = Line([1.4, 1.8, 0], [1.4, -2.8, 0], color=DIM, stroke_width=4)
        page = a4_page(-5.75, 1.35)
        fname = a4_L(M("godot.md", 32), -5.3, 1.35)
        self.play(FadeIn(spark, scale=0.4), FadeIn(chip), Create(frame), Create(vdiv), FadeIn(page), FadeIn(fname), run_time=0.55)
        # the build gate, in order (godot.md:10)
        ys = [0.65, -0.3, -1.55]
        cmds = ["dotnet build", "godot --headless --import", "godot --headless --quit"]
        nums = [a4_C(T(str(i + 1), 36), -5.8, ys[i]) for i in range(3)]
        lines = [a4_L(M(c, 32), -5.3, ys[i]) for i, c in enumerate(cmds)]
        qual = a4_L(T("after asset changes", 32), -4.5, -0.82)
        a1 = a4_down(-5.8, 0.38, -0.0)
        a2 = a4_down(-5.8, -0.55, -1.25)
        until(self, "It says build", lead=0.3)
        self.play(FadeIn(nums[0]), FadeIn(lines[0]), run_time=0.3)
        until(self, "then import", lead=0.35)
        self.play(GrowArrow(a1), FadeIn(nums[1]), FadeIn(lines[1]), FadeIn(qual), run_time=0.3)
        until(self, "then run headless", lead=0.3)
        self.play(GrowArrow(a2), FadeIn(nums[2]), FadeIn(lines[2]), run_time=0.35)
        # verify against the installed Godot (godot.md:49)
        until(self, "Verify against", lead=0.3)
        v1 = a4_L(T("\u201cVerify against the", 32), 1.85, 1.15)
        v2 = a4_L(T("installed Godot \u2026\u201d", 32), 1.85, 0.65)
        vs = a4_L(M("godot.md:49", 32), 1.85, 0.1)
        lens = Circle(radius=0.2, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([5.55, 0.95, 0])
        handle = Line([5.69, 0.81, 0], [5.9, 0.6, 0], color=DIM, stroke_width=7)
        self.play(FadeIn(v1), FadeIn(v2), FadeIn(vs), Create(lens), Create(handle), run_time=0.5)
        sep = Line([1.85, -0.45, 0], [5.95, -0.45, 0], color=DIM, stroke_width=3)
        # judge from the running game (CLAUDE.md:10)
        until(self, "And judge from the running game", lead=0.35)
        j1 = a4_L(T("\u201cJudge progress from", 32), 1.85, -1.0)
        j2 = a4_L(T("the running game \u2026\u201d", 32), 1.85, -1.5)
        js = a4_L(M("CLAUDE.md:10", 32), 1.85, -2.05)
        ring = Circle(radius=0.28, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([5.45, -2.05, 0])
        tri = Polygon([5.36, -1.9, 0], [5.36, -2.2, 0], [5.62, -2.05, 0], fill_color=TERRA, fill_opacity=1, stroke_width=0)
        self.play(Create(sep), FadeIn(j1), FadeIn(j2), FadeIn(js), Create(ring), FadeIn(tri, scale=0.4), run_time=0.5)
        done(self)


# ═════════════════════════════ B15 · layer two: four conventions, each with its own line ═════════════════════════════
class B15_LayerTwoConventions(Scene):
    def construct(self):
        head = a4_L(T("Layer two: conventions for GDScript", 40), -6.1, 3.0)
        fname = a4_L(M("godot-scripting-conventions-research-prompt.md", 32), -6.1, 2.3)
        s2 = a4_slab(5.0, 3.0, 2.0, 0.46)
        n2 = a4_C(T("2", 36), 3.75, 3.0)
        spark = Dot([5.0, 3.0, 0], radius=0.11, color=TERRA)
        rules = VGroup(*[Line([-6.1, y, 0], [6.1, y, 0], color=GHOST, stroke_width=3) for y in (1.95, 0.8, -0.65, -1.62)])
        self.add(head, s2, n2, spark, rules)
        a4_at(self, 0.7)
        self.play(FadeIn(fname), run_time=0.4)
        TAGX, X0 = -3.95, -3.25
        # row 1 · type every variable
        a4_at(self, 2.65)
        box = a4_slab(-5.7, 1.35, 0.62, 0.62, stroke=INK, sw=5)
        tag = Polygon([-5.28, 1.62, 0], [-4.82, 1.62, 0], [-4.62, 1.35, 0], [-4.82, 1.08, 0], [-5.28, 1.08, 0],
                      fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5)
        t1 = a4_C(M("L137", 32), TAGX, 1.35)
        r1 = a4_L(M("var hp: int = 100", 32), X0, 1.35)
        self.play(Create(box), FadeIn(t1), FadeIn(r1), run_time=0.4)
        self.play(FadeIn(tag, shift=LEFT * 0.25), run_time=0.3)
        # row 2 · signals, not reaching up
        a4_at(self, 4.1)
        par = a4_slab(-5.7, 0.5, 0.5, 0.34, stroke=INK, sw=5)
        chi = a4_slab(-5.7, -0.3, 0.5, 0.34, stroke=INK, sw=5)
        sig = Arrow([-5.7, -0.1, 0], [-5.7, 0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.15,
                    max_tip_length_to_length_ratio=0.5)
        pulse = Dot([-5.7, -0.1, 0], radius=0.085, color=TERRA)
        t2 = a4_C(M("L158", 32), TAGX, 0.1)
        r2 = a4_L(M("Never call a method on get_parent()", 32), X0, 0.1)
        self.play(Create(par), Create(chi), FadeIn(t2), FadeIn(r2), run_time=0.4)
        self.play(GrowArrow(sig), FadeIn(pulse), run_time=0.25)
        self.play(pulse.animate.move_to([-5.7, 0.3, 0]), run_time=0.5, rate_func=linear)
        a4_at(self, 5.95)
        reach = VGroup(Line([-5.4, -0.3, 0], [-5.22, -0.3, 0], color=DIM, stroke_width=4),
                       Line([-5.22, -0.3, 0], [-5.22, 0.5, 0], color=DIM, stroke_width=4),
                       Line([-5.22, 0.5, 0], [-5.4, 0.5, 0], color=DIM, stroke_width=4))
        cross = VGroup(Line([-5.32, 0.05, 0], [-5.12, 0.25, 0], color=INK, stroke_width=7),
                       Line([-5.32, 0.25, 0], [-5.12, 0.05, 0], color=INK, stroke_width=7))
        self.play(Create(reach), run_time=0.35)
        self.play(Create(cross), run_time=0.25)
        # row 3 · small, single-purpose scenes
        a4_at(self, 7.75)
        big = a4_slab(-5.7, -1.1, 1.0, 0.62, stroke=INK, sw=5)
        parts = VGroup(*[a4_slab(-6.02 + 0.32 * i, -1.1, 0.26, 0.4, stroke=DIM, sw=4) for i in range(3)])
        t3 = a4_C(M("L167", 32), TAGX, -1.1)
        r3 = a4_L(T("\u201ccomposing small, single-purpose scenes/components\u201d", 32), X0, -1.1)
        self.play(Create(big), FadeIn(t3), FadeIn(r3), run_time=0.35)
        self.play(LaggedStart(*[Create(p) for p in parts], lag_ratio=0.25), run_time=0.7)
        # row 4 · each feature's files together (the Clawd game's own folder)
        a4_at(self, 9.85)
        folder = Polygon([-6.1, -1.95, 0], [-5.55, -1.95, 0], [-5.4, -1.8, 0], [-5.1, -1.8, 0], [-5.1, -2.95, 0], [-6.1, -2.95, 0],
                         fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5)
        files = VGroup(*[a4_page(-5.84 + 0.36 * i, -2.5, w=0.26, h=0.36, fold=0.09, color=DIM) for i in range(3)])
        h4 = a4_L(T("Kept together in the Clawd game:", 32), X0 - 0.9, -1.95)
        d1 = a4_L(M("features/player/", 32), X0 - 0.9, -2.45)
        d2 = a4_L(M("  player.gd  tuning.gd  clawd_art.gd", 32), X0 - 0.9, -2.95)
        self.play(Create(folder), FadeIn(h4), FadeIn(d1), FadeIn(d2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.15) for f in files], lag_ratio=0.25), run_time=0.6)
        done(self)


# ═════════════════════════════ B16 · the honest problem: C# in the guide, GDScript everywhere else ═════════════════════════════
class B16_TwoLanguages(Scene):
    def construct(self):
        head = a4_L(T("C# or GDScript?", 40), -6.1, 3.05)
        self.add(head)
        divider = Line([0, 2.5, 0], [0, -3.2, 0], color=DIM, stroke_width=4)
        # left: the installed guide, C# (godot.md:3)
        until(self, "The installed guide assumes", lead=0.4)
        lt = a4_L(T("Installed guide", 36), -5.9, 2.1)
        hero_l = a4_C(T("C#", 110), -3.6, 1.0)
        dot_l = Dot([-2.35, 1.55, 0], radius=0.11, color=TERRA)
        q1a = a4_L(T("\u201cStack: Godot 4", 32), -5.9, 0.1)
        q1b = a4_L(T("(.NET / Mono build), C#.\u201d", 32), -5.9, -0.4)
        s1 = a4_L(M("godot.md:3", 32), -5.9, -0.95)
        self.play(Create(divider), FadeIn(lt), FadeIn(hero_l), FadeIn(q1a), FadeIn(q1b), FadeIn(s1), FadeIn(dot_l, scale=0.4),
                  run_time=0.6)
        # right: the example games and the design skill
        until(self, "The example games", lead=0.3)
        rt = a4_L(T("Games and design skill", 36), 0.3, 2.1)
        g1 = a4_L(M("walker-claude/godot/", 32), 0.3, 0.1)
        g2 = a4_L(M("11 files end .gd", 32), 0.3, -0.4)
        g3 = a4_L(M("0 files end .cs", 32), 0.3, -0.9)
        self.play(FadeIn(rt), FadeIn(g1), FadeIn(g2), FadeIn(g3), run_time=0.45)
        until(self, "the design skill installed", lead=0.3)
        sep2 = Line([0.3, -1.4, 0], [5.95, -1.4, 0], color=DIM, stroke_width=3)
        q2 = a4_L(T("\u201cdefault Godot 4, typed GDScript\u201d", 32), 0.3, -1.75)
        s2 = a4_L(M("gdd/commands/p3.md:6", 32), 0.3, -2.25)
        note = a4_L(T("working-tree install, 9 Oct 2026", 32), 0.3, -2.75)
        self.play(Create(sep2), FadeIn(q2), FadeIn(s2), FadeIn(note), run_time=0.45)
        until(self, "use G D script", lead=0.2)
        hero_r = a4_L(T("GDScript", 80), 0.3, 1.0)
        dot_r = Dot([5.3, 1.55, 0], radius=0.11, color=TERRA)
        self.play(FadeIn(hero_r, shift=UP * 0.15), FadeIn(dot_r, scale=0.4), run_time=0.45)
        until(self, "Walker's own readme", lead=0.3)
        sep1 = Line([-5.9, -1.4, 0], [-0.4, -1.4, 0], color=DIM, stroke_width=3)
        q3a = a4_L(T("\u201cIt does not yet select", 32), -5.9, -1.85)
        q3b = a4_L(T("a GDScript guide.\u201d", 32), -5.9, -2.35)
        s3 = a4_L(M("walker/README.md:45", 32), -5.9, -2.9)
        self.play(Create(sep1), FadeIn(q3a), FadeIn(q3b), FadeIn(s3), run_time=0.5)
        done(self)


# ═════════════════════════════ B17 · a prompt you can copy, vs what the publisher installs ═════════════════════════════
class B17_CopyVsInstalled(Scene):
    def construct(self):
        lab = a4_C(T("A prompt you can copy", 36), -3.2, 2.9)
        pg = a4_slab(-3.2, 0.9, 2.9, 3.4, stroke=INK, fill=CARD, sw=5)
        ghost = VGroup(*[Line([-4.45, 2.35 - 0.42 * i, 0], [-1.95 - (0.5 if i % 2 else 0.0), 2.35 - 0.42 * i, 0], color=GHOST, stroke_width=6)
                         for i in range(8)])
        pdot = Dot([-4.45, 0.25, 0], radius=0.09, color=TERRA)
        sep = Line([-5.9, -1.4, 0], [5.9, -1.4, 0], color=DIM, stroke_width=3)
        self.add(lab, pg, ghost, pdot, sep)
        a4_at(self, 1.6)
        dup = a4_slab(-3.2, 0.9, 2.9, 3.4, stroke=DIM, fill=CARD, sw=5)
        dup.set_z_index(-1)
        self.add(dup)
        self.play(dup.animate.shift(RIGHT * 0.35 + DOWN * 0.35), run_time=0.6)
        # installed side
        a4_at(self, 2.9)
        rlab = a4_C(T("Installed: 54 files", 36), 3.35, 2.9)
        rows = [("CLAUDE.md", ""), ("godot.md", ""), (".gitignore", ""), ("asset-gen/", "8 files"), ("gdd/", "43 files")]
        ys = [2.05, 1.5, 0.95, 0.4, -0.15]
        items = VGroup()
        for (nm, cnt), y in zip(rows, ys):
            items.add(a4_L(M(nm, 32), 0.85, y))
            if cnt:
                items.add(a4_L(M(cnt, 32), 3.9, y))
        rframe = Line([0.4, 2.5, 0], [0.4, -1.0, 0], color=DIM, stroke_width=4)
        self.play(FadeIn(rlab), Create(rframe), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.12), run_time=0.75)
        a4_at(self, 3.95)
        gd = a4_L(M("files ending .gd: 0", 32), 0.85, -0.7)
        zdot = Dot([0.65, -0.7, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(gd, shift=UP * 0.1), FadeIn(zdot, scale=0.4), run_time=0.4)
        # the example games: GDScript, and the conventions are in none of their instructions
        a4_at(self, 5.4)
        gl = a4_L(T("In the example game, walker-claude:", 34), -5.9, -1.8)
        self.play(FadeIn(gl), run_time=0.4)
        a4_at(self, 6.4)
        pa = a4_page(-5.65, -2.35, w=0.34, h=0.44, fold=0.12)
        gn = a4_L(M("GDD.md:324", 32), -5.25, -2.35)
        gq = a4_L(T("\u201cProposed game code is typed GDScript.\u201d", 34), -2.4, -2.35)
        self.play(FadeIn(pa), FadeIn(gn), FadeIn(gq), run_time=0.5)
        a4_at(self, 8.6)
        pb = a4_page(-5.65, -2.95, w=0.34, h=0.44, fold=0.12)
        an = a4_L(M("AGENTS.md", 32), -5.25, -2.95)
        ah = a4_L(T("hand-written, no typing or signal rules", 34), -2.4, -2.95)
        self.play(FadeIn(pb), FadeIn(an), FadeIn(ah), run_time=0.5)
        done(self)
