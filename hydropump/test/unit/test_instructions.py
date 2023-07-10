import pytest

from ... import Service


@pytest.mark.run(order=1)
def test_create_template(
    test_service: Service,
    test_template: dict,
    test_template_id: str,
) -> None:
    _ = test_service.create_template(
        metadata={}, source=test_template, template_id=test_template_id
    )
    template = test_service.get_template(test_template_id)
    assert template["template"] == test_template


@pytest.mark.run(order=2)
def test_create_instruction(
    test_service: Service,
    test_instruction_id: str,
    test_metadata: dict,
    test_source: dict,
    expected_compiled_result: dict,
) -> None:
    test_service.create_instruction(
        instruction_id=test_instruction_id,
        metadata=test_metadata,
        source=test_source,
    )
    instruction = test_service.get_instruction(test_instruction_id)
    assert instruction == expected_compiled_result


@pytest.mark.run(order=3)
def test_delete_instruction(
    test_service: Service,
    test_instruction_id: str,
) -> None:
    test_service.delete_instruction(instruction_id=test_instruction_id)
    with pytest.raises(Exception):
        test_service.get_instruction(instruction_id=test_instruction_id)


@pytest.mark.run(order=4)
def test_delete_template(
    test_service: Service,
    test_template_id: str,
) -> None:
    test_service.delete_template(template_id=test_template_id)
    with pytest.raises(Exception):
        test_service.get_template(template_id=test_template_id)
