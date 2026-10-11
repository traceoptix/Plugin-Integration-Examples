"""Browser-based search tests — no step() or TraceOptix imports needed.

TraceOptix records the outcome, duration, markers, and captured output of each
test automatically from standard pytest hooks.
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://bookshop.example.com"


@pytest.mark.ui
def test_search_returns_results(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.locator('[data-testid="search-input"]').fill("The Pragmatic Programmer")
    page.locator('[data-testid="search-submit"]').click()
    page.wait_for_selector('[data-testid="results-container"]', timeout=10_000)

    cards = page.locator('[data-testid="book-card"]')
    assert cards.count() > 0


@pytest.mark.ui
def test_search_no_match_shows_empty_state(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.locator('[data-testid="search-input"]').fill("zzznomatchzzz")
    page.locator('[data-testid="search-submit"]').click()

    msg = page.locator('[data-testid="no-results-message"]')
    msg.wait_for(timeout=5_000)
    expect(msg).to_be_visible()


@pytest.mark.ui
def test_add_to_cart_increments_badge(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.locator('[data-testid="search-input"]').fill("Clean Code")
    page.locator('[data-testid="search-submit"]').click()
    page.wait_for_selector('[data-testid="book-card"]', timeout=10_000)

    page.locator('[data-testid="add-to-cart"]').first.click()

    badge = page.locator('[data-testid="cart-count"]')
    badge.wait_for(timeout=5_000)
    expect(badge).to_have_text("1")


@pytest.mark.ui
def test_book_detail_page_loads(page: Page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)
    page.locator('[data-testid="search-input"]').fill("Clean Code")
    page.locator('[data-testid="search-submit"]').click()
    page.wait_for_selector('[data-testid="book-card"]', timeout=10_000)

    page.locator('[data-testid="book-card"] a').first.click()
    page.wait_for_selector('[data-testid="book-title"]', timeout=10_000)
    expect(page.locator('[data-testid="book-title"]')).not_to_be_empty()
