from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import UnutilizedAbstractionDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return UnutilizedAbstractionDetector()


@pytest.fixture
def used_class():
    sm_class = create_autospec(SMClass)
    sm_class.name = "UsedClass"
    sm_class.start_line = 1
    sm_class.end_line = 50
    sm_class.is_used = True
    sm_class.super_classes = []
    return sm_class


@pytest.fixture
def unused_class():
    sm_class = create_autospec(SMClass)
    sm_class.name = "UnusedClass"
    sm_class.start_line = 1
    sm_class.end_line = 50
    sm_class.is_used = False
    sm_class.super_classes = []
    return sm_class


@pytest.fixture
def base_class():
    sm_class = create_autospec(SMClass)
    sm_class.name = "BaseClass"
    sm_class.start_line = 1
    sm_class.end_line = 50
    sm_class.is_used = False
    sm_class.super_classes = []
    return sm_class


@pytest.fixture
def derived_class(base_class):
    sm_class = create_autospec(SMClass)
    sm_class.name = "DerivedClass"
    sm_class.start_line = 1
    sm_class.end_line = 50
    sm_class.is_used = True
    sm_class.super_classes = [base_class.name]
    return sm_class


@pytest.fixture
def mock_module(used_class, unused_class, base_class, derived_class):
    module = create_autospec(SMModule)
    module.name = "TestModule"
    module.classes = [used_class, unused_class, base_class, derived_class]
    return module


def test_no_unutilized_abstraction(detector, mock_module, used_class):
    smells = detector._detect_smells(mock_module, {})
    assert not any(smell['entity_name'] == used_class.name for smell in smells), \
        "No unutilized abstraction should be detected for a used class."


def test_detect_unutilized_abstraction(detector, mock_module, unused_class):
    smells = detector._detect_smells(mock_module, {})
    assert any(smell['entity_name'] == unused_class.name for smell in smells), \
        "Should detect unutilized abstraction for an unused class."


def test_base_class_not_detected_as_unutilized(detector, mock_module, base_class):
    smells = detector._detect_smells(mock_module, {})
    assert not any(smell['entity_name'] == base_class.name for smell in smells), \
        "Should not detect a base class as unutilized abstraction if it has derived classes."


def test_error_handling(detector, caplog):
    faulty_module = create_autospec(SMModule)

    def raise_exception():
        raise Exception("Module Exception")

    faulty_module.classes = property(raise_exception)
    faulty_module.name = "FaultyModule"  # Ensure the name attribute is set for logging
    detector._detect_smells(faulty_module, {})
    assert "Error detecting unutilized abstractions" in caplog.text, "Should log an error for exceptions in module check."
