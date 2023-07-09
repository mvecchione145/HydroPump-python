from datetime import datetime
from uuid import uuid4

import pytest


@pytest.fixture(scope="session")
def example_id():
    return str(uuid4())


@pytest.fixture(scope="session")
def example_source():
    return {"system": "darwin", "zone": "us-east1-a"}


@pytest.fixture(scope="session")
def example_metadata():
    return {"createdAt": str(datetime.now()), "createdBy": "mvecchione145"}
