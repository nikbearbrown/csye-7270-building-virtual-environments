"""ACT IV · Connect Claude to Blender  (B29, B30, B34–B40 Manim; B31 BrowserCapture, B32–B33 CCPlainShell: see lanes/act4.json)

HONESTY RULE for the whole act: the course has NEVER run the MCP route. No beat shows an MCP session, a tool call's output, or the
add-on's panel. The route is drawn as an idea (the act's cast) and labelled "documented, not run"; the three typed commands are shown
without output; README text is the project's own words (<= 15 words per quote, version and date on screen). The script route WAS run:
B39A/B39B replay its real output (evidence/assets/build_lantern.log, evidence/exitcode/*.log).

One cast for the act (ACTS.md): three blocks, Claude Code (kraft block), the server (the kit's dark server stack) and Blender (kraft
block + Blender's REAL icon) with its add-on (the kit's dark MCP block) sitting on it; the socket (a ring with a terracotta dot) on
the add-on's face is where the line from the server ends. `a4_cast` builds it at any scale so every beat shows the same objects.
"""

A4_CABLE = "#9C8462"                           # deep kraft for connectors (ink-edged pipes fuse blocks into one text blob)
A4_ICON = "pantry/ev_icon_blender.png"         # the REAL Blender app icon
A4_TAG = "documented, not run"
A4_XL = -6.25                                  # left edge of a Menlo 32 command block (0.25 units per character)
A4_DX = -6.05                                  # x of the terracotta 'you are here' dot beside indented flag rows


# ═════════════════════════════ cast helpers ═════════════════════════════
def a4_iso(cx, cy, s, W, D, H=0.0):
    """An Iso whose projected footprint W x D x H is centred on the scene point (cx, cy)."""
    ox = cx - (W - D) * C30 * s / 2
    oy = cy - ((W + D) / 2 + H) * s / 2
    return Iso(ox, oy, s)


def a4_socket(x, y, r=0.22, open_=True):
    """The add-on's socket: a ring; a terracotta dot inside while it is open (listening)."""
    ring = Circle(radius=r, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    dot = Dot([x, y, 0], radius=r * 0.38, color=TERRA if open_ else GHOST)
    return VGroup(ring, dot)


def a4_cable(p, q, w=8):
    return Line(np.array([p[0], p[1], 0.0]), np.array([q[0], q[1], 0.0]), color=A4_CABLE, stroke_width=w)


def a4_page(cx, cy, s=1.0):
    """A script / file page (kit page: white slab, ghost lines, terracotta dot), centred on (cx, cy)."""
    return a4_iso(cx, cy, s, 1.1, 1.4, 0.06).page(0, 0, 0, 1.1, 1.4)


def a4_cast(x0=0.0, y0=0.0, k=1.0):
    """The act's cast, designed at k=1 for B29, scaled by k about the origin and shifted by (x0, y0). Returns a dict."""
    def P(x, y):
        return (x0 + x * k, y0 + y * k)
    c = {}
    c["cc"] = a4_iso(*P(-4.7, -0.55), k, 1.3, 1.3, 0.8).box(0, 0, 0, 1.3, 1.3, 0.8)
    stack, lights = a4_iso(*P(-0.9, -0.45), k, 1.2, 1.2, 1.16).server(0, 0, 0, 1.2, 1.2, 0.36, 3)
    c["server"], c["lights"] = stack, lights
    bi = a4_iso(*P(3.9, -0.65), k, 1.5, 1.5, 0.9)
    c["blender"] = bi.box(0, 0, 0, 1.5, 1.5, 0.9)
    c["addon"] = bi.mcp(0.1, 0.75, 0.9, 0.6, 0.6, 0.45)
    c["icon"] = ImageMobject(A4_ICON).set_height(1.15 * k).move_to([*P(4.35, 1.35), 0])
    sx, sy = P(3.08, -0.15)
    c["sock"] = np.array([sx, sy, 0.0])
    c["socket"] = a4_socket(sx, sy, 0.22 * max(k, 0.75))
    c["cc_r"] = np.array([*P(-3.5, -0.5), 0.0])           # Claude Code's right face
    c["srv_l"] = np.array([*P(-1.95, -0.5), 0.0])         # server, left face
    c["srv_r"] = np.array([*P(0.2, -0.45), 0.0])          # server, right face
    c["sock_l"] = np.array([*P(3.08 - 0.24, -0.17), 0.0])  # where the server's line meets the socket ring
    c["land"] = np.array([*P(4.35, -0.3), 0.0])           # where a call lands, on Blender's top face
    c["c1"] = a4_cable(c["cc_r"], c["srv_l"], 8 if k >= 0.7 else 6)
    c["c2"] = a4_cable(c["srv_r"], c["sock_l"], 8 if k >= 0.7 else 6)
    c["c1"].set_z_index(-1); c["c2"].set_z_index(-1)
    return c


def a4_doc(cx, cy, w, h, lines, src, size=34, src_size=32, gap=0.56):
    """README words, shown as the project's own words: an outline page (DIM, no fill behind text) holding the quote lines
    (serif ink, centred) and, last, the source line (version and date). Returns (outline, [line texts], source text)."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([cx, cy, 0])
    n = len(lines) + 1
    y0 = cy + gap * (n - 1) / 2
    txt = [T(s, size).move_to([cx, y0 - i * gap, 0]) for i, s in enumerate(lines)]
    srct = T(src, src_size).move_to([cx, y0 - (n - 1) * gap, 0])
    return box, txt, srct


def a4_mline(s, y, indent=0, color=INK):
    """One Menlo 32 line, left edge at A4_XL + indent characters."""
    return M(s, 32, color).move_to([A4_XL + (indent + len(s) / 2.0) * 0.25, y, 0])


def a4_switch(x, y, on=False):
    """A plain on/off switch (an idea of a setting, not the add-on's panel): outline pill + knob (left = off)."""
    pill = RoundedRectangle(width=0.8, height=0.42, corner_radius=0.21, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    knob = Circle(radius=0.13, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([x + (0.19 if on else -0.19), y, 0])
    return pill, knob


def a4_strike(cx, cy, w, h, color=INK, sw=8):
    return VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=color, stroke_width=sw),
                  Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=color, stroke_width=sw))


# ── B29 · the MCP route: add-on, socket, server, Claude Code (ACT TITLE) ─────────────────────────────────────────
class B29_MCPRoute(Scene):
    def construct(self):
        c = a4_cast()
        title = T("Connect  Claude to Blender", 40).move_to([-3.05, 3.05, 0])   # double space: Pango fuses the single one
        tag = T(A4_TAG, 32).move_to([0.0, -3.05, 0])
        self.add(title, tag)
        until(self, "An add-on inside", lead=0.35)
        bl = T("Blender", 34).move_to([4.35, -2.3, 0])
        self.play(FadeIn(c["blender"]), FadeIn(c["icon"]), FadeIn(bl), run_time=0.5)
        al = T("add-on", 34).move_to([3.0, 0.98, 0])
        self.play(FadeIn(c["addon"], shift=DOWN * 0.25), FadeIn(al), run_time=0.45)
        until(self, "opens a local socket", lead=0.25)
        sl = T("socket", 34).move_to([1.95, 0.3, 0])
        self.play(GrowFromCenter(c["socket"]), FadeIn(sl), run_time=0.5)
        until(self, "a small server", lead=0.3)
        srl = T("server", 34).move_to([-0.9, -2.2, 0])
        self.play(FadeIn(c["server"]), FadeIn(c["lights"]), FadeIn(srl), run_time=0.45)
        self.play(Create(c["c2"]), run_time=0.35)
        until(self, "launched by Claude Code", lead=0.2)
        ccl = T("Claude Code", 34).move_to([-4.7, -2.2, 0])
        self.play(FadeIn(c["cc"]), FadeIn(ccl), Create(c["c1"]), run_time=0.55)
        until(self, "relays", lead=0.25)
        path = VMobject().set_points_as_corners([c["cc_r"], c["srv_l"], c["srv_r"], c["sock"], c["land"]])
        dots = [Dot(c["cc_r"], radius=0.13, color=TERRA) for _ in range(3)]
        self.add(*dots)
        self.play(c["lights"].animate.set_color(TERRA), run_time=0.25)
        self.play(LaggedStart(*[MoveAlongPath(d, path, rate_func=linear) for d in dots], lag_ratio=0.4), run_time=2.2)
        self.play(*[FadeOut(d) for d in dots], run_time=0.2)
        until(self, "That's the M C P route", lead=0.15)
        br = VGroup(Line([-5.6, 1.5, 0], [-5.6, 1.75, 0]), Line([-5.6, 1.75, 0], [3.2, 1.75, 0]),
                    Line([3.2, 1.75, 0], [3.2, 1.5, 0])).set_stroke(DIM, 4)
        ml = T("the MCP route", 36).move_to([-1.2, 2.2, 0])
        self.play(Create(br), FadeIn(ml), run_time=0.45)
        done(self)


# ── B30 · what is known: not run by the course; the README's steps as recorded 27 Sept; 7 releases in 9 days ───────
A4_T0, A4_T1 = -5.6, 5.6                     # the release strip: 27 Sept 2026 .. 6 Oct 2026 (9 days)


def a4_day(d):
    return A4_T0 + d * (A4_T1 - A4_T0) / 9.0


class B30_KnownAndNot(Scene):
    def construct(self):
        c = a4_cast(-2.6, 2.4, 0.5)
        self.add(c["cc"], c["server"], c["lights"], c["blender"], c["addon"], c["icon"], c["socket"], c["c1"], c["c2"])
        until(self, "hasn't run", lead=0.3)
        g1 = DashedLine(c["cc_r"], c["srv_l"], dash_length=0.12, color=GHOST, stroke_width=6)
        g2 = DashedLine(c["srv_r"], c["sock_l"], dash_length=0.12, color=GHOST, stroke_width=6)
        tag = T(A4_TAG, 36).move_to([3.4, 2.4, 0])
        self.play(FadeOut(c["c1"]), FadeOut(c["c2"]), Create(g1), Create(g2), c["socket"][1].animate.set_color(GHOST),
                  FadeIn(tag), run_time=0.6)
        until(self, "These steps come from", lead=0.2)
        box, _, head = a4_doc(-2.2, -0.05, 7.6, 2.55, [], "README, version 2.1.1 · 27 Sept 2026")
        head.move_to([-2.2, 0.82, 0])
        steps = ["1. Install uv", "2. Add the MCP server to your client", "3. Install the Blender addon"]
        widths = [2.08, 6.89, 5.08]                      # measured EB Garamond 36 widths (Text(...).width)
        rows = [T(s, 36).move_to([-5.55 + w / 2, 0.22 - i * 0.6, 0]) for i, (s, w) in enumerate(zip(steps, widths))]
        self.play(Create(box), FadeIn(head), run_time=0.45)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.25)
        until(self, "as recorded on", lead=0.15)
        axis = Line([A4_T0 - 0.2, -2.55, 0], [A4_T1 + 0.2, -2.55, 0], color=DIM, stroke_width=4)
        d0 = Dot([A4_T0, -2.25, 0], radius=0.12, color=TERRA)
        l0 = T("2.1.1", 32).move_to([A4_T0 + 0.68, -2.22, 0])
        day0 = T("27 Sept", 32).move_to([A4_T0 + 0.05, -3.02, 0])
        self.play(Create(axis), FadeIn(d0), FadeIn(l0), FadeIn(day0), run_time=0.5)
        until(self, "And the project changes fast", lead=0.6)
        rel = [(3, 0), (3, 1), (8, 0), (8, 1), (8, 2), (8, 3), (9, 0)]    # 2.1.2, 2.1.3 (30 Sept); 2.1.5-2.1.8 (5 Oct); 2.1.9 (6 Oct)
        for d, j in rel:
            self.play(GrowFromCenter(Dot([a4_day(d), -2.25 + 0.32 * j, 0], radius=0.11, color=INK)), run_time=0.09)
        l9 = T("2.1.9", 32).move_to([A4_T1, -1.82, 0])
        day9 = T("6 Oct", 32).move_to([A4_T1 - 0.1, -3.02, 0])
        cnt = T("7 releases in 9 days", 34).move_to([1.15, -1.75, 0])
        self.play(FadeIn(l9), FadeIn(day9), FadeIn(cnt), run_time=0.35)
        done(self)


# ── B34 · step three: the add-on; Edit > Preferences > Add-ons (REAL captures); the README's words for the row ────────
class B34_AddOn(Scene):
    """The real dark Blender captures land AFTER the clip midpoint (GATE T reads a dark capture's interior as stacked text blobs);
    before it, the shell and Blender's real icon carry "in Blender"."""
    def construct(self):
        shell = ImageMobject("pantry/a4_shell_install_addon.png").set_width(12.2).move_to([0.0, 2.45, 0])
        self.add(shell)                                   # the toolkit's plain shell: the command, no output, "documented, not run"
        until(self, "Then, in Blender", lead=0.2)
        ic = ImageMobject(A4_ICON).set_height(0.95).move_to([-5.55, -0.1, 0])
        il = T("Blender", 32).move_to([-5.55, -1.0, 0])
        cap = T("real Blender 5.1.2 windows", 32).move_to([-2.0, -2.45, 0])
        self.play(FadeIn(ic), FadeIn(il), run_time=0.45)
        until(self, "Preferences", lead=0.0)              # lands just after the midpoint, on the word
        edit = ImageMobject("pantry/a4_edit_menu_prefs.png").set_width(3.0).move_to([-3.25, -0.1, 0])     # REAL Blender Edit menu
        el = T("Edit menu", 32).move_to([-3.25, -1.0, 0])
        d1 = Dot([-1.6, -0.36, 0], radius=0.1, color=TERRA)                                              # beside "Preferences..."
        self.play(FadeIn(edit), FadeIn(el), FadeIn(d1), FadeIn(cap), run_time=0.35)
        until(self, "Add-ons, and", lead=0.35)
        a1 = Arrow([-1.47, -0.36, 0], [-1.1, -0.2, 0], buff=0, color=INK, stroke_width=5, tip_length=0.14)
        prefs = ImageMobject("pantry/a4_prefs_addons_tab.png").set_height(1.65).move_to([0.45, -0.1, 0])  # REAL Preferences, Add-ons tab
        pl = T("Preferences", 32).move_to([0.45, -1.35, 0])
        d2 = Dot([2.08, -0.2, 0], radius=0.1, color=TERRA)                                               # beside "Add-ons"
        self.play(Create(a1), FadeIn(prefs), FadeIn(pl), FadeIn(d2), run_time=0.4)
        until(self, "and enable", lead=0.1)
        a2 = Arrow([2.21, -0.2, 0], [2.6, -0.2, 0], buff=0, color=INK, stroke_width=5, tip_length=0.14)
        box, txt, src = a4_doc(4.45, -0.15, 3.9, 2.6, ["\u201cenable Interface:", "MCP for Blender\u201d", "README 2.1.1"],
                               "27 Sept 2026", size=34, gap=0.52)
        self.play(Create(a2), Create(box), run_time=0.3)
        self.play(FadeIn(txt[0]), FadeIn(txt[1]), run_time=0.4)
        self.play(FadeIn(txt[2]), FadeIn(src), run_time=0.3)
        done(self)


# ── B35 · the server starts when Blender opens; press N, the tab; services off; a fresh Claude Code session ────────────
class B35_Checks(Scene):
    def construct(self):
        c = a4_cast(0.2, 1.75, 0.7)
        self.add(c["blender"], c["addon"])
        until(self, "starts its server", lead=0.25)
        self.play(FadeIn(c["icon"]), GrowFromCenter(c["socket"]), run_time=0.5)
        # README words (2.1.9): one sentence, then the tab instruction as two verbatim fragments (its arrow glyph is left out)
        box = RoundedRectangle(width=12.0, height=1.9, corner_radius=0.18, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([0.0, -2.4, 0])
        q1 = T("\u201cThe addon starts its server when Blender opens.\u201d", 32).move_to([0.0, -2.1, 0])
        src = T("README 2.1.9 \u00b7 6 Oct 2026", 32).move_to([0.0, -2.9, 0])
        self.play(Create(box), FadeIn(q1), FadeIn(src), run_time=0.45)
        until(self, "To check, press N", lead=0.2)
        key = RoundedRectangle(width=0.95, height=0.95, corner_radius=0.16, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([-5.0, -0.55, 0])
        kn = T("N", 44).move_to([-5.0, -0.55, 0])
        q2a = T("\u201cTo check, press N in the 3D viewport\u201d", 32).move_to([0.0, -1.85, 0])
        q2b = T("\u201copen the MCP for Blender tab\u201d", 32).move_to([0.0, -2.37, 0])
        self.play(Create(key), FadeIn(kn), FadeOut(q1), run_time=0.4)
        self.play(FadeIn(q2a), FadeIn(q2b), run_time=0.35)
        until(self, "Every service", lead=-0.3)          # the row starts just after the clip midpoint
        sw = []
        for i in range(6):
            pill, knob = a4_switch(1.0 + i * 0.9, -0.4)
            sw += [pill, knob]
        sl = T("services and downloads: off", 34).move_to([3.25, -1.0, 0])
        for i in range(6):
            self.play(Create(sw[2 * i]), FadeIn(sw[2 * i + 1]), run_time=0.14)
        self.play(FadeIn(sl), run_time=0.3)
        until(self, "start a fresh Claude Code session", lead=0.25)
        nl = T("new session", 34).move_to([-3.09, 0.25, 0])
        self.play(FadeIn(c["cc"]), FadeIn(nl), FadeIn(c["server"]), FadeIn(c["lights"]), Create(c["c1"]), Create(c["c2"]), run_time=0.55)
        until(self, "so it sees the server", lead=0.15)
        d = Dot(c["cc_r"], radius=0.11, color=TERRA)
        self.add(d)
        self.play(d.animate.move_to(c["srv_l"]), c["lights"].animate.set_color(TERRA), run_time=0.4, rate_func=linear)
        done(self)


# ── B36 · the safety note: Python that Claude writes runs with no guard; the socket has no authentication ──────────────
class B36_OpenPort(Scene):
    def construct(self):
        c = a4_cast(0.2, 0.5, 1.0)
        tag = T(A4_TAG, 32).move_to([-4.15, 3.05, 0])
        self.add(c["cc"], c["server"], c["lights"], c["blender"], c["addon"], c["icon"], c["socket"], c["c1"], c["c2"], tag)
        ccl = T("Claude Code", 32).move_to([-4.5, -1.6, 0])
        self.add(ccl)
        until(self, "runs Python that Claude writes", lead=0.4)
        pg = a4_page(-4.5, 1.15, 0.45)
        pyl = T("Python", 34).move_to([-4.5, 1.95, 0])
        rp = T("runs Python", 34).move_to([4.55, 2.85, 0])
        self.play(FadeIn(pg, shift=DOWN * 0.2), FadeIn(pyl), run_time=0.4)
        until(self, "inside your Blender", lead=0.5)
        self.play(pg.animate.move_to(c["srv_l"] + np.array([0.0, 0.55, 0])), FadeOut(pyl), run_time=0.45, rate_func=linear)
        self.play(pg.animate.move_to(c["sock"] + np.array([-0.55, 0.45, 0])), run_time=0.5, rate_func=linear)
        self.play(pg.animate.move_to(c["sock"]).scale(0.25), run_time=0.3)
        self.play(FadeOut(pg), FadeIn(rp), Indicate(c["socket"], color=TERRA, scale_factor=1.3), run_time=0.45)
        until(self, "with no guard", lead=0.35)
        posts = VGroup(Line([1.85, -0.35, 0], [1.85, 0.75, 0]), Line([2.35, -0.35, 0], [2.35, 0.75, 0])).set_stroke(INK, 8)
        ng = T("no guard", 34).move_to([1.6, -0.85, 0])
        self.play(Create(posts), FadeIn(ng), run_time=0.45)
        until(self, "The readme says", lead=0.2)
        box, txt, src = a4_doc(0.0, -2.6, 12.0, 1.3, ["“the addon’s socket server has no authentication or encryption”"],
                               "README 2.1.9 · 6 Oct 2026", size=32, gap=0.52)
        self.play(Create(box), FadeIn(txt[0]), FadeIn(src), run_time=0.5)
        until(self, "anyone who can reach", lead=0.3)
        xs = [-1.55, -0.35, 0.85]
        outs = VGroup(*[RoundedRectangle(width=0.8, height=0.6, corner_radius=0.12, fill_opacity=0, stroke_color=DIM,
                                         stroke_width=5).move_to([x, 2.55, 0]) for x in xs])
        anl = T("anyone", 34).move_to([2.35, 2.55, 0])
        paths = VGroup(*[DashedLine([x, 2.2, 0], c["sock"] + np.array([-0.12, 0.2, 0]), dash_length=0.12, color=DIM, stroke_width=4)
                         for x in xs])
        paths.set_z_index(-1)
        self.play(Create(outs), FadeIn(anl), Create(paths), run_time=0.45)
        until(self, "can run Python inside", lead=0.6)
        ps = [a4_page(x, 2.55, 0.3) for x in xs]
        for p in ps:
            self.add(p)
        self.play(*[p.animate.move_to(c["sock"]).scale(0.3) for p in ps], run_time=0.55, rate_func=linear)
        self.play(*[FadeOut(p) for p in ps], Indicate(c["socket"], color=TERRA, scale_factor=1.3), run_time=0.45)
        done(self)


# ── B37A · localhost; save first; the add-on off when not in use (the socket opens whenever Blender starts with it on) ──
class B37A_ThreeHabits(Scene):
    def construct(self):
        # 1 · localhost: a wall round this machine; a call from outside stops at it
        wall = RoundedRectangle(width=2.6, height=2.5, corner_radius=0.25, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-3.9, 0.45, 0])
        ic1 = ImageMobject(A4_ICON).set_height(0.85).move_to([-4.15, 0.95, 0])
        so1 = a4_socket(-4.45, -0.15, 0.22)
        self.add(ic1, so1)
        until(self, "keep the port on localhost", lead=0.3)
        out = Dot([-6.0, -0.15, 0], radius=0.13, color=TERRA)
        lh = M("localhost", 32).move_to([-3.9, -1.3, 0])
        self.play(Create(wall), FadeIn(out), FadeIn(lh), run_time=0.45)
        self.play(out.animate.move_to([-5.38, -0.15, 0]), run_time=0.4, rate_func=linear)
        # 2 · save your work first
        until(self, "Save your work first", lead=0.25)
        pg = a4_page(0.0, 0.5, 1.0)
        sv = T("save first", 34).move_to([0.0, -1.3, 0])
        self.play(FadeIn(pg, shift=DOWN * 0.2), FadeIn(sv), run_time=0.4)
        self.play(Create(check(0.65, 1.55, 0.3)), run_time=0.35)
        # 3 · the add-on off: the switch goes off and the socket closes
        pill, knob = a4_switch(4.1, 1.55, on=True)
        ic3 = ImageMobject(A4_ICON).set_height(0.85).move_to([3.55, 0.2, 0])
        so3 = a4_socket(4.65, 0.2, 0.25)
        self.play(FadeIn(pill), FadeIn(knob), FadeIn(ic3), FadeIn(so3), run_time=0.35)
        until(self, "turn the add-on off", lead=0.2)
        of = T("add-on off", 34).move_to([4.1, -1.3, 0])
        shut = Line([4.47, 0.2, 0], [4.83, 0.2, 0], color=INK, stroke_width=8)
        self.play(knob.animate.move_to([3.91, 1.55, 0]), so3[1].animate.set_color(GHOST), FadeIn(of), run_time=0.5)
        self.play(Create(shut), run_time=0.3)
        # the reason: on every start it would open; off, it stays shut
        until(self, "the socket opens whenever", lead=0.3)
        self.play(ic3.animate.set_opacity(0.15), run_time=0.4)                    # Blender closed ...
        until(self, "Blender starts", lead=0.3)
        self.play(ic3.animate.set_opacity(1.0), Indicate(VGroup(so3, shut), color=INK, scale_factor=1.12), run_time=0.6)   # ... starts: stays shut
        done(self)


# ── B37B · don't open files from people you don't trust while the server is running ────────────────────────────────────
class B37B_Untrusted(Scene):
    def construct(self):
        c = a4_cast(0.8, 0.2, 1.0)
        rl = T("server running", 34).move_to([4.7, -2.15, 0])
        self.add(c["blender"], c["addon"], c["icon"], c["socket"])
        pg = a4_page(-4.6, -0.1, 1.0)
        ul = T("a .blend from a stranger", 34).move_to([-4.0, -1.5, 0])
        self.add(pg, ul)
        until(self, "open Blender files", lead=0.3)
        self.play(pg.animate.shift(RIGHT * 2.9), ul.animate.shift(RIGHT * 1.2), run_time=0.75)
        until(self, "people you don't trust", lead=0.35)
        x = a4_strike(1.6, -0.1, 0.8, 0.8)
        dl = T("don't open", 34).move_to([1.6, 1.05, 0])
        self.play(Create(x), FadeIn(dl), run_time=0.4)
        until(self, "while the server is running", lead=0.2)
        self.play(FadeIn(rl), Indicate(c["socket"], color=TERRA, scale_factor=1.3), run_time=0.6)
        done(self)


# ── B38 · it won't connect: that's data. About two hours, every step logged; then the script route ────────────────────
class B38_TimeBox(Scene):
    """Spread across the full width (Gate V fill): the broken connection runs along the top, the clock ring left, the log
    card centre, and the script route lands on the right on its words."""
    def construct(self):
        # no connection: the server's line stops short of the socket
        srv, lts = a4_iso(-5.1, 2.7, 0.5, 1.2, 1.2, 1.16).server(0, 0, 0, 1.2, 1.2, 0.36, 3)
        so = a4_socket(-0.15, 2.7, 0.22, open_=False)
        ca = a4_cable((-4.45, 2.7), (-2.65, 2.7), 7)
        cb = a4_cable((-1.75, 2.7), (-0.42, 2.7), 7)
        self.add(srv, lts, so)
        until(self, "doesn't connect", lead=0.3)
        gap = a4_strike(-2.2, 2.7, 0.36, 0.36, sw=6)
        nc = T("no connection", 36).move_to([3.3, 2.7, 0])
        self.play(Create(ca), Create(cb), Create(gap), FadeIn(nc), run_time=0.5)
        until(self, "that's data", lead=0.2)
        log = RoundedRectangle(width=4.2, height=3.3, corner_radius=0.2, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-0.15, -0.3, 0])
        lh = M("FRICTIONAL.md", 32).move_to([-0.15, 0.85, 0])
        self.play(Create(log), FadeIn(lh), run_time=0.4)
        until(self, "about two hours", lead=0.25)
        ring = Circle(radius=1.5, stroke_color=GHOST, stroke_width=14).move_to([-4.55, -0.3, 0])
        hl = T("about 2 hours", 36).move_to([-4.55, -2.45, 0])
        self.play(Create(ring), FadeIn(hl), run_time=0.3)
        arc = Arc(radius=1.5, start_angle=PI / 2, angle=-TAU * 0.999, color=INK, stroke_width=14).move_to([-4.55, -0.3, 0])
        self.play(Create(arc), run_time=1.6, rate_func=linear)
        until(self, "each step", lead=0.3)
        rows = VGroup()
        for i in range(3):
            y = 0.1 - i * 0.65
            rows.add(VGroup(Dot([-1.85, y, 0], radius=0.1, color=TERRA), Line([-1.55, y, 0], [1.5 - 0.45 * (i % 2), y, 0], color=DIM, stroke_width=9)))
        el = T("each step, its exact error", 36).move_to([-0.15, -2.45, 0])
        for r in rows:
            self.play(FadeIn(r), run_time=0.22)
        self.play(FadeIn(el), run_time=0.3)
        until(self, "switch to the script route", lead=0.3)
        fork = Arrow([2.15, -0.3, 0], [2.85, -0.3, 0], buff=0, color=INK, stroke_width=6, tip_length=0.22)
        sr = T("script route", 36).move_to([4.5, 1.5, 0])
        self.play(Create(fork), FadeIn(sr), run_time=0.45)
        until(self, "Claude writes a Blender script", lead=0.2)
        sp = a4_page(3.6, -0.3, 0.85)
        spl = T("script", 34).move_to([3.6, 0.65, 0])
        self.play(FadeIn(sp), FadeIn(spl), run_time=0.4)
        until(self, "and you run Blender", lead=0.45)
        a2 = Arrow([4.35, -0.3, 0], [4.8, -0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.16)
        bi = ImageMobject(A4_ICON).set_height(1.0).move_to([5.45, -0.3, 0])
        nw = T("no window", 32).move_to([5.2, -1.45, 0])
        self.play(Create(a2), FadeIn(bi), FadeIn(nw), run_time=0.45)
        done(self)


# ── B39A · the command (REAL, as run for the lantern): -b, --factory-startup, --python; its real output ──────────────────
A4_RY = [3.0, 2.3, 1.6, 0.9, 0.2]            # the command block rows


def a4_cmd_rows(exit_flag_color=GHOST):
    return [a4_mline("/Applications/Blender.app/Contents/MacOS/Blender \\", A4_RY[0]),
            a4_mline("-b \\", A4_RY[1], 2), a4_mline("--factory-startup \\", A4_RY[2], 2),
            a4_mline("--python-exit-code 1 \\", A4_RY[3], 2, exit_flag_color),
            a4_mline("--python build_lantern.py", A4_RY[4], 2)]


class B39A_Command(Scene):
    def construct(self):
        rows = a4_cmd_rows()
        self.play(FadeIn(VGroup(*rows)), run_time=0.45)
        # what it printed lands with the command (recorded output, excerpt), so the frame is full while the flags are read
        until(self, "that command", lead=0.1)
        oh = T("recorded output, excerpt", 32).move_to([-3.2, -0.6, 0])
        out = [a4_mline("Blender 5.1.2 | metric, 1 unit = 1 m | Z up", -1.15),     # build_lantern.log line 1
               a4_mline("\u2026", -1.62),                                           # lines 2-10 omitted
               a4_mline("exported lantern.glb (16520 bytes), +Y Up on", -2.09),    # line 11
               a4_mline("\u2026", -2.56),                                           # lines 12-13 omitted
               a4_mline("Blender quit", -3.03)]                                     # line 14
        rule = Line([-6.2, -0.25, 0], [6.2, -0.25, 0], color=GHOST, stroke_width=4)
        self.play(Create(rule), FadeIn(oh), *[FadeIn(o) for o in out], run_time=0.4)
        dot = Dot([A4_DX, A4_RY[1], 0], radius=0.12, color=TERRA)
        until(self, "Dash b", lead=0.2)
        l1 = T("no window", 34).move_to([3.2, A4_RY[1], 0])
        self.play(FadeIn(dot), FadeIn(l1), run_time=0.4)
        until(self, "Factory startup", lead=0.15)
        l2 = T("your settings, skipped", 34).move_to([3.2, A4_RY[2], 0])
        self.play(dot.animate.move_to([A4_DX, A4_RY[2], 0]), run_time=0.25)
        self.play(FadeIn(l2), run_time=0.35)
        until(self, "Python runs the script", lead=0.5)
        l3 = T("runs the script", 34).move_to([3.2, A4_RY[4], 0])
        self.play(dot.animate.move_to([A4_DX, A4_RY[4], 0]), run_time=0.25)
        self.play(FadeIn(l3), run_time=0.3)
        done(self)


# ── B39B · --python-exit-code 1: the same error, exit 1 with it, exit 0 without it (REAL output) ──────────────────────
class B39B_ExitCode(Scene):
    def construct(self):
        flag = a4_mline("--python-exit-code 1", 2.95, 2)
        dot = Dot([A4_DX, 2.95, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(flag), FadeIn(dot), run_time=0.4)
        until(self, "makes a crashing script", lead=0.3)
        wl = T("with the flag", 34).move_to([2.6, 2.95, 0])
        e1 = a4_mline("ValueError: this script fails on purpose", 2.3)
        self.play(FadeIn(wl), FadeIn(e1), run_time=0.4)
        until(self, "fail loudly", lead=0.35)
        e2 = a4_mline("Error: script failed, file: 'bad.py', exiting.", 1.7)
        k1 = a4_mline("$ echo $?", 1.05)
        n1 = T("1", 88).move_to([-3.15, 1.0, 0])
        x1 = T("exit code", 32).move_to([-1.85, 1.0, 0])
        self.play(FadeIn(e2), FadeIn(k1), FadeIn(n1), FadeIn(x1), run_time=0.45)
        until(self, "Without it", lead=0.0)
        rule = Line([-6.2, 0.35, 0], [6.2, 0.35, 0], color=GHOST, stroke_width=4)
        wo = T("without the flag", 34).move_to([-4.7, -0.25, 0])
        e3 = a4_mline("ValueError: this script fails on purpose", -0.9)
        self.play(Create(rule), FadeIn(wo), FadeIn(e3), run_time=0.45)
        until(self, "exits with zero", lead=0.3)
        k0 = a4_mline("$ echo $?", -1.55)
        n0 = T("0", 88).move_to([-3.15, -1.6, 0])
        x0_ = T("exit code", 32).move_to([-1.85, -1.6, 0])
        self.play(FadeIn(k0), FadeIn(n0), FadeIn(x0_), run_time=0.4)
        until(self, "raises an error", lead=0.3)
        sp = Dot([4.1, -0.9, 0], radius=0.12, color=TERRA)
        rec = T("recorded output, excerpts", 32).move_to([2.6, -2.75, 0])
        self.play(FadeIn(sp), FadeIn(rec), run_time=0.35)
        done(self)


# ── B40 · an honest failed attempt + a working script fallback: up to 6 of the 8 MCP points, not all 8 ────────────────
class B40_SixOfEight(Scene):
    def construct(self):
        x0, cw, gp, y = -3.0, 0.95, 0.1, 0.3
        cells = [Rectangle(width=cw, height=0.9, fill_color=BAR1, fill_opacity=0, stroke_color=DIM, stroke_width=4)
                 .move_to([x0 + cw / 2 + i * (cw + gp), y, 0]) for i in range(8)]
        self.add(*cells)
        until(self, "honest, specific account", lead=0.3)
        h1 = T("honest account", 34).move_to([-4.75, 0.62, 0])
        self.play(FadeIn(h1), run_time=0.35)
        until(self, "working script fallback", lead=0.3)
        h2 = T("+ script fallback", 34).move_to([-4.75, -0.02, 0])
        self.play(FadeIn(h2), run_time=0.35)
        until(self, "earns up to six", lead=0.3)
        for i in range(6):
            self.play(cells[i].animate.set_fill(BAR1, 1), run_time=0.11)
        xe = x0 + 6 * cw + 5 * gp
        br = VGroup(Line([x0, -0.35, 0], [x0, -0.55, 0]), Line([x0, -0.55, 0], [xe, -0.55, 0]),
                    Line([xe, -0.55, 0], [xe, -0.35, 0])).set_stroke(INK, 5)
        u6 = T("up to 6", 36).move_to([(x0 + xe) / 2, -1.05, 0])
        self.play(Create(br), FadeIn(u6), run_time=0.4)
        until(self, "of the eight", lead=0.2)
        x8 = x0 + 8 * cw + 7 * gp
        top = VGroup(Line([x0, 0.95, 0], [x0, 1.15, 0]), Line([x0, 1.15, 0], [x8, 1.15, 0]),
                     Line([x8, 1.15, 0], [x8, 0.95, 0])).set_stroke(DIM, 4)
        e8 = T("8 MCP points", 36).move_to([(x0 + x8) / 2, 1.6, 0])
        self.play(Create(top), FadeIn(e8), run_time=0.4)
        until(self, "Not all eight", lead=0.15)
        s7 = a4_strike(x0 + cw / 2 + 6 * (cw + gp), y, 0.6, 0.6, sw=6)
        s8 = a4_strike(x0 + cw / 2 + 7 * (cw + gp), y, 0.6, 0.6, sw=6)
        na = T("not all 8", 36).move_to([x0 + 7 * (cw + gp), -1.05, 0])
        self.play(Create(s7), Create(s8), FadeIn(na), run_time=0.4)
        done(self)
