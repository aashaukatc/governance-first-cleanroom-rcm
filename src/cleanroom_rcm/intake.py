from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import hashlib
from .specs import REPORT_SPECS, ReportSpec

@dataclass
class IntakeRecord:
    source_file: str
    sha256: str
    size_bytes: int
    report_family: str | None
    status: str
    reason: str
    columns: list[str]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_header(path: Path) -> list[str]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        return next(reader, [])


def candidate_spec(path: Path, header: list[str]) -> ReportSpec | None:
    lower_name = path.name.lower()
    exact = [s for s in REPORT_SPECS if set(s.required_columns).issubset(set(header))]
    if len(exact) == 1:
        return exact[0]
    by_name = [s for s in REPORT_SPECS if all(t in lower_name for t in s.filename_tokens)]
    return by_name[0] if len(by_name) == 1 else None


def inspect_directory(raw_dir: Path) -> list[IntakeRecord]:
    seen: dict[str, str] = {}
    records: list[IntakeRecord] = []
    for path in sorted(raw_dir.glob("*.csv")):
        digest = sha256_file(path)
        header = read_header(path)
        if digest in seen:
            records.append(IntakeRecord(path.name, digest, path.stat().st_size, None,
                                        "QUARANTINED_DUPLICATE", f"Byte-identical to {seen[digest]}", header))
            continue
        seen[digest] = path.name
        spec = candidate_spec(path, header)
        if spec is None:
            records.append(IntakeRecord(path.name, digest, path.stat().st_size, None,
                                        "PENDING_ONBOARDING", "No approved report-family contract matched", header))
            continue
        required = set(spec.required_columns)
        actual = set(header)
        missing = sorted(required - actual)
        unexpected = sorted(actual - required - set(spec.optional_columns))
        if missing or unexpected:
            reason = f"Contract drift; missing={missing}; unexpected={unexpected}"
            records.append(IntakeRecord(path.name, digest, path.stat().st_size, spec.family,
                                        "QUARANTINED_SCHEMA_DRIFT", reason, header))
            continue
        records.append(IntakeRecord(path.name, digest, path.stat().st_size, spec.family,
                                    "ACCEPTED", "Contract matched", header))
    return records


def to_dicts(records: list[IntakeRecord]) -> list[dict]:
    return [asdict(r) for r in records]
