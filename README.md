# Governance-First Clean-Room Architecture for Healthcare RCM Analytics

This repository is the reproducible companion to **A Governance-First Clean-Room Architecture for Transforming Fragmented Healthcare Revenue-Cycle Exports into Decision-Ready Analytics**.

It packages a design-science working paper, executable synthetic demonstration, SQL Server reference objects, governance controls, architecture assets, and publishing metadata.

## What the release proves

Using entirely synthetic, fictional, non-PHI data, the reference implementation demonstrates:

- immutable source handling with SHA-256 fingerprints;
- byte-identical duplicate detection;
- versionable report-family contracts;
- schema-drift quarantine;
- pending onboarding for unknown report families;
- governed payer, provider, CPT, and denial mappings;
- row-level source lineage;
- financial reconciliation;
- deterministic GREEN/YELLOW/RED publication gates;
- SQL Server schemas and a decision-mart pattern.

## Reproduce the evaluation

No database server is required for the Python demonstration.

```bash
python scripts/generate_synthetic_fixtures.py
python run_demo.py
python -m pytest -q
```

Expected results:

| Scenario | Expected gate | Reason |
|---|---:|---|
| `scenario_a_dirty` | **RED** | One accepted record has an unresolved fictional payer mapping. Duplicate, drift, and unknown-family inputs are preserved and visibly contained. |
| `scenario_b_resolved` | **GREEN** | Approved files conform to contracts, semantic mappings are complete, lineage is present, and financial equations reconcile. |

Both scenarios produce 180 clean synthetic claim records and 20 clean synthetic denial records. The dirty scenario also proves that RED blocks semantic publication without deleting source evidence.

## Primary artifacts

- [Manuscript source sections](publication/manuscript/)
- [Architecture diagram](docs/architecture.svg)
- [Machine-readable QA controls](docs/qa_control_matrix.csv)
- [Source provenance and claim boundaries](publication/SOURCE_PROVENANCE_AND_CLAIM_BOUNDARIES.md)
- [Package manifest](publication/PACKAGE_MANIFEST.md)

The evidence-gated **Build and publish release** workflow generates the archival DOCX, PDF, XLSX control workbook, PNG architecture figure, source ZIP, and SHA-256 checksum before creating GitHub Release `v0.1.1` for Zenodo.

## Repository map

| Location | Purpose |
|---|---|
| `data/` | Fictional mappings, report contracts, and remediation patch; raw fixtures are generated deterministically. |
| `src/cleanroom_rcm/` | Intake, contract, mapping, lineage, reconciliation, and QA implementation. |
| `sql/` | SQL Server control, cross-reference, clean-fact, QA-gate, and mart objects. |
| `outputs/` | Reproducible outputs for dirty and remediated scenarios. |
| `tests/` | Executable acceptance tests. |
| `docs/` | Architecture sources and QA-control workbook. |
| `publication/` | Sectioned manuscript source, deposit metadata, provenance, release manifest, and publication files. |
| `evidence/` | Test, accessibility, PDF-preflight, and release-validation records. |

## Data and privacy boundary

The release contains no production data, patient data, client data, credentials, screenshots, payer-portal material, or protected health information. Plan names, identifiers, dates, claim numbers, and financial values in the fixtures are fictional or mechanically generated.

Read [DATA_USE_AND_PRIVACY.md](DATA_USE_AND_PRIVACY.md) before extending the repository.

## Research status

This is a design-science reference architecture evaluated through a reproducible synthetic demonstration. It is not a clinical study, regulatory certification, independent financial audit, or complete production healthcare platform.

## Citation and archival

`CITATION.cff` and `.zenodo.json` include the author ORCID (https://orcid.org/0009-0009-0342-9877). The canonical source repository is https://github.com/aashaukatc/governance-first-cleanroom-rcm. Versioned GitHub releases are archived through Zenodo.

## License

Apache License 2.0.
