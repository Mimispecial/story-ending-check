# Architecture

## Deployment boundary

Deploy once per story-ending review. The same source is reusable through a fresh deployment for another story, continuity boundary, and required-beat set.

Constructor data establishes the deployment subject and fixed role boundary. Later writes add only the bounded records permitted by the lifecycle; a completed instance cannot be reopened.

## Participants

The deployer is the author and controls beat setup, ending submission, the optional revision, and final adoption. Any address may cast one vote in the bounded three-reader round.

Addresses are normalized before authorization comparisons. Role checks and lifecycle gates execute before semantic assessment.

## State machine

`BEAT_SETUP → AWAITING_ENDING → CONTINUITY_CHECK → READER_ROUND → AUTHOR_DECISION or REVISION_REQUESTED → COMPLETE`

The phase-like field is the primary lifecycle lock. Each write advances that path, performs a documented bounded loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

The stored story title and setup, continuity boundary, ordered required beats, and current ending version. No external manuscript or reference is fetched.

Before consensus, the contract normalizes bounded text, copies required storage into plain local values, serializes a sorted JSON packet, and places it between explicit START/END delimiters. Nondeterministic callbacks do not read contract storage.

## Consensus boundary

Return a required-beat closure mask and COHERENT, OPEN_ENDED, or CONTRADICTORY continuity label.

The leader callback validates exact JSON shape, field types, closed labels, masks or codes, and length bounds. A validator reruns the same semantic operation and rejects disagreement before state is committed.

## Deterministic boundary

Beat freezing, versioning, one vote per address, exactly three reader votes, majority resolution, one revision, and author outcome are deterministic.

Important invariants:

- Required beats freeze before the author can submit an ending.
- A reader address can vote only once in a round, and resolution requires three votes.
- At most one revised ending can be submitted.
- AI does not judge literary quality and cannot force the author to adopt an ending.

No method sends value, pays rewards, escrows assets, deletes external data, calls another contract, or invokes a webhook.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and cannot be stored.
- Validator disagreement cannot commit the semantic result.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
