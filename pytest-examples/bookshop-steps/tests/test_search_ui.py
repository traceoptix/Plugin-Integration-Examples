"""Browser-based search tests with explicit step() timeline entries."""

import re

import pytest
from playwright.sync_api import Page, expect

from pytest_traceoptix import step

BASE_URL = "https://bookshop.example.com"


@pytest.mark.ui
def test_search_returns_matching_title(page: Page):
    with step("Open bookshop homepage"):
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)

    with step("Search for a known title"):
        page.locator('[data-testid="search-input"]').fill("The Pragmatic Programmer")
        page.locator('[data-testid="search-submit"]').click()
        page.wait_for_selector('[data-testid="results-container"]', timeout=10_000)

    with step("Verify the book appears in results") as s:
        cards = page.locator('[data-testid="book-card"]')
        count = cards.count()
        s.annotate("result_count", str(count))
        assert count > 0, f"Expected results, got {count}"

    with step("Verify the author is shown"):
        author = page.locator('[data-testid="book-card"] [data-testid="author"]').first
        expect(author).not_to_be_empty()


@pytest.mark.ui
def test_search_with_no_match_shows_empty_state(page: Page):
    with step("Open bookshop homepage"):
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)

    with step("Search for a query with no results"):
        page.locator('[data-testid="search-input"]').fill("zzznomatchzzz")
        page.locator('[data-testid="search-submit"]').click()

    with step("Verify empty-results message appears"):
        msg = page.locator('[data-testid="no-results-message"]')
        msg.wait_for(timeout=5_000)
        expect(msg).to_be_visible()


@pytest.mark.ui
def test_add_to_cart_updates_badge(page: Page):
    with step("Open bookshop homepage"):
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30_000)

    with step("Search for a book"):
        page.locator('[data-testid="search-input"]').fill("Clean Code")
        page.locator('[data-testid="search-submit"]').click()
        page.wait_for_selector('[data-testid="book-card"]', timeout=10_000)

    with step("Add the first result to the cart"):
        page.locator('[data-testid="add-to-cart"]').first.click()

    with step("Verify cart badge increments to 1"):
        badge = page.locator('[data-testid="cart-count"]')
        badge.wait_for(timeout=5_000)
        expect(badge).to_have_text("1")
