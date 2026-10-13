# Threat model

| Threat | Contract response |
|---|---|
| Opener self-assesses | Revert; full record unchanged |
| Arbitrary/malicious URL | Impossible; source root selected internally |
| Wrong hash or executor returned | `SOURCE_INVALID`; never positive |
| Failed transaction or missing decoding | `SOURCE_INVALID`; never positive |
| Source timeout/429/5xx | `RETRYABLE`; no fabricated verdict |
| Model omits fields or emits invalid tokens | `REVIEW_REQUIRED` |
| Mandatory fact is `UNKNOWN` | `REVIEW_REQUIRED` |
| Definite material omission plus another unknown | `DIVERGENT`, never softened |
| Validator disagreement | Non-positive retryable standing |
| Prompt injection in user/source text | Inputs are delimited as untrusted data; deterministic gate remains decisive |
| Duplicate sealed intent | Revert before counter mutation |
| Same transaction reused by another observation | Revert after a verified observation |
| Challenge against different source snapshot | Original snapshot preserved; challenge remains open |
| Repeated challenge | Revert; record unchanged |
| Deployer intervention | No stored owner/admin/deployer capability exists |

## Residual risks

- Blockscout may decode calldata incorrectly or omit internal/log effects.
- Consensus may classify nuanced disclosure language incorrectly.
- A transaction can be semantically aligned while still malicious or unauthorized.
- A proxy target can change implementation outside the bounded snapshot.

These are documented limits, not converted into positive claims.
