## 2. Background and Problem Context

### 2.1 Data quality is broader than correctness

A common failure in operational analytics is to treat data quality as a binary question: either a value is correct or it is not. Wang and Strong (1996) demonstrated that data consumers evaluate quality through broader categories, including intrinsic, contextual, representational, and accessibility dimensions. That observation remains relevant to RCM. A claim amount may be numerically correct but contextually misleading if its date basis is unclear. A payer field may be complete but not interoperable if the same plan appears under several raw strings. A denial table may contain valid codes but remain unusable if the relationship between codes, categories, procedure lines, and claim outcomes is undocumented.

Health-data research has developed more specialized terminology. Weiskopf and Weng (2013) reviewed methods for assessing electronic health record data quality and highlighted recurring dimensions such as completeness, correctness, concordance, plausibility, and currency. Kahn et al. (2016) proposed a harmonized framework organized around conformance, completeness, and plausibility, evaluated through verification against local expectations or validation against external standards. Although RCM exports are administrative rather than clinical research datasets, the same logic applies. A report can be assessed for conformance to a declared schema, completeness of required fields and populations, and plausibility of financial relationships and categorical values.

The practical implication is that one “data quality score” is insufficient. A governance architecture must expose which control failed, where it failed, how many records were affected, whether the issue is contained, and whether the output is fit for its intended use. A report that is adequate for a preliminary operational review may be inadequate for provider compensation, payer contracting, or formal financial reporting. Decision readiness is therefore a governed state, not an aesthetic property.

### 2.2 Provenance and reproducibility

Provenance records the origin, history, and transformation of data. The W3C PROV family formalizes relationships among entities, activities, and agents, providing a conceptual foundation for traceability (World Wide Web Consortium, 2013). More recent clinical data-warehouse research has shown that provenance can support quality management by linking errors and quality findings back to source data and transformation steps (Johns et al., 2025). In an RCM context, provenance should answer at least five questions:

1. Which source file produced this row?
2. What was the file’s byte-level fingerprint?
3. Which report-family contract was applied?
4. Which transformation and mapping versions were used?
5. Which quality controls passed or failed before publication?

Without these answers, investigation becomes dependent on memory and local spreadsheet history. The organization may know that a number changed, but not whether the change originated in a replacement file, a mapping revision, a transformation defect, a late payment, or a different reporting period. Row-level lineage does not eliminate errors, but it shortens the path from observed anomaly to root cause.

### 2.3 Systematic quality checks and transparent exceptions

The OHDSI Data Quality Dashboard illustrates the value of executable, systematic, and transparent checks. Its published evaluation describes thousands of configurable checks applied to a common data model, with findings summarized for review rather than silently repaired (Blacketer et al., 2021). The present architecture adopts the same general principle but applies it to operational RCM exports with heterogeneous report contracts and business mappings.

A central design choice is that unresolved values must remain visible. Many analytics systems use fallback labels such as “Unknown,” “Other,” or “Unclassified.” Such categories are sometimes legitimate, but they become dangerous when used as permanent containers for incomplete governance. If a new payer string is automatically assigned to “Other Commercial,” the dashboard may refresh successfully while payer performance becomes materially distorted. The clean-room architecture therefore distinguishes between an intentionally approved category and an unresolved mapping exception. The latter blocks or qualifies publication according to severity.

### 2.4 FAIR principles and reusable research artifacts

The FAIR principles call for digital research objects to be findable, accessible, interoperable, and reusable, with an emphasis on machine actionability as well as human use (Wilkinson et al., 2016). Production RCM data cannot generally be made openly accessible, and de-identification does not remove every contractual or re-identification risk. HHS guidance identifies Safe Harbor and Expert Determination as the two HIPAA de-identification methods, while also noting that de-identified data can retain nonzero re-identification risk (U.S. Department of Health and Human Services, n.d.).

For that reason, this project separates the public research artifact from the operational data environment. The architecture, code, schema, tests, mappings, and synthetic records can be published and reused; client files, patient identifiers, credentials, and proprietary operational evidence cannot. This separation supports transparent methods without treating a public repository as a substitute for a governed healthcare data environment.
