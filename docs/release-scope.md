# Release scope

- This initial release publishes a bilingual report, evaluation methodology, scenario catalog and selected numerical results.
- It excludes original execution materials and operational identifiers. It is not a complete executable benchmark release.
- The included script validates file integrity and numerical consistency; it cannot establish independently that an original model call or test execution occurred.

## Included

Customer-facing findings, model names, generation settings from the reported direct API experiments, scenario requirements summarized in ordinary business language, per-scenario run counts and acceptance results, calculated cost totals, timing summaries, and public research/pricing references.

The reports identify the role of automated scoring and AI-assisted analysis. Antigravity results are separate, with underlying settings described as tool-managed.

## Excluded

Original prompts and generated submissions; hidden tests and reference implementations; raw model requests/responses and reasoning traces; infrastructure configuration; internal source excerpts and model cards; credentials, account/project identifiers, private storage locations, local machine paths, personal contact details and token-bearing publication links; third-party dependency bundles and build artifacts.

Files are assembled in a separate repository using an explicit release allowlist. The release uses a generic contributor commit identity and a fresh history, without importing the working directory's history.

## What can be reproduced?

`python3 tools/recompute_results.py` recomputes complete-success rates, functional/regression/instruction totals and cost per success from the public data. It verifies cross-file counts, denominator rules and release checksums. It does not call a model, run the original checks, rebuild token charges from usage logs, or reproduce timing statistics from traces.

Full experiment reproduction would require a separately reviewed release of task specifications, test implementations, model-call orchestration and execution environments. Those materials are not part of this initial release.

## Privacy and maintenance

The initial release was reviewed for secrets, internal identifiers, private links and unintended files. This is a bounded review of the published files and Git history, not an absolute guarantee that no disclosure issue can exist.

Do not add raw archives, copied execution directories, credentials or signed URLs to this repository. New content needs a fresh content review, an updated file allowlist and checksum inventory, and successful numerical validation. A clean scan is not permission to disclose confidential material.

The HTML report does not include analytics or model-service requests. Its optional web fonts are requested from Google Fonts when internet access is available; the report uses local fallback fonts offline. Other external links lead to public documentation, papers or this GitHub repository.
