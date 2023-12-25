import ast
import logging
import pytest
from unittest.mock import MagicMock

from src.smells.implementation_smells import MissingDefaultDetector
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction

# Sample code snippets for functions and classes
code_with_missing_default = """
def function_with_missing_default(a):
    if a == 1:
        return 'one'
    elif a == 2:
        return 'two'
"""

code_with_default_case = """
def function_with_default(a):
    if a == 1:
        return 'one'
    else:
        return 'other'
"""


@pytest.fixture
def missing_default_function_node():
    return ast.parse(code_with_missing_default).body[0]


@pytest.fixture
def default_case_function_node():
    return ast.parse(code_with_default_case).body[0]


@pytest.fixture
def sm_function_with_missing_default(missing_default_function_node):
    return SMFunction(name="function_with_missing_default", start_line=1, end_line=10,
                      ast_node=missing_default_function_node)


@pytest.fixture
def sm_function_with_default(default_case_function_node):
    return SMFunction(name="function_with_default", start_line=1, end_line=10, ast_node=default_case_function_node)


@pytest.fixture
def mock_module(sm_function_with_missing_default, sm_function_with_default):
    mock_module = SMModule(name="test_module", package_name="test_package")
    mock_module.functions = [sm_function_with_missing_default, sm_function_with_default]
    return mock_module


@pytest.fixture
def detector():
    return MissingDefaultDetector()


# Test for a function with a missing default case
def test_detect_missing_default(detector, mock_module):
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1, "Should detect a missing default case"


# Test for a function with a default case
def test_no_missing_default(detector, mock_module, sm_function_with_default):
    mock_module.functions = [sm_function_with_default]  # Override with just the default case function
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0, "Should not detect a missing default case when it is present"


# Test for error handling in the detector
def test_error_handling(detector, mock_module, caplog):
    faulty_function = MagicMock(spec=SMFunction)
    mock_module.functions = [faulty_function]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {})
    assert "Error analyzing" in caplog.text, "Should log analysis errors"
    assert len(smells) == 0, "Should not return any smells when an error occurs"
