import logging
from unittest.mock import MagicMock
import pytest
from src.smells.architecture_smells.unstable_dependency import UnstableDependencyDetector

@pytest.fixture
def detector():
    return UnstableDependencyDetector()

def test_detect_unstable_dependency_above_threshold(detector):
    package_a_module = MagicMock()
    package_a_module.name = "ModuleA"
    
    package_b_module = MagicMock()
    package_b_module.name = "ModuleB"

    package_c_module = MagicMock()
    package_c_module.name = "ModuleC"
    
    package_x_module = MagicMock()
    package_x_module.name = "ModuleX"

    package_details = {
        "PackageA": [package_a_module],
        "PackageB": [package_b_module],
        "PackageC": [package_c_module],
        "PackageX": [package_x_module]
    }

    package_a_module.dependency_graph.get_dependencies.side_effect = lambda x: ["ModuleB", "ModuleC"]
    package_b_module.dependency_graph.get_dependencies.side_effect = lambda x: ["ModuleA"]
    package_x_module.dependency_graph.get_dependencies.side_effect = lambda x: ["ModuleB"]

    config = {'instability_threshold': 0.5}
    smells = detector.detect(package_details, config)
    assert len(smells) == 1
    assert smells[0]['entity_name'] == "Unstable Dependency"


def test_detect_no_unstable_dependency_below_threshold(detector):
    package_a_module = MagicMock()
    package_a_module.name = "ModuleA"
    
    package_b_module = MagicMock()
    package_b_module.name = "ModuleB"

    package_details = {
        "PackageA": [package_a_module],
        "PackageB": [package_b_module],
    }

    package_a_module.dependency_graph.get_dependencies.side_effect = lambda x: ["ModuleB"]
    package_b_module.dependency_graph.get_dependencies.side_effect = lambda x: []

    config = {'instability_threshold': 0.5}
    smells = detector.detect(package_details, config)
    assert len(smells) == 0