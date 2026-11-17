"""Differential forms visualization section."""

from typing import TYPE_CHECKING, NamedTuple, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path

import manimgx as m

from deck import (
    CONTENT_FONT_SIZE,
    FRONTCOL,
    DeckScene,
    typst_preamble,
)

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


#   The one- and two-dimensional densities are superpositions of Gaussians: the number
#   of dots in a small interval (area) is proportional to the density there.
def gaussian_1d(x, center, width):
    return np.exp(-0.5 * ((x - center) / width) ** 2)


def density_1d(x):
    return (
        #0.6 * gaussian_1d(x, -1.7, 0.3)
        #+ 0.5 * gaussian_1d(x, 0.2, 0.3)
        + 0.5 * gaussian_1d(x, -1.5, 1.5)
        + 0.3 * gaussian_1d(x, 0.0, 10.0)
    )


def gaussian_2d(x, y, center, sigma):
    return np.exp(
        -0.5 * (((x - center[0]) / sigma) ** 2 + ((y - center[1]) / sigma) ** 2)
    )


def density_2d(x, y):
    return (
        #0.6 * gaussian_2d(x, y, (-0.65, 0.60), 0.42)
        #+ 0.5 * gaussian_2d(x, y, (0.60, 0.40), 0.40)
        + 0.5 * gaussian_2d(x, y, (-0.3, -1), 1.5)
        + 0.3 * gaussian_2d(x, y, (0.0, 0.0), 10.0)
    )


def points_in_polygon(x, y, polygon):
    """A boolean mask of the points (arrays x, y) inside the closed polygon."""
    shape = np.broadcast(x, y).shape
    points = np.column_stack([np.ravel(x), np.ravel(y)])
    inside = Path(polygon).contains_points(points)
    return inside.reshape(shape)


#   Matplotlib's viridis: its 256 colours, from dark purple to yellow.
VIRIDIS = plt.cm.viridis(np.linspace(0.0, 1.0, 256))[:, :3]
DENSITY_STOPS = np.column_stack([np.linspace(0.0, 1.0, 256), VIRIDIS])


def density_rgb(values):
    rgb = np.empty((*np.shape(values), 3))
    for channel in range(3):
        rgb[..., channel] = np.interp(
            values, DENSITY_STOPS[:, 0], DENSITY_STOPS[:, channel + 1]
        )
    return (255 * np.clip(rgb, 0.0, 1.0)).astype(np.uint8)


def regular_points(candidates, density, count, iterations=30, contains=None):
    """Regularly spaced points with a number density proportional to `density`.

    `candidates` is an (N, d) array of allowed positions, `density` maps an (M, d)
    array of points to M nonnegative weights, and `contains` (optional) maps such
    an array to a mask of the points inside the allowed region.

    Weighted Lloyd relaxation moves every point to the density-weighted centroid of
    its cell, so each point represents (approximately) the same amount of
    probability mass. This works in any dimension: 1D gives the regular spacing
    along a line, 2D the regular distribution over an area.
    """
    candidates = np.asarray(candidates, dtype=float)
    weights = density(candidates)
    dimension = candidates.shape[1]

    #   Farthest-point initialisation, weighted by the density: a deterministic,
    #   already fairly regular starting configuration.
    nearest_sq = np.full(len(candidates), np.inf)
    first = int(np.argmax(weights))
    sites = [candidates[first]]
    nearest_sq = np.sum((candidates - candidates[first]) ** 2, axis=1)
    for _ in range(count - 1):
        index = int(np.argmax(nearest_sq * weights))
        sites.append(candidates[index])
        nearest_sq = np.minimum(
            nearest_sq, np.sum((candidates - candidates[index]) ** 2, axis=1)
        )
    sites = np.array(sites)

    #   Weighted Lloyd relaxation: each site moves to the weighted centroid of the
    #   candidates closest to it, which equalises the mass represented by each site.
    #   Weighting the centroids by the squared density sharpens the equal-mass
    #   property: each point then covers an interval (area) proportional to
    #   1 / density.
    candidate_sq = np.sum(candidates**2, axis=1)
    centroid_weights = weights**2
    for _ in range(iterations):
        distances = (
            candidate_sq[:, np.newaxis]
            + np.sum(sites**2, axis=1)[np.newaxis, :]
            - 2.0 * candidates @ sites.T
        )
        assignments = np.argmin(distances, axis=1)
        masses = np.bincount(
            assignments, weights=centroid_weights, minlength=count
        )

        relaxed = sites.copy()
        occupied = masses > 0
        for axis in range(dimension):
            sums = np.bincount(
                assignments,
                weights=centroid_weights * candidates[:, axis],
                minlength=count,
            )
            relaxed[occupied, axis] = sums[occupied] / masses[occupied]

        #   A centroid can leave a concave region; snap it back to the inside.
        if contains is not None:
            still_inside = contains(relaxed)
            for index in np.flatnonzero(~still_inside):
                nearest = np.argmin(
                    np.sum((candidates - relaxed[index]) ** 2, axis=1)
                )
                relaxed[index] = candidates[nearest]
        sites = relaxed

    return sites


class Interval(m.VGroup):
    """A line segment with a tick at each end, drawn as one mobject."""

    def __init__(self, start, end, tick_height=0.22, **kwargs):
        self.tick_height = tick_height
        self.segment = m.Line(start, end, **kwargs)
        self.start_tick = m.Line(m.ORIGIN, m.UP * tick_height, **kwargs)
        self.end_tick = m.Line(m.ORIGIN, m.UP * tick_height, **kwargs)
        super().__init__(self.segment, self.start_tick, self.end_tick)
        self.set_endpoints(start, end)

    def set_endpoints(self, start, end):
        half = self.tick_height / 2
        self.segment.put_start_and_end_on(start, end)
        self.start_tick.put_start_and_end_on(
            start - half * m.UP, start + half * m.UP
        )
        self.end_tick.put_start_and_end_on(end - half * m.UP, end + half * m.UP)


class OneFormVisual(NamedTuple):
    """The 1D visual and the trackers that drive its interval."""

    group: m.VGroup
    x_axis: m.VGroup
    y_axis: m.VGroup
    graph: m.VMobject
    dots: m.Group[m.Mobject]
    interval: Interval
    formula: m.Group[m.Mobject]
    formula_orig: m.MathTypst
    x0: m.ValueTracker
    vx: m.ValueTracker


class TwoFormVisual(NamedTuple):
    """The 2D visual and the trackers that drive its parallelogram."""

    group: m.VGroup
    image: m.ImageMobject
    dots: m.Group[m.Mobject]
    region: m.VGroup
    colorbar: m.VGroup
    parallelogram: m.Polygon
    formula: m.MathTypst
    formula_orig: m.MathTypst
    numbers: list
    p0: m.ComplexValueTracker
    v: m.ComplexValueTracker
    u: m.ComplexValueTracker


def parallelogram_area(v, u):
    return abs(v.real * u.imag - v.imag * u.real)


def make_one_form_visual(dot_mass=0.08):
    """The line R with f(x), and dots on it whose density is f(x)."""
    x_min, x_max = -2.5, 2.5
    y_max = 1
    x_axis = m.NumberLine(
        [x_min, x_max, 1],
        length=5,
        include_ticks=False,
        include_tip=False,
        color=FRONTCOL,
    )
    y_axis = m.NumberLine(
        [0, y_max, 1],
        length=3.8,
        include_ticks=False,
        include_tip=False,
        rotation=m.PI / 2,
        color=FRONTCOL,
    )
    y_axis.next_to(x_axis.get_center(), m.UP, buff=0)

    def to_point(x, y):
        return (
            x_axis.number_to_point(x)
            + y_axis.number_to_point(y)
            - y_axis.number_to_point(0)
        )

    graph = m.ParametricFunction(
        lambda t: to_point(t, density_1d(t)),
        t_range=[x_min, x_max, 0.02],
        color=FRONTCOL,
    )

    #   One dot per `dot_mass` of mass under f.
    candidates = np.linspace(x_min, x_max, 2000)[:, np.newaxis]
    mass = np.trapezoid(density_1d(candidates[:, 0]), candidates[:, 0])
    count = max(1, round(mass / dot_mass))
    dot_x = regular_points(
        candidates,
        lambda p: density_1d(p[:, 0]),
        count,
    )[:, 0]
    dot_x = np.sort(dot_x)

    dots = m.VGroup(
        *[
            m.Dot(to_point(x, 0), radius=0.045, color=FRONTCOL)
            for x in dot_x
        ]
    )

    x0 = m.ValueTracker(dot_x[-3])
    vx = m.ValueTracker(dot_x[-1]-dot_x[-3])

    #   The interval [x0, x0 + vx], with a tick at each end: one mobject.
    interval = Interval(
        to_point(x0.get_value(), 0),
        to_point(x0.get_value() + vx.get_value(), 0),
        tick_height=0.22,
        color=m.RED,
        stroke_width=4,
        z_index=4,
    )
    interval.add_updater(
        lambda group: group.set_endpoints(
            to_point(x0.get_value(), 0),
            to_point(x0.get_value() + vx.get_value(), 0),
        )
    )

    preamble = typst_preamble(CONTENT_FONT_SIZE)
    x0_number = m.DecimalNumber(
        x0.get_value(), num_decimal_places=1, font_size=0.8*CONTENT_FONT_SIZE
    )
    arg_number = m.DecimalNumber(
        vx.get_value(), num_decimal_places=1, font_size=0.8*CONTENT_FONT_SIZE
    )
    value = m.DecimalNumber(
        density_1d(x0.get_value()) * vx.get_value() / dot_mass,
        num_decimal_places=1,
        font_size=0.8*CONTENT_FONT_SIZE,
    )
    formula_orig = m.MathTypst("(f(x) d x)(v)", font_size=CONTENT_FONT_SIZE, typst_preamble=preamble)
    formula = m.VGroup(
        m.MathTypst("(f(", font_size=0.8*CONTENT_FONT_SIZE, typst_preamble=preamble),
        x0_number,
        m.MathTypst(") d x)(", font_size=0.8*CONTENT_FONT_SIZE, typst_preamble=preamble),
        arg_number,
        m.MathTypst(") =", font_size=0.8*CONTENT_FONT_SIZE, typst_preamble=preamble),
        value,
    )
    x0_number.add_updater(lambda decimal: decimal.set_value(x0.get_value()))
    arg_number.add_updater(
        lambda decimal: decimal.set_value(vx.get_value())
    )
    value.add_updater(
        lambda decimal: decimal.set_value(
            density_1d(x0.get_value()) * vx.get_value() / dot_mass
        )
    )

    label = m.Typst(r"$RR$", typst_preamble=typst_preamble(CONTENT_FONT_SIZE)).next_to(x_axis.get_right(), buff=m.SMALL_BUFF)
    f_label = m.Typst(
        r"$f(x)$",
        font_size=CONTENT_FONT_SIZE,
        typst_preamble=typst_preamble(CONTENT_FONT_SIZE),
    ).next_to(y_axis.get_end(), m.DR, buff=0.12)
    vg = m.VGroup(x_axis, y_axis, label, f_label, graph, dots, interval)

    #   The parts follow the numbers' changing widths and stay above the plot.
    def layout_formula(group):
        first, x0_decimal, second, arg_decimal, third, result = group
        x0_decimal.next_to(first, m.RIGHT, buff=0.08)
        second.next_to(x0_decimal, m.RIGHT, buff=0.02)
        arg_decimal.next_to(second, m.RIGHT, buff=0.02)
        third.next_to(arg_decimal, m.RIGHT, buff=0.02)
        result.next_to(third, m.RIGHT, buff=0.10)
        group.center()
        group.next_to(vg.get_top(), m.UP, buff=m.MED_SMALL_BUFF)

    formula_orig.next_to(vg.get_top(), m.UP, buff=m.MED_SMALL_BUFF)
    formula.add_updater(layout_formula)
    layout_formula(formula)
    return OneFormVisual(
        m.VGroup(x_axis, y_axis, label, f_label, graph, dots, interval, formula, formula_orig),
        m.VGroup(x_axis,label),
        m.VGroup(y_axis,f_label),
        graph,
        dots,
        interval,
        formula,
        formula_orig,
        x0,
        vx,
    ), vg


def make_two_form_visual(dot_mass=0.02):
    """A region with density g, regularly spaced dots and a parallelogram."""
    half = 2.0
    resolution = 600
    angles = np.linspace(0.0, m.TAU, 240, endpoint=False)
    radii = (
        1.55
        + 0.25 * np.cos(3 * angles)
        + 0.10 * np.sin(2 * angles)
        + 0.06 * np.cos(5 * angles)
    )
    polygon = np.column_stack([radii * np.cos(angles), radii * np.sin(angles)])

    #   The color plot, as an RGBA image: transparent outside the region.
    xs = np.linspace(-half, half, resolution)
    ys = np.linspace(half, -half, resolution)
    grid_x, grid_y = np.meshgrid(xs, ys)
    inside = points_in_polygon(grid_x, grid_y, polygon)
    values = density_2d(grid_x, grid_y)
    value_min = values[inside].min()
    value_max = values[inside].max()
    normalized = np.zeros_like(values)
    normalized[inside] = (values[inside] - value_min) / (value_max - value_min)

    #   One dot per `dot_mass` of mass under g.
    cell_area = (2 * half / (resolution - 1)) ** 2
    mass = values[inside].sum() * cell_area
    count = max(1, round(mass / dot_mass))

    pixels = np.empty((resolution, resolution, 4), dtype=np.uint8)
    pixels[..., :3] = density_rgb(normalized)
    pixels[..., 3] = np.where(inside, 255, 0)
    image = m.ImageMobject(pixels)
    image.set_resampling_algorithm(m.RESAMPLING_ALGORITHMS["linear"])
    image.scale_to_fit_height(2 * half)

    #   Candidate positions for the dots: a coarser grid inside the eroded region.
    inner = polygon * (
        1.0 - 0.08 / np.linalg.norm(polygon, axis=1)
    )[:, np.newaxis]
    candidate_resolution = 180
    candidate_xs = np.linspace(-half, half, candidate_resolution)
    candidate_ys = np.linspace(-half, half, candidate_resolution)
    candidate_x, candidate_y = np.meshgrid(candidate_xs, candidate_ys)
    candidate_inside = points_in_polygon(candidate_x, candidate_y, inner)
    candidates = np.column_stack(
        [candidate_x[candidate_inside], candidate_y[candidate_inside]]
    )
    points = regular_points(
        candidates,
        lambda p: density_2d(p[:, 0], p[:, 1]),
        count=count,
        iterations=18,
        contains=lambda p: points_in_polygon(p[:, 0], p[:, 1], inner),
    )

    dots = m.VGroup(
        *[
            m.Dot([x, y, 0.0], radius=0.042, color=FRONTCOL)
            for x, y in points
        ]
    )

    border = m.Polygon(
        *[[x, y, 0.0] for x, y in polygon],
        stroke_color=FRONTCOL,
        stroke_width=2.5,
    )

    p0 = m.ComplexValueTracker(-0.5 + 0.9j)
    v = m.ComplexValueTracker(0.45 + 0.0j)
    u = m.ComplexValueTracker(0.05 + 0.45j)

    def parallelogram_vertices():
        origin = image.get_center()
        p = p0.get_value()
        vv = v.get_value()
        uu = u.get_value()
        return np.array(
            [
                origin + np.array([z.real, z.imag, 0.0])
                for z in (p, p + vv, p + vv + uu, p + uu)
            ]
        )

    parallelogram = m.Polygon(
        *parallelogram_vertices(),
        fill_color=m.RED,
        fill_opacity=0.12,
        stroke_color=m.RED,
        stroke_width=4,
        z_index=3,
    )

    def update_parallelogram(shape):
        vertices = parallelogram_vertices()
        shape.set_points_as_corners(np.vstack([vertices, vertices[0]]))

    parallelogram.add_updater(update_parallelogram)

    #   A viridis colorbar, labelled with the density g.
    colorbar_values = np.linspace(1.0, 0.0, 256)[:, np.newaxis]
    colorbar_pixels = np.empty((256, 1, 4), dtype=np.uint8)
    colorbar_pixels[..., :3] = density_rgb(colorbar_values)
    colorbar_pixels[..., 3] = 255
    colorbar = m.ImageMobject(
        colorbar_pixels, stroke_width=1.5, stroke_color=FRONTCOL
    )
    colorbar.set_resampling_algorithm(m.RESAMPLING_ALGORITHMS["linear"])
    colorbar.scale_to_fit_height(1.6)
    colorbar.stretch_to_fit_width(0.18)
    colorbar.next_to(border, m.RIGHT, buff=0.2)
    colorbar_label = m.Typst(
        r"$g(x,y)$",
        font_size=CONTENT_FONT_SIZE,
        typst_preamble=typst_preamble(CONTENT_FONT_SIZE),
    ).next_to(colorbar, m.RIGHT, buff=0.12)

    label = m.Typst(r"$M subset RR^2$", typst_preamble=typst_preamble(CONTENT_FONT_SIZE)).next_to(border.get_bottom(), buff=m.SMALL_BUFF)

    #   The title substitutes the position, the two vectors and the result.
    formula_orig = m.MathTypst("(g(x,y) d x and d y)(v,u)", font_size=CONTENT_FONT_SIZE, typst_preamble=typst_preamble(CONTENT_FONT_SIZE))
    formula = m.MathTypst(
        r"(g({{ -0.0 : x0 }}, {{ -0.0 : y0 }}) d x and d y)"
        r"(vec({{ 0.00 : vx }}, {{ 0.00 : vy }}),"
        r" vec({{ 0.00 : ux }}, {{ 0.00 : uy }}))"
        r" = {{ 0.0 : result }}",
        font_size=0.8*CONTENT_FONT_SIZE,
        typst_preamble=typst_preamble(0.8*CONTENT_FONT_SIZE),
    )
    for name in ("x0", "y0", "vx", "vy", "ux", "uy", "result"):
        formula.select(name).set_opacity(0)

    def bind_number(name, value, getter, decimals=1):
        number = m.DecimalNumber(
            value, num_decimal_places=decimals, font_size=0.8*CONTENT_FONT_SIZE
        )

        def update(decimal):
            decimal.set_value(getter())
            decimal.move_to(formula.select(name).get_center())

        number.add_updater(update)
        return number, update

    def area():
        return parallelogram_area(v.get_value(), u.get_value())

    def result_value():
        return (
            density_2d(p0.get_value().real, p0.get_value().imag)
            * area()
            / dot_mass
        )

    x0_number, update_x0 = bind_number(
        "x0", p0.get_value().real, lambda: p0.get_value().real
    )
    y0_number, update_y0 = bind_number(
        "y0", p0.get_value().imag, lambda: p0.get_value().imag
    )
    vx_number, update_vx = bind_number(
        "vx", v.get_value().real, lambda: v.get_value().real, decimals=2
    )
    vy_number, update_vy = bind_number(
        "vy", v.get_value().imag, lambda: v.get_value().imag, decimals=2
    )
    ux_number, update_ux = bind_number(
        "ux", u.get_value().real, lambda: u.get_value().real, decimals=2
    )
    uy_number, update_uy = bind_number(
        "uy", u.get_value().imag, lambda: u.get_value().imag, decimals=2
    )
    value, update_value = bind_number("result", result_value(), result_value)

    vg = m.VGroup(dots, label, colorbar, colorbar_label)
    formula.next_to(vg.get_top(), m.UP, buff=m.MED_SMALL_BUFF)
    formula_orig.next_to(vg.get_top(), m.UP, buff=m.MED_SMALL_BUFF)
    numbers = (
        (x0_number, update_x0),
        (y0_number, update_y0),
        (vx_number, update_vx),
        (vy_number, update_vy),
        (ux_number, update_ux),
        (uy_number, update_uy),
        (value, update_value),
    )
    for number, update in numbers:
        update(number)
    return TwoFormVisual(
        m.VGroup(
            image,
            border,
            dots,
            label,
            colorbar,
            colorbar_label,
            parallelogram,
            formula,
            formula_orig,
            *(number for number, _ in numbers),
        ),
        image,
        dots,
        m.VGroup(border,label),
        m.VGroup(colorbar,colorbar_label),
        parallelogram,
        formula,
        formula_orig,
        [number for number, _ in numbers],
        p0,
        v,
        u,
    ), vg


class FormsVisSection(_SectionBase):
    PAGE = 3
    TITLE = r"Interpretation of differential forms"

    def play_formsvis(self):
        self.nslide()
        points = self.get_lines(self.slide_title, """- number of dots inside an infinitesimal parallelpiped spanned by $k$ vectors""")
        self.camera.add_fixed_in_frame_mobjects(*points)
        for point in points:
            self.play(m.Write(point))
            self.nslide()

        left, vgl = make_one_form_visual()
        left.group.next_to(points[-1].get_corner(m.DL),m.DR)
        right, vgr = make_two_form_visual()
        right.group.next_to(left.group,m.RIGHT,aligned_edge=m.UP)
        #for vg in [vgl,vgr]:
        #    vg.add_background_rectangle(background_stroke_color=FRONTCOL,background_stroke_opacity=1.0,background_stroke_width=4,opacity=0.0)
        #    self.add_fixed_in_frame_mobjects(vg.background_rectangle)

        visuals = m.VGroup(left.group, right.group)
        self.camera.add_fixed_in_frame_mobjects(visuals)
        self.play(m.Write(left.x_axis),m.Write(left.formula_orig))
        self.nslide()
        self.play(m.Write(left.y_axis),m.Write(left.graph))
        self.nslide()
        self.play(m.Write(left.dots))
        self.nslide()
        self.play(m.Write(left.interval),m.ReplacementTransform(left.formula_orig, left.formula))
        self.nslide()

        #   Vary v_x, keeping x_0 fixed.
        vx_initial = left.vx.get_value()
        self.play(left.vx.animate.set_value(vx_initial/2), run_time=2)
        self.nslide()
        self.play(left.vx.animate.set_value(vx_initial), run_time=2)
        self.nslide()

        #   Move x_0, keeping v_x fixed.
        self.play(left.x0.animate.set_value(-1.0), run_time=4)
        self.nslide()

        self.play(m.Write(right.region), m.Write(right.formula_orig))
        self.nslide()
        self.play(m.Write(right.colorbar),m.Write(right.image))
        self.nslide()
        self.play(m.Write(right.dots))
        self.nslide()
        self.play(m.Write(right.parallelogram),m.ReplacementTransform(right.formula_orig,m.VGroup(right.formula,*right.numbers)))
        self.nslide()

        #   Vary u, keeping p_0 fixed.
        u_initial = right.u.get_value()
        self.play(right.u.animate.set_value(0.35+0.15j),run_time=2)
        self.nslide()
        self.play(right.u.animate.set_value(u_initial),run_time=2)
        self.nslide()

        #   Move p_0, keeping v and u fixed.
        self.play(right.p0.animate.set_value(-0.3 - 1.0j), run_time=4)
        self.nslide()


class FormsVisPreview(FormsVisSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(FormsVisSection)
        self.play_formsvis()
