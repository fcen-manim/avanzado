from manim import *

class Main(Scene):
    def construct(self):
        Intro.construct(self)
        Puntual.construct(self)
        Uniforme.construct(self)

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
        a_n = MathTex(r"a_n = \frac{1}{n}").move_to(RIGHT)
        self.play(recta.animate.move_to(LEFT), Write(a_n))
        self.wait()

        n = ValueTracker(1)
        p = Dot(recta.n2p(1 / n.get_value()), color = RED)
        self.play(a_n[0][1].animate.set_color(RED), a_n[0][5].animate.set_color(RED), Create(p))
        self.wait()
        p.add_updater(lambda m: m.move_to(recta.n2p(1 / n.get_value()))) # (!) get shit together subindices rojos
        a_n.add_updater(lambda m: m.become(MathTex("a_{%d} = \\frac{1}{%d}"%(n.get_value(), n.get_value())).move_to(RIGHT)))
        self.play(n.animate.set_value(1))
        self.play(n.animate.set_value(2))
        self.wait()
        self.play(n.animate.set_value(10))
        self.wait()
        a_inf = MathTex(r"a_{\infty} = \frac{1}{\infty}").move_to(RIGHT)
        self.play(n.animate.set_value(99))
        self.remove(a_n)
        self.add(a_inf)
        self.remove(p)
        self.add(Dot(recta.n2p(0), color = RED))
        self.wait()
        self.play(FadeIn(MathTex(r"= 0").move_to(RIGHT*2.5)))
        self.wait(3)
        self.clear()

class Puntual(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-2, 8, 1],
            y_range = [-2, 8, 1],
            tips = False
        )
        title = MathTex(r"f_n(x) = \frac{x^2 + nx}{n}")
        f_n = VGroup()
        for n in range(1, 30, 5):
            f_n += axes.plot(
                lambda x: (x ** 2 + n*x) / n,
                color = BLUE_A,
            )
        f_n += axes.plot(lambda x: x, color = BLUE)
        self.play(Write(title))
        self.wait(3)
        self.play(
            title.animate.to_corner(RIGHT),
            title.animate.become(MathTex("f_%d(x) = \\frac{x^2 + %dx}{%d}"%(1, 1, 1), color = BLUE_A).to_corner(RIGHT)),
            Create(axes)
        )
        plot = VGroup(axes, f_n.copy())
        self.play(Create(f_n[0]))
        for n in range(1, 6):
            self.play(
                ReplacementTransform(f_n[n-1], f_n[n]),
            )
            title.become(MathTex("f_%d(x) = \\frac{x^2 + %dx}{%d}"%(n+1, n+1, n+1), color = BLUE_A).to_corner(RIGHT))
        self.wait()
        self.play(
            ReplacementTransform(f_n[5], f_n[len(f_n) - 1]),
            title.animate.become(MathTex(r"f_{\infty}(x) = \frac{x^2 + \infty \cdot x}{\infty}", color = BLUE).to_corner(RIGHT))
        )
        self.wait(2)
        self.play(FadeOut(f_n[len(f_n) - 1]), FadeOut(axes), FadeOut(title))
        self.clear()

        converge = Text("¿Converge?")
        self.play(Write(converge))
        self.wait(2)

        desarrollo = MathTex("f_n(x) = \\frac{x^2 + nx}{n}", " = ", "\\frac{1}{n}", "x^2 + ", "\\frac{n}{n}", "x", "  \\rightarrow x")
        desarrollo.set_color_by_tex("  \\rightarrow x", YELLOW)
        c1 = SurroundingRectangle(desarrollo[2])
        c2 = SurroundingRectangle(desarrollo[4])
        self.play(
            FadeOut(converge),
            FadeIn(desarrollo[0])
        )
        self.wait(2)
        self.play(Write(desarrollo[1:-1]))
        self.wait()
        self.play(Create(c1))
        self.play(Create(c2))
        self.wait()
        expl1 = MathTex("\\rightarrow 0", color = YELLOW).next_to(c1, DOWN)
        expl2 = MathTex("= 1", color = YELLOW).next_to(c2, DOWN)
        self.play(Create(expl1))
        self.play(Create(expl2))
        self.wait()
        self.play(Write(desarrollo[-1:]))
        self.wait(2)
        self.play(Write(MathTex("\checkmark", color = GREEN).next_to(desarrollo[-1], RIGHT)))
        self.wait()
        self.clear()

        self.play(FadeIn(plot))
        self.play(plot.animate.scale(2, about_point=axes.c2p(0, 0)))
        t = ValueTracker(0.5)
        vert = VGroup(
            axes.plot_line_graph([t.get_value()]*(len(f_n) + 3), [-10, 10] + [(t.get_value() ** 2 + n*t.get_value()) / n for n in range(1, 30, 5)] + [t.get_value()], line_color = RED),
            MathTex("x = ", color = RED),
            DecimalNumber(color = RED)
        )
        vert[0].add_updater(lambda m: m.become(axes.plot_line_graph([t.get_value()]*(len(f_n) + 3), [-10, 10] + [(t.get_value() ** 2 + n*t.get_value()) / n for n in range(1, 30, 5)] + [t.get_value()], line_color = RED)))
        vert[1].add_updater(lambda m: m.move_to(axes.c2p(t.get_value(), 0) + RIGHT + DOWN))
        vert[2].add_updater(lambda m: m.next_to(vert[1]).set_value(t.get_value()))
        texto = VGroup(Arrow(start = ORIGIN, end = LEFT, color = BLUE).next_to(axes.c2p(t.get_value(), t.get_value())))
        texto += Text("converge 'rápido'", color = BLUE).next_to(texto[0], RIGHT)
        self.wait()
        self.play(Create(vert))
        self.wait()
        self.play(Create(texto))
        self.wait(2)
        self.play(FadeOut(texto))
        self.wait()
        self.play(t.animate.set_value(3))
        self.wait()
        texto[0] = Arrow(start = ORIGIN, end = UP + RIGHT, color = BLUE).next_to(axes.c2p(t.get_value(), t.get_value()), LEFT + DOWN)
        texto[1] = Text("converge 'lento'", color = BLUE).next_to(texto[0], DOWN*0.5 + LEFT)
        self.play(Create(texto))
        self.wait()

        axes2 = Axes(
            x_range = [-8, 2, 1],
            y_range = [-2, 8, 1],
            tips = False
        )
        title2 = MathTex(r"g_n = \frac{1}{n} - x", color = GREEN_A)
        g_n = VGroup()
        for n in range(1, 5):
            g_n += axes2.plot(
                lambda x: 1/n - x,
                color = GREEN_A,
            )
        g_n += axes2.plot(lambda x: -x, color = GREEN)
        plot2 = VGroup(axes2, g_n.copy())
        self.remove(texto, vert)
        plot2.scale(2, about_point=axes2.c2p(0, 0))
        plot2.scale(1/4, about_point=axes2.c2p(0, 0)).to_corner(RIGHT)
        self.play(plot.animate.scale(1/4, about_point=axes.c2p(0, 0)).to_corner(LEFT), FadeIn(plot2))
        self.wait()
        title2.next_to(plot2, UP)
        self.play(Write(title2))
        self.wait()
        self.clear()

class Uniforme(Scene):
    def construct(self):
        desarrollo = MathTex("g_n(x) = ", "\\frac{1}{n}", " - x", "  \\rightarrow -x")
        desarrollo.set_color_by_tex("  \\rightarrow -x", YELLOW)
        c = SurroundingRectangle(desarrollo[1])
        self.play(Write(desarrollo[:-1]))
        self.wait(2)
        expl = MathTex("\\rightarrow 0", color = YELLOW).next_to(c, DOWN)
        self.play(Create(expl), Write(desarrollo[-1:]), Create(c))
        self.wait()
        self.play(Write(MathTex("\checkmark", color = GREEN).next_to(desarrollo[-1], RIGHT)))
        self.wait()
        self.clear()

        axes = Axes(
            x_range = [-8, 2, 1],
            y_range = [-2, 8, 1],
            tips = False
        )
        title = MathTex(r"g_n = \frac{1}{n} - x")
        g_n = VGroup()
        for n in range(1, 5):
            g_n += axes.plot(
                lambda x: 1/n - x,
                color = GREEN_A,
            )
        g_n += axes.plot(lambda x: -x, color = GREEN)
        plot = VGroup(axes, g_n.copy())
        self.play(Create(plot))
        self.wait()

        t = ValueTracker(-0.5)
        vert = VGroup(
            axes.plot_line_graph([t.get_value()]*(len(g_n) + 3), [-10, 10] + [1 / n - t.get_value() for n in range(1, 30, 5)] + [-t.get_value()], line_color = RED),
            MathTex("x = ", color = RED),
            DecimalNumber(color = RED)
        )
        vert[0].add_updater(lambda m: m.become(axes.plot_line_graph([t.get_value()]*(len(g_n) + 3), [-10, 10] + [1 / n - t.get_value() for n in range(1, 30, 5)] + [-t.get_value()], line_color = RED)))
        vert[1].add_updater(lambda m: m.move_to(axes.c2p(t.get_value(), 0) + RIGHT + DOWN))
        vert[2].add_updater(lambda m: m.next_to(vert[1]).set_value(t.get_value()))
        texto = VGroup(Arrow(start = ORIGIN, end = RIGHT + UP, color = GREEN).next_to(axes.c2p(t.get_value(), -t.get_value())))
        texto += Text("converge 'igual'", color = GREEN).next_to(texto[0], LEFT + DOWN)
        texto.add_updater(lambda m: m.next_to(axes.c2p(t.get_value(), -t.get_value()), LEFT + DOWN))
        self.wait()
        self.play(Create(vert))
        self.wait()
        self.play(Create(texto))
        self.wait()
        self.play(t.animate.set_value(-4))
        self.wait()