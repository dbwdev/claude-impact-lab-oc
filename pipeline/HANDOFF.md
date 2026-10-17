# Handoff: integrating the intake pipeline

For the app side (Next.js + Supabase + eve). The pipeline is a local Python service; your app
talks to it over HTTP and owns all persistence. Setup is in [README.md](README.md).

## TL;DR

```bash
cd pipeline && uv sync && cp .env.example .env   # add your ANTHROPIC_API_KEY and TYPESAFE_API_KEY
uv run intake serve                               # http://127.0.0.1:8000  (OpenAPI UI at /docs)
```

1. `POST /packets/R05/runs` → `{run_id, events_url, result_url}`
2. Open `events_url` as an `EventSource`; show progress as `page` events arrive
3. On the `result` event, `GET result_url` → a `PacketResult` JSON; write it to Supabase

The pipeline keeps no database. Runs live in memory (lost on restart); results are files in
`pipeline/out/<ID>.json` and survive restarts, so `GET /packets/{id}/result` keeps working.

## Endpoints

| Method | Path | Request | Response |
|---|---|---|---|
| GET | `/health` | | `{ok: true, model}` |
| GET | `/packets` | | `PacketInfo[]`: `{packet_id, has_result, bucket, headline}` |
| POST | `/packets` | multipart, field `file` = PDF | `201 PacketInfo` (id = sanitized filename) |
| POST | `/packets/{id}/runs` | query `force` (bool, default false) | `202 {run_id, packet_id, events_url, result_url}` |
| GET | `/runs/{run_id}/events` | | `text/event-stream` (below) |
| GET | `/runs/{run_id}` | | `{run_id, packet_id, status, error, events[]}`; status = `queued \| running \| done \| failed` |
| GET | `/packets/{id}/result` | | `PacketResult` or 404 if never run |
| GET | `/packets/{id}/pages/{n}` | n is 1-based | upright page JPEG |
| GET | `/contract` | | JSON Schema of `PacketResult` |

```bash
curl -X POST localhost:8000/packets/R05/runs
curl -N localhost:8000/runs/<run_id>/events
curl localhost:8000/packets/R05/result | jq .recommendation
curl -F file=@/path/to/new-packet.pdf localhost:8000/packets
```

## Streaming events (SSE)

The stream replays from the first event, so connecting late is fine. It closes after `result` or
`error`. Every `data` is JSON and includes `packet_id`.

| event | data | When |
|---|---|---|
| `stage` | `{stage, status: "started"\|"finished", seconds?, message}` | stage = `render`, `transcribe`, `review`, `verify` |
| `page` | `{page, total, page_type, legibility, rotated}` | each page as it is read (any order) |
| `halt` | `{pages, message}` | possible unredacted identifier: stop, tell an organizer |
| `done` | `{bucket, message}` | result written |
| `result` | `{bucket}` | last event on success: now fetch `result_url` |
| `error` | `{message}` | last event on failure (usually network: just start the run again; it resumes from cache) |

Typical timing for a 14–34 page packet: transcribe 20–60 s, review ~2 min, verify ~2–10 s.
The review stage shows no progress for those ~2 minutes; show a spinner there.

```ts
const run = await fetch(`${API}/packets/${id}/runs`, { method: "POST" }).then(r => r.json());
const es = new EventSource(`${API}${run.events_url}`);
es.addEventListener("page", e => setPages(p => [...p, JSON.parse(e.data)]));
es.addEventListener("stage", e => setStage(JSON.parse(e.data)));
es.addEventListener("halt", e => showPrivacyStop(JSON.parse(e.data)));
es.addEventListener("result", async () => {
  es.close();
  const result: PacketResult = await fetch(`${API}${run.result_url}`).then(r => r.json());
  await saveToSupabase(result);
});
es.addEventListener("error", () => es.close()); // fires for our `error` event and for dropped connections
```

TypeScript types from the contract:

```bash
npx json-schema-to-typescript pipeline/contract/packet-result.schema.json > src/types/packet-result.ts
```

## The result (`PacketResult`)

Full schema: [`contract/packet-result.schema.json`](contract/packet-result.schema.json). The parts
the screens need:

```text
packet_id, page_count, model, pipeline_version, timings_s, usage
recommendation
  bucket            ready_to_accept | one_call_away | needs_full_read | likely_deny_nurse_review | halted_privacy
  headline          one line for the queue
  hard_fails[]      criteria not met (strings "RULE-ID (rule text): why")
  open_questions[]  unknowns + missing documents → what to ask the hospital
  judgment_calls[]  rules the written criteria leave to the coordinator
  confirm_at_admission[]  rules that depend on a blacked-out date/time
  verification_flags  count
review
  patient           age, sex, reason_for_hospitalization, key_conditions[], living_situation,
                    mobility_summary, referral_form_present   (clinical only, no identifiers)
  findings[]        one per rule ID: {rule_id, status, claim, evidence[{page, quote, source}], reasoning, confidence}
  condition_findings[]  body-system rules that match this patient, same shape
  contradictions[]  {topic, first{page,quote,source}, second{...}, why_it_matters}
  questions_for_hospital[]   ready-to-send questions (draft only, never auto-send)
  red_flags[]
verification[]      {rule_id, check, detail, verifier_score}
checklist[]         {doc_id, text, status: found|not_found|not_checked, pages[]}
pages[]             {page, page_type, legibility, transcript, rotated_by_pipeline, ...}
```

**Finding status** is always relative to eligibility: `meets` = no problem (for an exclusion
rule, the excluding condition is absent), `fails` = a problem, `unknown` = the packet does not
say, `cant_tell_redacted` = depends on a blacked-out date, `not_applicable`, `needs_judgment`.
Rule text for an ID is in `challenges/1-referral-intake/criteria/admission-criteria.json`.

**Bucket** is computed by plain code in `src/intake/decide.py`, not by a model:
- `likely_deny_nurse_review`: a must/exclusion rule failed and its evidence verified. IHH sends denials to a nurse, so this is the hand-off to them, not a denial.
- `needs_full_read`: a decisive finding failed verification (quote not found, Jev says the page doesn't support it, etc.). Fails that didn't verify show as `UNVERIFIED …` in `hard_fails`.
- `one_call_away`: nothing failed; open questions or judgment calls remain.
- `ready_to_accept`: every checked criterion met with cited evidence.

**Verification checks**: `quote_not_found`, `quote_on_other_page`, `evidence_contradicts`,
`evidence_says_nothing`, `low_verifier_confidence`, `unknown_may_be_answered`, `missing_rule`,
`verifier_unavailable` (Jev unreachable; the result is still valid, just less checked).

## Suggested Supabase tables

One table per list keeps the screens simple; `result_json` keeps everything else.

| Table | Columns |
|---|---|
| `packet_runs` | `packet_id`, `bucket`, `headline`, `page_count`, `model`, `pipeline_version`, `created_at`, `result_json jsonb` |
| `findings` | `packet_id`, `rule_id`, `status`, `claim`, `reasoning`, `confidence`, `evidence jsonb`, `is_condition bool` |
| `verification_flags` | `packet_id`, `rule_id`, `check`, `detail`, `verifier_score` |
| `hospital_questions` | `packet_id`, `question`, `status` (draft / asked / answered), owned by your app |

## eve

Wrap the API as one tool, e.g. `review_referral({packet_id})`: POST the run, poll
`GET /runs/{id}` every few seconds until `done`/`failed` (or consume SSE), then return
`recommendation` plus `questions_for_hospital`. Keep the full result out of the agent's context;
it is large. The agent drafts messages; it never sends them (event ground rule 2).

## Watch out for

- **Privacy.** `result.pages[].transcript` and every `quote` are packet content. Keep them on the
  demo laptop: local Supabase is safest. Ask an organizer before putting them in a hosted
  database. Never commit `pipeline/out/` or `pipeline/.cache/`.
- **Show the source.** Next to every quote, show `/packets/{id}/pages/{page}` so the coordinator
  checks the actual fax, not our transcript (the transcript is AI output too).
- **Unknown is not normal.** Render `unknown` and `cant_tell_redacted` visibly; never as a pass.
- **A recommendation, never a decision.** Label buckets as suggestions. `[REDACTED]` in text
  means privacy redaction, not missing info.
- **Cost and time.** A fresh run is about $1 and 3–5 minutes. Re-running a cached packet is
  free and instant. `force=true` throws the cache away: avoid it in the demo.
- **Concurrency.** Two runs at a time; more queue. The server is single-process: run one.
- **Network blips.** The model APIs sometimes fail with connection errors. Starting the same run
  again resumes from cache. The CLI retries 3 times automatically.
- **Ports and CORS.** Default `127.0.0.1:8000` (`--port`, `--host` to change). CORS allows
  `http://localhost:3000` only; edit `server.py` if Next.js runs elsewhere.
- **Uploaded packets** are saved into the packets folder under a sanitized filename and are
  gitignored there.
- **Live judge packet.** Upload with `POST /packets`, then run. Budget ~5 minutes.
