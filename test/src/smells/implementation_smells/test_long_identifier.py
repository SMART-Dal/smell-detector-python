import ast
import logging

import pytest
from unittest.mock import MagicMock
from src.smells.implementation_smells import LongIdentifierDetector
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction

# Sample code for class and function identifiers
short_class_name = "ShortClass"
long_class_name = "VeryLongClassNameExceedingTheUsualLength"
short_function_name = "short_func"
long_function_name = "very_long_function_name_exceeding_usual_length"


@pytest.fixture
def sm_short_class():
    return SMClass(name=short_class_name, start_line=1, end_line=1)


@pytest.fixture
def sm_long_class():
    return SMClass(name=long_class_name, start_line=2, end_line=2)


@pytest.fixture
def sm_short_function():
    return SMFunction(name=short_function_name, start_line=3, end_line=4, ast_node=ast.parse(""))


@pytest.fixture
def sm_long_function():
    return SMFunction(name=long_function_name, start_line=5, end_line=6, ast_node=ast.parse(""))


@pytest.fixture
def mock_module(sm_short_class, sm_long_class, sm_short_function, sm_long_function):
    module = MagicMock(spec=SMModule)
    module.name = "test_module"
    module.classes = [sm_short_class, sm_long_class]
    module.functions = [sm_short_function, sm_long_function]
    return module


@pytest.fixture
def detector():
    return LongIdentifierDetector()


def test_no_long_identifiers(detector, mock_module):
    # Set the threshold high to avoid detecting long identifiers
    smells = detector.detect(mock_module, {"threshold": 100})
    assert len(smells) == 0, "Should not detect any long identifiers"


def test_long_identifier(detector, mock_module):
    # Set a lower threshold to detect long class names
    smells = detector.detect(mock_module, {"threshold": 15})
    assert len(smells) == 2, "Should detect one long class name"
    assert smells[0]['entity_name'] == long_class_name, "Should correctly identify the long class name"
    assert smells[1]['entity_name'] == long_function_name, "Should correctly identify the long function name"


def test_error_handling(detector, mock_module, caplog):
    faulty_function = MagicMock(spec=SMFunction)
    mock_module.functions = [faulty_function]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {})
    assert "Error " in caplog.text, "Should log analysis errors"
