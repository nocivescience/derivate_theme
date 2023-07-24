from manim import *
class DerivateScene(Scene):
    configuration = {
        'x_start': 3,
        'x_end': 7,
        'x_axes_config': {
            'x_range': [0, 10, 1],
        },
        'func_der': lambda x: .1*(x-2)*(x-8)*(x-5)+3,
        'func_der_config': {
            'color': RED,
            'stroke_width': 5,
        },
        'dot_radius': 0.1,
    }
    def construct(self):
        axes=self.axes=self.get_axes()
        func=axes.plot(self.configuration['func_der'], **self.configuration['func_der_config'])
        tangent= axes.plot_derivative_graph(func)  # estaba ingresando la funcvion lambda en vez de func
        tangent.set_opacity(0.2)
        integrales=axes.get_vertical_lines_to_graph(func, x_range=[3, 7, 1])
        secante=axes.get_secant_slope_group(
            3, func,
            dx=.1,
            dx_label=Tex("dx = 1.0"),
            dy_label="dy",
            dx_line_color=GREEN_B,
            secant_line_length=4,
            secant_line_color=RED_D,

        )
        dot_start=self.get_dot_form_x_coord(self.configuration['x_start'])
        dot_end=self.get_dot_form_x_coord(self.configuration['x_end'])
        line=VMobject()
        line.add_updater(self.get_line_updater(dot_start, dot_end, buff=0))
        self.add(axes, func, line, dot_start, dot_end, tangent, integrales, secante)
        for a, b in [(3, 7), (3, 4), (3, 3.5), (3, 3.3), (3, 3.1), (3, 3.5)]:
            self.move_dot(dot_end, a, b, run_time=3, rate_func=there_and_back)
            self.wait()
        self.wait()
    def move_dot(self, dot, start, end, *args, **kwargs):
        self.play(
            UpdateFromAlphaFunc(
                dot,
                self.get_dot_updater(start, end),
                *args,
                **kwargs
            )
        )
    def get_line_across_points(self, dot_start, dot_end, buff=3, **kwargs):
        reference_line=Line(dot_start.get_center(), dot_end.get_center(), buff=buff)
        vector= reference_line.get_unit_vector() # vector unitario
        return Line(dot_start.get_center()-vector*buff, dot_end.get_center()+vector*buff, **kwargs)
    def get_line_updater(self, dot_start, dot_end, buff=3, **kwargs):
        def updater(l):
            l.become(self.get_line_across_points(dot_start, dot_end, buff=buff, **kwargs))
        return updater
    def get_f(self, x_coord):
        return self.axes.c2p(x_coord, self.configuration['func_der'](x_coord))
    def get_dot_form_x_coord(self, x_coord):
        return Dot(self.get_f(x_coord), radius=self.configuration['dot_radius']).set_z_index(2)
    def get_axes(self):
        return Axes(**self.configuration['x_axes_config'])
    def get_dot_updater(self, start, end):
        def updater(d, alpha):
            x= interpolate(start, end, alpha)
            coord=self.get_f(x)
            d.move_to(coord)
        return updater