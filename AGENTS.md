# AGENTS.md

## What this repository is

Source for the group-seminar presentation **“Cartan's Differential Calculus on
Manifolds”** (Marvin Henke, supervisor Dr. Nikodem Szpak, AG König).
This is a presentation project, not the ManimGX library.

- `presentation.py` — the full talk: `Presentation` composes the sections in order.
- `deck.py` — shared setup: theme, presentation metadata, Typst defaults, and the
  `DeckScene` base class with the canvas/HUD and slide plumbing.
- `section_*.py` — one file per section. Each defines a section mixin (`play_*`
  methods, `PAGE`, `TITLE`) and a `*Preview` scene that renders just that section.
- `assets/` — title background and UDE logos. Do not edit, rename, or move these;
  paths in the scene are relative to the repository root.
- `output/` — generated artifacts only, ignored by git. Never edit these by hand.

## Environment

Always run commands from the repository root and load the custom ManimGX environment:

```sh
cd /home/marvin/Documents/university/mth_presentation_v2
source /home/marvin/Documents/Projects/manimgx/.venv/bin/activate
```

`manimgx` must resolve to that virtual environment. The ManimGX checkout at
`/home/marvin/Documents/Projects/manimgx` is a custom build; released or web
documentation may not match it. When unsure about an API, read the local docs:

- `/home/marvin/Documents/Projects/manimgx/docs/content/reference/`
- `/home/marvin/Documents/Projects/manimgx/skills/manimgx/SKILL.md`

Do not install or upgrade ManimGX. Do not edit the ManimGX checkout unless the user
has explicitly requested it beforehand. If the presentation needs a ManimGX change,
stop and report the blocker.

## Commands

The target is **1920×1080 at 60 fps**, which is ManimGX's default. Pass the
resolution and frame rate explicitly anyway so the intent is clear. Use `-o` so
generated files never land beside the source:

```sh
mkdir -p output/storyboard

# Fast layout/storyboard pass of the whole talk
manimgx inspect presentation.py -o output/storyboard/presentation.png

# A single section, with short rendering time
manimgx inspect section_forms.py FormsPreview -o output/storyboard/forms.png

# Final video
manimgx render presentation.py -r 1920x1080 --fps 60 -o output/presentation.mp4

# Slide deck; also writes output/presentation.html beside the video
manimgx present presentation.py -r 1920x1080 --fps 60 -o output/presentation.mp4 --no-open
```

`inspect` writes `presentation.png`, `presentation-2.png`, …; review every sheet. To
inspect particular moments:

```sh
manimgx inspect presentation.py -t 12.5,end -o output/storyboard/presentation.png
```

`render` also writes a storyboard beside the video. Use `--no-open` when no browser
should be launched.

`Presentation` and the section previews are `ThreeDScene`s, so `inspect` gives pictures
and a timeline but **skips the automatic 2D layout checks**. Visual review is
mandatory; a clean exit does not mean the layout is correct.

## Slide architecture

Follow the existing patterns; do not rewrite the scene plumbing.

- The talk is split into sections. Each `section_*.py` holds a mixin with `PAGE`,
  `TITLE` and a `play_*` method; `presentation.py` composes them in order. A preview
  scene in the same file renders just that section.
- In the full deck, move to a section with `self.start_section(FormsSection)`: it
  animates the page number and title, fades out the previous content, and checks the
  page against `PAGE`. Then call the section's `play_*` method.
- In a preview scene, call `self.prepare_section(FormsSection)` instead: it recreates
  the HUD at the section's page and title without animations, then call the same
  `play_*` method. This is why a preview needs no state from earlier sections.
- Section mixins are typed as `DeckScene` subclasses only under `TYPE_CHECKING` (the
  `_SectionBase` block at the top of each section file); at runtime they are plain
  classes. Keep this pattern in new section files so Pyright resolves the deck API.
- Begin each slide with `self.nslide()`. Do not call `next_section` directly; `nslide`
  sets the section type used by `manimgx present`. Speaker notes are not used, so the
  `notes` argument is not needed.
- The title slide is slide 0 and has no page number. `TitleSection.play_title` creates
  the HUD and ends with it visible on page 1. After it, `start_section` advances the
  title and page number and fades out the previous slide's content. Page numbers are
  automatic; never set `slide_number_val` by hand outside `make_hud`.
- `self.hud_objs` and `self.canvas_objs` hold the persistent fixed-in-frame overlays:
  slide title, logo, contact info, presentation title, and page number. Add a new
  persistent overlay in `DeckScene.make_hud`; `update_back_rects` then picks it up
  automatically, and `cleanup=True` leaves it alone.
- Use `self.camera.add_fixed_in_frame_mobjects(...)` for HUD or 2D overlays (pin only);
  `self.add(...)` shows them at once (previews). Normal slide content belongs in the
  scene via `self.play(...)`.
- `self.add(...)` only adds objects; use `self.play(...)` and `self.wait(...)` for time.
  `wait` takes seconds.

A new section normally looks like:

```python
# section_foo.py
import manimgx as m

from deck import DeckScene


class FooSection:
    PAGE = 4
    TITLE = r"A short title"

    def play_foo(self):
        self.nslide()
        content = m.VGroup(...)
        self.play(m.FadeIn(content))
        self.wait(1)


class FooPreview(FooSection, DeckScene):
    def construct(self) -> None:
        self.prepare_section(FooSection)
        self.play_foo()
```

Then add it to `presentation.py`:

```python
self.start_section(FooSection)
self.play_foo()
```

## Style and content

- Keep the current theme: `DARK_MODE`, `BACKCOL`, `FRONTCOL`, `TITLE_FONT_SIZE`,
  `CONTENT_FONT_SIZE`, and the `m.Typst`/`m.DecimalNumber` defaults. Do not hardcode a
  different palette or font size without a reason.
- Write raw strings and pass `typst_preamble(font_size)` so text wraps at `MAX_TEXT_WIDTH`.
  Keep `PresentationTitle` and `PresentationTitleShort` consistent.
- Slide titles are wrapped in Typst bold `*...*`; avoid unbalanced Typst markup, labels
  or special characters in the title strings.
- Compose with `VGroup`, `next_to`, `arrange`, and `to_edge` rather than absolute
  coordinates. Keep content clear of the fixed overlays and inside the 1920×1080 frame.
- Prefer one idea per slide, incremental reveals, and readable body text. Match the
  existing animation vocabulary (`FadeIn`, `Write`, `Transform`).
- This is a physics talk. Do not invent equations, results, citations, or claims. If
  the outline or content is missing, leave a clearly marked TODO and ask. Preserve the
  author, date, supervisor, and contact details unless asked to change them.

## Validation

1. Edit the section file (and `deck.py` only if the change is shared).
2. Run `inspect` on that section's preview first — it is much faster — then on the full
   `presentation.py`.
3. Open every storyboard sheet and check for clipping, overlap, small labels, and
   timing.
4. Fix and repeat 1-3.
5. Report what changed and the exact output paths.
6. The user will run `render` / `present` for final validation.

There is no automated test suite; these checks are the test.

## Guardrails

- Do not edit or commit `output/`; it is generated and ignored by git.
- Do not modify `assets/` or the ManimGX checkout unless the task requires it and the
  user has agreed beforehand.
- Do not delete slides or existing content unless asked.