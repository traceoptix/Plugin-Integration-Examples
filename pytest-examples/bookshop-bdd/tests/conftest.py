"""Shared fixtures and BDD step definitions for the bookshop-bdd example.

No step() or requests_session() imports — TraceOptix collects all BDD steps
automatically from pytest-bdd hooks.
"""

import pytest
import requests
from playwright.sync_api import Page

BASE_URL = "https://bookshop.example.com"
API_BASE = "https://api.bookshop.example.com"


# ── Shared fixtures ───────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def api_session():
    with requests.Session() as session:
        session.headers["Accept"] = "application/json"
        yield session


@pytest.fixture
def cart_state():
    """Per-test cart state accumulated by step definitions."""
    return {"response": None, "book_id": None}


# ── Background ────────────────────────────────────────────────────────────────


@pytest.fixture
def catalogue_available():
    """Background step: confirm the catalogue endpoint is reachable."""
    # In a real suite this would do a lightweight health check.
    return True


# ── Step definitions: search.feature ─────────────────────────────────────────


from pytest_bdd import given, then, when, scenario, scenarios  # noqa: E402

scenarios("features/search.feature", "features/checkout.feature")


@given("the bookshop catalogue is available", target_fixture="catalogue")
def step_catalogue_available():
    return {"url": BASE_URL, "api": API_BASE}


@given("I am on the bookshop homepage")
def step_homepage(page: Page, catalogue):
    page.goto(catalogue["url"], wait_until="domcontentloaded", timeout=30_000)


@when('I search for "<query>"', target_fixture="search_results")
def step_search(page: Page, query: str):
    page.locator('[data-testid="search-input"]').fill(query)
    page.locator('[data-testid="search-submit"]').click()
    page.wait_for_selector('[data-testid="results-container"]', timeout=10_000)
    return page


@then("I see the book listed in the results")
def step_results_visible(page: Page):
    results = page.locator('[data-testid="book-card"]')
    assert results.count() > 0, "Expected at least one result"


@then("the result shows the correct author")
def step_author_visible(page: Page):
    author = page.locator('[data-testid="book-card"] [data-testid="author"]').first
    assert author.inner_text().strip(), "Expected a non-empty author"


@then("I see the empty-results message")
def step_empty_results(page: Page):
    msg = page.locator('[data-testid="no-results-message"]')
    msg.wait_for(timeout=5_000)
    assert msg.is_visible()


@when('I call the search API with query "<query>"', target_fixture="api_response")
def step_api_search(api_session: requests.Session, catalogue, query: str):
    return api_session.get(f"{catalogue['api']}/search", params={"q": query}, timeout=10)


@then("the API response contains at least one result")
def step_api_has_results(api_response: requests.Response):
    api_response.raise_for_status()
    body = api_response.json()
    assert len(body.get("results", [])) > 0


@then('the first result title contains "<expected>"')
def step_first_result_title(api_response: requests.Response, expected: str):
    body = api_response.json()
    title = body["results"][0]["title"]
    assert expected in title, f"Expected '{expected}' in '{title}'"


@then("the API response contains an empty results list")
def step_api_empty_results(api_response: requests.Response):
    api_response.raise_for_status()
    body = api_response.json()
    assert body.get("results", []) == []


# ── Step definitions: checkout.feature ───────────────────────────────────────


@when("I add the first result to the cart")
def step_add_to_cart(page: Page):
    page.locator('[data-testid="add-to-cart"]').first.click()


@then("the cart badge shows 1 item")
def step_cart_badge(page: Page):
    badge = page.locator('[data-testid="cart-count"]')
    badge.wait_for(timeout=5_000)
    assert badge.inner_text().strip() == "1"


@given("a valid book id exists in the catalogue", target_fixture="book_id")
def step_book_id(api_session: requests.Session, catalogue):
    resp = api_session.get(f"{catalogue['api']}/books", params={"limit": 1}, timeout=10)
    resp.raise_for_status()
    return resp.json()["books"][0]["id"]


@when("I add the book to the cart via the API", target_fixture="cart_response")
def step_api_add_cart(api_session: requests.Session, catalogue, book_id: str):
    return api_session.post(
        f"{catalogue['api']}/cart",
        json={"bookId": book_id, "quantity": 1},
        timeout=10,
    )


@then("the cart API returns a 200 response")
def step_cart_200(cart_response: requests.Response):
    assert cart_response.status_code == 200, cart_response.text


@then("the response body contains the book id")
def step_cart_has_book(cart_response: requests.Response, book_id: str):
    body = cart_response.json()
    ids = [item["bookId"] for item in body.get("items", [])]
    assert book_id in ids
