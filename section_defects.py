"""Dislocation & Burgers vector as torsion.

The right-hand picture starts from a perfect square lattice, applies a simple
edge-dislocation displacement field and reads the geometry back off the result:
the local frame, the Burgers circuit and, finally, the torsion concentrated at
the defect. The left-hand column carries the matching formulas.
"""

from typing import TYPE_CHECKING

import manimgx as m
import matplotlib.pyplot as plt
import numpy as np

from deck import CONTENT_FONT_SIZE, FRONTCOL, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


MATH_FONT_SIZE = CONTENT_FONT_SIZE
NOTE_FONT_SIZE = 0.62 * CONTENT_FONT_SIZE
LABEL_FONT_SIZE = 0.75 * CONTENT_FONT_SIZE

#   The lattice. Columns and rows sit at half-integer spacings, so the defect
#   sits in the middle of a cell and no lattice line runs exactly through it.
SPACING = 0.62
LATTICE_ORIGIN = np.array([3.05, 0.05, 0.0])
COLUMNS = [(index + 0.5) * SPACING for index in range(-5, 5)]
ROWS = [(index + 0.5) * SPACING for index in range(-4, 4)]
LINE_SAMPLES = 361

#   The displacement field: the extra half-plane is the negative y-axis. Points
#   left of it move left, points right of it move right, and the rows above it
#   relax toward the core. The field is smooth, so the lattice stays connected.
BURGERS = SPACING
OUTWARD = 0.55 * BURGERS
OUTWARD_WIDTH = 3*OUTWARD
UPWARD_FADE = 0.6 * SPACING
VERTICAL_PULL = 0.35 * BURGERS
VERTICAL_WIDTH = 1.0 * SPACING
VERTICAL_DECAY = 1.2 * SPACING

#   The Burgers circuit follows lattice lines around the defect.
CIRCUIT_HALF = 2.5 * SPACING
FRAME_LENGTH = 0.18
FRAME_COLUMNS = [column for column in COLUMNS if abs(column) <= 3.5 * SPACING]
FRAME_ROWS = [row for row in ROWS if abs(row) <= 2.5 * SPACING]
NEW_LINE_ROWS = [
    row for row in ROWS if row < 0 and abs(row) <= 2.5 * SPACING
]

#   The torsion colorplot: a compact blob at the core.
TORSION_REGION = 1.75
TORSION_SIGMA = 0.42
TORSION_RESOLUTION = 256

LATTICE_COLOR = FRONTCOL
LATTICE_STROKE = 1.9
CIRCUIT_COLOR = m.ORANGE
BURGERS_COLOR = m.RED
SURFACE_COLOR = m.TEAL
FRAME_X_COLOR = m.GOLD_A
FRAME_Y_COLOR = m.GOLD_E

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


def typesettex(*parts, font_size=MATH_FONT_SIZE):
    """A formula, at this section's sizes."""
    return m.MathTex(
        *parts, font_size=font_size, typst_preamble=typst_preamble(font_size)
    )


def dim(mobject, opacity=0.6):
    """Dim a typeset aside: a definition recalled, a footnote."""
    return mobject.set_opacity(opacity)


def displacement(point):
    """The displacement u^a of a reference point.

    The defect line is the negative y-axis. The displacement opens the lattice
    outwards on both sides of it and relaxes the rows above the core downward.
    """
    x, y = point[0], point[1]
    fade = 1.0 / (1.0 + np.exp(y / UPWARD_FADE))
    u_x = OUTWARD * np.exp(- x**2 / (2*OUTWARD_WIDTH**2)) * np.sign(x) * fade
    pull = np.tanh(max(y, 0.0) / UPWARD_FADE)
    dent = np.exp(-(x / VERTICAL_WIDTH) ** 2) * np.exp(
        -(y / VERTICAL_DECAY) ** 2
    )
    u_y = -VERTICAL_PULL * dent * pull
    return np.array([u_x, u_y, 0.0])


def deformed(point):
    """Where a reference point is drawn after the displacement."""
    point = np.asarray(point, dtype=float)
    return LATTICE_ORIGIN + point + displacement(point)


def reference_runs():
    """The lattice lines in reference coordinates."""
    runs = []
    xs = np.linspace(COLUMNS[0], COLUMNS[-1], LINE_SAMPLES)
    for y in ROWS:
        runs.append(np.array([[x, y, 0.0] for x in xs]))
    ys = np.linspace(ROWS[0], ROWS[-1], LINE_SAMPLES)
    for x in COLUMNS:
        runs.append(np.array([[x, y, 0.0] for y in ys]))
    return runs


def polyline(points, color=LATTICE_COLOR, stroke_width=LATTICE_STROKE):
    """A polyline through sampled points."""
    line = m.TipableVMobject(color=color, stroke_width=stroke_width)
    line.set_points_as_corners(np.asarray(points, dtype=float))
    return line


def lattice_pair():
    """The perfect and the dislocated lattice, as matching groups of lines."""
    perfect = m.VGroup()
    dislocated = m.VGroup()
    for points in reference_runs():
        perfect.add(polyline(points + LATTICE_ORIGIN))
        dislocated.add(polyline(np.array([deformed(point) for point in points])))
    return perfect, dislocated


def circuit_sides():
    """The Burgers circuit, sampled along the deformed lattice lines."""
    half = CIRCUIT_HALF
    corners = [
        np.array([-half, -half, 0.0]),
        np.array([half, -half, 0.0]),
        np.array([half, half, 0.0]),
        np.array([-half, half, 0.0]),
        np.array([-half, -half, 0.0]),
    ]
    sides = []
    for index in range(len(corners) - 1):
        start, end = corners[index], corners[index + 1]
        points = np.array(
            [
                (1 - t) * start + t * end
                for t in np.linspace(0.0, 1.0, 81)
            ]
        )
        sides.append(np.array([deformed(point) for point in points]))
    return sides


def add_frame(frames, point):
    """Two short arrows along the deformed coordinate directions at a site."""
    base = deformed(point)
    step = 1e-3
    along_x = deformed(point + np.array([step, 0.0, 0.0])) - deformed(
        point - np.array([step, 0.0, 0.0])
    )
    along_y = deformed(point + np.array([0.0, step, 0.0])) - deformed(
        point - np.array([0.0, step, 0.0])
    )
    along_x /= np.linalg.norm(along_x)
    along_y /= np.linalg.norm(along_y)
    for direction, color in (
        (along_x, FRAME_X_COLOR),
        (along_y, FRAME_Y_COLOR),
    ):
        frames.add(
            m.Arrow(
                base,
                base + FRAME_LENGTH * direction,
                buff=0,
                color=color,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.45,
                max_stroke_width_to_length_ratio=12,
            )
        )


def frame_field():
    """A local frame at the lattice sites, from the deformed grid directions."""
    frames = m.VGroup()
    for x in FRAME_COLUMNS:
        for y in FRAME_ROWS:
            add_frame(frames, np.array([x, y, 0.0]))
    for y in NEW_LINE_ROWS:
        add_frame(frames, np.array([0.0, y, 0.0]))
    return frames


def torsion_image():
    """The torsion as a colorplot: a bright core with a faint halo."""
    coordinates = np.linspace(-TORSION_REGION, TORSION_REGION, TORSION_RESOLUTION)
    x, y = np.meshgrid(coordinates, coordinates)
    radius2 = x * x + y * y
    density = np.exp(-radius2 / (2 * TORSION_SIGMA**2))
    density += 0.16 * np.exp(-radius2 / (2 * (2.0 * TORSION_SIGMA) ** 2))
    density /= density.max()
    #   Fade the picture out to nothing at its rim, so the square does not show.
    window = np.clip(1.0 - (np.sqrt(radius2) / TORSION_REGION) ** 6, 0.0, 1.0)
    pixels = np.zeros((TORSION_RESOLUTION, TORSION_RESOLUTION, 4), dtype=np.uint8)
    pixels[..., :3] = density_rgb(density)
    pixels[..., 3] = np.round(
        255 * np.clip(density**0.7, 0.0, 1.0) * window
    ).reshape(TORSION_RESOLUTION, TORSION_RESOLUTION)
    image = m.ImageMobject(pixels, scale_to_resolution=0)
    image.scale_to_fit_height(2 * TORSION_REGION)
    image.move_to(LATTICE_ORIGIN)
    return image


class DefectsSection(_SectionBase):
    PAGE = 14
    TITLE = r"Dislocations as torsion"

    def play_defects(self):
        self.set_camera_orientation(phi=0, theta=-90 * m.DEGREES)
        self.nslide()

        #   The perfect lattice and the reference coordinate.
        x_label = typesettex(r"x", "^a")
        x_label.next_to(
            self.slide_title, m.DOWN, buff=m.MED_LARGE_BUFF, aligned_edge=m.LEFT
        )
        perfect, dislocated = lattice_pair()
        self.play(m.Create(perfect), m.Write(x_label))
        self.nslide()

        #   Apply the displacement field; in parallel the coordinate transforms.
        coordinates = typesettex(
            r"y", "^a", "=", r"x", "^a", "+", r"u", "^a", "(", "x", ")"
        )
        coordinates.move_to(x_label, aligned_edge=m.LEFT)
        coordinates[6:8].set_color(m.YELLOW)
        self.play(
            *[
                m.Transform(before, after)
                for before, after in zip(perfect, dislocated)
            ],
            m.TransformMatchingTex(x_label, coordinates),
        )

        #   The extra half-plane is a new line of sites below the core. It ends
        #   at the core, the only free end of the lattice; its bottom end joins
        #   the lowest row.
        core = deformed(np.array([0.0, 0.0, 0.0]))
        new_line = m.Line(
            core,
            deformed(np.array([0.0, ROWS[0], 0.0])),
            color=LATTICE_COLOR,
            stroke_width=LATTICE_STROKE,
        )
        self.play(m.Create(new_line))
        self.nslide()

        #   The frame field lives on the deformed lattice, including the new line.
        frames = frame_field()
        self.play(
            m.LaggedStart(*[m.Create(frame) for frame in frames], lag_ratio=0.01)
        )

        #   The coframe 1-form.
        coframe = typesettex(
            r"e",
            "^a",
            "=",
            "d",
            r"y",
            "^a",
            "=",
            r"e",
            "^a",
            r"{}_\mu",
            r"d x",
            r"^\mu",
        )
        coframe[0:2].set_color(m.GOLD)
        coframe[7:10].set_color(m.GOLD)
        coframe.next_to(
            coordinates, m.DOWN, aligned_edge=m.LEFT
        )
        self.play(m.Write(coframe),m.FadeOut(perfect), m.FadeOut(new_line))
        self.nslide()

        #   The Burgers circuit and its vector. The vector lies along the bottom
        #   side, pointing from the defect line toward the right.
        sides = circuit_sides()
        circuit = m.VGroup()
        tips = m.VGroup()
        circuit_points = []
        for points in sides:
            side_line = polyline(points, color=CIRCUIT_COLOR, stroke_width=3.2)
            circuit.add(side_line)
            circuit_points.extend(points)
            #   The tip is its own short arrow, not a submobject of the line: fading
            #   it leaves the contour itself in place.
            direction = points[-1] - points[-4]
            direction /= np.linalg.norm(direction)
            tips.add(
                m.Arrow(
                    points[-1] - 0.20 * direction,
                    points[-1],
                    buff=0,
                    color=CIRCUIT_COLOR,
                    stroke_width=3.2,
                    max_tip_length_to_length_ratio=0.8,
                    max_stroke_width_to_length_ratio=20,
                )
            )
        b_start = deformed(np.array([0.0, -CIRCUIT_HALF, 0.0]))
        b_end = b_start + np.array([BURGERS, 0.0, 0.0])
        burgers_arrow = m.Arrow(
            b_start,
            b_end,
            buff=0,
            color=BURGERS_COLOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.4,
            max_stroke_width_to_length_ratio=14,
        )
        burgers_label = typesettex(r"b", "^a", font_size=LABEL_FONT_SIZE)
        burgers_label[0:2].set_color(BURGERS_COLOR)
        burgers_label.next_to(burgers_arrow, m.DOWN, buff=0.12)

        burgers_line = typesettex(r"b", "^a", "=", r"\oint_C", r"e", "^a")
        burgers_line[0:2].set_color(BURGERS_COLOR)
        burgers_line[4:6].set_color(m.GOLD)
        burgers_line.next_to(coframe, m.DOWN, aligned_edge=m.LEFT)
        self.play(
            m.LaggedStart(*[m.Create(line) for line in circuit], lag_ratio=0.08),
            m.FadeIn(tips),
            m.Create(burgers_arrow),
            m.Write(burgers_label),
            m.Write(burgers_line),
        )
        self.nslide()

        #   The surface integral inside the circuit.
        surface = m.Polygon(
            *circuit_points,
            fill_color=SURFACE_COLOR,
            fill_opacity=0.24,
            stroke_width=0,
        )
        surface_label = typesettex(r"S", font_size=LABEL_FONT_SIZE)
        surface_label.set_color(SURFACE_COLOR)
        surface_label.move_to(
            LATTICE_ORIGIN + 0.1*m.UP #+ 0.42 * CIRCUIT_HALF * m.DOWN + 0.42 * CIRCUIT_HALF * m.RIGHT
        )
        surface_line = typesettex(r"b", "^a", "=", r"\int_S", "d", r"e", "^a", "=", r"\int_S", "T", "^a")
        surface_line[0:2].set_color(BURGERS_COLOR)
        surface_line[4:7].set_color(m.RED)
        surface_line[-2:].set_color(m.BLUE)
        surface_line.next_to(burgers_line, m.DOWN, aligned_edge=m.LEFT)
        self.play(m.FadeIn(surface), m.Write(surface_label),m.Write(surface_line[:-4]))
        self.nslide()

        #   Poincaré/Stokes has localized the integral at the defect; with a
        #   vanishing connection the torsion is simply d e^a.
        torsion_line = typesettex(
            r"\omega",
            "=",
            "0",
            r"\quad\Longrightarrow\quad",
            r"T",
            "^a",
            "=",
            "d",
            r"e",
            "^a",
        )
        torsion_line[4:6].set_color(m.BLUE)
        torsion_line[7:10].set_color(m.RED)
        torsion_line.next_to(surface_line, m.DOWN, aligned_edge=m.LEFT)
        note = dim(
            typesettex(
                r"T^a = d e^a + \omega^a{}_b \wedge e^b",
                font_size=NOTE_FONT_SIZE,
            ),
            opacity=0.55,
        )
        note.next_to(self.contact_info, m.UP).to_edge(m.LEFT)
        self.play(m.Write(note))
        self.nslide()
        torsion_plot = torsion_image()
        torsion_label = typesettex(r"T", "^a", font_size=LABEL_FONT_SIZE)
        torsion_label.set_color(m.BLUE)
        torsion_label.move_to(
            LATTICE_ORIGIN
            + 1.15 * m.RIGHT
            + 1.15 * m.UP
        )
        self.play(
            m.Write(torsion_line),
            m.Write(surface_line[-4:]),
            m.FadeOut(frames),
            m.FadeOut(surface),
            m.FadeOut(surface_label),
            m.FadeOut(tips),
            m.FadeIn(torsion_plot),
            m.Write(torsion_label),
        )
        self.nslide()

        poincare = m.MathTex(r"&\text{Poincaré lemma: \\}", r"&T^a", "= 0", r"\text{ for smooth }", r"u^a", r"(x)")
        poincare[1].set_color(m.BLUE)
        poincare[-2].set_color(m.YELLOW)
        poincare.next_to(torsion_line, m.DOWN, aligned_edge=m.LEFT)
        self.play(m.Write(poincare))
        self.nslide()


class DefectsPreview(DefectsSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(DefectsSection)
        self.play_defects()
