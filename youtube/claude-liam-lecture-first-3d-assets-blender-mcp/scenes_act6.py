"""ACT VI · Export, Import, Check  (B50–B60, all Manim)

The act's worked example, and nearly everything on screen is a real record:
  B50  Blender 5.1.2's own glTF export dialog (pantry/ev_bl_export_gltf.png), pushed into its options (pantry/a6_export_opts.png).
  B51  axes drawn as an idea; the lantern's numbers are real (Blender sidebar 0.3/0.3/0.5; Godot check, +Y Up on and off).
  B52  Blender's own File > Export submenu, captured for this act (evidence/act6/run_file_export.sh -> pantry/a6_bl_file_export.png,
       crops pantry/a6_file_menu.png, a6_export_submenu.png); the exporter call is build_lantern.py line 119, wrapped at its commas.
  B53  the real `ls` and `godot --headless --path godot --import` output (evidence/act6/a6_*.log, drawn by make_terminals.py), then the
       real Godot render of the scene (pantry/ev_godot_showcase_crop.png).
  B54  the real check output, every line (evidence/act6/a6_check.log -> pantry/a6_term_check.png); dots land on what is spoken.
Gate notes (pre-checked with type_check.py / final_frame_check.py functions on 1080p and 1620p renders): at the 50% and 85% samples
every capture sits INSIDE the title-safe box (no camera crop past the frame: Gate V edge-bleed), and a capture whose dark UI greys fall
inside GATE T's ink tolerance is shown only where it forms one large panel (B50) or is replaced at the midpoint by a tighter crop of
its own pixels (B52 submenu, B57 status bar); each midpoint carries at least one INK label on the cream.
  B55  a drawn table of real numbers (assets/ASSETS.md, the check's BRIEF, a6_check.log).
  B56  the real gap values and the origin check's real verdict (evidence/godot/demo_iii_*.log).
  B57  Blender's status bar with Scene Statistics (pantry/ev_bl_status_stats.png), then the three real triangle counts against 500.
  B58  a recorded case from the course's own example run (examples/03-blender-mcp-to-godot: logs/verify1-test_checkpoint_post.log,
       logs/verify1-independent.log), drawn to scale in a side view.
  B59  the real lantern renders (back, below) and the real Godot render.
  B60  the real x10 demonstration (evidence/godot/demo_iv_lantern_x10.log) against the good check, and the assignment's own example
       commit message, labelled as an example.
Cues use the measured audio: word start times from faster-whisper (evidence/act6/whisper_words.log), via a6_at().
Cast: the lantern is the act's recurring object (B50-B55, B57, B59, B60); the crate carries the origin demonstrations (B56, as in the
real runs); B58's post is a different, labelled, recorded case.
"""


def a6_at(self, t):
    """Wait until t seconds into the beat (t = a word's start in the measured audio, evidence/act6/whisper_words.log)."""
    gap = t - _elapsed(self)
    if gap > 0.03:
        self.wait(gap)


def a6_place(w_px, h_px, width, center):
    """Pixel (origin top-left) -> scene point, for an image w_px x h_px drawn `width` units wide at `center` (its rest state)."""
    k = width / float(w_px)
    cx, cy = center
    return lambda px, py: np.array([cx + (px - w_px / 2.0) * k, cy - (py - h_px / 2.0) * k, 0.0])


def a6_img(path, width, center):
    return ImageMobject(path).set_width(width).move_to([center[0], center[1], 0])


def a6_mono(s, xl, y, size=32, color=INK):
    """Menlo line whose LEFT edge sits at xl (Menlo is about 0.25 units per character at size 32)."""
    return M(s, size, color).move_to([xl + 0.25 * (size / 32.0) * len(s) / 2.0, y, 0])


def a6_cell(x, y, letter, value, w=1.05, h=1.15, strong=False):
    """An outlined cell: axis letter on top, the number under it (no fill behind text)."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.16, fill_opacity=0, stroke_color=INK if strong else DIM,
                           stroke_width=7 if strong else 4).move_to([x, y, 0])
    a = T(letter, 32, DIM).move_to([x, y + 0.3, 0])
    n = T(value, 42).move_to([x, y - 0.2, 0])
    return VGroup(box, a, n)


# ── B50 · export as a .glb; +Y Up on, by default (carries the act title) ───────────────────────────────────────────────────
class B50_ExportGLB(Scene):
    def construct(self):
        title = T("Export, Import, Check", 40).move_to([-3.75, 3.05, 0])
        W1, C1 = 9.6, (0.9, -0.5)
        pv1 = a6_place(3456, 2006, W1, C1)
        full = a6_img("pantry/ev_bl_export_gltf.png", W1, C1)
        self.add(full, title)
        # 'Export each asset as a G L B': the file the dialog will write, lantern.glb
        a6_at(self, 1.1)
        d_file = Dot(pv1(1290, 1921), radius=0.09, color=TERRA)
        self.play(FadeIn(d_file, scale=0.5), run_time=0.3)
        # 'binary glTF': the options column comes forward (the crop sits exactly on its own pixels, then moves)
        a6_at(self, 2.3)
        cw, ch = 916, 788                                                    # pantry/a6_export_opts.png = (2540, 292) .. (3456, 1080)
        opts = a6_img("pantry/a6_export_opts.png", cw * W1 / 3456.0, pv1(2540 + cw / 2.0, 292 + ch / 2.0)[:2])
        self.add(opts)
        W2, C2 = 6.5, (2.75, -0.3)
        pv2 = a6_place(cw, ch, W2, C2)
        self.play(FadeOut(full), FadeOut(d_file), opts.animate.set_width(W2).move_to([C2[0], C2[1], 0]), run_time=0.9)
        d_fmt = Dot(pv2(150, 51), radius=0.11, color=TERRA)                  # beside Format: glTF Binary (.glb)
        self.play(FadeIn(d_fmt, scale=0.5), run_time=0.3)
        # 'a format Godot reads directly'
        a6_at(self, 3.7)
        gd = ImageMobject("pantry/ev_icon_godot.png").set_height(1.45).move_to([-4.3, 1.3, 0])
        gl = T("Godot", 36).move_to([-4.3, 0.2, 0])
        arr = Arrow(pv2(0, 51) + np.array([-0.25, 0.0, 0]), [-3.35, 1.45, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(GrowArrow(arr), FadeIn(gd), FadeIn(gl), run_time=0.7)
        # 'the plus Y up option should be on'
        a6_at(self, 7.15)
        self.play(d_fmt.animate.move_to(pv2(330, 551)), run_time=0.5)      # beside the +Y Up checkbox, ticked
        # 'It is by default'
        a6_at(self, 9.05)
        lab = T("on by default", 36).move_to([-3.5, pv2(330, 551)[1], 0])
        self.play(FadeIn(lab), run_time=0.4)
        done(self)


# ── B51 · Blender is Z-up; glTF and Godot are Y-up; the exporter turns the world ────────────────────────────────────────────
def a6_gizmo(o, kind):
    """Three axes at o. kind 'blender': X right-front, Y into the screen (dim), Z up (returned separately).
    kind 'godot': X right-front, Z toward you (left-front), Y up (returned separately)."""
    o = np.array([o[0], o[1], 0.0], dtype=float)
    ax = Arrow(o, o + np.array([1.3, -0.55, 0]), buff=0, color=INK, stroke_width=5, tip_length=0.18)
    lx = T("X", 34).move_to(o + np.array([1.62, -0.62, 0]))
    if kind == "blender":
        side = Arrow(o, o + np.array([0.95, 0.55, 0]), buff=0, color=DIM, stroke_width=5, tip_length=0.18)
        ls = T("Y", 34, DIM).move_to(o + np.array([1.22, 0.78, 0]))
        up_l = "Z"
    else:
        side = Arrow(o, o + np.array([-1.3, -0.55, 0]), buff=0, color=DIM, stroke_width=5, tip_length=0.18)
        ls = T("Z", 34, DIM).move_to(o + np.array([-1.62, -0.62, 0]))
        up_l = "Y"
    up = Arrow(o, o + np.array([0.0, 1.6, 0]), buff=0, color=INK, stroke_width=7, tip_length=0.24)
    lu = T(up_l + " up", 36).move_to(o + np.array([0.75, 1.55, 0]))
    return VGroup(ax, lx, side, ls), VGroup(up, lu)


class B51_YUp(Scene):
    def construct(self):
        O1, O2 = (-3.55, 0.35), (3.45, 0.35)
        hb = Group(ImageMobject("pantry/ev_icon_blender.png").set_height(0.75).move_to([-4.85, 2.85, 0]),
                   T("Blender", 36).move_to([-3.55, 2.85, 0]))
        base1, up1 = a6_gizmo(O1, "blender")
        self.add(hb, base1)
        # 'Blender's Z axis points up'
        a6_at(self, 0.85)
        self.play(GrowArrow(up1[0]), FadeIn(up1[1]), run_time=0.6)
        # its numbers: the sidebar's dimensions of the lantern, 0.3 / 0.3 / 0.5 m (height on Z)
        yb = -1.5
        c1 = VGroup(a6_cell(-4.75, yb, "x", "0.3"), a6_cell(-3.55, yb, "y", "0.3"), a6_cell(-2.35, yb, "z", "0.5", strong=True))
        self.play(FadeIn(c1), run_time=0.4)
        # 'and in glTF and Godot'
        a6_at(self, 2.5)
        hg = Group(ImageMobject("pantry/ev_icon_godot.png").set_height(0.75).move_to([1.9, 2.85, 0]),
                   T("glTF · Godot", 36).move_to([3.75, 2.85, 0]))
        base2, up2 = a6_gizmo(O2, "godot")
        self.play(FadeIn(hg), FadeIn(base2), run_time=0.5)
        a6_at(self, 3.1)
        self.play(GrowArrow(up2[0]), FadeIn(up2[1]), run_time=0.55)
        # 'The exporter turns the world on the way out': +Y Up, and the 0.5 moves from Z to Y
        a6_at(self, 5.1)
        turn = CurvedArrow(np.array([-1.15, 1.0, 0]), np.array([1.15, 1.0, 0]), angle=-PI / 2.2, color=INK, stroke_width=5, tip_length=0.2)
        tl = T("+Y Up", 38).move_to([0.0, 1.95, 0])
        self.play(Create(turn), FadeIn(tl), run_time=0.45)
        xs = [2.3, 3.5, 4.7]
        on_l = T("+Y Up on", 32).move_to([0.75, yb, 0])
        boxes = VGroup(*[RoundedRectangle(width=1.05, height=1.15, corner_radius=0.16, fill_opacity=0, stroke_color=INK if i == 1 else DIM,
                                          stroke_width=7 if i == 1 else 4).move_to([x, yb, 0]) for i, x in enumerate(xs)])
        letters = VGroup(*[T(a, 32, DIM).move_to([x, yb + 0.3, 0]) for a, x in zip("xyz", xs)])
        self.play(Create(boxes), FadeIn(letters), FadeIn(on_l), run_time=0.35)
        mv = [c1[0][2].copy(), c1[2][2].copy(), c1[1][2].copy()]        # x 0.3 -> X, z 0.5 -> Y, y 0.3 -> Z
        self.play(*[MoveAlongPath(m, ArcBetweenPoints(m.get_center(), np.array([x, yb - 0.2, 0]), angle=-PI / 4))
                    for m, x in zip(mv, xs)], run_time=0.75)
        # +Y Up off: the same lantern measures (0.3, 0.3, 0.5): its height lies on Z
        yo = -2.7
        off = VGroup(T("+Y Up off", 32).move_to([0.75, yo, 0]),
                     a6_cell(2.3, yo, "x", "0.3", h=1.0), a6_cell(3.5, yo, "y", "0.3", h=1.0), a6_cell(4.7, yo, "z", "0.5", h=1.0, strong=True))
        for c in off[1:]:
            c[1].shift(UP * -0.03); c[2].shift(UP * 0.05)
        self.play(FadeIn(off), run_time=0.35)
        done(self)


# ── B52 · no export tool: Blender's own File > Export > glTF 2.0, or the exporter as code, saved ──────────────────────────────
class B52_TwoRoutes(Scene):
    def construct(self):
        hdr = T("version 2.1.9", 34).move_to([-4.5, 2.85, 0])          # mcp-for-blender 2.1.9 (6 Oct)
        self.add(hdr)
        # 'The newer add-on has no export tool'
        a6_at(self, 0.45)
        slot = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.18, stroke_color=DIM, stroke_width=5,
                                fill_opacity=0).move_to([-4.5, 1.95, 0])              # an empty slot: no export tool
        none_l = T("no export tool", 34).move_to([-4.5, 1.05, 0])
        self.play(Create(slot), run_time=0.6)
        self.play(FadeIn(none_l), run_time=0.35)
        # 'So use Blender's own File, Export, glTF 2.0'  (Blender's own window, the submenu open; nothing is clicked in it)
        a6_at(self, 2.35)
        W, C = 9.0, (1.7, -0.25)
        pv = a6_place(1800, 1330, W, C)
        menu = a6_img("pantry/a6_file_menu.png", W, C)
        self.play(FadeIn(menu, shift=LEFT * 0.3), run_time=0.5)
        a6_at(self, 3.2)
        dot = Dot(pv(224, 52), radius=0.1, color=TERRA)                       # between File and Edit
        self.play(FadeIn(dot, scale=0.5), run_time=0.25)
        a6_at(self, 3.92)
        self.play(dot.animate.move_to(pv(388, 1268)), run_time=0.35)         # after "Export"
        # 'glTF 2.0': in to the submenu (a tighter crop of the same capture, laid on its own pixels, then enlarged)
        a6_at(self, 4.28)
        sw, sh = 916, 812                                                     # pantry/a6_export_submenu.png = (862, 500) .. (1778, 1312)
        sub = a6_img("pantry/a6_export_submenu.png", sw * W / 1800.0, pv(862 + sw / 2.0, 500 + sh / 2.0)[:2])
        self.add(sub)
        W2, C2 = 6.4, (2.75, -0.15)
        ps = a6_place(sw, sh, W2, C2)
        fe = T("File › Export", 34).move_to([-4.5, -0.6, 0])
        self.play(FadeOut(menu), FadeOut(dot), sub.animate.set_width(W2).move_to([C2[0], C2[1], 0]), FadeIn(fe), run_time=0.6)
        gdot = Dot(ps(530, 768), radius=0.11, color=TERRA)                   # after "glTF 2.0 (.glb/.gltf)"
        self.play(FadeIn(gdot, scale=0.5), run_time=0.25)
        # 'or have Claude run the exporter through execute Blender code'
        a6_at(self, 6.2)
        self.play(FadeOut(sub), FadeOut(gdot), FadeOut(fe), FadeOut(hdr), FadeOut(slot), FadeOut(none_l), run_time=0.35)
        cap = T("the exporter, in Python", 34).move_to([-3.1, 2.75, 0])
        code = ["bpy.ops.export_scene.gltf(", "    filepath=path,", "    export_format='GLB',", "    export_yup=True,",
                "    use_selection=True)"]
        rows = VGroup(*[a6_mono(s, -5.9, 1.9 - 0.55 * i) for i, s in enumerate(code)])
        self.play(FadeIn(cap), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.18), run_time=0.75)
        yup = Dot([-5.9 + 0.25 * 20 + 0.3, 1.9 - 0.55 * 3, 0], radius=0.09, color=TERRA)   # beside export_yup=True (B50's +Y Up)
        self.play(FadeIn(yup, scale=0.5), run_time=0.25)
        a6_at(self, 7.85)
        tool = a6_mono("execute_blender_code", 1.15, 0.85)
        tnote = T("documented, not run", 32).move_to([3.65, 0.2, 0])
        self.play(FadeIn(tool, shift=LEFT * 0.15), FadeIn(tnote), run_time=0.45)
        # 'and save that code too': it goes into the asset's build script
        a6_at(self, 9.0)
        page = VGroup(Polygon([-5.75, -1.25, 0], [-5.2, -1.25, 0], [-4.98, -1.47, 0], [-4.98, -2.3, 0], [-5.75, -2.3, 0],
                              fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4),
                      Line([-5.2, -1.25, 0], [-5.2, -1.47, 0], color=INK, stroke_width=3),
                      Line([-5.2, -1.47, 0], [-4.98, -1.47, 0], color=INK, stroke_width=3))
        fname = a6_mono("build_lantern.py", -4.55, -1.78)
        ghost = rows.copy()
        self.play(FadeIn(page), FadeIn(fname), run_time=0.35)
        self.play(ghost.animate.scale(0.12).move_to([-5.37, -1.85, 0]).set_opacity(0), run_time=0.6)
        done(self)


# ── B53 · the three files into the project, import; the small scene, in Godot ──────────────────────────────────────────────
class B53_IntoGodot(Scene):
    def construct(self):
        WT, CT = 8.4, (-1.5, 0.15)
        pt = a6_place(1797, 996, WT, CT)
        row = lambda i: 129 + 62 * i                                         # pantry/a6_term_import.png row centres (terminals.json)
        term = a6_img("pantry/a6_term_import.png", WT, CT)
        self.add(term)
        # 'Put the three files inside your Godot project'
        a6_at(self, 0.3)
        d = Dot(pt(44 + 24.078 * 8 + 60, row(1)), radius=0.08, color=TERRA)  # after coin.glb
        self.play(FadeIn(d, scale=0.5), run_time=0.25)
        self.play(d.animate.move_to(pt(44 + 24.078 * 9 + 60, row(2))), run_time=0.3)
        self.play(d.animate.move_to(pt(44 + 24.078 * 11 + 60, row(3))), run_time=0.3)
        # 'and import'
        a6_at(self, 2.15)
        self.play(d.animate.move_to(pt(44 + 24.078 * 40 + 60, row(4))), run_time=0.35)
        ys = [pt(0, row(i))[1] for i in (7, 9, 11)]
        checks = VGroup(*[check(3.25, y + 0.05, s=0.17) for y in ys])
        imp = T("imported", 34).move_to([4.75, ys[1], 0])
        self.play(LaggedStart(*[Create(c) for c in checks], lag_ratio=0.3), FadeIn(imp), run_time=0.7)
        # 'Then build the small scene: a floor': the real Godot render of it
        a6_at(self, 4.93)
        W, C = 9.0, (1.3, -0.15)
        pg = a6_place(1600, 900, W, C)
        shot = a6_img("pantry/ev_godot_showcase_crop.png", W, C)
        gi = ImageMobject("pantry/ev_icon_godot.png").set_height(1.2).move_to([-4.75, 0.6, 0])
        gv = T("Godot 4.7.2", 32).move_to([-4.75, -0.4, 0])
        self.play(FadeOut(term), FadeOut(d), FadeOut(checks), FadeOut(imp), FadeIn(shot), FadeIn(gi), FadeIn(gv), run_time=0.4)
        fp = pg(150, 820)
        fl = T("floor", 34).move_to([fp[0], 2.82, 0])
        fld = Dot(fp, radius=0.09, color=TERRA)
        fll = Line([fp[0], 2.35, 0], fp + np.array([0, 0.14, 0]), color=INK, stroke_width=4)
        self.play(FadeIn(fl), Create(fll), FadeIn(fld), run_time=0.35)
        # 'a light': the shadows it casts
        a6_at(self, 5.62)
        lp = pg(1240, 632)
        ll = T("light", 34).move_to([lp[0], 2.82, 0])
        lld = Dot(lp, radius=0.09, color=TERRA)
        lll = Line([lp[0], 2.35, 0], lp + np.array([0, 0.14, 0]), color=INK, stroke_width=4)
        self.play(FadeIn(ll), Create(lll), FadeIn(lld), run_time=0.35)
        # 'a camera': this picture is its view
        a6_at(self, 6.0)
        x0, x1, y0, y1 = C[0] - W / 2 - 0.15, C[0] + W / 2 + 0.15, C[1] - W * 900 / 1600 / 2 - 0.15, C[1] + W * 900 / 1600 / 2 + 0.15
        L = 0.45
        brk = VGroup(*[VGroup(Line([x, y, 0], [x + sx * L, y, 0], color=INK, stroke_width=6), Line([x, y, 0], [x, y + sy * L, 0], color=INK, stroke_width=6))
                       for x, y, sx, sy in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]])
        cl = T("camera", 34).move_to([5.25, 2.82, 0])
        self.play(Create(brk), FadeIn(cl), run_time=0.4)
        # 'and the three assets side by side at game scale'
        a6_at(self, 6.6)
        names = [("crate", 585), ("lantern", 1060), ("coin", 1340)]
        labs = [T(n, 34).move_to([pg(px, 0)[0], -3.05, 0]) for n, px in names]
        for lb in labs:
            self.play(FadeIn(lb, shift=UP * 0.1), run_time=0.3)
        done(self)


# ── B54 · the headless check: the real command and every line it printed ───────────────────────────────────────────────────
class B54_CheckByNumber(Scene):
    def construct(self):
        W, C = 10.6, (0.0, -0.35)
        pv = a6_place(2375, 1368, W, C)
        col = lambda c: 44 + 24.078 * c                                     # pantry/a6_term_check.png (evidence/act6/terminals.json)
        row = lambda i: 129 + 62 * i
        term = a6_img("pantry/a6_term_check.png", W, C)
        self.add(term)
        # 'Ask Claude Code to write a short headless script'
        a6_at(self, 1.45)
        cap = T("headless check", 34).move_to([-3.95, 3.1, 0])
        self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.4)
        # 'one that runs with no window': --headless
        a6_at(self, 4.15)
        hd = Dot(pv(col(24.5), row(0) - 46), radius=0.08, color=TERRA)       # just above "--headless"
        self.play(FadeIn(hd, scale=0.5), run_time=0.3)
        # 'It loads each asset and prints its bounding box size'
        a6_at(self, 7.15)
        bb = [5, 10, 15]
        dots = VGroup(*[Dot(pv(col(0.8), row(i)), radius=0.08, color=TERRA) for i in bb])
        self.play(FadeOut(hd), FadeIn(dots, scale=0.5), run_time=0.3)
        # 'its node scale'
        a6_at(self, 8.6)
        self.play(*[d.animate.move_to(pv(col(0.8), row(i + 1))) for d, i in zip(dots, bb)], run_time=0.4)
        # 'and the axis it stands along': the end of each size line, 'longest axis ... | height (Y) ...'
        a6_at(self, 9.62)
        ends = [87 + 1.6, 83 + 1.6, 87 + 1.6]                                  # the three size lines are 87, 83, 87 characters
        self.play(*[d.animate.move_to(pv(col(c), row(i))) for d, i, c in zip(dots, bb, ends)], run_time=0.45)
        done(self)


# ── B55 · compare: brief, Blender's sidebar, Godot's box, node scale ─────────────────────────────────────────────────────────
A6_COLS = {"asset": -5.3, "brief": -3.1, "blender": 0.15, "godot": 3.15, "scale": 5.55}
A6_DX = {"blender": 0.85, "godot": 1.0, "scale": 0.4}
A6_ROWS = {"crate": 0.55, "lantern": -0.55, "coin": -1.65}
A6_VALS = {   # brief w x d x h (check_assets.gd BRIEF) | Blender sidebar x y z (assets/ASSETS.md) | Godot box x y z (a6_check.log)
    "crate":   ("0.8 × 0.8 × 0.8", ("0.8", "0.8", "0.8"), ("0.8", "0.8", "0.8")),
    "lantern": ("0.3 × 0.3 × 0.5", ("0.3", "0.3", "0.5"), ("0.3", "0.5", "0.3")),
    "coin":    ("0.3 × 0.3 × 0.04", ("0.3", "0.3", "0.04"), ("0.3", "0.04", "0.3")),
}


def a6_triple(vals, x, y, dx, size=34):
    return VGroup(*[T(v, size).move_to([x + (i - 1) * dx, y, 0]) for i, v in enumerate(vals)])


class B55_Compare(Scene):
    def construct(self):
        hy, sy = 2.15, 1.5
        C, D = A6_COLS, A6_DX
        H = {"brief": VGroup(T("brief", 34).move_to([C["brief"], hy, 0]), T("w × d × h, m", 32, DIM).move_to([C["brief"], sy, 0]))}
        for k, name in (("blender", "Blender"), ("godot", "Godot box"), ("scale", "scale")):
            H[k] = VGroup(T(name, 34).move_to([C[k], hy, 0]), *[T(c, 32, DIM).move_to([C[k] + (i - 1) * D[k], sy, 0]) for i, c in enumerate("xyz")])
        names = VGroup(*[T(n, 36).move_to([C["asset"], y, 0]) for n, y in A6_ROWS.items()])
        rules = VGroup(*[Line([-6.2, y, 0], [6.2, y, 0], color=GHOST, stroke_width=3) for y in (1.05, 0.0, -1.1)])
        cols = {"brief": VGroup(*[T(A6_VALS[n][0], 32).move_to([C["brief"], y, 0]) for n, y in A6_ROWS.items()]),
                "blender": VGroup(*[a6_triple(A6_VALS[n][1], C["blender"], y, D["blender"]) for n, y in A6_ROWS.items()]),
                "godot": VGroup(*[a6_triple(A6_VALS[n][2], C["godot"], y, D["godot"]) for n, y in A6_ROWS.items()])}
        self.add(names, H["godot"], cols["godot"])
        # 'Compare those numbers with your brief'
        a6_at(self, 0.25)
        self.play(Create(rules), run_time=0.5)
        a6_at(self, 1.05)
        self.play(FadeIn(H["brief"]), FadeIn(cols["brief"], shift=RIGHT * 0.15), run_time=0.45)
        # 'and with the dimensions in Blender's sidebar'
        a6_at(self, 2.0)
        self.play(FadeIn(H["blender"]), FadeIn(cols["blender"], shift=RIGHT * 0.15), run_time=0.45)
        # the lantern row, the one this act follows: Blender 0.3 0.3 0.5 = Godot 0.3 0.5 0.3 (the height moved from Z to Y)
        a6_at(self, 3.15)
        ld = Dot([-6.2, A6_ROWS["lantern"], 0], radius=0.1, color=TERRA)
        self.play(FadeIn(ld, scale=0.5), run_time=0.3)
        # 'The node scale should be one, one, one'  (the check printed (1.0, 1.0, 1.0) for all three)
        a6_at(self, 4.25)
        sc = [VGroup(*[T("1", 34).move_to([C["scale"] + (i - 1) * D["scale"], y, 0]) for y in A6_ROWS.values()]) for i in range(3)]
        self.play(FadeIn(H["scale"]), run_time=0.3)
        for t, s_ in zip((5.2, 5.65, 6.0), sc):
            a6_at(self, t)
            self.play(FadeIn(s_, shift=DOWN * 0.1), run_time=0.25)
        # 'Each asset should stand upright': every height sits on Godot's Y
        a6_at(self, 6.6)
        ring = RoundedRectangle(width=1.04, height=2.95, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=7).move_to([C["godot"], -0.55, 0])
        upl = T("height on Y", 32).move_to([C["godot"], -2.55, 0])
        self.play(Create(ring), FadeIn(upl), run_time=0.5)
        done(self)


# ── B56 · sit, sink or float: the origin; moving the node hides it ────────────────────────────────────────────────────────────
A6_U = 1.5                                                                    # scene units per metre (the crate is 0.8 m = 1.2 units)


def a6_crate(cx, bottom):
    s = 0.8 * A6_U
    body = Square(side_length=s, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([cx, bottom + s / 2, 0])
    band_lo = Line([cx - s / 2, bottom + 0.15, 0], [cx + s / 2, bottom + 0.15, 0], color=BOX_FLOOR, stroke_width=6)
    band_hi = Line([cx - s / 2, bottom + s - 0.15, 0], [cx + s / 2, bottom + s - 0.15, 0], color=BOX_FLOOR, stroke_width=6)
    return VGroup(body, band_lo, band_hi)


class B56_SitSinkFloat(Scene):
    def construct(self):
        fy = 0.0
        floor = Line([-6.1, fy, 0], [6.1, fy, 0], color=DIM, stroke_width=8)
        self.add(floor)
        xs = [-4.0, 0.0, 4.0]
        # base origin (gap 0.0) | centre origin at floor level (gap -0.4) | centre origin, node lifted 0.5 by a guess (gap 0.1)
        bottoms = [fy, fy - 0.4 * A6_U, fy + 0.1 * A6_U]
        crates = [a6_crate(x, b) for x, b in zip(xs, bottoms)]
        origins = [Dot([xs[0], fy, 0], radius=0.11, color=TERRA), Dot([xs[1], fy, 0], radius=0.11, color=TERRA),
                   Dot([xs[2], fy + 0.5 * A6_U, 0], radius=0.11, color=TERRA)]
        # 'Place each asset on the floor without moving it'
        a6_at(self, 0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in crates], lag_ratio=0.25), run_time=1.0)
        a6_at(self, 1.5)
        self.play(*[FadeIn(o, scale=0.5) for o in origins], run_time=0.35)
        # 'Does it sit, sink or float?'  (gap to floor, from the real check runs)
        words = [("sits", "gap 0.0 m", 2.55), ("sinks", "gap -0.4 m", 3.0), ("floats", "gap 0.1 m", 3.45)]
        tops = []
        for x, (w, g, t) in zip(xs, words):
            a6_at(self, t)
            grp = VGroup(T(w, 38).move_to([x, 2.75, 0]), T(g, 34).move_to([x, 2.15, 0]))
            tops.append(grp)
            self.play(FadeIn(grp, shift=DOWN * 0.1), run_time=0.3)
        guess = T("node lifted 0.5", 32).move_to([xs[2], -0.6, 0])
        self.play(FadeIn(guess), run_time=0.25)
        # 'Move the node to compensate': lift the sinking crate by exactly 0.4 m
        a6_at(self, 5.5)
        self.play(VGroup(crates[1], origins[1]).animate.shift(UP * 0.4 * A6_U), run_time=0.7)
        new = VGroup(T("sits", 38).move_to([xs[1], 2.75, 0]), T("gap 0.0 m", 34).move_to([xs[1], 2.15, 0]))
        self.play(FadeOut(tops[1]), FadeIn(new), run_time=0.3)
        # 'and you've hidden the problem': the origin check's real verdict
        a6_at(self, 6.95)
        oc = T("origin check", 34).move_to([-4.7, -1.4, 0])
        v = ["FAIL crate_origin_centre.glb: the origin is", "0.4 m above the base: it sits on the floor", "only because the node was moved"]
        vr = VGroup(*[a6_mono(s, -5.4, -2.0 - 0.5 * i) for i, s in enumerate(v)])
        ring = Circle(radius=0.3, stroke_color=INK, stroke_width=6).move_to([xs[1], fy + 0.4 * A6_U, 0])        # round the moved origin
        self.play(FadeIn(oc), FadeIn(vr), Create(ring), run_time=0.5)
        done(self)


# ── B57 · triangle count: Blender's status bar, Scene Statistics; each asset against 500 ──────────────────────────────────────
class B57_Triangles(Scene):
    def construct(self):
        W, C = 11.0, (0.0, -0.3)
        pv = a6_place(3456, 2006, W, C)
        win = a6_img("pantry/ev_bl_status_stats.png", W, C)
        self.add(win)
        # 'Right-click Blender's status bar and enable Scene Statistics': the status bar's own pixels, lifted out and enlarged
        a6_at(self, 1.9)
        strip = a6_img("pantry/a6_statusbar.png", 1336 * W / 3456.0, pv(1830 + 668, 1915 + 44.5)[:2])
        self.add(strip)
        SW, SY = 12.2, 0.15
        self.play(FadeOut(win), strip.animate.set_width(SW).move_to([0, SY, 0]), run_time=1.0)
        lab = T("Scene Statistics", 36).move_to([0, 1.25, 0])
        self.play(FadeIn(lab), run_time=0.3)
        a6_at(self, 3.05)
        ks = SW / 1336.0
        td = Dot([(2808 - 2498) * ks, SY - 89 * ks / 2 - 0.32, 0], radius=0.11, color=TERRA)     # under "Tris:202"
        self.play(FadeIn(td, scale=0.5), run_time=0.3)
        # 'Is each asset within your budget?': the strip moves up; three counts against 500
        a6_at(self, 4.95)
        self.play(FadeOut(lab), FadeOut(td), strip.animate.set_width(10.4).move_to([0, 2.8, 0]), run_time=0.6)
        base_y, k = -2.55, 4.0 / 500.0
        axis = Line([-4.4, base_y, 0], [4.4, base_y, 0], color=DIM, stroke_width=5)
        lim = DashedLine([-4.4, base_y + 500 * k, 0], [4.4, base_y + 500 * k, 0], color=INK, stroke_width=5, dash_length=0.3)
        liml = T("500", 40).move_to([5.25, base_y + 500 * k + 0.05, 0])
        limn = T("budget", 32).move_to([5.25, base_y + 500 * k - 0.5, 0])
        self.play(Create(axis), Create(lim), FadeIn(liml), FadeIn(limn), run_time=0.4)
        data = [("crate", 60, -2.7, BAR2), ("lantern", 202, 0.0, BAR1), ("coin", 180, 2.7, BAR2)]
        bars = VGroup(*[Rectangle(width=1.3, height=n * k, fill_color=c, fill_opacity=1, stroke_width=0).move_to([x, base_y + n * k / 2, 0])
                        for _, n, x, c in data])
        self.play(*[GrowFromEdge(b, DOWN) for b in bars], run_time=0.5)
        nums = VGroup(*[T(str(n), 40).move_to([x, base_y + n * k + 0.38, 0]) for _, n, x, _ in data])
        names = VGroup(*[T(nm, 34).move_to([x, base_y - 0.45, 0]) for nm, _, x, _ in data])
        ld = Dot([0.75, base_y + 202 * k + 0.38, 0], radius=0.1, color=TERRA)  # beside 202, the count the status bar shows
        self.play(FadeIn(nums), FadeIn(names), FadeIn(ld), run_time=0.35)
        done(self)


# ── B58 · a check can prove less than it claims: the ray stopped on the object's own collider (a recorded case) ──────────────
A6_RU = 1.3                                                                   # units per metre in the side view


def a6_ry(wy):
    """Scene y of world height wy (Godot Y, metres) in the recorded run: the ray starts at -0.2, the floor is at -4.0."""
    return 2.6 + (wy + 0.2) * A6_RU


class B58_RayStops(Scene):
    def construct(self):
        px = -1.2                                                             # the post's axis on screen
        fy = a6_ry(-4.0)
        floor = Line([-5.9, fy, 0], [2.9, fy, 0], color=DIM, stroke_width=8)
        fl = T("floor, y = -4.0", 34).move_to([4.6, fy, 0])
        u = A6_RU
        base = Rectangle(width=0.6 * u, height=0.1 * u, fill_color=BOX_R, fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([px, fy + 0.05 * u, 0])
        pole = Rectangle(width=0.16 * u, height=1.7 * u, fill_color=BOX_L, fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([px, fy + 0.95 * u, 0])
        pen = Rectangle(width=0.4 * u, height=0.25 * u, fill_color=BOX_TOP, fill_opacity=1, stroke_color="#9C8462", stroke_width=4).move_to([px + 0.28 * u, fy + 1.675 * u, 0])
        post = VGroup(pole, pen, base)
        self.add(floor, fl, post)
        # 'Read the check Claude wrote': its own collider, a 0.6 x 1.8 m box
        a6_at(self, 0.35)
        box = Rectangle(width=0.6 * u, height=1.8 * u, stroke_color=INK, stroke_width=5, fill_opacity=0).move_to([px, fy + 0.9 * u, 0])
        bl = T("its own collider", 34).move_to([-3.75, fy + 1.0 * u, 0])
        self.play(Create(box), FadeIn(bl), run_time=0.7)
        # 'A check can prove less than it claims': it printed PASS
        a6_at(self, 1.4)
        ck = VGroup(T("the check printed", 34).move_to([2.25, 1.55, 0]), M("PASS", 40).move_to([4.85, 1.55, 0]))
        self.play(FadeIn(ck), run_time=0.4)
        # 'In one recorded case'
        a6_at(self, 3.55)
        rc = T("a recorded case", 36).move_to([3.1, 2.8, 0])
        self.play(FadeIn(rc), run_time=0.4)
        # 'an agent's floor check stopped on the object's own collider'
        a6_at(self, 5.25)
        top = np.array([px, a6_ry(-0.2), 0])
        hit = np.array([px, a6_ry(-2.2), 0])
        ray = Line(top, hit + np.array([0, 0.1, 0]), color=INK, stroke_width=7)
        rl = T("ray", 34).move_to([px + 0.7, a6_ry(-0.2) - 0.3, 0])
        self.play(Create(ray), FadeIn(rl), run_time=0.6)
        hd = Dot(hit, radius=0.12, color=TERRA)
        hl = a6_mono("ray hit at y=-2.2000", 0.85, hit[1])
        self.play(FadeIn(hd, scale=0.5), FadeIn(hl), run_time=0.35)
        a6_at(self, 7.05)
        self.play(Indicate(VGroup(box, bl), color=INK, scale_factor=1.06), run_time=0.6)
        # 'and proved nothing about the floor': the floor under the post was never reached
        a6_at(self, 8.1)
        rest = DashedLine(hit + np.array([0, -0.15, 0]), [px, fy + 0.2, 0], color=DIM, stroke_width=6, dash_length=0.25)
        q = T("?", 64).move_to([px + 1.1, fy + 0.85, 0])
        self.play(Create(rest), run_time=0.5)
        self.play(FadeIn(q, scale=0.6), run_time=0.3)
        done(self)


# ── B59 · the part no number covers: walk the camera round, behind and below; at game size ───────────────────────────────────
class B59_LookYourself(Scene):
    def construct(self):
        H, C = 4.9, (1.4, -0.25)
        views = [ImageMobject(f"pantry/a6_lantern_{v}.png").set_height(H).move_to([C[0], C[1], 0]) for v in ("34", "back", "below")]
        views[1].set_opacity(0); views[2].set_opacity(0)
        orbit = Ellipse(width=5.6, height=1.5, stroke_color=DIM, stroke_width=6).move_to([C[0], C[1] - 2.05, 0])
        self.add(orbit, *views)
        cam = Dot(orbit.point_from_proportion(0.75), radius=0.13, color=TERRA)      # the bottom of the ellipse: in front
        cl = T("you", 34).move_to(orbit.point_from_proportion(0.75) + np.array([0.6, -0.05, 0]))
        # 'Walk the camera around each asset'
        a6_at(self, 1.6)
        self.play(FadeIn(cam, scale=0.5), FadeIn(cl), run_time=0.3)
        self.play(FadeOut(cl), run_time=0.2)
        arc = ArcBetweenPoints(orbit.point_from_proportion(0.75), orbit.point_from_proportion(0.25), angle=-PI * 0.75)
        a6_at(self, 2.2)
        self.play(MoveAlongPath(cam, arc), run_time=1.3)
        # 'including from behind'
        a6_at(self, 3.75)
        bl = T("behind", 36).move_to([-3.6, 1.2, 0])
        self.play(views[1].animate.set_opacity(1), views[0].animate.set_opacity(0), FadeIn(bl), run_time=0.45)
        # 'and from below'
        a6_at(self, 4.4)
        b2 = T("below", 36).move_to([-3.6, 0.3, 0])
        self.play(cam.animate.move_to([C[0], C[1] - 3.05, 0]), views[2].animate.set_opacity(1), views[1].animate.set_opacity(0), FadeIn(b2), run_time=0.5)
        # 'Do the shapes read as what they are at game size?': the lantern among the others, in the game's own render
        a6_at(self, 5.65)
        Wg, Cg = 8.6, (1.85, -0.2)
        pg = a6_place(1600, 900, Wg, Cg)
        shot = a6_img("pantry/ev_godot_showcase_crop.png", Wg, Cg)
        self.play(FadeOut(views[2]), FadeOut(orbit), FadeOut(cam), FadeOut(bl), FadeOut(b2), FadeIn(shot), run_time=0.5)
        gl = T("game size", 36).move_to([-4.4, 1.3, 0])
        self.play(FadeIn(gl), run_time=0.3)
        # 'Are faces missing, or colours wrong?'
        a6_at(self, 7.95)
        fd = Dot(pg(1058, 700), radius=0.1, color=TERRA)                     # the lantern's base
        f1 = T("faces?", 36).move_to([-4.4, 0.2, 0])
        self.play(FadeIn(fd, scale=0.5), FadeIn(f1), run_time=0.3)
        a6_at(self, 9.2)
        f2 = T("colours?", 36).move_to([-4.4, -0.9, 0])
        self.play(fd.animate.move_to(pg(1062, 515)), FadeIn(f2), run_time=0.35)     # the flame
        done(self)


# ── B60 · one revision from something you saw; write the cycle down; keep the failing check ──────────────────────────────────
class B60_Revise(Scene):
    def construct(self):
        # the real lantern render; x10 (the real demonstration: every axis 10x the brief) shrinking to the real 0.5 m
        lx, lb = -3.6, -1.6                                                   # the lantern's foot on screen
        k1 = 0.85 / 787.0                                                     # 787 px of render = the lantern's 0.5 m
        im = ImageMobject("pantry/a6_lantern_34.png").set_height(867 * k1 * 10).move_to([lx + (274 - 274) * k1 * 10, lb + (827 - 433.5) * k1 * 10, 0])
        big_a = Arrow([lx + 3.25, lb, 0], [lx + 3.25, 3.3, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
        big_l = T("5.0 m", 38).move_to([lx + 2.45, 1.0, 0])
        demo = T("demonstration runs", 32).move_to([3.0, -0.05, 0])
        fail = VGroup(M("FAIL", 32).move_to([0.95, 1.25, 0]), a6_mono("(3.0, 5.0, 3.0)", 1.8, 1.25))
        self.add(im, big_a, big_l)
        # 'from something you saw'
        a6_at(self, 1.1)
        self.play(FadeIn(fail, shift=LEFT * 0.15), FadeIn(demo), run_time=0.35)
        # 'a size you corrected'
        a6_at(self, 2.55)
        w1 = T("size", 36).move_to([1.4, 2.75, 0])
        w1d = Dot([0.75, 2.75, 0], radius=0.1, color=TERRA)
        self.play(FadeIn(w1), FadeIn(w1d, scale=0.5), run_time=0.3)
        self.play(im.animate.scale(0.1, about_point=np.array([lx, lb, 0])), FadeOut(big_a), FadeOut(big_l), run_time=0.7)
        sm_a = dim_arrow([lx + 0.65, lb, 0], [lx + 0.65, lb + 0.85, 0], w=4, tip=0.12)
        sm_l = T("0.5 m", 38).move_to([lx + 1.55, lb + 0.43, 0])
        ok = VGroup(M("PASS", 32).move_to([0.95, 0.6, 0]), a6_mono("(0.3, 0.5, 0.3)", 1.8, 0.6))
        self.play(Create(sm_a), FadeIn(sm_l), FadeIn(ok, shift=LEFT * 0.15), run_time=0.4)
        # 'an origin you moved, a part you rebuilt'
        a6_at(self, 3.85)
        w2 = T("origin", 36).move_to([3.15, 2.75, 0])
        self.play(FadeIn(w2), run_time=0.3)
        a6_at(self, 4.95)
        w3 = T("part", 36).move_to([4.85, 2.75, 0])
        self.play(FadeIn(w3), run_time=0.25)
        # 'Write the cycle down'  (the assignment's own example message)
        a6_at(self, 6.2)
        ml = T("example commit message", 32).move_to([0.0, -2.35, 0])
        msg = a6_mono("Fix lantern height to 0.9 m; origin to base", -5.5, -2.95)
        node = Circle(radius=0.14, stroke_color=INK, stroke_width=5).move_to([-5.85, -2.95, 0])
        self.play(FadeIn(ml), FadeIn(msg), Create(node), run_time=0.45)
        # 'Don't delete a failing assertion to turn a report green': the FAIL stays on the record
        a6_at(self, 7.65)
        ring = RoundedRectangle(width=5.75, height=0.74, corner_radius=0.18, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([3.0, 1.25, 0])
        keep = T("keep it", 34).move_to([5.0, 1.95, 0])
        self.play(Create(ring), FadeIn(keep), run_time=0.45)
        done(self)
