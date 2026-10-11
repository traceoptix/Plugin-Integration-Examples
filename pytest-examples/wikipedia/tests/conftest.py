"""Shared fixtures for the Wikipedia example suite."""

import pytest
import requests


@pytest.fixture
def wikipedia_api():
    """Plain requests.Session with the Wikipedia User-Agent header set."""
    with requests.Session() as session:
        session.headers["User-Agent"] = (
            "TraceOptixPytestSample/0.1 (Wikipedia search test)"
        )
        yield session


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "locale": "en-US", "viewport": {"width": 1280, "height": 900}}
