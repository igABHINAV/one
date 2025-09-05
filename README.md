# One

This repository contains an AI agent that takes a GitHub repository URL and delivers two core functions:

1. **Auto-generate `README.md`** for the target repo.
2. **Answer questions about the repo** via natural language queries.

It connects to GitHub using **GitHub’s MCP server**, orchestrates **multiple LLMs** and **Google’s coding agents** to analyze codebases and draft accurate documentation.

Also when with the command *adk web* , it creates a **FastAPI** server for agent testing in orchestrated fashion.

---

## Features

- Repo ingestion from a GitHub URL
- Multi-LLM tool-use and reasoning
- README synthesis with sections (overview, setup, usage, API, architecture)
- Q&A over code, files, and commit history
- Cited answers with file and line references where available
- Caching to reduce repeated analysis

---

## Tech Stack

- **Language:** Python  
- **Agents:** Google coding agents  
- **Protocol:** MCP (GitHub server)  
- **LLMs:** Orchestrates 3+ models for drafting, verification, and refactoring  
- **Storage:** Local cache (pluggable)
