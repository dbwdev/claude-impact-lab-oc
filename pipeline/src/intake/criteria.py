"""Loads IHH's criteria JSON into a flat id → rule table."""

import json
from dataclasses import dataclass
from functools import cache

from . import config


@dataclass(frozen=True)
class Rule:
    id: str
    text: str
    kind: str  # must | exclude | document | conditional | ask | note | any_of | eligible_condition | ineligible_condition
    group: str  # general | rules | by_system | checklist | form
    superseded_by: str | None = None


@cache
def raw() -> dict:
    return json.loads(config.CRITERIA_PATH.read_text())


@cache
def rules() -> dict[str, Rule]:
    d = raw()
    out: dict[str, Rule] = {}
    for r in d["general"]["any_of"]:
        out[r["id"]] = Rule(r["id"], r["text"], "any_of", "general")
    for r in d["rules"]:
        out[r["id"]] = Rule(r["id"], r["text"], r["kind"], "rules")
    for system in d["by_system"]:
        for r in system.get("eligible", []):
            out[r["id"]] = Rule(r["id"], r["text"], "eligible_condition", "by_system")
        for r in system.get("ineligible", []):
            out[r["id"]] = Rule(r["id"], r["text"], "ineligible_condition", "by_system")
    for r in d["referral_checklist"]["items"]:
        out[r["id"]] = Rule(r["id"], r["text"], "document", "checklist")
    form = d["referral_form_screen"]
    for r in form["must_meet_all"]:
        out[r["id"]] = Rule(r["id"], r["text"], "must", "form", r.get("superseded_by"))
    for r in form["not_eligible_if"]:
        out[r["id"]] = Rule(r["id"], r["text"], "exclude", "form", r.get("superseded_by"))
    return out


def required_ids() -> list[str]:
    """Rules the review must answer for every packet. By-system and checklist rules are separate."""
    return [r.id for r in rules().values() if r.group in ("general", "rules", "form")]
