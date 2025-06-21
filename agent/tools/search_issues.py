# tools/search_issues.py

from pydantic import BaseModel
from jira_client import search_issues


class SearchIssuesInput(BaseModel):
    jql_query: str
    max_results: int = 5

class SearchIssuesOutput(BaseModel):
    results_summary: str

def search_issues_tool(input: SearchIssuesInput) -> SearchIssuesOutput:
    results = search_issues(input.jql_query, input.max_results)
    summary = "\n".join(results) if results else "No matching issues found."
    return SearchIssuesOutput(results_summary=summary)