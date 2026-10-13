# Verification record

Date: 2026-10-13

## Completed

- `py -3.12 -m pytest tests -q --tb=short -p no:cacheprovider`
- Result: `25 passed`.
- `PYTHONUTF8=1 genvm-lint check contracts/ballot_mirror.py`
- Result: lint passed (3 checks), validation passed, 7 public methods.
- Runner header pinned to v0.2.16 with an exact immutable dependency hash.

## Windows test-runner note

The installed `gltest` loader uses POSIX unlink-after-dup semantics that Windows
rejects with `WinError 32`. `tests/conftest.py` delays only that temporary-file
unlink until process shutdown. It does not alter VM state, nondeterministic mocks,
consensus behavior or contract code.

## StudioNet

- Contract `0x86546300BF0Be7B423E7Eb2e9912E38f829E5E72` read back as
  `BALLOT_MIRROR_V1` with `deployer_authority = NONE`.
- Independent auxiliary wallets produced a committed `ALIGNED` result and a
  deterministic `SOURCE_INVALID` negative result.
- Three semantic-conflict assessments finalized `MAJORITY_DISAGREE`; post-state
  remained `SEALED`, proving no disputed AI output was committed.
- Explorer-linked details: `docs/STUDIONET_E2E.md`.
