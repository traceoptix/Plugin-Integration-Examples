# bookshop-bdd

pytest-bdd + TraceOptix — BDD scenarios with **zero `step()` calls**.

Every Given/When/Then step is captured automatically from `pytest_bdd_before_step` /
`pytest_bdd_after_step` hooks. No instrumentation needed in test code.

## What this example shows

- `Feature` files drive Gherkin scenarios for a fictional bookshop
- UI tests use Playwright (browser-based search, add-to-cart)
- API tests use `requests` directly
- TraceOptix publishes each scenario with its Given/When/Then step timeline
  without any `step()` or `requests_session()` imports

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Configure TraceOptix in `pytest.ini` or via environment:

```ini
# pytest.ini
[pytest]
traceoptix_url     = https://your-traceoptix.example.com
traceoptix_project = bookshop
```

## Run

```bash
# All scenarios — BDD steps appear in the TraceOptix step timeline automatically
TRACEOPTIX_TOKEN=td_... pytest --traceoptix

# UI only
TRACEOPTIX_TOKEN=td_... pytest --traceoptix -m ui

# API only (no browser needed)
TRACEOPTIX_TOKEN=td_... pytest --traceoptix -m api
```

## BDD steps in the timeline

TraceOptix collects each step's outcome, duration and keyword automatically.
If a step raises, the step is marked `failed` and later steps in the scenario
are not shown (pytest-bdd stops at the first failure).

You can still add `step()` inside a step definition for finer granularity —
it appears as a nested child of the BDD step:

```python
from pytest_traceoptix import step

@when("I search for the book")
def step_search(page, query):
    with step("Fill search field"):
        page.locator('[data-testid="search-input"]').fill(query)
    with step("Submit and wait for results"):
        page.locator('[data-testid="search-submit"]').click()
        page.wait_for_selector('[data-testid="results-container"]')
```
