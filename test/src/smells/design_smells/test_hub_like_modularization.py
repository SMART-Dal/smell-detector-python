import logging
from unittest.mock import create_autospec, MagicMock

import pytest

from src.smells.design_smells import HubLikeModularizationDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return HubLikeModularizationDetector()


@pytest.fixture
def sm_class():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "TestClass"
    sm_class.start_line = 1
    return sm_class


@pytest.fixture
def another_sm_class():
    another_class = create_autospec(SMClass, instance=True)
    another_class.name = "AnotherTestClass"
    another_class.start_line = 10
    another_class.metrics = {'fan_in': 10, 'fan_out': 12}
    return another_class


@pytest.fixture
def mock_module(sm_class):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [sm_class]
    return module


def test_detects_hub_like_modularization(detector, mock_module, sm_class):
    sm_class.metrics = {'fan_in': 6, 'fan_out': 7}  # Values exceeding the default thresholds
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect a smell for class acting as a hub."


def test_ignores_non_hub_classes(detector, mock_module, sm_class):
    sm_class.metrics = {'fan_in': 2, 'fan_out': 3}  # Values below the default thresholds
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect a smell for non-hub classes."


def test_custom_thresholds(detector, mock_module, sm_class):
    sm_class.metrics = {'fan_in': 4, 'fan_out': 4}
    custom_config = {'max_fan_in': 3, 'max_fan_out': 3}  # Custom thresholds lower than the class's metrics
    smells = detector._detect_smells(mock_module, custom_config)
    assert len(smells) == 1, "Should detect a smell with custom thresholds."


def test_error_handling(detector, mock_module, sm_class, caplog):
    sm_class.metrics = Exception("Unexpected error")
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {})
        assert "Error detecting Hub-Like Modularization smells" in caplog.text, "Should log an error for exceptions."


def test_multiple_classes_in_module(detector, mock_module, sm_class, another_sm_class):
    mock_module.classes = [sm_class, another_sm_class]
    sm_class.metrics = {'fan_in': 1, 'fan_out': 1}  # Non-hub class
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect smells only for the class acting as a hub."


@pytest.mark.parametrize("fan_in,fan_out,expected", [
    (6, 4, 0),  # High fan-in, moderate fan-out
    (3, 7, 0),  # Moderate fan-in, high fan-out
    (0, 0, 0),  # No connections
    (6, 6, 1),  # Both high
])
def test_various_fan_in_out_combinations(detector, mock_module, sm_class, fan_in, fan_out, expected):
    sm_class.metrics = {'fan_in': fan_in, 'fan_out': fan_out}
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == expected, f"Expected {expected} smells for fan_in {fan_in} and fan_out {fan_out}."


def test_inbound_only_connections(detector, mock_module, sm_class):
    sm_class.metrics = {'fan_in': 8, 'fan_out': 0}  # Only inbound connections
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Classes with only inbound connections shouldn't be detected as hubs."


def test_outbound_only_connections(detector, mock_module, sm_class):
    sm_class.metrics = {'fan_in': 0, 'fan_out': 9}  # Only outbound connections
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Classes with only outbound connections shouldn't be detected as hubs."
