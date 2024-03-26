import logging
import pytest
from unittest.mock import MagicMock

from src.smells.architecture_smells.ambiguous_interface import AmbiguousInterfaceDetector

public_method_1 = MagicMock(name="public_method")
public_method_1.access_modifier = "public"
public_method_1.name = "method_1"
protected_method = MagicMock(name="protected_method")
protected_method.access_modifier = "protected"
protected_method.name = "method_2"
private_method = MagicMock(name="private_method")
private_method.access_modifier = "private"
private_method.name = "method_3"
public_method_2 = MagicMock(name="public_method_2")
public_method_2.access_modifier = "public"
public_method_2.name = "method_4"


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.name = "test_module"
    module.functions = [public_method_1, protected_method, private_method]
    return module

@pytest.fixture
def detector():
    return AmbiguousInterfaceDetector()

# Test case for module with one public methods
def test_single_entry_point_true(detector, mock_module):
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1

# Test case for module with multiple public methods
def test_multiple_entry_points_false(detector, mock_module):
    mock_module.functions.append(public_method_2)
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0

 # Test case for module with no public methods
def test_no_public_entry_points_false(detector, mock_module):
    mock_module.functions.remove(public_method_1)
    print(mock_module.functions)
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0