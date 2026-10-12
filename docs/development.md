# Development and verification / 开发与验证

For the author and authorized evaluators. [Rights](../COPYRIGHT.md) are unchanged.

## Runtime

Python 3.12+, Git and PyYAML 6.0.3 for repository validation. The installed ledger uses only standard libraries. No credentials or network access are needed for deterministic tests. Public fixtures use fictional identities and example.org evidence.

```bash
python scripts/validate_project.py
python -m unittest discover -s tests -v
python scripts/build_package.py
python scripts/validate_project.py --archive dist/undergrad-research-outreach-v1.1.0.zip
```

Use the same virtual-environment interpreter for dependencies and commands. [Runtime operations](../undergrad-research-outreach/references/runtime.md), [behavior protocol](../evals/README.md).

## Intentional release changes

The explicit `CORE_FILES` allowlist, metadata version, checksum manifest, package name, CI and documentation must agree. Update the manifest only after reviewing an authorized change; never suppress an unexplained integrity failure. Preserve the v1.0 manifest. Tests reject extra private files and unsafe archive paths. Generated __pycache__ is ignored but never packaged.

Private records, outputs, databases and backups are ignored by Git. Stage only reviewed public paths; do not use blanket staging. Do not reset a user's ledger or overwrite existing profile/contact documents. Import legacy snapshots with originals intact and unsupported conclusions unverified.

## Validation boundaries

Business tests check counting, references, conflict/unknown handling, scoped exceptions, immutable events, idempotence, rollback and restart. Repository tests check YAML, links, checksum integrity and reproducible archives. They do not verify current professor facts or live model discovery. Behavior evaluation must use audited source packets and hidden reference answers; do not publish private user records.

Before publishing: run the complete checks, review the public diff, verify the archive manifest, then commit and push normally. Install only the verified package content, backing up a previous version. No force push is needed. Published CI results should be reported separately from local tests.
