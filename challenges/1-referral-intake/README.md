# Challenge 1: Referral intake

> How might we help a coordinator say yes in minutes, so a patient doesn't leave the hospital for
> the street?

**Who it's for.** The referral coordinator, and the patient who is ready to leave the hospital but
too sick to recover outside.

**Today.** Each referral is 15 to 35 faxed pages, read by hand against six pages of criteria.
Hospitals send the same referral to several providers, so a slow answer can mean the person is
discharged with nowhere to go. IHH promises hospitals an answer within two hours.

**If you crack it.** A faster, surer answer. A bed instead of the street, and coordinators spending
their time on people, not pages.

**Get the packets first.** They are too big for this repo. Open the
[packets folder on Google Drive](https://drive.google.com/drive/folders/1ISmUtoNCTW3NJNqCQJHJzb6C319RgrXM), choose **Download all**, and unzip the files into
`challenges/1-referral-intake/packets/`, so you have `packets/R01.pdf` to `packets/R11.pdf`.

## The work is done by hand

Open `packets/R01.pdf` ([on Drive](https://drive.google.com/drive/folders/1ISmUtoNCTW3NJNqCQJHJzb6C319RgrXM)) and scroll. That is one referral: 34 pages of faxed scans,
crooked, handwritten in places. The 11 packets here total 282 pages. A coordinator reads every one,
finds the note deep in the chart that contradicts the form on page 2, checks it against the criteria
and writes back to the hospital. Then the next fax arrives.

These are real referrals IHH received and decided, with every name, date, facility, number,
signature and barcode blacked out. A black box means "removed for privacy", not "missing". Do not
copy the packets into your team's repo. If you spot an identifier we missed, stop and tell an
organizer.

## The brief

These are a direction, not a spec. Build what you think will help.

- **Build:** a tool that reads the packet, shows which criteria are met with the page and words,
  lists what's missing, and drafts the reply.
- **A great demo:** a coordinator opens a packet they haven't seen, gets the recommendation in
  under a minute, fixes one thing, and has a reply ready.
- **The coordinator decides. Your tool never accepts or denies anyone.**

## Why it's hard

- The referral form is one person's summary. The fact that decides the case is often deep in the
  chart.
- "Not in the packet" means unknown, not normal.
- IHH's two rule documents don't always agree. The internal admission criteria win over the
  referral form. Where the rules run out, show the coordinator the gap instead of guessing.

## What's in this folder

| Path | What it is |
|---|---|
| [`packets/`](packets/) | Where the 11 de-identified packets go once you [download them](https://drive.google.com/drive/folders/1ISmUtoNCTW3NJNqCQJHJzb6C319RgrXM). Image-only PDFs, as a coordinator receives them |
| [`criteria/`](criteria/) | IHH's admission criteria and referral form: the original PDFs, transcribed, and as JSON with rule IDs |
| [`eval/`](eval/) | IHH's real decision on each packet (7 approved, 4 denied), the output shape and a scoring script |
| [`starter-prompt.md`](starter-prompt.md) | A prompt to paste into Claude to review your first packet |

Keep `eval/decisions.json` out of your tool's sight while it reviews. IHH never wrote down the
reasons, so working out *why* is the job.

## Start

Paste [`starter-prompt.md`](starter-prompt.md) into Claude Code, then score the result:

```bash
python3 challenges/1-referral-intake/eval/score.py challenges/1-referral-intake/my-output/
```

The starter is a baseline, not the product.

## Ask IHH

Jordan and David are in the room all day. What do you read first? What makes you pick up the
phone? What do hospitals get wrong most often? What would make you distrust a tool like this?

No real patient information beyond these de-identified packets. See the
[ground rules](../../docs/ground-rules.md).
