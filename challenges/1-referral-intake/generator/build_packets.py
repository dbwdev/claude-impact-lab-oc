#!/usr/bin/env python3
"""Build the synthetic referral packets for Challenge 1.

Every patient, clinician, hospital, phone number and record number produced here is invented.
Nothing is copied from a real record.

For each case this writes:
  packets/<ID>/packet.pdf      image-only pages that look like a faxed hospital packet
  packets/<ID>/text/pNN.txt    the exact text of each page, so OCR is optional
and it writes the answer key (decision, findings with page numbers, missing documents).

Needs: Python 3.9+, Google Chrome (headless print), poppler (pdftoppm, pdftotext, pdfinfo),
ImageMagick 7 (magick).

    python3 build_packets.py                       # dev cases -> ../packets, ../answer-key
    python3 build_packets.py --cases other.py --out DIR --key FILE
"""
import argparse
import html
import importlib.util
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]
FOOTER = "SYNTHETIC RECORD FOR A HACKATHON - NOT A REAL PATIENT - Claude Impact Lab OC 2026"
IHH_FAX = "888-555-0155"  # invented; not IHH's real fax line

HOSPITALS = {
    "pcmc": {"name": "Pacific Crest Medical Center", "short": "PACIFIC CREST MED CTR",
             "addr": "4100 Harbor Mesa Parkway, Orange County, CA", "phone": "714-555-0100",
             "fax": "714-555-0142", "font": "Arial, Helvetica, sans-serif"},
    "sbch": {"name": "St. Brendan Community Hospital", "short": "ST BRENDAN COMM HOSP",
             "addr": "2250 Citrus Grove Avenue, Orange County, CA", "phone": "657-555-0110",
             "fax": "657-555-0163", "font": "Menlo, Monaco, 'Courier New', monospace", "size": "8.6pt"},
    "lorh": {"name": "Los Olivos Regional Hospital", "short": "LOS OLIVOS REGIONAL",
             "addr": "880 Mission Ridge Road, Orange County, CA", "phone": "949-555-0120",
             "fax": "949-555-0177", "font": "Georgia, 'Times New Roman', serif"},
    "bumc": {"name": "Bayfront University Medical Center", "short": "BAYFRONT UNIV MED CTR",
             "addr": "1 University Health Plaza, Orange County, CA", "phone": "714-555-0130",
             "fax": "714-555-0188", "font": "Verdana, Geneva, sans-serif"},
}

DOC_TITLES = {
    "cover": "Fax cover sheet", "form": "IHH recuperative care referral form",
    "face": "Face sheet / demographics", "auth": "Health plan authorization request",
    "hp": "History and physical", "progress": "Progress notes", "consult": "Consult note",
    "ptot": "PT/OT evaluation", "nursing": "Nursing assessment", "vitals": "Vital signs",
    "labs": "Laboratory results", "imaging": "Imaging reports", "meds": "Medication list",
    "cm": "Case management note",
}

NORMAL_EXAM = [
    ("General", "Awake, alert, in no acute distress."),
    ("HEENT", "Normocephalic. Mucous membranes moist."),
    ("Cardiovascular", "Regular rate and rhythm. No murmurs."),
    ("Respiratory", "Clear to auscultation bilaterally. No increased work of breathing."),
    ("Abdomen", "Soft, non-tender, non-distended."),
    ("Extremities", "No edema."),
    ("Skin", "Warm and dry."),
    ("Neuro", "Alert and oriented x4. No focal deficits."),
    ("Psych", "Calm, cooperative. Normal mood and affect."),
]
NORMAL_CBC = [("WBC", "7.4", "4.0-11.0", "K/uL"), ("Hemoglobin", "13.6", "12.0-17.0", "g/dL"),
              ("Hematocrit", "40.8", "36-50", "%"), ("Platelets", "248", "150-400", "K/uL")]
NORMAL_BMP = [("Sodium", "139", "135-145", "mmol/L"), ("Potassium", "4.1", "3.5-5.1", "mmol/L"),
              ("Chloride", "103", "98-107", "mmol/L"), ("CO2", "24", "22-29", "mmol/L"),
              ("BUN", "14", "7-20", "mg/dL"), ("Creatinine", "0.9", "0.6-1.3", "mg/dL"),
              ("Glucose", "92", "70-99", "mg/dL")]


def e(x):
    return html.escape(str(x), quote=False)


def paras(text):
    return "".join(f"<p>{e(p.strip())}</p>" for p in str(text).strip().split("\n\n") if p.strip())


def ul(items):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>" if items else "<p>None.</p>"


def kv(rows, cols=2):
    cells = [f"<td class='k'>{e(k)}</td><td class='v'>{e(v)}</td>" for k, v in rows]
    out = []
    for i in range(0, len(cells), cols):
        out.append("<tr>" + "".join(cells[i:i + cols]) + "</tr>")
    return "<table class='kv'>" + "".join(out) + "</table>"


def tbl(head, rows, cls="grid"):
    h = "".join(f"<th>{e(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table class='{cls}'><tr>{h}</tr>{b}</table>"


def cb(on):
    return f"<span class='cb'>{'X' if on else '&nbsp;'}</span>"


def opt(on, label):
    """A checkbox and its label, kept together on one line."""
    return f"<span class='opt'>{cb(on)} {e(label)}</span>"


def yn(val, yes="Yes", no="No"):
    v = (val or "").upper()
    return f"{opt(v == 'Y', yes)} &nbsp; {opt(v == 'N', no)}"


def band(c, title, sub=""):
    p, h = c["patient"], HOSPITALS[c["hospital"]]
    last, first = p["name"].split(", ")
    return (
        f"<div class='band'><div><b>{e(last)}, {e(first)}</b> (MRN: {e(p['mrn'])}) "
        f"DOB: {e(p['dob'])} &nbsp; {e(p['age'])}y {e(p['sex'])}</div>"
        f"<div>{e(h['name'])} &middot; {e(c['unit'])}</div></div>"
        f"<h1>{e(title)}</h1>" + (f"<div class='sub'>{e(sub)}</div>" if sub else "")
    )


# --- documents -------------------------------------------------------------------------------

def doc_cover(c):
    h, cm = HOSPITALS[c["hospital"]], c["cm"]
    return (
        f"<div class='cover'><h1 class='big'>FAX</h1><div class='hosp'>{e(h['name'])}</div>"
        f"<div>{e(h['addr'])}</div><div>Case Management Department</div>"
        + kv([("To", "Illumination Health + Home, Recuperative Care Referrals"),
              ("Fax", IHH_FAX), ("From", f"{cm['name']}, {cm['title']}"),
              ("Phone", cm["phone"]), ("Date", c["refer_dt"]),
              ("Re", "Recuperative care referral")], cols=1)
        + f"<h2>Message</h2>{paras(c['cover_note'])}"
        "<p class='fine'>CONFIDENTIALITY NOTICE: This transmission is intended only for the "
        "addressee and may contain protected health information. If you received it in error, "
        "notify the sender and destroy all copies.</p></div>"
    )


def doc_form(c):
    p, h, cm, f = c["patient"], HOSPITALS[c["hospital"]], c["cm"], c["form"]
    g = p["sex"]
    flags = set(f.get("flags", []))
    return (
        "<div class='form'><h1>Recuperative Care Referral Form</h1>"
        "<div class='sub'>Illumination Health + Home. Submit this form with supporting documents "
        f"by fax to {IHH_FAX}.</div>"
        "<h2>Referring Party</h2>"
        + kv([("Referring Hospital", h["name"]), ("Dept/Floor", c["unit"]),
              ("SW/CM/RN", cm["name"]), ("Phone/Pager #", cm["phone"]),
              ("Email", cm["email"]), ("Nursing Station #", h["phone"]),
              ("Authorized by", f.get("authorized_by", c["attending"])), ("Phone #", h["phone"])])
        + "<h2>Patient Information</h2>"
        + kv([("Patient Name", " ".join(reversed(p["name"].split(", ")))), ("MRN", p["mrn"]),
              ("Date of Birth", p["dob"]), ("Ethnicity", p.get("ethnicity", "")),
              ("Insurance", p["insurance"]), ("Preferred Language", p["language"])])
        + f"<p>Gender: {opt(g == 'M', 'Male')} {opt(g == 'F', 'Female')} {opt(False, 'Transgender')} "
          f"{opt(False, 'Other')} &nbsp;&nbsp; Last 4 # of Social Security: xxx-xx-{e(p.get('ssn4', '____'))}</p>"
        + f"<p>Housing Situation: {opt('unhoused' in flags, 'Currently Unhoused')} &nbsp; "
          f"{opt('chronic' in flags, '4+ episodes of homelessness in the past 3 years')}</p>"
        + "<h2>Hospital Admission Details</h2>"
        + f"<p>Chief Complaint / Admitting Diagnosis: <u>{e(c['dx'])}</u></p>"
        + f"<p>Admit Date: <u>{e(c['admit_dt'].split()[0])}</u> &nbsp;&nbsp; Any Wounds? {yn(f.get('wounds'))}</p>"
        + f"<p>If yes, explain the number, location, size and stage: <u>{e(f.get('wounds_explain', ''))}</u></p>"
        + f"<p>Independent with Wound Care? {yn(f.get('wound_indep'))} &nbsp; If no, will Home Health be ordered? {yn(f.get('hh_ordered'))}</p>"
        + f"<p>Was PPD/TB Test or Chest X-Ray Performed? {yn(f.get('tb'))} &nbsp; Date: <u>{e(f.get('tb_date', ''))}</u> Results: <u>{e(f.get('tb_result', ''))}</u></p>"
        + "<h2>History of Health &amp; Living Situation</h2><table class='yn'>"
        + "".join(
            f"<tr><td>{e(a)}</td><td>{yn(f.get(ak))}</td><td>{e(b)}</td><td>{yn(f.get(bk)) if bk else ''}</td></tr>"
            for a, ak, b, bk in [
                ("O2", "o2", "Active Infection", "active_infection"),
                ("Self Administer All Meds", "self_meds", "Ambulatory", "ambulatory"),
                ("Continent of Bowel & Bladder", "continent", "Assistive Device", "assistive"),
                ("Colostomy/Ileostomy", "colostomy", "Hospice", "hospice"),
                ("Foley Catheter", "foley", "Car", "car"),
                ("Diabetes", "diabetes", "Service Animal", "service_animal"),
                ("Insulin", "insulin", "", None),
                ("Diabetes related Oral Meds", "dm_oral", "", None),
            ])
        + "</table>"
        + f"<p>Explain (O2 / infection / device / hospice): <u>{e(f.get('explain', ''))}</u></p>"
        + "<h2>Behavioral and Mental Health Status</h2>"
        + f"<p>Does the patient have any limitations, behavioral or mental health challenges? {yn(f.get('behavioral'), 'Yes', 'No')}</p>"
        + f"<p>{opt('mh_dx' in flags, 'Mental Health DX')} &nbsp; If checked, what type? <u>{e(f.get('mh_dx', ''))}</u></p>"
        + f"<p>{opt('noncompliant' in flags, 'Non-compliant')} &nbsp; {opt('forgetful' in flags, 'Forgetful')} &nbsp; "
          f"{opt('cognitive' in flags, 'Cognitive Impairment')} &nbsp; {opt('rso' in flags, 'Registered Sex Offender')}</p>"
        + f"<p>{opt(bool(f.get('other')), 'Other')} &nbsp; Explain: <u>{e(f.get('other', ''))}</u></p>"
        + f"<p class='los'>Length of Stay Authorized in Recuperative Care: <u>&nbsp;{e(f.get('los', ''))}&nbsp;</u> Days</p>"
        + "<div class='staff'><b>ILLUMINATION STAFF ONLY</b><br>Date Received: ____________ Reviewed by: ____________<br>"
          "Approved: [ ] Yes [ ] No &nbsp; Date: ________ Authorization #: ________ Reason for Denial: ____________<br>"
          "Admission Date: ________ Admission Time: ________ Exit Date: ________</div></div>"
    )


def doc_face(c):
    p, h = c["patient"], HOSPITALS[c["hospital"]]
    return (
        band(c, "Patient Face Sheet", f"Printed {c['refer_dt']} by {c['cm']['name']}")
        + "<h2>Patient Information</h2>"
        + kv([("Patient", p["name"]), ("Sex", p["sex"]), ("DOB", p["dob"]), ("Age", f"{p['age']}y"),
              ("Address", p.get("address", "NO FIXED ADDRESS")), ("Language", p["language"]),
              ("Phone", p.get("phone", "NONE")), ("Marital Status", p.get("marital", "Single")),
              ("Emergency Contact", p.get("contact", "None listed")), ("Interpreter", "No")])
        + "<h2>Insurance Information</h2>"
        + kv([("Primary", p["insurance"]), ("Member ID", p.get("member_id", "SYN-M-000000")),
              ("Secondary", "None"), ("Financial Class", "Medi-Cal Managed Care")])
        + "<h2>Encounter Information</h2>"
        + kv([("Admit Date/Time", c["admit_dt"]), ("Mode of Arrival", c.get("arrival", "Walk-in")),
              ("Patient Class", c.get("pt_class", "Inpatient")), ("Unit", c["unit"]),
              ("Admitting Diagnosis", c["dx"]), ("Diagnosis Code", c.get("icd", "")),
              ("Attending", c["attending"]), ("Expected Discharge", c["dc_dt"])])
        + f"<p class='fine'>{e(h['name'])}, {e(h['addr'])}. Main {e(h['phone'])}.</p>"
    )


def doc_auth(c):
    p, a = c["patient"], c.get("auth", {})
    return (
        band(c, "Authorization Request: Recuperative Care (Community Support)",
             f"Submitted {c['refer_dt']} by {c['cm']['name']}")
        + kv([("Health Plan", p["insurance"]), ("Member ID", p.get("member_id", "SYN-M-000000")),
              ("Service Requested", "Recuperative care (medical respite)"),
              ("Requested Provider", "Illumination Health + Home"),
              ("Days Requested", a.get("days", c.get("form", {}).get("los", "30"))), ("Diagnosis Code(s)", c.get("icd", "")),
              ("Status", a.get("status", "Pending health plan review")),
              ("Authorization #", a.get("number", "Not yet assigned"))], cols=1)
        + "<h2>Clinical justification</h2>" + paras(a.get("why", c["cover_note"]))
    )


def doc_hp(c):
    x = c["hp"]
    exam = dict(NORMAL_EXAM)
    exam.update(x.get("exam", {}))
    return (
        band(c, "History and Physical", f"{c['attending']} - Admission date {c['admit_dt'].split()[0]} - Signed")
        + f"<h2>Chief Complaint</h2><p>{e(x['cc'])}</p>"
        + "<h2>History of Present Illness</h2>" + paras(x["hpi"])
        + "<h2>Past Medical History</h2>" + ul(x.get("pmh", []))
        + "<h2>Past Surgical History</h2>" + ul(x.get("psh", []))
        + "<h2>Home Medications</h2>" + ul(x.get("meds_home", []))
        + f"<h2>Allergies</h2><p>{e(x.get('allergies', 'No known drug allergies.'))}</p>"
        + "<h2>Social History</h2>" + paras(x["social"])
        + "<h2>Physical Exam</h2>"
        + "".join(f"<p><b>{e(k)}:</b> {e(v)}</p>" for k, v in exam.items())
        + "<h2>Assessment and Plan</h2>" + ul(x["plan"])
    )


def doc_progress(c):
    out = band(c, "Progress Notes")
    for n in c["progress"]:
        out += (f"<div class='note'><div class='nh'>{e(n['date'])} &nbsp; {e(n['author'])} &nbsp; "
                f"{e(n.get('type', 'Hospital Medicine Progress Note'))}</div>{paras(n['text'])}</div>")
    return out


def doc_consult(c):
    out = ""
    for i, n in enumerate(c["consult"]):
        out += (band(c, f"{n['service']} Consult" if i == 0 else f"{n['service']} Note",
                     f"{n['author']} - {n['date']} - Signed")
                + f"<p><b>Reason for consult:</b> {e(n['reason'])}</p>" + paras(n["text"])
                + ("<h2>Recommendations</h2>" + ul(n["recs"]) if n.get("recs") else ""))
        if i < len(c["consult"]) - 1:
            out += "<div class='brk'></div>"
    return out


def doc_ptot(c):
    x = c["ptot"]
    return (
        band(c, x.get("title", "Physical Therapy Evaluation"), f"{x['author']} - {x['date']} - Signed")
        + tbl(["Area", "Finding"], x["rows"]) + "<h2>Assessment</h2>" + paras(x["text"])
        + f"<p><b>Discharge recommendation:</b> {e(x['rec'])}</p>"
    )


def doc_nursing(c):
    x = c["nursing"]
    return (
        band(c, "Nursing Assessment / ADL Flowsheet", f"{x['author']} - {x['date']}")
        + tbl(["Item", "Assessment"], x["rows"])
        + ("<h2>Nursing note</h2>" + paras(x["text"]) if x.get("text") else "")
    )


def doc_vitals(c):
    return (
        band(c, "Vital Signs Flowsheet")
        + tbl(["Date/Time", "BP", "HR", "RR", "Temp F", "SpO2", "O2"], c["vitals"])
        + (f"<p class='fine'>{e(c['vitals_note'])}</p>" if c.get("vitals_note") else "")
    )


def vary(rows, rng):
    """Nudge each normal value a little, staying inside its reference range."""
    spread = {"WBC": 1.4, "Hemoglobin": 0.9, "Platelets": 55, "Sodium": 2, "Potassium": 0.3, "Chloride": 2,
              "CO2": 1, "BUN": 3, "Creatinine": 0.12, "Glucose": 6}
    out = []
    for name, val, ref, unit in rows:
        if name in spread:
            v = float(val) + rng.uniform(-spread[name], spread[name])
            val = f"{v:.1f}" if "." in val else f"{round(v)}"
        out.append([name, val, ref, unit])
    hgb = next(r for r in out if r[0] == "Hemoglobin") if any(r[0] == "Hemoglobin" for r in out) else None
    for r in out:
        if r[0] == "Hematocrit" and hgb:
            r[1] = f"{float(hgb[1]) * 3:.1f}"
    return out


def doc_labs(c):
    x = c["labs"]
    out = band(c, "Laboratory Results", f"Collected {x.get('date', c['admit_dt'].split()[0])}")
    rng = random.Random(c["id"] + "-labs")
    cbc = vary(NORMAL_CBC, rng)
    bmp = vary(NORMAL_BMP, rng)
    for name, val in x.get("override", {}).items():
        for r in cbc + bmp:
            if r[0] == name:
                r[1] = val
    out += "<h2>Complete Blood Count</h2>" + tbl(["Test", "Result", "Reference", "Units"], cbc)
    out += "<h2>Basic Metabolic Panel</h2>" + tbl(["Test", "Result", "Reference", "Units"], bmp)
    if x.get("extra"):
        out += f"<h2>{e(x.get('extra_title', 'Additional results'))}</h2>" + tbl(
            ["Test", "Collected", "Result", "Reference"], x["extra"])
    if x.get("micro"):
        out += "<h2>Microbiology</h2>" + tbl(["Test", "Collected", "Result"], x["micro"])
    return out


def doc_imaging(c):
    out = ""
    for i, s in enumerate(c["imaging"]):
        out += (band(c, "Diagnostic Imaging Report", f"{s['study']} - {s['date']}")
                + f"<p><b>Indication:</b> {e(s['indication'])}</p>"
                + "<h2>Findings</h2>" + paras(s["findings"])
                + f"<h2>Impression</h2><p>{e(s['impression'])}</p>"
                + f"<p class='fine'>Electronically signed by {e(s.get('rad', 'Radiology attending'))}</p>")
        if i < len(c["imaging"]) - 1:
            out += "<div class='brk'></div>"
    return out


def doc_meds(c):
    return (
        band(c, "Discharge Medication List", f"Reconciled {c['refer_dt'].split()[0]}")
        + tbl(["Medication", "Dose", "Route", "Frequency", "Notes"], c["meds"])
        + (f"<p>{e(c['meds_note'])}</p>" if c.get("meds_note") else "")
    )


def doc_cm(c):
    x = c["cmnote"]
    return (
        band(c, "Case Management / Social Work Note", f"{c['cm']['name']}, {c['cm']['title']} - {x['date']}")
        + paras(x["text"]) + "<h2>Discharge planning</h2>" + tbl(["Item", "Status"], x["rows"])
    )


RENDER = {"cover": doc_cover, "form": doc_form, "face": doc_face, "auth": doc_auth, "hp": doc_hp,
          "progress": doc_progress, "consult": doc_consult, "ptot": doc_ptot, "nursing": doc_nursing,
          "vitals": doc_vitals, "labs": doc_labs, "imaging": doc_imaging, "meds": doc_meds, "cm": doc_cm}

CSS = """
@page { size: 8.5in 11in; margin: 0.5in 0.5in 0.55in 0.5in;
  @top-left { content: "%(fax)s"; font: bold 8pt Menlo, Monaco, 'Courier New', monospace; }
  @top-right { content: "P." counter(page) "/" counter(pages); font: bold 8pt Menlo, Monaco, 'Courier New', monospace; }
  @bottom-center { content: "%(footer)s"; font: 6.5pt Arial, sans-serif; } }
* { box-sizing: border-box; }
body { font: %(size)s/1.32 %(font)s; color: #000; margin: 0; }
.doc { break-after: page; } .doc:last-child { break-after: auto; } .brk { break-after: page; }
.mk { color: #fff; font-size: 1px; }
.band { display: flex; justify-content: space-between; border-bottom: 1.5px solid #000; padding-bottom: 3px; font-size: 8.5pt; }
h1 { font-size: 14pt; margin: 8px 0 2px; } h1.big { font-size: 44pt; margin: 0.4in 0 6px; }
.opt { white-space: nowrap; } .band div:first-child { white-space: nowrap; padding-right: 12px; } .band div:last-child { text-align: right; }
h2 { font-size: 10pt; margin: 9px 0 3px; border-bottom: 0.5px solid #000; text-transform: uppercase; }
.sub { font-size: 8.5pt; margin-bottom: 5px; } p { margin: 3px 0; } ul { margin: 3px 0 3px 16px; padding: 0; }
table { border-collapse: collapse; width: 100%%; margin: 4px 0; }
table.kv td { padding: 2px 5px; vertical-align: top; } table.kv td.k { width: 19%%; font-weight: bold; }
table.kv td.v { border-bottom: 0.5px solid #000; }
table.grid td, table.grid th { border: 0.5px solid #000; padding: 2px 5px; text-align: left; vertical-align: top; }
table.grid th { background: #ddd; font-size: 8.5pt; }
table.yn td { padding: 2px 4px; } .cb { display: inline-block; width: 11px; height: 11px; border: 1px solid #000;
  font: bold 8pt/10px Arial; text-align: center; vertical-align: middle; }
.note { margin: 7px 0 11px; } .nh { font-weight: bold; background: #e6e6e6; padding: 2px 4px; }
.cover .hosp { font-size: 15pt; font-weight: bold; } .fine { font-size: 7.5pt; margin-top: 12px; }
.staff { border: 1px solid #000; padding: 5px; margin-top: 8px; font-size: 8.5pt; line-height: 1.7; }
.los { font-weight: bold; text-align: center; margin-top: 8px; } .form h2 { margin-top: 6px; }
"""


def build_html(c):
    h = HOSPITALS[c["hospital"]]
    fax = f"{c['refer_dt']}  FROM: {h['short']} CASE MGMT  FAX {h['fax']}  TO: IHH RECUP"
    css = CSS % {"fax": fax, "footer": FOOTER, "font": h["font"], "size": h.get("size", "9.5pt")}
    body = "".join(
        f"<section class='doc'><span class='mk'>@@DOC:{d}@@</span>{RENDER[d](c)}</section>" for d in c["docs"])
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"


# --- pipeline --------------------------------------------------------------------------------

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw)


def find_chrome():
    for c in CHROME:
        if Path(c).exists() or shutil.which(c):
            return c
    sys.exit("Google Chrome or Chromium is required to print the packets.")


def build_case(c, out_root, chrome, tmp):
    cid = c["id"]
    work = Path(tmp) / cid
    work.mkdir(parents=True)
    (work / "p.html").write_text(build_html(c), encoding="utf-8")
    run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={work / 'clean.pdf'}", f"file://{work / 'p.html'}"])
    n = int(re.search(r"Pages:\s+(\d+)", run(["pdfinfo", str(work / "clean.pdf")]).stdout.decode()).group(1))

    out = Path(out_root) / cid
    if out.exists():
        shutil.rmtree(out)
    (out / "text").mkdir(parents=True)
    page_doc, current = {}, None
    for i in range(1, n + 1):
        t = run(["pdftotext", "-layout", "-f", str(i), "-l", str(i), str(work / "clean.pdf"), "-"]).stdout.decode()
        m = re.search(r"@@DOC:(\w+)@@", t)
        if m:
            current = m.group(1)
        page_doc[i] = current
        t = re.sub(r"[ \t]*@@DOC:\w+@@[ \t]*\n?", "", t).replace("\f", "")
        (out / "text" / f"p{i:02d}.txt").write_text(t.rstrip() + "\n", encoding="utf-8")

    # make it look faxed: tilt a little, soften, speckle, then drop to pure black and white
    run(["pdftoppm", "-r", "200", "-gray", "-png", str(work / "clean.pdf"), str(work / "pg")])
    rng = random.Random(cid)
    pages = sorted(work.glob("pg-*.png"))
    low_res = c.get("low_res_fax", False)
    for pg in pages:
        cmd = ["magick", str(pg), "-virtual-pixel", "white", "-distort", "SRT", f"{rng.uniform(-0.55, 0.55):.3f}"]
        if low_res:  # standard-resolution fax keeps only half the vertical detail
            cmd += ["-filter", "box", "-resize", "100%x50%!", "-filter", "point", "-resize", "100%x200%!"]
        cmd += ["-blur", "0x0.55", "-attenuate", f"{rng.uniform(0.05, 0.14):.3f}", "+noise", "Impulse",
                "-threshold", f"{rng.randint(56, 64)}%", "-type", "bilevel", str(pg)]
        run(cmd)
    run(["magick", "-units", "PixelsPerInch", "-density", "200"] + [str(p) for p in pages]
        + ["-compress", "Group4", str(out / "packet.pdf")])

    doc_pages = {}
    for pg, d in page_doc.items():
        doc_pages.setdefault(d, []).append(pg)
    t = c["truth"]
    findings = []
    for f in t.get("findings", []):
        pgs = sorted({p for d in f.get("docs", []) for p in doc_pages.get(d, [])})
        findings.append({"rule": f["rule"], "status": f["status"], "why": f["why"], "pages": pgs})
    return {
        "packet_id": cid, "decision": t["decision"], "summary": t["summary"], "pages": n,
        "findings": findings, "missing_documents": t.get("missing_documents", []),
        "follow_up": t.get("follow_up", []), "contradictions": t.get("contradictions", []),
        "page_map": [{"page": p, "document": page_doc[p], "title": DOC_TITLES.get(page_doc[p], page_doc[p])}
                     for p in sorted(page_doc)],
    }


def load_cases(path):
    spec = importlib.util.spec_from_file_location("cases_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CASES


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cases", default=str(HERE / "cases.py"))
    ap.add_argument("--out", default=str(HERE.parent / "packets"))
    ap.add_argument("--key", default=str(HERE.parent / "answer-key" / "answer-key.json"))
    ap.add_argument("--only", nargs="*", help="build only these case IDs")
    a = ap.parse_args()
    chrome = find_chrome()
    cases = [c for c in load_cases(a.cases) if not a.only or c["id"] in a.only]
    key = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in cases:
            k = build_case(c, a.out, chrome, tmp)
            key.append(k)
            print(f"{k['packet_id']}: {k['pages']} pages, {k['decision']}")
    if not a.only:
        Path(a.key).parent.mkdir(parents=True, exist_ok=True)
        Path(a.key).write_text(json.dumps({"packets": key}, indent=2) + "\n", encoding="utf-8")
        print(f"answer key -> {a.key}")


if __name__ == "__main__":
    main()
