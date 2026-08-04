## 3. Research Method

The study follows a design-science research methodology. Design science is appropriate when the objective is to create and evaluate an artifact that addresses a recognized organizational or information-systems problem (Peffers et al., 2007). The process used here contains six connected activities.

### 3.1 Problem identification and motivation

The problem was identified through operational work involving recurring healthcare RCM exports and analytics pipelines. The observed failure modes included inconsistent filenames, changing schemas, duplicate extracts, mixed reporting grains, manually edited raw files, fragmented mapping logic, unresolved classifications, weak lineage, and dashboards built before reconciliation. These patterns created a gap between available data and defensible decision support.

### 3.2 Objectives for a solution

The artifact was required to satisfy the following objectives:

- preserve raw source evidence without manual correction;
- assign every discovered file an explicit disposition;
- detect byte-identical duplicates before loading;
- recognize approved report families through contracts;
- quarantine schema drift rather than coercing it silently;
- preserve unknown report families for onboarding;
- separate raw values from approved canonical mappings;
- retain source and transformation lineage in clean records;
- enforce financial and structural invariants;
- prevent unresolved classifications from becoming permanent semantic labels;
- produce deterministic publication status;
- support SQL and BI consumption without binding the concept to one vendor;
- permit public reproduction using synthetic, non-PHI data.

### 3.3 Design and development

The artifact was implemented as a layered architecture, a Python reference pipeline, SQL Server data-definition scripts, synthetic input files, governed mapping examples, automated tests, and a QA-control matrix. The design evolved from an operational architecture into a smaller public reference implementation. Historical technology choices that were no longer required were excluded from the public baseline. The resulting package uses Python for intake and demonstration logic, CSV for inspectable synthetic fixtures, and SQL Server scripts for persistent control, mapping, clean-fact, QA, and mart objects.

### 3.4 Demonstration

Two scenarios were created. Scenario A intentionally contains a byte-identical duplicate, a claim export with schema drift, an unknown operational export, and an accepted claim record containing an unmapped payer. Scenario B contains only conforming report files and a complete mapping set. Both scenarios use the same financial reconciliation rule and lineage requirements.

### 3.5 Evaluation

Evaluation uses executable acceptance tests and control outcomes rather than claims of clinical effectiveness. The tests verify that the dirty scenario surfaces each intended exception and returns RED, while the resolved scenario returns GREEN. Evaluation measures include file accountability, duplicate detection, schema-drift detection, unknown-family visibility, mapping completeness, row-level lineage, and financial reconciliation.

### 3.6 Communication

The communication package includes this manuscript, an architecture diagram, source code, SQL scripts, synthetic datasets, test results, mapping examples, a control workbook, citation metadata, and deposit checklists. The artifact is designed for archival through a research repository and linkage to an ORCID record after a DOI is assigned.
