from uuid import uuid4

import pytest

from ...hydropump import Backend, Instruction, Service


def test_create_instruction(example_instruction: dict):
    example_id = str(uuid4())
    service = Service()
    instruction = Instruction(example_instruction)
    service.create_instruction(instruction=instruction, identifier=example_id)
    payload = service.get_instruction(example_id)
    assert len(payload.keys()) > 0
