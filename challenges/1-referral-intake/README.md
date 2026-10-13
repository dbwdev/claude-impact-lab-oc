# Challenge 1: Referral intake

> Help coordinators review referral packets faster and understand what supports a referral
> decision or still needs follow-up. The coordinator stays in control.

## The situation

Someone experiencing homelessness is ready to leave the hospital but is too sick to recover on the
street. The hospital's case manager looks for a recuperative care bed and faxes a **referral
packet** to Illumination Health + Home (IHH): the referral form plus pages from the hospital chart.

An IHH **referral coordinator** reads the packet against IHH's admission criteria and answers one
of three ways: yes, no with a brief reason, or "send me what's missing."

- **Speed matters.** IHH's referral form promises a decision within two hours. Hospitals often send
  the same referral to more than one provider. A slow answer can mean the person is discharged
  with nowhere to go.
- **It is slow by hand.** A packet often runs 15 to 35 pages of faxed scans, sometimes far more,
  and every hospital's chart looks different. The criteria run six pages.
- **The answer is often buried.** A consult on page 12 can contradict the form on page 2.
- **Packets are often incomplete.** Then the coordinator has to work out what to ask for.

## Who you are building for

The referral coordinator. They make the decision. Your tool does the reading, shows its evidence
and gets out of the way. It does not accept or deny anyone.

## What a useful tool does with one packet

1. Reads the scanned pages.
2. Says which criteria are met, not met, or cannot be determined, each with the page number and the
   words that support it.
3. Lists what is missing from IHH's referral checklist.
4. Points out where two documents disagree.
5. Drafts the reply to the hospital: approve, deny with a brief reason, or a list of what to send.
6. Lets the coordinator check and correct any of it in seconds.

A good demo: a coordinator opens a packet they have not seen, understands the recommendation in
under a minute, corrects one thing, and has a reply ready to send.

## What is in this folder

| Path | What it is |
|---|---|
| [`criteria/admission-criteria.md`](criteria/admission-criteria.md) | IHH's adult admission criteria, transcribed |
| [`criteria/admission-criteria.json`](criteria/admission-criteria.json) | The same rules with IDs such as `MOB-3`, plus the 10-item referral checklist |
| [`criteria/referral-form-and-checklist.md`](criteria/referral-form-and-checklist.md) | What the referral form asks and what hospitals must send |
| [`criteria/childrens-admission-criteria.md`](criteria/childrens-admission-criteria.md) | Criteria for patients under 18. No sample packets; optional |
| [`criteria/source/`](criteria/source/) | IHH's original PDFs |
| [`packets/`](packets/) | 10 synthetic referral packets: a scanned PDF and the text of every page |
| [`answer-key/`](answer-key/) | The expected decision, findings with page numbers and missing documents for each packet |
| [`eval/`](eval/) | The output shape, a worked example and a scoring script |
| [`starter-prompt.md`](starter-prompt.md) | A prompt to paste into Claude to review your first packet |
| [`generator/`](generator/) | How the packets were made. Use it to write more test cases |

## Start in ten minutes

1. Open Claude Code in this repo and paste the prompt from [`starter-prompt.md`](starter-prompt.md).
2. Compare what you get with the two worked examples in [`eval/example-output/`](eval/example-output/):
   `S05.json` is a denial and `S09.json` is a packet with too much missing to decide.
3. Save your reviews as JSON and score them:

   ```bash
   python3 challenges/1-referral-intake/eval/score.py challenges/1-referral-intake/my-output/
   ```

The scorer reports five things per packet: whether your recommendation matches, whether you
flagged the rules that drive the decision, whether your page citations are right, whether you
caught the missing documents, and whether every quote you gave appears on the page you cited. A
quote score under 1.00 means your tool put words in the packet's mouth.

Then decide what you are building. The starter is a baseline, not the product.

## The packets

All ten are **synthetic**. Every patient, clinician, hospital, phone number and record number is
invented. Each case was written from IHH's criteria to exercise specific rules.

- `packet.pdf` is image-only, like a real fax: skewed, speckled, black and white, no text layer.
  One is a low-resolution fax. This is what coordinators receive.
- `text/pNN.txt` is the exact text of each page. Use it if you would sooner skip OCR.
- Page order differs from packet to packet. One packet is missing most of its documents.

Judges hold a few more packets that are not in this repo and may ask you to run one live.

**Keep the answer key out of your tool's sight.** `answer-key/` and `generator/cases.py` contain
the expected answers. If Claude reads them while reviewing a packet, your scores mean nothing.
Use them to check your work, not to do it.

## Ideas

Pick one user and one moment. Do not build a portal.

- **Evidence-first review.** One screen: the recommendation, each driving rule, and a click through
  to the page and sentence behind it.
- **What's missing.** Turn an incomplete packet into a short, polite fax-back to the hospital
  listing exactly what to send.
- **Contradiction finder.** The form says one thing, the therapy note says another. Surface it.
- **The two-hour clock.** Several packets arrive at once. Which can be answered now, which need a
  phone call, which is about to breach two hours?
- **Rule explainer.** A coordinator asks "why not?" and gets the criterion in IHH's own words.
- **Privacy check.** Before a packet is shared outside the care team, flag any names, record
  numbers, dates or barcodes still visible.

## Watch out for

- **The referral form is one person's summary.** It can be out of date or wrong. Check the chart.
- **"Not in the packet" is not "negative."** A missing MRSA swab is unknown, not clear.
- **Time rules.** Several criteria turn on hours: 24 hours on insulin, 72 hours after alcohol
  intoxication, a COVID swab within 24 hours of admission. Treat the fax time stamped on the cover
  sheet as "now".
- **The written rules have gaps.** See the table at the end of
  [`criteria/admission-criteria.md`](criteria/admission-criteria.md). Show the coordinator the gap.
- **A confident wrong answer is worse than "I can't tell."** Say unknown when it is unknown.
- **Reading faxes is error-prone.** A misread digit in a lab value changes the answer.

## Ask the people in the room

IHH staff are here all day. Good questions for them: What do you read first? What makes you pick
up the phone? What do hospitals get wrong most often? What would make you distrust a tool like this?

## Ground rules

Synthetic data only. No real patient information, from anyone, for any reason. See
[`docs/ground-rules.md`](../../docs/ground-rules.md).
