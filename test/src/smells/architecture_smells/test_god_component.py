import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.god_component import GodComponentDetector

@pytest.fixture
def detector():
    return GodComponentDetector()

# Test a module with a number of classes and functions below the thresholds
def test_detect_god_component_below_threshold(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.classes = [MagicMock(name=f"Class_{i}") for i in range(4)]  # Number of classes below threshold
    mock_module.functions = [
        MagicMock(start_line=1, end_line=10)  # LOC below threshold
    ]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 0

# Test a module with LOC exceeding the threshold
def test_detect_god_component_above_loc_threshold(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.classes = [MagicMock(name=f"Class_{i}") for i in range(5)]
    mock_module.functions = [
        MagicMock(start_line=1, end_line=210)
    ]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1
    assert "LOC" in smells[0]["details"]

# Test a module with the number of classes exceeding the threshold
def test_detect_god_component_above_num_classes_threshold(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.classes = [MagicMock(name=f"Class_{i}") for i in range(6)] 
    mock_module.functions = [
        MagicMock(start_line=1, end_line=10) for _ in range(199)
    ]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1
    assert "classes" in smells[0]["details"]

# Test a module with both LOC and number of classes exceeding the thresholds
def test_detect_god_component_above_both_thresholds(detector):
    mock_module = MagicMock()
    mock_module.name = "test_module"
    mock_module.classes = [MagicMock(name=f"Class_{i}") for i in range(6)]
    mock_module.functions = [
        MagicMock(start_line=1, end_line=10) for _ in range(201)
    ]
    smells = detector.detect(mock_module, {})
    assert len(smells) == 1
    assert "LOC" in smells[0]["details"]
    assert "classes" in smells[0]["details"]