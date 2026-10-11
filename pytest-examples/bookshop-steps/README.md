# bookshop-steps

pytest + TraceOptix with **explicit `step()` timeline entries**.

Use `step()` when you want named, timed steps in the TraceOptix execution panel.
`requests_session()` captures the HTTP calls made inside those steps automatically.

## What this example shows

- UI tests: Playwright page interactions wrapped in `step()` blocks
- API tests: `requests_session()` fixture records HTTP calls as timeline entries
- `step.annotate()` adds structured key/value details to any step
- No BDD or fixture injection needed — `step()` is a plain context manager

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Configure TraceOptix in `pytest.ini`:

```ini
[pytest]
traceoptix_url     = https://your-traceoptix.example.com
traceoptix_project = bookshop
```

## Run

```bash
# All tests with step timeline
TRACEOPTIX_TOKEN=td_... pytest --traceoptix

# UI only
TRACEOPTIX_TOKEN=td_... pytest --traceoptix -m ui

# API only
TRACEOPTIX_TOKEN=td_... pytest --traceoptix -m api
```

## How steps appear in TraceOptix

Each `with step("…")` becomes a named row in the execution panel with its own
duration and status. `step.annotate("key", "value")` adds structured detail
visible in the step's detail view. HTTP calls made inside a `requests_session()`
fixture appear as `http`-category children with a sanitized curl annotation.

Nesting works naturally — a `with step(…)` inside another creates a child:

```python
with step("Search for a book"):           # parent
    with step("Fill search field"):       # child
        page.fill('[…]', query)
    with step("Submit form"):             # child
        page.click('[…]')
```
