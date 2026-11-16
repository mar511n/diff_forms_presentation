"""Generate the title-screen backdrop: Cartan reproduced in formulas.

A pool of short LaTeX/Typst formulas and objects is typeset once (via Typst)
and then scattered over the canvas at arbitrary positions, sizes and colours,
greedily filling the regions where the Cartan portrait is bright -- the same
trick as an ASCII-art generator, but the "characters" are real formulas.
Cartan's structure equations are placed last, at anchor size and full opacity,
so they stay legible on top of the field.

Run it with the art toolchain, not the ManimGX environment:

    python -m venv ~/.venvs/title-art
    ~/.venvs/title-art/bin/pip install typst pillow numpy
    ~/.venvs/title-art/bin/python tools/make_title_art.py

Writes ``assets/title_math_background.png`` (1920x1080), which
``section_title.py`` loads as the title background.
"""

import functools
import io
from pathlib import Path

import numpy as np
import typst
from PIL import Image, ImageFilter

W, H = 1920, 1080
SEED = 7

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "cartan.png"
DESTINATION = ROOT / "assets" / "title_math_background.png"

# Deck palette: BACKCOL is the slide background.
BACK = np.array([18, 19, 23], dtype=np.float64)

PORTRAIT_HEIGHT = 0.94  # fraction of the frame the photo spans
FLOOR = 0.02  # ink density in the darkest regions, so the void keeps texture
COUNT = 13_000  # sprite placements; the run stops early once converged
SAMPLE_STEP = 4  # block size of the sampling grid, in pixels
INK_ALPHA = 1.0  # sprites are placed crisp, not as a fog
FORCED_HEIGHT = 64  # structure equations, in pixels

# Duotone by local brightness: deep blue shadows, warm taupe midtones, warm
# paper highlights -- echoes the old nebula background while staying quiet.
STOPS = [
    (0.00, (34, 54, 96)),
    (0.55, (150, 128, 106)),
    (1.00, (250, 236, 210)),
]

# (Typst math, weight). Single objects are common, whole equations are rare.
POOL = [
    (r"integral", 4), (r"partial", 4), (r"and", 4),
    (r"star.op", 4),
    (r"nabla", 4), (r"times", 2), (r"⊕", 1), (r"⊗", 1),
    (r"Omega", 3), (r"omega", 5), (r"alpha", 4), (r"beta", 4), (r"theta", 4),
    (r"delta", 3), (r"Sigma", 3), (r"Lambda", 2), (r"eta", 3), (r"RR", 2),
    (r"d omega", 4), (r"d alpha", 3), (r"d beta", 3), (r"d theta", 3),
    (r"d x^i", 2), (r"d x^1", 2), (r"d x^n", 2), (r"d A", 2), (r"d F", 2),
    (r"omega|_p", 2), (r"Omega^k", 3), (r"Omega^k (M)", 2),
    (r"omega in Omega^k (M)", 2),
    (r"T_p M", 2), (r"T^a", 2), (r"R^a_b", 2), (r"theta^a", 2),
    (r"omega^a_b", 2), (r"omega^a_c and omega^c_b", 1),
    (r"partial_i", 3), (r"partial_i f", 2), (r"v^i", 2), (r"x^i", 2),
    (r"f_i", 2), (r"g^(\mu nu)", 2), (r"eta_(a b)", 2),
    (r'"sgn"(sigma)', 2), (r"(-1)^k", 2), (r"(-1)^i", 1), (r"k!", 2),
    (r'"vol"_g', 2), (r"chevron.l alpha, beta chevron.r", 2),
    (r"integral_M", 2), (r"integral_(partial M)", 2),
    (r"integral_M d omega", 2), (r"integral_(partial M) omega", 2),
    (r"d^2 = 0", 2), (r"d F = 0", 2), (r"F = d A", 2),
    (r"d star.op F = star.op J", 2),
    (r"d : Omega^k -> Omega^(k+1)", 1),
    (r"d beta = 0 ==> beta = d alpha", 1),
    (r"alpha and star.op beta = chevron.l alpha, beta chevron.r", 1),
    (r"star.op star.op = (-1)^(k (n - k) + q)", 1),
    (r"T^a = d theta^a + omega^a_b and theta^b", 2),
    (r"R^a_b = d omega^a_b + omega^a_c and omega^c_b", 2),
    (r"integral_M d omega = integral_(partial M) omega", 1),
    (r"g = eta_(a b) theta^a ⊗ theta^b", 1),
    (r"d f (v) = v^i partial_i f", 1),
    (r"1/(k! ell!)", 1), (r"sum_(sigma in S_(k + ell))", 1), (r"8 pi G", 1),
    (r"omega_p : T_p M times dots.c times T_p M -> RR", 1),
]

# Cartan's structure equations: formula and the anchor their x is pulled to.
FORCED = [
    (r"T^a = d theta^a + omega^a_b and theta^b", (0.0, H / 2)),
    (r"R^a_b = d omega^a_b + omega^a_c and omega^c_b", (3 * W / 4, H / 2)),
]

PREAMBLE = "#set page(width: auto, height: auto, margin: 0pt, fill: none)"


# --- typesetting -----------------------------------------------------------


@functools.lru_cache(maxsize=160)
def sprite(source, ppi):
    """Typeset one formula and return its ink as a float alpha mask."""
    document = f"{PREAMBLE}\n$ {source} $"
    png = typst.compile(document.encode(), format="png", ppi=ppi)
    image = Image.open(io.BytesIO(png)).convert("RGBA")
    bbox = image.split()[3].getbbox()
    if bbox:
        image = image.crop(bbox)
    return np.asarray(image.split()[3], dtype=np.float64) / 255.0


def ink_at(source, height_px):
    """Alpha mask for a formula, rendered sharp enough for `height_px`.

    Returns ``None`` when the formula would have to be upscaled, which would
    blur it into a blob (e.g. the dots of ``dots.c``).
    """
    base = sprite(source, 600)
    need = height_px * 1.4 / base.shape[0]
    ppi = 600 if need <= 1 else (1200 if need <= 2 else 2400)
    mask = sprite(source, ppi) if ppi != 600 else base
    if mask.shape[0] < height_px:
        return None
    width = max(1, round(mask.shape[1] * height_px / mask.shape[0]))
    return np.asarray(
        Image.fromarray((mask * 255).astype(np.uint8)).resize(
            (width, height_px), Image.LANCZOS
        ),
        dtype=np.float64,
    ) / 255.0


# --- density and colour maps ----------------------------------------------


def colour_lut():
    """256-entry RGB lookup: brightness -> ink colour."""
    xs = np.array([stop[0] for stop in STOPS])
    channels = np.array([stop[1] for stop in STOPS], dtype=np.float64)
    ts = np.linspace(0.0, 1.0, 256)
    return np.stack(
        [np.interp(ts, xs, channels[:, c]) for c in range(3)], axis=1
    )


def blur(a, radius):
    return np.asarray(
        Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).filter(
            ImageFilter.GaussianBlur(radius)
        ),
        dtype=np.float64,
    ) / 255.0


def block_mean(a, step):
    return a.reshape(a.shape[0] // step, step, a.shape[1] // step, step).mean(
        axis=(1, 3)
    )


def target_density():
    """Portrait brightness as a density map on the full canvas."""
    photo = Image.open(SOURCE).convert("L")
    height = int(H * PORTRAIT_HEIGHT)
    width = round(photo.width * height / photo.height)
    photo = photo.resize((width, height), Image.LANCZOS)

    lum = np.asarray(photo, dtype=np.float64) / 255.0
    lum = np.clip((lum - 0.04) / 0.94, 0.0, 1.0) ** 1.1

    canvas = np.zeros((H, W), dtype=np.float64)
    x0, y0 = (W - width) // 2, (H - height) // 2
    canvas[y0:y0 + height, x0:x0 + width] = lum
    return FLOOR + (1.0 - FLOOR) * blur(canvas, 2), x0, y0, width, height


# --- placement -------------------------------------------------------------


def sample_position(rng, grid):
    """Draw a canvas position, weighted by the current deficit map."""
    cell = rng.choice(grid.size, p=grid.ravel())
    row, column = np.divmod(cell, grid.shape[1])
    return (
        int(column * SAMPLE_STEP + rng.integers(0, SAMPLE_STEP)),
        int(row * SAMPLE_STEP + rng.integers(0, SAMPLE_STEP)),
    )


def paste(canvas, ink, x, y, colour, alpha=1.0):
    """Composite one sprite onto the canvas (alpha-over) at (x, y)."""
    a = (ink * alpha)[..., None]
    view = canvas[y:y + ink.shape[0], x:x + ink.shape[1]]
    view[:] = view * (1.0 - a) + colour * a


def main():
    rng = np.random.default_rng(SEED)
    lut = colour_lut()

    target, px0, py0, pw, ph = target_density()

    # Colour driver: the portrait's own brightness, softly blurred.
    brightness = np.zeros((H, W), dtype=np.float64)
    brightness[py0:py0 + ph, px0:px0 + pw] = np.asarray(
        Image.open(SOURCE).convert("L").resize((pw, ph), Image.LANCZOS),
        dtype=np.float64,
    ) / 255.0
    brightness = np.clip((blur(brightness, 5) - 0.03) / 0.94, 0.0, 1.0)

    # Edge map, to pull sprites towards the drawing's features.
    gy, gx = np.gradient(target)
    edges = blur(np.hypot(gx, gy) / (np.hypot(gx, gy).max() + 1e-9), 6)
    detail = np.abs(target - blur(target, 5))

    weighted = [source for source, weight in POOL for _ in range(weight)]
    aspect = {}
    for source, _ in POOL:
        mask = sprite(source, 600)
        aspect[source] = mask.shape[1] / mask.shape[0]
    compact = [source for source, _ in POOL if aspect[source] <= 7]

    coverage = np.zeros((H, W), dtype=np.float64)
    canvas = np.empty((H, W, 3), dtype=np.float64)
    canvas[:] = BACK

    grid = None
    for i in range(COUNT):
        if i % 16 == 0:
            error = np.maximum(target - coverage, 0.0)
            if error.mean() < 0.004:
                print(f"converged after {i} sprites")
                break
            error = np.maximum(error, 1.4 * detail * (error > 0.02))
            pull = block_mean(error, SAMPLE_STEP) ** 1.5
            boost = 1.0 + 4.0 * block_mean(edges, SAMPLE_STEP)
            grid = pull * boost
            total = grid.sum()
            if total <= 0.0:
                break
            grid /= total

        share = i / COUNT
        u = rng.random()
        if share < 0.04:  # rare large anchors
            lo, hi, pool = np.log(44), np.log(88), compact
        elif share < 0.32:
            lo, hi, pool = np.log(20), np.log(40), weighted
        else:
            lo, hi, pool = np.log(9), np.log(20), weighted
        source = pool[rng.integers(len(pool))]
        height_px = int(round(float(np.exp(lo + u * (hi - lo)))))

        # Try a few candidates, keep the one that fits the local deficit best.
        best = None
        for _ in range(6):
            x, y = sample_position(rng, grid)
            ink = ink_at(source, height_px)
            if ink is None:
                continue
            x = min(max(x, 0), W - ink.shape[1])
            y = min(max(y, 0), H - height_px)
            want = target[y:y + height_px, x:x + ink.shape[1]].mean()
            have = coverage[y:y + height_px, x:x + ink.shape[1]].mean()
            margin = (want - have) / max(ink.mean(), 1e-3)
            if best is None or margin > best[0]:
                best = (margin, ink, x, y)
        margin, ink, x, y = best

        if margin < 0.08:
            continue  # region already at its target density
        alpha = INK_ALPHA * float(np.clip(margin, 0.5, 1.0))
        tone = lut[int(np.clip(
            brightness[y:y + height_px, x:x + ink.shape[1]].mean() * 255, 0, 255
        ))]
        colour = np.clip(
            tone * (0.85 + 0.3 * rng.random()) + rng.normal(0, 7, 3), 0, 255
        )

        paste(canvas, ink, x, y, colour, alpha)
        coverage[y:y + height_px, x:x + ink.shape[1]] += ink * alpha

    # Cartan's structure equations go in last, at anchor size, so nothing
    # covers them and they stay legible on top of the field.
    for source, (anchor_x, anchor_y) in FORCED:
        best = None
        for _ in range(10):
            x, y = sample_position(rng, grid)
            x = int(x * 0.3 + 0.7 * anchor_x)
            y = int(y * 0.8 + 0.2 * anchor_y)
            ink = ink_at(source, FORCED_HEIGHT)
            if ink is None:
                continue
            x = min(max(x, 0), W - ink.shape[1])
            y = min(max(y, 0), H - FORCED_HEIGHT)
            deficit = target[y:y + FORCED_HEIGHT, x:x + ink.shape[1]].mean() - (
                coverage[y:y + FORCED_HEIGHT, x:x + ink.shape[1]].mean()
            )
            if best is None or deficit > best[0]:
                best = (deficit, ink, x, y)
        deficit, ink, x, y = best
        tone = lut[int(np.clip(
            brightness[y:y + FORCED_HEIGHT, x:x + ink.shape[1]].mean() * 255, 0, 255
        ))]
        colour = np.clip(tone * 1.05 + rng.normal(0, 5, 3), 0, 255)
        paste(canvas, ink, x, y, colour)
        print(f"forced source at ({x}, {y})")

    residual = np.maximum(target - coverage, 0).mean()
    print(f"placed sprites, mean residual error {residual:.4f}")
    out = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8), "RGB")
    out.save(DESTINATION)
    print(f"wrote {DESTINATION}")


if __name__ == "__main__":
    main()
