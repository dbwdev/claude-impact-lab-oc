# Orange County | Claude Impact Lab

**Saturday, October 17, 2026 · EvoNexus Irvine · with Illumination Health + Home**

One day. Three real problems from a nonprofit that provides housing, healthcare and case management
for people experiencing homelessness. Teams of 4 to 5 build a working prototype with Claude.
Everything built today is open source and donated to Illumination Health + Home (IHH).

Organized by Claude Community Orange County. Hosted by EvoNexus Irvine.

## Start here

1. Read the [ground rules](docs/ground-rules.md). Two minutes. The first one is not negotiable:
   **synthetic data only, no real patient or client information.**
2. Pick one challenge with your team.
3. Make your team's repo from this one and get set up: [getting started](docs/getting-started.md).
4. Build one workflow for one user. Talk to IHH staff early and often.
5. [Submit](docs/submission.md) by **4:30 PM**.

## Today

| Time | What |
|---|---|
| 8:30 AM | Doors and check-in |
| 9:00 AM | Kickoff. IHH frames the three challenges |
| 9:30 AM | Build |
| Midday | Lunch at the tables |
| **4:30 PM** | **Submissions due.** Judges visit every table |
| 5:00 PM | Finalist demos and judging with IHH |
| 6:00 PM | Close |

## The three challenges

| | Challenge | Who it helps | What you get |
|---|---|---|---|
| 1 | [**Referral intake**](challenges/1-referral-intake/) | The coordinator who decides, within two hours, whether a hospital patient can come to recuperative care | IHH's admission criteria, 10 synthetic faxed referral packets, an answer key and a scoring script |
| 2 | [**Finding the right resource**](challenges/2-finding-the-right-resource/) | A client working out where to turn next: shelter, work, ID, a way home | A sourced seed directory of Orange County resources, a guide to larger data sources, 12 client scenarios |
| 3 | [**Staff AI confidence**](challenges/3-staff-ai-confidence/) | Frontline staff who have been told AI will help and have reasons to doubt it | Role cards and a practice kit: a visit transcript, an AI-drafted note with seven planted errors, an answer key |

New to this field? Read the short [background](docs/background.md) and keep the
[glossary](docs/glossary.md) open.

## Ground rules, in short

- **Synthetic data only.** No real patient or client information, from anyone, for any reason.
- **Prototypes only.** Nothing connects to or changes IHH's systems.
- **People decide.** Your tool informs a coordinator, a client or a staff member. It does not
  decide for them.
- **Start today.** Your first commit comes after 9:30 AM. Libraries and frameworks are fine.
- **Open source.** Public repo, open license, donated to IHH.

The full version is in [docs/ground-rules.md](docs/ground-rules.md).

## Submitting

One submission per team, by 4:30 PM: a public repo with a README, and a two-minute screen
recording if you can. Details and the form are in [docs/submission.md](docs/submission.md).

## Judging

Four things, scored 0 to 5, with the first counting double:

| Criterion | The question |
|---|---|
| **Day-one impact** (counts double) | Is it ready to be used, and would it matter on day one? |
| **Product** | Could the person it is for use it without help? |
| **Idea** | Is it a creative, original way in? |
| **Clarity of the demo** | Are the problem, the user and the outcome obvious? |

The full scoring card is in [docs/judging.md](docs/judging.md).

## Help

- **About the problems:** IHH staff are in the room all day. Ask them. Their experience is the
  most valuable thing here.
- **About the day, the repo or your setup:** find an organizer.
- **Something looks like real personal information:** stop and tell an organizer right away.

## What is in this repo

```text
README.md            this page
CLAUDE.md            instructions Claude Code reads when you open this repo
docs/                ground rules, getting started, submission, judging, background, glossary
challenges/
  1-referral-intake/              criteria, synthetic packets, answer key, scorer, generator
  2-finding-the-right-resource/   seed directory, data sources, client scenarios
  3-staff-ai-confidence/          role cards, practice kit
templates/           the README your team's repo needs
```

## License

Code in this repo is released under the [MIT License](LICENSE). The synthetic packets, scenarios
and practice kit are dedicated to the public domain (CC0). The admission criteria and referral
form are Illumination Health + Home's documents and remain theirs.
