import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.cyclic_dependency import CyclicDependencyDetector

# Mocked classes for testing
class MockSMClass:
    def __init__(self, name, dependencies=None):
        self.name = name
        self.dependencies = dependencies or []

@pytest.fixture
def detector():
    return CyclicDependencyDetector()

#Test for no cyclic dependencies
def test_detect_no_cyclic_dependencies(detector):
    mock_module = MagicMock()
    mock_module.classes = [
        MockSMClass("A.py", dependencies=["B.py"]),
        MockSMClass("B.py"),
        MockSMClass("C.py", dependencies=["D.py"]),
        MockSMClass("D.py")
    ]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0

#Test for cyclic dependency
def test_detect_cyclic_dependencies(detector):
    mock_module = MagicMock()
    mock_module.classes = [
        MockSMClass("A.py", dependencies=["B.py"]),
        MockSMClass("B.py", dependencies=["C.py"]),
        MockSMClass("C.py", dependencies=["A.py"])
    ]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1
    assert smells[0].name == "Cyclic Dependency"