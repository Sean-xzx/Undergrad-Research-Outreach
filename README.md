[English](README.md) | [简体中文](README.zh-CN.md)

# Undergraduate Research Outreach v1.1.4

A Codex skill for evidence-grounded supervisor discovery and undergraduate research outreach. It preserves drafting, follow-up, interview and trial-task guidance while adding broad discovery, condition checks and a local evidence ledger.

## Multi-target outreach (v1.1.4)

Direction priorities persist when new screenshots arrive. Before declaring a draft ready, check the actual internship host, duration, location, materials and channel; keep unresolved conditions explicit. Model aliases, scoped availability and latest edits remain traceable. Public-source failures and missing form evidence are reported within the checked scope. [Twenty multi-target cases](evals/multi-target-cases.json) are a protocol, not executed model results.

## Writing and application forms (v1.1.3)

Paper selection considers the student's interests and the faculty member's documented role together. New guidance handles acceptance/publication conflicts, short participation plans when requested, English form answers, and field-level recovery of user edits. Form preparation, submission and email sending stay separate. [Form regression cases](evals/form-cases.json) are a test protocol, not executed model results.

## Writing update (v1.1.2)

Drafting now connects verified experience to supported abilities and research fit, keeps concrete appreciation separate from scientific claims, preserves user edits during local revisions, and checks recent work and collaboration attribution. No new student facts or framework skills are inferred. See the [writing evaluation cases](evals/writing-cases.json) and [validation scope](docs/validation.md).

## Discovery and records (v1.1)

Three modes distinguish quick starts, broad discovery and targeted verification. Broad discovery follows institutions/departments, paper authors and project collaborations. Research relevance, inquiry readiness and verified public conditions remain separate.

The bundled Python/SQLite ledger stores stable identities, source-linked claims, canonical papers, scoped constraints, search tasks and immutable contact events. Ingestion is transactional and idempotent; changed sources invalidate dependent supported claims. Narrative news cannot substitute for verified annual paper counts. Legacy imports retain originals without promoting them to verified facts.

## Install and use

Install `undergrad-research-outreach/` into your host's skills directory. Back up an existing installation; keep student records in the user's project. Host rediscovery may require a new chat.

> Use $undergrad-research-outreach. I am a second-year undergraduate interested in embodied world-action models. Please discover candidates broadly, separate direct and adjacent research, and retain sources and unknown participation conditions.

This is an example, not an executed model evaluation. Existing letters or professor replies can enter directly at their current stage. [Chinese usage guide](docs/usage.zh-CN.md), [runtime contract](undergrad-research-outreach/references/runtime.md).

## Requirements and verification

The instruction workflow needs a skill-capable host and browsing tools. The ledger uses Python 3.12+ standard libraries; repository validation additionally uses PyYAML. There is no standalone crawler, model API client or email sender.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_project.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_package.py
.venv/bin/python scripts/validate_project.py --archive dist/undergrad-research-outreach-v1.1.4.zip
```

On Windows replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`. CI checks Windows/Linux Python 3.12. The current package contains 12 verified public files; the seven-file v1.0 manifest is preserved separately. Private records, databases, generated candidate spreadsheets and backups are excluded.

## Architecture and evidence

[Design](docs/design.md) · [Development](docs/development.md) · [Validation](docs/validation.md) · [Sources](docs/sources.md) · [Behavior evaluation](evals/README.md) · [Issues](https://github.com/Sean-xzx/Undergrad-Research-Outreach/issues)

Unit/integration tests check deterministic business invariants and release packaging. Model behavior cases are provided as a separate evaluation protocol, not claimed as executed results. No improved discovery, reply or acceptance rate has been established. Source truth and semantic classification still require actual reading and review.

**All rights reserved; no open-source license is granted.** Use, modification and redistribution require permission. [Rights](COPYRIGHT.md). Original sources and dependencies retain their own rights.
