# DEVLOG: Challenge 1 referral intake pipeline

Running notes so anyone (or a fresh Claude session) can pick up where we left off. Newest entry
on top. Keep entries short: what changed, what we decided, what's next.

## Current state (update this block each time)

- **Pipeline:** Python package in `pipeline/` (uv-managed, all deps in `pipeline/.venv`).
  Not yet run end to end against the API: waiting on API keys in `pipeline/.env`.
- **Integration point:** `pipeline/out/<packet>.json`, shaped by `PacketResult` in
  `pipeline/src/intake/schemas.py`. JSON Schema export: `pipeline/contract/packet-result.schema.json`.
  Teammate's Next.js + Supabase + eve app consumes this.
- **Next:** add keys → `uv run intake run R05` → `uv run intake run --all` → `uv run intake eval`.
- **Verified offline (no API):** render (R05, 14 pages in ~4 s), schema export, quote check,
  recommendation logic. An unverified "fails" goes to `needs_full_read`, not to deny.
- **Not yet verified:** any Claude or Jev call (no keys yet). First real run may surface
  schema/API errors; fix those first.

## How to run (from `pipeline/`)

```bash
cp .env.example .env          # add ANTHROPIC_API_KEY and TYPESAFE_API_KEY
uv sync                       # installs into pipeline/.venv only
uv run intake render R05      # no API calls; page images into .cache/
uv run intake run R05         # full pipeline on one packet → out/R05.json
uv run intake run --all       # all packets (results cached per page and per review)
uv run intake eval            # agreement with IHH decisions
uv run intake schema          # rewrite contract/packet-result.schema.json
```

Delete `.cache/<ID>/review.json` to re-run only the review after prompt changes.

## HTTP API (`uv run intake serve` → http://localhost:8000, OpenAPI at `/docs`)

No database in the pipeline. It is stateless apart from a file cache; the app (Supabase) owns
persistence. Run it on the demo laptop next to Next.js. CORS allows `localhost:3000`.

| Method | Path | What |
|---|---|---|
| GET | `/health` | `{ok, model}` |
| GET | `/packets` | packets on disk + latest bucket if run |
| POST | `/packets` (multipart `file`) | add an unseen packet (judge hand-off) |
| POST | `/packets/{id}/runs?force=false` | start a run → 202 `{run_id, events_url, result_url}` |
| GET | `/runs/{run_id}/events` | **SSE**: `stage`, `page`, `halt`, `done`, `result`, `error`; replays from start for late clients |
| GET | `/runs/{run_id}` | run status + all events so far |
| GET | `/packets/{id}/result` | full `PacketResult` JSON (the contract) |
| GET | `/packets/{id}/pages/{n}` | upright page JPEG, to show next to a cited quote |
| GET | `/contract` | JSON Schema of `PacketResult` |

Client flow: POST run → open `EventSource(events_url)` → on `result` event GET `result_url` →
write to Supabase from the Next.js side. An eve tool can do the same (POST, then poll `/runs/{id}`).

## Team and split

- Teammate: eve project, Next.js + Supabase full stack, agent templates, screens (a Claude
  artifact holds the UI mock to map onto real data).
- Data pipeline engineer (this log): packet ingestion → structured JSON for Supabase,
  accuracy, verification, eval.

## Decisions

| Decision | Why |
|---|---|
| Python + uv for the pipeline, JSON contract to the TS app | Better PDF tooling; deps live in the repo's `.venv`, nothing global |
| Claude reads page images as OCR (no Tesseract) | Crooked 200 dpi faxes, handwriting, sideways pages; we still keep a text layer for search, citations and Jev |
| `pypdfium2` renders pages | pip wheel, no poppler/system install |
| Opus 5.5 (`claude-opus-5-5`); effort low for transcription, high for review | Skill default model; effort is the cost/quality dial |
| Jev (TypeSafe) as a verifier, not the primary reader | Jev is weak on long state, numbers, dates; strong as a cheap calibrated check (SDE-cascade / citation-check cookbooks) |
| Code, not a model, makes the recommendation | Any failed must/exclusion → "likely deny, nurse review" (matches IHH's process: denials go to a nurse) |
| `decisions.json` read only by `intake eval` | CLAUDE.md: keep it out of the tool's sight while reviewing |
| `pipeline/.cache/` and `pipeline/out/` gitignored | They contain transcribed packet content; packets must never enter git |

## Pipeline steps

0. Ingest (`intake run <ID>`), packet read in place from `challenges/1-referral-intake/packets/`.
1. Render pages → `.cache/<ID>/pages/*.jpg`.
2. Transcribe each page with Claude (typed `PageReading`), auto-rotate and re-read sideways
   pages, flag un-redacted identifiers (pipeline halts the packet: tell an organizer).
3. Checklist DOC-1..10 from page types (code).
4–5. Rule review: one Claude call per packet, criteria JSON as cached system prompt, a finding
   per rule ID with page + exact quote, plus form-vs-chart contradictions.
6. Verify: (a) every quote fuzzy-matched on its cited page (code); (b) Jev Choice
   supports/contradicts/says_nothing per finding; (c) Jev Noul "is this unknown actually
   answered in the top pages?".
7. Recommend (code): `ready_to_accept | one_call_away | needs_full_read |
   likely_deny_nurse_review | halted_privacy`.
8. Eval (`intake eval`): compare to IHH decisions; deny ⇔ `likely_deny_nurse_review`.

## Open questions / risks

- Voice-agent demo calling real people conflicts with ground rule 2 (draft, don't send).
  Needs organizer sign-off; only with a teammate playing the social worker.
- Kipu / IHH systems: out of scope for the demo (no IHH systems).
- Hospital and contact names are redacted in packets; CRM data must be invented and labelled.
- Sending packet text to hosted Supabase may count as "posting" packets. Prefer local Supabase
  or keep transcripts local; confirm with an organizer.
- Packet text goes to Anthropic and TypeSafe APIs for processing. Confirm that's fine with organizers.
- Refusal fallbacks (`fallbacks: "default"`) not wired yet; refusals raise `RefusalError`.

## Log

### 2026-10-17 ~11:45: pipeline POC scaffolded

- Read challenge 1, criteria (155 IDs incl. by-system, DOC, FORM), judging, ground rules,
  team-context notes, TypeSafe docs (confidence, building guide, citation-check, SDE cascade,
  JS/Python SDK, images, Jev 1.13 jaggedness).
- Created `pipeline/` uv project (anthropic 1.15, typesafe-sdk 0.7.5, pypdfium2, pydantic,
  rapidfuzz). Modules: config, schemas, render, llm, transcribe, review, verify, decide,
  pipeline, cli, evaluate.
- Skills found via find-skills (not installed): `vercel/workflow@workflow`,
  `elevenlabs/skills@agents`; `anthropic-skills:pdf` already available.
