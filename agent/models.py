from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Severity(StrEnum):
    CRITICAL = "Critical"
    MAJOR = "Major"
    MEDIUM = "Medium"
    MINOR = "Minor"


class FailureType(StrEnum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    API = "API"
    TEST_AUTOMATION = "test automation"
    ENVIRONMENT = "environment"
    DATA = "data"
    UNKNOWN = "unknown"


class BugReport(BaseModel):
    title: str = Field(min_length=5)
    environment: str = Field(min_length=1)
    preconditions: list[str]
    steps_to_reproduce: list[str] = Field(min_length=1)
    actual_result: str = Field(min_length=1)
    expected_result: str = Field(min_length=1)
    severity: Severity
    failure_type: FailureType
    suspected_area: str
    evidence: list[str]


class TestFailure(BaseModel):
    test_name: str = Field(min_length=1)
    feature: str = Field(min_length=1)
    environment: str = Field(min_length=1)
    expected_result: str = Field(min_length=1)
    actual_result: str = Field(min_length=1)
    endpoint: str | None = None
    request: dict[str, Any] | list[Any] | str | None = None
    response: dict[str, Any] | list[Any] | str | None = None
    error_message: str | None = None
    stack_trace: str | None = None
    build_version: str | None = None
