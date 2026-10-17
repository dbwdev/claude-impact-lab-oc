"""Step 1: render each packet page to a JPEG in the cache. No system tools needed."""

from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image

from . import config


def page_dir(packet_id: str) -> Path:
    return config.CACHE_DIR / packet_id / "pages"


def render_packet(pdf_path: Path, packet_id: str) -> list[Path]:
    out = page_dir(packet_id)
    out.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(pdf_path)
    paths = []
    for i in range(len(pdf)):
        path = out / f"p{i + 1:03d}.jpg"
        if not path.exists():
            page = pdf[i]
            w, h = page.get_size()
            scale = config.RENDER_LONG_EDGE / max(w, h)
            img = page.render(scale=scale, grayscale=True).to_pil()
            img.save(path, "JPEG", quality=85)
        paths.append(path)
    return paths


def rotate_clockwise(src: Path, degrees: int) -> Path:
    dst = src.with_name(f"{src.stem}_r{degrees}.jpg")
    if not dst.exists():
        # PIL rotates counter-clockwise for positive angles.
        Image.open(src).rotate(-degrees, expand=True).save(dst, "JPEG", quality=85)
    return dst
