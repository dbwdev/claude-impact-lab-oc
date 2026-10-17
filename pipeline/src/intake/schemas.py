"""The data contract. `intake schema` exports PacketResult as JSON Schema for the app side."""

from typing import Literal

from pydantic import BaseModel, Field

PageType = Literal[
    "fax_cover",
    "ihh_referral_form",
    "health_plan_authorization",
    "face_sheet",
    "history_and_physical",
    "progress_note",
    "nursing_note",
    "pt_evaluation",
    "ot_evaluation",
    "social_work_note",
    "psychiatry_or_consult_note",
    "wound_care_note",
    "medication_record",
    "labs",
    "vitals",
    "imaging",
    "cardiac_study",
    "physician_orders",
    "discharge_summary",
    "blank_or_near_blank",
    "other",
]


# ---- Step 2: one page, as read by Claude ----------------------------------------------------


class PageReading(BaseModel):
    """What Claude returns for a single page image."""

    rotate_clockwise_to_upright: Literal["0", "90", "180", "270"] = Field(
        description="Degrees to rotate the image clockwise so the main text reads upright."
    )
    page_type: PageType
    document_title: str = Field(description="Title printed on the page, or '' if none.")
    legibility: Literal["good", "partial", "poor"]
    transcript: str = Field(
        description="Faithful transcription. [REDACTED] for black boxes, [illegible] where unreadable."
    )
    handwriting_present: bool
    looks_like_prior_stay: bool = Field(
        description="True if the page appears to be from an earlier hospital stay than the referral."
    )
    possible_unredacted_identifier: bool = Field(
        description="True if a name, full date, phone, address, record number or similar is visible."
    )
    identifier_kinds: list[str] = Field(
        description="Kinds of identifier seen (e.g. 'patient name'). Never the value itself."
    )


class Page(PageReading):
    page: int = Field(description="1-based page number in the packet PDF.")
    rotated_by_pipeline: int = 0


# ---- Step 4/5: rule review --------------------------------------------------------------------

RuleStatus = Literal[
    "meets",  # no problem for eligibility (for an exclusion: the excluding condition is absent)
    "fails",  # a problem for eligibility (for an exclusion: the excluding condition is present)
    "unknown",  # the packet does not say
    "cant_tell_redacted",  # the answer depends on a blacked-out date or time
    "not_applicable",
    "needs_judgment",  # the written rules leave this to the coordinator
]


class Evidence(BaseModel):
    page: int
    quote: str = Field(description="Exact words copied from that page's transcript.")
    source: Literal["referral_form", "chart", "other"]


class RuleFinding(BaseModel):
    rule_id: str
    status: RuleStatus
    claim: str = Field(
        description="One plain factual sentence about the patient that the evidence should support. '' if unknown."
    )
    evidence: list[Evidence]
    reasoning: str
    confidence: Literal["high", "medium", "low"]


class Contradiction(BaseModel):
    topic: str
    first: Evidence
    second: Evidence
    why_it_matters: str


class PatientSummary(BaseModel):
    """Clinical facts only. No names, dates or identifiers."""

    age: str = Field(description="Age as stated, or 'unknown'.")
    sex: str = Field(description="As stated, or 'unknown'.")
    reason_for_hospitalization: str
    key_conditions: list[str]
    living_situation: str
    mobility_summary: str
    referral_form_present: bool


class SectionReview(BaseModel):
    """One parallel slice of the review (see review.SECTIONS)."""

    findings: list[RuleFinding]
    contradictions: list[Contradiction]
    questions_for_hospital: list[str]
    red_flags: list[str]


class PacketReview(BaseModel):
    patient: PatientSummary
    findings: list[RuleFinding] = Field(description="One per rule ID in the required list.")
    condition_findings: list[RuleFinding] = Field(
        description="By-body-system eligible/ineligible entries that match this patient's conditions."
    )
    contradictions: list[Contradiction]
    questions_for_hospital: list[str]
    red_flags: list[str]


# ---- Step 6: verification ---------------------------------------------------------------------


class VerificationFlag(BaseModel):
    rule_id: str
    check: Literal[
        "quote_not_found",
        "quote_on_other_page",
        "evidence_contradicts",
        "evidence_says_nothing",
        "low_verifier_confidence",
        "unknown_may_be_answered",
        "missing_rule",
        "verifier_unavailable",
    ]
    detail: str
    verifier_score: float | None = None


# ---- Step 7: recommendation -------------------------------------------------------------------

Bucket = Literal[
    "ready_to_accept",
    "one_call_away",
    "needs_full_read",
    "likely_deny_nurse_review",
    "halted_privacy",
]


class Recommendation(BaseModel):
    bucket: Bucket
    headline: str
    hard_fails: list[str]
    open_questions: list[str]
    judgment_calls: list[str]
    confirm_at_admission: list[str]
    verification_flags: int


class ChecklistItem(BaseModel):
    doc_id: str
    text: str
    status: Literal["found", "not_found", "not_checked"]
    pages: list[int]


class PacketResult(BaseModel):
    packet_id: str
    pipeline_version: str
    model: str
    page_count: int
    pages: list[Page]
    checklist: list[ChecklistItem]
    review: PacketReview | None
    verification: list[VerificationFlag]
    recommendation: Recommendation
    timings_s: dict[str, float]
    usage: dict[str, int]
