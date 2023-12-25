import ast
import logging
import pytest
from unittest.mock import MagicMock

from src.smells.implementation_smells import LongStatementDetector
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_function import SMFunction

# Sample code snippets for functions
short_statement_code = "a = 1"
long_statement_code = "some_variable = 'some_really_long_string_value' + 'another_long_string' + 'yet_another_long_string_part' * 10"


@pytest.fixture
def short_statement_node():
    return ast.parse(short_statement_code).body[0]


@pytest.fixture
def long_statement_node():
    return ast.parse(long_statement_code).body[0]


@pytest.fixture
def sm_function_with_short_statement(short_statement_node):
    return SMFunction(name="short_statement_function", start_line=1, end_line=3,
                      ast_node=MagicMock(function_body=[short_statement_node]))


@pytest.fixture
def sm_function_with_long_statement(long_statement_node):
    return SMFunction(name="long_statement_function", start_line=1, end_line=3,
                      ast_node=MagicMock(function_body=[long_statement_node]))


@pytest.fixture
def mock_module(sm_function_with_short_statement, sm_function_with_long_statement):
    mock_module = SMModule(name="test_module", package_name="test_package")
    mock_module.functions = [sm_function_with_short_statement, sm_function_with_long_statement]
    return mock_module


@pytest.fixture
def detector():
    return LongStatementDetector()


# Test for no long statements
def test_no_long_statements(detector, mock_module, sm_function_with_short_statement):
    """Test that no smells are detected for short statements."""
    mock_module.functions = [sm_function_with_short_statement]  # Override with just the short statement function
    smells = detector.detect(mock_module, {"threshold": 100})
    assert len(smells) == 0, "Should not detect smells in short statements"


# Test for long statements
# def test_long_statements(detector, mock_module, sm_function_with_long_statement):
#     """Test that smells are detected for long statements."""
#     mock_module.functions = [sm_function_with_long_statement]  # Override with just the long statement function
#     smells = detector.detect(mock_module, {"threshold": 100})
#     assert len(smells) == 1, "Should detect smells in long statements"


# Test error handling
def test_error_handling(detector, mock_module, mocker, caplog):
    """Test that errors during analysis are logged and handled gracefully."""
    faulty_function = MagicMock(spec=SMFunction,
                                ast_node=MagicMock(function_body=[MagicMock(side_effect=Exception("Test Exception"))]))
    mock_module.functions = [faulty_function]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {"threshold": 100})
    assert "Error analyzing" in caplog.text, "Should log analysis errors"
    assert len(smells) == 0, "Should not return any smells when an error occurs"


# Test configuration respect
def test_configuration_respect(detector, mock_module, sm_function_with_long_statement):
    """Test that the detector respects the given threshold configuration."""
    mock_module.functions = [sm_function_with_long_statement]  # Override with just the long statement function
    smells = detector.detect(mock_module, {"threshold": 250})
    assert len(smells) == 0, "Should not detect smells when the statement length is within the threshold"
