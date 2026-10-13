# BallotMirror

BallotMirror is a contract-only GenLayer application that records whether a
sealed DAO execution disclosure materially matches one exact, canonical
transaction observed through a fixed Blockscout source.

It is deliberately narrow. It does **not** prove that a proposal passed, that a
signer was authorized, that an execution was beneficial, or that a transaction
was legally valid. It proves only the semantic relationship between disclosure
bytes sealed before assessment and the decoded effects of the bound transaction.

## Why GenLayer

Deterministic code binds the opener, executor, chain, transaction hash, source
snapshot, replay keys and lifecycle. Validators independently fetch the same
fixed-origin transaction object and compare its decoded material effects with
the sealed disclosure. A positive result requires unanimous semantic fields:
action, recipient, value and authority effects must be disclosed, and no hidden
privileged effect may be present.

## Distinct architecture

```text
wallet A seals prospective disclosure + exact executor
                         |
wallet B binds one public transaction hash
                         |
validators independently fetch fixed Blockscout endpoint
                         |
exact canonical snapshot digest + semantic field agreement
                         |
ALIGNED / DIVERGENT / REVIEW_REQUIRED immutable standing
                         |
one optional opener challenge re-fetches the exact snapshot
```

This is a `PROSPECTIVE_DUAL_SNAPSHOT_DIVERGENCE_LEDGER`, not an escrow, permit,
admin registry or payout gate. There are no funds, owner controls or deployer
privileges.

## Roles

- Main wallet: deployment only; the contract stores no deployer identity.
- Auxiliary wallet A: opens an observation and may submit its one challenge.
- Auxiliary wallet B: independently assesses and resolves a challenge.
- Any reviewer wallet can use the same public methods; there is no allowlist.

## Supported authority sources

- Optimism: `https://optimism.blockscout.com/api/v2/transactions/{hash}`
- Base: `https://base.blockscout.com/api/v2/transactions/{hash}`

`proposal_ref` is only a caller label. It is never treated as proof of a DAO
proposal, vote result or authorization.

## Public methods

- `open_observation(chain_key, executor, proposal_ref, disclosure)`
- `assess_execution(observation_id, transaction_hash)`
- `challenge_finding(observation_id, counter_statement)`
- `resolve_challenge(observation_id)`
- `cancel_observation(observation_id)`
- `get_observation(observation_id)`
- `get_config()`

## Local verification

```powershell
py -3.12 -m pytest tests -q --tb=short -p no:cacheprovider
$env:PYTHONUTF8='1'; genvm-lint check contracts\ballot_mirror.py
```

Verified locally: **25 tests passed**; lint and contract validation passed.
The four warnings are expected unused LLM mocks on tests where source validation
fails before AI evaluation.

Deploy `contracts/ballot_mirror.py` with the main wallet and no constructor
arguments. Do not use the deployer in lifecycle evidence.

StudioNet deployment:
[`0x86546300BF0Be7B423E7Eb2e9912E38f829E5E72`](https://explorer-studio.genlayer.com/address/0x86546300BF0Be7B423E7Eb2e9912E38f829E5E72).
Live evidence is recorded in [`docs/STUDIONET_E2E.md`](docs/STUDIONET_E2E.md).

After selecting real fixtures, copy
`docs/studionet-scenarios.example.json`, replace every placeholder, audit the
source URLs, and run `py scripts\\run_studionet_e2e.py CONTRACT_ADDRESS
docs\\studionet-scenarios.json`.

See [proof obligation](docs/PROOF_OBLIGATION.md),
[threat model](docs/THREAT_MODEL.md), [test matrix](docs/TEST_MATRIX.md), and
[test-source manifest](docs/TEST_RESOURCE_MANIFEST.md).
