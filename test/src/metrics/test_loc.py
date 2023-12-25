import pytest
from unittest.mock import create_autospec

from src.metrics import calculate_module_loc, calculate_class_loc, calculate_function_loc
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction
import logging


# Mock SMClass
@pytest.fixture
def mock_class():
    py_class = create_autospec(SMClass, instance=True)
    py_class.start_line = 10
    py_class.end_line = 50
    return py_class


# Mock SMFunction
@pytest.fixture
def mock_function():
    py_function = create_autospec(SMFunction, instance=True)
    py_function.start_line = 100
    py_function.end_line = 150
    return py_function


# Mock SMModule with a class and a function
@pytest.fixture
def mock_module(mock_class, mock_function):
    py_module = create_autospec(SMModule, instance=True)
    py_module.classes = [mock_class]
    py_module.functions = [mock_function]
    return py_module


# Test calculate_module_loc
def test_calculate_module_loc(mock_module, mock_class, mock_function):
    loc = calculate_module_loc(mock_module)
    expected_loc = calculate_class_loc(mock_class) + calculate_function_loc(mock_function)
    assert loc == expected_loc, "Total LOC should be the sum of class LOC and function LOC"


# Test calculate_class_loc
def test_calculate_class_loc(mock_class):
    loc = calculate_class_loc(mock_class)
    assert loc == 41, "LOC should be calculated correctly for class"


# Test calculate_function_loc
def test_calculate_function_loc(mock_function):
    loc = calculate_function_loc(mock_function)
    assert loc == 51, "LOC should be calculated correctly for function"


# Test calculate_module_loc with invalid module
def test_calculate_module_loc_invalid_module(caplog):
    invalid_module = "not a module object"
    loc = calculate_module_loc(invalid_module)
    assert loc == 0, "LOC should be 0 for invalid module object"
    assert "Invalid module object provided" in caplog.text


# Test calculate_class_loc with invalid class
def test_calculate_class_loc_invalid_class(caplog):
    invalid_class = "not a class object"
    loc = calculate_class_loc(invalid_class)
    assert loc == 0, "LOC should be 0 for invalid class object"
    assert "Invalid class object provided" in caplog.text


# Test calculate_function_loc with invalid function
def test_calculate_function_loc_invalid_function(caplog):
    invalid_function = "not a function object"
    loc = calculate_function_loc(invalid_function)
    assert loc == 0, "LOC should be 0 for invalid function object"
    assert "Invalid function object provided" in caplog.text
