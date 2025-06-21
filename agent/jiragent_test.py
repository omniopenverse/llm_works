# jira_agent_test.py

import dspy
import traceback
import mlflow
from jira_agents import JirAgent

from tools.create_story import create_story
from tools.create_task import create_task
from tools.create_bug import create_bug
from tools.create_epic import create_epic
from tools.transition_issue import transition_issue_tool 
from tools.search_issues import search_issues_tool

from typing import Optional, Literal, Union

from utils import ModelSelector


# Tell MLflow about the server URI.
mlflow.set_tracking_uri("http://127.0.0.1:5000")
# Create a unique name for your experiment.
mlflow.set_experiment("DSPy  Jira Agent Test")


# Load the DSPy ReAct agent

model_selector = ModelSelector(model_name="gpt-4o", service_provider="openai")
model_selector.model_selection()
agent = dspy.ReAct(JirAgent , tools=[ create_story, create_task, create_bug, create_epic , search_issues_tool, transition_issue_tool],)



# Define test prompts
test_cases = [
    # --- Creation ---
    "Create a story in project LLM titled 'Enable OAuth login' with description 'Add Google login support via OAuth2.'",
    "Create a task in project LLM titled 'Set up deployment pipeline' with description 'Configure GitHub Actions for CI/CD.'",
    "Create a bug in project LLM titled 'Dropdown not working' with description 'Dropdown menu fails to open on Safari.'",
    "Create an epic in project LLM titled 'User Authentication Overhaul' with description 'Unify all login and security flows.'",

    # --- Transitions ---
    "Move issue LLM-10 to Selected for Development",
    "Move issue LLM-10 to In Progress",
    "Move issue LLM-10 to Peer Review",
    "Move issue LLM-10 to Done",

    # --- Queries ---
    "Find all open bugs in project LLM",
    "Show tasks assigned to rockIO",
    "List all epics in progress in LLM",
    "What stories are selected for development in LLM?"
]

# Run tests
def run_tests():
    print("\n================== JIRA AGENT TESTS ==================\n")
    for idx, query in enumerate(test_cases, 1):
        print(f"🧪 Test {idx}: {query}")
        try:
            result = agent(query = query)
            print("✅ Thoughts:", result.trajectory)
            print("✅ Response:", result.response)
        except Exception as e:
            print("❌ Error:")
            traceback.print_exc()
        print("-" * 60)

if __name__ == "__main__":
    run_tests()