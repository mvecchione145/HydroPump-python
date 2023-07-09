import json
from typing import Optional
from uuid import uuid4

import yaml


class Instruction:
    def __init__(self, identifier: Optional[str] = None) -> None:
        self.identifier = identifier or str(uuid4())
