import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.scattered_functionality import ScatteredFunctionalityDetector

@pytest.fixture
def detector():
    return ScatteredFunctionalityDetector()

# Test case for no scattered functionality detected
def test_detect_no_scattered_functionality(detector):
    mock_method = MagicMock()
    mock_method.used_modules = ["PackageA.ModuleA.ClassA", "PackageA.ModuleA.ClassB"]
    package_details = {"PackageA": [MagicMock(classes=[MagicMock(methods=[mock_method])])]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 0

# Test case for scattered functionality detected in one method
def test_detect_scattered_functionality_in_one_method(detector):
    mock_method = MagicMock()
    mock_method.used_modules = ["PackageA.ModuleA.ClassA", "PackageB.ModuleB.ClassB"]
    package_details = {"PackageA": [MagicMock(classes=[MagicMock(methods=[mock_method])])]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 1
    assert smells[0]['entity_name'] == "Scattered Functionality"

# Test case for scattered functionality detected in multiple methods
def test_detect_scattered_functionality_in_multiple_methods(detector):
    mock_method1 = MagicMock()
    mock_method1.used_modules = ["PackageA.ModuleA.ClassA", "PackageB.ModuleB.ClassB"]
    mock_method2 = MagicMock()
    mock_method2.used_modules = ["PackageC.ModuleC.ClassC", "PackageD.ModuleD.ClassD"]
    package_details = {"PackageA": [MagicMock(classes=[MagicMock(methods=[mock_method1])])],
                       "PackageB": [MagicMock(classes=[MagicMock(methods=[mock_method2])])]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 2
    assert smells[0]['entity_name'] == "Scattered Functionality"
    assert smells[1]['entity_name'] == "Scattered Functionality"