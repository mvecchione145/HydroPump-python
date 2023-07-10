from datetime import datetime
from typing import Optional
from uuid import uuid4


class Template(dict):
    def __init__(
        self,
        metadata: Optional[dict] = None,
        source: Optional[dict] = None,
        template_id: Optional[str] = None,
    ) -> None:
        self.template_id = template_id or str(uuid4())
        self.metadata = metadata
        self.source = source
        if self.metadata is None:
            self.metadata = {}
        self.metadata.update({"compiled": False})
        if self.source is None:
            self.source = {}
        self.set_source()

    def set_source(self):
        super().__init__({"metadata": self.metadata, "template": self.source})

    def update_template(
        self, metadata: Optional[dict] = None, source: Optional[dict] = None
    ) -> None:
        if metadata is not None:
            self.metadata = metadata
        if source is not None:
            self.source = source
        self.metadata.update({"modifiedAt": str(datetime.now())})
        self.set_source()


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
        self.set_source()

    def set_source(self):
        super().__init__({"metadata": self.metadata, "instruction": self.source})

    def update_instruction(
        self, metadata: Optional[dict] = None, source: Optional[dict] = None
    ) -> None:
        if metadata is not None:
            self.metadata = metadata
        if source is not None:
            self.source = source
        self.metadata.update({"modifiedAt": str(datetime.now())})
        self.set_source()
