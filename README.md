# Claude Smart Tools

A collection of reusable tools for various purposes, designed to be modular and easy to extend.

## Overview

Claude Smart Tools is a Python project that provides a framework for building and organizing various tools. Each tool is self-contained but can share common functionality and utilities with other tools in the collection.

## Features

- **Modular Architecture**: Each tool is independent but can leverage shared utilities
- **Consistent Interface**: All tools inherit from a common base class
- **Type Safety**: Full type hints with mypy validation
- **Quality Assurance**: Pre-commit hooks, testing, and code formatting
- **Easy Extension**: Simple framework for adding new tools

## Installation

### For Users

```bash
pip install claude-smart-tools
```

### For Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/claude-smart-tools.git
cd claude-smart-tools
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Project Structure

```
claude-smart-tools/
├── src/
│   └── claude_tools/
│       ├── __init__.py
│       ├── core/           # Core functionality and base classes
│       │   ├── __init__.py
│       │   └── base_tool.py
│       ├── tools/          # Individual tools
│       │   └── __init__.py
│       └── utils/          # Shared utilities
│           ├── __init__.py
│           └── logging.py
├── tests/                  # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/                   # Documentation
├── examples/               # Example usage
├── pyproject.toml         # Project configuration
├── requirements.txt       # Core dependencies
└── requirements-dev.txt   # Development dependencies
```

## Creating a New Tool

To create a new tool, follow these steps:

1. Create a new module in `src/claude_tools/tools/`
2. Inherit from `BaseTool` class
3. Implement required methods: `execute()` and `validate_inputs()`
4. Add tests in `tests/unit/`

Example:

```python
from claude_tools.core.base_tool import BaseTool

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Does something useful",
            version="0.1.0"
        )
    
    def validate_inputs(self, **kwargs):
        # Validate your inputs
        return True
    
    def execute(self, **kwargs):
        # Implement your tool's logic
        return "Result"
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
ruff check . --fix
```

### Type Checking

```bash
mypy src
```

### Running All Checks

```bash
pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-tool`)
3. Commit your changes (`git commit -m 'Add amazing tool'`)
4. Push to the branch (`git push origin feature/amazing-tool`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.