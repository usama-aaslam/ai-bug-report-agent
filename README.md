# AI Bug Report Agent

A QA-focused Python project that converts automated test failure evidence into a structured, Jira-ready bug report using the OpenAI Agents SDK.

## What it does

1. Reads structured failure evidence from JSON.
2. Validates the evidence with Pydantic.
3. Sends the evidence to a QA Bug Report Agent.
4. Requires a structured `BugReport` response.
5. Saves the result as a Markdown report.

## Project structure

```text
ai-bug-report-agent/
├── agent/
│   ├── __init__.py
│   ├── bug_agent.py
│   ├── models.py
│   ├── prompts.py
│   └── report_generator.py
├── inputs/
│   └── sample_failure.json
├── reports/
│   └── .gitkeep
├── tests/
│   ├── evaluation_cases.json
│   └── test_bug_agent.py
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## Setup

Python 3.11+ is recommended.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your OpenAI API key to `.env`:

```text
OPENAI_API_KEY=your_key_here
```

Do not commit `.env`.

## Validate the input without an API call

```bash
python main.py --validate-only
```

## Generate a bug report

```bash
python main.py
```

The generated Markdown report is written to:

```text
reports/bug-report.md
```

You can provide different files:

```bash
python main.py --input inputs/sample_failure.json --output reports/my-report.md
```

## Run tests

```bash
pytest -q
```

The unit tests intentionally do not call the OpenAI API, so they can run safely in CI without spending API credits.

## Current scope

This is the first working version. Good next increments are:

- capture failure evidence automatically from pytest;
- add screenshot evidence from Playwright;
- add API request/response capture;
- add product-bug vs test-bug classification;
- add evaluation scoring from `tests/evaluation_cases.json`;
- detect duplicate Jira issues;
- add human-approved Jira ticket creation.
