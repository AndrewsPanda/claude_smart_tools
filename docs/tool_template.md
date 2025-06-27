# Tool Template

This template provides a starting point for creating new tools in the Claude Smart Tools collection.

## Tool Structure

```python
"""Brief description of what your tool does."""
from typing import Any, Dict, Optional
from claude_tools.core.base_tool import BaseTool


class YourTool(BaseTool):
    """Detailed description of your tool.
    
    Explain what the tool does, its main features,
    and any important considerations.
    """
    
    def __init__(self):
        """Initialize your tool."""
        super().__init__(
            name="your_tool_name",
            description="Brief description for tool registry",
            version="0.1.0"
        )
        # Initialize any tool-specific attributes here
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate the inputs before execution.
        
        Args:
            **kwargs: The inputs to validate
            
        Returns:
            True if inputs are valid, False otherwise
        """
        # Implement your validation logic
        # Log errors for invalid inputs
        # Example:
        # if "required_param" not in kwargs:
        #     self.logger.error("Missing required parameter: 'required_param'")
        #     return False
        return True
    
    def execute(self, **kwargs) -> Any:
        """Execute the main functionality of your tool.
        
        Args:
            **kwargs: Tool-specific arguments
            
        Returns:
            Tool-specific return value
            
        Raises:
            ValueError: If inputs are invalid
            Any other exceptions your tool might raise
        """
        if not self.validate_inputs(**kwargs):
            raise ValueError("Invalid inputs provided")
        
        # Implement your tool's logic here
        # Use self.logger for logging
        # Access configuration with self._config
        
        return result
```

## Best Practices

1. **Validation**: Always validate inputs in `validate_inputs()` before execution
2. **Logging**: Use `self.logger` for all logging needs
3. **Error Handling**: Provide clear error messages
4. **Documentation**: Write comprehensive docstrings
5. **Type Hints**: Use type hints for all parameters and return values
6. **Testing**: Write unit tests for your tool

## Example Test Template

```python
"""Tests for YourTool."""
import pytest
from claude_tools.tools.your_tool import YourTool


class TestYourTool:
    """Test cases for YourTool."""
    
    def test_initialization(self):
        """Test tool initialization."""
        tool = YourTool()
        assert tool.name == "your_tool_name"
        assert tool.version == "0.1.0"
    
    def test_validate_inputs_success(self):
        """Test input validation with valid inputs."""
        tool = YourTool()
        assert tool.validate_inputs(required_param="value") is True
    
    def test_validate_inputs_failure(self):
        """Test input validation with invalid inputs."""
        tool = YourTool()
        assert tool.validate_inputs() is False
    
    def test_execute_success(self):
        """Test successful execution."""
        tool = YourTool()
        result = tool.execute(required_param="value")
        # Assert expected results
    
    def test_execute_failure(self):
        """Test execution with invalid inputs."""
        tool = YourTool()
        with pytest.raises(ValueError):
            tool.execute()
```

## Integration Guide

1. Create your tool file in `src/claude_tools/tools/`
2. Add tests in `tests/unit/test_your_tool.py`
3. Update `src/claude_tools/tools/__init__.py` to export your tool
4. Add documentation in `docs/tools/your_tool.md`
5. Create examples in `examples/your_tool_example.py`