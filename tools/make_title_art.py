"""Generate the title-screen backdrop: Cartan reproduced in formulas.

A pool of short Typst formulas -- the lines of ``tools/formulas.txt`` and the
subexpressions they are built from -- is typeset once (via Typst) and then
scattered over the canvas at arbitrary positions, sizes and colours, greedily
filling the regions where the Cartan portrait is bright -- the same trick as an
ASCII-art generator, but the "characters" are real formulas.
Cartan's structure equations are placed last, at anchor size and full opacity,
so they stay legible on top of the field.

Run it with the art toolchain, not the ManimGX environment:

    python -m venv ~/.venvs/title-art
    ~/.venvs/title-art/bin/pip install typst pillow numpy tqdm
    ~/.venvs/title-art/bin/python tools/make_title_art.py

Writes ``assets/title_math_background.png`` (1920x1080), which
``section_title.py`` loads as the title background.

Typeset sprites are cached under ``$XDG_CACHE_HOME/cartan-title-art``
(``~/.cache/cartan-title-art`` by default), so tweaking ``COUNT``, ``SEED`` or
the placement constants and rerunning is fast; delete that directory to force
a fresh typeset.
"""

import functools
import hashlib
import io
import os
from pathlib import Path

import numpy as np
import typst
import tqdm
from PIL import Image, ImageFilter

W, H = 1920, 1080
SEED = 10

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "cartan.png"
DESTINATION = ROOT / "assets" / "title_math_background_10.png"

# Deck palette: BACKCOL is the slide background.
BACK = np.array([18, 19, 23], dtype=np.float64)

PORTRAIT_HEIGHT = 0.94  # fraction of the frame the photo spans
FLOOR = 0.002  # ink density in the darkest regions, so the void keeps texture
COUNT = 20_000  # sprite placements; the run stops early once converged
SAMPLE_STEP = 4  # block size of the sampling grid, in pixels
INK_ALPHA = 0.95  # sprites are placed crisp, not as a fog
FORCED_HEIGHT = 64  # structure equations, in pixels

# Duotone by local brightness: deep blue shadows, warm taupe midtones, warm
# paper highlights -- echoes the old nebula background while staying quiet.
STOPS = [
    (0.00, (34, 54, 96)),
    (0.55, (150, 128, 106)),
    (1.00, (250, 236, 210)),
]

# (Typst math, weight). The formulas of tools/formulas.txt come first, one
# entry per line with weight 1.
POOL = [
    # -- tools/formulas.txt, one entry per line ------------------------------
    (r"T(X,Y) = nabla_X Y - nabla_Y X - [X,Y]", 1),
    (r"nabla_(partial_mu) partial_nu = Gamma^rho #h(0cm)_(mu nu) partial_rho", 1),
    (r"nabla_X e_b = omega^a #h(0cm)_b (X) e_a", 1),
    (r"R(X,Y) e_b = nabla_X nabla_Y e_b - nabla_Y nabla_X - nabla_([X,Y]) e_b", 1),
    (r"d e^a", 3),
    (r"d omega^a #h(0cm)_b", 2),
    (r"e^a", 3),
    (r"omega^a #h(0cm)_b", 3),
    (r"b^a = integral.cont_C e^a", 1),
    (r"T^a = T^a #h(0cm)_(mu nu) d x^mu and d x^nu", 1),
    (r"R^a #h(0cm)_(b mu nu) d x^mu and d x^nu", 1),
    (r"g = eta_(a b) e^a times.o e^b", 1),
    (r"e^a = (delta^a_mu + partial_mu u^a) d x^mu", 1),
    (r"T_p M", 1),
    (r"f(x) d x", 1),
    (r"g(x,y) d x and d y", 1),
    (r"Omega^k (M)", 1),
    (r"d^2 = 0", 1),
    (r"integral_M d omega = integral_(partial M) omega", 1),
    (r"F_x d x + F_y d y + F_z d z", 1),
    (r"F_x d y and d z + F_y d z and d x + F_z d x and d y", 1),
    (r"integral.double_S (bold(nabla) times bold(F)) dot.c d bold(A) = integral.cont_(partial S) bold(F) dot.c d bold(r)", 1),
    (r"integral.triple_V (bold(nabla) dot.c bold(F)) d V = integral.double_(partial V) bold(F) dot.c d bold(A)", 1),
    (r"bold(nabla) times bold(F) = 0", 1),
    (r"bold(F) = bold(nabla) f", 1),
    (r"bold(nabla) dot.c bold(F)", 1),
    (r"bold(F) = bold(nabla) times bold(A)", 1),

    # -- torsion and the covariant derivative -------------------------------
    (r"T^a", 5),
    (r"nabla_X Y", 4),
    (r"T(X,Y)", 3),
    (r"nabla_Y X", 3),
    (r"nabla_X", 3),
    (r"nabla_Y", 3),
    (r"[X,Y]", 3),

    # -- connection, frames and curvature -----------------------------------
    (r"nabla_X e_b", 4),
    (r"R(X,Y)", 4),
    (r"R^a #h(0cm)_(b mu nu)", 4),
    (r"T^a #h(0cm)_(mu nu)", 4),
    (r"nabla_(partial_mu) partial_nu", 3),
    (r"Gamma^rho #h(0cm)_(mu nu)", 3),
    (r"Gamma^rho", 3),
    (r"omega^a #h(0cm)_b (X)", 3),
    (r"e_a", 3),
    (r"e_b", 3),
    (r"R(X,Y) e_b", 3),
    (r"nabla_X nabla_Y e_b", 3),
    (r"nabla_([X,Y]) e_b", 2),

    # -- forms, coframes and coordinates ------------------------------------
    (r"d x", 4),
    (r"d x^mu", 4),
    (r"d x^mu and d x^nu", 4),
    (r"d omega", 4),
    (r"Omega^k", 4),
    (r"partial_mu", 4),
    (r"and", 4),
    (r"d y", 3),
    (r"d z", 3),
    (r"d x^nu", 3),
    (r"d x and d y", 3),
    (r"d y and d z", 3),
    (r"d z and d x", 3),
    (r"d^2", 3),
    (r"partial_nu", 3),
    (r"partial_rho", 3),
    (r"partial_mu u^a", 3),
    (r"(delta^a_mu + partial_mu u^a) d x^mu", 2),
    (r"delta^a_mu", 3),
    (r"eta_(a b)", 3),
    (r"e^a times.o e^b", 3),
    (r"times.o", 3),
    (r"f(x)", 3),
    (r"b^a", 4),
    (r"integral.cont_C e^a", 4),
    (r"F_x d x", 3),
    (r"F_y d y", 3),
    (r"F_z d z", 3),

    # -- integrals, gradient and Stokes -------------------------------------
    (r"integral_M", 4),
    (r"integral_(partial M)", 4),
    (r"integral_M d omega", 4),
    (r"integral_(partial M) omega", 4),
    (r"partial M", 3),
    (r"bold(nabla) times bold(F)", 3),
    (r"bold(nabla) f", 3),
    (r"bold(nabla) times bold(A)", 3),
    (r"bold(F) dot.c d bold(A)", 3),
    (r"bold(F) dot.c d bold(r)", 3),
    (r"d bold(A)", 3),
    (r"d bold(r)", 3),
    (r"d V", 3),
    (r"integral.double_S", 3),
    (r"integral.cont_(partial S)", 3),
    (r"integral.triple_V", 3),
    (r"integral.double_(partial V)", 3),
    (r"partial S", 3),
    (r"partial V", 3),
    (r"times", 4),
    (r"integral", 3),
]

# Cartan's structure equations: formula and the anchor their x is pulled to.
FORCED = [
    (r"T^a = d e^a + omega^a #h(0cm)_b and e^b", (0.76*W, H / 2)),
    (r"R^a #h(0cm)_b = d omega^a #h(0cm)_b + omega^a #h(0cm)_c and omega^c #h(0cm)_b", (30,3/4*H)),
]

PREAMBLE = "#set page(width: auto, height: auto, margin: 0pt, fill: none)"

# Typeset sprites are cached on disk (formula + ppi + Typst version), so a run
# with new layout parameters or a new seed only redoes the placement. The cache
# lives outside the repository; delete it, or point XDG_CACHE_HOME elsewhere,
# to force a fresh typeset.
CACHE = Path(
    os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache"
) / "cartan-title-art"


# --- typesetting -----------------------------------------------------------


def cache_path(source, ppi):
    version = getattr(typst, "__version__", "unknown")
    key = "\0".join((version, PREAMBLE, source, str(ppi)))
    return CACHE / (hashlib.sha256(key.encode()).hexdigest()[:24] + ".png")


@functools.lru_cache(maxsize=384)
def sprite(source, ppi):
    """Typeset one formula and return its ink as a uint8 alpha mask.

    The cropped mask is cached on disk, so repeated runs are not slowed down
    by Typst except on the very first run.
    """
    path = cache_path(source, ppi)
    try:
        with Image.open(path) as cached:
            return np.array(cached.convert("L"), dtype=np.uint8)
    except (OSError, ValueError):
        pass  # missing or unreadable cache entry: typeset it again

    document = f"{PREAMBLE}\n$ {source} $"
    png = typst.compile(document.encode(), format="png", ppi=ppi)
    image = Image.open(io.BytesIO(png)).convert("RGBA")
    bbox = image.split()[3].getbbox()
    if bbox:
        image = image.crop(bbox)
    mask = np.asarray(image.split()[3], dtype=np.uint8)

    CACHE.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.stem}.{os.getpid()}.tmp")
    Image.fromarray(mask).save(temporary, format="PNG")
    os.replace(temporary, path)  # atomic, so parallel runs cannot corrupt it
    return mask


@functools.lru_cache(maxsize=256)
def ink_at(source, height_px):
    """Alpha mask for a formula, rendered sharp enough for `height_px`.

    Returns ``None`` when the formula would have to be upscaled, which would
    blur it into a blob (e.g. the dot of ``dot.c``).
    """
    base = sprite(source, 600)
    need = height_px * 1.4 / base.shape[0]
    ppi = 600 if need <= 1 else (1200 if need <= 2 else 2400)
    mask = sprite(source, ppi)
    if mask.shape[0] < height_px:
        return None
    width = max(1, round(mask.shape[1] * height_px / mask.shape[0]))
    scaled = Image.fromarray(mask).resize((width, height_px), Image.LANCZOS)
    return np.asarray(scaled, dtype=np.float64) / 255.0


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
    """Mean over `step` x `step` blocks, summing the contiguous axes first."""
    rows = a.reshape(a.shape[0] // step, step, a.shape[1]).sum(axis=1)
    return rows.reshape(
        a.shape[0] // step, a.shape[1] // step, step
    ).sum(axis=2) / (step * step)


def integral_image(a):
    """Summed-area table, so region means cost only four lookups."""
    return np.pad(a, ((1, 0), (1, 0))).cumsum(axis=0).cumsum(axis=1)


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


def sample_position(rng, grid, cdf):
    """Draw a canvas position, weighted by the current deficit map."""
    index = min(np.searchsorted(cdf, rng.random(), side="right"), grid.size - 1)
    row, column = np.divmod(index, grid.shape[1])
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
    detail_scale = 1.4 * detail
    # The edge boost is constant, so its block grid is built once.
    edge_grid = 1.0 + 4.0 * block_mean(edges, SAMPLE_STEP)
    # Region means of the target are read off a summed-area table.
    target_sum = integral_image(target)

    weighted = [source for source, weight in POOL for _ in range(weight)]
    metrics = {}
    for source, _ in POOL:
        mask = sprite(source, 600)
        metrics[source] = mask.shape[1] / mask.shape[0], mask.shape[0]
    # Only sprites that stay sharp when enlarged can serve as large anchors:
    # the biggest anchor is 88 px and `ink_at` tops out at 2400 ppi, i.e. four
    # times the 600 ppi height, so anything shorter than 22 px is out.
    compact = [
        source
        for source, _ in POOL
        if metrics[source][0] <= 7 and metrics[source][1] >= 22
    ]

    coverage = np.zeros((H, W), dtype=np.float64)
    canvas = np.empty((H, W, 3), dtype=np.float64)
    canvas[:] = BACK

    grid = None
    cdf = None
    for i in tqdm.tqdm(range(COUNT)):
        if i % 16 == 0:
            error = np.maximum(target - coverage, 0.0)
            if error.mean() < 0.004:
                print(f"converged after {i} sprites")
                break
            error = np.maximum(error, detail_scale * (error > 0.02))
            pull = block_mean(error, SAMPLE_STEP) ** 1.5
            grid = pull * edge_grid
            total = grid.sum()
            if total <= 0.0:
                break
            grid /= total
            cdf = np.cumsum(grid.ravel())

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

        ink = ink_at(source, height_px)
        if ink is None:
            continue  # sprite too small to be typeset sharp at this size
        density = max(ink.mean(), 1e-3)
        width = ink.shape[1]

        # Try a few candidates, keep the one that fits the local deficit best.
        best = None
        for _ in range(6):
            x, y = sample_position(rng, grid, cdf)
            x = min(max(x, 0), W - width)
            y = min(max(y, 0), H - height_px)
            want = (
                target_sum[y + height_px, x + width]
                - target_sum[y, x + width]
                - target_sum[y + height_px, x]
                + target_sum[y, x]
            ) / (height_px * width)
            have = coverage[y:y + height_px, x:x + width].mean()
            margin = (want - have) / density
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
        ink = ink_at(source, FORCED_HEIGHT)
        for _ in range(10):
            x, y = sample_position(rng, grid, cdf)
            x = int(x * 0.01 + 0.99 * anchor_x)
            y = int(y * 0.01 + 0.99 * anchor_y)
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
