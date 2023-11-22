import json
import yaml
from enum import Enum
from abc import ABC, abstractmethod

from ..instruction import Instruction


class InstructionType(Enum):
    template = "template"
    base = "base"


class SupportedFileExtensions(Enum):
    json = "json"
    yaml = "yaml"
    yml = "yaml"


class Backend(ABC):
    """
    Abstract base class for different backends.
    """

    def __init__(
        self, backend_type: str, file_extension: SupportedFileExtensions
    ) -> None:
        """
        Initialize the backend.

        Args:
            backend_type (str): The type of the backend.
            file_extension (SupportedFileExtensions): The supported file extension.
        """
        self.backend_type = backend_type
        self.file_extension = SupportedFileExtensions(file_extension)
        self.set_dump_load()

    def _compile(self, parent: dict, child: dict, output: dict = None) -> dict:
        """
        Recursively compile the parent and child dictionaries.

        Args:
            parent (dict): The parent dictionary.
            child (dict): The child dictionary.
            output (dict, optional): The output dictionary. Defaults to None.

        Returns:
            dict: The compiled dictionary.
        """
        if output is None:
            output = child
        for k, v in parent.items():
            if isinstance(v, (str, int, float, bool)):
                output[k] = v
            elif isinstance(v, list):
                output[k] = output.get(k, []) + v
            elif isinstance(v, dict):
                output[k] = self._compile(v, child.get(k, {}), output.get(k, {}))
        return output

    def compile_instruction(self, instruction: Instruction) -> Instruction:
        """
        Compile the instruction by applying templates.

        Args:
            instruction (Instruction): The instruction object.

        Returns:
            Instruction: The compiled instruction.
        """
        template = {}
        for template_id in instruction.metadata.get("templates", []):
            template_instruction = self.get_template(template_id)
            template = self._compile(template_instruction["template"], template)
        instruction.source = self._compile(instruction.source, template)
        instruction.metadata["compiled"] = True
        instruction.set_source()
        return instruction

    def set_dump_load(self):
        """
        Set the dump and load functions based on the file extension.
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
        Abstract method to delete base.
        """
        pass

    @abstractmethod
    def delete_template(self) -> None:
        """
        Abstract method to delete template.
        """
        pass

    @abstractmethod
    def get_base(self) -> None:
        """
        Abstract method to get base.
        """
        pass

    @abstractmethod
    def get_template(self) -> None:
        """
        Abstract method to get template.
        """
        pass

    @abstractmethod
    def put_base(self) -> None:
        """
        Abstract method to put base.
        """
        pass

    @abstractmethod
    def put_template(self) -> None:
        """
        Abstract method to put template.
        """
        pass
