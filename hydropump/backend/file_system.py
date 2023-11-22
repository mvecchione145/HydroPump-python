import os
from pathlib import Path
from typing import Optional, Union

from ..instruction import Instruction, Template
from .base import Backend, SupportedFileExtensions, InstructionType


class FileSystemBackend(Backend):
    """
    Backend implementation for file system storage.
    """

    def __init__(
        self,
        file_extension: SupportedFileExtensions,
        root_directory: Optional[Union[str, Path]] = Path(),
    ) -> None:
        """
        Initialize the file system backend.

        Args:
            file_extension (SupportedFileExtensions): The supported file extension.
            root_directory (Optional[Union[str, Path]], optional): The root directory. Defaults to Path().
        """
        self.root_directory = Path(root_directory)
        if not self.root_directory.exists:
            raise FileNotFoundError(
                "Root Directory must exist for FileSystemBackend to initialize"
            )
        super().__init__(backend_type="FileSystem", file_extension=file_extension)
        self._set_sub_directories()

    def _set_sub_directories(self):
        """
        Create base and template sub-directories if they don't exist.
        """
        base_path = Path(self.root_directory, "base")
        template_path = Path(self.root_directory, "template")
        if not base_path.exists():
            os.mkdir(base_path)
        if not template_path.exists():
            os.mkdir(template_path)

    def _get_path(self, identifier: str, object_type: InstructionType) -> Path:
        """
        Get the path for the given identifier and object type.

        Args:
            identifier (str): The identifier.
            object_type (InstructionType): The object type.

        Returns:
            Path: The path.
        """
        object_type = InstructionType(object_type)
        return Path(
            self.root_directory,
            object_type.value,
            f"{identifier}.{self.file_extension.value}",
        )

    def get_template(self, template_id: str) -> Template:
        """
        Get the template with the given template ID.

        Args:
            template_id (str): The template ID.

        Returns:
            Template: The template object.
        """
        path = self._get_path(identifier=template_id, object_type="template")
        if not path.exists():
            raise FileNotFoundError(f"template ({template_id}) not found in backend.")
        with open(path) as f:
            payload = self.load(f)
        return Template(
            metadata=payload.get("metadata", {}),
            source=payload.get("template", {}),
            template_id=template_id,
        )

    def get_base(self, instruction_id: str) -> Instruction:
        """
        Get the base with the given instruction ID.

        Args:
            instruction_id (str): The instruction ID.

        Returns:
            Instruction: The base instruction object.
        """
        path = self._get_path(identifier=instruction_id, object_type="base")
        if not path.exists():
            raise FileNotFoundError(f"base ({instruction_id}) not found in backend.")
        with open(path) as f:
            payload = self.load(f)
        return Instruction(
            instruction_id=instruction_id,
            metadata=payload.get("metadata", {}),
            source=payload.get("instruction", {}),
        )

    def put_template(
        self,
        template: Optional[Template] = None,
        template_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        source: Optional[dict] = None,
    ) -> None:
        """
        Put the template into the backend.

        Args:
            template (Optional[Template], optional): The template object. Defaults to None.
            template_id (Optional[str], optional): The template ID. Defaults to None.
            metadata (Optional[dict], optional): The template metadata. Defaults to None.
            source (Optional[dict], optional): The template source. Defaults to None.

        Returns:
            None
        """
        if template is None and template_id is None:
            raise ValueError("Need either template_id or template to identify.")
        template_id = template_id or template.template_id
        source = source or template.source
        metadata = metadata or template.metadata
        if template is None:
            template = Template(
                template_id=template_id, metadata=metadata, source=source
            )
        path = self._get_path(identifier=template_id, object_type="template")
        if path.exists():
            os.remove(path)
        with open(path, "w") as f:
            self.dump(template, f)
        return template

    def put_base(
        self,
        instruction: Optional[Instruction] = None,
        instruction_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        source: Optional[dict] = None,
    ) -> Instruction:
        """
        Put the base instruction into the backend.

        Args:
            instruction (Optional[Instruction], optional): The instruction object. Defaults to None.
            instruction_id (Optional[str], optional): The instruction ID. Defaults to None.
            metadata (Optional[dict], optional): The instruction metadata. Defaults to None.
            source (Optional[dict], optional): The instruction source. Defaults to None.

        Returns:
            Instruction: The base instruction object.
        """
        if instruction is None and instruction_id is None:
            raise ValueError("Need either instruction_id or instruction to identify.")
        instruction_id = instruction_id or instruction.instruction_id
        source = source or instruction.source
        metadata = metadata or instruction.metadata
        if instruction is None:
            instruction = Instruction(
                instruction_id=instruction_id, metadata=metadata, source=source
            )
        path = self._get_path(identifier=instruction_id, object_type="base")
        if path.exists():
            os.remove(path)
        with open(path, "w") as f:
            self.dump(instruction, f)
        return instruction

    def delete_template(
        self,
        template: Optional[str] = None,
        template_id: Optional[str] = None,
    ) -> None:
        """
        Delete the template.

        Args:
            template (Optional[Template], optional): The template object. Defaults to None.
            template_id (Optional[str], optional): The template ID. Defaults to None.
        """
        if template is None and template_id is None:
            raise ValueError("Need either instruction_id or instruction to identify.")
        template_id = template_id or template.template_id
        path = self._get_path(identifier=template_id, object_type="template")
        if path.exists():
            os.remove(path)

    def delete_base(
        self,
        instruction: Optional[Instruction] = None,
        instruction_id: Optional[str] = None,
    ) -> None:
        """
        Delete the base instruction.

        Args:
            instruction (Optional[Instruction], optional): The instruction object. Defaults to None.
            instruction_id (Optional[str], optional): The instruction ID. Defaults to None.
        """
        if instruction is None and instruction_id is None:
            raise ValueError("Need either instruction_id or instruction to identify.")
        instruction_id = instruction_id or instruction.instruction_id
        path = self._get_path(identifier=instruction_id, object_type="base")
        if path.exists():
            os.remove(path)
