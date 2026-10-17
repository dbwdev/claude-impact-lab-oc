"""Runs one packet end to end and writes out/<ID>.json."""

import time
from pathlib import Path

from . import config, llm
from .decide import checklist, recommend
from .render import render_packet
from .review import review_packet
from .schemas import PacketResult, Recommendation
from .transcribe import transcribe_packet
from .verify import verify

VERSION = "0.1.0"


def _print_events(event: str, data: dict) -> None:
    if event in ("stage", "halt", "done"):
        print(f"[{data.get('packet_id')}] {event}: {data.get('message', '')}")


def run_packet(pdf_path: Path, emit=_print_events) -> PacketResult:
    """emit(event, data) receives progress: stage, page, halt, done. The server streams these."""
    packet_id = pdf_path.stem
    timings: dict[str, float] = {}

    def step(name, fn, *args, **kwargs):
        t = time.monotonic()
        emit("stage", {"packet_id": packet_id, "stage": name, "status": "started", "message": f"{name}…"})
        result = fn(*args, **kwargs)
        timings[name] = round(time.monotonic() - t, 1)
        emit("stage", {"packet_id": packet_id, "stage": name, "status": "finished",
                       "seconds": timings[name], "message": f"{name} done in {timings[name]}s"})
        return result

    def on_page(page, total):
        emit("page", {"packet_id": packet_id, "page": page.page, "total": total, "page_type": page.page_type,
                      "legibility": page.legibility, "rotated": page.rotated_by_pipeline})

    paths = step("render", render_packet, pdf_path, packet_id)
    pages = step("transcribe", transcribe_packet, packet_id, paths, on_page=on_page)
    docs = checklist(pages)

    exposed = [p.page for p in pages if p.possible_unredacted_identifier]
    if exposed:
        # Ground rule 1: stop and get an organizer. Nothing past this point runs.
        emit("halt", {"packet_id": packet_id, "pages": exposed,
                      "message": f"Possible unredacted identifier on pages {exposed}. Tell an organizer."})
        rec = Recommendation(bucket="halted_privacy",
                             headline=f"Possible unredacted identifier on pages {exposed}. Tell an organizer.",
                             hard_fails=[], open_questions=[], judgment_calls=[], confirm_at_admission=[],
                             verification_flags=0)
        result = PacketResult(packet_id=packet_id, pipeline_version=VERSION, model=config.MODEL,
                              page_count=len(pages), pages=[], checklist=docs, review=None,
                              verification=[], recommendation=rec, timings_s=timings, usage=dict(llm.usage))
    else:
        review = step("review", review_packet, packet_id, pages)
        flags = step("verify", verify, review, pages)
        rec = recommend(review, flags, docs)
        result = PacketResult(packet_id=packet_id, pipeline_version=VERSION, model=config.MODEL,
                              page_count=len(pages), pages=pages, checklist=docs, review=review,
                              verification=flags, recommendation=rec, timings_s=timings, usage=dict(llm.usage))

    config.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (config.OUT_DIR / f"{packet_id}.json").write_text(result.model_dump_json(indent=1))
    emit("done", {"packet_id": packet_id, "bucket": rec.bucket, "message": f"{rec.bucket}: {rec.headline}"})
    return result
