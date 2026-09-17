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

def parse_arguments():
    parser = argparse.ArgumentParser(
        description = "AI Bug Report Agent",
    )


    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Path to test failure JSON file",
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate input without calling the AI",
    )

    return parser.parse_args()

def load_failure(input_path: str) -> TestFailure:
   path = Path(input_path)
   with path.open(
       "r",
       encoding="utf-8",
   ) as file:
       data = json.load(file)
       return TestFailure.model_validate(data)


def generate_bug_report(failure: TestFailure):
    failure_json = failure.model_dump_json(
        indent=2,
    )

    result = Runner.run_sync(
        bug_report_agent,
        failure_json,
    )

    return result.final_output
def main():
    load_dotenv()

    args = parse_arguments()

    failure = load_failure(args.input)

    if args.validate_only:
        print("Input is valid.")
        print(
            failure.model_dump_json(
                indent=2,
            )
        )
        return

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. "
            "Add it to your .env file."
        )

    report = generate_bug_report(failure)

    save_markdown_report(
        report,
        args.output,
    )

    print("Bug report generated successfully.")
    print(f"Report: {args.output}")


if __name__ == "__main__":
    main()