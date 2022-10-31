from manim import *


class Escena(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-0.1, 2, 1],
            y_range = ([-0.1, 1.5, 1])
        )
        title = MathTex(r"f_n(x) = \frac{nx}{nx^2 + 1}", color=BLUE)
        self.play(Write(title))
        self.wait()
        f_1 = axes.plot(lambda x: x / (x ** 2 + 1), color=BLUE)
        self.play(
            title.animate.to_corner(UP),
            Create(axes),
            Create(f_1)
        )
        f_n = VGroup(f_1.copy())
        for n in range(1, 20):
            f_n += axes.plot(lambda x: n * x / (n * x**2 + 1), color=BLUE_A)
        f_n_label = axes.get_graph_label(f_n[19], f"n = 1", color = BLUE)
        plot = VGroup(axes, f_n, f_n_label, title)
        for n in range(2, 5):
            self.play(
                FadeTransform(f_n[n-1], f_n[n]),
                Transform(f_n_label, axes.get_graph_label(f_n[19], f"n = {n}", direction = UP)),
            )
        self.play(
            FadeTransform(f_n[4], f_n[19]),
            Transform(f_n_label, axes.get_graph_label(f_n[19], r"n = 20", direction = UP, buff = 0.5))
        )
        self.wait()
        self.play(
            Create(plot),
            plot.animate.scale(0.5).move_to(LEFT * 2)
        )

        