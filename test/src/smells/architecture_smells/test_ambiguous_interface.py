import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.ambiguous_interface import AmbiguousInterfaceDetector

# Mocking entities for testing
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
def mock_second_module():
    module = MagicMock()
    module.name = "test_module_2"
    module.functions = [public_method_1, public_method_2]
    return module

@pytest.fixture
def mock_third_module():
    module = MagicMock()
    module.name = "test_module_3"
    module.functions = [protected_method, private_method]
    return module

@pytest.fixture
def mock_second_package(mock_second_module):
    package = MagicMock()
    package.name = "test_package_2"
    package.modules = [mock_second_module]
    return package

@pytest.fixture
def detector():
    return AmbiguousInterfaceDetector()

# Test case for a package with a single entry point
def test_single_entry_point_true(detector, mock_module):
    package_details = {"test_package": [mock_module]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 1

# Test case for a package with no entry points
def test_no_entry_point_false(detector, mock_third_module):
    package_details = {"test_package3": [mock_third_module]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 0

# Test case for a package with multiple entry points
def test_multiple_entry_points_true(detector, mock_second_module):
    package_details = {"test_package_2": [mock_second_module]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 0