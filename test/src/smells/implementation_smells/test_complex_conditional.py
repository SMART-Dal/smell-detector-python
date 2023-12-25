import ast
import logging
from unittest.mock import MagicMock

import pytest

from src.smells.implementation_smells import ComplexConditionalDetector
from src.sourcemodel.sm_function import SMFunction
from src.sourcemodel.sm_module import SMModule

simple_conditional_code = "if a < b: pass"
complex_conditional_code = "if a and b or c: pass"


@pytest.fixture
def simple_conditional_node():
    return ast.parse(simple_conditional_code).body[0]


@pytest.fixture
def complex_conditional_node():
    return ast.parse(complex_conditional_code).body[0]


@pytest.fixture
def sm_function_with_simple_conditional(simple_conditional_node):
    return SMFunction(name="function_with_simple_conditional", start_line=1, end_line=10,
                      ast_node=simple_conditional_node)


@pytest.fixture
def sm_function_with_complex_conditional(complex_conditional_node):
    return SMFunction(name="function_with_complex_conditional", start_line=1, end_line=10,
                      ast_node=complex_conditional_node)


@pytest.fixture
def mock_module(sm_function_with_simple_conditional, sm_function_with_complex_conditional):
    mock_module = SMModule(name="test_module", package_name="test_package")
    mock_module.functions = [sm_function_with_simple_conditional, sm_function_with_complex_conditional]
    return mock_module


@pytest.fixture
def detector():
    return ComplexConditionalDetector()


# Test for a function with simple conditional
def test_no_complex_conditionals(detector, mock_module, sm_function_with_simple_conditional):
    mock_module.functions = [sm_function_with_simple_conditional]
    smells = detector.detect(mock_module, {"threshold": 1})
    assert len(smells) == 0, "Should not detect complex conditionals under the threshold"


# Test for a function with complex conditional
def test_detect_complex_conditionals(detector, mock_module, sm_function_with_complex_conditional):
    mock_module.functions = [sm_function_with_complex_conditional]
    smells = detector.detect(mock_module, {"threshold": 1})
    assert len(smells) > 0, "Should detect complex conditionals over the threshold"


# Test for error handling in the detector
def test_error_handling(detector, mock_module, caplog):
    faulty_function = MagicMock(spec=SMFunction)
    mock_module.functions = [faulty_function]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {})
    assert "Error analyzing" in caplog.text, "Should log analysis errors"
    assert len(smells) == 0, "Should not return any smells when an error occurs"
