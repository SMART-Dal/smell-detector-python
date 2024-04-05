import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.dense_structure import DenseStructureDetector

@pytest.fixture
def detector():
    return DenseStructureDetector()

def test_detect_dense_structure_below_threshold(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.components = [MagicMock(dependencies=[MagicMock()]) for _ in range(9)]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0

def test_detect_dense_structure_above_threshold_no_structure(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.components = [MagicMock(dependencies=[MagicMock()]) for _ in range(11)]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0

def test_detect_dense_structure_above_threshold_with_structure(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.components = [MagicMock(dependencies=[MagicMock()]) for _ in range(11)]
    mock_module.components[0].dependencies = [MagicMock() for _ in range(5)]
    mock_module.components[1].dependencies = [MagicMock() for _ in range(3)]
    mock_module.components[2].dependencies = [MagicMock() for _ in range(7)]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1
    assert smells[0]["entity_name"] == "Dense Structure"