from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Review one versioned ending"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"closure_mask": "11", "continuity": "COHERENT"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_reader_round_and_author_outcome():
    author_account, first_reader, second_reader = create_accounts(3)
    story = "Mara finds an unsigned map in a returned library book. It leads to a locked greenhouse holding her late grandfather's community seed records. The donor page is missing, a storm is expected, and Ivo brings an archive box and borrowed key."
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "story_ending_check.py")
    deployed = factory.deploy_contract_tx(args=["The Greenhouse Map", story, "The ending may resolve the donor page and protect the records, but cannot change the established storm, map, greenhouse, or characters."], account=author_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    author = factory.build_contract(address, account=author_account)
    reader_one = factory.build_contract(address, account=first_reader)
    reader_two = factory.build_contract(address, account=second_reader)
    ok(author.append_required_beat(args=["Address what happens to the missing page naming the community seed donors."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.append_required_beat(args=["Address how Mara and Ivo protect the records before the storm."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.freeze_story_requirements(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ending = "Mara finds the donor page behind the map frame. She and Ivo copy each donor name into the archive index, place the seed records in the dry archive box, and carry it to the library before the first storm rain reaches the greenhouse."
    ok(author.submit_ending(args=[ending]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.check_ending_continuity(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.cast_reader_vote(args=["KEEP"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(reader_one.cast_reader_vote(args=["KEEP"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(reader_two.cast_reader_vote(args=["KEEP"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.resolve_reader_round(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(author.record_author_outcome(args=["ADOPT", "The author adopts the coherent ending after the recorded reader majority."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert author.get_state(args=[]).call()["author_outcome"] == "ADOPT"
