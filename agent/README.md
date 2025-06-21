# 🤖 DSPy Jira Agent

A natural language agent powered by [DSPy](https://github.com/stanfordnlp/dspy) that lets you interact with your Jira instance via simple prompts. You can:

- Create stories, tasks, bugs, and epics
- Query issues with natural language (via JQL)
- Transition issues between workflow statuses
- Automate real Jira workflows with ReAct-style reasoning

---

## 🚀 Quickstart

### 1. Dependancies
A requirement file is  needed to be installed

### 2. ⚙️ Environment Configuration

Create a .env file in the root directory and populate it with:

#### 🔐 Jira Authentication and 🔑 OpenAI API Key
JIRA_API_TOKEN="ATAT...."

JIRA_EMAIL="your_login_email"

JIRA_BASE_URL="https://omniopenverse.atlassian.net/"

OPENAI_API_KEY='sk-proj-...'

You could also use ollama via ollama container. Use the thinking models only

### 3. How to use the agent
Run the test suite from terminal:

```python jira_agent_test.py```

This is a rough implementation. It works but need to be properly set up