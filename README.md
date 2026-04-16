# HEARTLAND Protocol — REDCap Instrument Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://img.shields.io/badge/DOI-pending%20Zenodo-blue)](#citation)
[![Protocol](https://img.shields.io/badge/Protocol-HEARTLAND%20v3.3-green)](https://doi.org/10.5281/zenodo.18566403)

Pre-built REDCap data collection instrument for the **HEARTLAND Protocol** (Heart failure Evidence-based Access in Rural Treatment, Linking Advanced Network Delivery). Rural hospitals and research institutions with REDCap can import this template and immediately begin structured data collection for HEARTLAND Protocol validation studies — zero development cost.

## What's included

- **Data Dictionary CSV** — 75 fields across 5 forms (enrollment, baseline, GDMT status, monthly follow-up, 12-month outcomes)
- **REDCap XML instrument** — equivalent ODM-compatible instrument file
- **Synthetic sample data** — 20 patients × 12-month follow-ups (no PHI)
- **Codebook PDF** — human-readable variable reference
- **Import guide** — step-by-step instructions for REDCap 14.x
- **Suggested validation study protocol** — n=150 reference design, STROBE-aligned

## Quickstart

1. Clone or download this repository.
2. In your REDCap instance, create a new empty project.
3. Upload `instruments/heartland_data_dictionary.csv` via *Data Dictionary → Upload*.
4. Enable the repeating instrument `monthly_followup`.
5. Optional — dry-run `examples/sample_data.csv` via the *Data Import Tool* to verify.

Full walkthrough: [`docs/import_guide.md`](docs/import_guide.md)

## What this template captures

### 5 forms

| # | Form | Purpose |
|-|-|-|
| 1 | `enrollment` | Demographics, facility, consent |
| 2 | `baseline` | 10 HEARTLAND risk variables + calculated risk score / tier |
| 3 | `gdmt_status` | RAS inhibitor / β-blocker / MRA / SGLT2i status with target doses |
| 4 | `monthly_followup` (repeating ×12) | Vitals, labs, GDMT changes, red flags, hospitalizations, KCCQ-12 |
| 5 | `outcomes_12mo` | Mortality, HF hospitalizations, DAOH, GDMT optimization |

### Calculated fields

- **`bl_risk_score`** — weighted sum (0-18 points) per Protocol v3.3 Table 1
- **`bl_risk_tier`** — `low` (0-4) / `moderate` (5-8) / `high` (≥9)
- **`gdmt_classes_count`** — count of HFrEF foundational classes on board (0-4)

### Branching logic

Lab fields are optional; HFpEF-specific agents branch on LVEF category; KCCQ-12 is gated by patient consent; HF-specific hospitalization and ED fields branch on any-cause occurrence.

## Files

```
redcap-template/
├── README.md
├── LICENSE (MIT)
├── .zenodo.json
├── CITATION.cff
├── instruments/
│   ├── heartland_data_dictionary.csv   <- PRIMARY artifact
│   ├── heartland_instrument.xml        <- ODM XML alternative
│   └── heartland_codebook.pdf          <- human-readable codebook
├── docs/
│   ├── import_guide.md
│   ├── variable_definitions.md
│   └── validation_study_protocol.md
├── examples/
│   └── sample_data.csv                 <- 20 synthetic patients
└── scripts/
    ├── csv_to_xml.py                   <- regenerate XML from CSV
    └── generate_sample_data.py         <- regenerate synthetic data
```

## Regenerate from source

If you modify `heartland_data_dictionary.csv`, regenerate downstream artifacts:

```bash
python3 scripts/csv_to_xml.py \
    --input  instruments/heartland_data_dictionary.csv \
    --output instruments/heartland_instrument.xml

python3 scripts/generate_sample_data.py \
    --output examples/sample_data.csv

sed -e 's/≥/>=/g' -e 's/≤/<=/g' -e 's/≠/!=/g' -e 's/⁺/+/g' -e 's/×/x/g' \
    docs/variable_definitions.md > /tmp/codebook_ascii.md
pandoc /tmp/codebook_ascii.md \
    -o instruments/heartland_codebook.pdf \
    --pdf-engine=xelatex
# (sed substitutes Unicode math glyphs that xelatex's default font lacks;
#  install the `newunicodechar` LaTeX package to skip the sed step.)
```

## Protocol reference

HEARTLAND Protocol v3.3 — Ferreira VM. Heart failure Evidence-based Access in Rural Treatment, Linking Advanced Network Delivery. *Cureus* 2026. DOI [10.5281/zenodo.18566403](https://doi.org/10.5281/zenodo.18566403). Clinical definitions in this template match v3.3 Table 1 (Risk Score) and Module 4 (GDMT).

## Citation

```
Ferreira VM. HEARTLAND Protocol REDCap Instrument Template, v1.0.0. 2026.
  Zenodo. DOI: 10.5281/zenodo.<to-be-minted-on-release>.
```

Machine-readable citation: [`CITATION.cff`](CITATION.cff).

## Author

**Vicky Muller Ferreira, MD**
ORCID: [0009-0009-1099-5690](https://orcid.org/0009-0009-1099-5690)
<vickymuller@heartlandprotocol.org>

## License

MIT — see [LICENSE](LICENSE). Clinical content remains © 2026 Vicky Muller Ferreira; license covers the REDCap instrument definition, scripts, and documentation. You are free to adopt, adapt, and redistribute.

## Disclaimer

This template is non-clinical reference material. Any site adopting it for patient care or research assumes full responsibility for local IRB approval, informed consent, and clinical oversight. The HEARTLAND Risk Score is a pragmatic heuristic and has not been formally validated — the suggested validation study (`docs/validation_study_protocol.md`) is the first step toward validation.
