import ast
import pytest
from unittest.mock import MagicMock
from src.smells.implementation_smells import EmptyCatchBlockDetector

# Sample code snippets
code_with_empty_catch = """
try:
    risky_operation()
except Exception:
    pass  # Empty catch block
"""

code_with_non_empty_catch = """
try:
    risky_operation()
except Exception as e:
    log_error(e)  # Non-empty catch block
"""


@pytest.fixture
def mock_module():
    # Mock module with functions and methods
    module = MagicMock()
    module.name = "test_module"
    module.classes = []
    module.functions = []
    return module


@pytest.fixture
def detector():
    return EmptyCatchBlockDetector()


@pytest.fixture
def empty_catch_function_node():
    return ast.parse(code_with_empty_catch).body[0]


@pytest.fixture
def non_empty_catch_function_node():
    return ast.parse(code_with_non_empty_catch).body[0]


def test_empty_catch_block_detection(detector, mock_module, empty_catch_function_node):
    mock_module.functions = [MagicMock(ast_node=empty_catch_function_node, name="function_with_empty_catch")]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1, "Should detect a single smell for an empty catch block."


def test_non_empty_catch_block_detection(detector, mock_module, non_empty_catch_function_node):
    mock_module.functions = [MagicMock(ast_node=non_empty_catch_function_node, name="function_with_non_empty_catch")]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0, "Should not detect smells for non-empty catch blocks."


def test_error_handling(detector, mock_module):
    mock_module.functions = [MagicMock(side_effect=Exception("Test exception"))]
    smells = detector.detect(mock_module, {})
    # Check that no smells are returned and no unhandled exceptions occur
    assert isinstance(smells, list), "Should return a list even on error."
    assert len(smells) == 0, "Should return an empty list on error."


def test_detector_with_methods(detector, mock_module, empty_catch_function_node):
    mock_class = MagicMock()
    mock_class.methods = [MagicMock(ast_node=empty_catch_function_node, name="method_with_empty_catch")]
    mock_module.classes = [mock_class]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1, "Should detect smells in class methods as well."
