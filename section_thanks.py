"""Closing slide: the thank-you on the bare background.

This slide carries no overlays at all, so it never uses `start_section` (which
would advance the page number and swap the title) or `prepare_section` (which
would create the overlays). `play_thanks` fades the whole deck out instead and
writes the message on the empty background.
"""

from typing import TYPE_CHECKING

import manimgx as m

from deck import TITLE_FONT_SIZE, DeckScene, typst_preamble

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object

THANKS_TEXT = "Thank you for your attention."


class ThanksSection(_SectionBase):
    #   The closing slide has no overlays and does not advance the deck, so PAGE and
    #   TITLE only keep it in line with the other sections.
    PAGE = 17
    TITLE = r""

    def play_thanks(self):
        self.nslide()
        #   The previous section may have been three-dimensional; look flat again.
        self.set_camera_orientation(phi=0, theta=-90 * m.DEGREES)

        #   Clear the slide: its content, then the whole HUD, then the backdrop.
        content = self.get_non_canvas_mobjs()
        for mobj in content:
            mobj.clear_updaters()
        overlays = [*self.hud_objs]
        if self.back_rects is not None:
            overlays.append(self.back_rects)
        if content or overlays:
            self.play(m.FadeOut(*content, *overlays))

        if self.back_rects is not None:
            self.camera.remove_fixed_in_frame_mobjects(self.back_rects)
        self.camera.remove_fixed_in_frame_mobjects(*self.hud_objs)
        self.hud_objs = []
        self.canvas_objs = []
        self.back_rects = None

        #   Only the background is left.
        thanks = m.Typst(
            THANKS_TEXT,
            font_size=TITLE_FONT_SIZE,
            typst_preamble=typst_preamble(TITLE_FONT_SIZE),
        ).move_to(m.ORIGIN)
        self.play(m.Write(thanks))
        
        back_img = m.SVGMobject("assets/title_math_background.svg",height=m.config.frame_height)
        self.play(m.Write(back_img, run_time=6))
        self.nslide()


class ThanksPreview(ThanksSection, DeckScene):
    def construct(self) -> None:
        #   There are no overlays on this slide, so nothing needs preparing.
        self.begin_deck()
        self.play_thanks()
