---
name: developer_assist
description: Describe what this custom agent does and when to use it.
argument-hint: The inputs this agent expects, e.g., "a task to implement" or "a question to answer".
# tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo'] # specify the tools this agent can use. If not set, all enabled tools are allowed.
---

<!-- Tip: Use /create-agent in chat to generate content with agent assistance -->

## UV Environment

Run development verification in the UV environment. This UV environment is defined in pyproject.toml, and add modules when needed.
Run pytest with uv run pytest. For coverage checks, run uv run pytest --cov=src --cov-report=term-missing --cov-report=xml.
Run Ruff with uv run ruff check src. When needed, use uv run ruff check --fix src for automatic fixes.
Run mypy with uv run mypy src. When needed, use uv run mypy --install-types --non-interactive src to automatically install missing type stubs.

