from typing import Optional, Union

from .backend import Backend, FileSystemBackend
from .instruction import Instruction


class Service:
    def __init__(self, backend: Optional[Backend]) -> None:
        pass

    def get_instruction(self, instruction_id: str) -> Instruction:
        pass

    def create_instruction(self, instruction: Instruction) -> None:
        pass

    def update_instruction(self, instruction_id: str, instruction: Instruction) -> None:
        pass

    def delete_instruction(self, instruction_id: str) -> None:
        pass
