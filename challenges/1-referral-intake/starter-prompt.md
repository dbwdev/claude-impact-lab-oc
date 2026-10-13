# Starter prompt

Paste this into Claude Code from the root of the repo. Change `S05` to any packet.

```text
You are helping a referral coordinator at a recuperative care program review a hospital referral.
The coordinator makes the decision. You do the reading and show your evidence.

Read these files:
- challenges/1-referral-intake/criteria/admission-criteria.md
- challenges/1-referral-intake/criteria/admission-criteria.json   (rule IDs and the referral checklist)
- challenges/1-referral-intake/criteria/referral-form-and-checklist.md
- challenges/1-referral-intake/packets/S05/packet.pdf             (a scanned fax; read every page)

Then write challenges/1-referral-intake/my-output/S05.json in the shape described by
challenges/1-referral-intake/eval/output-schema.json:

- recommendation: approve, deny, or needs_info
- findings: only the rules that matter for this patient, each with status met, not_met or unknown,
  the page number in packet.pdf and a short exact quote from that page
- missing_documents: checklist IDs (DOC-1 to DOC-10) that are not in the packet
- follow_up_questions: what to ask the hospital
- contradictions: places where two documents in the packet disagree
- summary: two or three plain sentences the coordinator could send to the hospital

Rules for you:
- Check the chart, not just the referral form. The form can be wrong.
- If the packet does not say, the status is unknown. Do not assume a missing result is normal.
- Quote the packet exactly. Do not invent a page number or a quote. For a table, quote the cell and
  name its row.
- Treat the fax time on the cover sheet as "now" for rules that count hours.
- Do not open the answer-key folder or generator/cases.py. They hold the expected answers.
- Where IHH's written criteria are unclear, say so instead of choosing.
```

Then score it:

```bash
python3 challenges/1-referral-intake/eval/score.py challenges/1-referral-intake/my-output/
```
