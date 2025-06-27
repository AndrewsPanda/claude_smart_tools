"""Example tool to demonstrate the framework."""
from typing import Dict, Any
from claude_tools.core.base_tool import BaseTool


class ExampleTool(BaseTool):
    """An example tool that demonstrates the framework.
    
    This tool performs simple text transformations to show
    how to implement a tool using the BaseTool interface.
    """
    
    def __init__(self):
        """Initialize the example tool."""
        super().__init__(
            name="example_tool",
            description="Demonstrates the tool framework with text transformations",
            version="0.1.0"
        )
    
    def validate_inputs(self, **kwargs) -> bool:
        """Validate that required inputs are provided.
        
        Args:
            **kwargs: Should contain 'text' and 'operation'
            
        Returns:
            True if inputs are valid, False otherwise
        """
        if "text" not in kwargs:
            self.logger.error("Missing required parameter: 'text'")
            return False
        
        if "operation" not in kwargs:
            self.logger.error("Missing required parameter: 'operation'")
            return False
        
        valid_operations = ["upper", "lower", "reverse", "capitalize"]
        if kwargs["operation"] not in valid_operations:
            self.logger.error(
                f"Invalid operation: {kwargs['operation']}. "
                f"Valid operations are: {valid_operations}"
            )
            return False
        
        return True
    
    def execute(self, text: str, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute the text transformation.
        
        Args:
            text: The text to transform
            operation: The operation to perform (upper, lower, reverse, capitalize)
            **kwargs: Additional optional parameters
            
        Returns:
            Dictionary containing the result and metadata
        """
        if not self.validate_inputs(text=text, operation=operation, **kwargs):
            raise ValueError("Invalid inputs provided")
        
        self.logger.info(f"Performing '{operation}' operation on text")
        
        result = ""
        if operation == "upper":
            result = text.upper()
        elif operation == "lower":
            result = text.lower()
        elif operation == "reverse":
            result = text[::-1]
        elif operation == "capitalize":
            result = text.capitalize()
        
        return {
            "original": text,
            "result": result,
            "operation": operation,
            "length_before": len(text),
            "length_after": len(result)
        }