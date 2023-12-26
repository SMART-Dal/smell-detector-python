import logging
from unittest.mock import create_autospec, MagicMock, PropertyMock

import pytest

from src.smells.design_smells import UnnecessaryAbstractionDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule


# Fixture for the detector
@pytest.fixture
def detector():
    return UnnecessaryAbstractionDetector()


# Fixture for a minimal method
@pytest.fixture
def minimal_method():
    method = create_autospec(SMMethod, instance=True)
    method.name = "MinimalMethod"
    method.loc = 10  # Lines of code less than the min_method_loc threshold
    return method


# Fixture for a substantial method
@pytest.fixture
def substantial_method():
    method = create_autospec(SMMethod, instance=True)
    method.name = "SubstantialMethod"
    method.loc = 50  # Lines of code more than the min_method_loc threshold
    return method


# Fixture for an unnecessary class (minimal methods and fields)
@pytest.fixture
def unnecessary_class(minimal_method):
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "UnnecessaryClass"
    sm_class.start_line = 1
    sm_class.end_line = 50
    sm_class.class_fields = {}
    sm_class.instance_fields = {}
    sm_class.methods = [minimal_method]
    return sm_class


# Fixture for a substantial class (more methods or fields)
@pytest.fixture
def substantial_class(substantial_method):
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "SubstantialClass"
    sm_class.start_line = 1
    sm_class.end_line = 100
    sm_class.class_fields = {'field1': 'public'}
    sm_class.instance_fields = {}
    sm_class.methods = [substantial_method]
    return sm_class


# Fixture for a mock module with an unnecessary class only
@pytest.fixture
def mock_module_with_unnecessary_class(unnecessary_class):
    module = MagicMock(spec=SMModule)
    module.name = "UnnecessaryTestModule"
    module.classes = [unnecessary_class]
    return module


# Fixture for a mock module with a substantial class only
@pytest.fixture
def mock_module_with_substantial_class(substantial_class):
    module = MagicMock(spec=SMModule)
    module.name = "SubstantialTestModule"
    module.classes = [substantial_class]
    return module


# Test to detect unnecessary abstraction
def test_detects_unnecessary_abstraction(detector, mock_module_with_unnecessary_class):
    smells = detector._detect_smells(mock_module_with_unnecessary_class,
                                     {'max_methods': 1, 'max_fields': 1, 'min_method_loc': 25})
    assert len(smells) == 1, "Should detect one unnecessary abstraction in the provided class."


# Test to ignore substantial classes
def test_ignores_substantial_classes(detector, mock_module_with_substantial_class):
    smells = detector._detect_smells(mock_module_with_substantial_class,
                                     {'max_methods': 1, 'max_fields': 1, 'min_method_loc': 25})
    assert len(smells) == 0, "Should not detect unnecessary abstraction in a substantial class."


def test_error_handling_in_class_check(detector, caplog, unnecessary_class, mock_module_with_unnecessary_class):
    def raise_exception():
        raise Exception("Test Exception")
    unnecessary_class.methods = property(raise_exception)
    detector._detect_smells(mock_module_with_unnecessary_class, {})
    assert "Error in _is_unnecessary_abstraction" in caplog.text, "Should log an error for exceptions in class check."


def test_error_handling_in_module_check(detector, caplog):
    faulty_module = MagicMock(spec=SMModule)

    def raise_exception():
        raise Exception("Module Exception")
    faulty_module.classes = property(raise_exception)
    faulty_module.name = "FaultyModule"  # Ensure the name attribute is set for logging
    detector._detect_smells(faulty_module, {})
    assert "Error detecting Unnecessary Abstraction smells in module" in caplog.text, "Should log an error for exceptions in module check."


