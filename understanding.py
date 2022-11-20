from manim import *

class Main(Scene):
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
        self.wait()
        self.play(
            title.animate.to_corner(UP + LEFT),
            GrowFromCenter(axes),
            Create(f_n[0])
        )
        self.wait()
        f_n_label = axes.get_graph_label(f_n[0], "n=1")
        plot = VGroup(axes, f_n)
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
        self.play(plot.animate.scale(2).move_to(UP*0.5 + LEFT*6.5))
        self.wait()
        t = ValueTracker(2.5)
        vert = VGroup(
            axes.plot_line_graph([t.get_value()]*(len(f_n) + 1), [0] + [(t.get_value() ** 2 + n*t.get_value()) / n for n in range(1, 30, 5)] + [t.get_value()], line_color = RED),
            Text("x = ", color = RED),
            DecimalNumber(color = RED)
        )
        vert[1].next_to(vert[0], DOWN)
        vert[2].next_to(vert[1]).add_updater(lambda m: m.set_value(t.get_value()))
        self.play(Create(vert))