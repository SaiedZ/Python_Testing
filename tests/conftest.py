import pytest

import server


@pytest.fixture
def client():
    server.app.config.update({"TESTING": True})
    with server.app.test_client() as client:
        yield client
