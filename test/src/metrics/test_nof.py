import pytest
from unittest.mock import create_autospec

from src.metrics import calculate_nof, calculate_nopf, calculate_module_nof, calculate_module_nopf
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule
import logging


# Mock SMClass with class fields
@pytest.fixture
def mock_class():
    py_class = create_autospec(SMClass, instance=True)
    py_class.class_fields = {'private_field': 'private', 'public_field': 'public'}
    return py_class


# Mock SMModule with global variables
@pytest.fixture
def mock_module():
    py_module = create_autospec(SMModule, instance=True)
    py_module.global_variables = ['_private_var', 'public_var']
    return py_module


# Test calculate_nof with a valid class
def test_calculate_nof(mock_class):
    nof = calculate_nof(mock_class)
    assert nof == 2, "NOF should be calculated correctly for class"


# Test calculate_nopf with a valid class
def test_calculate_nopf(mock_class):
    nopf = calculate_nopf(mock_class)
    assert nopf == 1, "NOPF should be calculated correctly for class"


# Test calculate_module_nof with a valid module
def test_calculate_module_nof(mock_module):
    nof = calculate_module_nof(mock_module)
    assert nof == 2, "Module NOF should be calculated correctly for module"


# Test calculate_module_nopf with a valid module
def test_calculate_module_nopf(mock_module):
    nopf = calculate_module_nopf(mock_module)
    assert nopf == 1, "Module NOPF should be calculated correctly for module"


# Test calculate_nof with invalid class
def test_calculate_nof_invalid_class(caplog):
    invalid_class = "not a class object"
    nof = calculate_nof(invalid_class)
    assert nof == 0, "NOF should be 0 for invalid class object"
    assert "Invalid class object provided" in caplog.text


# Test calculate_nopf with invalid class
def test_calculate_nopf_invalid_class(caplog):
    invalid_class = "not a class object"
    nopf = calculate_nopf(invalid_class)
    assert nopf == 0, "NOPF should be 0 for invalid class object"
    assert "Invalid class object provided" in caplog.text


# Test calculate_module_nof with invalid module
def test_calculate_module_nof_invalid_module(caplog):
    invalid_module = "not a module object"
    nof = calculate_module_nof(invalid_module)
    assert nof == 0, "Module NOF should be 0 for invalid module object"
    assert "Invalid module object provided" in caplog.text


# Test calculate_module_nopf with invalid module
def test_calculate_module_nopf_invalid_module(caplog):
    invalid_module = "not a module object"
    nopf = calculate_module_nopf(invalid_module)
    assert nopf == 0, "Module NOPF should be 0 for invalid module object"
    assert "Invalid module object provided" in caplog.text
