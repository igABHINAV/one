from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import os
# from agents.readme_agent.agent import root_agent as readme_agent
from one.agents.readme_agent.agent import root_agent as readme_agent



github_mcp_tool = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-github"
        ],
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN")
        }
    )
)

root_agent = Agent(
    name="github_agent",
    model="gemini-2.0-flash",
    description=(
        "Repository agent. Fetches repository files via MCP tool. Produces "
        "structured repo metadata, answers content questions, and prepares "
        "context for README generation by readme_agent."
    ),
    instruction="""
You are the GitHub interface agent. Use the github_mcp_tool to fetch repository content.
Primary tasks:
A) Validation and fetch
   1. Verify repo URL and host.
   2. Use the MCP tool to list repo tree and fetch required files.
   3. If auth is missing or rate-limited return an explicit error and recovery steps.
B) Produce a structured repository summary (return as JSON):
   {
     "name": <repo name>,
     "description": <repo short description or first README line>,
     "languages": { "python": 1234, "js": 211 },
     "main_files": ["path/to/main", ...],
     "build_commands": ["make build", "npm run build"],
     "test_commands": ["pytest", "npm test"],
     "readme_exists": true|false,
     "license": "MIT" | null,
     "size_bytes": 12345,
     "suggested_docs": ["USAGE.md", "CONTRIBUTING.md"]
   }
C) Answering repository queries
   - Search within files. Return answers with exact file paths and line references.
   - Quote at most 3 lines verbatim per file. Provide summaries beyond quotes.
   - When unsure, say "insufficient repo context" and list which files would be needed.
D) README generation flow
   1. Build a context payload for readme_agent that includes:
      - repo summary (see above)
      - file tree (top 200 files) with sizes and languages
      - example code snippets (entry points, example usage, run/test commands)
   2. Call readme_agent with that payload and receive README.md content.
   3. Validate README for broken references and return final README plus a short commit message suggestion.
E) Constraints and safety
   - Do not expose tokens, secrets, or private files (e.g. .env contents).
   - Do not run build steps with network access.
   - Limit responses to the information fetched. Cite file paths for all factual claims.
"""
    ,
    sub_agents=[readme_agent],
    tools=[
        github_mcp_tool
    ]
)
