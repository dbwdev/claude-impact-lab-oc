"""Synthetic referral cases for Challenge 1.

Every person, hospital, phone number and record number here is invented. Each case was written
from IHH's admission criteria to exercise specific rules. None is based on a real
patient. `truth` is the organizers' reading of the written criteria and is pending IHH review.

status in truth.findings:
  met      the requirement is satisfied, or the exclusion does not apply
  not_met  the requirement fails, or the exclusion applies
  unknown  the packet does not say; the coordinator has to ask
"""

LINDQVIST = {"name": "Karen Lindqvist", "title": "RN, CCM", "phone": "714-555-0143",
             "email": "klindqvist@pacificcrest.example.org"}
BRANDT = {"name": "Olivia Brandt", "title": "MSW", "phone": "714-555-0144",
          "email": "obrandt@pacificcrest.example.org"}
ORTEGA = {"name": "Miguel Ortega", "title": "MSW", "phone": "657-555-0164",
          "email": "mortega@stbrendan.example.org"}
WHITFIELD = {"name": "Dana Whitfield", "title": "LCSW", "phone": "949-555-0178",
             "email": "dwhitfield@losolivos.example.org"}
IMANI = {"name": "Rachel Imani", "title": "RN Case Manager", "phone": "714-555-0189",
         "email": "rimani@bayfrontumc.example.org"}

ADL_OK = [("Orientation", "Alert and oriented x4"), ("Bathing", "Independent"),
          ("Dressing", "Independent"), ("Toileting", "Independent. Continent of bowel and bladder"),
          ("Feeding", "Independent"), ("Medications", "Takes own medications with RN observing. Names each one and its purpose"),
          ("Fall risk", "Low"), ("Skin", "Intact"), ("Isolation", "None"),
          ("Safety screen", "Suicide risk screen negative. Denies thoughts of self-harm")]


def adl(**changes):
    """ADL flowsheet rows with selected rows replaced."""
    return [(k, changes.get(k.split()[0].lower(), v)) for k, v in ADL_OK]


CASES = [
    # ---------------------------------------------------------------- S01 approve, clean packet
    {
        "id": "S01", "hospital": "pcmc", "unit": "4 West Medical-Surgical",
        "attending": "Priya Nandakumar, MD", "cm": LINDQVIST,
        "patient": {"name": "ELLERY, MARCUS", "dob": "02/11/1972", "age": 54, "sex": "M",
                    "mrn": "SYN-104417", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-552019", "ssn4": "0000"},
        "dx": "Cellulitis of left lower leg", "icd": "L03.116, Z59.02",
        "admit_dt": "08/03/2026 21:17", "refer_dt": "08/06/2026 15:42", "dc_dt": "08/07/2026",
        "cover_note": "Referral for recuperative care. 54-year-old man with left leg cellulitis, now on oral antibiotics and "
                      "medically ready for discharge 08/07. Unhoused, no place to elevate the leg or keep it clean. "
                      "Independent with all care. Please review and advise.",
        "docs": ["cover", "form", "face", "auth", "hp", "progress", "ptot", "nursing", "vitals", "labs", "imaging", "meds", "cm"],
        "form": {"flags": ["unhoused"], "wounds": "Y", "wounds_explain": "Healing 2 cm abrasion, left shin. No dressing needed",
                 "wound_indep": "Y", "tb": "N",
                 "o2": "N", "active_infection": "Y", "self_meds": "Y", "ambulatory": "Y", "continent": "Y",
                 "assistive": "N", "colostomy": "N", "hospice": "N", "foley": "N", "car": "N", "diabetes": "N",
                 "service_animal": "N", "explain": "Left leg cellulitis, improving, on oral antibiotics",
                 "behavioral": "N", "los": "30"},
        "hp": {
            "cc": "Redness, swelling and pain of the left lower leg for 3 days.",
            "hpi": "54-year-old man with hypertension who scraped his left shin on a fence about one week ago. Over the last 3 days "
                   "he developed spreading redness, warmth and pain from the ankle to mid-calf, with chills. Temperature 101.1 F in "
                   "the emergency department. No drainage, no prior similar episodes.\n\n"
                   "Bedside ultrasound showed no fluid collection. Venous duplex negative for deep vein thrombosis. Blood cultures "
                   "drawn. Started IV cefazolin and admitted for IV antibiotics and leg elevation.",
            "pmh": ["Hypertension", "Tobacco use, half a pack per day"], "psh": [],
            "meds_home": ["Lisinopril 10 mg by mouth daily (takes inconsistently)"],
            "social": "Unhoused for about 14 months. Sleeps outdoors. Works occasional day labor. Denies alcohol or drug use. "
                      "Manages his own medications and appointments when he has them.",
            "exam": {"Extremities": "Left lower leg with erythema, warmth and mild edema from ankle to mid-calf. Borders marked. "
                                    "No fluctuance, no crepitus, no drainage. Healing 2 cm abrasion over the shin. Pulses intact.",
                     "Skin": "As above. Otherwise intact."},
            "plan": ["Left lower leg cellulitis, non-purulent: IV cefazolin, elevate, mark borders, follow cultures.",
                     "Hypertension: resume lisinopril.",
                     "Disposition: unhoused. Case management consult for recuperative care."]},
        "progress": [
            {"date": "08/05/2026 09:10", "author": "Priya Nandakumar, MD",
             "text": "Afebrile for 24 hours. Erythema receding about 4 cm inside the marked border. Pain 3 of 10. Walking in the "
                     "hallway without help. WBC 11.2, down from 13.8. Blood cultures no growth to date.\n\n"
                     "Plan: change to oral cephalexin 500 mg every 6 hours today. Watch 24 hours on oral therapy."},
            {"date": "08/06/2026 08:45", "author": "Priya Nandakumar, MD",
             "text": "Afebrile for more than 48 hours. Erythema continues to recede on oral cephalexin. No drainage. WBC 8.9. "
                     "Blood cultures no growth at 48 hours. Takes his own oral antibiotic at the bedside on schedule.\n\n"
                     "Medically ready for discharge 08/07 to finish 7 more days of oral cephalexin. Needs a clean place to rest "
                     "and elevate the leg. Recuperative care referral in progress."}],
        "ptot": {"author": "Brooke Tanaka, PT, DPT", "date": "08/05/2026 13:20",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "250 ft, modified independent, no device, one standing rest break"),
                          ("Stairs", "12 steps with rail, independent"), ("Balance", "Good static and dynamic"),
                          ("Assistive device", "None needed")],
                 "text": "Patient moves safely and independently. Mild antalgic gait from left leg discomfort. No loss of balance. "
                         "No skilled physical therapy needs.",
                 "rec": "No PT follow-up needed. Safe for discharge to a community setting."},
        "nursing": {"author": "J. Castellanos, RN", "date": "08/06/2026 07:30", "rows": adl(skin="Left lower leg erythema, receding. Small healing abrasion on shin. No open wound"),
                    "text": "Patient showers independently. Manages own hygiene. Calm and cooperative."},
        "vitals": [["08/05/2026 20:00", "128/78", "82", "16", "98.4", "97%", "Room air"],
                   ["08/06/2026 00:10", "122/74", "76", "16", "98.1", "98%", "Room air"],
                   ["08/06/2026 04:05", "118/72", "72", "14", "97.9", "97%", "Room air"],
                   ["08/06/2026 08:00", "126/80", "78", "16", "98.2", "98%", "Room air"],
                   ["08/06/2026 12:15", "130/82", "80", "16", "98.6", "98%", "Room air"]],
        "labs": {"date": "08/06/2026 05:40", "override": {"WBC": "8.9"}, "extra_title": "Trends and other results",
                 "extra": [("WBC", "08/03, 08/05, 08/06", "13.8, 11.2, 8.9 K/uL", "4.0-11.0"),
                           ("Lactate", "08/03/2026 21:40", "1.1 mmol/L", "0.5-2.0"),
                           ("C-reactive protein", "08/04/2026 05:30", "48 mg/L", "<10")],
                 "micro": [("Blood culture x2", "08/03/2026 21:45", "No growth at 48 hours"),
                           ("MRSA nares PCR", "08/04/2026 06:10", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "08/06/2026 14:10", "NEGATIVE")]},
        "imaging": [{"study": "Venous duplex ultrasound, left lower extremity", "date": "08/03/2026 22:30",
                     "indication": "Leg swelling and redness. Rule out deep vein thrombosis.",
                     "findings": "The common femoral, femoral, popliteal and calf veins are compressible with normal flow. "
                                 "Subcutaneous edema of the lower leg. No drainable fluid collection.",
                     "impression": "No deep vein thrombosis. Soft tissue edema consistent with cellulitis.", "rad": "A. Greenbaum, MD"}],
        "meds": [("Cephalexin", "500 mg", "By mouth", "Every 6 hours", "Through 08/13/2026"),
                 ("Lisinopril", "10 mg", "By mouth", "Daily", "Home medication"),
                 ("Acetaminophen", "650 mg", "By mouth", "Every 6 hours as needed", "For pain")],
        "meds_note": "30-day supply of all discharge medications will be delivered to the bedside before discharge.",
        "cmnote": {"date": "08/06/2026 14:55",
                   "text": "Met with patient at bedside. He has been unhoused about 14 months and sleeps outdoors. He has no safe place "
                           "to rest, elevate the leg or keep it clean while he finishes antibiotics. He is agreeable to recuperative "
                           "care. He takes his own medications without reminders and keeps his own appointments.",
                   "rows": [("Housing", "Unhoused about 14 months. No shelter bed."),
                            ("Disposition", "Recuperative care referral faxed to Illumination Health + Home 08/06/2026."),
                            ("Medications", "Self-manages. 30-day supply to bedside before discharge."),
                            ("Follow-up", "Primary care, community clinic, 08/14/2026 10:30."),
                            ("Transportation", "Hospital will arrange a ride at discharge."),
                            ("Health plan authorization", "Submitted 08/06/2026. Pending.")]},
        "truth": {"decision": "approve",
                  "summary": "Approve. Uncomplicated leg cellulitis on oral antibiotics, unhoused, independent, alert and oriented. "
                             "MRSA and COVID swabs negative, five sets of stable vitals, PT note included. Packet is complete.",
                  "findings": [
                      {"rule": "GEN-1", "status": "met", "why": "Unhoused and needs a place to recover.", "docs": ["cm", "hp"]},
                      {"rule": "INT-E1", "status": "met", "why": "Uncomplicated cellulitis treated with oral cephalexin.", "docs": ["hp", "progress"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 250 ft, modified independent, no device.", "docs": ["ptot"]},
                      {"rule": "MOB-2", "status": "met", "why": "PT evaluation is in the packet.", "docs": ["ptot"]},
                      {"rule": "ADL-1", "status": "met", "why": "Independent with bathing, dressing and toileting.", "docs": ["nursing"]},
                      {"rule": "COG-2", "status": "met", "why": "Alert and oriented x4.", "docs": ["nursing", "hp"]},
                      {"rule": "COG-1", "status": "met", "why": "Takes his own medications.", "docs": ["nursing", "cm"]},
                      {"rule": "INF-1", "status": "met", "why": "MRSA nares PCR not detected 08/04.", "docs": ["labs"]},
                      {"rule": "INF-2", "status": "met", "why": "COVID antigen negative 08/06 14:10, within 24 hours of the planned 08/07 admission.", "docs": ["labs"]},
                      {"rule": "ID-1", "status": "met", "why": "Five sets of vitals, afebrile, no sign of sepsis.", "docs": ["vitals"]},
                      {"rule": "ID-2", "status": "met", "why": "Takes his oral antibiotic on his own.", "docs": ["progress", "meds"]}],
                  "missing_documents": [], "follow_up": [], "contradictions": []},
    },

    # ---------------------------------------------------------------- S02 approve, diabetes rules
    {
        "id": "S02", "hospital": "sbch", "unit": "3 North Medical",
        "attending": "Thomas Achterberg, MD", "cm": ORTEGA,
        "patient": {"name": "FARROW, DENISE", "dob": "05/23/1965", "age": 61, "sex": "F",
                    "mrn": "SYN-220836", "language": "English", "ethnicity": "Black/African American",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-417730", "ssn4": "0000"},
        "dx": "Hyperglycemia, type 2 diabetes mellitus, no ketoacidosis", "icd": "E11.65, Z59.02",
        "admit_dt": "08/10/2026 11:48", "refer_dt": "08/12/2026 13:20", "dc_dt": "08/13/2026", "arrival": "Walk-in to ED",
        "cover_note": "Recuperative care referral. 61-year-old woman admitted with high blood sugar after her insulin and meter "
                      "were stolen. No DKA. Back on her home insulin at a slightly higher dose, sugars coming down, does her own injections. Unhoused. "
                      "Ready for discharge 08/13.",
        "docs": ["cover", "face", "form", "hp", "labs", "vitals", "progress", "consult", "ptot", "nursing", "meds", "cm", "auth"],
        "form": {"flags": ["unhoused"], "wounds": "N", "tb": "N",
                 "o2": "N", "active_infection": "N", "self_meds": "Y", "ambulatory": "Y", "continent": "Y",
                 "assistive": "N", "colostomy": "N", "hospice": "N", "foley": "N", "car": "N", "diabetes": "Y",
                 "insulin": "Y", "dm_oral": "Y", "service_animal": "N", "behavioral": "N", "los": "30"},
        "hp": {
            "cc": "High blood sugar, thirst and frequent urination for 5 days.",
            "hpi": "61-year-old woman with type 2 diabetes for 9 years. She has taken insulin glargine 24 units nightly for about "
                   "3 years, plus metformin. Six days ago her bag with her insulin pens, glucometer and test strips was stolen "
                   "while she slept outdoors. She has had no insulin since. She reports thirst, frequent urination and blurry vision.\n\n"
                   "Glucose 512 mg/dL in the emergency department. Anion gap 12, bicarbonate 23, beta-hydroxybutyrate 0.3 mmol/L, "
                   "venous pH 7.38. She is not in diabetic ketoacidosis. Given IV fluids and subcutaneous insulin. Her home "
                   "insulin glargine was restarted the evening of 08/10.",
            "pmh": ["Type 2 diabetes mellitus, 9 years. Hemoglobin A1C 10.9% this admission", "Hypertension", "Hyperlipidemia",
                    "Diabetic peripheral neuropathy"], "psh": ["Cholecystectomy, 2011"],
            "meds_home": ["Insulin glargine 24 units under the skin nightly (none for 6 days)", "Metformin 1000 mg by mouth twice daily",
                          "Losartan 50 mg by mouth daily", "Atorvastatin 20 mg by mouth nightly"],
            "social": "Unhoused for 8 months after an eviction. Sleeps outdoors near a transit center. No tobacco, alcohol or drug "
                      "use. Has checked her own sugars and given her own insulin for years.",
            "exam": {"General": "Awake, alert, mildly dehydrated, in no distress.", "HEENT": "Dry mucous membranes.",
                     "Extremities": "No edema. No foot ulcers. Decreased light touch sensation in both feet."},
            "plan": ["Hyperglycemia from missed insulin, no DKA: IV fluids, restart home glargine tonight, correction scale, check sugars four times daily.",
                     "Diabetes education consult to confirm meter and injection technique and replace supplies.",
                     "Hypertension and hyperlipidemia: continue home medications.",
                     "Disposition: unhoused. Case management consult."]},
        "labs": {"date": "08/10/2026 12:05",
                 "override": {"Glucose": "512", "Sodium": "133", "Chloride": "98", "CO2": "23", "BUN": "22", "Creatinine": "1.1"},
                 "extra_title": "Diabetes labs and point-of-care glucose",
                 "extra": [("Hemoglobin A1C", "08/10/2026 12:05", "10.9 %", "<5.7"),
                           ("Beta-hydroxybutyrate", "08/10/2026 12:05", "0.3 mmol/L", "<0.4"),
                           ("Venous pH", "08/10/2026 12:20", "7.38", "7.32-7.42"),
                           ("Anion gap", "08/10/2026 12:05", "12", "8-16"),
                           ("POC glucose", "08/11/2026 07:10", "248 mg/dL", "70-180"),
                           ("POC glucose", "08/11/2026 11:45", "214 mg/dL", "70-180"),
                           ("POC glucose", "08/11/2026 17:05", "186 mg/dL", "70-180"),
                           ("POC glucose", "08/11/2026 21:30", "171 mg/dL", "70-180"),
                           ("POC glucose", "08/12/2026 07:05", "158 mg/dL", "70-180")],
                 "micro": [("MRSA nares PCR", "08/10/2026 14:30", "NOT DETECTED"),
                           ("SARS-CoV-2 PCR", "08/12/2026 12:40", "NOT DETECTED")]},
        "vitals": [["08/11/2026 16:00", "134/82", "84", "16", "98.2", "98%", "Room air"],
                   ["08/11/2026 20:00", "128/78", "80", "16", "98.0", "98%", "Room air"],
                   ["08/12/2026 00:00", "124/76", "74", "14", "97.8", "97%", "Room air"],
                   ["08/12/2026 04:00", "122/74", "72", "14", "97.9", "98%", "Room air"],
                   ["08/12/2026 08:00", "130/80", "78", "16", "98.1", "98%", "Room air"]],
        "progress": [
            {"date": "08/11/2026 10:05", "author": "Thomas Achterberg, MD",
             "text": "Feeling better. Thirst and urination improved. Glargine 26 units given last night, up from her home dose of "
                     "24. Morning glucose 248. No low blood sugars. Eating a full diet. Metformin resumed today."},
            {"date": "08/12/2026 09:40", "author": "Thomas Achterberg, MD",
             "text": "Last five point-of-care glucose readings: 248, 214, 186, 171, 158. Steadily improving. No episodes of "
                     "hypoglycemia this admission. Dials and injects her own insulin pen with nursing watching.\n\n"
                     "Discharge 08/13 on glargine 26 units nightly, metformin, and a written correction scale. Primary care "
                     "visit booked for 08/18. Needs a safe place to store insulin and supplies."}],
        "consult": [{"service": "Diabetes Education", "author": "Monique Ferrell, RN, CDCES", "date": "08/12/2026 11:15",
                     "reason": "Confirm self-management skills and replace supplies.",
                     "text": "Patient checked her own blood sugar with the new glucometer: washed hands, loaded strip, lanced, "
                             "read and logged the result correctly. She dialed and injected insulin glargine with a pen correctly "
                             "on 08/11 at 21:00 and again by teach-back today. She rotates sites.\n\n"
                             "She names the symptoms of low blood sugar and describes treating it with 15 grams of fast sugar and "
                             "rechecking in 15 minutes. She was given a written plan: glargine 26 units nightly, correction scale "
                             "before meals, and when to hold a dose and call.",
                     "recs": ["New glucometer, strips, lancets and pen needles, 30-day supply at discharge.",
                              "Primary care follow-up 08/18/2026.", "No barriers to self-administration of insulin."]}],
        "ptot": {"author": "Andre Whitaker, PT", "date": "08/11/2026 14:10", "title": "Physical Therapy Screen",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "300 ft, independent, no device"), ("Balance", "Good"),
                          ("Assistive device", "None")],
                 "text": "No mobility deficits. Mild neuropathy does not affect gait.", "rec": "No PT needs."},
        "nursing": {"author": "T. Okonkwo, RN", "date": "08/12/2026 07:20",
                    "rows": adl(medications="Checks own glucose and injects own insulin with RN observing. Names each medication"),
                    "text": "Independent in the shower. No assistance needed."},
        "meds": [("Insulin glargine", "26 units", "Under the skin", "Nightly", "Home regimen, restarted 08/10/2026. Was 24 units"),
                 ("Insulin lispro", "Per written scale", "Under the skin", "Before meals", "Correction scale given to patient"),
                 ("Metformin", "1000 mg", "By mouth", "Twice daily", "Home medication"),
                 ("Losartan", "50 mg", "By mouth", "Daily", "Home medication"),
                 ("Atorvastatin", "20 mg", "By mouth", "Nightly", "Home medication")],
        "meds_note": "30-day supply of all medications, plus glucometer, strips, lancets and pen needles, from the outpatient pharmacy at discharge.",
        "cmnote": {"date": "08/12/2026 12:40",
                   "text": "Patient has been unhoused for 8 months. Her insulin and supplies were stolen while she slept outside. "
                           "She wants a place where she can keep insulin safe while her sugars settle. She is agreeable to "
                           "recuperative care and manages all of her own diabetes care.",
                   "rows": [("Housing", "Unhoused 8 months."), ("Disposition", "Recuperative care referral faxed 08/12/2026."),
                            ("Medications", "Self-manages, including insulin."),
                            ("Follow-up", "Primary care, community health center, 08/18/2026 09:00."),
                            ("Health plan authorization", "Submitted 08/12/2026. Pending.")]},
        "truth": {"decision": "approve",
                  "summary": "Approve. Hyperglycemia without DKA on a long-standing insulin regimen that was restarted 08/10. "
                             "Five consecutive glucose readings improve from 248 to 158, no hypoglycemia, self-injection and "
                             "glucometer use confirmed by the diabetes educator, primary care booked.",
                  "findings": [
                      {"rule": "GEN-1", "status": "met", "why": "Unhoused, needs a safe place to stabilize.", "docs": ["cm", "hp"]},
                      {"rule": "DM-1", "status": "met", "why": "Five consecutive readings: 248, 214, 186, 171, 158.", "docs": ["labs", "progress"]},
                      {"rule": "DM-3", "status": "met", "why": "Not a new regimen. Glargine for 3 years, restarted 08/10, more than 48 hours before admission.", "docs": ["hp", "meds", "progress"]},
                      {"rule": "DM-5", "status": "met", "why": "Demonstrated glucometer use.", "docs": ["consult"]},
                      {"rule": "DM-6", "status": "met", "why": "Demonstrated pen injection twice.", "docs": ["consult", "nursing"]},
                      {"rule": "COG-1", "status": "met", "why": "Self-administers insulin, confirmed.", "docs": ["consult", "nursing"]},
                      {"rule": "END-X3", "status": "met", "why": "Not in DKA: pH 7.38, anion gap 12, ketones normal.", "docs": ["hp", "labs"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 300 ft independently.", "docs": ["ptot"]},
                      {"rule": "INF-1", "status": "met", "why": "MRSA nares PCR not detected.", "docs": ["labs"]},
                      {"rule": "INF-2", "status": "met", "why": "COVID PCR not detected 08/12 12:40.", "docs": ["labs"]}],
                  "missing_documents": [], "follow_up": [], "contradictions": []},
    },

    # ---------------------------------------------------------------- S03 approve, wheelchair and staples
    {
        "id": "S03", "hospital": "lorh", "unit": "Orthopedic Unit 2B", "low_res_fax": True,
        "attending": "Elena Vasquez-Ruiz, DO", "cm": WHITFIELD,
        "patient": {"name": "WHITLOCK, GREGORY", "dob": "11/02/1978", "age": 47, "sex": "M",
                    "mrn": "SYN-318255", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-803164", "ssn4": "0000"},
        "dx": "Closed right bimalleolar ankle fracture, status post open reduction and internal fixation 08/18/2026",
        "icd": "S82.841A, Z59.02",
        "admit_dt": "08/17/2026 19:05", "refer_dt": "08/20/2026 10:12", "dc_dt": "08/21/2026", "arrival": "Ambulance",
        "cover_note": "Recuperative care referral. 47-year-old man, right ankle fracture repaired 08/18. Non-weight-bearing 6 weeks. "
                      "Uses a wheelchair and transfers on his own. Lives in a tent and cannot keep the leg dry or elevated. "
                      "Ready 08/21.",
        "docs": ["cover", "form", "face", "hp", "imaging", "progress", "ptot", "nursing", "vitals", "labs", "meds", "cm", "auth"],
        "form": {"flags": ["unhoused"], "wounds": "Y",
                 "wounds_explain": "2 surgical incisions, right ankle, closed with staples, under splint",
                 "wound_indep": "Y", "tb": "N", "o2": "N", "active_infection": "N", "self_meds": "Y", "ambulatory": "N",
                 "continent": "Y", "assistive": "Y", "colostomy": "N", "hospice": "N", "foley": "N", "car": "N",
                 "diabetes": "N", "service_animal": "N",
                 "explain": "Wheelchair. Non-weight-bearing right leg 6 weeks. Transfers independently",
                 "behavioral": "N", "los": "45"},
        "hp": {
            "cc": "Right ankle pain and deformity after a fall.",
            "hpi": "47-year-old man who stepped off a curb in the dark and twisted his right ankle. Immediate pain, swelling and "
                   "inability to bear weight. X-rays show a displaced bimalleolar fracture. Skin intact. Foot warm with normal "
                   "sensation and pulses. Reduced and splinted in the emergency department and admitted for surgery.\n\n"
                   "Addendum 08/18/2026: open reduction and internal fixation with plate and screws by orthopedic surgery. No "
                   "external fixator. Incisions closed with staples. Non-weight-bearing on the right leg for 6 weeks.",
            "pmh": ["No chronic medical conditions", "Tobacco use"], "psh": ["Right ankle open reduction and internal fixation, 08/18/2026"],
            "meds_home": [],
            "social": "Unhoused for about 2 years. Lives in a tent. Day labor when available. No alcohol in 5 years, no drug use. "
                      "He cannot keep the leg elevated or the splint dry where he stays.",
            "exam": {"Extremities": "Right lower leg in a padded short leg splint. Toes warm, capillary refill under 2 seconds, "
                                    "sensation intact, moves all toes.",
                     "Skin": "Closed fracture. No open wound before surgery."},
            "plan": ["Closed right bimalleolar ankle fracture: surgery 08/18. Non-weight-bearing right leg 6 weeks.",
                     "Clot prevention: aspirin 81 mg twice daily for 4 weeks.",
                     "Orthopedic follow-up in 2 weeks for wound check and staple removal.",
                     "Physical therapy for transfers and wheelchair skills. Case management for disposition."]},
        "imaging": [{"study": "X-ray right ankle, 3 views", "date": "08/17/2026 19:40", "indication": "Fall, ankle deformity.",
                     "findings": "Displaced fractures of the lateral and medial malleoli. Mild lateral shift of the talus. "
                                 "No dislocation. Soft tissue swelling. No gas in the soft tissues.",
                     "impression": "Displaced bimalleolar ankle fracture. Closed injury.", "rad": "S. Ferreira, MD"},
                    {"study": "X-ray right ankle, post-operative", "date": "08/18/2026 15:05", "indication": "After fixation.",
                     "findings": "Lateral plate with screws and two medial malleolar screws. Anatomic alignment of the ankle "
                                 "mortise. No hardware complication.",
                     "impression": "Satisfactory internal fixation. No external fixation device.", "rad": "S. Ferreira, MD"}],
        "progress": [
            {"date": "08/19/2026 08:30", "author": "Elena Vasquez-Ruiz, DO", "type": "Orthopedic Progress Note, post-op day 1",
             "text": "Pain controlled with oral medication. Splint clean, dry and intact. Toes warm, sensation intact. "
                     "Started aspirin for clot prevention. Physical therapy today."},
            {"date": "08/20/2026 08:15", "author": "Elena Vasquez-Ruiz, DO", "type": "Orthopedic Progress Note, post-op day 2",
             "text": "Doing well. Afebrile. Transfers to wheelchair on his own per therapy. Splint stays on until clinic. No "
                     "dressing changes needed before follow-up; keep the splint dry.\n\n"
                     "Orthopedic clinic 09/02/2026 09:15 for wound check and staple removal. Ready for discharge 08/21."}],
        "ptot": {"author": "Joel Marchetti, PT", "date": "08/19/2026 14:30",
                 "rows": [("Weight bearing", "Non-weight-bearing, right lower extremity"), ("Bed mobility", "Independent"),
                          ("Transfers", "Independent stand-pivot: bed to wheelchair, wheelchair to toilet, wheelchair to shower bench. 3 of 3 trials, keeps weight off the right leg"),
                          ("Wheelchair mobility", "Independent. Propels 300 ft on level ground, manages brakes and elevating leg rest"),
                          ("Ambulation", "15 ft hop-to with front-wheeled walker. Wheelchair is primary mobility"),
                          ("Balance", "Good sitting. Fair standing on the left leg"),
                          ("Assistive device", "Standard wheelchair with elevating right leg rest")],
                 "text": "Patient depends on a wheelchair for mobility while non-weight-bearing. He transfers independently and "
                         "safely and follows weight-bearing precautions without cues. He manages the wheelchair on his own.",
                 "rec": "Recuperative care or home with wheelchair. Outpatient physical therapy booked: Los Olivos Outpatient Rehab, 09/03/2026 13:00."},
        "nursing": {"author": "M. Delacroix, RN", "date": "08/20/2026 07:10",
                    "rows": adl(bathing="Independent using shower bench and splint cover", skin="Surgical incisions under splint. Splint clean, dry, intact",
                                fall="Moderate. Follows precautions"),
                    "text": "Transfers himself to the toilet and shower bench. No assistance needed."},
        "vitals": [["08/19/2026 16:00", "126/78", "76", "16", "98.4", "98%", "Room air"],
                   ["08/19/2026 20:00", "122/76", "74", "16", "98.6", "98%", "Room air"],
                   ["08/20/2026 00:00", "118/72", "68", "14", "98.2", "97%", "Room air"],
                   ["08/20/2026 04:00", "120/74", "70", "14", "98.0", "98%", "Room air"],
                   ["08/20/2026 08:00", "124/78", "72", "16", "98.3", "98%", "Room air"]],
        "labs": {"date": "08/19/2026 05:30", "override": {"Hemoglobin": "12.9", "Hematocrit": "38.6"},
                 "micro": [("MRSA nares PCR", "08/17/2026 21:10", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "08/20/2026 09:50", "NEGATIVE")]},
        "meds": [("Aspirin", "81 mg", "By mouth", "Twice daily", "For 28 days, clot prevention"),
                 ("Acetaminophen", "1000 mg", "By mouth", "Every 8 hours", "For pain"),
                 ("Oxycodone", "5 mg", "By mouth", "Every 6 hours as needed", "5 days, 20 tablets"),
                 ("Docusate", "100 mg", "By mouth", "Twice daily", "While taking oxycodone")],
        "meds_note": "30-day supply dispensed to bedside 08/20/2026, except oxycodone (5 days).",
        "cmnote": {"date": "08/20/2026 09:50",
                   "text": "Patient lives in a tent and has been unhoused about 2 years. He cannot keep a splint dry or use a "
                           "wheelchair where he stays. He wants recuperative care while he is non-weight-bearing. He manages his "
                           "own medications.",
                   "rows": [("Housing", "Unhoused about 2 years. Tent."),
                            ("Equipment", "Wheelchair with elevating leg rest delivered to bedside 08/20/2026. Patient showed he can use it."),
                            ("Follow-up", "Orthopedic clinic 09/02/2026 09:15, wound check and staple removal."),
                            ("Therapy", "Outpatient physical therapy 09/03/2026 13:00."),
                            ("Disposition", "Recuperative care referral faxed 08/20/2026."),
                            ("Health plan authorization", "Submitted 08/20/2026. Pending.")]},
        "truth": {"decision": "approve",
                  "summary": "Approve. Closed ankle fracture with internal fixation, no external fixator. Wheelchair dependent but "
                             "transfers and uses the chair independently. Staple removal and outpatient PT are both scheduled.",
                  "findings": [
                      {"rule": "GEN-1", "status": "met", "why": "Unhoused, cannot recover in a tent.", "docs": ["cm", "hp"]},
                      {"rule": "MSK-E1", "status": "met", "why": "Closed fracture.", "docs": ["hp", "imaging"]},
                      {"rule": "MSK-X3", "status": "met", "why": "Internal plate and screws. No external fixation device.", "docs": ["hp", "imaging"]},
                      {"rule": "MOB-4", "status": "met", "why": "Wheelchair dependent and transfers independently, 3 of 3 trials.", "docs": ["ptot"]},
                      {"rule": "MOB-1", "status": "met", "why": "Uses the wheelchair independently.", "docs": ["ptot", "cm"]},
                      {"rule": "MOB-2", "status": "met", "why": "PT evaluation included.", "docs": ["ptot"]},
                      {"rule": "INT-E5", "status": "met", "why": "Staple removal booked 09/02/2026.", "docs": ["progress", "cm"]},
                      {"rule": "MSK-E2", "status": "met", "why": "Outpatient PT booked 09/03/2026.", "docs": ["ptot", "cm"]},
                      {"rule": "ADL-2", "status": "met", "why": "Showers independently with a bench.", "docs": ["nursing", "ptot"]},
                      {"rule": "INF-1", "status": "met", "why": "MRSA nares PCR not detected.", "docs": ["labs"]},
                      {"rule": "INF-2", "status": "met", "why": "COVID antigen negative 08/20.", "docs": ["labs"]}],
                  "missing_documents": [], "follow_up": [], "contradictions": []},
    },

    # ---------------------------------------------------------------- S04 approve, pneumonia with COPD
    {
        "id": "S04", "hospital": "bumc", "unit": "5 Tower Pulmonary",
        "attending": "Samuel Oyelaran, MD", "cm": IMANI,
        "patient": {"name": "BENNING, HAROLD", "dob": "01/30/1960", "age": 66, "sex": "M",
                    "mrn": "SYN-407192", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-296481", "ssn4": "0000"},
        "dx": "Community-acquired pneumonia, right lower lobe, with COPD exacerbation", "icd": "J18.9, J44.0, J44.1, Z59.02",
        "admit_dt": "08/24/2026 06:32", "refer_dt": "08/27/2026 11:05", "dc_dt": "08/28/2026", "arrival": "Ambulance",
        "cover_note": "Recuperative care referral. 66-year-old man with pneumonia and COPD. Off oxygen since 08/26, on oral "
                      "antibiotics, walking on his own. No home oxygen needed. Unhoused. Ready 08/28.",
        "docs": ["cover", "form", "face", "auth", "hp", "imaging", "labs", "progress", "consult", "vitals", "ptot", "nursing", "meds", "cm"],
        "form": {"flags": ["unhoused"], "wounds": "N", "tb": "Y", "tb_date": "08/24/2026", "tb_result": "CXR: right lower lobe pneumonia",
                 "o2": "N", "active_infection": "Y", "self_meds": "Y", "ambulatory": "Y", "continent": "Y", "assistive": "N",
                 "colostomy": "N", "hospice": "N", "foley": "N", "car": "N", "diabetes": "N", "service_animal": "N",
                 "explain": "Pneumonia, improving on oral antibiotics. Off oxygen since 08/26", "behavioral": "N", "los": "30"},
        "hp": {
            "cc": "Cough, fever and shortness of breath for 4 days.",
            "hpi": "66-year-old man with COPD who presents with 4 days of productive cough, fever and worsening shortness of "
                   "breath. Temperature 101.8 F, oxygen saturation 88% on room air on arrival, improving to 94% on 2 liters by "
                   "nasal cannula. Chest X-ray shows a right lower lobe infiltrate.\n\n"
                   "Started ceftriaxone and azithromycin, nebulized bronchodilators and prednisone. Admitted to the pulmonary unit. "
                   "He does not use oxygen at home.",
            "pmh": ["COPD, moderate. FEV1 58% of predicted in 2025", "Hypertension", "Former smoker, quit 2023",
                    "Gastroesophageal reflux"], "psh": [],
            "meds_home": ["Tiotropium 18 mcg inhaled daily", "Albuterol inhaler, 2 puffs every 4 to 6 hours as needed",
                          "Amlodipine 5 mg by mouth daily"],
            "social": "Lost his apartment 5 months ago. Stays outdoors or in an emergency shelter when a bed is open. No alcohol "
                      "or drug use. Manages his own inhalers and pills.",
            "exam": {"General": "Awake, alert, mildly short of breath with talking.",
                     "Respiratory": "Crackles at the right base. Scattered expiratory wheezes. Speaking full sentences."},
            "plan": ["Right lower lobe pneumonia: ceftriaxone and azithromycin, change to oral when improving.",
                     "COPD exacerbation: nebulizers, prednisone 40 mg for 5 days, wean oxygen as tolerated.",
                     "Hypertension: continue amlodipine.", "Disposition: unhoused. Case management consult."]},
        "imaging": [{"study": "Chest X-ray, 2 views", "date": "08/24/2026 06:55", "indication": "Cough, fever, low oxygen.",
                     "findings": "Airspace consolidation in the right lower lobe. Hyperinflated lungs. No pleural effusion. "
                                 "No pneumothorax. Heart size normal.",
                     "impression": "Right lower lobe pneumonia. Changes of COPD.", "rad": "D. Okafor, MD"},
                    {"study": "Chest X-ray, 1 view", "date": "08/27/2026 07:20", "indication": "Follow-up pneumonia.",
                     "findings": "Right lower lobe consolidation is smaller and less dense than on 08/24. No effusion. No pneumothorax.",
                     "impression": "Improving right lower lobe pneumonia.", "rad": "D. Okafor, MD"}],
        "labs": {"date": "08/27/2026 05:15", "override": {"WBC": "9.1"}, "extra_title": "Trends and other results",
                 "extra": [("WBC", "08/24, 08/25, 08/27", "14.6, 12.0, 9.1 K/uL", "4.0-11.0"),
                           ("Procalcitonin", "08/24/2026 07:05", "1.8 ng/mL", "<0.25")],
                 "micro": [("Blood culture x2", "08/24/2026 07:10", "No growth at 72 hours"),
                           ("Sputum culture", "08/24/2026 08:30", "Normal respiratory flora"),
                           ("MRSA nares PCR", "08/24/2026 09:00", "NOT DETECTED"),
                           ("SARS-CoV-2, influenza, RSV PCR", "08/24/2026 07:00", "ALL NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "08/27/2026 10:15", "NEGATIVE")]},
        "progress": [
            {"date": "08/26/2026 09:30", "author": "Samuel Oyelaran, MD",
             "text": "Breathing easier. Off supplemental oxygen since 07:00 today. Saturation 94 to 96% at rest on room air. "
                     "Afebrile for 24 hours. Changed to oral amoxicillin-clavulanate. Completed 3 days of azithromycin."},
            {"date": "08/27/2026 09:10", "author": "Samuel Oyelaran, MD",
             "text": "Afebrile for 48 hours. Room air saturations 94 to 96% at rest and 93 to 94% walking. He does not need "
                     "and does not qualify for home oxygen. Using his inhalers correctly.\n\n"
                     "Ready for discharge 08/28 to finish antibiotics through 08/31. Last prednisone dose 08/28."}],
        "consult": [{"service": "Respiratory Therapy", "author": "Sofia Paredes, RRT", "date": "08/27/2026 10:40",
                     "reason": "Oxygen assessment and inhaler teaching before discharge.",
                     "text": "Breathing treatments this admission: albuterol-ipratropium by nebulizer every 6 hours through 08/26, "
                             "then changed to metered-dose inhaler with spacer.\n\n"
                             "Walking oximetry on room air: 95% at rest, 93% after walking 200 ft, back to 95% within one minute. "
                             "No oxygen needed at rest or with activity. Patient showed correct inhaler and spacer technique on "
                             "teach-back.",
                     "recs": ["No home oxygen.", "Continue tiotropium daily and albuterol as needed with spacer."]}],
        "vitals": [["08/26/2026 20:00", "132/80", "84", "18", "98.6", "95%", "Room air"],
                   ["08/27/2026 00:00", "128/78", "80", "18", "98.2", "94%", "Room air"],
                   ["08/27/2026 04:00", "126/76", "78", "16", "98.0", "95%", "Room air"],
                   ["08/27/2026 08:00", "130/80", "82", "18", "98.3", "96%", "Room air"],
                   ["08/27/2026 10:30", "134/82", "86", "18", "98.4", "95%", "Room air"]],
        "ptot": {"author": "Priscilla Nwosu, PT, DPT", "date": "08/26/2026 15:00",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "250 ft, independent, no device, one standing rest break"),
                          ("Balance", "Good"), ("Assistive device", "None")],
                 "text": "Mild shortness of breath with exertion that settles with a short rest. Safe and independent.",
                 "rec": "No PT follow-up needed."},
        "nursing": {"author": "L. Hartigan, RN", "date": "08/27/2026 07:15",
                    "rows": adl(medications="Uses own inhalers and takes own pills with RN observing"), "text": ""},
        "meds": [("Amoxicillin-clavulanate", "875/125 mg", "By mouth", "Twice daily", "Through 08/31/2026"),
                 ("Prednisone", "40 mg", "By mouth", "Daily", "Last dose 08/28/2026"),
                 ("Tiotropium", "18 mcg", "Inhaled", "Daily", "Home medication"),
                 ("Albuterol inhaler with spacer", "2 puffs", "Inhaled", "Every 4 to 6 hours as needed", "Home medication"),
                 ("Amlodipine", "5 mg", "By mouth", "Daily", "Home medication")],
        "meds_note": "30-day supply to bedside before discharge.",
        "cmnote": {"date": "08/27/2026 10:55",
                   "text": "Patient lost his apartment 5 months ago and has been outdoors or in emergency shelter since. He needs a "
                           "place to rest and finish antibiotics while his breathing recovers. Agreeable to recuperative care.",
                   "rows": [("Housing", "Unhoused 5 months."), ("Oxygen", "None needed. No equipment ordered."),
                            ("Follow-up", "Primary care 09/03/2026 14:00. Pulmonary clinic 09/17/2026."),
                            ("Disposition", "Recuperative care referral faxed 08/27/2026."),
                            ("Health plan authorization", "Submitted 08/27/2026. Pending.")]},
        "truth": {"decision": "approve",
                  "summary": "Approve. Pneumonia with COPD, off oxygen for more than 48 hours with room-air saturations of 94 to "
                             "96%, on oral antibiotics, independent. Chest imaging and respiratory therapy notes are included.",
                  "findings": [
                      {"rule": "GEN-1", "status": "met", "why": "Unhoused and recovering from pneumonia.", "docs": ["cm", "hp"]},
                      {"rule": "RSP-E1", "status": "met", "why": "Pneumonia is an eligible condition.", "docs": ["hp", "imaging"]},
                      {"rule": "RSP-E3", "status": "met", "why": "COPD, no oxygen needed at rest or walking.", "docs": ["consult", "progress"]},
                      {"rule": "RESP-1", "status": "met", "why": "Two chest X-ray reports included.", "docs": ["imaging"]},
                      {"rule": "RESP-2", "status": "met", "why": "Five sets of vitals, saturations stable 94 to 96% on room air.", "docs": ["vitals"]},
                      {"rule": "RESP-4", "status": "met", "why": "Respiratory therapy note included.", "docs": ["consult"]},
                      {"rule": "ID-2", "status": "met", "why": "Takes oral antibiotics himself.", "docs": ["nursing", "meds"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 250 ft independently.", "docs": ["ptot"]},
                      {"rule": "INF-1", "status": "met", "why": "MRSA nares PCR not detected.", "docs": ["labs"]},
                      {"rule": "INF-2", "status": "met", "why": "COVID antigen negative 08/27 10:15.", "docs": ["labs"]}],
                  "missing_documents": [], "follow_up": [], "contradictions": []},
    },

    # ---------------------------------------------------------------- S05 deny, mental health
    {
        "id": "S05", "hospital": "pcmc", "unit": "6 East Medical",
        "attending": "Priya Nandakumar, MD", "cm": LINDQVIST,
        "patient": {"name": "PRUITT, DWAYNE", "dob": "07/19/1987", "age": 39, "sex": "M",
                    "mrn": "SYN-118903", "language": "English", "ethnicity": "Black/African American",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-640257", "ssn4": "0000"},
        "dx": "Cellulitis of right hand", "icd": "L03.113, F25.0, Z59.02",
        "admit_dt": "08/29/2026 16:40", "refer_dt": "09/01/2026 09:30", "dc_dt": "09/01/2026",
        "cover_note": "Recuperative care referral. 39-year-old man with right hand cellulitis, improving on oral antibiotics. "
                      "Unhoused. Independent. History of schizoaffective disorder. Medically cleared.",
        "docs": ["cover", "form", "face", "hp", "cm", "auth", "labs", "vitals", "ptot", "progress", "nursing", "consult", "meds"],
        "form": {"flags": ["unhoused", "mh_dx"], "mh_dx": "Schizoaffective disorder, stable on meds", "wounds": "N",
                 "tb": "N", "o2": "N", "active_infection": "Y", "self_meds": "Y", "ambulatory": "Y", "continent": "Y",
                 "assistive": "N", "colostomy": "N", "hospice": "N", "foley": "N", "car": "N", "diabetes": "N",
                 "service_animal": "N", "explain": "Right hand cellulitis on oral antibiotics", "behavioral": "Y", "los": "30"},
        "hp": {
            "cc": "Swollen, red right hand for 2 days.",
            "hpi": "39-year-old man who cut the back of his right hand on a can lid 4 days ago. Two days of spreading redness and "
                   "swelling over the back of the hand. No fever. X-ray shows no foreign body or gas. No abscess on ultrasound. "
                   "Started IV ampicillin-sulbactam.\n\n"
                   "He has schizoaffective disorder, bipolar type, and says he stopped olanzapine about 2 months ago when he ran "
                   "out. On admission he is calm and cooperative and denies thoughts of harming himself or others.",
            "pmh": ["Schizoaffective disorder, bipolar type. Two prior psychiatric hospitalizations, most recent 2024"], "psh": [],
            "meds_home": ["Olanzapine 10 mg by mouth nightly (not taking for about 2 months)"],
            "social": "Unhoused for about 4 years. Sleeps near a rail yard. No current alcohol use. Smokes cigarettes.",
            "exam": {"Extremities": "Back of right hand red, warm and swollen to the wrist. 1 cm healing cut. Full finger motion "
                                    "with mild pain. No fluctuance.",
                     "Psych": "Calm and cooperative. Limited eye contact. Denies suicidal or homicidal thoughts."},
            "plan": ["Right hand cellulitis: IV ampicillin-sulbactam, elevate, hand checks.",
                     "Schizoaffective disorder, off medication: monitor. Psychiatry if symptoms emerge.",
                     "Disposition: unhoused. Case management consult."]},
        "cmnote": {"date": "08/30/2026 15:10",
                   "text": "Met with patient. Calm and pleasant. Unhoused about 4 years. Agreeable to recuperative care to finish "
                           "antibiotics. States he will take his medications. Referral form completed today.",
                   "rows": [("Housing", "Unhoused about 4 years."), ("Disposition", "Recuperative care referral prepared 08/30/2026. Faxed 09/01/2026."),
                            ("Medications", "Reports he can manage his own."),
                            ("Health plan authorization", "Submitted 09/01/2026. Pending.")]},
        "labs": {"date": "08/31/2026 05:20", "override": {"WBC": "8.2"}, "extra_title": "Trends",
                 "extra": [("WBC", "08/29, 08/31", "12.1, 8.2 K/uL", "4.0-11.0")],
                 "micro": [("MRSA nares PCR", "08/29/2026 18:20", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "09/01/2026 07:45", "NEGATIVE")]},
        "vitals": [["08/31/2026 12:00", "124/78", "88", "16", "98.4", "99%", "Room air"],
                   ["08/31/2026 16:00", "128/80", "92", "18", "98.6", "99%", "Room air"],
                   ["08/31/2026 20:00", "122/76", "86", "16", "98.2", "98%", "Room air"],
                   ["09/01/2026 00:00", "120/74", "84", "16", "98.0", "99%", "Room air"],
                   ["09/01/2026 06:00", "126/78", "82", "16", "98.3", "99%", "Room air"]],
        "ptot": {"author": "Brooke Tanaka, PT, DPT", "date": "08/30/2026 11:00", "title": "Physical Therapy Screen",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "300 ft, independent, no device"), ("Balance", "Good"), ("Assistive device", "None")],
                 "text": "No mobility deficits.", "rec": "No PT needs."},
        "progress": [
            {"date": "08/30/2026 09:20", "author": "Priya Nandakumar, MD",
             "text": "Hand redness improving. Afebrile. Changed to oral amoxicillin-clavulanate.\n\n"
                     "Nursing reports the patient was awake most of the night talking to someone who was not there. "
                     "Psychiatry consult requested."},
            {"date": "08/31/2026 15:05", "author": "Priya Nandakumar, MD",
             "text": "Hand continues to improve on oral antibiotics. Medically stable.\n\n"
                     "Seen by psychiatry this afternoon. See their note. One-to-one observation ordered at 14:20. Olanzapine "
                     "restarted tonight. Discharge to a community setting is on hold pending psychiatry."}],
        "nursing": {"author": "R. Vasquez, RN", "date": "08/31/2026 22:40",
                    "rows": adl(orientation="Alert and oriented x4. Distracted, responding to voices",
                                medications="Took first dose of olanzapine with encouragement",
                                fall="Low", isolation="None. One-to-one sitter at bedside for safety",
                                safety="Suicide risk screen POSITIVE 08/31/2026. See psychiatry note. One-to-one observation"),
                    "text": "Patient pacing and talking to himself. Says, 'He keeps telling me to do it.' Sitter remains at the "
                            "bedside. Belongings secured."},
        "consult": [{"service": "Psychiatry", "author": "Leonard Abiodun, MD", "date": "08/31/2026 14:30",
                     "reason": "Responding to internal stimuli. Off antipsychotic medication.",
                     "text": "Patient reports that for about 3 weeks he has heard a man's voice telling him to step in front of a "
                             "train and that he deserves to die. The voice has been louder since he stopped olanzapine. He says he "
                             "has thought about walking onto the tracks near where he sleeps and cannot promise that he would stay "
                             "safe if he left the hospital. He denies thoughts of harming others.\n\n"
                             "Mental status: disheveled, guarded, intermittently turning to respond to a voice. Speech soft. "
                             "Thought process tangential. Mood 'tired.' Affect flat. Insight and judgment poor.\n\n"
                             "Assessment: schizoaffective disorder, bipolar type, acute exacerbation, with command auditory "
                             "hallucinations and active suicidal ideation with a plan.",
                     "recs": ["One-to-one observation.", "Restart olanzapine 10 mg nightly and titrate.",
                              "Involuntary psychiatric hold started 08/31/2026 14:10.",
                              "Transfer to an inpatient psychiatric unit when medically cleared.",
                              "Not appropriate for discharge to a community setting at this time."]}],
        "meds": [("Amoxicillin-clavulanate", "875/125 mg", "By mouth", "Twice daily", "Through 09/05/2026"),
                 ("Olanzapine", "10 mg", "By mouth", "Nightly", "Restarted 08/31/2026")],
        "meds_note": "30-day supply to bedside before discharge.",
        "truth": {"decision": "deny",
                  "summary": "Deny. Psychiatry documented command auditory hallucinations and active suicidal ideation with a plan "
                             "on 08/31, started an involuntary hold and recommended inpatient psychiatric care. The referral form's "
                             "'stable on meds' was written the day before that consult.",
                  "findings": [
                      {"rule": "MH-2", "status": "not_met", "why": "Active suicidal ideation with a plan.", "docs": ["consult"]},
                      {"rule": "MH-3", "status": "not_met", "why": "Command auditory hallucinations telling him to harm himself.", "docs": ["consult", "nursing"]},
                      {"rule": "MH-1", "status": "not_met", "why": "Not stable on medication. Olanzapine restarted 08/31, on a hold with one-to-one observation.", "docs": ["consult", "progress"]},
                      {"rule": "INT-E1", "status": "met", "why": "The hand cellulitis itself would qualify.", "docs": ["hp", "progress"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 300 ft independently.", "docs": ["ptot"]}],
                  "missing_documents": [], "follow_up": [],
                  "contradictions": [{"documents": ["form", "consult"],
                                      "what": "The referral form and the 08/30 case management note describe him as stable and calm. The 08/31 psychiatry consult documents command hallucinations, suicidal ideation with a plan and an involuntary hold."}]},
    },

    # ---------------------------------------------------------------- S06 deny, stroke with deficits
    {
        "id": "S06", "hospital": "lorh", "unit": "Neuro Stepdown 3A",
        "attending": "Elena Vasquez-Ruiz, DO", "cm": WHITFIELD,
        "patient": {"name": "HENSLEY, LORRAINE", "dob": "03/08/1955", "age": 71, "sex": "F",
                    "mrn": "SYN-331740", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-118592", "ssn4": "0000"},
        "dx": "Acute ischemic stroke, left middle cerebral artery territory, with right-sided weakness",
        "icd": "I63.512, G81.91, Z59.02",
        "admit_dt": "09/02/2026 08:14", "refer_dt": "09/08/2026 14:02", "dc_dt": "09/09/2026", "arrival": "Ambulance",
        "cover_note": "Recuperative care referral. 71-year-old woman, stroke 09/02, medically stable. Walks with a walker. "
                      "Unhoused with no family. Rehab facilities have not accepted. Please consider.",
        "docs": ["cover", "form", "face", "hp", "imaging", "consult", "progress", "vitals", "labs", "nursing", "ptot", "meds", "cm", "auth"],
        "form": {"flags": ["unhoused"], "wounds": "N", "tb": "N", "o2": "N", "active_infection": "N", "self_meds": "Y",
                 "ambulatory": "Y", "continent": "Y", "assistive": "Y", "colostomy": "N", "hospice": "N", "foley": "N",
                 "car": "N", "diabetes": "N", "service_animal": "N", "explain": "Walker", "behavioral": "N", "los": "60"},
        "hp": {
            "cc": "Right-sided weakness and slurred speech.",
            "hpi": "71-year-old woman found by outreach workers with right arm and leg weakness and slurred speech. She was last "
                   "seen well more than 12 hours earlier, so clot-dissolving treatment was not given. CT head showed no bleeding. "
                   "MRI brain confirmed an acute infarct in the left middle cerebral artery territory.\n\n"
                   "Admitted to neuro stepdown. Started aspirin and high-intensity statin. Atrial fibrillation not seen on telemetry.",
            "pmh": ["Hypertension, untreated", "No prior stroke"], "psh": [], "meds_home": [],
            "social": "Unhoused for about 3 years. Sleeps in a doorway downtown. No family contacts. No alcohol or drug use.",
            "exam": {"Neuro": "Alert and oriented x4 with delayed responses. Mild expressive aphasia, word-finding pauses. "
                              "Right facial droop. Strength right arm 3 of 5, right leg 4-minus of 5, left side 5 of 5. "
                              "Right-sided sensory loss to light touch.",
                     "Extremities": "No edema. Right arm drifts downward when held out."},
            "plan": ["Acute left middle cerebral artery stroke: aspirin, atorvastatin 80 mg, telemetry, swallow screen.",
                     "Hypertension: start amlodipine after 48 hours.",
                     "Physical, occupational and speech therapy evaluations.", "Disposition per therapy recommendations."]},
        "imaging": [{"study": "MRI brain without contrast", "date": "09/02/2026 11:30", "indication": "Right-sided weakness.",
                     "findings": "Restricted diffusion in the left frontal and parietal lobes in the middle cerebral artery "
                                 "territory. No hemorrhage. No mass effect. Mild chronic small vessel changes.",
                     "impression": "Acute infarct, left middle cerebral artery territory.", "rad": "S. Ferreira, MD"}],
        "consult": [{"service": "Neurology", "author": "Hannah Whitcombe, MD", "date": "09/03/2026 10:10",
                     "reason": "Acute stroke.",
                     "text": "Left middle cerebral artery ischemic stroke. NIH Stroke Scale 8. Persistent right arm greater than "
                             "leg weakness and mild expressive aphasia. Likely cause is small vessel or large artery disease; "
                             "no atrial fibrillation captured. Echocardiogram shows no clot.",
                     "recs": ["Aspirin 81 mg daily and atorvastatin 80 mg nightly.", "Blood pressure goal under 140/90.",
                              "Intensive rehabilitation. Expect residual right-sided weakness."]}],
        "progress": [
            {"date": "09/07/2026 09:00", "author": "Elena Vasquez-Ruiz, DO",
             "text": "Neurologically stable. Right-sided weakness unchanged. Passed the swallow screen on 09/03; speech therapy is "
                     "following for word-finding difficulty. Needs help from one person to stand and to walk. "
                     "Therapy recommends acute inpatient rehabilitation or a skilled nursing facility.\n\n"
                     "Two facilities have declined because she has no discharge address. Case management is exploring other options."}],
        "vitals": [["09/07/2026 16:00", "138/84", "76", "16", "98.2", "97%", "Room air"],
                   ["09/07/2026 20:00", "134/82", "72", "16", "98.4", "97%", "Room air"],
                   ["09/08/2026 00:00", "130/78", "70", "14", "98.0", "96%", "Room air"],
                   ["09/08/2026 04:00", "132/80", "68", "14", "97.8", "97%", "Room air"],
                   ["09/08/2026 08:00", "136/82", "74", "16", "98.1", "97%", "Room air"]],
        "labs": {"date": "09/07/2026 05:30", "override": {},
                 "extra_title": "Other results", "extra": [("LDL cholesterol", "09/03/2026 05:40", "148 mg/dL", "<100"),
                                                           ("Hemoglobin A1C", "09/03/2026 05:40", "5.6 %", "<5.7")],
                 "micro": [("MRSA nares PCR", "09/02/2026 13:15", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "09/08/2026 13:10", "NEGATIVE")]},
        "nursing": {"author": "M. Delacroix, RN", "date": "09/08/2026 07:20",
                    "rows": adl(orientation="Alert and oriented x4, slow to answer. Word-finding difficulty",
                                bathing="Needs one person to help. Cannot wash or dry the right side",
                                dressing="Needs one person to help",
                                toileting="Needs one person to help with transfer and clothing. Incontinent of urine at night; staff change briefs",
                                feeding="Set-up help. Eats with left hand",
                                medications="RN administers. Cannot open bottles with right hand",
                                fall="High. Bed alarm on. Two near-falls this admission"),
                    "text": "Calls for help appropriately. Needs one-person assistance for every transfer."},
        "ptot": {"author": "Joel Marchetti, PT, and Nadia Farouk, OTR/L", "date": "09/06/2026 10:20",
                 "title": "Physical Therapy and Occupational Therapy Evaluation",
                 "rows": [("Bed mobility", "Minimal assistance"),
                          ("Transfers", "Moderate assistance of one person, sit to stand and bed to chair"),
                          ("Ambulation", "20 ft with hemi-walker and moderate assistance of one person. Right foot drags. Two losses of balance"),
                          ("Wheelchair mobility", "Cannot propel with right arm. Needs assistance"),
                          ("Bathing", "Moderate assistance"), ("Dressing", "Moderate assistance upper body, maximal assistance lower body"),
                          ("Toileting", "Minimal to moderate assistance for transfer and clothing"),
                          ("Communication", "Follows two-step commands. Mild expressive aphasia")],
                 "text": "Patient has significant right-sided weakness after stroke. She cannot walk, transfer, bathe, dress or "
                         "toilet without hands-on help. She is at high risk of falls. She is motivated and has good rehabilitation "
                         "potential.",
                 "rec": "Acute inpatient rehabilitation or skilled nursing facility. Not safe for a setting without hands-on assistance."},
        "meds": [("Aspirin", "81 mg", "By mouth", "Daily", "New"), ("Atorvastatin", "80 mg", "By mouth", "Nightly", "New"),
                 ("Amlodipine", "5 mg", "By mouth", "Daily", "New")],
        "meds_note": "30-day supply to bedside before discharge.",
        "cmnote": {"date": "09/08/2026 13:30",
                   "text": "Patient is unhoused with no family or contacts. Acute rehabilitation and one skilled nursing facility "
                           "declined for lack of a discharge address. A second skilled nursing referral is pending. Sending a "
                           "recuperative care referral as an alternative so she is not discharged to the street.",
                   "rows": [("Housing", "Unhoused about 3 years."), ("Rehabilitation referrals", "Declined by 2. One pending."),
                            ("Disposition", "Recuperative care referral faxed 09/08/2026."),
                            ("Health plan authorization", "Submitted 09/08/2026. Pending.")]},
        "truth": {"decision": "deny",
                  "summary": "Deny. Stroke with residual right-sided weakness. She needs one person's help to transfer, walks 20 ft "
                             "with assistance, and needs help bathing, dressing and toileting. Therapy recommends rehabilitation "
                             "or skilled nursing. The referral form says ambulatory and continent, which the therapy and nursing "
                             "notes contradict.",
                  "findings": [
                      {"rule": "NEU-X1", "status": "not_met", "why": "Stroke with residual deficit: right-sided weakness and aphasia.", "docs": ["hp", "consult", "ptot"]},
                      {"rule": "MOB-3", "status": "not_met", "why": "Walks 20 ft with moderate assistance, not 100 ft at modified independence.", "docs": ["ptot"]},
                      {"rule": "MOB-1", "status": "not_met", "why": "Cannot use the walker or a wheelchair without help.", "docs": ["ptot"]},
                      {"rule": "ADL-1", "status": "not_met", "why": "Needs hands-on help with bathing and dressing.", "docs": ["ptot", "nursing"]},
                      {"rule": "ADL-3", "status": "not_met", "why": "Needs help toileting; staff change briefs at night.", "docs": ["nursing", "ptot"]},
                      {"rule": "COG-1", "status": "not_met", "why": "Nurse administers medications; she cannot open bottles.", "docs": ["nursing"]}],
                  "missing_documents": [], "follow_up": [],
                  "contradictions": [{"documents": ["form", "ptot", "nursing"],
                                      "what": "The referral form marks ambulatory, continent and able to self-administer medications. The therapy evaluation and nursing assessment show she needs one-person assistance, is incontinent at night and has medications given by the nurse."}]},
    },

    # ---------------------------------------------------------------- S07 deny, C. diff on isolation
    {
        "id": "S07", "hospital": "sbch", "unit": "2 South Medical",
        "attending": "Thomas Achterberg, MD", "cm": ORTEGA,
        "patient": {"name": "KESSLER, BERNARD", "dob": "12/14/1967", "age": 58, "sex": "M",
                    "mrn": "SYN-245571", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-730946", "ssn4": "0000"},
        "dx": "Dehydration and acute kidney injury from diarrhea", "icd": "A04.72, E86.0, N17.9, Z59.02",
        "admit_dt": "09/05/2026 03:25", "refer_dt": "09/08/2026 10:48", "dc_dt": "09/09/2026", "arrival": "Ambulance",
        "cover_note": "Recuperative care referral. 58-year-old man admitted with dehydration. Kidney function back to normal. "
                      "Eating and walking. Unhoused. Ready 09/09.",
        "docs": ["cover", "face", "form", "auth", "hp", "progress", "vitals", "labs", "nursing", "ptot", "meds", "cm"],
        "form": {"flags": ["unhoused"], "wounds": "N", "tb": "N", "o2": "N", "active_infection": "N", "self_meds": "Y",
                 "ambulatory": "Y", "continent": "Y", "assistive": "N", "colostomy": "N", "hospice": "N", "foley": "N",
                 "car": "N", "diabetes": "N", "service_animal": "N", "behavioral": "N", "los": "30"},
        "hp": {
            "cc": "Watery diarrhea for 5 days, lightheaded.",
            "hpi": "58-year-old man with 5 days of watery diarrhea, 8 to 10 times a day, with cramping and lightheadedness. He "
                   "finished a course of clindamycin for a dental infection about 3 weeks ago. Blood pressure 92/58 and heart "
                   "rate 112 on arrival. Creatinine 2.1, up from a baseline of 1.0.\n\n"
                   "Given IV fluids. Stool sent for Clostridioides difficile testing. Placed on contact enteric precautions.",
            "pmh": ["Dental abscess, treated with clindamycin in August 2026", "Hypertension"], "psh": [],
            "meds_home": ["Hydrochlorothiazide 25 mg by mouth daily (held)"],
            "social": "Unhoused for about 1 year. Uses public restrooms. No alcohol or drug use.",
            "exam": {"General": "Tired, dry, in no distress.", "Abdomen": "Soft. Mild diffuse tenderness. Active bowel sounds. No guarding."},
            "plan": ["Diarrhea after antibiotics, suspect C. difficile: stool testing, contact enteric precautions, IV fluids.",
                     "Acute kidney injury from volume loss: IV fluids, hold hydrochlorothiazide, recheck daily.",
                     "Disposition: unhoused. Case management consult."]},
        "progress": [
            {"date": "09/05/2026 14:20", "author": "Thomas Achterberg, MD",
             "text": "Stool C. difficile toxin PCR positive. Started oral vancomycin 125 mg four times daily for 10 days. "
                     "Continue contact enteric precautions."},
            {"date": "09/08/2026 09:15", "author": "Thomas Achterberg, MD",
             "text": "Creatinine back to 1.0. Eating. Stool frequency down to 5 or 6 loose stools a day from 10. Day 4 of 10 of "
                     "oral vancomycin, to finish 09/15.\n\n"
                     "Remains on contact enteric precautions. Infection prevention will lift isolation 48 hours after diarrhea stops."}],
        "vitals": [["09/07/2026 16:00", "118/74", "84", "16", "98.6", "98%", "Room air"],
                   ["09/07/2026 20:00", "122/76", "80", "16", "98.4", "98%", "Room air"],
                   ["09/08/2026 00:00", "116/72", "78", "14", "98.2", "97%", "Room air"],
                   ["09/08/2026 04:00", "120/74", "76", "14", "98.0", "98%", "Room air"],
                   ["09/08/2026 08:00", "124/78", "80", "16", "98.3", "98%", "Room air"]],
        "labs": {"date": "09/08/2026 05:10", "override": {"WBC": "10.2", "Creatinine": "1.0", "BUN": "16", "Potassium": "3.8"},
                 "extra_title": "Trends", "extra": [("Creatinine", "09/05, 09/06, 09/08", "2.1, 1.4, 1.0 mg/dL", "0.6-1.3"),
                                                     ("WBC", "09/05, 09/08", "16.4, 10.2 K/uL", "4.0-11.0")],
                 "micro": [("C. difficile toxin B gene PCR, stool", "09/05/2026 04:10", "DETECTED"),
                           ("GI pathogen panel, stool", "09/05/2026 04:10", "No other pathogens detected"),
                           ("MRSA nares PCR", "09/05/2026 06:30", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "09/08/2026 10:05", "NEGATIVE")]},
        "nursing": {"author": "T. Okonkwo, RN", "date": "09/08/2026 07:05",
                    "rows": adl(toileting="Independent to bathroom. Urgency. 5 loose stools in the last 24 hours. Two episodes of incontinence on 09/07",
                                isolation="Contact enteric precautions for C. difficile since 09/05/2026. Not cleared"),
                    "text": "Private room. Gown and gloves for all entries. Patient taught hand washing with soap and water."},
        "ptot": {"author": "Andre Whitaker, PT", "date": "09/07/2026 13:00", "title": "Physical Therapy Screen",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "200 ft in room and hallway, independent, no device"), ("Balance", "Good"),
                          ("Assistive device", "None")],
                 "text": "No mobility deficits once rehydrated.", "rec": "No PT needs."},
        "meds": [("Vancomycin", "125 mg", "By mouth", "Four times daily", "Through 09/15/2026, for C. difficile"),
                 ("Hydrochlorothiazide", "25 mg", "By mouth", "Daily", "HOLD until primary care visit")],
        "meds_note": "30-day supply to bedside before discharge.",
        "cmnote": {"date": "09/08/2026 10:20",
                   "text": "Patient has been unhoused about a year and relies on public restrooms. He needs a place with a bathroom "
                           "to finish treatment. Agreeable to recuperative care.",
                   "rows": [("Housing", "Unhoused about 1 year."), ("Disposition", "Recuperative care referral faxed 09/08/2026."),
                            ("Follow-up", "Primary care 09/16/2026."), ("Health plan authorization", "Submitted 09/08/2026. Pending.")]},
        "truth": {"decision": "deny",
                  "summary": "Deny for now. C. difficile infection, toxin PCR positive 09/05, still having 5 to 6 loose stools a "
                             "day and on contact enteric isolation that has not been cleared. The referral form says no active "
                             "infection. He could be re-referred once isolation is lifted.",
                  "findings": [
                      {"rule": "GI-X3", "status": "not_met", "why": "C. difficile infection, on treatment day 4 of 10.", "docs": ["labs", "progress"]},
                      {"rule": "OTH-4", "status": "not_met", "why": "On contact enteric isolation, not cleared.", "docs": ["nursing", "progress"]},
                      {"rule": "FORM-X4", "status": "not_met", "why": "Active C. difficile infection not cleared.", "docs": ["labs", "nursing"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 200 ft independently.", "docs": ["ptot"]},
                      {"rule": "INF-1", "status": "met", "why": "MRSA nares PCR not detected.", "docs": ["labs"]}],
                  "missing_documents": [], "follow_up": ["When is isolation expected to be lifted? Re-refer after it is cleared."],
                  "contradictions": [{"documents": ["form", "labs", "nursing"],
                                      "what": "The referral form marks 'Active Infection: No' and the cover sheet does not mention C. difficile. The lab report shows a positive C. difficile PCR and nursing documents ongoing isolation."}]},
    },

    # ---------------------------------------------------------------- S08 deny, dementia
    {
        "id": "S08", "hospital": "bumc", "unit": "7 Tower Geriatrics",
        "attending": "Samuel Oyelaran, MD", "cm": IMANI,
        "patient": {"name": "DOMBROWSKI, WALTER", "dob": "06/01/1948", "age": 78, "sex": "M",
                    "mrn": "SYN-452608", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-905312", "ssn4": "0000"},
        "dx": "Urinary tract infection with confusion", "icd": "N39.0, G93.41, G30.9, F02.80, Z59.02",
        "admit_dt": "09/09/2026 22:10", "refer_dt": "09/12/2026 12:30", "dc_dt": "09/13/2026", "arrival": "Brought in by police",
        "cover_note": "Recuperative care referral. 78-year-old man treated for a urinary tract infection. Infection resolved. "
                      "Walks well without a device. Unhoused. Ready 09/13.",
        "docs": ["cover", "form", "face", "auth", "hp", "labs", "vitals", "ptot", "progress", "nursing", "consult", "meds", "cm"],
        "form": {"flags": ["unhoused", "forgetful"], "wounds": "N", "tb": "N", "o2": "N", "active_infection": "N",
                 "self_meds": "Y", "ambulatory": "Y", "continent": "Y", "assistive": "N", "colostomy": "N", "hospice": "N",
                 "foley": "N", "car": "N", "diabetes": "N", "service_animal": "N", "behavioral": "Y", "los": "30"},
        "hp": {
            "cc": "Found wandering and confused.",
            "hpi": "78-year-old man brought in by police after he was found walking in traffic. He could not say where he lived. "
                   "Temperature 100.9 F. Urinalysis consistent with infection. No other source found. CT head without acute findings.\n\n"
                   "Started IV ceftriaxone for a urinary tract infection with acute confusion. A former landlord reached by phone "
                   "reports memory problems for at least 2 years and that he was evicted after repeatedly leaving the stove on.",
            "pmh": ["Memory problems for at least 2 years by report, not previously evaluated", "Hypertension"], "psh": [],
            "meds_home": ["Unknown. Patient cannot name any medications"],
            "social": "Unhoused since an eviction about 6 months ago. No known family. Found with no identification or belongings.",
            "exam": {"Neuro": "Awake. Oriented to name only. Not oriented to place, date or situation. Follows one-step commands. "
                              "No focal weakness. Normal gait.",
                     "Psych": "Pleasant. Inattentive. Asks the same question repeatedly."},
            "plan": ["Urinary tract infection: ceftriaxone, follow urine culture.",
                     "Confusion: treat infection, reassess thinking once infection clears. Geriatrics consult.",
                     "Safety: wandering precautions.", "Disposition to follow cognitive evaluation."]},
        "labs": {"date": "09/12/2026 05:25", "override": {"WBC": "7.8"}, "extra_title": "Trends and other results",
                 "extra": [("WBC", "09/09, 09/12", "13.2, 7.8 K/uL", "4.0-11.0"),
                           ("Vitamin B12", "09/10/2026 05:30", "412 pg/mL", "200-900"),
                           ("TSH", "09/10/2026 05:30", "2.1 mIU/L", "0.4-4.5")],
                 "micro": [("Urine culture", "09/09/2026 22:40", "E. coli, more than 100,000 CFU/mL, sensitive to cephalosporins"),
                           ("MRSA nares PCR", "09/10/2026 06:00", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "09/12/2026 11:40", "NEGATIVE")]},
        "vitals": [["09/11/2026 16:00", "136/80", "72", "16", "98.2", "97%", "Room air"],
                   ["09/11/2026 20:00", "132/78", "70", "16", "98.0", "97%", "Room air"],
                   ["09/12/2026 00:00", "128/76", "68", "14", "97.8", "96%", "Room air"],
                   ["09/12/2026 04:00", "130/78", "66", "14", "97.9", "97%", "Room air"],
                   ["09/12/2026 08:00", "134/80", "70", "16", "98.1", "97%", "Room air"]],
        "ptot": {"author": "Priscilla Nwosu, PT, DPT", "date": "09/11/2026 10:30",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "200 ft, independent, no device, steady gait"), ("Balance", "Good"),
                          ("Assistive device", "None"), ("Safety awareness", "Poor. Walked toward the exit twice and needed redirection")],
                 "text": "Physically independent with walking and transfers. Mobility is not the limiting factor. He needs "
                         "supervision because he does not recognize hazards and tries to leave.",
                 "rec": "No physical therapy needs. Requires supervision for safety."},
        "progress": [
            {"date": "09/12/2026 11:50", "author": "Samuel Oyelaran, MD",
             "text": "Afebrile for 48 hours. Changed to oral cefpodoxime to finish 7 days. Urine culture E. coli, sensitive. Blood "
                     "pressure ran in the 150s over 90s on 09/10, so amlodipine 5 mg was started 09/11.\n\n"
                     "The acute confusion has cleared, but he remains disoriented at his baseline. Geriatrics evaluated today. "
                     "See their note. Infection is resolved; disposition depends on supervision needs."}],
        "nursing": {"author": "L. Hartigan, RN", "date": "09/12/2026 07:00",
                    "rows": adl(orientation="Oriented to name only. Thinks he is in a hotel. Does not know the year",
                                bathing="Needs step-by-step cueing. Does not start on his own",
                                dressing="Needs cueing. Puts clothes on in the wrong order",
                                toileting="Continent with prompting every 2 to 3 hours",
                                medications="RN administers all medications. Patient cannot name them or say what they are for",
                                fall="Moderate. Wanders. Bed and door alarms on"),
                    "text": "Found in another patient's room twice overnight. Easily redirected. Pleasant."},
        "consult": [{"service": "Geriatric Medicine", "author": "Ingrid Solheim, MD", "date": "09/12/2026 11:20",
                     "reason": "Cognitive evaluation after confusion cleared.",
                     "text": "Montreal Cognitive Assessment 14 of 30 today, after the infection was treated. Consistently oriented "
                             "to person only. Could not state the month, year or why he is in the hospital. Could not name his "
                             "medications or their purpose. On a four-compartment pill box task he placed 0 of 4 correctly.\n\n"
                             "History from his former landlord fits a gradual decline over at least 2 years. Assessment: major "
                             "neurocognitive disorder, probable Alzheimer type, moderate stage. He lacks the capacity to manage "
                             "medications or live without supervision.",
                     "recs": ["Needs 24-hour supervision. Memory care or skilled nursing level of care.",
                              "Start donepezil 5 mg nightly.",
                              "Adult Protective Services referral placed. Public guardian evaluation for conservatorship requested.",
                              "Not safe for a setting where residents manage their own medications."]}],
        "meds": [("Cefpodoxime", "200 mg", "By mouth", "Twice daily", "Through 09/16/2026"),
                 ("Donepezil", "5 mg", "By mouth", "Nightly", "New"), ("Amlodipine", "5 mg", "By mouth", "Daily", "New")],
        "meds_note": "30-day supply to bedside before discharge.",
        "cmnote": {"date": "09/12/2026 12:05",
                   "text": "Patient is unhoused with no family. He walks well and his infection is treated. Memory care placement "
                           "will take time. Sending a recuperative care referral so he has somewhere to go while placement and the "
                           "Adult Protective Services referral proceed.",
                   "rows": [("Housing", "Unhoused about 6 months."), ("Adult Protective Services", "Referral placed 09/12/2026."),
                            ("Conservatorship", "Public guardian evaluation requested 09/12/2026."),
                            ("Disposition", "Recuperative care referral faxed 09/12/2026."),
                            ("Health plan authorization", "Submitted 09/12/2026. Pending.")]},
        "truth": {"decision": "deny",
                  "summary": "Deny. Moderate dementia. Oriented to person only, cannot manage or name his medications, needs cueing "
                             "for hygiene and 24-hour supervision. He walks independently, so the mobility criteria alone would "
                             "pass. A conservatorship evaluation has also been requested, which touches the conservatorship rule.",
                  "findings": [
                      {"rule": "NEU-X5", "status": "not_met", "why": "Dementia, probable Alzheimer type, moderate.", "docs": ["consult"]},
                      {"rule": "COG-2", "status": "not_met", "why": "Oriented to person only, not AOx4.", "docs": ["consult", "nursing"]},
                      {"rule": "COG-1", "status": "not_met", "why": "Cannot self-administer medications; 0 of 4 on pill box task; nurse gives all doses.", "docs": ["consult", "nursing"]},
                      {"rule": "ADL-1", "status": "not_met", "why": "Needs cueing to bathe and dress.", "docs": ["nursing"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 200 ft independently.", "docs": ["ptot"]},
                      {"rule": "GU-E1", "status": "met", "why": "The urinary tract infection itself would qualify.", "docs": ["hp", "progress"]}],
                  "missing_documents": [], "follow_up": [],
                  "contradictions": [{"documents": ["form", "consult", "nursing"],
                                      "what": "The referral form marks 'Self Administer All Meds: Yes' and ticks only 'Forgetful', not 'Cognitive Impairment'. Geriatrics documents moderate dementia and inability to manage medications."}]},
    },

    # ---------------------------------------------------------------- S09 needs info, thin packet
    {
        "id": "S09", "hospital": "pcmc", "unit": "5 West Medical",
        "attending": "Priya Nandakumar, MD", "cm": BRANDT,
        "patient": {"name": "ROWLAND, TAMIKA", "dob": "04/27/1993", "age": 33, "sex": "F",
                    "mrn": "SYN-127364", "language": "English", "ethnicity": "Black/African American",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-381675", "ssn4": "0000"},
        "dx": "Abscess of right forearm with cellulitis, status post incision and drainage", "icd": "L02.413, L03.113, Z59.02",
        "admit_dt": "09/13/2026 18:52", "refer_dt": "09/15/2026 08:20", "dc_dt": "09/15/2026",
        "cover_note": "Recuperative care referral for today if possible. 33-year-old woman, forearm abscess drained 09/13, on oral "
                      "antibiotics. Unhoused. Independent. Remaining documents available on request.",
        "docs": ["cover", "face", "hp", "progress", "vitals", "cm"],
        "hp": {
            "cc": "Painful swelling of the right forearm for 4 days.",
            "hpi": "33-year-old woman with 4 days of a painful, enlarging lump on the inner right forearm with surrounding redness. "
                   "No fever. Exam shows a 3 cm fluctuant abscess with 4 cm of surrounding cellulitis.\n\n"
                   "Incision and drainage at the bedside on 09/13/2026 at 20:30. About 6 mL of pus drained. Wound culture sent. "
                   "Cavity packed with gauze. Admitted for IV antibiotics overnight because of the surrounding cellulitis.",
            "pmh": ["No chronic medical conditions"], "psh": [], "meds_home": [],
            "social": "Unhoused for about 10 months. Sleeps in a park. Denies injection drug use. Walks and cares for herself "
                      "independently.",
            "exam": {"Extremities": "Right inner forearm: 3 cm fluctuant, tender swelling with 4 cm of surrounding redness. "
                                    "After drainage: 1.5 cm incision, packed. Hand strength and sensation normal.",
                     "Neuro": "Alert and oriented x4. Walks without difficulty."},
            "plan": ["Right forearm abscess with cellulitis: drained 09/13. IV antibiotics overnight, then oral.",
                     "Wound culture pending.", "Packing change and wound check in 48 hours.",
                     "Disposition: unhoused. Case management consult."]},
        "progress": [
            {"date": "09/15/2026 07:10", "author": "Priya Nandakumar, MD",
             "text": "Afebrile. Redness receding. Pain controlled. Changed to oral trimethoprim-sulfamethoxazole yesterday evening. "
                     "Dressing dry. Wound culture still pending.\n\n"
                     "Plan discharge today. Needs packing change and wound check 09/16."}],
        "vitals": [["09/14/2026 20:05", "118/74", "82", "16", "98.8", "99%", "Room air"],
                   ["09/15/2026 06:30", "116/72", "76", "16", "98.3", "99%", "Room air"]],
        "vitals_note": "Two sets shown. Complete flowsheet available from the unit.",
        "cmnote": {"date": "09/15/2026 07:50",
                   "text": "Patient is unhoused and sleeps in a park. She has no way to keep the wound clean or get the packing "
                           "changed. She is interested in recuperative care. Sending the referral now so she is not delayed; the "
                           "rest of the chart can follow.",
                   "rows": [("Housing", "Unhoused about 10 months."),
                            ("Wound follow-up", "Packing change due 09/16/2026. Location not yet arranged."),
                            ("Medications", "Prescription sent to outpatient pharmacy. Not yet filled."),
                            ("Disposition", "Recuperative care referral faxed 09/15/2026 08:20."),
                            ("Health plan authorization", "Not yet submitted.")]},
        "truth": {"decision": "needs_info",
                  "summary": "Cannot decide yet. What is in the packet points to an eligible patient, but most of the required "
                             "documents are missing: no referral form, no authorization, no medication list, no PT/OT or nursing "
                             "notes, only two sets of vitals, no MRSA or COVID swab, culture pending, and no wound care arranged "
                             "for a packing change due 09/16.",
                  "findings": [
                      {"rule": "GEN-1", "status": "met", "why": "Unhoused and cannot care for the wound outdoors.", "docs": ["cm", "hp"]},
                      {"rule": "INT-E1", "status": "met", "why": "Drained abscess with cellulitis, now on oral antibiotics.", "docs": ["hp", "progress"]},
                      {"rule": "INF-1", "status": "unknown", "why": "No MRSA swab result in the packet.", "docs": []},
                      {"rule": "INF-2", "status": "unknown", "why": "No COVID swab result in the packet.", "docs": []},
                      {"rule": "ID-1", "status": "unknown", "why": "Only two sets of vitals sent; five are required.", "docs": ["vitals"]},
                      {"rule": "MOB-2", "status": "unknown", "why": "No PT/OT or nursing notes sent.", "docs": []},
                      {"rule": "INT-E2", "status": "unknown", "why": "Packing change due within 48 hours; no wound care arranged.", "docs": ["cm", "progress"]}],
                  "missing_documents": ["DOC-1", "DOC-3", "DOC-7", "DOC-8", "DOC-9", "DOC-10"],
                  "follow_up": ["Send the completed IHH referral form.",
                                "Send the last five sets of vital signs.",
                                "Send MRSA and COVID swab results.",
                                "Send the medication list and confirm a 30-day supply will come with her.",
                                "Send PT/OT or nursing notes showing she is independent.",
                                "Send the wound culture result when final.",
                                "Who will do the packing change on 09/16, and has that been scheduled?",
                                "Has the health plan authorization been submitted?"],
                  "contradictions": []},
    },

    # ---------------------------------------------------------------- S10 needs info, wound care not arranged
    {
        "id": "S10", "hospital": "lorh", "unit": "Medical Unit 4C",
        "attending": "Elena Vasquez-Ruiz, DO", "cm": WHITFIELD,
        "patient": {"name": "ARCENEAUX, PHILLIP", "dob": "09/30/1963", "age": 62, "sex": "M",
                    "mrn": "SYN-339018", "language": "English", "ethnicity": "White",
                    "insurance": "Medi-Cal managed care plan", "member_id": "SYN-M-574203", "ssn4": "0000"},
        "dx": "Sepsis from pneumonia, resolved; stage 3 pressure injury of the sacrum", "icd": "A41.9, J18.9, L89.153, Z59.02",
        "admit_dt": "09/04/2026 13:40", "refer_dt": "09/18/2026 11:35", "dc_dt": "09/19/2026", "arrival": "Ambulance",
        "cover_note": "Recuperative care referral. 62-year-old man recovering from a long hospital stay for pneumonia with sepsis. "
                      "Infection resolved. Walks with a walker on his own. Has a sacral pressure wound that needs dressing "
                      "changes. Unhoused. Ready 09/19.",
        "docs": ["cover", "form", "face", "auth", "hp", "imaging", "progress", "consult", "ptot", "nursing", "vitals", "labs", "meds", "cm"],
        "imaging": [{"study": "Chest X-ray, 2 views", "date": "09/15/2026 08:10", "indication": "Follow-up pneumonia after sepsis.",
                     "findings": "Patchy airspace opacities in both lower lobes are much smaller than on 09/04. No pleural effusion. "
                                 "No pneumothorax. Breathing tube has been removed.",
                     "impression": "Resolving multilobar pneumonia.", "rad": "S. Ferreira, MD"}],
        "form": {"flags": ["unhoused"], "wounds": "Y", "wounds_explain": "1 wound, sacrum and coccyx, 3.0 x 2.5 cm, stage 3",
                 "wound_indep": "N", "hh_ordered": "Y", "tb": "Y", "tb_date": "09/04/2026", "tb_result": "CXR: pneumonia",
                 "o2": "N", "active_infection": "N", "self_meds": "Y", "ambulatory": "Y", "continent": "Y", "assistive": "Y",
                 "colostomy": "N", "hospice": "N", "foley": "N", "car": "N", "diabetes": "N", "service_animal": "N",
                 "explain": "Front-wheeled walker", "behavioral": "N", "los": "45"},
        "hp": {
            "cc": "Fever, cough and confusion.",
            "hpi": "62-year-old man brought by ambulance with fever, cough and low blood pressure. Chest X-ray showed multilobar "
                   "pneumonia. He needed a breathing tube and blood pressure support and was in intensive care from 09/04 to "
                   "09/10, on a ventilator for 4 days.\n\n"
                   "Addendum 09/16/2026: breathing tube out 09/08. Transferred to the medical unit 09/10. Antibiotics finished "
                   "09/14. A pressure injury over the sacrum and coccyx was first noted on 09/09 after prolonged bed rest and is now stage 3.",
            "pmh": ["No known chronic conditions before this admission"], "psh": [], "meds_home": [],
            "social": "Unhoused for about 18 months. Stays at an encampment. Drinks 2 to 3 beers a few times a week. No drug use.",
            "exam": {"General": "Critically ill on arrival. See addendum for current status.",
                     "Cardiovascular": "Fast heart rate. Blood pressure low on arrival.",
                     "Respiratory": "Fast, labored breathing. Coarse breath sounds in both lungs.",
                     "Neuro": "Confused on arrival. Oriented to name only. Moves all limbs.",
                     "Psych": "Unable to assess on arrival.",
                     "Skin": "On 09/16: stage 3 pressure injury over the sacrum. See wound care note."},
            "plan": ["Septic shock from pneumonia: resolved. Antibiotics complete.",
                     "Deconditioning after critical illness: physical therapy.",
                     "Stage 3 sacral pressure injury: wound care nurse following.", "Disposition: unhoused. Case management consult."]},
        "progress": [
            {"date": "09/17/2026 09:20", "author": "Elena Vasquez-Ruiz, DO",
             "text": "Afebrile, off antibiotics for 3 days. Breathing comfortably on room air with no breathing treatments since "
                     "09/11; respiratory therapy has signed off. Eating well. Walking with a front-wheeled walker.\n\n"
                     "The sacral wound is clean and healing but needs skilled dressing changes after discharge. He cannot reach "
                     "it himself. Home health wound care to be arranged before discharge."}],
        "consult": [{"service": "Wound Care", "author": "Trevor Halloran, RN, CWOCN", "date": "09/17/2026 13:10",
                     "reason": "Sacral pressure injury.",
                     "text": "Stage 3 pressure injury over the sacrum and coccyx, 3.0 x 2.5 x 0.5 cm. Wound bed 90% red granulation "
                             "tissue. No undermining or tunneling. Small amount of clear drainage. No odor. Surrounding skin intact. "
                             "No signs of infection.\n\n"
                             "The patient cannot see or reach the wound and cannot change the dressing himself.",
                     "recs": ["Cleanse with saline, apply hydrofiber and a foam border dressing. Change daily and when soiled.",
                              "Skilled nursing wound care after discharge. First visit within 24 hours of discharge.",
                              "Offload: turn side to side in bed, use a pressure-relief cushion when sitting."]}],
        "ptot": {"author": "Joel Marchetti, PT", "date": "09/17/2026 10:45",
                 "rows": [("Bed mobility", "Independent"), ("Transfers", "Independent"),
                          ("Ambulation", "150 ft with front-wheeled walker, modified independent, one standing rest break"),
                          ("Balance", "Fair. Safe with walker"), ("Assistive device", "Front-wheeled walker. Uses it correctly without cues")],
                 "text": "Deconditioned after critical illness but improving daily. Safe and independent with a walker.",
                 "rec": "Recuperative care with a walker. Home health physical therapy if available."},
        "nursing": {"author": "M. Delacroix, RN", "date": "09/18/2026 07:15",
                    "rows": adl(bathing="Independent with shower chair", skin="Stage 3 sacral pressure injury. Dressing clean, dry, intact",
                                fall="Moderate. Uses walker"),
                    "text": "Turns himself in bed. Uses cushion in chair."},
        "vitals": [["09/17/2026 16:00", "122/76", "78", "16", "98.2", "97%", "Room air"],
                   ["09/17/2026 20:00", "118/74", "76", "16", "98.4", "97%", "Room air"],
                   ["09/18/2026 00:00", "116/72", "72", "14", "98.0", "96%", "Room air"],
                   ["09/18/2026 04:00", "118/72", "70", "14", "97.9", "97%", "Room air"],
                   ["09/18/2026 08:00", "124/78", "76", "16", "98.1", "97%", "Room air"]],
        "labs": {"date": "09/17/2026 05:20", "override": {"WBC": "8.4", "Hemoglobin": "10.8", "Hematocrit": "33.1"},
                 "extra_title": "Other results", "extra": [("Albumin", "09/17/2026 05:20", "3.1 g/dL", "3.5-5.0"),
                                                           ("Prealbumin", "09/17/2026 05:20", "16 mg/dL", "18-38")],
                 "micro": [("Blood culture x2", "09/04/2026 14:00", "Streptococcus pneumoniae; repeat 09/06 no growth"),
                           ("MRSA nares PCR", "09/04/2026 15:30", "NOT DETECTED"),
                           ("SARS-CoV-2 antigen", "09/18/2026 10:50", "NEGATIVE")]},
        "meds": [("Multivitamin", "1 tablet", "By mouth", "Daily", "New"), ("Vitamin C", "500 mg", "By mouth", "Twice daily", "Wound healing"),
                 ("Acetaminophen", "650 mg", "By mouth", "Every 6 hours as needed", "For pain")],
        "meds_note": "30-day supply to bedside before discharge. Dressing supplies for 3 days will be sent with the patient.",
        "cmnote": {"date": "09/18/2026 11:10",
                   "text": "Patient is unhoused and recovering from critical illness. He needs daily dressing changes to a sacral "
                           "wound he cannot reach. Home health referral for skilled nursing wound care was faxed to two agencies "
                           "today at 10:05. Neither has accepted yet. No start-of-care date.",
                   "rows": [("Housing", "Unhoused about 18 months."),
                            ("Home health", "Referral sent 09/18/2026 to two agencies. NOT yet accepted. Start-of-care date: to be determined."),
                            ("Equipment", "Front-wheeled walker and pressure-relief cushion delivered 09/17/2026."),
                            ("Disposition", "Recuperative care referral faxed 09/18/2026."),
                            ("Health plan authorization", "Submitted 09/18/2026. Pending.")]},
        "truth": {"decision": "needs_info",
                  "summary": "Hold for one answer. He meets the mobility, self-care and infection-control criteria. A stage 3 "
                             "sacral pressure injury is eligible only when wound care is coordinated and scheduled before "
                             "admission. Home health was requested on 09/18 but no agency has accepted and there is no start date.",
                  "findings": [
                      {"rule": "INT-E6", "status": "unknown", "why": "Stage 3 pressure injury. Wound care is requested but not yet scheduled.", "docs": ["cm", "consult"]},
                      {"rule": "INT-E2", "status": "unknown", "why": "Hard-to-reach wound needing daily dressing changes; first visit must be within 24 hours of discharge; no agency confirmed.", "docs": ["consult", "cm"]},
                      {"rule": "GEN-1", "status": "met", "why": "Unhoused, recovering from critical illness.", "docs": ["cm", "hp"]},
                      {"rule": "MOB-3", "status": "met", "why": "Walks 150 ft with walker, modified independent.", "docs": ["ptot"]},
                      {"rule": "MOB-1", "status": "met", "why": "Uses the walker correctly without cues.", "docs": ["ptot"]},
                      {"rule": "ADL-1", "status": "met", "why": "Independent with bathing, dressing, toileting.", "docs": ["nursing"]},
                      {"rule": "INF-1", "status": "met", "why": "MRSA nares PCR not detected.", "docs": ["labs"]},
                      {"rule": "INF-2", "status": "met", "why": "COVID antigen negative 09/18.", "docs": ["labs"]}],
                  "missing_documents": [],
                  "follow_up": ["Which home health agency has accepted the wound care referral?",
                                "What is the start-of-care date? The first dressing change must happen within 24 hours of discharge."],
                  "contradictions": []},
    },
]
