from uuid import uuid4

import pytest

from ..backend import FileSystemBackend
from ..service import Service


@pytest.fixture(scope="session")
def test_backend():
    return FileSystemBackend(
        file_extension="json", root_directory="hydropump/test/unit/test_root"
    )


@pytest.fixture(scope="session")
def test_service(test_backend):
    return Service(backend=test_backend)


@pytest.fixture(scope="session")
def test_user():
    return "mvecchione145"


@pytest.fixture(scope="session")
def test_instruction_id():
    return str(uuid4())


@pytest.fixture(scope="session")
def test_template_id():
    return "example_template"


@pytest.fixture(scope="session")
def test_source():
    return {"system": "darwin", "zone": "us-east1-a"}


@pytest.fixture(scope="session")
def test_metadata(test_template_id, test_user):
    return {"createdBy": test_user, "templates": [test_template_id]}


@pytest.fixture(scope="session")
def test_template(test_user):
    return {
        "connectionArgs": {
            "host": "0.0.0.0",
            "port": "5432",
            "db": "postgres",
            "user": test_user,
            "password": "PROTECTED",
        }
    }


@pytest.fixture(scope="session")
def expected_compiled_result(test_metadata, test_source, test_template):
    return {
        "instruction": {**test_source, **test_template},
        "metadata": test_metadata,
    }
