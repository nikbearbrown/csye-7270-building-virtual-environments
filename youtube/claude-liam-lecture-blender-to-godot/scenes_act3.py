"""ACT III · Metres, Axes and Applied Scale  (B19-B32, all Manim; B21/B24/B26/B28/B29 carry REAL captures as ImageMobjects)

One cast for the act: the COLUMN and its side view (Act I's language: Godot's Y up, Z across, 1.5 scene units per metre),
the 1 m dimension bar, the player's capsule, and one 2 m cube that is scaled down to the column. Numbers on screen are real
probe output (evidence/probe/*.log, evidence/act3/*.log) or values read from the real captures; nothing is invented.
Captures (all real): pantry/a3_demo_capsule_lit.png (Godot's platformer demo, collision shapes on, orthographic side view),
pantry/a3_yup_on|off_tight.png (Blender 5.1.2's glTF export dialog), pantry/a3_bl_transform_*.png and a3_bl_apply_menu.png
(Blender's Properties editor and Apply menu), pantry/a3_docs_*.png (two public Godot docs pages).
"""

A3_U = 1.5                                   # side view: scene units per metre (same as Act I)
A3_O = np.array([-3.3, -2.55, 0.0])          # side view: ground point under the column's bottom-right corner
A3_W, A3_H = 0.2, 1.8                        # the column, metres


# ───────────────────────── shared pieces ─────────────────────────
def a3_axes(up="Y up", across="Z"):
    """Side-view axes (Act I's): vertical up, horizontal across, meeting at the left of the ground line."""
    y_ax = Arrow([-6.0, -2.55, 0], [-6.0, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    z_ax = Arrow([-6.0, -2.55, 0], [-0.1, -2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.22)
    ly = T(up, 34).move_to([-5.25, 1.1, 0])
    lz = T(across, 34).move_to([0.3, -2.55, 0])
    return y_ax, z_ax, ly, lz


def a3_rect(w_m, h_m, fill=BOX_L):
    """A column in the side view standing on the ground with its bottom-RIGHT corner at A3_O."""
    r = Rectangle(width=w_m * A3_U, height=h_m * A3_U, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=5)
    r.move_to(A3_O + np.array([-w_m * A3_U / 2, h_m * A3_U / 2, 0]))
    return r


def a3_chips(vals, x0=1.0, y=1.15, hi=None, labels="XYZ", dx=1.95):
    """Three outlined cells X / Y / Z with their numbers. No fill behind text; `hi` rings one cell."""
    cells = VGroup()
    for i, (ax, v) in enumerate(zip(labels, vals)):
        x = x0 + i * dx
        box = RoundedRectangle(width=1.6, height=1.55, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == hi else DIM,
                               stroke_width=6 if i == hi else 4).move_to([x, y, 0])
        a = T(ax, 36, DIM).move_to([x, y + 0.42, 0])
        n = T(v, 62).move_to([x, y - 0.22, 0])
        cells.add(VGroup(box, a, n))
    return cells


def a3_file(x, y, w=0.95, h=1.2):
    """A drawn file icon (for the glTF/glb file): page outline with a folded corner."""
    x0, x1, y0, y1, f = x - w / 2, x + w / 2, y - h / 2, y + h / 2, 0.3
    page = Polygon([x0, y0, 0], [x1, y0, 0], [x1, y1 - f, 0], [x1 - f, y1, 0], [x0, y1, 0],
                   fill_color=CARD, fill_opacity=1, stroke_color=INK, stroke_width=5)
    fold = Polygon([x1 - f, y1, 0], [x1 - f, y1 - f, 0], [x1, y1 - f, 0], fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(page, fold)


def a3_mark(kind, x, y, h=1.2):
    if kind == "blender":
        return ImageMobject("pantry/icon_blender.png").set_height(h).move_to([x, y, 0])
    if kind == "godot":
        return ImageMobject("pantry/icon_godot.png").set_height(h).move_to([x, y, 0])
    return a3_file(x, y, 0.95 * h / 1.2, h)


def a3_bar(x, y, half=1.2):
    """The 1 m bar of the unit beats: one dimension line, the same length in every place it appears."""
    return dim_arrow([x - half, y, 0], [x + half, y, 0])


def a3_cross(x, y, s=0.22, color=INK, w=7):
    return VGroup(Line([x - s, y - s, 0], [x + s, y + s, 0], color=color, stroke_width=w),
                  Line([x - s, y + s, 0], [x + s, y - s, 0], color=color, stroke_width=w))


def a3_capsule(cx, cy, u=1.0, color=INK, sw=5):
    """The player's collision capsule drawn to scale: 0.4 m radius, 2.1 m tall, `u` scene units per metre."""
    return RoundedRectangle(width=0.8 * u, height=2.1 * u, corner_radius=0.4 * u, fill_opacity=0, stroke_color=color,
                            stroke_width=sw).move_to([cx, cy, 0])


# ═════════════════════════ B19 · units: one bar, three places ═════════════════════════
A3_UX = [-4.4, 0.0, 4.4]                       # the three places: Blender, glTF, Godot
A3_UKIND = ["blender", "gltf", "godot"]
A3_UNAME = ["Blender", "glTF", "Godot"]
A3_UNOTE = ["1 unit = 1 m", "all in metres", "1 unit = 1 m"]
A3_UY = dict(mark=1.65, name=0.25, bar=-0.85, note=-1.6)


def a3_unit_place(i):
    """(mark, name, bar, note) for place i of the unit beats."""
    x = A3_UX[i]
    return (a3_mark(A3_UKIND[i], x, A3_UY["mark"], 1.9), T(A3_UNAME[i], 44).move_to([x, A3_UY["name"], 0]),
            a3_bar(x, A3_UY["bar"], 1.5), T(A3_UNOTE[i], 44).move_to([x, A3_UY["note"], 0]))


class B19_UnitBar(Scene):
    def construct(self):
        title = T("Metres, Axes and Applied Scale", 40).move_to([-2.6, 3.05, 0])
        self.add(title)
        parts = [a3_unit_place(i) for i in range(3)]
        for mark, name, bar, note in parts:           # the pipeline is on stage from the start: Blender, glTF file, Godot
            self.add(mark, name)
        phrases = ["one unit is one metre", "every linear distance is in metres", "one unit in three-D is one metre"]
        for i in range(3):
            mark, name, bar, note = parts[i]
            until(self, phrases[i], lead=0.35)
            self.play(Create(bar), FadeIn(note), run_time=0.5)
        done(self)


# ═════════════════════════ B20 · no conversion on the way ═════════════════════════
class B20_NoConversion(Scene):
    def construct(self):
        for i in range(3):
            self.add(*a3_unit_place(i))
        y = A3_UY["mark"]
        a1 = Arrow([-3.3, y, 0], [-1.2, y, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        a2 = Arrow([1.2, y, 0], [3.3, y, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        x1 = T("× 1", 40).move_to([-2.25, y + 0.5, 0])
        x2 = T("× 1", 40).move_to([2.25, y + 0.5, 0])
        until(self, "no conversion", lead=0.1)
        self.play(Create(a1), FadeIn(x1), run_time=0.4)
        self.play(Create(a2), FadeIn(x2), run_time=0.4)
        rider = Dot([-3.3, y, 0], radius=0.13, color=TERRA)
        self.add(rider)
        self.play(rider.animate.move_to([3.3, y, 0]), run_time=1.0, rate_func=linear)
        until(self, "as long as Blender's unit scale", lead=0.1)
        cell = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-4.4, -2.75, 0])
        cl = T("unit scale", 34, DIM).move_to([-4.4, -2.5, 0])
        cn = T("1.0", 50).move_to([-4.4, -2.97, 0])
        self.play(Create(cell), FadeIn(cl), FadeIn(cn), run_time=0.5)
        lg = M("scale_length=1.0", 32, DIM).move_to([-1.0, -2.75, 0])
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ═════════════════════════ B21 · the platformer demo's capsule: 2.1 m, gravity 22, 120 ticks ═════════════════════════
# Real capture: Godot's 3D platformer demo, Debug > Visible Collision Shapes on, orthographic side view whose 3.6 m tall view
# is shown 4.05 units tall (1.125 units per metre), the capsule centred on the picture. (evidence/act3/capture_demo.gd)
A3_IMG = np.array([2.6, 0.0, 0.0])
A3_K = 1.125                                   # scene units per metre inside the capture


class B21_Capsule(Scene):
    def construct(self):
        img = ImageMobject("pantry/a3_demo_capsule_lit.png").set_width(7.2).move_to(A3_IMG)
        cap = T("3D platformer demo", 36).move_to([2.6, 2.5, 0])
        self.play(FadeIn(img), FadeIn(cap), run_time=0.7)
        until(self, "collision capsule", lead=0.3)
        shape = a3_capsule(2.6, 0.0, A3_K, CARD, 8)
        hh = 2.1 * A3_K / 2
        dim = dim_arrow([-1.4, -hh, 0], [-1.4, hh, 0])
        dl = T("2.1 m", 48).move_to([-2.45, 0.0, 0])
        self.play(Create(shape), Create(dim), FadeIn(dl), run_time=0.8)
        until(self, "under gravity of", lead=0.2)
        g = VGroup(RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-4.75, 1.6, 0]),
                   T("gravity", 34, DIM).move_to([-4.75, 1.97, 0]), T("22", 56).move_to([-4.4, 1.38, 0]))
        garrow = Arrow([-5.5, 1.65, 0], [-5.5, 1.05, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(g), Create(garrow), run_time=0.5)
        gl = M("3d/default_gravity=22.0", 32, DIM).move_to([-3.1, -2.6, 0])
        self.play(FadeIn(gl), run_time=0.3)
        until(self, "at a hundred and twenty", lead=0.2)
        t = VGroup(RoundedRectangle(width=2.5, height=1.5, corner_radius=0.2, fill_opacity=0, stroke_color=INK, stroke_width=6).move_to([-4.75, -0.3, 0]),
                   T("ticks / s", 34, DIM).move_to([-4.75, 0.07, 0]), T("120", 56).move_to([-4.75, -0.52, 0]))
        self.play(FadeIn(t), run_time=0.5)
        tl = M("common/physics_ticks_per_second=120", 32, DIM).move_to([-1.6, -3.05, 0])
        self.play(FadeIn(tl), run_time=0.3)
        done(self)


# ═════════════════════════ B22 · a prop at the wrong scale: a wall, or a step it never notices ═════════════════════════
class B22_WrongScale(Scene):
    def construct(self):
        g1, g2 = 0.55, -2.75
        ground1 = Line([-6.0, g1, 0], [6.0, g1, 0], color=INK, stroke_width=5)
        ground2 = Line([-6.0, g2, 0], [6.0, g2, 0], color=INK, stroke_width=5)
        cap1 = a3_capsule(-4.4, g1 + 1.05, 1.0, INK, 5)
        cap2 = a3_capsule(-4.4, g2 + 1.05, 1.0, INK, 5)
        self.add(ground1, ground2, cap1, cap2)
        until(self, "wrong scale", lead=0.4)
        wall = Rectangle(width=0.6, height=2.4, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to([0.9, g1 + 1.2, 0])
        step = Rectangle(width=0.6, height=0.14, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([0.9, g2 + 0.07, 0])
        self.play(GrowFromEdge(wall, DOWN), GrowFromEdge(step, DOWN), run_time=0.5)
        until(self, "a wall the robot", lead=0.6)
        self.play(cap1.animate.shift(RIGHT * 4.6), run_time=1.0, rate_func=smooth)
        spark = Dot([0.6, g1 + 1.3, 0], radius=0.12, color=TERRA)
        wl = T("wall", 40).move_to([2.3, g1 + 1.2, 0])
        self.play(FadeIn(spark), FadeIn(wl), run_time=0.3)
        until(self, "or a step it never notices", lead=0.3)
        sl = T("step", 40).move_to([4.7, g2 + 0.45, 0])
        self.play(FadeIn(sl), run_time=0.3)
        self.play(cap2.animate.shift(RIGHT * 4.2), run_time=0.7, rate_func=smooth)
        self.play(cap2.animate.shift(RIGHT * 2.6 + UP * 0.14), run_time=0.5, rate_func=smooth)
        done(self)


# ═════════════════════════ B23 · direction: Blender's Z-up world, glTF/Godot's Y-up world (isometric) ═════════════════════════
class B23_Turn(Scene):
    def construct(self):
        ib = Iso(-3.7, -1.7, 1.5)         # Blender's world (left): X back-right, Y back-left, Z up
        ig = Iso(3.4, -1.7, 1.5)          # glTF / Godot's world (right): X back-right, Y up, Z toward the viewer (iso -y)
        o = ib.p(0, 0, 0)
        ebx, eby, ebz = ib.p(1.55, 0, 0), ib.p(0, 1.55, 0), ib.p(0, 0, 2.09)
        bx, by, bz = [Arrow(o, tip, buff=0, color=INK, stroke_width=5, tip_length=0.22) for tip in (ebx, eby, ebz)]
        lbx = T("X", 40).move_to(ebx + np.array([0.35, 0.12, 0]))
        lby = T("Y", 40).move_to(eby + np.array([-0.35, 0.12, 0]))
        lbz = T("Z", 40).move_to(ebz + np.array([0.0, 0.42, 0]))
        bicon = a3_mark("blender", -3.7, 2.65, 0.95)
        o2 = ig.p(0, 0, 0)
        egx, egy, egz = ig.p(1.55, 0, 0), ig.p(0, 0, 2.09), ig.p(0, -1.55, 0)
        gx, gy, gz = [Arrow(o2, tip, buff=0, color=INK, stroke_width=5, tip_length=0.22) for tip in (egx, egy, egz)]
        lgx = T("X", 40).move_to(egx + np.array([0.35, 0.12, 0]))
        lgy = T("Y", 40).move_to(egy + np.array([0.0, 0.42, 0]))
        lgz = T("Z", 40).move_to(egz + np.array([0.38, -0.1, 0]))
        gfile = a3_file(2.55, 2.65, 0.75, 0.95)
        gicon = a3_mark("godot", 3.9, 2.65, 0.95)
        cap_b = T("Z up", 40).move_to([-3.7, -3.0, 0])
        cap_g = T("Y up", 40).move_to([3.4, -3.0, 0])
        self.add(bicon)
        until(self, "Blender is right-handed", lead=0.2)
        self.play(Create(bx), Create(by), FadeIn(lbx), FadeIn(lby), run_time=0.6)
        until(self, "Z pointing up", lead=0.45)
        up = Dot(ebz, radius=0.11, color=TERRA)
        self.play(Create(bz), FadeIn(lbz), FadeIn(cap_b), run_time=0.5)
        self.play(FadeIn(up), run_time=0.2)
        until(self, "The glTF format and Godot", lead=0.2)
        self.play(FadeIn(gfile), FadeIn(gicon), Create(gx), Create(gz), FadeIn(lgx), FadeIn(lgz), run_time=0.7)
        until(self, "Y pointing up", lead=0.45)
        up2 = Dot(egy, radius=0.11, color=TERRA)
        self.play(Create(gy), FadeIn(lgy), FadeIn(cap_g), run_time=0.5)
        self.play(FadeIn(up2), run_time=0.2)
        until(self, "Somebody has to turn the world", lead=0.2)
        arc = ArcBetweenPoints(np.array([-1.9, 2.1, 0]), np.array([1.1, 2.1, 0]), angle=-TAU / 5)
        arc.add_tip(tip_length=0.22)
        arc.set_stroke(INK, 5)
        turn = T("turn", 40).move_to([-0.4, 3.1, 0])
        self.play(Create(arc), FadeIn(turn), run_time=0.7)
        done(self)


# ═════════════════════════ B24 · the exporter's +Y Up option maps Blender's Z extent onto Godot's Y ═════════════════════════
# Real captures: Blender 5.1.2's glTF export dialog, Transform panel (pantry/a3_yup_on_row.png).
# Real numbers: evidence/act3/extents_probe.log - a box with THREE different extents, so a swap cannot hide.
class B24_YUp(Scene):
    def construct(self):
        panel = ImageMobject("pantry/a3_yup_on_row.png").set_width(5.2).move_to([-3.4, 1.5, 0])
        pcap = T("glTF export dialog", 36).move_to([-3.4, 2.95, 0])
        self.add(panel, pcap)
        until(self, "plus Y up", lead=0.3)
        # the +Y Up row sits at 0.7 of the crop's height
        spark = Dot([-6.15, 1.5 + 1.105 - 0.768 * 2.21, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "on by default", lead=0.3)
        dflt = T("on by default", 38).move_to([-3.4, -0.2, 0])
        self.play(FadeIn(dflt), run_time=0.3)
        until(self, "It puts", lead=1.0)
        X0, DX = 1.7, 1.8
        bicon = a3_mark("blender", 0.1, 1.75, 0.7)
        gicon = a3_mark("godot", 0.1, -1.1, 0.7)
        brow = a3_chips(["0.2", "0.6", "1.8"], x0=X0, y=1.75, hi=2, dx=DX)
        grow = VGroup(*[RoundedRectangle(width=1.6, height=1.55, corner_radius=0.2, fill_opacity=0, stroke_color=INK if i == 1 else DIM,
                                          stroke_width=6 if i == 1 else 4).move_to([X0 + i * DX, -1.1, 0]) for i in range(3)])
        glet = VGroup(*[T(ax, 36, DIM).move_to([X0 + i * DX, -1.1 + 0.42, 0]) for i, ax in enumerate("XYZ")])
        tb = T("test box", 38).move_to([X0 + DX, 2.95, 0])
        self.play(FadeIn(bicon), FadeIn(brow), FadeIn(gicon), FadeIn(grow), FadeIn(glet), FadeIn(tb), run_time=0.6)
        until(self, "Blender's Z extent", lead=0.1)
        n18 = brow[2][2].copy()
        self.play(n18.animate.move_to([X0 + DX, -1.1 - 0.22, 0]), run_time=0.6)
        until(self, "and Blender's Y extent", lead=0.1)
        n06 = brow[1][2].copy()
        self.play(n06.animate.move_to([X0 + 2 * DX, -1.1 - 0.22, 0]), run_time=0.6)
        n02 = brow[0][2].copy()
        self.play(n02.animate.move_to([X0, -1.1 - 0.22, 0]), run_time=0.5)
        until(self, "a claim a test can check", lead=0.2)
        l1 = M("Blender extents X, Y, Z = (0.2, 0.6, 1.8)", 32, DIM).move_to([-0.9, -2.55, 0])
        l2 = M("Godot extents X, Y, Z = (0.2, 1.8, 0.6)", 32).move_to([-1.15, -3.05, 0])
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.5)
        done(self)


# ═════════════════════════ B25 · switch +Y Up off: the second column lies on its side ═════════════════════════
class B25_YUpOff(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a3_axes("Y up", "Z")
        col = a3_rect(A3_W, A3_H)
        cap = T("bounding box, in metres", 36).move_to([2.6, 2.45, 0])
        chips = a3_chips(["0.2", "1.8", "0.2"], hi=1)
        ring = Dot([A3_O[0] - 0.15, A3_O[1] + 1.8 * A3_U + 0.2, 0], radius=0.12, color=TERRA)
        on = ImageMobject("pantry/a3_yup_on_row.png").set_width(4.2).move_to([-3.5, 2.35, 0])
        off = ImageMobject("pantry/a3_yup_off_row.png").set_width(4.2).move_to([-3.5, 2.35, 0])
        self.add(y_ax, z_ax, ly, lz, col, cap, chips, ring, on)
        until(self, "Switch the option off", lead=0.2)
        self.play(FadeOut(on), FadeIn(off), run_time=0.3)
        until(self, "second column", lead=0.5)
        self.play(FadeOut(ring), Rotate(col, angle=-PI / 2, about_point=A3_O.copy()), run_time=1.0)
        lab = T("1.8 now along Z", 34).move_to([-3.7, -1.5, 0])
        self.play(FadeIn(lab), run_time=0.3)
        until(self, "one point eight on the wrong axis", lead=0.2)
        newvals = a3_chips(["0.2", "0.2", "1.8"], hi=2)
        self.play(Transform(chips[1][2], newvals[1][2]), Transform(chips[2][2], newvals[2][2]),
                  chips[1][0].animate.set_stroke(DIM, 4), chips[2][0].animate.set_stroke(INK, 6), run_time=0.7)
        ring2 = Dot([1.0 + 2 * 1.95 + 0.62, 1.15 + 0.62, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(ring2), run_time=0.3)
        until(self, "and a column lying on its side", lead=0.2)
        lg = M("mesh AABB size (0.2, 0.2, 1.8)", 32, DIM).move_to([2.2, -1.5, 0])
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ═════════════════════════ B26 · a transform vs. mesh data: the vertices still describe a 2 m cube ═════════════════════════
# Real captures: Blender 5.1.2's Properties > Object > Transform panel (a3_bl_transform_after.png = scale 1.000, as the 2 m cube is added;
# a3_bl_transform_before.png = scale 0.1, 0.1, 0.9). Real numbers: evidence/act3/apply_probe.log (vertices span 2.0, 2.0, 2.0).
A3_OB = np.array([-3.4, -0.1, 0.0])           # the object (cube -> pole), centre
A3_OU = 1.35                                  # scene units per metre


def a3_cube_parts(c=A3_OB, u=A3_OU):
    cube = Rectangle(width=2 * u, height=2 * u, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(c)
    ghost = Rectangle(width=2 * u, height=2 * u, fill_opacity=0, stroke_color=DIM, stroke_width=6).move_to(c)
    pole = Rectangle(width=0.2 * u, height=1.8 * u, fill_color=BOX_L, fill_opacity=1, stroke_color=INK, stroke_width=5).move_to(c)
    dots = VGroup(*[Dot([c[0] + sx * u, c[1] + sy * u, 0], radius=0.11, color=TERRA) for sx in (-1, 1) for sy in (-1, 1)])
    return cube, ghost, pole, dots


class B26_TransformVsMesh(Scene):
    def construct(self):
        cube, ghost, pole, dots = a3_cube_parts()
        self.add(ghost, cube)
        p_after = ImageMobject("pantry/a3_bl_transform_after.png").set_width(6.4).move_to([2.9, 0.3, 0])
        p_before = ImageMobject("pantry/a3_bl_transform_before.png").set_width(6.4).move_to([2.9, 0.3, 0])
        tl = T("transform", 40).move_to([2.9, 2.1, 0])
        ml = T("mesh data", 40).move_to([-3.4, 1.8, 0])
        vl = T("vertices", 36).move_to([-3.4, -1.8, 0])
        until(self, "a transform", lead=0.2)
        self.play(FadeIn(p_after), FadeIn(tl), run_time=0.5)
        until(self, "separate mesh data", lead=0.6)
        self.play(FadeIn(ml), Create(dots), run_time=0.5)
        until(self, "the vertices", lead=0.9)
        self.play(FadeIn(vl), run_time=0.3)
        until(self, "scale it down to a pole", lead=0.2)
        ring = RoundedRectangle(width=5.65, height=0.82, corner_radius=0.12, fill_opacity=0, stroke_color=TERRA, stroke_width=6).move_to([2.96, 0.3 + (0.5 - 0.845) * 2.738, 0])
        self.play(Transform(cube, pole), FadeOut(p_after), FadeIn(p_before), run_time=1.0)
        self.play(Create(ring), run_time=0.4)
        until(self, "still describe", lead=0.4)
        lg = M("vertices span (2.0, 2.0, 2.0)", 32, DIM).move_to([-2.5, -2.75, 0])
        self.play(FadeIn(lg), run_time=0.4)
        done(self)


# ═════════════════════════ B27 · the exporter writes that scale onto the node; Godot draws right and measures wrong ═════════════════════════
# Real: the exported file's own JSON (evidence/act3/glb_json.log, float32 noise rounded) and Godot's own readout (evidence/probe/godot-mutations.log).
class B27_NodeScale(Scene):
    def construct(self):
        cube, ghost, pole, dots = a3_cube_parts(np.array([-4.3, 0.1, 0.0]), 1.25)
        bicon = a3_mark("blender", -4.3, 2.55, 1.0)
        self.add(ghost, pole, dots, bicon)
        spark = Dot([-4.3, 0.1 + 0.9 * 1.25 + 0.25, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "The exporter writes", lead=0.3)
        file = a3_file(-0.6, 2.55, 0.75, 0.95)
        arr1 = Arrow([-3.4, 2.55, 0], [-1.4, 2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(file), Create(arr1), run_time=0.5)
        until(self, "onto the node", lead=0.2)
        j1 = M('"scale": [0.1, 0.9, 0.1]', 32).move_to([-2.2 + 3.0, 1.55, 0])
        self.play(FadeIn(j1), run_time=0.3)
        j2 = M('"min": [-1, -1, -1]', 32, DIM).move_to([-2.2 + 2.375, 1.0, 0])
        j3 = M('"max": [1, 1, 1]', 32, DIM).move_to([-2.2 + 2.0, 0.45, 0])
        self.play(FadeIn(j2), FadeIn(j3), run_time=0.3)
        until(self, "and Godot shows", lead=0.1)
        gicon = a3_mark("godot", 4.0, 2.55, 1.0)
        arr2 = Arrow([0.3, 2.55, 0], [3.2, 2.55, 0], buff=0, color=INK, stroke_width=5, tip_length=0.2)
        self.play(FadeIn(gicon), Create(arr2), run_time=0.5)
        until(self, "a scale that isn't one", lead=0.2)
        r1 = M("node scale (0.1, 0.9, 0.1)", 32).move_to([6.2 - 3.25, -0.9, 0])
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "It draws right", lead=0.2)
        r2 = M("AABB in scene (0.2, 1.8, 0.2)", 32).move_to([6.2 - 3.625, -1.6, 0])
        ok = check(-1.75, -1.6, 0.2, INK, 7)
        self.play(FadeIn(r2), Create(ok), run_time=0.4)
        until(self, "and measures wrong", lead=0.2)
        r3 = M("mesh AABB size (2.0, 2.0, 2.0)", 32).move_to([6.2 - 3.75, -2.3, 0])
        no = a3_cross(-1.75, -2.3, 0.2, INK, 7)
        self.play(FadeIn(r3), Create(no), run_time=0.4)
        done(self)


# ═════════════════════════ B28 · what Godot's own documentation says (two public pages, as themselves) ═════════════════════════
# Real captures (evidence/act3/capture_docs.py, 2026-10-06, stable docs): the section's heading + paragraph, crops of the live pages.
class B28_GodotDocs(Scene):
    def construct(self):
        W = 11.4
        c1 = ImageMobject("pantry/a3_docs_collision.png").set_width(W).move_to([0, 1.55, 0])
        h1 = W * 579 / 2637
        c2 = ImageMobject("pantry/a3_docs_export.png").set_width(W).move_to([0, -1.55, 0])
        h2 = W * 250 / 2637
        f1 = Rectangle(width=W, height=h1, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([0, 1.55, 0])
        f2 = Rectangle(width=W, height=h2, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([0, -1.55, 0])
        k1 = T("docs.godotengine.org: Collision shapes (3D)", 36).move_to([0, 1.55 - h1 / 2 - 0.4, 0])
        k2 = T("docs.godotengine.org: Model export considerations", 36).move_to([0, -1.55 - h2 / 2 - 0.4, 0])
        dt = T("stable docs, captured 6 October 2026", 32, DIM).move_to([0, -3.1, 0])
        # the phrase boxes (fractions of each crop, from capture_docs.json)
        def ring(cx, cy, w, h, box, pad=0.07):
            x0, y0, x1, y1 = box
            return Rectangle(width=(x1 - x0) * w + 2 * pad, height=(y1 - y0) * h + 2 * pad, fill_color=TERRA, fill_opacity=0.28,
                             stroke_width=0).move_to([cx - w / 2 + (x0 + x1) / 2 * w, cy + h / 2 - (y0 + y1) / 2 * h, 0])
        r1 = ring(0, 1.55, W, h1, [0.3562, 0.6575, 0.8416, 0.7680])
        r2a = ring(0, -1.55, W, h2, [0.6433, 0.2051, 0.9722, 0.4615])
        r2b = ring(0, -1.55, W, h2, [0.0170, 0.5256, 0.4397, 0.7821])
        r1b = ring(0, 1.55, W, h1, [0.0175, 0.8000, 0.4110, 0.9500])
        self.play(FadeIn(c1), Create(f1), FadeIn(k1), run_time=0.5)
        until(self, "avoid scaling collision shapes", lead=0.5)
        self.play(FadeIn(r1), run_time=0.5)
        until(self, "so the physics engine", lead=0.4)
        self.play(FadeIn(r1b), run_time=0.4)
        until(self, "export guidance", lead=0.9)
        self.play(FadeIn(c2), Create(f2), FadeIn(k2), FadeIn(dt), run_time=0.5)
        until(self, "apply the object transform", lead=0.3)
        self.play(FadeIn(r2a), run_time=0.4)
        until(self, "in the modelling software", lead=0.3)
        self.play(FadeIn(r2b), run_time=0.4)
        done(self)


# ═════════════════════════ B29 · Object > Apply > Rotation & Scale; afterwards the scale is one ═════════════════════════
# Real: Blender 5.1.2's own Apply menu and Transform panel (pantry/a3_bl_apply_menu.png, a3_bl_transform_*.png);
# the one-call form is the line from evidence/probe/make_mutations.py; the result is evidence/act3/apply_probe.log.
class B29_ApplyScale(Scene):
    def construct(self):
        menu = ImageMobject("pantry/a3_bl_apply_menu.png").set_width(4.6).move_to([-2.2, 1.45, 0])
        mframe = Rectangle(width=4.6, height=4.6 * 570 / 810, fill_opacity=0, stroke_color=INK, stroke_width=4).move_to([-2.2, 1.45, 0])
        path = T("Object > Apply", 40).move_to([2.2, 2.55, 0])
        bicon = a3_mark("blender", 4.9, 2.55, 0.8)
        p_before = ImageMobject("pantry/a3_bl_transform_before.png").set_width(5.6).move_to([3.3, 0.35, 0])
        p_after = ImageMobject("pantry/a3_bl_transform_after.png").set_width(5.6).move_to([3.3, 0.35, 0])
        self.play(FadeIn(menu), Create(mframe), FadeIn(path), FadeIn(bicon), FadeIn(p_before), run_time=0.5)
        until(self, "Rotation and Scale", lead=0.5)
        spark = Dot([0.3, 1.45 + 1.62 - 0.84 * 3.237, 0], radius=0.12, color=TERRA)
        self.play(FadeIn(spark), run_time=0.3)
        until(self, "In a script", lead=0.2)
        c1 = M("bpy.ops.object.transform_apply(", 32).move_to([-5.7 + 15.5 * 0.5 + 0.0, -2.2, 0])
        c1.move_to([-5.7 + len("bpy.ops.object.transform_apply(") * 0.125, -2.2, 0])
        c2 = M("    location=False, rotation=True, scale=True)", 32).move_to([-5.7 + len("    location=False, rotation=True, scale=True)") * 0.125, -2.75, 0])
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.4)
        until(self, "Afterwards", lead=0.3)
        cube, ghost, pole, dots = a3_cube_parts(np.array([-2.4, 1.0, 0.0]), 1.2)
        old = Group(menu, mframe, spark, path)
        self.play(FadeOut(old), run_time=0.3)
        self.add(ghost, pole, dots)
        self.play(FadeIn(ghost), FadeIn(pole), FadeIn(dots), run_time=0.4)
        until(self, "the scale is one", lead=0.2)
        ring = RoundedRectangle(width=5.65, height=0.82, corner_radius=0.12, fill_opacity=0, stroke_color=TERRA, stroke_width=6).move_to([3.06, 0.35 + (0.5 - 0.845) * 5.6 * 1020 / 2384, 0])
        self.play(FadeOut(p_before), FadeIn(p_after), run_time=0.3)
        self.play(Create(ring), run_time=0.3)
        until(self, "the vertices carry the real size", lead=0.2)
        targets = [np.array([-2.4 + sx * 0.12, 1.0 + sy * 1.08, 0]) for sx in (-1, 1) for sy in (-1, 1)]
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], FadeOut(ghost), run_time=0.8)
        lg = M("vertices span (0.2, 0.2, 1.8)", 32, DIM).move_to([2.5, -1.5, 0])
        self.play(FadeIn(lg), run_time=0.3)
        done(self)


# ═════════════════════════ B30 · a test checks both halves ═════════════════════════
# Real: the 'good' line of evidence/probe/godot-mutations.log (the column that arrives right).
class B30_BothHalves(Scene):
    def construct(self):
        y_ax, z_ax, ly, lz = a3_axes("Y up", "Z")
        col = a3_rect(A3_W, A3_H)
        l1 = T("unit scale", 40).move_to([4.6, 1.5, 0])
        l2 = T("size in metres", 40).move_to([3.9, -0.5, 0])
        self.add(y_ax, z_ax, ly, lz, col, l1, l2)
        until(self, "unit scale on every node", lead=0.4)
        r1 = M("node scale (1.0, 1.0, 1.0)", 32).move_to([6.2 - 3.25, 0.85, 0])
        k1 = check(-0.75, 0.85, 0.22, INK, 8)
        self.play(FadeIn(r1), Create(k1), run_time=0.4)
        until(self, "the right size in metres", lead=0.3)
        r2 = M("mesh AABB size (0.2, 1.8, 0.2)", 32).move_to([6.2 - 3.75, -1.15, 0])
        k2 = check(-1.75, -1.15, 0.22, INK, 8)
        self.play(FadeIn(r2), Create(k2), run_time=0.4)
        done(self)


# ═════════════════════════ B31 · the stale-dimensions trap: set the scale, print right away, get the old size ═════════════════════════
# Real: evidence/probe/stale_dimensions.py (wrapped over two lines for width: same tokens) and its output, evidence/probe/stale-dimensions.log
A3_CX = -5.7                                   # code block left edge
A3_CH = 0.125                                  # Menlo 32: scene units per character


def a3_code(s, y, color=INK):
    return M(s, 32, color).move_to([A3_CX + len(s) * A3_CH, y, 0])


A3_STALE = dict(
    r1=('o.scale = (0.1, 0.1, 0.9)', 2.35),
    r2=('print("BEFORE view_layer.update():",', 1.8),
    r3=('      tuple(round(v, 4) for v in o.dimensions))', 1.3),
    r4=('bpy.context.view_layer.update()', 0.55),
    r5=('print("AFTER  view_layer.update():",', 0.0),
    r6=('      tuple(round(v, 4) for v in o.dimensions))', -0.5),
    o1=('BEFORE view_layer.update(): (2.0, 2.0, 2.0)', -1.7),
    o2=('AFTER  view_layer.update(): (0.2, 0.2, 1.8)', -2.3),
)


def a3_num_dots(key, nums, dy=-0.33):
    """Terracotta dots under the numbers of one output line (so the voice can point at each one)."""
    text, y = A3_STALE[key]
    out, start = [], 0
    for n in nums:
        i = text.index(n, start)
        start = i + len(n)
        out.append(Dot([A3_CX + (i + len(n) / 2.0) * 2 * A3_CH, y + dy, 0], radius=0.09, color=TERRA))
    return out


class B31_StaleDims(Scene):
    def construct(self):
        P = A3_STALE
        bicon = a3_mark("blender", 5.4, 2.35, 0.8)
        bl = T("Blender 5.1", 36).move_to([3.1, 2.35, 0])
        self.add(bicon, bl)
        until(self, "In Blender five point one", lead=0.3)
        r1 = a3_code(*P["r1"])
        self.play(FadeIn(r1), run_time=0.3)
        until(self, "dimensions don't refresh", lead=0.5)
        r2, r3 = a3_code(*P["r2"]), a3_code(*P["r3"])
        self.play(FadeIn(r2), FadeIn(r3), run_time=0.4)
        until(self, "Set the scale", lead=0.2)
        ptr = Dot([A3_CX - 0.4, P["r1"][1], 0], radius=0.11, color=TERRA)
        self.play(FadeIn(ptr), run_time=0.2)
        until(self, "print the dimensions", lead=0.3)
        self.play(ptr.animate.move_to([A3_CX - 0.4, P["r2"][1], 0]), run_time=0.4)
        until(self, "you get the old size", lead=0.5)
        o1 = a3_code(*P["o1"])
        self.play(ptr.animate.move_to([A3_CX - 0.4, P["o1"][1], 0]), FadeIn(o1), run_time=0.5)
        d1, d2, d3 = a3_num_dots("o1", ["2.0", "2.0", "2.0"])
        until(self, "two, two, two", lead=0.4)
        self.play(FadeIn(d1), run_time=0.12)
        self.wait(0.1)
        self.play(FadeIn(d2), run_time=0.12)
        self.wait(0.1)
        self.play(FadeIn(d3), run_time=0.12)
        done(self)


# ═════════════════════════ B32 · update the view layer first, and the log is current ═════════════════════════
class B32_Update(Scene):
    def construct(self):
        P = A3_STALE
        bicon = a3_mark("blender", 5.4, 2.35, 0.8)
        bl = T("Blender 5.1", 36).move_to([3.1, 2.35, 0])
        rows = [a3_code(*P[k]) for k in ("r1", "r2", "r3")]
        o1 = a3_code(*P["o1"])
        self.add(bicon, bl, *rows, o1)
        until(self, "Update the view layer", lead=0.1)
        r4 = a3_code(*P["r4"])
        ptr = Dot([A3_CX - 0.4, P["r4"][1], 0], radius=0.11, color=TERRA)
        self.play(FadeIn(r4), FadeIn(ptr), run_time=0.3)
        until(self, "you get point two", lead=0.9)
        r5, r6 = a3_code(*P["r5"]), a3_code(*P["r6"])
        self.play(FadeIn(r5), FadeIn(r6), ptr.animate.move_to([A3_CX - 0.4, P["r5"][1], 0]), run_time=0.4)
        until(self, "point two, point two", lead=0.5)
        o2 = a3_code(*P["o2"])
        self.play(ptr.animate.move_to([A3_CX - 0.4, P["o2"][1], 0]), FadeIn(o2), run_time=0.4)
        e1, e2, e3 = a3_num_dots("o2", ["0.2", "0.2", "1.8"])
        until(self, "point two, point two", lead=0.0)
        self.play(FadeIn(e1), run_time=0.12)
        self.wait(0.4)
        self.play(FadeIn(e2), run_time=0.12)
        until(self, "one point eight", lead=0.1)
        self.play(FadeIn(e3), run_time=0.12)
        until(self, "If an agent's log is its evidence", lead=0.1)
        ok = check(A3_CX + 2 * len(P["o2"][0]) * A3_CH + 0.6, P["o2"][1], 0.22, INK, 8)
        self.play(o1.animate.set_color(DIM), Create(ok), run_time=0.5)
        done(self)
