from manim import *


class Escena(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-0.1, 2, 1],
            y_range = ([-0.1, 1.5, 1])
        )
        title = MathTex(r"f_n(x) = \frac{nx^2}{nx^2 + 1}", color=BLUE)
        self.play(Write(title))
        self.wait()
        f_1 = axes.plot(lambda x: x ** 2 / (x ** 2 + 1), color=BLUE)
        self.play(
            title.animate.to_corner(UP),
            Create(axes),
            Create(f_1)
        )
        f_n = VGroup()
        for n in range(15):
            f_n += axes.plot(lambda x: n * x**2 / (n * x**2 + 1), color=BLUE_A)
        f_n_label = axes.get_graph_label(f_n[14], f"n = 1", color = BLUE)
        for n in range(2, 5):
            label = axes.get_graph_label(f_n[14], f"n = {n}", direction = UP)
            self.play(
                Create(f_n[n]),
                Transform(f_n_label, label),
            )
        self.wait()
        label = axes.get_graph_label(f_n[14], r"n = \infty", direction = UP)
        self.add(f_n)
        self.play(Transform(f_n_label, label))
        