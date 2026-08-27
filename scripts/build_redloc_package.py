#!/usr/bin/env python3
"""Build scored and unscored REDLOC-ready HEARTLAND risk instruments."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "instruments/heartland_data_dictionary.csv"
OUTPUT = ROOT / "library_submission/heartland_risk_assessment_v1.0.2"
CONVERTER = ROOT / "scripts/csv_to_xml.py"
VERSION = "1.0.2"

FIELD_MAP = [
    ("age", "hl_age"),
    ("bl_prior_hf_hosp_6mo", "hl_hosp6m"),
    ("bl_egfr", "hl_egfr"),
    ("bl_np_type", "hl_np_type"),
    ("bl_np_value", "hl_np_value"),
    ("bl_sbp_admit", "hl_sbp"),
    ("bl_diabetes", "hl_diabetes"),
    ("bl_lvef_pct", "hl_lvef"),
    ("bl_ckm_stage", "hl_ckm"),
    ("bl_distance_cardio_mi", "hl_cardio_distance"),
    ("bl_social_support_limited", "hl_limited_support"),
]

DISCLAIMER = (
    "HEARTLAND Risk Assessment v1.0.2 - research use only. The HEARTLAND score is an "
    "unvalidated implementation heuristic and must not be used for clinical decision-making."
)


def read_source() -> tuple[list[str], dict[str, dict[str, str]]]:
    with SOURCE.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            raise ValueError("Missing REDCap data dictionary header")
        return reader.fieldnames, {
            row["Variable / Field Name"]: row for row in reader
        }


def base_rows(source: dict[str, dict[str, str]], *, scored: bool) -> list[dict[str, str]]:
    suffix = "_sc" if scored else ""
    form_name = "heartland_risk_assess_sc" if scored else "heartland_risk_assessment"
    rows: list[dict[str, str]] = []
    for index, (source_name, short_name) in enumerate(FIELD_MAP):
        row = dict(source[source_name])
        row["Variable / Field Name"] = short_name + suffix
        row["Form Name"] = form_name
        row["Section Header"] = DISCLAIMER if index == 0 else ""
        row["Identifier?"] = ""
        row["Branching Logic (Show field only if...)"] = ""
        row["Field Annotation"] = ""
        rows.append(row)
    return rows


def scored_rows(source: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    rows = base_rows(source, scored=True)
    score = dict(source["bl_risk_score"])
    score["Variable / Field Name"] = "hl_risk_score_sc"
    score["Form Name"] = "heartland_risk_assess_sc"
    score["Section Header"] = "Calculated research score"
    score["Choices, Calculations, OR Slider Labels"] = (
        "if([hl_age_sc]>=75,2,0) + "
        "if([hl_hosp6m_sc]=\"1\",3,0) + "
        "if([hl_egfr_sc]<45,2,0) + "
        "if(([hl_np_type_sc]=\"1\" and [hl_np_value_sc]>=500) or "
        "([hl_np_type_sc]=\"2\" and [hl_np_value_sc]>=1500),2,0) + "
        "if([hl_sbp_sc]<100,2,0) + "
        "if([hl_diabetes_sc]=\"1\",1,0) + "
        "if([hl_lvef_sc]<30,2,0) + "
        "if([hl_ckm_sc]>=3,2,0) + "
        "if([hl_cardio_distance_sc]>50,1,0) + "
        "if([hl_limited_support_sc]=\"1\",1,0)"
    )
    score["Field Note"] = (
        "Unvalidated implementation heuristic; research use only; not for patient-care decisions."
    )
    score["Identifier?"] = ""
    score["Branching Logic (Show field only if...)"] = ""
    score["Required Field?"] = ""
    score["Field Annotation"] = ""

    tier = dict(source["bl_risk_tier"])
    tier["Variable / Field Name"] = "hl_risk_tier_sc"
    tier["Form Name"] = "heartland_risk_assess_sc"
    tier["Section Header"] = ""
    tier["Choices, Calculations, OR Slider Labels"] = ""
    tier["Field Note"] = "Low 0-4; moderate 5-8; high 9-18. Research use only."
    tier["Identifier?"] = ""
    tier["Branching Logic (Show field only if...)"] = ""
    tier["Required Field?"] = ""
    tier["Field Annotation"] = (
        "@CALCTEXT(if([hl_risk_score_sc]<5,'low',"
        "if([hl_risk_score_sc]<9,'moderate','high')))"
    )
    return [*rows, score, tier]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def convert(csv_path: Path, xml_path: Path, study_name: str) -> None:
    subprocess.run(
        [
            sys.executable,
            str(CONVERTER),
            "--input",
            str(csv_path),
            "--output",
            str(xml_path),
            "--version",
            VERSION,
            "--study-name",
            study_name,
        ],
        check=True,
    )


def main() -> int:
    fieldnames, source = read_source()
    unscored_csv = OUTPUT / "heartland_risk_assessment_unscored_v1.0.2.csv"
    scored_csv = OUTPUT / "heartland_risk_assessment_scored_v1.0.2.csv"
    write_csv(unscored_csv, fieldnames, base_rows(source, scored=False))
    write_csv(scored_csv, fieldnames, scored_rows(source))
    convert(
        unscored_csv,
        OUTPUT / "heartland_risk_assessment_unscored_v1.0.2.xml",
        "HEARTLAND Risk Assessment v1.0.2",
    )
    convert(
        scored_csv,
        OUTPUT / "heartland_risk_assessment_scored_v1.0.2.xml",
        "HEARTLAND Risk Assessment Scored v1.0.2",
    )
    print(f"Built REDLOC package in {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
