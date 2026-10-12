# Behavior evaluation protocol

These are evaluation requests, not executed model results. [Cases](cases.json) define observable checks. Use fictional or redacted frozen source packets and separately audited reference entities/claims; do not treat a historical candidate spreadsheet as ground truth.

Give the executor only the request, skill and permitted sources. Keep expected names and suspected bugs out of its context. Record actual source reads, output, false inclusions, reference-set misses, unsupported PASS assertions, user corrections and repeated searches. Compare v1.0 and v1.1 on the same scope and budget. Reference-set recall is not global recall.

Offline CI runs business invariants and packaging, not independent model behavior. Live browsing needs a dated, separate run. Store private transcripts/results under ignored `evals/results/`; publish only redacted metrics with execution details. No contact messages or applications are sent in evaluation.

Structural tests cannot establish improved discovery or acceptance rates. Cases are a maintained manual/model test protocol; no model API credential or automatic model runner is included.
