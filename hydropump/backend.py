import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Optional, Union

import yaml

from .instruction import Instruction, Template


class InstructionType(Enum):
    template = "template"
    base = "base"


class SupportedFileExtensions(Enum):
    """
    An enumeration representing supported file extensions.

    Attributes:
    - json (str): The file extension for JSON files.
    - yaml (str): The file extension for YAML files (also known as YML).
    """

    json = "json"
    # xml = "xml"
    yaml = "yaml"
    yml = "yaml"


class Backend(ABC):
    """
    Abstract base class representing a backend.

    Attributes:
    - backend_type (str): The type of the backend.
    - file_extension (SupportedFileExtensions): The supported file extension for the backend.
    - load (function): The function used to load data from the backend.
    - dump (function): The function used to dump data into the backend.
    """

    def __init__(
        self, backend_type: str, file_extension: SupportedFileExtensions
    ) -> None:
        """
        Initialize the Backend instance.

        Parameters:
        - backend_type (str): The type of the backend.
        - file_extension (SupportedFileExtensions): The supported file extension for the backend.
        """
        self.backend_type = backend_type
        self.file_extension = SupportedFileExtensions(file_extension)
        self.set_dump_load()

    def _compile(self, parent: dict, child: dict, output: dict = None) -> dict:
        if output is None:
            output = child
        for k, v in parent.items():
            if isinstance(v, (str, int, float, bool)):
                output[k] = v
            elif isinstance(v, list):
                output[k] = output.get(k, []) + v
            elif isinstance(v, dict):
                output[k] = self._compile(v, child.get(k, {}), output.get())
        return output

    def compile_instruction(self, instruction: Instruction) -> Instruction:
        """TODO: implement secrets/variables"""
        for template_id in instruction.metadata.get("templates", []):
            template_instruction = self.get_template(template_id)
            instruction.source = self._compile(
                instruction.source, template_instruction["template"]
            )
        instruction.set_source()
        return instruction

    def set_dump_load(self):
        """
        Set the appropriate load and dump functions based on the file extension.
        """
        if self.file_extension == SupportedFileExtensions.json:
            self.load = json.load
            self.dump = json.dump
        elif (
            self.file_extension == SupportedFileExtensions.yaml
            or self.file_extension == SupportedFileExtensions.yml
        ):
            self.load = yaml.safe_load
            self.dump = yaml.safe_dump

    @abstractmethod
    def delete_base(self) -> None:
        """
        Abstract method to delete the base from the backend.
        """
        pass

    @abstractmethod
    def delete_template(self) -> None:
        """
        Abstract method to delete the template from the backend.
        """
        pass

    @abstractmethod
    def get_base(self) -> None:
        """
        Abstract method to get the base from the backend.
        """
        pass

    @abstractmethod
    def get_template(self) -> None:
        """
        Abstract method to get the template from the backend.
        """
        pass

    @abstractmethod
    def put_base(self) -> None:
        """
        Abstract method to put the base into the backend.
        """
        pass

    @abstractmethod
    def put_template(self) -> None:
        """
        Abstract method to put the template into the backend.
        """
        pass


class FileSystemBackend(Backend):
    """
    A class representing a file system backend.

    Parameters:
    - file_extension (SupportedFileExtensions): The supported file extension for the backend.
    - root_directory (Optional[Union[str, Path]], optional): The root directory for the backend. Defaults to Path().

    Raises:
    - FileNotFoundError: If the root directory does not exist.

    Attributes:
    - root_directory (Path): The root directory for the backend.
    """

    def __init__(
        self,
        file_extension: SupportedFileExtensions,
        root_directory: Optional[Union[str, Path]] = Path(),
    ) -> None:
        """
        Initializes the FileSystemBackend.

        Parameters:
        - file_extension (SupportedFileExtensions): The supported file extension for the backend.
        - root_directory (Optional[Union[str, Path]], optional): The root directory for the backend. Defaults to Path().
        """
        self.root_directory = Path(root_directory)
        if not self.root_directory.exists:
            raise FileNotFoundError(
                "Root Directory must exist for FileSystemBackend to initialize"
            )
        super().__init__(backend_type="FileSystem", file_extension=file_extension)
        self._set_sub_directories()

    def _set_sub_directories(self):
        base_path = Path(self.root_directory, "base")
        template_path = Path(self.root_directory, "template")
        if not base_path.exists():
            os.mkdir(base_path)
        if not template_path.exists():
            os.mkdir(template_path)

    def _get_path(self, identifier: str, object_type: InstructionType) -> Path:
        """
        Returns the path for a given identifier.

        Parameters:
        - instruction_id (str): The ID of the instruction.
        - object_type (InstructionType): Will generate a prefix based on object_type.

        Returns:
        - Path: The path to the instruction file.
        """
        object_type = InstructionType(object_type)
        return Path(
            self.root_directory,
            object_type.value,
            f"{identifier}.{self.file_extension.value}",
        )

    def get_template(self, template_id: str) -> Template:
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
        Retrieves the contents of an instruction.

        Parameters:
        - instruction_id (str): The ID of the instruction.

        Raises:
        - FileNotFoundError: If file not found given instruction_id.

        Returns:
        - Instruction: The instruction object given instruction_id.
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
        Puts the contents of an instruction into a file.

        Parameters:
        - instruction (Optional[Instruction], optional): The instruction object. Defaults to None.
        - instruction_id (Optional[str], optional): The ID of the instruction. Defaults to None.
        - metadata (Optional[dict], optional): The metadata of the instruction. Defaults to None.
        - source (Optional[dict], optional): The payload of the instruction. Defaults to None.

        Raises:
        - ValueError: If either instruction or instruction_id is not provided.

        Returns:
        - Instruction: The instruction object given instruction_id.
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
        template_id: str,
    ) -> None:
        path = self._get_path(identifier=template_id, object_type="template")
        if path.exists():
            os.remove(path)

    def delete_base(
        self,
        instruction: Optional[Instruction] = None,
        instruction_id: Optional[str] = None,
    ) -> None:
        """
        Deletes the contents of an instruction.

        Parameters:
        - instruction (Optional[Instruction], optional): The instruction object. Defaults to None.
        - instruction_id (Optional[str], optional): The ID of the instruction. Defaults to None.

        Raises:
        - ValueError: If either instruction or instruction_id is not provided.
        """
        if instruction is None and instruction_id is None:
            raise ValueError("Need either instruction_id or instruction to identify.")
        instruction_id = instruction_id or instruction.instruction_id
        path = self._get_path(identifier=instruction_id, object_type="base")
        if path.exists():
            os.remove(path)
