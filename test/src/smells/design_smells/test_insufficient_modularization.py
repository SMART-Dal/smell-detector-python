import logging
from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import InsufficientModularizationDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return InsufficientModularizationDetector()


@pytest.fixture
def sm_class():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "SampleClass"
    sm_class.start_line = 1
    sm_class.metrics = {'nopm': 5, 'wmc': 10, 'nom': 15, 'loc': 200}
    return sm_class


@pytest.fixture
def another_sm_class():
    another_class = create_autospec(SMClass, instance=True)
    another_class.name = "AnotherClass"
    another_class.start_line = 10
    another_class.metrics = {'nopm': 12, 'wmc': 16, 'nom': 25, 'loc': 350}
    return another_class


@pytest.fixture
def mock_module(sm_class):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [sm_class]
    return module


def test_no_smell_with_acceptable_metrics(detector, mock_module):
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect any smells for a class with acceptable metrics."


def test_smell_detected_for_excessive_metrics(detector, mock_module, sm_class):
    # Adjust metrics to exceed the thresholds
    sm_class.metrics.update({'nopm': 20, 'wmc': 30, 'nom': 40, 'loc': 500})

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect a smell for a class with excessive metrics."
    assert sm_class.name in smells[0]['details'], "The smell detail should mention the class name."


def test_smell_detection_with_custom_config(detector, mock_module, sm_class):
    custom_config = {'max_nopm': 5, 'max_wmc': 5, 'max_nom': 5, 'max_loc': 100}
    sm_class.metrics.update({'nopm': 6})

    smells = detector._detect_smells(mock_module, custom_config)
    assert len(smells) == 1, "Should detect a smell with custom configuration when thresholds are exceeded."


def test_metrics_on_threshold(detector, mock_module, sm_class):
    sm_class.metrics = {'nopm': 10, 'wmc': 15, 'nom': 20, 'loc': 300}  # Exactly on the default thresholds
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect smells for metrics exactly on thresholds."


def test_no_smell_for_classes_without_metrics(detector, mock_module, sm_class):
    sm_class.metrics = {}  # Empty metrics
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect smells for classes without metrics."


def test_multiple_classes_in_module(detector, mock_module, sm_class, another_sm_class):
    mock_module.classes = [sm_class, another_sm_class]
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect smells for only the class with excessive metrics."


def test_error_handling_in_class_check(detector, mock_module, sm_class, caplog):
    sm_class.metrics = Exception("Unexpected Error")

    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {})
        assert "Error checking Insufficient Modularization" in caplog.text, "Should log an error for exceptions in class check."


def test_error_handling_at_module_level(detector, caplog):
    faulty_module = create_autospec(SMModule, instance=True)
    faulty_module.name = "faulty_module"
    faulty_module.classes = Exception("Module level Exception")

    with caplog.at_level(logging.ERROR):
        detector._detect_smells(faulty_module, {})
        assert "Error detecting Insufficient Modularization smells" in caplog.text, \
            "Should log an error for exceptions at the module level."
