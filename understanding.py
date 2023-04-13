from manim import *

class Main(Scene):
    def construct(self):
        Intro.construct(self)
        Puntual.construct(self)
        Uniforme.construct(self)
        Comparacion.construct(self)
        Dini.construct(self)

def graficar_funciones(func, rango = range(1, 30, 5), x_r = [-4, 4, 1], y_r = [-4, 4, 1], color = WHITE):
        axes = Axes(x_range = x_r, y_range = y_r, tips = False)
        f_n = VGroup(*[axes.plot(lambda x: func(n, x), color = color) for n in rango])
        return VGroup(axes, f_n)

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
        a_n = MathTex("a_n = \\frac{1}{n}").move_to(RIGHT)
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
        self.wait(0.5)
        self.play(n.animate.set_value(99))
        self.wait(0.25)
        self.play(p.animate.become(Dot(recta.n2p(0), color = RED)))
        self.wait(2)
        a_n.clear_updaters()
        self.play(a_n.animate.become(MathTex("a_n", " \\rightarrow ", "0").set_color_by_tex(" \\rightarrow ", YELLOW).move_to(RIGHT)))
        self.wait(2)
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
        self.wait(4)
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

        converge = MathTex("\\text{?`}\\rightarrow ?")
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

        plot2 = graficar_funciones(lambda n, x: 1/n - x, range(1, 5), [-8, 2, 1], [-2, 8, 1], GREEN_A)
        plot2[1] += plot2[0].plot(lambda x: -x, color = GREEN)
        title2 = MathTex(r"g_n = \frac{1}{n} - x", color = GREEN_A)
        self.remove(texto, vert)
        plot2.scale(2, about_point=plot2[0].c2p(0, 0))
        plot2.scale(1/4, about_point=plot2[0].c2p(0, 0)).to_corner(RIGHT)
        self.play(plot.animate.scale(1/4, about_point=axes.c2p(0, 0)).to_corner(LEFT), FadeIn(plot2))
        self.wait()
        title2.next_to(plot2, UP)
        self.play(Write(title2))
        self.wait(4)
        self.clear()

class Uniforme(Scene):
    def construct(self):
        desarrollo = MathTex("g_n(x) = ", "\\frac{1}{n}", " - x", "  \\rightarrow -x").set_color_by_tex("  \\rightarrow -x", YELLOW)
        c = SurroundingRectangle(desarrollo[1])
        self.play(Write(desarrollo[:-1]))
        self.wait(2)
        expl = MathTex("\\rightarrow 0", color = YELLOW).next_to(c, DOWN)
        self.play(Create(expl), Write(desarrollo[-1:]), Create(c))
        self.wait(4)
        self.play(Write(MathTex("\checkmark", color = GREEN).next_to(desarrollo[-1], RIGHT)))
        self.wait(2)
        self.clear()

        plot = graficar_funciones(lambda n, x: 1/n - x, range(1, 5), [-8, 2, 1], [-2, 8, 1], GREEN_A)
        plot[1] += plot[0].plot(lambda x: -x, color = GREEN)
        self.play(Create(plot))
        self.wait()

        t = ValueTracker(-0.5)
        vert = VGroup(
            plot[0].plot_line_graph([t.get_value()]*(len(plot[1]) + 3), [-10, 10] + [1 / n - t.get_value() for n in range(1, 30, 5)] + [-t.get_value()], line_color = RED),
            MathTex("x = ", color = RED),
            DecimalNumber(color = RED)
        )
        vert[0].add_updater(lambda m: m.become(plot[0].plot_line_graph([t.get_value()]*(len(plot[1]) + 3), [-10, 10] + [1 / n - t.get_value() for n in range(1, 30, 5)] + [-t.get_value()], line_color = RED)))
        vert[1].add_updater(lambda m: m.move_to(plot[0].c2p(t.get_value(), 0) + RIGHT + DOWN))
        vert[2].add_updater(lambda m: m.next_to(vert[1]).set_value(t.get_value()))
        texto = VGroup(Arrow(start = ORIGIN, end = RIGHT + UP, color = GREEN).next_to(plot[0].c2p(t.get_value(), -t.get_value())))
        texto += Text("converge 'igual'", color = GREEN).next_to(texto[0], LEFT + DOWN)
        texto.add_updater(lambda m: m.next_to(plot[0].c2p(t.get_value(), -t.get_value()), LEFT + DOWN))
        self.wait()
        self.play(Create(vert))
        self.wait()
        self.play(Create(texto))
        self.wait()
        self.play(t.animate.set_value(-4))
        self.wait(2)
        self.clear()

class Comparacion(Scene):
    def construct(self):
        desarrollo = MathTex(r'f_n(x) = \frac{x^2 + nx}{n}  &\rightarrow x\\', r'&\neq\\', r'g_n(x) = \frac{1}{n} - x',  r'&\rightarrow', " -x")
        self.play(Write(desarrollo[0]), Write(desarrollo[2:]))
        self.wait(2)
        self.play(Write(desarrollo[1]))
        self.wait(4)
        self.play(desarrollo.animate.become(
            MathTex(r'f_n(x) = \frac{x^2 + nx}{n}  &\rightarrow x\\', r'&\neq\\', r'g_n(x) = \frac{1}{n} - x',  r'&\rightrightarrows', " -x").set_color_by_tex(r'&\rightrightarrows', YELLOW)
        ))
        self.wait(2)
        self.clear()
        self.play(Write(MathTex("\\text{?`}\\rightrightarrows ?")))
        self.wait(2)
        self.clear()

        plot = graficar_funciones(lambda n, x: (x ** 2 + n*x) / n, range(1, 30, 5), [-1, 3, 1], [-1, 3, 1], BLUE_A)
        plot[1] += plot[0].plot(lambda x: x, color = BLUE)
        plot2 = graficar_funciones(lambda n, x: 1/n - x, range(1, 5), [-3, 1, 1], [-1, 3, 1], GREEN_A)
        plot2[1] += plot2[0].plot(lambda x: -x, color = GREEN)
        plot2.scale(1/2, about_point=plot2[0].c2p(0, 0)).to_corner(RIGHT + UP)
        plot.scale(1/2, about_point=plot[0].c2p(0, 0)).shift(UP*2 + LEFT*2)
        self.play(FadeIn(plot), FadeIn(plot2))

        tg = ValueTracker(-1.5)
        epsg = MathTex("(\hspace{0.5em})", color = RED).rotate(PI/3)
        epsg.add_updater(lambda m: m.move_to(plot2[0].c2p(tg.get_value(), -tg.get_value())))
        self.play(Create(epsg))
        self.wait()
        self.play(plot2[1][:2].animate.set_color(RED_A))
        self.wait()
        self.play(epsg.animate.become(MathTex("(\hspace{3em})", color = RED).rotate(PI/3)),
                  plot2[1][:2].animate.set_color(GREEN_A))
        self.wait()
        self.play(tg.animate.set_value(-2.5))
        self.play(tg.animate.set_value(0))
        self.wait()
        self.play(Write(MathTex("g_n(x) = \\frac{1}{n} - x \\rightrightarrows -x", "\\, \\checkmark", color = GREEN_A).set_color_by_tex(" \\checkmark", GREEN).next_to(plot2, DOWN)))
        self.wait(2)

        tf = ValueTracker(0.25)
        epsf = MathTex("(\hspace{0.5em})", color = RED).rotate(-PI/3)
        epsf.add_updater(lambda m: m.move_to(plot[0].c2p(tf.get_value(), tf.get_value())))
        self.play(Create(epsf))
        self.wait()
        self.play(tf.animate.set_value(0.5),
                  plot[1][0].animate.set_color(RED_A))
        self.wait()
        self.play(epsf.animate.become(MathTex("(\hspace{1em})", color = RED).rotate(-PI/3)),
                  plot[1][0].animate.set_color(BLUE_A))
        self.wait(DEFAULT_WAIT_TIME / 2)
        self.play(tf.animate.set_value(1),
                  plot[1][0].animate.set_color(RED_A))
        self.wait(DEFAULT_WAIT_TIME / 4)
        self.play(epsf.animate.become(MathTex("(\hspace{2em})", color = RED).rotate(-PI/3)),
                  plot[1][0].animate.set_color(BLUE_A))
        self.wait(DEFAULT_WAIT_TIME / 4)
        self.play(tf.animate.set_value(2.5),
                  plot[1][:2].animate.set_color(RED_A))
        self.wait()
        self.play(Write(MathTex("f_n(x) = \\frac{x^2 + nx}{n} \\rightrightarrows x", "\\, \\chi", color = BLUE_A).set_color_by_tex("\\, \\chi", RED).next_to(plot, DOWN)))
        self.wait(2)
        self.clear()

class Dini(Scene):
    def construct(self):
        teodini = Text("Teorema de Dini")
        self.play(Write(teodini))
        self.wait(2)

        plot = graficar_funciones(lambda n, x: (x ** 2 + n*x) / n, range(1, 30, 5), [-1, 3, 1], [-1, 3, 1], BLUE_A)
        plot[1] += plot[0].plot(lambda x: x, color = BLUE)
        self.play(FadeOut(teodini), FadeIn(plot))
        self.wait(0.5)
        compacto = MathTex("[", "]", color = BLUE, width = 10)
        compacto[0].move_to(plot[0].c2p(0.02, 0))
        compacto[1].move_to(plot[0].c2p(0.98, 0))
        self.play(Create(compacto))
        self.wait(0.5)
        axes = Axes(x_range = [0, 1, 1], y_range = [0, 1, 1], tips = False)
        f_n = VGroup(*[axes.plot(lambda x: (x ** 2 + n*x) / n, color = BLUE_A) for n in range(1, 30, 5)])
        f_n += axes.plot(lambda x: x, color = BLUE)
        f_n.scale(1/4).move_to(plot[0].c2p(0.5, 1))
        self.play(FadeOut(plot[1]), FadeIn(f_n))
        self.wait(2)

        tf = ValueTracker(0.25)
        epsf = MathTex("(\hspace{0.5em})", color = RED).rotate(-PI/3)
        epsf.add_updater(lambda m: m.move_to(plot[0].c2p(tf.get_value(), tf.get_value())))
        self.play(Create(epsf))
        self.wait()
        self.play(epsf.animate.become(MathTex("(\hspace{2em})", color = RED).rotate(-PI/3)))
        self.wait(0.25)
        self.play(tf.animate.set_value(0.8),
                  f_n[0].animate.set_color(RED_A))
        self.wait(0.25)
        self.play(epsf.animate.become(MathTex("(\hspace{8em})", color = RED).rotate(-PI/3)),
                  f_n[0].animate.set_color(BLUE_A))
        self.wait(0.5)
        self.play(tf.animate.set_value(1))
        self.wait(0.125)
        self.play(tf.animate.set_value(0))
        self.wait(0.125)
        self.play(tf.animate.set_value(1))
        self.wait()
        self.clear()

        title = MathTex("f_n(x) = \\frac{x^2 + nx}{n} \\rightrightarrows x", "\\quad \\chi").set_color_by_tex("\\quad \\chi", RED)
        self.play(Write(title))
        self.wait(2)
        self.play(Write(MathTex("\\text{monótona en } [a, b]").next_to(title, UP*2)))
        self.wait()
        self.play(title.animate.become(MathTex("f_n(x) = \\frac{x^2 + nx}{n} \\rightrightarrows x", "\\quad \\checkmark").set_color_by_tex("\\quad \\checkmark", GREEN)))