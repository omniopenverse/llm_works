# main_agent.py
# from dspy.teleprompt.react import ReActAgent
import dspy

from typing import Optional, Literal, Union


class JirAgent(dspy.Signature):
    """You are a Jira support agent that helps users create and manage issues like tasks, stories, bugs, and epics.

    You are given a list of tools to handle user requests, and you should decide the right tool to use in order to
    fulfill the user's request.
    """

    query: str = dspy.InputField()
    response: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and provides any relevant details, "
            "e.g., the issue key and a URL if a new issue was created."
        )
    )

