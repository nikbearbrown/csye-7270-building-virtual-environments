"""ACT II · Two Ways to Let an Agent Drive Blender  (B08–B10, B12–B18 Manim; B11 is a Remotion BrowserCapture, see lanes/act2.json)

One cast for the act, so the two routes read as two consistent things across eleven beats:
  LIVE route   = the agent (rounded box with a spark) -> a small dark MCP server block -> a socket ring on the edge of the REAL Blender window
                 (pantry/blender_window.png, a real Blender 5.1.2 screenshot). Tool calls are terracotta dots riding deep-kraft cables.
  SCRIPT route = a script PAGE (white slab, terracotta dot) -> Blender's real icon (no window) -> a .glb file; the window stays a ghost outline
                 with a strike through it. The command line is Menlo text, one flag per row (same rows in B14 and B15).
Real things on screen: Blender's window and icon, the real post render (a2_post.png), the real exit-code output (evidence/act2/exit_code_transcript.txt),
the real Lab-page warning (a2_lab_warning.png, captured 2026-10-06; evidence/act2/capture_pages.py). Nothing is drawn onto the Blender window itself.
"""

A2_ASPECT = 3456.0 / 2006.0          # the real window screenshot
A2_CABLE = "#9C8462"                 # deep kraft for connectors (ink-edged pipes fuse blocks into one text blob)
A2_XL = -6.25                        # left edge of the command block (Menlo 32 = 0.25 units per character)
A2_DX = -6.05                        # x of the terracotta 'you are here' dot beside the flag rows (flags are indented two characters)


# ═════════════════════════════ cast helpers ═════════════════════════════
def a2_iso(cx, cy, s, W, D, H=0.0):
    """An Iso whose projected footprint W x D x H is centred on the scene point (cx, cy)."""
    ox = cx - (W - D) * C30 * s / 2
    oy = cy - ((W + D) / 2 + H) * s / 2
    return Iso(ox, oy, s)


def a2_agent(x, y, s=1.0):
    """The coding agent: a rounded box with a four-point spark in it (generic, not any one product)."""
    box = RoundedRectangle(width=1.5 * s, height=1.2 * s, corner_radius=0.22 * s, fill_color=CARD, fill_opacity=1,
                           stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    r, q = 0.34 * s, 0.09 * s
    star = Polygon([x, y + r, 0], [x + q, y + q, 0], [x + r, y, 0], [x + q, y - q, 0], [x, y - r, 0], [x - q, y - q, 0],
                   [x - r, y, 0], [x - q, y + q, 0], fill_color=INK, fill_opacity=1, stroke_width=0)
    return VGroup(box, star)


def a2_term(x, y, s=1.0):
    """A terminal chip: rounded box, a > chevron and an underscore (commands)."""
    box = RoundedRectangle(width=1.5 * s, height=1.2 * s, corner_radius=0.22 * s, fill_opacity=0,
                           stroke_color=INK, stroke_width=5).move_to([x, y, 0])
    a = Line([x - 0.38 * s, y + 0.24 * s, 0], [x - 0.1 * s, y, 0], color=INK, stroke_width=7)
    b = Line([x - 0.1 * s, y, 0], [x - 0.38 * s, y - 0.24 * s, 0], color=INK, stroke_width=7)
    u = Line([x + 0.06 * s, y - 0.26 * s, 0], [x + 0.42 * s, y - 0.26 * s, 0], color=INK, stroke_width=7)
    return VGroup(box, a, b, u)


def a2_page(cx, cy, s=1.0):
    """The script page (kit page: white slab, ghost lines, one terracotta dot), centred on (cx, cy)."""
    return a2_iso(cx, cy, s, 1.1, 1.4, 0.06).page(0, 0, 0, 1.1, 1.4)


def a2_server(cx, cy, s=1.0):
    """The small MCP server: the kit's dark block with two ports (the act's one dark object)."""
    return a2_iso(cx, cy, s, 1.3, 1.3, 0.7).mcp(0, 0, 0)


def a2_window(cx, cy, w):
    """The REAL Blender window (screenshot) with an ink outline. Returns (image, outline, height)."""
    h = w / A2_ASPECT
    img = ImageMobject("pantry/blender_window.png").set_height(h).move_to([cx, cy, 0])
    frame = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([cx, cy, 0])
    return img, frame, h


def a2_icon(cx, cy, h):
    return ImageMobject("pantry/icon_blender.png").set_height(h).move_to([cx, cy, 0])


def a2_ghost_window(cx, cy, w, h):
    """An empty window outline (where the live route's window would be): DIM frame + title bar."""
    fr = Rectangle(width=w, height=h, stroke_color=DIM, stroke_width=5, fill_opacity=0).move_to([cx, cy, 0])
    bar = Line([cx - w / 2, cy + h / 2 - 0.4, 0], [cx + w / 2, cy + h / 2 - 0.4, 0], color=DIM, stroke_width=4)
    return VGroup(fr, bar)


def a2_strike(cx, cy, w, h, color=INK):
    """Two crossing lines (a cross-out) over an object of size w x h."""
    return VGroup(Line([cx - w / 2, cy + h / 2, 0], [cx + w / 2, cy - h / 2, 0], color=color, stroke_width=8),
                  Line([cx - w / 2, cy - h / 2, 0], [cx + w / 2, cy + h / 2, 0], color=color, stroke_width=8))


def a2_socket(x, y):
    """The add-on's socket: a ring with a terracotta dot, sitting on the edge of the window."""
    ring = Circle(radius=0.3, fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=6).move_to([x, y, 0])
    dot = Dot([x, y, 0], radius=0.09, color=TERRA)
    return VGroup(ring, dot)


def a2_cable(p, q):
    return Line(p, q, color=A2_CABLE, stroke_width=8)


def a2_eye(x, y, s=1.0):
    """An eye (review): almond outline plus a pupil."""
    top = ArcBetweenPoints([x - 0.62 * s, y, 0], [x + 0.62 * s, y, 0], angle=-1.0, color=INK, stroke_width=6)
    bot = ArcBetweenPoints([x - 0.62 * s, y, 0], [x + 0.62 * s, y, 0], angle=1.0, color=INK, stroke_width=6)
    return VGroup(top, bot, Circle(radius=0.2 * s, stroke_color=INK, stroke_width=6, fill_opacity=0).move_to([x, y, 0]),
                  Dot([x, y, 0], radius=0.07 * s, color=INK))


def a2_mline(s, y, indent=0, color=INK):
    """One line of the command block (Menlo 32), left edge at A2_XL + indent characters."""
    return M(s, 32, color).move_to([A2_XL + (indent + len(s) / 2.0) * 0.25, y, 0])


# the command block rows (y). The row at A2_Y3 is empty in B14 and holds `--python-exit-code 1 \` in B15
A2_Y0, A2_Y1, A2_Y2, A2_Y3, A2_Y4 = 3.05, 2.2, 1.35, 0.5, -0.35


def a2_cmd(with_flag=False):
    """The real command, one flag per row: (path, -b, --factory-startup, [--python-exit-code 1], --python script). Same rows in B14 and B15."""
    rows = [a2_mline("/Applications/Blender.app/Contents/MacOS/Blender \\", A2_Y0),
            a2_mline("-b \\", A2_Y1, 2), a2_mline("--factory-startup \\", A2_Y2, 2),
            a2_mline("--python tools/blender/build_checkpoint_post.py", A2_Y4, 2)]
    flag = a2_mline("--python-exit-code 1 \\", A2_Y3, 2)
    return rows, flag


# ── B08 · what a coding agent is, then the two ways ────────────────────────────────────────────────────────
class B08_TwoWays(Scene):
    def construct(self):
        ag = a2_agent(-5.0, 0.1)
        ag_l = T("coding agent", 34).move_to([-5.0, -1.15, 0])
        self.play(FadeIn(ag), FadeIn(ag_l), run_time=0.5)
        until(self, "edits files", lead=0.4)
        pg = a2_page(-2.0, 1.45, 0.8)
        pg_l = T("files", 34).move_to([-0.55, 1.45, 0])
        ar1 = Arrow([-4.1, 0.45, 0], [-3.25, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(ar1), FadeIn(pg), FadeIn(pg_l), run_time=0.5)
        until(self, "runs commands", lead=0.4)
        tm = a2_term(-2.0, -1.35, 0.9)
        tm_l = T("commands", 34).move_to([-0.2, -1.35, 0])
        ar2 = Arrow([-4.1, -0.25, 0], [-3.1, -0.95, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(ar2), FadeIn(tm), FadeIn(tm_l), run_time=0.5)
        until(self, "When it builds a model", lead=0.0)
        self.play(FadeOut(VGroup(pg, pg_l, ar1, tm, tm_l, ar2)), run_time=0.4)
        img, fr, h = a2_window(2.9, 1.55, 3.6)
        pg2 = a2_page(2.9, -1.55, 0.95)
        self.play(FadeIn(img), Create(fr), FadeIn(pg2), run_time=0.5)
        until(self, "two ways", lead=1.4)
        a_top = Arrow([-4.05, 0.5, 0], [0.95, 1.45, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
        a_bot = Arrow([-4.05, -0.2, 0], [1.65, -1.5, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
        self.play(Create(a_top), Create(a_bot), run_time=0.6)
        l_live = T("live", 38).move_to([2.9, 0.1, 0])
        l_scr = T("script", 38).move_to([2.9, -2.85, 0])
        self.play(FadeIn(l_live), FadeIn(l_scr), run_time=0.4)
        done(self)


# ── B09 · the live route: add-on socket, small server, tool calls into the open window ──────────────────────
class B09_LiveRoute(Scene):
    def construct(self):
        img, fr, h = a2_window(2.95, 0.25, 6.2)
        win_l = T("Blender, open", 34).move_to([2.95, -1.95, 0])
        note = T("route documented, not run", 32).move_to([0.0, -3.0, 0])      # honesty: the MCP route was read about, never run
        self.play(FadeIn(img), Create(fr), FadeIn(win_l), FadeIn(note), run_time=0.4)
        until(self, "opens a local socket", lead=0.9)
        sock = a2_socket(-0.15, 0.25)
        sock_l = T("socket", 34).move_to([-0.95, 1.0, 0])
        self.play(GrowFromCenter(sock), FadeIn(sock_l), run_time=0.5)
        until(self, "a small server", lead=1.5)
        srv = a2_server(-2.85, -0.1, 0.95)
        srv_l = T("server", 34).move_to([-2.85, -1.45, 0])
        self.play(FadeIn(srv), FadeIn(srv_l), run_time=0.4)
        ag = a2_agent(-5.45, 0.15, 0.9)
        ag_l = T("agent", 34).move_to([-5.45, -0.75, 0])
        self.play(FadeIn(ag), FadeIn(ag_l), run_time=0.3)
        c1 = a2_cable([-4.75, 0.15, 0], [-3.85, 0.05, 0])
        c2 = a2_cable([-1.7, -0.05, 0], [-0.45, 0.22, 0])
        c1.set_z_index(-1); c2.set_z_index(-1)
        self.play(Create(c1), Create(c2), run_time=0.4)
        until(self, "relays the agent's tool calls", lead=0.0)
        ring = Rectangle(width=6.4, height=h + 0.2, stroke_color=TERRA, stroke_width=8, fill_opacity=0).move_to([2.95, 0.25, 0])
        for i in range(3):
            d = Dot([-4.7, 0.15, 0], radius=0.14, color=TERRA)
            self.add(d)
            self.play(d.animate.move_to([-3.2, 0.05, 0]), run_time=0.25, rate_func=linear)
            self.play(d.animate.move_to([-0.15, 0.25, 0]), run_time=0.4, rate_func=linear)
            if i == 2:
                self.play(d.animate.move_to([1.4, 0.25, 0]), Create(ring), run_time=0.45, rate_func=linear)
            else:
                self.play(d.animate.move_to([1.4, 0.25, 0]), run_time=0.25, rate_func=linear)
            self.play(FadeOut(d), run_time=0.1)
        until(self, "M C P route", lead=0.3)
        mcp_l = T("MCP", 40).move_to([-2.85, 1.55, 0])
        self.play(FadeIn(mcp_l), run_time=0.4)
        done(self)


# ── B10 · two projects, both do both ──────────────────────────────────────────────────────────────────────────
class B10_TwoProjects(Scene):
    def construct(self):
        xs = [0.5, 4.35]                                   # the two project columns
        blk = [a2_server(x, 2.75, 0.5) for x in xs]
        self.play(FadeIn(blk[0]), FadeIn(blk[1]), run_time=0.5)
        until(self, "a community one", lead=0.3)
        n1 = T("MCP for Blender", 34).move_to([xs[0], 1.85, 0])
        s1 = T("community", 34).move_to([xs[0], 1.3, 0])
        self.play(FadeIn(n1), FadeIn(s1), run_time=0.4)
        until(self, "the Blender Lab", lead=0.4)
        n2 = T("Blender MCP", 34).move_to([xs[1], 1.85, 0])
        s2 = T("Blender Lab", 34).move_to([xs[1], 1.3, 0])
        self.play(FadeIn(n2), FadeIn(s2), run_time=0.4)
        cells = VGroup()
        for x in xs:
            for y in (0.1, -1.45):
                cells.add(RoundedRectangle(width=3.3, height=1.15, corner_radius=0.2, fill_opacity=0, stroke_color=DIM,
                                           stroke_width=4).move_to([x, y, 0]))
        r1 = T("run Python", 36).move_to([-3.95, 0.1, 0])
        r2 = T("screenshots", 36).move_to([-3.95, -1.45, 0])
        self.play(FadeIn(cells), FadeIn(r1), FadeIn(r2), run_time=0.5)
        until(self, "run Python", lead=0.2)
        for x in xs:
            self.play(Create(check(x, 0.1, 0.3)), run_time=0.3)
        until(self, "screenshots", lead=0.2)
        for x in xs:
            self.play(Create(check(x, -1.45, 0.3)), run_time=0.3)
        done(self)


# ── B12 · the Lab page says the same; two rules, shown as rules ───────────────────────────────────────────────
class B12_TwoRules(Scene):
    def construct(self):
        warn = ImageMobject("pantry/a2_lab_warning.png").set_width(11.8).move_to([0.2, 1.95, 0])
        edge = Rectangle(width=11.8, height=11.8 * 430.0 / 2640.0, stroke_color=DIM, stroke_width=4, fill_opacity=0).move_to([0.2, 1.95, 0])
        src = T("blender.org/lab/mcp-server, captured 2026-10-06", 32).move_to([0.2, 0.65, 0])
        spark = Dot([-6.0, 1.95, 0], radius=0.13, color=TERRA)
        self.play(FadeIn(warn), Create(edge), FadeIn(src), run_time=0.5)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "So two rules", lead=0.0)
        # rule 1 (left): localhost only. A boundary around this machine; a remote box is stopped at the edge.
        bound = RoundedRectangle(width=3.5, height=2.1, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=7).move_to([-2.05, -1.6, 0])
        win, wfr, wh = a2_window(-1.75, -1.6, 2.0)
        sock = a2_socket(-2.75, -1.6)
        remote = RoundedRectangle(width=1.0, height=0.8, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([-5.4, -1.6, 0])
        out_l = T("outside", 34).move_to([-5.4, -2.4, 0])
        self.play(Create(bound), FadeIn(win), Create(wfr), GrowFromCenter(sock), FadeIn(remote), FadeIn(out_l), run_time=0.5)
        until(self, "Keep the port on localhost", lead=0.0)
        host = M("localhost", 32).move_to([-2.05, -3.1, 0])
        wall = Line([-3.8, -2.2, 0], [-3.8, -1.0, 0], color=INK, stroke_width=10)
        d = Dot([-4.7, -1.6, 0], radius=0.14, color=TERRA)
        self.play(FadeIn(host), Create(wall), FadeIn(d), run_time=0.4)
        self.play(d.animate.move_to([-4.05, -1.6, 0]), run_time=0.5, rate_func=linear)
        # rule 2 (right): three generation services, switched on at first, each calling out to a remote service
        until(self, "And leave", lead=0.0)
        names = ["Rodin", "Hunyuan3D", "Tripo"]
        ys = [-0.85, -1.85, -2.85]
        pills, knobs, nms, cabs, boxes = VGroup(), VGroup(), VGroup(), VGroup(), VGroup()
        for n, y in zip(names, ys):
            pills.add(RoundedRectangle(width=0.95, height=0.5, corner_radius=0.25, fill_opacity=0, stroke_color=INK, stroke_width=5).move_to([0.8, y, 0]))
            knobs.add(Circle(radius=0.17, fill_color=INK, fill_opacity=1, stroke_width=0).move_to([0.98, y, 0]))
            nms.add(T(n, 34).move_to([1.7 + {"Rodin": 0.55, "Hunyuan3D": 1.05, "Tripo": 0.5}[n], y, 0]))
            cabs.add(a2_cable([4.3, y, 0], [5.05, y, 0]))
            boxes.add(RoundedRectangle(width=0.9, height=0.7, corner_radius=0.15, fill_opacity=0, stroke_color=DIM, stroke_width=5).move_to([5.5, y, 0]))
        self.play(FadeIn(pills), FadeIn(knobs), FadeIn(nms), FadeIn(cabs), FadeIn(boxes), run_time=0.45)
        until(self, "services off", lead=0.0)
        self.play(*[k.animate.move_to([0.62, y, 0]) for k, y in zip(knobs, ys)], FadeOut(cabs), run_time=0.7)
        until(self, "approved the spend", lead=0.2)
        spend = T("$", 44).move_to([0.8, -0.15, 0])
        self.play(FadeIn(spend), run_time=0.3)
        until(self, "remote services", lead=0.3)
        rem = T("remote", 34).move_to([5.5, -0.15, 0])
        self.play(FadeIn(rem), run_time=0.3)
        done(self)


# ── B13 · the script route: no window; a script runs in Blender, builds, exports, exits ───────────────────────
class B13_ScriptRoute(Scene):
    def construct(self):
        gw = a2_ghost_window(-4.9, 0.55, 2.4, 1.6)
        gw_l = T("window", 34).move_to([-4.9, -0.7, 0])
        self.play(FadeIn(gw), FadeIn(gw_l), run_time=0.5)
        until(self, "no window at all", lead=0.3)
        stk = a2_strike(-4.9, 0.55, 2.4, 1.6)
        self.play(Create(stk), run_time=0.5)
        until(self, "Blender can run", lead=0.0)
        pg = a2_page(-2.0, 0.45, 1.0)
        pg_l = T("script", 34).move_to([-2.0, -0.95, 0])
        self.play(FadeIn(pg), FadeIn(pg_l), run_time=0.5)
        bl = a2_icon(1.2, 0.4, 1.5)
        bl_l = T("Blender", 34).move_to([1.2, -0.7, 0])
        self.play(FadeIn(bl), FadeIn(bl_l), run_time=0.5)
        until(self, "in the background", lead=0.0)
        ar1 = Arrow([-0.85, 0.4, 0], [0.3, 0.4, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(Create(ar1), run_time=0.4)
        until(self, "it builds the model", lead=0.0)
        post = ImageMobject("pantry/a2_post.png").set_height(1.75).move_to([1.2, 2.25, 0])
        post_l = T("model", 34).move_to([2.6, 2.25, 0])
        self.play(FadeIn(post), FadeIn(post_l), run_time=0.5)
        until(self, "exports it", lead=0.0)
        ar2 = Arrow([2.15, 0.4, 0], [3.85, 0.4, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        glb = a2_iso(5.0, 0.4, 0.9, 1.0, 1.0, 0.5).box(0, 0, 0, 1.0, 1.0, 0.5)
        glb_l = T(".glb", 34).move_to([5.0, -0.75, 0])
        self.play(Create(ar2), FadeIn(glb), FadeIn(glb_l), run_time=0.5)
        until(self, "and exits", lead=0.0)
        self.play(bl.animate.fade(0.8), FadeOut(bl_l), run_time=0.4)
        done(self)


# ── B14 · read the flags: -b, --factory-startup, --python ─────────────────────────────────────────────────────
class B14_Flags(Scene):
    def construct(self):
        rows, flag = a2_cmd()
        self.play(FadeIn(VGroup(*rows)), run_time=0.4)
        dot = Dot([A2_DX, A2_Y1, 0], radius=0.12, color=TERRA)
        until(self, "Dash b", lead=0.2)
        gw = a2_ghost_window(-0.9, A2_Y1, 1.2, 0.6)
        stk = a2_strike(-0.9, A2_Y1, 1.2, 0.6)
        l1 = T("no window", 34).move_to([1.2, A2_Y1, 0])
        self.play(FadeIn(dot), FadeIn(gw), Create(stk), FadeIn(l1), run_time=0.5)
        until(self, "Factory startup", lead=0.3)
        pref = a2_page(0.0, A2_Y2, 0.45)
        stk2 = a2_strike(0.0, A2_Y2, 1.0, 0.6)
        l2 = T("your settings, skipped", 34).move_to([3.0, A2_Y2, 0])
        self.play(dot.animate.move_to([A2_DX, A2_Y2, 0]), run_time=0.25)
        self.play(FadeIn(pref), Create(stk2), FadeIn(l2), run_time=0.5)
        until(self, "every run starts the same", lead=0.2)
        l3 = T("same every run", 34).move_to([3.0, A2_Y3, 0])
        self.play(FadeIn(l3), run_time=0.4)
        until(self, "python runs the script", lead=0.5)
        self.play(dot.animate.move_to([A2_DX, A2_Y4, 0]), run_time=0.25)
        pg = a2_page(-3.2, -2.0, 1.0)
        ar = Arrow([-1.9, -1.9, 0], [-0.4, -1.9, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        bl = a2_icon(1.0, -1.9, 1.5)
        bl_l = T("Blender runs it", 34).move_to([3.7, -1.9, 0])
        self.play(FadeIn(pg), Create(ar), FadeIn(bl), FadeIn(bl_l), run_time=0.5)
        done(self)


# ── B15 · one more flag: the same error, exit 0 without it, exit 1 with it (real output) ─────────────────────
class B15_ExitCode(Scene):
    def construct(self):
        rows, flag = a2_cmd()
        self.add(VGroup(*rows))
        dot = Dot([A2_DX, A2_Y3, 0], radius=0.12, color=TERRA)
        until(self, "python exit code one", lead=0.25)
        self.play(FadeIn(flag), FadeIn(dot), run_time=0.4)
        until(self, "Without it", lead=0.1)
        pan_l = RoundedRectangle(width=5.8, height=2.55, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([-3.15, -2.1, 0])
        h_l = T("without the flag", 34).move_to([-3.15, -1.3, 0])
        self.play(flag.animate.set_color(GHOST), FadeOut(dot), Create(pan_l), FadeIn(h_l), run_time=0.4)
        until(self, "Blender exits with zero", lead=-0.2)
        x_l = T("exit code", 34).move_to([-4.3, -2.85, 0])
        n0 = T("0", 96).move_to([-1.6, -2.7, 0])
        self.play(FadeIn(x_l), FadeIn(n0), run_time=0.4)
        until(self, "raises an exception", lead=1.6)
        e_l = M("ValueError: boom", 32).move_to([-3.15, -1.95, 0])
        self.play(FadeIn(e_l), run_time=0.4)
        until(self, "the same error both ways", lead=0.3)
        pan_r = RoundedRectangle(width=5.8, height=2.55, corner_radius=0.25, fill_opacity=0, stroke_color=DIM, stroke_width=4).move_to([3.15, -2.1, 0])
        h_r = T("with the flag", 34).move_to([3.15, -1.3, 0])
        e_r = M("ValueError: boom", 32).move_to([3.15, -1.95, 0])
        dot2 = Dot([A2_DX, A2_Y3, 0], radius=0.12, color=TERRA)
        self.play(Create(pan_r), FadeIn(h_r), FadeIn(e_r), flag.animate.set_color(INK), FadeIn(dot2), run_time=0.5)
        until(self, "and one", lead=0.15)
        x_r = T("exit code", 34).move_to([2.0, -2.85, 0])
        n1 = T("1", 96).move_to([4.5, -2.7, 0])
        self.play(FadeIn(x_r), FadeIn(n1), run_time=0.35)
        done(self)


# ── B16 · exits zero looks like success downstream; the one flag is the difference ──────────────────────────
class B16_LooksLikeSuccess(Scene):
    def construct(self):
        y1, y2 = 1.25, -1.55
        ds_l = T("downstream", 34).move_to([3.4, 3.0, 0])
        l1 = T("no flag", 34).move_to([-4.6, y1 + 1.05, 0])
        l2 = M("--python-exit-code 1", 32).move_to([-3.3, y2 + 1.05, 0])
        gt_l = T("exit check", 34).move_to([-0.6, 2.2, 0])
        pgs = [a2_page(-4.7, y, 0.75) for y in (y1, y2)]
        bxs = [a2_iso(3.4, y, 0.9, 1.1, 1.1, 0.8).box(0, 0, 0, 1.1, 1.1, 0.8) for y in (y1, y2)]
        # the gate beside each row: raised (open) above the path at first
        gates = [Line([1.0, y + 0.6, 0], [1.0, y + 1.5, 0], color=INK, stroke_width=12) for y in (y1, y2)]
        self.add(ds_l, l1, l2, gt_l, *pgs, *bxs, *gates)
        until(self, "fails", lead=0.3)
        xs = [a2_strike(-4.7, y, 0.9, 0.9) for y in (y1, y2)]
        self.play(Create(xs[0]), Create(xs[1]), run_time=0.4)
        until(self, "exits zero", lead=0.4)
        c0 = T("0", 72).move_to([-2.5, y1, 0])
        c1 = T("1", 72).move_to([-2.5, y2, 0])
        self.play(FadeIn(c0), FadeIn(c1), run_time=0.3)
        until(self, "looks like success", lead=0.55)
        self.play(c0.animate.move_to([2.0, y1, 0]), c1.animate.move_to([0.2, y2, 0]),
                  gates[1].animate.shift(DOWN * 1.1), run_time=0.8, rate_func=linear)
        ok = check(3.4, y1 + 1.2, 0.3, INK)
        ok_l = T("looks like success", 34).move_to([3.4, y1 - 1.3, 0])
        no_l = T("stops here", 34).move_to([0.6, y2 - 0.95, 0])
        self.play(Create(ok), FadeIn(ok_l), FadeIn(no_l), run_time=0.4)
        until(self, "That one flag", lead=0.1)
        sp = Dot([-6.2, y2 + 1.05, 0], radius=0.13, color=TERRA)
        self.play(FadeIn(sp), run_time=0.3)
        done(self)


# ── B17 · what you keep from each route ────────────────────────────────────────────────────────────────────────
class B17_WhatYouKeep(Scene):
    def construct(self):
        img, fr, h = a2_window(-3.2, 2.4, 2.4)
        pg = a2_page(3.2, 2.4, 0.7)
        h_l = T("live", 38).move_to([-5.45, 2.4, 0])
        h_s = T("script", 38).move_to([1.3, 2.4, 0])
        div = Line([0.0, 3.2, 0], [0.0, -3.1, 0], color=GHOST, stroke_width=5)
        self.add(img, fr, pg, h_l, h_s, div)
        until(self, "a transcript of tool calls", lead=0.4)
        rows = VGroup()
        for i in range(4):
            y = 0.9 - i * 0.62
            rows.add(VGroup(Dot([-5.55, y, 0], radius=0.09, color=TERRA), Line([-5.3, y, 0], [-3.2 - 0.25 * (i % 2), y, 0], color=DIM, stroke_width=7)))
        tl = T("tool calls", 34).move_to([-4.2, -1.4, 0])
        for r in rows:
            self.play(FadeIn(r), run_time=0.2)
        self.play(FadeIn(tl), run_time=0.2)
        until(self, "a scene that changed", lead=0.4)
        q = T("?", 110).move_to([-1.7, -0.2, 0])
        q_l = T("no record", 34).move_to([-1.9, -1.3, 0])
        self.play(FadeIn(q), FadeIn(q_l), run_time=0.4)
        until(self, "you keep a Python file", lead=0.0)
        pg_d = a2_page(1.55, -0.1, 0.75)
        self.play(FadeIn(pg_d), run_time=0.4)
        until(self, "diff,", lead=0.35)
        pg_d2 = a2_page(1.95, 0.15, 0.75)
        d_l = T("diff", 34).move_to([1.75, -1.3, 0])
        self.play(FadeIn(pg_d2), FadeIn(d_l), run_time=0.3)
        until(self, "rerun", lead=0.2)
        arc = Arc(radius=0.55, start_angle=0.5, angle=4.9, color=INK, stroke_width=7).move_to([3.7, -0.1, 0])
        tip = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.14).move_to([3.7 + 0.55 * np.cos(0.5), -0.1 + 0.55 * np.sin(0.5), 0])
        r_l = T("rerun", 34).move_to([3.7, -1.3, 0])
        self.play(Create(arc), FadeIn(tip), FadeIn(r_l), run_time=0.3)
        until(self, "review", lead=0.2)
        ey = a2_eye(5.45, -0.1, 0.9)
        e_l = T("review", 34).move_to([5.45, -1.3, 0])
        self.play(Create(ey), FadeIn(e_l), run_time=0.3)
        done(self)


# ── B18 · the script repeats a wrong assumption faithfully; neither route makes it look right; both hand you numbers ──
class B18_NumbersNotLooks(Scene):
    def construct(self):
        pg = a2_page(-4.6, 0.3, 1.1)
        pg_l = T("script", 34).move_to([-4.6, -1.3, 0])
        self.play(FadeIn(pg), FadeIn(pg_l), run_time=0.4)
        until(self, "a wrong assumption", lead=0.6)
        wd = Dot([-4.65, 0.45, 0], radius=0.16, color=TERRA)
        wl = T("wrong assumption", 34).move_to([-4.6, 1.95, 0])
        self.play(FadeIn(wd), FadeIn(wl), run_time=0.3)
        until(self, "repeat it faithfully", lead=1.4)
        outs = VGroup()
        xs = (-1.4, 0.9, 3.2)
        for x in xs:
            b = a2_iso(x, 0.3, 0.8, 1.0, 1.0, 0.6).box(0, 0, 0, 1.0, 1.0, 0.6)
            outs.add(VGroup(b, a2_strike(x, 0.3, 0.7, 0.7)))
        ars = VGroup(*[Arrow([x - 1.35, 0.3, 0], [x - 0.85, 0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.18) for x in xs])
        for i in range(3):
            self.play(Create(ars[i]), FadeIn(outs[i]), run_time=0.3)
        rl = T("same wrong result", 34).move_to([0.9, -1.45, 0])
        self.play(FadeIn(rl), run_time=0.3)
        until(self, "Neither route", lead=0.1)
        self.play(FadeOut(VGroup(pg, pg_l, wd, wl, outs, ars, rl)), run_time=0.4)
        img, fr, h = a2_window(-4.7, 1.3, 2.6)
        pg2 = a2_page(-4.7, -1.4, 0.8)
        self.play(FadeIn(img), Create(fr), FadeIn(pg2), run_time=0.4)
        a1 = Arrow([-3.25, 1.2, 0], [0.0, 0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        a2 = Arrow([-3.6, -1.4, 0], [0.0, -0.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        ey = a2_eye(1.1, 0.0, 1.0)
        self.play(Create(a1), Create(a2), Create(ey), run_time=0.5)
        stk = a2_strike(1.1, 0.0, 1.7, 1.1)
        lk = T("looks right", 34).move_to([1.1, 1.25, 0])
        self.play(Create(stk), FadeIn(lk), run_time=0.4)
        until(self, "hand you numbers", lead=0.2)
        cells = VGroup()
        for i, v in enumerate(("0.2", "1.8", "0.2")):
            x = 1.0 + i * 1.75
            cells.add(VGroup(RoundedRectangle(width=1.5, height=1.2, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == 1 else DIM,
                                              stroke_width=6 if i == 1 else 4).move_to([x, 0.0, 0]),
                             T(v, 52).move_to([x, 0.0, 0])))
        nl = T("numbers, in metres", 34).move_to([2.75, -1.2, 0])
        self.play(FadeOut(VGroup(ey, stk, lk)), FadeIn(cells), FadeIn(nl), run_time=0.45)
        done(self)
