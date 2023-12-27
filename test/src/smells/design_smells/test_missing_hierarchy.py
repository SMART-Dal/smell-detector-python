import ast
import logging
from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import MissingHierarchyDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule


# Fixture for the detector
@pytest.fixture
def detector():
    return MissingHierarchyDetector()


@pytest.fixture
def simple_method():
    method = create_autospec(SMMethod, instance=True)
    method.name = "simple_method"
    method.start_line = 1
    # Creating an AST node with a simple if-else structure
    method.ast_node = ast.parse("""
if condition:
    do_something()
else:
    do_something_else()
    """).body[0]
    return method


@pytest.fixture
def complex_method():
    method = create_autospec(SMMethod, instance=True)
    method.name = "complex_method"
    method.start_line = 1
    # Creating an AST node with multiple branches
    method.ast_node = ast.parse("""
if condition1:
    do_something()
elif condition2:
    do_something_else()
elif condition3:
    do_another_thing()
else:
    do_default()
    """).body[0]
    return method


# Fixture for a mock module
@pytest.fixture
def mock_module(simple_method, complex_method):
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "TestClass"
    sm_class.methods = [simple_method, complex_method]
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [sm_class]
    return module


def test_detects_missing_hierarchy(detector, mock_module, complex_method):
    smells = detector._detect_smells(mock_module, {'max_branches': 2})
    assert len(smells) == 1, "Should detect one missing hierarchy smell."
    assert complex_method.name in smells[0]['details'], "The smell should be detected for the complex method."


def test_ignores_simple_structure(detector, mock_module, simple_method):
    smells = detector._detect_smells(mock_module, {'max_branches': 2})
    assert not any(simple_method.name in smell['details'] for smell in
                   smells), "Should not detect missing hierarchy smell for simple method."


def test_error_handling(detector, mock_module, caplog):
    def raise_exception():
        raise Exception("Test Exception")
    mock_module.classes = raise_exception
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {})
        assert "Error detecting Missing Hierarchy smells in module TestModule" in caplog.text, "Should log an error for exceptions during smell detection."
