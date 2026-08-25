from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "story_ending_check.py"
SDK = "v0.2.16"
PROMPT = "Review one versioned ending"
STORY = "Mara finds an unsigned map inside a returned library book. The map leads to a locked greenhouse where her late grandfather kept community seed records. She discovers that the final page naming the seed donors is missing, while a storm is expected that evening. Her friend Ivo brings an empty archive box and a key borrowed from the librarian."
BOUNDARY = "The ending may resolve the missing donor page and protection of the seed records, but cannot introduce supernatural facts or change the established storm, map, greenhouse, or characters."
ENDING = "Mara finds the donor page tucked behind the map frame beside her grandfather's penciled inventory. She and Ivo copy every donor name into the archive index, place the seed records in the dry archive box, and carry it to the library before the first storm rain reaches the greenhouse."


def story(vm, direct_deploy, author):
    vm.sender = author
    contract = direct_deploy(str(CONTRACT), "The Greenhouse Map", STORY, BOUNDARY, sdk_version=SDK)
    contract.append_required_beat("Address what happens to the missing page that identifies the community seed donors.")
    contract.append_required_beat("Address how Mara and Ivo protect the greenhouse seed records before the storm.")
    contract.freeze_story_requirements()
    contract.submit_ending(ENDING)
    return contract


def test_continuity_three_reader_votes_and_author_adoption(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = story(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"closure_mask": "11", "continuity": "COHERENT"}))
    contract.check_ending_continuity()
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    contract.cast_reader_vote("KEEP")
    direct_vm.sender = direct_bob
    contract.cast_reader_vote("KEEP")
    direct_vm.sender = direct_charlie
    contract.cast_reader_vote("KEEP")
    direct_vm.sender = direct_alice
    contract.resolve_reader_round()
    contract.record_author_outcome("ADOPT", "The author adopts the coherent ending after the recorded reader majority while retaining editorial responsibility.")
    assert contract.get_state()["author_outcome"] == "ADOPT"


def test_reader_rewrite_majority_opens_one_revision(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    contract = story(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"closure_mask": "10", "continuity": "OPEN_ENDED"}))
    contract.check_ending_continuity()
    contract.cast_reader_vote("KEEP")
    direct_vm.sender = direct_bob
    contract.cast_reader_vote("REWRITE")
    direct_vm.sender = direct_charlie
    contract.cast_reader_vote("REWRITE")
    direct_vm.sender = direct_alice
    contract.resolve_reader_round()
    contract.revise_ending(ENDING + " They also leave a duplicate donor index with the greenhouse committee before locking the building.")
    assert contract.get_state()["version"] == 2
    assert contract.get_state()["revision_used"] is True


def test_duplicate_reader_vote_and_bad_mask_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = story(direct_vm, direct_deploy, direct_alice)
    direct_vm.mock_llm(PROMPT, json.dumps({"closure_mask": "111", "continuity": "COHERENT"}))
    with direct_vm.expect_revert("invalid_mask"):
        contract.check_ending_continuity()
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"closure_mask": "11", "continuity": "COHERENT"}))
    contract.check_ending_continuity()
    direct_vm.sender = direct_bob
    contract.cast_reader_vote("KEEP")
    with direct_vm.expect_revert("reader_already_voted"):
        contract.cast_reader_vote("REWRITE")
