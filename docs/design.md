# Design and architecture / 设计与架构

v1.1 separates task routing, model-assisted discovery and deterministic evidence/state handling. The host performs browsing and semantic interpretation; the bundled Python ledger performs structural checks, reference validation, canonical-paper counting and transactional persistence. No standalone crawler or model API runner is included.

## Information flow

User facts and scoped constraints → coverage/search tasks → actual source reads → source-linked claims and identity resolution → condition evaluation → candidate views → explicitly authorized real contact events.

The three discovery paths are institution/department, paper-author reverse lookup and project collaboration. User corrections trigger same-class coverage reviews, not a permanent name whitelist. Search completion is relative to recorded scope; it does not prove worldwide completeness.

## Storage and rules

SQLite contains keyed typed JSON records, revision history and schema metadata. This is a small single-writer implementation, not a distributed graph service. Identities use stable IDs; canonical paper IDs must be resolved before ingestion. Claims contain field evidence tied to sources. Source changes mark dependent supported claims pending.

Annual counts require matching supported evidence for authors, venue year, formal status, paper type and CCF category/catalog. Counts are verified lower bounds. Fewer verified papers in an incomplete list remains UNKNOWN. Research candidates, inquiry readiness and public-condition matches are distinct. Events are immutable and never reset by candidate rebuilding.

## Modules

- [Entry](../undergrad-research-outreach/SKILL.md): modes and stage routing.
- [Discovery](../undergrad-research-outreach/references/discovery.md): scope, three paths, queues and stopping boundaries.
- [Evidence](../undergrad-research-outreach/references/evidence.md): factual and counting rules.
- [Runtime](../undergrad-research-outreach/references/runtime.md): executable contract and limitations.
- [Records](../undergrad-research-outreach/references/records.md): privacy and continuity.
- [Writing](../undergrad-research-outreach/references/writing.md): v1.1.2 connects experience to supported ability, concrete research appreciation and scoped revisions; current user edits take precedence over older drafts. Recent-paper scanning and collaboration attribution feed the choice of a research entry point. Personal preferences remain private.
- v1.1.3 extends writing with interest-and-role-based paper selection and application-field answers. Records distinguish latest edits from unresolved factual conflicts and preserve field-level revisions. Form preparation, actual submission and email sending remain separate states.
- v1.1.4 makes the user's direction priorities persistent across targets and new screenshots. Writing checks the relevant recruitment organization and conditions before readiness advice; evidence distinguishes model aliases, versions and limited-access findings. Scoped availability and meaningful conditions use existing records rather than new schema fields or a second state system.
- Follow-through and source-learning guidance remains available.

Original v1.0 fingerprints are preserved. v1.1 intentionally changes behavior and has its own manifest and packaging checks; the historical unchanged-byte policy is not presented as the current functional validation.

## v1.1.5 revision continuity

Complete drafts and scoped fragments have distinct provenance in existing private notes. Accepted lines are reused; a local topic change triggers only necessary subject/plan checks. Attachment and sending evidence do not follow from content acceptance. No ledger/schema change or parallel state system is introduced.
