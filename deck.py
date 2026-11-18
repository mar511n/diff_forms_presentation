"""Shared deck setup: theme, presentation metadata and scene plumbing.

Every section of the talk is a method on a `DeckScene`. The final `Presentation`
inherits all section mixins, so the canvas objects (slide title, logo, contact
info, presentation title and page number) are simply attributes of one scene and
persist between sections. A section file also defines a preview scene that
recreates the same state with `prepare_section` and runs only its own animations.
"""

import manimgx as m

class Write(m.Write):
    def __init__(self, vmobject, reverse=False, **kwargs):
        kwargs.setdefault("run_time", 1.0)
        super().__init__(vmobject, reverse=reverse, **kwargs)
m.Write = Write

DARK_MODE: bool = True
LIGHT_MODE: bool = False  # experimental
Theme = DARK_MODE
OFFBLACK = m.ManimColor("#121317")
OFFWHITE = m.ManimColor("#F0F8FF")
BACKCOL = OFFBLACK if Theme else OFFWHITE
FRONTCOL = OFFWHITE if Theme else OFFBLACK
TITLE_FONT_SIZE = 52
CONTENT_FONT_SIZE = 0.75 * TITLE_FONT_SIZE
m.config.background_color = BACKCOL

# The largest width a Typst text may use, in scene units. Typst is typeset at
# SCALE_FACTOR_PER_FONT_POINT scene units per point and then scaled by its font size,
# so the page width in points depends on the font size.
MAX_TEXT_WIDTH = m.config.frame_width - 2 * m.DEFAULT_MOBJECT_TO_EDGE_BUFFER


def typst_preamble(font_size=CONTENT_FONT_SIZE, leading="1em", display_math=False):
    """Typst page setup that wraps text at MAX_TEXT_WIDTH scene units."""
    width_pt = MAX_TEXT_WIDTH / (font_size * m.SCALE_FACTOR_PER_FONT_POINT)
    return (
        f"\n#set page(width: {width_pt:.3f}pt, height: auto, margin: 0pt, fill: none)"
        + ("\n#show math.equation.where(block: false): it => math.display(it)" if display_math else "")
        + f"\n#set par(leading: {leading})"
    )


# Defaults for all typeset text (Text, Typst, ...)
m.Typst.set_default(font_size=CONTENT_FONT_SIZE, fill_color=FRONTCOL)
# Numbers manage their own font size and glyph colors
m.DecimalNumber.set_default(font_size=CONTENT_FONT_SIZE, fill_color=FRONTCOL)

PresentationTitle = r"*Cartan's Differential Calculus on Manifolds*"
PresentationTitleShort = "Cartan's Differential Calculus on Manifolds"
PresentationInfo = r"""Marvin Henke - 24.11.2026 \
Supervisor: Dr. Nikodem Szpak \
Group seminar AG König"""
PresentationContactInfo = r'marvin.henke\@stud.uni-due.de'
PresentationContents = """- Differential forms
- wedge product
- exterior derivative
- generalized Stokes theorem
- Poincaré lemma
- Cartan structure equations
- defect geometry
- (Maxwell/Einstein eq)
"""


class DeckScene(m.ThreeDScene):
    """The scene shared by the whole talk and by every section preview."""

    def begin_deck(self):
        """Start a deck: reset the persistent canvas state."""
        self.canvas_objs = []
        self.hud_objs = []
        self.back_rects = None

    def make_hud(self, page, title):
        """Create and pin the persistent overlays, without showing them yet.

        The overlays are the slide title, logo, contact info, presentation title
        and page number. They are pinned with the camera (not added to the scene),
        so a section can introduce them with its own animations; previews use
        `show_hud` to show them at once.
        """
        self.slide_title = m.Typst(
            f"*{title}*",
            font_size=TITLE_FONT_SIZE,
            typst_preamble=typst_preamble(TITLE_FONT_SIZE),
        )
        self.slide_title.to_corner(m.UL)

        self.ude_logo = m.SVGMobject(
            './assets/logo/logo_claim_rgb.svg'
            if Theme
            else './assets/logo/logo_claim_rgb_neg.svg',
            height=1,
        )
        self.ude_logo.to_corner(m.UR, buff=0)
        self.ude_logo.shift(m.DOWN * 0.1)

        self.contact_info = m.Typst(
            PresentationContactInfo,
            font_size=CONTENT_FONT_SIZE * 0.6,
            typst_preamble=typst_preamble(CONTENT_FONT_SIZE * 0.6),
        ).to_corner(m.DL, buff=m.MED_SMALL_BUFF)

        self.presentation_title = m.Typst(
            PresentationTitleShort,
            font_size=CONTENT_FONT_SIZE * 0.6,
            typst_preamble=typst_preamble(CONTENT_FONT_SIZE * 0.6),
        ).align_to(self.contact_info, m.UP)

        self.slide_number_val = page
        self.slide_number = m.Integer(
            page, font_size=CONTENT_FONT_SIZE * 0.6
        ).to_corner(m.DR, buff=m.MED_SMALL_BUFF)

        self.hud_objs = [
            self.slide_title,
            self.ude_logo,
            self.contact_info,
            self.presentation_title,
            self.slide_number,
        ]
        for obj in self.hud_objs:
            self.camera.add_fixed_in_frame_mobjects(obj)
            self.canvas_objs.append(obj)

    def show_hud(self):
        """Show the pinned overlays at once (previews)."""
        self.add(*self.hud_objs)

    def prepare_section(self, section):
        """Set the deck to the state a section starts in, without animations."""
        self.begin_deck()
        self.make_hud(section.PAGE, section.TITLE)
        self.show_hud()
        self.update_back_rects()

    def start_section(self, section):
        """Animate the transition into a section, then check its page number."""
        self.setup_new_slide(section.TITLE, cleanup=True)
        #   A section starts flat; a three-dimensional one sets its own view.
        self.set_camera_orientation(phi=0, theta=-90 * m.DEGREES)
        assert self.slide_number_val == section.PAGE, (
            f"{section.__name__}: deck is on page {self.slide_number_val}, "
            f"but the section declares PAGE = {section.PAGE}"
        )

    def update_back_rects(self):
        """Draw the backdrop rectangles behind the current canvas overlays."""
        if self.back_rects is not None:
            self.canvas_objs.remove(self.back_rects)
            self.remove(self.back_rects)
        rects = [
            m.SurroundingRectangle(
                obj,
                color=BACKCOL,
                fill_opacity=0.6,
                stroke_width=0,
                z_index=-1,
            )
            for obj in self.hud_objs
        ]
        for rect in rects:
            self.camera.add_fixed_in_frame_mobjects(rect)
        self.back_rects = m.VGroup(*rects)
        self.add(self.back_rects)
        self.canvas_objs.append(self.back_rects)

    def get_lines(self, anchor, points, buff=m.MED_LARGE_BUFF, font_size=CONTENT_FONT_SIZE, preamble=typst_preamble()):
        """Place a Typst object below `anchor` and return its lines.

        `points` is Typst code. Each non-empty newline-separated source line becomes
        one group: the function creates a single Typst object and returns an ordered
        list of references to its lines, which can e.g. be used to Write the lines one
        at a time with Write(lines[0]), ...

        A zero-size transparent marker is appended to every non-empty source line. The
        markers are parts of the Typst object in document order, so the object's parts
        can be split at them without measuring positions, and their labels let
        `select` find them. Lines are the source's newline-separated lines (even where
        Typst joins them into one visual line), and lines with no visible parts are
        omitted. Each non-empty line should be complete Typst markup: a construct that
        spans several source lines would receive a marker inside itself.
        """
        if not any(line.strip() for line in points.split("\n")):
            return []

        # A label that the points' own labels cannot collide with.
        marker_label = "_get_lines_break"
        while f"<{marker_label}>" in points:
            marker_label += "_"
        marker = (
            "#box(width: 0pt, height: 0pt, clip: true)"
            f'[#text(fill: rgb("#00000000"), size: 0.1pt)[|]] <{marker_label}>'
        )
        marked = "\n".join(
            line + marker if line.strip() else line for line in points.split("\n")
        )

        text = m.Typst(
            marked,
            font_size=font_size,
            typst_preamble=preamble,
        )
        text.next_to(anchor, m.DOWN, buff=buff, aligned_edge=m.LEFT)
        try:
            breaks = {id(part) for part in text.select(marker_label).submobjects}
        except KeyError:  # no marker survived: return the object as one line
            return [text]

        lines = []
        current = m.VGroup()
        for part in text.submobjects:
            if id(part) in breaks:
                if len(current) > 0:
                    lines.append(current)
                    current = m.VGroup()
            else:
                current.add(part)
        if len(current) > 0:
            lines.append(current)

        return lines

    def nslide(self, name="", notes="", loop=False, auto_next=False):
        sect = 'presentation.normal'
        if loop:
            sect = 'presentation.loop'
        if auto_next:
            sect = 'presentation.skip'
        self.next_section(
            name=name, notes=notes, section_type=sect, skip_animations=False
        )
        self.wait(2 / m.config.frame_rate)

    def get_non_canvas_mobjs(self):
        return [mobj for mobj in self.mobjects if mobj not in self.canvas_objs]

    def next_slide_number_animation(self):
        self.slide_number_val += 1
        return self.slide_number.animate(run_time=0.5).set_value(
            self.slide_number_val
        )

    def next_slide_title_animation(self, title):
        newT = m.Typst(
            f"*{title}*",
            font_size=TITLE_FONT_SIZE,
            typst_preamble=typst_preamble(TITLE_FONT_SIZE),
        ).move_to(self.slide_title, m.UP).align_to(self.slide_title, m.LEFT)
        self.camera.add_fixed_in_frame_mobjects(newT)
        return m.Transform(
            self.slide_title,
            newT,
            run_time=0.5,
        )

    def setup_new_slide(self, title, cleanup=False):
        print(f"{self.slide_number_val}:{title}")
        if cleanup:
            ncos = self.get_non_canvas_mobjs()
            anims = [self.next_slide_number_animation(), self.next_slide_title_animation(title)]
            if len(ncos) > 0:
                for mobj in ncos:
                    mobj.clear_updaters()
                anims.append(m.FadeOut(*ncos, shift=m.LEFT))
            self.play(*anims)
            for nco in ncos:
                del nco
        else:
            self.play(
                self.next_slide_number_animation(),
                self.next_slide_title_animation(title),
            )
        self.update_back_rects()
