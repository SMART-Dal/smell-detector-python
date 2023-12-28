from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import MultifacetedAbstractionDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return MultifacetedAbstractionDetector()


@pytest.fixture
def simple_class():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "SimpleClass"
    sm_class.start_line = 1
    sm_class.end_line = 50
    sm_class.metrics = {'lcom4': 1.0}
    sm_class.methods = ['method1', 'method2']
    return sm_class


@pytest.fixture
def multifaceted_class():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "MultifacetedClass"
    sm_class.start_line = 1
    sm_class.end_line = 110
    sm_class.metrics = {'lcom4': 2.0}  # Greater than the default max_lcom of 1.5
    sm_class.methods = ['method1', 'method2', 'method3', 'method4']  # More than the min_methods of 3
    return sm_class


@pytest.fixture
def mock_module(simple_class, multifaceted_class):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [simple_class, multifaceted_class]
    return module


def test_no_multifaceted_abstraction(detector, mock_module, simple_class):
    smells = detector._detect_smells(mock_module, {})
    assert not any(smell['entity_name'] == simple_class.name for smell in smells), \
        "No multifaceted abstraction should be detected in a simple class."


def test_detect_multifaceted_abstraction(detector, mock_module, multifaceted_class):
    smells = detector._detect_smells(mock_module, {})
    assert any(smell['entity_name'] == multifaceted_class.name for smell in smells), \
        "Should detect multifaceted abstraction in the provided class."


def test_error_handling_in_class_check(detector, mock_module, multifaceted_class, caplog):
    def raise_exception():
        raise Exception("Test Exception")
    multifaceted_class.methods = property(raise_exception)
    detector._detect_smells(mock_module, {})
    assert "Error detecting Multifaceted" in caplog.text, "Should log an error for exceptions in class check."
