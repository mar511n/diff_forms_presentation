"""Shared deck setup: theme, presentation metadata and scene plumbing.

Every section of the talk is a method on a `DeckScene`. The final `Presentation`
inherits all section mixins, so the canvas objects (slide title, logo, contact
info, presentation title and page number) are simply attributes of one scene and
persist between sections. A section file also defines a preview scene that
recreates the same state with `prepare_section` and runs only its own animations.
"""

import re

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

def split_typst_lines(mobj, count=2):
    """Split a typeset object into its `count` visual lines, top to bottom.

    The parts are grouped by vertical position: the widest `count - 1` gaps between
    neighbouring parts are the line boundaries. The groups hold the original parts, not
    copies, so a multi-line `&`-aligned equation keeps its alignment while the lines can
    be written one at a time. `count` must be the object's number of lines. Within each
    group the parts are sorted left to right.
    """
    parts = sorted(mobj.submobjects, key=lambda part: part.get_center()[1])
    ys = [part.get_center()[1] for part in parts]
    widest = sorted(range(len(ys) - 1), key=lambda i: ys[i + 1] - ys[i], reverse=True)
    boundaries = sorted((ys[i] + ys[i + 1]) / 2 for i in widest[: count - 1])
    groups = [m.VGroup() for _ in range(count)]
    for part, y in zip(parts, ys):
        groups[sum(y < boundary for boundary in boundaries)].add(part)
    for group in groups:
        group.sort()
    return groups


def typst_preamble(font_size=CONTENT_FONT_SIZE, leading="", display_math=False):
    """Typst page setup that wraps text at MAX_TEXT_WIDTH scene units."""
    width_pt = MAX_TEXT_WIDTH / (font_size * m.SCALE_FACTOR_PER_FONT_POINT)
    return (
        f"\n#set page(width: {width_pt:.3f}pt, height: auto, margin: 0pt, fill: none)"
        + ("\n#show math.equation.where(block: false): it => math.display(it)" if display_math else "")
        + (f"\n#set par(leading: {leading})" if leading != "" else "")
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
PresentationContents = """
- differential forms
- wedge product
- exterior derivative
- generalized Stokes theorem
- Poincaré lemma
- Cartan structure equations
- defect geometry
- (Maxwell/Einstein eq)
"""


def _ends_in_math(line, in_math):
    """Whether `line` leaves a `$...$` math block open, given whether it starts in one."""
    escaped = False
    for char in line:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "$":
            in_math = not in_math
    return in_math


# Typst markup that starts a block, and so a new line, by itself.
_BLOCK_START = re.compile(r"[-+/]\s|=+\s|\d+[.)]\s")


def _starts_block(line, in_math):
    """Whether `line` begins a Typst block: a list item, a term, a heading or an enum."""
    return not in_math and _BLOCK_START.match(line.lstrip()) is not None


def _ends_with_break(line):
    """Whether `line` ends with a Typst `\\` line break, an odd number of them."""
    stripped = line.rstrip()
    return (len(stripped) - len(stripped.rstrip("\\"))) % 2 == 1


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
        """Place a Typst object below `anchor` and return its groups.

        `points` is Typst code. The function creates one Typst object and returns its
        groups in order, e.g. to Write them one at a time with Write(lines[0]), ...
        Empty source lines are ignored.

        A source line break does one of three things:

        - it starts a new group on a new line; the `\\` Typst needs is inserted for you,
          also inside `$...$` math, where `&` alignment points stay aligned,
        - it keeps the next line in the same group but breaks the line visibly, when the
          line ends with `\\`,
        - it keeps the next line in the same group without a visible break, when that
          line is indented deeper than the line that started the group; Typst then wraps
          or joins the text.

        A line that starts a Typst block (`- `, `+ `, `/ `, `= `, `1. `) always starts a
        new group, because Typst starts those on a new line by itself.

        A zero-size transparent marker is inserted at every group boundary. The markers
        are parts of the Typst object at known byte offsets in the code, so its parts can
        be split there without measuring positions. Every line should be complete Typst
        markup, except that one `$...$` math block may span several lines.
        """
        # Every non-empty line, with its indent and whether it starts inside math.
        lines = []
        in_math = False
        for line in points.split("\n"):
            stripped = line.lstrip()
            if stripped:
                lines.append((line, len(line) - len(stripped), in_math, stripped))
            in_math = _ends_in_math(line, in_math)
        if not lines:
            return []

        # A line continues the current group if the group's last line ends with `\` or
        # the line is indented deeper than the line that started the group. A block
        # starts a new group, whatever its indent.
        groups: list[tuple[int, bool, list[str]]] = []
        for line, indent, starts_in_math, stripped in lines:
            if groups and not _starts_block(stripped, starts_in_math):
                first_indent, _, members = groups[-1]
                if _ends_with_break(members[-1]) or indent > first_indent:
                    members.append(line)
                    continue
            groups.append((indent, starts_in_math, [line]))

        # The marker: a clipped, zero-size box holding one tiny transparent glyph. Its
        # glyph starts at a known byte offset in the marked code that we record.
        marker_open = (
            '#box(width: 0pt, height: 0pt, clip: true)'
            '[#text(fill: rgb("#00000000"), size: 0.1pt)['
        )
        marker = marker_open + "|" + "]]"

        marked = []
        markers = set()  # byte offset of every marker glyph in the marked code
        offset = 0  # bytes written so far

        def emit(piece):
            nonlocal offset
            marked.append(piece)
            offset += len(piece.encode())

        def emit_marker():
            markers.add(offset + len(marker_open.encode()))
            emit(marker)

        for index, (_, _, members) in enumerate(groups):
            following = groups[index + 1] if index + 1 < len(groups) else None
            for position, line in enumerate(members):
                last = position == len(members) - 1
                if not last:
                    emit(line + "\n")  # same group: Typst joins or wraps it
                elif following is None:
                    emit(line)
                elif _starts_block(following[2][0], following[1]):
                    # Typst starts the next block on a new line by itself, so the marker
                    # ends this line, before a line break the line already ends with.
                    if _ends_with_break(line):
                        cut = line.rstrip().rfind("\\")
                        emit(line[:cut])
                        emit_marker()
                        emit(line[cut:] + "\n")
                    else:
                        emit(line)
                        emit_marker()
                        emit("\n")
                else:
                    emit(line if _ends_with_break(line) else line + " \\")
                    emit("\n")
                    emit_marker()

        text = m.Typst("".join(marked), font_size=font_size, typst_preamble=preamble)
        text.next_to(anchor, m.DOWN, buff=buff, aligned_edge=m.LEFT)
        breaks = {
            id(part)
            for part in text.submobjects
            if getattr(part, "node", None) in markers
        }
        if not breaks:  # no marker survived: return the object as one group
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
