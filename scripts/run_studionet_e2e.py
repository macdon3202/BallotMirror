"""Run real BallotMirror cases with two non-deployer wallets."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC = "https://studio.genlayer.com/api"
EXPLORER = "https://explorer-studio.genlayer.com"
ROOT = Path(__file__).resolve().parents[1]


def load_wallets():
    for raw in (ROOT.parent / "secrets" / "genlayer-test-wallets.env").read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\"").strip("<>"))


def plain(value):
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)


def signals(info):
    status = str(info.get("status_name") or info.get("statusName") or info.get("status") or "UNKNOWN").upper()
    consensus = str(info.get("result_name") or info.get("consensus_result_name") or info.get("consensus_result") or "UNKNOWN").upper()
    data = info.get("consensus_data") if isinstance(info.get("consensus_data"), dict) else {}
    receipts = data.get("leader_receipt") or data.get("validators") or []
    if isinstance(receipts, dict): receipts = [receipts]
    leader = next((r for r in receipts if isinstance(r, dict) and str(r.get("mode", "")).lower() == "leader"), receipts[0] if receipts else {})
    result = leader.get("result") if isinstance(leader.get("result"), dict) else {}
    payload = result.get("payload") if isinstance(result.get("payload"), dict) else {}
    execution = str(leader.get("execution_result") or info.get("execution_result") or "UNKNOWN").upper()
    return status, consensus, execution, payload.get("readable") or result.get("readable")


def wait(client, tx_hash):
    for _ in range(200):
        try:
            info = plain(client.get_transaction(tx_hash))
        except Exception as exc:
            print(json.dumps({"poll_retry": tx_hash, "error": type(exc).__name__}), flush=True)
            time.sleep(3)
            continue
        status, consensus, execution, returned = signals(info)
        if status == "FINALIZED":
            if consensus not in {"MAJORITY_AGREE", "AGREE", "ACCEPTED"} or execution != "SUCCESS":
                raise AssertionError({"tx": tx_hash, "status": status, "consensus": consensus, "execution": execution})
            return {"hash": tx_hash, "url": f"{EXPLORER}/tx/{tx_hash}", "status": status, "consensus": consensus, "execution": execution, "returned": returned}
        time.sleep(3)
    raise TimeoutError(tx_hash)


def write(client, address, account, method, args):
    tx_hash = str(client.write_contract(address=address, function_name=method, account=account, args=args, value=0))
    print(json.dumps({"submitted": tx_hash, "method": method}), flush=True)
    return wait(client, tx_hash)


def read(client, address, account, method, args):
    return plain(client.read_contract(address=address, function_name=method, args=args, account=account))


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: run_studionet_e2e.py CONTRACT_ADDRESS SCENARIOS_JSON")
    contract, scenario_path = sys.argv[1], Path(sys.argv[2])
    scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))
    if not isinstance(scenarios, list) or not scenarios: raise ValueError("SCENARIOS_MUST_BE_NONEMPTY_LIST")
    load_wallets()
    wallet_a = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    wallet_b = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    client = create_client(chain=studionet, account=wallet_a, endpoint=RPC)
    config = read(client, contract, wallet_a, "get_config", [])
    if config.get("version") != "BALLOT_MIRROR_V1" or config.get("deployer_authority") != "NONE": raise AssertionError(config)
    cases = []
    roots = {"OPTIMISM": "https://optimism.blockscout.com/api/v2/transactions/", "BASE": "https://base.blockscout.com/api/v2/transactions/"}
    required = {"chain_key", "executor", "proposal_ref", "disclosure", "tx_hash", "expected_state", "source_url"}
    for scenario in scenarios:
        if not isinstance(scenario, dict) or set(scenario) != required: raise ValueError("INVALID_SCENARIO_SCHEMA")
        if scenario["source_url"].lower() != roots[scenario["chain_key"]] + scenario["tx_hash"].lower(): raise ValueError("SOURCE_URL_NOT_CANONICAL")
        opened = write(client, contract, wallet_a, "open_observation", [scenario["chain_key"], scenario["executor"], scenario["proposal_ref"], scenario["disclosure"]])
        observation_id = int(str(opened["returned"]).strip('"'))
        sealed = read(client, contract, wallet_a, "get_observation", [observation_id])
        assessed = write(client, contract, wallet_b, "assess_execution", [observation_id, scenario["tx_hash"]])
        final = read(client, contract, wallet_b, "get_observation", [observation_id])
        if sealed["state"] != "SEALED" or final["state"] != scenario["expected_state"]: raise AssertionError({"sealed": sealed, "final": final})
        cases.append({"scenario": scenario, "open": opened, "sealed_readback": sealed, "assess": assessed, "final_readback": final})
    evidence = {"network": "studionet", "contract": contract, "contract_url": f"{EXPLORER}/address/{contract}", "wallet_a_opener": str(wallet_a.address), "wallet_b_assessor": str(wallet_b.address), "main_wallet_used_in_lifecycle": False, "config": config, "cases": cases}
    (ROOT / "docs" / "studionet-e2e.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__": main()
