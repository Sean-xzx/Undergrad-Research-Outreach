# Behavior evaluation protocol

These are evaluation requests, not executed model results. [Cases](cases.json) define observable checks. Use fictional or redacted frozen source packets and separately audited reference entities/claims; do not treat a historical candidate spreadsheet as ground truth.

Give the executor only the request, skill and permitted sources. Keep expected names and suspected bugs out of its context. Record actual source reads, output, false inclusions, reference-set misses, unsupported PASS assertions, user corrections and repeated searches. Compare v1.0 and v1.1 on the same scope and budget. Reference-set recall is not global recall.

Offline CI runs business invariants and packaging, not independent model behavior. Live browsing needs a dated, separate run. Store private transcripts/results under ignored `evals/results/`; publish only redacted metrics with execution details. No contact messages or applications are sent in evaluation.

Structural tests cannot establish improved discovery or acceptance rates. Cases are a maintained manual/model test protocol; no model API credential or automatic model runner is included.

## Writing regression (v1.1.2)

[Writing cases](writing-cases.json) provide fictional frozen facts, revision inputs and observable acceptance criteria. Give the executor only each request and input packet; reserve acceptance criteria for assessment. Compare the prior and current writing skill on identical inputs. Record unsupported additions, lost facts, unintended changes and source-scope errors separately from style. These cases are not an automated model runner and are not claimed as executed model results.

## Application-form regression (v1.1.3)

[Form cases](form-cases.json) add 16 fictional frozen tasks covering author roles, interest-based selection, conflicting edits, changing preferences, concise drafts, form fields and submission states. Keep acceptance criteria hidden from the executor. Run prior and updated skills on the same input; assess source-supported facts before style. These cases have not been run as independent model evaluations.

## Multi-target regression (v1.1.4)

[Multi-target cases](multi-target-cases.json) provide 20 fictional frozen tasks for persistent interests, recruitment checks, hosting organizations, model aliases, scoped commitments and restricted evidence. Keep criteria hidden from the executor; compare prior/current instructions on identical inputs. No model execution or outreach-result improvement is claimed.

## Revision recovery (v1.1.5)

[Twelve recovery cases](revision-recovery-cases.json) cover scoped topic changes, renamed papers, accepted lines, fragment/body merging, stale files, metadata-only edits and independent content/attachment/send states. These are fictional frozen protocols. Validate packet structure separately; assess semantic behavior through actual runs, not string matching. No independent model execution is claimed.
