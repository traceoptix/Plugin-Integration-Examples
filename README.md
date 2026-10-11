# TraceOptix Plugin Integration Examples

This repository contains runnable examples that show how to integrate TraceOptix with common test tooling and automation workflows. It is meant to be a practical reference for teams that want to publish test execution evidence, browser traces, API payloads, and step-level details from Playwright, pytest, or AI agent workflows into TraceOptix.

The examples are intentionally small, self-contained, and focused on real usage patterns instead of demo-only code. They cover both the easiest “zero-instrumentation” setup and more advanced step-level reporting when you want richer execution timelines.

## What this repo includes

- Playwright examples
  - Plain browser/API checks using the TraceOptix Playwright reporter
  - BDD-style example using Gherkin + Playwright steps
- pytest examples
  - Automatic reporting with no custom test instrumentation
  - Step-based reporting for granular execution timelines
  - Real API + UI validation against public sample services
- AI agent integration
  - TraceOptix MCP plugin for agent workflows

## Repository structure

```text
.
├── playwright-examples/
│   ├── README.md
│   ├── plain/
│   └── bdd/
├── pytest-examples/
│   ├── bookshop/
│   ├── bookshop-steps/
│   └── wikipedia/
└── README.md
```

## TraceOptix packages

### Playwright reporter

Package: `@traceoptix/playwright`

Install:

```bash
npm install @traceoptix/playwright
```

This integration helps publish Playwright results, browser artifacts, HTTP evidence, screenshots, and trace data to TraceOptix. It works well for both plain Playwright tests and BDD-based test flows.

### MCP plugin for AI agents

Package: `@traceoptix/mcp`

Install:

```bash
npm install @traceoptix/mcp
```

This integration is designed for AI-agent tooling and workflow tracing, allowing the agent or orchestrated automation to emit execution evidence and context into TraceOptix in a structured way.

### pytest plugin

Package: `pytest-traceoptix`

Install:

```bash
pip install pytest-traceoptix
```

This plugin integrates with pytest to capture run metadata, markers, captured output, browser results, and optional step-level execution detail without requiring heavy changes to the tests themselves.

## Example categories

### 1) Playwright examples

The Playwright examples under `playwright-examples/` demonstrate how to integrate the TraceOptix reporter into typical browser and API testing flows.

Included patterns:

- Plain Playwright tests
- BDD-style tests using Gherkin features and step definitions
- API-level evidence capture from request/response activity
- UI evidence capture including screenshots, videos, and browser traces
- Local HTML reports and exported result bundles

Typical setup:

```bash
cd playwright-examples/plain
npm install
npx playwright install chromium
npm test
```

The default examples are built to intentionally include a couple of failing checks so the report clearly shows how TraceOptix surfaces failed assertions, API evidence, and browser artifacts.

### 2) pytest examples

The pytest examples under `pytest-examples/` show both automatic and explicit step-based reporting.

#### bookshop

This is the simplest pytest integration example. It shows zero-instrumentation usage: no custom test hooks or `step()` calls are required. TraceOptix automatically captures result metadata, markers, and captured output from standard pytest runs.

Use it when you want the quickest path to publishing test results without changing test code.

#### bookshop-steps

This example extends the same pattern with explicit `step()` timeline entries. It demonstrates named execution blocks and how HTTP calls made within those blocks become child timeline entries in TraceOptix.

Use it when you want richer execution detail for debugging slow flows or complex test scenarios.

#### wikipedia

This example runs live API + UI checks against a public service and shows how TraceOptix can bind request evidence to results in a real-world test flow. It uses pytest with browser automation and demonstrates both standard and step-enabled reporting patterns.

### 3) MCP workflow integration

The repository also includes the TraceOptix MCP plugin, which is intended for AI agent-driven workflows. It enables observability and trace capture for agent actions and tool usage when integrated into agent orchestration or multi-step automation flows.

## Typical TraceOptix configuration

Across the examples, the expected configuration is generally based on a few environment variables such as:

```bash
export TRACEOPTIX_URL="https://your-traceoptix-server.com"
export TRACEOPTIX_TOKEN="td_your_token"
export TRACEOPTIX_PROJECT="your-project-key"
```

Optional values may include:

```bash
export TRACEOPTIX_ORG="your-organization-slug"
export TRACEOPTIX_RUN_NAME="example-run"
export TRACEOPTIX_ENVIRONMENT="local"
```

The exact variables depend on the plugin and the example being used, but the pattern is the same: point the reporter at your TraceOptix server and provide a valid token and project target.

## How to use this repository

- Start with the example closest to your stack: Playwright or pytest
- Read the example-specific README in the corresponding directory
- Install the package and dependencies
- Configure TraceOptix environment variables or project settings
- Run the sample to generate local results and/or publish them to TraceOptix

## Notes

- The examples are meant for learning and validation, not production test scaffolding.
- They often use public services such as Wikipedia to make the behavior easy to reproduce.
- Some examples intentionally include failing assertions to demonstrate how TraceOptix records failed runs and collects evidence.
- When you want the richest debugging context, prefer step-based examples for nested actions, HTTP evidence, and structured execution details.

## Further reading

- Playwright package: https://www.npmjs.com/package/@traceoptix/playwright
- pytest plugin: https://pypi.org/project/pytest-traceoptix/#description
- MCP package: https://www.npmjs.com/package/@traceoptix/mcp

This repository is a practical companion for understanding how TraceOptix integrates into real-world automation and test pipelines across multiple ecosystems.
