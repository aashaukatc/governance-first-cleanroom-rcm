# Data Use and Privacy Boundary

## Included

All CSV records in this repository are generated synthetic fixtures created solely to test intake, mapping, lineage, reconciliation, and publication-gate behavior. Names, identifiers, dates, claim numbers, and financial values do not represent real people, organizations, or transactions.

## Excluded

The repository must not contain:

- patient names, dates of birth, addresses, medical-record numbers, account numbers, or claim identifiers from real systems;
- client files, screenshots, email chains, payer-portal exports, authorization records, or credentials;
- production connection strings, secrets, tokens, private keys, or environment files;
- proprietary mappings or operational metrics that the contributor is not authorized to disclose.

## Intended use

The fixtures may be used to reproduce the working paper's design-science demonstration, test extensions, teach governance patterns, and compare alternative implementations.

## Production use

A production deployment requires separate privacy, security, access-control, retention, audit, business-associate, incident-response, and legal review. A successful synthetic test does not establish HIPAA compliance, production readiness, or financial accuracy in a real organization.
