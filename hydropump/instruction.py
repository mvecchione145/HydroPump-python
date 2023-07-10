from datetime import datetime
from typing import Optional
from uuid import uuid4


class Template(dict):
    """
    A class representing a template.

    Parameters:
    - metadata (Optional[dict]): An optional parameter specifying the metadata of the template.
    - source (Optional[dict]): An optional parameter specifying the source of the template.
    - template_id (Optional[str]): An optional parameter specifying the ID of the template.
      If not provided, a unique ID will be generated using the uuid4() function.

    Attributes:
    - template_id (str): The ID of the template.
    """

    def __init__(
        self,
        metadata: Optional[dict] = None,
        source: Optional[dict] = None,
        template_id: Optional[str] = None,
    ) -> None:
        """
        Initializes a new instance of the Template class.

        Parameters:
        - metadata (Optional[dict]): An optional parameter specifying the metadata of the template.
        - source (Optional[dict]): An optional parameter specifying the source of the template.
        - template_id (Optional[str]): An optional parameter specifying the ID of the template.
          If not provided, a unique ID will be generated using the uuid4() function.

        Returns:
        - None
        """
        self.template_id = template_id or str(uuid4())
        self.metadata = metadata or {}
        self.source = source or {}
        self.metadata.update({"compiled": False})
        self.set_source()

    def set_source(self) -> None:
        """
        Sets the source of the template.

        Returns:
        - None
        """
        super().__init__({"metadata": self.metadata, "template": self.source})

    def update_template(
        self, metadata: Optional[dict] = None, source: Optional[dict] = None
    ) -> None:
        """
        Updates the metadata and source of the template.

        Parameters:
        - metadata (Optional[dict]): An optional parameter specifying the metadata of the template.
        - source (Optional[dict]): An optional parameter specifying the source of the template.

        Returns:
        - None
        """
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
    - source (Optional[dict]): An optional parameter specifying the source of the instruction.

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
        Initializes a new instance of the Instruction class.

        Parameters:
        - instruction_id (Optional[str]): An optional parameter specifying the ID of the instruction.
          If not provided, a unique ID will be generated using the uuid4() function.
        - metadata (Optional[dict]): An optional parameter specifying the metadata of the instruction.
        - source (Optional[dict]): An optional parameter specifying the source of the instruction.

        Returns:
        - None
        """
        self.instruction_id = instruction_id or str(uuid4())
        self.metadata = metadata or {}
        self.source = source or {}
        self.metadata.update({"compiled": False})
        self.set_source()

    def set_source(self) -> None:
        """
        Sets the source of the instruction.

        Returns:
        - None
        """
        super().__init__({"metadata": self.metadata, "instruction": self.source})

    def update_instruction(
        self, metadata: Optional[dict] = None, source: Optional[dict] = None
    ) -> None:
        """
        Updates the metadata and source of the instruction.

        Parameters:
        - metadata (Optional[dict]): An optional parameter specifying the metadata of the instruction.
        - source (Optional[dict]): An optional parameter specifying the source of the instruction.

        Returns:
        - None
        """
        if metadata is not None:
            self.metadata = metadata
        if source is not None:
            self.source = source
        self.metadata.update({"modifiedAt": str(datetime.now())})
        self.set_source()
