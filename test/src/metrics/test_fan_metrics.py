from unittest.mock import MagicMock

import pytest

from src.metrics import calculate_fan_in_class, calculate_fan_out_class, calculate_fan_in_module, \
    calculate_fan_out_module


# Mock the classes and modules
@pytest.fixture
def mock_class():
    py_class = MagicMock()
    py_class.method_interactions = {'method1': ['interaction1', 'interaction2'], 'method2': ['interaction3']}
    py_class.external_dependencies = {'dependency1', 'dependency2', 'dependency3'}
    return py_class


@pytest.fixture
def mock_module():
    py_module = MagicMock()
    py_module.name = "test_module"
    return py_module


@pytest.fixture
def mock_dependency_graph():
    graph = MagicMock()
    graph.in_degree.return_value = 3  # Suppose the module has 3 incoming dependencies
    graph.out_degree.return_value = 2  # Suppose the module has 2 outgoing dependencies
    return graph


# Test the calculate_fan_in_class function
def test_calculate_fan_in_class(mock_class):
    assert calculate_fan_in_class(mock_class) == 2, "Should return the correct count of method interactions"


# Test the calculate_fan_out_class function
def test_calculate_fan_out_class(mock_class):
    assert calculate_fan_out_class(mock_class) == 3, "Should return the correct count of external dependencies"


# Test the calculate_fan_in_module function
def test_calculate_fan_in_module(mock_module, mock_dependency_graph):
    assert calculate_fan_in_module(mock_module,
                                   mock_dependency_graph) == 3, "Should return the correct fan-in for the module"


# Test the calculate_fan_out_module function
def test_calculate_fan_out_module(mock_module, mock_dependency_graph):
    assert calculate_fan_out_module(mock_module,
                                    mock_dependency_graph) == 2, "Should return the correct fan-out for the module"


# Test for invalid class object
def test_calculate_fan_in_class_invalid_object(caplog):
    invalid_class = "not a class object"
    assert calculate_fan_in_class(invalid_class) == 0, "Should return 0 for invalid class object"
    assert "Invalid class object provided" in caplog.text


# Test for invalid module object
def test_calculate_fan_in_module_invalid_object(caplog, mock_dependency_graph):
    invalid_module = "not a module object"
    assert calculate_fan_in_module(invalid_module,
                                   mock_dependency_graph) == 0, "Should return 0 for invalid module object"
    assert "Error calculating fan-in for module" in caplog.text
