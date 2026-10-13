# Challenge 2: Finding the right resource

> Help clients identify community resources that fit needs they choose to share, understand
> eligibility and next steps, with a staff handoff when unsure.

## The situation

A client at Illumination Health + Home (IHH) is getting better. The next questions are practical.
Where do I sleep after this? How do I get an ID? Who can help me find work? Can anyone help me get
to my sister's?

Orange County has programs for most of these. Finding the one that fits, working out whether you
qualify, and making the first call is the hard part. IHH put it this way: clients "can struggle
searching for and accessing community resources to suit their specific needs (be it shelter
referral, microloans to start a business and generate income, travel cost assistance to reunify
with family, resume coaching, etc)."

IHH already points clients to a tool for health information. This challenge is about community
resources, not health advice.

## Who you are building for

The client. They may be using it alone on a phone, or sitting next to a case manager. Assume a
small screen, limited data, and that English may not be their first language.

## What a useful tool does

1. Asks what the person needs, in plain words, and takes only what they choose to share.
2. Suggests two or three resources that fit, and says why each one fits.
3. Explains who qualifies and what to bring, in plain language.
4. Says how to reach the service: walk in, call, or get a referral from staff.
5. Helps prepare the first contact, such as a call script or a short message. It does not send it.
6. Shows where each fact came from and when it was last checked.
7. Says "I'm not sure, ask a staff member" when the information is thin, old or sensitive.

A good demo: take a scenario from [`scenarios/`](scenarios/), show two or three fitting resources
with their sources, explain the match, and end with a first step the person could take today.

## What is in this folder

| Path | What it is |
|---|---|
| [`data/oc-resources.seed.json`](data/oc-resources.seed.json) | A seed directory of real Orange County resources, each with a source link, a supporting quote and the date it was checked |
| [`data/DATA-SOURCES.md`](data/DATA-SOURCES.md) | Larger directories and data sources you can pull from, with notes on access and terms |
| [`scenarios/client-scenarios.json`](scenarios/client-scenarios.json) | Twelve made-up client situations to design and test against, including ones where the right move is a staff handoff |

**The seed directory is a starting point, not a source of truth.** It was assembled from public web
pages on the date shown in each entry. Programs close, phone numbers change and eligibility rules
move. Anything you show a client needs its source and its date beside it.

### What the seed covers well, and what it does not

Forty entries, each from the organization's own page or a government page.

| Need IHH named | What we found in public sources |
|---|---|
| Shelter | Solid: the county's coordinated entry system, county and city shelters, 211. Most shelters take people by referral only, and several require ties to one city |
| Job and resume help | Solid: four programs, including walk-in resume help |
| Microloans | Thin. No Orange County or homelessness-specific program. Regional nonprofit lenders ask for a registered business and a credit review |
| Travel home to family | Nearly empty. No public Orange County program with a way to apply. Two weak city leads and one national program for ages 12 to 21 |

The thin rows are part of the problem. A tool that says "there is no public program for this, here
is who to ask" is more useful than one that fills the gap with a guess. Ask IHH staff how they
handle these today.

## Rules for this challenge

- **Never invent a fact about a service.** No made-up phone numbers, addresses, hours or
  eligibility rules. If the source does not say, your tool says it does not know.
- **Show the source and the date** for every resource.
- **Take the least information you need.** Do not ask for a full name, date of birth, Social
  Security number, immigration status or diagnosis. Do not store what people tell you.
- **Do not send anything on a client's behalf.** Prepare the message. The person sends it.
- **Do not give medical, legal or immigration advice.** Point to the right service.
- **Safety first.** If someone says they are in danger, give the hotline and bring in staff.
  Never list the address of a domestic violence shelter.
- **Respect each data source's terms of use.** See `data/DATA-SOURCES.md`.

## Ideas

- **Three questions to three options.** A phone flow that gets from "what do you need?" to a short
  list in under a minute.
- **The first call.** A script the person can read aloud, with what to ask and what to have ready.
- **What to bring.** A checklist per resource, printable on one page.
- **In my language.** The same answer in Spanish or Vietnamese at a sixth-grade reading level.
- **Is this still true?** An agent that re-checks a listing against its source page and flags
  what changed.
- **For the case manager.** The same search, with a note the case manager can add to the care plan.
- **Close to here.** Sort by what is reachable by bus from where the person is staying.

## Watch out for

- **Access is the catch.** Many shelters and housing programs take people only by referral from an
  outreach team or the county's coordinated entry system. A tool that says "go here" when the door
  is referral-only sends someone across town for nothing.
- **Stale listings do harm.** A wrong number costs a person in crisis their one phone call.
- **Eligibility is rarely simple.** Age, city of last residence, veteran status, family size and
  income can all matter. Say what is known and what to ask.
- **Do not overwhelm.** Three good options beat thirty.
- **Tone.** People using this have been turned away a lot. Be plain, warm and brief.

## Ask the people in the room

Which resources do you refer to most? Which ones are harder to get into than they look? What do
clients ask for that you cannot find? What phones and languages do clients have? Would a client use
this alone, or with you beside them?

## Ground rules

Made-up clients only. No real client information, from anyone, for any reason. See
[`docs/ground-rules.md`](../../docs/ground-rules.md).
