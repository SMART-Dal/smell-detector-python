import logging
from unittest.mock import create_autospec

import pytest

from src.metrics import calculate_parameter_count
from src.sourcemodel.sm_function import SMFunction
from src.sourcemodel.sm_parameter import SMParameter


# Mock SMFunction with parameters
@pytest.fixture
def mock_function():
    py_function = create_autospec(SMFunction, instance=True)
    param1 = create_autospec(SMParameter, instance=True)
    param2 = create_autospec(SMParameter, instance=True)
    py_function.parameters = [param1, param2]
    return py_function


# Test calculate_parameter_count with a valid function
def test_calculate_parameter_count(mock_function):
    param_count = calculate_parameter_count(mock_function)
    assert param_count == 2, "Parameter count should be calculated correctly for function"


# Test calculate_parameter_count with invalid function
def test_calculate_parameter_count_invalid_function(caplog):
    invalid_function = "not a function object"
    param_count = calculate_parameter_count(invalid_function)
    assert param_count == 0, "Parameter count should be 0 for invalid function object"
    assert "Invalid function object provided" in caplog.text
