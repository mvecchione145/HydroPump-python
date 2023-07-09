from typing import Optional, Union

from .backend import Backend, FileSystemBackend
from .instruction import Instruction


class Service:
    """
    A class representing a service that interacts with an underlying backend.

    Parameters:
    - backend (Optional[Backend]): An optional parameter specifying the backend to use.
      If not provided, a default FileSystemBackend instance will be used.
    """

    def __init__(self, backend: Optional[Backend] = None) -> None:
        """
        Initializes a new instance of the Service class.

        Parameters:
        - backend (Optional[Backend]): An optional parameter specifying the backend to use.
          If not provided, a default FileSystemBackend instance will be used.

        Raises:
        - ValueError: If the provided backend is not of type Backend.
        """
        self.backend = backend
        if self.backend is None:
            self.backend = FileSystemBackend()
        if not isinstance(self.backend, Backend):
            raise ValueError("Backend is not of type Backend.")

    def get_instruction(self, instruction_id: str) -> Instruction:
        """
        Retrieves an instruction from the backend based on the given instruction ID.

        Parameters:
        - instruction_id (str): The ID of the instruction to retrieve.

        Returns:
        - Instruction: An Instruction object representing the retrieved instruction.
        """
        payload = self.backend.get_contents(instruction_id=instruction_id)
        return Instruction(instruction_id=instruction_id, payload=payload)

    def create_instruction(
        self, payload: dict, instruction_id: Optional[str] = None
    ) -> Instruction:
        """
        Creates a new instruction in the backend with the specified payload and instruction ID.

        Parameters:
        - payload (dict): The payload of the instruction to create.
        - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
          If not provided, a unique ID will be generated.

        Returns:
        - Instruction: the created Instruction object.
        """
        instruction = Instruction(instruction_id=instruction_id, payload=payload)
        return self.backend.put_contents(instruction=instruction)

    def update_instruction(self, instruction_id: str, payload: dict) -> Instruction:
        """
        Updates an existing instruction in the backend with the specified payload.

        Parameters:
        - instruction_id (str): The ID of the instruction to update.
        - payload (dict): The updated payload of the instruction.

        Returns:
        - Instruction: the updated Instruction object.
        """
        instruction = Instruction(instruction_id=instruction_id, payload=payload)
        return self.backend.put_contents(instruction=instruction)

    def delete_instruction(self, instruction_id: str) -> None:
        """
        Deletes an instruction from the backend based on the given instruction ID.

        Parameters:
        - instruction_id (str): The ID of the instruction to delete.

        Returns:
        - None
        """
        self.backend.delete_contents(instruction_id=instruction_id)
