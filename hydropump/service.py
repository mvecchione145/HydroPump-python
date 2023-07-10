from datetime import datetime
from typing import Optional, Union

from .backend import Backend, FileSystemBackend
from .instruction import Instruction, Template


class Service:
    """
    A class representing a service that interacts with an underlying backend.

    Parameters:
    - backend (Optional[Backend]): An optional parameter specifying the backend to use.
      If not provided, a default FileSystemBackend instance will be used.
    """

    def __init__(
        self,
        backend: Optional[Backend] = None,
        backend_config: Optional[dict] = None,
        debug: Optional[bool] = False,
    ) -> None:
        """
        Initializes a new instance of the Service class.

        Parameters:
        - backend (Optional[Backend]): An optional parameter specifying the backend to use.
          If not provided, a default FileSystemBackend instance will be used.
        - backend_config (Optional[dict]): TODO
        - debug (Optional[bool]): TODO

        Raises:
        - ValueError: If the provided backend is not of type Backend.
        """
        self.backend = backend
        self.debug = debug
        if self.backend is None and backend_config is None:
            self.backend = FileSystemBackend()
        if not isinstance(self.backend, Backend):
            raise ValueError("Backend is not of type Backend.")

    def get_instruction(
        self, instruction_id: str, compile: Optional[bool] = True
    ) -> Instruction:
        """
        Retrieves an instruction from the backend based on the given instruction ID.

        Parameters:
        - instruction_id (str): The ID of the instruction to retrieve.
        - compile (Optional[bool]): TODO

        Returns:
        - Instruction: An Instruction object representing the retrieved instruction.
        """
        instruction = self.backend.get_base(instruction_id=instruction_id)
        if not self.debug and compile:
            instruction = self.backend.compile_instruction(instruction)
        return instruction

    def get_template(self, template_id: str) -> Template:
        return self.backend.get_template(template_id=template_id)

    def create_template(
        self, metadata: dict, source: dict, template_id: Optional[str]
    ) -> str:
        metadata.update({"createdAt": str(datetime.now())})
        return self.backend.put_template(
            metadata=metadata, source=source, template_id=template_id
        )

    def create_instruction(
        self, metadata: dict, source: dict, instruction_id: Optional[str] = None
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
        metadata.update({"createdAt": str(datetime.now())})
        instruction = Instruction(
            instruction_id=instruction_id, metadata=metadata, source=source
        )
        return self.backend.put_base(instruction=instruction)

    def update_template(
        self,
        template_id: str,
        metadata: Optional[dict] = None,
        source: Optional[dict] = None,
    ) -> str:
        template = self.backend.get_template(template_id=template_id)
        template.update_template(metadata=metadata, source=source)
        return self.backend.put_template(template=template)

    def update_instruction(
        self,
        instruction_id: str,
        metadata: Optional[dict] = None,
        source: Optional[dict] = None,
    ) -> Instruction:
        """
        Updates an existing instruction in the backend with the specified payload.

        Parameters:
        - instruction_id (str): The ID of the instruction to update.
        - payload (dict): The updated payload of the instruction.

        Returns:
        - Instruction: the updated Instruction object.
        """
        instruction = self.backend.get_base(instruction_id=instruction_id)
        instruction.update_instruction(metadata=metadata, source=source)
        return self.backend.put_base(instruction=instruction)

    def delete_template(self, template_id: str) -> None:
        self.backend.delete_template(template_id=template_id)

    def delete_instruction(self, instruction_id: str) -> None:
        """
        Deletes an instruction from the backend based on the given instruction ID.

        Parameters:
        - instruction_id (str): The ID of the instruction to delete.

        Returns:
        - None
        """
        self.backend.delete_base(instruction_id=instruction_id)
