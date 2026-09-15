from agents import Agent

from agent.models import BugReport
from agent.prompts import BUG_REPORT_AGENT_INSTRUCTIONS


bug_report_agent = Agent(
    name="Bug Report Agent",
    instructions=BUG_REPORT_AGENT_INSTRUCTIONS,
    output_type=BugReport,
)