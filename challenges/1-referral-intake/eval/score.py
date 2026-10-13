#!/usr/bin/env python3
"""Score your packet reviews against the answer key.

    python3 score.py my-output/                # a folder of S01.json, S02.json, ...
    python3 score.py my-output/S05.json        # a single review
    python3 score.py my-output/ --key other-key.json

Each review is a JSON object shaped like example-output/S05.json. See output-schema.json.

What is scored, per packet:
  decision   your recommendation equals the key (approve / deny / needs_info)
  rules      of the rules that drive the decision (not_met or unknown in the key), the share you
             also flagged as not_met or unknown. The two are treated alike here, because "not
             arranged yet" can fairly be read either way
  evidence   of those matched rules, the share where one of your cited pages is a page the key cites
  docs       F1 between your missing_documents and the key's
  quotes     the share of your evidence quotes whose words appear, in order, on the page you
             cited. Anything under 1.00 means your tool quoted something the packet does not say there

The key is the organizers' reading of IHH's written criteria. IHH staff have the final word.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_reviews(path):
    p = Path(path)
    files = sorted(p.glob("*.json")) if p.is_dir() else [p]
    out = {}
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for r in data if isinstance(data, list) else [data]:
            if isinstance(r, dict) and r.get("packet_id"):
                out[r["packet_id"]] = r
    return out


def f1(pred, gold):
    pred, gold = set(pred), set(gold)
    if not pred and not gold:
        return 1.0
    hit = len(pred & gold)
    if hit == 0:
        return 0.0
    precision, recall = hit / len(pred), hit / len(gold)
    return 2 * precision * recall / (precision + recall)


def norm(text):
    text = text.lower().replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"[^a-z0-9%./:<>'-]+", " ", text).strip()


def on_page(quote, page):
    """True if the quote is on the page. A table cell that wraps is split across lines in the page
    text, so fall back to: every word of the quote appears on the page in the same order."""
    if quote in page:
        return True
    words = iter(page.split())
    return all(w in words for w in quote.split())


def quote_rate(review, packets_dir):
    """Share of evidence quotes found on the cited page of packets/<ID>/text/pNN.txt."""
    folder = Path(packets_dir) / str(review.get("packet_id")) / "text"
    if not folder.is_dir():
        return None, []
    found, total, bad = 0, 0, []
    for f in review.get("findings", []):
        for ev in f.get("evidence", []) if isinstance(f, dict) else []:
            quote, page = (ev or {}).get("quote"), (ev or {}).get("page")
            if not quote or not isinstance(page, int):
                continue
            total += 1
            page_file = folder / f"p{page:02d}.txt"
            if page_file.exists() and on_page(norm(quote), norm(page_file.read_text(encoding="utf-8"))):
                found += 1
            else:
                bad.append(f"{f.get('rule')} p{page}")
    return (found / total if total else None), bad


# The referral form restates some criteria in its own words. Flagging either one counts.
SAME_FACT = {"NEU-X5": ["FORM-X1"], "COG-2": ["FORM-M3"], "COG-1": ["FORM-M5"], "MOB-3": ["FORM-M6", "FORM-X3"],
             "MOB-1": ["FORM-X3"], "ADL-1": ["FORM-M4", "FORM-X2"], "GI-X3": ["FORM-X4"], "OTH-4": ["FORM-X4"],
             "MH-1": ["FORM-M2"], "OTH-1": ["FORM-X7"], "CARD-5": ["CIR-E7"], "CIR-E7": ["CARD-5"],
             "INT-E6": ["INT-E2"], "OTH-3": ["ID-3", "INT-E3"], "ID-3": ["OTH-3", "INT-E3"], "INT-E3": ["OTH-3", "ID-3"]}


def score_one(review, key):
    decision = review.get("recommendation") == key["decision"]
    mine = {f.get("rule"): f for f in review.get("findings", []) if isinstance(f, dict)}
    decisive = [f for f in key["findings"] if f["status"] != "met"]

    def flagged(rule):
        return any(mine.get(r, {}).get("status") in ("not_met", "unknown") for r in [rule] + SAME_FACT.get(rule, []))

    matched = [f for f in decisive if flagged(f["rule"])]
    rules = len(matched) / len(decisive) if decisive else None
    checkable = [f for f in matched if f["pages"]]
    cited = 0
    for f in checkable:
        pages = {e.get("page") for r in [f["rule"]] + SAME_FACT.get(f["rule"], [])
                 for e in mine.get(r, {}).get("evidence", []) if isinstance(e, dict)}
        cited += bool(pages & set(f["pages"]))
    evidence = cited / len(checkable) if checkable else None
    known = {d["rule"] for d in decisive} | {r for d in decisive for r in SAME_FACT.get(d["rule"], [])}
    extra = sorted(r for r, f in mine.items() if f.get("status") in ("not_met", "unknown") and r not in known)
    return {"decision": decision, "rules": rules, "evidence": evidence,
            "docs": f1(review.get("missing_documents", []), key["missing_documents"]),
            "missed": [f["rule"] for f in decisive if f not in matched], "extra": extra}


def fmt(x):
    return "  -  " if x is None else f"{x:5.2f}"


def main():
    ap = argparse.ArgumentParser(description="Score packet reviews against the answer key.")
    ap.add_argument("reviews", help="a review JSON file, or a folder of them")
    ap.add_argument("--key", default=str(HERE.parent / "answer-key" / "answer-key.json"))
    ap.add_argument("--packets", default=str(HERE.parent / "packets"), help="folder holding <ID>/text/ for the quote check")
    a = ap.parse_args()
    key = {p["packet_id"]: p for p in json.loads(Path(a.key).read_text(encoding="utf-8"))["packets"]}
    reviews = load_reviews(a.reviews)
    if not reviews:
        sys.exit("No reviews found. Each review needs a packet_id.")
    rows = []
    print(f"{'packet':7} {'key':10} {'yours':10} {'ok':3} {'rules':5} {'evid':5} {'docs':5} {'quote':5}  notes")
    for pid in sorted(reviews):
        if pid not in key:
            print(f"{pid:7} not in this answer key")
            continue
        s = score_one(reviews[pid], key[pid])
        s["quotes"], bad_quotes = quote_rate(reviews[pid], a.packets)
        rows.append(s)
        notes = []
        if bad_quotes:
            notes.append("quote not found: " + ", ".join(bad_quotes[:4]) + (" ..." if len(bad_quotes) > 4 else ""))
        if s["missed"]:
            notes.append("missed " + ", ".join(s["missed"]))
        if s["extra"]:
            notes.append("also flagged " + ", ".join(s["extra"]))
        print(f"{pid:7} {key[pid]['decision']:10} {str(reviews[pid].get('recommendation')):10} "
              f"{'yes' if s['decision'] else 'NO':3} {fmt(s['rules'])} {fmt(s['evidence'])} {fmt(s['docs'])} {fmt(s['quotes'])}  {'; '.join(notes)}")
    if rows:
        def avg(k):
            v = [r[k] for r in rows if r[k] is not None]
            return sum(v) / len(v) if v else None
        n = len(rows)
        print(f"\n{n} of {len(key)} packets reviewed. "
              f"Decisions right: {sum(r['decision'] for r in rows)}/{n}. "
              f"Rules {fmt(avg('rules')).strip()}, evidence {fmt(avg('evidence')).strip()}, docs {fmt(avg('docs')).strip()}, "
              f"quotes {fmt(avg('quotes')).strip()}.")
        print("'also flagged' rules are not counted against you. They may be fair points the key does not list.")


if __name__ == "__main__":
    main()
