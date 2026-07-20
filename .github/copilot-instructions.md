# Copilot Agent Instructions

- User unit test by `uv run pytest`.
- Use `uv run pytest --cov=src --cov-report=term-missing --cov-report=xml` when coverage check is needed.
- Run Ruff with `uv run ruff check src`.
- Run pylint with `uv run pylint src`.
- Run mypy with `uv run mypy src`.
- The CI configuration is based on `.github/workflows/ci.yaml`.
