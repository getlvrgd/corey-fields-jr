"""Turn the black-matte JPEG cutouts in images/web/ into transparent WebP files in images/cut/.

Several pack images were transparent PNGs that got flattened onto black. This flood-fills the
black matte from the image border, feathers a thin edge band by un-multiplying against black,
and writes WebP with alpha. Run from the pack root:  python3 tools/make_cutouts.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "web"
OUT = ROOT / "images" / "cut"

# name -> (source file, optional crop box (l, t, r, b), max long edge)
JOBS = {
    "logo-mark": ("15-logo-c-window-mark.jpg", None, 400),
    "jobsite-collage": ("03-corey-on-jobsite-collage.jpg", None, 1600),
    "portrait-process": ("04-portrait-process-collage.jpg", None, 912),
    "nbo-bundle": ("05-nbo-program-bundle.jpg", None, 1000),
    "before-you-build": ("06-before-you-build-guide.jpg", None, 1000),
    "deal-worksheet": ("07-deal-viability-worksheet.jpg", None, 1100),  # see PAPER_MASKS
    # Top sketch only. The lower half is a cashflow chart in another currency plus a 3D house render.
    "six-phase": ("09-six-phase-overview.jpg", (0, 0, 741, 366), 741),
}

# Drop shadows here sit inside a ring of lighter JPEG noise the flood fill cannot cross.
# For these, keep only the paper rectangle (l, t, r, b) in source px. The pencil tip past the
# paper edge is clipped. Its shadow sits on the same black and cannot be separated cleanly.
PAPER_MASKS = {
    "deal-worksheet": (75, 9, 1231, 1516),
}

THRESH = 30   # max channel value treated as matte
# Higher matte threshold where white photo borders protect the content and the drop shadow
# carries JPEG noise brighter than THRESH.
THRESH_OVERRIDES = {"jobsite-collage": 100, "portrait-process": 100}
BAND = 3      # px feather band around the matte


def flood_matte(rgb: np.ndarray, thresh: int = THRESH) -> np.ndarray:
    dark = (rgb.max(axis=2) < thresh).astype(np.uint8) * 255
    mask = Image.fromarray(dark).copy()  # copy: floodfill is a no-op on array-backed images
    w, h = mask.size
    px = mask.load()
    border = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    border += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    for xy in border:
        if px[xy] == 255:
            ImageDraw.floodfill(mask, xy, 128)
    return np.array(mask) == 128


def dilate(m: np.ndarray, n: int) -> np.ndarray:
    out = m.copy()
    for _ in range(n):
        g = out.copy()
        g[1:] |= out[:-1]
        g[:-1] |= out[1:]
        g[:, 1:] |= out[:, :-1]
        g[:, :-1] |= out[:, 1:]
        out = g
    return out


def cutout(im: Image.Image, paper=None, thresh: int = THRESH) -> Image.Image:
    rgb = np.asarray(im.convert("RGB")).astype(np.float32)
    bg = flood_matte(rgb.astype(np.uint8), thresh)
    if paper:
        l, t, r, b = paper
        bg = np.ones(bg.shape, bool)
        bg[t:b, l:r] = False
    band = dilate(bg, BAND) & ~bg
    alpha = np.ones(bg.shape, np.float32)
    alpha[bg] = 0
    a_band = np.clip(rgb.max(axis=2) / 110.0, 0, 1)
    alpha[band] = a_band[band]
    safe = np.maximum(alpha, 1e-3)[..., None]
    color = np.where(band[..., None], np.clip(rgb / safe, 0, 255), rgb)
    rgba = np.dstack([color, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba)


# Plain rectangular crops (no matte removal): name -> (source, box)
CROPS = {
    # Middle print of the jobsite collage: Corey measuring a footing trench.
    "jobsite-measuring": ("03-corey-on-jobsite-collage.jpg", (572, 64, 1090, 404)),
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, box) in CROPS.items():
        dest = OUT / f"{name}.jpg"
        Image.open(SRC / src).convert("RGB").crop(box).save(dest, quality=90)
        print(f"{dest.relative_to(ROOT)}  {box[2] - box[0]}x{box[3] - box[1]}")
    for name, (src, crop, max_edge) in JOBS.items():
        im = Image.open(SRC / src)
        if crop:
            im = im.crop(crop)
        out = cutout(im, PAPER_MASKS.get(name), THRESH_OVERRIDES.get(name, THRESH))
        bbox = out.getchannel("A").getbbox()
        if bbox:
            out = out.crop(bbox)
        out.thumbnail((max_edge, max_edge), Image.LANCZOS)
        dest = OUT / f"{name}.webp"
        out.save(dest, "WEBP", quality=84, method=6)
        print(f"{dest.relative_to(ROOT)}  {out.size}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
