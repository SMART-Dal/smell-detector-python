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
def mock_package(mock_module):
    package = MagicMock()
    package.name = "test_package"
    package.modules = [mock_module]
    return package

@pytest.fixture
def detector():
    return AmbiguousInterfaceDetector()

# Test case for package with one public method
def test_single_entry_point_true(detector, mock_package):
    smells = detector.detect(mock_package, {})
    assert len(smells) == 1

# Test case for package with multiple public methods
def test_multiple_entry_points_in_multi_module(detector, mock_package):
    mock_module = MagicMock()
    mock_module.name = "test_module_2"
    mock_module.functions = [public_method_1, protected_method, private_method, public_method_2]
    mock_package.modules.append(mock_module)
    smells = detector.detect(mock_package, {})
    assert len(smells) == 1

# Test case for package with no public methods
def test_no_public_entry_points_false(detector, mock_package):
    for mock_module in mock_package.modules:
        mock_module.functions.remove(public_method_1)
    smells = detector.detect(mock_package, {})
    assert len(smells) == 0