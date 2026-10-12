# Validation evidence / 验证证据

Validation has four separate layers: release integrity, deterministic business behavior, model discovery behavior and actual outreach outcomes.

## Historical v1.0

The original seven-file v1.0 manifest is preserved in [baseline checksums](../checksums/skill-sha256-v1.0.0.json). Earlier evidence included 20 manual instruction scenarios and 12 repository tests. Published commit `054c23e364d257f6e8f244bf3dfc5b7fc7a28ba2` passed Windows/Linux [run 38058311571](https://github.com/Sean-xzx/Undergrad-Research-Outreach/actions/runs/38058311571). That evidence referred to the preserved instruction package, not improved discovery.

## Current v1.1

The current release intentionally changes core behavior and uses a separate [current manifest](../checksums/skill-sha256.json). The public allowlist contains 12 files. Repository tests check modified/missing bytes, metadata, links, private-file rejection, archive membership, deterministic packaging and output-path safety.

New business tests use fictional frozen evidence to check paper deduplication, formal/preprint/workshop exclusion, field evidence, incomplete-list unknowns, same-name identities, scoped exceptions, source invalidation, conflicts, immutable events, rollback, idempotence, interruption recovery and legacy preservation.

On 2026-10-12, local Windows/Python 3.12.14 execution passed 47 tests (35 ledger business tests and 12 release tests), skill frontmatter validation, current-package verification and historical v1.0 archive verification. Legacy import and original-record preservation were checked locally; private source records are not included in this evidence page.

[Actions](https://github.com/Sean-xzx/Undergrad-Research-Outreach/actions) contains published runs. Current-release CI status is checked after pushing; an earlier green run does not validate this version. These local tests are deterministic execution, not independent model discovery evaluation.

## Not established

The [behavior requests](../evals/cases.json) and [evaluation protocol](../evals/README.md) have not been run by an independent model as part of deterministic CI. The project does not claim improved recall, reduced user corrections, accurate current supervisor facts, reply rates or acceptance rates. Tests cannot prove semantic evidence interpretation or source truth. Live browsing and real contact events require separate dated evidence.

No model weights, training dataset, standalone crawler, automatic sender or paid-model client is included. Private student records are not published.
