"""Cartan structure equations: the derivation in differential forms only.

The local frame, its dual coframe and the connection 1-forms are the only
ingredients. Expanding the definitions of torsion and curvature in the frame and
identifying the two resulting pieces with the exterior derivative and the wedge
product gives the structure equations; no coordinate components appear.

Four sections share the topic, so each of the four slides carries its own page
number: the setup (11), the first equation (12), the second equation (13) and the
matrix form (14).
"""

from typing import TYPE_CHECKING

import numpy as np

import manimgx as m

from deck import (
    CONTENT_FONT_SIZE,
    FRONTCOL,
    DeckScene,
    split_typst_lines,
    typst_preamble,
)

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


MATH_FONT_SIZE = 0.8 * CONTENT_FONT_SIZE
NOTE_FONT_SIZE = 0.62 * CONTENT_FONT_SIZE
RECAP_FONT_SIZE = 0.72 * CONTENT_FONT_SIZE
RESULT_FONT_SIZE = CONTENT_FONT_SIZE
MATRIX_FONT_SIZE = 1.2 * CONTENT_FONT_SIZE
D_COLOR = m.BLUE  # the exterior-derivative part
W_COLOR = m.YELLOW  # the connection part


def typeset(code, font_size=MATH_FONT_SIZE):
    """A formula in display math, at this section's sizes."""
    return m.MathTypst(
        code, font_size=font_size, typst_preamble=typst_preamble(font_size)
    )


def typeset_text(code, font_size=MATH_FONT_SIZE):
    """Typeset text with inline math, at this section's sizes."""
    return m.Typst(code, font_size=font_size, typst_preamble=typst_preamble(font_size))


def formula_block(code, count, font_size=MATH_FONT_SIZE):
    """An aligned formula and its `count` visual lines, top to bottom."""
    block = typeset(code, font_size)
    return block, split_typst_lines(block, count)


def dim(mobject, opacity=0.6):
    """Dim a typeset aside: a definition recalled, a footnote, an outlook."""
    return mobject.set_opacity(opacity)


#   The setup slide's globe on the right: a sphere with the coordinate lines of its
#   chart, the point p with the coordinate frame and the general frame e_a, and the
#   frame carried along a short geodesic to a nearby point p2.
SPHERE_RADIUS = 2.5
SPHERE_SCREEN = np.array([4.2, -0.1])  # where the centre lands, in frame units
POINT_THETA = 60 * m.DEGREES  # the chart coordinates of p
POINT_PHI = -15 * m.DEGREES
FRAME_LENGTH = 0.85  # the arrows of both frames, in scene units
FRAME_ANGLE = 30 * m.DEGREES  # how far e_a is turned from the coordinate frame
PATH_ANGLE = 40 * m.DEGREES  # how far the frame travels to p2
PATH_HEADING = 270 * m.DEGREES  # the path's direction at p, from theta to phi
LABEL_FONT_SIZE = 0.75 * CONTENT_FONT_SIZE

#   The two flat pictures that follow the globe: the torsion and the curvature of
#   the connection, drawn on one pair of axes.
PICTURE_ORIGIN = np.array([2.5, -2.0, 0.0])
PICTURE_Y = np.array([2.0, 0.45, 0.0])
PICTURE_X = np.array([1.25, 1.75, 0.0])
PICTURE_Z = np.array([-0.2, 1.3, 0.0])
TORSION_DIFF = np.array([-1.0,0.8,0])/2
CURVATURE_DIFF = -np.array([-1.4,0.1,0])/2


def turned(vector, angle):
    """A vector of the plane, turned by an angle."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c * vector[0] - s * vector[1], s * vector[0] + c * vector[1], 0.0])


def left_of(vector, distance):
    """A displacement of `distance`, to the left of a direction."""
    normal = np.array([-vector[1], vector[0], 0.0])
    return normal / np.linalg.norm(normal) * distance


def picture_arrow(start, end, color, ratio=12, tip_ratio=0.22):
    """An arrow of the flat pictures: a vector, or the gap between two vectors."""
    return m.Arrow(
        start,
        end,
        buff=0,
        color=color,
        stroke_width=6,
        max_stroke_width_to_length_ratio=ratio,
        max_tip_length_to_length_ratio=tip_ratio,
    )


def picture_label(code, point, color=FRONTCOL):
    """A label of the flat pictures, centred on a point."""
    return m.Typst(
        code,
        font_size=LABEL_FONT_SIZE,
        fill_color=color,
        typst_preamble=typst_preamble(LABEL_FONT_SIZE),
    ).move_to(point)


def camera_rows(camera):
    """The camera's screen axes in world coordinates: right, up, toward the viewer."""
    phi, theta, gamma = camera.get_phi(), camera.get_theta(), camera.get_gamma()
    c, s = np.cos(-phi), np.sin(-phi)

    def rz(angle):
        return np.array(
            [
                [np.cos(angle), -np.sin(angle), 0.0],
                [np.sin(angle), np.cos(angle), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )

    rx = np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])
    return rz(gamma) @ rx @ rz(-theta - np.pi / 2)


def screen_point(camera, point):
    """Where a world point lands on the screen, in frame coordinates."""
    rows = camera_rows(camera)
    center = np.asarray(camera.frame_center, dtype=float)
    zoom, focal = camera.get_zoom(), camera.get_focal_distance()
    middle = rows @ center
    point = np.asarray(point, dtype=float)
    depth = (focal + middle[2] - rows[2] @ point) / focal
    return np.array(
        [
            zoom * (rows[0] @ point - middle[0]) / depth,
            zoom * (rows[1] @ point - middle[1]) / depth,
            0.0,
        ]
    )


def unit_point(theta, phi):
    """The point of the unit sphere at colatitude theta and longitude phi."""
    return np.array(
        [
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta),
        ]
    )


def theta_direction(theta, phi):
    """The unit tangent at (theta, phi) toward growing theta."""
    return np.array(
        [
            np.cos(theta) * np.cos(phi),
            np.cos(theta) * np.sin(phi),
            -np.sin(theta),
        ]
    )


def phi_direction(phi):
    """The unit tangent toward growing phi."""
    return np.array([-np.sin(phi), np.cos(phi), 0.0])


def axis_rotation(axis, angle):
    """Rodrigues' rotation about a direction, by an angle in radians."""
    x, y, z = np.asarray(axis, dtype=float) / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    k = 1 - c
    return np.array(
        [
            [c + x * x * k, x * y * k - z * s, x * z * k + y * s],
            [y * x * k + z * s, c + y * y * k, y * z * k - x * s],
            [z * x * k - y * s, z * y * k + x * s, c + z * z * k],
        ]
    )


def orbit(points, center, axis, angle):
    """Points turned about a centre, around an axis."""
    rotation = axis_rotation(axis, angle)
    points = np.asarray(points, dtype=float)
    center = np.asarray(center, dtype=float)
    return points @ rotation.T + center - center @ rotation.T


def polyline(points, color, stroke_width=1.6, opacity=0.55):
    """A curve through points in space."""
    path = m.VMobject(color=color, stroke_width=stroke_width)
    path.set_points_as_corners(np.asarray(points, dtype=float))
    path.set_stroke(opacity=opacity)
    return path


def visible_runs(points, center, toward):
    """The runs of a sampled curve on the camera's side of the sphere."""
    runs, run = [], []
    for point in points:
        if np.dot(point - center, toward) > 0.0:
            run.append(point)
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    return [run for run in runs if len(run) > 1]


def sphere_grid(center, toward):
    """The coordinate lines of the sphere's chart, the halves the camera sees."""
    grid = m.VGroup()
    for theta in np.linspace(0.25 * np.pi, 0.75 * np.pi, 5):
        points = [
            center + SPHERE_RADIUS * unit_point(theta, phi)
            for phi in np.linspace(0.0, m.TAU, 181)
        ]
        for run in visible_runs(points, center, toward):
            grid.add(polyline(run, m.GREY_B))
    for phi in np.linspace(0.0, m.TAU, 12, endpoint=False):
        #   The meridians stop short of the poles: there they would crowd into a blob.
        points = [
            center + SPHERE_RADIUS * unit_point(theta, phi)
            for theta in np.linspace(0.12 * np.pi, 0.88 * np.pi, 91)
        ]
        for run in visible_runs(points, center, toward):
            grid.add(polyline(run, m.GREY_B))
    return grid


def tangent_square(point, normal, first, second, half=0.6, lift=0.0):
    """A translucent square of the tangent plane at a point of the sphere."""
    corners = [
        point + lift * normal + a * half * first + b * half * second
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    square = m.Polygon(
        *corners,
        fill_color=m.GREY_A,
        fill_opacity=0.16,
        stroke_color=FRONTCOL,
        stroke_width=1.2,
    )
    square.set_stroke(opacity=0.7)
    return square


class CartanSetupSection(_SectionBase):
    PAGE = 11
    TITLE = r"Cartan structure equations"

    def globe_label(self, code, point, offset, color=FRONTCOL):
        """A label pinned where a world point is drawn, moved by a screen offset."""
        label = m.Typst(
            code,
            font_size=LABEL_FONT_SIZE,
            fill_color=color,
            typst_preamble=typst_preamble(LABEL_FONT_SIZE),
        )
        label.move_to(screen_point(self.camera, point) + np.array([*offset, 0.0]))
        return label

    def play_cartan_setup(self):
        self.nslide()
        frame = typeset_text(
            r"Local frame $e_a$ and dual coframe $e^a$: "
            r"#h(0.3cm) $e^a (e_b) = delta^a_b$"
        )
        connection = typeset_text(
            r"Connection 1-forms: #h(0.3cm) "
            r"$nabla_X e_b = omega^a #h(0cm)_b (X) e_a$"
        )
        torsion = typeset(
            r"T (X,Y) &= nabla_X Y - nabla_Y X - [X,Y] \ "
            r"T^a (X,Y) &= e^a (T (X,Y))"
        )
        curvature = typeset(
            r"R (X,Y) Z &= nabla_X nabla_Y Z - nabla_Y nabla_X Z "
            r"- nabla_([X,Y]) Z \ "
            r"R (X,Y) e_b &= R^a #h(0cm)_b (X,Y) e_a"
        )
        goal = typeset_text(
            r"Goal: express torsion $T^a$ and curvature $R^a #h(0cm)_b$ "
            r"through $d$ and $omega$."
        )

        frame.next_to(
            self.slide_title, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT
        )
        connection.next_to(frame, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        torsion.next_to(connection, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        curvature.next_to(torsion, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        goal.next_to(curvature, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)

        #   The globe on the right. The text is pinned, so turning the camera only
        #   turns the globe.
        self.set_camera_orientation(
            phi=65 * m.DEGREES,
            theta=-30 * m.DEGREES,
            zoom=1,
            frame_center=m.ORIGIN,
        )
        rows = camera_rows(self.camera)
        center = SPHERE_SCREEN[0] * rows[0] + SPHERE_SCREEN[1] * rows[1]
        sphere = m.Sphere(
            center=center,
            radius=SPHERE_RADIUS,
            checkerboard_colors=[m.GREY_D, m.GREY_E],
            fill_opacity=1.0,
            stroke_width=0,
        )

        normal = unit_point(POINT_THETA, POINT_PHI)
        point = center + SPHERE_RADIUS * normal
        first = theta_direction(POINT_THETA, POINT_PHI)
        second = phi_direction(POINT_PHI)
        directions = (
            np.cos(FRAME_ANGLE) * first + np.sin(FRAME_ANGLE) * second,
            -np.sin(FRAME_ANGLE) * first + np.cos(FRAME_ANGLE) * second,
        )

        dot = m.Dot3D(point + 0.015 * normal, radius=0.065, color=m.WHITE)
        coordinate_frame = m.VGroup(
            *[
                m.Arrow3D(
                    point,
                    point + FRAME_LENGTH * direction,
                    thickness=0.012,
                    height=0.2,
                    base_radius=0.05,
                    color=m.WHITE,
                )
                for direction in (first, second)
            ]
        )
        general_frame = m.VGroup(
            *[
                m.Arrow3D(
                    point,
                    point + FRAME_LENGTH * direction,
                    thickness=0.016,
                    height=0.22,
                    base_radius=0.055,
                    color=m.TEAL,
                )
                for direction in directions
            ]
        )

        p_label = self.globe_label(r"$p$", point, (-0.1, -0.24))
        mu_label = self.globe_label(
            r"$bold(partial)_mu$", point + FRAME_LENGTH * second, (0.22, -0.04)
        )
        ea_label = self.globe_label(
            r"$bold(e)_a$",
            point + FRAME_LENGTH * directions[1],
            (0.2, 0.07),
            m.TEAL,
        )

        #   The frame travels along a geodesic: start p, tangent X, arrival p2.
        heading = np.cos(PATH_HEADING) * first + np.sin(PATH_HEADING) * second
        axis = np.cross(normal, heading)
        steps = np.linspace(0.0, 1.0, 41)
        path_points = [
            center
            + 1.02 * SPHERE_RADIUS * (axis_rotation(axis, step * PATH_ANGLE) @ normal)
            for step in steps
        ]
        #   X is the curve's first piece: the curve starts where the arrow ends.
        curve = polyline(path_points, m.RED, stroke_width=4.5, opacity=1.0)
        x_arrow = m.Arrow3D(
            point,
            point + 0.4 * heading,
            thickness=0.014,
            height=0.2,
            base_radius=0.05,
            color=m.RED,
        )
        second_normal = axis_rotation(axis, PATH_ANGLE) @ normal
        second_point = center + SPHERE_RADIUS * second_normal
        second_theta = np.arccos(second_normal[2])
        second_phi = np.arctan2(second_normal[1], second_normal[0])
        first2 = theta_direction(second_theta, second_phi)
        second2 = phi_direction(second_phi)
        actual_directions = (
            np.cos(FRAME_ANGLE) * first2 + np.sin(FRAME_ANGLE) * second2,
            -np.sin(FRAME_ANGLE) * first2 + np.cos(FRAME_ANGLE) * second2,
        )
        landed_directions = tuple(
            axis_rotation(axis, PATH_ANGLE) @ direction for direction in directions
        )

        plane = tangent_square(point, normal, directions[0], directions[1])
        plane2 = tangent_square(
            second_point, second_normal, actual_directions[0], actual_directions[1]
        )
        second_dot = m.Dot3D(
            second_point + 0.015 * second_normal, radius=0.055, color=m.WHITE
        )
        actual_frame = m.VGroup(
            *[
                m.Arrow3D(
                    second_point,
                    second_point + FRAME_LENGTH * direction,
                    thickness=0.016,
                    height=0.22,
                    base_radius=0.055,
                    color=m.TEAL,
                )
                for direction in actual_directions
            ]
        )
        differences = m.VGroup(
            *[
                m.Arrow3D(
                    second_point + FRAME_LENGTH * actual,
                    second_point + FRAME_LENGTH * landed,
                    thickness=0.012,
                    height=0.12,
                    base_radius=0.04,
                    color=m.YELLOW,
                )
                for landed, actual in zip(landed_directions, actual_directions)
            ]
        )
        p2_label = self.globe_label(r"$p_2$", second_point, (0.02, 0.3))
        x_label = self.globe_label(r"$X$", point + 0.2 * heading, (0.0, 0.26), m.RED)
        gamma_label = self.globe_label(
            r"$gamma$", path_points[len(path_points) // 2], (0.0, -0.24), m.RED
        )

        #   Transport is the rotation about the sphere's centre that carries p to p2:
        #   the arrows turn rigidly along the arc.
        def spin(start_points, end_points, alpha):
            return orbit(start_points, center, axis, alpha * PATH_ANGLE)

        landed_targets = [
            arrow.copy().rotate(PATH_ANGLE, axis=axis, about_point=center)
            for arrow in general_frame
        ]

        self.camera.add_fixed_in_frame_mobjects(
            frame, connection, torsion, curvature, goal
        )
        self.camera.add_fixed_in_frame_mobjects(
            p_label, mu_label, ea_label, p2_label, x_label, gamma_label
        )

        self.play(m.Write(frame))
        self.nslide()
        self.play(m.Create(sphere))
        self.play(
            m.Create(dot),
            m.Write(p_label),
            m.Create(coordinate_frame),
            m.Write(mu_label),
        )
        self.nslide()
        self.play(m.Create(general_frame), m.Write(ea_label))
        self.nslide()
        self.play(m.Write(connection))
        self.nslide()
        self.play(m.Uncreate(coordinate_frame), m.Unwrite(mu_label))
        self.play(m.Create(plane), m.Create(x_arrow), m.Write(x_label))
        self.nslide()
        self.play(m.Create(curve), m.Write(gamma_label))
        self.play(m.Create(plane2), m.Create(second_dot), m.Write(p2_label))
        self.nslide()
        self.play(
            *[
                m.Transform(arrow, target, path_func=spin)
                for arrow, target in zip(general_frame, landed_targets)
            ],
            *[arrow.animate.set_color(m.TEAL_E) for arrow in general_frame],
            m.Unwrite(ea_label),
        )
        self.play(m.Create(actual_frame))
        self.nslide()
        self.play(m.Create(differences))
        self.nslide()
        #   The globe has done its work: it goes, and a flat axes cross takes its
        #   place for the torsion and the curvature.
        self.play(
            m.Uncreate(sphere),
            m.Uncreate(dot),
            m.Uncreate(general_frame),
            m.Uncreate(actual_frame),
            m.Uncreate(differences),
            m.Uncreate(plane),
            m.Uncreate(plane2),
            m.Uncreate(second_dot),
            m.Uncreate(curve),
            m.Uncreate(x_arrow),
            m.Unwrite(p_label),
            m.Unwrite(p2_label),
            m.Unwrite(x_label),
            m.Unwrite(gamma_label),
        )
        #   Nothing is three-dimensional any more: look straight at the picture.
        self.set_camera_orientation(
            phi=0, theta=-90 * m.DEGREES, zoom=1, frame_center=m.ORIGIN
        )
        origin = PICTURE_ORIGIN
        vector_x, vector_y, vector_z = PICTURE_X, PICTURE_Y, PICTURE_Z
        x_name = picture_label(r"$X$", origin + vector_x + np.array([-0.34, 0.26, 0.0]))
        y_name = picture_label(r"$Y$", origin + vector_y + np.array([0.18, -0.26, 0.0]))
        x_shaft = picture_arrow(origin, origin + vector_x, FRONTCOL)
        y_shaft = picture_arrow(origin, origin + vector_y, FRONTCOL)
        self.play(m.LaggedStart(m.Write(torsion), m.Create(x_shaft), m.Write(x_name), m.Create(y_shaft), m.Write(y_name)))#,m.Create(axes))
        self.nslide()
        #   The parallelogram: Y carried along X, and X carried along Y. The
        #   connection turns each copy a little, so the two corners miss each other.
        carried_y = y_shaft.copy().set_color(m.GREY_A)
        carried_x = x_shaft.copy().set_color(m.GREY_A)
        self.add(carried_y, carried_x)
        self.play(
            carried_y.animate.put_start_and_end_on(start=origin+vector_x, end=origin+vector_x+vector_y+TORSION_DIFF/2),
            carried_x.animate.put_start_and_end_on(start=origin+vector_y, end=origin+vector_y+vector_x-TORSION_DIFF/2),
        )
        torsion_gap = picture_arrow(carried_x.get_end(), carried_y.get_end(), m.YELLOW, ratio=30, tip_ratio=0.3)
        torsion_name = picture_label(
            r"$T$", (carried_x.get_end() + carried_y.get_end()) / 2 + np.array([0.2, 0.2, 0.0]), color=m.YELLOW
        )
        self.play(m.Create(torsion_gap), m.Write(torsion_name))
        self.nslide()
        #   The curvature picture takes the axes over: the same X and Y, with a
        #   third vector carried to their far corner along both ways round.
        self.play(
            m.Write(curvature),
            m.Uncreate(carried_y),
            m.Uncreate(carried_x),
            m.Uncreate(torsion_gap),
            m.Unwrite(torsion_name),
        )
        corner = origin + vector_x + vector_y
        parallelogram = m.VGroup(
            m.Line(origin + vector_x, corner, color=FRONTCOL, stroke_width=2.5),
            m.Line(origin + vector_y, corner, color=FRONTCOL, stroke_width=2.5),
        )
        z_shaft = picture_arrow(origin, origin + vector_z, m.TEAL)
        z_name = picture_label(
            r"$Z$", origin + vector_z + np.array([0.26, 0.16, 0.0]), m.TEAL
        )
        self.play(m.Create(parallelogram), m.Create(z_shaft), m.Write(z_name))
        self.nslide()
        along_x = z_shaft.copy().set_color(m.TEAL_E)
        along_y = z_shaft.copy().set_color(m.TEAL_E)
        self.add(along_x, along_y)
        self.play(
            along_x.animate.put_start_and_end_on(start=origin+vector_x, end=origin+vector_x+vector_z-CURVATURE_DIFF/4),
            along_y.animate.put_start_and_end_on(start=origin+vector_y, end=origin+vector_y+vector_z+CURVATURE_DIFF/4)
        )
        self.play(
            along_x.animate.put_start_and_end_on(start=origin+vector_x+vector_y, end=origin+vector_x+vector_y+vector_z-CURVATURE_DIFF/2),
            along_y.animate.put_start_and_end_on(start=origin+vector_y+vector_x, end=origin+vector_y+vector_x+vector_z+CURVATURE_DIFF/2)
        )
        first_end = along_x.get_end()
        second_end = along_y.get_end()
        curvature_gap = picture_arrow(
            first_end, second_end, m.YELLOW, ratio=30, tip_ratio=0.3
        )
        curvature_name = picture_label(
            r"$R$", (first_end + second_end) / 2 + np.array([0, 0.24, 0.0]), color=m.YELLOW
        )
        self.play(m.Create(curvature_gap), m.Write(curvature_name))
        self.nslide()
        self.play(m.Write(goal))
        self.nslide()


class CartanFirstSection(_SectionBase):
    PAGE = 12
    TITLE = r"First structure equation: torsion"

    def play_cartan_first(self):
        self.nslide()
        reference = dim(typeset(r"T^a (X,Y) = e^a (T (X,Y))", NOTE_FONT_SIZE))
        steps, step_lines = formula_block(
            r"nabla_X Y &= nabla_X (e^b (Y)) e_b + e^b (Y) nabla_X e_b \ "
            r"e^a (nabla_X Y) &= nabla_X (e^a (Y)) "
            r"+ {{omega^a_b (X) e^b (Y) : conn}}",
            2,
        )
        steps.select("conn").set_color(W_COLOR)
        split, split_lines = formula_block(
            r"T^a (X,Y) &= {{nabla_X (e^a (Y)) - nabla_Y (e^a (X)) "
            r"- e^a ([X,Y]) : dpart}} \ "
            r"&+ {{omega^a_b (X) e^b (Y) "
            r"- omega^a_b (Y) e^b (X) : wpart}} \ "
            r"&= {{d e^a (X,Y) : dfin}} "
            r"+ {{(omega^a_b and e^b)(X,Y) : wfin}}",
            3,
        )
        split.select("dpart").set_color(D_COLOR)
        split.select("wpart").set_color(W_COLOR)
        split.select("dfin").set_color(D_COLOR)
        split.select("wfin").set_color(W_COLOR)
        footnotes = dim(
            typeset(
                r"d omega (X,Y) &= nabla_X (omega (Y)) - nabla_Y (omega (X)) "
                r"- omega ([X,Y]) \ "
                r"(omega and e)(X,Y) &= omega (X) e (Y) - omega (Y) e (X)",
                NOTE_FONT_SIZE,
            )
        )
        result = typeset(
            r"T^a = {{d e^a : d}} + {{omega^a_b and e^b : w}}",
            RESULT_FONT_SIZE,
        )
        result.select("d").set_color(D_COLOR)
        result.select("w").set_color(W_COLOR)

        reference.next_to(
            self.slide_title, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT
        )
        steps.next_to(reference, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        split.next_to(steps, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        footnotes.next_to(split, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        result.next_to(footnotes, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        box = m.SurroundingRectangle(
            result, color=FRONTCOL, stroke_width=1.5, buff=0.16
        )

        self.camera.add_fixed_in_frame_mobjects(
            reference, steps, split, footnotes, result, box
        )
        self.play(m.FadeIn(reference), m.Write(step_lines[0]))
        self.nslide()
        self.play(m.Write(step_lines[1]))
        self.play(m.Indicate(steps.select("conn"), color=W_COLOR, scale_factor=1.1))
        self.nslide()
        self.play(m.Write(split_lines[0]), m.Write(split_lines[1]))
        self.nslide()
        self.play(m.Write(split_lines[2]), m.FadeIn(footnotes))
        self.nslide()
        self.play(
            m.LaggedStart(
                m.Circumscribe(split.select("dfin"), color=D_COLOR),
                m.Circumscribe(split.select("wfin"), color=W_COLOR),
                lag_ratio=0.4,
            )
        )
        self.nslide()
        self.play(m.Write(result))
        self.play(m.Create(box))


class CartanSecondSection(_SectionBase):
    PAGE = 13
    TITLE = r"Second structure equation: curvature"

    def play_cartan_second(self):
        self.nslide()
        reference = dim(typeset(r"R (X,Y) e_b = R^a_b (X,Y) e_a", NOTE_FONT_SIZE))
        expansions, expansion_lines = formula_block(
            r"nabla_X nabla_Y e_b &= (nabla_X (omega^a_b (Y)) "
            r"+ omega^a_c (X) omega^c_b (Y)) e_a \ "
            r"nabla_Y nabla_X e_b &= (nabla_Y (omega^a_b (X)) "
            r"+ omega^a_c (Y) omega^c_b (X)) e_a \ "
            r"nabla_([X,Y]) e_b &= omega^a_b ([X,Y]) e_a",
            3,
        )
        split, split_lines = formula_block(
            r"R^a_b (X,Y) &= {{nabla_X (omega^a_b (Y)) "
            r"- nabla_Y (omega^a_b (X)) "
            r"- omega^a_b ([X,Y]) : dpart}} \ "
            r"&+ {{omega^a_c (X) omega^c_b (Y) "
            r"- omega^a_c (Y) omega^c_b (X) : wpart}} \ "
            r"&= {{d omega^a_b (X,Y) : dfin}} "
            r"+ {{(omega^a_c and omega^c_b)(X,Y) : wfin}}",
            3,
        )
        split.select("dpart").set_color(D_COLOR)
        split.select("wpart").set_color(W_COLOR)
        split.select("dfin").set_color(D_COLOR)
        split.select("wfin").set_color(W_COLOR)
        footnote = dim(
            typeset(
                r"d omega (X,Y) = nabla_X (omega (Y)) - nabla_Y (omega (X)) "
                r"- omega ([X,Y])",
                NOTE_FONT_SIZE,
            )
        )
        result = typeset(
            r"R^a_b = {{d omega^a_b : d}} "
            r"+ {{omega^a_c and omega^c_b : w}}",
            RESULT_FONT_SIZE,
        )
        result.select("d").set_color(D_COLOR)
        result.select("w").set_color(W_COLOR)

        reference.next_to(
            self.slide_title, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT
        )
        expansions.next_to(
            reference, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT
        )
        split.next_to(expansions, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        footnote.next_to(split, m.DOWN, buff=m.MED_SMALL_BUFF, aligned_edge=m.LEFT)
        result.next_to(footnote, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        box = m.SurroundingRectangle(
            result, color=FRONTCOL, stroke_width=1.5, buff=0.16
        )

        self.camera.add_fixed_in_frame_mobjects(
            reference, expansions, split, footnote, result, box
        )
        self.play(m.FadeIn(reference), m.Write(expansion_lines[0]))
        self.nslide()
        self.play(m.Write(expansion_lines[1]), m.Write(expansion_lines[2]))
        self.nslide()
        self.play(m.Write(split_lines[0]), m.Write(split_lines[1]))
        self.nslide()
        self.play(m.Write(split_lines[2]), m.FadeIn(footnote))
        self.nslide()
        self.play(
            m.LaggedStart(
                m.Circumscribe(split.select("dfin"), color=D_COLOR),
                m.Circumscribe(split.select("wfin"), color=W_COLOR),
                lag_ratio=0.4,
            )
        )
        self.nslide()
        self.play(m.Write(result))
        self.play(m.Create(box))


class CartanMatrixSection(_SectionBase):
    PAGE = 14
    TITLE = r"Cartan's equations in matrix form"

    def play_cartan_matrix(self):
        self.nslide()
        recap = dim(
            typeset(
                r"T^a = d e^a + omega^a_b and e^b quad quad "
                r"R^a_b = d omega^a_b "
                r"+ omega^a_c and omega^c_b",
                RECAP_FONT_SIZE,
            )
        )
        heading = typeset_text(r"In matrix notation:")
        torsion = typeset(r"T = {{d e : d}} + {{omega and e : w}}", MATRIX_FONT_SIZE)
        torsion.select("d").set_color(D_COLOR)
        torsion.select("w").set_color(W_COLOR)
        curvature = typeset(
            r"R = {{d omega : d}} + {{omega and omega : w}}", MATRIX_FONT_SIZE
        )
        curvature.select("d").set_color(D_COLOR)
        curvature.select("w").set_color(W_COLOR)
        note = dim(
            typeset_text(
                r"$omega = (omega^a_b)$, $e = (e^a)$; "
                r"the wedge includes the matrix product",
                NOTE_FONT_SIZE,
            )
        )
        outlook = dim(
            typeset_text(r"Next: torsion and curvature as defects", NOTE_FONT_SIZE)
        )

        recap.next_to(
            self.slide_title, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT
        )
        heading.next_to(recap, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        torsion.next_to(heading, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        curvature.next_to(torsion, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        note.next_to(curvature, m.DOWN, buff=m.LARGE_BUFF, aligned_edge=m.LEFT)
        outlook.next_to(note, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT)
        torsion_box = m.SurroundingRectangle(
            torsion, color=FRONTCOL, stroke_width=1.5, buff=0.18
        )
        curvature_box = m.SurroundingRectangle(
            curvature, color=FRONTCOL, stroke_width=1.5, buff=0.18
        )

        self.camera.add_fixed_in_frame_mobjects(
            recap,
            heading,
            torsion,
            curvature,
            note,
            outlook,
            torsion_box,
            curvature_box,
        )
        self.play(m.FadeIn(recap), m.Write(heading))
        self.nslide()
        self.play(m.Write(torsion), m.Write(curvature))
        self.play(m.Create(torsion_box), m.Create(curvature_box))
        self.nslide()
        self.play(m.FadeIn(note), m.FadeIn(outlook))


class CartanSetupPreview(CartanSetupSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(CartanSetupSection)
        self.play_cartan_setup()


class CartanFirstPreview(CartanFirstSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(CartanFirstSection)
        self.play_cartan_first()


class CartanSecondPreview(CartanSecondSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(CartanSecondSection)
        self.play_cartan_second()


class CartanMatrixPreview(CartanMatrixSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(CartanMatrixSection)
        self.play_cartan_matrix()
