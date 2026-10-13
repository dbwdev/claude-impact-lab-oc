# Answer key

[`answer-key.json`](answer-key.json) has one entry per packet:

| Field | Meaning |
|---|---|
| `decision` | `approve`, `deny` or `needs_info` |
| `summary` | The reasoning in two or three sentences |
| `findings` | The rules that matter for that patient, with `status` and the `pages` that support it |
| `missing_documents` | Referral checklist items (`DOC-1` to `DOC-10`) not in the packet |
| `follow_up` | What a coordinator would ask the hospital |
| `contradictions` | Where documents in the packet disagree |
| `page_map` | Which document each page belongs to |

Status values: `met` means the requirement is satisfied or the exclusion does not apply. `not_met`
means the requirement fails or the exclusion applies. `unknown` means the packet does not say, or
says something is still pending. The scoring script treats `not_met` and `unknown` alike.

## How the key reads the checklist

- A health plan authorization that is submitted and pending counts as sent (`DOC-3`).
- "30-day supply to bedside before discharge" counts as present (`DOC-10`). "Not yet filled" or
  "to follow" counts as missing.
- Fewer than five sets of vitals is recorded against the rule that asks for five (`ID-1`,
  `RESP-2`, `CARD-1`), not as a missing document.
- A swab or culture with no result in the packet is `unknown`.
- A COVID swab that is negative on the day the referral is sent is recorded as `met`. Whether it
  is still inside 24 hours at arrival depends on the arrival time, which no packet gives.

## How much to trust it

The key is the organizers' reading of IHH's written criteria, applied to cases we wrote to test
specific rules. It is a development aid, not IHH policy. Where your tool disagrees with the key and
you can show why from the packet and the criteria, take it to IHH staff in the room. If they agree
with you, you are right and the key is wrong.

`findings` lists the rules that drive each decision plus a few that confirm it. It is not a full
audit of every rule.

Judges hold additional packets with their own key that is not in this repo.
