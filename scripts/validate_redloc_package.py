#!/usr/bin/env python3
"""Validate the public master dictionary and REDLOC package."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "instruments/heartland_data_dictionary.csv"
PACKAGE = ROOT / "library_submission/heartland_risk_assessment_v1.0.2"
DATE_FIELDS = {
    "enr_date",
    "consent_date",
    "gdmt_arni_acei_arb_start",
    "gdmt_bb_start",
    "gdmt_mra_start",
    "gdmt_sglt2_start",
    "mo_date",
    "out_death_date",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def validate_references(instrument_rows: list[dict[str, str]]) -> None:
    names = {row["Variable / Field Name"] for row in instrument_rows}
    for row in instrument_rows:
        combined = " ".join(
            [
                row["Choices, Calculations, OR Slider Labels"],
                row["Branching Logic (Show field only if...)"],
                row["Field Annotation"],
            ]
        )
        for reference in re.findall(r"\[([a-z0-9_]+)\]", combined):
            assert reference in names, f"Missing reference {reference}"


def main() -> None:
    master = rows(MASTER)
    marked_dates = {
        row["Variable / Field Name"]
        for row in master
        if row["Text Validation Type OR Show Slider Number"].startswith("date_")
        and row["Identifier?"].lower() == "y"
    }
    assert marked_dates == DATE_FIELDS
    facility = next(row for row in master if row["Variable / Field Name"] == "facility_name")
    assert facility["Identifier?"].lower() == "y"

    unscored = rows(PACKAGE / "heartland_risk_assessment_unscored_v1.0.2.csv")
    scored = rows(PACKAGE / "heartland_risk_assessment_scored_v1.0.2.csv")
    assert len(unscored) == 11
    assert len(scored) == 13
    assert not any(row["Field Type"] == "calc" for row in unscored)
    assert sum(row["Field Type"] == "calc" for row in scored) == 1
    assert all(len(row["Variable / Field Name"]) <= 26 for row in [*unscored, *scored])
    assert all(not row["Identifier?"] for row in [*unscored, *scored])
    assert all("kccq" not in str(row).lower() for row in [*unscored, *scored])
    validate_references(unscored)
    validate_references(scored)

    redcap_ns = "https://projectredcap.org"
    for xml_path in PACKAGE.glob("*.xml"):
        root = ET.parse(xml_path).getroot()
        item_defs = [element for element in root.iter() if element.tag.endswith("ItemDef")]
        assert item_defs
        assert all(f"{{{redcap_ns}}}Variable" in element.attrib for element in item_defs)
    print("REDLOC_PACKAGE_VALID")


if __name__ == "__main__":
    main()
