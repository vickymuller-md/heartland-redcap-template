"""Serialization regressions, not clinical validation or a REDCap import test."""
from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("csv_to_xml", ROOT / "scripts/csv_to_xml.py")
converter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(converter)
NS = {"o": converter.ODM_NS, "r": converter.RC_NS}


def row(**overrides):
    base = {key: "" for key in ("var", "form", "section", "field_type", "label", "choices",
        "field_note", "val_type", "val_min", "val_max", "identifier", "branching", "required",
        "align", "qn", "matrix_group", "matrix_rank", "annotation")}
    base.update(var="fixture_value", form="synthetic", field_type="text", val_type="number", label="Synthetic <value> & unit")
    base.update(overrides)
    return base


def bounds(item):
    return [(entry.get("Comparator"), entry.findtext("o:CheckValue", namespaces=NS), entry.get("SoftHard"))
        for entry in item.findall("o:RangeCheck", NS)]


class RangeSerializationTests(unittest.TestCase):
    def test_range_does_not_invent_numeric_precision(self):
        for validation_type in ["number", "integer", "date_ymd"]:
            with self.subTest(validation_type=validation_type):
                xml = converter.build_xml([row(val_type=validation_type, val_min="0")], version="test", study_name="Synthetic fixture")
                item = ET.fromstring(ET.tostring(xml)).find(".//o:ItemDef", NS)
                self.assertNotIn("SignificantDigits", item.attrib)

    def test_each_bound_is_emitted_independently(self):
        for low, high in [("", ""), ("0", ""), ("", "0"), ("0", "100"), ("-2.5", "1.25"), ("1.20", "1.20")]:
            with self.subTest(low=low, high=high):
                xml = converter.build_xml([row(val_min=low, val_max=high)], version="test", study_name="Synthetic fixture")
                item = xml.find(".//o:ItemDef", NS)
                expected = [(operator, value, "Soft") for operator, value in [("GE", low), ("LE", high)] if value != ""]
                self.assertEqual(bounds(item), expected)

    def test_date_strings_are_preserved_without_numeric_coercion(self):
        xml = converter.build_xml([row(val_type="date_ymd", val_min="2020-01-01", val_max="2030-12-31")], version="test", study_name="Synthetic fixture")
        item = xml.find(".//o:ItemDef", NS)
        self.assertEqual(item.get("DataType"), "date")
        self.assertEqual(bounds(item), [("GE", "2020-01-01", "Soft"), ("LE", "2030-12-31", "Soft")])

    def test_labels_calculations_branching_and_notes_are_not_rewritten(self):
        source = row(field_type="calc", choices="[a] + [b]", val_min="0", val_max="18", required="y",
            field_note="Missing is not zero", branching='[consent] = "1"', section="Synthetic section", annotation="@READONLY")
        xml = converter.build_xml([source], version="candidate", study_name="Synthetic fixture")
        # Exercise actual XML escaping and parse round-trip, not only in-memory objects.
        item = ET.fromstring(ET.tostring(xml)).find(".//o:ItemDef", NS)
        self.assertEqual(item.findtext("o:Question/o:TranslatedText", namespaces=NS), source["label"])
        for key, element in [("choices", "Calculation"), ("field_note", "FieldNote"), ("branching", "BranchingLogic"),
            ("section", "SectionHeader"), ("annotation", "FieldAnnotation")]:
            self.assertEqual(item.findtext(f"r:{element}", namespaces=NS), source[key])
        self.assertEqual(item.get(f"{{{converter.RC_NS}}}RequiredField"), "y")

    def test_cli_preserves_every_dictionary_bound_and_never_edits_source(self):
        dictionary = ROOT / "instruments/heartland_data_dictionary.csv"
        original = dictionary.read_bytes()
        with dictionary.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        with tempfile.TemporaryDirectory(prefix="heartland-redcap-test-") as directory:
            destination = Path(directory) / "candidate.xml"
            run = subprocess.run([sys.executable, str(ROOT / "scripts/csv_to_xml.py"), "--input", str(dictionary),
                "--output", str(destination), "--version", "local-range-check-candidate"], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            xml = ET.parse(destination)
            items = {item.get("Name"): item for item in xml.findall(".//o:ItemDef", NS)}
            self.assertEqual(len(items), len(rows))
            paired = 0
            for source in rows:
                name = source["Variable / Field Name"]
                low, high = source["Text Validation Min"], source["Text Validation Max"]
                paired += bool(low and high)
                with self.subTest(variable=name):
                    self.assertEqual(bounds(items[name]), [(operator, value, "Soft")
                        for operator, value in [("GE", low), ("LE", high)] if value != ""])
                    self.assertEqual(items[name].findtext("o:Question/o:TranslatedText", namespaces=NS), source["Field Label"])
                    self.assertNotIn("SignificantDigits", items[name].attrib)
            self.assertEqual(paired, 28, "Reconcile changed dictionary fixture coverage explicitly")
        self.assertEqual(dictionary.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
