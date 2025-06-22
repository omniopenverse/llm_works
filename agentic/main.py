from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import dspy
from os  import getenv
from dotenv import load_dotenv
import json


# Create server parameters for stdio connection
print("Setting up server parameters for MCP client...")
load_dotenv(dotenv_path="../.env")
SERVER_HOST = getenv("SERVER_HOST", "localhost")

# Load config from file
with open("../claude_desktop_config.json", "r") as f:
    config = json.load(f)

mcp_config = config["mcpServers"]["mcp-atlassian"]

# Build the server parameters
server_params = StdioServerParameters(
    command=mcp_config["command"],
    args=mcp_config["args"],
    env=mcp_config["env"]
)

# Define the DSPy agent for JIRA user service
class DSPyJiraUserService(dspy.Signature):
    """
    You are a JIRA user service agent. You are given a list of tools to handle user requests.
    
    You should decide the right tool to use in order to fulfill users' requests.
    """

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and the information users need, "
            "e.g., the issue_key if it's a JIRA issue request."
        )
    )

# Configure DSPy with the Ollama model
dspy.configure(
    lm=dspy.LM(
        model="ollama_chat/qwen3:14b",  # e.g., "qwen3:8b", "qwen3:1.7b", "qwen3:14b"
        api_base=f"http://{SERVER_HOST}:11434",
        api_key=""  # Dummy key, Ollama doesn't require authentication
    )
)


print("DSPy configured with Gemini model.")
async def run(user_request):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()

            # Convert MCP tools to DSPy tools
            dspy_tools = []
            for tool in tools.tools:
                dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))

            # # Gather only the tools we want to use
            # tools_to_use = ["jira_get_issue", "jira_search_issues", "jira_create_issue", "jira_search"]
            # for tool in tools.tools:
            #     if tool.name in tools_to_use:
            #         dspy_tools.append(dspy.Tool.from_mcp_tool(session, tool))

            # Create the agent
            react = dspy.ReAct(DSPyJiraUserService, tools=dspy_tools)

            result = await react.acall(user_request=user_request)
            print(result)

if __name__ == "__main__":
    import asyncio
    
    print("Starting the DSPy JIRA agent...")
    asyncio.run(run
        (
            """
            Create a story in project TEST titled 'Configure GitHub Actions for CI/CD.' with description 'Configure GitHub Actions for CI/CD.'
            """
        )
)