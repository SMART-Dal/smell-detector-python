import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.cyclic_dependency import CyclicDependencyDetector

@pytest.fixture
def detector():
    return CyclicDependencyDetector()

# Test case for no cyclic dependencies
def test_no_cyclic_dependencies(detector):
    package_details = {
        "package1": [MockModule("module1")],
        "package2": [MockModule("module2")],
        "package3": [MockModule("module3")]
    }
    smells = detector.detect(package_details, {})
    assert len(smells) == 0

# Test case for single cyclic dependency
def test_single_cyclic_dependency(detector):
    module1 = MockModule("module1")
    module2 = MockModule("module2")
    module3 = MockModule("module3")

    module1.external_dependencies = ["module2"]
    module2.external_dependencies = ["module3"]
    module3.external_dependencies = ["module1"]

    package_details = {
        "package1": [module1],
        "package2": [module2],
        "package3": [module3]
    }

    smells = detector.detect(package_details, {})
    assert len(smells) == 0

class MockModule:
    def __init__(self, name):
        self.name = name
        self.external_dependencies = []
        self.classes = []

    def add_class(self, class_name):
        self.classes.append(class_name)