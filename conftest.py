import json
from pathlib import Path

import pytest


FAILURE_OUTPUT = Path(
    "inputs/generated_failure.json"
)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
        item,
        call,
):
    outcome = yield
    report = outcome.get_result()

    if (
            report.when == "call"
            and report.failed
    ):
        failure_data = {
            "test_name": item.name,
            "feature": "ReqRes API",
            "environment": "TEST",
            "expected_result": (
                "Test assertion should pass."
            ),
            "actual_result": str(
                report.longrepr
            ),
            "error_message": str(
                report.longrepr
            ),
        }

        FAILURE_OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        FAILURE_OUTPUT.write_text(
            json.dumps(
                failure_data,
                indent=2,
            ),
            encoding="utf-8",
        )

        print(
            "\nFailure captured:"
            f" {FAILURE_OUTPUT}"
        )