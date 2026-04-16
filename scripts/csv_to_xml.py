#!/usr/bin/env python3
"""Convert the HEARTLAND REDCap data dictionary CSV to a REDCap ODM-style XML instrument.

REDCap's native XML export is CDISC ODM with REDCap extensions. For instrument-level
distribution we emit a simplified, REDCap-compatible ODM document: MetaDataVersion
containing FormDef, ItemGroupDef, ItemDef, and CodeListDef elements. This XML can be
imported via "Upload instrument ZIP/XML" in REDCap 14.x.

Usage:
    python3 scripts/csv_to_xml.py \\
        --input  instruments/heartland_data_dictionary.csv \\
        --output instruments/heartland_instrument.xml
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom

ODM_NS = "http://www.cdisc.org/ns/odm/v1.3"
RC_NS = "https://projectredcap.org"

TYPE_MAP = {
    "text": "text",
    "notes": "text",
    "calc": "float",
    "yesno": "integer",
    "truefalse": "integer",
    "radio": "integer",
    "dropdown": "integer",
    "checkbox": "boolean",
    "date_ymd": "date",
    "date_mdy": "date",
    "date_dmy": "date",
    "integer": "integer",
    "number": "float",
}


def parse_choices(raw: str) -> list[tuple[str, str]]:
    """Parse 'code, label | code, label' into [(code, label), ...]."""
    if not raw:
        return []
    out = []
    for chunk in raw.split("|"):
        chunk = chunk.strip()
        if not chunk:
            continue
        code, _, label = chunk.partition(",")
        out.append((code.strip(), label.strip()))
    return out


def build_xml(rows: list[dict]) -> ET.Element:
    ET.register_namespace("", ODM_NS)
    ET.register_namespace("redcap", RC_NS)

    odm = ET.Element(f"{{{ODM_NS}}}ODM", {
        "FileType": "Snapshot",
        "FileOID": "heartland_redcap_template_v1",
        "Granularity": "Metadata",
        "CreationDateTime": "2026-04-16T00:00:00",
        "SourceSystem": "HEARTLAND REDCap template generator",
        "ODMVersion": "1.3.2",
    })
    study = ET.SubElement(odm, f"{{{ODM_NS}}}Study", {"OID": "heartland_study"})
    gv = ET.SubElement(study, f"{{{ODM_NS}}}GlobalVariables")
    ET.SubElement(gv, f"{{{ODM_NS}}}StudyName").text = "HEARTLAND Protocol REDCap Template"
    ET.SubElement(gv, f"{{{ODM_NS}}}StudyDescription").text = (
        "Pre-built REDCap instrument for HEARTLAND Protocol v3.3 data collection."
    )
    ET.SubElement(gv, f"{{{ODM_NS}}}ProtocolName").text = "HEARTLAND v3.3"

    mdv = ET.SubElement(study, f"{{{ODM_NS}}}MetaDataVersion", {
        "OID": "Metadata.1",
        "Name": "HEARTLAND v1.0.0",
    })

    # Group rows by form
    forms: dict[str, list[dict]] = {}
    for r in rows:
        forms.setdefault(r["form"], []).append(r)

    # Protocol + StudyEventDef
    protocol = ET.SubElement(mdv, f"{{{ODM_NS}}}Protocol")
    for fname in forms:
        ET.SubElement(protocol, f"{{{ODM_NS}}}StudyEventRef", {
            "StudyEventOID": f"Event.{fname}", "Mandatory": "Yes", "OrderNumber": str(list(forms).index(fname) + 1),
        })

    for fname in forms:
        sed = ET.SubElement(mdv, f"{{{ODM_NS}}}StudyEventDef", {
            "OID": f"Event.{fname}",
            "Name": fname,
            "Repeating": "Yes" if fname == "monthly_followup" else "No",
            "Type": "Common",
        })
        ET.SubElement(sed, f"{{{ODM_NS}}}FormRef", {"FormOID": f"Form.{fname}", "Mandatory": "Yes"})

    # FormDef per form
    codelists: dict[str, list[tuple[str, str]]] = {}
    for fname, fields in forms.items():
        form = ET.SubElement(mdv, f"{{{ODM_NS}}}FormDef", {
            "OID": f"Form.{fname}",
            "Name": fname,
            "Repeating": "Yes" if fname == "monthly_followup" else "No",
        })
        ET.SubElement(form, f"{{{ODM_NS}}}ItemGroupRef", {
            "ItemGroupOID": f"ItemGroup.{fname}",
            "Mandatory": "Yes",
            "OrderNumber": "1",
        })

        group = ET.SubElement(mdv, f"{{{ODM_NS}}}ItemGroupDef", {
            "OID": f"ItemGroup.{fname}",
            "Name": fname,
            "Repeating": "No",
        })
        for i, f in enumerate(fields, 1):
            ET.SubElement(group, f"{{{ODM_NS}}}ItemRef", {
                "ItemOID": f"Item.{f['var']}",
                "Mandatory": "Yes" if f["required"].lower() == "y" else "No",
                "OrderNumber": str(i),
            })

    # ItemDef + CodeListRef
    for r in rows:
        ftype = r["field_type"]
        val_type = r["val_type"] or ftype
        datatype = TYPE_MAP.get(val_type, TYPE_MAP.get(ftype, "text"))

        attrs = {
            "OID": f"Item.{r['var']}",
            "Name": r["var"],
            "DataType": datatype,
        }
        if r["val_min"]:
            attrs["SignificantDigits"] = "0"  # purely cosmetic
        item = ET.SubElement(mdv, f"{{{ODM_NS}}}ItemDef", attrs)

        q = ET.SubElement(item, f"{{{ODM_NS}}}Question")
        tr = ET.SubElement(q, f"{{{ODM_NS}}}TranslatedText", {"{http://www.w3.org/XML/1998/namespace}lang": "en"})
        tr.text = r["label"]

        if r["val_min"] or r["val_max"]:
            rc = ET.SubElement(item, f"{{{ODM_NS}}}RangeCheck", {
                "Comparator": "GE" if r["val_min"] else "LE",
                "SoftHard": "Soft",
            })
            ET.SubElement(rc, f"{{{ODM_NS}}}CheckValue").text = r["val_min"] or r["val_max"]

        # Attach CodeListRef for radio/dropdown/checkbox/yesno
        if ftype in ("radio", "dropdown", "checkbox"):
            cl_oid = f"CL.{r['var']}"
            codelists[cl_oid] = parse_choices(r["choices"])
            ET.SubElement(item, f"{{{ODM_NS}}}CodeListRef", {"CodeListOID": cl_oid})
        elif ftype == "yesno":
            cl_oid = "CL.yesno"
            codelists.setdefault(cl_oid, [("1", "Yes"), ("0", "No")])
            ET.SubElement(item, f"{{{ODM_NS}}}CodeListRef", {"CodeListOID": cl_oid})
        elif ftype == "truefalse":
            cl_oid = "CL.truefalse"
            codelists.setdefault(cl_oid, [("1", "True"), ("0", "False")])
            ET.SubElement(item, f"{{{ODM_NS}}}CodeListRef", {"CodeListOID": cl_oid})

        # REDCap-specific extensions
        if r["field_type"] == "calc":
            ET.SubElement(item, f"{{{RC_NS}}}Calculation").text = r["choices"]
        if r["branching"]:
            ET.SubElement(item, f"{{{RC_NS}}}BranchingLogic").text = r["branching"]
        if r["annotation"]:
            ET.SubElement(item, f"{{{RC_NS}}}FieldAnnotation").text = r["annotation"]
        if r["section"]:
            ET.SubElement(item, f"{{{RC_NS}}}SectionHeader").text = r["section"]
        if r["field_note"]:
            ET.SubElement(item, f"{{{RC_NS}}}FieldNote").text = r["field_note"]
        if r["form"]:
            ET.SubElement(item, f"{{{RC_NS}}}FormName").text = r["form"]

    # Emit CodeLists
    for cl_oid, choices in codelists.items():
        cl = ET.SubElement(mdv, f"{{{ODM_NS}}}CodeList", {
            "OID": cl_oid,
            "Name": cl_oid,
            "DataType": "text",
        })
        for code, label in choices:
            ci = ET.SubElement(cl, f"{{{ODM_NS}}}CodeListItem", {"CodedValue": code})
            d = ET.SubElement(ci, f"{{{ODM_NS}}}Decode")
            tr = ET.SubElement(d, f"{{{ODM_NS}}}TranslatedText",
                               {"{http://www.w3.org/XML/1998/namespace}lang": "en"})
            tr.text = label

    return odm


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    with args.input.open() as fh:
        reader = csv.reader(fh)
        _ = next(reader)  # header
        rows = []
        for r in reader:
            rows.append({
                "var": r[0],
                "form": r[1],
                "section": r[2],
                "field_type": r[3],
                "label": r[4],
                "choices": r[5],
                "field_note": r[6],
                "val_type": r[7],
                "val_min": r[8],
                "val_max": r[9],
                "identifier": r[10],
                "branching": r[11],
                "required": r[12],
                "align": r[13],
                "qn": r[14],
                "matrix_group": r[15],
                "matrix_rank": r[16],
                "annotation": r[17],
            })

    tree = build_xml(rows)
    pretty = minidom.parseString(ET.tostring(tree, encoding="unicode")).toprettyxml(indent="  ")
    args.output.write_text(pretty, encoding="utf-8")
    print(f"Wrote {args.output} ({len(rows)} items across {len({r['form'] for r in rows})} forms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
