# tools/create_task.py
# from dspy.teleprompt.react import Tool
from pydantic import BaseModel
from jira_client import create_issue

class CreateTaskInput(BaseModel):
    project_key: str
    summary: str
    description: str

class CreateTaskOutput(BaseModel):
    issue_key: str
    issue_url: str

# @Tool("CreateTask")
def create_task(input: CreateTaskInput) -> CreateTaskOutput:
    result = create_issue(input.project_key, input.summary, input.description, issue_type="Task")
    return CreateTaskOutput(**result)