# Test matrix

| Path / adversarial case | Expected result | Local coverage |
|---|---|---|
| Complete disclosure, exact successful transaction | `ALIGNED` | Yes |
| Material action/recipient omission | `DIVERGENT` | Yes |
| Hidden privileged effect | `DIVERGENT` | Yes |
| Unknown or malformed semantic output | `REVIEW_REQUIRED` | Yes |
| Source 5xx | `RETRYABLE`, then opener may cancel | Yes |
| Wrong hash, executor, status or missing decode | `REVIEW_REQUIRED` / invalid source | Yes |
| Opener attempts self-assessment | Revert + full rollback | Yes |
| Verified transaction replay across observations | Revert + full rollback | Yes |
| Duplicate intent | Revert + counter unchanged | Yes |
| One challenge corrects semantic finding | Same snapshot; round 2 result | Yes |
| Challenge source unavailable | Preserve snapshot; remain `CHALLENGED` | Yes |
| Outsider challenges | Revert + full rollback | Yes |
| Prompt injection in disclosure | Treated as data; no positive bypass | Yes |
| Comparative consensus failure | Non-positive | Yes |
| Invalid input | Revert + no record | Yes |
| Arbitrary non-deployer wallet opens | Success | Yes |
| Deployer authority | Exactly `NONE` | Yes |

Local result on 2026-10-13: 25 passed. Live StudioNet rows remain pending
deployment and must not be marked complete without explorer-linked transactions
and post-transaction readbacks.
