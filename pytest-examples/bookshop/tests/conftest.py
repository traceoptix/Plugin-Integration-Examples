"""Shared fixtures — no pytest_traceoptix imports needed here."""

import os

import pytest
import requests

BASE_URL = "https://bookshop.example.com"
API_BASE = "https://api.bookshop.example.com"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "en-GB", "viewport": {"width": 1280, "height": 900}}


@pytest.fixture(scope="session")
def api_token():
    return os.environ.get("BOOKSHOP_API_TOKEN", "test-token")


@pytest.fixture
def api(api_token):
    with requests.Session() as session:
        session.headers["Authorization"] = f"Bearer {api_token}"
        session.headers["Accept"] = "application/json"
        yield session
