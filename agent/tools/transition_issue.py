
# tools/transition_issue.py
from pydantic import BaseModel
from jira_client import transition_issue

class TransitionIssueInput(BaseModel):
    issue_key: str
    target_status: str  # e.g., "Done", "In Progress", "To Do"

class TransitionIssueOutput(BaseModel):
    message: str


def transition_issue_tool(input: TransitionIssueInput) -> TransitionIssueOutput:
    result = transition_issue(input.issue_key, input.target_status)
    return TransitionIssueOutput(**result)