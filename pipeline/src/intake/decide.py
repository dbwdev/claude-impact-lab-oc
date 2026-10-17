"""Steps 3 and 7: document checklist and the recommendation. Plain code, no model."""

from . import criteria
from .schemas import ChecklistItem, Page, PacketReview, Recommendation, VerificationFlag

# Which page types satisfy which checklist item. Items not listed are not checked automatically.
DOC_PAGE_TYPES = {
    "DOC-1": {"ihh_referral_form"},
    "DOC-2": {"face_sheet"},
    "DOC-3": {"health_plan_authorization"},
    "DOC-4": {"history_and_physical"},
    "DOC-5": {"progress_note"},
    "DOC-6": {"vitals", "nursing_note"},
    "DOC-7": {"medication_record"},
    "DOC-8": {"pt_evaluation", "ot_evaluation", "nursing_note"},
}

HARD_KINDS = {"must", "exclude", "conditional", "ineligible_condition"}
NEVER_AUTO_DENY = {"OTH-2"}


def checklist(pages: list[Page]) -> list[ChecklistItem]:
    out = []
    for r in criteria.rules().values():
        if r.group != "checklist":
            continue
        types = DOC_PAGE_TYPES.get(r.id)
        if types is None:
            out.append(ChecklistItem(doc_id=r.id, text=r.text, status="not_checked", pages=[]))
            continue
        hits = [p.page for p in pages if p.page_type in types]
        out.append(ChecklistItem(doc_id=r.id, text=r.text, status="found" if hits else "not_found", pages=hits))
    return out


def _label(rule_id: str, why: str) -> str:
    r = criteria.rules().get(rule_id)
    return f"{rule_id}: {why}" if r is None else f"{rule_id} ({r.text[:70]}): {why}"


def recommend(review: PacketReview, flags: list[VerificationFlag], docs: list[ChecklistItem]) -> Recommendation:
    table = criteria.rules()
    flagged = {fl.rule_id for fl in flags}
    hard_fails, unverified_fails, open_q, judgment, at_admission = [], [], [], [], []
    for f in review.findings + review.condition_findings:
        rule = table.get(f.rule_id)
        if rule is None or rule.superseded_by:
            continue
        hard = rule.kind in HARD_KINDS
        if f.status == "fails" and hard and f.rule_id not in NEVER_AUTO_DENY:
            # A fail whose evidence did not verify is not a confirmed fail.
            (unverified_fails if f.rule_id in flagged else hard_fails).append(_label(f.rule_id, f.reasoning))
        elif f.status == "needs_judgment" or (f.status == "fails" and f.rule_id in NEVER_AUTO_DENY):
            judgment.append(_label(f.rule_id, f.reasoning))
        elif (f.status == "unknown" and (hard or rule.kind == "document")) or (
            f.status == "fails" and rule.kind in ("document", "ask")
        ):
            # A missing document or unanswered question is something to request, not a denial.
            open_q.append(_label(f.rule_id, f.reasoning))
        elif f.status == "cant_tell_redacted" and hard:
            at_admission.append(_label(f.rule_id, f.reasoning))
    for d in docs:
        if d.status == "not_found":
            open_q.append(f"{d.doc_id}: {d.text} not found in packet")

    # Flags on rules that decide the outcome send the packet to a full read.
    decisive = {f.rule_id for f in review.findings + review.condition_findings
                if f.status in ("meets", "fails") and table.get(f.rule_id)
                and table[f.rule_id].kind in HARD_KINDS}
    serious = [fl for fl in flags if fl.rule_id in decisive or fl.check == "missing_rule"]

    if hard_fails:
        bucket, headline = "likely_deny_nurse_review", f"{len(hard_fails)} criteria not met. Nurse review before denying."
    elif serious or unverified_fails:
        bucket, headline = "needs_full_read", f"{len(serious)} findings failed verification. Read the cited pages."
        hard_fails = [f"UNVERIFIED {x}" for x in unverified_fails]
    elif open_q or judgment:
        bucket, headline = "one_call_away", f"No criteria failed. {len(open_q)} open questions, {len(judgment)} judgment calls."
    else:
        bucket, headline = "ready_to_accept", "Every checked criterion is met with cited evidence."
    return Recommendation(bucket=bucket, headline=headline, hard_fails=hard_fails, open_questions=open_q,
                          judgment_calls=judgment, confirm_at_admission=at_admission,
                          verification_flags=len(flags))
