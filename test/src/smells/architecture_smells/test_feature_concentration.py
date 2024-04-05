import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.feature_concentration import FeatureConcentrationDetector

@pytest.fixture
def detector():
    return FeatureConcentrationDetector()

def test_detect_feature_concentration_below_threshold(detector):
    mock_module = MagicMock()
    mock_module.classes = [MagicMock(external_dependencies=[])]
    mock_dependency_graph = MagicMock()
    mock_dependency_graph.weakly_connected_components.return_value = []
    detector._build_dependency_graph = MagicMock(return_value=mock_dependency_graph)

    smells = detector._detect_smells({"test_package": [mock_module]}, {})
    assert len(smells) == 0

def test_detect_feature_concentration_above_threshold(detector):
    mock_module = MagicMock()
    mock_module.classes = [
        MagicMock(external_dependencies=["ClassB"]),
        MagicMock(external_dependencies=["ClassA"]),
        MagicMock(external_dependencies=["ClassC"]),
    ]
    mock_dependency_graph = MagicMock()
    mock_dependency_graph.weakly_connected_components.return_value = [[], []]
    detector._build_dependency_graph = MagicMock(return_value=mock_dependency_graph)
    smells = detector._detect_smells({"test_package": [mock_module]}, {})
    assert len(smells) == 1