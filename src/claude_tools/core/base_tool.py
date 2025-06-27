"""Base class for all tools in the Claude Smart Tools collection."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


class BaseTool(ABC):
    """Abstract base class for all tools.
    
    Each tool should inherit from this class and implement the required methods.
    This provides a consistent interface across all tools in the collection.
    """
    
    def __init__(self, name: str, description: str, version: str = "0.1.0"):
        """Initialize the base tool.
        
        Args:
            name: The name of the tool
            description: A brief description of what the tool does
            version: Tool version (default: "0.1.0")
        """
        self.name = name
        self.description = description
        self.version = version
        self.logger = logging.getLogger(f"claude_tools.{name}")
        self._config: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the main functionality of the tool.
        
        This method must be implemented by each tool.
        
        Args:
            **kwargs: Tool-specific arguments
            
        Returns:
            Tool-specific return value
        """
        pass
    
    @abstractmethod
    def validate_inputs(self, **kwargs) -> bool:
        """Validate the inputs before execution.
        
        This method must be implemented by each tool.
        
        Args:
            **kwargs: Tool-specific arguments to validate
            
        Returns:
            True if inputs are valid, False otherwise
        """
        pass
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the tool with specific settings.
        
        Args:
            config: Configuration dictionary
        """
        self._config.update(config)
        self.logger.debug(f"Tool {self.name} configured with: {config}")
    
    def get_info(self) -> Dict[str, str]:
        """Get information about the tool.
        
        Returns:
            Dictionary containing tool information
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version
        }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', version='{self.version}')"