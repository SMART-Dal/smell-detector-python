import ast
import logging

import pytest
from unittest.mock import MagicMock, create_autospec
from src.smells.implementation_smells import MagicNumberDetector
from src.sourcemodel.sm_function import SMFunction

# Sample code for functions with and without magic numbers
code_with_magic_number = "def func(): return 42"
code_without_magic_number = "def func(): return 1"  # Assuming 1 is not considered a magic number here


@pytest.fixture
def function_with_magic_number_node():
    return ast.parse(code_with_magic_number).body[0]


@pytest.fixture
def function_without_magic_number_node():
    return ast.parse(code_without_magic_number).body[0]


@pytest.fixture
def sm_function_with_magic_number(function_with_magic_number_node):
    function = create_autospec(SMFunction, instance=True)
    function.name = "function_with_magic_number"
    function.ast_node = function_with_magic_number_node
    return function


@pytest.fixture
def sm_function_without_magic_number(function_without_magic_number_node):
    function = create_autospec(SMFunction, instance=True)
    function.name = "function_without_magic_number"
    function.ast_node = function_without_magic_number_node
    return function


@pytest.fixture
def mock_module(sm_function_with_magic_number, sm_function_without_magic_number):
    module = MagicMock()
    module.name = "test_module"
    module.functions = [sm_function_with_magic_number, sm_function_without_magic_number]
    return module


@pytest.fixture
def detector():
    return MagicNumberDetector()


def test_detect_magic_numbers(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": [0, 1]})
    assert len(smells) == 1, "Should detect one magic number"
    assert "42" in smells[0]['details'], "Should detect the magic number 42"


def test_no_magic_numbers(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": range(0, 100)})  # Assuming all numbers are allowed
    assert len(smells) == 0, "Should not detect any magic numbers when all are allowed"


def test_error_handling(detector, mock_module, caplog):
    faulty_function = MagicMock(spec=SMFunction)
    mock_module.functions = [faulty_function]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {})
    assert "Error analyzing" in caplog.text, "Should log analysis errors"
    assert len(smells) == 0, "Should not return any smells when an error occurs"
