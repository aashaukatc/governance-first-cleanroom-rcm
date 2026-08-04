# Zenodo Deposit Checklist

1. Confirm `CITATION.cff` points to the canonical public repository.
2. Run `python run_demo.py` and `python -m pytest` from a clean checkout.
3. Confirm every file is synthetic and contains no PHI, credentials, client data, or proprietary screenshots.
4. Merge the release branch; the release workflow creates `v0.1.1` automatically.
5. Enable the repository in the Zenodo GitHub integration.
6. After Zenodo archives the release, record the assigned DOI in `CITATION.cff`, the README, manuscript, and ORCID.
7. Upload/archive the release and verify creators, title, description, license, keywords, related identifiers, and access rights.
8. Publish only after reviewing the Zenodo preview; then import the DOI into ORCID.
