"""Search the public MediaWiki API without launching a browser."""

import pytest
import requests

from pytest_traceoptix import step


@pytest.mark.api
def test_wikipedia_api_search_finds_python_article(wikipedia_api: requests.Session):
    with step("Search Wikipedia through the API"):
        response = wikipedia_api.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": 'intitle:"Python (programming language)"',
                "srnamespace": 0,
                "srlimit": 5,
                "format": "json",
                "formatversion": 2,
            },
            timeout=30,
        )
    with step("Verify the Python article search result"):
        response.raise_for_status()
        payload = response.json()
        assert "error" not in payload, payload.get("error")
        assert payload["query"]["searchinfo"]["totalhits"] > 0
        matches = [
            hit
            for hit in payload["query"]["search"]
            if hit["title"] == "Python (programming language)"
        ]
        assert matches, "Search did not return the Python programming language article"
        assert matches[0]["pageid"] > 0
        assert matches[0]["ns"] == 0
