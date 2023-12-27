import logging
from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import BrokenHierarchyDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_parameter import SMParameter
from src.sourcemodel.sm_project import SMProject


@pytest.fixture
def detector():
    return BrokenHierarchyDetector()


@pytest.fixture
def subclass():
    subclass = create_autospec(SMClass, instance=True)
    subclass.name = "SubClass"
    subclass.start_line = 1
    subclass.super_classes = ["SuperClass"]
    return subclass


@pytest.fixture
def superclass():
    superclass = create_autospec(SMClass, instance=True)
    superclass.name = "SuperClass"
    superclass.start_line = 1
    return superclass


@pytest.fixture
def method():
    method = create_autospec(SMMethod, instance=True)
    method.name = "sample_method"
    method.return_type = "int"
    method.parameters = [create_autospec(SMParameter, instance=True, name="param1", param_type="int")]
    return method


@pytest.fixture
def mock_module(subclass, superclass):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.project = create_autospec(SMProject, instance=True)
    module.classes = [subclass]
    module.project.find_class.return_value = superclass
    return module


# Test cases
def test_detects_broken_hierarchy(detector, mock_module, subclass, superclass, method):
    subclass.methods = [method]
    superclass.methods = [method]

    detector.is_behavior_consistent = lambda sub_method, super_method: False  # Mocking behavior as inconsistent

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect one broken hierarchy smell."


def test_no_broken_hierarchy_detected(detector, mock_module, subclass, superclass, method):
    subclass.methods = [method]
    superclass.methods = [method]

    detector.is_behavior_consistent = lambda sub_method, super_method: True  # Mocking behavior as consistent

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect broken hierarchy smell when methods are consistent."


def test_superclass_without_methods(detector, mock_module, subclass, superclass):
    subclass.methods = [create_autospec(SMMethod, instance=True)]
    superclass.methods = []

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect broken hierarchy smell when superclass has no methods."


def test_method_signature_mismatch(detector, mock_module, subclass, superclass, method):
    method.parameters = [create_autospec(SMParameter, instance=True, name="param1", param_type="int")]
    super_method = create_autospec(SMMethod, instance=True)
    super_method.name = "sample_method"
    super_method.return_type = "int"
    super_method.parameters = [
        create_autospec(SMParameter, instance=True, name="param1", param_type="string")]  # Different type

    subclass.methods = [method]
    superclass.methods = [super_method]

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect broken hierarchy smell when method signatures are mismatched."


def test_subclass_without_superclass(detector, mock_module, subclass):
    subclass.super_classes = []
    subclass.methods = [create_autospec(SMMethod, instance=True)]

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect broken hierarchy smell for classes without a superclass."


def test_error_handling(detector, mock_module, subclass, superclass, method, caplog):
    mock_module.classes = [subclass]
    mock_module.project.find_class.side_effect = Exception("Unexpected Error")

    with caplog.at_level(logging.ERROR):
        smells = detector._detect_smells(mock_module, {})
        assert "Error detecting Broken Hierarchy smells" in caplog.text, "Should log an error for exceptions during smell detection."
        assert len(smells) == 0, "Should not detect any smells when an error occurs."

