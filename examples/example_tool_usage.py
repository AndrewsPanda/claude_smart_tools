"""Example usage of the ExampleTool."""
from claude_tools.tools.example_tool import ExampleTool
from claude_tools.utils.logging import setup_logging


def main():
    """Demonstrate how to use the ExampleTool."""
    # Set up logging
    setup_logging(level="INFO")
    
    # Create an instance of the tool
    tool = ExampleTool()
    
    # Get tool information
    info = tool.get_info()
    print(f"Tool: {info['name']} v{info['version']}")
    print(f"Description: {info['description']}")
    print()
    
    # Example text
    sample_text = "Hello, Claude Smart Tools!"
    
    # Demonstrate different operations
    operations = ["upper", "lower", "reverse", "capitalize"]
    
    for operation in operations:
        print(f"Operation: {operation}")
        result = tool.execute(text=sample_text, operation=operation)
        print(f"  Original: {result['original']}")
        print(f"  Result: {result['result']}")
        print(f"  Length change: {result['length_before']} -> {result['length_after']}")
        print()
    
    # Demonstrate configuration
    tool.configure({"verbose": True, "max_length": 100})
    
    # Demonstrate error handling
    print("Testing error handling:")
    try:
        tool.execute(text=sample_text, operation="invalid")
    except ValueError as e:
        print(f"  Caught expected error: {e}")


if __name__ == "__main__":
    main()