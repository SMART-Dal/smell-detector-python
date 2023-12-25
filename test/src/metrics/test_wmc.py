import ast
from unittest.mock import create_autospec

import pytest

from src.metrics import calculate_wmc_for_class, calculate_wmc_for_module
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction
from src.sourcemodel.sm_module import SMModule

# Real complex Python code for testing
complex_code = """
def complex_function(a, b):
    if a > b and b < 0 or a == 100:
        return a * b
    elif a == b:
        return a + b
    else:
        return a - b
"""


# Parse the complex code to an AST node
@pytest.fixture
def complex_function_node():
    return ast.parse(complex_code).body[0]  # The first statement should be the function definition


# Mock a function with a real complex AST node
@pytest.fixture
def mock_function_with_real_complexity(complex_function_node):
    function = create_autospec(SMFunction, instance=True)
    function.ast_node = complex_function_node
    return function


# Mock class with a list of functions including the complex one
@pytest.fixture
def mock_class(mock_function_with_real_complexity):
    py_class = create_autospec(SMClass, instance=True)
    py_class.methods = [mock_function_with_real_complexity]
    return py_class


# Mock module with a list of classes
@pytest.fixture
def mock_module(mock_class):
    module = create_autospec(SMModule, instance=True)
    module.classes = [mock_class]
    return module


# Test calculate_wmc_for_class with real complex node
def test_calculate_wmc_for_class_real_complex(mock_class):
    wmc = calculate_wmc_for_class(mock_class)
    assert wmc > 0, "WMC should be correctly calculated for the class with real complexity"


# Test calculate_wmc_for_module with real complex node
def test_calculate_wmc_for_module_real_complex(mock_module):
    wmc = calculate_wmc_for_module(mock_module)
    assert wmc > 0, "WMC should be correctly calculated for the module with real complexity"
