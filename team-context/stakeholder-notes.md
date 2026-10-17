# Stakeholder Notes

Sat, 17 Oct 26

## Referral Intake Process (Illuminate)

- Referrals come from hospital staff via fax or email, submitted on behalf of patients
  - ~40% of cases are referrals; hospital staff submit to Illuminate’s referral team
  - Current CRM: Kipu (EMR); hospital contacts tracked in Excel, not the CRM
- Target turnaround: 2 hours from receipt, but actual time unknown
  - 24/7 coverage: lead + director only; 3 additional staff during business hours
  - No solid assignment process for who picks up which case
- Biggest bottleneck: can’t reach hospital social workers after acceptance/denial
  - Social workers stop picking up; no warm contacts to fall back on
  - Relationship management is ~50% of the problem; process speed is the other 50%
- Packet review flow:
  1. Packet arrives (fax or email), team acknowledges receipt
  2. Check for missing info or red flags immediately
  3. Review for acceptance criteria (no suicidal ideation, sufficient self-care capacity)
  4. Denials escalate to a nurse for review before final decision
  5. Accepted: coordinate with hospital + ops team for bed placement (6 locations, 1 specializes in kids)
  6. Follow-up next day to confirm patient arrived; case stays open or closes if unreachable
- Packets can exceed 100 pages PDF; surfacing relevant criteria quickly is a key challenge

## Proposed Solutions

- Improve hospital relationship management
  - Maintain 3+ contacts per hospital in CRM so there’s always a fallback
  - Make multi-contact capture part of the acceptance protocol
- Auto-acknowledgment on packet receipt with immediate flag for missing info
- AI agent for persistent outreach to unreachable social workers
  - Agent polls the social worker’s line every 10-15 minutes
  - When social worker picks up, agent auto-connects them to the referral coordinator
  - Agent briefs the referral coordinator on the case before the live handoff
  - Groq voice agent flagged as a feasible, low-friction option
- Dynamic CRM layer on top of Kipu, or a replacement
  - Fax contract nearly up; open to switching vendors
  - Kipu has an API ($30 cost); worth noting for future integration

## Hackathon Build Plan

- Stack: Eve (already configured with full SDLC, testing, MCP support)
  - One team member builds the app framework and scaffold using Eve (~30 min setup)
  - Other team member handles API integration and problem-specific logic
- Repo: fork the existing hackathon repo into a new Eve project (“Eve intake”), reference the PRD already created
- Demo idea: trigger a live agent call during the presentation to show the follow-up flow in action
  - Groq voice agent likely sufficient; need a number provisioned
- Presentation notes: polished but not fully working is fine; include a “one more thing” moment to push judges over the edge
  - Animation/programmatic demo video is an option to illustrate the agent workflow

## Next Steps

- **Set up Eve project and scaffold the intake app**
- **Post repo link in team notes**
- **Provision a phone number for the Groq voice agent demo**
