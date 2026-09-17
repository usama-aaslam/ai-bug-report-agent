from pathlib import Path

from agent.models import BugReport


def generate_markdown(report: BugReport) -> str:
    preconditions = "\n".join(
        f"- {precondition}"
        for precondition in report.preconditions
    )

    steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(
            report.steps_to_reproduce,
            start=1,
        )
    )

    evidence = "\n".join(
        f"- {item}"
        for item in report.evidence
    )

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


def save_markdown_report(
        report: BugReport,
        output_path: str,
) -> None:
    path = Path(output_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    markdown = generate_markdown(report)

    path.write_text(
        markdown,
        encoding="utf-8",
    )