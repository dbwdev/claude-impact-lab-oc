# Synthetic referral packets

**Everything here is invented.** No patient, clinician, hospital, phone number, email address or
record number in these packets is real. Each page carries a footer that says so. The cases were
written from IHH's admission criteria and are not based on any real person's record.

| Packet | Pages | Fax quality |
|---|---|---|
| S01 | 13 | standard |
| S02 | 13 | standard, monospace print |
| S03 | 14 | low resolution |
| S04 | 15 | standard |
| S05 | 13 | standard |
| S06 | 14 | standard |
| S07 | 12 | standard, monospace print |
| S08 | 13 | standard |
| S09 | 6 | standard |
| S10 | 14 | standard |

Each folder has:

- `packet.pdf`: the referral as a coordinator would receive it. Image-only pages, slightly skewed
  and speckled, no text layer. Page numbers in the answer key refer to this file.
- `text/p01.txt` and so on: the exact text of each page.

A packet can contain any of these, in any order: fax cover sheet, IHH referral form, face sheet,
health plan authorization request, history and physical, progress notes, consult notes, PT/OT
evaluation, nursing assessment, vital signs, laboratory results, imaging reports, medication list,
case management note.

Decisions and the reasons for them are in [`../answer-key/`](../answer-key/). Try a packet before
you look.

To make more packets, see [`../generator/`](../generator/).
