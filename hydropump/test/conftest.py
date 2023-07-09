from datetime import datetime
from uuid import uuid4

import pytest

from hydropump import FileSystemBackend, Instruction, Service


@pytest.fixture(scope="session")
def example_id():
    return str(uuid4())


@pytest.fixture(scope="session")
def example_instruction(example_id):
    return {"system": "darwin", "create_date": str(datetime.now())}
