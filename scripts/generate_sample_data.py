#!/usr/bin/env python3
"""Generate 20 fully synthetic sample rows for the HEARTLAND REDCap template.

Layout:
  - 20 enrollment + baseline + gdmt_status records across the 3 risk tiers
    (low 0-4, moderate 5-8, high >=9).
  - 2 of those patients (record_id 1 and 2) get 12 monthly follow-ups each
    (24 rows in the repeating `monthly_followup` instrument).
  - All 20 patients get 12-month outcomes.

No PHI. Seeded for reproducibility.

Usage:
    python3 scripts/generate_sample_data.py --output examples/sample_data.csv
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

RNG = random.Random(20260416)

STATES = ["MT", "WY", "ND", "SD", "NE", "IA", "MS", "AR", "WV", "AL"]
FACILITIES = [
    "Glacier County CAH", "Powder River Memorial", "Sacred Heart Rural",
    "Prairie View Medical", "Big Horn Community", "Ozark Community Clinic",
    "Delta Regional CAH", "Appalachian Rural Care",
]


def synth_row(rid: int) -> dict[str, str]:
    """Build one enrollment/baseline/gdmt row with internally consistent clinical values."""
    tier_bucket = rid % 3  # 0=low, 1=moderate, 2=high

    if tier_bucket == 0:
        age = RNG.randint(55, 70)
        prior_hf = "0"
        egfr = RNG.uniform(55, 90)
        lvef = RNG.randint(40, 55)
        sbp = RNG.randint(110, 140)
        diabetes = RNG.choice(["0", "1"])
        ckm = str(RNG.choice([0, 1, 2]))
        distance = RNG.randint(5, 40)
        limited_support = "0"
        np_type, np_value = "1", RNG.randint(50, 400)
    elif tier_bucket == 1:
        age = RNG.randint(65, 80)
        prior_hf = RNG.choice(["0", "1"])
        egfr = RNG.uniform(35, 60)
        lvef = RNG.randint(28, 45)
        sbp = RNG.randint(95, 130)
        diabetes = "1"
        ckm = str(RNG.choice([2, 3]))
        distance = RNG.randint(30, 70)
        limited_support = RNG.choice(["0", "1"])
        np_type, np_value = "2", RNG.randint(800, 2000)
    else:
        age = RNG.randint(75, 92)
        prior_hf = "1"
        egfr = RNG.uniform(18, 40)
        lvef = RNG.randint(18, 32)
        sbp = RNG.randint(85, 110)
        diabetes = "1"
        ckm = str(RNG.choice([3, 4]))
        distance = RNG.randint(55, 120)
        limited_support = "1"
        np_type, np_value = "2", RNG.randint(2500, 8000)

    enr_date = date(2026, 1, 1) + timedelta(days=RNG.randint(0, 90))
    consent_date = enr_date - timedelta(days=RNG.randint(0, 3))

    lvef_cat = "1" if lvef <= 40 else ("2" if lvef <= 49 else "3")

    gdmt_arni = RNG.choice(["1", "2", "4"])
    gdmt_bb = RNG.choice(["1", "2", "3"])
    gdmt_mra = RNG.choice(["1", "3", "0"])
    gdmt_sglt2 = RNG.choice(["1", "2", "0"])

    facility = RNG.choice(FACILITIES)
    facility_tier = str(RNG.choice([1, 2, 3]))

    row = {
        "record_id": str(rid),
        "enr_date": enr_date.isoformat(),
        "consent_date": consent_date.isoformat(),
        "facility_name": facility,
        "facility_cah": RNG.choice(["0", "1"]),
        "facility_tier": facility_tier,
        "state": RNG.choice(STATES),
        "county_fips": f"{RNG.randint(1001, 56045):05d}",
        "rural_urban": str(RNG.choice([3, 4])),
        "age": str(age),
        "sex": str(RNG.choice([1, 2])),
        "race___5": "1",
        "ethnicity": str(RNG.choice([1, 2])),
        "bl_prior_hf_hosp_6mo": prior_hf,
        "bl_lvef_pct": str(lvef),
        "bl_lvef_category": lvef_cat,
        "bl_egfr": f"{egfr:.1f}",
        "bl_np_type": np_type,
        "bl_np_value": str(np_value),
        "bl_sbp_admit": str(sbp),
        "bl_diabetes": diabetes,
        "bl_ckm_stage": ckm,
        "bl_distance_cardio_mi": str(distance),
        "bl_social_support_limited": limited_support,
        "bl_enrichd_score": str(RNG.randint(12, 33)),
        "bl_pro_consent": RNG.choice(["0", "1"]),
        "gdmt_arni_acei_arb_drug": gdmt_arni,
        "gdmt_arni_acei_arb_dose": str(RNG.choice([40, 80, 100, 200])),
        "gdmt_arni_acei_arb_target": "200",
        "gdmt_arni_acei_arb_start": enr_date.isoformat(),
        "gdmt_bb_drug": gdmt_bb,
        "gdmt_bb_dose": str(RNG.choice([12.5, 25, 50])),
        "gdmt_bb_target": "50",
        "gdmt_bb_start": enr_date.isoformat(),
        "gdmt_mra_drug": gdmt_mra,
        "gdmt_mra_dose": "25" if gdmt_mra != "0" else "",
        "gdmt_mra_target": "25",
        "gdmt_mra_start": enr_date.isoformat() if gdmt_mra != "0" else "",
        "gdmt_sglt2_drug": gdmt_sglt2,
        "gdmt_sglt2_dose": "10" if gdmt_sglt2 != "0" else "",
        "gdmt_sglt2_start": enr_date.isoformat() if gdmt_sglt2 != "0" else "",
        "gdmt_hfpef_glp1": "1" if lvef_cat == "3" and RNG.random() < 0.4 else "0",
        "gdmt_generic_bridge": RNG.choice(["0", "1"]),
        "gdmt_init_tier": facility_tier,
        "redcap_repeat_instrument": "",
        "redcap_repeat_instance": "",
    }
    return row


def monthly_row(rid: int, month: int, base_date: date, track: str) -> dict[str, str]:
    visit_date = base_date + timedelta(days=30 * month + RNG.randint(-3, 3))
    weight_drift = RNG.uniform(-2, 2)
    row = {
        "record_id": str(rid),
        "redcap_repeat_instrument": "monthly_followup",
        "redcap_repeat_instance": str(month),
        "mo_event_number": str(month),
        "mo_date": visit_date.isoformat(),
        "mo_track": track,
        "mo_weight_lb": f"{180 + weight_drift:.1f}",
        "mo_sbp": str(RNG.randint(100, 140)),
        "mo_dbp": str(RNG.randint(60, 88)),
        "mo_hr": str(RNG.randint(58, 84)),
        "mo_spo2": str(RNG.randint(94, 99)),
        "mo_egfr": f"{RNG.uniform(35, 70):.1f}",
        "mo_k": f"{RNG.uniform(3.6, 4.8):.1f}",
        "mo_bnp": str(RNG.randint(200, 2500)) if month % 3 == 0 else "",
        "mo_gdmt_change": RNG.choice(["0", "0", "0", "1"]),
        "mo_gdmt_change_notes": "",
        "mo_red_flag_count": str(RNG.choice([0, 0, 0, 1])),
        "mo_hosp_any": "0",
        "mo_hosp_hf": "",
        "mo_ed_any": "0",
        "mo_ed_hf": "",
        "mo_kccq12_score": str(RNG.randint(55, 90)),
    }
    return row


def outcomes_row(rid: int, baseline: dict[str, str]) -> dict[str, str]:
    mortality = RNG.random() < 0.08
    hf_hosp_count = RNG.randint(0, 3) if not mortality else RNG.randint(1, 4)
    return {
        "record_id": str(rid),
        "out_vital_status": "2" if mortality else "1",
        "out_death_date": (date(2026, 12, 15) - timedelta(days=RNG.randint(0, 250))).isoformat() if mortality else "",
        "out_death_cardiovascular": "1" if mortality and RNG.random() < 0.7 else ("0" if mortality else ""),
        "out_hf_hosp_count": str(hf_hosp_count),
        "out_hf_ed_count": str(RNG.randint(0, 5)),
        "out_days_alive_oh": str(365 - hf_hosp_count * RNG.randint(3, 10)) if not mortality else str(RNG.randint(30, 300)),
        "out_gdmt_optimized": "1" if RNG.random() < 0.55 else "0",
        "out_kccq12_12mo": str(RNG.randint(55, 95)) if baseline.get("bl_pro_consent") == "1" else "",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    baselines = [synth_row(rid) for rid in range(1, 21)]

    all_columns: list[str] = []
    seen: set[str] = set()
    for b in baselines:
        for k in b:
            if k not in seen:
                all_columns.append(k)
                seen.add(k)

    monthly_keys = [
        "record_id", "redcap_repeat_instrument", "redcap_repeat_instance",
        "mo_event_number", "mo_date", "mo_track", "mo_weight_lb", "mo_sbp", "mo_dbp",
        "mo_hr", "mo_spo2", "mo_egfr", "mo_k", "mo_bnp", "mo_gdmt_change",
        "mo_gdmt_change_notes", "mo_red_flag_count", "mo_hosp_any", "mo_hosp_hf",
        "mo_ed_any", "mo_ed_hf", "mo_kccq12_score",
    ]
    for k in monthly_keys:
        if k not in seen:
            all_columns.append(k)
            seen.add(k)

    outcome_keys = [
        "out_vital_status", "out_death_date", "out_death_cardiovascular",
        "out_hf_hosp_count", "out_hf_ed_count", "out_days_alive_oh",
        "out_gdmt_optimized", "out_kccq12_12mo",
    ]
    for k in outcome_keys:
        if k not in seen:
            all_columns.append(k)
            seen.add(k)

    rows_out: list[dict[str, str]] = []
    rows_out.extend(baselines)
    for rid in (1, 2):
        base_date = date.fromisoformat(baselines[rid - 1]["enr_date"])
        track = "A" if rid == 1 else "B"
        for m in range(1, 13):
            rows_out.append(monthly_row(rid, m, base_date, track))
    for rid, b in enumerate(baselines, 1):
        outcome = {"record_id": str(rid), **outcomes_row(rid, b)}
        rows_out.append(outcome)

    with args.output.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=all_columns, extrasaction="ignore")
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    print(f"Wrote {args.output} — {len(rows_out)} rows, {len(all_columns)} columns")
    print(f"  20 baselines / 24 monthly / 20 outcomes")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
