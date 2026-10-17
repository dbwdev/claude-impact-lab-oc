"""Step 6: catch the reviewer's mistakes.

a) code: each quote must appear on the page it cites (fuzzy, to tolerate OCR spacing)
b) Jev Choice: does the cited page support, contradict or say nothing about the claim?
c) Jev Noul: for an "unknown", do the most relevant pages actually answer the rule?
"""

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

from rapidfuzz import fuzz, process

from . import config, criteria
from .schemas import Page, PacketReview, RuleFinding, VerificationFlag

# Rule kinds where a wrong answer changes the recommendation.
STAKES = {"must", "exclude", "conditional", "eligible_condition", "ineligible_condition"}


def _norm(s: str) -> str:
    s = s.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def check_quotes(review: PacketReview, pages: list[Page]) -> list[VerificationFlag]:
    text = {p.page: _norm(p.transcript) for p in pages}
    flags = []
    for f in review.findings + review.condition_findings:
        for ev in f.evidence:
            q = _norm(ev.quote)
            if not q:
                continue
            score = fuzz.partial_ratio(q, text.get(ev.page, ""))
            if score >= config.QUOTE_MATCH_MIN:
                continue
            best = max(text.items(), key=lambda kv: fuzz.partial_ratio(q, kv[1]), default=None)
            if best and fuzz.partial_ratio(q, best[1]) >= config.QUOTE_MATCH_MIN:
                flags.append(VerificationFlag(
                    rule_id=f.rule_id, check="quote_on_other_page",
                    detail=f"Quote cited on p{ev.page} was found on p{best[0]}.",
                    verifier_score=score / 100))
            else:
                flags.append(VerificationFlag(
                    rule_id=f.rule_id, check="quote_not_found",
                    detail=f"Quote cited on p{ev.page} not found in the packet: {ev.quote[:80]!r}",
                    verifier_score=score / 100))
    return flags


def check_coverage(review: PacketReview) -> list[VerificationFlag]:
    seen = {f.rule_id for f in review.findings}
    table = criteria.rules()
    return [VerificationFlag(rule_id=rid, check="missing_rule", detail="Reviewer returned no finding.")
            for rid in criteria.required_ids() if rid not in seen and not table[rid].superseded_by]


# ---- Jev ----------------------------------------------------------------------------------------


def jev_enabled() -> bool:
    return bool(os.environ.get("TYPESAFE_API_KEY"))


def _ask(client, **kwargs):
    for attempt in range(3):
        try:
            return client.system_one(**kwargs)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1 + 2 * attempt)


def _support_check(client, f: RuleFinding, rule_text: str, pages: dict[int, Page]) -> list[VerificationFlag]:
    from typesafe_sdk import Choice

    cited = sorted({ev.page for ev in f.evidence if ev.page in pages})
    if not cited or not f.claim:
        return []
    state = {
        "rule": rule_text,
        "claim": f.claim,
        "pages": [{"page": n, "text": pages[n].transcript} for n in cited[:3]],
    }
    resp = _ask(client, 
        state=state,
        questions={
            "relation": Choice(
                instructions="How do the hospital chart pages in `pages` relate to `claim` about the patient?",
                criteria={
                    "supports": "The pages state the claim or directly imply it is true.",
                    "contradicts": "The pages state the opposite or imply the claim is false.",
                    "says_nothing": "The pages do not address the claim either way.",
                },
            )
        },
    )
    a = resp.choices["relation"]
    conf = getattr(a, "confidence", None)
    if a.choice == "contradicts":
        return [VerificationFlag(rule_id=f.rule_id, check="evidence_contradicts",
                                 detail=f"Cited pages appear to contradict: {f.claim}", verifier_score=conf)]
    if a.choice == "says_nothing":
        return [VerificationFlag(rule_id=f.rule_id, check="evidence_says_nothing",
                                 detail=f"Cited pages may not support: {f.claim}", verifier_score=conf)]
    if conf is not None and conf < config.JEV_AUTO_ACCEPT:
        return [VerificationFlag(rule_id=f.rule_id, check="low_verifier_confidence",
                                 detail=f"Support for '{f.claim}' is uncertain.", verifier_score=conf)]
    return []


def _absence_check(client, f: RuleFinding, rule_text: str, pages: list[Page]) -> list[VerificationFlag]:
    from typesafe_sdk import Noul

    top = process.extract(rule_text, {p.page: p.transcript for p in pages},
                          scorer=fuzz.token_set_ratio, limit=3)
    state = {"rule": rule_text,
             "pages": [{"page": key, "text": pages[key - 1].transcript} for _, _, key in top]}
    resp = _ask(client, 
        state=state,
        questions={
            "answered": Noul(instructions=(
                "Do the chart pages in `pages` contain information that shows whether the patient "
                "meets or fails `rule`?"))
        },
    )
    p = resp.nouls["answered"].noul
    if p > config.JEV_FLAG:
        return [VerificationFlag(rule_id=f.rule_id, check="unknown_may_be_answered",
                                 detail=f"Marked unknown, but pages {[k for _, _, k in top]} may answer it.",
                                 verifier_score=p)]
    return []


def jev_checks(review: PacketReview, pages: list[Page]) -> list[VerificationFlag]:
    from typesafe_sdk import TypeSafeClient

    table = criteria.rules()
    by_no = {p.page: p for p in pages}
    jobs = []
    for f in review.findings + review.condition_findings:
        rule = table.get(f.rule_id)
        if rule is None or rule.kind not in STAKES:
            continue
        if f.status in ("meets", "fails"):
            jobs.append(("support", f, rule.text))
        elif f.status == "unknown":
            jobs.append(("absence", f, rule.text))
    flags: list[VerificationFlag] = []
    errors: list[str] = []
    with TypeSafeClient() as client, ThreadPoolExecutor(4) as pool:
        futures = [
            pool.submit(_support_check, client, f, t, by_no) if kind == "support"
            else pool.submit(_absence_check, client, f, t, pages)
            for kind, f, t in jobs
        ]
        for fut in futures:
            try:
                flags.extend(fut.result())
            except Exception as e:  # a verifier outage must not hide the review
                errors.append(f"{type(e).__name__}: {e}")
    if errors:
        flags.append(VerificationFlag(rule_id="*", check="verifier_unavailable",
                                      detail=f"{len(errors)}/{len(jobs)} Jev checks failed; first: {errors[0]}"))
    return flags


def verify(review: PacketReview, pages: list[Page]) -> list[VerificationFlag]:
    flags = check_coverage(review) + check_quotes(review, pages)
    if jev_enabled():
        flags += jev_checks(review, pages)
    return flags
