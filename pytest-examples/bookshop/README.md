# bookshop

pytest + TraceOptix — **zero instrumentation**.

No `step()`, no `requests_session()`, no imports from `pytest_traceoptix` anywhere in
test code. TraceOptix collects outcomes, durations, markers, and captured output
automatically from standard pytest hooks.

## What this example shows

- UI tests: Playwright browser tests written as normal pytest functions
- API tests: `requests.Session` used directly, no wrapping needed
- Markers (`@pytest.mark.ui`, `@pytest.mark.api`) appear as tags on each run
- Failure text and captured output are attached without any test-code changes

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Configure TraceOptix in `pytest.ini` or environment:

```ini
[pytest]
traceoptix_url     = https://your-traceoptix.example.com
traceoptix_project = bookshop
```

## Run

```bash
# Publish all results automatically — no code changes needed
TRACEOPTIX_TOKEN=td_... pytest --traceoptix

# UI only
TRACEOPTIX_TOKEN=td_... pytest --traceoptix -m ui

# API only
TRACEOPTIX_TOKEN=td_... pytest --traceoptix -m api
```

## When to add step() later

Start here. If you later need step-level timing in the execution panel — to
pinpoint which navigation or API call is slow — add `from pytest_traceoptix import step`
and wrap those actions. Everything already published stays unchanged; the step
timeline is additive. See the `bookshop-steps` example for that pattern.
