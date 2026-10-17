"""HTTP API for the app side. Local only: packets and results never leave this machine except
for the model calls. Run with `uv run intake serve` (default http://localhost:8000, docs at /docs).

A run happens in a worker thread; its progress events are kept in memory and streamed over SSE,
so a client that connects late still gets every event from the start.
"""

import asyncio
import json
import re
import shutil
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Literal

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

from . import config
from .pipeline import run_packet
from .render import page_dir
from .schemas import PacketResult

app = FastAPI(title="IHH referral intake pipeline", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_executor = ThreadPoolExecutor(max_workers=2)
_lock = threading.Lock()


class Run(BaseModel):
    run_id: str
    packet_id: str
    status: Literal["queued", "running", "done", "failed"] = "queued"
    error: str | None = None
    events: list[dict] = []


_runs: dict[str, Run] = {}


class PacketInfo(BaseModel):
    packet_id: str
    has_result: bool
    bucket: str | None = None
    headline: str | None = None


class RunStarted(BaseModel):
    run_id: str
    packet_id: str
    events_url: str
    result_url: str


def _pdf(packet_id: str):
    path = config.PACKETS_DIR / f"{packet_id}.pdf"
    if not re.fullmatch(r"[A-Za-z0-9_-]+", packet_id) or not path.exists():
        raise HTTPException(404, f"No packet {packet_id!r}")
    return path


def _result(packet_id: str) -> PacketResult | None:
    path = config.OUT_DIR / f"{packet_id}.json"
    return PacketResult.model_validate_json(path.read_text()) if path.exists() else None


@app.get("/health")
def health() -> dict:
    return {"ok": True, "model": config.MODEL}


@app.get("/packets")
def list_packets() -> list[PacketInfo]:
    out = []
    for pdf in sorted(config.PACKETS_DIR.glob("*.pdf")):
        r = _result(pdf.stem)
        out.append(PacketInfo(packet_id=pdf.stem, has_result=r is not None,
                              bucket=r and r.recommendation.bucket, headline=r and r.recommendation.headline))
    return out


@app.post("/packets", status_code=201)
async def upload_packet(file: UploadFile) -> PacketInfo:
    """Add a new packet (e.g. one a judge hands us). Saved next to the others, which git ignores."""
    stem = re.sub(r"[^A-Za-z0-9_-]", "_", (file.filename or "packet").rsplit(".", 1)[0])[:40] or "packet"
    path = config.PACKETS_DIR / f"{stem}.pdf"
    with path.open("wb") as fh:
        shutil.copyfileobj(file.file, fh)
    return PacketInfo(packet_id=stem, has_result=False)


@app.post("/packets/{packet_id}/runs", status_code=202)
def start_run(packet_id: str, force: bool = False) -> RunStarted:
    """Start the pipeline. force=true re-reads every page and re-runs the review (costs API calls)."""
    pdf = _pdf(packet_id)
    if force:
        shutil.rmtree(config.CACHE_DIR / packet_id / "transcripts", ignore_errors=True)
        for f in (config.CACHE_DIR / packet_id).glob("review-*.json"):
            f.unlink()
        shutil.rmtree(config.CACHE_DIR / packet_id / "review-sections", ignore_errors=True)
    run = Run(run_id=uuid.uuid4().hex[:12], packet_id=packet_id)
    _runs[run.run_id] = run

    def emit(event: str, data: dict) -> None:
        with _lock:
            run.events.append({"event": event, "data": data})

    def work() -> None:
        run.status = "running"
        try:
            result = run_packet(pdf, emit=emit)
            emit("result", {"packet_id": packet_id, "bucket": result.recommendation.bucket})
            run.status = "done"
        except Exception as e:
            run.error = f"{type(e).__name__}: {e}"
            emit("error", {"packet_id": packet_id, "message": run.error})
            run.status = "failed"

    _executor.submit(work)
    return RunStarted(run_id=run.run_id, packet_id=packet_id, events_url=f"/runs/{run.run_id}/events",
                      result_url=f"/packets/{packet_id}/result")


@app.get("/runs/{run_id}")
def get_run(run_id: str) -> Run:
    if run_id not in _runs:
        raise HTTPException(404, "No such run")
    return _runs[run_id]


@app.get("/runs/{run_id}/events")
async def run_events(run_id: str) -> StreamingResponse:
    """Server-sent events: stage, page, halt, done, result, error. The stream ends after result/error."""
    if run_id not in _runs:
        raise HTTPException(404, "No such run")
    run = _runs[run_id]

    async def stream():
        sent = 0
        while True:
            events = run.events[sent:]
            for e in events:
                yield f"event: {e['event']}\ndata: {json.dumps(e['data'])}\n\n"
            sent += len(events)
            if run.status in ("done", "failed") and sent == len(run.events):
                return
            await asyncio.sleep(0.25)

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/packets/{packet_id}/result")
def get_result(packet_id: str) -> PacketResult:
    r = _result(packet_id)
    if r is None:
        raise HTTPException(404, f"{packet_id} has not been run")
    return r


@app.get("/packets/{packet_id}/pages/{page}")
def get_page_image(packet_id: str, page: int) -> FileResponse:
    """The page image as the pipeline read it (upright), for showing next to cited quotes."""
    _pdf(packet_id)
    base = page_dir(packet_id) / f"p{page:03d}.jpg"
    r = _result(packet_id)
    rotated = next((p.rotated_by_pipeline for p in r.pages if p.page == page), 0) if r else 0
    path = base.with_name(f"{base.stem}_r{rotated}.jpg") if rotated else base
    if not path.exists():
        raise HTTPException(404, "Page not rendered yet")
    return FileResponse(path, media_type="image/jpeg")


@app.get("/contract")
def contract() -> dict:
    return PacketResult.model_json_schema()
