from unittest import mock

import pytest
from fastapi.testclient import TestClient

from api.main import app, settings

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(settings.DYNAMODB_TABLE_NAME):
        yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
