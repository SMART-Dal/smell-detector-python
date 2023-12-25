import pytest
import logging
import networkx as nx

from src.metrics import calculate_lcom4
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod


# Helper function to create a mock method with specified interactions
def create_mock_method(mocker, name, interactions):
    method = mocker.create_autospec(SMMethod, instance=True)
    method.name = name
    method.method_interactions = interactions
    return method


# Test fixture for a simple class with no interactions (LCOM4 should be high)
@pytest.fixture
def simple_class_no_interactions(mocker):
    methods = [
        create_mock_method(mocker, 'method1', set()),
        create_mock_method(mocker, 'method2', set())
    ]
    py_class = mocker.create_autospec(SMClass, instance=True)
    py_class.methods = methods
    py_class.method_interactions = {method.name: method.method_interactions for method in methods}
    return py_class


# Test fixture for a complex class with interactions (LCOM4 should be lower)
@pytest.fixture
def complex_class_with_interactions(mocker):
    methods = [
        create_mock_method(mocker, 'method1', {'method2'}),
        create_mock_method(mocker, 'method2', {'method1', 'method3'}),
        create_mock_method(mocker, 'method3', {'method2'})
    ]
    py_class = mocker.create_autospec(SMClass, instance=True)
    py_class.methods = methods
    py_class.method_interactions = {method.name: method.method_interactions for method in methods}
    return py_class


@pytest.fixture
def class_with_single_method(mocker):
    methods = [create_mock_method(mocker, 'single_method', set())]
    py_class = mocker.create_autospec(SMClass, instance=True)
    py_class.methods = methods
    py_class.method_interactions = {method.name: method.method_interactions for method in methods}
    return py_class


# Test fixture for a class where all methods interact with each other
@pytest.fixture
def fully_connected_class(mocker):
    methods = [
        create_mock_method(mocker, 'method1', {'method2', 'method3'}),
        create_mock_method(mocker, 'method2', {'method1', 'method3'}),
        create_mock_method(mocker, 'method3', {'method1', 'method2'})
    ]
    py_class = mocker.create_autospec(SMClass, instance=True)
    py_class.methods = methods
    py_class.method_interactions = {method.name: method.method_interactions for method in methods}
    return py_class


# Test for class with no method interactions
def test_lcom4_high_for_no_interactions(simple_class_no_interactions):
    lcom4 = calculate_lcom4(simple_class_no_interactions)
    assert lcom4 == len(
        simple_class_no_interactions.methods), "LCOM4 should be equal to the number of methods for a class with no interactions"


# Test for class with method interactions
def test_lcom4_lower_for_interactions(complex_class_with_interactions):
    lcom4 = calculate_lcom4(complex_class_with_interactions)
    assert lcom4 < len(
        complex_class_with_interactions.methods), "LCOM4 should be lower than the number of methods for a class with interactions"


# Test for a class with a single method
def test_lcom4_for_single_method(class_with_single_method):
    lcom4 = calculate_lcom4(class_with_single_method)
    assert lcom4 == 1, "LCOM4 should be 1 for a class with a single method"


# Test for fully connected class (all methods interact)
def test_lcom4_for_fully_connected_class(fully_connected_class):
    lcom4 = calculate_lcom4(fully_connected_class)
    assert lcom4 == 1, "LCOM4 should be 1 for a fully connected class"


# Test to handle unexpected errors during LCOM4 calculation
def test_lcom4_unexpected_error(mocker, complex_class_with_interactions):
    mocker.patch.object(nx, 'number_connected_components', side_effect=Exception("Unexpected Error"))
    mocker.patch.object(logging, 'error')  # Patch logging to suppress output during test
    lcom4 = calculate_lcom4(complex_class_with_interactions)
    assert lcom4 == 0, "LCOM4 should be 0 when an unexpected error occurs"
    logging.error.assert_called_once()  # Ensure that an error was logged


# Test for invalid class structure
def test_lcom4_error_with_invalid_class_structure(mocker):
    py_class = mocker.create_autospec(SMClass, instance=True)
    mocker.patch.object(logging, 'error')  # Patch logging to suppress output during test
    lcom4 = calculate_lcom4(py_class)
    assert lcom4 == 0, "LCOM4 should be 0 for an invalid class structure"
    logging.error.assert_called_once()  # Ensure that an error was logged
