"""Pytest configuration and fixtures."""
import pytest
from pathlib import Path
import sys

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_config():
    """Provide a sample configuration for testing."""
    return {
        "debug": True,
        "timeout": 30,
        "retry_count": 3
    }


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace for file-based tests."""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace