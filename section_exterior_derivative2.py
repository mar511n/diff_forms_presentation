"""Exterior derivative visualization section."""

from typing import TYPE_CHECKING

import numpy as np
from isosurfaces import plot_isoline

import manimgx as m

from deck import DeckScene

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


#   Replace these to change the visualization; the contour levels and intersections
#   follow from them.
X_RANGE = (-2.5, 2.5)
Y_RANGE = (-2.0, 2.0)
CURVE_T_RANGE = (0.0, 1.0)
CONTOUR_FRACTIONS = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
CONTOUR_LIFT = 0.02
CONTOUR_MAX_POINTS = 120  # fewer points than raw marching-squares curves
SURFACE_RESOLUTION = (72, 56)

def gaussian_2d(x, y, x0r, y0r, sigma):
    return np.exp(
        -0.5 * (((x - (X_RANGE[0]+x0r*(X_RANGE[-1]-X_RANGE[0]))) / sigma) ** 2 + ((y - (Y_RANGE[0]+y0r*(Y_RANGE[-1]-Y_RANGE[0]))) / sigma) ** 2)
    )

def surface_height(x, y):
    """The height of the surface z = f(x, y); it takes NumPy arrays too."""
    return 1.8*gaussian_2d(x,y, 1.0,1.0, 1)+1.1*gaussian_2d(x,y, 1.1, 0.2, 1.5)+1.2*gaussian_2d(x,y, 0.5, 1.1, 1.0)+0.4*gaussian_2d(x,y, 0.4,0.4, 2.0)+0.3*gaussian_2d(x,y, 0.0, 1.0, 1.0)


def curve_xy(t):
    """The x- and y-coordinates of the curve, at z = 0."""
    return np.array(
        [
            -2.6 + 5.2 * t,
            0.5 * np.sin(m.TAU * t) - 0.8 + 2*t,
        ]
    )


def contour_levels():
    xs = np.linspace(*X_RANGE, 120)
    ys = np.linspace(*Y_RANGE, 100)
    grid_x, grid_y = np.meshgrid(xs, ys)
    values = surface_height(grid_x, grid_y)
    low, high = values.min(), values.max()
    return [low + fraction * (high - low) for fraction in CONTOUR_FRACTIONS]


def make_contours(levels):
    contours = []
    pmin = np.array([X_RANGE[0], Y_RANGE[0]])
    pmax = np.array([X_RANGE[1], Y_RANGE[1]])
    for level in levels:
        curves = plot_isoline(
            fn=lambda point, level=level: surface_height(point[0], point[1])
            - level,
            pmin=pmin,
            pmax=pmax,
            max_quads=5000,
        )
        contour = m.VMobject(color=m.RED, stroke_width=2.5)
        for curve in curves:
            if len(curve) < 2:
                continue
            curve = np.asarray(curve)
            if len(curve) > CONTOUR_MAX_POINTS:
                keep = np.linspace(
                    0, len(curve) - 1, CONTOUR_MAX_POINTS
                ).round().astype(int)
                curve = curve[keep]
            points = np.column_stack(
                [
                    curve[:, 0],
                    curve[:, 1],
                    np.full(len(curve), level + CONTOUR_LIFT),
                ]
            )
            contour.start_new_path(points[0])
            contour.add_points_as_corners(points[1:])
        if contour.points.size:
            contours.append((level, contour))
    return contours


def curve_intersections(levels):
    """Where the curve crosses the level sets of f."""
    ts = np.linspace(*CURVE_T_RANGE, 1000)
    xy = np.array([curve_xy(t) for t in ts])
    values = surface_height(xy[:, 0], xy[:, 1])
    points = []
    for level in levels:
        difference = values - level
        for index in np.where(difference[:-1] * difference[1:] < 0)[0]:
            t0, t1 = ts[index], ts[index + 1]
            d0, d1 = difference[index], difference[index + 1]
            t = t0 - d0 * (t1 - t0) / (d1 - d0)
            x, y = curve_xy(t)
            point = np.array([x, y, 0.0])
            if all(np.linalg.norm(point - other) > 1e-3 for other in points):
                points.append(point)
    return points


class ExteriorDerivative2Section(_SectionBase):
    PAGE = 7
    TITLE = r"Visual interpretation of $d$ for $0$-forms"

    def play_ext_deriv2(self):
        self.nslide()

        self.set_camera_orientation(
            phi=65 * m.DEGREES,
            theta=-100 * m.DEGREES,
            zoom=1.5,
            frame_center=(0, 0, 1.0),
        )

        surface = m.Surface(
            lambda u, v: np.array([u, v, surface_height(u, v)]),
            u_range=X_RANGE,
            v_range=Y_RANGE,
            checkerboard_colors=[m.GREY_C,m.GREY_D],
            fill_opacity=1.0,
            stroke_width=0,
        )

        levels = contour_levels()
        contours = make_contours(levels)
        contour_group = m.VGroup(*[contour for _, contour in contours])

        #   Animating the mesh is much slower than showing it at the slide boundary.
        self.play(m.Create(surface))
        self.nslide()

        self.play(
            m.LaggedStart(
                *[m.Create(contour) for _, contour in contours],
                lag_ratio=0.1,
                run_time=1,
            )
        )
        self.nslide()


        self.move_camera(
            phi=0,
            theta=-90 * m.DEGREES,
            frame_center=(0, 0.2, 0),
            added_anims=[
                *[
                    contour.animate.shift(-(level + CONTOUR_LIFT) * m.OUT)
                    for level, contour in contours
                ],
                m.Uncreate(surface),
            ],
            run_time=2,
        )
        self.nslide()

        curve = m.ParametricFunction(
            lambda t: np.array([*curve_xy(t), 0.0]),
            t_range=[*CURVE_T_RANGE, 0.005],
            color=m.BLUE,
            stroke_width=4,
        )
        self.play(m.Create(curve))
        self.nslide()

        intersection_points = curve_intersections(levels)
        dots = m.VGroup(
            *[
                m.Dot3D(point, radius=0.07, color=m.YELLOW)
                for point in intersection_points
            ]
        )
        self.play(m.Create(dots))
        self.nslide()

        self.play(m.Uncreate(contour_group))
        self.nslide()


class ExteriorDerivative2Preview(ExteriorDerivative2Section, DeckScene):
    def construct(self) -> None:
        self.prepare_section(ExteriorDerivative2Section)
        self.play_ext_deriv2()
