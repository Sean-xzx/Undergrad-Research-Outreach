[English](README.md) | [简体中文](README.zh-CN.md)

# Undergrad Research Outreach

An evidence-based AI skill that helps undergraduates turn research interests into a concrete next step toward joining a university or research-institute group.

## Value, contribution, method, evidence

- **Value:** addresses the gap between “I want to do research” and finding a suitable professor, explaining relevant experience, and following an opportunity through.
- **Contribution:** defined an undergraduate-specific scope; synthesized 11 experience posts and two skill projects; designed the complete workflow, evidence records, and low-friction interaction; added reproducible validation and packaging. Development was author-led and AI-assisted.
- **Method:** enter at any stage, retrieve only the relevant guidance, connect professor work to the student's actual contribution, and track contact states through replies, interviews, trial tasks, and confirmed arrangements.
- **Evidence:** the v1.0 skill has **7 preserved files**, **20 documented manual scenarios**, and **12 repository regression tests**. Tests verify integrity, metadata, links, failure handling, and packaging; they do not establish improved professor reply or acceptance rates.

## What is implemented

Goal clarification → professor screening → paper introduction → CV and first email → follow-up → reply interpretation → interview/trial preparation → opportunity confirmation.

The skill accepts existing CVs, links, drafts, or replies. Beginners can use coursework and self-study evidence. It distinguishes the assistant's paper reading from the student's, avoids fabricated fit, and defaults to one main deliverable and one next step. See [design and sources](docs/design.md) and the [Chinese user guide](docs/usage.zh-CN.md).

## Quick start

For the owner or authorized evaluators; see [rights](COPYRIGHT.md).

**Requirements:** Git; a skill-capable Codex host for the outreach workflow; Python 3.12 for optional repository validation. The skill itself is Markdown/YAML and needs no Python, model weights, dataset, database, or repository API key. Live professor research needs the host's browsing tools; sending needs an available mail tool and specific authorization.

```bash
git clone https://github.com/Sean-xzx/Undergrad-Research-Outreach.git
cd Undergrad-Research-Outreach
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-cache-dir -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/validate_project.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/build_package.py
.\.venv\Scripts\python.exe scripts/validate_project.py --archive dist/undergrad-research-outreach-v1.0.0.zip
```

Linux/macOS shells: replace `.\.venv\Scripts\python.exe` with `.venv/bin/python` in the five commands above. Local verification used Windows and Python 3.12.14; [validation notes](docs/validation.md) distinguish local evidence, CI, and unverified host behavior.

Expected successful output includes:

```text
PASS: 7 core files unchanged; YAML and local documentation links valid.
Ran 12 tests
OK
Built undergrad-research-outreach-v1.0.0.zip: 7 verified skill files.
PASS: archive contains exactly the 7 original core files.
```

The generated ZIP includes only the skill. Dependency installation needs network access; validation, tests, and packaging work offline afterward and do not contact professors or call a model API. No GPU or paid service is needed for these checks. Host subscription/tool costs are separate; no specific response time is promised.

## Use in Codex

The folder `undergrad-research-outreach/` is the installable unit. For the local Codex setup used in this project, copy it into the user's `.codex/skills/` directory. Back up an existing installation before replacing it; host discovery may require a new session.

First installation in Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -LiteralPath .\undergrad-research-outreach -Destination "$env:USERPROFILE\.codex\skills" -Recurse
```

First installation in Linux/macOS shells:

```bash
mkdir -p ~/.codex/skills
cp -R undergrad-research-outreach ~/.codex/skills/
```

Then send:

> Use $undergrad-research-outreach. I am a second-year undergraduate with a Python course project and no publications. I am exploring summer research and do not know which professors to contact. Start from my current situation and give me one concrete next step.

This is an **illustrative input**, not a measured agent run. Expected behavior is to organize existing facts, ask only decision-relevant questions, and avoid inventing publications or silently sending mail. See [the worked scenario](examples/first-contact.md). If automatic discovery is unavailable, ask the host to read `undergrad-research-outreach/SKILL.md` and its relevant references.

## Structure and flow

```text
undergrad-research-outreach/  unchanged v1.0 skill and five stage references
docs/                       design, sources, usage, validation and development
examples/                   synthetic first-contact scenario
scripts/                    validator and skill-only ZIP builder
tests/                      isolated positive and negative regression tests
checksums/skill-sha256.json  protected core-file fingerprints
.github/workflows/          Windows/Linux Python 3.12 checks
```

`SKILL.md` routes the current situation to opportunity, writing, or follow-through guidance. `records.md` supplies a minimal persistent profile and contact record when needed; `learning.md` governs source-based revisions. The host supplies tools and judgment. The validator checks the preserved source and documentation; the builder packages the same verified bytes. [Module map](docs/design.md).

## Development, limits, and rights

- [Development and update commands](docs/development.md); [validation scope](docs/validation.md); [source index](docs/sources.md).
- This is a v1.0 instruction artifact, not a standalone crawler, mail sender, or trained model. Automated checks cannot prove factual browsing, stable agent compliance, or outreach outcomes. No measured success-rate improvement, performance benchmark, or cross-agent compatibility claim is provided.
- Private profiles, contact records, caches, backups, and machine-specific working notes are excluded. No secret configuration is needed for the repository checks.
- Report a reproducible tooling issue through [Issues](https://github.com/Sean-xzx/Undergrad-Research-Outreach/issues). Permission is required before using, modifying, or distributing the project; changes to core behavior are not authorized by public visibility.
- **All rights reserved. No open-source license is granted.** [Copyright and platform rights](COPYRIGHT.md). External references and dependencies retain their own rights.
