"""Steps 4–5: Claude checks the transcribed packet against every rule, with page-cited quotes."""

import json

from . import config, criteria, llm
from .schemas import PacketReview, Page
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

Output:
- findings: exactly one entry for each rule ID in the required list, in that order.
- condition_findings: the by_system eligible/ineligible entries that match this patient's \
conditions (skip the ones that don't apply).
- questions_for_hospital: specific questions that would resolve unknowns, one per item.
- red_flags: anything a coordinator must see first.
- patient: clinical facts only. No names, dates, facilities or identifiers."""


def _system() -> list[dict]:
    body = (
        INSTRUCTIONS
        + "\n\n<admission_criteria>\n"
        + json.dumps(criteria.raw(), indent=1)
        + "\n</admission_criteria>\n\n<required_rule_ids>\n"
        + ", ".join(criteria.required_ids())
        + "\n</required_rule_ids>"
    )
    # Same prefix for every packet, so it is cached after the first call.
    return [{"type": "text", "text": body, "cache_control": {"type": "ephemeral"}}]


def review_packet(packet_id: str, pages: list[Page]) -> PacketReview:
    cache = config.CACHE_DIR / packet_id / "review.json"
    if cache.exists():
        return PacketReview.model_validate_json(cache.read_text())
    text = f"<packet pages=\"{len(pages)}\">\n{pages_as_text(pages)}\n</packet>"
    review = llm.parse(
        output=PacketReview,
        system=_system(),
        content=[{"type": "text", "text": text}],
        effort=config.REVIEW_EFFORT,
        max_tokens=64000,
    )
    cache.write_text(review.model_dump_json(indent=1))
    return review
