# Source Provenance and Claim Boundaries

## Purpose

This record explains how prior operational work informed the publication while preventing private client information, historical design drift, and commercial-product plans from being misrepresented as public empirical evidence.

## Evidence classes

| Evidence class | Examples reviewed | How it was used |
|---|---|---|
| Project-governance record | `08_Project_Names_and_Context.md` | Established the separation between client-specific RCM analytics and the separate DIRT commercial-product direction; confirmed immutable-source, mapping, QA, and privacy principles. |
| Operational repository documentation | private `aashaukatc/rcm-data-platform` README and architecture/status documents | Identified recurring failure modes, intake responsibilities, warehouse layers, historical architecture changes, and honest GREEN/YELLOW/RED status practices. |
| Executable operational controls | SQL validation-gate scripts and Power BI gate artifacts | Informed mapping-population checks, fact-integrity checks, orphan-key checks, no-silent-gap rules, and deterministic go/no-go behavior. |
| Public scholarly and standards literature | data-quality, provenance, FAIR, design-science, and HHS de-identification sources | Supplied the external conceptual foundation and citations in the manuscript. |
| Public reference implementation | files in this release | Provides the only executable evidence reported in the Results section. All evaluation data are synthetic. |

## Implemented and demonstrated in this public release

- SHA-256 source-file fingerprints;
- byte-identical duplicate detection;
- report-family contracts;
- schema-drift quarantine;
- pending onboarding for unknown report families;
- governed payer, provider, CPT, and denial mappings;
- clean claim and denial outputs with source-file lineage;
- charge/payment/adjustment/balance reconciliation;
- deterministic GREEN/YELLOW/RED status;
- SQL Server reference DDL and QA gates;
- two automated acceptance tests and reproducible evidence outputs.

## Documented design patterns, not claimed as public production validation

- enterprise orchestration, monitoring, notification, and role-based stewardship;
- full multi-specialty report coverage;
- production-scale performance, refresh duration, or compute efficiency;
- production PHI handling or regulatory certification;
- real-world financial improvement, denial reduction, or collection uplift;
- multi-tenant authentication, authorization, billing, support, and commercial SaaS readiness.

## Explicit exclusions

The publication does not use or disclose:

- patient-level or client-level source data;
- patient names, account numbers, authorization references, screenshots, or email chains;
- exact client operational metrics as study results;
- proprietary payer or practice mappings;
- private repository code as the public executable artifact;
- the DIRT product roadmap as evidence that a production platform exists.

## Architecture evolution

Historical materials contained both MongoDB-assisted and later SQL Server-only variants, along with retired Docker and Metabase components. The paper abstracts the stable governance controls and provides a smaller vendor-neutral reference pattern. The supplied SQL scripts use SQL Server for persistence; the Python demonstration uses CSV and JSON so that reviewers can reproduce the control behavior without a database server.

## Public-claim rule

A claim appears in the manuscript's Results section only when it can be reproduced from this release with:

```bash
python run_demo.py
python -m pytest -q
```

Historical operational records are used for problem motivation and design provenance, not as independently verified study outcomes.
