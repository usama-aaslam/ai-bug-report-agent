from pathlib import Path

from agent.models import BugReport


def generate_markdown(report: BugReport) -> str:
    preconditions = _bullet_list(report.preconditions, fallback="Not provided")
    steps = _numbered_list(report.steps_to_reproduce)
    evidence = _bullet_list(report.evidence, fallback="No additional evidence provided")

    return f"""# {report.title}

## Environment

{report.environment}

## Preconditions

{preconditions}

## Steps to Reproduce

{steps}

## Actual Result

{report.actual_result}

## Expected Result

{report.expected_result}

## Severity

{report.severity.value}

## Failure Classification

{report.failure_type.value}

## Suspected Area

{report.suspected_area}

## Evidence

{evidence}
"""


def save_markdown(report: BugReport, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generate_markdown(report), encoding="utf-8")
    return output_path


def _bullet_list(items: list[str], fallback: str) -> str:
    if not items:
        return fallback
    return "\n".join(f"- {item}" for item in items)


def _numbered_list(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))
