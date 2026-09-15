import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from agent.models import BugReport, TestFailure
from agent.report_generator import save_markdown

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = PROJECT_ROOT / "inputs" / "sample_failure.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "reports" / "bug-report.md"


def load_failure(input_path: Path) -> TestFailure:
    with input_path.open("r", encoding="utf-8") as file:
        payload = json.load(file)
    return TestFailure.model_validate(payload)


def generate_bug_report(failure: TestFailure) -> BugReport:
    from agents import Runner

    from agent.bug_agent import bug_report_agent

    result = Runner.run_sync(
        bug_report_agent,
        failure.model_dump_json(indent=2),
    )

    if not isinstance(result.final_output, BugReport):
        raise TypeError("Bug Report Agent returned an unexpected output type.")

    return result.final_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a structured Jira-ready bug report from test failure evidence."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="Path to the test failure JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Path where the Markdown bug report will be written.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate the input JSON without making an OpenAI API call.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv(PROJECT_ROOT / ".env")
    args = parse_args()

    try:
        failure = load_failure(args.input)
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        print(f"Input validation failed: {error}")
        return 1

    if args.validate_only:
        print("Input is valid.")
        print(failure.model_dump_json(indent=2))
        return 0

    if not os.getenv("OPENAI_API_KEY"):
        print(
            "OPENAI_API_KEY is not configured. Copy .env.example to .env, add your key, "
            "or run with --validate-only."
        )
        return 1

    try:
        report = generate_bug_report(failure)
        saved_path = save_markdown(report, args.output)
    except Exception as error:  # CLI boundary: show a concise failure to the user.
        print(f"Bug report generation failed: {error}")
        return 1

    print(report.model_dump_json(indent=2))
    print(f"\nMarkdown report saved to: {saved_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
