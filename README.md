# Story Ending Check

Checks one versioned story ending against frozen continuity facts and required beats, then records a three-reader round while leaving adoption to the author.

## Why it is an Intelligent Contract

Return a required-beat closure mask and COHERENT, OPEN_ENDED, or CONTRADICTORY continuity label. GenLayer validators independently replay that semantic judgment before it becomes shared state. Beat freezing, versioning, one vote per address, exactly three reader votes, majority resolution, one revision, and author outcome are deterministic.

## Reusable deployment model

Deploy once per story-ending review. The same source is reusable through a fresh deployment for another story, continuity boundary, and required-beat set.

A completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer is the author and controls beat setup, ending submission, the optional revision, and final adoption. Any address may cast one vote in the bounded three-reader round.

State path: `BEAT_SETUP → AWAITING_ENDING → CONTINUITY_CHECK → READER_ROUND → AUTHOR_DECISION or REVISION_REQUESTED → COMPLETE`

## Evidence boundary

The stored story title and setup, continuity boundary, ordered required beats, and current ending version. No external manuscript or reference is fetched.

## Core invariants

- Required beats freeze before the author can submit an ending.
- A reader address can vote only once in a round, and resolution requires three votes.
- At most one revised ending can be submitted.
- AI does not judge literary quality and cannot force the author to adopt an ending.

## Public interface

Write methods: `append_required_beat, cast_reader_vote, check_ending_continuity, freeze_story_requirements, record_author_outcome, resolve_reader_round, revise_ending, submit_ending`

View methods: `get_ending_version, get_policy, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/story_ending_check.py
genvm-lint typecheck contracts/story_ending_check.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and uses three disposable Mimi-only accounts protected outside the workspace. It asserts finalized successful execution and reads committed state with `LATEST_FINAL`.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0x71a6be83bbd6aA002C3c0725A826a1722668A054
- Studio import: https://studio.genlayer.com/?import-contract=0x71a6be83bbd6aA002C3c0725A826a1722668A054
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0x9246cfb0a72b0fdc066117c48645db89bb1ac6504443c5ec690697ca245b462f
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x124c646cbec866faf51b55ab63f7af5f04932ffd03ce1fb2615ce88596246ba4
- Observed committed state: `{"closure_mask":"11","continuity":"COHERENT"}`
- Audited source SHA-256: `75b045ec9bce05b95c3301be91ff09acb84c6f88b3c6d0294a4262d1cf8fee88`

## Limitations

- Continuity is evaluated only against the stored setup, boundary, and beats.
- Reader votes are pseudonymous addresses and are not identity-verified audience research.
- The result is drafting feedback, not a copyright, authorship, or publication determination.

## Repository map

- `contracts/story_ending_check.py` — Intelligent Contract source
- `tests/direct` — hardened leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — reviewer material

License: MIT.
