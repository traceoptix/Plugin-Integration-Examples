"""Search through Wikipedia's public portal and verify the article opens."""

import re

import pytest
from playwright.sync_api import Page, expect

from pytest_traceoptix import step


@pytest.mark.ui
def test_wikipedia_ui_search_opens_python_article(page: Page):
    with step("Open Wikipedia"):
        page.goto("https://www.wikipedia.org/", wait_until="domcontentloaded", timeout=60_000)
    with step("Search for the Python programming language"):
        page.locator("#searchLanguage").select_option("en")
        search = page.locator("#searchInput")
        search.fill("Python (programming language)")
        search.press("Enter")

    with step("Verify the Python article opens"):
        expect(page).to_have_url(
            re.compile(
                r"https://en\.wikipedia\.org/wiki/Python_\(programming_language\)(?:[?#].*)?$"
            ),
            timeout=30_000,
        )
        expect(page.locator("#firstHeading")).to_have_text("Python (programming language)")
        expect(page.locator("#mw-content-text")).to_contain_text("programming language")
