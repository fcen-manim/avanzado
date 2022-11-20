from manim import *

class Escena(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-10, 10, 1],
            y_range = [-5, 10, 1]
        )
        title = MathTex(r"f_n(x) = \frac{x^2 + nx}{n}")
        f_n = VGroup(axes.plot(lambda x: x ** 2 + x))
        
        self.play(Write(title))
        self.wait()
        self.play(
            title.animate.to_corner(UP + LEFT),
            Create(axes),
            Create(f_n[0])
        )
        self.wait()
        for n in range(1, 31):
            f_n += axes.plot(lambda x: (x ** 2 + n*x) / n)
        f_n_label = axes.get_graph_label(f_n[0], "n=1")
        plot = VGroup(axes, f_n, f_n_label, title)
        for n in range(2, 5):
            self.play(
                FadeTransform(f_n[n-1], f_n[n]),
                Transform(f_n_label, axes.get_graph_label(f_n[0], f"n = {n}"))
            )
        self.wait()