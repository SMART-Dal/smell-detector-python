import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.cyclic_dependency import CyclicDependencyDetector

class MockSMClass:
    def __init__(self, name, external_dependencies=None):
        self.name = name
        self.external_dependencies = external_dependencies or []

class MockPackage:
    def __init__(self, name, modules):
        self.name = name
        self.modules = modules

@pytest.fixture
def detector():
    return CyclicDependencyDetector()

def test_detect_no_cyclic_dependencies(detector):
    mock_module_a = MagicMock()
    mock_module_a.classes = [
        MockSMClass("A.py"),
        MockSMClass("B.py"),
    ]
    mock_module_b = MagicMock()
    mock_module_b.classes = [
        MockSMClass("C.py"),
        MockSMClass("D.py"),
    ]
    mock_package = MockPackage("Package", [mock_module_a, mock_module_b])

    mock_module_a.classes[0].external_dependencies = ["D.py"]
    mock_module_b.classes[0].external_dependencies = ["X.py"]

    smells = detector.detect(mock_package, {})
    assert len(smells) == 0

def test_detect_cyclic_dependencies(detector):
    mock_module_a = MagicMock()
    mock_module_a.classes = [
        MockSMClass("A.py", external_dependencies=["B.py"]),
        MockSMClass("B.py", external_dependencies=["C.py"]),
        MockSMClass("C.py", external_dependencies=["A.py"])
    ]
    mock_package = MockPackage("Package", [mock_module_a])

    smells = detector.detect(mock_package, {})
    assert len(smells) == 1