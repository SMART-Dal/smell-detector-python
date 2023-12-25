import logging
import pytest
from unittest.mock import MagicMock, create_autospec
from src.smells.implementation_smells import ComplexMethodDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction


# Create mock instances for SMClass and SMFunction
@pytest.fixture
def simple_method():
    method = create_autospec(SMFunction, instance=True)
    method.name = "SimpleMethod"
    method.complexity = 5
    method.start_line = 10
    method.end_line = 20
    return method


@pytest.fixture
def complex_method():
    method = create_autospec(SMFunction, instance=True)
    method.name = "ComplexMethod"
    method.complexity = 15
    method.start_line = 30
    method.end_line = 50
    return method


@pytest.fixture
def mock_sm_class(complex_method):
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.methods = [complex_method]
    return sm_class


@pytest.fixture
def mock_module(simple_method, mock_sm_class):
    module = MagicMock()
    module.name = "TestModule"
    # Assign the mock functions and classes to the module
    module.functions = [simple_method]
    module.classes = [mock_sm_class]
    return module


@pytest.fixture
def detector():
    return ComplexMethodDetector()


# Test when no methods exceed the complexity threshold
def test_no_complex_methods(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 20})
    assert len(smells) == 0, "Should not detect complex methods below the threshold."


# Test when a method exceeds the complexity threshold
def test_complex_method_detection(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 10})
    assert len(smells) == 1, "Should detect a single complex method."
    assert smells[0]['entity_name'] == "ComplexMethod", "Should correctly identify the complex method."


# Test respecting the configuration threshold
def test_configuration_respect(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 5})
    assert len(smells) == 1, "Should detect smells when the threshold is lower than the method complexities."


# Test the structure of the smell information
def test_smell_structure(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 10})  # Will detect the complex method
    for smell in smells:
        assert 'module' in smell, "The smell should have a 'module' field."
        assert 'type' in smell, "The smell should have a 'type' field."
        assert 'entity_name' in smell, "The smell should have an 'entity_name' field."
        assert 'location' in smell, "The smell should have a 'location' field."
        assert 'details' in smell, "The smell should have a 'details' field."
