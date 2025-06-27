# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Smart Tools is a Python project providing a modular framework for building various tools. Each tool is self-contained but can share common functionality through the base class and utilities.

## Development Commands

### Virtual Environment
- Activate: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
- Deactivate: `deactivate`

### Dependencies
- Install core dependencies: `pip install -r requirements.txt`
- Install dev dependencies: `pip install -r requirements-dev.txt`
- Install in editable mode: `pip install -e .`

### Testing
- Run all tests: `pytest`
- Run with coverage: `pytest --cov=claude_tools`
- Run specific test: `pytest tests/unit/test_base_tool.py::TestBaseTool::test_initialization`
- Run tests in parallel: `pytest -n auto`

### Code Quality
- Format code: `black src tests`
- Lint code: `ruff check . --fix`
- Type check: `mypy src`
- Run all checks: `pre-commit run --all-files`

### Pre-commit Hooks
- Install hooks: `pre-commit install`
- Update hooks: `pre-commit autoupdate`
- Run manually: `pre-commit run --all-files`

## Project Architecture

```
src/claude_tools/
├── core/           # Core functionality
│   └── base_tool.py    # Abstract base class for all tools
├── tools/          # Individual tool implementations
│   └── example_tool.py # Example tool showing the pattern
├── utils/          # Shared utilities
│   └── logging.py      # Logging configuration
└── cli.py          # Command-line interface
```

### Key Design Patterns

1. **Base Tool Pattern**: All tools inherit from `BaseTool` which provides:
   - Standard initialization with name, description, version
   - Abstract methods: `execute()` and `validate_inputs()`
   - Built-in logging per tool
   - Configuration management
   - Consistent interface via `get_info()`

2. **Tool Organization**: Each tool is a separate module in `src/claude_tools/tools/`
   - Self-contained functionality
   - Can import from `utils` for shared code
   - Must implement validation and execution

3. **Testing Structure**: Mirrors source structure
   - Unit tests for each tool in `tests/unit/`
   - Integration tests in `tests/integration/`
   - Shared fixtures in `tests/conftest.py`

## Adding a New Tool

1. Create tool file: `src/claude_tools/tools/your_tool.py`
2. Inherit from `BaseTool` and implement required methods
3. Add unit tests: `tests/unit/test_your_tool.py`
4. Update CLI if needed in `src/claude_tools/cli.py`
5. Add example usage in `examples/`
6. Document in `docs/tools/`

See `docs/tool_template.md` for a complete template.

## Important Conventions

- Use type hints for all functions and methods
- Follow PEP 8 (enforced by black and ruff)
- Write comprehensive docstrings (Google style)
- Log important operations using `self.logger`
- Validate inputs before execution
- Raise clear exceptions with helpful messages
- Test both success and failure cases

## Current Tools

- **example_tool**: Demonstrates the framework with text transformations
- **text_analyzer**: Analyzes text files for metrics and statistics (word count, frequency, readability)

## Project Status

### Completed Setup (Initial Session)
- ✅ Project structure with src layout
- ✅ Modern Python packaging with pyproject.toml
- ✅ Development dependencies and requirements files
- ✅ Pre-commit hooks for code quality
- ✅ Testing framework with pytest and coverage
- ✅ Base tool framework with abstract class
- ✅ Two example tools with full test coverage
- ✅ Documentation and templates

### Next Steps
- Implement first production tool
- Set up continuous integration (GitHub Actions)
- Add more comprehensive documentation
- Create tool registry/discovery system
- Add tool chaining capabilities

## Common Issues and Solutions

1. **Import Errors**: Ensure you've installed the package in editable mode: `pip install -e .`
2. **Pre-commit Failures**: Run `black src tests` and `ruff check . --fix` before committing
3. **Test Failures**: Check that test fixtures match expected data formats
4. **Type Errors**: Run `mypy src` to catch type issues early
