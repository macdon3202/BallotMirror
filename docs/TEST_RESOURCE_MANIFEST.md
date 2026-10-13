# Test-resource manifest

## Rule

Live evidence must use real, stable, publicly readable transactions from one of
the contract's fixed authority sources. A test page, gist, local server, mutable
mock response or user-controlled proxy is not acceptable live evidence.

## Local deterministic resources

| Resource | Purpose | Authority status |
|---|---|---|
| `tests/test_ballot_mirror.py::transaction` | Bounded canonical fixture | Mock only; never presented as live fact |
| Direct Mode web mocks | Failure/object-binding branches | Mock only |
| Direct Mode LLM mocks | Semantic gate branches | Mock only |

## Required live resources before submission

For each live observation, record:

- chain key and exact Blockscout transaction URL;
- transaction hash and executor address;
- why the disclosure should be aligned/divergent/ambiguous;
- auxiliary opener and assessor addresses;
- GenLayer transaction hashes for open, assess and optional challenge/resolve;
- post-write `get_observation` readback;
- source-access date and an exact snapshot digest returned by the contract.

The main deployment wallet must not appear as opener, assessor, challenger or
challenge resolver. External transactions must be selected for decoded calldata
that remains within the contract's stated epistemic boundary.
