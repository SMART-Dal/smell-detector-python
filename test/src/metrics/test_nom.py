from unittest.mock import create_autospec

import pytest

from src.metrics import calculate_nom, calculate_nopm
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod


# Mock SMClass with methods
@pytest.fixture
def mock_class():
    py_class = create_autospec(SMClass, instance=True)
    method1 = create_autospec(SMMethod, instance=True)
    method1.name = "public_method"
    method2 = create_autospec(SMMethod, instance=True)
    method2.name = "_private_method"
    py_class.methods = [method1, method2]
    return py_class


# Test calculate_nom with a valid class
def test_calculate_nom(mock_class):
    nom = calculate_nom(mock_class)
    assert nom == 2, "NOM should be calculated correctly for class"


# Test calculate_nopm with a valid class
def test_calculate_nopm(mock_class):
    nopm = calculate_nopm(mock_class)
    assert nopm == 1, "NOPM should be calculated correctly for class"


# Test calculate_nom with invalid class
def test_calculate_nom_invalid_class(caplog):
    invalid_class = "not a class object"
    nom = calculate_nom(invalid_class)
    assert nom == 0, "NOM should be 0 for invalid class object"
    assert "Invalid class object provided" in caplog.text


# Test calculate_nopm with invalid class
def test_calculate_nopm_invalid_class(caplog):
    invalid_class = "not a class object"
    nopm = calculate_nopm(invalid_class)
    assert nopm == 0, "NOPM should be 0 for invalid class object"
    assert "Invalid class object provided" in caplog.text
