import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_story_continuity(default_account, secondary_account, tertiary_account):
    story = "Mara finds an unsigned map in a returned library book. It leads to a locked greenhouse holding her late grandfather's community seed records. The donor page is missing, a storm is expected, and Ivo brings an archive box and borrowed key."
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "story_ending_check.py")
    deployed = ok(factory.deploy_contract_tx(args=["The Greenhouse Map", story, "The ending may resolve the donor page and protect the records, but cannot change the established storm, map, greenhouse, or characters."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    author = factory.build_contract(address, account=default_account)
    ok(author.append_required_beat(args=["Address what happens to the missing page naming the community seed donors."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.append_required_beat(args=["Address how Mara and Ivo protect the records before the storm."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.freeze_story_requirements(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ending = "Mara finds the donor page behind the map frame. She and Ivo copy each donor name into the archive index, place the seed records in the dry archive box, and carry it to the library before the first storm rain reaches the greenhouse."
    ok(author.submit_ending(args=[ending]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(author.check_ending_continuity(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = author.get_state(args=[]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["phase"] == "READER_ROUND"
    assert state["continuity"] in ("COHERENT", "OPEN_ENDED", "CONTRADICTORY")
    observed = {"closure_mask": state["closure_mask"], "continuity": state["continuity"]}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
