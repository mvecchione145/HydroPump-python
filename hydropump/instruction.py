from typing import Optional
from uuid import uuid4
from datetime import datetime


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
        source: Optional[dict] = None,
        debug: Optional[bool] = False,
    ) -> None:
        """
        Initializes a new instance of the RawInstruction class.

        Parameters:
        - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
          If not provided, a unique ID will be generated using the uuid4() function.
        - metadata (Optional[dict]): An optional parameter specifying the metadata of the instruction.
        - source (Optional[dict]): An optional parameter specifying the payload of the instruction.
        - debug (Optional[bool]): An optional parameter that will not compile on initialization.

        Returns:
        - None
        """
        self.instruction_id = instruction_id or str(uuid4())
        self.metadata = metadata
        self.source = source
        if self.metadata is None:
            self.metadata = {}
        self.metadata.update({"compiled": False})
        if self.source is None:
            self.source = {}
        super().__init__({"metadata": self.metadata, "rawSource": self.source})
        if not debug:
            self.compile()

    def update_instruction(
        self, metadata: Optional[dict] = None, source: Optional[dict] = None
    ) -> None:
        if metadata is not None:
            self.metadata = metadata
        if source is not None:
            self.source = source
        self.metadata.update({"modifiedAt": str(datetime.now())})
        super().__init__({"metadata": self.metadata, "rawSource": self.source})

    def compile(self) -> None:
        for template in self.metadata.get("templates", []):
            pass
        self.metadata.update({"compiled": True})
