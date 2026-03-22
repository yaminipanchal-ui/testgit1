import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(scope="function")
def client():
    # preserve initial activity state to ensure test isolation
    original = copy.deepcopy(activities)
    yield TestClient(app)
    activities.clear()
    activities.update(original)
