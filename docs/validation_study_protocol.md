---
title: "HEARTLAND Protocol — Suggested Validation Study Design"
subtitle: "A reference protocol for sites adopting `heartland-redcap-template`"
author: "Vicky Muller Ferreira, MD"
date: "2026-04-16"
---

# 1. Purpose

This document describes a **reference validation study** that any site can adopt or adapt after importing the HEARTLAND REDCap template. It is intended as a minimum-viable protocol suitable for submission to a local IRB and to justify data collection in a rural / resource-limited US heart-failure cohort.

The HEARTLAND Risk Score is a **pragmatic heuristic** (Protocol v3.3, Table 1) and has not been formally validated. This document proposes the first such validation.

> **Legal and clinical disclaimer.** This protocol is non-clinical reference material. Local adaptation, IRB approval, informed consent procedures, and sponsor oversight remain the responsibility of the implementing institution.

---

# 2. Primary objective

To prospectively evaluate whether the HEARTLAND Risk Tier classification at baseline (low / moderate / high) discriminates 12-month all-cause mortality in adults with heart failure managed in rural or resource-limited US settings.

## Secondary objectives

1. Assess discrimination (c-statistic) and calibration of the HEARTLAND score against MAGGIC and GWTG-HF in the same cohort.
2. Describe GDMT optimization trajectories by tier and implementation intensity (Tier 1 / 2 / 3).
3. Describe days alive and out of hospital (DAOH) by risk tier.
4. Explore the association between monitoring track (digital A vs analog B) and outcomes.

---

# 3. Design

- **Type:** Prospective observational cohort, multi-site, single-arm.
- **Setting:** Critical Access Hospitals, rural health clinics, or primary-care-led HF programs in the continental US.
- **Follow-up:** 12 months per participant.
- **Data platform:** REDCap instance hosted at the participating institution, using this template.
- **Registration:** ClinicalTrials.gov registration recommended before first enrollment.

---

# 4. Participants

## Inclusion criteria
1. Adults aged ≥18 years.
2. Documented heart failure (ICD-10 I50.x) with LVEF measured within 12 months of enrollment.
3. Receives primary-care-led or community-based HF management (not continuously followed by a cardiologist).
4. Provides written informed consent.

## Exclusion criteria
1. Enrolled in an interventional trial that forbids protocol-driven monitoring.
2. Life expectancy <6 months for reasons unrelated to heart failure (e.g., metastatic malignancy).
3. Planned transplantation or durable LVAD within 6 months.
4. Unable to complete the minimum baseline assessment (10 risk variables).

---

# 5. Sample size

| Stratum | Target n | Rationale |
|-|-|-|
| Low tier (0-4) | 50 | Minimum for tier-specific mortality estimate (expected 2-5%) |
| Moderate tier (5-8) | 50 | Expected mortality 10-15% |
| High tier (≥9) | 50 | Expected mortality ≥25% |
| **Total** | **150** | Powers primary endpoint with 80% at α = 0.05 assuming the mortality gradient above |

Interim accrual review at n = 75 to adjust site activation.

---

# 6. Endpoints

## Primary
`out_vital_status` (alive / deceased / lost to follow-up) at 12 months.

## Secondary
1. HF hospitalization count: `out_hf_hosp_count`
2. HF ED visit count: `out_hf_ed_count`
3. Days alive and out of hospital: `out_days_alive_oh`
4. GDMT optimization rate (≥3 classes at target dose): `out_gdmt_optimized`
5. KCCQ-12 change from baseline to 12 months: `out_kccq12_12mo - mo_kccq12_score[month=1]`

## Exploratory
- Discrimination: c-statistic for HEARTLAND tier vs MAGGIC vs GWTG-HF.
- Calibration: observed vs predicted mortality by decile of HEARTLAND score.
- Track A vs Track B comparison for monitoring adherence and clinical outcomes.

---

# 7. Assessments & schedule

| Visit | Window | Data captured |
|-|-|-|
| Baseline | Day 0 | `enrollment`, `baseline`, `gdmt_status` |
| Month 1-12 | ±5 days | `monthly_followup` (repeating) |
| 12-month close | Day 365 ±14 | `outcomes_12mo` |

Digital-track (A) patients upload daily vitals via app / Bluetooth; analog-track (B) patients return paper diaries at monthly phone contacts.

---

# 8. Statistical analysis plan

All analyses per intention-to-manage; sensitivity analyses on per-protocol population.

## Primary analysis
Time-to-event for all-cause mortality by HEARTLAND tier. Kaplan-Meier curves with log-rank test (α = 0.05, two-sided). Cox proportional-hazards model adjusted for age, sex, LVEF category.

## Discrimination / calibration
- Harrell's c for HEARTLAND vs MAGGIC vs GWTG-HF.
- Hosmer-Lemeshow goodness-of-fit.

## Secondary / exploratory
- Negative binomial regression for hospitalization and ED visit counts.
- Mixed-effects model for KCCQ-12 trajectory (fixed: time, tier, interaction; random: patient).
- Pre-planned sensitivity excluding high-tier patients with CKM Stage 4 to test robustness.

## Missing data
- Multiple imputation (m = 20) for variables with >5% missingness using chained equations.
- Mortality cannot be imputed; lost to follow-up censored at last contact date.

## Reporting
- STROBE checklist for observational studies.
- Pre-registered analysis plan on OSF or ClinicalTrials.gov before database lock.

---

# 9. Regulatory & ethics

| Item | Responsibility |
|-|-|
| IRB approval | Each site obtains approval from its own IRB |
| Informed consent | Standard written consent; recommended language in supplementary appendix |
| Data sharing | Recommended: aggregate site-level data deposited to Zenodo at study close |
| Authorship | Prospective authorship agreement with all contributing sites before analysis |

---

# 10. References

- HEARTLAND Protocol v3.3 (Cureus 2026; Zenodo DOI 10.5281/zenodo.18566403).
- Pocock SJ et al. *Predicting survival in heart failure: a risk score based on 39,372 patients from 30 studies* (MAGGIC). Eur Heart J. 2013;34:1404-1413.
- Peterson PN et al. *A validated risk score for in-hospital mortality in patients with heart failure from the American Heart Association Get With The Guidelines-Heart Failure program.* Circ Cardiovasc Qual Outcomes. 2010;3:25-32.
- Mebazaa A et al. *STRONG-HF: Safety, tolerability and efficacy of up-titration of GDMT for acute heart failure.* Lancet. 2022;400:1938-1952.
- Ndumele CE et al. *Cardiovascular-Kidney-Metabolic Health: A Presidential Advisory.* Circulation. 2023;148:1606-1635.
