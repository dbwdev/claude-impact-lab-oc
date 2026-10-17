"""Step 2: Claude reads each page image (our OCR layer). Results are cached per page."""

import base64
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import config, llm
from .render import rotate_clockwise
from .schemas import Page, PageReading

SYSTEM = """You transcribe one page of a faxed hospital referral packet for a recuperative care \
intake team. The packet has been de-identified: black boxes cover names, dates, facilities, \
numbers and signatures.

Rules:
- Transcribe faithfully, including handwriting, checkboxes ([x] / [ ]) and table rows. \
Keep the page's own reading order. Do not summarize, correct or add anything.
- Write [REDACTED] for each black box. A black box means "removed for privacy", never "missing".
- Write [illegible] where you cannot read the text. Do not guess at clinical values.
- If you can see an identifier that was NOT blacked out (a person's name, a full date, phone, \
address, record or account number), do not transcribe it: write [IDENTIFIER] instead, set \
possible_unredacted_identifier to true and list only the kind of identifier.
- If the page is sideways or upside down, still transcribe what you can and report the \
clockwise rotation that would make it upright."""


def _image_block(path: Path) -> dict:
    data = base64.standard_b64encode(path.read_bytes()).decode()
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}


def _read(path: Path, page_no: int, total: int) -> PageReading:
    return llm.parse(
        output=PageReading,
        system=SYSTEM,
        content=[_image_block(path), {"type": "text", "text": f"Page {page_no} of {total}."}],
        effort=config.TRANSCRIBE_EFFORT,
    )


def transcribe_page(path: Path, page_no: int, total: int, cache: Path) -> Page:
    if cache.exists():
        return Page.model_validate_json(cache.read_text())
    reading = _read(path, page_no, total)
    rotated = 0
    if reading.rotate_clockwise_to_upright != "0":
        # Re-read the upright image once; sideways faxes transcribe much better upright.
        rotated = int(reading.rotate_clockwise_to_upright)
        reading = _read(rotate_clockwise(path, rotated), page_no, total)
    page = Page(page=page_no, rotated_by_pipeline=rotated, **reading.model_dump())
    cache.write_text(page.model_dump_json(indent=1))
    return page


def transcribe_packet(packet_id: str, page_paths: list[Path]) -> list[Page]:
    cache_dir = config.CACHE_DIR / packet_id / "transcripts"
    cache_dir.mkdir(parents=True, exist_ok=True)
    total = len(page_paths)
    with ThreadPoolExecutor(config.PAGE_WORKERS) as pool:
        futures = [
            pool.submit(transcribe_page, p, i + 1, total, cache_dir / f"p{i + 1:03d}.json")
            for i, p in enumerate(page_paths)
        ]
        return [f.result() for f in futures]


def pages_as_text(pages: list[Page]) -> str:
    parts = []
    for p in pages:
        attrs = {"n": p.page, "type": p.page_type, "legibility": p.legibility}
        if p.looks_like_prior_stay:
            attrs["prior_stay"] = "likely"
        head = " ".join(f'{k}="{v}"' for k, v in attrs.items())
        parts.append(f"<page {head}>\n{p.transcript}\n</page>")
    return "\n\n".join(parts)


def dump_text(pages: list[Page]) -> str:
    return json.dumps([p.model_dump() for p in pages])
