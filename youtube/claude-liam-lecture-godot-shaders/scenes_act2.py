"""ACT II · Setting Up a Shader (Manim beats B09, B12). Cast: the node, ShaderMaterial and shader boxes (outlined)."""


def a2_cube(cx, cy, k=0.8):
    """A small isometric cube (three faces, light to mid teal, no near-black fills)."""
    P = lambda x, y: np.array([cx + x * k, cy + y * k, 0.0])
    top = Polygon(P(0, 1), P(0.87, 0.5), P(0, 0), P(-0.87, 0.5), fill_color=GHOST, fill_opacity=1, stroke_color=INK, stroke_width=4)
    lf = Polygon(P(-0.87, 0.5), P(0, 0), P(0, -1), P(-0.87, -0.5), fill_color=TEAL, fill_opacity=1, stroke_color=INK, stroke_width=4)
    rt = Polygon(P(0, 0), P(0.87, 0.5), P(0.87, -0.5), P(0, -1), fill_color="#7FB8A8", fill_opacity=1, stroke_color=INK, stroke_width=4)
    return VGroup(top, lf, rt)


# ───────────────────────────────────────────────────────────────────────────
class B09_ThreeBoxes(Scene):
    def construct(self):
        title = T("Setting Up  a  Shader", 40)
        title.move_to([-6.2 + title.width / 2, 3.0, 0])
        y = -0.1
        b1 = box(-4.4, y, 3.5, 2.6); b2 = box(0, y, 3.5, 2.6); b3 = box(4.4, y, 3.5, 2.6)
        t1 = VGroup(T("a node", 36).move_to([-4.4, y + 0.8, 0]), T("Sprite2D", 32).move_to([-4.4, y + 0.15, 0]), T("ColorRect…", 32).move_to([-4.4, y - 0.4, 0]))
        t2 = T("ShaderMaterial", 36).move_to([0, y, 0])
        t3 = VGroup(T("your shader", 36).move_to([4.4, y + 0.6, 0]), T(".gdshader file", 32).move_to([4.4, y - 0.1, 0]))
        a12 = arrow([-2.6, y, 0], [-1.85, y, 0], w=5)
        a23 = arrow([1.85, y, 0], [2.6, y, 0], w=5)
        self.wait(0.3)
        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(b1, shift=RIGHT * 0.5), FadeIn(t1, shift=RIGHT * 0.5), run_time=0.6)
        until(self, "You attach")
        self.play(FadeIn(b2, shift=RIGHT * 0.5), FadeIn(t2, shift=RIGHT * 0.5), GrowArrow(a12), run_time=0.6)
        until(self, "through a material")
        self.play(FadeIn(b3, shift=RIGHT * 0.5), FadeIn(t3, shift=RIGHT * 0.5), GrowArrow(a23), run_time=0.6)
        until(self, "and the Shader Material holds", lead=0.5)
        p0 = np.array([4.4, y + 1.3, 0.0]); p1 = np.array([-4.4, y + 1.3, 0.0])
        path = VMobject()
        path.set_points([p0, p0 + np.array([-1.5, 1.4, 0]), p1 + np.array([1.5, 1.4, 0]), p1])
        dashed = DashedVMobject(path, num_dashes=24).set_stroke(DIM, width=4)
        dot = Dot(p0, radius=0.16, color=TERRA).set_stroke(DIM, width=3)
        self.add(dashed)
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=1.6, rate_func=smooth)
        done(self)


# ───────────────────────────────────────────────────────────────────────────
class B12_TwoWorlds(Scene):
    def construct(self):
        lead = T("the first line", 36, DIM).move_to([0, 3.0, 0])
        l1 = M("shader_type canvas_item;", 32)
        l2 = M("shader_type spatial;", 32)
        print("[width] canvas", l1.width, "spatial", l2.width)
        l1.move_to([-5.9 + l1.width / 2 + 0.0, 2.0, 0])
        l2.move_to([6.2 - l2.width / 2, 2.0, 0])
        spr = sprite_icon(-3.1, 0.2, 0.8)
        cube = a2_cube(3.6, 0.2, 0.95)
        d2 = T("2D", 36).move_to([-3.1, -1.0, 0])
        d3 = T("3D", 36).move_to([3.6, -1.0, 0])
        self.wait(0.3)
        self.play(FadeIn(lead), run_time=0.5)
        until(self, "Canvas item is")
        self.play(AddTextLetterByLetter(l1, time_per_char=0.05), FadeIn(spr), run_time=1.4)
        self.play(FadeIn(d2), run_time=0.3)
        until(self, "Spatial is")
        self.play(AddTextLetterByLetter(l2, time_per_char=0.05), FadeIn(cube), run_time=1.2)
        self.play(FadeIn(d3), run_time=0.3)
        until(self, "Particles, sky")
        names = ["particles", "sky", "fog"]
        xs = [-3.4, 0.0, 3.4]
        tiles = VGroup()
        icons = VGroup()
        for n, x in zip(names, xs):
            tiles.add(box(x, -2.4, 3.0, 1.5, color=DIM, sw=4), T(n, 34).move_to([x, -2.75, 0]))
        icons.add(VGroup(*[Dot([-3.4 + dx, -1.95 + dy, 0], radius=0.07, color=TEAL) for dx, dy in ((-0.4, 0.05), (-0.1, 0.15), (0.2, -0.05), (0.45, 0.1), (0.05, -0.12))]))
        icons.add(VGroup(Arc(radius=0.5, start_angle=0, angle=PI, stroke_color=INK, stroke_width=4).move_to([0, -2.0, 0]),
                         Circle(radius=0.14, stroke_color=GOLD, stroke_width=5).move_to([0, -1.95, 0])))
        icons.add(VGroup(*[Line([3.4 - 0.55 + 0.1 * i, -1.85 - 0.14 * i, 0], [3.4 + 0.55 - 0.1 * i, -1.85 - 0.14 * i, 0], color=DIM, stroke_width=5) for i in range(3)]))
        self.play(FadeIn(tiles), FadeIn(icons), run_time=0.8)
        until(self, "This film uses canvas item")
        rg = ring(l1, pad=0.14, sw=6)
        self.play(Create(rg), run_time=0.7)
        done(self)
