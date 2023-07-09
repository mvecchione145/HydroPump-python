from typing import Optional
from uuid import uuid4

from .compiler import Compiler


class Instruction(dict):
    """
    A class representing an instruction.

    Parameters:
    - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
      If not provided, a unique ID will be generated using the uuid4() function.
    - metadata (Optional[dict]): An optional parameter specifying the metadata of the instruction.
    - payload (Optional[dict]): An optional parameter specifying the payload of the instruction.

    Attributes:
    - instruction_id (str): The ID of the instruction.
    """

    def __init__(
        self,
        instruction_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        payload: Optional[dict] = None,
    ) -> None:
        """
        Initializes a new instance of the RawInstruction class.

        Parameters:
        - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
          If not provided, a unique ID will be generated using the uuid4() function.
        - metadata (Optional[dict]): An optional parameter specifying the metadata of the instruction.
        - payload (Optional[dict]): An optional parameter specifying the payload of the instruction.

        Returns:
        - None
        """
        self.instruction_id = instruction_id or str(uuid4())
        self.metadata = metadata
        if self.metadata is None:
            self.metadata = {}
        if payload is None:
            payload = {}
        super().__init__(payload)

    def compile(self, compiler: Optional[Compiler] = None) -> None:
        if compiler is None:
            compiler = Compiler
        super().__init__(compiler.compile(self))
