# Proof obligation and epistemic boundary

## Positive claim

For observation `i`, `ALIGNED` means all of the following were established by
comparative validator consensus for the exact fixed-origin transaction snapshot:

1. the returned transaction hash equals the assessor-supplied hash;
2. the transaction target equals the executor sealed by the opener;
3. Blockscout reports transaction status `ok` and supplies bounded decoded input;
4. the sealed disclosure materially covers action, recipient/target, value and
   visible authority-changing effects;
5. no material privileged effect visible in decoded input is omitted; and
6. every consequential semantic field agrees across validators.

All mandatory facts must be positive. `UNKNOWN`, malformed model output,
consequential validator disagreement and incomplete decoding cannot produce
`ALIGNED`.

## What is not proved

BallotMirror does not prove proposal existence, vote passage, contributor
identity, signer authority, economic safety, legality, token-transfer logs not
represented in decoded calldata, internal traces, proxy implementation state,
or any timing relationship. The GenLayer clock is intentionally unused.

The external transaction is authoritative only for the bounded calldata facts
returned by the selected Blockscout API. The opener's `proposal_ref` and
disclosure are untrusted claims.

## Source and object binding

The contract selects the hostname from an internal chain-key map. Users cannot
supply a URL. It checks returned hash, target, success status, decoded structure,
field bounds and payload size. It stores a digest of the exact canonical object
used by validators. The raw calldata is validated and represented in that object
by its SHA-256 digest to bound storage.

## Challenge rule

A challenge is a single clarification, not a mutation of canonical facts. It
must reproduce the original snapshot digest. Source unavailability or a changed
snapshot leaves the challenge open and preserves the original snapshot.
