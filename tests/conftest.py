"""Pytest fixture configuration for the web app tests."""
import os
import sys
import pytest
# Add the parent directory to the system path to import web_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from web_app.app import app  # noqa: E402


@pytest.fixture
def client():
    """Creates a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
