# tools/create_epic.py
# from dspy.teleprompt.react import Tool
from pydantic import BaseModel
from jira_client import create_issue

class CreateEpicInput(BaseModel):
    project_key: str
    summary: str
    description: str

class CreateEpicOutput(BaseModel):
    issue_key: str
    issue_url: str

# @Tool("CreateEpic")
def create_epic(input: CreateEpicInput) -> CreateEpicOutput:
    result = create_issue(input.project_key, input.summary, input.description, issue_type="Epic")
    return CreateEpicOutput(**result)