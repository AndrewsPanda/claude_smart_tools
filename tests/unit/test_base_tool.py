"""Tests for the base tool class."""
import pytest
from claude_tools.core.base_tool import BaseTool


class TestTool(BaseTool):
    """A concrete implementation of BaseTool for testing."""
    
    def execute(self, **kwargs):
        """Execute test tool."""
        if not self.validate_inputs(**kwargs):
            raise ValueError("Invalid inputs")
        return f"Executed with: {kwargs}"
    
    def validate_inputs(self, **kwargs):
        """Validate test inputs."""
        return "value" in kwargs


class TestBaseTool:
    """Test cases for BaseTool."""
    
    def test_initialization(self):
        """Test tool initialization."""
        tool = TestTool(
            name="test_tool",
            description="A test tool",
            version="1.0.0"
        )
        
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
        assert tool.version == "1.0.0"
        assert tool._config == {}
    
    def test_get_info(self):
        """Test getting tool information."""
        tool = TestTool(
            name="test_tool",
            description="A test tool"
        )
        
        info = tool.get_info()
        assert info["name"] == "test_tool"
        assert info["description"] == "A test tool"
        assert info["version"] == "0.1.0"  # default version
    
    def test_configure(self):
        """Test tool configuration."""
        tool = TestTool(
            name="test_tool",
            description="A test tool"
        )
        
        config = {"option1": "value1", "option2": 42}
        tool.configure(config)
        
        assert tool._config == config
    
    def test_execute_with_valid_inputs(self):
        """Test execution with valid inputs."""
        tool = TestTool(
            name="test_tool",
            description="A test tool"
        )
        
        result = tool.execute(value="test")
        assert result == "Executed with: {'value': 'test'}"
    
    def test_execute_with_invalid_inputs(self):
        """Test execution with invalid inputs."""
        tool = TestTool(
            name="test_tool",
            description="A test tool"
        )
        
        with pytest.raises(ValueError, match="Invalid inputs"):
            tool.execute(invalid="test")
    
    def test_repr(self):
        """Test string representation."""
        tool = TestTool(
            name="test_tool",
            description="A test tool",
            version="1.0.0"
        )
        
        assert repr(tool) == "TestTool(name='test_tool', version='1.0.0')"