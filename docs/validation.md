# Validation evidence / 验证证据

Validation has four separate layers: release integrity, deterministic business behavior, model discovery behavior and actual outreach outcomes.

## Historical v1.0

The original seven-file v1.0 manifest is preserved in [baseline checksums](../checksums/skill-sha256-v1.0.0.json). Earlier evidence included 20 manual instruction scenarios and 12 repository tests. Published commit `054c23e364d257f6e8f244bf3dfc5b7fc7a28ba2` passed Windows/Linux [run 38058311571](https://github.com/Sean-xzx/Undergrad-Research-Outreach/actions/runs/38058311571). That evidence referred to the preserved instruction package, not improved discovery.

## v1.1 deterministic baseline

The current release intentionally changes core behavior and uses a separate [current manifest](../checksums/skill-sha256.json). The public allowlist contains 12 files. Repository tests check modified/missing bytes, metadata, links, private-file rejection, archive membership, deterministic packaging and output-path safety.

New business tests use fictional frozen evidence to check paper deduplication, formal/preprint/workshop exclusion, field evidence, incomplete-list unknowns, same-name identities, scoped exceptions, source invalidation, conflicts, immutable events, rollback, idempotence, interruption recovery and legacy preservation.

On 2026-10-12, local Windows/Python 3.12.14 execution passed 47 tests (35 ledger business tests and 12 release tests), skill frontmatter validation, current-package verification and historical v1.0 archive verification. Legacy import and original-record preservation were checked locally; private source records are not included in this evidence page.

[Actions](https://github.com/Sean-xzx/Undergrad-Research-Outreach/actions) contains published runs. Current-release CI status is checked after pushing; an earlier green run does not validate this version. These local tests are deterministic execution, not independent model discovery evaluation.

On 2026-10-12, implementation commit `6165fa7475964447e92adc1c700a27793acacb26` passed both Windows and Linux jobs in [run 38199197977](https://github.com/Sean-xzx/Undergrad-Research-Outreach/actions/runs/38199197977). Both jobs executed source checks, all 47 tests, package construction and packaged-byte verification. A fresh clone of that published commit also passed these checks locally with the existing Python 3.12.14 validation environment. Later documentation commits have their own Actions runs.

## v1.1.2 writing update — 2026-10-15

Local Windows/Python execution passed the existing 47 tests and repository source validation after the writing/reference update. The runtime schema and ledger implementation are unchanged. The release still has 12 allowlisted skill files. Frontmatter and archive checks are reported separately from model behavior; the historical v1.0 archive remains preserved.

[Twenty writing cases](../evals/writing-cases.json) now supply fictional frozen inputs and observable acceptance criteria for ability inference, study scope, praise, preference updates, local-edit preservation, attribution and attachment status. These are a protocol, not executed model tests. The instructions were reviewed against these failure modes; no independent model comparison or reduction in user corrections has been established. See [evaluation procedure](../evals/README.md).

## v1.1.3 application-form update — 2026-10-15

After the selection, revision and form-writing changes, local Windows execution passed all 47 existing deterministic tests, frontmatter validation and source/link/checksum checks. Ledger code and schema are unchanged; the release continues to contain 12 allowlisted skill files.

[Sixteen form cases](../evals/form-cases.json) add fictional frozen inputs covering author-role evidence, changing plan preferences, acceptance/publication conflicts, compact English answers, field-level recovery and submission status. Their JSON structure was checked and the instructions reviewed against the described cases; no independent model run or prior/new output comparison has been executed. These cases supplement, rather than replace, the v1.1.2 writing protocol.

## v1.1.4 multi-target update — 2026-10-15

Local Windows execution passed all 47 existing deterministic tests, skill frontmatter validation and source/link/checksum checks after the priority, recruitment and organization changes. No ledger implementation or schema change was made. The package remains limited to 12 public skill files.

[Twenty multi-target cases](../evals/multi-target-cases.json) provide fictional inputs for persistent direction priorities, aliases, official recruitment checks, actual internship hosts, scoped availability, restricted sources and revision recovery. Their structure is validated separately from semantic behavior. These are not executed independent model evaluations; no reduction in user corrections or improved reply/acceptance rate is established.

## Not established

The [behavior requests](../evals/cases.json) and [evaluation protocol](../evals/README.md) have not been run by an independent model as part of deterministic CI. The project does not claim improved recall, reduced user corrections, accurate current supervisor facts, reply rates or acceptance rates. Tests cannot prove semantic evidence interpretation or source truth. Live browsing and real contact events require separate dated evidence.

No model weights, training dataset, standalone crawler, automatic sender or paid-model client is included. Private student records are not published.

## v1.1.5 revision continuity — 2026-10-16

The update is limited to instruction/reference decisions, documentation and a [12-case recovery protocol](../evals/revision-recovery-cases.json). Ledger implementation and schema are unchanged. Local validation covers the existing 47 deterministic tests, frontmatter, source/link/checksum integrity, package membership and the historical v1.0 archive. JSON structure checks and an author review of instruction coverage do not constitute independent model execution; no improvement in real outreach outcomes is claimed.
