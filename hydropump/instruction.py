from typing import Optional
from uuid import uuid4


class Instruction(dict):
    """
    A class representing an instruction.

    Parameters:
    - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
      If not provided, a unique ID will be generated using the uuid4() function.
    - payload (Optional[dict]): An optional parameter specifying the payload of the instruction.

    Attributes:
    - instruction_id (str): The ID of the instruction.
    """

    def __init__(
        self, instruction_id: Optional[str] = None, payload: Optional[dict] = None
    ) -> None:
        """
        Initializes a new instance of the Instruction class.

        Parameters:
        - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
          If not provided, a unique ID will be generated using the uuid4() function.
        - payload (Optional[dict]): An optional parameter specifying the payload of the instruction.

        Returns:
        - None
        """
        self.instruction_id = instruction_id or str(uuid4())
        super().__init__(payload)
