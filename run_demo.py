from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from cleanroom_rcm.pipeline import run_pipeline
from generate_synthetic_fixtures import generate


def main() -> None:
    generate(ROOT)
    results = {
        "scenario_a_dirty": run_pipeline(
            ROOT / "data/scenario_a_dirty/raw",
            ROOT / "data/mappings",
            ROOT / "outputs/scenario_a_dirty",
        ),
        "scenario_b_resolved": run_pipeline(
            ROOT / "data/scenario_b_resolved/raw",
            ROOT / "data/mappings",
            ROOT / "outputs/scenario_b_resolved",
            payer_patch=ROOT / "data/remediation/payer_mapping_patch.csv",
        ),
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
