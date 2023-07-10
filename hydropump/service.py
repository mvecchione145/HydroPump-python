from datetime import datetime
from typing import Optional

from .backend import Backend, FileSystemBackend
from .instruction import Instruction, Template


class Service:
    """
    A service class for managing instructions and templates.
    """

    def __init__(
        self,
        backend: Optional[Backend] = None,
        config: Optional[dict] = None,
        debug: Optional[bool] = False,
    ) -> None:
        """
        Initialize the Service instance.

        Args:
            backend (Optional[Backend]): The backend implementation to use.
            config (Optional[dict]): Configuration options for the backend.
            debug (Optional[bool]): Enable debug mode.
        """
        self.backend = backend
        self.debug = debug
        if self.backend is None and config is None:
            self.backend = FileSystemBackend()
        if config is not None and self.backend is None:
            self.backend = self._set_backend(config)
        if not isinstance(self.backend, Backend):
            raise ValueError("Backend is not of type Backend.")

    def _set_backend(config: dict) -> Backend:
        """
        Set the backend based on the provided configuration.

        Args:
            config (dict): The configuration options for the backend.

        Returns:
            Backend: The initialized backend instance.

        Raises:
            ValueError: If the backend type is not recognized.
        """
        backend_type = config.pop("backend_type")
        if backend_type == "FileSystem":
            return FileSystemBackend(**config)
        elif backend_type == "GCPBucket":
            return None  # TODO: implement
        elif backend_type == "AWSBucket":
            return None  # TODO: implement
        else:
            raise ValueError(f"backend type not recognized ({backend_type})")

    def get_instruction(
        self, instruction_id: str, compile: Optional[bool] = True
    ) -> Instruction:
        """
        Get an instruction by its ID.

        Args:
            instruction_id (str): The ID of the instruction.
            compile (Optional[bool]): Whether to compile the instruction. Defaults to True.

        Returns:
            Instruction: The retrieved instruction.

        Raises:
            NotImplementedError: If debug mode is not enabled and compilation is requested.
        """
        instruction = self.backend.get_base(instruction_id=instruction_id)
        if compile:
            instruction = self.backend.compile_instruction(instruction=instruction)
        return instruction

    def get_template(self, template_id: str) -> Template:
        """
        Get a template by its ID.

        Args:
            template_id (str): The ID of the template.

        Returns:
            Template: The retrieved template.
        """
        return self.backend.get_template(template_id=template_id)

    def create_template(
        self, metadata: dict, source: dict, template_id: Optional[str]
    ) -> str:
        """
        Create a new template.

        Args:
            metadata (dict): Metadata for the template.
            source (dict): Source code for the template.
            template_id (Optional[str]): The ID of the template. If not provided, a new ID will be generated.

        Returns:
            str: The ID of the created template.
        """
        metadata.update({"createdAt": str(datetime.now())})
        return self.backend.put_template(
            metadata=metadata, source=source, template_id=template_id
        )

    def create_instruction(
        self, metadata: dict, source: dict, instruction_id: Optional[str] = None
    ) -> Instruction:
        """
        Create a new instruction.

        Args:
            metadata (dict): Metadata for the instruction.
            source (dict): Source code for the instruction.
            instruction_id (Optional[str]): The ID of the instruction. If not provided, a new ID will be generated.

        Returns:
            Instruction: The created instruction.
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
        """
        Update an existing template.

        Args:
            template_id (str): The ID of the template.
            metadata (Optional[dict]): New metadata for the template.
            source (Optional[dict]): New source code for the template.

        Returns:
            str: The ID of the updated template.
        """
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
        Update an existing instruction.

        Args:
            instruction_id (str): The ID of the instruction.
            metadata (Optional[dict]): New metadata for the instruction.
            source (Optional[dict]): New source code for the instruction.

        Returns:
            Instruction: The updated instruction.
        """
        instruction = self.backend.get_base(instruction_id=instruction_id)
        instruction.update_instruction(metadata=metadata, source=source)
        return self.backend.put_base(instruction=instruction)

    def delete_template(self, template_id: str) -> None:
        """
        Delete a template by its ID.

        Args:
            template_id (str): The ID of the template.
        """
        self.backend.delete_template(template_id=template_id)

    def delete_instruction(self, instruction_id: str) -> None:
        """
        Delete an instruction by its ID.

        Args:
            instruction_id (str): The ID of the instruction.
        """
        self.backend.delete_base(instruction_id=instruction_id)
