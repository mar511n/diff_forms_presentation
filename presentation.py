"""The full talk: the sections composed in order.

Each section lives in its own `section_*.py`, which also defines a preview scene
for rendering just that section. See `deck.py` for the shared setup.
"""

from deck import DeckScene
from section_contents import ContentsSection
from section_exterior_derivative import ExteriorDerivativeSection
from section_forms import FormsSection
from section_title import TitleSection


class Presentation(
    TitleSection,
    ContentsSection,
    FormsSection,
    ExteriorDerivativeSection,
    DeckScene,
):
    def construct(self) -> None:
        self.play_title()
        self.play_contents()
        self.start_section(FormsSection)
        self.play_forms()
        self.start_section(ExteriorDerivativeSection)
