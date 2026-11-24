import pytest

from app import create_app
from app.store import reset_store


@pytest.fixture(autouse=True)
def clean_store():
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret"})
    return app.test_client()
