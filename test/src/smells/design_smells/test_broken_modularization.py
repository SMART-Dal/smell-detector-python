import logging
from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import BrokenModularizationDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return BrokenModularizationDetector()


@pytest.fixture
def mock_module():
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    return module


@pytest.fixture
def sm_class_with_external_calls():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "SampleClass"
    sm_class.start_line = 1
    sm_class.methods = [
        create_autospec(SMMethod, instance=True, external_calls=["ExternalClass1.method", "ExternalClass2.method"])]
    return sm_class


@pytest.fixture
def sm_class_with_no_external_calls():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "IsolatedClass"
    sm_class.methods = [create_autospec(SMMethod, instance=True, external_calls=[])]
    return sm_class

@pytest.fixture
def py_class():
    mock_class = create_autospec(SMClass, instance=True)
    mock_class.name = "SampleClass"
    mock_class.methods = []  # You might want to populate this with mock methods as needed
    return mock_class


def test_broken_modularization_detected(detector, mock_module, sm_class_with_external_calls):
    mock_module.classes = [sm_class_with_external_calls]
    smells = detector._detect_smells(mock_module, {'x_references': 1})
    assert len(smells) == 1, "Should detect broken modularization for class with too many external references."


def test_no_broken_modularization_detected(detector, mock_module, sm_class_with_no_external_calls):
    mock_module.classes = [sm_class_with_no_external_calls]
    smells = detector._detect_smells(mock_module, {'x_references': 5})
    assert len(smells) == 0, "Should not detect broken modularization for class with acceptable external references."


def test_no_external_calls(detector, mock_module, sm_class_with_no_external_calls):
    sm_class_with_no_external_calls.methods = [create_autospec(SMMethod, instance=True)]
    mock_module.classes = [sm_class_with_no_external_calls]
    smells = detector._detect_smells(mock_module, {'x_references': 5})
    assert len(smells) == 0, "Should not detect broken modularization when there are no external calls."


def test_external_calls_below_threshold(detector, mock_module, sm_class_with_external_calls):
    sm_class_with_external_calls.methods = [create_autospec(SMMethod, instance=True, external_calls=["ExternalClass"] * 3)]
    mock_module.classes = [sm_class_with_external_calls]
    smells = detector._detect_smells(mock_module, {'x_references': 5})
    assert len(smells) == 0, "Should not detect broken modularization when external calls are below the threshold."


def test_error_handling(detector, mock_module, caplog):
    mock_module.classes = Exception("Test Exception")
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {})
        assert "Error detecting Broken Modularization smells" in caplog.text, "Should log an error message when an exception occurs."
