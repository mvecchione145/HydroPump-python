from ... import FileSystemBackend, Service


def test_create_instruction(
    example_id: str, example_metadata: dict, example_source: dict
):
    """
    Test case for the `create_instruction` method of the Service class.

    Parameters:
    - example_id (str): The ID of the example instruction.
    - example_metadata (dict): The example instruction metadata.
    - example_source (dict): The example instruction payload.

    Steps:
    1. Create an instance of the FileSystemBackend class with the file_extension set to "json"
       and the root_directory set to "hydropump/test/unit/test_root".
    2. Create an instance of the Service class with the backend set to the previously created fs_backend instance.
    3. Call the create_instruction method of the hp_service instance, passing in the example_id as instruction_id
       and example_source as source and example_metadata as metadata.
    4. Call the get_instruction method of the hp_service instance, passing in the example_id
       and store the returned instruction in a variable named 'instruction'.
    5. Assert that the length of the keys of the instruction dictionary is greater than 0.
    6. Call the delete_instruction method of the hp_service instance, passing in the instruction_id of the instruction.
    """
    fs_backend = FileSystemBackend(
        file_extension="json", root_directory="hydropump/test/unit/test_root"
    )
    hp_service = Service(backend=fs_backend)
    hp_service.create_instruction(
        instruction_id=example_id, metadata=example_metadata, source=example_source
    )
    instruction = hp_service.get_instruction(example_id)
    assert len(instruction.keys()) > 0


#  hp_service.delete_instruction(instruction_id=instruction.instruction_id)
