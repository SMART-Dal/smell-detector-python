import ast
import logging
from unittest.mock import create_autospec

import pytest

from src.smells.design_smells import DeficientEncapsulationDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return DeficientEncapsulationDetector()


@pytest.fixture
def class_with_public_field():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = 'TestClass'
    sm_class.start_line = 1
    sm_class.methods = []
    sm_class.class_fields = {'publicField': 'public'}
    sm_class.instance_fields = {}
    return sm_class


@pytest.fixture
def accessing_class():
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = 'AccessingClass'
    method = create_autospec(SMMethod, instance=True)
    method.ast_node = ast.parse("some_object.publicField").body[0]  # Simulating access to a public field
    sm_class.start_line = 1
    sm_class.methods = [method]
    sm_class.class_fields = {}
    sm_class.instance_fields = {}
    return sm_class


@pytest.fixture
def mock_module(class_with_public_field):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [class_with_public_field]
    return module


def test_public_field_not_accessed_by_other_classes(detector, mock_module, class_with_public_field):
    smells = detector._detect_smells(mock_module, {})
    assert len(
        smells) == 0, "No deficient encapsulation smell should be detected if a public field is not accessed by other classes."


def test_public_field_accessed_by_other_classes(detector, mock_module, class_with_public_field, accessing_class):
    mock_module.classes = [class_with_public_field, accessing_class]
    smells = detector._detect_smells(mock_module, {})
    assert len(
        smells) == 1, "Deficient encapsulation smell should be detected if a public field is accessed by other classes."


def test_protected_field_not_flagged(detector, mock_module, class_with_public_field):
    class_with_public_field.class_fields = {'_protectedField': 'protected'}
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Protected fields should not be flagged as deficiently encapsulated."


def test_multiple_public_fields(detector, mock_module, class_with_public_field, accessing_class):
    class_with_public_field.class_fields = {'publicField1': 'public', 'publicField2': 'public'}
    accessing_method = create_autospec(SMMethod, instance=True)
    accessing_method.ast_node = ast.parse("some_object.publicField1\nsome_object.publicField2").body[0]
    accessing_class.methods = [accessing_method]
    mock_module.classes = [class_with_public_field, accessing_class]
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) >= 1, "Should detect deficient encapsulation for at least one public field."


def test_private_field_not_flagged(detector, mock_module, class_with_public_field):
    class_with_public_field.class_fields = {'__privateField': 'private'}
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Private fields should not be flagged as deficiently encapsulated."


def test_no_fields_class(detector, mock_module, class_with_public_field):
    class_with_public_field.class_fields = {}
    class_with_public_field.instance_fields = {}
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Classes with no fields should not have deficient encapsulation smells."


def test_internal_class_usage(detector, mock_module, class_with_public_field):
    method = create_autospec(SMMethod, instance=True)
    method.ast_node = ast.parse("self.publicField").body[0]  # Simulating internal access to a public field
    class_with_public_field.methods = [method]
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Public fields used internally should not be flagged as deficiently encapsulated."


def test_inherited_public_field(detector, mock_module, class_with_public_field):
    subclass = create_autospec(SMClass, instance=True)
    subclass.name = 'SubClass'
    subclass.super_classes = ['TestClass']
    subclass.class_fields = {}
    subclass.instance_fields = {}
    mock_module.classes = [class_with_public_field, subclass]
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Inherited public fields should not automatically be flagged as deficiently encapsulated."


def test_error_handling(detector, mock_module, caplog):
    def raise_exception(*args, **kwargs):
        raise Exception("Test Exception")
    mock_module.classes = raise_exception
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {})
        assert "Error detecting Deficient Encapsulation smells" in caplog.text, \
            "Should log an error message when an exception occurs."
