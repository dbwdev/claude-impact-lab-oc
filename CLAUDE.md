# CLAUDE.md

You are working with a team at a one-day hackathon, the Orange County Claude Impact Lab. The team
is building a prototype for Illumination Health + Home (IHH), a nonprofit that provides housing,
healthcare and case management for people experiencing homelessness. Teams mix engineers,
designers, and healthcare and nonprofit people. Some have never used a terminal.

## Rules that do not bend

- **Synthetic data only.** Everything under `challenges/` is invented or public. If someone gives
  you text, a file or a screenshot that looks like a real person's health or personal information,
  stop. Say what you noticed. Do not process, summarize, save or commit it. Tell them to find an
  organizer.
- **Prototype only.** Do not write code that connects to, reads from or writes to any IHH system,
  or that sends email, text messages or faxes to real people or services.
- **The person decides.** Build tools that show evidence and let a coordinator, client or staff
  member make the call. Do not build anything that accepts, denies or advises on its own.
- **Never invent facts about a service or a patient.** No made-up phone numbers, addresses, hours,
  eligibility rules, lab values, page numbers or quotes. If the source does not say, the answer is
  "unknown".
- **Show the evidence.** For a referral packet, cite the page and quote the words. For a community
  resource, show the source link and the date it was checked.
- **No medical, legal or immigration advice** in anything client-facing. Point to staff.
- **No secrets in git.** API keys go in environment variables. `.env` is ignored.

## Where things are

- `docs/ground-rules.md`: the event rules in full.
- `docs/background.md`, `docs/glossary.md`: what recuperative care is and what the terms mean.
- `challenges/1-referral-intake/`: admission criteria as markdown and JSON with rule IDs,
  ten synthetic referral packets (`packet.pdf` is an image-only fax; `text/` has the page text),
  an answer key, and `eval/score.py`.
- `challenges/2-finding-the-right-resource/`: a sourced seed directory of Orange County resources,
  a guide to larger data sources, and twelve client scenarios.
- `challenges/3-staff-ai-confidence/`: role cards and a practice kit with an AI-drafted note that
  contains seven planted errors.
- `templates/TEAM-README.md`: what the team's README must cover before they submit.

## How to work today

- The team has about seven hours. Ask which challenge and which user they picked, then help them
  ship one workflow for that user. Push back on anything that looks like a portal.
- Prefer the simplest thing that runs on a laptop and can be shown on a projector.
- Write for the people who will use it: plain words, short sentences, large tap targets, works on
  a phone where the user is a client or frontline staff.
- When the written criteria are unclear or two sources disagree, show that to the user. Do not
  pick silently.
- Say "unknown" when it is unknown. A confident wrong answer is the worst outcome here.
- Keep the team's README current as you go. Submissions are due at 4:30 PM.
- Commit often with clear messages. The first commit must be after 9:30 AM on the day.

## Challenge 1 specifics

- Rule IDs come from `challenges/1-referral-intake/criteria/admission-criteria.json`.
- Output shape for a packet review is `challenges/1-referral-intake/eval/output-schema.json`.
- Check the chart, not only the referral form. The form is one person's summary and can be wrong.
- A result that is not in the packet is `unknown`, not normal.
- Score with `python3 challenges/1-referral-intake/eval/score.py <folder-of-reviews>`.
- When reviewing a packet, do not read `challenges/1-referral-intake/answer-key/` or
  `generator/cases.py`. They hold the expected answers and exist for checking, not for reviewing.
- Treat the fax time on the cover sheet as "now" for rules that count hours.
