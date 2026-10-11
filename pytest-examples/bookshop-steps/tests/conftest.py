"""Shared fixtures for the bookshop-steps example."""

import pytest
from pytest_traceoptix import requests_session

BASE_URL = "https://bookshop.example.com"
API_BASE = "https://api.bookshop.example.com"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "en-GB", "viewport": {"width": 1280, "height": 900}}


@pytest.fixture
def api(bookshop_token):
    """requests.Session with HTTP calls captured in the step timeline."""
    with requests_session() as client:
        client.headers["Authorization"] = f"Bearer {bookshop_token}"
        client.headers["Accept"] = "application/json"
        yield client


@pytest.fixture(scope="session")
def bookshop_token():
    """A token for the bookshop API (read from env or use a test value)."""
    import os
    return os.environ.get("BOOKSHOP_API_TOKEN", "test-token")
