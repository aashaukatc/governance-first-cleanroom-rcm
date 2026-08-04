from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from cleanroom_rcm.intake import inspect_directory
from cleanroom_rcm.pipeline import run_pipeline
from generate_synthetic_fixtures import generate


def test_dirty_scenario_surfaces_every_exception(tmp_path):
    generate(ROOT)
    records = inspect_directory(ROOT / "data/scenario_a_dirty/raw")
    statuses = {record.status for record in records}
    assert "QUARANTINED_DUPLICATE" in statuses
    assert "QUARANTINED_SCHEMA_DRIFT" in statuses
    assert "PENDING_ONBOARDING" in statuses
    result = run_pipeline(
        ROOT / "data/scenario_a_dirty/raw",
        ROOT / "data/mappings",
        tmp_path / "dirty",
    )
    assert result["overall_status"] == "RED"
    assert result["clean_claim_count"] == 180
    assert result["clean_denial_count"] == 20
    assert result["unmapped_value_count"] > 0
    assert result["reconciliation_exception_count"] == 0


def test_resolved_scenario_is_green(tmp_path):
    generate(ROOT)
    result = run_pipeline(
        ROOT / "data/scenario_b_resolved/raw",
        ROOT / "data/mappings",
        tmp_path / "resolved",
        payer_patch=ROOT / "data/remediation/payer_mapping_patch.csv",
    )
    assert result["overall_status"] == "GREEN"
    assert result["clean_claim_count"] == 180
    assert result["clean_denial_count"] == 20
    assert result["unmapped_value_count"] == 0
    assert result["reconciliation_exception_count"] == 0
