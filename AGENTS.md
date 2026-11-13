# AGENTS.md

## What this repository is

Source for the group-seminar presentation **“A physical mapping between metric and
torsionful geometry in 2D”** (Marvin Henke, supervisor Dr. Nikodem Szpak, AG König).
This is a presentation project, not the ManimGX library.

- `presentation.py` — the talk. `Presentation` is the only scene.
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

# Fast layout/storyboard pass
manimgx inspect presentation.py -o output/storyboard/presentation.png

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

`Presentation` is a `ThreeDScene`, so `inspect` gives pictures and a timeline but
**skips the automatic 2D layout checks**. Visual review is mandatory; a clean exit
does not mean the layout is correct.

## Slide architecture

Follow the existing patterns; do not rewrite the scene plumbing.

- Begin each slide with `self.nslide()`. Do not call `next_section` directly; `nslide`
  sets the section type used by `manimgx present`. Speaker notes are not used, so the
  `notes` argument is not needed.
- The title slide is slide 0 and has no page number. After it,
  `self.setup_new_slide("Title", cleanup=True)` advances the title and page number
  and fades out the previous slide's content. Page numbers are automatic; never set
  `slide_number_val` by hand.
- `self.canvas_objs` holds persistent fixed-in-frame overlays: slide title, logo,
  contact info, presentation title, and page number. Add a new persistent overlay to
  `self.canvas_objs`; otherwise `cleanup=True` will fade it out with the slide content.
- If a new overlay needs the backdrop treatment used on the table-of-contents slide,
  also add it to the list inside `update_back_rects()`.
- Use `self.camera.add_fixed_in_frame_mobjects(...)` for HUD or 2D overlays. Normal
  slide content belongs in the scene via `self.play(...)`.
- `self.add(...)` only adds objects; use `self.play(...)` and `self.wait(...)` for time.
  `wait` takes seconds.

A new slide normally looks like:

```python
self.nslide()
self.setup_new_slide("Short title", cleanup=True)
content = m.VGroup(...)
self.play(m.FadeIn(content))
self.wait(1)
```

## Style and content

- Keep the current theme: `DARK_MODE`, `BACKCOL`, `FRONTCOL`, `TITLE_FONT_SIZE`,
  `CONTENT_FONT_SIZE`, and the `m.Typst`/`m.DecimalNumber` defaults. Do not hardcode a
  different palette or font size without a reason.
- Use `m.Tex`/`m.MathTex` for typeset text and math, matching nearby code, and use raw
  strings. Preserve the existing `tex_environment=""` pattern for multi-line TeX.
  Keep `PresentationTitle` and `PresentationTitleShort` consistent.
- Slide titles are injected into `\textbf{...}`; avoid unescaped braces and backslashes
  in the title strings.
- Compose with `VGroup`, `next_to`, `arrange`, and `to_edge` rather than absolute
  coordinates. Keep content clear of the fixed overlays and inside the 1920×1080 frame.
- Prefer one idea per slide, incremental reveals, and readable body text. Match the
  existing animation vocabulary (`FadeIn`, `Write`, `Transform`).
- This is a physics talk. Do not invent equations, results, citations, or claims. If
  the outline or content is missing, leave a clearly marked TODO and ask. Preserve the
  author, date, supervisor, and contact details unless asked to change them.

## Validation

1. Edit `presentation.py` (and assets only if necessary).
2. Run `inspect`; open every storyboard sheet and check for clipping, overlap, small
   labels, and timing.
3. Fix and repeat 1-2.
4. Report what changed and the exact output paths.
5. The user will run `render` / `present` for final validation.

There is no automated test suite; these checks are the test.

## Guardrails

- Do not edit or commit `output/`; it is generated and ignored by git.
- Do not modify `assets/` or the ManimGX checkout unless the task requires it and the
  user has agreed beforehand.
- Do not delete slides or existing content unless asked.