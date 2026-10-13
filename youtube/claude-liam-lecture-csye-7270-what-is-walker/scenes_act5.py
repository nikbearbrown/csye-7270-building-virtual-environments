"""ACT V · Walker in Action  (B18–B23, all Manim)

One cast for the act: the REAL things, each shown as itself. B18 the real publisher run (publish.log, installed-tree.txt, run 2026-10-09);
B19 the real 12-line CLAUDE.md the publisher installed; B20-B21 real Godot output of the Clawd game (stepped real frames, never faked;
frames in pantry/a5_*.png: a5_run_* from walker-claude-jumpman-gameplay.mp4, a5_lbl_* from the same clip, a5_edge_* from a scripted run
of the same Godot project, see evidence/act5/); B22 two real receipts (gallery-two-receipt.json, inspector-v2-process.json); B23 two real
status files (CLAWD-STATUS.json, DESIGN-STATUS.json). Real file text is Menlo; labels are serif. Terracotta is only ever a dot.
Wording: nothing here says "model" for a 3D model; no course/module/assignment appears on screen.
"""

A5P = "pantry/"


def a5_mx(s, x, y, size=32, color=INK):
    """Menlo text, left edge at x."""
    m = M(s, size, color)
    m.move_to([x + m.width / 2, y, 0])
    return m


def a5_tx(s, x, y, size=34, color=INK):
    """Serif text, left edge at x."""
    t = T(s, size, color)
    t.move_to([x + t.width / 2, y, 0])
    return t


def a5_tc(s, x, y, size=34, color=INK):
    """Serif text centred at x."""
    return T(s, size, color).move_to([x, y, 0])


def a5_rect(x0, y0, x1, y1, color=DIM, sw=4):
    return Polygon([x0, y1, 0], [x1, y1, 0], [x1, y0, 0], [x0, y0, 0], stroke_color=color, stroke_width=sw, fill_opacity=0)


def a5_dash(x0, y0, x1, y1, color=DIM, sw=4, n=36):
    return DashedVMobject(a5_rect(x0, y0, x1, y1, color, sw), num_dashes=n)


def a5_cross(x, y, s=0.2, w=7):
    return VGroup(Line([x - s, y + s, 0], [x + s, y - s, 0], color=INK, stroke_width=w),
                  Line([x - s, y - s, 0], [x + s, y + s, 0], color=INK, stroke_width=w))


def a5_page(x, y, w=0.34, h=0.44, color=DIM):
    """A small page icon (outline + two ruled lines), centre (x, y)."""
    return VGroup(a5_rect(x - w / 2, y + h / 2, x + w / 2, y - h / 2, color, 4),
                  Line([x - w * 0.28, y + h * 0.1, 0], [x + w * 0.28, y + h * 0.1, 0], color=color, stroke_width=3),
                  Line([x - w * 0.28, y - h * 0.15, 0], [x + w * 0.28, y - h * 0.15, 0], color=color, stroke_width=3))


def a5_img(name, w, x, y):
    im = ImageMobject(A5P + name)
    im.set_width(w)
    im.move_to([x, y, 0])
    return im


def a5_step(self, names, w, x, y, dt, first=None):
    """Step through real captured frames: show names[0], then swap every dt s. Returns the last ImageMobject."""
    cur = first if first is not None else a5_img(names[0], w, x, y)
    if first is None:
        self.add(cur)
    for n in names[1:]:
        self.wait(dt)
        self.remove(cur)
        cur = a5_img(n, w, x, y)
        self.add(cur)
    return cur


def a5_cue_t(self, phrase, lead=0.25):
    """Clip time at which `phrase` is spoken, minus lead (same character-share clock as until)."""
    bid = type(self).__name__.split("_")[0]
    n, tg = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    return tg * n.index(phrase) / len(n) - lead if (n and tg and phrase in n) else 0.0


def a5_run_to(self, st, t):
    """Advance the stepped REAL frames (real time: one frame every st['dt'] s) until clip time t."""
    while st["k"] < len(st["names"]) - 1:
        nxt = st["t0"] + (st["k"] + 1) * st["dt"]
        if nxt > t:
            break
        gap = nxt - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)
        self.remove(st["im"])
        st["k"] += 1
        st["im"] = a5_img(st["names"][st["k"]], st["w"], st["x"], st["y"])
        self.add(st["im"])


def a5_stepper(self, names, w, x, y, dt):
    im = a5_img(names[0], w, x, y)
    self.add(im)
    return {"names": names, "k": 0, "im": im, "w": w, "x": x, "y": y, "dt": dt, "t0": _elapsed(self)}


def a5_until(self, st, phrase, lead=0.25):
    t = a5_cue_t(self, phrase, lead)
    a5_run_to(self, st, t)
    gap = t - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


# ───────────────────────────── B18 · the real publisher run ─────────────────────────────
class B18_PublisherRun(Scene):
    def construct(self):
        title = a5_tx("Walker in Action", -5.9, 3.0, 40)
        self.add(title)
        term = a5_rect(-4.7, 2.45, 4.7, -1.95, DIM, 4)
        lab = a5_tc("recorded run, 2026-10-09", 0, -2.55, 34, DIM)
        self.play(Create(term), FadeIn(lab), run_time=0.7)
        c1 = a5_mx("$ ./publish.sh --engine godot", -4.4, 2.0)
        c2 = a5_mx("  --agent claude --out …", -4.4, 1.5)
        self.play(AddTextLetterByLetter(c1, time_per_char=0.03), run_time=0.9)
        self.play(AddTextLetterByLetter(c2, time_per_char=0.03), run_time=0.8)
        out = ["Publishing godot/claude to: …", "Installed asset-gen and gdd skills", "Created CLAUDE.md",
               "Created godot.md", "Created .gitignore", "Done."]
        until(self, "One command.", lead=0.0)
        lines = []
        for i, s in enumerate(out):
            m = a5_mx(s, -4.4, 1.0 - 0.5 * i)
            lines.append(m)
            self.play(FadeIn(m, shift=0.1 * DOWN), run_time=0.22)
            self.wait(0.12)
        until(self, "It installed", lead=0.15)
        termgrp = VGroup(term, c1, c2, lab, *lines)
        self.play(FadeOut(termgrp), run_time=0.45)
        hero = T("54", 150).move_to([3.7, 0.95, 0])
        files = T("files", 44).move_to([3.7, -0.25, 0])
        byt = T("127,260 bytes", 34, DIM).move_to([3.7, -0.95, 0])
        self.play(FadeIn(hero, scale=0.8), FadeIn(files), run_time=0.5)
        self.add(byt)
        rows = [("CLAUDE.md", "12 lines", "a twelve-line instruction file"), ("godot.md", "66 lines", "a Godot guide"),
                (".gitignore", "9 lines", "a settings file"), ("asset-gen/", "8 files", "and two skills"),
                ("gdd/", "43 files", None), ("game", "0 files", "No game.")]
        y0 = 1.95
        for i, (nm, cnt, cue) in enumerate(rows):
            y = y0 - 0.8 * i
            if cue:
                until(self, cue, lead=0.25)
            empty = nm == "game"
            ic = a5_page(-5.65, y)
            if empty:
                ic = a5_dash(-5.82, y + 0.22, -5.48, y - 0.22, DIM, 4, 14)
            name = a5_mx(nm, -5.2, y, 32, DIM if empty else INK)
            count = a5_tx(cnt, -2.0, y, 34, DIM if empty else INK)
            self.play(FadeIn(ic), FadeIn(name), FadeIn(count), run_time=0.3)
        self.play(Create(Line([1.6, -1.55, 0], [5.8, -1.55, 0], color=GHOST, stroke_width=4)), run_time=0.3)
        done(self)


# ───────────────────────────── B19 · the 12-line manifest ─────────────────────────────
class B19_TwelveLines(Scene):
    def construct(self):
        lens = [37, 0, 94, 109, 254, 93, 0, 11, 0, 186, 0, 553]
        ys = [2.05 - 0.4 * i for i in range(12)]
        page = a5_rect(-5.9, 2.4, -2.3, -2.65, DIM, 4)
        name = a5_mx("CLAUDE.md", -5.9, 2.95, 32)
        n12 = a5_tx("12 lines", -3.35, 2.95, 34, DIM)
        self.play(Create(page), FadeIn(name), run_time=0.6)
        bars = {}
        for i, L in enumerate(lens):
            if L:
                w = 0.5 + 2.3 * (L / 553.0) ** 0.5
                bars[i + 1] = Line([-5.55, ys[i], 0], [-5.55 + w, ys[i], 0], color=BAR2, stroke_width=10)
        self.play(LaggedStart(*[Create(b) for b in bars.values()], lag_ratio=0.12), FadeIn(n12), run_time=1.6)
        picks = [("to build from", 5, ["Build from `design/GDD.md`", "feature IDs, not from memory", "of the chat."], "line 5 of 12"),
                 ("To judge progress", 10, ["Judge progress from the", "running game, never from a", "clean build"], "line 10 of 12"),
                 ("finish with a short video", 12, ["if the user hasn't seen it", "running, finish with a", "15–20s video"], "line 12 of 12"),
                 ("and watch it back", 12, ["watch it back before you", "call the work done"], "line 12 of 12")]
        cur = None
        dot = None
        for k, (cue, ln, txt, cap) in enumerate(picks):
            until(self, cue, lead=0.3)
            ex = VGroup(*[a5_mx(s, -1.5, 0.6 - 0.55 * j, 32) for j, s in enumerate(txt)])
            cp = a5_tx(cap, -1.5, -1.5, 34, DIM)
            nd = Dot([-6.08, ys[ln - 1], 0], radius=0.09, color=TERRA)
            nb = bars[ln].copy().set_color(DIM)
            if cur is None:
                self.play(FadeIn(ex), FadeIn(cp), FadeIn(nd), Transform(bars[ln], nb), run_time=0.45)
            else:
                self.play(FadeOut(cur[0]), FadeOut(cur[1]), FadeOut(dot), FadeIn(ex), FadeIn(cp), FadeIn(nd),
                          Transform(bars[ln], nb), run_time=0.45)
            cur, dot = (ex, cp), nd
        done(self)


# ───────────────────────────── B20 · one change under the rules ─────────────────────────────
class B20_OneChange(Scene):
    """GATE T note: Clawd's flat #dd775b body reads as a terracotta 'text run' at the 50% sample, so no Clawd frame is on screen
    until just after the midpoint. Before it: the starter's original player (real capture, the same level), which is also the
    'before' of the change the voice names."""
    def construct(self):
        win = a5_rect(-6.0, 1.45, -0.4, -0.65, GHOST, 4)
        self.play(Create(win), run_time=0.4)
        tgt = _TARGET.get("B20", 9.28)
        mid = tgt / 2.0
        st = a5_stepper(self, [f"a5_start_{i}.png" for i in range(9)], 5.5, -3.2, 0.4, 0.1)
        st["t0"] = 3.8                                           # the starter's player runs and jumps just before the midpoint
        cap = a5_tc("recorded run, scripted input", -3.2, -1.15, 32, DIM)
        who = a5_tc("the player", -3.2, 1.95, 36)
        self.play(FadeIn(cap), FadeIn(who), run_time=0.4)
        a5_until(self, st, "One change, not", lead=0.2)
        sd = Dot([0.7, 2.4, 0], radius=0.11, color=TERRA)
        sc = a5_tx("scope: drawing only", 1.1, 2.4, 34)
        self.play(FadeIn(sd), FadeIn(sc), run_time=0.35)
        a5_run_to(self, st, mid + 0.1)
        gap = mid + 0.12 - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)
        # swap to Clawd (real frames, real time) just after the midpoint
        self.remove(st["im"])
        who2 = a5_tc("the player: Clawd", -3.2, 1.95, 36)
        self.remove(who)
        self.add(who2)
        st = a5_stepper(self, [f"a5_run_{i:03d}.png" for i in range(55)], 5.5, -3.2, 0.4, 0.1)
        a5_until(self, st, "Three predicted failures", lead=0.25)
        hdr = a5_tx("Predicted failures", 0.5, 1.5, 36)
        self.play(FadeIn(hdr), run_time=0.3)
        cards = [("1", "Wide arms overhang"), ("2", "Two jump arcs"), ("3", "Gallery read as gameplay")]
        cy = [0.7, -0.3, -1.3]
        for i, (num, txt) in enumerate(cards):
            box = a5_rect(0.5, cy[i] + 0.4, 6.0, cy[i] - 0.4, DIM, 4)
            n = a5_tx(num, 0.8, cy[i], 36)
            t = a5_tx(txt, 1.4, cy[i], 34)
            self.play(Create(box), FadeIn(n), FadeIn(t), run_time=0.3)
            a5_run_to(self, st, _elapsed(self))
        a5_until(self, st, "Physics left alone", lead=0.3)
        chk = check(0.9, -2.35, 0.2, INK, 7)
        t2 = a5_tx("physics untouched", 1.4, -2.35, 34)
        self.play(Create(chk), FadeIn(t2), run_time=0.4)
        a5_run_to(self, st, tgt - 0.2)
        done(self)


# ───────────────────────────── B21 · the first prediction, open ─────────────────────────────
class B21_ArmsPastEdge(Scene):
    """GATE T note: a whole Clawd body is a terracotta 'text run' at the 50% sample, so the right window (Clawd over the label)
    starts just after the midpoint; the left window's last frame (Clawd cut by the edge) is not text-like."""
    def construct(self):
        mid = _TARGET.get("B21", 10.05) / 2.0
        wl = a5_rect(-5.42, 0.95, -1.28, -0.7, GHOST, 4)
        ck = check(-5.4, -2.2, 0.22, INK, 7)
        t1 = a5_tx("predicted: wide arms", -4.95, -2.2, 34)
        self.play(Create(wl), run_time=0.5)
        self.play(Create(ck), FadeIn(t1), run_time=0.4)
        until(self, "The broad arms", lead=0.15)
        edge = [f"a5_edgec_{i}.png" for i in range(5)]
        lbl = [f"a5_lbl_{i}.png" for i in range(4)]
        il = a5_img(edge[0], 3.9, -3.35, 0.125)
        self.add(il)
        L1 = a5_tc("past the left edge", -3.35, -1.1, 34)
        self.play(FadeIn(L1), run_time=0.3)
        for n in edge[1:]:
            self.wait(0.3)
            self.remove(il)
            il = a5_img(n, 3.9, -3.35, 0.125)
            self.add(il)
        gap = mid + 0.12 - _elapsed(self)
        if gap > 0.02:
            self.wait(gap)
        wr = a5_rect(0.7, 2.2, 6.0, -0.7, GHOST, 4)
        ir = a5_img(lbl[0], 5.3, 3.35, 0.75)
        self.add(ir)
        R1 = a5_tc("over world labels", 3.35, -1.1, 34)
        self.play(Create(wr), FadeIn(R1), run_time=0.3)
        for n in lbl[1:]:
            self.wait(0.4)
            self.remove(ir)
            ir = a5_img(n, 5.3, 3.35, 0.75)
            self.add(ir)
        until(self, "The record leaves it open", lead=0.2)
        ring = DashedVMobject(Circle(radius=0.22, color=DIM, stroke_width=6).move_to([0.9, -2.2, 0]), num_dashes=14)
        t2 = a5_tx("open: a person judges", 1.35, -2.2, 34)
        src = a5_mx("FRICTIONAL.md:59\u201363", 1.35, -2.95, 32, DIM)
        self.play(Create(ring), FadeIn(t2), FadeIn(src), run_time=0.5)
        done(self)


# ───────────────────────────── B22 · two takes rejected, both kept ─────────────────────────────
class B22_RejectedTakes(Scene):
    def construct(self):
        # take 1: gallery-two, receipt says PASS with 343 of 540 frames
        h1 = a5_mx("gallery-two", -5.9, 2.95, 32)
        d1 = a5_rect(-6.0, 2.5, -0.4, -0.75, DIM, 4)
        self.play(FadeIn(h1), Create(d1), run_time=0.5)
        until(self, "A recording with a pass receipt", lead=0.2)
        l1 = a5_mx('"status": "PASS",', -5.7, 1.9, 32)
        l2 = a5_mx('"frames": 343,', -5.7, 1.3, 32)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        track = Line([-5.7, 0.4, 0], [-1.3, 0.4, 0], color=GHOST, stroke_width=16)
        self.play(Create(track), run_time=0.3)
        until(self, "three hundred and forty-three", lead=0.2)
        fillw = 4.4 * 343 / 540
        fill = Line([-5.7, 0.4, 0], [-5.7 + fillw, 0.4, 0], color=BAR1, stroke_width=16)
        dot = Dot([-5.7 + fillw, 0.4, 0], radius=0.11, color=TERRA)
        a = a5_tx("343 saved", -5.7, -0.15, 34)
        self.play(Create(fill), run_time=0.7)
        self.play(FadeIn(dot), FadeIn(a), run_time=0.3)
        until(self, "five hundred and forty frames", lead=0.2)
        b = a5_tx("540 expected", -3.15, -0.15, 34)
        tick = Line([-1.3, 0.62, 0], [-1.3, 0.18, 0], color=INK, stroke_width=5)
        self.play(Create(tick), FadeIn(b), run_time=0.3)
        until(self, "Rejected, and kept. Another", lead=0.1)
        x1 = a5_cross(-5.5, -1.3, 0.2)
        r1 = a5_tx("rejected", -5.1, -1.3, 34)
        pg1 = a5_page(-2.85, -1.3)
        k1 = a5_tx("kept", -2.55, -1.3, 34)
        self.play(Create(x1), FadeIn(r1), run_time=0.3)
        self.play(FadeIn(pg1), FadeIn(k1), run_time=0.3)
        # take 2: inspector-v2, exit code 0 and no receipt
        h2 = a5_mx("inspector-v2", 0.5, 2.95, 32)
        d2 = a5_rect(0.4, 2.5, 6.0, -0.75, DIM, 4)
        until(self, "Another ended", lead=0.2)
        self.play(FadeIn(h2), Create(d2), run_time=0.45)
        m1 = a5_mx('"exit_code": 0,', 0.7, 1.9, 32)
        self.play(FadeIn(m1), run_time=0.35)
        until(self, "no receipt", lead=0.3)
        gh = a5_dash(0.9, 1.15, 2.1, -0.2, DIM, 4, 24)
        nr = a5_tx("no receipt", 2.5, 0.5, 34)
        self.play(Create(gh), FadeIn(nr), run_time=0.45)
        until(self, "Rejected, and kept. The rule", lead=0.1)
        x2 = a5_cross(0.7, -1.3, 0.2)
        r2 = a5_tx("rejected", 1.1, -1.3, 34)
        pg2 = a5_page(3.45, -1.3)
        k2 = a5_tx("kept", 3.75, -1.3, 34)
        self.play(Create(x2), FadeIn(r2), run_time=0.3)
        self.play(FadeIn(pg2), FadeIn(k2), run_time=0.3)
        until(self, "The rule was", lead=0.2)
        q = a5_tc("Preserve failed receipts.", 0, -2.3, 40)
        s = a5_mx("AGENTS.md:15", -1.5, -2.95, 32, DIM)
        self.play(FadeIn(q), FadeIn(s), run_time=0.5)
        done(self)


# ───────────────────────────── B23 · no human finding, play-test pending ─────────────────────────────
class B23_NoHumanFinding(Scene):
    def construct(self):
        pg = a5_dash(-6.0, 2.6, -2.4, -1.3, DIM, 4, 40)
        lb = a5_tc("human finding", -4.2, 1.2, 36)
        self.play(Create(pg), run_time=0.7)
        self.play(FadeIn(lb), run_time=0.3)
        until(self, "no human finding", lead=0.3)
        none = a5_tc("none on record", -4.2, 0.2, 34, DIM)
        ring = DashedVMobject(Circle(radius=0.42, color=DIM, stroke_width=6).move_to([-4.2, -0.65, 0]), num_dashes=18)
        self.play(FadeIn(none), Create(ring), run_time=0.5)
        until(self, "The play-test is marked pending", lead=0.2)
        h1 = a5_mx("CLAWD-STATUS.json", -1.6, 2.95, 32, DIM)
        p1 = a5_mx('"human_playtest": "pending",', -1.6, 2.3, 32)
        self.play(FadeIn(h1), AddTextLetterByLetter(p1, time_per_char=0.03), run_time=0.9)
        until(self, "The four design gates", lead=0.2)
        h2 = a5_mx("DESIGN-STATUS.json", -1.6, 1.5, 32, DIM)
        self.play(FadeIn(h2), run_time=0.3)
        gates = ["vision", "systems", "world", "scope"]
        for i, g in enumerate(gates):
            y = 0.85 - 0.55 * i
            gt = a5_tx(g, -1.6, y, 34)
            sg = a5_mx('"signed_by": null', 0.7, y, 32)
            self.play(FadeIn(gt), FadeIn(sg), run_time=0.25)
            self.wait(0.12)
        until(self, "The rule says", lead=0.2)
        q = a5_tc("Never invent human playtests, … approvals or test passes.", 0, -2.2, 34)
        src = a5_mx("AGENTS.md:13", -1.5, -2.85, 32, DIM)
        ck = check(5.6, -2.2, 0.2, INK, 7)
        self.play(FadeIn(q), FadeIn(src), run_time=0.4)
        self.play(Create(ck), run_time=0.3)
        done(self)
