# tools/create_story.py
# from dspy.teleprompt.react import Tool
from pydantic import BaseModel
from jira_client import create_issue

class CreateStoryInput(BaseModel):
    project_key: str
    summary: str
    description: str

class CreateStoryOutput(BaseModel):
    issue_key: str
    issue_url: str

# @Tool("CreateStory")
def create_story(input: CreateStoryInput) -> CreateStoryOutput:
    result = create_issue(input.project_key, input.summary, input.description, issue_type="Story")
    return CreateStoryOutput(**result)