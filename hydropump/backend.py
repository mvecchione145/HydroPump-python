import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Optional, Union

import yaml

from .instruction import Instruction


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
    def get_contents(self) -> None:
        """
        Abstract method to get the contents from the backend.
        """
        pass

    @abstractmethod
    def put_contents(self) -> None:
        """
        Abstract method to put the contents into the backend.
        """
        pass

    @abstractmethod
    def delete_contents(self) -> None:
        """
        Abstract method to delete the contents from the backend.
        """
        pass


class FileSystemBackend(Backend):
    """
    A class representing a file system backend.

    Parameters:
        file_extension (SupportedFileExtensions): The supported file extension for the backend.
        root_directory (Optional[Union[str, Path]], optional): The root directory for the backend. Defaults to Path().

    Raises:
        FileNotFoundError: If the root directory does not exist.

    Attributes:
        root_directory (Path): The root directory for the backend.
    """

    def __init__(
        self,
        file_extension: SupportedFileExtensions,
        root_directory: Optional[Union[str, Path]] = Path(),
    ) -> None:
        """
        Initializes the FileSystemBackend.

        Parameters:
            file_extension (SupportedFileExtensions): The supported file extension for the backend.
            root_directory (Optional[Union[str, Path]], optional): The root directory for the backend. Defaults to Path().
        """
        self.root_directory = Path(root_directory)
        if not self.root_directory.exists:
            raise FileNotFoundError(
                "Root Directory must exist for FileSystemBackend to initialize"
            )
        super().__init__(backend_type="FileSystem", file_extension=file_extension)

    def _get_path(self, instruction_id: str) -> Path:
        """
        Returns the path for a given instruction ID.

        Parameters:
            instruction_id (str): The ID of the instruction.

        Returns:
            Path: The path to the instruction file.
        """
        return Path(
            self.root_directory, f"{instruction_id}.{self.file_extension.value}"
        )

    def get_contents(self, instruction_id: str) -> dict:
        """
        Retrieves the contents of an instruction.

        Parameters:
            instruction_id (str): The ID of the instruction.

        Returns:
            dict: The contents of the instruction.
        """
        path = self._get_path(instruction_id=instruction_id)
        with open(path) as f:
            return self.load(f)

    def put_contents(
        self,
        instruction: Optional[Instruction] = None,
        instruction_id: Optional[str] = None,
        payload: Optional[dict] = None,
    ) -> None:
        """
        Puts the contents of an instruction into a file.

        Parameters:
            instruction (Optional[Instruction], optional): The instruction object. Defaults to None.
            instruction_id (Optional[str], optional): The ID of the instruction. Defaults to None.
            payload (Optional[dict], optional): The payload of the instruction. Defaults to None.

        Raises:
            ValueError: If either instruction or instruction_id is not provided.

        Returns:
            None
        """
        if instruction is None and instruction_id is None:
            raise ValueError("Need either instruction_id or instruction to identify.")
        instruction_id = instruction_id or instruction.instruction_id
        payload = payload or instruction
        path = self._get_path(instruction_id=instruction_id)
        if path.exists():
            os.remove(path)
        with open(path, "w") as f:
            self.dump(payload, f)

    def delete_contents(
        self,
        instruction: Optional[Instruction] = None,
        instruction_id: Optional[str] = None,
    ) -> None:
        """
        Deletes the contents of an instruction.

        Parameters:
            instruction (Optional[Instruction], optional): The instruction object. Defaults to None.
            instruction_id (Optional[str], optional): The ID of the instruction. Defaults to None.

        Raises:
            ValueError: If either instruction or instruction_id is not provided.

        Returns:
            None
        """
        if instruction is None and instruction_id is None:
            raise ValueError("Need either instruction_id or instruction to identify.")
        instruction_id = instruction_id or instruction.instruction_id
        path = self._get_path(instruction_id=instruction_id)
        if path.exists:
            os.remove(path)
