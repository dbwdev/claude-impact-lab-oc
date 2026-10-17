"""Steps 4–5: Claude checks the transcribed packet against every rule, with page-cited quotes."""

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from . import config, criteria, llm
from .schemas import PacketReview, Page, SectionReview
from .transcribe import pages_as_text

INSTRUCTIONS = """You are helping a recuperative care referral coordinator at Illumination Health + \
Home (IHH) review a hospital referral packet against IHH's admission criteria (below). You \
prepare the review; a person makes the decision.

How to judge:
- Check the chart, not only the referral form. The form is one person's summary and can be \
wrong. When the form and the chart disagree, record a contradiction and judge on the chart.
- A result that is not in the packet is "unknown", never assumed normal.
- Dates are blacked out. A rule that needs a date, a time window or a count of hours (24 hours \
on insulin, 72 hours after alcohol, a swab within 24 hours) is "cant_tell_redacted" unless the \
packet states the interval in words.
- [REDACTED] marks a privacy redaction, not a missing document or a finding.
- Pages marked prior_stay may describe an earlier admission; say so if you rely on one.
- Precedence: the admission criteria outline wins over the referral form (FORM-*). Rules with \
superseded_by are judged by the superseding rule; mark the FORM rule "not_applicable" when the \
superseding rule covers it. Where the outline is silent (tuberculosis, refusing detox) the \
form's exclusion applies.
- OTH-2 (sex offender) is case by case: never "fails"; use "needs_judgment" if it applies.
- Use "needs_judgment" where the written rules leave the call to the coordinator.

Status meaning (always relative to eligibility):
- meets: no problem. For an exclusion, the excluding condition is absent (with evidence).
- fails: a problem. For an exclusion, the excluding condition is present.
- unknown / cant_tell_redacted / not_applicable / needs_judgment as above.
For "document" rules: meets = the document is in the packet.
For "ask" rules: meets = the packet answers the question.
GEN-1..3 are any-of: judge each separately.

Evidence:
- Every quote must be copied exactly, word for word, from the transcript of the page you cite \
(short quotes, under 30 words). Never paraphrase inside a quote. Never cite a page you did not \
read. If you have no evidence, give an empty list.
- claim is one plain factual sentence about the patient that your evidence supports, phrased \
positively (e.g. "The patient walked 150 feet with a front-wheeled walker."). Empty if unknown.

Output (the task at the end of the packet says which rules this call covers):
- findings: exactly one entry for each rule ID the task lists, in that order.
- condition_findings: only when the task asks for them: the by_system eligible/ineligible \
entries that match this patient's conditions (skip the ones that don't apply).
- contradictions, questions_for_hospital and red_flags: about the task's rules, plus anything \
the task asks for.
- questions_for_hospital: specific questions that would resolve unknowns, one per item.
- red_flags: anything a coordinator must see first.
- patient: clinical facts only. No names, dates, facilities or identifiers."""


def _system() -> list[dict]:
    body = INSTRUCTIONS + "\n\n<admission_criteria>\n" + json.dumps(criteria.raw(), indent=1) + "\n</admission_criteria>"
    # Same for every packet and every section, so it is cached after the first call.
    return [{"type": "text", "text": body, "cache_control": {"type": "ephemeral"}}]


# Parallel review sections, by rule ID prefix or exact ID. Anything unmatched goes to "overview",
# which also produces the patient summary, condition findings and cross-cutting contradictions.
SECTIONS: dict[str, tuple[str, ...]] = {
    "function": ("ADL-", "MOB-", "COG-", "FORM-M3", "FORM-M4", "FORM-M5", "FORM-M6",
                 "FORM-X1", "FORM-X2", "FORM-X3"),
    "mental_health_behavior": ("MH-", "OTH-1", "OTH-2", "FORM-X5", "FORM-X6", "FORM-X7"),
    "infection_lines_eol": ("INF-", "ID-", "OTH-3", "OTH-4", "EOL-", "FORM-X4"),
    "diabetes": ("DM-",),
    "respiratory_cardiac": ("RESP-", "CARD-"),
}


def section_ids() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {name: [] for name in [*SECTIONS, "overview"]}
    for rid in criteria.required_ids():
        name = next((n for n, keys in SECTIONS.items()
                     if any(rid == k or (k.endswith("-") and rid.startswith(k)) for k in keys)), "overview")
        out[name].append(rid)
    return out


def _task(ids: list[str], overview: bool) -> str:
    text = f"<task>\nReview these rule IDs only: {', '.join(ids)}.\n"
    if overview:
        text += ("Also fill in the patient summary and condition_findings, and list contradictions "
                 "between the referral form and the chart on any topic.\n")
    return text + "</task>"


def _packet_block(pages: list[Page]) -> dict:
    text = f"<packet pages=\"{len(pages)}\">\n{pages_as_text(pages)}\n</packet>"
    # Cached so the parallel section calls share it.
    return {"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}


def _review_single(pages: list[Page]) -> PacketReview:
    return llm.parse(output=PacketReview, system=_system(),
                     content=[_packet_block(pages), {"type": "text", "text": _task(criteria.required_ids(), True)}],
                     effort=config.REVIEW_EFFORT, max_tokens=64000)


def _review_sectioned(pages: list[Page], on_section=None) -> PacketReview:
    sections = section_ids()
    packet = _packet_block(pages)
    primed = threading.Event()

    t0 = time.monotonic()

    def run(name: str, ids: list[str]):
        overview = name == "overview"
        if not overview:
            # Start after the overview call has processed (and cached) the shared prompt.
            primed.wait(timeout=20)
        result = llm.parse(output=PacketReview if overview else SectionReview, system=_system(),
                           content=[packet, {"type": "text", "text": _task(ids, overview)}],
                           effort=config.REVIEW_EFFORT, max_tokens=32000,
                           on_start=primed.set if overview else None)
        if on_section:
            on_section(name, result, round(time.monotonic() - t0, 1))
        return name, result

    with ThreadPoolExecutor(len(sections)) as pool:
        parts = dict(f.result() for f in [pool.submit(run, n, ids) for n, ids in sections.items()])
    overview: PacketReview = parts.pop("overview")
    order = {rid: i for i, rid in enumerate(criteria.required_ids())}
    findings = overview.findings + [f for part in parts.values() for f in part.findings]
    questions = overview.questions_for_hospital + [q for p in parts.values() for q in p.questions_for_hospital]
    return PacketReview(
        patient=overview.patient,
        findings=sorted(findings, key=lambda f: order.get(f.rule_id, len(order))),
        condition_findings=overview.condition_findings,
        contradictions=overview.contradictions + [c for p in parts.values() for c in p.contradictions],
        questions_for_hospital=list(dict.fromkeys(questions)),
        red_flags=overview.red_flags + [r for p in parts.values() for r in p.red_flags],
    )


def review_packet(packet_id: str, pages: list[Page], on_section=None) -> PacketReview:
    cache = config.CACHE_DIR / packet_id / f"review-{config.REVIEW_MODE}.json"
    if cache.exists():
        return PacketReview.model_validate_json(cache.read_text())
    if config.REVIEW_MODE == "sectioned":
        review = _review_sectioned(pages, on_section)
    else:
        review = _review_single(pages)
    cache.write_text(review.model_dump_json(indent=1))
    return review
