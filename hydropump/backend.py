from abc import ABC, abstractmethod
from typing import Union
from pathlib import Path
from enum import Enum

import json
import yaml


class SupportedFileExtensions(Enum):
    json = "json"
    # xml = "xml"
    yaml = "yaml"
    yml = "yaml"


class Backend(ABC):
    def __init__(
        self, backend_type: str, file_extension: SupportedFileExtensions
    ) -> None:
        self.backend_type = backend_type
        self.file_extension = SupportedFileExtensions(file_extension)
        self.set_dump_load()

    def set_dump_load(self):
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
        pass


class FileSystemBackend(Backend):
    def __init__(
        self,
        file_extension: SupportedFileExtensions,
        root_directory: Union[str, Path] = Path(),
    ) -> None:
        self.root_directory = Path(root_directory)
        if not self.root_directory.exists:
            raise FileNotFoundError(
                "Root Directory must exist for FileSystemBackend to initialize"
            )
        super().__init__(backend_type="FileSystem", file_extension=file_extension)

    def _get_path(self, identifier: str) -> Path:
        return Path(self.root_directory, identifier)

    def get_contents(self, identifier: str) -> dict:
        path = self._get_path(identifier=identifier)
        with open(path) as f:
            return self.load(f)
