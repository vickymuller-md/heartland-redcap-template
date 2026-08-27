# HEARTLAND Risk Assessment - REDCap Shared Library Submission Notes

Version: 1.0.1

Prepared: 2026-08-27

Author and copyright holder: Vicky Muller Ferreira, MD

Contact: vickymuller@heartlandprotocol.org

ORCID: 0009-0009-1099-5690

## Proposed library title

HEARTLAND Risk Assessment, version 1.0.1

## Package

- `heartland_risk_assessment_unscored_v1.0.1.csv` and `.xml`: eleven raw HEARTLAND risk-input fields, with no calculated score or tier.
- `heartland_risk_assessment_scored_v1.0.1.csv` and `.xml`: the same inputs with `_sc` variable suffixes plus the published 0-18 weighted score and three-tier calculation.
- Scored and unscored variants follow the REDLOC coding guideline.
- Variable names are lowercase, underscore-delimited, and no longer than 26 characters.
- The standalone instruments contain no dates, names, KCCQ content, or other direct identifiers.

## Research relevance and source

The instrument operationalizes Table 1 of:

Muller Ferreira V. HEARTLAND Protocol: A Tiered Clinical Implementation Toolkit for Primary Care-Led Heart Failure Management in Rural and Resource-Limited Settings. Cureus. 2026;18(3):e104817. DOI: 10.7759/cureus.104817. PMID: 41948265.

Current protocol deposit: https://doi.org/10.5281/zenodo.19101219

Template deposit: https://doi.org/10.5281/zenodo.19635000

## Validation and use boundary

The HEARTLAND score is a pragmatic implementation heuristic. It has not undergone external or prospective clinical validation. The scored version is provided only to support reproducible research and validation studies. It must not be used for patient-care decisions, diagnosis, treatment selection, or autonomous clinical decision support.

## Rights

The author created the HEARTLAND instrument and authorizes REDCap Shared Library distribution under the MIT license. The package does not reproduce a third-party questionnaire or proprietary scoring instructions.

## Submission route

The REDCap Shared Library is available only within REDCap partner instances. Final submission must be transmitted through an eligible institutional REDCap account or local REDCap administrator and will remain subject to REDLOC review for research relevance, function/coding, and copyright.
