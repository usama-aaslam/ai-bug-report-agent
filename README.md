# AI Bug Report Agent

A Python-based QA project that captures automated test failures and uses the OpenAI Agents SDK to generate structured, Jira-ready bug reports.

## Current Flow

```text
API Test
   ↓
pytest failure
   ↓
conftest.py
   ↓
generated_failure.json
   ↓
Bug Report Agent
   ↓
reports/bug-report.md
```

## Features

* API testing with `pytest`
* automatic failure capture
* Pydantic validation
* OpenAI-powered bug report generation
* structured severity and failure classification
* Markdown bug report output
* ReqRes API integration
* `.env` based API key management

## Project Structure

```text
ai-bug-report-agent/
├── agent/
│   ├── bug_agent.py
│   ├── models.py
│   ├── prompts.py
│   └── report_generator.py
├── services/
│   └── reqres_client.py
├── inputs/
│   ├── sample_failure.json
│   └── generated_failure.json
├── reports/
├── tests/
│   ├── test_bug_agent.py
│   └── test_reqres_api.py
├── conftest.py
├── main.py
├── requirements.txt
└── .env.example
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```text
OPENAI_API_KEY=your_openai_api_key
REQRES_API_KEY=your_reqres_api_key
```

Do not commit `.env`.

## Run API Test

```bash
python -m pytest tests/test_reqres_api.py -v
```

If the test fails, the failure is saved to:

```text
inputs/generated_failure.json
```

## Generate Bug Report

```bash
python main.py --input inputs/generated_failure.json
```

The generated report is saved to:

```text
reports/bug-report.md
```

## Validate Input Without Calling OpenAI

```bash
python main.py --validate-only
```

## Run Unit Tests

```bash
python -m pytest -q
```

## Current Limitation

The workflow currently requires two commands:

```bash
python -m pytest tests/test_reqres_api.py -v
python main.py --input inputs/generated_failure.json
```

The next improvement is to automatically trigger the Bug Report Agent whenever pytest detects a failed test.

## Planned Improvements

* automatic agent execution after test failure
* API request/response evidence capture
* product bug vs test issue classification
* confidence scoring
* screenshot analysis
* duplicate bug detection
* Jira integration
* AI evaluation metrics

## Goal

Build an AI-assisted QA workflow that converts automation failures into structured, evidence-based bug reports with minimal manual effort.
