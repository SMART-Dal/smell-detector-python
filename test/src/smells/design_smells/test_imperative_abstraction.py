from unittest.mock import create_autospec, MagicMock

import pytest

from src.smells.design_smells import ImperativeAbstractionDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return ImperativeAbstractionDetector()


@pytest.fixture
def simple_method():
    method = create_autospec(SMMethod)
    method.name = "simple_method"
    method.access_modifier = 'public'
    method.loc = 10
    return method


@pytest.fixture
def large_method():
    large_method = create_autospec(SMMethod)
    large_method.name = "large_method"
    large_method.access_modifier = 'public'
    large_method.loc = 100
    return large_method


# Fixture for a simple class with one small public method
@pytest.fixture
def simple_class(simple_method):
    sm_class = create_autospec(SMClass)
    sm_class.name = "SimpleClass"
    sm_class.start_line = 1
    sm_class.end_line = 10
    sm_class.class_fields = {'field1': 'public'}
    sm_class.instance_fields = {}
    sm_class.methods = [simple_method]
    return sm_class


# Fixture for a class that would be considered an Imperative Abstraction
@pytest.fixture
def imperative_class(large_method):
    sm_class = create_autospec(SMClass)
    sm_class.name = "ImperativeClass"
    sm_class.start_line = 1
    sm_class.end_line = 100
    sm_class.class_fields = {}
    sm_class.instance_fields = {}
    sm_class.methods = [large_method]
    return sm_class


# Fixture for a mock module with a simple class only
@pytest.fixture
def mock_module_with_simple_class(simple_class):
    module = MagicMock(spec=SMModule)
    module.name = "SimpleTestModule"
    module.classes = [simple_class]
    return module


# Fixture for a mock module with an imperative class only
@pytest.fixture
def mock_module_with_imperative_class(imperative_class):
    module = MagicMock(spec=SMModule)
    module.name = "ImperativeTestModule"
    module.classes = [imperative_class]
    return module


def test_no_imperative_abstraction(detector, mock_module_with_simple_class):
    smells = detector._detect_smells(mock_module_with_simple_class, {})
    assert len(smells) == 0, "No imperative abstraction should be detected in a simple class."


def test_detect_imperative_abstraction(detector, mock_module_with_imperative_class):
    smells = detector._detect_smells(mock_module_with_imperative_class, {})
    assert len(smells) == 1, "Should detect one imperative abstraction in the provided class."


def test_error_handling_in_class_check(detector, mock_module_with_simple_class, simple_class, caplog):
    def raise_exception():
        raise Exception("Test Exception")

    # Assign this function to the `loc` attribute of the method
    simple_class.methods[0].loc = property(raise_exception)
    detector._detect_smells(mock_module_with_simple_class, {})
    assert "Error checking Imperative Abstraction" in caplog.text, "Should log an error for exceptions in class check."


def test_error_handling_in_module_check(detector, caplog):
    faulty_module = MagicMock(spec=SMModule)

    # Define a property that raises an exception when accessed
    def raise_exception():
        raise Exception("Module Exception")
    faulty_module.classes = property(raise_exception)
    faulty_module.name = "FaultyModule"  # Ensure the name attribute is set for logging
    detector._detect_smells(faulty_module, {})
    assert "Error detecting Imperative Abstraction smells in module" in caplog.text, "Should log an error for exceptions in module check."
