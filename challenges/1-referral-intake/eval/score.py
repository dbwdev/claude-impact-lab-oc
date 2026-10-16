#!/usr/bin/env python3
"""Check your packet reviews against IHH's real decisions.

    python3 score.py my-output/            # a folder of R01.json, R02.json, ...
    python3 score.py my-output/R01.json    # a single review

Each review is a JSON object shaped like output-schema.json. Only the recommendation is scored.
IHH never recorded its reasons, so the findings are for the coordinator, and IHH staff, to judge.
A needs_info answer is counted separately: it is not wrong, but it is not a decision either.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEY = {p["packet_id"]: p["decision"] for p in json.loads((HERE / "decisions.json").read_text())["packets"]}


def load(path):
    p = Path(path)
    out = {}
    for f in sorted(p.glob("*.json")) if p.is_dir() else [p]:
        data = json.loads(f.read_text(encoding="utf-8"))
        for r in data if isinstance(data, list) else [data]:
            if isinstance(r, dict) and r.get("packet_id") in KEY:
                out[r["packet_id"]] = r
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    reviews = load(sys.argv[1])
    if not reviews:
        sys.exit("No reviews found for R01 to R11.")
    right = asked = 0
    for pid, r in sorted(reviews.items()):
        rec, ihh = r.get("recommendation"), KEY[pid]
        mark = "asks for more" if rec == "needs_info" else ("match" if rec == ihh else "differs")
        right += rec == ihh
        asked += rec == "needs_info"
        print(f"{pid}  yours: {rec or '-':<10} IHH: {ihh:<8} {mark}")
    n = len(reviews)
    print(f"\n{n} of {len(KEY)} packets reviewed. Matches IHH: {right}/{n}. Asked for more: {asked}.")
    print("Where you differ, show the coordinator your evidence. IHH staff have the final word.")


if __name__ == "__main__":
    main()
