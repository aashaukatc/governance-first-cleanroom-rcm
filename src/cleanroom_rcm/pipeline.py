from __future__ import annotations
from pathlib import Path
import csv, json
from decimal import Decimal
from .intake import inspect_directory, to_dicts
from .mappings import load_mapping, canonical


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    cols = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)


def run_pipeline(raw_dir: Path, mappings_dir: Path, output_dir: Path, payer_patch: Path | None = None) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    intake = inspect_directory(raw_dir)
    accepted = {r.source_file: r for r in intake if r.status == "ACCEPTED"}

    payer_map = load_mapping(mappings_dir / "payer_mapping.csv", payer_patch)
    provider_map = load_mapping(mappings_dir / "provider_mapping.csv")
    cpt_map = load_mapping(mappings_dir / "cpt_mapping.csv")
    denial_map = load_mapping(mappings_dir / "denial_mapping.csv")

    clean_claims: list[dict] = []
    clean_denials: list[dict] = []
    unmapped: list[dict] = []

    for filename, rec in accepted.items():
        path = raw_dir / filename
        rows = read_rows(path)
        if rec.report_family == "claim_financial":
            for row in rows:
                payer = canonical(row["Payer Name"], payer_map)
                provider = canonical(row["Rendering Provider"], provider_map)
                cpt = canonical(row["CPT"], cpt_map)
                for domain, raw_value, mapped in [
                    ("payer", row["Payer Name"], payer),
                    ("provider", row["Rendering Provider"], provider),
                    ("cpt", row["CPT"], cpt),
                ]:
                    if mapped is None:
                        unmapped.append({"source_file": filename, "record_id": row["Claim No"],
                                         "domain": domain, "raw_value": raw_value})
                clean_claims.append({
                    "claim_id": row["Claim No"], "service_date": row["DOS"],
                    "payer": payer or "__UNMAPPED__", "provider": provider or "__UNMAPPED__",
                    "cpt": cpt or "__UNMAPPED__", "claim_status": row["Claim Status"],
                    "charge_amount": row["Charge Amount"], "payment_amount": row["Payment Amount"],
                    "adjustment_amount": row["Adjustment Amount"], "balance_amount": row["Balance Amount"],
                    "source_file": filename, "source_sha256": rec.sha256,
                })
        elif rec.report_family == "denial":
            for row in rows:
                payer = canonical(row["Payer Name"], payer_map)
                cpt = canonical(row["CPT"], cpt_map)
                dcode = canonical(row["Denial Code"], denial_map)
                for domain, raw_value, mapped in [("payer",row["Payer Name"],payer),("cpt",row["CPT"],cpt),("denial",row["Denial Code"],dcode)]:
                    if mapped is None:
                        unmapped.append({"source_file": filename, "record_id": row["Denial ID"],
                                         "domain": domain, "raw_value": raw_value})
                clean_denials.append({
                    "denial_id": row["Denial ID"], "claim_id": row["Claim No"],
                    "denial_date": row["Denial Date"], "payer": payer or "__UNMAPPED__",
                    "cpt": cpt or "__UNMAPPED__", "denial_code": dcode or "__UNMAPPED__",
                    "source_file": filename, "source_sha256": rec.sha256,
                })

    # QA calculations
    duplicate_count = sum(r.status == "QUARANTINED_DUPLICATE" for r in intake)
    drift_count = sum(r.status == "QUARANTINED_SCHEMA_DRIFT" for r in intake)
    pending_count = sum(r.status == "PENDING_ONBOARDING" for r in intake)
    recon_exceptions=[]
    for r in clean_claims:
        charge=Decimal(r["charge_amount"]); payment=Decimal(r["payment_amount"])
        adjustment=Decimal(r["adjustment_amount"]); balance=Decimal(r["balance_amount"])
        if abs(charge-payment-adjustment-balance) > Decimal("0.01"):
            recon_exceptions.append({"claim_id":r["claim_id"],"difference":str(charge-payment-adjustment-balance)})

    checks = [
        {"control_id":"INT-001","control":"Every source file receives a disposition","status":"GREEN" if len(intake)==len(list(raw_dir.glob('*.csv'))) else "RED","count":len(intake)},
        {"control_id":"INT-002","control":"Byte-identical duplicates are blocked","status":"YELLOW" if duplicate_count else "GREEN","count":duplicate_count},
        {"control_id":"INT-003","control":"Schema drift is quarantined","status":"YELLOW" if drift_count else "GREEN","count":drift_count},
        {"control_id":"INT-004","control":"Unknown report families remain visible","status":"YELLOW" if pending_count else "GREEN","count":pending_count},
        {"control_id":"MAP-001","control":"Accepted semantic values are fully mapped","status":"RED" if unmapped else "GREEN","count":len(unmapped)},
        {"control_id":"FIN-001","control":"Charge = payment + adjustment + balance","status":"RED" if recon_exceptions else "GREEN","count":len(recon_exceptions)},
        {"control_id":"LIN-001","control":"Clean records retain source filename and SHA-256","status":"GREEN" if all(r.get('source_sha256') for r in clean_claims+clean_denials) else "RED","count":len(clean_claims)+len(clean_denials)},
    ]
    statuses={c['status'] for c in checks}
    overall = "RED" if "RED" in statuses else ("YELLOW" if "YELLOW" in statuses else "GREEN")
    result = {
        "overall_status": overall,
        "source_file_count": len(intake),
        "accepted_file_count": len(accepted),
        "clean_claim_count": len(clean_claims),
        "clean_denial_count": len(clean_denials),
        "duplicate_count": duplicate_count,
        "schema_drift_count": drift_count,
        "pending_onboarding_count": pending_count,
        "unmapped_value_count": len(unmapped),
        "reconciliation_exception_count": len(recon_exceptions),
        "checks": checks,
    }
    (output_dir/"intake_registry.json").write_text(json.dumps(to_dicts(intake), indent=2), encoding="utf-8")
    (output_dir/"qa_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_csv(output_dir/"clean_claim_financial.csv", clean_claims)
    write_csv(output_dir/"clean_denials.csv", clean_denials)
    write_csv(output_dir/"unmapped_values.csv", unmapped)
    write_csv(output_dir/"reconciliation_exceptions.csv", recon_exceptions)
    return result
