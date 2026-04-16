# REDCap Import Guide — HEARTLAND Template v1.0.0

This guide shows how to load the HEARTLAND Protocol instrument set into any REDCap instance (version 14.x or later). Choose **Path A (CSV)** or **Path B (XML)** depending on how your institution prefers to provision new projects. Both paths produce an equivalent set of forms.

---

## Before you start

| Requirement | Notes |
|-|-|
| REDCap account with project-creation privileges | If you don't have this, ask your REDCap administrator |
| REDCap version | 14.x or later (all modern features supported); 13.x works with minor exceptions |
| Local copy of this repository | Download from `https://github.com/vickymuller-md/heartland-redcap-template` |
| Files you will upload | `instruments/heartland_data_dictionary.csv` **or** `instruments/heartland_instrument.xml` |

Both paths yield the same 5 forms:

1. `enrollment`
2. `baseline`
3. `gdmt_status`
4. `monthly_followup` (repeating)
5. `outcomes_12mo`

---

## Path A — Data Dictionary CSV (recommended)

1. **Create an empty project.** REDCap Home → *New Project* → Name it (e.g. "HEARTLAND Validation — Site X"), Purpose = *Research*, storage location per your IRB.
2. **Open the Data Dictionary upload page.** In your new project, go to *Project Setup* → *Design your data collection instruments* → **Upload data dictionary (CSV)**.
3. **Upload the file.** Select `instruments/heartland_data_dictionary.csv` from your local copy of the repository.
4. **Review the preview.** REDCap will show a diff. Confirm that all 5 forms appear and there are zero errors. The calculated fields (`bl_risk_score`, `bl_risk_tier`, `gdmt_classes_count`) should validate without warnings.
5. **Commit the changes.** Click *Commit Changes* to apply the data dictionary.
6. **Enable the repeating instrument.** *Project Setup* → *Enable optional modules and customizations* → toggle **Repeatable instruments and events**. Then click *Modify*, mark `monthly_followup` as repeating, save.
7. **Move project to Production.** When ready for real data, click *Move project to production* (top of *Project Setup*).

### Troubleshooting Path A

- **"Variable name exceeds 26 chars":** check the row where it errors; rename carefully (keep leading prefix). This template ships with all names ≤25 chars.
- **Calc field parse error:** copy the formula shown in `variable_definitions.md` exactly; watch for smart-quote pasting.
- **Branching logic parse error:** REDCap expects `[field] = "1"` (with double quotes). If your CSV was opened in Excel and re-saved, smart quotes may have been introduced — re-download from GitHub.

---

## Path B — XML instrument

Use this path if you prefer ODM XML or if your institution's REDCap blocks CSV uploads.

1. **Create an empty project** (same as Path A step 1).
2. **Open instrument designer.** *Project Setup* → *Online Designer* → **Upload instrument ZIP file** (the "Upload from shared library or XML" option in newer versions accepts raw `.xml`).
3. **Upload the XML.** Select `instruments/heartland_instrument.xml`.
4. **Confirm** each of the 5 forms is created.
5. **Enable repeating instrument** (same as Path A step 6).
6. **Move to Production** when ready.

### Troubleshooting Path B

- **"Invalid ODM document":** run `xmllint --noout instruments/heartland_instrument.xml` locally to confirm well-formedness before uploading.
- **Missing REDCap extensions:** some institutions run a stripped-down REDCap that does not recognize the `redcap:` namespace. Fall back to Path A.

---

## After import — verify with sample data

1. Go to *Data Import Tool* (left sidebar).
2. Upload `examples/sample_data.csv` in **dry-run** mode.
3. Expect "20 enrollment rows, 24 monthly follow-up rows, 20 outcomes rows — 0 errors."
4. Do **not** commit the sample data to a production project — it is synthetic, seeded with fixed random numbers, and will contaminate any real cohort.

---

## What to customize for your site

Fields that commonly need local adjustment before go-live:

| Field | Why adjust |
|-|-|
| `facility_name` choices | Restrict to a drop-down of your site list |
| `rural_urban` mapping | Some sites prefer raw RUCA 1-10 rather than the collapsed 4-bucket version |
| `gdmt_*_target` defaults | Your formulary may bound titration differently |
| PRO instruments beyond KCCQ-12 | Add any your IRB has already approved |

For protocol-level customization (e.g. a research-only subset of variables), see `docs/validation_study_protocol.md`.

---

## Citing this template

```
Ferreira VM. HEARTLAND Protocol REDCap Instrument Template, v1.0.0. 2026.
  Zenodo. DOI: 10.5281/zenodo.<to-be-minted-on-release>.
```

## Support

- GitHub Issues: `https://github.com/vickymuller-md/heartland-redcap-template/issues`
- Protocol questions: <vickymuller@heartlandprotocol.org>
- REDCap-specific questions: your institution's REDCap administrator
