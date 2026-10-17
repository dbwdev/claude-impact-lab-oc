"""uv run intake run R05 | run --all | eval | schema | render R05"""

import argparse
import json
import sys
from pathlib import Path

from . import config


def main() -> int:
    ap = argparse.ArgumentParser(prog="intake")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="run the pipeline on packets")
    run.add_argument("packets", nargs="*", help="packet IDs like R05, or paths to PDFs")
    run.add_argument("--all", action="store_true")
    ren = sub.add_parser("render", help="only render page images (no API calls)")
    ren.add_argument("packets", nargs="+")
    sub.add_parser("eval", help="compare out/*.json to IHH decisions")
    sub.add_parser("schema", help="write the JSON Schema contract")
    args = ap.parse_args()

    if args.cmd == "schema":
        from .schemas import PacketResult

        path = config.PIPELINE_DIR / "contract" / "packet-result.schema.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(PacketResult.model_json_schema(), indent=2))
        print(path)
        return 0
    if args.cmd == "eval":
        from .evaluate import evaluate

        return evaluate()

    names = sorted(p.stem for p in config.PACKETS_DIR.glob("*.pdf")) if getattr(args, "all", False) else args.packets
    pdfs = [config.PACKETS_DIR / f"{n}.pdf" if not n.endswith(".pdf") else Path(n) for n in names]
    missing = [p for p in pdfs if not p.exists()]
    if missing:
        print(f"Missing packets: {missing}. Download them into {config.PACKETS_DIR}.", file=sys.stderr)
        return 1

    if args.cmd == "render":
        from .render import render_packet

        for pdf in pdfs:
            print(pdf.stem, len(render_packet(pdf, pdf.stem)), "pages")
        return 0

    from .pipeline import run_packet

    failed = []
    for pdf in pdfs:
        try:
            run_packet(pdf)
        except Exception as e:
            print(f"[{pdf.stem}] FAILED: {type(e).__name__}: {e}", file=sys.stderr)
            failed.append(pdf.stem)
    from . import llm

    print(f"usage: {llm.usage}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
