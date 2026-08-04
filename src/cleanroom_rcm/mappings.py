from __future__ import annotations
from pathlib import Path
import csv


def load_mapping(path: Path, patch_path: Path | None = None) -> dict[str, dict[str, str]]:
    rows: list[dict[str, str]] = []
    for p in [path, patch_path]:
        if p and p.exists():
            with p.open("r", newline="", encoding="utf-8-sig") as f:
                rows.extend(csv.DictReader(f))
    return {r["raw_value"].strip(): r for r in rows if r.get("active", "1") == "1"}


def canonical(raw: str, mapping: dict[str, dict[str, str]]) -> str | None:
    item = mapping.get((raw or "").strip())
    return item.get("canonical_value") if item else None
