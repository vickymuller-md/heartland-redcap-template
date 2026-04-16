# HEARTLAND REDCap Instrument Template

## Parent Project

Subproject of `~/NIW-project/`. Part of the HEARTLAND Protocol ecosystem for the EB-2 NIW petition of Vicky Muller Ferreira, MD.

## Purpose

Pre-built REDCap data collection instrument (XML + data dictionary CSV) containing the HEARTLAND Protocol variables, outcome measures, and follow-up schedules. Any rural hospital or research institution with REDCap can import this template and immediately begin structured data collection for HEARTLAND Protocol validation studies — zero development cost.

## NIW Role

- **Prong 2**: directly enables the formal validation study described in the V14 Professional Plan Phase 3
- **Prong 3**: any institution can adopt it; lowers the barrier for multi-site collaboration
- **Evidence**: Zenodo downloads, adoption by pilot sites

## What is REDCap

REDCap (Research Electronic Data Capture) is the dominant clinical research data platform used by 6,800+ institutions in 155 countries. It supports XML instrument import, making template distribution trivial. Vicky's target pilot facilities (Critical Access Hospitals) commonly have REDCap access via their affiliated academic medical centers.

## Instrument Design

### Forms (REDCap instruments)

1. **Enrollment** — demographics, facility info, consent date
   - Age, sex, race/ethnicity
   - State, county (FIPS), rural/urban classification
   - Facility name, CAH designation, implementation tier (1/2/3)
   - Consent date, enrollment date

2. **Baseline Assessment** — the 10 HEARTLAND risk variables
   - HF history (hospitalization past year: Y/N)
   - LVEF (numeric + category: HFrEF/HFmrEF/HFpEF)
   - eGFR (numeric)
   - Natriuretic peptide (BNP/NT-proBNP, numeric)
   - SBP (numeric)
   - Diabetes (Y/N)
   - CKM stage (0-4)
   - Distance to nearest cardiologist (miles, numeric)
   - Social support score (numeric, ENRICHD-based)
   - Computed: HEARTLAND risk score + tier (calculated field)

3. **GDMT Status** — current medications
   - ACEi/ARB/ARNi: drug, dose, date started
   - Beta-blocker: drug, dose, date started
   - MRA: drug, dose, date started
   - SGLT2i: drug, dose, date started
   - GDMT classes count (calculated: 0-4)
   - Generic bridge status (Y/N)

4. **Monthly Follow-up** (repeating instrument, months 1-12)
   - Vitals: weight, SBP, DBP, HR, SpO2
   - Lab: eGFR, K+, BNP (if available)
   - GDMT changes (titration events)
   - Monitoring track: A (digital) or B (analog)
   - Red flag events (count + type)
   - Hospitalizations (Y/N + reason)
   - ED visits (Y/N + reason)

5. **Outcomes (12-month)** — primary + secondary endpoints
   - All-cause mortality
   - HF hospitalization
   - HF-related ED visits
   - Days alive and out of hospital
   - GDMT optimization rate (% at target doses)
   - Patient-reported outcomes (KCCQ-12 if available)

### Calculated Fields

- HEARTLAND risk score (sum of 10 binary variables)
- HEARTLAND risk tier (branching logic: 0-2=low, 3-4=moderate, 5-7=high, 8-10=very-high)
- GDMT classes count
- Days between enrollment and each follow-up

### Branching Logic

- Monthly follow-up fields conditional on enrollment completion
- Lab fields optional (marked as "if available")
- KCCQ-12 conditional on patient consent for PROs

## Output Files

```
redcap-template/
├── CLAUDE.md                          # this file
├── README.md                          # instructions for importing into REDCap
├── LICENSE                            # MIT
├── .zenodo.json
├── instruments/
│   ├── heartland_data_dictionary.csv  # REDCap data dictionary (primary)
│   ├── heartland_instrument.xml       # REDCap XML export (alternative import)
│   └── heartland_codebook.pdf         # Human-readable field reference
├── docs/
│   ├── import_guide.md                # Step-by-step REDCap import instructions
│   ├── variable_definitions.md        # Clinical definitions for each field
│   └── validation_study_protocol.md   # Suggested study design using this template
└── examples/
    └── sample_data.csv                # 20-row synthetic example (for testing import)
```

## DOI Strategy

- GitHub repo: `vickymuller-md/heartland-redcap-template` (public)
- Zenodo DOI as "dataset" type
- `.zenodo.json` at repo root

## Rules

- English only
- All variable names must use REDCap conventions (lowercase, underscores, ≤26 chars)
- Clinical definitions must match HEARTLAND Protocol v3.2 exactly
- Include both CSV data dictionary AND XML instrument (different institutions prefer different import methods)
- Sample data must be synthetic — no real patients
- Author: Vicky Muller Ferreira, MD
- License: MIT

## Execution Plan

### Session 1 (single session)
1. Create REDCap data dictionary CSV with all 5 forms
2. Add calculated fields and branching logic
3. Generate XML instrument from CSV (REDCap format)
4. Create sample_data.csv (20 synthetic rows)
5. Write import_guide.md with screenshots/steps
6. Write variable_definitions.md
7. Write validation_study_protocol.md (suggested n, endpoints, analysis plan)
8. Generate codebook PDF
9. README + LICENSE + .zenodo.json
10. Push to vickymuller-md/heartland-redcap-template → release → DOI

## Timeline

1 session estimated.
