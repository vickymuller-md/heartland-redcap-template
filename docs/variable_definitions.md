---
title: "HEARTLAND Protocol — REDCap Variable Definitions"
subtitle: "Codebook for `heartland_data_dictionary.csv` (v1.0.0)"
author: "Vicky Muller Ferreira, MD"
date: "2026-04-16"
---

# Overview

This codebook documents every field in the HEARTLAND REDCap instrument template. For each field you will find: REDCap variable name, form, field type, units/range, clinical definition, and the HEARTLAND Protocol v3.3 reference.

Companion file: `instruments/heartland_data_dictionary.csv` — the machine-readable data dictionary that produces this codebook.

Cutoffs and weighted points for the HEARTLAND Risk Score reproduce **Table 1 of Protocol v3.3** (Zenodo DOI 10.5281/zenodo.18566403; published in *Cureus* 2026).

---

# Form 1 — Enrollment (`enrollment`)

| Variable | Type | Range | Definition | Ref |
|-|-|-|-|-|
| `record_id` | auto | integer | REDCap record identifier, auto-assigned on import | — |
| `enr_date` | date | YYYY-MM-DD | Date patient was enrolled in the HEARTLAND cohort | Module 1 |
| `consent_date` | date | YYYY-MM-DD | Date of signed informed consent | Module 1 |
| `facility_name` | text | free text (PHI if site is identifiable) | Enrolling facility | Module 2 |
| `facility_cah` | yesno | Y / N | Designated Critical Access Hospital (CMS CAH program) | Module 2 |
| `facility_tier` | radio | 1 / 2 / 3 | Implementation tier (Tier 1 Minimal, Tier 2 Standard, Tier 3 Advanced) | Protocol Table 2 |
| `state` | text | 2-letter US state | Facility US state code | Module 2 |
| `county_fips` | text | 5-digit | County FIPS code for geographic analysis | Module 2 |
| `rural_urban` | radio | 1-4 | USDA Rural-Urban Commuting Area category collapsed to Metro / Micro / Small-town / Rural | Module 2 |
| `age` | integer | 18-110 years | Age in completed years at enrollment | Demographics |
| `sex` | radio | Male / Female / Other | Sex at birth as documented in the medical record | Demographics |
| `race` | checkbox | NIH categories | Race — check all that apply (NIH categories) | Demographics |
| `ethnicity` | radio | Hispanic / Not / Unknown | Ethnicity per NIH categories | Demographics |

---

# Form 2 — Baseline Assessment (`baseline`)

This form captures the **10 HEARTLAND Risk Variables** (Protocol v3.3 Table 1). The risk score is **0-18 points weighted** (not a simple binary sum). Three tiers drive monitoring intensity: Low 0-4, Moderate 5-8, High ≥9.

## Risk variables (10)

| Variable | Rule → Points |
|-|-|
| `age` (from enrollment) | +2 if ≥75 |
| `bl_prior_hf_hosp_6mo` | +3 if prior HF hospitalization within last 6 months |
| `bl_egfr` | +2 if <45 mL/min/1.73 m² |
| `bl_np_type` + `bl_np_value` | +2 if BNP ≥500 OR NT-proBNP ≥1500 pg/mL |
| `bl_sbp_admit` | +2 if admission systolic BP <100 mmHg |
| `bl_diabetes` | +1 if diabetes mellitus |
| `bl_lvef_pct` | +2 if LVEF <30% |
| `bl_ckm_stage` | +2 if AHA CKM Stage 3 or 4 |
| `bl_distance_cardio_mi` | +1 if distance to nearest cardiologist >50 miles |
| `bl_social_support_limited` | +1 if lives alone OR limited social support |

## Calculated fields

- `bl_risk_score` (calc, 0-18): weighted sum using the REDCap formula embedded in the data dictionary.
- `bl_risk_tier` (text + `@CALCTEXT`): `"low"` if <5, `"moderate"` if 5-8, `"high"` if ≥9.

## Supporting baseline fields

| Variable | Definition |
|-|-|
| `bl_lvef_category` | HFrEF (≤40%) / HFmrEF (41-49%) / HFpEF (≥50%) — drives GDMT branching |
| `bl_enrichd_score` | Optional 7-item ENRICHD Social Support Scale total (range 7-35); ≤19 suggests limited support (Mitchell et al., 2003) |
| `bl_pro_consent` | Gate for KCCQ-12 fields on monthly follow-up and outcomes forms |

---

# Form 3 — GDMT Status (`gdmt_status`)

Captures current heart-failure guideline-directed medical therapy. For HFrEF, the four foundational classes (Protocol Module 4): RAS inhibitor (preferably ARNI), beta-blocker, MRA, SGLT2 inhibitor. HFpEF-specific fields branch on `bl_lvef_category = HFpEF`.

## RAS inhibitor (`gdmt_arni_acei_arb_*`)
Drug (ARNI / ACEi / ARB), total daily dose (mg), site-specified target (protocol default sacubitril/valsartan 97/103 BID = 200 mg/day), start date. Fields suppressed when drug = `None`.

## Beta-blocker (`gdmt_bb_*`)
Carvedilol, metoprolol succinate, or bisoprolol. Protocol target: carvedilol 25 mg BID (50 mg BID if >85 kg).

## MRA (`gdmt_mra_*`)
Spironolactone, eplerenone, or finerenone. Finerenone indicated for HFpEF with CKD (FINEARTS-HF). Target dose spironolactone 25-50 mg/day.

## SGLT2 inhibitor (`gdmt_sglt2_*`)
Dapagliflozin 10 mg or empagliflozin 10 mg (no titration). Safety gate: eGFR >20.

## HFpEF-specific
- `gdmt_hfpef_glp1`: GLP-1 RA (e.g., semaglutide) — STEP-HFpEF indication if BMI ≥30 (HFpEF only).

## Summary
- `gdmt_classes_count` (calc, 0-4): number of the four HFrEF classes currently prescribed (non-zero drug selected).
- `gdmt_generic_bridge`: Y if patient is on the $4 generic bridge (ACE-I + BB + spironolactone) while pursuing optimal agents.
- `gdmt_init_tier`: site's initiation strategy — Tier 1 (≥2 classes before discharge, prioritize SGLT2i + BB), Tier 2 (all tolerated, uptitrate 2-4 wk), Tier 3 (rapid-sequence per STRONG-HF).

---

# Form 4 — Monthly Follow-up (`monthly_followup`, repeating instrument, months 1-12)

## Encounter metadata
| Variable | Definition |
|-|-|
| `mo_event_number` | 1-12 — month number |
| `mo_date` | Visit / contact date |
| `mo_track` | A (digital: Bluetooth + app) vs B (analog: paper diary + phone). Assigned at enrollment; can switch. |

## Vitals (all tracks)
`mo_weight_lb` (50-600), `mo_sbp` (60-250), `mo_dbp` (30-150), `mo_hr` (30-200), `mo_spo2` (50-100).

## Labs (optional — "if available")
`mo_egfr`, `mo_k` (K⁺ mEq/L), `mo_bnp` — quarterly if available. Labs are not required for protocol adherence.

## GDMT & events
- `mo_gdmt_change` (Y/N): any change this month (titration, discontinuation, new agent).
- `mo_gdmt_change_notes`: free text, gated by `mo_gdmt_change = 1`.
- `mo_red_flag_count`: count of red-flag events.
- `mo_red_flag_types` (checkbox, gated if count > 0): weight gain, orthopnea, PND, edema, syncope, angina, arrhythmia, other.
- `mo_hosp_any`, `mo_hosp_hf` (gated on any=Y), `mo_ed_any`, `mo_ed_hf` (gated on any=Y).

## Patient-reported outcomes (consent-gated)
`mo_kccq12_score` (0-100): KCCQ-12 summary. Shown only when `bl_pro_consent = Yes`.

---

# Form 5 — Outcomes at 12 Months (`outcomes_12mo`)

## Primary endpoint
- `out_vital_status`: Alive / Deceased / Lost to follow-up.

## Secondary endpoints
| Variable | Definition |
|-|-|
| `out_death_date` | Date of death (if deceased) |
| `out_death_cardiovascular` | Cardiovascular cause of death (Y/N) |
| `out_hf_hosp_count` | HF hospitalizations in 12 months |
| `out_hf_ed_count` | HF-related ED visits in 12 months |
| `out_days_alive_oh` | Days alive and out of hospital (0-365) |
| `out_gdmt_optimized` | Y if ≥3 HFrEF classes at target dose at 12 months |
| `out_kccq12_12mo` | KCCQ-12 at 12 months (consent-gated) |

---

# Branching logic summary

| Condition | Fields gated |
|-|-|
| `bl_lvef_category = "HFpEF"` | `gdmt_hfpef_glp1` |
| `bl_pro_consent = 1` | `mo_kccq12_score`, `out_kccq12_12mo` |
| `mo_gdmt_change = 1` | `mo_gdmt_change_notes` |
| `mo_red_flag_count > 0` | `mo_red_flag_types` |
| `mo_hosp_any = 1` | `mo_hosp_hf` |
| `mo_ed_any = 1` | `mo_ed_hf` |
| `out_vital_status = 2` | `out_death_date`, `out_death_cardiovascular` |
| Drug selector ≠ `0 (None)` | Associated dose / target / start-date fields per class |

# Calculated fields summary

| Variable | Formula source |
|-|-|
| `bl_risk_score` | Sum of 10 weighted indicator rules (Protocol Table 1) |
| `bl_risk_tier` | `@CALCTEXT` over `bl_risk_score`: <5 low / 5-8 moderate / ≥9 high |
| `gdmt_classes_count` | Count of non-None drug selections across RAS / BB / MRA / SGLT2 |

---

# Data-integrity notes

- Field names follow REDCap conventions (lowercase, underscores, ≤26 chars).
- The `record_id` column is REDCap's mandatory primary key.
- Repeating instrument (`monthly_followup`) must be enabled in the target project's Project Setup after import.
- Sample data in `examples/sample_data.csv` is fully synthetic (no real patients).

# References

- Ferreira VM. *HEARTLAND Protocol v3.3: Heart failure Evidence-based Access in Rural Treatment, Linking Advanced Network Delivery.* Cureus. 2026. DOI 10.5281/zenodo.18566403.
- Mitchell PH, Powell L, Blumenthal J, et al. *A short social support measure for patients recovering from myocardial infarction: the ENRICHD Social Support Inventory.* J Cardiopulm Rehabil. 2003;23(6):398-403.
- Solomon SD, et al. *Finerenone in HFpEF* (FINEARTS-HF). N Engl J Med. 2024.
- Mebazaa A, et al. *Safety, tolerability and efficacy of up-titration of guideline-directed medical therapies for acute heart failure* (STRONG-HF). Lancet. 2022;400:1938-52.
