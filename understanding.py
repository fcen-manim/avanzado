from manim import *

class Escena(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-5, 5, 1],
            y_range = [-2, 5, 1],
            tips = False
        )
        title = MathTex(r"f_n(x) = \frac{x^2 + nx}{n}", color = BLUE_A)
        f_n = VGroup(axes.plot(lambda x: x ** 2 + x, color = BLUE_A))
        
        self.play(Write(title))
        self.wait()
        self.play(
            title.animate.to_corner(UP + LEFT),
            Create(axes),
            Create(f_n[0])
        )
        self.wait()
        for n in range(1, 30, 5):
            f_n += axes.plot(lambda x: (x ** 2 + n*x) / n, color = BLUE_A)
        f_n += axes.plot(lambda x: x, color = BLUE)
        f_n_label = axes.get_graph_label(f_n[0], "n=1")
        plot = VGroup(axes, f_n)
        for n in range(1, 6):
            self.play(
                FadeTransform(f_n[n-1], f_n[n]),
                Transform(f_n_label, axes.get_graph_label(f_n[0], f"n = {n}"))
            )
        self.wait()
        self.play(
            FadeTransform(f_n[5], f_n[len(f_n) - 1]),
            Transform(f_n_label, axes.get_graph_label(f_n[0], MathTex("n = \infty"), color = BLUE))
        )
        self.wait(5)

        self.clear()
        converge = Text("¿Converge?")
        self.play(Write(converge))