# Contributing

Contributions are welcome when they preserve the repository's research and privacy boundaries.

## Required controls

1. Use only synthetic or explicitly public data.
2. Never commit patient, client, payer-portal, credential, or production extracts.
3. Preserve raw synthetic fixtures; resolve defects through contracts, mappings, or replacement fixtures rather than undocumented edits.
4. Add or update tests for every behavior change.
5. Keep GREEN/YELLOW/RED status semantics deterministic and evidence based.
6. Clearly distinguish implemented behavior from proposed production extensions.

## Local validation

```bash
python -m pip install -e ".[dev]"
python run_demo.py
python -m pytest -q
```

Pull requests should describe the control being changed, expected status behavior, test evidence, and any effect on the manuscript or data dictionary.
