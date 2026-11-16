from typing import TYPE_CHECKING

from deck import DeckScene

if TYPE_CHECKING:
    # Type-checkers see the deck API; at runtime the section is a plain mixin.
    _SectionBase = DeckScene
else:
    _SectionBase = object


class EmptySection(_SectionBase):
    PAGE = -1
    TITLE = r""


class EmptyPreview(EmptySection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(EmptySection)
