# tools/create_bug.py
# from dspy.teleprompt.react import Tool
from pydantic import BaseModel
from jira_client import create_issue

class CreateBugInput(BaseModel):
    project_key: str
    summary: str
    description: str

class CreateBugOutput(BaseModel):
    issue_key: str
    issue_url: str

# @Tool("CreateBug")
def create_bug(input: CreateBugInput) -> CreateBugOutput:
    result = create_issue(input.project_key, input.summary, input.description, issue_type="Bug")
    return CreateBugOutput(**result)