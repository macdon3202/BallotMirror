# StudioNet E2E evidence

Run date: 2026-10-13
Contract: [`0x86546300BF0Be7B423E7Eb2e9912E38f829E5E72`](https://explorer-studio.genlayer.com/address/0x86546300BF0Be7B423E7Eb2e9912E38f829E5E72)

## Role separation

- Main wallet: deployed only; not used in any lifecycle call.
- Auxiliary opener: `0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`.
- Auxiliary assessor: `0xc67532aeF9D2879cBA9375a02E6217A3524657B8`.
- On-chain config readback: `deployer_authority = NONE`.

## Happy path — exact disclosure

External authority: [Optimism Blockscout transaction](https://optimism.blockscout.com/tx/0xe01e786b1207039697a73bba3110beb571a7a4ff0ce46dd772603923415fd118).

1. [Open observation 1](https://explorer-studio.genlayer.com/tx/0x7ed44447ec33f43406c9c0bc37030e4e15ddf2b485f8ce211214d648caaada8b)
2. [Assess from independent wallet](https://explorer-studio.genlayer.com/tx/0xb29e94a5d96eea36e3ee82fb57008b77d3b777bfd78c1149952568ab4a703936)

Readback: `ALIGNED`, `SOURCE_VERIFIED`, reason
`MATERIAL_EFFECTS_DISCLOSED`, snapshot digest
`0385f0366566e304da6aa72169c2336e908b66a429e3b80f4e836704085efded`.
All four mandatory disclosure flags are `YES`; hidden privileged effect is `NO`.

## Consensus-conflict / rollback evidence

External authority: [Optimism Blockscout transfer](https://optimism.blockscout.com/tx/0x82528e7256f31fc559e78c6e0955f9aff807c2b24119a1a472f000ec462e7363).

- [Open observation 2](https://explorer-studio.genlayer.com/tx/0x5e8cadf9fbf12b85fa81bdc611d29212d93e7ffb3d46c7c7ed80491e33e96f72)
- [Ambiguous assessment](https://explorer-studio.genlayer.com/tx/0x30b8de72e4465e5780a231993e5cecab7b6410749538b1bca1df75bfccdc3755): `MAJORITY_DISAGREE`
- [Retry](https://explorer-studio.genlayer.com/tx/0x62899a85c633b418069b7d4fc646ed1c641db72b027f462047cddae6b3f421e4): `MAJORITY_DISAGREE`
- [Open explicit-conflict observation 3](https://explorer-studio.genlayer.com/tx/0x87c75ba2185e517ff444ff1dca7d208a264bf83ed3aa7dd44a1ad04ed6f26a5a)
- [Explicit-conflict assessment](https://explorer-studio.genlayer.com/tx/0x5fceebcf1c77ec3a001332efd6163127d2d71266f40629e646499caeb6ab8328): `MAJORITY_DISAGREE`

Readback after all rejected assessments: observations 2 and 3 remain exactly
`SEALED`, `assessment_round = 0`, empty transaction/snapshot fields and zero
assessor. No conflicting AI outcome was committed.

## Deterministic source/object-binding failure

Observation 4 sealed an executor unequal to the canonical transaction target.

1. [Open wrong-executor case](https://explorer-studio.genlayer.com/tx/0x4a816552658982a52b238fa5aee167c88e5bf91ea02d0957b535d8bf50340a5e)
2. [Assess wrong-executor case](https://explorer-studio.genlayer.com/tx/0x43918169ff6f5228aa858b5bf0475f567c43775f95a6dad68d632b562488f93b)

Readback: `REVIEW_REQUIRED`, `SOURCE_INVALID`, reason
`SOURCE_OR_OBJECT_BINDING_INVALID`; every semantic field is `UNKNOWN` and no
snapshot was fabricated.

## Conclusion

Live evidence establishes a positive result, independent roles, exact external
source binding, deterministic negative handling, and consensus-conflict
rollback. A semantic `DIVERGENT` result is covered locally but is not falsely
claimed as committed live evidence; StudioNet validators disagreed and the
contract preserved pre-assessment state.
