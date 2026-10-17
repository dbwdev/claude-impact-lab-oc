# Referral intake pipeline

Reads an IHH recuperative care referral packet (an image-only faxed PDF), checks it against
IHH's admission criteria, verifies its own findings, and returns one JSON result a coordinator
can review. It recommends; a person decides.

```
PDF → page images → Claude reads each page → Claude reviews every rule with page-cited quotes
    → verify (quote match in code + Jev checks) → recommendation bucket (plain code) → JSON
```

## Setup

You need [uv](https://docs.astral.sh/uv/). It installs Python and every dependency into
`pipeline/.venv`; nothing else goes on your machine.

```bash
# install uv once, if `uv --version` fails
curl -LsSf https://astral.sh/uv/install.sh | sh     # or: brew install uv

cd pipeline
uv sync                     # creates .venv with Python 3.12 and all deps
cp .env.example .env        # then paste your keys into .env (it is gitignored)
```

`.env` needs:

| Variable | Used for |
|---|---|
| `ANTHROPIC_API_KEY` | Page reading and rule review (Claude Opus 5.5) |
| `TYPESAFE_API_KEY` | Verification checks (Jev). Without it the pipeline still runs; those checks are skipped |

The packets are not in git. Download them as described in
[`../challenges/1-referral-intake/packets/README.md`](../challenges/1-referral-intake/packets/README.md)
so the folder holds `R01.pdf` … `R11.pdf`. The pipeline reads them in place.

## Use

```bash
uv run intake render R05      # page images only, no API calls (quick sanity check)
uv run intake run R05         # one packet → out/R05.json  (~1.5 min, ~$1.50)
uv run intake run --all       # every packet in the folder
uv run intake eval            # compare out/*.json with IHH's real decisions
uv run intake serve           # HTTP API on http://127.0.0.1:8000, docs at /docs
uv run intake schema          # rewrite contract/packet-result.schema.json
```

Results are cached per page and per review in `.cache/`, so a rerun or a retry after a network
error resumes where it stopped. To redo a packet from scratch, delete `.cache/<ID>/` (or call the
API with `force=true`). To redo only the review after a prompt change, delete
`.cache/<ID>/review-*.json`.

Settings (all optional, in `.env`): `INTAKE_MODEL`, `INTAKE_TRANSCRIBE_EFFORT` (default `low`),
`INTAKE_REVIEW_EFFORT` (`high`), `INTAKE_REVIEW_MODE` (`sectioned` = 6 parallel calls, or
`single`), `INTAKE_PAGE_WORKERS` (`32`), `INTAKE_PACKETS_DIR`,
`INTAKE_JEV_AUTO_ACCEPT` (`0.8`), `INTAKE_JEV_FLAG` (`0.7`), `INTAKE_QUOTE_MATCH_MIN` (`88`).

## What is where

| Path | What |
|---|---|
| `src/intake/render.py` | PDF → upright JPEG per page (pypdfium2) |
| `src/intake/transcribe.py` | Claude reads one page: type, transcript, rotation, identifier check |
| `src/intake/review.py` | Claude checks the packet against every rule ID, with quotes |
| `src/intake/verify.py` | Quote match (code) and Jev support / absence checks |
| `src/intake/decide.py` | Document checklist and recommendation bucket (no model) |
| `src/intake/server.py` | FastAPI + server-sent events |
| `src/intake/evaluate.py` | The only code that reads `eval/decisions.json` |
| `contract/packet-result.schema.json` | JSON Schema of the output |
| `.cache/`, `out/` | Packet-derived content. Gitignored. Never commit or upload |

Integration details for the app side: [HANDOFF.md](HANDOFF.md).

## Where it gets things wrong

**Agreement with IHH's real decisions: 9 of 11** (`uv run intake eval`). Treat that as
optimistic: it was 7/11 until one prompt change (judge the patient's status at discharge, not
during the stay) that we made after seeing which packets it missed. Eleven packets are a small
sample, and a judge's unseen packet is the honest test.

The two it still misses:

| Packet | IHH | Pipeline | What happened |
|---|---|---|---|
| R03 | approved | likely deny → nurse review | The chart does not meet a written cardiac threshold (CARD-5), and orientation is not documented as x4 (COG-2). Either IHH used discretion beyond the written rule or the tool is too literal. A question for IHH staff |
| R05 | denied | one call away | A psychiatric-only admission. The tool raised it as judgment calls ("too ill or frail?", GEN-1; violence history, OTH-1/FORM-X7) instead of denying, because the written rules don't exclude it outright |

Known weaknesses:

- **Lots of "unknown".** Missing evidence becomes "unknown" plus a question for the hospital, by
  design. Packets come back with 14–23 open questions; some are answered somewhere in the packet.
  Jev flags those (`unknown_may_be_answered`), but nothing re-checks them automatically yet.
- **The transcript is AI output too.** Handwriting, faint faxes and sideways tables can be
  misread. Quotes are checked against our transcript, not the image, so the UI must show the page
  image next to every quote.
- **Findings vary between runs.** With the same prompt, the one-call and six-call reviews gave
  the same approve/deny on all 11 packets, but individual rule findings (e.g. "meets" vs
  "unknown") change from run to run.
- **Dates are blacked out**, so any rule with a time window (insulin within 24 h, 72 h after
  alcohol, a swab within 24 h) is `cant_tell_redacted`.
- **Adult criteria only.** The children's criteria aren't implemented.
- **Body-system rules** (e.g. GI, neurology) are only checked for the conditions the review
  notices; a condition it misses gets no rule check.
- **The verifier's thresholds are cookbook defaults** (0.8 / 0.7 / 0.5), not tuned for medical
  charts.
- **Untested** on packets over 34 pages or on referral forms other than IHH's.

What we would not trust it with: making the decision, sending a denial without a nurse's
review, or any finding nobody checked against the cited page.

## Privacy

Packet images, transcripts and results stay on the machine running the pipeline. Pages are sent
to the Anthropic API and transcript text to the TypeSafe API for processing. If a page shows an
identifier the redaction missed, the pipeline stops that packet with `halted_privacy`: tell an
organizer.
