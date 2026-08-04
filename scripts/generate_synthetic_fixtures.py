#!/usr/bin/env python3
"""Generate deterministic, fictional, non-PHI RCM CSV fixtures."""
from __future__ import annotations

import csv
import random
import shutil
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 20260804

CLAIM_COLUMNS = [
    "Claim No", "DOS", "Payer Name", "Rendering Provider", "CPT",
    "Charge Amount", "Payment Amount", "Adjustment Amount", "Balance Amount", "Claim Status",
]
PAYMENT_COLUMNS = ["Payment ID", "Claim No", "Posting Date", "Payer Name", "Provider ID", "Payment Amount"]
DENIAL_COLUMNS = ["Denial ID", "Claim No", "Denial Date", "Payer Name", "CPT", "Denial Code", "Denial Category"]

PAYERS = [
    "Northstar Community Health",
    "Meridian Blue Health",
    "Summit United Plan",
    "Federal Senior Plan",
    "Harbor Community Plan",
]
PROVIDERS = ["PROV-001", "PROV-002", "PROV-003", "PROV-004"]
CPTS = ["99213", "99214", "93000", "97110", "97530", "11042"]
CHARGES = {
    "99213": Decimal("85.00"),
    "99214": Decimal("135.00"),
    "93000": Decimal("120.00"),
    "97110": Decimal("70.00"),
    "97530": Decimal("95.00"),
    "11042": Decimal("780.00"),
}
DENIAL_CODES = ["CO-16", "CO-50", "CO-97", "PR-204"]


def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def write_csv(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def build_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    rng = random.Random(SEED)
    claims: list[dict[str, str]] = []
    payments: list[dict[str, str]] = []
    denials: list[dict[str, str]] = []
    start = date(2026, 1, 1)

    for i in range(1, 181):
        claim_id = f"SYN-{i:06d}"
        cpt = CPTS[(i - 1) % len(CPTS)]
        provider = PROVIDERS[(i - 1) % len(PROVIDERS)]
        payer = "Frontier Regional Plan" if i == 179 else PAYERS[rng.randrange(len(PAYERS))]
        service_date = start + timedelta(days=rng.randrange(90))
        charge = CHARGES[cpt]
        denied = i % 9 == 0  # exactly 20 denial events across 180 claims
        partial = (i % 5 == 0) and not denied

        if denied:
            payment = Decimal("0.00")
            adjustment = Decimal("0.00")
            balance = charge
            status = "Denied"
        elif partial:
            payment = charge * Decimal("0.60")
            adjustment = charge * Decimal("0.20")
            balance = charge - payment - adjustment
            status = "Partially Paid"
        else:
            allowed_rate = Decimal(str(rng.choice(["0.72", "0.78", "0.84", "0.90"])))
            payment = charge * allowed_rate
            adjustment = charge - payment
            balance = Decimal("0.00")
            status = "Paid"

        claim = {
            "Claim No": claim_id,
            "DOS": service_date.isoformat(),
            "Payer Name": payer,
            "Rendering Provider": provider,
            "CPT": cpt,
            "Charge Amount": money(charge),
            "Payment Amount": money(payment),
            "Adjustment Amount": money(adjustment),
            "Balance Amount": money(balance),
            "Claim Status": status,
        }
        claims.append(claim)

        if payment > 0:
            payments.append({
                "Payment ID": f"PAY-{len(payments) + 1:06d}",
                "Claim No": claim_id,
                "Posting Date": (service_date + timedelta(days=14 + (i % 21))).isoformat(),
                "Payer Name": payer,
                "Provider ID": provider,
                "Payment Amount": money(payment),
            })

        if denied:
            denials.append({
                "Denial ID": f"DEN-{i:06d}",
                "Claim No": claim_id,
                "Denial Date": (service_date + timedelta(days=18)).isoformat(),
                "Payer Name": payer,
                "CPT": cpt,
                "Denial Code": DENIAL_CODES[(i // 9 - 1) % len(DENIAL_CODES)],
                "Denial Category": "",
            })

    assert len(claims) == 180
    assert len(denials) == 20
    return claims, payments, denials


def generate(root: Path = ROOT, *, clean: bool = True) -> None:
    claims, payments, denials = build_rows()
    scenario_a = root / "data" / "scenario_a_dirty" / "raw"
    scenario_b = root / "data" / "scenario_b_resolved" / "raw"
    if clean:
        for directory in [scenario_a.parent, scenario_b.parent]:
            shutil.rmtree(directory, ignore_errors=True)

    for directory in [scenario_a, scenario_b]:
        write_csv(directory / "claim_financial_export_2026Q1.csv", CLAIM_COLUMNS, claims)
        write_csv(directory / "provider_payments_export_2026Q1.csv", PAYMENT_COLUMNS, payments)
        write_csv(directory / "denials_export_2026Q1.csv", DENIAL_COLUMNS, denials)

    # Dirty-only evidence: exact duplicate, schema drift, and unknown family.
    shutil.copyfile(
        scenario_a / "claim_financial_export_2026Q1.csv",
        scenario_a / "claim_financial_export_2026Q1_COPY.csv",
    )
    drift_columns = [
        "Claim No", "DOS", "Rendering Provider", "CPT", "Charge Amount", "Payment Amount",
        "Adjustment Amount", "Balance Amount", "Claim Status", "Carrier Name", "Unexpected Internal Note",
    ]
    drift_rows = []
    for claim in claims[:12]:
        drift_rows.append({
            "Claim No": claim["Claim No"],
            "DOS": claim["DOS"],
            "Rendering Provider": claim["Rendering Provider"],
            "CPT": claim["CPT"],
            "Charge Amount": claim["Charge Amount"],
            "Payment Amount": claim["Payment Amount"],
            "Adjustment Amount": claim["Adjustment Amount"],
            "Balance Amount": claim["Balance Amount"],
            "Claim Status": claim["Claim Status"],
            "Carrier Name": claim["Payer Name"],
            "Unexpected Internal Note": "synthetic drift field",
        })
    write_csv(scenario_a / "claim_financial_export_2026Q2_CHANGED.csv", drift_columns, drift_rows)
    write_csv(
        scenario_a / "misc_operational_export.csv",
        ["Queue", "Items", "Owner"],
        [
            {"Queue": "A", "Items": "12", "Owner": "Team 1"},
            {"Queue": "B", "Items": "7", "Owner": "Team 2"},
        ],
    )


if __name__ == "__main__":
    generate()
    print("Generated deterministic synthetic fixtures for both scenarios.")
