# Packet generator

This is how the synthetic packets were made. Use it to write your own test cases or to hand IHH a
way to make more.

```bash
python3 build_packets.py                 # rebuild all packets and the answer key
python3 build_packets.py --only S05      # rebuild one packet, leave the key alone
python3 build_packets.py --cases my_cases.py --out my-packets --key my-key.json
```

Needs Python 3.9+, Google Chrome or Chromium, poppler (`pdftoppm`, `pdftotext`, `pdfinfo`) and
ImageMagick 7 (`magick`). On a Mac: `brew install poppler imagemagick`.

## How it works

1. [`cases.py`](cases.py) holds each case as plain data: the patient, the documents in the packet
   and their order, the clinical content, and `truth` (the expected decision and why).
2. `build_packets.py` lays each case out as hospital-style pages and prints them to PDF with
   headless Chrome. The exact page text is saved to `text/`.
3. Each page is then tilted slightly, blurred, speckled and reduced to black and white so it looks
   faxed, and the pages are reassembled into an image-only `packet.pdf`.
4. Page numbers for every finding in the answer key are filled in from where each document landed.

## Writing a case

Copy a case in `cases.py`, change the `id`, and edit. To test a rule, decide the answer first, then
write the chart so the deciding fact sits where a real chart would put it. The more interesting
cases have a referral form that disagrees with the chart, or leave a required document out of
`docs`.

Keep everything invented: names, hospitals, `555-01xx` phone numbers, `example.org` email addresses
and `SYN-` record numbers. Never model a case on a real person.
