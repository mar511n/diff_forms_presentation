"""Table of contents slide."""

from typing import TYPE_CHECKING

import manimgx as m

from deck import (
    DeckScene,
    PresentationContents,
    PresentationTitleShort,
)

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class ContentsSection(_SectionBase):
    PAGE = 1
    TITLE = PresentationTitleShort

    def play_contents(self):
        self.nslide()
        contents = self.get_lines(self.slide_title, PresentationContents)
        self.camera.add_fixed_in_frame_mobjects(*contents)
        for point in contents:
            self.play(m.Write(point))
            self.nslide()


class ContentsPreview(ContentsSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(ContentsSection)
        self.play_contents()
