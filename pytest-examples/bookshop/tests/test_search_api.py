"""API tests — no step() or TraceOptix imports needed.

Outcomes, durations, markers, captured output, and failure text are all
collected automatically by the plugin.
"""

import pytest
import requests

API_BASE = "https://api.bookshop.example.com"


@pytest.mark.api
def test_search_api_returns_results(api: requests.Session):
    response = api.get(f"{API_BASE}/search", params={"q": "Domain-Driven Design"}, timeout=10)
    response.raise_for_status()
    body = response.json()
    assert len(body.get("results", [])) > 0
    assert "Domain-Driven Design" in body["results"][0]["title"]


@pytest.mark.api
def test_search_api_empty_query_returns_empty_list(api: requests.Session):
    response = api.get(f"{API_BASE}/search", params={"q": "zzznomatchzzz"}, timeout=10)
    response.raise_for_status()
    assert response.json().get("results", []) == []


@pytest.mark.api
def test_add_book_to_cart(api: requests.Session):
    books_resp = api.get(f"{API_BASE}/books", params={"limit": 1}, timeout=10)
    books_resp.raise_for_status()
    book_id = books_resp.json()["books"][0]["id"]

    cart_resp = api.post(
        f"{API_BASE}/cart",
        json={"bookId": book_id, "quantity": 1},
        timeout=10,
    )
    cart_resp.raise_for_status()
    items = cart_resp.json().get("items", [])
    assert any(item["bookId"] == book_id for item in items)


@pytest.mark.api
def test_get_book_detail(api: requests.Session):
    books_resp = api.get(f"{API_BASE}/books", params={"limit": 1}, timeout=10)
    books_resp.raise_for_status()
    book_id = books_resp.json()["books"][0]["id"]

    detail = api.get(f"{API_BASE}/books/{book_id}", timeout=10)
    detail.raise_for_status()
    body = detail.json()
    assert body["id"] == book_id
    assert body.get("title")
    assert body.get("author")
