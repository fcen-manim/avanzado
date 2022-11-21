from manim import *

class Main(Scene):
    def construct(self):
        Intro.construct(self)
        Conv.construct(self)

class Intro(Scene):
    def construct(self):
        recta = NumberLine(
            include_numbers = True,
            length = 7,
            x_range = [0, 1],
            rotation = 90 * DEGREES,
            label_direction = RIGHT,
            decimal_number_config={"num_decimal_places": 2},
        )
        self.play(Create(recta))
        self.wait()
        a_n = MathTex(r"a_n = \frac{1}{n}", substrings_to_isolate = ["n"]).move_to(RIGHT)
        self.play(recta.animate.move_to(LEFT), Write(a_n))
        self.wait()

        n = ValueTracker(1)
        p = Dot(recta.n2p(1 / n.get_value()), color = RED)
        self.play(a_n.animate.set_color_by_tex("n", RED), Create(p))
        p.add_updater(lambda m: m.move_to(recta.n2p(1 / n.get_value()))) # (!) get shit together subindices rojos
        a_n.add_updater(lambda m: m.become(MathTex("a_{%d} = \\frac{1}{%d}"%(n.get_value(), n.get_value())).move_to(RIGHT)))
        self.play(n.animate.set_value(2))
        self.wait()
        self.play(n.animate.set_value(10))
        self.wait()
        a_inf = MathTex(r"a_{\infty} = \frac{1}{\infty}").move_to(RIGHT)
        self.play(n.animate.set_value(99))
        self.remove(a_n)
        self.add(a_inf)
        self.wait()
        self.play(FadeIn(MathTex(r"= 0").move_to(RIGHT*2.5)))
        self.clear()

class Conv(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-5, 5, 1],
            y_range = [-2, 5, 1],
            tips = False
        )
        title = MathTex(r"f_n(x) = \frac{x^2 + nx}{n}", color = BLUE_A)
        f_n = VGroup()
        for n in range(1, 30, 5):
            f_n += axes.plot(lambda x: (x ** 2 + n*x) / n, color = BLUE_A)
        f_n += axes.plot(lambda x: x, color = BLUE)
        self.play(Write(title))
        self.wait(3)
        self.play(
            title.animate.to_corner(UP + LEFT),
            GrowFromCenter(axes),
            Create(f_n[0])
        )
        self.wait()
        f_n_label = axes.get_graph_label(f_n[0], "n=1")
        plot = VGroup(axes, f_n.copy())
        for n in range(1, 6):
            self.play(
                ReplacementTransform(f_n[n-1], f_n[n]),
                Transform(f_n_label, axes.get_graph_label(f_n[0], f"n = {n}"))
            )
        self.wait()
        self.play(
            ReplacementTransform(f_n[5], f_n[len(f_n) - 1]),
            Transform(f_n_label, axes.get_graph_label(f_n[0], MathTex("n = \infty"), color = BLUE))
        )
        self.wait(2)
        self.clear()
        converge = Text("¿Converge?")
        self.play(Write(converge))
        self.wait(2)

        self.play(
            FadeOut(converge),
            FadeIn(plot)
        )
        self.play(plot.animate.scale(1.5).move_to(UP*13.3 + LEFT*4))
        self.wait()
        t = ValueTracker(1)
        vert = VGroup(
            axes.plot_line_graph([t.get_value()]*(len(f_n) + 2), [0, 10] + [(t.get_value() ** 2 + n*t.get_value()) / n for n in range(1, 30, 5)] + [t.get_value()], line_color = RED),
            MathTex("x = ", color = RED),
            DecimalNumber(color = RED)
        )
        vert[0].add_updater(lambda m: m.become(axes.plot_line_graph([t.get_value()]*(len(f_n) + 2), [0, 10] + [(t.get_value() ** 2 + n*t.get_value()) / n for n in range(1, 30, 5)] + [t.get_value()], line_color = RED)))
        vert[1].add_updater(lambda m: m.next_to(vert[0], DOWN))
        vert[2].add_updater(lambda m: m.next_to(vert[1]).set_value(t.get_value()))
        self.play(Create(vert))
        self.wait(3)
        self.play(t.animate.set_value(2.5))
        self.wait()
        self.play(t.animate.set_value(3))