# HEARTLAND Protocol — REDCap Instrument Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19634999.svg)](https://doi.org/10.5281/zenodo.19634999)
[![Protocol](https://img.shields.io/badge/Protocol-HEARTLAND%20v3.3-green)](https://doi.org/10.7759/cureus.104817)

Research instrument candidate for the **HEARTLAND Protocol** (Heart failure Evidence-based Access in Rural Treatment, Linking Advanced Network Delivery). Local generation tests do not establish clinical validity or compatibility with an institution's REDCap installation.

## Local candidate hold — 24 September 2026

The CSV-to-XML converter now preserves both validation bounds when both are supplied. The regression
suite checks all 75 dictionary fields, including 28 with minimum and maximum, without changing the CSV.
Run `python3 -m unittest discover -s tests -v` to reproduce those serialization checks.
The converter also no longer invents `SignificantDigits=0` from a minimum bound. Numeric precision
and values such as 4.5, 150.5 and 12.5 still require an actual import/export round-trip in the target instance.

The checked-in XML/codebook/library packages have **not** been replaced by this narrow converter fix.
The CSV's ESSI representation remains unresolved (8–40 bounds versus a 7–35 note); generated output
copies that source and must not be treated as clinical adjudication. Do not distribute or import
the candidate as a clinically approved instrument. No target REDCap import, calculation execution,
branching behavior or cross-format equivalence has been verified in this update. Use only an
authorized nonproduction synthetic test project once the candidate and import procedure are agreed.

## What's included

- **Data Dictionary CSV** — 75 fields across 5 forms (enrollment, baseline, GDMT status, monthly follow-up, 12-month outcomes)
- **REDCap XML instrument** — ODM-style alternative; range regeneration and target import/parity gates remain open
- **Synthetic sample data** — 20 patients × 12-month follow-ups (no PHI)
- **Codebook PDF** — human-readable variable reference
- **Import guide** — draft rehearsal instructions; version compatibility and menus require target-instance verification
- **Suggested validation study protocol** — n=150 reference design, STROBE-aligned
- **REDCap Shared Library package** — scored and unscored standalone HEARTLAND Risk Assessment instruments prepared to REDLOC coding guidance

## Synthetic test preparation (import validation still required)

1. Clone or download this repository.
2. In your REDCap instance, create a new empty project.
3. Review the source/ESSI hold above before any test upload. Do not infer clinical approval from a successful upload.
4. For an authorized import rehearsal, use `instruments/heartland_data_dictionary.csv` via *Data Dictionary → Upload* and preserve the import validation report.
5. Verify the repeating instrument `monthly_followup` in the target instance.
6. Dry-run `examples/sample_data.csv` in that isolated project; inspect errors and actual calculations. These steps have not been executed in this update.

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
├── library_submission/
│   └── heartland_risk_assessment_v1.0.2/  <- REDLOC scored/unscored package
├── examples/
│   └── sample_data.csv                 <- 20 synthetic patients
└── scripts/
    ├── csv_to_xml.py                   <- regenerate XML from CSV
    └── generate_sample_data.py         <- regenerate synthetic data
```

Note: `county_fips` values in `examples/sample_data.csv` are synthetic placeholders generated for demonstration, not real ANSI/FIPS county codes.

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

Ferreira VM. HEARTLAND Protocol v3.3 - *Cureus*. 2026;18(3):e104817. DOI [10.7759/cureus.104817](https://doi.org/10.7759/cureus.104817); protocol deposit [10.5281/zenodo.19101219](https://doi.org/10.5281/zenodo.19101219). Table 1 (Risk Score) and Module 4 (GDMT) are intended source references; the unresolved ESSI discrepancy prevents a blanket equivalence claim.

## Citation

```
Ferreira VM. HEARTLAND Protocol REDCap Instrument Template, v1.0.2. 2026.
  Zenodo. DOI: 10.5281/zenodo.22132635.
```

Machine-readable citation: [`CITATION.cff`](CITATION.cff).

## Changelog

- Historical CSV range change: `bl_lvef_pct` 5–80 and `bl_enrichd_score` 8–40. The ESSI range is recorded as source history, not confirmed instrument alignment; its conflicting 7–35 note still requires adjudication.

## Software preservation

Software Heritage snapshot (archived 2026-08-25): [`swh:1:snp:f3ff79845487b0c6ff853b772f14364f74849687`](https://archive.softwareheritage.org/swh:1:snp:f3ff79845487b0c6ff853b772f14364f74849687/)

This persistent SWHID identifies the repository snapshot captured on that date; archival does not imply endorsement or validation.

## Author

**Vicky Muller Ferreira, MD**
ORCID: [0009-0009-1099-5690](https://orcid.org/0009-0009-1099-5690)
<vickymuller@heartlandprotocol.org>

## License

MIT — see [LICENSE](LICENSE). Clinical content remains © 2026 Vicky Muller Ferreira; license covers the REDCap instrument definition, scripts, and documentation. You are free to adopt, adapt, and redistribute.

## Disclaimer

This template is non-clinical reference material. Any site adopting it for research assumes full responsibility for local IRB approval, informed consent, privacy review, and clinical oversight. All full dates and facility name are marked as identifiers in the primary data dictionary. KCCQ-12 fields store only site-computed summary scores; this repository does not reproduce the copyrighted questionnaire. The HEARTLAND Risk Score is a pragmatic heuristic that has not been externally validated and must not be used for patient-care decisions.
