## 5. Synthetic Demonstration and Results

### 5.1 Dataset

The synthetic dataset models three common report families: claim financial, provider payment, and denial. The clean scenario contains 180 claim records and 20 denial records. Claim fields include claim identifier, date of service, payer, provider, CPT, charge, payment, adjustment, balance, and status. Mapping files cover five payers, four providers, six CPT codes, and four denial codes. No real organization, patient, or transaction is represented.

Scenario A contains six files:

1. one conforming claim-financial file;
2. one conforming provider-payment file;
3. one conforming denial file;
4. one byte-identical copy of the claim file;
5. one claim file with a renamed payer column and an unexpected internal-note column;
6. one unknown operational queue export.

The accepted claim file also contains one payer value absent from the approved mapping. Scenario B contains only the three conforming report files and a complete mapping set.

### 5.2 Executed controls

The demonstration evaluates seven automated controls:

- INT-001: every source file receives a disposition;
- INT-002: byte-identical duplicates are blocked;
- INT-003: schema drift is quarantined;
- INT-004: unknown report families remain visible;
- MAP-001: accepted semantic values are fully mapped;
- FIN-001: charge equals payment plus adjustment plus balance;
- LIN-001: every clean record retains source filename and SHA-256.

The broader control workbook specifies additional production controls for provider, CPT, denial, business-key, row-count, status-integrity, and privacy requirements.

### 5.3 Results

| Measure | Scenario A: dirty | Scenario B: resolved |
|---|---:|---:|
| Source files discovered | 6 | 3 |
| Accepted files | 3 | 3 |
| Clean claim records | 180 | 180 |
| Clean denial records | 20 | 20 |
| Byte-identical duplicates | 1 | 0 |
| Schema-drift files | 1 | 0 |
| Pending-onboarding files | 1 | 0 |
| Unmapped values | 1 | 0 |
| Financial reconciliation exceptions | 0 | 0 |
| Records with source lineage | 200 | 200 |
| Overall status | **RED** | **GREEN** |

Scenario A behaved as intended. All six source files received a disposition. The duplicate was blocked, the drifted file was quarantined, and the unknown report family remained visible in pending onboarding. These contained exceptions generated YELLOW controls. The unresolved payer appeared in an accepted record, so mapping completeness returned RED and semantic publication was blocked. Importantly, the pipeline still preserved the source evidence and produced clean technical outputs for inspection; RED did not mean that evidence was deleted.

Scenario B passed every executed control. All three files matched approved contracts, all semantic values mapped, all 200 clean records retained source hashes, and no financial reconciliation exceptions were detected. The overall gate returned GREEN. Two automated acceptance tests passed in the supplied implementation.

### 5.4 Interpretation

The demonstration does not establish performance at enterprise scale, compare database engines, or prove improved financial outcomes. It evaluates the behavior of governance controls under deliberately constructed conditions. The result supports the core proposition: a pipeline can preserve and process problematic inputs without silently converting them into decision-ready data, and it can distinguish contained operational exceptions from publication blockers.

The RED result in Scenario A is a feature, not a failed demonstration. Many conventional pipelines would load the conforming files, ignore or manually move the other files, place the payer under “Unknown,” and refresh the dashboard. The governance-first architecture instead makes the incompleteness explicit and prevents an unresolved business meaning from becoming an authoritative metric.
