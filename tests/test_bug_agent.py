import json
from pathlib import Path

from agent.models import BugReport, FailureType, Severity, TestFailure as FailureInput
from agent.report_generator import generate_markdown, save_markdown
from main import load_failure

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def sample_report() -> BugReport:
    return BugReport(
        title="[Marketplace Search] Recovery results are not returned",
        environment="STAGE | Build 5.69.0",
        preconditions=["Current merchant results are below four."],
        steps_to_reproduce=[
            "Perform a marketplace merchant search.",
            "Inspect the search response.",
        ],
        actual_result="market_place_results is missing.",
        expected_result="market_place_results should be returned.",
        severity=Severity.MAJOR,
        failure_type=FailureType.API,
        suspected_area="Suspected: marketplace progressive recovery logic.",
        evidence=["current_merchant_results count = 1"],
    )


def test_sample_failure_json_is_valid() -> None:
    failure = load_failure(PROJECT_ROOT / "inputs" / "sample_failure.json")

    assert isinstance(failure, FailureInput)
    assert failure.test_name == "testMarketplaceSearchRecovery"
    assert isinstance(failure.response, dict)
    assert failure.response["current_merchant_results"]["count"] == 1


def test_bug_report_serializes_with_expected_values() -> None:
    report = sample_report()
    payload = json.loads(report.model_dump_json())

    assert payload["severity"] == "Major"
    assert payload["failure_type"] == "API"


def test_generate_markdown_contains_jira_sections() -> None:
    markdown = generate_markdown(sample_report())

    assert "## Steps to Reproduce" in markdown
    assert "## Actual Result" in markdown
    assert "## Expected Result" in markdown
    assert "## Evidence" in markdown


def test_save_markdown_creates_report(tmp_path: Path) -> None:
    output = tmp_path / "reports" / "bug-report.md"

    saved = save_markdown(sample_report(), output)

    assert saved == output
    assert output.exists()
    assert "Recovery results are not returned" in output.read_text(encoding="utf-8")
