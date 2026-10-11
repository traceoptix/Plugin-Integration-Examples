"""API search and cart tests with explicit step() and requests_session() capture."""

import pytest
import requests

from pytest_traceoptix import step

API_BASE = "https://api.bookshop.example.com"


@pytest.mark.api
def test_search_api_returns_results(api: requests.Session):
    with step("Search catalogue for a known title") as s:
        response = api.get(f"{API_BASE}/search", params={"q": "Domain-Driven Design"}, timeout=10)
        s.annotate("status_code", str(response.status_code))

    with step("Assert response is successful"):
        response.raise_for_status()

    with step("Assert at least one result returned") as s:
        body = response.json()
        results = body.get("results", [])
        s.annotate("result_count", str(len(results)))
        assert len(results) > 0

    with step("Assert first result title matches") as s:
        title = results[0]["title"]
        s.annotate("first_title", title)
        assert "Domain-Driven Design" in title


@pytest.mark.api
def test_search_api_empty_query_returns_empty_list(api: requests.Session):
    with step("Search for a query with no matches"):
        response = api.get(f"{API_BASE}/search", params={"q": "zzznomatchzzz"}, timeout=10)

    with step("Assert HTTP 200 and empty results"):
        response.raise_for_status()
        body = response.json()
        assert body.get("results", []) == []


@pytest.mark.api
def test_add_book_to_cart(api: requests.Session):
    with step("Fetch a book id from the catalogue") as s:
        resp = api.get(f"{API_BASE}/books", params={"limit": 1}, timeout=10)
        resp.raise_for_status()
        book_id = resp.json()["books"][0]["id"]
        s.annotate("book_id", book_id)

    with step("POST book to cart") as s:
        cart_resp = api.post(
            f"{API_BASE}/cart",
            json={"bookId": book_id, "quantity": 1},
            timeout=10,
        )
        s.annotate("status_code", str(cart_resp.status_code))

    with step("Assert cart contains the book"):
        cart_resp.raise_for_status()
        items = cart_resp.json().get("items", [])
        assert any(item["bookId"] == book_id for item in items)
