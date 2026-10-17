"""Compares pipeline output to IHH's real decisions. The only module that reads decisions.json."""

import json

from . import config
from .schemas import PacketResult


def evaluate() -> int:
    truth = {p["packet_id"]: p["decision"] for p in json.loads(config.DECISIONS_PATH.read_text())["packets"]}
    rows, correct, scored = [], 0, 0
    for pid in sorted(truth):
        path = config.OUT_DIR / f"{pid}.json"
        if not path.exists():
            rows.append((pid, truth[pid], "-", "not run", ""))
            continue
        r = PacketResult.model_validate_json(path.read_text())
        rec = r.recommendation
        if rec.bucket == "halted_privacy":
            rows.append((pid, truth[pid], "-", rec.bucket, rec.headline))
            continue
        predicted = "deny" if rec.bucket == "likely_deny_nurse_review" else "approve"
        actual = "approve" if truth[pid].lower().startswith("approv") else "deny"
        ok = predicted == actual
        scored += 1
        correct += ok
        top = (rec.hard_fails or rec.judgment_calls or rec.open_questions or [""])[0]
        rows.append((pid, truth[pid], predicted, ("✓ " if ok else "✗ ") + rec.bucket, top[:90]))

    print(f"{'packet':7} {'IHH':9} {'pipeline':9} {'bucket':28} first reason")
    for pid, t, p, b, why in rows:
        print(f"{pid:7} {t:9} {p:9} {b:28} {why}")
    if scored:
        print(f"\nAgreement with IHH: {correct}/{scored}")
        print("(predicted deny = bucket likely_deny_nurse_review; every other bucket counts as approve)")
    return 0
