"""Recover evidence after transient RPC failure without replaying writes."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from run_studionet_e2e import EXPLORER, RPC, load_wallets, read, wait

ROOT = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 7:
        raise SystemExit("usage: recover_studionet_e2e.py CONTRACT SCENARIOS OPEN1 ASSESS1 OPEN2 ASSESS2")
    contract, scenario_file, *hashes = sys.argv[1:]
    scenarios = json.loads(Path(scenario_file).read_text(encoding="utf-8"))
    load_wallets()
    wallet_a = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    wallet_b = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    client = create_client(chain=studionet, account=wallet_a, endpoint=RPC)
    finalized = [wait(client, value) for value in hashes]
    config = read(client, contract, wallet_a, "get_config", [])
    cases = []
    for index, scenario in enumerate(scenarios):
        observation_id = index + 1
        final = read(client, contract, wallet_b, "get_observation", [observation_id])
        if final["state"] != scenario["expected_state"]: raise AssertionError({"id": observation_id, "final": final, "expected": scenario["expected_state"]})
        cases.append({"scenario": scenario, "observation_id": observation_id, "open": finalized[index * 2], "assess": finalized[index * 2 + 1], "final_readback": final})
    evidence = {"network": "studionet", "contract": contract, "contract_url": f"{EXPLORER}/address/{contract}", "wallet_a_opener": str(wallet_a.address), "wallet_b_assessor": str(wallet_b.address), "main_wallet_used_in_lifecycle": False, "config": config, "cases": cases}
    (ROOT / "docs" / "studionet-e2e.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__": main()
