# Wikipedia API + UI sample

A standalone consumer project with exactly two tests:

- `tests/test_api_search.py` searches Wikipedia's MediaWiki API and checks the Python
  programming language article's title, page ID and namespace. It uses the instrumented `traceoptix_requests` session, with no browser; its prepared request is captured as sanitized cURL.
- `tests/test_ui_search.py` opens Wikipedia's portal in Chromium, selects English, submits
  the same article name and verifies the destination URL, heading and article content. Named step contexts describe each action.

Both run serially in one pytest session and publish **one TraceOptix run** through the locally
installed `pytest-traceoptix` plugin. You need Python 3.10+ and outbound access to Wikipedia.
The tests use real public services; network outages or site changes are test failures, not skips.

## Set up

From the TraceOptix repository root:

```bash
cd plugins/traceoptix-pytest/examples/wikipedia
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

On Linux CI, use `python -m playwright install --with-deps chromium` to install system
libraries too. Run pip from this directory: `-e ../..` installs the local TraceOptix plugin.
You do not need a published package or a second manual `-p` plugin registration.

## Run locally

```bash
pytest                  # Both tests, no TraceOptix requests
pytest -m api           # API only; browser installation not required
pytest -m ui --headed   # Watch the browser search
```

`pytest.ini` always writes `test-results/junit.xml`. Failed UI tests also retain local
screenshots and Playwright traces under `test-results/browser/`.
These browser artifacts are **local only**: this plugin currently uploads JUnit, not attachments.
Open a trace with `python -m playwright show-trace path/to/trace.zip`.

## Publish to TraceOptix

Create or choose a project and a token with `runs:write` access to that project. Then:

```bash
cp traceoptix.env.example traceoptix.env
# Edit traceoptix.env with your server origin, token, project key and organisation slug.
set -a
source traceoptix.env
set +a
pytest --traceoptix
```

The environment file is ignored by Git and must be sourced explicitly. Never put a token in
`pytest.ini`. The project key must already exist; the sample does not provision a project.
Omit `TRACEOPTIX_ORG` if you do not need the final browser link.

For a Full details project, the plugin publishes the finalized JUnit file and prints
`accepted for ingestion`; the worker then parses the two test results and binds their steps. The API test has two named steps plus one nested HTTP step; the UI test has three named steps. Expand the API request step to see its sanitized cURL and HTTP status. For Summary-only,
it publishes aggregate counts and run metadata, with no test names, XML, steps, cURL or diagnostics.
A successful combined run has total **2**, passed **2**. Selectors such as `-m api` intentionally
publish a run containing only the selected test. Each new pytest invocation creates a new run.

Publication is opt-in. Missing configuration or an upload failure prints a warning and leaves
pytest's test exit code unchanged; a green pytest exit alone does not prove publication succeeded.
Do not use `-n` or `--reruns`: this plugin's serial release skips publication in those modes.
The Wikipedia requests never receive the TraceOptix token.

## Verified locally

Both tests passed against live Wikipedia on Python 3.14.7, pytest 9.1.1,
pytest-playwright 0.9.0 and Playwright 1.63.0 (Chromium). A local TraceOptix HTTP
fixture verified one run creation, one JUnit upload containing both passed results,
exact declared/uploaded bytes, no API authorization header on the storage upload,
and one completion request. API-only execution and collection of exactly two tests
were also checked.

On 2026-10-03, the sample was also published to the explicitly selected `checkout-web`
project on a running local TraceOptix server. API readback confirmed ingestion status
`complete`, total **2**, passed **2**, and both expected test identities. Credentials
remain in the ignored local environment file and are not part of this example. The step-enabled
run was also verified: all **6 steps** were bound to the correct two results, with one
sanitized cURL annotation on the API request.

The [plugin step guide](../../README.md#steps-and-api-curl) explains nested contexts, request
body opt-in, redaction rules and capture limits. Requests from the example use no credentials.

## CI command sequence

After checkout, use this directory as the working directory and supply `TRACEOPTIX_URL`,
`TRACEOPTIX_TOKEN`, `TRACEOPTIX_PROJECT` and optional `TRACEOPTIX_ORG` through your CI's
secret/environment settings:

```bash
python -m pip install -r requirements.txt
python -m playwright install --with-deps chromium
pytest --traceoptix
```

GitHub Actions, GitLab CI and Jenkins metadata are detected by the reporter. Retain
`test-results/` as a CI artifact even when pytest fails. This live Wikipedia sample is kept
out of the plugin's default unit/integration suite so that those checks remain self-contained.

See the [plugin guide](../../README.md), [MediaWiki search API](https://www.mediawiki.org/wiki/API:Search)
and [Playwright pytest setup](https://playwright.dev/python/docs/intro).
